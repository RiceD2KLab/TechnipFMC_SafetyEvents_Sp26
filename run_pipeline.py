import os
import pandas as pd
from dotenv import load_dotenv

from pipeline.pipeline import PetroSuperPipeline
from pipeline.label_generator import LabelGenerator

load_dotenv()

labels = LabelGenerator("data/schema/catalogue.xlsx").generate_labels()

pipeline = PetroSuperPipeline(
    labels=labels,
    uri=os.getenv("NEO4J_URI"),
    user=os.getenv("NEO4J_USER"),
    pw=os.getenv("NEO4J_PASSWORD")
)

df = pd.read_csv("data/sample/sample_incidents.csv")

for i, row in df.iterrows():
    text = " ".join([str(v) for v in row.values if pd.notna(v)])
    pipeline.process_row(str(i), text)
