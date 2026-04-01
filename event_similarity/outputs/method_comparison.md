# Event Similarity Method Comparison

**Test incidents (N):** 50  |  **Top-K:** 10

Correlation columns are computed against the text embedding baseline.
Hit rate = avg fraction of top-K retrievals sharing ≥1 entity of the given type with the query.
Overlap = avg Jaccard overlap of top-K lists with text embedding top-K.

| Method | Pearson r (vs text) | Spearman ρ (vs text) | Hit Rate — Equipment | Hit Rate — Injury | Hit Rate — Location | Top-K Overlap (vs text) | N | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Text Embedding (all-MiniLM-L6-v2) | 1.0000 | 1.0000 | 0.0111 | 0.0000 | 0.3040 | 1.0000 | 50 | active (baseline) |
| Structural Overlap (Weighted Jaccard) | 0.1331 | 0.1197 | 0.0083 | 0.0000 | 0.6980 | 0.1646 | 50 | active |
| KG Embedding — Node2Vec | 0.1927 | 0.1710 | 0.0028 | 0.0000 | 0.7380 | 0.1897 | 50 | active |
| KG Embedding — TransE | 0.1097 | 0.0906 | 0.0028 | 0.0000 | 0.6700 | 0.1686 | 50 | active |
| KG Embedding — RDF2Vec | 0.0841 | 0.0681 | 0.0111 | 0.0000 | 0.6640 | 0.1635 | 50 | active |
| GNN Embedding — GraphSAGE | 0.0798 | 0.0714 | 0.0056 | 0.0000 | 0.2340 | 0.1455 | 50 | active |
| Hybrid (weighted combination) | 0.7323 | 0.7412 | 0.0083 | 0.0000 | 0.6560 | 0.3975 | 50 | active |