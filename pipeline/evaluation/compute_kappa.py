"""Compute Cohen's kappa for inter-annotator agreement on L2 causal annotations.

Usage:
    python pipeline/evaluation/compute_kappa.py \
        pipeline/annotation/l2_gt_v2_claude.jsonl \
        pipeline/annotation/l2_gt_v2_codex.jsonl \
        [--overlap-only]

For each record, each relation type is binarised: 1 if the annotator
produced at least one edge of that type, 0 otherwise.  Cohen's kappa
is computed per relation type and as a macro average.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Set

import pandas as pd

from kg_schema import L2_RELATION_NAMES


def cohens_kappa(y1, y2):
    """Compute Cohen's kappa from two binary lists."""
    n = len(y1)
    if n == 0:
        return float("nan")

    # Confusion matrix
    a = sum(1 for a, b in zip(y1, y2) if a == 1 and b == 1)
    b_ = sum(1 for a, b in zip(y1, y2) if a == 1 and b == 0)
    c = sum(1 for a, b in zip(y1, y2) if a == 0 and b == 1)
    d = sum(1 for a, b in zip(y1, y2) if a == 0 and b == 0)

    po = (a + d) / n  # observed agreement
    pe = ((a + b_) * (a + c) + (c + d) * (b_ + d)) / (n * n)  # expected

    if pe == 1.0:
        return 1.0 if po == 1.0 else 0.0
    return (po - pe) / (1 - pe)


def _load_jsonl(path: Path) -> List[dict]:
    records: List[dict] = []
    with path.open("r", encoding="utf-8") as fp:
        for line in fp:
            line = line.strip()
            if line:
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return records


_L2_RELATIONS = L2_RELATION_NAMES


def _binarize_jsonl(
    edges: List[dict],
    record_nos: List[str],
) -> Dict[str, List[int]]:
    """Binarize JSONL edges by relation type per record.

    Returns {relation: [0/1 per record_no]}.
    """
    by_record: Dict[str, Set[str]] = defaultdict(set)
    for e in edges:
        rno = str(e.get("record_no", ""))
        rel = str(e.get("relation", "")).strip()
        if rno and rel:
            by_record[rno].add(rel)

    result: Dict[str, List[int]] = {}
    for rel in _L2_RELATIONS:
        result[rel] = [1 if rel in by_record.get(rno, set()) else 0 for rno in record_nos]
    return result


def _print_verdict(macro: float, agreement_rates: dict[str, float] | None = None) -> None:
    print(f"\n**Macro-average kappa: {macro:.4f}**")

    # For high-prevalence relations, use raw agreement rate instead of kappa.
    if agreement_rates:
        causal_rate = agreement_rates.get("CAUSAL")
        if causal_rate is not None and causal_rate >= 0.95:
            print(f"\nCAUSAL raw agreement: {causal_rate:.1%}")
            print(f"\nGate 3 prerequisite: PASS (CAUSAL agreement >= 95%)")
            return

    if macro >= 0.70:
        print("\nGate 3 prerequisite: PASS (kappa >= 0.70)")
    elif macro >= 0.50:
        print("\nGate 3 prerequisite: MODERATE (0.50–0.69) — adjudicate disagreements before proceeding")
    else:
        print("\nGate 3 prerequisite: FAIL (kappa < 0.50) — revise guidelines, re-annotate overlap set")


def main() -> None:
    parser = argparse.ArgumentParser(description="Compute Cohen's kappa on L2 causal annotations")
    parser.add_argument("file_a", type=Path, help="Annotator A JSONL file")
    parser.add_argument("file_b", type=Path, help="Annotator B JSONL file")
    parser.add_argument("--overlap-only", action="store_true",
                        help="Restrict to protocol overlap set (rows 81-120)")
    args = parser.parse_args()

    edges_a = _load_jsonl(args.file_a)
    edges_b = _load_jsonl(args.file_b)

    # Get annotator names from first edge
    ann_a = edges_a[0].get("annotator", "A") if edges_a else "A"
    ann_b = edges_b[0].get("annotator", "B") if edges_b else "B"

    # Find common record_nos
    records_a = set(str(e.get("record_no", "")) for e in edges_a)
    records_b = set(str(e.get("record_no", "")) for e in edges_b)
    # Sort: numeric records numerically, non-numeric alphabetically
    def _sort_key(x: str) -> tuple[int, str]:
        try:
            return (0, int(x))  # Numeric: sort by int value
        except (ValueError, TypeError):
            return (1, x)  # Non-numeric: sort alphabetically
    common = sorted(records_a & records_b, key=_sort_key)

    if args.overlap_only:
        # Overlap set: rows 81-120 of the annotation template (0-indexed)
        template_path = Path(__file__).parent.parent / "annotation" / "annotation_template.csv"
        if not template_path.exists():
            print(f"Error: Template file not found: {template_path}", file=sys.stderr)
            sys.exit(1)
        template = pd.read_csv(template_path)
        if len(template) < 120:
            print(f"Warning: Template has only {len(template)} rows, expected >= 120", file=sys.stderr)
        overlap_records = set(str(r) for r in template.iloc[80:120]["record_no"].values)
        common = [r for r in common if r in overlap_records]
        label = f"Overlap set (rows 81–120, n={len(common)})"
    else:
        label = f"Common records (n={len(common)})"

    if not common:
        print("No common records found between the two files.")
        return

    bin_a = _binarize_jsonl(edges_a, common)
    bin_b = _binarize_jsonl(edges_b, common)

    results = {}

    print(f"## Cohen's Kappa (JSONL L2) — {label}")
    print(f"\nAnnotator A: {ann_a} ({len(edges_a)} edges, {len(records_a)} records)")
    print(f"Annotator B: {ann_b} ({len(edges_b)} edges, {len(records_b)} records)")
    print()

    print("| Relation | Kappa | A present | B present | Both present | Both absent | Disagree |")
    print("|----------|------:|----------:|----------:|-------------:|------------:|---------:|")

    agreement_rates: dict[str, float] = {}

    for rel in list(bin_a.keys()):
        y_a = bin_a[rel]
        y_b = bin_b[rel]

        k = cohens_kappa(y_a, y_b)
        results[rel] = k

        both_yes = sum(1 for x, y in zip(y_a, y_b) if x == 1 and y == 1)
        both_no = sum(1 for x, y in zip(y_a, y_b) if x == 0 and y == 0)
        disagree = len(y_a) - both_yes - both_no
        a_present = sum(y_a)
        b_present = sum(y_b)

        # Track raw agreement for high-prevalence detection
        n = len(y_a)
        if n > 0:
            agreement_rates[rel] = (both_yes + both_no) / n

        print(f"| {rel} | {k:.4f} | {a_present} | {b_present} | {both_yes} | {both_no} | {disagree} |")

    macro = sum(results.values()) / len(results)
    _print_verdict(macro, agreement_rates=agreement_rates)


if __name__ == "__main__":
    main()
