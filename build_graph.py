import networkx as nx
import pandas as pd
from typing import Optional


def build_graph(
    entity_file: str,
    mention_file: str,
    causal_file: Optional[str] = None
) -> nx.MultiDiGraph:
    """
    Build a multi-layer knowledge graph from parquet files.

    Parameters
    ----------
    entity_file : str
        Path to entities.parquet
        Expected columns: [entity_id, entity_type]

    mention_file : str
        Path to relations.parquet
        Expected columns: [source, target]

    causal_file : str, optional
        Path to causal_edges.parquet
        Expected columns: [source, target, doc_id]

    Returns
    -------
    nx.MultiDiGraph
        Constructed knowledge graph with:
        - ENTITY nodes
        - INCIDENT nodes
        - MENTIONS edges
        - CAUSES edges
    """

    G = nx.MultiDiGraph()

    # -------------------------
    # LOAD ENTITY NODES
    # -------------------------
    entities = pd.read_parquet(entity_file)

    required_cols = {"entity_id"}
    if not required_cols.issubset(entities.columns):
        raise ValueError(f"Missing required columns in {entity_file}")

    print(f"Loading {len(entities)} entity nodes...")

    G.add_nodes_from(
        (
            row["entity_id"],
            {
                "label": "ENTITY",
                "type": row.get("entity_type")
            }
        )
        for _, row in entities.iterrows()
    )

    # -------------------------
    # LOAD MENTION EDGES
    # -------------------------
    mentions = pd.read_parquet(mention_file)

    if not {"source", "target"}.issubset(mentions.columns):
        raise ValueError(f"Missing required columns in {mention_file}")

    print(f"Loading {len(mentions)} mention edges...")

    # Add incident nodes + edges
    for _, row in mentions.iterrows():
        incident_id = row["source"]

        if not G.has_node(incident_id):
            G.add_node(incident_id, label="INCIDENT")

        G.add_edge(
            row["source"],
            row["target"],
            type="MENTIONS"
        )

    # -------------------------
    # LOAD CAUSAL EDGES
    # -------------------------
    if causal_file:
        causal = pd.read_parquet(causal_file)

        if not {"source", "target"}.issubset(causal.columns):
            raise ValueError(f"Missing required columns in {causal_file}")

        print(f"Loading {len(causal)} causal edges...")

        G.add_edges_from(
            (
                row["source"],
                row["target"],
                {
                    "type": "CAUSES",
                    "doc_id": row.get("doc_id")
                }
            )
            for _, row in causal.iterrows()
        )

    # -------------------------
    # FINAL STATS
    # -------------------------
    print(f"Graph built successfully:")
    print(f"Nodes: {G.number_of_nodes()}")
    print(f"Edges: {G.number_of_edges()}")

    return G