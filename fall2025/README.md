# Fall 2025 Capstone Work

Archived code from the Fall 2025 phase of the TechnipFMC safety capstone project.
This work was **superseded by the Spring 2026 pipeline** (`pipeline/`) which uses
GLiNER NER under a controlled schema (`kg_schema/`) instead of free-form LLM extraction.

## Contents

| Directory | Description |
|-----------|-------------|
| `graphRAG/` | Original GraphRAG pipeline (Mistral 7B / Phi extraction, 83K nodes, 156K edges) |
| `evaluation/` | Graph evaluation framework (entity consistency, link prediction, semantic distance) |
| `eda/` | Exploratory data analysis (data profiling, visualization, cleaning) |
| `KG_Plumber/` | ThePlumber-based triple extraction (Docker-based) |
| `KG_spaCy/` | spaCy rule-based subject-verb-object extraction |
| `translator/` | M2M100 multi-language translation for international incident data |
| `incident-embedding-analysis/` | Embedding comparison (text, Node2Vec, TransE) — exploratory research |
| `logics_old/` | Archived dashboard logic handlers (replaced by `visual_dashboard/dashboard/`) |

## Why it was replaced

The GraphRAG approach produced a large but noisy graph with ~156K edges and 3,380
unique relation types. Analysis in `eda/graph_topology/` showed that schema enforcement
was essential. The Spring 2026 pipeline uses:

- **GLiNER** for precise NER under a fixed 7-type L1 schema
- **Deterministic relation assignment** (no free-text relation extraction)
- **LLM-based L2 causal enrichment** with evidence grounding
- **Gate-based evaluation** (topology, inter-annotator agreement, precision/recall)

See `eda/schema_validation/` for the empirical analysis that motivated the redesign.
