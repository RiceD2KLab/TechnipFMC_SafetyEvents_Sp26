# Event Similarity Method Comparison

**Test incidents (N):** 50  |  **Top-K:** 10

Correlation columns are computed against the text embedding baseline.
Hit rate = avg fraction of top-K retrievals sharing ≥1 entity of the given type with the query.
Overlap = avg Jaccard overlap of top-K lists with text embedding top-K.

| Method | Pearson r (vs text) | Spearman ρ (vs text) | Hit Rate — Equipment | Hit Rate — Injury | Hit Rate — Location | Top-K Overlap (vs text) | N | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Text Embedding (all-MiniLM-L6-v2) | 1.0000 | 1.0000 | 0.0111 | 0.0000 | 0.3040 | 1.0000 | 50 | active (baseline) |
| Structural Overlap (Weighted Jaccard) | 0.1331 | 0.1197 | 0.0083 | 0.0000 | 0.6980 | 0.1646 | 50 | active |
| KG Embedding — Node2Vec | nan | nan | nan | nan | nan | nan | 0 | not trained / threshold not met |
| KG Embedding — TransE | 0.1330 | 0.1258 | 0.0000 | 0.0000 | 0.6820 | 0.1541 | 50 | active |
| GNN Embedding — GraphSAGE | -0.0664 | -0.0352 | 0.0056 | 0.0000 | 0.4440 | 0.1200 | 50 | active |
| Hybrid (weighted combination) | 0.8385 | 0.8411 | 0.0111 | 0.0000 | 0.5360 | 0.4894 | 50 | active |