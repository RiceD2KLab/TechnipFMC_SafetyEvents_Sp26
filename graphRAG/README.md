# GraphRAG Pipeline (Fall 2025)

Original knowledge graph extraction pipeline from the Fall 2025 capstone. Uses Microsoft
GraphRAG with Mistral 7B / Phi models to extract entity-relation triplets from safety
incident narratives.

This pipeline was **superseded by `pipeline/`** in Spring 2026, which uses GLiNER for L1
entity extraction and LLM-based L2 causal enrichment under a controlled schema (`kg_schema/`).

## What it does

1. Takes raw incident CSV as input (`input/dev_sample.csv`, 23.3K records)
2. Runs GraphRAG entity/relation extraction via LLM (Mistral 7B or Phi)
3. Post-processes extracted graphs: filters entity types, drops metadata-heavy relations
4. Exports to CSV for downstream analysis

## Files

| File | Purpose |
|------|---------|
| `settings.yaml` | GraphRAG configuration (LLM models, chunking, extraction) |
| `extract.py` | Extract triplets from GraphRAG parquet output, grouped by incident ID |
| `postprocess.py` | Filter output to allowed entity types, drop noise |
| `to_csv.py` | Convert parquet outputs to CSV |
| `input/` | Input data directory |
| `input/convert_csv.py` | CSV conversion utility |
| `prompts/` | 17 prompt files for extraction, community reports, drift reduction |

## Output directories

| Directory | Description |
|-----------|-------------|
| `output/` | Full Mistral 7B extraction (83K nodes, 156K edges) |
| `output_1k_mistral/` | 1K-record Mistral sample |
| `output_1k_phi/` | 1K-record Phi sample |

## Why it was replaced

The GraphRAG approach produced a large but noisy graph with ~156K edges and no schema
enforcement. The v2 pipeline (`pipeline/`) uses GLiNER for precise NER under a fixed
7-type L1 schema, deterministic relation assignment, and LLM-based L2 causal enrichment
with evidence grounding. See `eda/v2_design/schema_validation/` for the empirical
analysis that motivated the redesign.
