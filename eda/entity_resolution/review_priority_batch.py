#!/usr/bin/env python3
"""
Create a prioritized manual review batch of entity candidate pairs for labeling.

Computes a risk score for each candidate pair as risk = similarity * (1 -
num_jaccard): pairs with high textual similarity but low numeric overlap are
highest risk because they look like duplicates but likely are not. Within each
entity type, sorts by num_mismatch flag first (both entities have numbers but
zero overlap), then by risk_score descending, then by raw score. Takes up to
per_type pairs per type and caps the total at max_total, then adds a blank
is_match column for human annotation.

Key findings: number mismatches are the highest-risk candidates and dominate
the top of the priority batch; this pattern is most prevalent in the EQUIPMENT
type where model numbers are critical disambiguation signals.

Decision: guides human review effort toward the highest-uncertainty pairs first,
ensuring that the most impactful labeling decisions are made before reviewer
fatigue sets in; the risk score formula was validated as the most useful
prioritization signal for this dataset.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def main() -> None:
    parser = argparse.ArgumentParser(description="Prioritized review batch for ER labeling.")
    parser.add_argument("--candidates", default="eda/fuzzy_match_candidates_training.csv")
    parser.add_argument("--out", default="eda/pairwise_labels_review_priority.csv")
    parser.add_argument("--per-type", type=int, default=40)
    parser.add_argument("--max-total", type=int, default=200)
    args = parser.parse_args()

    df = pd.read_csv(args.candidates)

    # Compute risk score: high score but low numeric overlap => higher risk
    df["num_jaccard"] = df["num_jaccard"].fillna(0.0)
    df["risk_score"] = df["score"] * (1.0 - df["num_jaccard"])

    # Flag number mismatch (both have numbers but no overlap)
    df["nums_l"] = df["nums_l"].fillna("")
    df["nums_r"] = df["nums_r"].fillna("")
    df["num_mismatch"] = (df["nums_l"] != "") & (df["nums_r"] != "") & (df["num_jaccard"] == 0.0)

    # Prioritize within each type
    batches = []
    for t, g in df.groupby("type"):
        g = g.sort_values(["num_mismatch", "risk_score", "score"], ascending=[False, False, False])
        batches.append(g.head(args.per_type))

    out_df = pd.concat(batches, ignore_index=True)
    out_df = out_df.sort_values(["num_mismatch", "risk_score", "score"], ascending=[False, False, False])
    if len(out_df) > args.max_total:
        out_df = out_df.head(args.max_total)

    # Add blank label column
    out_df.insert(0, "is_match", "")

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_df.to_csv(out_path, index=False)

    print(
        {
            "pairs": len(out_df),
            "types": out_df["type"].value_counts().to_dict(),
            "out": str(out_path),
        }
    )


if __name__ == "__main__":
    main()
