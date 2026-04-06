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
| KG Embedding — TransE | 0.1614 | 0.1677 | 0.0000 | 0.0000 | 0.6280 | 0.1589 | 50 | active |
| KG Embedding — RDF2Vec | 0.0722 | 0.0427 | 0.0111 | 0.0000 | 0.6740 | 0.1733 | 50 | active |
| GNN Embedding — GraphSAGE | 0.0798 | 0.0714 | 0.0056 | 0.0000 | 0.2340 | 0.1455 | 50 | active |
| Hybrid (weighted combination) | 0.7444 | 0.7513 | 0.0083 | 0.0000 | 0.6480 | 0.4033 | 50 | active |