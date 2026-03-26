#!/usr/bin/env python3
"""
Simulate degree impact of transitive closure on high-confidence entity pairs.

Loads fuzzy match candidates and applies union-find over pairs satisfying both
score >= threshold (default 0.95) and num_jaccard >= threshold (default 0.8) to
form merge clusters. Remaps relationship endpoints to cluster representatives,
deduplicates self-loops and parallel edges, and computes pre/post average degree
and component statistics. Reports pairs used, degree improvement, and component
changes as JSON.

Key findings: 1,027 pairs qualified under conservative thresholds (score >= 0.95,
num_jaccard >= 0.8), yielding only a 0.12% improvement in average degree; the
graph topology barely changed, confirming that conservative ER alone is
insufficient to reach the connectivity target needed for downstream reasoning.

Decision: demonstrated that conservative ER covers too few pairs to matter;
informed the conclusion that more aggressive strategies (domain features,
semantic similarity, number-based blocking) are required to meaningfully
improve graph connectivity.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
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


def component_stats(edges: Iterable[Tuple[str, str]], nodes: Iterable[str]) -> Dict[str, float]:
    dsu = DSU()
    for s, t in edges:
        dsu.union(s, t)
    sizes = Counter()
    for n in nodes:
        sizes[dsu.find(n)] += 1
    largest = max(sizes.values()) if sizes else 0
    return {
        "components": len(sizes),
        "largest_component": largest,
        "largest_component_pct": (largest / len(nodes) * 100) if nodes else 0.0,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Simulate merges and recompute graph metrics.")
    parser.add_argument("--entities", default="fall2025/graphRAG/output_schema_only/entities.parquet")
    parser.add_argument("--relations", default="fall2025/graphRAG/output_schema_only/relationships.parquet")
    parser.add_argument("--candidates", default="eda/fuzzy_match_candidates_training.csv")
    parser.add_argument("--score-threshold", type=float, default=0.95)
    parser.add_argument("--num-jaccard-threshold", type=float, default=0.8)
    parser.add_argument("--json-out", default="eda/merge_simulation.json")
    args = parser.parse_args()

    ents = pd.read_parquet(args.entities)
    rels = pd.read_parquet(args.relations)
    pairs = pd.read_csv(args.candidates)

    # Filter candidate pairs
    def is_merge(row) -> bool:
        if row["score"] < args.score_threshold:
            return False
        nums_l = str(row.get("nums_l", ""))
        nums_r = str(row.get("nums_r", ""))
        has_nums_l = bool(nums_l)
        has_nums_r = bool(nums_r)
        if not has_nums_l and not has_nums_r:
            return True
        if has_nums_l and has_nums_r:
            return row.get("num_jaccard", 0.0) >= args.num_jaccard_threshold
        return False

    pairs_f = pairs[pairs.apply(is_merge, axis=1)].copy()

    # Union-Find over entity IDs
    dsu = DSU()
    for _, row in pairs_f.iterrows():
        dsu.union(str(row["id_l"]), str(row["id_r"]))

    # Map title -> id
    ents["id"] = ents["id"].astype(str)
    title_to_id = dict(zip(ents["title"].astype(str), ents["id"]))

    # Pre-merge metrics
    edges_pre = [(s, t) for s, t in zip(rels["source"], rels["target"])]
    nodes_pre = set(rels["source"]) | set(rels["target"])
    avg_degree_pre = len(edges_pre) / len(nodes_pre) if nodes_pre else 0
    comp_pre = component_stats(edges_pre, nodes_pre)

    # Post-merge: map node titles -> ids -> clusters
    edges_post = set()
    nodes_post = set()
    for s, t in zip(rels["source"], rels["target"]):
        id_s = title_to_id.get(str(s))
        id_t = title_to_id.get(str(t))
        if id_s is None or id_t is None:
            continue
        cs = dsu.find(id_s)
        ct = dsu.find(id_t)
        if cs == ct:
            continue
        edge = (cs, ct) if cs < ct else (ct, cs)
        edges_post.add(edge)
        nodes_post.add(cs)
        nodes_post.add(ct)

    avg_degree_post = len(edges_post) / len(nodes_post) if nodes_post else 0
    comp_post = component_stats(edges_post, nodes_post)

    out = {
        "pairs_total": len(pairs),
        "pairs_used_for_merge": len(pairs_f),
        "avg_degree_pre": avg_degree_pre,
        "avg_degree_post": avg_degree_post,
        "edges_pre": len(edges_pre),
        "edges_post": len(edges_post),
        "nodes_pre": len(nodes_pre),
        "nodes_post": len(nodes_post),
        "components_pre": comp_pre,
        "components_post": comp_post,
    }

    out_path = Path(args.json_out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
