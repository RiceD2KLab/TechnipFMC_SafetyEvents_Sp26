#!/usr/bin/env python3
"""
Enhanced Splink pilot with weak labels and domain-specific comparison features.

Extends splink_pilot.py with richer entity features: stopword-removed title
(title_nostop), org-suffix-stripped title (org_norm), extracted numeric tokens
(num_tokens), measurement unit tokens (unit_tokens), and equipment class from a
keyword taxonomy (equip_class). Blocking adds type+equip_class in addition to
type+first_token. Uses weak positive labels from label_pairs.py to train
m-probabilities via estimate_m_from_pairwise_labels when labels are available.
Outputs cluster statistics per threshold.

Key findings: domain features (equipment class, numeric tokens, unit tokens)
meaningfully improve linkage quality over raw Jaro-Winkler on titles alone;
the labeled training approach produces more calibrated match probabilities than
unsupervised EM on this dataset.

Decision: informed the labeled Splink approach as the preferred path for
production ER; the equipment taxonomy and feature engineering patterns here
were adopted as the standard feature set for any future ER model iteration.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List

import pandas as pd

from splink import Linker
from splink.internals.settings_creator import SettingsCreator
from splink.comparison_library import JaroWinklerAtThresholds, ExactMatch
from splink.internals.blocking_rule_library import block_on
from splink.internals.duckdb.database_api import DuckDBAPI


STOPWORDS = {
    "THE", "A", "AN", "OF", "TO", "IN", "ON", "FOR", "AND", "OR", "WITH",
    "AT", "BY", "FROM", "AS", "IS", "ARE", "WAS", "WERE", "BE", "BEEN",
    "THIS", "THAT", "THESE", "THOSE", "DURING", "AFTER", "BEFORE",
}

ORG_SUFFIXES = {
    "INC", "INC.", "LTD", "LTD.", "LLC", "LLC.", "CORP", "CORP.", "CO", "CO.",
    "COMPANY", "PLC", "BV", "SA", "SRL", "GMBH", "NV", "AG", "AB", "AS",
}

DEFAULT_TAXONOMY = {
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

UNITS = {
    "MM", "CM", "M", "KM", "IN", "FT", "LBS", "LB", "KG", "G", "TON", "T",
    "PSI", "BAR", "KPA", "MPA",
}


def normalize_text(text: str) -> str:
    text = text.upper()
    text = "".join(ch if (ch.isalnum() or ch.isspace()) else " " for ch in text)
    return " ".join(text.split())


def extract_numbers(text: str) -> str:
    nums = [tok for tok in text.split() if tok.isdigit()]
    return " ".join(nums)

def remove_stopwords(text: str) -> str:
    toks = [t for t in text.split() if t not in STOPWORDS]
    return " ".join(toks)

def normalize_org(text: str) -> str:
    toks = [t for t in text.split() if t not in ORG_SUFFIXES]
    return " ".join(toks)

def extract_units(text: str) -> str:
    toks = [t for t in text.split() if t in UNITS]
    return " ".join(toks)

def load_taxonomy(path: str | None) -> dict:
    if not path:
        return DEFAULT_TAXONOMY
    p = Path(path)
    if not p.exists():
        return DEFAULT_TAXONOMY
    import json
    return json.loads(p.read_text(encoding="utf-8"))


def extract_equipment_class(text: str, taxonomy: dict) -> str:
    for cls, kws in taxonomy.items():
        for kw in kws:
            if kw in text:
                return cls
    return ""

def cluster_stats(cluster_ids: List[str]) -> Dict[str, float]:
    from collections import Counter

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


def main() -> None:
    parser = argparse.ArgumentParser(description="Splink pilot using weak labels.")
    parser.add_argument("--entities", default="graphRAG/output_schema_only/entities.parquet")
    parser.add_argument("--labels", default="eda/pairwise_labels_weak.csv")
    parser.add_argument("--sample-size", type=int, default=30000)
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--thresholds", default="0.9,0.8")
    parser.add_argument("--json-out", default="eda/splink_pilot_labeled.json")
    parser.add_argument("--taxonomy", default="eda/equipment_taxonomy.json")
    args = parser.parse_args()

    ents = pd.read_parquet(args.entities)
    ents = ents.copy()
    ents["title"] = ents["title"].astype(str).str.strip()
    ents["type"] = ents["type"].astype(str).str.strip()
    ents["title_norm"] = ents["title"].map(normalize_text)
    ents["title_nostop"] = ents["title_norm"].map(remove_stopwords)
    ents["org_norm"] = ents["title_norm"].map(normalize_org)
    ents["first_token"] = ents["title_norm"].str.split().str[0].fillna("")
    ents["num_tokens"] = ents["title_norm"].map(extract_numbers)
    ents["unit_tokens"] = ents["title_norm"].map(extract_units)
    taxonomy = load_taxonomy(args.taxonomy)
    ents["equip_class"] = ents["title_norm"].map(lambda t: extract_equipment_class(t, taxonomy))
    ents["unique_id"] = ents["id"].astype(str)

    if args.sample_size > 0 and args.sample_size < len(ents):
        sample = ents.sample(n=args.sample_size, random_state=args.seed).copy()
    else:
        sample = ents.copy()

    # Load weak labels and filter to sample
    labels = pd.read_csv(args.labels)
    sample_ids = set(sample["unique_id"])
    labels = labels[
        labels["unique_id_l"].isin(sample_ids) & labels["unique_id_r"].isin(sample_ids)
    ].copy()

    settings = SettingsCreator(
        link_type="dedupe_only",
        comparisons=[
            JaroWinklerAtThresholds("title_norm", [0.95, 0.9, 0.85]),
            JaroWinklerAtThresholds("title_nostop", [0.95, 0.9]),
            JaroWinklerAtThresholds("org_norm", [0.95, 0.9]),
            ExactMatch("num_tokens"),
            ExactMatch("unit_tokens"),
            ExactMatch("equip_class"),
        ],
        blocking_rules_to_generate_predictions=[
            block_on("type", "first_token"),
            block_on("type", "equip_class"),
            block_on("type"),
        ],
        unique_id_column_name="unique_id",
    )

    linker = Linker(sample, settings, DuckDBAPI())
    linker.training.estimate_u_using_random_sampling(max_pairs=1_000_000)

    # Use weak labels to estimate m if available
    if len(labels) > 0:
        linker.table_management.register_table(labels, "labels", overwrite=True)
        linker.training.estimate_m_from_pairwise_labels("labels")

    thresholds = [float(t.strip()) for t in args.thresholds.split(",") if t.strip()]
    results = {}

    # For each threshold, compute clusters + stats
    for thr in thresholds:
        preds = linker.inference.predict(threshold_match_probability=thr)
        pred_df = preds.as_pandas_dataframe()
        clusters = linker.clustering.cluster_pairwise_predictions_at_threshold(preds, thr)
        clusters_df = clusters.as_pandas_dataframe()

        stats = cluster_stats(list(clusters_df["cluster_id"]))
        results[str(thr)] = {
            "pairwise_predictions": len(pred_df),
            "cluster_stats": stats,
        }

    out = {
        "sample_size": len(sample),
        "labels_used": len(labels),
        "thresholds": thresholds,
        "results": results,
    }

    out_path = Path(args.json_out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
