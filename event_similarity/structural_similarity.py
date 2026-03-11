"""Schema-constrained relational overlap similarity.

Implements Equation 4 from Section 4.3.1 of the project report:

    S_struct(i, j) = Σ_{k ∈ K}  w_k * |E^k_i ∩ E^k_j| / |E^k_i ∪ E^k_j|

where:
  - E^k_i  is the set of entities of type k linked to incident i
  - w_k    is the domain-informed weight for entity type k (Σ w_k = 1)
  - K      = {EQUIPMENT, INJURY_TYPE, BODY_PART, LOCATION,
              ORGANIZATION, ROOT_CAUSE_CATEGORY}

Entity sets are built from the post-ER relations parquet so that Splink-merged
surface forms are treated as identical before Jaccard computation, directly
improving this measure as described in the report.

Two weight configurations are supported (built-in ablation):
  - domain_informed: EQUIPMENT=0.25, INJURY_TYPE=0.25, BODY_PART=0.15, …
  - uniform: equal weight for all entity types
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from .config import (
    ENTITIES_PATH,
    RELATIONS_PATH,
    SCHEMA_WEIGHTS,
)


# ── Data loading ──────────────────────────────────────────────────────────


def load_entity_sets(
    relations_path: Path = RELATIONS_PATH,
    entities_path: Path = ENTITIES_PATH,
) -> dict[str, dict[str, set[str]]]:
    """Build per-incident typed entity sets from the post-ER graph files.

    Reads the edges parquet (source INCIDENT::X → target ENTITY_TYPE::Y) and
    the nodes parquet (entity_id, entity_type, value) to resolve canonical
    entity values after Splink merging.

    Returns:
        {record_no (str): {entity_type (str): {canonical_value (str), …}}}
    """
    relations = pd.read_parquet(relations_path)

    # Build entity lookup: entity_id → (entity_type, canonical_value)
    ent_lookup: dict[str, tuple[str, str]] = {}
    if entities_path.exists():
        entities = pd.read_parquet(entities_path)
        req_cols = {"entity_id", "entity_type", "value"}
        if req_cols.issubset(entities.columns):
            for _, row in entities.iterrows():
                ent_lookup[str(row["entity_id"])] = (
                    str(row["entity_type"]),
                    str(row["value"]),
                )

    incident_sets: dict[str, dict[str, set[str]]] = {}

    for _, row in relations.iterrows():
        source = str(row.get("source", ""))
        target = str(row.get("target", ""))

        # Only process edges originating from INCIDENT nodes
        if not source.startswith("INCIDENT::"):
            continue

        record_no = source.split("::", 1)[1]

        # Resolve entity type and canonical value
        if target in ent_lookup:
            etype, evalue = ent_lookup[target]
        elif "::" in target:
            # Fall back to parsing the entity_id format ENTITY_TYPE::VALUE
            etype, evalue = target.split("::", 1)
        else:
            continue

        # Skip INCIDENT self-references and LOCATED_IN hierarchy edges
        if etype == "INCIDENT":
            continue

        if record_no not in incident_sets:
            incident_sets[record_no] = {}
        if etype not in incident_sets[record_no]:
            incident_sets[record_no][etype] = set()

        incident_sets[record_no][etype].add(evalue.strip().upper())

    return incident_sets


# ── Per-pair similarity ───────────────────────────────────────────────────


def _jaccard(set_a: set[str], set_b: set[str]) -> float:
    """Jaccard similarity between two entity sets."""
    union = set_a | set_b
    if not union:
        return 0.0
    return len(set_a & set_b) / len(union)


def structural_similarity_score(
    inc_i: dict[str, set[str]],
    inc_j: dict[str, set[str]],
    weights: dict[str, float] = SCHEMA_WEIGHTS,
) -> float:
    """Weighted Jaccard overlap (Eq. 4) between two incidents.

    Args:
        inc_i: {entity_type: {entity_values}} for incident i.
        inc_j: {entity_type: {entity_values}} for incident j.
        weights: Per-entity-type weights (must sum to 1).

    Returns:
        Float in [0, 1].
    """
    score = 0.0
    for etype, weight in weights.items():
        set_i = inc_i.get(etype, set())
        set_j = inc_j.get(etype, set())
        score += weight * _jaccard(set_i, set_j)
    return score


# ── Matrix computation ────────────────────────────────────────────────────


def structural_similarity_matrix(
    entity_sets: dict[str, dict[str, set[str]]],
    incident_ids: list[str],
    weights: dict[str, float] = SCHEMA_WEIGHTS,
) -> np.ndarray:
    """Compute the (N × N) pairwise structural similarity matrix.

    Uses symmetry (S[i,j] == S[j,i]) to halve the computation.

    Args:
        entity_sets: {record_no: {entity_type: {values}}}.
        incident_ids: Ordered list of N incident IDs.
        weights: Weight configuration for Eq. 4.

    Returns:
        np.ndarray of shape (N, N) with values in [0, 1].
    """
    n = len(incident_ids)
    mat = np.zeros((n, n), dtype=float)

    for i, id_i in enumerate(incident_ids):
        mat[i, i] = 1.0
        sets_i = entity_sets.get(id_i, {})
        for j in range(i + 1, n):
            id_j = incident_ids[j]
            sets_j = entity_sets.get(id_j, {})
            val = structural_similarity_score(sets_i, sets_j, weights)
            mat[i, j] = val
            mat[j, i] = val

    return mat


def top_k_structural(
    entity_sets: dict[str, dict[str, set[str]]],
    query_id: str,
    corpus_ids: list[str],
    k: int = 10,
    weights: dict[str, float] = SCHEMA_WEIGHTS,
) -> list[tuple[str, float]]:
    """Return the top-k structurally most similar incidents to query_id.

    The query incident is excluded from the result list.

    Args:
        entity_sets: {record_no: {entity_type: {values}}}.
        query_id: The incident to find neighbours for.
        corpus_ids: Pool of candidate incidents (query_id excluded internally).
        k: Number of results to return.
        weights: Weight configuration for Eq. 4.

    Returns:
        List of (record_no, score) sorted descending by structural similarity.
    """
    query_sets = entity_sets.get(query_id, {})
    corpus_filtered = [i for i in corpus_ids if i != query_id]

    scores = [
        (cid, structural_similarity_score(query_sets, entity_sets.get(cid, {}), weights))
        for cid in corpus_filtered
    ]
    return sorted(scores, key=lambda x: x[1], reverse=True)[:k]
