import sys
!{sys.executable} -m pip install "PyMuPDF<2.0.0,>=1.20.0"
import fitz 

# Install GLiNER to ensure it's available in this execution context
!{sys.executable} -m pip install "gliner==0.2.26"

# Install neo4j for database connectivity
!{sys.executable} -m pip install "neo4j"

import os
import pandas as pd
import torch
import logging
from tqdm.auto import tqdm
from gliner import GLiNER
from transformers import pipeline, AutoTokenizer, AutoModel
from dateutil import parser
from sklearn.metrics.pairwise import cosine_similarity
from neo4j import GraphDatabase

# --- LOGGING SETUP ---
logging.basicConfig(filename='ingestion_errors.log', level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class QHSEDictionaryMapper:
    """Helper class to turn the Excel Dictionary into AI instructions."""
    def __init__(self, excel_path):
        self.excel_path = excel_path
        self.df = pd.read_excel(excel_path)
        self.label_map = self._generate_label_map()

    def _generate_label_map(self):
        # Extract 'Asset Type' or high-level 'Table' names to create categories
        # DIM_SYNERGI_CONSEQUENCES -> Consequence
        # FACT_CONSOLIDATED_INCIDENT -> Incident_Detail
        mapping = {}
        if 'Name' in self.df.columns:
            for _, row in self.df.iterrows():
                key = str(row['Name']).upper()
                # Logic: If it contains 'EQUIPMENT' or 'ASSET', label it 'Equipment'
                if 'EQUIPMENT' in key or 'ASSET' in key:
                    mapping[key] = "Equipment"
                elif 'INJURY' in key or 'CONSEQUENCE' in key:
                    mapping[key] = "Consequence"
                elif 'ORG' in key:
                    mapping[key] = "Organization"
                elif 'HAZARD' in key or 'ROOT_CAUSE' in key:
                    mapping[key] = "Hazard"
                else:
                    mapping[key] = "Activity"
        return mapping

    def get_gliner_labels(self):
        # Returns a unique list of high-level categories for the AI to find
        return list(set(self.label_map.values())) + ["Location", "Person", "Date"]

class IntegratedPetroExtractor:
    def __init__(self, uri, user, password, dictionary_path):
        print("📖 Loading QHSE Dictionary mapping...")
        self.mapper = QHSEDictionaryMapper(dictionary_path)
        self.labels = self.mapper.get_gliner_labels()

        print(f"🤖 Loading GLiNER with Dictionary Labels: {self.labels}")
        self.gliner = GLiNER.from_pretrained("urchade/gliner_multi-v2.1").to("cuda")

        print("🔧 Loading Domain Expert (BART)...")
        self.validator = pipeline("zero-shot-classification", model="facebook/bart-large-mnli", device=0)
        self.embed_tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-mnli")
        self.embed_model = AutoModel.from_pretrained("facebook/bart-large-mnli").to("cuda")

        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.petro_categories = ["industrial equipment", "human role", "safety tool", "incident consequence"]

    def _get_vector(self, text):
        inputs = self.embed_tokenizer(text, return_tensors="pt", padding=True, truncation=True).to("cuda")
        with torch.no_grad():
            outputs = self.embed_model(**inputs)
        return outputs.last_hidden_state.mean(dim=1).cpu().numpy()

    def _resolve_entities(self, entity_list, threshold=0.88):
        if not entity_list: return {}
        items = list(entity_list)
        vectors = [self._get_vector(i) for i in items]
        resolved, used = {}, set()
        for i in range(len(items)):
            if i in used: continue
            group = [items[i]]
            used.add(i)
            for j in range(i + 1, len(items)):
                if j not in used:
                    sim = cosine_similarity(vectors[i], vectors[j])[0][0]
                    if sim >= threshold:
                        group.append(items[j])
                        used.add(j)
            resolved[max(group, key=len)] = group
        return resolved

    def process_text(self, incident_id, text, severity="Medium"):
        raw_entities = self.gliner.predict_entities(text, self.labels, threshold=0.3)
        data = {l: set() for l in self.labels}

        for ent in raw_entities:
            val = ent['text'].strip(",. ").upper()
            label = ent['label']
            if label == "Date":
                try: val = parser.parse(val, fuzzy=True).strftime('%Y-%m-%d')
                except: pass
            data[label].add(val)

        with self.driver.session() as session:
            inc_date = list(data.get('Date', ['2026-01-01']))[0]
            session.execute_write(self._ingest_incident, incident_id, inc_date, severity)
            for label, items in data.items():
                if label == "Date": continue
                resolved = self._resolve_entities(items)
                for canonical, aliases in resolved.items():
                    session.execute_write(self._ingest_entity, incident_id, label, canonical, list(aliases))

    @staticmethod
    def _ingest_incident(tx, inc_id, date, severity):
        tx.run("MERGE (i:Incident {id: $id}) SET i.date = $date, i.severity = $sev",
               id=inc_id, date=date, sev=severity)

    @staticmethod
    def _ingest_entity(tx, inc_id, label, name, aliases):
        rel = f"INVOLVED_{label.upper()}"
        tx.run(f"MERGE (n:{label} {{name: $name}}) SET n.aliases = $aliases "
               f"WITH n MATCH (i:Incident {{id: $inc_id}}) MERGE (i)-[:{rel}]->(n)",
               name=name, aliases=aliases, inc_id=inc_id)

def run_pipeline(source_path, dictionary_path, uri, user, pw, batch_size=10):
    extractor = IntegratedPetroExtractor(uri, user, pw, dictionary_path)

    # CASE: Excel/CSV Source
    if source_path.endswith(('.xlsx', '.csv')):
        df = pd.read_excel(source_path) if source_path.endswith('.xlsx') else pd.read_csv(source_path)
        for i in tqdm(range(0, len(df), batch_size), desc="Batches"):
            chunk = df.iloc[i:i+batch_size]
            for idx, row in chunk.iterrows():
                try:
                    content = " ".join([str(v) for v in row.values])
                    extractor.process_text(str(row.get('IncidentID', f"ROW_{idx}")), content)
                except Exception as e:
                    logger.error(f"Row {idx} failed: {e}")

    # CASE: PDF Directory
    elif os.path.isdir(source_path):
        for f in tqdm(os.listdir(source_path)):
            if f.endswith('.pdf'):
                try:
                    doc = fitz.open(os.path.join(source_path, f))
                    text = " ".join([p.get_text() for p in doc])
                    extractor.process_text(f.split('.')[0], text)
                except Exception as e:
                    logger.error(f"File {f} failed: {e}")

if __name__ == "__main__":
    # CONFIGURATION
    DICT_FILE = "/content/sample_data/QHSE Enterprise Schema - Columns Tables and Views.xlsx"  # Snowflake dictionary
    DATA_SRC = "/content/sample_data/DIM_CONSOLIDATED_ACCIDENTS.xlsx"                  # Incident Reports
    NEO4J_URI = "neo4j+s://9dccbd3e.databases.neo4j.io"
    NEO4J_USER = "9dccbd3e"
    NEO4J_PW = "pXNYt3e7QpCTEr-0kRbBmknJAh9usrbHEz13cmuNNbE"

    run_pipeline(DATA_SRC, DICT_FILE, NEO4J_URI, NEO4J_USER, NEO4J_PW, batch_size=10)