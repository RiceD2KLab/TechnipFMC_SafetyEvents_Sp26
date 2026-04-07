"""
Knowledge Graph data loader and subgraph extraction for the FastAPI backend.
Loads entities/relations parquets and builds a cached NetworkX DiGraph.

Ported from visual_dashboard/dashboard/handler/kg_loader.py.
"""

import pandas as pd
import networkx as nx
from pathlib import Path

# Path to KG parquet files (pipeline/outputs/)
_KG_DATA_DIR = Path(__file__).resolve().parent.parent.parent / "pipeline" / "outputs"

# Module-level cache
_kg_cache = {
    "G": None,
    "entities_df": None,
    "relations_df": None,
    "metadata_df": None,
    "incident_display_map": None,
}

# Color scheme for entity types (colorblind-friendly)
# Only L1 types are shown — L2 causal entities (Event, Condition, Action, etc.)
# are not directly connected to INCIDENT nodes and thus unreachable in subgraph queries.
ENTITY_COLORS = {
    "INCIDENT": "#E74C3C",
    "EQUIPMENT": "#3498DB",
    "BODY_PART": "#E67E22",
    "INJURY_TYPE": "#9B59B6",
    "LOCATION": "#27AE60",
    "ORGANIZATION": "#1ABC9C",
    "ROOT_CAUSE_CATEGORY": "#F1C40F",
}

ENTITY_TYPE_LABELS = {
    "INCIDENT": "Incident",
    "EQUIPMENT": "Equipment",
    "BODY_PART": "Body Part",
    "INJURY_TYPE": "Injury Type",
    "LOCATION": "Location",
    "ORGANIZATION": "Organization",
    "ROOT_CAUSE_CATEGORY": "Root Cause",
}

# Max nodes to return in a subgraph (prevents mega-hub browser freeze)
MAX_SUBGRAPH_NODES = 500

# Max hop-2 incidents to sample per shared entity
MAX_HOP2_PER_ENTITY = 5


def load_kg_data():
    """
    Load entities and relations parquets and build NetworkX DiGraph.
    Uses module-level caching so the graph is built only once per session.

    Returns:
        tuple: (G: nx.DiGraph, entities_df: pd.DataFrame, relations_df: pd.DataFrame)
    """
    if _kg_cache["G"] is not None:
        return _kg_cache["G"], _kg_cache["entities_df"], _kg_cache["relations_df"], _kg_cache["metadata_df"]

    entities_path = _KG_DATA_DIR / "entities.parquet"
    relations_path = _KG_DATA_DIR / "relations.parquet"

    if not entities_path.exists() or not relations_path.exists():
        raise FileNotFoundError(
            f"KG parquet files not found in {_KG_DATA_DIR}. "
            "Expected entities.parquet and relations.parquet."
        )

    entities_df = pd.read_parquet(entities_path)
    relations_df = pd.read_parquet(relations_path)

    G = nx.DiGraph()

    # --- Bulk-add nodes (vectorized, ~20x faster than iterrows) ---
    attr_cols = [c for c in entities_df.columns if c != "entity_id"]
    node_ids = entities_df["entity_id"].tolist()
    attr_records = entities_df[attr_cols].to_dict("records")
    nodes_with_attrs = [
        (nid, {k: v for k, v in attrs.items() if pd.notna(v)})
        for nid, attrs in zip(node_ids, attr_records)
    ]
    G.add_nodes_from(nodes_with_attrs)

    # --- Bulk-add edges (vectorized) ---
    node_set = set(node_ids)
    valid_mask = relations_df["source"].isin(node_set) & relations_df["target"].isin(node_set)
    valid_rels = relations_df[valid_mask]

    edge_records = valid_rels.to_dict("records")
    edges_with_attrs = [
        (
            rec["source"],
            rec["target"],
            {
                "relation": rec["relation"],
                **({"confidence": rec["confidence"]} if pd.notna(rec.get("confidence")) else {}),
                **({"source_type": rec["source_type"]} if pd.notna(rec.get("source_type")) else {}),
            },
        )
        for rec in edge_records
    ]
    G.add_edges_from(edges_with_attrs)

    # Load metadata (required for NLQ query execution)
    metadata_path = _KG_DATA_DIR / "metadata_parsed.parquet"
    if metadata_path.exists():
        metadata_df = pd.read_parquet(metadata_path)
    else:
        metadata_df = pd.DataFrame()

    _kg_cache["G"] = G
    _kg_cache["entities_df"] = entities_df
    _kg_cache["relations_df"] = relations_df
    _kg_cache["metadata_df"] = metadata_df

    return G, entities_df, relations_df, metadata_df


def get_incident_display_map(entities_df):
    """
    Return dict mapping display_label -> entity_id for incidents.
    Used for the incident selector dropdown. Cached after first call.
    """
    if _kg_cache["incident_display_map"] is not None:
        return _kg_cache["incident_display_map"]

    mask = entities_df["entity_type"] == "INCIDENT"
    incidents = entities_df.loc[mask, ["entity_id", "value"]].copy()
    incidents["value"] = incidents["value"].fillna("").astype(str)
    incidents["label"] = incidents["entity_id"] + " | " + incidents["value"].str[:80]

    display_map = dict(zip(incidents["label"], incidents["entity_id"]))
    _kg_cache["incident_display_map"] = display_map
    return display_map


def find_entities_by_value(entities_df, entity_type=None, value_pattern="",
                           case_insensitive=True, max_results=100):
    """
    Search entities by type and value regex.

    Returns:
        list of [entity_id, entity_type, value] lists
    """
    mask = pd.Series(True, index=entities_df.index)
    if entity_type and entity_type != "ALL":
        mask &= entities_df["entity_type"] == entity_type
    if value_pattern:
        if case_insensitive:
            mask &= entities_df["value"].str.lower().str.contains(
                value_pattern.lower(), na=False, regex=True
            )
        else:
            mask &= entities_df["value"].str.contains(
                value_pattern, na=False, regex=True
            )
    results = entities_df[mask][["entity_id", "entity_type", "value"]].head(max_results)
    return results.values.tolist()


def extract_subgraph(G, center_node_id, hops=1, entity_type_filter=None):
    """
    Extract a subgraph centered on center_node_id up to `hops` hops away.

    For hops=1: returns all direct neighbors (star graph, typically ~10 nodes).
    For hops=2: uses a smart expansion strategy — for each hop-1 entity,
    samples up to MAX_HOP2_PER_ENTITY other incidents that share that entity,
    avoiding mega-hub explosion.

    Args:
        G: Full NetworkX DiGraph
        center_node_id: The node to center on
        hops: 1 or 2
        entity_type_filter: Optional set of entity types to include (None = all)

    Returns:
        tuple: (nx.DiGraph subgraph, bool was_truncated)
    """
    if center_node_id not in G:
        return nx.DiGraph(), False

    undirected = G.to_undirected(as_view=True)

    if hops == 1:
        neighborhood_nodes = set(nx.ego_graph(undirected, center_node_id, radius=1).nodes())
    else:
        hop1_nodes = set(nx.ego_graph(undirected, center_node_id, radius=1).nodes())
        hop1_entities = hop1_nodes - {center_node_id}

        neighborhood_nodes = set(hop1_nodes)

        for entity_id in hop1_entities:
            other_incidents = []
            for neighbor in undirected.neighbors(entity_id):
                if neighbor == center_node_id:
                    continue
                if neighbor in neighborhood_nodes:
                    continue
                if G.nodes[neighbor].get("entity_type") == "INCIDENT":
                    other_incidents.append(neighbor)

            sampled = other_incidents[:MAX_HOP2_PER_ENTITY]
            neighborhood_nodes.update(sampled)

            for inc in sampled:
                for inc_neighbor in undirected.neighbors(inc):
                    if G.nodes[inc_neighbor].get("entity_type") != "INCIDENT":
                        neighborhood_nodes.add(inc_neighbor)

    # Filter by entity type if requested (always keep center node + incidents)
    if entity_type_filter:
        neighborhood_nodes = {
            n for n in neighborhood_nodes
            if G.nodes[n].get("entity_type") in entity_type_filter
            or n == center_node_id
        }

    # Safety cap
    was_truncated = False
    if len(neighborhood_nodes) > MAX_SUBGRAPH_NODES:
        was_truncated = True
        neighbor_degrees = [
            (n, undirected.degree(n)) for n in neighborhood_nodes if n != center_node_id
        ]
        neighbor_degrees.sort(key=lambda x: x[1], reverse=True)
        keep = {center_node_id}
        keep.update(n for n, _ in neighbor_degrees[: MAX_SUBGRAPH_NODES - 1])
        neighborhood_nodes = keep

    subgraph = G.subgraph(neighborhood_nodes).copy()
    return subgraph, was_truncated
