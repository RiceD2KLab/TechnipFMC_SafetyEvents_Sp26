"""Orchestrator for the Section 4.3 Event Similarity pipeline.

Executes the full Tier 1 evaluation workflow:
  1. Load incident narratives from pipeline/outputs/metadata_parsed.parquet.
  2. Load post-ER entity sets from pipeline/er_execution/outputs/.
  3. Select (or load) the Gold Standard incident IDs.
  4. Compute sentence-transformer text embeddings (cached to outputs/).
  5. Run Tier 1 evaluation for both weight configurations:
       - domain_informed (EQUIPMENT=0.25, INJURY_TYPE=0.25, …)
       - uniform (all entity types weighted equally — ablation)
  6. Train any requested KG / GNN embeddings (--models):
       - node2vec   (requires: pip install torch torch_geometric)
       - transe     (requires: pip install torch pykeen)
       - rdf2vec    (requires: pip install gensim)
       - graphsage  (requires: pip install torch torch_geometric)
  7. Build the sponsor comparison table across all available methods.

Usage:
    # Tier 1 only (text + structural) — default, always replaces pkl files
    python -m event_similarity.run_similarity

    # Add specific KG/GNN models
    python -m event_similarity.run_similarity --models node2vec
    python -m event_similarity.run_similarity --models node2vec transe
    python -m event_similarity.run_similarity --models node2vec transe rdf2vec graphsage

    # Run all models
    python -m event_similarity.run_similarity --models all

    # Reuse existing pkl caches instead of recomputing
    python -m event_similarity.run_similarity --models node2vec --cache

    # Supply a custom gold IDs file
    python -m event_similarity.run_similarity --gold-ids-file path/to/ids.json

Outputs (all written to event_similarity/outputs/):
    gold_standard_ids.json          Selected gold standard incident IDs
    text_embeddings.pkl             Cached sentence-transformer embeddings
    tier1_eval_domain_informed.json Per-query results + aggregate metrics
    tier1_eval_uniform.json         Ablation run with uniform weights
    node2vec_embeddings.pkl         Node2Vec KG embeddings (if requested)
    transe_embeddings.pkl           TransE KG embeddings   (if requested)
    rdf2vec_embeddings.pkl          RDF2Vec KG embeddings  (if requested)
    graphsage_embeddings.pkl        GraphSAGE GNN embeddings (if requested)
    method_comparison.csv           All-method comparison table (always regenerated)
    method_comparison.md            Markdown version of comparison table (always regenerated)
    pairwise_pearson.csv/md         Pairwise Pearson r matrix (always regenerated)
    pairwise_spearman.csv/md        Pairwise Spearman ρ matrix (always regenerated)
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from .comparison_table import build_comparison_table
from .config import (
    ENTITIES_PATH,
    GOLD_STANDARD_IDS,
    GOLD_STANDARD_N,
    GOLD_STANDARD_SEED,
    GOLDEN_SET_PATH,
    METADATA_PATH,
    OUTPUT_DIR,
    RELATIONS_PATH,
    SCHEMA_WEIGHTS,
    SCHEMA_WEIGHTS_UNIFORM,
    TOP_K,
)
from .similarity_eval import (
    load_gold_ids_from_golden_set,
    print_summary,
    run_tier1_evaluation,
    select_gold_standard_ids,
)
from .structural_similarity import load_entity_sets
from .text_similarity import compute_text_embeddings, load_narratives


def _check_inputs() -> None:
    """Raise informative errors if required pipeline outputs are missing."""
    missing = []
    if not METADATA_PATH.exists():
        missing.append(
            f"  {METADATA_PATH}\n"
            "  → run:  python -m pipeline.run_gliner_pipeline"
        )
    if not RELATIONS_PATH.exists():
        missing.append(
            f"  {RELATIONS_PATH}\n"
            "  → run:  python -m pipeline.er_execution.run_er_execution"
        )
    if missing:
        raise FileNotFoundError(
            "Required input files not found:\n" + "\n".join(missing)
        )


ALL_KG_MODELS = ("node2vec", "transe", "rdf2vec", "graphsage")


def main(
    recompute: bool = True,
    gold_ids_file: Path | None = None,
    models: set | None = None,
) -> None:
    """Run the event similarity pipeline end-to-end.

    Args:
        recompute: When True (default), replace existing pkl files.
        gold_ids_file: Optional path to a pre-built gold IDs JSON file.
        models: Set of KG/GNN model names to train, e.g. {"node2vec", "transe"}.
                Pass an empty set (or None) to run Tier 1 only.
                Pass set(ALL_KG_MODELS) to run everything.
    """
    if models is None:
        models = set()
    print("=" * 65)
    print("  Event Similarity Pipeline — Section 4.3")
    print("=" * 65)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    _check_inputs()

    # ── 1. Load metadata ──────────────────────────────────────────────────
    print("\n[1/5] Loading incident metadata …")
    metadata_df = pd.read_parquet(METADATA_PATH)
    print(f"      {len(metadata_df):,} records loaded")

    # ── 2. Load post-ER entity sets ───────────────────────────────────────
    print("\n[2/5] Loading post-ER entity sets …")
    entity_sets = load_entity_sets(RELATIONS_PATH, ENTITIES_PATH)
    print(f"      Entity sets available for {len(entity_sets):,} incidents")

    # ── 3. Determine gold standard IDs ───────────────────────────────────
    print("\n[3/5] Determining gold standard incidents …")
    gold_ids_cache = OUTPUT_DIR / "gold_standard_ids.json"

    if gold_ids_file is not None and Path(gold_ids_file).exists():
        with open(gold_ids_file) as fh:
            gold_ids: list[str] = json.load(fh)
        print(f"      Loaded {len(gold_ids)} IDs from {gold_ids_file}")

    elif GOLD_STANDARD_IDS is not None:
        gold_ids = [str(i) for i in GOLD_STANDARD_IDS]
        print(f"      Using {len(gold_ids)} pre-configured IDs from config.py")

    elif gold_ids_cache.exists() and not recompute:
        with open(gold_ids_cache) as fh:
            gold_ids = json.load(fh)
        print(f"      Loaded {len(gold_ids)} cached IDs from {gold_ids_cache}")

    elif GOLDEN_SET_PATH.exists():
        gold_ids = load_gold_ids_from_golden_set(
            GOLDEN_SET_PATH, metadata_df, seed=GOLD_STANDARD_SEED
        )
        with open(gold_ids_cache, "w") as fh:
            json.dump(gold_ids, fh, indent=2)
        print(f"      Derived {len(gold_ids)} IDs from {GOLDEN_SET_PATH.name} → {gold_ids_cache}")

    else:
        gold_ids = select_gold_standard_ids(
            metadata_df, n=GOLD_STANDARD_N, seed=GOLD_STANDARD_SEED
        )
        with open(gold_ids_cache, "w") as fh:
            json.dump(gold_ids, fh, indent=2)
        print(f"      Selected + saved {len(gold_ids)} stratified IDs → {gold_ids_cache}")

    # ── 4. Compute text embeddings ─────────────────────────────────────────
    print("\n[4/5] Computing / loading text embeddings …")
    emb_cache = None if recompute else OUTPUT_DIR / "text_embeddings.pkl"
    narratives_df = load_narratives(METADATA_PATH)
    emb_map = compute_text_embeddings(narratives_df, cache_path=emb_cache)
    print(f"      Embeddings available for {len(emb_map):,} incidents")

    # Corpus = incidents with both an embedding and an entity set
    corpus_ids = list(set(emb_map.keys()) & set(entity_sets.keys()))
    print(f"      Retrieval corpus (text ∩ structural): {len(corpus_ids):,} incidents")

    # ── 5. Tier 1 evaluation ──────────────────────────────────────────────
    print("\n[5/5] Running Tier 1 evaluation …")

    # 5a. Domain-informed weights (primary result)
    print("  → domain-informed weights")
    results_domain = run_tier1_evaluation(
        gold_ids=gold_ids,
        emb_map=emb_map,
        entity_sets=entity_sets,
        corpus_ids=corpus_ids,
        k=TOP_K,
        weights=SCHEMA_WEIGHTS,
        weights_label="domain_informed",
        output_dir=OUTPUT_DIR,
    )
    print_summary(results_domain)

    # 5b. Uniform weights (built-in ablation)
    print("  → uniform weights (ablation)")
    results_uniform = run_tier1_evaluation(
        gold_ids=gold_ids,
        emb_map=emb_map,
        entity_sets=entity_sets,
        corpus_ids=corpus_ids,
        k=TOP_K,
        weights=SCHEMA_WEIGHTS_UNIFORM,
        weights_label="uniform",
        output_dir=OUTPUT_DIR,
    )

    # ── 6. KG and GNN embeddings ──────────────────────────────────────────
    import pickle

    tier2_emb_maps: dict[str, dict] = {}

    _model_configs = {
        "node2vec":  OUTPUT_DIR / "node2vec_embeddings.pkl",
        "transe":    OUTPUT_DIR / "transe_embeddings.pkl",
        "rdf2vec":   OUTPUT_DIR / "rdf2vec_embeddings.pkl",
        "graphsage": OUTPUT_DIR / "graphsage_embeddings.pkl",
    }

    if models:
        print(f"\n[6/7] Training KG / GNN embeddings: {', '.join(sorted(models))} …")

        from .gnn_similarity import train_graphsage
        from .kg_embeddings import train_node2vec, train_rdf2vec, train_transe

        _trainers = {
            "node2vec":  lambda cache: train_node2vec(cache_path=cache),
            "transe":    lambda cache: train_transe(cache_path=cache),
            "rdf2vec":   lambda cache: train_rdf2vec(cache_path=cache),
            "graphsage": lambda cache: train_graphsage(cache_path=cache),
        }

        for model_name in ALL_KG_MODELS:
            if model_name not in models:
                continue
            cache = _model_configs[model_name]
            if recompute:
                cache.unlink(missing_ok=True)
            print(f"  → {model_name} …")
            try:
                emb = _trainers[model_name](cache)
                if emb:
                    tier2_emb_maps[model_name] = emb
                    print(f"     {model_name} embeddings: {len(emb):,} incidents")
                else:
                    print(f"     {model_name} returned empty — skipped")
            except ImportError as e:
                print(f"     {model_name} skipped (missing dependency): {e}")
    else:
        print("\n[6/7] No KG/GNN models requested (pass --models to select)")

    # ── Load cached embeddings for models not trained this run ────────────
    # Ensures the comparison table includes any previously trained models
    # even if they were not requested in this run.
    for _method, _cache in _model_configs.items():
        if _method not in tier2_emb_maps and _cache.exists():
            with open(_cache, "rb") as _f:
                tier2_emb_maps[_method] = pickle.load(_f)
            print(f"  Loaded cached {_method} embeddings ({len(tier2_emb_maps[_method]):,} incidents)")

    # ── 7. Method comparison table ────────────────────────────────────────
    print("\n[7/7] Building method comparison table …")
    emb_maps = {"text": emb_map, **tier2_emb_maps}
    build_comparison_table(
        gold_ids=gold_ids,
        emb_maps=emb_maps,
        entity_sets=entity_sets,
        corpus_ids=corpus_ids,
        k=TOP_K,
        output_dir=OUTPUT_DIR,
    )

    print("\nAll outputs written to:", OUTPUT_DIR)
    print("Done.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run the event similarity pipeline (Section 4.3).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--cache",
        action="store_true",
        help=(
            "Load embeddings and gold IDs from existing .pkl / .json cache files "
            "instead of recomputing. By default all pkl files are replaced on every run."
        ),
    )
    parser.add_argument(
        "--gold-ids-file",
        type=Path,
        default=None,
        metavar="FILE",
        help="Path to a JSON file containing a list of gold standard incident IDs.",
    )
    parser.add_argument(
        "--models",
        nargs="+",
        metavar="MODEL",
        default=[],
        help=(
            "KG/GNN models to train. Choose any combination of: "
            "node2vec, transe, rdf2vec, graphsage. "
            "Use 'all' to run every model. "
            "Example: --models node2vec transe"
        ),
    )
    args = parser.parse_args()

    requested = set(args.models)
    if "all" in requested:
        requested = set(ALL_KG_MODELS)

    invalid = requested - set(ALL_KG_MODELS)
    if invalid:
        parser.error(f"Unknown model(s): {', '.join(sorted(invalid))}. "
                     f"Valid options: {', '.join(ALL_KG_MODELS)}")

    main(recompute=not args.cache, gold_ids_file=args.gold_ids_file, models=requested)
