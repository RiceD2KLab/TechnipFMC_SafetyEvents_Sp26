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
                injury_counts[G.nodes[inj]["value"]] += 1

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


# ── CJ-01: Causal chain check (L2 required) ─────────────────────────────

def causal_chain_check(spec, G, entities_df, relations_df, metadata_df,
                       *, results=None):
    causal_edges = relations_df[relations_df["relation"].isin(
        ["CAUSED_BY", "CONTRIBUTED_TO", "LED_TO"])]
    corrosion_narr = incidents_matching_narrative(
        metadata_df, ["corrosion"])
    fire_rcc = find_entities_by_value(
        entities_df, "ROOT_CAUSE_CATEGORY",
        r"fire|explosion|flammable")
    fire_rcc_vals = [safe_get_node_value(G, e)
                     for e in fire_rcc if e in G]
    fire_incidents = set()
    for rcc_id in fire_rcc:
        fire_incidents.update(
            get_incidents_for_entity(G, rcc_id, "CATEGORIZED_AS"))

    approx_result = ({f"INCIDENT::{r}" for r in corrosion_narr}
                     & fire_incidents)

    lines = [
        f"Causal edges in graph: {len(causal_edges)} (EXPECTED: 0)",
        "\u26a0\ufe0f True causal chain query CANNOT be answered at L1",
        "",
        "Approximate fallback "
        "(narrative 'corrosion' intersection fire/explosion RCC):",
        f"  Corrosion narratives: {len(corrosion_narr)}",
        f"  Fire/explosion RCC values: {fire_rcc_vals}",
        f"  Fire/explosion incidents: {len(fire_incidents)}",
        f"  Intersection: {len(approx_result)}",
    ]
    if approx_result:
        lines.append(f"  Sample: {sorted(approx_result)[:5]}")

    return {
        "coverage": "\u274c",
        "diagnosis": "L2_REQUIRED",
        "result_summary":
            f"0 causal edges; approximate: {len(approx_result)} incidents",
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
}
