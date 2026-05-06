def clean_entities(df):
    df = df.copy()

    df["text"] = df["text"].str.upper().str.strip()
    df = df.dropna(subset=["text", "type"])

    df["entity_id"] = df["type"] + "::" + df["text"]

    return df.drop_duplicates(subset=["entity_id"])