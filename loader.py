import pandas as pd

def load_data():
    entities = pd.read_parquet("data/entities.parquet")
    relations = pd.read_parquet("data/relations.parquet")
    metadata = pd.read_parquet("data/metadata_fixed.parquet")
    causal = pd.read_parquet("data/MASTER_causal_extractions.parquet")

    return entities, relations, metadata, causal