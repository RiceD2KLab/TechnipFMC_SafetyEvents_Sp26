# Pipeline

Knowledge graph construction pipeline for TechnipFMC safety incident data. Takes raw
incident records (CSV/Parquet) and produces a typed property graph with causal enrichment.

## Pipeline Steps

```
Step 0: Pre-filter     Filter records with no narrative or non-English text
Step 1: GLiNER         Extract entities (equipment, body parts, injuries) via GLiNER NER
Step 2: Metadata       Parse structured fields (location, organization, root cause)
Step 3: Assembly       Build the property graph (nodes + typed edges per kg_schema)
Step 4: Gate 1         Topology evaluation (giant component, degree distribution)
   |
   v
ER Prep  ──────────>   Splink probabilistic entity resolution (optional)
ER Execution  ──────>  Deterministic normalization + similarity merge (sim >= 0.90)
   |
   v
L2 Enrichment  ─────>  LLM causal extraction (CAUSAL, PRECEDED_BY, FAILED_CONTROL, MITIGATED_BY)
L2 Merge  ──────────>  Merge L2 edges into the main graph
   |
   v
Gate 3  ────────────>  Precision/recall evaluation against annotated ground truth
Benchmark  ─────────>  258 golden set queries (kg_schema/golden_set.csv)
```

## Quick Start

```bash
# Steps 0-4 (L1 extraction + graph assembly + Gate 1)
python pipeline/run_gliner_pipeline.py --test           # first 1000 records (~5 min)
python pipeline/run_gliner_pipeline.py --full           # full 23k records (~90 min)

# Entity resolution
python -m pipeline.er_prep.run_er_prep                  # prepare pairwise candidates
python -m pipeline.er_execution.run_er_execution        # apply merge decisions

# L2 causal enrichment (requires Ollama or vLLM running)
python pipeline/enrichment/run_l2_enrichment.py \
    --nodes-csv pipeline/er_execution/outputs/entities_post_er_loc_dedup.parquet \
    --edges-csv pipeline/er_execution/outputs/relations_post_er_loc_dedup.parquet \
    --metadata-csv pipeline/outputs/metadata_parsed.parquet \
    --output-dir output/l2/ \
    --backend ollama --model qwen3:30b-a3b

# Merge L2 edges into graph
python pipeline/enrichment/merge_l2_edges.py \
    --l2-dir output/l2 \
    --entities-parquet pipeline/er_execution/outputs/entities_post_er_loc_dedup.parquet \
    --relations-parquet pipeline/er_execution/outputs/relations_post_er_loc_dedup.parquet \
    --output-dir pipeline/outputs/merged

# Gate 3 evaluation
python pipeline/evaluation/gate3_metrics.py \
    --predicted output/l2 \
    --ground-truth pipeline/annotation/l2_gt_v2_codex.jsonl

# Benchmark (258 golden set queries)
python -m pipeline.benchmark.run_benchmark
```

## Directory Structure

```
pipeline/
├── run_gliner_pipeline.py         # Main entry point (Steps 0-4)
├── extraction/
│   └── gliner_extract.py          # Step 1: GLiNER NER with subword chunking
├── assembly/
│   └── graph_builder.py           # Step 3: Property graph construction
├── evaluation/
│   ├── topology_metrics.py        # Step 4: Gate 1 topology report
│   ├── gate3_metrics.py           # Gate 3: L2 precision/recall/F1
│   ├── compute_kappa.py           # Inter-annotator agreement (Cohen's kappa)
│   └── relation_entropy.py        # Relation type distribution analysis
├── er_prep/
│   ├── run_er_prep.py             # ER candidate generation
│   ├── run_splink.py              # Probabilistic ER via Splink + DuckDB
│   └── splink_config/             # Per-type Splink settings
├── er_execution/
│   └── run_er_execution.py        # Deterministic ER merge (sim >= 0.90)
├── enrichment/
│   ├── run_l2_enrichment.py       # L2 causal extraction (Ollama/vLLM)
│   ├── prompts.py                 # System + user prompts for L2
│   ├── validate.py                # Edge validation (grounding, type checks)
│   ├── merge_l2_edges.py          # Merge L2 edges into main graph
│   └── vllm_client.py             # vLLM backend client
├── benchmark/
│   ├── run_benchmark.py           # Golden set query runner (imports from query_engine/)
│   └── report.py                  # Markdown report generator
├── annotation/
│   ├── l2_gt_v2_claude.jsonl      # Ground truth (Claude annotations, 414 edges)
│   ├── l2_gt_v2_codex.jsonl       # Ground truth (Codex annotations, 374 edges)
│   └── generate_annotation_set.py # Annotation template generator
├── neo4j/
│   └── load_graph.py              # Optional: load graph into Neo4j
├── outputs/                       # Generated parquet files (gitignored)
└── docs/                          # Pipeline-specific analysis docs
```

## Schema

All entity types, relation types, and evaluation data are defined in `kg_schema/`.
See [kg_schema/README.md](../kg_schema/README.md) for the full schema reference.

**L1** (extracted by GLiNER + metadata + validation): 8 entity types, 7 relation types
**L2** (extracted by LLM): 9 entity types, 4 relation types (CAUSAL, PRECEDED_BY, FAILED_CONTROL, MITIGATED_BY)

## Outputs

| File | Description |
|------|-------------|
| `outputs/metadata_parsed.parquet` | Parsed incident metadata used by the current graph (19,820 rows) |
| `outputs/entities.parquet` | Active L1+L2 entity table read by benchmark/dashboard (111,115 rows) |
| `outputs/relations.parquet` | Active L1+L2 relation table (268,781 rows, including L2 evidence columns) |
| `outputs/merged/` | Canonical L2 merge output copied into `outputs/` for consumers |
| `er_execution/outputs/entities_post_er_loc_dedup.parquet` | Post-ER, location-deduped L1 base for L2 enrichment (56,366 rows) |
| `er_execution/outputs/relations_post_er_loc_dedup.parquet` | Post-ER, location-deduped L1 relations for L2 enrichment (199,443 rows) |

## Dependencies

- **GLiNER** (`gliner`): NER model, runs on CPU (~278ms/record)
- **Ollama** or **vLLM**: Required for L2 enrichment only (not needed for L1)
- **DuckDB**: Used by Splink ER (pip-installable, no external service)
- **Neo4j**: Optional, only for `neo4j/load_graph.py`

See `requirements.txt` (full) or `requirements_cluster.txt` (lean, for HPC).

## Cluster Execution

For running on Rice NOTS HPC, see [cluster/README.md](../cluster/README.md).
SLURM batch files: `cluster/submit_l2_enrichment.sbatch`, `cluster/submit_l2_vllm.sbatch`.
