#!/usr/bin/env python3
"""Splink probabilistic ER — trains per-type models using labeled pairs.

Reads:
  - pipeline/outputs/entities.parquet  (source entities)
  - pipeline/er_prep/pairwise_labels_review.csv  (labeled pairs)
  - pipeline/er_prep/splink_config/*_config.py  (per-type settings)

Writes:
  - pipeline/er_prep/splink_output/merge_decisions.csv
  - pipeline/er_prep/splink_output/threshold_report.txt
"""

import sys
import random
from pathlib import Path
from collections import defaultdict

import duckdb
import pandas as pd

from splink import Linker, DuckDBAPI, block_on

# Reproducibility: seed DuckDB's internal RNG used by random sampling
SEED = 42

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE = Path(__file__).resolve().parent.parent  # pipeline/
ENTITIES_PATH = BASE / "outputs" / "entities.parquet"
LABELS_PATH = BASE / "er_prep" / "pairwise_labels_review.csv"
OUT_DIR = BASE / "er_prep" / "splink_output"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Import per-type configs
from splink_config import (
    bodypart_config,
    equipment_config,
    injury_config,
    location_config,
    organization_config,
)

TYPE_CONFIGS = {
    "BODY_PART": bodypart_config,
    "EQUIPMENT": equipment_config,
    "INJURY_TYPE": injury_config,
    "LOCATION": location_config,
    "ORGANIZATION": organization_config,
}

# ROOT_CAUSE_CATEGORY: skip Splink (handled by prefix-strip rules in ER execution)

# ---------------------------------------------------------------------------
# Load data
# ---------------------------------------------------------------------------
print("Loading entities...")
ent = pd.read_parquet(ENTITIES_PATH)
print(f"  {len(ent):,} entities")

print("Loading labeled pairs...")
labels = pd.read_csv(LABELS_PATH)
print(f"  {len(labels)} labeled pairs")

# ---------------------------------------------------------------------------
# Build entity ID lookup: (type, value) -> entity_id
# ---------------------------------------------------------------------------
eid_lookup = {}
for _, row in ent.iterrows():
    key = (row["entity_type"], row["value"])
    eid_lookup[key] = row["entity_id"]

# ---------------------------------------------------------------------------
# Run Splink per entity type
# ---------------------------------------------------------------------------
all_merge_decisions = []
report_lines = []


def resolve_label_pairs(type_labels, entity_type):
    """Convert text-based labels to entity ID pairs."""
    match_pairs = []
    for _, row in type_labels[type_labels["is_match"] == 1].iterrows():
        id_l = eid_lookup.get((entity_type, row["title_l"]))
        id_r = eid_lookup.get((entity_type, row["title_r"]))
        if id_l and id_r and id_l != id_r:
            match_pairs.append({"unique_id_l": id_l, "unique_id_r": id_r})
    return pd.DataFrame(match_pairs) if match_pairs else None


for entity_type, config in TYPE_CONFIGS.items():
    print(f"\n{'='*60}")
    print(f"  {entity_type}")
    print(f"{'='*60}")

    # Filter entities for this type
    type_ents = ent[ent["entity_type"] == entity_type].copy()
    if len(type_ents) < 2:
        print(f"  Skipping — only {len(type_ents)} entities")
        continue

    # Add unique_id column (required by Splink)
    type_ents = type_ents.rename(columns={"entity_id": "unique_id"})

    # Preprocess
    print(f"  Preprocessing {len(type_ents):,} entities...")
    type_ents = config.preprocess(type_ents)

    # Get labeled pairs for this type
    type_labels = labels[labels["type"] == entity_type]
    match_pairs_df = resolve_label_pairs(type_labels, entity_type)
    n_labels_match = len(match_pairs_df) if match_pairs_df is not None else 0
    n_labels_nonmatch = int((type_labels["is_match"] == 0).sum())
    print(f"  Labels: {n_labels_match} match, {n_labels_nonmatch} non-match")

    # Create Linker with seeded DuckDB connection for reproducibility
    try:
        con = duckdb.connect(database=":memory:")
        con.execute(f"SELECT setseed({SEED / 100})")  # setseed takes [0,1]
        linker = Linker(type_ents, config.settings, db_api=DuckDBAPI(con))
    except Exception as e:
        print(f"  ERROR creating Linker: {e}")
        continue

    # --- Train ---

    # Step 1: Estimate u (non-match) probabilities from random pairs
    print("  Estimating u probabilities...")
    linker.training.estimate_u_using_random_sampling(max_pairs=1_000_000)

    # Step 2: Estimate m (match) probabilities via EM
    # EM is more robust than pairwise labels (which only work when pairs
    # fall within blocking rules). We use labeled pairs for threshold
    # calibration instead.
    print("  Estimating m via EM...")
    blocking_rules = config.settings.blocking_rules_to_generate_predictions
    if blocking_rules:
        for br in blocking_rules:
            try:
                linker.training.estimate_parameters_using_expectation_maximisation(
                    br, fix_u_probabilities=True
                )
            except Exception as e:
                print(f"    EM warning for blocking rule: {e}")

    # --- Predict ---
    print("  Predicting...")
    try:
        predictions = linker.inference.predict(threshold_match_weight=0.0)
    except Exception as e:
        print(f"  ERROR predicting: {e}")
        continue

    pred_df = predictions.as_pandas_dataframe()
    print(f"  Raw predictions: {len(pred_df):,} pairs")

    if len(pred_df) == 0:
        print("  No predictions — skipping")
        continue

    # --- Apply body-part laterality filter ---
    if entity_type == "BODY_PART" and hasattr(config, "filter_laterality_conflicts"):
        # Splink predictions don't include laterality column — look it up
        lat_lookup = type_ents.set_index("unique_id")["laterality"].to_dict()
        pred_df["laterality_l"] = pred_df["unique_id_l"].map(lat_lookup).fillna("none")
        pred_df["laterality_r"] = pred_df["unique_id_r"].map(lat_lookup).fillna("none")
        before = len(pred_df)
        pred_df = config.filter_laterality_conflicts(pred_df)
        pred_df = pred_df.drop(columns=["laterality_l", "laterality_r"])
        print(f"  Laterality filter: {before} → {len(pred_df)} pairs")

    # --- Threshold calibration using labeled pairs ---
    # Evaluate predictions against ALL labeled pairs (match + non-match)
    threshold = config.AUTO_MERGE_THRESHOLD  # default

    if len(type_labels) >= 20:
        print("  Calibrating threshold from labels...")

        # Build lookup of labeled decisions
        label_decisions = {}
        for _, row in type_labels.iterrows():
            id_l = eid_lookup.get((entity_type, row["title_l"]))
            id_r = eid_lookup.get((entity_type, row["title_r"]))
            if id_l and id_r:
                label_decisions[(id_l, id_r)] = int(row["is_match"])
                label_decisions[(id_r, id_l)] = int(row["is_match"])

        # Score labeled pairs in predictions
        scored_labels = []
        for _, p in pred_df.iterrows():
            key = (p["unique_id_l"], p["unique_id_r"])
            if key in label_decisions:
                scored_labels.append({
                    "match_weight": p["match_weight"],
                    "is_match": label_decisions[key],
                })

        if len(scored_labels) >= 10:
            scored_df = pd.DataFrame(scored_labels)
            # Find threshold that maximizes F0.5 (precision-weighted).
            # Over-merging is much worse than under-merging, so we
            # penalise false positives more heavily than false negatives.
            BETA = 0.5  # F0.5 weights precision 2x over recall
            MIN_PRECISION = 0.90  # refuse to merge below this precision
            best_score, best_thresh = -1.0, threshold
            best_prec, best_rec = 0.0, 0.0
            for t in sorted(scored_df["match_weight"].unique()):
                predicted_match = scored_df["match_weight"] >= t
                tp = int((predicted_match & (scored_df["is_match"] == 1)).sum())
                fp = int((predicted_match & (scored_df["is_match"] == 0)).sum())
                fn = int((~predicted_match & (scored_df["is_match"] == 1)).sum())
                prec = tp / (tp + fp) if (tp + fp) > 0 else 0
                rec = tp / (tp + fn) if (tp + fn) > 0 else 0
                if prec < MIN_PRECISION:
                    continue  # skip thresholds with unacceptable precision
                fbeta = ((1 + BETA**2) * prec * rec /
                         (BETA**2 * prec + rec)) if (prec + rec) > 0 else 0
                if fbeta > best_score:
                    best_score = fbeta
                    best_thresh = t
                    best_prec = prec
                    best_rec = rec

            if best_score < 0:
                # No threshold achieved MIN_PRECISION — use config default
                print(f"  No threshold achieves P>={MIN_PRECISION:.0%} — using default {threshold}")
                report_lines.append(
                    f"{entity_type}: FALLBACK threshold={threshold} "
                    f"(no threshold achieved P>={MIN_PRECISION:.0%})"
                )
            else:
                threshold = best_thresh
                print(f"  Optimal threshold: {threshold:.2f} (F0.5={best_score:.3f}, P={best_prec:.3f}, R={best_rec:.3f})")
                report_lines.append(
                    f"{entity_type}: threshold={threshold:.2f}, F0.5={best_score:.3f}, "
                    f"P={best_prec:.3f}, R={best_rec:.3f}, "
                    f"labeled_pairs_scored={len(scored_labels)}"
                )
        else:
            print(f"  Only {len(scored_labels)} labeled pairs found in predictions — using default threshold {threshold}")
            report_lines.append(f"{entity_type}: using default threshold={threshold} (insufficient overlap)")
    else:
        print(f"  Insufficient labels ({len(type_labels)}) — using default threshold {threshold}")
        report_lines.append(f"{entity_type}: using default threshold={threshold} (insufficient labels)")

    # --- Cluster ---
    print(f"  Clustering at threshold {threshold:.2f}...")
    try:
        clusters = linker.clustering.cluster_pairwise_predictions_at_threshold(
            predictions, threshold_match_weight=threshold
        )
        cluster_df = clusters.as_pandas_dataframe()
    except Exception as e:
        print(f"  ERROR clustering: {e}")
        continue

    # Build merge mapping: cluster_id -> list of entity_ids
    # Reject clusters that are too large (transitive chains = noise)
    MAX_CLUSTER_SIZE = 10
    cluster_groups = cluster_df.groupby("cluster_id")["unique_id"].apply(list)
    n_clusters = 0
    n_entities_merged = 0
    n_rejected_clusters = 0

    for cluster_id, members in cluster_groups.items():
        if len(members) <= 1:
            continue
        if len(members) > MAX_CLUSTER_SIZE:
            n_rejected_clusters += 1
            continue
        n_clusters += 1
        n_entities_merged += len(members) - 1
        # Canonical = first member (Splink picks by cluster representative)
        canonical = members[0]
        for m in members[1:]:
            all_merge_decisions.append({
                "entity_type": entity_type,
                "entity_id": m,
                "canonical_id": canonical,
                "cluster_id": cluster_id,
            })

    print(f"  Clusters with merges: {n_clusters}")
    print(f"  Entities to merge: {n_entities_merged}")
    if n_rejected_clusters:
        print(f"  Clusters rejected (>{MAX_CLUSTER_SIZE} members): {n_rejected_clusters}")

# ---------------------------------------------------------------------------
# Save results
# ---------------------------------------------------------------------------
print(f"\n{'='*60}")
print("RESULTS")
print(f"{'='*60}")

merge_df = pd.DataFrame(all_merge_decisions)
merge_df.to_csv(OUT_DIR / "merge_decisions.csv", index=False)
print(f"Total merge decisions: {len(merge_df)}")

if merge_df.empty:
    print("No merges found.")
else:
    per_type = merge_df.groupby("entity_type").size()
    for t, c in per_type.items():
        print(f"  {t}: {c} entities to merge")

# Save threshold report
with open(OUT_DIR / "threshold_report.txt", "w") as f:
    f.write("Splink Threshold Calibration Report\n")
    f.write("=" * 50 + "\n\n")
    for line in report_lines:
        f.write(line + "\n")

print(f"\nOutputs in {OUT_DIR}")
