def save_outputs(nodes, edges):
    nodes.to_csv("data/neo4j_nodes.csv", index=False)
    edges.to_csv("data/neo4j_edges.csv", index=False)

    edges[edges["edge_type"] == "MENTIONS"].to_csv(
        "data/edges_mentions.csv", index=False
    )

    edges[edges["edge_type"] == "CAUSES"].to_csv(
        "data/edges_causal.csv", index=False
    )

    print("Saved outputs")