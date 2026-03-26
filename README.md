# TechnipFMC Safety Incident Knowledge Graph

Constructs a typed knowledge graph from ~23,000 TechnipFMC safety incident reports,
enabling structured querying, causal chain analysis, and similar-incident retrieval.

## What it does

1. **Entity extraction** — GLiNER NER identifies equipment, body parts, injuries, locations,
   organizations, and root cause categories from incident narratives
2. **Graph assembly** — Builds a property graph under a fixed schema (7 L1 entity types,
   7 relation types) with metadata-parsed incident properties
3. **Entity resolution** — Deterministic normalization + similarity merge (sim >= 0.90)
   deduplicates entity nodes
4. **Causal enrichment** — LLM-based Layer 2 extraction adds CAUSAL, PRECEDED_BY,
   FAILED_CONTROL, and MITIGATED_BY edges with evidence grounding
5. **Natural language querying** — Translates analyst questions to structured queries
   against the knowledge graph
6. **Event similarity** — Retrieves similar incidents via text embeddings + schema-weighted
   structural overlap
7. **Interactive dashboard** — FastAPI + React frontend for graph exploration and filtering

## Directory Structure

```
├── pipeline/                   # Core KG construction pipeline (L1 + ER + L2)
├── kg_schema/                  # Single source of truth: entity/relation types, golden set
├── natural_language_query/     # NL question -> structured query translation
├── event_similarity/           # Similar incident retrieval (text + structural)
├── visual_dashboard/           # Dashboard: FastAPI backend, React frontend, Streamlit legacy
├── graphRAG/                   # Fall 2025 pipeline (GraphRAG + Mistral 7B, superseded)
├── eda/                        # Exploratory data analysis (fall2025/ and v2_design/)
├── evaluation/                 # Fall 2025 graph evaluation framework
├── cluster/                    # Rice NOTS HPC scripts (SLURM, env setup)
├── incident-embedding-analysis/# Embedding comparison (text, Node2Vec, TransE)
├── translator/                 # Multi-language translation (M2M100, GPU)
├── docs/                       # Design decisions, reviews, operational runbook
├── KG_Plumber/                 # Fall 2025: ThePlumber triple extraction
├── KG_spaCy/                   # Fall 2025: spaCy rule-based extraction
└── data/                       # Incident data (gitignored, see Data Setup below)
```

Each directory has its own README with usage instructions and file descriptions.

## Setup

### Prerequisites

- Python 3.11+
- [Ollama](https://ollama.com/) (required only for L2 causal enrichment and NLQ)

### Local Development

```bash
git clone https://github.com/RiceD2KLab/TechnipFMC_SafetyEvents_Sp26.git
cd TechnipFMC_SafetyEvents_Sp26

python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Ollama Setup (for L2 enrichment and NLQ)

```bash
# Install Ollama (https://ollama.com/download)
ollama serve                    # start the server
ollama pull qwen3:30b-a3b       # L2 enrichment model
ollama pull qwen3:8b            # NLQ translation model (lighter alternative)
```

### Rice NOTS Cluster

See [cluster/README.md](cluster/README.md) for HPC-specific setup (modules, SLURM,
sharded enrichment). The cluster setup script handles venv, Ollama, and module loading:

```bash
bash cluster/setup_cluster_env.sh
```

## Data Setup

Incident data is not committed to the repository (too large). To populate the data directory:

**On Rice NOTS cluster:**
```bash
cp -r /rhf/allocations/dsci435/fmcsafetyevents_sp26/fmcsafetyevents_fa25/data .
```

**Local development:**
Request the consolidated incident CSV from the project sponsor or team lead. Place it at:
```
data/DIM_CONSOLIDATED_ACCIDENTS.xlsx    # or equivalent CSV
```

The pipeline expects a CSV/Excel file with at minimum these columns:
- `RECORD_NO` — unique incident identifier
- `NARRATIVE` — free-text incident description
- `REPORTED_DATE` — incident date
- Metadata fields: `SEVERITY_DESC`, `INCIDENT_TYPE`, `IMPACT_TYPE`, `WORK_PROCESS`,
  `WORKPLACE`, `CLIENT`, `CASE_CATEGORIZATION`, `GENERAL_BUSINESS_UNIT`

A dev sample (first 1,000 records) is available at `graphRAG/input/dev_sample.csv` for
testing the pipeline without the full dataset.

## Usage

### Run the pipeline (L1 extraction + graph assembly)

```bash
# Test run (first 1000 records, ~5 min, no GPU needed)
python pipeline/run_gliner_pipeline.py --test

# Full dataset (~90 min on CPU)
python pipeline/run_gliner_pipeline.py --full
```

Outputs land in `pipeline/outputs/` (entities, relations, metadata parquets).

### Entity resolution

```bash
python -m pipeline.er_prep.run_er_prep
python -m pipeline.er_execution.run_er_execution
```

### L2 causal enrichment (requires Ollama)

```bash
python pipeline/enrichment/run_l2_enrichment.py \
    --nodes-csv pipeline/outputs/entities.parquet \
    --edges-csv pipeline/outputs/relations.parquet \
    --metadata-csv pipeline/outputs/metadata_parsed.parquet \
    --output-dir output/l2/ \
    --backend ollama --model qwen3:30b-a3b
```

### Benchmark (52 golden set queries)

```bash
cd pipeline && python -m benchmark.run_benchmark
```

### Natural language querying

```bash
# Interactive mode
python -m natural_language_query.eval_harness -i

# Run golden set
python -m natural_language_query.run_golden_set
```

### Event similarity

```bash
python -m event_similarity.run_similarity
```

### Dashboard

```bash
# FastAPI backend
cd visual_dashboard/backend && uvicorn main:app --reload

# React frontend (separate terminal)
cd visual_dashboard/frontend && npm install && npm run dev

# Or legacy Streamlit dashboard
streamlit run visual_dashboard/dashboard/app.py
```

## Schema

All entity types, relation types, and evaluation data are defined in
[kg_schema/](kg_schema/README.md) — the single source of truth.

| Layer | Entity Types | Relation Types |
|-------|-------------|----------------|
| L1 (GLiNER + metadata) | 7: INCIDENT, EQUIPMENT, BODY_PART, INJURY_TYPE, LOCATION, ORGANIZATION, ROOT_CAUSE_CATEGORY | 7: INVOLVED, AFFECTED, RESULTED_IN, OCCURRED_AT, REPORTED_BY, CATEGORIZED_AS, LOCATED_IN |
| L2 (LLM enrichment) | 9: Incident, Event, Equipment, Location, Person, Injury, Material, Condition, Action | 4: CAUSAL, PRECEDED_BY, FAILED_CONTROL, MITIGATED_BY |

## Graph Statistics

| Metric | Value |
|--------|-------|
| Incidents processed | 23,311 |
| L1 entity nodes | ~57,000 |
| L1 edges | ~196,000 |
| L2 causal edges | ~34,500 |
| Total graph (merged) | ~100K nodes, ~234K edges |

## Dependencies

| File | Purpose |
|------|---------|
| `requirements.txt` | Full stack (123 packages, pinned versions) |
| `requirements_cluster.txt` | Lean HPC set (24 packages: GLiNER, Splink, DuckDB) |
| `visual_dashboard/backend/requirements.txt` | Dashboard backend (FastAPI, pandas) |
| `incident-embedding-analysis/requirements.txt` | Embedding analysis |

Key packages: `gliner`, `networkx`, `pandas`, `splink`, `duckdb`, `pydantic`,
`transformers`, `fastapi`, `streamlit`.

PyTorch must be installed separately for your CUDA/CPU target before `requirements_cluster.txt`.

## Documentation

- [docs/INDEX.md](docs/INDEX.md) — Central documentation hub
- [docs/operational_runbook.md](docs/operational_runbook.md) — End-to-end operations guide
- [kg_schema/README.md](kg_schema/README.md) — Schema reference
- [pipeline/README.md](pipeline/README.md) — Pipeline architecture and step-by-step guide
- [cluster/README.md](cluster/README.md) — HPC cluster setup and job submission

## Project Context

Rice University D2K Lab capstone project (DSCI 435/535, Spring 2026) in partnership with
TechnipFMC. Builds on Fall 2025 work (GraphRAG-based extraction) with a redesigned
schema-controlled pipeline for production-quality knowledge graph construction.
