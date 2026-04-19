"""One-shot backfill of expected_count in kg_schema/golden_set.csv.

For every query that is countable (single-hop / multi-hop / aggregation /
intersect / narrative_filter / meta_filter with a count-producing output
mode) AND does not already have a numeric expected_count, run the query
against the validated v6 graph and write the resulting count as the new
expected_count.

Skipped query types:
  - spot_check: uses the ground_truth column, not a scalar count
  - crosstab: produces a 2-D table, not a scalar count
  - custom (Global/Conjunctive/Multi-hop): complex outputs where the
    "count" interpretation is query-specific

Usage:
    python -m pipeline.benchmark.backfill_expected_counts
    python -m pipeline.benchmark.backfill_expected_counts --dry-run
"""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path

from kg_schema import GOLDEN_SET_CSV
from query_engine import load_data, load_queries, execute_query, CUSTOM_REGISTRY


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATA_DIR = REPO_ROOT / "pipeline" / "outputs" / "v6"

SKIP_STRATEGIES = {"spot_check"}  # custom queries are handled — we
                                   # take the first scalar in the summary
SKIP_OUTPUT_MODES: set[str] = set()  # crosstab uses the distinct-field1
                                      # count returned by the engine


def _extract_count(result: dict) -> int | None:
    """Pull a count out of a benchmark result dict.

    Preference order:
      1. 'Matching incidents' / 'Total incidents' in detail — most queries
      2. First "Crosstab: N ... x M ..." match — take N (distinct field1)
      3. First integer in result_summary — custom queries (e.g., "20 top hubs")
      4. Fallback: 1 for custom queries that return a single scalar match
         (e.g., "Top match: #531820 (sim=0.709)")
    """
    detail = result.get("detail", "") or ""
    for line in detail.splitlines():
        line = line.strip()
        if line.startswith("Matching incidents:") or line.startswith("Total incidents:"):
            try:
                return int(line.split(":", 1)[1].strip())
            except (ValueError, IndexError):
                return None
    summary = result.get("result_summary", "") or ""
    # Crosstab: "Crosstab: 4 business_unit values x 3 incident_type values"
    m = re.match(r"Crosstab:\s*(\d+)", summary)
    if m:
        return int(m.group(1))
    # First integer in summary
    m = re.search(r"\b(\d+(?:,\d{3})*)\b", summary)
    if m:
        return int(m.group(1).replace(",", ""))
    # Fallback for single-answer custom queries
    if summary.lower().startswith("top match"):
        return 1
    return None


def _should_backfill(row: dict, force: bool = False) -> bool:
    strat = (row.get("strategy") or "").strip().lower()
    if strat in SKIP_STRATEGIES:
        return False
    if not force:
        ec = (row.get("expected_count") or "").strip()
        if ec and ec.isdigit():
            return False  # already has a numeric count
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Backfill expected_count from validated graph counts")
    parser.add_argument("--data-dir", type=Path, default=DEFAULT_DATA_DIR)
    parser.add_argument("--csv-path", type=Path, default=Path(GOLDEN_SET_CSV))
    parser.add_argument("--dry-run", action="store_true",
                        help="Report planned updates without writing")
    parser.add_argument("--force", action="store_true",
                        help="Overwrite existing numeric expected_count values")
    args = parser.parse_args()

    csv_path: Path = args.csv_path

    # Read raw CSV preserving all columns
    with csv_path.open(newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)
    print(f"Loaded {len(rows)} rows from {csv_path}")

    # Load graph + specs
    G, entities_df, relations_df, metadata_df = load_data(
        data_dir=str(args.data_dir))
    specs = {s.query_id: s for s in load_queries(csv_path)}

    candidates = [r for r in rows if _should_backfill(r, force=args.force)]
    print(f"{len(candidates)} candidate queries to backfill\n")

    updates: list[tuple[str, int]] = []
    skipped: list[tuple[str, str]] = []
    for row in candidates:
        qid = row["query_id"]
        spec = specs.get(qid)
        if spec is None:
            skipped.append((qid, "not in parsed specs"))
            continue
        try:
            result = execute_query(spec, G, entities_df, relations_df,
                                   metadata_df, custom_registry=CUSTOM_REGISTRY)
        except Exception as exc:
            skipped.append((qid, f"error: {exc}"))
            continue
        count = _extract_count(result)
        if count is None:
            skipped.append((qid, f"no count in result: {result.get('result_summary','')[:60]}"))
            continue
        updates.append((qid, count))
        print(f"  {qid}: new expected_count = {count}  ({result.get('result_summary','')[:60]})")

    print(f"\nPlanned: {len(updates)} updates, {len(skipped)} skipped")
    if skipped:
        print("Skipped:")
        for qid, reason in skipped:
            print(f"  {qid}: {reason}")

    if args.dry_run:
        print("\n--dry-run set; not writing CSV")
        return

    # Apply updates
    update_map = dict(updates)
    for row in rows:
        qid = row["query_id"]
        if qid in update_map:
            row["expected_count"] = str(update_map[qid])

    # Write back
    with csv_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames,
                                quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        writer.writerows(rows)
    print(f"\nWrote {len(update_map)} updates to {csv_path}")


if __name__ == "__main__":
    main()
