# Event Similarity Method Comparison

**Test incidents (N):** 44  |  **Top-K:** 10

Correlation columns are computed against the text embedding baseline.
Hit rate = avg fraction of top-K retrievals sharing ≥1 entity of the given type with the query.
Overlap = avg Jaccard overlap of top-K lists with text embedding top-K.

| Method | Pearson r (vs text) | Spearman ρ (vs text) | Hit Rate — Equipment | Hit Rate — Injury | Hit Rate — Location | Top-K Overlap (vs text) | N | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Text Embedding (all-MiniLM-L6-v2) | 1.0000 | 1.0000 | 0.0257 | 0.0200 | 0.2409 | 1.0000 | 44 | active (baseline) |
| Structural Overlap (Weighted Jaccard) | 0.1552 | 0.1106 | 0.0343 | 0.0200 | 0.6250 | 0.1790 | 44 | active |
| KG Embedding — Node2Vec | 0.1758 | 0.1599 | 0.0086 | 0.0100 | 0.6545 | 0.1976 | 44 | active |
| KG Embedding — TransE | 0.1491 | 0.1408 | 0.0200 | 0.0200 | 0.6114 | 0.1981 | 44 | active |
| KG Embedding — RDF2Vec | 0.0822 | 0.0563 | 0.0286 | 0.0200 | 0.6000 | 0.1766 | 44 | active |
| GNN Embedding — GraphSAGE | 0.0672 | 0.0591 | 0.0086 | 0.0200 | 0.1932 | 0.1709 | 44 | active |
| Hybrid (weighted combination) | 0.7381 | 0.7493 | 0.0314 | 0.0200 | 0.5477 | 0.4433 | 44 | active |