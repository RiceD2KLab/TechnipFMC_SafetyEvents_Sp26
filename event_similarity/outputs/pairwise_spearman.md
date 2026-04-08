# Pairwise Spearman ρ — All Methods vs All Methods

**Test incidents (N):** 44

Each cell shows the Spearman ρ between the row method (reference) and the column method.
Diagonal entries are 1.0 (each method perfectly correlates with itself).

| Method | Text Embedding | Structural Overlap | Node2Vec | TransE | RDF2Vec | GraphSAGE | Hybrid |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Text Embedding | 1.0000 | 0.1106 | 0.1599 | 0.1408 | 0.0563 | 0.0591 | 0.7493 |
| Structural Overlap | 0.1106 | 1.0000 | 0.5184 | 0.5922 | 0.6118 | 0.0084 | 0.5730 |
| Node2Vec | 0.1599 | 0.5184 | 1.0000 | 0.4352 | 0.4004 | -0.0446 | 0.6236 |
| TransE | 0.1408 | 0.5922 | 0.4352 | 1.0000 | 0.4016 | -0.0035 | 0.6179 |
| RDF2Vec | 0.0563 | 0.6118 | 0.4004 | 0.4016 | 1.0000 | 0.2080 | 0.3703 |
| GraphSAGE | 0.0591 | 0.0084 | -0.0446 | -0.0035 | 0.2080 | 1.0000 | 0.0154 |
| Hybrid | 0.7493 | 0.5730 | 0.6236 | 0.6179 | 0.3703 | 0.0154 | 1.0000 |