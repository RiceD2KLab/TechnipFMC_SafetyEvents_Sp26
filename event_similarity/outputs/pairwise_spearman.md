# Pairwise Spearman ρ — All Methods vs All Methods

**Test incidents (N):** 258

Each cell shows the Spearman ρ between the row method (reference) and the column method.
Diagonal entries are 1.0 (each method perfectly correlates with itself).

| Method | Text Embedding | Structural Overlap | Node2Vec | TransE | RDF2Vec | Hybrid |
| --- | --- | --- | --- | --- | --- | --- |
| Text Embedding | 1.0000 | 0.1504 | 0.2188 | 0.1537 | 0.1051 | 0.7806 |
| Structural Overlap | 0.1504 | 1.0000 | 0.5635 | 0.5460 | 0.5417 | 0.5698 |
| Node2Vec | 0.2188 | 0.5635 | 1.0000 | 0.4611 | 0.4459 | 0.6556 |
| TransE | 0.1537 | 0.5460 | 0.4611 | 1.0000 | 0.3502 | 0.6066 |
| RDF2Vec | 0.1051 | 0.5417 | 0.4459 | 0.3502 | 1.0000 | 0.3889 |
| Hybrid | 0.7806 | 0.5698 | 0.6556 | 0.6066 | 0.3889 | 1.0000 |