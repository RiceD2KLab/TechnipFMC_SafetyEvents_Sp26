# Exploratory Data Analysis

Analysis and profiling work that informed the pipeline design. Split into two phases:

## `fall2025/` — Fall 2025 Capstone EDA

Initial data profiling of the raw TechnipFMC safety incident dataset. Covers data quality
assessment, missingness patterns, categorical distributions, and text analysis.

**Entry point:** `main.py` — loads, cleans, and visualizes the consolidated incident data.

| File | Purpose |
|------|---------|
| `main.py` | Entry point: data loading, cleaning, visualization |
| `dataFeatures.py` | Feature analysis: common columns across CSV files, dataset summaries |
| `dataModifier.py` | Data transformation: column-to-sentence conversion, cleaning |
| `dataVisualizer.py` | Visualization: data types, cardinality, missing values, correlations, n-grams |
| `consolidated_eda.py` | Advanced EDA: missingness correlation, coverage by org/system, categorical top values |
| `data_clean/` | Data loading and horizontal coalescing across multiple source files |
| `charts/` | 46 generated visualizations |
| `visualization/` | 16 text analysis visualizations (word clouds, n-grams, correlations) |

## `v2_design/` — V2 Pipeline Design Analysis

Empirical analysis that justified the v2 schema and pipeline architecture. Each subdirectory
has its own README with detailed methodology and results.

| Subdirectory | Purpose |
|--------------|---------|
| `schema_validation/` | Evidence for v1 to v2 schema changes (8 analyses, 23K records) |
| `benchmark_design/` | Data profiling that informed the 52 golden set queries |
| `graph_topology/` | Graph health metrics, schema enforcement, guardrail design |
| `entity_resolution/` | ER strategy evaluation, false positive analysis, Splink pilot |
| `ablation/` | Variant scoring framework (weighted metrics, hard gates) |
| `visualizations/` | V1 vs V2 comparison charts for the project report |
