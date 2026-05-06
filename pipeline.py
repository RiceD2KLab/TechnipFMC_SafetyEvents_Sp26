import os
import re
import glob
import logging
import pandas as pd
import torch
from tqdm.auto import tqdm
from gliner import GLiNER
from neo4j import GraphDatabase
from transformers import AutoTokenizer, AutoModel
from sklearn.metrics.pairwise import cosine_similarity
from dateutil import parser
from pathlib import Path

from .config import (
    CHUNK_MAX_TOKENS,
    CHUNK_OVERLAP,
    CONFIDENCE_THRESHOLD,
    SIMILARITY_THRESHOLD
)

logging.basicConfig(
    filename='pipeline.log',
    level=logging.ERROR
)
logger = logging.getLogger(__name__)


class PetroSuperPipeline:

    def __init__(self, uri, user, pw, catalogue_path):

        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        print(f"Loading GLiNER on {self.device}")
        self.model = GLiNER.from_pretrained("urchade/gliner_medium-v2.1").to(self.device)
        self.tokenizer = self.model.data_processor.transformer_tokenizer

        print("Loading embedding model")
        self.embed_tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-mnli")
        self.embed_model = AutoModel.from_pretrained("facebook/bart-large-mnli").to(self.device)

        self.labels = self._generate_hybrid_labels(catalogue_path)
        self.driver = GraphDatabase.driver(uri, auth=(user, pw))

        self.l1_nodes = []
        self.l1_edges = []
        self.l1_metadata = []

    def _generate_hybrid_labels(self, path):
        df = pd.read_excel(path)
        labels = {"EQUIPMENT", "HAZARD", "LOCATION", "INCIDENT"}

        for _, row in df.iterrows():
            col = str(row.get('Full Name', '')).strip().upper()
            if len(col) > 2:
                labels.add(col)

        return list(labels)

    def _chunk_text(self, text):
        words = text.split()
        word_tokens = [len(self.tokenizer.encode(w, add_special_tokens=False)) for w in words]

        chunks, pos = [], 0

        while pos < len(words):
            budget, end = CHUNK_MAX_TOKENS, pos

            while end < len(words) and budget >= word_tokens[end]:
                budget -= word_tokens[end]
                end += 1

            chunks.append((" ".join(words[pos:end]), pos))

            if end >= len(words):
                break

            pos = end - CHUNK_OVERLAP

        return chunks

    def process_document(self, doc_id, text):

        try:
            chunks = self._chunk_text(text)

            for chunk_text, _ in chunks:

                ents = self.model.predict_entities(
                    chunk_text,
                    self.labels,
                    threshold=CONFIDENCE_THRESHOLD
                )

                for ent in ents:

                    label = ent['label'].split(' (')[0]
                    val = ent['text'].strip().upper()

                    if label == "DATE":
                        try:
                            val = parser.parse(val).strftime('%Y-%m-%d')
                        except:
                            pass

                    eid = f"{label}::{val}"

                    self.l1_nodes.append({
                        "entity_id": eid,
                        "entity_type": label
                    })

                    self.l1_edges.append({
                        "source": f"INCIDENT::{doc_id}",
                        "target": eid,
                        "relation": "MENTIONS"
                    })

            self.l1_metadata.append({
                "record_no": doc_id,
                "narrative": text
            })

        except Exception as e:
            logger.error(f"{doc_id}: {str(e)}")

    def ingest_folder(self, folder_path):

        files = []
        for ext in ['*.xlsx', '*.csv']:
            files.extend(glob.glob(os.path.join(folder_path, ext)))

        for file_path in tqdm(files):

            df = pd.read_csv(file_path) if file_path.endswith('.csv') else pd.read_excel(file_path)

            for i, row in df.iterrows():
                rid = str(row.get("IncidentID", f"{file_path}_{i}"))
                content = " ".join(str(v) for v in row.values if pd.notna(v))
                self.process_document(rid, content)

    def save(self, output_dir="outputs"):

        Path(output_dir).mkdir(exist_ok=True)

        pd.DataFrame(self.l1_nodes).drop_duplicates().to_parquet(f"{output_dir}/entities.parquet")
        pd.DataFrame(self.l1_edges).drop_duplicates().to_parquet(f"{output_dir}/relations.parquet")
        pd.DataFrame(self.l1_metadata).to_parquet(f"{output_dir}/metadata.parquet")