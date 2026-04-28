import pandas as pd

# ===============================
# 1. LOAD RAW FILES
# ===============================

def load_data():
    entities = pd.read_parquet("data/entities.parquet")
    relations = pd.read_parquet("data/relations.parquet")
    metadata = pd.read_parquet("data/metadata_fixed.parquet")
    causal = pd.read_parquet("data/MASTER_causal_extractions.parquet")

    return entities, relations, metadata, causal


# ===============================
# 2. CLEAN ENTITIES (CRITICAL)
# ===============================

def clean_entities(entities):
    entities = entities.copy()

    # Normalize text
    entities["text"] = entities["text"].str.upper().str.strip()

    # Drop nulls
    entities = entities.dropna(subset=["text", "type"])

    # Remove duplicates
    entities = entities.drop_duplicates(subset=["text", "type"])

    # Create canonical ID
    entities["entity_id"] = entities["type"] + "::" + entities["text"]

    return entities


# ===============================
# 3. BUILD MENTIONS EDGES
# ===============================

def build_mentions_edges(entities):
    """
    DOCUMENT → ENTITY edges
    """
    mentions = entities.copy()

    mentions["source"] = mentions["doc_id"]
    mentions["target"] = mentions["entity_id"]

    mentions = mentions[["source", "target"]].drop_duplicates()

    mentions["edge_type"] = "MENTIONS"
    mentions["weight"] = 1

    return mentions


# ===============================
# 4. CLEAN RELATIONS (OPTIONAL)
# ===============================

def clean_relations(relations):
    relations = relations.copy()

    relations["source"] = relations["source"].str.upper().str.strip()
    relations["target"] = relations["target"].str.upper().str.strip()

    relations = relations.dropna()

    return relations


# ===============================
# 5. CLEAN & NORMALIZE CAUSAL EDGES
# ===============================

def clean_causal(causal):
    causal = causal.copy()

    # Normalize text
    causal["source"] = causal["source"].str.upper().str.strip()
    causal["target"] = causal["target"].str.upper().str.strip()

    # Drop nulls
    causal = causal.dropna(subset=["source", "target"])

    # Create pseudo entity IDs (ACTIVITY-based)
    causal["source_id"] = "ACTIVITY::" + causal["source"]
    causal["target_id"] = "ACTIVITY::" + causal["target"]

    causal["edge_type"] = "CAUSES"
    causal["weight"] = 1

    causal = causal[["source_id", "target_id", "edge_type", "weight"]]

    causal = causal.drop_duplicates()

    return causal


# ===============================
# 6. BUILD NODE TABLE
# ===============================

def build_nodes(mentions, causal):
    # Document nodes
    doc_nodes = pd.DataFrame({
        "id": mentions["source"].unique(),
        "node_type": "DOCUMENT"
    })

    # Entity nodes (from mentions + causal)
    entity_ids = set(mentions["target"]).union(
        set(causal["source_id"])
    ).union(
        set(causal["target_id"])
    )

    entity_nodes = pd.DataFrame({
        "id": list(entity_ids),
        "node_type": "ENTITY"
    })

    nodes = pd.concat([doc_nodes, entity_nodes]).drop_duplicates()

    return nodes


# ===============================
# 7. BUILD FINAL EDGE TABLE
# ===============================

def build_edges(mentions, causal):
    mentions_edges = mentions.rename(columns={
        "source": "source",
        "target": "target"
    })[["source", "target", "edge_type", "weight"]]

    causal_edges = causal.rename(columns={
        "source_id": "source",
        "target_id": "target"
    })[["source", "target", "edge_type", "weight"]]

    edges = pd.concat([mentions_edges, causal_edges]).drop_duplicates()

    return edges


# ===============================
# 8. SAVE FINAL FILES
# ===============================

def save_outputs(nodes, edges):
    nodes.to_csv("data/neo4j_nodes.csv", index=False)
    edges.to_csv("data/neo4j_edges.csv", index=False)

    # Optional splits
    edges[edges["edge_type"] == "MENTIONS"].to_csv(
        "data/edges_mentions.csv", index=False
    )

    edges[edges["edge_type"] == "CAUSES"].to_csv(
        "data/edges_causal.csv", index=False
    )

    print("Saved all outputs")


# ===============================
# 9. MAIN PIPELINE
# ===============================

def run_pipeline():
    entities, relations, metadata, causal = load_data()

    entities = clean_entities(entities)
    mentions = build_mentions_edges(entities)

    relations = clean_relations(relations)  # optional

    causal = clean_causal(causal)

    nodes = build_nodes(mentions, causal)
    edges = build_edges(mentions, causal)

    save_outputs(nodes, edges)

    print("Pipeline complete")
    print(f"Nodes: {nodes.shape}")
    print(f"Edges: {edges.shape}")


if __name__ == "__main__":
    run_pipeline()