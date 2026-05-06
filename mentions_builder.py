def build_mentions(df):
    mentions = df.copy()

    mentions["source"] = mentions["doc_id"]
    mentions["target"] = mentions["entity_id"]

    mentions = mentions[["source", "target"]].drop_duplicates()

    mentions["edge_type"] = "MENTIONS"
    mentions["weight"] = 1

    return mentions