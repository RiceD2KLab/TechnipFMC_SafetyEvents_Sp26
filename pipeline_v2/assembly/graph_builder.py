"""Step 3: Graph assembly — combine GLiNER + metadata into v2 schema graph."""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config.schema_v2 import ALLOWED_RELATIONS, HIERARCHY_RELATION, RELATION_MAP


def _is_valid_value(val: object) -> bool:
    """Return False for null, NaN, empty, or placeholder string values."""
    if val is None:
        return False
    s = str(val).strip()
    if s == "" or s.lower() in ("nan", "none", "null", "unknown"):
        return False
    if "please update" in s.lower():
        return False
    return True


def make_entity_id(entity_type: str, entity_value: str) -> str:
    """Create deterministic entity ID from type + normalized value."""
    normalized = entity_value.strip().upper()
    return f"{entity_type}::{normalized}"


def build_graph(
    gliner_df: pd.DataFrame,
    metadata_df: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Build node and edge lists from extraction outputs.

    Returns (nodes_df, edges_df).
    """
    # Normalize record_no to string in both DataFrames for consistent joins
    if "record_no" in gliner_df.columns:
        gliner_df = gliner_df.copy()
        gliner_df["record_no"] = gliner_df["record_no"].astype(str)
    if "record_no" in metadata_df.columns:
        metadata_df = metadata_df.copy()
        metadata_df["record_no"] = metadata_df["record_no"].astype(str)

    nodes: dict[str, dict[str, Any]] = {}
    edges: list[dict[str, Any]] = []
    seen_edges: set[tuple[str, str, str]] = set()

    def _add_edge(source: str, target: str, relation: str, props: dict[str, Any]) -> None:
        key = (source, target, relation)
        if key in seen_edges:
            return
        seen_edges.add(key)
        edges.append({"source": source, "target": target, "relation": relation, **props})

    # ── Process metadata: create Incident nodes + metadata-derived edges ──
    for _, row in metadata_df.iterrows():
        record_no = row["record_no"]
        inc_id = f"INCIDENT::{record_no}"

        # Create Incident node with properties
        nodes[inc_id] = {
            "entity_id": inc_id,
            "entity_type": "INCIDENT",
            "value": row.get("incident_label") or str(record_no),
            "incident_type": row.get("incident_type"),
            "severity": row.get("severity"),
            "severity_bin": row.get("severity_bin"),
            "likelihood": row.get("likelihood"),
            "impact_type": row.get("impact_type"),
            "work_process": row.get("work_process"),
            "reported_date": row.get("reported_date"),
            "event_datetime": row.get("event_datetime"),
            "risk_color": row.get("risk_color"),
            "business_unit": row.get("business_unit"),
        }

        # OCCURRED_AT — one edge per location granularity level
        for granularity in ("site", "city", "country", "region"):
            loc_value = row.get(f"loc_{granularity}")
            if not _is_valid_value(loc_value):
                continue
            loc_id = make_entity_id("LOCATION", f"{granularity}:{loc_value}")
            if loc_id not in nodes:
                nodes[loc_id] = {
                    "entity_id": loc_id,
                    "entity_type": "LOCATION",
                    "value": str(loc_value).strip(),
                    "granularity": granularity,
                }
            _add_edge(inc_id, loc_id, "OCCURRED_AT",
                      {"granularity": granularity, "layer": "L1", "source_type": "metadata",
                           "confidence": 1.0})

        # REPORTED_BY — from CLIENT
        client = row.get("client")
        if _is_valid_value(client):
            client_str = str(client).strip()
            org_id = make_entity_id("ORGANIZATION", client_str)
            if org_id not in nodes:
                nodes[org_id] = {"entity_id": org_id, "entity_type": "ORGANIZATION", "value": client_str}
            _add_edge(inc_id, org_id, "REPORTED_BY",
                      {"layer": "L1", "source_type": "metadata", "confidence": 1.0})

        # CATEGORIZED_AS — from CASE_CATEGORIZATION
        case_cat = row.get("case_categorization")
        if _is_valid_value(case_cat):
            cat_str = str(case_cat).strip()
            rcc_id = make_entity_id("ROOT_CAUSE_CATEGORY", cat_str)
            if rcc_id not in nodes:
                nodes[rcc_id] = {"entity_id": rcc_id, "entity_type": "ROOT_CAUSE_CATEGORY", "value": cat_str}
            _add_edge(inc_id, rcc_id, "CATEGORIZED_AS",
                      {"layer": "L1", "source_type": "metadata", "confidence": 1.0})

        # IMPACT_TYPE — stored as incident property only (not an entity).
        # Rationale: IMPACT_TYPE values like "Financial Impact", "Environment"
        # are not injury types; mapping them to INJURY_TYPE created mega-hubs.

    # ── Process GLiNER entities ───────────────────────────────────────────
    orphaned_records: set[str] = set()
    unknown_types: set[str] = set()

    for _, row in gliner_df.iterrows():
        record_no = row["record_no"]
        inc_id = f"INCIDENT::{record_no}"
        entity_type = str(row["type"])
        span_text = str(row["span"]).strip()
        score = float(row.get("score", 0.0))

        if entity_type not in RELATION_MAP:
            unknown_types.add(entity_type)
            continue

        # Guard: skip if no matching INCIDENT node from metadata
        if inc_id not in nodes:
            orphaned_records.add(record_no)
            continue

        relation = RELATION_MAP[entity_type]
        ent_id = make_entity_id(entity_type, span_text)

        if ent_id not in nodes:
            nodes[ent_id] = {"entity_id": ent_id, "entity_type": entity_type, "value": span_text}

        _add_edge(inc_id, ent_id, relation,
                  {"layer": "L1", "source_type": "narrative", "confidence": score})

    if orphaned_records:
        print(f"  WARNING: {len(orphaned_records)} GLiNER record_nos have no matching INCIDENT node (skipped)")
    if unknown_types:
        print(f"  WARNING: GLiNER returned unknown entity types (skipped): {unknown_types}")

    # ── Location hierarchy edges (LOCATED_IN: finer → coarser) ────────────
    for _, row in metadata_df.iterrows():
        levels: list[tuple[str, str]] = []
        for granularity in ("site", "city", "country", "region"):
            loc_value = row.get(f"loc_{granularity}")
            if _is_valid_value(loc_value):
                loc_id = make_entity_id("LOCATION", f"{granularity}:{loc_value}")
                levels.append((granularity, loc_id))

        for i in range(len(levels) - 1):
            _add_edge(levels[i][1], levels[i + 1][1], HIERARCHY_RELATION,
                      {"layer": "L1", "source_type": "metadata", "confidence": 1.0})

    # ── Convert to DataFrames ─────────────────────────────────────────────
    nodes_df = pd.DataFrame(list(nodes.values()))
    edges_df = pd.DataFrame(edges)

    # Validate: no disallowed relation types
    if not edges_df.empty:
        bad = edges_df[~edges_df["relation"].isin(ALLOWED_RELATIONS)]
        if not bad.empty:
            print(f"WARNING: {len(bad)} edges with disallowed relation types: {bad['relation'].unique().tolist()}")

    return nodes_df, edges_df
