def build_causal(df):
    df = df.copy()

    df["source"] = df["source"].str.upper().str.strip()
    df["target"] = df["target"].str.upper().str.strip()

    df = df.dropna(subset=["source", "target"])

    df["source_id"] = "ACTIVITY::" + df["source"]
    df["target_id"] = "ACTIVITY::" + df["target"]

    df["edge_type"] = "CAUSES"
    df["weight"] = 1

    return df[["source_id", "target_id", "edge_type", "weight"]].drop_duplicates()