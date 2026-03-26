# Reproducing Report Results

Maps every table and figure in the project report to the code that produces it.
All commands assume you are in the repository root with the venv activated.

## Prerequisites

```bash
python3.11 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

Ollama is required only for L2 enrichment and NLQ (see README.md for setup).

---

## Table-by-Table Reproduction

### Table 2: Extraction Method Comparison (four-method)

GLiNER column values come from the L1 pipeline run:

```bash
python pipeline/run_gliner_pipeline.py --full
```

**Output:** `pipeline/outputs/metrics_report.md` — contains schema violations, giant
component ratio, mean degree, node/edge counts, and extraction time.

Fall 2025 baselines (spaCy, Plumber, Mistral 7B) are from the prior team's published
evaluation and cannot be re-run from this repo.

### Table 3: Splink ER Pilot Results

Pilot scripts in `eda/entity_resolution/`:

```bash
python eda/entity_resolution/splink_pilot.py           # conservative + full cross-join
python eda/entity_resolution/splink_pilot_labeled.py    # weak-label pilot
```

These read from `fall2025/graphRAG/output_schema_only/` (Fall 2025 graph outputs).

### Table 5: Gate 1 Results

```bash
python pipeline/run_gliner_pipeline.py --full
```

**Output:** `pipeline/outputs/metrics_report.md` — reports schema violations (0),
giant component ratio (1.000), mean degree (6.57), total nodes (61,545), total edges
(202,141).

### Table 6: Gate 2 Entity Resolution Results

```bash
python -m pipeline.er_prep.run_er_prep
python -m pipeline.er_execution.run_er_execution
```

**Output:** Console output reports pre-ER vs post-ER node/edge counts, mean degree,
compression by entity type, and max cluster sizes. Post-ER parquets written to
`pipeline/er_execution/outputs/`.

### Table 7: Entity Compression by Type

Same command as Table 6. Compression percentages are printed to console during
`run_er_execution.py`.

### Table 8: Gate 3 Results

Requires L2 enrichment output (already committed at `pipeline/outputs/` in merged form).
To re-evaluate:

```bash
# Against Codex ground truth
python pipeline/evaluation/gate3_metrics.py \
    --predicted output/l2_edges_merged.jsonl \
    --ground-truth pipeline/annotation/l2_gt_v2_codex.jsonl

# Against Claude ground truth
python pipeline/evaluation/gate3_metrics.py \
    --predicted output/l2_edges_merged.jsonl \
    --ground-truth pipeline/annotation/l2_gt_v2_claude.jsonl
```

**Output:** Console prints precision, chain-adjusted recall, chain-adjusted F1,
evidence F1, causal presence, and pass/fail verdict.

To re-run the full L2 enrichment from scratch (requires Ollama + GPU, ~1 hour):

```bash
python pipeline/enrichment/run_l2_enrichment.py \
    --nodes-csv pipeline/outputs/entities.parquet \
    --edges-csv pipeline/outputs/relations.parquet \
    --metadata-csv pipeline/outputs/metadata_parsed.parquet \
    --output-dir output/l2/ \
    --backend ollama --model qwen3:30b-a3b
```

### Inter-Annotator Agreement (97.1% CAUSAL)

```bash
python pipeline/evaluation/compute_kappa.py \
    pipeline/annotation/l2_gt_v2_claude.jsonl \
    pipeline/annotation/l2_gt_v2_codex.jsonl
```

### Benchmark: 49/52 Queries Pass

```bash
cd pipeline && python -m benchmark.run_benchmark
```

**Output:** `pipeline/benchmark/benchmark_results.md` — per-query pass/fail table,
diagnosis of the 3 extraction-gap warnings, and summary statistics.

### Table 9: NLQ Golden Set Results (44/44)

```bash
# Default: uses local Ollama
python -m natural_language_query.run_golden_set

# Or with Anthropic API
ANTHROPIC_API_KEY=sk-... python -m natural_language_query.run_golden_set --backend anthropic

# Save results
python -m natural_language_query.run_golden_set -o golden_set_results.json
```

**Output:** Console prints per-query pass/fail and category summary. JSON file
contains full translation details.

### Figure 5: NLQ Accuracy Over Iterations

The accuracy chart (`accuracy_chart.png`) was generated during iterative development
and is not reproducible from a single command — it reflects 6 rounds of prompt
engineering. The final 44/44 result is reproducible via the command above.

### Table 10: Event Similarity Method Comparison

```bash
python -m event_similarity.run_similarity
```

**Output:** `event_similarity/outputs/method_comparison.md` — Pearson/Spearman
correlations, hit rates by entity type, top-K overlap, and per-method breakdowns.

Also produces:
- `event_similarity/outputs/tier1_eval_domain_informed.json` — full evaluation results
- `event_similarity/outputs/tier1_eval_uniform.json` — uniform weight ablation

### Table 11: Hit Rates by Entity Type

Same command as Table 10. Hit rates are reported in `method_comparison.md` under
both domain-informed and uniform weight configurations.

### Comparison Table (50 Gold Standard Incidents)

```bash
python -m event_similarity.comparison_table
```

**Output:** `event_similarity/outputs/method_comparison.csv` and `.md` — the sponsor
deliverable table comparing all five methods across 50 gold standard incidents.

---

## Figures

| Figure | Source | Reproducible? |
|--------|--------|---------------|
| Fig 1: KG triplet example | Static diagram (LaTeX tikz) | N/A |
| Fig 3: Pipeline architecture | Static diagram (LaTeX tikz) | N/A |
| Fig 4: Multi-hop reasoning path | Static diagram (LaTeX tikz) | N/A |
| Fig 5: NLQ accuracy over iterations | `accuracy_chart.png` (iterative dev) | Final result only |
| Fig 6: Dashboard main view | Screenshot of React frontend | Run `cd visual_dashboard/frontend && npm run dev` |
| Fig 7: Incident graph view | Screenshot of React + FastAPI | Run backend + frontend (see `visual_dashboard/README.md`) |

---

## Data Artifacts

| Artifact | Path | How to regenerate |
|----------|------|-------------------|
| Input dataset | `input/incidents.csv` | Provided (23,311 records) |
| L1 entities | `pipeline/outputs/entities.parquet` | `python pipeline/run_gliner_pipeline.py --full` |
| L1 relations | `pipeline/outputs/relations.parquet` | Same as above |
| Metadata | `pipeline/outputs/metadata_parsed.parquet` | Same as above |
| Post-ER entities | `pipeline/er_execution/outputs/entities_post_er.parquet` | `python -m pipeline.er_execution.run_er_execution` |
| Post-ER relations | `pipeline/er_execution/outputs/relations_post_er.parquet` | Same as above |
| L2 ground truth | `pipeline/annotation/l2_gt_v2_*.jsonl` | Manually annotated (not regenerable) |
| Golden set queries | `kg_schema/golden_set.csv` | Manually curated (52 queries) |
| Text embeddings | `event_similarity/outputs/text_embeddings.pkl` | `python -m event_similarity.run_similarity --recompute` |
| KG embeddings | `event_similarity/outputs/node2vec_embeddings.pkl` | Same as above |
| Similarity IDs | `event_similarity/outputs/gold_standard_ids.json` | Auto-generated on first run |

---

## Quick Validation (no GPU, ~5 minutes)

```bash
# Run L1 pipeline on first 1000 records
python pipeline/run_gliner_pipeline.py --test

# Run benchmark against existing graph outputs
cd pipeline && python -m benchmark.run_benchmark && cd ..

# Run NLQ golden set (requires Ollama running)
python -m natural_language_query.run_golden_set

# Run event similarity evaluation
python -m event_similarity.run_similarity
```
