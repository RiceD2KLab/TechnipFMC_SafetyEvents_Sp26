#!/usr/bin/env python3
"""Fix schema violations: align relation types with entity types after multi-type resolution.

Modifies relations_post_er.parquet in place.
"""

from pathlib import Path
from collections import Counter

import pandas as pd

OUT_DIR = Path(__file__).resolve().parent / "outputs"

ENTITY_TYPE_TO_RELATION = {
    "EQUIPMENT": "INVOLVED",
    "BODY_PART": "AFFECTED",
    "INJURY_TYPE": "RESULTED_IN",
    "LOCATION": "OCCURRED_AT",
    "ORGANIZATION": "REPORTED_BY",
    "ROOT_CAUSE_CATEGORY": "CATEGORIZED_AS",
}

# ---------------------------------------------------------------------------
# Load
# ---------------------------------------------------------------------------
print("Loading post-ER graph...")
ent = pd.read_parquet(OUT_DIR / "entities_post_er.parquet")
rel = pd.read_parquet(OUT_DIR / "relations_post_er.parquet")
print(f"  Entities: {len(ent):,}  Edges: {len(rel):,}")

entity_type_map = dict(zip(ent["entity_id"], ent["entity_type"]))

# ---------------------------------------------------------------------------
# Fix relation types
# ---------------------------------------------------------------------------
print("\nFixing relation types...")

transition_counts = Counter()  # (old_relation, new_relation) -> count
fix_count = 0

for idx, row in rel.iterrows():
    if row["relation"] == "LOCATED_IN":
        continue

    source_type = entity_type_map.get(row["source"])
    target_type = entity_type_map.get(row["target"])

    # INCIDENT → entity: relation should match target type
    if source_type == "INCIDENT" and target_type in ENTITY_TYPE_TO_RELATION:
        expected = ENTITY_TYPE_TO_RELATION[target_type]
        if row["relation"] != expected:
            transition_counts[(row["relation"], expected)] += 1
            rel.at[idx, "relation"] = expected
            fix_count += 1

    # entity → INCIDENT: relation should match source type
    elif target_type == "INCIDENT" and source_type in ENTITY_TYPE_TO_RELATION:
        expected = ENTITY_TYPE_TO_RELATION[source_type]
        if row["relation"] != expected:
            transition_counts[(row["relation"], expected)] += 1
            rel.at[idx, "relation"] = expected
            fix_count += 1

print(f"  Edges fixed: {fix_count}")
print("  Breakdown:")
for (old_rel, new_rel), cnt in sorted(transition_counts.items(), key=lambda x: -x[1]):
    print(f"    {old_rel} → {new_rel}: {cnt}")

# ---------------------------------------------------------------------------
# Validate zero violations remain
# ---------------------------------------------------------------------------
print("\nValidating...")
violations = 0
for _, row in rel.iterrows():
    if row["relation"] == "LOCATED_IN":
        continue
    source_type = entity_type_map.get(row["source"])
    target_type = entity_type_map.get(row["target"])

    if source_type == "INCIDENT" and target_type in ENTITY_TYPE_TO_RELATION:
        if row["relation"] != ENTITY_TYPE_TO_RELATION[target_type]:
            violations += 1
    elif target_type == "INCIDENT" and source_type in ENTITY_TYPE_TO_RELATION:
        if row["relation"] != ENTITY_TYPE_TO_RELATION[source_type]:
            violations += 1

print(f"  Remaining schema violations: {violations}")
assert violations == 0, f"Still have {violations} violations!"

# ---------------------------------------------------------------------------
# Deduplicate
# ---------------------------------------------------------------------------
pre_dedup = len(rel)
rel = rel.drop_duplicates(subset=["source", "target", "relation"])
post_dedup = len(rel)
deduped = pre_dedup - post_dedup
print(f"\nDeduplicated: {pre_dedup:,} → {post_dedup:,} edges (-{deduped})")

# ---------------------------------------------------------------------------
# Compute post-fix mean degree
# ---------------------------------------------------------------------------
import networkx as nx

G = nx.DiGraph()
for _, node in ent.iterrows():
    G.add_node(node["entity_id"])
for _, edge in rel.iterrows():
    if edge["source"] in G and edge["target"] in G:
        G.add_edge(edge["source"], edge["target"], relation=edge["relation"])

degrees = [d for _, d in G.degree()]
mean_degree = sum(degrees) / len(degrees) if degrees else 0

# ---------------------------------------------------------------------------
# Save
# ---------------------------------------------------------------------------
rel.to_parquet(OUT_DIR / "relations_post_er.parquet", index=False)
print(f"\nSaved: {len(rel):,} edges")

# ---------------------------------------------------------------------------
# Write report
# ---------------------------------------------------------------------------
report = f"""# Schema Violation Fix Report

**Generated:** 2026-02-19

## Fixes Applied

- Total edges fixed: {fix_count}
- Breakdown by old_relation → new_relation:
"""

for (old_rel, new_rel), cnt in sorted(transition_counts.items(), key=lambda x: -x[1]):
    report += f"  - {old_rel} → {new_rel}: {cnt}\n"

report += f"""- Edges deduplicated after fix: {deduped}
- Remaining schema violations: {violations}

## Topology After Fix

- Nodes: {len(ent):,} (unchanged)
- Edges: {post_dedup:,} (after dedup)
- Mean degree: {mean_degree:.2f}
"""

(OUT_DIR / "schema_fix_report.md").write_text(report)
print(f"\nReport: {OUT_DIR / 'schema_fix_report.md'}")
print("Done.")
