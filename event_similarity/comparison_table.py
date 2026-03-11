"""Sponsor measurable: comparison table of all similarity methods.

Produces the table requested in the Finalized Project Objectives (Objective 2):

    "Table comparing Cosine Similarity (LLM), Graph Embeddings, and GNNs
     across a standard set of (50) test safety incidents."

For each available method the table reports:

  Method              | Pearson r vs text | Spearman ρ vs text | Avg Hit Rate (Equip) | Avg Hit Rate (Injury) | Avg Hit Rate (Loc) | Top-10 Overlap vs text | Status
  ────────────────────|───────────────────|────────────────────|──────────────────────|───────────────────────|────────────────────|────────────────────────|────────

Outputs:
  event_similarity/outputs/method_comparison.csv    Machine-readable table
  event_similarity/outputs/method_comparison.md     Markdown-formatted table

Usage:
  # After running run_similarity.py (and optionally training KG/GNN embeddings):
  python -m event_similarity.comparison_table

  # Or import and call directly:
  from event_similarity.comparison_table import build_comparison_table
  df = build_comparison_table(gold_ids, emb_maps, entity_sets, corpus_ids)
"""
from __future__ import annotations

import json
import warnings
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from scipy.stats import pearsonr, spearmanr

from .config import (
    ENTITIES_PATH,
    GOLD_STANDARD_N,
    GOLD_STANDARD_SEED,
    HIGH_VALUE_TYPES,
    METADATA_PATH,
    OUTPUT_DIR,
    RELATIONS_PATH,
    SCHEMA_WEIGHTS,
    TOP_K,
)
from .similarity_eval import (
    _structural_hit_rate,
    compute_method_agreement,
    select_gold_standard_ids,
)
from .structural_similarity import (
    load_entity_sets,
    structural_similarity_matrix,
    top_k_structural,
)
from .text_similarity import (
    compute_text_embeddings,
    load_narratives,
    text_similarity_matrix,
    top_k_similar,
)


# ── Helpers ───────────────────────────────────────────────────────────────


def _cosine_matrix(emb_map: dict[str, np.ndarray], ids: list[str]) -> np.ndarray:
    from .text_similarity import text_similarity_matrix
    return text_similarity_matrix(emb_map, ids)


def _top_k_from_matrix(
    mat: np.ndarray,
    ids: list[str],
    query_id: str,
    k: int,
) -> list[tuple[str, float]]:
    q_idx = ids.index(query_id)
    row   = mat[q_idx]
    pairs = [(ids[j], float(row[j])) for j in range(len(ids)) if ids[j] != query_id]
    return sorted(pairs, key=lambda x: x[1], reverse=True)[:k]


def _avg_hit_rates(
    topk_per_query: dict[str, list[tuple[str, float]]],
    entity_sets: dict[str, dict[str, set[str]]],
) -> dict[str, float | None]:
    agg: dict[str, list[float]] = {et: [] for et in HIGH_VALUE_TYPES}
    for query_id, results in topk_per_query.items():
        hr = _structural_hit_rate(results, query_id, entity_sets, HIGH_VALUE_TYPES)
        for et in HIGH_VALUE_TYPES:
            if hr.get(et) is not None:
                agg[et].append(hr[et])
    return {
        et: round(float(np.mean(vals)), 4) if vals else None
        for et, vals in agg.items()
    }


def _avg_overlap(
    topk_a: dict[str, list[tuple[str, float]]],
    topk_b: dict[str, list[tuple[str, float]]],
    k: int,
) -> float:
    """Avg Jaccard overlap between top-k lists across all queries."""
    overlaps = []
    for q in topk_a:
        if q not in topk_b:
            continue
        set_a = {inc_id for inc_id, _ in topk_a[q][:k]}
        set_b = {inc_id for inc_id, _ in topk_b[q][:k]}
        union = set_a | set_b
        if union:
            overlaps.append(len(set_a & set_b) / len(union))
    return round(float(np.mean(overlaps)), 4) if overlaps else 0.0


# ── Per-method evaluation row ─────────────────────────────────────────────


def _evaluate_method(
    method_name: str,
    sim_matrix: np.ndarray,
    text_matrix: np.ndarray,
    valid_gold: list[str],
    entity_sets: dict[str, dict[str, set[str]]],
    text_topk: dict[str, list[tuple[str, float]]],
    k: int = TOP_K,
) -> dict[str, Any]:
    """Compute all comparison metrics for one method."""
    # Method agreement vs text embedding
    idx = np.tril_indices(sim_matrix.shape[0], k=-1)
    v_method = sim_matrix[idx]
    v_text   = text_matrix[idx]

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        pearson_r,  _ = pearsonr(v_text, v_method)
        spearman_r, _ = spearmanr(v_text, v_method)

    # Top-k retrieval
    method_topk: dict[str, list[tuple[str, float]]] = {
        q: _top_k_from_matrix(sim_matrix, valid_gold, q, k=k)
        for q in valid_gold
    }

    # Hit rates
    hit_rates = _avg_hit_rates(method_topk, entity_sets)

    # Overlap with text top-k
    overlap = _avg_overlap(text_topk, method_topk, k)

    return {
        "method":              method_name,
        "pearson_r_vs_text":   round(float(pearson_r),  4),
        "spearman_r_vs_text":  round(float(spearman_r), 4),
        "hit_rate_equipment":  hit_rates.get("EQUIPMENT"),
        "hit_rate_injury":     hit_rates.get("INJURY_TYPE"),
        "hit_rate_location":   hit_rates.get("LOCATION"),
        "avg_overlap_vs_text": overlap,
        "n_incidents":         len(valid_gold),
        "status":              "active",
    }


# ── Main table builder ────────────────────────────────────────────────────


def build_comparison_table(
    gold_ids: list[str],
    emb_maps: dict[str, dict[str, np.ndarray]],
    entity_sets: dict[str, dict[str, set[str]]],
    corpus_ids: list[str],
    k: int = TOP_K,
    output_dir: Path = OUTPUT_DIR,
) -> pd.DataFrame:
    """Build the sponsor-required method comparison table.

    Args:
        gold_ids: 50 test incident IDs.
        emb_maps: {method_name: {record_no: embedding}}.
                  Include any subset of: "text", "node2vec", "transe",
                  "graphsage".  Structural overlap is always computed.
        entity_sets: Post-ER entity sets {record_no: {type: {values}}}.
        corpus_ids: All incident IDs available for retrieval.
        k: Top-K.
        output_dir: Where to write CSV and Markdown outputs.

    Returns:
        pd.DataFrame with one row per method.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Restrict to incidents with both embeddings + entity sets
    text_emb = emb_maps.get("text", {})
    valid_gold = [
        g for g in gold_ids
        if g in text_emb and g in entity_sets
    ]
    # Further restrict to only those present in ALL provided emb_maps
    for method, emb in emb_maps.items():
        valid_gold = [g for g in valid_gold if g in emb]

    if len(valid_gold) < len(gold_ids):
        print(f"  Note: using {len(valid_gold)}/{len(gold_ids)} gold IDs "
              f"(others missing in one or more embedding maps)")

    rows: list[dict] = []

    # ── Text embedding (baseline) ─────────────────────────────────────────
    text_mat = _cosine_matrix(text_emb, valid_gold)
    text_topk: dict[str, list[tuple[str, float]]] = {
        q: _top_k_from_matrix(text_mat, valid_gold, q, k=k)
        for q in valid_gold
    }
    text_hit = _avg_hit_rates(text_topk, entity_sets)
    rows.append({
        "method":              "Text Embedding (all-MiniLM-L6-v2)",
        "pearson_r_vs_text":   1.0,
        "spearman_r_vs_text":  1.0,
        "hit_rate_equipment":  text_hit.get("EQUIPMENT"),
        "hit_rate_injury":     text_hit.get("INJURY_TYPE"),
        "hit_rate_location":   text_hit.get("LOCATION"),
        "avg_overlap_vs_text": 1.0,
        "n_incidents":         len(valid_gold),
        "status":              "active (baseline)",
    })

    # ── Structural overlap ────────────────────────────────────────────────
    struct_mat = structural_similarity_matrix(entity_sets, valid_gold, SCHEMA_WEIGHTS)
    rows.append(_evaluate_method(
        "Structural Overlap (Weighted Jaccard)",
        struct_mat, text_mat, valid_gold, entity_sets, text_topk, k=k,
    ))

    # ── KG embedding methods (Node2Vec, TransE) ───────────────────────────
    kg_label_map = {
        "node2vec":  "KG Embedding — Node2Vec",
        "transe":    "KG Embedding — TransE",
        "graphsage": "GNN Embedding — GraphSAGE",
    }
    for method_key, label in kg_label_map.items():
        emb = emb_maps.get(method_key, {})
        if not emb:
            rows.append({
                "method":              label,
                "pearson_r_vs_text":   None,
                "spearman_r_vs_text":  None,
                "hit_rate_equipment":  None,
                "hit_rate_injury":     None,
                "hit_rate_location":   None,
                "avg_overlap_vs_text": None,
                "n_incidents":         0,
                "status":              "not trained / threshold not met",
            })
            continue

        # Only evaluate on incidents present in this embedding map
        eval_ids = [g for g in valid_gold if g in emb]
        if len(eval_ids) < 2:
            rows.append({
                "method": label,
                **{k_: None for k_ in [
                    "pearson_r_vs_text", "spearman_r_vs_text",
                    "hit_rate_equipment", "hit_rate_injury", "hit_rate_location",
                    "avg_overlap_vs_text",
                ]},
                "n_incidents": len(eval_ids),
                "status":      "insufficient coverage",
            })
            continue

        method_mat = _cosine_matrix(emb, eval_ids)
        # Re-compute text matrix on the same eval_ids subset
        sub_text_mat = _cosine_matrix(text_emb, eval_ids)
        sub_text_topk: dict[str, list[tuple[str, float]]] = {
            q: _top_k_from_matrix(sub_text_mat, eval_ids, q, k=k)
            for q in eval_ids
        }
        rows.append(_evaluate_method(
            label, method_mat, sub_text_mat,
            eval_ids, entity_sets, sub_text_topk, k=k,
        ))

    # ── Hybrid ────────────────────────────────────────────────────────────
    from .hybrid_similarity import (
        DEFAULT_HYBRID_WEIGHTS,
        hybrid_similarity_matrix,
    )
    available_mats: dict[str, np.ndarray] = {
        "text":       text_mat,
        "structural": struct_mat,
    }
    for method_key in ("node2vec", "transe", "graphsage"):
        emb = emb_maps.get(method_key, {})
        if emb:
            sub_ids = [g for g in valid_gold if g in emb]
            if sub_ids == valid_gold:   # same coverage
                available_mats[method_key] = _cosine_matrix(emb, valid_gold)

    if len(available_mats) >= 2:
        hybrid_mat = hybrid_similarity_matrix(available_mats, valid_gold, DEFAULT_HYBRID_WEIGHTS)
        rows.append(_evaluate_method(
            "Hybrid (weighted combination)",
            hybrid_mat, text_mat, valid_gold, entity_sets, text_topk, k=k,
        ))
    else:
        rows.append({
            "method":  "Hybrid (weighted combination)",
            **{k_: None for k_ in [
                "pearson_r_vs_text", "spearman_r_vs_text",
                "hit_rate_equipment", "hit_rate_injury", "hit_rate_location",
                "avg_overlap_vs_text",
            ]},
            "n_incidents": 0,
            "status":      "insufficient methods available",
        })

    # ── Build DataFrame ───────────────────────────────────────────────────
    df = pd.DataFrame(rows)
    df = df[[
        "method",
        "pearson_r_vs_text", "spearman_r_vs_text",
        "hit_rate_equipment", "hit_rate_injury", "hit_rate_location",
        "avg_overlap_vs_text",
        "n_incidents", "status",
    ]]

    # ── Save outputs ──────────────────────────────────────────────────────
    csv_path = output_dir / "method_comparison.csv"
    df.to_csv(csv_path, index=False)
    print(f"  Comparison table → {csv_path}")

    md_path = output_dir / "method_comparison.md"
    _write_markdown(df, md_path, k=k, n_gold=len(valid_gold))
    print(f"  Markdown table   → {md_path}")

    return df


def _write_markdown(df: pd.DataFrame, path: Path, k: int, n_gold: int) -> None:
    """Write a formatted Markdown comparison table."""
    lines = [
        "# Event Similarity Method Comparison",
        "",
        f"**Test incidents (N):** {n_gold}  |  **Top-K:** {k}",
        "",
        "Correlation columns are computed against the text embedding baseline.",
        "Hit rate = avg fraction of top-K retrievals sharing ≥1 entity of the given type with the query.",
        "Overlap = avg Jaccard overlap of top-K lists with text embedding top-K.",
        "",
    ]

    # Header
    cols = [
        "Method",
        "Pearson r (vs text)",
        "Spearman ρ (vs text)",
        "Hit Rate — Equipment",
        "Hit Rate — Injury",
        "Hit Rate — Location",
        "Top-K Overlap (vs text)",
        "N",
        "Status",
    ]
    lines.append("| " + " | ".join(cols) + " |")
    lines.append("| " + " | ".join(["---"] * len(cols)) + " |")

    def _fmt(val, digits=4) -> str:
        if val is None:
            return "—"
        if isinstance(val, float):
            return f"{val:.{digits}f}"
        return str(val)

    for _, row in df.iterrows():
        cells = [
            str(row["method"]),
            _fmt(row["pearson_r_vs_text"]),
            _fmt(row["spearman_r_vs_text"]),
            _fmt(row["hit_rate_equipment"]),
            _fmt(row["hit_rate_injury"]),
            _fmt(row["hit_rate_location"]),
            _fmt(row["avg_overlap_vs_text"]),
            str(int(row["n_incidents"])) if row["n_incidents"] else "0",
            str(row["status"]),
        ]
        lines.append("| " + " | ".join(cells) + " |")

    path.write_text("\n".join(lines), encoding="utf-8")


# ── CLI entry point ───────────────────────────────────────────────────────


def main() -> None:
    """Load cached artifacts and regenerate the comparison table."""
    import pickle

    print("=" * 65)
    print("  Method Comparison Table — Sponsor Objective 2")
    print("=" * 65)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # ── Load gold IDs ─────────────────────────────────────────────────────
    gold_path = OUTPUT_DIR / "gold_standard_ids.json"
    if gold_path.exists():
        with open(gold_path) as f:
            gold_ids: list[str] = json.load(f)
        print(f"\n  Gold IDs: {len(gold_ids)} loaded from {gold_path}")
    else:
        metadata_df = pd.read_parquet(METADATA_PATH)
        gold_ids = select_gold_standard_ids(
            metadata_df, n=GOLD_STANDARD_N, seed=GOLD_STANDARD_SEED
        )
        print(f"\n  Gold IDs: {len(gold_ids)} auto-selected (stratified)")

    # ── Load entity sets ──────────────────────────────────────────────────
    print("  Loading entity sets …")
    entity_sets = load_entity_sets(RELATIONS_PATH, ENTITIES_PATH)

    # ── Load all available embedding caches ───────────────────────────────
    emb_maps: dict[str, dict[str, np.ndarray]] = {}

    cache_files = {
        "text":       OUTPUT_DIR / "text_embeddings.pkl",
        "node2vec":   OUTPUT_DIR / "node2vec_embeddings.pkl",
        "transe":     OUTPUT_DIR / "transe_embeddings.pkl",
        "graphsage":  OUTPUT_DIR / "graphsage_embeddings.pkl",
    }

    for method, cache in cache_files.items():
        if cache.exists():
            with open(cache, "rb") as f:
                emb_maps[method] = pickle.load(f)
            print(f"  Loaded {method} embeddings ({len(emb_maps[method]):,} incidents)")
        else:
            print(f"  {method}: cache not found at {cache} — skipped")

    if "text" not in emb_maps:
        print("\n  Text embeddings not found.  Run run_similarity.py first.")
        return

    corpus_ids = list(set(emb_maps["text"].keys()) & set(entity_sets.keys()))

    # ── Build table ───────────────────────────────────────────────────────
    print("\n  Building comparison table …")
    df = build_comparison_table(gold_ids, emb_maps, entity_sets, corpus_ids)

    # Print to console
    print("\n" + df.to_string(index=False))


if __name__ == "__main__":
    import json
    main()
