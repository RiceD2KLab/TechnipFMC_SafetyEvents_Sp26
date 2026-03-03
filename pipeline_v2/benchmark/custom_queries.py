"""Custom query functions for benchmark queries that cannot be expressed
purely via CSV configuration.

Each function receives (spec, G, entities_df, relations_df, metadata_df,
*, results=None) and returns a result dict with keys:
coverage, diagnosis, result_summary, detail.
"""

import re
from collections import Counter, defaultdict

import pandas as pd

from .helpers import (
    find_entities_by_value,
    get_entities_for_incident,
    get_incident_property,
    get_incidents_for_entity,
    incidents_matching_narrative,
    parse_year,
    safe_get_node_value,
)


# ── GL-01: Louvain communities ──────────────────────────────────────────

def louvain_communities(spec, G, entities_df, relations_df, metadata_df,
                        *, results=None):
    from networkx.algorithms.community import louvain_communities as _lc

    exclude = {n for n in G.nodes
               if G.nodes[n].get("granularity") == "region"}
    G_sub = G.subgraph([n for n in G.nodes if n not in exclude])
    communities = _lc(G_sub, seed=42)
    sorted_comms = sorted(communities, key=len, reverse=True)[:10]

    lines = [f"Total communities: {len(communities)}",
             "Top 10 by size:"]
    for i, comm in enumerate(sorted_comms):
        type_counts = Counter()
        sample_values = defaultdict(list)
        for node in comm:
            ntype = G.nodes[node].get("entity_type", "unknown")
            type_counts[ntype] += 1
            if len(sample_values[ntype]) < 3:
                sample_values[ntype].append(
                    G.nodes[node].get("value", ""))
        lines.append(f"\n  Community {i+1} (size={len(comm)}):")
        for t, c in type_counts.most_common():
            lines.append(
                f"    {t}: {c} (e.g. {sample_values[t][:3]})")

    return {
        "coverage": "\u2705",
        "diagnosis": "CLEAN",
        "result_summary": f"{len(communities)} communities detected",
        "detail": "\n".join(lines),
    }


# ── GL-02: Equipment recurring across regions ───────────────────────────

def equipment_across_regions(spec, G, entities_df, relations_df,
                             metadata_df, *, results=None):
    equipment_nodes = entities_df[
        entities_df["entity_type"] == "EQUIPMENT"]
    equip_region_map = defaultdict(set)

    for ent_id in equipment_nodes["entity_id"]:
        incidents = get_incidents_for_entity(G, ent_id, "INVOLVED")
        for inc_id in incidents:
            locs = get_entities_for_incident(
                G, inc_id, entity_type="LOCATION",
                relation_type="OCCURRED_AT")
            for loc in locs:
                if G.nodes[loc].get("granularity") == "region":
                    equip_val = safe_get_node_value(G, ent_id)
                    loc_val = safe_get_node_value(G, loc)
                    if equip_val and loc_val:
                        equip_region_map[equip_val].add(loc_val)

    global_equip = {
        eq: sorted(regions)
        for eq, regions in equip_region_map.items()
        if len(regions) >= 5
    }

    lines = [f"Equipment appearing in 5+ regions: {len(global_equip)}"]
    for eq in sorted(global_equip,
                     key=lambda x: -len(global_equip[x]))[:20]:
        lines.append(
            f"  {eq}: {len(global_equip[eq])} regions -> "
            f"{global_equip[eq]}")

    return {
        "coverage": "\u2705" if global_equip else "\u26a0\ufe0f",
        "diagnosis": "ER_NEEDED",
        "result_summary":
            f"{len(global_equip)} equipment types span 5+ regions",
        "detail": "\n".join(lines),
    }


# ── GL-04: Hub centrality (degree + PageRank) ───────────────────────────

def hub_centrality(spec, G, entities_df, relations_df, metadata_df,
                   *, results=None):
    import networkx as nx

    centrality = {}
    for node in G.nodes:
        if G.nodes[node].get("entity_type") != "INCIDENT":
            centrality[node] = G.degree(node)
    top20_degree = sorted(centrality.items(), key=lambda x: -x[1])[:20]

    lines = ["Top 20 non-incident nodes by degree:"]
    for node_id, degree in top20_degree:
        ntype = G.nodes[node_id].get("entity_type", "?")
        val = G.nodes[node_id].get("value", "?")
        lines.append(f"  {ntype}::{val} -- degree {degree}")

    # PageRank — pure Python fallback
    print("    Computing PageRank (pure Python)...")
    try:
        pr = nx.pagerank(G, backend="networkx")
    except (TypeError, ModuleNotFoundError):
        N = G.number_of_nodes()
        alpha = 0.85
        pr = {n: 1.0 / N for n in G.nodes}
        for _ in range(50):
            pr_new = {}
            for n in G.nodes:
                rank = (1 - alpha) / N
                # PageRank: sum over predecessors (incoming edges)
                for predecessor in G.predecessors(n):
                    out_deg = max(G.out_degree(predecessor), 1)
                    rank += alpha * pr[predecessor] / out_deg
                pr_new[n] = rank
            pr = pr_new

    top20_pr = sorted(
        [(n, pr[n]) for n in G.nodes
         if G.nodes[n].get("entity_type") != "INCIDENT"],
        key=lambda x: -x[1])[:20]

    lines.append("\nTop 20 non-incident nodes by PageRank:")
    for node_id, score in top20_pr:
        ntype = G.nodes[node_id].get("entity_type", "?")
        val = G.nodes[node_id].get("value", "?")
        lines.append(f"  {ntype}::{val} -- PR {score:.6f}")

    return {
        "coverage": "\u2705",
        "diagnosis": "CLEAN",
        "result_summary": "Hub analysis: degree + PageRank top 20",
        "detail": "\n".join(lines),
    }


# ── MH-01: Containment -> injury at offshore ────────────────────────────

def containment_injury_offshore(spec, G, entities_df, relations_df,
                                metadata_df, *, results=None):
    containment_rccs = find_entities_by_value(
        entities_df, "ROOT_CAUSE_CATEGORY",
        r"containment|spill|loss|hazardous liquid")
    containment_rcc_vals = sorted(set(
        safe_get_node_value(G, e)
        for e in containment_rccs if e in G))
    containment_incidents = set()
    for rcc_id in containment_rccs:
        containment_incidents.update(
            get_incidents_for_entity(G, rcc_id, "CATEGORIZED_AS"))

    offshore_containment = set()
    for inc_id in containment_incidents:
        wp = get_incident_property(G, inc_id, "work_process")
        if wp and "offshore" in str(wp).lower():
            offshore_containment.add(inc_id)

    injury_offshore_containment = set()
    for inc_id in offshore_containment:
        injuries = get_entities_for_incident(
            G, inc_id, entity_type="INJURY_TYPE",
            relation_type="RESULTED_IN")
        if injuries:
            injury_offshore_containment.add(inc_id)

    equip_counts = Counter()
    for inc_id in injury_offshore_containment:
        equips = get_entities_for_incident(
            G, inc_id, entity_type="EQUIPMENT",
            relation_type="INVOLVED")
        for eq in equips:
            eq_val = safe_get_node_value(G, eq)
            if eq_val:
                equip_counts[eq_val] += 1

    lines = [
        f"Containment RCC values matched: {containment_rcc_vals}",
        f"Containment incidents: {len(containment_incidents)}",
        f"-> Offshore containment: {len(offshore_containment)}",
        f"-> With injuries: {len(injury_offshore_containment)}",
        f"Equipment in those incidents:",
    ] + [f"  {eq}: {cnt}" for eq, cnt in equip_counts.most_common(10)]

    coverage = ("\u2705" if len(equip_counts) >= 3
                else ("\u26a0\ufe0f" if equip_counts else "\u274c"))
    diag = "CLEAN" if equip_counts else "DATA_SPARSE"

    return {
        "coverage": coverage,
        "diagnosis": diag,
        "result_summary":
            f"{len(injury_offshore_containment)} incidents, "
            f"{len(equip_counts)} equipment types",
        "detail": "\n".join(lines),
    }


# ── MH-04: Top injury per top-5 equipment ───────────────────────────────

def top_injury_per_equipment(spec, G, entities_df, relations_df,
                             metadata_df, *, results=None):
    equipment_nodes = entities_df[
        entities_df["entity_type"] == "EQUIPMENT"]

    # Compute equipment incident counts (same as AG-03 logic)
    equip_counts = Counter()
    for ent_id in equipment_nodes["entity_id"]:
        degree = len(get_incidents_for_entity(G, ent_id, "INVOLVED"))
        if degree > 0:
            equip_val = safe_get_node_value(G, ent_id)
            if equip_val:
                equip_counts[equip_val] = degree

    top5 = equip_counts.most_common(5)
    lines = ["Top 5 equipment (by incident count):"]

    for equip_val, count in top5:
        equip_entities = find_entities_by_value(
            entities_df, "EQUIPMENT", f"^{re.escape(equip_val)}$")
        equip_incs = set()
        for ent_id in equip_entities:
            equip_incs.update(
                get_incidents_for_entity(G, ent_id, "INVOLVED"))

        injury_counts = Counter()
        for inc_id in equip_incs:
            injuries = get_entities_for_incident(
                G, inc_id, entity_type="INJURY_TYPE",
                relation_type="RESULTED_IN")
            for inj in injuries:
                inj_val = safe_get_node_value(G, inj)
                if inj_val:
                    injury_counts[inj_val] += 1

        top_injuries = injury_counts.most_common(5)
        lines.append(f"\n  {equip_val} ({count} incidents):")
        for inj, cnt in top_injuries:
            lines.append(f"    {inj}: {cnt}")
        if not top_injuries:
            lines.append("    (no RESULTED_IN edges)")

    return {
        "coverage": "\u2705" if top5 else "\u274c",
        "diagnosis": "ER_NEEDED",
        "result_summary": "Injury breakdown for top 5 equipment",
        "detail": "\n".join(lines),
    }


# ── MH-06: Severity comparison (truck vs crane) ─────────────────────────

def severity_comparison(spec, G, entities_df, relations_df, metadata_df,
                        *, results=None):
    lines = []
    for equip_name in ["truck", "crane"]:
        entities = find_entities_by_value(
            entities_df, "EQUIPMENT", equip_name)
        incidents = set()
        for ent_id in entities:
            incidents.update(
                get_incidents_for_entity(G, ent_id, "INVOLVED"))

        sev_dist = Counter()
        for inc_id in incidents:
            sev = get_incident_property(G, inc_id, "severity_bin")
            if pd.notna(sev):
                sev_dist[int(sev)] += 1

        lines.append(f"\n  {equip_name} ({len(incidents)} incidents):")
        for sev_bin in sorted(sev_dist):
            lines.append(f"    Severity {sev_bin}: {sev_dist[sev_bin]}")
        mean_sev = (sum(k * v for k, v in sev_dist.items())
                    / max(sum(sev_dist.values()), 1))
        lines.append(f"    Mean severity: {mean_sev:.2f}")

    return {
        "coverage": "\u2705",
        "diagnosis": "ER_NEEDED",
        "result_summary": "Truck vs crane severity comparison",
        "detail": "Severity distribution comparison:\n"
                  + "\n".join(lines),
    }


# ── CJ-01: Causal chain check (L2 traversal) ─────────────────────────────

def causal_chain_check(spec, G, entities_df, relations_df, metadata_df,
                       *, results=None):
    causal_rels = ["CAUSAL", "PRECEDED_BY", "FAILED_CONTROL"]
    causal_edges = relations_df[relations_df["relation"].isin(causal_rels)]

    if len(causal_edges) == 0:
        return {
            "coverage": "\u274c",
            "diagnosis": "L2_REQUIRED",
            "result_summary": "0 causal edges in graph — L2 merge needed",
            "detail": "No L2 causal edges found. Run merge_l2_edges.py first.",
        }

    # Query: "What caused fire/explosion incidents?" — trace CAUSAL edges backward
    fire_rcc = find_entities_by_value(
        entities_df, "ROOT_CAUSE_CATEGORY",
        r"fire|explosion|flammable")
    fire_incidents = set()
    for rcc_id in fire_rcc:
        fire_incidents.update(
            get_incidents_for_entity(G, rcc_id, "CATEGORIZED_AS"))

    # For fire incidents, find causal chains by traversing L2 edges
    # L2 edges connect free-text entities (not INCIDENT nodes directly),
    # so we find causal edges whose record_no matches fire incidents
    fire_record_nos = {inc.split("::")[-1] for inc in fire_incidents}
    fire_causal = causal_edges[
        causal_edges["record_no"].astype(str).isin(fire_record_nos)]

    # Count causal factors (sources of CAUSAL edges for fire incidents)
    # Filter out tautological edges where source AND target are both fire-related
    fire_keywords = re.compile(
        r"\b(?:fire|flame|burn|smoke|spark|ignit)", re.IGNORECASE)
    causal_sources = fire_causal[fire_causal["relation"] == "CAUSAL"]
    source_counts = Counter()
    tautological = 0
    for _, e in causal_sources.iterrows():
        src_val = safe_get_node_value(G, e["source"], "")
        tgt_val = safe_get_node_value(G, e["target"], "")
        # Skip tautological: both source and target are fire-related
        if fire_keywords.search(src_val) and fire_keywords.search(tgt_val):
            tautological += 1
            continue
        if src_val:
            source_counts[src_val] += 1

    # Also find corrosion-related causal chains
    corrosion_narr = incidents_matching_narrative(metadata_df, ["corrosion"])
    corrosion_fire = fire_record_nos & set(str(r) for r in corrosion_narr)
    corrosion_causal = causal_edges[
        causal_edges["record_no"].astype(str).isin(corrosion_fire)]

    lines = [
        f"L2 causal edges in graph: {len(causal_edges):,}",
        f"  CAUSAL: {len(causal_edges[causal_edges['relation'] == 'CAUSAL']):,}",
        f"  PRECEDED_BY: {len(causal_edges[causal_edges['relation'] == 'PRECEDED_BY']):,}",
        f"  FAILED_CONTROL: {len(causal_edges[causal_edges['relation'] == 'FAILED_CONTROL']):,}",
        "",
        f"Fire/explosion incidents: {len(fire_incidents):,}",
        f"  With causal edges: {fire_causal['record_no'].nunique():,}",
        f"  Total causal edges: {len(fire_causal):,}",
        f"  Tautological (fire→fire) filtered: {tautological}",
        "",
        "Top root causes for fire/explosion (non-tautological):",
    ]
    for factor, count in source_counts.most_common(10):
        lines.append(f"  {factor}: {count}")

    lines.extend([
        "",
        f"Corrosion + fire/explosion intersection: {len(corrosion_fire)} records",
        f"  Causal edges in these: {len(corrosion_causal)}",
    ])

    return {
        "coverage": "\u2705",
        "diagnosis": "CLEAN",
        "result_summary":
            f"{len(causal_edges):,} causal edges; "
            f"{len(fire_causal):,} for fire/explosion",
        "detail": "\n".join(lines),
    }


# ── CJ-04: Dual-risk detection ──────────────────────────────────────────

def dual_risk_detection(spec, G, entities_df, relations_df, metadata_df,
                        *, results=None):
    equipment_nodes = entities_df[
        entities_df["entity_type"] == "EQUIPMENT"]

    equip_by_degree = sorted(
        [(eid, len(get_incidents_for_entity(G, eid, "INVOLVED")))
         for eid in equipment_nodes["entity_id"]],
        key=lambda x: -x[1])[:3000]

    equip_accident_locs = defaultdict(lambda: defaultdict(set))
    equip_nearmiss_locs = defaultdict(lambda: defaultdict(set))

    for ent_id, _ in equip_by_degree:
        incidents = get_incidents_for_entity(G, ent_id, "INVOLVED")
        equip_val = safe_get_node_value(G, ent_id)
        for inc_id in incidents:
            inc_type = get_incident_property(G, inc_id, "incident_type")
            date = get_incident_property(G, inc_id, "reported_date")
            locs = get_entities_for_incident(
                G, inc_id, entity_type="LOCATION",
                relation_type="OCCURRED_AT")
            city_locs = [
                safe_get_node_value(G, loc) for loc in locs
                if loc in G
                and G.nodes[loc].get("granularity") == "city"]
            city_locs = [c for c in city_locs if c is not None]
            yr = parse_year(date)
            if yr and city_locs:
                for city in city_locs:
                    key = (city, yr)
                    if inc_type and "accident" in str(inc_type).lower():
                        equip_accident_locs[equip_val][key].add(inc_id)
                    elif (inc_type
                          and "near miss" in str(inc_type).lower()):
                        equip_nearmiss_locs[equip_val][key].add(inc_id)

    dual_risk = []
    for equip_val in equip_accident_locs:
        for key in equip_accident_locs[equip_val]:
            if key in equip_nearmiss_locs.get(equip_val, {}):
                dual_risk.append({
                    "equipment": equip_val,
                    "location": key[0],
                    "year": key[1],
                    "accidents": len(
                        equip_accident_locs[equip_val][key]),
                    "near_misses": len(
                        equip_nearmiss_locs[equip_val][key]),
                })
    dual_risk.sort(key=lambda x: -(x["accidents"] + x["near_misses"]))

    lines = [
        f"Equipment nodes scanned: {len(equip_by_degree)}",
        f"Dual-risk (accident + near-miss at same location/year): "
        f"{len(dual_risk)} combos",
        "Top 10:",
    ]
    for dr in dual_risk[:10]:
        lines.append(
            f"  {dr['equipment']} @ {dr['location']} ({dr['year']}): "
            f"{dr['accidents']} accidents, "
            f"{dr['near_misses']} near-misses")

    return {
        "coverage": "\u2705" if dual_risk else "\u26a0\ufe0f",
        "diagnosis": "CLEAN" if dual_risk else "DATA_SPARSE",
        "result_summary":
            f"{len(dual_risk)} dual-risk equipment/location/year combos",
        "detail": "\n".join(lines),
    }


# ── CJ-05: Procedural → dropped → head/hand injury (L2 traversal) ────

def procedural_dropped_injury(spec, G, entities_df, relations_df, metadata_df,
                              *, results=None):
    """Trace L2 causal edges: procedural violation → dropped object → injury."""
    causal_rels = ["CAUSAL", "PRECEDED_BY", "FAILED_CONTROL"]
    causal_edges = relations_df[relations_df["relation"].isin(causal_rels)]

    if len(causal_edges) == 0:
        return {
            "coverage": "❌",
            "diagnosis": "L2_REQUIRED",
            "result_summary": "0 causal edges in graph — L2 merge needed",
            "detail": "No L2 causal edges found. Run merge_l2_edges.py first.",
        }

    # Step 1: Find dropped-object incidents via L1 categorization
    drop_rcc = find_entities_by_value(
        entities_df, "ROOT_CAUSE_CATEGORY",
        r"drop|fall.*object|loose.*material")
    drop_incidents = set()
    for rcc_id in drop_rcc:
        drop_incidents.update(
            get_incidents_for_entity(G, rcc_id, "CATEGORIZED_AS"))

    # Also find via narrative keywords
    narr_drops = incidents_matching_narrative(
        metadata_df, ["dropped", "drop"], match_all=False)
    narr_drop_ids = {f"INCIDENT::{rn}" for rn in narr_drops}
    drop_incidents.update(narr_drop_ids & set(G.nodes()))

    # Step 2: Among drop incidents, find those with head/hand body parts
    head_hand_drops = set()
    for inc_id in drop_incidents:
        bps = get_entities_for_incident(
            G, inc_id, entity_type="BODY_PART", relation_type="AFFECTED")
        for bp_id in bps:
            val = safe_get_node_value(G, bp_id, "").lower()
            if re.search(r"head|hand|finger|skull|wrist|thumb", val):
                head_hand_drops.add(inc_id)
                break

    # Step 3: For those incidents, trace L2 causal edges
    drop_record_nos = {inc.split("::")[-1] for inc in head_hand_drops}
    drop_causal = causal_edges[
        causal_edges["record_no"].astype(str).isin(drop_record_nos)]

    # Step 4: Find procedural causal factors in those edges
    proc_keywords = re.compile(
        r"proced|supervis|training|instruct|permit|protocol|compliance|"
        r"briefing|communication|rule|violat|failure to follow|"
        r"inadequate|not follow|organization", re.IGNORECASE)

    proc_edges = []
    all_factors = Counter()
    for _, e in drop_causal.iterrows():
        src_val = safe_get_node_value(G, e["source"], "")
        tgt_val = safe_get_node_value(G, e["target"], "")
        if src_val:
            all_factors[src_val] += 1
        if proc_keywords.search(src_val) or proc_keywords.search(tgt_val):
            proc_edges.append((src_val, e["relation"], tgt_val,
                               str(e.get("record_no", ""))))

    lines = [
        f"Dropped-object incidents: {len(drop_incidents):,}",
        f"  With head/hand injury: {len(head_hand_drops):,}",
        f"  With L2 causal edges: {drop_causal['record_no'].nunique():,}",
        f"  Total causal edges: {len(drop_causal):,}",
        "",
        f"Procedural causal edges: {len(proc_edges):,}",
    ]

    # Show procedural edge samples
    if proc_edges:
        lines.append("  Samples:")
        seen = set()
        for src, rel, tgt, rn in proc_edges[:15]:
            key = (src, rel, tgt)
            if key not in seen:
                lines.append(f"    [{rn}] {src} --{rel}--> {tgt}")
                seen.add(key)

    lines.extend(["", "Top causal factors for dropped → head/hand:"])
    for factor, count in all_factors.most_common(10):
        lines.append(f"  {factor}: {count}")

    has_results = len(head_hand_drops) > 0 and len(drop_causal) > 0
    return {
        "coverage": "✅" if has_results else "❌",
        "diagnosis": "CLEAN" if has_results else "L2_REQUIRED",
        "result_summary": (
            f"{len(head_hand_drops):,} incidents; "
            f"{len(proc_edges)} procedural causal edges"
            if has_results else "0 incidents"),
        "detail": "\n".join(lines),
    }


# ── CJ-07: Corrosion effects analysis (L2 traversal) ────────────────────

def corrosion_effects(spec, G, entities_df, relations_df, metadata_df,
                      *, results=None):
    """Find what corrosion causes by tracing L2 CAUSAL edges."""
    causal_edges = relations_df[relations_df["relation"] == "CAUSAL"]

    if len(causal_edges) == 0:
        return {
            "coverage": "❌",
            "diagnosis": "L2_REQUIRED",
            "result_summary": "0 causal edges in graph — L2 merge needed",
            "detail": "No L2 causal edges found. Run merge_l2_edges.py first.",
        }

    # Find CAUSAL edges where source mentions corrosion/rust/degradation
    corrosion_pat = re.compile(
        r"corros|rust|degradat|oxidat|erosion|pitting|deteriorat",
        re.IGNORECASE)

    corrosion_edges = []
    for _, e in causal_edges.iterrows():
        src_val = safe_get_node_value(G, e["source"], "")
        if corrosion_pat.search(src_val):
            tgt_val = safe_get_node_value(G, e["target"], "")
            corrosion_edges.append({
                "source": src_val,
                "target": tgt_val,
                "record_no": str(e.get("record_no", "")),
            })

    # Categorize targets
    categories = {
        "equipment failure": re.compile(
            r"fail|malfunction|break|crack|ruptur|burst|collapse", re.IGNORECASE),
        "leak/release": re.compile(
            r"leak|spill|releas|discharg|seep", re.IGNORECASE),
        "structural damage": re.compile(
            r"structur|damag|weaken|thin|hole|perfora", re.IGNORECASE),
        "loss of containment": re.compile(
            r"containment|breach|integrit", re.IGNORECASE),
        "safety system impact": re.compile(
            r"safe|alarm|detect|protect|barrier|shut.?down", re.IGNORECASE),
    }

    cat_counts = Counter()
    cat_examples = defaultdict(list)
    uncategorized = Counter()

    for edge in corrosion_edges:
        tgt = edge["target"]
        matched = False
        for cat_name, cat_pat in categories.items():
            if cat_pat.search(tgt):
                cat_counts[cat_name] += 1
                if len(cat_examples[cat_name]) < 3:
                    cat_examples[cat_name].append(tgt)
                matched = True
                break
        if not matched:
            uncategorized[tgt] += 1

    unique_records = {e["record_no"] for e in corrosion_edges}

    lines = [
        f"Corrosion-source CAUSAL edges: {len(corrosion_edges)}",
        f"Unique incidents with corrosion causes: {len(unique_records)}",
        "",
        "Effects by category:",
    ]
    for cat, cnt in cat_counts.most_common():
        examples = cat_examples[cat]
        lines.append(f"  {cat}: {cnt} edges (e.g. {examples})")

    if uncategorized:
        lines.append(f"\n  Other effects: {sum(uncategorized.values())} edges")
        for tgt, cnt in uncategorized.most_common(5):
            lines.append(f"    {tgt}: {cnt}")

    has_results = len(corrosion_edges) > 0
    return {
        "coverage": "✅" if has_results else "⚠️",
        "diagnosis": "CLEAN" if has_results else "DATA_SPARSE",
        "result_summary": (
            f"{len(corrosion_edges)} corrosion causal edges across "
            f"{len(unique_records)} incidents"
            if has_results else "No corrosion causal edges found"),
        "detail": "\n".join(lines),
    }


# ── Registry ─────────────────────────────────────────────────────────────

CUSTOM_REGISTRY = {
    "louvain_communities": louvain_communities,
    "equipment_across_regions": equipment_across_regions,
    "hub_centrality": hub_centrality,
    "containment_injury_offshore": containment_injury_offshore,
    "top_injury_per_equipment": top_injury_per_equipment,
    "severity_comparison": severity_comparison,
    "causal_chain_check": causal_chain_check,
    "dual_risk_detection": dual_risk_detection,
    "procedural_dropped_injury": procedural_dropped_injury,
    "corrosion_effects": corrosion_effects,
}
