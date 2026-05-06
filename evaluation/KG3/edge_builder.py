import pandas as pd

def build_edges(mentions, causal):
    mentions = mentions[["source", "target", "edge_type", "weight"]]

    causal = causal.rename(columns={
        "source_id": "source",
        "target_id": "target"
    })[["source", "target", "edge_type", "weight"]]

    return pd.concat([mentions, causal]).drop_duplicates()