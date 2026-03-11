"""Hybrid incident similarity — method (d) in the sponsor objectives.

Combines multiple similarity signals into a single score via a weighted linear
combination:

    S_hybrid(i, j) = Σ_m  α_m * S_m(i, j)     where  Σ α_m = 1

Available signal slots
──────────────────────
  text       : sentence-transformer cosine similarity (method a)
  structural : schema-constrained weighted Jaccard overlap (Eq. 4)
  node2vec   : Node2Vec graph embedding cosine similarity (method b)
  transe     : TransE KG embedding cosine similarity      (method b)
  graphsage  : GraphSAGE GNN embedding cosine similarity  (method c)

Any signal not provided (e.g., because KG training hasn't run yet) is simply
omitted and the remaining weights are re-normalised to sum to 1.  This means
the hybrid always produces a valid score regardless of which methods are
available.

Default weight configuration
─────────────────────────────
  text=0.35, structural=0.35, node2vec=0.15, transe=0.15
  (graphsage=0.0 — not activated until graph quality threshold is met)

These defaults can be overridden by passing a custom weights dict to any
function in this module.
"""
from __future__ import annotations

import numpy as np

# Default hybrid weights (must sum to 1 when all methods present)
DEFAULT_HYBRID_WEIGHTS: dict[str, float] = {
    "text":       0.35,
    "structural": 0.35,
    "node2vec":   0.15,
    "transe":     0.15,
    "graphsage":  0.00,
}


def _normalise_weights(
    weights: dict[str, float],
    available: set[str],
) -> dict[str, float]:
    """Return a copy of weights restricted to available signals, renormalised.

    If a signal is in `weights` but not in `available`, its weight is
    redistributed proportionally among the remaining signals.
    """
    active = {k: v for k, v in weights.items() if k in available and v > 0}
    total  = sum(active.values())
    if total == 0:
        raise ValueError(
            "All hybrid weights are zero after filtering to available signals. "
            f"Available: {available}, weights: {weights}"
        )
    return {k: v / total for k, v in active.items()}


# ── Per-pair hybrid score ─────────────────────────────────────────────────


def hybrid_score(
    inc_i: str,
    inc_j: str,
    similarity_maps: dict[str, dict[str, dict[str, float]]],
    weights: dict[str, float] = DEFAULT_HYBRID_WEIGHTS,
) -> float:
    """Compute the hybrid similarity score between two incidents.

    Args:
        inc_i, inc_j: record_no strings.
        similarity_maps: {method_name: {(inc_a, inc_b): score}} pre-computed
                         pairwise scores.  Keys can be any subset of the
                         DEFAULT_HYBRID_WEIGHTS keys.
        weights: Per-method weights.

    Returns:
        Weighted average similarity score in [0, 1].
    """
    available = set(similarity_maps.keys())
    active_weights = _normalise_weights(weights, available)

    score = 0.0
    for method, w in active_weights.items():
        pair = (inc_i, inc_j)
        rev  = (inc_j, inc_i)
        sim  = similarity_maps[method].get(pair) or similarity_maps[method].get(rev, 0.0)
        score += w * sim

    return score


# ── Matrix combination ────────────────────────────────────────────────────


def hybrid_similarity_matrix(
    similarity_matrices: dict[str, np.ndarray],
    incident_ids: list[str],
    weights: dict[str, float] = DEFAULT_HYBRID_WEIGHTS,
) -> np.ndarray:
    """Combine per-method similarity matrices into a single hybrid matrix.

    Args:
        similarity_matrices: {method_name: (N × N) np.ndarray}.
                             Any subset of methods is accepted.
        incident_ids: Ordered list of N incident IDs (defines matrix rows/cols).
        weights: Per-method weights.

    Returns:
        (N × N) np.ndarray hybrid similarity matrix.
    """
    available = set(similarity_matrices.keys())
    active    = _normalise_weights(weights, available)

    n = len(incident_ids)
    combined = np.zeros((n, n), dtype=float)

    for method, w in active.items():
        combined += w * similarity_matrices[method]

    return combined


# ── Top-k retrieval ───────────────────────────────────────────────────────


def top_k_hybrid(
    similarity_matrices: dict[str, np.ndarray],
    query_id: str,
    incident_ids: list[str],
    k: int = 10,
    weights: dict[str, float] = DEFAULT_HYBRID_WEIGHTS,
) -> list[tuple[str, float]]:
    """Top-k most similar incidents to query_id under the hybrid score.

    Args:
        similarity_matrices: {method_name: (N × N) np.ndarray}.
        query_id: The query incident (must be in incident_ids).
        incident_ids: Ordered list matching the matrix rows/cols.
        k: Number of results to return.
        weights: Per-method weights.

    Returns:
        List of (record_no, hybrid_score) sorted descending, excluding query.
    """
    hybrid_mat = hybrid_similarity_matrix(similarity_matrices, incident_ids, weights)
    q_idx      = incident_ids.index(query_id)
    row        = hybrid_mat[q_idx]

    results = [
        (incident_ids[j], float(row[j]))
        for j in range(len(incident_ids))
        if incident_ids[j] != query_id
    ]
    return sorted(results, key=lambda x: x[1], reverse=True)[:k]


# ── Weight search (optional) ──────────────────────────────────────────────


def learn_hybrid_weights(
    similarity_matrices: dict[str, np.ndarray],
    gold_top_k: dict[str, list[str]],
    incident_ids: list[str],
    k: int = 10,
    n_trials: int = 200,
    seed: int = 42,
) -> dict[str, float]:
    """Find weights maximising average overlap with a gold top-k ranking.

    Uses random search over the simplex to avoid the cost of gradient
    optimisation.  Suitable for up to ~5 methods and a gold set of ≤50
    queries.

    Args:
        similarity_matrices: {method_name: (N × N) np.ndarray}.
        gold_top_k: {query_id: [top-k incident IDs ranked by expert/gold label]}.
        incident_ids: Ordered list matching matrix rows/cols.
        k: Top-K to evaluate.
        n_trials: Number of random weight vectors to try.
        seed: Random seed.

    Returns:
        Best weight dict found (normalised to sum to 1).
    """
    methods = list(similarity_matrices.keys())
    rng     = np.random.default_rng(seed)
    best_score = -1.0
    best_weights: dict[str, float] = {}

    for _ in range(n_trials):
        # Sample a random point on the probability simplex
        raw  = rng.exponential(scale=1.0, size=len(methods))
        norm = raw / raw.sum()
        trial_weights = dict(zip(methods, norm.tolist()))

        # Evaluate: average top-k overlap with gold ranking
        overlap_sum = 0.0
        count = 0
        for query_id, gold_ids in gold_top_k.items():
            if query_id not in incident_ids:
                continue
            retrieved = {
                inc_id
                for inc_id, _ in top_k_hybrid(
                    similarity_matrices, query_id, incident_ids, k=k,
                    weights=trial_weights,
                )
            }
            gold_set = set(gold_ids[:k])
            if gold_set:
                overlap_sum += len(retrieved & gold_set) / len(gold_set)
                count += 1

        avg = overlap_sum / count if count else 0.0
        if avg > best_score:
            best_score   = avg
            best_weights = trial_weights

    print(f"  Best hybrid weights (avg overlap={best_score:.4f}):")
    for m, w in best_weights.items():
        print(f"    {m:<12} = {w:.4f}")

    return best_weights
