# Event Similarity Method Comparison

**Test incidents (N):** 258  |  **Top-K:** 10

Correlation columns are computed against the text embedding baseline.
Hit rate = avg fraction of top-K retrievals sharing ≥1 entity of the given type with the query.
Overlap = avg Jaccard overlap of top-K lists with text embedding top-K.

| Method | Pearson r (vs text) | Spearman ρ (vs text) | Hit Rate — Equipment | Hit Rate — Injury | Hit Rate — Location | Top-K Overlap (vs text) | N | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Text Embedding (all-MiniLM-L6-v2) | 1.0000 | 1.0000 | 0.0409 | 0.0438 | 0.3814 | 1.0000 | 258 | active (baseline) |
| Structural Overlap (Weighted Jaccard) | 0.1603 | 0.1327 | 0.0649 | 0.1260 | 0.6504 | 0.0839 | 258 | active |
| KG Embedding — Node2Vec | 0.2050 | 0.2014 | 0.0236 | 0.0329 | 0.9318 | 0.0666 | 258 | active |
| KG Embedding — TransE | 0.1628 | 0.1537 | 0.0269 | 0.0370 | 0.8461 | 0.0619 | 258 | active |
| KG Embedding — RDF2Vec | 0.0993 | 0.0866 | 0.0543 | 0.0603 | 0.8496 | 0.0797 | 258 | active |
| GNN Embedding — GraphSAGE | 0.0914 | 0.0841 | 0.0115 | 0.0411 | 0.2907 | 0.0358 | 258 | active |
| Hybrid (weighted combination) | 0.7664 | 0.7669 | 0.0611 | 0.0973 | 0.8140 | 0.2442 | 258 | active |