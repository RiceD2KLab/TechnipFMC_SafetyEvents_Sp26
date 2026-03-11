"""
Converts a NetworkX subgraph into a JSON-serializable response
with layout positions computed via spring_layout.
"""

import networkx as nx
import pandas as pd

from schemas import (
    GraphNode,
    GraphEdge,
    SubgraphStats,
    SubgraphResponse,
)
from kg_loader import ENTITY_COLORS, ENTITY_TYPE_LABELS

# Properties to include on INCIDENT nodes when available
_INCIDENT_PROPS = [
    "incident_type", "severity", "severity_bin", "likelihood",
    "impact_type", "work_process", "risk_color", "business_unit",
    "reported_date", "event_datetime",
]


def serialize_subgraph(subgraph: nx.DiGraph, center_node_id: str) -> SubgraphResponse:
    """
    Compute spring layout and serialize a NetworkX subgraph to a SubgraphResponse.

    Args:
        subgraph: The extracted subgraph (DiGraph).
        center_node_id: The entity_id of the center node.

    Returns:
        SubgraphResponse with nodes (including x,y), edges, and stats.
    """
    n = max(1, subgraph.number_of_nodes())

    # Compute layout — same parameters as the Streamlit version (graph_makers.py)
    if n > 0:
        pos = nx.spring_layout(
            subgraph.to_undirected(),
            seed=42,
            k=2.0 / (n ** 0.3),
        )
    else:
        pos = {}

    # Normalize positions to [0, 1] range with padding
    normalized = _normalize_positions(pos)

    # Build node list
    nodes = []
    for node_id, attrs in subgraph.nodes(data=True):
        x, y = normalized.get(node_id, (0.5, 0.5))
        entity_type = attrs.get("entity_type", "UNKNOWN")

        properties = {}
        for prop in _INCIDENT_PROPS:
            val = attrs.get(prop)
            if val is not None and not (isinstance(val, float) and pd.isna(val)):
                properties[prop] = val

        nodes.append(GraphNode(
            id=node_id,
            entity_type=entity_type,
            value=str(attrs.get("value", node_id)),
            x=x,
            y=y,
            is_center=(node_id == center_node_id),
            properties=properties,
        ))

    # Build edge list
    edges = []
    for src, tgt, attrs in subgraph.edges(data=True):
        edges.append(GraphEdge(
            source=src,
            target=tgt,
            relation=attrs.get("relation", "UNKNOWN"),
            confidence=attrs.get("confidence"),
            source_type=attrs.get("source_type"),
        ))

    # Compute stats
    entity_type_counts: dict[str, int] = {}
    for _, attrs in subgraph.nodes(data=True):
        et = attrs.get("entity_type", "UNKNOWN")
        entity_type_counts[et] = entity_type_counts.get(et, 0) + 1

    relation_type_counts: dict[str, int] = {}
    for _, _, attrs in subgraph.edges(data=True):
        rel = attrs.get("relation", "UNKNOWN")
        relation_type_counts[rel] = relation_type_counts.get(rel, 0) + 1

    stats = SubgraphStats(
        node_count=subgraph.number_of_nodes(),
        edge_count=subgraph.number_of_edges(),
        entity_type_counts=entity_type_counts,
        relation_type_counts=relation_type_counts,
    )

    return SubgraphResponse(
        nodes=nodes,
        edges=edges,
        stats=stats,
        truncated=False,  # Caller sets this after the fact
        center_node_id=center_node_id,
    )


def _normalize_positions(pos: dict) -> dict:
    """Normalize layout positions to [0, 1] with padding."""
    if not pos:
        return {}

    xs = [p[0] for p in pos.values()]
    ys = [p[1] for p in pos.values()]
    x_min, x_max = min(xs), max(xs)
    y_min, y_max = min(ys), max(ys)
    x_range = x_max - x_min if x_max != x_min else 1.0
    y_range = y_max - y_min if y_max != y_min else 1.0

    padding = 0.05
    normalized = {}
    for node_id, (x, y) in pos.items():
        normalized[node_id] = (
            padding + (1 - 2 * padding) * (x - x_min) / x_range,
            padding + (1 - 2 * padding) * (y - y_min) / y_range,
        )
    return normalized
