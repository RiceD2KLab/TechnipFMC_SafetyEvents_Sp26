#!/usr/bin/env python3
"""
Generate weak positive labels and a stratified review sample from fuzzy candidates.

Applies rule-based weak labeling over fuzzy match candidates: pairs with
score >= 0.95 are labeled positive when they lack numbers or when num_jaccard
>= 0.5 for number-bearing entities; org suffix normalization and equipment class
matching provide additional domain boosts at score >= 0.97. Outputs two files:
a weak label CSV formatted for Splink's estimate_m_from_pairwise_labels, and a
balanced review sample with equal representation from high (>= 0.95) and medium
(0.90-0.95) score bands for human annotation.

Key findings: the domain boost rules (org suffix match, equipment class match)
capture a category of pairs that pure score thresholding misses; number Jaccard
at 0.5 is more permissive than the 0.8 threshold used in merge_simulation.py,
reflecting that labels need to include borderline cases for Splink training.

Decision: established the Splink training data generation approach and the
prioritized human review batch format used in review_priority_batch.py.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import re

import pandas as pd


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate weak labels and review samples.")
    parser.add_argument("--candidates", default="eda/fuzzy_match_candidates_training.csv")
    parser.add_argument("--out-weak", default="eda/pairwise_labels_weak.csv")
    parser.add_argument("--out-review", default="eda/pairwise_labels_review.csv")
    parser.add_argument("--score-threshold", type=float, default=0.95)
    parser.add_argument("--num-jaccard-threshold", type=float, default=0.5)
    parser.add_argument("--review-sample", type=int, default=500)
    parser.add_argument("--seed", type=int, default=7)
    args = parser.parse_args()

    df = pd.read_csv(args.candidates)

    ORG_SUFFIXES = {
        "INC", "INC.", "LTD", "LTD.", "LLC", "LLC.", "CORP", "CORP.", "CO", "CO.",
        "COMPANY", "PLC", "BV", "SA", "SRL", "GMBH", "NV", "AG", "AB", "AS",
    }

    EQUIP_KEYWORDS = {
        "FORKLIFT": ["FORKLIFT", "LIFT TRUCK"],
        "CRANE": ["CRANE", "OVERHEAD CRANE", "GANTRY", "JIB CRANE"],
        "PUMP": ["PUMP", "PUMPS"],
        "VALVE": ["VALVE", "VALVES"],
        "HOSE": ["HOSE", "HOSES", "HYDRAULIC HOSE"],
        "PIPE": ["PIPE", "PIPES", "PIPELINE", "RIGID PIPE"],
        "WINCH": ["WINCH"],
        "COMPRESSOR": ["COMPRESSOR"],
        "GENERATOR": ["GENERATOR"],
        "MOTOR": ["MOTOR"],
        "GEARBOX": ["GEARBOX"],
        "FLANGE": ["FLANGE"],
        "GASKET": ["GASKET"],
        "SCAFFOLD": ["SCAFFOLD", "SCAFFOLDING"],
        "LADDER": ["LADDER"],
        "RIG": ["RIG", "DRILLING RIG"],
        "TRUCK": ["TRUCK", "TRAILER"],
        "VESSEL": ["VESSEL", "SHIP", "BARGE", "BOAT"],
        "RIGGING": ["RIGGING", "SLING", "SHACKLE", "CABLE", "WIRE", "CHAIN"],
        "CYLINDER": ["CYLINDER"],
        "HYDRAULIC": ["HYDRAULIC"],
        "ELECTRICAL": ["ELECTRICAL", "ELECTRIC"],
    }

    def normalize_text(text: str) -> str:
        text = text.upper()
        text = re.sub(r"[^A-Z0-9\\s]", " ", text)
        text = re.sub(r"\\s+", " ", text).strip()
        return text

    def org_norm(text: str) -> str:
        toks = [t for t in text.split() if t not in ORG_SUFFIXES]
        return " ".join(toks)

    def equip_class(text: str) -> str:
        for cls, kws in EQUIP_KEYWORDS.items():
            for kw in kws:
                if kw in text:
                    return cls
        return ""

    # Normalize numeric overlap logic
    def is_match(row) -> bool:
        score = row["score"]
        num_j = row["num_jaccard"]
        nums_l = str(row.get("nums_l", ""))
        nums_r = str(row.get("nums_r", ""))
        has_nums_l = bool(nums_l)
        has_nums_r = bool(nums_r)

        if score < args.score_threshold:
            return False
        t_l = normalize_text(str(row["title_l"]))
        t_r = normalize_text(str(row["title_r"]))
        org_l = org_norm(t_l)
        org_r = org_norm(t_r)
        eq_l = equip_class(t_l)
        eq_r = equip_class(t_r)

        if not has_nums_l and not has_nums_r:
            # Use org or equipment match to boost confidence
            if org_l and org_l == org_r:
                return True
            if eq_l and eq_l == eq_r:
                return True
            return True
        if has_nums_l and has_nums_r:
            if num_j >= args.num_jaccard_threshold:
                return True
            # Allow org/equip match even if numbers differ slightly
            if org_l and org_l == org_r and score >= 0.97:
                return True
            if eq_l and eq_l == eq_r and score >= 0.97:
                return True
        return False

    df["weak_match"] = df.apply(is_match, axis=1)

    # Weak labels: only positive matches (Splink expects matches for estimate_m_from_pairwise_labels)
    weak = df[df["weak_match"]].copy()
    weak["source_dataset_l"] = "df"
    weak["source_dataset_r"] = "df"
    weak_labels = weak[
        ["source_dataset_l", "id_l", "source_dataset_r", "id_r"]
    ].rename(
        columns={"id_l": "unique_id_l", "id_r": "unique_id_r"}
    )

    # Review sample: balanced-ish sample of high/low candidates
    high = df[df["score"] >= 0.95]
    low = df[(df["score"] < 0.95) & (df["score"] >= 0.90)]
    review = pd.concat(
        [
            high.sample(min(len(high), args.review_sample // 2), random_state=args.seed),
            low.sample(min(len(low), args.review_sample // 2), random_state=args.seed),
        ]
    ).sample(frac=1.0, random_state=args.seed)

    out_weak = Path(args.out_weak)
    out_review = Path(args.out_review)
    out_weak.parent.mkdir(parents=True, exist_ok=True)
    out_review.parent.mkdir(parents=True, exist_ok=True)

    weak_labels.to_csv(out_weak, index=False)
    review.to_csv(out_review, index=False)

    print(
        {
            "weak_labels": len(weak_labels),
            "review_sample": len(review),
            "out_weak": str(out_weak),
            "out_review": str(out_review),
        }
    )


if __name__ == "__main__":
    main()
