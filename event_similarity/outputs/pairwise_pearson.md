# Pairwise Pearson r — All Methods vs All Methods

**Test incidents (N):** 258

Each cell shows the Pearson r between the row method (reference) and the column method.
Diagonal entries are 1.0 (each method perfectly correlates with itself).

| Method | Text Embedding | Structural Overlap | Node2Vec | TransE | RDF2Vec | GraphSAGE | Hybrid |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Text Embedding | 1.0000 | 0.1603 | 0.2050 | 0.1628 | 0.0993 | 0.0914 | 0.7664 |
| Structural Overlap | 0.1603 | 1.0000 | 0.4890 | 0.4817 | 0.6130 | 0.0730 | 0.5859 |
| Node2Vec | 0.2050 | 0.4890 | 1.0000 | 0.5319 | 0.4805 | 0.0130 | 0.6918 |
| TransE | 0.1628 | 0.4817 | 0.5319 | 1.0000 | 0.4405 | 0.0866 | 0.6555 |
| RDF2Vec | 0.0993 | 0.6130 | 0.4805 | 0.4405 | 1.0000 | 0.1811 | 0.4595 |
| GraphSAGE | 0.0914 | 0.0730 | 0.0130 | 0.0866 | 0.1811 | 1.0000 | 0.1006 |
| Hybrid | 0.7664 | 0.5859 | 0.6918 | 0.6555 | 0.4595 | 0.1006 | 1.0000 |