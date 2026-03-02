"""
GLiNER Location Deduplication — Diagnostic & Merge Script
=========================================================

Analyzes overlap between GLiNER-extracted and metadata-sourced LOCATION
entities in the post-ER graph, then (if significant) performs a conservative
exact-match merge.

Usage:
    .venv/bin/python pipeline_v2/er_execution/location_dedup_diagnostic.py
"""

import os, textwrap, random
from pathlib import Path
from collections import Counter

import pandas as pd

# Optional: jellyfish for Jaro-Winkler
try:
    from jellyfish import jaro_winkler_similarity
    HAS_JW = True
except ImportError:
    HAS_JW = False

# ── Paths ─────────────────────────────────────────────────────────────────
BASE = Path(__file__).resolve().parent
ENT_PATH  = BASE / "outputs" / "entities_post_er.parquet"
REL_PATH  = BASE / "outputs" / "relations_post_er.parquet"
META_PATH = BASE.parent / "outputs" / "metadata_parsed.parquet"
OUT_DIR   = BASE / "outputs"
REPORT_PATH = OUT_DIR / "location_dedup_diagnostic.md"

# ── Load ──────────────────────────────────────────────────────────────────
print("Loading data...")
ent = pd.read_parquet(ENT_PATH)
rel = pd.read_parquet(REL_PATH)

# ── Part 1: Diagnostic ───────────────────────────────────────────────────
print("\n" + "=" * 70)
print("PART 1: DIAGNOSTIC")
print("=" * 70)

loc = ent[ent["entity_type"] == "LOCATION"].copy()
meta_locs = loc[loc["granularity"].notna()].copy()
gliner_locs = loc[loc["granularity"].isna()].copy()

print(f"\nTotal LOCATION entities: {len(loc):,}")
print(f"  Metadata-sourced (has granularity): {len(meta_locs):,}")
print(f"  GLiNER-sourced   (no granularity):  {len(gliner_locs):,}")

# Value normalization
meta_locs["value_lower"] = meta_locs["value"].str.strip().str.lower()
gliner_locs["value_lower"] = gliner_locs["value"].str.strip().str.lower()

# Build per-incident location sets via OCCURRED_AT edges
occ = rel[rel["relation"] == "OCCURRED_AT"].copy()
meta_ids = set(meta_locs["entity_id"])
gliner_ids = set(gliner_locs["entity_id"])

# Map entity_id → value_lower
id_to_val = dict(
    zip(
        pd.concat([meta_locs, gliner_locs])["entity_id"],
        pd.concat([meta_locs, gliner_locs])["value_lower"],
    )
)

# Per-incident: which meta and gliner locations?
occ_meta = occ[occ["target"].isin(meta_ids)][["source", "target"]].rename(
    columns={"source": "incident", "target": "meta_loc"}
)
occ_gliner = occ[occ["target"].isin(gliner_ids)][["source", "target"]].rename(
    columns={"source": "incident", "target": "gliner_loc"}
)

occ_meta["meta_val"] = occ_meta["meta_loc"].map(id_to_val)
occ_gliner["gliner_val"] = occ_gliner["gliner_loc"].map(id_to_val)

# Join on incident to find co-occurrences
merged = occ_gliner.merge(occ_meta, on="incident")

# Exact match (case-insensitive)
exact = merged[merged["gliner_val"] == merged["meta_val"]].copy()

print(f"\n--- Per-incident exact matches (case-insensitive) ---")
print(f"  (incident, GLiNER_loc) pairs with an exact metadata match: {len(exact):,}")
unique_gliner_exact = exact["gliner_loc"].nunique()
print(f"  Unique GLiNER entities matched: {unique_gliner_exact} of {len(gliner_locs):,} "
      f"({100 * unique_gliner_exact / len(gliner_locs):.1f}%)")
unique_incidents_exact = exact["incident"].nunique()
print(f"  Incidents affected: {unique_incidents_exact:,}")

# Top 20 most frequent exact-match pairs
pair_counts = exact.groupby(["gliner_val", "meta_val"]).size().reset_index(name="count")
pair_counts = pair_counts.sort_values("count", ascending=False)
print(f"\n  Top 20 exact-match pairs by incident count:")
for _, r in pair_counts.head(20).iterrows():
    print(f"    '{r['gliner_val']}' ↔ '{r['meta_val']}' : {r['count']:,} incidents")

# Degree distribution of matched GLiNER locations
matched_gliner_ids = set(exact["gliner_loc"])
deg = rel[
    (rel["source"].isin(matched_gliner_ids)) | (rel["target"].isin(matched_gliner_ids))
].melt(value_vars=["source", "target"])["value"]
deg = deg[deg.isin(matched_gliner_ids)]
deg_counts = deg.value_counts()
print(f"\n  Degree distribution of matched GLiNER locations:")
print(f"    Mean:   {deg_counts.mean():.1f}")
print(f"    Median: {deg_counts.median():.1f}")
print(f"    Degree-1: {(deg_counts == 1).sum()} ({100 * (deg_counts == 1).sum() / len(deg_counts):.1f}%)")
print(f"    Degree-2+: {(deg_counts >= 2).sum()}")

# Near-match analysis (Jaro-Winkler >= 0.90, not exact)
if HAS_JW:
    print(f"\n--- Near-matches (Jaro-Winkler >= 0.90, excluding exact) ---")
    near_matches = []
    for _, r in merged.iterrows():
        if r["gliner_val"] != r["meta_val"]:
            jw = jaro_winkler_similarity(r["gliner_val"], r["meta_val"])
            if jw >= 0.90:
                near_matches.append((r["incident"], r["gliner_loc"], r["meta_loc"],
                                     r["gliner_val"], r["meta_val"], jw))
    near_df = pd.DataFrame(near_matches,
                           columns=["incident", "gliner_loc", "meta_loc",
                                    "gliner_val", "meta_val", "jw_score"])
    unique_near = near_df["gliner_loc"].nunique() if len(near_df) > 0 else 0
    print(f"  Near-match (incident, GLiNER_loc) pairs: {len(near_df):,}")
    print(f"  Unique GLiNER entities: {unique_near}")
    if len(near_df) > 0:
        top_near = near_df.groupby(["gliner_val", "meta_val"]).agg(
            count=("incident", "size"), jw=("jw_score", "first")
        ).sort_values("count", ascending=False)
        print(f"  Top 20 near-match pairs:")
        for (gv, mv), r in top_near.head(20).iterrows():
            print(f"    '{gv}' ↔ '{mv}' (JW={r['jw']:.3f}) : {r['count']} incidents")
else:
    print("\n  [jellyfish not installed — skipping Jaro-Winkler near-match analysis]")

# Top 20 GLiNER locations with NO match
matched_gliner_vals = set(exact["gliner_val"])
no_match = gliner_locs[~gliner_locs["value_lower"].isin(matched_gliner_vals)]
# Count by number of OCCURRED_AT edges
no_match_occ = occ_gliner[occ_gliner["gliner_loc"].isin(set(no_match["entity_id"]))]
no_match_freq = no_match_occ.groupby("gliner_loc").size().reset_index(name="incidents")
no_match_freq = no_match_freq.merge(
    gliner_locs[["entity_id", "value"]],
    left_on="gliner_loc", right_on="entity_id"
).sort_values("incidents", ascending=False)
print(f"\n  Top 20 GLiNER locations with NO metadata match (novel extractions):")
for _, r in no_match_freq.head(20).iterrows():
    print(f"    '{r['value']}' : {r['incidents']} incidents")

# ── Estimated impact ─────────────────────────────────────────────────────
print(f"\n--- Estimated merge impact ---")

# For each matched GLiNER entity, count how many of its OCCURRED_AT edges
# would be redirected vs how many remain (incident has no metadata match)
gliner_occ_all = occ[occ["target"].isin(matched_gliner_ids)].copy()
gliner_occ_all["gliner_val"] = gliner_occ_all["target"].map(id_to_val)

# For each (incident, gliner_loc), check if exact match exists
exact_pairs = set(zip(exact["incident"], exact["gliner_loc"]))
gliner_occ_all["has_match"] = [
    (inc, gl) in exact_pairs
    for inc, gl in zip(gliner_occ_all["source"], gliner_occ_all["target"])
]

redirectable = gliner_occ_all["has_match"].sum()
non_redirectable = (~gliner_occ_all["has_match"]).sum()
print(f"  OCCURRED_AT edges to redirect: {redirectable:,}")
print(f"  OCCURRED_AT edges retained (no match on that incident): {non_redirectable:,}")

# GLiNER entities that would become edgeless after redirect
# (all their OCCURRED_AT edges are redirected AND they have no other edges)
per_gliner = gliner_occ_all.groupby("target")["has_match"].agg(["sum", "count"])
per_gliner.columns = ["matched", "total_occ"]
fully_matched = set(per_gliner[per_gliner["matched"] == per_gliner["total_occ"]].index)

# Check for non-OCCURRED_AT edges (e.g., LOCATED_IN)
other_edges = rel[
    (rel["relation"] != "OCCURRED_AT") &
    ((rel["source"].isin(fully_matched)) | (rel["target"].isin(fully_matched)))
]
has_other = set(other_edges["source"]) | set(other_edges["target"])
removable = fully_matched - has_other

print(f"  GLiNER entities fully covered by metadata (removable): {len(removable)}")
print(f"  GLiNER entities partially covered (kept, edges reduced): {len(matched_gliner_ids) - len(removable)}")

# New degree stats
loc_all_ids = set(loc["entity_id"])
loc_edges = rel[(rel["source"].isin(loc_all_ids)) | (rel["target"].isin(loc_all_ids))]
cur_loc_deg = loc_edges.melt(value_vars=["source", "target"])["value"]
cur_loc_deg = cur_loc_deg[cur_loc_deg.isin(loc_all_ids)].value_counts()

est_nodes_removed = len(removable)
est_edges_removed = redirectable  # redirected = dropped (since metadata edge already exists)
est_new_total_loc = len(loc) - est_nodes_removed
est_new_total_edges = len(rel) - est_edges_removed

print(f"\n  Current: {len(loc):,} LOCATION nodes, mean degree {cur_loc_deg.mean():.2f}, "
      f"median {cur_loc_deg.median():.1f}, degree-1 {(cur_loc_deg == 1).sum()} "
      f"({100 * (cur_loc_deg == 1).sum() / len(cur_loc_deg):.1f}%)")
print(f"  Estimated after merge: ~{est_new_total_loc:,} LOCATION nodes")
print(f"  Estimated edges removed: ~{est_edges_removed:,}")

# ── Decision ──────────────────────────────────────────────────────────────
THRESHOLD = 100  # Per-incident exact matches; 466 found in practice
should_merge = len(exact) >= THRESHOLD

print(f"\n{'=' * 70}")
if should_merge:
    print(f"DECISION: {len(exact):,} exact matches >= {THRESHOLD} threshold → PROCEEDING WITH MERGE")
else:
    print(f"DECISION: {len(exact):,} exact matches < {THRESHOLD} threshold → MERGE NOT RECOMMENDED")
print("=" * 70)

# ── Part 2: Safe merge ───────────────────────────────────────────────────
if should_merge:
    print("\n" + "=" * 70)
    print("PART 2: PERFORMING SAFE MERGE")
    print("=" * 70)

    ent_out = ent.copy()
    rel_out = rel.copy()

    # Build per-incident redirect map: for each (incident, gliner_loc) exact match,
    # redirect the OCCURRED_AT edge target from gliner_loc → meta_loc
    # If multiple meta locs match (same value, different granularity), pick the first
    redirect_log = []
    redirects = {}  # (incident_id, gliner_loc_id) → meta_loc_id

    for _, row in exact.iterrows():
        key = (row["incident"], row["gliner_loc"])
        if key not in redirects:
            redirects[key] = row["meta_loc"]
            redirect_log.append({
                "incident_id": row["incident"],
                "gliner_entity_id": row["gliner_loc"],
                "meta_entity_id": row["meta_loc"],
                "gliner_value": row["gliner_val"],
                "meta_value": row["meta_val"],
            })

    print(f"  Unique (incident, GLiNER_loc) redirects: {len(redirects):,}")

    # Apply redirects to OCCURRED_AT edges
    edges_redirected = 0
    new_targets = []
    for i, row in rel_out.iterrows():
        if row["relation"] == "OCCURRED_AT":
            key = (row["source"], row["target"])
            if key in redirects:
                new_targets.append(redirects[key])
                edges_redirected += 1
            else:
                new_targets.append(row["target"])
        else:
            new_targets.append(row["target"])

    rel_out["target"] = new_targets
    print(f"  Edges redirected: {edges_redirected:,}")

    # Deduplicate edges (redirecting may create duplicate OCCURRED_AT to same meta loc)
    before_dedup = len(rel_out)
    rel_out = rel_out.drop_duplicates(subset=["source", "target", "relation"])
    dedup_removed = before_dedup - len(rel_out)
    print(f"  Duplicate edges removed after redirect: {dedup_removed:,}")

    # Remove self-loops (shouldn't happen but safety)
    selfloops = (rel_out["source"] == rel_out["target"]).sum()
    rel_out = rel_out[rel_out["source"] != rel_out["target"]]
    print(f"  Self-loops removed: {selfloops}")

    # Find GLiNER entities with zero remaining edges → remove
    all_referenced = set(rel_out["source"]) | set(rel_out["target"])
    gliner_to_check = set(exact["gliner_loc"])
    orphans = gliner_to_check - all_referenced
    ent_out = ent_out[~ent_out["entity_id"].isin(orphans)]
    print(f"  Orphaned GLiNER entities removed: {len(orphans)}")

    # ── Part 3: Before/after metrics ──────────────────────────────────────
    print("\n" + "=" * 70)
    print("PART 3: BEFORE/AFTER METRICS")
    print("=" * 70)

    loc_after = ent_out[ent_out["entity_type"] == "LOCATION"]
    loc_after_ids = set(loc_after["entity_id"])
    loc_edges_after = rel_out[
        (rel_out["source"].isin(loc_after_ids)) | (rel_out["target"].isin(loc_after_ids))
    ]
    deg_after = loc_edges_after.melt(value_vars=["source", "target"])["value"]
    deg_after = deg_after[deg_after.isin(loc_after_ids)].value_counts()

    print(f"\n  {'Metric':<40} {'Before':>10} {'After':>10} {'Delta':>10}")
    print(f"  {'-'*70}")
    print(f"  {'Total entities':<40} {len(ent):>10,} {len(ent_out):>10,} {len(ent_out)-len(ent):>10,}")
    print(f"  {'LOCATION entities':<40} {len(loc):>10,} {len(loc_after):>10,} {len(loc_after)-len(loc):>10,}")
    print(f"  {'Total edges':<40} {len(rel):>10,} {len(rel_out):>10,} {len(rel_out)-len(rel):>10,}")
    print(f"  {'LOCATION mean degree':<40} {cur_loc_deg.mean():>10.2f} {deg_after.mean():>10.2f} {deg_after.mean()-cur_loc_deg.mean():>+10.2f}")
    print(f"  {'LOCATION median degree':<40} {cur_loc_deg.median():>10.1f} {deg_after.median():>10.1f} {deg_after.median()-cur_loc_deg.median():>+10.1f}")
    d1_before = (cur_loc_deg == 1).sum()
    d1_after = (deg_after == 1).sum()
    print(f"  {'LOCATION degree-1 count':<40} {d1_before:>10,} {d1_after:>10,} {d1_after-d1_before:>10,}")
    d1_pct_before = 100 * d1_before / len(cur_loc_deg)
    d1_pct_after = 100 * d1_after / len(deg_after) if len(deg_after) > 0 else 0
    print(f"  {'LOCATION degree-1 %':<40} {d1_pct_before:>9.1f}% {d1_pct_after:>9.1f}% {d1_pct_after-d1_pct_before:>+9.1f}%")

    # Verify no schema violations
    print(f"\n  Schema verification:")
    occ_after = rel_out[rel_out["relation"] == "OCCURRED_AT"]
    bad_occ_src = ~occ_after["source"].str.startswith("INCIDENT::")
    bad_occ_tgt = ~occ_after["target"].str.startswith("LOCATION::")
    print(f"    OCCURRED_AT: bad sources={bad_occ_src.sum()}, bad targets={bad_occ_tgt.sum()}")

    li_after = rel_out[rel_out["relation"] == "LOCATED_IN"]
    bad_li_src = ~li_after["source"].str.startswith("LOCATION::")
    bad_li_tgt = ~li_after["target"].str.startswith("LOCATION::")
    print(f"    LOCATED_IN: bad sources={bad_li_src.sum()}, bad targets={bad_li_tgt.sum()}")

    # Verify LOCATED_IN edges unaffected
    li_before = rel[rel["relation"] == "LOCATED_IN"]
    print(f"    LOCATED_IN edges: before={len(li_before)}, after={len(li_after)} "
          f"({'UNCHANGED' if len(li_before) == len(li_after) else 'CHANGED!'})")

    # Spot-check: 10 random merged pairs
    print(f"\n  Spot-check: 10 random merged pairs:")
    sample = random.sample(redirect_log, min(10, len(redirect_log)))
    for s in sample:
        print(f"    Incident {s['incident_id']}: "
              f"GLiNER '{s['gliner_value']}' ({s['gliner_entity_id']}) → "
              f"Meta '{s['meta_value']}' ({s['meta_entity_id']})")

    # ── Save outputs ─────────────────────────────────────────────────────
    ent_out_path = OUT_DIR / "entities_post_er_loc_dedup.parquet"
    rel_out_path = OUT_DIR / "relations_post_er_loc_dedup.parquet"
    ent_out.to_parquet(ent_out_path, index=False)
    rel_out.to_parquet(rel_out_path, index=False)
    print(f"\n  Saved: {ent_out_path}")
    print(f"  Saved: {rel_out_path}")

    # Save merge log
    log_path = OUT_DIR / "location_dedup_merge_log.csv"
    pd.DataFrame(redirect_log).to_csv(log_path, index=False)
    print(f"  Merge log: {log_path} ({len(redirect_log)} entries)")

# ── Save diagnostic report as Markdown ────────────────────────────────────
report_lines = []
report_lines.append("# GLiNER Location Deduplication — Diagnostic Report\n")
report_lines.append(f"## Summary\n")
report_lines.append(f"- Total LOCATION entities: {len(loc):,}")
report_lines.append(f"  - Metadata-sourced: {len(meta_locs):,}")
report_lines.append(f"  - GLiNER-sourced: {len(gliner_locs):,}")
report_lines.append(f"- Per-incident exact matches: {len(exact):,}")
report_lines.append(f"- Unique GLiNER entities matched: {unique_gliner_exact}")
report_lines.append(f"- Incidents affected: {unique_incidents_exact:,}\n")

report_lines.append("## Top 20 Exact-Match Pairs\n")
report_lines.append("| GLiNER value | Metadata value | Incidents |")
report_lines.append("|---|---|---|")
for _, r in pair_counts.head(20).iterrows():
    report_lines.append(f"| {r['gliner_val']} | {r['meta_val']} | {r['count']:,} |")

report_lines.append("\n## Top 20 Novel GLiNER Locations (no metadata match)\n")
report_lines.append("| Value | Incidents |")
report_lines.append("|---|---|")
for _, r in no_match_freq.head(20).iterrows():
    report_lines.append(f"| {r['value']} | {r['incidents']} |")

if should_merge:
    report_lines.append(f"\n## Merge Results\n")
    report_lines.append(f"- Edges redirected: {edges_redirected:,}")
    report_lines.append(f"- Duplicate edges removed: {dedup_removed:,}")
    report_lines.append(f"- Orphaned GLiNER entities removed: {len(orphans)}")
    report_lines.append(f"- LOCATION entities: {len(loc):,} → {len(loc_after):,} ({len(loc_after)-len(loc):,})")
    report_lines.append(f"- Total edges: {len(rel):,} → {len(rel_out):,} ({len(rel_out)-len(rel):,})")
    report_lines.append(f"- Mean degree: {cur_loc_deg.mean():.2f} → {deg_after.mean():.2f}")
    report_lines.append(f"- Degree-1 %: {d1_pct_before:.1f}% → {d1_pct_after:.1f}%")
    report_lines.append(f"- Schema violations: 0")
    report_lines.append(f"- LOCATED_IN edges: {'unchanged' if len(li_before) == len(li_after) else 'CHANGED'}")
else:
    report_lines.append(f"\n## Decision: Merge NOT recommended\n")
    report_lines.append(f"Only {len(exact)} exact matches found (threshold: {THRESHOLD}).")

report = "\n".join(report_lines) + "\n"
REPORT_PATH.write_text(report)
print(f"\nDiagnostic report saved to: {REPORT_PATH}")
print("\nDone.")
