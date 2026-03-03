#!/usr/bin/env python3
"""Compare L2 enrichment outputs across multiple model runs.

Reads l2_edges.jsonl from multiple output directories and computes:
- Edge count, edges/record, tautology rate
- Relation type distribution
- Entity type distribution
- Token-overlap agreement between model pairs

Usage:
    python pipeline_v2/enrichment/compare_model_runs.py \
        --dirs output/l2/comparison/qwen3_30b_baseline \
               output/l2/comparison/qwen35_9b_dense \
               output/l2/comparison/qwen35_35b_moe
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path

import pandas as pd


def _load_jsonl(path: Path) -> list[dict]:
    records = []
    with path.open("r", encoding="utf-8") as fp:
        for line in fp:
            line = line.strip()
            if line:
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return records


def _tokenize(text: str) -> set[str]:
    return set(re.findall(r"\w+", text.lower()))


def _tautology_rate(edges: list[dict]) -> float:
    if not edges:
        return 0.0
    taut = 0
    for e in edges:
        src_tokens = _tokenize(e.get("source", ""))
        tgt_tokens = _tokenize(e.get("target", ""))
        if src_tokens and tgt_tokens:
            overlap = len(src_tokens & tgt_tokens) / min(len(src_tokens), len(tgt_tokens))
            if overlap >= 0.8:
                taut += 1
    return taut / len(edges)


def _token_overlap_agreement(edges_a: list[dict], edges_b: list[dict]) -> float:
    """Compute average best-match token overlap between two edge sets per record."""
    # Group by record_no
    by_record_a: dict[str, list[dict]] = {}
    for e in edges_a:
        rn = str(e.get("record_no", ""))
        by_record_a.setdefault(rn, []).append(e)

    by_record_b: dict[str, list[dict]] = {}
    for e in edges_b:
        rn = str(e.get("record_no", ""))
        by_record_b.setdefault(rn, []).append(e)

    common_records = set(by_record_a.keys()) & set(by_record_b.keys())
    if not common_records:
        return 0.0

    overlaps = []
    for rn in common_records:
        ea = by_record_a[rn]
        eb = by_record_b[rn]
        for edge_a in ea:
            a_src = _tokenize(edge_a.get("source", ""))
            a_tgt = _tokenize(edge_a.get("target", ""))
            a_tokens = a_src | a_tgt
            best = 0.0
            for edge_b in eb:
                b_src = _tokenize(edge_b.get("source", ""))
                b_tgt = _tokenize(edge_b.get("target", ""))
                b_tokens = b_src | b_tgt
                if a_tokens and b_tokens:
                    jaccard = len(a_tokens & b_tokens) / len(a_tokens | b_tokens)
                    best = max(best, jaccard)
            overlaps.append(best)

    return sum(overlaps) / len(overlaps) if overlaps else 0.0


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare L2 model runs.")
    parser.add_argument("--dirs", nargs="+", required=True, help="Output directories to compare")
    args = parser.parse_args()

    model_data: dict[str, list[dict]] = {}
    for d in args.dirs:
        p = Path(d)
        jsonl_path = p / "l2_edges.jsonl"
        if not jsonl_path.exists():
            print(f"WARNING: {jsonl_path} not found, skipping")
            continue
        edges = _load_jsonl(jsonl_path)
        label = p.name
        model_data[label] = edges

    if len(model_data) < 2:
        print("Need at least 2 model directories with l2_edges.jsonl")
        return

    # Per-model stats
    print(f"\n{'Model':<30} {'Edges':>8} {'Records':>8} {'E/R':>6} {'Taut%':>7}")
    print("-" * 65)
    for label, edges in model_data.items():
        n_edges = len(edges)
        n_records = len({str(e.get("record_no", "")) for e in edges})
        epr = n_edges / max(n_records, 1)
        taut = _tautology_rate(edges)
        print(f"{label:<30} {n_edges:>8} {n_records:>8} {epr:>6.2f} {taut:>6.1%}")

    # Relation type distribution
    print(f"\n{'Model':<30} {'CAUSAL':>8} {'PRECEDED':>8} {'FAILED_C':>8}")
    print("-" * 58)
    for label, edges in model_data.items():
        rel_counts = Counter(e.get("relation", "") for e in edges)
        total = max(len(edges), 1)
        c = rel_counts.get("CAUSAL", 0)
        p = rel_counts.get("PRECEDED_BY", 0)
        f = rel_counts.get("FAILED_CONTROL", 0)
        print(f"{label:<30} {c/total:>7.1%} {p/total:>7.1%} {f/total:>7.1%}")

    # Entity type distribution (source_type + target_type)
    print(f"\n{'Model':<30} Top source_type → Top target_type")
    print("-" * 70)
    for label, edges in model_data.items():
        src_types = Counter(e.get("source_type", "") for e in edges)
        tgt_types = Counter(e.get("target_type", "") for e in edges)
        top_src = src_types.most_common(3)
        top_tgt = tgt_types.most_common(3)
        src_str = ", ".join(f"{t}:{c}" for t, c in top_src)
        tgt_str = ", ".join(f"{t}:{c}" for t, c in top_tgt)
        print(f"{label:<30} {src_str} → {tgt_str}")

    # Pairwise agreement
    labels = list(model_data.keys())
    print(f"\nPairwise token-overlap agreement:")
    print(f"{'':>30}", end="")
    for l in labels:
        print(f" {l[:12]:>12}", end="")
    print()
    for i, l1 in enumerate(labels):
        print(f"{l1:<30}", end="")
        for j, l2 in enumerate(labels):
            if i == j:
                print(f" {'—':>12}", end="")
            elif j > i:
                agreement = _token_overlap_agreement(model_data[l1], model_data[l2])
                print(f" {agreement:>11.1%}", end="")
            else:
                print(f" {'':>12}", end="")
        print()


if __name__ == "__main__":
    main()
