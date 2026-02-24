#!/usr/bin/env python3
"""
Per-entity-type cluster diagnostics at configurable ER thresholds.

Applies union-find over fuzzy match candidates filtered by score >= threshold
and num_jaccard >= num_jaccard threshold (with number-free pairs always allowed),
then reports cluster statistics broken down by entity type: cluster count,
clusters with more than one member, entities absorbed, average/median/max cluster
size, and total merges. Outputs both JSON and CSV. Designed to be run at
multiple threshold combinations (strict: score >= 0.95 + num_jaccard >= 0.8;
loose: score >= 0.90 + num_jaccard >= 0.5) to compare ER aggressiveness.

Key findings at strict settings: 889 total merges across all types; EQUIPMENT
max cluster size 18 (indicating some legitimate equipment families); loose
settings produce substantially more merges with higher overmerge risk.

Decision: strict vs loose ER threshold selection for the v2 pipeline; confirmed
that strict thresholds are safe (max cluster 18) while loose settings require
human review due to larger cluster sizes that likely contain false positives.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, Iterable, Tuple

import pandas as pd


class DSU:
    def __init__(self) -> None:
        self.parent: Dict[str, str] = {}
        self.size: Dict[str, int] = {}

    def find(self, x: str) -> str:
        p = self.parent.get(x, x)
        if p != x:
            p = self.find(p)
            self.parent[x] = p
        return p

    def union(self, a: str, b: str) -> None:
        ra = self.find(a)
        rb = self.find(b)
        if ra == rb:
            return
        sa = self.size.get(ra, 1)
        sb = self.size.get(rb, 1)
        if sa < sb:
            ra, rb = rb, ra
            sa, sb = sb, sa
        self.parent[rb] = ra
        self.size[ra] = sa + sb
        if rb in self.size:
            del self.size[rb]


def cluster_stats(ids: Iterable[str], unions: Iterable[Tuple[str, str]]) -> Dict[str, float]:
    dsu = DSU()
    for a, b in unions:
        dsu.union(a, b)
    counts = Counter()
    for i in ids:
        counts[dsu.find(i)] += 1
    sizes = list(counts.values())
    if not sizes:
        return {}
    sizes.sort()
    clusters_gt1 = [s for s in sizes if s > 1]
    merged = sum(s - 1 for s in sizes)
    return {
        "nodes": len(ids),
        "clusters": len(sizes),
        "clusters_gt1": len(clusters_gt1),
        "entities_in_clusters_gt1": sum(clusters_gt1),
        "avg_cluster_size": sum(sizes) / len(sizes),
        "median_cluster_size": sizes[len(sizes) // 2],
        "max_cluster_size": sizes[-1],
        "merged_entities": merged,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Type-specific cluster diagnostics.")
    parser.add_argument("--candidates", default="eda/fuzzy_match_candidates_training.csv")
    parser.add_argument("--threshold", type=float, default=0.95)
    parser.add_argument("--num-jaccard", type=float, default=0.8)
    parser.add_argument("--json-out", default="eda/type_cluster_diagnostics.json")
    parser.add_argument("--csv-out", default="eda/type_cluster_diagnostics.csv")
    args = parser.parse_args()

    df = pd.read_csv(args.candidates)

    # Filter
    df["num_jaccard"] = df["num_jaccard"].fillna(0.0)
    df["nums_l"] = df["nums_l"].fillna("")
    df["nums_r"] = df["nums_r"].fillna("")

    def keep(row) -> bool:
        if row["score"] < args.threshold:
            return False
        has_nums_l = bool(row["nums_l"])
        has_nums_r = bool(row["nums_r"])
        if not has_nums_l and not has_nums_r:
            return True
        if has_nums_l and has_nums_r:
            return row["num_jaccard"] >= args.num_jaccard
        return False

    df_f = df[df.apply(keep, axis=1)].copy()

    out = {}
    rows = []
    for t, g in df_f.groupby("type"):
        ids = set(g["id_l"]).union(set(g["id_r"]))
        unions = list(zip(g["id_l"], g["id_r"]))
        stats = cluster_stats(ids, unions)
        out[t] = stats
        if stats:
            row = {"type": t, **stats}
            rows.append(row)

    out_path = Path(args.json_out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")

    pd.DataFrame(rows).to_csv(args.csv_out, index=False)
    print({"types": len(rows), "json": str(out_path), "csv": args.csv_out})


if __name__ == "__main__":
    main()
