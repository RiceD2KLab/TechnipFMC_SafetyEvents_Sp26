#!/usr/bin/env python3
"""Pre-ER cleanup: garbage filter, multi-type resolution, merge candidates.

Reads from pipeline_v2/outputs/ (does not modify).
Writes to pipeline_v2/er_prep/.
"""

import re
from pathlib import Path

import pandas as pd

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE = Path(__file__).resolve().parent.parent  # pipeline_v2/
OUT_DIR = BASE / "er_prep"
OUT_DIR.mkdir(exist_ok=True)

ENTITIES_PATH = BASE / "outputs" / "entities.parquet"
RELATIONS_PATH = BASE / "outputs" / "relations.parquet"
GLINER_PATH = BASE / "outputs" / "gliner_extractions.parquet"

# ---------------------------------------------------------------------------
# Load data
# ---------------------------------------------------------------------------
print("Loading data...")
ent = pd.read_parquet(ENTITIES_PATH)
rel = pd.read_parquet(RELATIONS_PATH)
gli = pd.read_parquet(GLINER_PATH)

print(f"  Entities: {len(ent):,}  Relations: {len(rel):,}  GLiNER spans: {len(gli):,}")

# Precompute degree (source + target appearances)
degree_source = rel["source"].value_counts()
degree_target = rel["target"].value_counts()
degree = degree_source.add(degree_target, fill_value=0).astype(int)
degree.name = "degree"
ent = ent.merge(degree.rename("degree"), left_on="entity_id", right_index=True, how="left")
ent["degree"] = ent["degree"].fillna(0).astype(int)

# =========================================================================
# Part A: Garbage Entity Filter
# =========================================================================
print("\n=== Part A: Garbage Entity Filter ===")

STOP_WORDS = {
    "a", "an", "the", "and", "or", "but", "is", "was", "were", "are",
    "be", "been", "being", "have", "has", "had", "do", "does", "did",
    "will", "would", "shall", "should", "may", "might", "can", "could",
    "we", "he", "she", "it", "they", "them", "his", "her", "its", "our",
    "to", "of", "in", "on", "at", "for", "with", "by", "from",
    "so", "no", "not", "yes",
}

KNOWN_ABBREVIATIONS = {"HP", "IP", "UK", "US", "UV", "AC", "DC", "CO", "H2", "O2", "ER", "BP", "DP"}

# Exclude INCIDENT and ROOT_CAUSE_CATEGORY
mask_eligible = ~ent["entity_type"].isin(["INCIDENT", "ROOT_CAUSE_CATEGORY"])
candidates = ent[mask_eligible].copy()

garbage_rows = []


def flag(row, category):
    garbage_rows.append({
        "entity_id": row["entity_id"],
        "entity_type": row["entity_type"],
        "value": row["value"],
        "garbage_category": category,
        "degree": row["degree"],
    })


for _, row in candidates.iterrows():
    val = str(row["value"]).strip()
    val_upper = val.upper()

    # 1. Single-character
    if len(val) == 1:
        flag(row, "single_char")
        continue

    # 2. Numeric-only
    if re.match(r"^\d+\.?\d*$", val):
        flag(row, "numeric_only")
        continue

    # 3. Stop words
    if val.lower() in STOP_WORDS:
        flag(row, "stop_word")
        continue

    # 4. Very short non-abbreviation (≤2 chars, not in known list)
    if len(val) <= 2 and val_upper not in KNOWN_ABBREVIATIONS:
        flag(row, "short_non_abbreviation")
        continue

garbage_df = pd.DataFrame(garbage_rows)

# Compute edges_affected for each garbage entity
if len(garbage_df) > 0:
    garbage_ids = set(garbage_df["entity_id"])
    edges_affected_map = {}
    for eid in garbage_ids:
        n = int(((rel["source"] == eid) | (rel["target"] == eid)).sum())
        edges_affected_map[eid] = n
    garbage_df["edges_affected"] = garbage_df["entity_id"].map(edges_affected_map)
else:
    garbage_df["edges_affected"] = []

garbage_df.to_csv(OUT_DIR / "garbage_entities.csv", index=False)

total_edges_affected = garbage_df["edges_affected"].sum() if len(garbage_df) > 0 else 0
print(f"  Flagged: {len(garbage_df):,} entities")
print(f"  Edges affected: {total_edges_affected:,}")
print(f"  By category: {garbage_df['garbage_category'].value_counts().to_dict() if len(garbage_df) > 0 else {}}")

# =========================================================================
# Part B: Multi-Type Resolution
# =========================================================================
print("\n=== Part B: Multi-Type Resolution ===")

# Find values appearing under multiple entity types
value_types = ent.groupby("value")["entity_type"].apply(set).reset_index()
multi_type = value_types[value_types["entity_type"].apply(len) >= 2].copy()
print(f"  Values with 2+ types: {len(multi_type):,}")

# Count occurrences per (value, type) across edges
# An entity's "occurrence count" = its degree
value_type_count = ent.groupby(["value", "entity_type"])["degree"].sum().reset_index()
value_type_count.columns = ["value", "entity_type", "edge_count"]

resolution_rows = []
manual_review_rows = []

for _, row in multi_type.iterrows():
    val = row["value"]
    types_found = row["entity_type"]

    # Get counts per type
    subset = value_type_count[value_type_count["value"] == val].copy()
    subset = subset.sort_values("edge_count", ascending=False)

    total_count = subset["edge_count"].sum()
    if total_count == 0:
        # Zero-degree entities — use entity count instead of edge count
        entity_counts = ent[ent["value"] == val].groupby("entity_type").size().reset_index(name="edge_count")
        entity_counts.columns = ["entity_type", "edge_count"]
        subset = entity_counts.sort_values("edge_count", ascending=False)
        total_count = subset["edge_count"].sum()

    top_type = subset.iloc[0]["entity_type"]
    top_count = subset.iloc[0]["edge_count"]
    top_pct = top_count / total_count if total_count > 0 else 0

    # Confidence
    if top_pct > 0.80:
        confidence = "high"
    elif top_pct > 0.50:
        confidence = "moderate"
    else:
        confidence = "ambiguous"

    count_per_type = "; ".join(f"{r['entity_type']}={int(r['edge_count'])}" for _, r in subset.iterrows())

    # Count entities to reclassify (those NOT in canonical type)
    minority_entities = ent[(ent["value"] == val) & (ent["entity_type"] != top_type)]
    entities_to_reclassify = len(minority_entities)

    # Edges affected by reclassification
    minority_ids = set(minority_entities["entity_id"])
    edges_aff = int(((rel["source"].isin(minority_ids)) | (rel["target"].isin(minority_ids))).sum())

    rec = {
        "value": val,
        "canonical_type": top_type,
        "confidence": confidence,
        "types_found": "; ".join(sorted(types_found)),
        "count_per_type": count_per_type,
        "entities_to_reclassify": entities_to_reclassify,
        "edges_affected": edges_aff,
    }

    resolution_rows.append(rec)

    if confidence == "ambiguous":
        manual_review_rows.append(rec)

resolution_df = pd.DataFrame(resolution_rows)
resolution_df = resolution_df.sort_values("edges_affected", ascending=False)
resolution_df.to_csv(OUT_DIR / "multitype_resolution.csv", index=False)

manual_df = pd.DataFrame(manual_review_rows)
manual_df = manual_df.sort_values("edges_affected", ascending=False)
manual_df.to_csv(OUT_DIR / "manual_review_needed.csv", index=False)

print(f"  Resolved: {len(resolution_df):,} values")
print(f"  High confidence: {(resolution_df['confidence'] == 'high').sum():,}")
print(f"  Moderate confidence: {(resolution_df['confidence'] == 'moderate').sum():,}")
print(f"  Ambiguous (manual review): {len(manual_df):,}")

# =========================================================================
# Part C: ER Merge Candidate Report
# =========================================================================
print("\n=== Part C: ER Merge Candidate Report ===")

# Use jellyfish if available, otherwise fallback to difflib
try:
    from jellyfish import jaro_winkler_similarity as jw_sim
except ImportError:
    try:
        from rapidfuzz.distance import JaroWinkler
        def jw_sim(a, b):
            return JaroWinkler.similarity(a, b)
    except ImportError:
        from difflib import SequenceMatcher
        def jw_sim(a, b):
            """Approximate Jaro-Winkler using SequenceMatcher."""
            return SequenceMatcher(None, a, b).ratio()

LATERALITY_TOKENS = {"left", "right"}
ORDINAL_TOKENS = {"index", "middle", "ring"}
SEVERITY_QUALIFIERS = {"minor", "small", "slight", "mild", "severe", "major", "deep", "superficial"}
LEGAL_SUFFIXES = {"PLC", "INC", "INC.", "LLC", "LTD", "LTD.", "S.A.", "AG", "GMBH"}
ABBREVIATION_MAP = {"TFMC": "TECHNIPFMC"}


def normalize_base(val):
    """Lowercase, strip, remove trailing 's'."""
    v = val.lower().strip()
    if len(v) > 3 and v.endswith("s") and not v.endswith("ss"):
        v = v[:-1]
    return v


def normalize_equipment(val):
    v = normalize_base(val)
    return v, v[:3] if len(v) >= 3 else v


def normalize_body_part(val):
    tokens = val.lower().strip().split()
    stripped = [t for t in tokens if t not in LATERALITY_TOKENS and t not in ORDINAL_TOKENS]
    base = " ".join(stripped) if stripped else val.lower().strip()
    base = normalize_base(base)
    return base, base[:3] if len(base) >= 3 else base


def normalize_injury(val):
    tokens = val.lower().strip().split()
    stripped = [t for t in tokens if t not in SEVERITY_QUALIFIERS]
    # Also strip trailing "injury"
    if len(stripped) > 1 and stripped[-1] == "injury":
        stripped = stripped[:-1]
    base = " ".join(stripped) if stripped else val.lower().strip()
    base = normalize_base(base)
    return base, base[:3] if len(base) >= 3 else base


def normalize_organization(val):
    tokens = val.upper().strip().split()
    stripped = [t for t in tokens if t not in LEGAL_SUFFIXES]
    v = " ".join(stripped).strip()
    # Apply abbreviation expansion
    for abbr, full in ABBREVIATION_MAP.items():
        if v == abbr:
            v = full
    return v, v[:5] if len(v) >= 5 else v


def normalize_location(val, granularity=None):
    v = str(val).strip()
    # Strip zObsolete prefix
    if v.lower().startswith("zobsolete"):
        v = re.sub(r"^zObsolete\s*[-–—]\s*", "", v, flags=re.IGNORECASE).strip()
    v_lower = v.lower()
    gran = str(granularity) if pd.notna(granularity) else "unk"
    block = gran + "_" + (v_lower[:3] if len(v_lower) >= 3 else v_lower)
    return v_lower, block


# Build merge candidates per entity type
merge_rows = []

# Map entity_id -> (value, degree, entity_type) - granularity only for LOCATION
# Note: ent_lookup is currently unused but kept for potential future use
if "granularity" in ent.columns:
    ent_lookup = ent.set_index("entity_id")[["value", "degree", "entity_type", "granularity"]].to_dict("index")
else:
    ent_lookup = ent.set_index("entity_id")[["value", "degree", "entity_type"]].to_dict("index")

TYPE_CONFIGS = {
    "EQUIPMENT": {"normalizer": normalize_equipment, "threshold": 0.85},
    "BODY_PART": {"normalizer": normalize_body_part, "threshold": 0.85},
    "INJURY_TYPE": {"normalizer": normalize_injury, "threshold": 0.85},
    "ORGANIZATION": {"normalizer": normalize_organization, "threshold": 0.85},
    "LOCATION": {"normalizer": normalize_location, "threshold": 0.85},
}

for etype, cfg in TYPE_CONFIGS.items():
    print(f"  Processing {etype}...")
    type_ents = ent[ent["entity_type"] == etype].copy()

    if etype == "LOCATION":
        # Normalize with granularity
        # Use .get() with default None for safety, but granularity should exist for LOCATION entities
        if "granularity" in type_ents.columns:
            type_ents["normalized"] = type_ents.apply(
                lambda r: normalize_location(r["value"], r.get("granularity", None))[0], axis=1
            )
            type_ents["block_key"] = type_ents.apply(
                lambda r: normalize_location(r["value"], r.get("granularity", None))[1], axis=1
            )
        else:
            # Fallback if granularity column missing (shouldn't happen for LOCATION)
            type_ents["normalized"] = type_ents["value"].apply(lambda v: normalize_location(v, None)[0])
            type_ents["block_key"] = type_ents["value"].apply(lambda v: normalize_location(v, None)[1])
    else:
        norms = type_ents["value"].apply(cfg["normalizer"])
        type_ents["normalized"] = norms.apply(lambda x: x[0])
        type_ents["block_key"] = norms.apply(lambda x: x[1])

    # Group by block_key and compare within blocks
    blocks = type_ents.groupby("block_key")
    type_pairs = 0

    for block_key, group in blocks:
        if len(group) < 2:
            continue
        items = group[["entity_id", "value", "degree", "normalized"]].values.tolist()
        for i in range(len(items)):
            for j in range(i + 1, len(items)):
                id_a, val_a, deg_a, norm_a = items[i]
                id_b, val_b, deg_b, norm_b = items[j]

                # Skip if same normalized form AND same value (exact dups are trivial)
                if val_a == val_b:
                    continue

                sim = jw_sim(norm_a, norm_b)
                if sim >= cfg["threshold"]:
                    # Determine merge rule
                    if norm_a == norm_b:
                        rule = "exact_normalized"
                    elif sim >= 0.95:
                        rule = "near_exact"
                    else:
                        rule = "jaro_winkler"

                    # Special rules for BODY_PART
                    if etype == "BODY_PART":
                        a_tokens = set(val_a.lower().split())
                        b_tokens = set(val_b.lower().split())
                        if a_tokens & LATERALITY_TOKENS != b_tokens & LATERALITY_TOKENS:
                            if a_tokens & LATERALITY_TOKENS and b_tokens & LATERALITY_TOKENS:
                                # "left hand" vs "right hand" — skip
                                continue
                            rule = "laterality_strip"

                    if etype == "INJURY_TYPE":
                        a_tokens = set(val_a.lower().split())
                        b_tokens = set(val_b.lower().split())
                        if a_tokens & SEVERITY_QUALIFIERS != b_tokens & SEVERITY_QUALIFIERS:
                            rule = "severity_strip"

                    if etype == "ORGANIZATION":
                        a_upper = val_a.upper().split()
                        b_upper = val_b.upper().split()
                        a_stripped = set(a_upper) - LEGAL_SUFFIXES
                        b_stripped = set(b_upper) - LEGAL_SUFFIXES
                        if a_stripped == b_stripped and set(a_upper) != set(b_upper):
                            rule = "legal_suffix_strip"

                    if etype == "LOCATION":
                        if val_a.lower().startswith("zobsolete") or val_b.lower().startswith("zobsolete"):
                            rule = "obsolete_prefix"

                    merge_rows.append({
                        "entity_type": etype,
                        "entity_a_id": id_a,
                        "entity_a_value": val_a,
                        "entity_a_degree": deg_a,
                        "entity_b_id": id_b,
                        "entity_b_value": val_b,
                        "entity_b_degree": deg_b,
                        "similarity_score": round(sim, 4),
                        "merge_rule": rule,
                    })
                    type_pairs += 1

    print(f"    → {type_pairs:,} merge candidates")

# Also add ROOT_CAUSE_CATEGORY merge candidates
print("  Processing ROOT_CAUSE_CATEGORY...")
rcc_ents = ent[ent["entity_type"] == "ROOT_CAUSE_CATEGORY"].copy()
rcc_pairs = 0
rcc_items = rcc_ents[["entity_id", "value", "degree"]].values.tolist()
for i in range(len(rcc_items)):
    for j in range(i + 1, len(rcc_items)):
        id_a, val_a, deg_a = rcc_items[i]
        id_b, val_b, deg_b = rcc_items[j]
        if val_a == val_b:
            continue
        # Check if one is a substring/prefix of the other
        va_lower = val_a.lower().strip()
        vb_lower = val_b.lower().strip()
        sim = jw_sim(va_lower, vb_lower)
        # Also check if one contains the other (e.g., "Equipment condition" in "Mechanical - Equipment condition")
        is_substring = va_lower in vb_lower or vb_lower in va_lower
        if sim >= 0.80 or is_substring:
            rule = "substring_match" if is_substring else "jaro_winkler"
            merge_rows.append({
                "entity_type": "ROOT_CAUSE_CATEGORY",
                "entity_a_id": id_a,
                "entity_a_value": val_a,
                "entity_a_degree": deg_a,
                "entity_b_id": id_b,
                "entity_b_value": val_b,
                "entity_b_degree": deg_b,
                "similarity_score": round(sim, 4),
                "merge_rule": rule,
            })
            rcc_pairs += 1
print(f"    → {rcc_pairs:,} merge candidates")

merge_df = pd.DataFrame(merge_rows)
merge_df = merge_df.sort_values(["entity_type", "similarity_score"], ascending=[True, False])
merge_df.to_csv(OUT_DIR / "merge_candidates.csv", index=False)
print(f"  Total merge candidates: {len(merge_df):,}")

# Priority ranking: top 50 by combined degree
if len(merge_df) > 0:
    merge_df["combined_degree"] = merge_df["entity_a_degree"] + merge_df["entity_b_degree"]
    priorities = merge_df.nlargest(50, "combined_degree")
    priorities.to_csv(OUT_DIR / "merge_priorities.csv", index=False)
    print(f"  Top 50 priority merges saved")
else:
    pd.DataFrame().to_csv(OUT_DIR / "merge_priorities.csv", index=False)

# =========================================================================
# Summary stats for reporting
# =========================================================================
print("\n=== Summary ===")
print(f"  Garbage entities: {len(garbage_df):,} ({total_edges_affected:,} edges affected)")
print(f"  Multi-type values: {len(resolution_df):,} resolved, {len(manual_df):,} need manual review")
if len(merge_df) > 0:
    per_type = merge_df.groupby("entity_type").size()
    print(f"  Merge candidates per type:")
    for t, c in per_type.items():
        print(f"    {t}: {c:,}")
print("\nDone. Outputs in pipeline_v2/er_prep/")
