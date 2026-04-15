# Event Similarity Method Comparison

**Test incidents (N):** 258  |  **Top-K:** 10

Correlation columns are computed against the text embedding baseline.
Hit rate = avg fraction of top-K retrievals sharing ≥1 entity of the given type with the query.
Overlap = avg Jaccard overlap of top-K lists with text embedding top-K.

| Method | Pearson r (vs text) | Spearman ρ (vs text) | Hit Rate — Equipment | Hit Rate — Injury | Hit Rate — Location | Top-K Overlap (vs text) | N | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Text Embedding (all-MiniLM-L6-v2) | 1.0000 | 1.0000 | 0.1550 | 0.0787 | 0.3795 | 1.0000 | 258 | active (baseline) |
| Structural Overlap (Weighted Jaccard) | 0.1713 | 0.1504 | 0.1382 | 0.2040 | 0.6155 | 0.0814 | 258 | active |
| KG Embedding — Node2Vec | 0.2241 | 0.2188 | 0.1164 | 0.0800 | 0.8857 | 0.0781 | 258 | active |
| KG Embedding — TransE | 0.1628 | 0.1537 | 0.0929 | 0.0573 | 0.8446 | 0.0619 | 258 | active |
| KG Embedding — RDF2Vec | 0.1178 | 0.1051 | 0.1794 | 0.0960 | 0.7872 | 0.0814 | 258 | active |
| GNN Embedding — GraphSAGE | nan | nan | nan | nan | nan | nan | 0 | not trained / threshold not met |
| Hybrid (weighted combination) | 0.7842 | 0.7806 | 0.1790 | 0.1600 | 0.7775 | 0.2604 | 258 | active |