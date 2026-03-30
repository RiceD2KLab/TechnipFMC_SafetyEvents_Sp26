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
    parse_yearmonth,
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

    coverage = "\u2705" if equip_counts else "\u274c"
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
    causal_rels = ["CAUSAL", "PRECEDED_BY", "FAILED_CONTROL", "MITIGATED_BY"]
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
        src_val = str(safe_get_node_value(G, e["source"], "") or "")
        tgt_val = str(safe_get_node_value(G, e["target"], "") or "")
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
    causal_rels = ["CAUSAL", "PRECEDED_BY", "FAILED_CONTROL", "MITIGATED_BY"]
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
            val = str(safe_get_node_value(G, bp_id, "") or "").lower()
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
        src_val = str(safe_get_node_value(G, e["source"], "") or "")
        tgt_val = str(safe_get_node_value(G, e["target"], "") or "")
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
        src_val = str(safe_get_node_value(G, e["source"], "") or "")
        if corrosion_pat.search(src_val):
            tgt_val = str(safe_get_node_value(G, e["target"], "") or "")
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


# ── IOGP-05: Electrical incidents with LOTO failures (L2 FAILED_CONTROL) ─

def loto_failures_l2(spec, G, entities_df, relations_df, metadata_df,
                     *, results=None):
    """Find electrical/LOTO incidents and trace FAILED_CONTROL edges via L2."""
    if relations_df is None or "relation" not in relations_df.columns:
        return {
            "coverage": "❌",
            "diagnosis": "L2_REQUIRED",
            "result_summary": "0 FAILED_CONTROL edges — L2 merge needed",
            "detail": "No relations data available. Run merge_l2_edges.py first.",
        }
    failed_ctrl_edges = relations_df[relations_df["relation"] == "FAILED_CONTROL"]

    if len(failed_ctrl_edges) == 0:
        return {
            "coverage": "❌",
            "diagnosis": "L2_REQUIRED",
            "result_summary": "0 FAILED_CONTROL edges — L2 merge needed",
            "detail": "No L2 FAILED_CONTROL edges found. Run merge_l2_edges.py first.",
        }

    # Step 1: Find electrical/LOTO incidents via narrative keywords
    loto_keywords = ["lock out", "lockout", "tag out", "tagout", "loto",
                     "energized", "arc flash", "electrical isolation",
                     "de-energi", "deenergiz"]
    loto_record_nos = incidents_matching_narrative(
        metadata_df, loto_keywords, match_all=False)
    loto_incident_ids = {f"INCIDENT::{rn}" for rn in loto_record_nos} & set(G.nodes())

    # Step 2: Filter FAILED_CONTROL edges to LOTO incidents
    loto_fc = failed_ctrl_edges[
        failed_ctrl_edges["record_no"].astype(str).isin(
            {str(rn) for rn in loto_record_nos})]

    # Step 3: Categorize the failed controls (targets of FAILED_CONTROL edges)
    control_counts = Counter()
    sample_edges = []
    seen_keys = set()
    for _, e in loto_fc.iterrows():
        src_val = str(safe_get_node_value(G, e["source"], "") or "")
        tgt_val = str(safe_get_node_value(G, e["target"], "") or "")
        control_counts[tgt_val] += 1
        key = (src_val, tgt_val)
        if key not in seen_keys and len(sample_edges) < 12:
            sample_edges.append((src_val, tgt_val, str(e.get("record_no", "")),
                                 str(e.get("evidence", ""))))
            seen_keys.add(key)

    # Step 4: All FAILED_CONTROL edges (not just LOTO) for overview
    all_fc_counts = Counter()
    for _, e in failed_ctrl_edges.iterrows():
        tgt_val = str(safe_get_node_value(G, e["target"], "") or "")
        if tgt_val:
            all_fc_counts[tgt_val] += 1

    lines = [
        f"Total FAILED_CONTROL edges in graph: {len(failed_ctrl_edges):,}",
        f"LOTO/electrical incidents (narrative match): {len(loto_incident_ids):,}",
        f"  With FAILED_CONTROL edges: {loto_fc['record_no'].nunique():,}",
        f"  FAILED_CONTROL edges in LOTO incidents: {len(loto_fc):,}",
        "",
        "Top failed controls in LOTO incidents:",
    ]
    for ctrl, cnt in control_counts.most_common(10):
        lines.append(f"  {ctrl or '(unknown)'}: {cnt}")

    if sample_edges:
        lines.extend(["", "Sample edges (hazard --FAILED_CONTROL--> barrier):"])
        for src, tgt, rn, evid in sample_edges:
            evid_str = f" | \"{evid[:60]}\"" if evid and evid != "nan" else ""
            lines.append(f"  [{rn}] {src} --> {tgt}{evid_str}")

    lines.extend(["", "Top failed controls across all incidents:"])
    for ctrl, cnt in all_fc_counts.most_common(10):
        lines.append(f"  {ctrl or '(unknown)'}: {cnt}")

    has_results = len(loto_incident_ids) > 0 and len(loto_fc) > 0
    return {
        "coverage": "✅" if has_results else "⚠️",
        "diagnosis": "CLEAN" if has_results else "DATA_SPARSE",
        "result_summary": (
            f"{len(loto_incident_ids):,} incidents; "
            f"{len(loto_fc):,} FAILED_CONTROL edges"
            if has_results else f"{len(loto_incident_ids):,} incidents, 0 FAILED_CONTROL edges"),
        "detail": "\n".join(lines),
    }


# ── GL-05: Equipment–body-part co-occurrence ─────────────────────────────

def equipment_bodypart_cooccurrence(spec, G, entities_df, relations_df,
                                     metadata_df, *, results=None):
    """Find most common (equipment, body_part) pairs across incidents."""
    equipment_nodes = set(
        entities_df[entities_df["entity_type"] == "EQUIPMENT"]["entity_id"])
    bodypart_nodes = set(
        entities_df[entities_df["entity_type"] == "BODY_PART"]["entity_id"])

    pair_counts = Counter()
    incident_nodes = [n for n in G.nodes if n.startswith("INCIDENT::")]

    for inc_id in incident_nodes:
        equips = [
            safe_get_node_value(G, nbr)
            for nbr in G.successors(inc_id)
            if nbr in equipment_nodes
            and G.nodes[nbr].get("entity_type") == "EQUIPMENT"]
        bps = [
            safe_get_node_value(G, nbr)
            for nbr in G.successors(inc_id)
            if nbr in bodypart_nodes
            and G.nodes[nbr].get("entity_type") == "BODY_PART"]
        for eq in equips:
            for bp in bps:
                if eq and bp:
                    pair_counts[(eq, bp)] += 1

    top_n = pair_counts.most_common(spec.output_top_n)
    lines = [f"Total distinct (equipment, body_part) pairs: {len(pair_counts)}",
             f"Top {spec.output_top_n}:"]
    for (eq, bp), cnt in top_n:
        lines.append(f"  {eq} + {bp}: {cnt} incidents")

    return {
        "coverage": "✅" if pair_counts else "❌",
        "diagnosis": "CLEAN",
        "result_summary": f"{len(pair_counts)} equipment–body part pairs",
        "detail": "\n".join(lines),
    }


# ── GL-06: Client safety comparison ─────────────────────────────────────

def client_safety_comparison(spec, G, entities_df, relations_df,
                              metadata_df, *, results=None):
    """Compare safety profiles (severity, incident type) for top 5 clients."""
    org_nodes = entities_df[entities_df["entity_type"] == "ORGANIZATION"]
    org_counts = Counter()
    for ent_id in org_nodes["entity_id"]:
        deg = len(get_incidents_for_entity(G, ent_id, "REPORTED_BY"))
        if deg > 0:
            val = safe_get_node_value(G, ent_id)
            if val:
                org_counts[val] = max(org_counts[val], deg)

    top5 = org_counts.most_common(5)
    lines = ["Top 5 clients by incident count:"]

    for org_val, total in top5:
        org_entities = find_entities_by_value(
            entities_df, "ORGANIZATION", f"^{re.escape(org_val)}$")
        incidents = set()
        for ent_id in org_entities:
            incidents.update(
                get_incidents_for_entity(G, ent_id, "REPORTED_BY"))

        sev_dist = Counter()
        type_dist = Counter()
        for inc_id in incidents:
            sev = get_incident_property(G, inc_id, "severity_bin")
            itype = get_incident_property(G, inc_id, "incident_type")
            if pd.notna(sev):
                sev_dist[int(sev)] += 1
            if itype:
                type_dist[str(itype)] += 1

        mean_sev = (sum(k * v for k, v in sev_dist.items())
                    / max(sum(sev_dist.values()), 1))
        lines.append(f"\n  {org_val} ({total} incidents):")
        lines.append(f"    Types: {dict(type_dist)}")
        lines.append(f"    Severity dist: {dict(sorted(sev_dist.items()))}")
        lines.append(f"    Mean severity: {mean_sev:.2f}")

    return {
        "coverage": "✅" if top5 else "❌",
        "diagnosis": "CLEAN",
        "result_summary": f"Safety profiles for top {len(top5)} clients",
        "detail": "\n".join(lines),
    }


# ── GL-07: Seasonal (monthly) patterns ──────────────────────────────────

def seasonal_patterns(spec, G, entities_df, relations_df, metadata_df,
                      *, results=None):
    """Detect monthly patterns in incident frequency."""
    monthly = Counter()
    for _, row in metadata_df.iterrows():
        ym = parse_yearmonth(row.get("reported_date"))
        if ym:
            month = int(ym.split("-")[1])
            monthly[month] += 1

    month_names = {1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May",
                   6: "Jun", 7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct",
                   11: "Nov", 12: "Dec"}

    lines = ["Monthly incident totals (all years combined):"]
    total = sum(monthly.values())
    expected_avg = total / 12 if total else 1
    peaks = []
    troughs = []
    for m in range(1, 13):
        cnt = monthly.get(m, 0)
        pct_diff = (cnt - expected_avg) / expected_avg * 100
        marker = ""
        if pct_diff > 15:
            marker = " ↑ PEAK"
            peaks.append(month_names[m])
        elif pct_diff < -15:
            marker = " ↓ TROUGH"
            troughs.append(month_names[m])
        lines.append(
            f"  {month_names[m]}: {cnt} ({pct_diff:+.1f}%){marker}")

    lines.extend([
        "",
        f"Peak months (>15% above avg): {', '.join(peaks) or 'none'}",
        f"Trough months (>15% below avg): {', '.join(troughs) or 'none'}",
    ])

    return {
        "coverage": "✅",
        "diagnosis": "CLEAN",
        "result_summary": (
            f"Peaks: {', '.join(peaks) or 'none'}; "
            f"Troughs: {', '.join(troughs) or 'none'}"),
        "detail": "\n".join(lines),
    }


# ── GL-08: Root causes by geographic region ──────────────────────────────

def rcc_by_region(spec, G, entities_df, relations_df, metadata_df,
                  *, results=None):
    """Show top root cause categories for each geographic region."""
    region_nodes = entities_df[
        (entities_df["entity_type"] == "LOCATION")
        & (entities_df["granularity"] == "region")]

    region_rcc = defaultdict(Counter)
    for _, row in region_nodes.iterrows():
        reg_id = row["entity_id"]
        reg_val = row["value"]
        incidents = get_incidents_for_entity(G, reg_id, "OCCURRED_AT")
        for inc_id in incidents:
            rccs = get_entities_for_incident(
                G, inc_id, entity_type="ROOT_CAUSE_CATEGORY",
                relation_type="CATEGORIZED_AS")
            for rcc_id in rccs:
                rcc_val = safe_get_node_value(G, rcc_id)
                if rcc_val:
                    region_rcc[reg_val][rcc_val] += 1

    lines = [f"Regions with RCC data: {len(region_rcc)}"]
    for region in sorted(region_rcc,
                         key=lambda r: -sum(region_rcc[r].values())):
        total = sum(region_rcc[region].values())
        top3 = region_rcc[region].most_common(3)
        lines.append(f"\n  {region} ({total} categorised incidents):")
        for rcc_val, cnt in top3:
            lines.append(f"    {rcc_val}: {cnt}")

    return {
        "coverage": "✅" if region_rcc else "❌",
        "diagnosis": "CLEAN",
        "result_summary": f"RCC breakdown for {len(region_rcc)} regions",
        "detail": "\n".join(lines),
    }


# ── L2-01: Mitigated-by analysis ────────────────────────────────────────

def mitigated_by_analysis(spec, G, entities_df, relations_df, metadata_df,
                          *, results=None):
    """Analyze MITIGATED_BY edges: what controls successfully prevented harm."""
    mit_edges = relations_df[relations_df["relation"] == "MITIGATED_BY"]
    if len(mit_edges) == 0:
        return {
            "coverage": "❌",
            "diagnosis": "L2_REQUIRED",
            "result_summary": "0 MITIGATED_BY edges — L2 merge needed",
            "detail": "No MITIGATED_BY edges found.",
        }

    # Count what mitigated (targets = controls that worked)
    control_counts = Counter()
    harm_counts = Counter()
    sample_edges = []
    for _, e in mit_edges.iterrows():
        src_val = str(safe_get_node_value(G, e["source"], "") or "")
        tgt_val = str(safe_get_node_value(G, e["target"], "") or "")
        if tgt_val:
            control_counts[tgt_val] += 1
        if src_val:
            harm_counts[src_val] += 1
        if len(sample_edges) < 8:
            sample_edges.append((src_val, tgt_val, str(e.get("record_no", ""))))

    lines = [
        f"Total MITIGATED_BY edges: {len(mit_edges):,}",
        f"Unique incidents: {mit_edges['record_no'].nunique():,}",
        "",
        f"Top successful controls/mitigations ({len(control_counts)} distinct):",
    ]
    for ctrl, cnt in control_counts.most_common(spec.output_top_n):
        lines.append(f"  {ctrl}: {cnt}")

    lines.extend(["", "Top harms mitigated:"])
    for harm, cnt in harm_counts.most_common(10):
        lines.append(f"  {harm}: {cnt}")

    lines.extend(["", "Sample edges (harm → control that worked):"])
    for src, tgt, rn in sample_edges:
        lines.append(f"  [{rn}] {src} → {tgt}")

    return {
        "coverage": "✅",
        "diagnosis": "CLEAN",
        "result_summary": (
            f"{len(mit_edges):,} MITIGATED_BY edges, "
            f"{len(control_counts)} distinct controls"),
        "detail": "\n".join(lines),
    }


# ── L2-02: Failed-control overview ──────────────────────────────────────

def failed_control_overview(spec, G, entities_df, relations_df, metadata_df,
                            *, results=None):
    """Analyze all FAILED_CONTROL edges: what barriers failed most often."""
    fc_edges = relations_df[relations_df["relation"] == "FAILED_CONTROL"]
    if len(fc_edges) == 0:
        return {
            "coverage": "❌",
            "diagnosis": "L2_REQUIRED",
            "result_summary": "0 FAILED_CONTROL edges — L2 merge needed",
            "detail": "No FAILED_CONTROL edges found.",
        }

    barrier_counts = Counter()
    hazard_counts = Counter()
    sample_edges = []
    for _, e in fc_edges.iterrows():
        src_val = str(safe_get_node_value(G, e["source"], "") or "")
        tgt_val = str(safe_get_node_value(G, e["target"], "") or "")
        if tgt_val:
            barrier_counts[tgt_val] += 1
        if src_val:
            hazard_counts[src_val] += 1
        if len(sample_edges) < 8:
            sample_edges.append((src_val, tgt_val, str(e.get("record_no", ""))))

    lines = [
        f"Total FAILED_CONTROL edges: {len(fc_edges):,}",
        f"Unique incidents: {fc_edges['record_no'].nunique():,}",
        "",
        f"Top failed barriers ({len(barrier_counts)} distinct):",
    ]
    for barrier, cnt in barrier_counts.most_common(spec.output_top_n):
        lines.append(f"  {barrier}: {cnt}")

    lines.extend(["", "Top hazards with barrier failures:"])
    for hazard, cnt in hazard_counts.most_common(10):
        lines.append(f"  {hazard}: {cnt}")

    lines.extend(["", "Sample edges (hazard → failed barrier):"])
    for src, tgt, rn in sample_edges:
        lines.append(f"  [{rn}] {src} → {tgt}")

    return {
        "coverage": "✅",
        "diagnosis": "CLEAN",
        "result_summary": (
            f"{len(fc_edges):,} FAILED_CONTROL edges, "
            f"{len(barrier_counts)} distinct barriers"),
        "detail": "\n".join(lines),
    }


# ── L2-03: Preceded-by analysis ─────────────────────────────────────────

def preceded_by_analysis(spec, G, entities_df, relations_df, metadata_df,
                         *, results=None):
    """Analyze PRECEDED_BY edges: most common temporal event sequences."""
    pb_edges = relations_df[relations_df["relation"] == "PRECEDED_BY"]
    if len(pb_edges) == 0:
        return {
            "coverage": "❌",
            "diagnosis": "L2_REQUIRED",
            "result_summary": "0 PRECEDED_BY edges — L2 merge needed",
            "detail": "No PRECEDED_BY edges found.",
        }

    sequence_counts = Counter()
    sample_edges = []
    for _, e in pb_edges.iterrows():
        src_val = str(safe_get_node_value(G, e["source"], "") or "")
        tgt_val = str(safe_get_node_value(G, e["target"], "") or "")
        if src_val and tgt_val:
            sequence_counts[(tgt_val, src_val)] += 1  # tgt preceded src
        if len(sample_edges) < 8:
            sample_edges.append((src_val, tgt_val, str(e.get("record_no", ""))))

    lines = [
        f"Total PRECEDED_BY edges: {len(pb_edges):,}",
        f"Unique incidents: {pb_edges['record_no'].nunique():,}",
        "",
        f"Top temporal sequences (A → B means A preceded B):",
    ]
    for (prior, later), cnt in sequence_counts.most_common(spec.output_top_n):
        lines.append(f"  {prior} → {later}: {cnt}")

    lines.extend(["", "Sample edges (event → prior event):"])
    for src, tgt, rn in sample_edges:
        lines.append(f"  [{rn}] {src} preceded by {tgt}")

    return {
        "coverage": "✅",
        "diagnosis": "CLEAN",
        "result_summary": (
            f"{len(pb_edges):,} PRECEDED_BY edges, "
            f"{len(sequence_counts)} distinct sequences"),
        "detail": "\n".join(lines),
    }


# ── L2-04: Causal factors for dropped objects ───────────────────────────

def causal_factors_dropped(spec, G, entities_df, relations_df, metadata_df,
                           *, results=None):
    """Find causal factors for dropped-object incidents via L2 CAUSAL edges."""
    causal_edges = relations_df[relations_df["relation"] == "CAUSAL"]
    if len(causal_edges) == 0:
        return {
            "coverage": "❌",
            "diagnosis": "L2_REQUIRED",
            "result_summary": "0 CAUSAL edges — L2 merge needed",
            "detail": "No L2 CAUSAL edges found.",
        }

    drop_rcc = find_entities_by_value(
        entities_df, "ROOT_CAUSE_CATEGORY",
        r"drop|fall.*object|loose.*material")
    drop_incidents = set()
    for rcc_id in drop_rcc:
        drop_incidents.update(
            get_incidents_for_entity(G, rcc_id, "CATEGORIZED_AS"))
    drop_record_nos = {inc.split("::")[-1] for inc in drop_incidents}

    drop_causal = causal_edges[
        causal_edges["record_no"].astype(str).isin(drop_record_nos)]

    source_counts = Counter()
    for _, e in drop_causal.iterrows():
        src_val = str(safe_get_node_value(G, e["source"], "") or "")
        if src_val:
            source_counts[src_val] += 1

    lines = [
        f"Dropped-object incidents (via RCC): {len(drop_incidents):,}",
        f"With CAUSAL edges: {drop_causal['record_no'].nunique():,}",
        f"Total CAUSAL edges: {len(drop_causal):,}",
        "",
        "Top causal factors for dropped objects:",
    ]
    for factor, cnt in source_counts.most_common(spec.output_top_n):
        lines.append(f"  {factor}: {cnt}")

    return {
        "coverage": "✅" if drop_causal.size > 0 else "❌",
        "diagnosis": "CLEAN" if drop_causal.size > 0 else "L2_REQUIRED",
        "result_summary": (
            f"{len(drop_causal):,} causal edges for "
            f"{len(drop_incidents):,} dropped-object incidents"),
        "detail": "\n".join(lines),
    }


# ── L2-05: Causal factors for vehicle incidents ─────────────────────────

def causal_factors_vehicle(spec, G, entities_df, relations_df, metadata_df,
                           *, results=None):
    """Find causal factors for vehicle/transport incidents via L2 CAUSAL edges."""
    causal_edges = relations_df[relations_df["relation"] == "CAUSAL"]
    if len(causal_edges) == 0:
        return {
            "coverage": "❌",
            "diagnosis": "L2_REQUIRED",
            "result_summary": "0 CAUSAL edges — L2 merge needed",
            "detail": "No L2 CAUSAL edges found.",
        }

    vehicle_rcc = find_entities_by_value(
        entities_df, "ROOT_CAUSE_CATEGORY",
        r"motor vehicle|traffic")
    vehicle_incidents = set()
    for rcc_id in vehicle_rcc:
        vehicle_incidents.update(
            get_incidents_for_entity(G, rcc_id, "CATEGORIZED_AS"))
    vehicle_record_nos = {inc.split("::")[-1] for inc in vehicle_incidents}

    vehicle_causal = causal_edges[
        causal_edges["record_no"].astype(str).isin(vehicle_record_nos)]

    source_counts = Counter()
    for _, e in vehicle_causal.iterrows():
        src_val = str(safe_get_node_value(G, e["source"], "") or "")
        if src_val:
            source_counts[src_val] += 1

    lines = [
        f"Vehicle/traffic incidents (via RCC): {len(vehicle_incidents):,}",
        f"With CAUSAL edges: {vehicle_causal['record_no'].nunique():,}",
        f"Total CAUSAL edges: {len(vehicle_causal):,}",
        "",
        "Top causal factors for vehicle incidents:",
    ]
    for factor, cnt in source_counts.most_common(spec.output_top_n):
        lines.append(f"  {factor}: {cnt}")

    return {
        "coverage": "✅" if vehicle_causal.size > 0 else "❌",
        "diagnosis": "CLEAN" if vehicle_causal.size > 0 else "L2_REQUIRED",
        "result_summary": (
            f"{len(vehicle_causal):,} causal edges for "
            f"{len(vehicle_incidents):,} vehicle incidents"),
        "detail": "\n".join(lines),
    }


# ── L2-06: Causal chains leading to fractures ───────────────────────────

def causal_factors_fracture(spec, G, entities_df, relations_df, metadata_df,
                            *, results=None):
    """Find causal factors leading to fracture injuries via L2 CAUSAL edges."""
    causal_edges = relations_df[relations_df["relation"] == "CAUSAL"]
    if len(causal_edges) == 0:
        return {
            "coverage": "❌",
            "diagnosis": "L2_REQUIRED",
            "result_summary": "0 CAUSAL edges — L2 merge needed",
            "detail": "No L2 CAUSAL edges found.",
        }

    fracture_entities = find_entities_by_value(
        entities_df, "INJURY_TYPE", r"fracture")
    fracture_incidents = set()
    for ent_id in fracture_entities:
        fracture_incidents.update(
            get_incidents_for_entity(G, ent_id, "RESULTED_IN"))
    fracture_record_nos = {inc.split("::")[-1] for inc in fracture_incidents}

    fracture_causal = causal_edges[
        causal_edges["record_no"].astype(str).isin(fracture_record_nos)]

    source_counts = Counter()
    for _, e in fracture_causal.iterrows():
        src_val = str(safe_get_node_value(G, e["source"], "") or "")
        if src_val:
            source_counts[src_val] += 1

    lines = [
        f"Fracture incidents (via INJURY_TYPE): {len(fracture_incidents):,}",
        f"With CAUSAL edges: {fracture_causal['record_no'].nunique():,}",
        f"Total CAUSAL edges: {len(fracture_causal):,}",
        "",
        "Top causal factors leading to fractures:",
    ]
    for factor, cnt in source_counts.most_common(spec.output_top_n):
        lines.append(f"  {factor}: {cnt}")

    return {
        "coverage": "✅" if fracture_causal.size > 0 else "❌",
        "diagnosis": "CLEAN" if fracture_causal.size > 0 else "L2_REQUIRED",
        "result_summary": (
            f"{len(fracture_causal):,} causal edges for "
            f"{len(fracture_incidents):,} fracture incidents"),
        "detail": "\n".join(lines),
    }


# ── EG-01: Extraction gap — burns ────────────────────────────────────────

def _extraction_gap_generic(spec, G, entities_df, relations_df, metadata_df,
                            narr_pattern, entity_type, entity_pattern,
                            relation, label):
    """Generic extraction gap check: narrative mentions X but entity not extracted."""
    narr_re = re.compile(narr_pattern, re.IGNORECASE)
    narr_matches = set()
    for _, row in metadata_df.iterrows():
        narr = str(row.get("narrative") or "")
        if narr_re.search(narr):
            narr_matches.add(str(row["record_no"]))

    entity_incidents = set()
    matched_ents = find_entities_by_value(entities_df, entity_type, entity_pattern)
    for ent_id in matched_ents:
        for inc_id in get_incidents_for_entity(G, ent_id, relation):
            entity_incidents.add(inc_id.split("::")[-1])

    gap = narr_matches - entity_incidents
    extracted = narr_matches & entity_incidents
    gap_rate = len(gap) / max(len(narr_matches), 1) * 100

    # Sample gap incidents
    samples = []
    for rec in sorted(gap)[:5]:
        narr = metadata_df[metadata_df["record_no"].astype(str) == rec]["narrative"]
        if len(narr) > 0:
            samples.append(f"  #{rec}: \"{str(narr.iloc[0])[:120]}...\"")

    lines = [
        f"Narrative mentions '{label}': {len(narr_matches):,}",
        f"  With {entity_type} extracted: {len(extracted):,}",
        f"  WITHOUT {entity_type} extracted (gap): {len(gap):,}",
        f"  Gap rate: {gap_rate:.1f}%",
        "",
        "Sample gap incidents:",
    ] + samples

    return {
        "coverage": "✅",
        "diagnosis": "EXTRACTION_GAP",
        "result_summary": (
            f"{len(gap):,} / {len(narr_matches):,} "
            f"({gap_rate:.0f}%) missing {entity_type}"),
        "detail": "\n".join(lines),
    }


def extraction_gap_burn(spec, G, entities_df, relations_df, metadata_df,
                        *, results=None):
    return _extraction_gap_generic(
        spec, G, entities_df, relations_df, metadata_df,
        narr_pattern=r"\bburn\b",
        entity_type="INJURY_TYPE", entity_pattern=r"burn",
        relation="RESULTED_IN", label="burn")


def extraction_gap_fracture(spec, G, entities_df, relations_df, metadata_df,
                            *, results=None):
    return _extraction_gap_generic(
        spec, G, entities_df, relations_df, metadata_df,
        narr_pattern=r"fracture",
        entity_type="INJURY_TYPE", entity_pattern=r"fracture",
        relation="RESULTED_IN", label="fracture")


def extraction_gap_crane(spec, G, entities_df, relations_df, metadata_df,
                         *, results=None):
    return _extraction_gap_generic(
        spec, G, entities_df, relations_df, metadata_df,
        narr_pattern=r"\bcrane\b",
        entity_type="EQUIPMENT", entity_pattern=r"crane",
        relation="INVOLVED", label="crane")


def extraction_gap_forklift(spec, G, entities_df, relations_df, metadata_df,
                            *, results=None):
    return _extraction_gap_generic(
        spec, G, entities_df, relations_df, metadata_df,
        narr_pattern=r"\bforklift\b",
        entity_type="EQUIPMENT", entity_pattern=r"forklift|flt",
        relation="INVOLVED", label="forklift")


# ── EG-05: Severity >= 4 but no INJURY_TYPE ─────────────────────────────

def extraction_gap_severity_injury(spec, G, entities_df, relations_df,
                                   metadata_df, *, results=None):
    """Find high-severity incidents missing INJURY_TYPE edges."""
    sev4 = set(metadata_df[metadata_df["severity_bin"] >= 4]["record_no"].astype(str))
    has_injury = set()
    for _, e in relations_df[relations_df["relation"] == "RESULTED_IN"].iterrows():
        src = str(e["source"]).replace("INCIDENT::", "")
        tgt_type = entities_df[entities_df["entity_id"] == e["target"]]
        if len(tgt_type) > 0 and tgt_type["entity_type"].iloc[0] == "INJURY_TYPE":
            has_injury.add(src)

    gap = sev4 - has_injury
    gap_rate = len(gap) / max(len(sev4), 1) * 100

    # Get severity breakdown of gap incidents
    gap_meta = metadata_df[metadata_df["record_no"].astype(str).isin(gap)]
    sev_dist = gap_meta["severity_bin"].value_counts().sort_index()

    lines = [
        f"Incidents with severity >= 4: {len(sev4):,}",
        f"  With INJURY_TYPE extracted: {len(sev4) - len(gap):,}",
        f"  WITHOUT INJURY_TYPE (gap): {len(gap):,}",
        f"  Gap rate: {gap_rate:.1f}%",
        "",
        "Severity breakdown of gap incidents:",
    ]
    for sev, cnt in sev_dist.items():
        lines.append(f"  Severity {int(sev)}: {cnt}")

    samples = []
    for _, row in gap_meta.head(5).iterrows():
        samples.append(
            f"  #{row['record_no']} (sev={row['severity_bin']}): "
            f"\"{str(row.get('narrative',''))[:100]}...\"")
    lines.extend(["", "Sample gap incidents:"] + samples)

    return {
        "coverage": "✅",
        "diagnosis": "EXTRACTION_GAP",
        "result_summary": (
            f"{len(gap):,} / {len(sev4):,} "
            f"({gap_rate:.0f}%) high-severity missing INJURY_TYPE"),
        "detail": "\n".join(lines),
    }


# ── EG-06: Impact=Injury but no BODY_PART ────────────────────────────────

def extraction_gap_injury_bodypart(spec, G, entities_df, relations_df,
                                   metadata_df, *, results=None):
    """Find injury-impact incidents missing BODY_PART edges."""
    injury_impact = set(
        metadata_df[metadata_df["impact_type"].astype(str).str.contains(
            "Injury", na=False)]["record_no"].astype(str))
    has_bp = set()
    bp_ents = set(entities_df[entities_df["entity_type"] == "BODY_PART"]["entity_id"])
    for _, e in relations_df[relations_df["relation"] == "AFFECTED"].iterrows():
        if e["target"] in bp_ents:
            has_bp.add(str(e["source"]).replace("INCIDENT::", ""))

    gap = injury_impact - has_bp
    gap_rate = len(gap) / max(len(injury_impact), 1) * 100

    lines = [
        f"Incidents with impact_type=Injury: {len(injury_impact):,}",
        f"  With BODY_PART extracted: {len(injury_impact) - len(gap):,}",
        f"  WITHOUT BODY_PART (gap): {len(gap):,}",
        f"  Gap rate: {gap_rate:.1f}%",
    ]

    return {
        "coverage": "✅",
        "diagnosis": "EXTRACTION_GAP",
        "result_summary": (
            f"{len(gap):,} / {len(injury_impact):,} "
            f"({gap_rate:.0f}%) injury incidents missing BODY_PART"),
        "detail": "\n".join(lines),
    }


# ── EG-07: Short narratives with no entities ─────────────────────────────

def extraction_gap_short_narrative(spec, G, entities_df, relations_df,
                                   metadata_df, *, results=None):
    """Find incidents with very short narratives and no entity extraction."""
    short = metadata_df[metadata_df["narrative"].astype(str).str.len() < 100]
    short_recs = set(short["record_no"].astype(str))

    # Check which have ANY entity edge
    has_entity = set()
    inc_rels = relations_df[relations_df["source"].str.startswith("INCIDENT::")]
    entity_rels = inc_rels[inc_rels["relation"].isin(
        ["INVOLVED", "AFFECTED", "RESULTED_IN"])]
    for src in entity_rels["source"]:
        has_entity.add(src.replace("INCIDENT::", ""))

    short_no_entity = short_recs - has_entity
    short_with_entity = short_recs & has_entity

    # Categorize short narratives
    test_records = set()
    for _, row in short.iterrows():
        narr = str(row.get("narrative", "")).strip().lower()
        if narr in ("test", "ttt", "t", "....", "", "n/a", "na", "-"):
            test_records.add(str(row["record_no"]))

    lines = [
        f"Incidents with narrative < 100 chars: {len(short_recs):,}",
        f"  With entity extraction: {len(short_with_entity):,}",
        f"  Without any entity extraction: {len(short_no_entity):,}",
        f"  Likely test/placeholder records: {len(test_records):,}",
        f"  Genuine short narratives (no entities): "
        f"{len(short_no_entity - test_records):,}",
    ]

    # Sample genuine gaps
    genuine = short[
        short["record_no"].astype(str).isin(short_no_entity - test_records)]
    samples = []
    for _, row in genuine.head(5).iterrows():
        samples.append(
            f"  #{row['record_no']}: \"{str(row.get('narrative',''))[:90]}\"")
    lines.extend(["", "Sample short-narrative gaps:"] + samples)

    return {
        "coverage": "✅",
        "diagnosis": "EXTRACTION_GAP",
        "result_summary": (
            f"{len(short_no_entity):,} short-narrative incidents "
            f"with 0 entity extraction ({len(test_records)} test records)"),
        "detail": "\n".join(lines),
    }


# ── EG-08: Foreign language narratives ────────────────────────────────────

def extraction_gap_foreign_language(spec, G, entities_df, relations_df,
                                    metadata_df, *, results=None):
    """Detect non-English narratives and compare extraction rates."""
    lang_markers = {
        "Portuguese": [r"\bdurante\b", r"\btrabalhador\b", r"\bincidente\b",
                       r"\bequipamento\b"],
        "French": [r"\bopération\b", r"\btravailleur\b", r"\bincident\b",
                   r"\béquipement\b"],
        "Spanish": [r"\bdurante\b", r"\btrabajador\b", r"\bincidente\b",
                    r"\bequipo\b"],
        "Russian": [r"[а-яА-Я]{3,}"],
    }

    inc_rels = relations_df[relations_df["source"].str.startswith("INCIDENT::")]
    entity_rels = inc_rels[inc_rels["relation"].isin(
        ["INVOLVED", "AFFECTED", "RESULTED_IN"])]
    entity_per_inc = entity_rels.groupby("source").size()

    all_inc_ids = set(f"INCIDENT::{r}" for r in metadata_df["record_no"].astype(str))
    english_entity_counts = []
    for iid in all_inc_ids:
        english_entity_counts.append(entity_per_inc.get(iid, 0))
    import numpy as np
    english_mean = np.mean(english_entity_counts) if english_entity_counts else 0

    lines = [f"Overall mean entity extraction per incident: {english_mean:.2f}", ""]
    total_foreign = 0
    total_gap = 0

    for lang, markers in lang_markers.items():
        combined = "|".join(markers)
        foreign = metadata_df[metadata_df["narrative"].astype(str).str.contains(
            combined, case=False, na=False, regex=True)]
        if len(foreign) == 0:
            continue

        foreign_recs = set(foreign["record_no"].astype(str))
        foreign_inc_ids = {f"INCIDENT::{r}" for r in foreign_recs}
        foreign_counts = [entity_per_inc.get(iid, 0) for iid in foreign_inc_ids]
        foreign_mean = np.mean(foreign_counts) if foreign_counts else 0
        zero_extraction = sum(1 for c in foreign_counts if c == 0)

        total_foreign += len(foreign)
        total_gap += zero_extraction

        lines.append(
            f"{lang}: {len(foreign):,} incidents, "
            f"mean entities={foreign_mean:.2f} "
            f"(vs {english_mean:.2f} overall), "
            f"{zero_extraction} with zero extraction")

    lines.extend(["", f"Total non-English incidents: {total_foreign:,}",
                   f"Total with zero extraction: {total_gap:,}"])

    return {
        "coverage": "✅",
        "diagnosis": "EXTRACTION_GAP",
        "result_summary": (
            f"{total_foreign:,} non-English incidents, "
            f"{total_gap:,} with zero entity extraction"),
        "detail": "\n".join(lines),
    }


# ── Similarity helpers (lazy-loaded from event_similarity) ────────────────

_SIM_CACHE = {}  # module-level cache for embeddings + model


def _load_similarity():
    """Lazily load text embeddings and structural similarity data."""
    if _SIM_CACHE:
        return _SIM_CACHE

    import pickle
    from pathlib import Path

    root = Path(__file__).resolve().parent.parent.parent
    sim_dir = root / "event_similarity" / "outputs"

    # Text embeddings: {record_no_str: np.ndarray(384,)}
    text_path = sim_dir / "text_embeddings.pkl"
    if text_path.exists():
        with open(text_path, "rb") as f:
            _SIM_CACHE["text"] = pickle.load(f)
    else:
        _SIM_CACHE["text"] = {}

    # Node2Vec embeddings
    n2v_path = sim_dir / "node2vec_embeddings.pkl"
    if n2v_path.exists():
        with open(n2v_path, "rb") as f:
            _SIM_CACHE["node2vec"] = pickle.load(f)
    else:
        _SIM_CACHE["node2vec"] = {}

    # TransE embeddings
    transe_path = sim_dir / "transe_embeddings.pkl"
    if transe_path.exists():
        with open(transe_path, "rb") as f:
            _SIM_CACHE["transe"] = pickle.load(f)
    else:
        _SIM_CACHE["transe"] = {}

    return _SIM_CACHE


def _top_k_text(seed_record, k=10):
    """Find top-k most similar incidents by text embedding cosine similarity."""
    import numpy as np

    cache = _load_similarity()
    text_emb = cache.get("text", {})
    if seed_record not in text_emb:
        return []

    seed_vec = text_emb[seed_record]
    scores = []
    for rec, vec in text_emb.items():
        if rec == seed_record:
            continue
        sim = float(np.dot(seed_vec, vec))  # unit-normalized → dot = cosine
        scores.append((rec, sim))

    scores.sort(key=lambda x: -x[1])
    return scores[:k]


def _top_k_text_from_query(query_text, k=10):
    """Find top-k incidents similar to a free-text query string."""
    import numpy as np
    from pathlib import Path

    cache = _load_similarity()
    text_emb = cache.get("text", {})
    if not text_emb:
        return []

    # Lazy-load the sentence-transformer model
    if "model" not in cache:
        try:
            from sentence_transformers import SentenceTransformer
            cache["model"] = SentenceTransformer(
                "sentence-transformers/all-MiniLM-L6-v2")
        except ImportError:
            return []

    model = cache["model"]
    query_vec = model.encode([query_text], normalize_embeddings=True)[0]

    scores = []
    for rec, vec in text_emb.items():
        sim = float(np.dot(query_vec, vec))
        scores.append((rec, sim))

    scores.sort(key=lambda x: -x[1])
    return scores[:k]


# ── GL-17: Seed-based hybrid similarity retrieval ─────────────────────────

def _similarity_seed(spec, G, entities_df, relations_df, metadata_df,
                     seed_record, *, results=None):
    """Generic seed-based similarity retrieval."""
    top_text = _top_k_text(seed_record, k=10)

    if not top_text:
        return {
            "coverage": "❌",
            "diagnosis": "DATA_SPARSE",
            "result_summary": f"No text embeddings for incident #{seed_record}",
            "detail": "Text embeddings not found. Run event_similarity first.",
        }

    lines = [f"Seed incident: #{seed_record}",
             "", "Top 10 most similar incidents (text embedding cosine):"]

    for rec, sim in top_text:
        inc_id = f"INCIDENT::{rec}"
        label = get_incident_property(G, inc_id, "incident_type") or "?"
        sev = get_incident_property(G, inc_id, "severity_bin") or "?"
        equips = get_entities_for_incident(
            G, inc_id, entity_type="EQUIPMENT", relation_type="INVOLVED")
        eq_vals = [safe_get_node_value(G, e) for e in equips[:3]]
        lines.append(f"  #{rec} (sim={sim:.3f}) type={label} sev={sev} "
                     f"eq={eq_vals}")

    # Check structural overlap: how many share equipment type with seed?
    seed_id = f"INCIDENT::{seed_record}"
    seed_equips = {safe_get_node_value(G, e)
                   for e in get_entities_for_incident(
                       G, seed_id, entity_type="EQUIPMENT",
                       relation_type="INVOLVED")}
    hits = 0
    for rec, _ in top_text:
        inc_id = f"INCIDENT::{rec}"
        nbr_equips = {safe_get_node_value(G, e)
                      for e in get_entities_for_incident(
                          G, inc_id, entity_type="EQUIPMENT",
                          relation_type="INVOLVED")}
        if seed_equips & nbr_equips:
            hits += 1

    hit_rate = hits / max(len(top_text), 1) * 100
    lines.extend([
        "",
        f"Seed equipment: {sorted(seed_equips)}",
        f"Equipment overlap (hit rate): {hits}/{len(top_text)} ({hit_rate:.0f}%)",
    ])

    return {
        "coverage": "✅",
        "diagnosis": "CLEAN",
        "result_summary": (
            f"Top 10 similar to #{seed_record}, "
            f"{hit_rate:.0f}% equipment overlap"),
        "detail": "\n".join(lines),
    }


def similarity_seed_incident(spec, G, entities_df, relations_df, metadata_df,
                             *, results=None):
    return _similarity_seed(spec, G, entities_df, relations_df, metadata_df,
                            "29857", results=results)


def similarity_seed_incident_2(spec, G, entities_df, relations_df, metadata_df,
                               *, results=None):
    return _similarity_seed(spec, G, entities_df, relations_df, metadata_df,
                            "569346", results=results)


# ── GL-19/20: Structural hit rate for equipment-specific queries ──────────

def _similarity_hit_rate(spec, G, entities_df, relations_df, metadata_df,
                         equipment_pattern, incident_type_filter=None,
                         *, results=None):
    """Pick a seed incident matching equipment pattern, find top-10 text-similar,
    measure how many share the same equipment type."""
    # Find a seed incident with this equipment
    equip_ents = find_entities_by_value(entities_df, "EQUIPMENT", equipment_pattern)
    seed_record = None
    for eid in equip_ents:
        incidents = get_incidents_for_entity(G, eid, "INVOLVED")
        for inc_id in incidents:
            if incident_type_filter:
                itype = get_incident_property(G, inc_id, "incident_type")
                if itype and incident_type_filter.lower() in str(itype).lower():
                    seed_record = inc_id.split("::")[-1]
                    break
            else:
                seed_record = inc_id.split("::")[-1]
                break
        if seed_record:
            break

    if not seed_record:
        return {
            "coverage": "❌",
            "diagnosis": "DATA_SPARSE",
            "result_summary": f"No matching seed for {equipment_pattern}",
            "detail": "Could not find a seed incident.",
        }

    top_text = _top_k_text(seed_record, k=10)
    if not top_text:
        return {
            "coverage": "❌",
            "diagnosis": "DATA_SPARSE",
            "result_summary": "No text embeddings available",
            "detail": "Run event_similarity first.",
        }

    # Check how many top-10 share the same equipment pattern
    equip_re = re.compile(equipment_pattern, re.IGNORECASE)
    hits = 0
    lines = [f"Seed: #{seed_record} (equipment={equipment_pattern})", ""]

    for rec, sim in top_text:
        inc_id = f"INCIDENT::{rec}"
        nbr_equips = [
            safe_get_node_value(G, e)
            for e in get_entities_for_incident(
                G, inc_id, entity_type="EQUIPMENT",
                relation_type="INVOLVED")]
        match = any(equip_re.search(str(v or "")) for v in nbr_equips)
        if match:
            hits += 1
        marker = "✓" if match else "✗"
        lines.append(f"  {marker} #{rec} (sim={sim:.3f}) eq={nbr_equips[:3]}")

    hit_rate = hits / max(len(top_text), 1) * 100
    lines.extend(["", f"Hit rate: {hits}/10 ({hit_rate:.0f}%)"])

    return {
        "coverage": "✅",
        "diagnosis": "CLEAN",
        "result_summary": f"{hit_rate:.0f}% hit rate for {equipment_pattern} retrieval",
        "detail": "\n".join(lines),
    }


def similarity_hit_rate_forklift(spec, G, entities_df, relations_df,
                                 metadata_df, *, results=None):
    return _similarity_hit_rate(
        spec, G, entities_df, relations_df, metadata_df,
        r"forklift|flt", "accident", results=results)


def similarity_hit_rate_crane(spec, G, entities_df, relations_df,
                              metadata_df, *, results=None):
    return _similarity_hit_rate(
        spec, G, entities_df, relations_df, metadata_df,
        r"crane", "near miss", results=results)


# ── GL-21: Method agreement analysis ─────────────────────────────────────

def similarity_method_agreement(spec, G, entities_df, relations_df,
                                metadata_df, *, results=None):
    """Compare text vs KG embedding rankings for a sample of incidents."""
    import numpy as np

    cache = _load_similarity()
    text_emb = cache.get("text", {})
    n2v_emb = cache.get("node2vec", {})

    if not text_emb:
        return {
            "coverage": "❌",
            "diagnosis": "DATA_SPARSE",
            "result_summary": "No embeddings available",
            "detail": "Run event_similarity first.",
        }

    # Pick 20 random seed incidents that have both text + node2vec
    common = sorted(set(text_emb.keys()) & set(n2v_emb.keys()))[:20]
    if len(common) < 5:
        return {
            "coverage": "⚠️",
            "diagnosis": "DATA_SPARSE",
            "result_summary": f"Only {len(common)} incidents with both embeddings",
            "detail": "Need text + node2vec embeddings for comparison.",
        }

    overlaps = []
    for seed in common:
        text_top = {r for r, _ in _top_k_text(seed, k=10)}
        # Node2Vec top-k
        seed_vec = n2v_emb[seed]
        n2v_scores = []
        for rec, vec in n2v_emb.items():
            if rec == seed:
                continue
            sim = float(np.dot(seed_vec, vec))
            n2v_scores.append((rec, sim))
        n2v_scores.sort(key=lambda x: -x[1])
        n2v_top = {r for r, _ in n2v_scores[:10]}

        overlap = len(text_top & n2v_top) / 10
        overlaps.append(overlap)

    mean_overlap = np.mean(overlaps)
    lines = [
        f"Compared text vs node2vec top-10 for {len(common)} seed incidents",
        f"Mean overlap (Jaccard@10): {mean_overlap:.2%}",
        "",
        "Per-seed overlap:",
    ]
    for seed, ov in zip(common[:10], overlaps[:10]):
        lines.append(f"  #{seed}: {ov:.0%}")

    return {
        "coverage": "✅",
        "diagnosis": "CLEAN",
        "result_summary": f"Text vs Node2Vec mean overlap: {mean_overlap:.1%}",
        "detail": "\n".join(lines),
    }


# ── GL-22/23: Free-text semantic search ───────────────────────────────────

def _similarity_text_query(spec, G, entities_df, relations_df, metadata_df,
                           query_text, *, results=None):
    """Semantic search: find incidents similar to a free-text query."""
    top = _top_k_text_from_query(query_text, k=10)

    if not top:
        return {
            "coverage": "❌",
            "diagnosis": "DATA_SPARSE",
            "result_summary": "No text embeddings or model unavailable",
            "detail": "Needs sentence-transformers + pre-computed embeddings.",
        }

    lines = [f'Query: "{query_text}"', "",
             "Top 10 semantically similar incidents:"]
    for rec, sim in top:
        inc_id = f"INCIDENT::{rec}"
        label = get_incident_property(G, inc_id, "incident_type") or "?"
        sev = get_incident_property(G, inc_id, "severity_bin") or "?"
        equips = [safe_get_node_value(G, e)
                  for e in get_entities_for_incident(
                      G, inc_id, entity_type="EQUIPMENT",
                      relation_type="INVOLVED")[:3]]
        injuries = [safe_get_node_value(G, e)
                    for e in get_entities_for_incident(
                        G, inc_id, entity_type="INJURY_TYPE",
                        relation_type="RESULTED_IN")[:2]]
        lines.append(f"  #{rec} (sim={sim:.3f}) {label}/sev={sev} "
                     f"eq={equips} inj={injuries}")

    return {
        "coverage": "✅",
        "diagnosis": "CLEAN",
        "result_summary": (
            f"Top match: #{top[0][0]} (sim={top[0][1]:.3f})"),
        "detail": "\n".join(lines),
    }


def similarity_text_query(spec, G, entities_df, relations_df, metadata_df,
                          *, results=None):
    return _similarity_text_query(
        spec, G, entities_df, relations_df, metadata_df,
        "worker fell from scaffold due to missing guardrail",
        results=results)


def similarity_text_query_2(spec, G, entities_df, relations_df, metadata_df,
                            *, results=None):
    return _similarity_text_query(
        spec, G, entities_df, relations_df, metadata_df,
        "crane load dropped because sling failed under tension",
        results=results)


# ── GL-24: Equipment patterns in high-severity neighborhoods ──────────────

def similarity_severity_equipment(spec, G, entities_df, relations_df,
                                  metadata_df, *, results=None):
    """For high-severity incidents, find top-10 similar and tally equipment."""
    cache = _load_similarity()
    text_emb = cache.get("text", {})
    if not text_emb:
        return {
            "coverage": "❌",
            "diagnosis": "DATA_SPARSE",
            "result_summary": "No text embeddings available",
            "detail": "Run event_similarity first.",
        }

    # Find high-severity incidents (sev >= 4) with embeddings
    sev4_records = []
    for _, row in metadata_df.iterrows():
        if pd.notna(row.get("severity_bin")) and row["severity_bin"] >= 4:
            rec = str(row["record_no"])
            if rec in text_emb:
                sev4_records.append(rec)

    if not sev4_records:
        return {
            "coverage": "❌",
            "diagnosis": "DATA_SPARSE",
            "result_summary": "No high-severity incidents with embeddings",
            "detail": "",
        }

    # For each high-sev incident, find top-10 similar, tally equipment
    neighbor_equip = Counter()
    for seed in sev4_records[:50]:  # sample up to 50
        top = _top_k_text(seed, k=10)
        for rec, _ in top:
            inc_id = f"INCIDENT::{rec}"
            equips = get_entities_for_incident(
                G, inc_id, entity_type="EQUIPMENT",
                relation_type="INVOLVED")
            for eid in equips:
                val = safe_get_node_value(G, eid)
                if val:
                    neighbor_equip[val] += 1

    lines = [
        f"High-severity incidents sampled: {min(len(sev4_records), 50)}",
        f"Total high-severity with embeddings: {len(sev4_records)}",
        "",
        "Most common equipment in similar-incident neighborhoods:",
    ]
    for eq, cnt in neighbor_equip.most_common(spec.output_top_n):
        lines.append(f"  {eq}: {cnt}")

    return {
        "coverage": "✅",
        "diagnosis": "CLEAN",
        "result_summary": (
            f"Top equipment in high-sev neighborhoods: "
            f"{neighbor_equip.most_common(3)}"),
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
    "loto_failures_l2": loto_failures_l2,
    "equipment_bodypart_cooccurrence": equipment_bodypart_cooccurrence,
    "client_safety_comparison": client_safety_comparison,
    "seasonal_patterns": seasonal_patterns,
    "rcc_by_region": rcc_by_region,
    "mitigated_by_analysis": mitigated_by_analysis,
    "failed_control_overview": failed_control_overview,
    "preceded_by_analysis": preceded_by_analysis,
    "causal_factors_dropped": causal_factors_dropped,
    "causal_factors_vehicle": causal_factors_vehicle,
    "causal_factors_fracture": causal_factors_fracture,
    "extraction_gap_burn": extraction_gap_burn,
    "extraction_gap_fracture": extraction_gap_fracture,
    "extraction_gap_crane": extraction_gap_crane,
    "extraction_gap_forklift": extraction_gap_forklift,
    "extraction_gap_severity_injury": extraction_gap_severity_injury,
    "extraction_gap_injury_bodypart": extraction_gap_injury_bodypart,
    "extraction_gap_short_narrative": extraction_gap_short_narrative,
    "extraction_gap_foreign_language": extraction_gap_foreign_language,
    "similarity_seed_incident": similarity_seed_incident,
    "similarity_seed_incident_2": similarity_seed_incident_2,
    "similarity_hit_rate_forklift": similarity_hit_rate_forklift,
    "similarity_hit_rate_crane": similarity_hit_rate_crane,
    "similarity_method_agreement": similarity_method_agreement,
    "similarity_text_query": similarity_text_query,
    "similarity_text_query_2": similarity_text_query_2,
    "similarity_severity_equipment": similarity_severity_equipment,
}
