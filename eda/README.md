# Exploratory Data Analysis

Design-phase analysis that informed the pipeline architecture. Each subdirectory
has its own README with detailed methodology and results.

| Subdirectory | Purpose |
|--------------|---------|
| `schema_validation/` | Evidence for v1 to v2 schema changes (8 analyses, 23K records) |
| `benchmark_design/` | Data profiling that informed the 52 golden set queries |
| `graph_topology/` | Graph health metrics, schema enforcement, guardrail design |
| `entity_resolution/` | ER strategy evaluation, false positive analysis, Splink pilot |
| `ablation/` | Variant scoring framework (weighted metrics, hard gates) |
| `visualizations/` | V1 vs V2 comparison charts for the project report |

Fall 2025 EDA work is in `fall2025/eda/`.
