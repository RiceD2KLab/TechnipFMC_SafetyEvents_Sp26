"""Orchestrator for the Section 4.3 Event Similarity pipeline.

Executes the full Tier 1 evaluation workflow:
  1. Load incident narratives from pipeline/outputs/metadata_parsed.parquet.
  2. Load post-ER entity sets from pipeline/er_execution/outputs/.
  3. Select (or load) the 50 Gold Standard incident IDs.
  4. Compute sentence-transformer text embeddings (cached to outputs/).
  5. Run Tier 1 evaluation for both weight configurations:
       - domain_informed (EQUIPMENT=0.25, INJURY_TYPE=0.25, …)
       - uniform (all entity types weighted equally — ablation)
  6. (Optional, --tier2) Train KG and GNN embeddings:
       - Node2Vec   (requires: pip install torch torch_geometric)
       - TransE     (requires: pip install torch pykeen)
       - GraphSAGE  (requires: pip install torch torch_geometric)
  7. Build the sponsor comparison table across all available methods.

Usage:
    python -m event_similarity.run_similarity
    python -m event_similarity.run_similarity --recompute
    python -m event_similarity.run_similarity --tier2
    python -m event_similarity.run_similarity --tier2 --recompute
    python -m event_similarity.run_similarity --gold-ids-file path/to/ids.json

Outputs (all written to event_similarity/outputs/):
    gold_standard_ids.json          Selected gold standard incident IDs
    text_embeddings.pkl             Cached sentence-transformer embeddings
    tier1_eval_domain_informed.json Per-query results + aggregate metrics
    tier1_eval_uniform.json         Ablation run with uniform weights
    node2vec_embeddings.pkl         Node2Vec KG embeddings (--tier2 only)
    transe_embeddings.pkl           TransE KG embeddings   (--tier2 only)
    rdf2vec_embeddings.pkl          RDF2Vec KG embeddings  (--tier2 only)
    graphsage_embeddings.pkl        GraphSAGE GNN embeddings (--tier2 only)
    method_comparison.csv           All-method comparison table (always regenerated)
    method_comparison.md            Markdown version of comparison table (always regenerated)
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
    METADATA_PATH,
    OUTPUT_DIR,
    RELATIONS_PATH,
    SCHEMA_WEIGHTS,
    SCHEMA_WEIGHTS_UNIFORM,
    TOP_K,
)
from .similarity_eval import (
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


def main(
    recompute: bool = False,
    gold_ids_file: Path | None = None,
    run_tier2: bool = False,
) -> None:
    """Run the event similarity pipeline end-to-end."""
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

    # ── 6. Tier 2: KG and GNN embeddings ─────────────────────────────────
    tier2_emb_maps: dict[str, dict] = {}

    if run_tier2:
        print("\n[6/7] Training Tier 2 KG / GNN embeddings …")

        from .gnn_similarity import train_graphsage
        from .kg_embeddings import train_node2vec, train_rdf2vec, train_transe

        n2v_cache    = OUTPUT_DIR / "node2vec_embeddings.pkl"
        transe_cache = OUTPUT_DIR / "transe_embeddings.pkl"
        sage_cache   = OUTPUT_DIR / "graphsage_embeddings.pkl"

        if recompute:
            for _p in (n2v_cache, transe_cache, sage_cache):
                _p.unlink(missing_ok=True)

        print("  → Node2Vec …")
        try:
            node2vec_emb = train_node2vec(cache_path=n2v_cache)
            if node2vec_emb:
                tier2_emb_maps["node2vec"] = node2vec_emb
                print(f"     Node2Vec embeddings: {len(node2vec_emb):,} incidents")
            else:
                print("     Node2Vec returned empty — skipped")
        except ImportError as e:
            print(f"     Node2Vec skipped: {e}")

        print("  → TransE …")
        try:
            transe_emb = train_transe(cache_path=transe_cache)
            if transe_emb:
                tier2_emb_maps["transe"] = transe_emb
                print(f"     TransE embeddings: {len(transe_emb):,} incidents")
            else:
                print("     TransE returned empty — skipped")
        except ImportError as e:
            print(f"     TransE skipped: {e}")

        print("  → RDF2Vec …")
        try:
            rdf2vec_cache = OUTPUT_DIR / "rdf2vec_embeddings.pkl"
            if recompute:
                rdf2vec_cache.unlink(missing_ok=True)
            rdf2vec_emb = train_rdf2vec(cache_path=rdf2vec_cache)
            if rdf2vec_emb:
                tier2_emb_maps["rdf2vec"] = rdf2vec_emb
                print(f"     RDF2Vec embeddings: {len(rdf2vec_emb):,} incidents")
            else:
                print("     RDF2Vec returned empty — skipped")
        except ImportError as e:
            print(f"     RDF2Vec skipped: {e}")

        print("  → GraphSAGE …")
        try:
            graphsage_emb = train_graphsage(cache_path=sage_cache)
            if graphsage_emb:
                tier2_emb_maps["graphsage"] = graphsage_emb
                print(f"     GraphSAGE embeddings: {len(graphsage_emb):,} incidents")
            else:
                print("     GraphSAGE returned empty (quality gate not met) — skipped")
        except ImportError as e:
            print(f"     GraphSAGE skipped: {e}")
    else:
        print("\n[6/7] Tier 2 skipped (pass --tier2 to train KG/GNN embeddings)")

    # ── Load any cached Tier 2 embeddings not trained this run ───────────
    # Ensures the comparison table is always complete even without --tier2,
    # as long as the .pkl files exist from a prior --tier2 run.
    import pickle
    _tier2_caches = {
        "node2vec":  OUTPUT_DIR / "node2vec_embeddings.pkl",
        "transe":    OUTPUT_DIR / "transe_embeddings.pkl",
        "rdf2vec":   OUTPUT_DIR / "rdf2vec_embeddings.pkl",
        "graphsage": OUTPUT_DIR / "graphsage_embeddings.pkl",
    }
    for _method, _cache in _tier2_caches.items():
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
        "--recompute",
        action="store_true",
        help="Ignore cached embeddings and gold IDs; recompute from scratch.",
    )
    parser.add_argument(
        "--gold-ids-file",
        type=Path,
        default=None,
        metavar="FILE",
        help="Path to a JSON file containing a list of gold standard incident IDs.",
    )
    parser.add_argument(
        "--tier2",
        action="store_true",
        help=(
            "Train Tier 2 KG and GNN embeddings (Node2Vec, TransE, RDF2Vec, GraphSAGE). "
            "Requires: pip install torch torch_geometric pykeen gensim"
        ),
    )
    args = parser.parse_args()
    main(recompute=args.recompute, gold_ids_file=args.gold_ids_file, run_tier2=args.tier2)
