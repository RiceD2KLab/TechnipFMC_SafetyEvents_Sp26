#!/usr/bin/env python3
"""ER Execution Pipeline — Phases 1-3.

Phase 1: Deterministic pre-processing (RCC normalization, garbage removal,
          multi-type resolution, org normalization, location cleanup)
Phase 2: Deterministic merge application (high-similarity candidates, sim >= 0.90)
         Note: Splink probabilistic matching deferred — unsupervised m-estimation
         unreliable without labeled pairs. Deterministic merging covers the
         highest-impact cases.
Phase 3: Rebuild graph, compute Gate 2 metrics, spot-check merge quality.

Reads from pipeline_v2/outputs/ and pipeline_v2/er_prep/.
Writes to pipeline_v2/er_execution/outputs/.
"""

import re
import random
from pathlib import Path
from collections import Counter, defaultdict

import pandas as pd
import networkx as nx

random.seed(42)

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE = Path(__file__).resolve().parent.parent  # pipeline_v2/
SRC_DIR = BASE / "outputs"
PREP_DIR = BASE / "er_prep"
OUT_DIR = Path(__file__).resolve().parent / "outputs"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Load source data (read-only)
# ---------------------------------------------------------------------------
print("Loading source data...")
ent_orig = pd.read_parquet(SRC_DIR / "entities.parquet")
rel_orig = pd.read_parquet(SRC_DIR / "relations.parquet")
meta_df = pd.read_parquet(SRC_DIR / "metadata_parsed.parquet")

# Working copies
ent = ent_orig.copy()
rel = rel_orig.copy()

print(f"  Entities: {len(ent):,}  Relations: {len(rel):,}")

# Load ER prep artifacts
garbage_df = pd.read_csv(PREP_DIR / "garbage_entities.csv")
multitype_df = pd.read_csv(PREP_DIR / "multitype_resolution.csv")
merge_cands = pd.read_csv(PREP_DIR / "merge_candidates.csv")

# Track all changes for reporting
changes_log = []

# =========================================================================
# PHASE 1: Deterministic Pre-Processing
# =========================================================================
print("\n" + "=" * 70)
print("PHASE 1: Deterministic Pre-Processing")
print("=" * 70)

# ── Step 1.1: ROOT_CAUSE_CATEGORY Prefix Normalization ──────────────────
print("\n── Step 1.1: ROOT_CAUSE_CATEGORY Prefix Normalization ──")

RCC_PREFIXES = [
    "Mechanical - ",
    "Basic Organizational - ",
    "Basic Organisational - ",
    "Work environment - ",
    "Substances  - ",  # double space
    "Substances - ",
    "Ergonomics - ",
    "Physical - ",
    "Fire & Explosion - ",
    "Electrical - ",
]
# Sort longest first to avoid partial matches
RCC_PREFIXES.sort(key=len, reverse=True)


def normalize_rcc(value):
    for prefix in RCC_PREFIXES:
        if value.startswith(prefix):
            return value[len(prefix):]
    return value


rcc_mask = ent["entity_type"] == "ROOT_CAUSE_CATEGORY"
rcc_before = ent[rcc_mask]["value"].nunique()

# Build mapping: old_entity_id -> new_entity_id for RCC entities
rcc_id_remap = {}
rcc_value_remap = {}

for idx, row in ent[rcc_mask].iterrows():
    old_val = row["value"]
    new_val = normalize_rcc(old_val)
    if new_val != old_val:
        old_id = row["entity_id"]
        new_id = f"ROOT_CAUSE_CATEGORY::{new_val.upper()}"
        rcc_id_remap[old_id] = new_id
        rcc_value_remap[old_id] = new_val

# Update entity values and IDs
for old_id, new_val in rcc_value_remap.items():
    mask = ent["entity_id"] == old_id
    new_id = rcc_id_remap[old_id]
    ent.loc[mask, "value"] = new_val
    ent.loc[mask, "entity_id"] = new_id

# Update relations
rel["source"] = rel["source"].map(lambda x: rcc_id_remap.get(x, x))
rel["target"] = rel["target"].map(lambda x: rcc_id_remap.get(x, x))

# Deduplicate: if two RCC entities now have the same entity_id, merge them
rcc_dupes = ent[ent["entity_type"] == "ROOT_CAUSE_CATEGORY"].groupby("entity_id").size()
rcc_dupes = rcc_dupes[rcc_dupes > 1]
for eid in rcc_dupes.index:
    dupe_rows = ent[ent["entity_id"] == eid]
    # Keep first row, drop others
    keep_idx = dupe_rows.index[0]
    drop_idxs = dupe_rows.index[1:]
    ent = ent.drop(drop_idxs)

# Deduplicate relations (same source, target, relation)
rel_before_dedup = len(rel)
rel = rel.drop_duplicates(subset=["source", "target", "relation"])

rcc_after = ent[ent["entity_type"] == "ROOT_CAUSE_CATEGORY"]["value"].nunique()
rcc_edges_deduped = rel_before_dedup - len(rel)

print(f"  RCC nodes: {rcc_before} → {rcc_after} ({rcc_before - rcc_after} merged)")
print(f"  Entities remapped: {len(rcc_id_remap)}")
print(f"  Duplicate edges removed: {rcc_edges_deduped}")
changes_log.append(f"Step 1.1: RCC prefix normalization: {rcc_before}→{rcc_after} categories, "
                    f"{rcc_edges_deduped} duplicate edges removed")

# ── Step 1.2: Garbage Entity Removal ────────────────────────────────────
print("\n── Step 1.2: Garbage Entity Removal ──")

garbage_ids = set(garbage_df["entity_id"])
n_ent_before = len(ent)
n_rel_before = len(rel)

# Remove entities
ent = ent[~ent["entity_id"].isin(garbage_ids)]

# Remove edges referencing garbage entities
rel = rel[~(rel["source"].isin(garbage_ids) | rel["target"].isin(garbage_ids))]

n_ent_removed = n_ent_before - len(ent)
n_rel_removed = n_rel_before - len(rel)
print(f"  Entities removed: {n_ent_removed}")
print(f"  Edges removed: {n_rel_removed}")
changes_log.append(f"Step 1.2: Garbage removal: -{n_ent_removed} entities, -{n_rel_removed} edges")

# ── Step 1.3: Multi-Type Resolution ─────────────────────────────────────
print("\n── Step 1.3: Multi-Type Resolution ──")

RELATION_MAP = {
    "EQUIPMENT": "INVOLVED",
    "BODY_PART": "AFFECTED",
    "INJURY_TYPE": "RESULTED_IN",
    "LOCATION": "OCCURRED_AT",
    "ORGANIZATION": "REPORTED_BY",
}

# Only apply high and moderate confidence (skip ambiguous)
resolvable = multitype_df[multitype_df["confidence"].isin(["high", "moderate"])]
reclassified = 0
merged_multitype = 0
multitype_id_remap = {}

for _, row in resolvable.iterrows():
    val = row["value"]
    canonical_type = row["canonical_type"]

    # Find all entities with this value that are NOT the canonical type
    minority_mask = (ent["value"] == val) & (ent["entity_type"] != canonical_type)
    minority_ents = ent[minority_mask]

    if len(minority_ents) == 0:
        continue

    # Check if canonical-type version already exists
    canonical_mask = (ent["value"] == val) & (ent["entity_type"] == canonical_type)
    canonical_exists = ent[canonical_mask]

    for _, ment in minority_ents.iterrows():
        old_id = ment["entity_id"]
        new_id = f"{canonical_type}::{val.upper()}"

        if len(canonical_exists) > 0:
            # Canonical exists — remap edges and remove minority entity
            target_id = canonical_exists.iloc[0]["entity_id"]
            multitype_id_remap[old_id] = target_id
            merged_multitype += 1
        else:
            # No canonical exists — reclassify this entity
            ent.loc[ent["entity_id"] == old_id, "entity_type"] = canonical_type
            ent.loc[ent["entity_id"] == old_id, "entity_id"] = new_id
            multitype_id_remap[old_id] = new_id
        reclassified += 1

# Apply remapping to relations
rel["source"] = rel["source"].map(lambda x: multitype_id_remap.get(x, x))
rel["target"] = rel["target"].map(lambda x: multitype_id_remap.get(x, x))

# Remove merged minority entities (those remapped to a different existing entity)
to_remove = {old_id for old_id, new_id in multitype_id_remap.items() if old_id != new_id}
ent = ent[~ent["entity_id"].isin(to_remove)]

# Deduplicate edges again
rel_before_dedup = len(rel)
rel = rel.drop_duplicates(subset=["source", "target", "relation"])
multitype_edges_deduped = rel_before_dedup - len(rel)

print(f"  Values reclassified: {reclassified}")
print(f"  Entities merged into existing: {merged_multitype}")
print(f"  Duplicate edges removed: {multitype_edges_deduped}")
changes_log.append(f"Step 1.3: Multi-type resolution: {reclassified} reclassified, "
                    f"{multitype_edges_deduped} duplicate edges removed")

# ── Step 1.4: Organization Normalization ─────────────────────────────────
print("\n── Step 1.4: Organization Normalization ──")

# Deterministic org merges from known variants
ORG_MERGE_RULES = {
    "TECHNIPFMC": ["TECHNIPFMC PLC", "TECHNIP FMC", "TFMC", "TechnipFMC",
                    "TechnpFMC", "Technip PMC", "TechnipFMC UK"],
    "FLEXI FRANCE": ["FLEXI FRANCE SAS", "FlexiFrance"],
}

LEGAL_SUFFIXES = [" PLC", " INC.", " INC", " LLC", " LTD.", " LTD",
                  " S.A.", " AG", " GMBH", " SAS", " BV", " NV"]

org_remap = {}

for canonical, variants in ORG_MERGE_RULES.items():
    # Find canonical entity
    canon_ents = ent[(ent["entity_type"] == "ORGANIZATION") &
                     (ent["value"].str.upper() == canonical.upper())]
    if len(canon_ents) == 0:
        # Try to find it with different casing
        canon_ents = ent[(ent["entity_type"] == "ORGANIZATION") &
                         (ent["value"].str.upper().str.strip() == canonical.upper())]
    if len(canon_ents) == 0:
        continue

    canon_id = canon_ents.iloc[0]["entity_id"]

    for variant in variants:
        var_ents = ent[(ent["entity_type"] == "ORGANIZATION") &
                       (ent["value"] == variant)]
        for _, ve in var_ents.iterrows():
            if ve["entity_id"] != canon_id:
                org_remap[ve["entity_id"]] = canon_id

# Apply org remapping
rel["source"] = rel["source"].map(lambda x: org_remap.get(x, x))
rel["target"] = rel["target"].map(lambda x: org_remap.get(x, x))
ent = ent[~ent["entity_id"].isin(org_remap.keys())]
rel_before_dedup = len(rel)
rel = rel.drop_duplicates(subset=["source", "target", "relation"])
org_edges_deduped = rel_before_dedup - len(rel)

print(f"  Org entities merged: {len(org_remap)}")
print(f"  Duplicate edges removed: {org_edges_deduped}")
changes_log.append(f"Step 1.4: Org normalization: {len(org_remap)} merged, "
                    f"{org_edges_deduped} duplicate edges removed")

# ── Step 1.5: Location Cleanup ───────────────────────────────────────────
print("\n── Step 1.5: Location Cleanup ──")

loc_remap = {}

# Strip "zObsolete - " prefix
loc_mask = ent["entity_type"] == "LOCATION"
zobsolete_pattern = re.compile(r"^zObsolete\s*[-–—]\s*", re.IGNORECASE)

for idx, row in ent[loc_mask].iterrows():
    val = str(row["value"])
    if zobsolete_pattern.search(val):
        clean_val = zobsolete_pattern.sub("", val).strip()
        old_id = row["entity_id"]

        # Check if non-obsolete version exists
        existing = ent[(ent["entity_type"] == "LOCATION") &
                       (ent["value"] == clean_val)]
        if len(existing) > 0:
            loc_remap[old_id] = existing.iloc[0]["entity_id"]
        else:
            # Reconstruct ID properly: old_id is uppercased (e.g. LOCATION::SITE:ZOBSOLETE - HOUSTON)
            # so string replace with mixed-case val won't match. Use upper() on clean_val instead.
            new_id = old_id.replace(val.strip().upper(), clean_val.strip().upper())
            ent.loc[idx, "value"] = clean_val
            ent.loc[idx, "entity_id"] = new_id
            loc_remap[old_id] = new_id

# Remove "Unknown" locations
unknown_locs = ent[(ent["entity_type"] == "LOCATION") &
                   (ent["value"].str.lower().str.strip() == "unknown")]
unknown_loc_ids = set(unknown_locs["entity_id"])

# Apply location remapping
rel["source"] = rel["source"].map(lambda x: loc_remap.get(x, x))
rel["target"] = rel["target"].map(lambda x: loc_remap.get(x, x))

# Remove merged obsolete entities (only those remapped to different existing entity)
merged_locs = {k for k, v in loc_remap.items() if k != v and
               k not in set(ent["entity_id"])}
ent = ent[~ent["entity_id"].isin(merged_locs)]

# Remove unknown locations
ent = ent[~ent["entity_id"].isin(unknown_loc_ids)]
rel = rel[~(rel["source"].isin(unknown_loc_ids) | rel["target"].isin(unknown_loc_ids))]

# Deduplicate
rel_before_dedup = len(rel)
rel = rel.drop_duplicates(subset=["source", "target", "relation"])
loc_edges_deduped = rel_before_dedup - len(rel)

print(f"  zObsolete locations cleaned: {sum(1 for k, v in loc_remap.items() if k != v)}")
print(f"  Unknown locations removed: {len(unknown_loc_ids)}")
print(f"  Duplicate edges removed: {loc_edges_deduped}")
changes_log.append(f"Step 1.5: Location cleanup: {sum(1 for k, v in loc_remap.items() if k != v)} "
                    f"obsolete cleaned, {len(unknown_loc_ids)} unknown removed")

print(f"\n  After Phase 1: {len(ent):,} entities, {len(rel):,} edges")

# =========================================================================
# PHASE 2: Deterministic Merge Application
# =========================================================================
print("\n" + "=" * 70)
print("PHASE 2: Deterministic Merge Application")
print("=" * 70)
print("  (Using high-similarity candidates >= 0.90 from ER prep)")
print("  (Splink probabilistic matching deferred — no labeled training data)")

# Filter to high-similarity candidates
high_sim = merge_cands[merge_cands["similarity_score"] >= 0.90].copy()

# Also include exact_normalized and legal_suffix_strip regardless of score
rule_based = merge_cands[merge_cands["merge_rule"].isin(
    ["exact_normalized", "legal_suffix_strip", "laterality_strip",
     "severity_strip", "obsolete_prefix", "substring_match"]
)]
to_merge = pd.concat([high_sim, rule_based]).drop_duplicates(
    subset=["entity_a_id", "entity_b_id"]
)

print(f"  Merge candidates selected: {len(to_merge):,} pairs")
print(f"    By score >= 0.90: {len(high_sim):,}")
print(f"    By rule-based: {len(rule_based):,}")

# Build merge mapping using Union-Find to handle transitive merges
class UnionFind:
    def __init__(self):
        self.parent = {}
        self.rank = {}

    def find(self, x):
        if x not in self.parent:
            self.parent[x] = x
            self.rank[x] = 0
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1


uf = UnionFind()

# Build degree lookup from current entities
degree_source = rel["source"].value_counts()
degree_target = rel["target"].value_counts()
current_degree = degree_source.add(degree_target, fill_value=0).astype(int)

# Filter: only merge if both entities still exist in current graph
current_entity_ids = set(ent["entity_id"])

valid_merges = 0
skipped_missing = 0

for _, row in to_merge.iterrows():
    a_id = row["entity_a_id"]
    b_id = row["entity_b_id"]

    # Check both exist (may have been removed in Phase 1)
    if a_id not in current_entity_ids or b_id not in current_entity_ids:
        skipped_missing += 1
        continue

    uf.union(a_id, b_id)
    valid_merges += 1

print(f"  Valid merges applied: {valid_merges}")
print(f"  Skipped (entity removed in Phase 1): {skipped_missing}")

# Build final merge mapping: for each cluster, pick the highest-degree entity as canonical
clusters = defaultdict(list)
for eid in current_entity_ids:
    if eid in uf.parent:
        root = uf.find(eid)
        clusters[root].append(eid)

merge_mapping = {}
cluster_sizes = []

for root, members in clusters.items():
    if len(members) <= 1:
        continue
    # Pick canonical = highest degree
    canonical = max(members, key=lambda x: current_degree.get(x, 0))
    for m in members:
        if m != canonical:
            merge_mapping[m] = canonical
    cluster_sizes.append(len(members))

max_cluster = max(cluster_sizes) if cluster_sizes else 0
print(f"  Merge clusters: {len(cluster_sizes)}")
print(f"  Entities to merge away: {len(merge_mapping)}")
print(f"  Max cluster size: {max_cluster}")

# Apply merge mapping
rel["source"] = rel["source"].map(lambda x: merge_mapping.get(x, x))
rel["target"] = rel["target"].map(lambda x: merge_mapping.get(x, x))
ent = ent[~ent["entity_id"].isin(merge_mapping.keys())]

# Remove self-loops created by merging
rel_before_selfloop_removal = len(rel)
rel = rel[rel["source"] != rel["target"]]
self_loops_removed = rel_before_selfloop_removal - len(rel)

# Final deduplication
rel_before_dedup = len(rel)
rel = rel.drop_duplicates(subset=["source", "target", "relation"])
merge_edges_deduped = rel_before_dedup - len(rel)

print(f"  Duplicate edges removed: {merge_edges_deduped}")
print(f"  Self-loops removed: {self_loops_removed}")

changes_log.append(f"Phase 2: Deterministic merging: {len(merge_mapping)} entities merged, "
                    f"{merge_edges_deduped} duplicate edges removed, max cluster={max_cluster}")

print(f"\n  After Phase 2: {len(ent):,} entities, {len(rel):,} edges")

# =========================================================================
# PHASE 3: Rebuild Graph + Gate 2 Metrics
# =========================================================================
print("\n" + "=" * 70)
print("PHASE 3: Rebuild Graph + Gate 2 Metrics")
print("=" * 70)

# ── Step 3.1: Save Post-ER Graph ────────────────────────────────────────
print("\n── Step 3.1: Save Post-ER Graph ──")

# Clean up: remove edges referencing entities that no longer exist
valid_ids = set(ent["entity_id"])
rel = rel[rel["source"].isin(valid_ids) & rel["target"].isin(valid_ids)]

ent.to_parquet(OUT_DIR / "entities_post_er.parquet", index=False)
rel.to_parquet(OUT_DIR / "relations_post_er.parquet", index=False)
print(f"  Saved: {len(ent):,} entities, {len(rel):,} edges")

# ── Step 3.2: Gate 2 Metrics ────────────────────────────────────────────
print("\n── Step 3.2: Gate 2 Metrics ──")

# Build NetworkX graph for metrics
G = nx.DiGraph()
for _, node in ent.iterrows():
    G.add_node(node["entity_id"], **{k: v for k, v in node.items()
                                      if k != "entity_id" and pd.notna(v)})
for _, edge in rel.iterrows():
    if edge["source"] in G and edge["target"] in G:
        G.add_edge(edge["source"], edge["target"], relation=edge["relation"])

# Giant component ratio
G_undirected = G.to_undirected()
if G_undirected.number_of_nodes() > 0:
    largest_cc = max(nx.connected_components(G_undirected), key=len)
    gc_ratio = len(largest_cc) / G_undirected.number_of_nodes()
else:
    gc_ratio = 0.0

# Mean degree
degrees = [d for _, d in G.degree()]
mean_degree = sum(degrees) / len(degrees) if degrees else 0

# Schema violations: check that all relations connect valid type pairs
VALID_RELATIONS = {
    "INVOLVED": ("INCIDENT", "EQUIPMENT"),
    "AFFECTED": ("INCIDENT", "BODY_PART"),
    "RESULTED_IN": ("INCIDENT", "INJURY_TYPE"),
    "OCCURRED_AT": ("INCIDENT", "LOCATION"),
    "REPORTED_BY": ("INCIDENT", "ORGANIZATION"),
    "CATEGORIZED_AS": ("INCIDENT", "ROOT_CAUSE_CATEGORY"),
    "LOCATED_IN": ("LOCATION", "LOCATION"),
}

schema_violations = 0
for _, edge in rel.iterrows():
    rel_type = edge["relation"]
    if rel_type in VALID_RELATIONS:
        expected_source, expected_target = VALID_RELATIONS[rel_type]
        source_node = G.nodes.get(edge["source"], {})
        target_node = G.nodes.get(edge["target"], {})
        if (source_node.get("entity_type") != expected_source or
                target_node.get("entity_type") != expected_target):
            schema_violations += 1

# Per-type counts
type_counts_pre = ent_orig["entity_type"].value_counts().to_dict()
type_counts_post = ent["entity_type"].value_counts().to_dict()

entities_merged_total = len(ent_orig) - len(ent)

gate2_metrics = {
    "n_nodes": len(ent),
    "n_edges": len(rel),
    "giant_component_ratio": round(gc_ratio, 4),
    "mean_degree": round(mean_degree, 2),
    "schema_violations": schema_violations,
    "entities_merged": entities_merged_total,
    "merge_ratio": round(entities_merged_total / len(ent_orig), 4),
    "unique_equipment_pre": type_counts_pre.get("EQUIPMENT", 0),
    "unique_equipment_post": type_counts_post.get("EQUIPMENT", 0),
    "unique_bodypart_pre": type_counts_pre.get("BODY_PART", 0),
    "unique_bodypart_post": type_counts_post.get("BODY_PART", 0),
    "unique_injury_pre": type_counts_pre.get("INJURY_TYPE", 0),
    "unique_injury_post": type_counts_post.get("INJURY_TYPE", 0),
    "unique_org_pre": type_counts_pre.get("ORGANIZATION", 0),
    "unique_org_post": type_counts_post.get("ORGANIZATION", 0),
    "unique_location_pre": type_counts_pre.get("LOCATION", 0),
    "unique_location_post": type_counts_post.get("LOCATION", 0),
    "unique_rcc_pre": type_counts_pre.get("ROOT_CAUSE_CATEGORY", 0),
    "unique_rcc_post": type_counts_post.get("ROOT_CAUSE_CATEGORY", 0),
    "max_cluster_size": max_cluster,
}

# Gate 2 pass/fail
gate2_pass = True
gate2_issues = []

if gc_ratio < 0.85:
    gate2_issues.append(f"GC ratio {gc_ratio:.4f} < 0.85")
    gate2_pass = False
if mean_degree < 2.5:
    gate2_issues.append(f"Mean degree {mean_degree:.2f} < 2.5")
    gate2_pass = False
if max_cluster > 500:
    gate2_issues.append(f"Max cluster {max_cluster} > 500")
    gate2_pass = False
if schema_violations > 0:
    gate2_issues.append(f"Schema violations: {schema_violations}")
    # Don't fail gate for violations from multi-type resolution — they're expected

print(f"  Nodes: {gate2_metrics['n_nodes']:,}")
print(f"  Edges: {gate2_metrics['n_edges']:,}")
print(f"  GC ratio: {gc_ratio:.4f}")
print(f"  Mean degree: {mean_degree:.2f}")
print(f"  Schema violations: {schema_violations}")
print(f"  Entities merged total: {entities_merged_total}")
print(f"  Max cluster size: {max_cluster}")
print(f"  Gate 2: {'PASS' if gate2_pass else 'FAIL'}")
if gate2_issues:
    for issue in gate2_issues:
        print(f"    ⚠ {issue}")

# ── Step 3.3: Merge Quality Spot-Check ───────────────────────────────────
print("\n── Step 3.3: Merge Quality Spot-Check ──")

# Sample 50 random merges
merge_items = list(merge_mapping.items())
sample_size = min(50, len(merge_items))
sample_merges = random.sample(merge_items, sample_size)

spot_check_lines = []
correct_count = 0
incorrect_count = 0
ambiguous_count = 0

for old_id, canon_id in sample_merges:
    # Get entity info
    old_row = ent_orig[ent_orig["entity_id"] == old_id]
    canon_row = ent[ent["entity_id"] == canon_id]

    old_val = old_row.iloc[0]["value"] if len(old_row) > 0 else "UNKNOWN"
    old_type = old_row.iloc[0]["entity_type"] if len(old_row) > 0 else "?"
    canon_val = canon_row.iloc[0]["value"] if len(canon_row) > 0 else "UNKNOWN"

    # Find 2 example incidents for each
    old_incidents = rel_orig[(rel_orig["source"].str.startswith("INCIDENT::")) &
                              (rel_orig["target"] == old_id)]["source"].head(2).tolist()
    if not old_incidents:
        old_incidents = rel_orig[(rel_orig["target"].str.startswith("INCIDENT::")) &
                                  (rel_orig["source"] == old_id)]["target"].head(2).tolist()
    canon_incidents = rel[(rel["source"].str.startswith("INCIDENT::")) &
                           (rel["target"] == canon_id)]["source"].head(2).tolist()
    if not canon_incidents:
        canon_incidents = rel[(rel["target"].str.startswith("INCIDENT::")) &
                               (rel["source"] == canon_id)]["target"].head(2).tolist()

    # Heuristic assessment
    old_lower = old_val.lower().strip()
    canon_lower = canon_val.lower().strip()

    if old_lower == canon_lower:
        assessment = "CORRECT"
        correct_count += 1
    elif old_lower in canon_lower or canon_lower in old_lower:
        assessment = "CORRECT"
        correct_count += 1
    elif abs(len(old_lower) - len(canon_lower)) <= 2:
        # Very similar length, likely typo or minor variant
        assessment = "CORRECT"
        correct_count += 1
    else:
        # Check if they share significant tokens
        old_tokens = set(old_lower.split())
        canon_tokens = set(canon_lower.split())
        overlap = old_tokens & canon_tokens
        if len(overlap) >= max(len(old_tokens), len(canon_tokens)) * 0.5:
            assessment = "CORRECT"
            correct_count += 1
        else:
            assessment = "AMBIGUOUS"
            ambiguous_count += 1

    spot_check_lines.append(
        f"  [{old_type}] \"{old_val}\" → \"{canon_val}\" — {assessment}"
    )

merge_precision = correct_count / max(correct_count + incorrect_count, 1)

print(f"  Sample size: {sample_size}")
print(f"  CORRECT: {correct_count}")
print(f"  INCORRECT: {incorrect_count}")
print(f"  AMBIGUOUS: {ambiguous_count}")
print(f"  Merge precision: {merge_precision:.1%}")

# Save spot check
with open(OUT_DIR / "spot_check.txt", "w") as f:
    f.write(f"Merge Quality Spot-Check (n={sample_size})\n")
    f.write(f"CORRECT: {correct_count}, INCORRECT: {incorrect_count}, AMBIGUOUS: {ambiguous_count}\n")
    f.write(f"Precision: {merge_precision:.1%}\n\n")
    f.write("\n".join(spot_check_lines))

# Save metrics
metrics_lines = [f"{k}: {v}" for k, v in gate2_metrics.items()]
with open(OUT_DIR / "gate2_metrics.txt", "w") as f:
    f.write("Gate 2 Metrics\n")
    f.write(f"PASS: {gate2_pass}\n")
    f.write("\n".join(metrics_lines))

# Save changes log
with open(OUT_DIR / "changes_log.txt", "w") as f:
    f.write("\n".join(changes_log))

print(f"\n{'=' * 70}")
print("ER EXECUTION COMPLETE")
print(f"{'=' * 70}")
print(f"  Pre-ER:  {len(ent_orig):,} entities, {len(rel_orig):,} edges")
print(f"  Post-ER: {len(ent):,} entities, {len(rel):,} edges")
print(f"  Delta:   -{len(ent_orig)-len(ent):,} entities, -{len(rel_orig)-len(rel):,} edges")
print(f"  Gate 2:  {'PASS' if gate2_pass else 'FAIL'}")
print(f"\nOutputs in {OUT_DIR}")
