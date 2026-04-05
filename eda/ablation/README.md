# Ablation Variant Framework

Scoring framework to objectively rank pipeline variants (baseline, +classifier,
+enrichment LLM, +both) using weighted metrics and production readiness gates.

## Context

The v2 pipeline has a modular architecture where a classifier and/or enrichment LLM
can be layered on top of the base GLiNER + deterministic pipeline. This framework
defines how to compare variants objectively, rather than relying on subjective
assessment.

## Metrics (11 total, weighted)

| Metric | Weight | Gate Threshold |
|--------|--------|----------------|
| Relation precision | 0.20 | >= 0.80 |
| Relation recall | 0.15 | - |
| Retrieval precision@5 | 0.15 | - |
| Evidence coverage | 0.10 | >= 0.90 (if LLM used) |
| Overmerge rate | 0.10 | <= 0.10 |
| Max cluster size | 0.05 | - |
| Schema violations | 0.05 | = 0 |
| Runtime (sec/incident) | 0.05 | - |
| Cost ($/1K incidents) | 0.05 | - |
| JSON validity | 0.05 | >= 0.99 (if LLM used) |
| Human agreement | 0.05 | - |

## Current Status

The template exists but no variant has been evaluated yet — all metric cells are empty.
The framework is ready to use once annotation data (from `pipeline/annotation/`)
provides ground truth for precision/recall calculation.

## Files

| File | Purpose |
|------|---------|
| `ablation_scorecard.py` | Scoring engine + gate evaluation |
| `ablation_scorecard.json` | Current scorecard state (empty metrics) |
| `ablation_scorecard.md` | Human-readable scorecard report |
| `ablation_runs_template.csv` | Template for recording variant run metrics |
