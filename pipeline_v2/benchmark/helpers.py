"""Helper functions for benchmark queries."""

import pandas as pd
import networkx as nx
from collections import Counter
from pathlib import Path
from dateutil import parser as dateparser
import warnings

warnings.filterwarnings("ignore", category=UserWarning)

BASE = Path(__file__).resolve().parent.parent


def load_data():
    """Load parquet files and build NetworkX graph."""
    print("Loading parquet files...")
    entities_df = pd.read_parquet(BASE / "outputs" / "entities.parquet")
    relations_df = pd.read_parquet(BASE / "outputs" / "relations.parquet")
    metadata_df = pd.read_parquet(BASE / "outputs" / "metadata_parsed.parquet")

    print(f"  Entities: {len(entities_df):,}")
    print(f"  Relations: {len(relations_df):,}")
    print(f"  Metadata: {len(metadata_df):,}")

    print("Building NetworkX graph...")
    G = nx.DiGraph()
    for _, node in entities_df.iterrows():
        G.add_node(node["entity_id"], **{k: v for k, v in node.items()
                                          if k != "entity_id" and pd.notna(v)})
    for _, edge in relations_df.iterrows():
        source, target = edge["source"], edge["target"]
        if source in G and target in G:
            G.add_edge(source, target, relation=edge["relation"])

    print(f"  Graph: {G.number_of_nodes():,} nodes, {G.number_of_edges():,} edges")
    return G, entities_df, relations_df, metadata_df


def get_neighbors(G, node_id, relation_type=None):
    """Get successors of a node, optionally filtered by relation type."""
    if node_id not in G:
        return []
    neighbors = []
    for neighbor in G.successors(node_id):
        edge_data = G.edges[node_id, neighbor]
        if relation_type is None or edge_data.get("relation") == relation_type:
            neighbors.append(neighbor)
    return neighbors


def get_incidents_for_entity(G, entity_id, relation_type=None):
    """Get incident nodes connected to an entity via predecessors."""
    if entity_id not in G:
        return []
    incidents = []
    for neighbor in G.predecessors(entity_id):
        if not neighbor.startswith("INCIDENT::"):
            continue
        edge_data = G.edges[neighbor, entity_id]
        if relation_type is None or edge_data.get("relation") == relation_type:
            incidents.append(neighbor)
    return incidents


def get_entities_for_incident(G, incident_id, entity_type=None, relation_type=None):
    """Get entity nodes connected to an incident via successors."""
    if incident_id not in G:
        return []
    results = []
    for neighbor in G.successors(incident_id):
        edge_data = G.edges[incident_id, neighbor]
        if relation_type and edge_data.get("relation") != relation_type:
            continue
        node_data = G.nodes[neighbor]
        if entity_type and node_data.get("entity_type") != entity_type:
            continue
        results.append(neighbor)
    return results


def find_entities_by_value(entities_df, entity_type, value_pattern,
                           case_insensitive=True):
    """Find entity IDs matching type + value regex."""
    mask = entities_df["entity_type"] == entity_type
    if case_insensitive:
        mask &= entities_df["value"].str.lower().str.contains(
            value_pattern.lower(), na=False, regex=True)
    else:
        mask &= entities_df["value"].str.contains(
            value_pattern, na=False, regex=True)
    return entities_df[mask]["entity_id"].tolist()


def get_incident_property(G, incident_id, prop):
    """Get a property from an incident node."""
    if incident_id not in G:
        return None
    return G.nodes[incident_id].get(prop)


def safe_get_node_value(G, node_id, default=None):
    """Safely get node value, returning default if node doesn't exist."""
    if node_id not in G:
        return default
    return G.nodes[node_id].get("value", default)


def incidents_matching_narrative(metadata_df, keywords, match_all=True):
    """Find record_no strings whose narrative contains keywords."""
    # Start with True for AND (all must match), False for OR (any may match)
    mask = pd.Series(match_all, index=metadata_df.index)
    for kw in keywords:
        kw_mask = metadata_df["narrative"].str.lower().str.contains(
            kw.lower(), na=False)
        mask = mask & kw_mask if match_all else mask | kw_mask
    return set(metadata_df[mask]["record_no"].astype(str).tolist())


def parse_year(date_val):
    """Extract year from a date value."""
    if not date_val or str(date_val).lower() in ("nan", "none", "nat", ""):
        return None
    try:
        return dateparser.parse(str(date_val)).year
    except Exception:
        return None


def parse_yearmonth(date_val):
    """Extract YYYY-MM from a date value."""
    if not date_val or str(date_val).lower() in ("nan", "none", "nat", ""):
        return None
    try:
        dt = dateparser.parse(str(date_val))
        return f"{dt.year}-{dt.month:02d}"
    except Exception:
        return None


def incidents_for_entity_filter(G, entities_df, entity_type, value_pattern,
                                relation_type):
    """Find all incidents matching an entity filter triple.

    Returns (incident_set, entity_id_list).
    """
    entity_ids = find_entities_by_value(entities_df, entity_type, value_pattern)
    incidents = set()
    for eid in entity_ids:
        incidents.update(get_incidents_for_entity(G, eid, relation_type))
    return incidents, entity_ids


def incidents_for_meta_filter(metadata_df, field, op, value):
    """Filter metadata by field op value and return INCIDENT:: IDs."""
    if field == "year":
        col = metadata_df["reported_date"].apply(parse_year)
        val = int(value)
    elif op == "contains":
        col = metadata_df[field].astype(str).str.lower()
        # Use regex directly (pipe-separated values work as OR)
        mask = col.str.contains(value.lower(), na=False, regex=True)
        return {f"INCIDENT::{row['record_no']}"
                for _, row in metadata_df[mask].iterrows()}
    else:
        col = metadata_df[field]
        try:
            val = float(value)
            col = pd.to_numeric(col, errors="coerce")
        except ValueError:
            val = value

    ops = {
        "==": lambda c, v: c == v,
        "!=": lambda c, v: c != v,
        ">=": lambda c, v: c >= v,
        "<=": lambda c, v: c <= v,
        ">":  lambda c, v: c > v,
        "<":  lambda c, v: c < v,
    }
    mask = ops.get(op, lambda c, v: pd.Series(False, index=c.index))(col, val)
    return {f"INCIDENT::{row['record_no']}"
            for _, row in metadata_df[mask].iterrows()}
