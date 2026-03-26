"""Relation entropy report — measures edge-type diversity in the graph.

Usage:
    python pipeline/evaluation/relation_entropy.py EDGES_FILE [--baseline EDGES_FILE2]

Reads a Parquet or CSV edges file, computes Shannon entropy over the
``relation`` column, and prints a compact report.  Optionally compares
against a baseline file (e.g. pre-ER vs post-ER, or pre- vs post-label
change) to flag regressions.

Maximum entropy = log2(K) where K = number of distinct relation types.
A normalised value (H / H_max) near 1.0 means edges are evenly spread;
near 0.0 means one type dominates.
"""
from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

import pandas as pd


def _load_edges(path: Path) -> pd.DataFrame:
    if path.suffix == ".parquet":
        return pd.read_parquet(path)
    return pd.read_csv(path)


def relation_entropy(edges: pd.DataFrame) -> dict:
    """Return entropy stats for the 'relation' column."""
    counts = edges["relation"].value_counts()
    total = counts.sum()
    k = len(counts)

    probs = counts / total
    h = -sum(p * math.log2(p) for p in probs if p > 0)
    h_max = math.log2(k) if k > 1 else 0.0
    h_norm = h / h_max if h_max > 0 else 0.0

    return {
        "n_edges": int(total),
        "n_relation_types": k,
        "entropy": round(h, 4),
        "max_entropy": round(h_max, 4),
        "normalised_entropy": round(h_norm, 4),
        "counts": counts.to_dict(),
    }


def _fmt_report(stats: dict, label: str = "Current") -> str:
    lines = [
        f"## Relation Entropy — {label}",
        "",
        f"| Metric | Value |",
        f"|--------|------:|",
        f"| Edges | {stats['n_edges']:,} |",
        f"| Relation types | {stats['n_relation_types']} |",
        f"| Shannon entropy (H) | {stats['entropy']} |",
        f"| Max entropy (log2 K) | {stats['max_entropy']} |",
        f"| Normalised (H/Hmax) | {stats['normalised_entropy']} |",
        "",
        "| Relation | Count | Share |",
        "|----------|------:|------:|",
    ]
    total = stats["n_edges"]
    for rel, cnt in sorted(stats["counts"].items(), key=lambda x: -x[1]):
        pct = 100 * cnt / total
        lines.append(f"| {rel} | {cnt:,} | {pct:.1f}% |")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Relation entropy report")
    parser.add_argument("edges", type=Path, help="Edges Parquet or CSV")
    parser.add_argument("--baseline", type=Path, help="Baseline edges file for comparison")
    args = parser.parse_args()

    if not args.edges.exists():
        print(f"Error: {args.edges} not found", file=sys.stderr)
        sys.exit(1)

    current = relation_entropy(_load_edges(args.edges))
    report = _fmt_report(current, label=args.edges.name)

    if args.baseline:
        if not args.baseline.exists():
            print(f"Warning: baseline {args.baseline} not found, skipping comparison", file=sys.stderr)
        else:
            base = relation_entropy(_load_edges(args.baseline))
            report += "\n\n" + _fmt_report(base, label=f"Baseline ({args.baseline.name})")
            delta = current["normalised_entropy"] - base["normalised_entropy"]
            direction = "improved" if delta > 0 else "regressed" if delta < 0 else "unchanged"
            report += f"\n\n**Delta:** normalised entropy {direction} by {abs(delta):.4f}"

    print(report)


if __name__ == "__main__":
    main()
