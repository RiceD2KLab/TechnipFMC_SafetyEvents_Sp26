"""Compute Cohen's kappa for inter-annotator agreement on causal annotations.

Usage:
    python pipeline_v2/evaluation/compute_kappa.py \
        pipeline_v2/annotation/annotation_llm.csv \
        pipeline_v2/annotation/annotation_codex.csv \
        [--overlap-only]

By default, computes kappa on all records present in both files.
With --overlap-only, restricts to the protocol-defined overlap set
(rows 81–120, 0-indexed).

For each record, each relation type (CAUSED_BY, CONTRIBUTED_TO, LED_TO)
is binarised: 1 if the annotator filled in at least one edge of that type,
0 otherwise.  Cohen's kappa is computed per relation type and as a macro
average.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd


def _has_edge(row: pd.Series, prefix: str) -> int:
    """Return 1 if the annotator recorded at least one edge of this type."""
    # Column naming: caused_by_1_cause, caused_by_2_cause,
    #                contributed_to_1_factor, contributed_to_2_factor,
    #                led_to_1_event, led_to_2_event, led_to_3_event
    if prefix == "caused_by":
        cols = [c for c in row.index if c.startswith("caused_by_") and c.endswith("_cause")]
    elif prefix == "contributed_to":
        cols = [c for c in row.index if c.startswith("contributed_to_") and c.endswith("_factor")]
    elif prefix == "led_to":
        cols = [c for c in row.index if c.startswith("led_to_") and c.endswith("_event")]
    else:
        return 0
    return int(any(pd.notna(row[c]) and str(row[c]).strip() != "" for c in cols))


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


def main() -> None:
    parser = argparse.ArgumentParser(description="Compute Cohen's kappa on causal annotations")
    parser.add_argument("file_a", type=Path, help="Annotator A CSV")
    parser.add_argument("file_b", type=Path, help="Annotator B CSV")
    parser.add_argument("--overlap-only", action="store_true",
                        help="Restrict to protocol overlap set (rows 81-120)")
    args = parser.parse_args()

    a = pd.read_csv(args.file_a)
    b = pd.read_csv(args.file_b)

    if args.overlap_only:
        a = a.iloc[80:120]
        b = b.iloc[80:120]
        label = "Overlap set (rows 81–120, n=40)"
    else:
        label = f"All records (n={len(a)})"

    assert len(a) == len(b), f"Row count mismatch: {len(a)} vs {len(b)}"
    assert (a["record_no"].values == b["record_no"].values).all(), "record_no mismatch"

    relation_types = ["caused_by", "contributed_to", "led_to"]
    results = {}

    print(f"## Cohen's Kappa — {label}")
    print(f"\nAnnotator A: {a['annotator_id'].iloc[0]}")
    print(f"Annotator B: {b['annotator_id'].iloc[0]}")
    print()

    print("| Relation | Kappa | A present | B present | Both present | Both absent | Disagree |")
    print("|----------|------:|----------:|----------:|-------------:|------------:|---------:|")

    for rel in relation_types:
        y_a = [_has_edge(a.iloc[i], rel) for i in range(len(a))]
        y_b = [_has_edge(b.iloc[i], rel) for i in range(len(b))]

        k = cohens_kappa(y_a, y_b)
        results[rel] = k

        both_yes = sum(1 for x, y in zip(y_a, y_b) if x == 1 and y == 1)
        both_no = sum(1 for x, y in zip(y_a, y_b) if x == 0 and y == 0)
        disagree = len(y_a) - both_yes - both_no
        a_present = sum(y_a)
        b_present = sum(y_b)

        display_name = rel.upper()
        print(f"| {display_name} | {k:.4f} | {a_present} | {b_present} | {both_yes} | {both_no} | {disagree} |")

    macro = sum(results.values()) / len(results)
    print(f"\n**Macro-average kappa: {macro:.4f}**")

    if macro >= 0.70:
        print("\nGate 3 prerequisite: PASS (kappa >= 0.70)")
    elif macro >= 0.50:
        print("\nGate 3 prerequisite: MODERATE (0.50–0.69) — adjudicate disagreements before proceeding")
    else:
        print("\nGate 3 prerequisite: FAIL (kappa < 0.50) — revise guidelines, re-annotate overlap set")


if __name__ == "__main__":
    main()
