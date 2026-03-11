"""Orchestrator for the Section 4.3 Event Similarity pipeline.

Executes the full Tier 1 evaluation workflow:
  1. Load incident narratives from pipeline_v2/outputs/metadata_parsed.parquet.
  2. Load post-ER entity sets from pipeline_v2/er_execution/outputs/.
  3. Select (or load) the 30 Gold Standard incident IDs.
  4. Compute sentence-transformer text embeddings (cached to outputs/).
  5. Run Tier 1 evaluation for both weight configurations:
       - domain_informed (EQUIPMENT=0.25, INJURY_TYPE=0.25, …)
       - uniform (all entity types weighted equally — ablation)

Usage:
    python -m event_similarity.run_similarity
    python -m event_similarity.run_similarity --recompute
    python -m event_similarity.run_similarity --gold-ids-file path/to/ids.json

Outputs (all written to event_similarity/outputs/):
    gold_standard_ids.json          Selected gold standard incident IDs
    text_embeddings.pkl             Cached sentence-transformer embeddings
    tier1_eval_domain_informed.json Per-query results + aggregate metrics
    tier1_eval_uniform.json         Ablation run with uniform weights
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

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
            "  → run:  python -m pipeline_v2.run_gliner_pipeline"
        )
    if not RELATIONS_PATH.exists():
        missing.append(
            f"  {RELATIONS_PATH}\n"
            "  → run:  python -m pipeline_v2.er_execution.run_er_execution"
        )
    if missing:
        raise FileNotFoundError(
            "Required input files not found:\n" + "\n".join(missing)
        )


def main(
    recompute: bool = False,
    gold_ids_file: Path | None = None,
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
    args = parser.parse_args()
    main(recompute=args.recompute, gold_ids_file=args.gold_ids_file)
