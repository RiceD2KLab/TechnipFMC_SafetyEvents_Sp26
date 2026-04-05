"""event_similarity — Section 4.3 Event Similarity Assessment.

Implements the two committed (Tier 1) similarity methods from the report:

  - Text Embedding Similarity (Eq. 3):
      S_text(i, j) = (z_i · z_j) / (||z_i|| * ||z_j||)
    Incident narratives are encoded with a sentence-transformer and compared
    via cosine similarity.

  - Schema-Constrained Relational Overlap (Eq. 4):
      S_struct(i, j) = Σ_k  w_k * |E^k_i ∩ E^k_j| / |E^k_i ∪ E^k_j|
    Typed entity sets are derived from the post-ER Layer 1 graph and combined
    via domain-informed weighted Jaccard overlap.

Evaluation (Section 5.5 Tier 1):
  - Top-10 retrieval for each method over the 50 Gold Standard query incidents.
  - Pearson / Spearman correlation between the two similarity matrices.
  - Structural hit rate: fraction of top-10 sharing ≥1 entity of each
    high-value type (Equipment, Injury Type, Location) with the query.
  - Complementarity analysis: characterise method disagreements.

Tier 2 extensions (TransE, Node2Vec, GraphSAGE) are implemented in
kg_embeddings.py and gnn_similarity.py within this module, activated only
if the post-ER graph passes the connectivity threshold (giant component
ratio ≥ 0.85, mean degree ≥ 3.0).

Entry point:
    python -m event_similarity.run_similarity [--recompute] [--gold-ids-file FILE]
"""
