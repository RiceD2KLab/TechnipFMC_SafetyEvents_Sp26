#!/usr/bin/env python3
"""
Mine high-similarity entity pairs to seed Splink training and blocking.

Uses rapidfuzz token-set-ratio with conservative blocking (entity type + first
token + length bucket) to avoid O(N^2) comparisons. Blocks larger than
max_block_size are skipped. For each candidate pair above the similarity
threshold (default 0.9), computes numeric Jaccard overlap between embedded
numbers to flag equipment serial/model number conflicts. Outputs a CSV of
candidate pairs with score, num_jaccard, and block metadata.

Key findings: 11,381 candidate pairs found at threshold 0.9; 81.4% of pairs
scored >= 0.95 confidence; numeric Jaccard revealed that a large fraction of
high-similarity equipment pairs carry different numbers (likely false positives).

Decision: informed ER candidate seeding strategy for Splink; the num_jaccard
field became the primary filter for distinguishing safe equipment merges from
false positives in all downstream scripts.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, List, Tuple

import pandas as pd
from rapidfuzz import fuzz
import re


def normalize_text(text: str) -> str:
    text = text.upper()
    text = "".join(ch if (ch.isalnum() or ch.isspace()) else " " for ch in text)
    return " ".join(text.split())


def length_bucket(s: str, bucket: int) -> int:
    return len(s) // bucket if bucket > 0 else len(s)

def extract_numbers(text: str) -> List[str]:
    return re.findall(r"\d+", text)

def num_jaccard(nums_a: List[str], nums_b: List[str]) -> float:
    set_a = set(nums_a)
    set_b = set(nums_b)
    if not set_a and not set_b:
        return 1.0
    if not set_a or not set_b:
        return 0.0
    inter = set_a & set_b
    union = set_a | set_b
    return len(inter) / len(union) if union else 0.0


def main() -> None:
    parser = argparse.ArgumentParser(description="Find high-similarity entity pairs.")
    parser.add_argument("--entities", default="graphRAG/output_schema_only/entities.parquet")
    parser.add_argument("--out", default="eda/fuzzy_match_candidates.csv")
    parser.add_argument("--threshold", type=float, default=0.9, help="Similarity threshold [0,1].")
    parser.add_argument("--length-bucket", type=int, default=4, help="Bucket size for length blocking.")
    parser.add_argument("--max-block-size", type=int, default=400, help="Skip blocks larger than this.")
    parser.add_argument("--max-pairs", type=int, default=50000, help="Cap total pairs written.")
    parser.add_argument("--exclude-types", default="DATE", help="Comma-separated list of types to skip.")
    args = parser.parse_args()

    ents = pd.read_parquet(args.entities)
    ents = ents.copy()
    ents["title"] = ents["title"].astype(str).str.strip()
    ents["type"] = ents["type"].astype(str).str.strip()
    ents["title_norm"] = ents["title"].map(normalize_text)
    ents["first_token"] = ents["title_norm"].str.split().str[0].fillna("")
    ents["len_bucket"] = ents["title_norm"].map(lambda s: length_bucket(s, args.length_bucket))
    exclude_types = {t.strip().upper() for t in args.exclude_types.split(",") if t.strip()}

    # Build blocks
    blocks = defaultdict(list)
    for _, row in ents.iterrows():
        if row["type"].upper() in exclude_types:
            continue
        key = (row["type"], row["first_token"], row["len_bucket"])
        blocks[key].append((row["id"], row["title"], row["title_norm"], row["type"]))

    threshold = args.threshold * 100.0
    pairs = []
    skipped_blocks = 0

    for key, items in blocks.items():
        n = len(items)
        if n <= 1:
            continue
        if n > args.max_block_size:
            skipped_blocks += 1
            continue
        for i in range(n):
            id_i, title_i, norm_i, t_i = items[i]
            for j in range(i + 1, n):
                id_j, title_j, norm_j, t_j = items[j]
                score = fuzz.token_set_ratio(norm_i, norm_j)
                if score >= threshold:
                    nums_i = extract_numbers(title_i)
                    nums_j = extract_numbers(title_j)
                    pairs.append(
                        {
                            "id_l": id_i,
                            "id_r": id_j,
                            "type": t_i,
                            "title_l": title_i,
                            "title_r": title_j,
                            "score": score / 100.0,
                            "nums_l": "|".join(nums_i),
                            "nums_r": "|".join(nums_j),
                            "num_jaccard": num_jaccard(nums_i, nums_j),
                            "block_key": "|".join(map(str, key)),
                        }
                    )
                    if len(pairs) >= args.max_pairs:
                        break
            if len(pairs) >= args.max_pairs:
                break
        if len(pairs) >= args.max_pairs:
            break

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(pairs).to_csv(out_path, index=False)

    # Summary stats
    score_bins = Counter()
    for p in pairs:
        s = p["score"]
        if s >= 0.95:
            score_bins[">=0.95"] += 1
        elif s >= 0.9:
            score_bins["0.90-0.95"] += 1
        elif s >= 0.85:
            score_bins["0.85-0.90"] += 1
        else:
            score_bins["<0.85"] += 1

    print(
        {
            "pairs": len(pairs),
            "skipped_blocks": skipped_blocks,
            "score_bins": dict(score_bins),
            "out": str(out_path),
        }
    )


if __name__ == "__main__":
    main()
