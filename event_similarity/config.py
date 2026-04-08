"""Centralised configuration for the event_similarity module.

All file paths, model names, weight configurations, and tunable parameters
live here.  Edit this file to point at different data sources or to swap the
sentence-transformer model without touching the core logic files.
"""
from __future__ import annotations

from pathlib import Path

from kg_schema import L1_ENTITY_TYPE_NAMES

# ── Project root ──────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent

# ── Input data (pipeline outputs) ──────────────────────────────────────
# narratives + incident properties (record_no, narrative, severity_bin, …)
METADATA_PATH = ROOT / "pipeline" / "outputs" / "metadata_parsed.parquet"

# post-ER entity nodes  (entity_id, entity_type, value, …)
ENTITIES_PATH = ROOT / "pipeline" / "er_execution" / "outputs" / "entities_post_er.parquet"

# post-ER edges  (source INCIDENT::X  →  target ENTITY_TYPE::Y, relation, …)
RELATIONS_PATH = ROOT / "pipeline" / "er_execution" / "outputs" / "relations_post_er.parquet"

# ── Output directory ──────────────────────────────────────────────────────
OUTPUT_DIR = ROOT / "event_similarity" / "outputs"

# ── Text embedding model ──────────────────────────────────────────────────
# all-MiniLM-L6-v2: 384-dim, fast, strong sentence-level semantics
SENTENCE_TRANSFORMER_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
EMBEDDING_BATCH_SIZE = 64

# ── Schema-constrained relational overlap weights (Eq. 4 in report) ───────
# Domain-informed configuration: EQUIPMENT and INJURY_TYPE carry more weight
# because shared equipment and injury patterns are stronger similarity signals
# than shared dates or organisations (per Section 4.3.1).
SCHEMA_WEIGHTS: dict[str, float] = {
    "EQUIPMENT":           0.25,
    "INJURY_TYPE":         0.25,
    "BODY_PART":           0.15,
    "LOCATION":            0.15,
    "ORGANIZATION":        0.10,
    "ROOT_CAUSE_CATEGORY": 0.10,
}

# Validate that all weighted types exist in the canonical schema
_unknown = set(SCHEMA_WEIGHTS) - L1_ENTITY_TYPE_NAMES
assert not _unknown, f"SCHEMA_WEIGHTS references unknown entity types: {_unknown}"

# Uniform ablation: equal weight for all entity types (built-in ablation)
SCHEMA_WEIGHTS_UNIFORM: dict[str, float] = {k: 1 / len(SCHEMA_WEIGHTS) for k in SCHEMA_WEIGHTS}

# ── Structural hit rate: high-value entity types (Section 5.5) ────────────
HIGH_VALUE_TYPES: list[str] = ["EQUIPMENT", "INJURY_TYPE", "LOCATION"]

# ── Gold standard selection ───────────────────────────────────────────────
# GOLD_STANDARD_IDS: pre-set list of record_no strings, or None to auto-select.
# When None, run_similarity.py calls load_gold_ids_from_golden_set() which reads
# directly from kg_schema/golden_set.csv — the canonical source of truth for all
# 258 benchmark queries.  No LLM translation step is required.
#
# Incident IDs explicitly referenced in query names (e.g. "#29857") are used as
# seed IDs; remaining slots are filled via stratified random sampling so that the
# total equals the number of queries in the CSV (currently 258).
from kg_schema.golden_set import GOLDEN_SET_CSV

GOLDEN_SET_PATH: Path = GOLDEN_SET_CSV   # points to kg_schema/golden_set.csv

GOLD_STANDARD_IDS: list[str] | None = None

def _gold_standard_n_default() -> int:
    """Return the number of rows in the golden set CSV, falling back to 258."""
    try:
        import csv as _csv
        with open(GOLDEN_SET_PATH, newline="", encoding="utf-8") as _fh:
            return sum(1 for _ in _csv.DictReader(_fh))
    except Exception:
        return 258

GOLD_STANDARD_N: int = _gold_standard_n_default()
GOLD_STANDARD_SEED: int = 42

# ── Retrieval ─────────────────────────────────────────────────────────────
TOP_K: int = 10

# ── KG / GNN embedding cache paths ───────────────────────────────────────
# These are populated by kg_embeddings.py and gnn_similarity.py.
# Set to None in those modules to skip caching (always retrain).
NODE2VEC_CACHE:  Path = OUTPUT_DIR / "node2vec_embeddings.pkl"
TRANSE_CACHE:    Path = OUTPUT_DIR / "transe_embeddings.pkl"
GRAPHSAGE_CACHE: Path = OUTPUT_DIR / "graphsage_embeddings.pkl"
RDF2VEC_CACHE:   Path = OUTPUT_DIR / "rdf2vec_embeddings.pkl"

# GraphSAGE activation thresholds (Section 4.3.2 of the project report)
GRAPHSAGE_GCR_THRESHOLD: float = 0.85   # giant component ratio
GRAPHSAGE_DEG_THRESHOLD: float = 3.0    # mean degree
