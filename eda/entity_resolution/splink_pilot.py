#!/usr/bin/env python3
"""
Probabilistic record linkage feasibility pilot using Splink (DuckDB backend).

Runs Splink deduplication on a random sample of up to 30,000 entities using
Jaro-Winkler similarity on normalized titles. Blocking rules are conservative:
type + first_char and type + first_token. Estimates u-probabilities via random
sampling and m-probabilities via EM. For each match-probability threshold,
reports cluster statistics and degree lift by remapping relationship edges to
cluster representatives. Uses DuckDB backend (no Spark dependency).

Key findings: conservative blocking produced very few candidate pairs; only 56
entities were absorbed into clusters at the primary threshold, demonstrating
that text similarity alone with type+first_token blocking is insufficient to
detect the full set of duplicates in this dataset.

Decision: demonstrated that blocking strategy needs domain-specific features
beyond text similarity; motivated the enhanced splink_pilot_labeled.py which
adds equipment class, numeric tokens, and unit tokens as additional comparison
features.
"""

from __future__ import annotations

import argparse
import json
import math
import random
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, List, Tuple

import pandas as pd

from splink import Linker
from splink.internals.settings_creator import SettingsCreator
from splink.comparison_library import JaroWinklerAtThresholds
from splink.internals.blocking_rule_library import block_on, CustomRule
from splink.internals.duckdb.database_api import DuckDBAPI


def normalize_text(text: str) -> str:
    text = text.upper()
    text = "".join(ch if (ch.isalnum() or ch.isspace()) else " " for ch in text)
    return " ".join(text.split())


def build_sample(df: pd.DataFrame, sample_size: int, seed: int) -> pd.DataFrame:
    if sample_size <= 0 or sample_size >= len(df):
        return df.copy()
    return df.sample(n=sample_size, random_state=seed).copy()


def cluster_stats(cluster_ids: List[int]) -> Dict[str, float]:
    counts = Counter(cluster_ids)
    sizes = list(counts.values())
    if not sizes:
        return {}
    sizes.sort()
    clusters_gt1 = [s for s in sizes if s > 1]
    merged = sum(s - 1 for s in sizes)
    return {
        "clusters": len(sizes),
        "clusters_gt1": len(clusters_gt1),
        "entities_in_clusters_gt1": sum(clusters_gt1),
        "avg_cluster_size": sum(sizes) / len(sizes),
        "median_cluster_size": sizes[len(sizes) // 2],
        "max_cluster_size": sizes[-1],
        "merged_entities": merged,
    }


def estimate_degree_lift(
    rels: pd.DataFrame, sample_nodes: set, node_to_cluster: Dict[str, int]
) -> Dict[str, float]:
    # Filter edges to sample nodes
    rels_s = rels[rels["source"].isin(sample_nodes) & rels["target"].isin(sample_nodes)]
    if rels_s.empty:
        return {}

    # Pre-merge
    nodes_pre = set(rels_s["source"]) | set(rels_s["target"])
    edges_pre = len(rels_s)
    avg_degree_pre = edges_pre / len(nodes_pre) if nodes_pre else 0

    # Post-merge: collapse to clusters
    edges_post = set()
    for s, t in zip(rels_s["source"], rels_s["target"]):
        cs = node_to_cluster.get(s)
        ct = node_to_cluster.get(t)
        if cs is None or ct is None:
            continue
        if cs == ct:
            continue
        edges_post.add((cs, ct) if cs < ct else (ct, cs))

    nodes_post = set(node_to_cluster.values())
    avg_degree_post = len(edges_post) / len(nodes_post) if nodes_post else 0

    return {
        "edges_pre": edges_pre,
        "nodes_pre": len(nodes_pre),
        "avg_degree_pre": avg_degree_pre,
        "edges_post": len(edges_post),
        "nodes_post": len(nodes_post),
        "avg_degree_post": avg_degree_post,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Splink pilot on entity titles.")
    parser.add_argument("--entities", default="fall2025/graphRAG/output_schema_only/entities.parquet")
    parser.add_argument("--relations", default="fall2025/graphRAG/output_schema_only/relationships.parquet")
    parser.add_argument("--sample-size", type=int, default=30000)
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--thresholds", default="0.95,0.90")
    parser.add_argument("--blocking-all", action="store_true", help="Use a full cross-join blocking rule (1=1) for tiny samples.")
    parser.add_argument("--json-out", default="eda/splink_pilot.json")
    args = parser.parse_args()

    ents = pd.read_parquet(args.entities)
    rels = pd.read_parquet(args.relations)

    # Build normalized fields
    ents = ents.copy()
    ents["title"] = ents["title"].astype(str).str.strip()
    ents["type"] = ents["type"].astype(str).str.strip()
    ents["title_norm"] = ents["title"].map(normalize_text)
    ents["first_char"] = ents["title_norm"].str[:1]
    ents["first_token"] = ents["title_norm"].str.split().str[0].fillna("")
    ents["unique_id"] = ents["id"].astype(str)

    # Sample
    sample_df = build_sample(ents, args.sample_size, args.seed)

    # Splink settings
    blocking_rules = [
        block_on("type", "first_char"),
        block_on("type", "first_token"),
        block_on("type"),
    ]
    if args.blocking_all:
        blocking_rules = [CustomRule("1=1")]

    settings = SettingsCreator(
        link_type="dedupe_only",
        comparisons=[
            JaroWinklerAtThresholds("title_norm", [0.95, 0.90, 0.85]),
        ],
        blocking_rules_to_generate_predictions=blocking_rules,
        unique_id_column_name="unique_id",
    )

    linker = Linker(sample_df, settings, DuckDBAPI())

    # Train (approximate)
    linker.training.estimate_u_using_random_sampling(max_pairs=1_000_000)
    linker.training.estimate_parameters_using_expectation_maximisation(
        blocking_rule=blocking_rules[0]
    )

    thresholds = [float(t.strip()) for t in args.thresholds.split(",") if t.strip()]
    results = {}

    sample_nodes = set(sample_df["title"])
    # Map for degree-lift estimation
    title_by_id = dict(zip(sample_df["unique_id"], sample_df["title"]))

    for thr in thresholds:
        preds = linker.inference.predict(threshold_match_probability=thr)
        pred_df = preds.as_pandas_dataframe()

        clusters = linker.clustering.cluster_pairwise_predictions_at_threshold(preds, thr)
        clusters_df = clusters.as_pandas_dataframe()

        # Build node->cluster mapping by title
        node_to_cluster = {}
        for _, row in clusters_df.iterrows():
            node = title_by_id.get(str(row["unique_id"]))
            if node is None:
                continue
            node_to_cluster[node] = str(row["cluster_id"])

        stats = cluster_stats(list(node_to_cluster.values()))
        lift = estimate_degree_lift(rels, sample_nodes, node_to_cluster)

        results[str(thr)] = {
            "pairwise_predictions": len(pred_df),
            "cluster_stats": stats,
            "degree_lift_sample": lift,
        }

    out = {
        "sample_size": len(sample_df),
        "unique_types": sample_df["type"].nunique(),
        "blocking_all": bool(args.blocking_all),
        "thresholds": thresholds,
        "results": results,
    }

    out_path = Path(args.json_out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
