# Event Similarity Assessment — Section 4.3

This module implements the **Tier 1 event similarity methods** described in
Section 4.3 of the Spring 2026 Capstone Report.  It operates entirely on
artifacts produced by `pipeline` (post-ER entities and relations) and
requires no additional model training.

---

## Background

The Fall 2025 correlation analysis found that **text embedding similarity and
graph structural distance capture largely independent signals** (Spearman
ρ ≈ −0.04 to −0.10).  The goal of this module is to provide retrieval methods
that reflect *both* signals, so that safety analysts querying for similar
incidents receive results grounded in narrative semantics *and* shared entity
overlap.

---

## Methods

### Tier 1 — Committed

#### 1. Text Embedding Similarity (Equation 3)

```
S_text(i, j) = (z_i · z_j) / (||z_i|| * ||z_j||)
```

Each incident narrative is encoded with
`sentence-transformers/all-MiniLM-L6-v2` (384-dim, unit-normalised).
Pairwise similarity is cosine similarity — equivalent to a dot product after
unit normalisation.

**Source:** `text_similarity.py`

#### 2. Schema-Constrained Relational Overlap (Equation 4)


```
S_struct(i, j) = Σ_k  w_k * |E^k_i ∩ E^k_j| / |E^k_i ∪ E^k_j|
```

For each schema entity type *k*, a weighted Jaccard overlap is computed over
the sets of entity values linked to each incident.  Two weight configurations
are evaluated as a built-in ablation:

| Configuration | EQUIPMENT | INJURY_TYPE | BODY_PART | LOCATION | ORGANIZATION | ROOT_CAUSE_CATEGORY |
|---------------|-----------|-------------|-----------|----------|--------------|---------------------|
| domain-informed | 0.25 | 0.25 | 0.15 | 0.15 | 0.10 | 0.10 |
| uniform        | 0.167 | 0.167 | 0.167 | 0.167 | 0.167 | 0.167 |

Entity sets are built from the **post-ER** relations parquet, so Splink-merged
surface forms are treated as identical before Jaccard computation.

**Source:** `structural_similarity.py`

### Tier 2 — Contingent

#### 3. RDF2Vec (Classic, Skip-Gram)

```
Walk: INCIDENT::i → rel_type → ENTITY_TYPE::v → INV_rel_type → INCIDENT::j → …
```

Classic RDF2Vec (Ristoski & Paulheim, 2016) generates random walks over the
incident–entity graph, interleaving node IDs and relation labels as tokens.
Word2Vec (skip-gram) is then trained on those token sequences, producing an
embedding for each incident node that captures both structural neighbourhood
and relation-type context.

Key differences from Node2Vec and TransE:

| Property | Node2Vec | TransE | RDF2Vec |
|----------|----------|--------|---------|
| Uses relation labels | No | Yes | Yes |
| Training objective | Biased walks + NCE | Margin ranking | Skip-gram |
| Dependency | torch, torch_geometric | pykeen | gensim |

Walks are seeded only from `INCIDENT::` nodes (RDF2vec Light strategy), so
embeddings are produced for incidents only — no vocabulary overhead for
entity nodes.

**Hyperparameters** (configurable in `train_rdf2vec()`):

| Parameter | Default | Note |
|-----------|---------|------|
| `embedding_dim` | 128 | Match other Tier 2 methods |
| `walks_per_node` | 200 | Paper uses 500 for DBpedia |
| `walk_depth` | 4 | Hops per walk; token length = 2×depth+1 |
| `window_size` | 5 | Word2Vec context window |
| `epochs` | 5 | Word2Vec training epochs |
| `sg` | 1 | 1 = skip-gram (recommended), 0 = CBOW |

**Source:** `kg_embeddings.py` — `train_rdf2vec()`

**Dependency:** `pip install gensim`

#### 4. Node2Vec / TransE / GraphSAGE

TransE, Node2Vec, RDF2Vec, and GraphSAGE embeddings are implemented in
`kg_embeddings.py` and `gnn_similarity.py` within this module. They are
activated only if the post-ER graph passes the connectivity threshold
(giant component ratio ≥ 0.85, mean degree ≥ 3.0). If this threshold is
not met the finding is reported as a pipeline diagnostic rather than a failure.

---

## Module Structure

```
event_similarity/
├── __init__.py              Package docstring and public API notes
├── config.py                Paths, model names, weights, gold-standard config
├── text_similarity.py       Eq. 3 — sentence-transformer cosine similarity
├── structural_similarity.py Eq. 4 — weighted Jaccard over entity sets
├── similarity_eval.py       Tier 1 evaluation (top-10, correlation, hit rates)
├── kg_embeddings.py         Tier 2 — Node2Vec, TransE, RDF2Vec embeddings
├── gnn_similarity.py        Tier 2 — GraphSAGE embeddings
├── run_similarity.py        Orchestrator / CLI entry point
├── outputs/                 Auto-created; all results written here
│   ├── gold_standard_ids.json
│   ├── text_embeddings.pkl
│   ├── tier1_eval_domain_informed.json
│   ├── tier1_eval_uniform.json
│   ├── node2vec_embeddings.pkl    (--tier2)
│   ├── transe_embeddings.pkl      (--tier2)
│   ├── rdf2vec_embeddings.pkl     (--tier2)
│   └── graphsage_embeddings.pkl   (--tier2)
└── README.md                This file
```

---

## Prerequisites

The following `pipeline` outputs must exist before running:

| File | Created by |
|------|-----------|
| `pipeline/outputs/metadata_parsed.parquet` | `pipeline/run_gliner_pipeline.py` |
| `pipeline/er_execution/outputs/entities_post_er.parquet` | `pipeline/er_execution/run_er_execution.py` |
| `pipeline/er_execution/outputs/relations_post_er.parquet` | `pipeline/er_execution/run_er_execution.py` |

---

## Running

```bash
# Standard run (uses cached embeddings and gold IDs if available)
python -m event_similarity.run_similarity

# Force recomputation of embeddings and gold IDs
python -m event_similarity.run_similarity --recompute

# Supply your own gold standard incident IDs
python -m event_similarity.run_similarity --gold-ids-file path/to/ids.json
```

The script prints a summary table to stdout and writes full results to
`event_similarity/outputs/`.

---

## Outputs

### `gold_standard_ids.json`
List of 50 incident IDs selected by stratified sampling (incident_type ×
severity_bin).  Fix this file to ensure reproducible evaluation across runs.

### `text_embeddings.pkl`
`Dict[str, np.ndarray]` mapping `record_no → unit-normalised embedding`.
Cached after the first run; delete to force re-encoding.

### `tier1_eval_domain_informed.json` / `tier1_eval_uniform.json`
JSON with the following structure:

```json
{
  "metadata": { "n_gold": 30, "k": 10, "weights_label": "domain_informed" },
  "method_agreement": {
    "pearson_r": 0.0,  "pearson_p": 0.0,
    "spearman_r": 0.0, "spearman_p": 0.0,
    "n_pairs": 435
  },
  "aggregate_hit_rates": {
    "text_embedding":     { "EQUIPMENT": 0.42, "INJURY_TYPE": 0.31, "LOCATION": 0.55 },
    "structural_overlap": { "EQUIPMENT": 0.78, "INJURY_TYPE": 0.65, "LOCATION": 0.71 }
  },
  "complementarity": {
    "total_text_only_disagreements": 12,
    "total_struct_only_disagreements": 9
  },
  "per_query": {
    "<record_no>": {
      "text_top_k":    [["<id>", 0.921], ...],
      "struct_top_k":  [["<id>", 0.500], ...],
      "text_hit_rates":   { "EQUIPMENT": 0.4, "INJURY_TYPE": null, "LOCATION": 0.6 },
      "struct_hit_rates": { "EQUIPMENT": 0.8, "INJURY_TYPE": 0.7,  "LOCATION": 0.9 },
      "disagreements":    { "text_only": [], "struct_only": ["<id>"] }
    }
  }
}
```

---

## Evaluation Metrics (Section 5.5 Tier 1)

| Metric | Description |
|--------|-------------|
| **Pearson r** | Linear correlation between text and structural similarity matrices |
| **Spearman ρ** | Rank correlation between text and structural similarity matrices |
| **Structural hit rate** | Avg fraction of top-10 retrievals sharing ≥1 entity of each high-value type with the query |
| **Text-only disagreements** | Incidents in text top-5 but absent from structural top-20 |
| **Struct-only disagreements** | Incidents in structural top-5 but absent from text top-20 |

---

## Configuration

Edit `config.py` to:

- **Change the sentence-transformer model** — set `SENTENCE_TRANSFORMER_MODEL`
- **Adjust entity type weights** — modify `SCHEMA_WEIGHTS`
- **Fix the gold standard IDs** — set `GOLD_STANDARD_IDS` to a list of
  `record_no` strings (prevents re-sampling on each run)
- **Change the retrieval depth** — set `TOP_K`
- **Tune RDF2Vec** — hyperparameters are arguments to `train_rdf2vec()` in
  `kg_embeddings.py`; cache path is `RDF2VEC_CACHE` in `config.py`

---

## Relationship to Other Modules

| Module | Relationship |
|--------|-------------|
| `pipeline/er_execution/` | Produces the post-ER entity/relation parquets consumed here |
| `pipeline/outputs/metadata_parsed.parquet` | Source of narrative text for embeddings |
| `kg_embeddings.py` / `gnn_similarity.py` | Tier 2 (TransE, Node2Vec, RDF2Vec, GraphSAGE); activated if graph quality thresholds are met |
| `fall2025/evaluation/semantic_similar_distance.py` | Fall 2025 semantic–structural correlation baseline |
| `kg_schema/golden_set.csv` | 258 golden set queries that informed gold standard selection |
