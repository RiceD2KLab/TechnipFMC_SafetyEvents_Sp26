# Pairwise Spearman ρ — All Methods vs All Methods

**Test incidents (N):** 258

Each cell shows the Spearman ρ between the row method (reference) and the column method.
Diagonal entries are 1.0 (each method perfectly correlates with itself).

| Method | Text Embedding | Structural Overlap | Node2Vec | TransE | RDF2Vec | GraphSAGE | Hybrid |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Text Embedding | 1.0000 | 0.1327 | 0.2014 | 0.1537 | 0.0990 | 0.0841 | 0.7669 |
| Structural Overlap | 0.1327 | 1.0000 | 0.5379 | 0.5607 | 0.6299 | 0.0429 | 0.5683 |
| Node2Vec | 0.2014 | 0.5379 | 1.0000 | 0.4813 | 0.4136 | 0.0060 | 0.6546 |
| TransE | 0.1537 | 0.5607 | 0.4813 | 1.0000 | 0.4278 | 0.0843 | 0.6215 |
| RDF2Vec | 0.0990 | 0.6299 | 0.4136 | 0.4278 | 1.0000 | 0.2109 | 0.4188 |
| GraphSAGE | 0.0841 | 0.0429 | 0.0060 | 0.0843 | 0.2109 | 1.0000 | 0.0929 |
| Hybrid | 0.7669 | 0.5683 | 0.6546 | 0.6215 | 0.4188 | 0.0929 | 1.0000 |