import pandas as pd

def build_nodes(mentions, causal):
    doc_nodes = pd.DataFrame({
        "id": mentions["source"].unique(),
        "node_type": "DOCUMENT"
    })

    entity_ids = set(mentions["target"]) \
        | set(causal["source_id"]) \
        | set(causal["target_id"])

    entity_nodes = pd.DataFrame({
        "id": list(entity_ids),
        "node_type": "ENTITY"
    })

    return pd.concat([doc_nodes, entity_nodes]).drop_duplicates()