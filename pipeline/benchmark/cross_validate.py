"""Independent cross-validation of benchmark query output.

For a curated set of golden_set queries, compute three counts:
  - pandas_count:   computed directly from raw metadata_parsed.parquet
                    (narrative regex, metadata filters) — independent of
                    GLiNER / ER / the knowledge graph
  - graph_count:    from the benchmark engine running against entities
                    + relations parquets — our pipeline output
  - expected_count: hand-curated baseline in golden_set.csv

Agreement between pandas_count and graph_count is the strongest signal
that the pipeline preserves the raw signal in the source data.

Usage:
    python -m pipeline.benchmark.cross_validate
    python -m pipeline.benchmark.cross_validate \
        --data-dir pipeline/outputs \
        --report-path pipeline/benchmark/cross_validation_report.md
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from kg_schema import GOLDEN_SET_CSV
from query_engine import load_data, load_queries, execute_query, CUSTOM_REGISTRY


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATA_DIR = REPO_ROOT / "pipeline" / "outputs"
DEFAULT_REPORT = REPO_ROOT / "pipeline" / "benchmark" / "cross_validation_report.md"


# Tolerance buckets (mirror the graph benchmark's classification).
TOL_VALIDATED = 0.10   # within 10% = VALIDATED
TOL_CLOSE = 0.25       # within 25% = CLOSE
# beyond that = DRIFT


@dataclass
class CrossCheck:
    query_id: str
    name: str
    kind: str              # pandas strategy label
    pandas_count: int
    graph_count: int | None
    expected_count: int
    pd_vs_expected: str    # VALIDATED / CLOSE / DRIFT
    pd_vs_graph: str       # VALIDATED / CLOSE / DRIFT / -
    graph_vs_expected: str


# ── Pandas equivalents ─────────────────────────────────────────────────────
#
# Each entry is (query_id, kind, callable(metadata_df) -> int). The callable
# reproduces the query using raw metadata only — no graph, no GLiNER, no ER.
# Narrative regex is intentionally slightly permissive (case-insensitive,
# word-boundary where helpful) so it mirrors what a human would count.


def _narr_regex(df: pd.DataFrame, pattern: str) -> int:
    """Count incidents whose narrative matches the regex (case-insensitive)."""
    narr = df["narrative"].fillna("")
    mask = narr.str.contains(pattern, case=False, regex=True, na=False)
    return int(mask.sum())


def _narr_any(df: pd.DataFrame, keywords: list[str]) -> int:
    pattern = "|".join(re.escape(k) for k in keywords)
    return _narr_regex(df, pattern)


def _year(df: pd.DataFrame, year: int) -> pd.Series:
    # reported_date looks like "7/19/2023"; year is the last 4 chars of the tail
    def _yr(s):
        if not isinstance(s, str):
            return None
        parts = s.strip().split("/")
        if len(parts) == 3 and len(parts[-1]) == 4 and parts[-1].isdigit():
            return int(parts[-1])
        return None
    return df["reported_date"].apply(_yr) == year


def _country(df: pd.DataFrame, pattern: str) -> pd.Series:
    return df["loc_country"].fillna("").str.contains(pattern, case=False, regex=True, na=False)


def _wp(df: pd.DataFrame, pattern: str) -> pd.Series:
    return df["work_process"].fillna("").str.contains(pattern, case=False, regex=True, na=False)


def _itype(df: pd.DataFrame, pattern: str) -> pd.Series:
    return df["incident_type"].fillna("").str.contains(pattern, case=False, regex=True, na=False)


def _impact(df: pd.DataFrame, pattern: str) -> pd.Series:
    return df["impact_type"].fillna("").str.contains(pattern, case=False, regex=True, na=False)


def _case_cat(df: pd.DataFrame, pattern: str) -> pd.Series:
    return df["case_categorization"].fillna("").str.contains(pattern, case=False, regex=True, na=False)


def _narr_mask(df: pd.DataFrame, pattern: str) -> pd.Series:
    return df["narrative"].fillna("").str.contains(pattern, case=False, regex=True, na=False)


PANDAS_CHECKS: list[tuple[str, str, callable]] = [
    # Single-hop narrative / metadata equivalents
    ("SH-01", "narrative+year",
     lambda d: int((_narr_mask(d, r"fork\s*lift|forklift|\bflt\b") & _year(d, 2022)).sum())),
    ("SH-05", "meta_filter",
     lambda d: int(_wp(d, r"offshore|marine").sum())),
    ("SH-06", "meta_filter",
     lambda d: int(d["client"].fillna("").str.contains("shell offshore", case=False, na=False).sum())),
    ("SH-07", "narrative",
     lambda d: _narr_regex(d, r"\bladder")),
    ("SH-08", "narrative",
     lambda d: _narr_regex(d, r"grinder")),
    ("SH-09", "narrative",
     lambda d: _narr_regex(d, r"\bhose")),
    ("SH-10", "narrative",
     lambda d: _narr_regex(d, r"\bpump")),
    ("SH-11", "narrative",
     lambda d: _narr_regex(d, r"\brov\b")),
    ("SH-12", "narrative",
     lambda d: _narr_regex(d, r"excavator")),
    ("SH-13", "narrative",
     lambda d: _narr_regex(d, r"\bppe\b|helmet|gloves|safety glasses|goggles")),
    ("SH-14", "narrative",
     lambda d: _narr_regex(d, r"\bsling")),
    ("SH-15", "narrative",
     lambda d: _narr_regex(d, r"compressor")),
    ("SH-16", "narrative",
     lambda d: _narr_regex(d, r"winch")),
    ("SH-20", "narrative",
     lambda d: _narr_regex(d, r"\bweld")),
    ("SH-21", "narrative",
     lambda d: _narr_regex(d, r"\bpallet")),
    ("SH-22", "narrative",
     lambda d: _narr_regex(d, r"fire extinguisher|\bextinguisher")),
    ("SH-23", "narrative",
     lambda d: _narr_regex(d, r"\breel")),
    ("SH-24", "narrative",
     lambda d: _narr_regex(d, r"umbilical")),
    ("SH-29", "narrative",
     lambda d: _narr_regex(d, r"confined space")),
    ("SH-30", "narrative",
     lambda d: _narr_regex(d, r"hot work")),
    ("SH-31", "narrative",
     lambda d: _narr_regex(d, r"chemical")),
    ("SH-32", "narrative",
     lambda d: _narr_regex(d, r"electric")),
    ("SH-34", "narrative",
     lambda d: _narr_any(d, ["overboard", "man overboard"])),
    ("SH-35", "narrative",
     lambda d: _narr_regex(d, r"fatigue")),
    ("SH-36", "narrative",
     lambda d: _narr_any(d, ["h2s", "hydrogen sulfide", "hydrogen sulphide"])),
    ("SH-38", "narrative",
     lambda d: _narr_regex(d, r"pressure")),
    ("SH-39", "narrative",
     lambda d: _narr_any(d, ["permit to work", "ptw", "work permit"])),
    ("SH-40", "narrative",
     lambda d: _narr_regex(d, r"struck by")),
    # Aggregation queries — count the filtered incident set
    ("AG-01", "narrative",
     lambda d: _narr_regex(d, r"dropped")),
    ("AG-02", "meta_filter",
     lambda d: int((d["severity_bin"] >= 4).sum())),
    ("AG-13", "meta_filter",
     lambda d: int(_impact(d, r"fire/explosion").sum())),
    # Multi-hop metadata intersections
    ("MH-17", "narrative+country",
     lambda d: int((_narr_mask(d, r"\brov\b") & _country(d, r"norway")).sum())),
    ("MH-18", "narrative+country",
     lambda d: int((_narr_mask(d, r"crane") & _country(d, r"brazil")).sum())),
    ("MH-19", "narrative+country",
     lambda d: int((_narr_mask(d, r"fork\s*lift|forklift|\bflt\b") & _country(d, r"\bu\.?k\.?\b|united kingdom")).sum())),
    ("MH-20", "narrative+country",
     lambda d: int((_narr_mask(d, r"scaffold") & _country(d, r"india")).sum())),
    ("MH-27", "narrative+year",
     lambda d: int((_narr_mask(d, r"crane") & _year(d, 2019)).sum())),
    ("MH-28", "narrative+year",
     lambda d: int((_narr_mask(d, r"fork\s*lift|forklift|\bflt\b") & _year(d, 2023)).sum())),
    ("MH-29", "narrative+year",
     lambda d: int((_narr_mask(d, r"scaffold") & _year(d, 2020)).sum())),
    ("MH-30", "narrative+year",
     lambda d: int((_narr_mask(d, r"\brov\b") & _year(d, 2017)).sum())),
    # Metadata-only filters (trivial, exact ground truth)
    ("SH-51", "meta_filter",
     lambda d: int(_year(d, 2024).sum())),
    ("SH-52", "meta_filter",
     lambda d: int((d["severity_bin"] >= 5).sum())),
    ("SH-53", "meta_filter",
     lambda d: int(_impact(d, r"occupational illness").sum())),
    ("SH-54", "meta_filter",
     lambda d: int(d["risk_color"].fillna("").str.lower().eq("red").sum())),
    ("SH-56", "meta_filter",
     lambda d: int(d["reported_date"].apply(
        lambda s: isinstance(s, str) and s.strip().endswith(tuple(str(y) for y in range(1900, 2016)))
     ).sum())),
    # ROOT_CAUSE_CATEGORY queries — map to metadata case_categorization
    ("AG-05", "case_cat",
     lambda d: int(_case_cat(d, r"fall|slip|trip").sum())),
    ("AG-10", "case_cat",
     lambda d: int(_case_cat(d, r"manual handling").sum())),
    ("IOGP-28", "case_cat",
     lambda d: int(_case_cat(d, r"motor vehicle").sum())),
    # Location queries — map to loc_site / loc_country fields
    ("SH-48", "loc_site",
     lambda d: int(d["loc_site"].fillna("").str.contains("sabetta", case=False, na=False).sum())),
    ("SH-49", "loc_site",
     lambda d: int(d["loc_site"].fillna("").str.contains("le trait", case=False, na=False).sum())),
    ("SH-57", "loc_country",
     lambda d: int(d["loc_country"].fillna("").str.contains("antarctica", case=False, na=False).sum())),
    # Organization queries — map to client field (GT may also include contractor mentions → CLOSE expected)
    ("SH-46", "client",
     lambda d: int(d["client"].fillna("").str.contains("petrobras", case=False, na=False).sum())),
    ("SH-47", "client",
     lambda d: int(d["client"].fillna("").str.contains("equinor|statoil", case=False, na=False).sum())),
    # Narrative-only queries
    ("SH-41", "narrative",
     lambda d: _narr_any(d, ["caught between", "caught in", "pinch point", "pinched"])),
    ("SH-42", "narrative",
     lambda d: _narr_regex(d, r"line of fire")),
    # Equipment / body_part / injury via narrative regex — graph is more
    # precise, so CLOSE rather than VALIDATED is acceptable here.
    ("SH-25", "narrative",
     lambda d: _narr_regex(d, r"left hand")),
    ("SH-26", "narrative",
     lambda d: _narr_regex(d, r"\bthumb")),
    ("SH-27", "narrative",
     lambda d: _narr_regex(d, r"contusion|bruise|bruising")),
    ("SH-28", "narrative",
     lambda d: _narr_regex(d, r"sprain|strain")),
    ("SH-50", "narrative",
     lambda d: _narr_regex(d, r"abrasion|scratch|scrape")),
    ("SH-55", "narrative",
     lambda d: _narr_regex(d, r"\brobot|\bdrone|\buav\b")),
    ("SH-58", "narrative",
     lambda d: _narr_regex(d, r"\btank\b")),
    ("AG-16", "narrative",
     lambda d: _narr_regex(d, r"\beye\b")),
    ("AG-19", "narrative",
     lambda d: _narr_regex(d, r"fracture")),
    ("AG-25", "narrative",
     lambda d: _narr_regex(d, r"contusion|bruise|bruising")),
    # Intersect queries with case_categorization + narrative + meta clauses
    ("MH-07", "entity+meta",
     lambda d: int((_narr_mask(d, r"scaffold") & _itype(d, r"near miss")).sum())),
    ("MH-24", "narrative+wp",
     lambda d: int((_narr_mask(d, r"fracture") & _wp(d, r"construction")).sum())),
    ("CJ-06", "case_cat+wp",
     lambda d: int((_case_cat(d, r"fall|slip|trip") & _wp(d, r"construction")).sum())),
    ("MH-02", "narrative+wp",
     lambda d: int((_narr_mask(d, r"\bfail") & _wp(d, r"maintenance")).sum())),
]


# ── Tolerance classification ───────────────────────────────────────────────

def _classify(actual: int, expected: int) -> str:
    if expected == 0:
        return "VALIDATED" if actual == 0 else "DRIFT"
    diff = abs(actual - expected) / expected
    if diff <= TOL_VALIDATED:
        return "VALIDATED"
    if diff <= TOL_CLOSE:
        return "CLOSE"
    return "DRIFT"


# ── Graph count extraction ────────────────────────────────────────────────

def _extract_incident_count(result: dict) -> int | None:
    """Pull the 'Matching incidents:' or 'Total incidents:' number out of the
    engine's detail block. Returns None if we can't find it.
    """
    detail = result.get("detail", "") or ""
    for line in detail.splitlines():
        line = line.strip()
        if line.startswith("Matching incidents:") or line.startswith("Total incidents:"):
            try:
                return int(line.split(":", 1)[1].strip())
            except (ValueError, IndexError):
                return None
    # fall back to the raw `count` field for count_incidents mode
    if result.get("result_summary", "").endswith("incidents"):
        try:
            return int(result["result_summary"].split()[0])
        except (ValueError, IndexError):
            return None
    return None


# ── Main ──────────────────────────────────────────────────────────────────

def run(data_dir: Path, report_path: Path) -> list[CrossCheck]:
    print(f"Loading data from {data_dir}...")
    G, entities_df, relations_df, metadata_df = load_data(data_dir=str(data_dir))
    specs = {s.query_id: s for s in load_queries(GOLDEN_SET_CSV)}

    results: list[CrossCheck] = []
    for qid, kind, fn in PANDAS_CHECKS:
        spec = specs.get(qid)
        if spec is None:
            print(f"  {qid}: not found in golden_set.csv, skipping")
            continue
        if spec.expected_count is None:
            print(f"  {qid}: no expected_count, skipping")
            continue

        pandas_count = fn(metadata_df)

        try:
            g_result = execute_query(
                spec, G, entities_df, relations_df, metadata_df,
                custom_registry=CUSTOM_REGISTRY,
            )
            graph_count = _extract_incident_count(g_result)
        except Exception as exc:
            print(f"  {qid}: graph query error: {exc}")
            graph_count = None

        pd_vs_exp = _classify(pandas_count, spec.expected_count)
        g_vs_exp = _classify(graph_count, spec.expected_count) if graph_count is not None else "-"
        if graph_count is not None:
            pd_vs_g = _classify(pandas_count, graph_count)
        else:
            pd_vs_g = "-"

        results.append(CrossCheck(
            query_id=qid,
            name=spec.name,
            kind=kind,
            pandas_count=pandas_count,
            graph_count=graph_count,
            expected_count=spec.expected_count,
            pd_vs_expected=pd_vs_exp,
            pd_vs_graph=pd_vs_g,
            graph_vs_expected=g_vs_exp,
        ))
        print(f"  {qid}: pd={pandas_count} graph={graph_count} exp={spec.expected_count} "
              f"| pd-vs-graph={pd_vs_g} | pd-vs-exp={pd_vs_exp} | g-vs-exp={g_vs_exp}")

    _write_report(results, report_path, data_dir)
    return results


def _summarise(label: str, values: list[str]) -> str:
    total = len(values)
    if total == 0:
        return f"{label}: 0 queries"
    v = values.count("VALIDATED")
    c = values.count("CLOSE")
    d = values.count("DRIFT")
    skip = values.count("-")
    return (f"{label}: {v}/{total} VALIDATED ({100*v/total:.0f}%), "
            f"{c} CLOSE, {d} DRIFT, {skip} skipped")


def _write_report(results: list[CrossCheck], path: Path, data_dir: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    pd_vs_g = [r.pd_vs_graph for r in results]
    pd_vs_e = [r.pd_vs_expected for r in results]
    g_vs_e = [r.graph_vs_expected for r in results]

    lines = [
        "# Cross-Validation Report — Independent Query Output Check",
        "",
        f"**Data dir:** `{data_dir}`",
        f"**Queries checked:** {len(results)}",
        "",
        "## Method",
        "",
        "For each query, three counts are computed independently:",
        "",
        "- `pandas_count` — from raw `metadata_parsed.parquet` via narrative "
        "regex or metadata filters. Does not touch GLiNER, ER, or the graph.",
        "- `graph_count` — from `entities.parquet` + `relations.parquet` via "
        "the benchmark engine. This is the pipeline output.",
        "- `expected_count` — hand-curated baseline in `golden_set.csv`.",
        "",
        "Agreement thresholds: **VALIDATED** within 10%, **CLOSE** within "
        "25%, otherwise **DRIFT**.",
        "",
        "The primary signal is **pandas vs graph**: the two share no code, "
        "so agreement is strong evidence the pipeline preserved the signal "
        "present in the raw narratives/metadata.",
        "",
        "## Summary",
        "",
        f"- {_summarise('pandas vs graph', pd_vs_g)}",
        f"- {_summarise('pandas vs expected', pd_vs_e)}",
        f"- {_summarise('graph vs expected', g_vs_e)}",
        "",
        "## Per-query results",
        "",
        "| ID | Kind | Pandas | Graph | Expected | pd↔graph | pd↔exp | graph↔exp | Query |",
        "|----|------|-------:|------:|---------:|:--------:|:------:|:---------:|-------|",
    ]
    for r in results:
        g = "—" if r.graph_count is None else f"{r.graph_count}"
        lines.append(
            f"| {r.query_id} | {r.kind} | {r.pandas_count} | {g} | "
            f"{r.expected_count} | {r.pd_vs_graph} | {r.pd_vs_expected} | "
            f"{r.graph_vs_expected} | {r.name[:70]} |"
        )
    lines.append("")
    lines.append("## Notes on method")
    lines.append("")
    lines.append(
        "- Narrative regex uses word boundaries where they help (e.g., "
        "`\\brov\\b` to avoid matching 'approval'). It's intentionally "
        "permissive — mirrors what a human reader would count — so CLOSE "
        "(not DRIFT) is the expected outcome when regex slightly "
        "over-counts compared to a semantic entity extractor."
    )
    lines.append(
        "- Queries like CJ-* that require L2 causal traversal are outside "
        "the scope of this cross-check — they're semantically impossible "
        "to express in pure pandas. Those are validated by Gate 3 (IAA + "
        "bipartite matching) instead."
    )
    lines.append(
        "- This report is additive to Gate 3 and to the 258-query benchmark "
        "harness. It specifically addresses the question: \"How do we know "
        "the count is right?\" by deriving the count a second, independent "
        "way."
    )

    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nReport written to {path}")


def main():
    parser = argparse.ArgumentParser(description="Independent benchmark cross-validation")
    parser.add_argument("--data-dir", type=Path, default=DEFAULT_DATA_DIR,
                        help="Directory with entities/relations/metadata parquets")
    parser.add_argument("--report-path", type=Path, default=DEFAULT_REPORT,
                        help="Output report path")
    args = parser.parse_args()

    results = run(args.data_dir, args.report_path)

    pd_vs_g = [r.pd_vs_graph for r in results]
    pass_rate = pd_vs_g.count("VALIDATED") / max(1, len(pd_vs_g))
    close_rate = (pd_vs_g.count("VALIDATED") + pd_vs_g.count("CLOSE")) / max(1, len(pd_vs_g))
    print(f"\npandas vs graph: {pass_rate:.0%} VALIDATED, {close_rate:.0%} within CLOSE")


if __name__ == "__main__":
    main()
