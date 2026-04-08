"""Tier 1 event similarity evaluation (Section 5.5 of the project report).

For each of the Gold Standard query incidents this module computes:

  1. Top-10 most similar incidents under text embedding similarity.
  2. Top-10 most similar incidents under schema-constrained structural overlap.
  3. Method agreement: Pearson and Spearman correlation between the two (N×N)
     similarity matrices over the gold standard subset.
  4. Structural relevance: for each method, the fraction of its top-10
     retrievals that share ≥1 entity of each high-value type (Equipment,
     Injury Type, Location) with the query incident.
  5. Complementarity analysis: incidents appearing in one method's top-5 but
     absent from the other method's top-20, categorised as informative
     divergence or extraction artefact.

Results are serialised to JSON in event_similarity/outputs/.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import pearsonr, spearmanr

from .config import HIGH_VALUE_TYPES, OUTPUT_DIR, SCHEMA_WEIGHTS, SCHEMA_WEIGHTS_UNIFORM, TOP_K
from .structural_similarity import (
    structural_similarity_matrix,
    top_k_structural,
)
from .text_similarity import (
    text_similarity_matrix,
    top_k_similar,
)


# ── Gold standard selection ───────────────────────────────────────────────


def load_gold_ids_from_golden_set(
    golden_set_path: Path,
    metadata_df: pd.DataFrame,
    seed: int = 42,
) -> list[str]:
    """Derive gold standard incident IDs from a golden_set_results.json file.

    Strategy:
      1. Extract every incident record number explicitly referenced in the
         query text (pattern ``#<digits>``) as seed IDs — these are curated
         spot-check incidents that must appear in the evaluation set.
      2. Fill remaining slots via stratified random sampling (same logic as
         ``select_gold_standard_ids``) so that the total equals the number of
         queries in the golden-set file.

    Args:
        golden_set_path: Path to the golden_set_results.json file.
        metadata_df: DataFrame with at minimum columns record_no, incident_type,
                     severity_bin.
        seed: Random seed for the stratified fill step.

    Returns:
        List of record_no strings (length == number of queries in file).
    """
    with open(golden_set_path) as fh:
        data = json.load(fh)

    queries = data.get("queries", [])
    n = len(queries)

    # Step 1 — collect explicitly referenced incident IDs (de-duplicated, ordered)
    seen: set[str] = set()
    seed_ids: list[str] = []
    for q in queries:
        for match in re.findall(r"#(\d+)", q.get("query", "")):
            if match not in seen:
                seen.add(match)
                seed_ids.append(match)

    # Step 2 — fill remainder with stratified sample
    remaining_n = max(0, n - len(seed_ids))
    if remaining_n > 0:
        fill = select_gold_standard_ids(
            metadata_df, n=remaining_n + len(seed_ids), seed=seed
        )
        # keep only those not already in seed_ids
        fill = [r for r in fill if r not in seen]
        seed_ids.extend(fill[: remaining_n])

    return seed_ids[:n]


def select_gold_standard_ids(
    metadata_df: pd.DataFrame,
    n: int = 50,
    seed: int = 42,
) -> list[str]:
    """Stratified sample of n incident IDs for the gold standard set.

    Stratifies jointly by incident_type (Accident / Near Miss / unlabeled)
    and severity_bin (1-5), allocating slots proportionally to stratum size.
    Any remaining slots are filled by uniform random sampling from the
    unstratified pool.

    Args:
        metadata_df: DataFrame with at minimum columns record_no, incident_type,
                     severity_bin.
        n: Number of incidents to select.
        seed: Random seed for reproducibility.

    Returns:
        List of n record_no strings.
    """
    df = metadata_df.copy()
    df["record_no"] = df["record_no"].astype(str)
    df = df.drop_duplicates(subset="record_no")

    df["_type"] = df.get("incident_type", pd.Series(dtype=str)).fillna("unlabeled")
    df["_sev"] = df.get("severity_bin", pd.Series(dtype=float)).fillna(0).astype(int)
    df["_strata"] = df["_type"].str[:3] + "_sev" + df["_sev"].astype(str)

    rng = np.random.default_rng(seed)
    strata_counts = df["_strata"].value_counts()
    n_strata = max(1, n // len(strata_counts))

    sampled: list[str] = []
    for strata in strata_counts.index:
        pool = df.loc[df["_strata"] == strata, "record_no"].tolist()
        take = min(n_strata, len(pool))
        sampled.extend(rng.choice(pool, size=take, replace=False).tolist())

    # Top up to exactly n from the remaining pool
    sampled_set = set(sampled)
    remainder = [r for r in df["record_no"].tolist() if r not in sampled_set]
    if len(sampled) < n and remainder:
        extra = rng.choice(remainder, size=min(n - len(sampled), len(remainder)), replace=False)
        sampled.extend(extra.tolist())

    return sampled[:n]


# ── Per-query helpers ─────────────────────────────────────────────────────


def _structural_hit_rate(
    top_k_results: list[tuple[str, float]],
    query_id: str,
    entity_sets: dict[str, dict[str, set[str]]],
    high_value_types: list[str],
) -> dict[str, float | None]:
    """Fraction of top-K retrievals sharing ≥1 entity of each high-value type.

    Returns {entity_type: hit_rate}.  If the query incident has no entities of
    a given type the value is None (not computable, not a zero).
    """
    query_sets = entity_sets.get(query_id, {})
    hit_rates: dict[str, float | None] = {}

    for etype in high_value_types:
        q_ents = query_sets.get(etype, set())
        if not q_ents:
            hit_rates[etype] = None
            continue
        hits = sum(
            1 for inc_id, _ in top_k_results
            if entity_sets.get(inc_id, {}).get(etype, set()) & q_ents
        )
        hit_rates[etype] = hits / len(top_k_results) if top_k_results else 0.0

    return hit_rates


def _identify_disagreements(
    text_top_k: list[tuple[str, float]],
    struct_top_k: list[tuple[str, float]],
    top_n: int = 5,
    absent_cutoff: int = 20,
) -> dict[str, list[str]]:
    """Identify incidents where the two methods strongly disagree.

    text_only  : in text top-{top_n} but absent from struct top-{absent_cutoff}
    struct_only: in struct top-{top_n} but absent from text top-{absent_cutoff}

    These are candidate informative divergences — they may reveal that the two
    methods capture genuinely different aspects of incident similarity.
    """
    text_top5 = {inc_id for inc_id, _ in text_top_k[:top_n]}
    text_top20 = {inc_id for inc_id, _ in text_top_k[:absent_cutoff]}
    struct_top5 = {inc_id for inc_id, _ in struct_top_k[:top_n]}
    struct_top20 = {inc_id for inc_id, _ in struct_top_k[:absent_cutoff]}

    return {
        "text_only": sorted(text_top5 - struct_top20),
        "struct_only": sorted(struct_top5 - text_top20),
    }


# ── Method agreement ──────────────────────────────────────────────────────


def compute_method_agreement(
    text_matrix: np.ndarray,
    struct_matrix: np.ndarray,
) -> dict[str, float]:
    """Pearson and Spearman correlation between the two similarity matrices.

    Only the lower triangle (excluding the diagonal) is used to avoid
    double-counting symmetric pairs.
    """
    idx = np.tril_indices(text_matrix.shape[0], k=-1)
    v_text = text_matrix[idx]
    v_struct = struct_matrix[idx]

    pearson_r, pearson_p = pearsonr(v_text, v_struct)
    spearman_r, spearman_p = spearmanr(v_text, v_struct)

    return {
        "pearson_r":  float(pearson_r),
        "pearson_p":  float(pearson_p),
        "spearman_r": float(spearman_r),
        "spearman_p": float(spearman_p),
        "n_pairs":    int(len(v_text)),
    }


# ── Main evaluation ───────────────────────────────────────────────────────


def run_tier1_evaluation(
    gold_ids: list[str],
    emb_map: dict[str, np.ndarray],
    entity_sets: dict[str, dict[str, set[str]]],
    corpus_ids: list[str],
    k: int = TOP_K,
    weights: dict[str, float] = SCHEMA_WEIGHTS,
    weights_label: str = "domain_informed",
    output_dir: Path = OUTPUT_DIR,
) -> dict:
    """Full Tier 1 evaluation for the gold standard query set.

    Args:
        gold_ids: 50 gold standard incident IDs (record_no as str).
        emb_map: {record_no: unit-normalised embedding}.
        entity_sets: {record_no: {entity_type: {values}}}.
        corpus_ids: All incident IDs available for retrieval.
        k: Top-K to retrieve per query.
        weights: Structural overlap weight configuration.
        weights_label: Human-readable label (written into output JSON).
        output_dir: Directory for JSON output.

    Returns:
        Dict with keys: metadata, method_agreement, aggregate_hit_rates,
        complementarity, per_query.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Restrict gold set to incidents with both embeddings and entity sets
    text_available = set(emb_map.keys())
    struct_available = set(entity_sets.keys())
    valid_gold = [g for g in gold_ids if g in text_available and g in struct_available]

    skipped = len(gold_ids) - len(valid_gold)
    if skipped:
        print(f"  Note: {skipped} gold IDs skipped (missing text embeddings or entity sets); "
              f"using {len(valid_gold)}")

    # ── Per-query retrieval ───────────────────────────────────────────────
    per_query: dict[str, dict] = {}

    for query_id in valid_gold:
        text_topk   = top_k_similar(emb_map, query_id, corpus_ids, k=k)
        struct_topk = top_k_structural(entity_sets, query_id, corpus_ids, k=k, weights=weights)

        text_hr   = _structural_hit_rate(text_topk,   query_id, entity_sets, HIGH_VALUE_TYPES)
        struct_hr = _structural_hit_rate(struct_topk, query_id, entity_sets, HIGH_VALUE_TYPES)
        disagree  = _identify_disagreements(text_topk, struct_topk)

        per_query[query_id] = {
            "text_top_k":    [(inc_id, round(float(s), 6)) for inc_id, s in text_topk],
            "struct_top_k":  [(inc_id, round(float(s), 6)) for inc_id, s in struct_topk],
            "text_hit_rates":   {et: (round(float(v), 4) if v is not None else None)
                                  for et, v in text_hr.items()},
            "struct_hit_rates": {et: (round(float(v), 4) if v is not None else None)
                                  for et, v in struct_hr.items()},
            "disagreements": disagree,
        }

    # ── Similarity matrix correlation ─────────────────────────────────────
    text_mat   = text_similarity_matrix(emb_map, valid_gold)
    struct_mat = structural_similarity_matrix(entity_sets, valid_gold, weights=weights)
    agreement  = compute_method_agreement(text_mat, struct_mat)

    # ── Aggregate hit rates ───────────────────────────────────────────────
    def _agg_hit_rates(field: str) -> dict[str, float | None]:
        agg: dict[str, float | None] = {}
        for etype in HIGH_VALUE_TYPES:
            vals = [
                r[field][etype]
                for r in per_query.values()
                if r[field].get(etype) is not None
            ]
            agg[etype] = round(float(np.mean(vals)), 4) if vals else None
        return agg

    agg_text   = _agg_hit_rates("text_hit_rates")
    agg_struct = _agg_hit_rates("struct_hit_rates")

    # ── Complementarity summary ───────────────────────────────────────────
    total_text_only   = sum(len(r["disagreements"]["text_only"])   for r in per_query.values())
    total_struct_only = sum(len(r["disagreements"]["struct_only"]) for r in per_query.values())

    results = {
        "metadata": {
            "n_gold":       len(valid_gold),
            "k":            k,
            "weights_label": weights_label,
        },
        "method_agreement": agreement,
        "aggregate_hit_rates": {
            "text_embedding":      agg_text,
            "structural_overlap":  agg_struct,
        },
        "complementarity": {
            "total_text_only_disagreements":   total_text_only,
            "total_struct_only_disagreements": total_struct_only,
        },
        "per_query": per_query,
    }

    out_file = output_dir / f"tier1_eval_{weights_label}.json"
    with open(out_file, "w") as fh:
        json.dump(results, fh, indent=2, default=str)
    print(f"  Results saved → {out_file}")

    return results


# ── Console summary ───────────────────────────────────────────────────────


def print_summary(results: dict) -> None:
    """Print a human-readable summary of Tier 1 evaluation results."""
    meta = results["metadata"]
    ag   = results["method_agreement"]
    hr   = results["aggregate_hit_rates"]
    comp = results["complementarity"]

    print("\n" + "=" * 65)
    print("  EVENT SIMILARITY EVALUATION — TIER 1 SUMMARY")
    print("=" * 65)
    print(f"  Gold incidents : {meta['n_gold']}  |  "
          f"Top-K : {meta['k']}  |  "
          f"Weights : {meta['weights_label']}")
    print()

    print("  ── Method Agreement (Pearson / Spearman) ──")
    print(f"     Pearson  r = {ag['pearson_r']:+.4f}  (p = {ag['pearson_p']:.2e})")
    print(f"     Spearman ρ = {ag['spearman_r']:+.4f}  (p = {ag['spearman_p']:.2e})")
    print(f"     n pairs      = {ag['n_pairs']:,}")
    print()

    print("  ── Structural Hit Rate (avg fraction of top-10 sharing ≥1 entity) ──")
    header = f"  {'Entity Type':<28}  {'Text Emb':>10}  {'Structural':>12}"
    print(header)
    print("  " + "-" * (len(header) - 2))
    for etype in HIGH_VALUE_TYPES:
        t = hr["text_embedding"].get(etype)
        s = hr["structural_overlap"].get(etype)
        t_str = f"{t:.1%}" if t is not None else "  N/A   "
        s_str = f"{s:.1%}" if s is not None else "    N/A   "
        print(f"  {etype:<28}  {t_str:>10}  {s_str:>12}")
    print()

    print("  ── Complementarity ──")
    print(f"     Incidents text-only in top-5 (not in struct top-20) : "
          f"{comp['total_text_only_disagreements']}")
    print(f"     Incidents struct-only in top-5 (not in text top-20) : "
          f"{comp['total_struct_only_disagreements']}")
    print("=" * 65 + "\n")
