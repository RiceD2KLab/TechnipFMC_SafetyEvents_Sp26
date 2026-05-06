import os
from src.entity_extraction.pipeline import PetroSuperPipeline

PIPELINE = PetroSuperPipeline(
    uri=os.getenv("NEO4J_URI"),
    user=os.getenv("NEO4J_USER"),
    pw=os.getenv("NEO4J_PASSWORD"),
    catalogue_path="data/catalogue.xlsx"
)

PIPELINE.ingest_folder("data/raw_reports")
PIPELINE.save()