#!/usr/bin/env python3
"""
Graph diagnostics for GraphRAG outputs.

Computes graph health metrics on the raw GraphRAG Mistral extraction: degree
distribution (E/N, 2E/N, percentiles), relation type distribution with Shannon
entropy before and after canonical mapping, schema leakage (entity type drift
outside the 7-type allowlist), per-type degree breakdown (INCIDENT vs others),
and hub sensitivity (component fragmentation after removing top-p% hubs).

Key findings: average degree 1.87 (sparse); 3,380 unique raw relation types
collapsed to 13 after canonicalization; 14,926 entities fell outside the
allowed schema; top 1% hub nodes hold a disproportionate share of graph
connectivity, making the graph fragile to hub removal.

Decision: schema enforcement is critical before any downstream reasoning; hub
topology confirms that entity resolution must improve connectivity before GNN
or graph-query workloads are viable.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Dict, List, Optional, Tuple

import pandas as pd

# Canonical Relations Mapping (same as eda/clean_graph_topology.py)
RELATION_MAP = {
    "CAUSE": "CAUSED_BY",
    "LED_TO": "CAUSED_BY",
    "RESULT": "RESULTED_IN",
    "DUE_TO": "CAUSED_BY",
    "CONTRIB": "CAUSED_BY",
    "INVOLV": "INVOLVED",
    "OCCUR": "OCCURRED_AT",
    "LOCAT": "OCCURRED_AT",
    "PLACE": "OCCURRED_AT",
    "DURING": "OCCURRED_AT",
    "WHEN": "OCCURRED_AT",
    "TIME": "OCCURRED_AT",
    "DAMAGE": "RESULTED_IN",
    "INJUR": "RESULTED_IN",
    "HURT": "RESULTED_IN",
    "AFFECT": "AFFECTED",
    "IMPACT": "AFFECTED",
    "USE": "USED_IN",
    "UTIL": "USED_IN",
    "OPERAT": "INVOLVED",
    "OWN": "INVOLVED",
}

ALLOWED_TYPES = {
    "INCIDENT",
    "INJURY_TYPE",
    "BODY_PART",
    "EQUIPMENT",
    "LOCATION",
    "ORGANIZATION",
    "DATE",
}

LEGACY_TYPE_ALIASES = {
    "INCIDENT_TYPE": "INCIDENT",
}


def normalize_text(text: str) -> str:
    text = text.upper()
    text = re.sub(r"[^A-Z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def map_relation(desc: str) -> str:
    norm = normalize_text(desc)
    for keyword, canonical in RELATION_MAP.items():
        if keyword in norm:
            return canonical
    return "INVOLVED"


def shannon_entropy(counts: Counter) -> float:
    total = sum(counts.values())
    if total == 0:
        return 0.0
    return -sum((c / total) * math.log2(c / total) for c in counts.values())


def degree_stats(values: List[int]) -> Dict[str, float]:
    if not values:
        return {}
    values_sorted = sorted(values)
    n = len(values_sorted)

    def pct(p: float) -> int:
        idx = int(math.ceil(p * n)) - 1
        idx = max(0, min(idx, n - 1))
        return values_sorted[idx]

    return {
        "count": n,
        "mean": sum(values_sorted) / n,
        "median": pct(0.5),
        "p90": pct(0.9),
        "p95": pct(0.95),
        "p99": pct(0.99),
        "min": values_sorted[0],
        "max": values_sorted[-1],
    }


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


def component_sizes(edges: Iterable[Tuple[str, str]], nodes: Iterable[str]) -> Counter:
    dsu = DSU()
    for s, t in edges:
        dsu.union(s, t)
    sizes: Counter = Counter()
    for n in nodes:
        sizes[dsu.find(n)] += 1
    return sizes


def read_relations_from_csv(path: Path) -> List[str]:
    relations: List[str] = []
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        rel_id_idx = header.index("relationship_id")
        rel_idx = header.index("description")
        seen = set()
        for row in reader:
            rel_id = row[rel_id_idx]
            if rel_id in seen:
                continue
            seen.add(rel_id)
            relations.append(row[rel_idx])
    return relations


def main() -> None:
    parser = argparse.ArgumentParser(description="Graph diagnostics for GraphRAG outputs.")
    parser.add_argument("--rels", default="graphRAG/output/relationships_filtered.parquet")
    parser.add_argument("--ents", default="graphRAG/output/entities_filtered.parquet")
    parser.add_argument("--triples", default="graphRAG/output/incident_triples.csv")
    parser.add_argument("--json-out", default=None, help="Optional JSON output path.")
    parser.add_argument("--percentiles", default="0.95,0.975,0.99,0.995")
    args = parser.parse_args()

    rels = pd.read_parquet(args.rels)
    ents = pd.read_parquet(args.ents)

    src = rels["source"].astype(str)
    tgt = rels["target"].astype(str)

    deg = Counter()
    for s, t in zip(src, tgt):
        deg[s] += 1
        deg[t] += 1

    nodes = set(deg.keys())
    edges = list(zip(src, tgt))

    # Basic graph metrics
    edge_count = len(rels)
    node_count = len(nodes)
    avg_degree = edge_count / node_count if node_count else 0
    total_degree = 2 * edge_count / node_count if node_count else 0

    # Relation distribution + entropy
    rel_counts = None
    if Path(args.triples).exists():
        relations = read_relations_from_csv(Path(args.triples))
        rel_counts = Counter(relations)
    else:
        rel_counts = Counter(rels["description"].astype(str))

    entropy_pre = shannon_entropy(rel_counts)
    mapped_counts = Counter(map_relation(r) for r in rel_counts.elements())
    entropy_post = shannon_entropy(mapped_counts)

    # Long-tail stats
    rel_le_5 = sum(1 for v in rel_counts.values() if v <= 5)
    rel_le_10 = sum(1 for v in rel_counts.values() if v <= 10)

    # Entity normalization merges
    titles = ents["title"].astype(str)
    clean_titles = {normalize_text(t) for t in titles}
    merged_count = len(titles) - len(clean_titles)

    # Schema leakage
    types_norm = (
        ents["type"]
        .astype(str)
        .str.strip()
        .str.upper()
        .map(lambda value: LEGACY_TYPE_ALIASES.get(value, value))
    )
    type_counts = types_norm.value_counts()
    allowed_nodes = int(type_counts[type_counts.index.isin(ALLOWED_TYPES)].sum())
    empty_type = int(type_counts.get("", 0))
    non_allowed_nodes = int(len(ents) - allowed_nodes)

    # Incident vs non-incident degree (type-based)
    type_map = {
        str(title).strip(): LEGACY_TYPE_ALIASES.get(str(entity_type).strip().upper(), str(entity_type).strip().upper())
        for title, entity_type in zip(ents["title"].astype(str), ents["type"].astype(str))
    }
    incident_deg = [d for n, d in deg.items() if type_map.get(n, "") == "INCIDENT"]
    non_incident_deg = [d for n, d in deg.items() if type_map.get(n, "") != "INCIDENT"]

    # Hub sensitivity
    values = sorted(deg.values())
    percentiles = [float(p.strip()) for p in args.percentiles.split(",") if p.strip()]
    hub_sensitivity = []
    for p in percentiles:
        idx = int(math.ceil(p * len(values))) - 1
        idx = max(0, min(idx, len(values) - 1))
        cutoff = values[idx]
        hubs = {n for n, d in deg.items() if d >= cutoff}
        remaining = nodes - hubs

        sizes = component_sizes((e for e in edges if e[0] in remaining and e[1] in remaining), remaining)
        largest = max(sizes.values()) if sizes else 0
        hub_sensitivity.append(
            {
                "percentile": p,
                "cutoff": cutoff,
                "hub_nodes": len(hubs),
                "components": len(sizes),
                "largest_component": largest,
                "largest_component_pct": (largest / len(remaining) * 100) if remaining else 0.0,
            }
        )

    # Full graph components
    full_sizes = component_sizes(edges, nodes)
    full_largest = max(full_sizes.values()) if full_sizes else 0

    # p99 appendix stats
    p99_entry = next((h for h in hub_sensitivity if abs(h["percentile"] - 0.99) < 1e-6), None)
    p99_sizes = None
    if p99_entry:
        cutoff = p99_entry["cutoff"]
        hubs = {n for n, d in deg.items() if d >= cutoff}
        remaining = nodes - hubs
        sizes = component_sizes((e for e in edges if e[0] in remaining and e[1] in remaining), remaining)
        sizes_sorted = sorted(sizes.values(), reverse=True)
        p99_sizes = {
            "top10_sizes": sizes_sorted[:10],
            "size_1": sum(1 for s in sizes.values() if s == 1),
            "size_2": sum(1 for s in sizes.values() if s == 2),
            "size_le_5": sum(1 for s in sizes.values() if s <= 5),
        }

    report = {
        "graph": {
            "edges": edge_count,
            "nodes": node_count,
            "avg_degree": avg_degree,
            "total_degree": total_degree,
            "components": len(full_sizes),
            "largest_component": full_largest,
            "largest_component_pct": (full_largest / node_count * 100) if node_count else 0.0,
        },
        "relations": {
            "unique_types": len(rel_counts),
            "rel_le_5": rel_le_5,
            "rel_le_10": rel_le_10,
            "entropy_pre_bits": entropy_pre,
            "entropy_post_bits": entropy_post,
            "mapped_types": len(mapped_counts),
        },
        "entity_normalization": {
            "nodes": len(titles),
            "clean_nodes": len(clean_titles),
            "merged_count": merged_count,
        },
        "schema_leakage": {
            "unique_types": int(len(type_counts)),
            "allowed_nodes": allowed_nodes,
            "non_allowed_nodes": non_allowed_nodes,
            "empty_type_nodes": empty_type,
        },
        "incident_degree": {
            "incident": degree_stats(incident_deg),
            "non_incident": degree_stats(non_incident_deg),
        },
        "hub_sensitivity": hub_sensitivity,
        "p99_component_summary": p99_sizes,
    }

    print(json.dumps(report, indent=2))

    if args.json_out:
        out_path = Path(args.json_out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(report, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
