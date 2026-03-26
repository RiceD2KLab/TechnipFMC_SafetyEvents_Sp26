#!/usr/bin/env python3
"""GLiNER Knowledge Graph Pipeline (v2 Schema).

Extracts entities via GLiNER, parses metadata, assembles a property graph,
and runs Gate 1 topology evaluation.

Usage:
    python pipeline/run_gliner_pipeline.py --test                    # First 1000 records (~5 min)
    python pipeline/run_gliner_pipeline.py --full                    # Full dataset (~90 min)
    python pipeline/run_gliner_pipeline.py --full --skip-gliner      # Skip GLiNER, use existing output
    python pipeline/run_gliner_pipeline.py --test --data-path /path  # Custom dataset path
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

# Ensure project root is on the path for imports
PROJECT_ROOT = Path(__file__).resolve().parent.parent
PIPELINE_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PIPELINE_ROOT))
sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd

DEFAULT_DATA_PATH = PROJECT_ROOT / "graphRAG" / "input" / "dev_sample.csv"
OUTPUTS_DIR = PIPELINE_ROOT / "outputs"


def main() -> None:
    parser = argparse.ArgumentParser(description="V2 Schema Pipeline")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--test", action="store_true", help="Run on first 1000 records (~5 min)")
    mode.add_argument("--full", action="store_true", help="Run on full dataset (~90 min)")
    parser.add_argument("--skip-gliner", action="store_true",
                        help="Skip GLiNER extraction, use existing output")
    parser.add_argument("--data-path", type=str, default=None,
                        help=f"Path to dataset CSV (default: {DEFAULT_DATA_PATH})")
    parser.add_argument("--threshold", type=float, default=0.5,
                        help="GLiNER confidence threshold (default: 0.5)")
    args = parser.parse_args()

    data_path = Path(args.data_path) if args.data_path else DEFAULT_DATA_PATH
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

    gliner_output = OUTPUTS_DIR / "gliner_extractions.parquet"
    metadata_output = OUTPUTS_DIR / "metadata_parsed.parquet"
    nodes_output = OUTPUTS_DIR / "entities.parquet"
    edges_output = OUTPUTS_DIR / "relations.parquet"
    report_output = OUTPUTS_DIR / "metrics_report.md"

    t_start = time.time()

    # ── Load data ─────────────────────────────────────────────────────────
    print(f"Loading dataset from {data_path}")
    df = pd.read_csv(data_path)
    total_records = len(df)
    if args.test:
        df = df.head(1000)
        print(f"TEST MODE: Using first 1,000 of {total_records:,} records")
    else:
        print(f"FULL MODE: Using all {len(df):,} records")

    # ── Step 0: Data Quality Pre-Filter ────────────────────────────────────
    # GLiNER extraction is expensive (~278ms/record). Pre-filter records that
    # will produce garbage output to avoid wasting cycles and polluting the
    # graph with low-quality entities. Metadata parsing still runs on ALL
    # records so every incident gets a node regardless of narrative quality.
    #
    # Filtered: ~88 Norwegian + ~109 other non-English narratives (0.8% of
    # data) that produce garbage GLiNER output (e.g. "pallen" → BODY_PART).
    # Also filters records with no NARRATIVE: section (empty text).
    print("\n" + "=" * 60)
    print("Step 0: Data Quality Pre-Filter")
    print("=" * 60)

    from extraction.gliner_extract import parse_narrative

    def _is_english(text: str, threshold: float = 0.30) -> bool:
        """Fast ASCII-ratio heuristic for English detection."""
        if not text:
            return False
        ascii_chars = sum(1 for c in text if ord(c) < 128)
        return (ascii_chars / len(text)) >= threshold

    df_all = df  # Keep full dataset for metadata parsing
    pre_filter_count = len(df)
    empty_narrative = 0
    non_english = 0
    gliner_mask = []
    for _, row in df.iterrows():
        narrative = parse_narrative(str(row.get("text", "")))
        if not narrative:
            gliner_mask.append(False)
            empty_narrative += 1
        elif not _is_english(narrative):
            gliner_mask.append(False)
            non_english += 1
        else:
            gliner_mask.append(True)

    df_for_gliner = df[gliner_mask].copy()
    filtered_count = pre_filter_count - len(df_for_gliner)
    print(f"  Total records: {pre_filter_count:,}")
    print(f"  Empty narratives: {empty_narrative:,}")
    print(f"  Non-English narratives: {non_english:,}")
    print(f"  Records for GLiNER: {len(df_for_gliner):,} ({filtered_count:,} filtered)")

    # ── Step 1: GLiNER Entity Extraction ──────────────────────────────────
    if not args.skip_gliner:
        print("\n" + "=" * 60)
        print("Step 1: GLiNER Entity Extraction")
        print("=" * 60)
        t0 = time.time()

        from extraction.gliner_extract import run_gliner_extraction
        gliner_df = run_gliner_extraction(df_for_gliner, gliner_output, threshold=args.threshold)

        t1 = time.time()
        print(f"  Time: {t1 - t0:.1f}s ({(t1 - t0) / 60:.1f} min)")
    else:
        print("\n[Skipping GLiNER extraction — loading existing output]")
        if not gliner_output.exists():
            print(f"ERROR: {gliner_output} not found. Run without --skip-gliner first.")
            sys.exit(1)
        gliner_df = pd.read_parquet(gliner_output)
        print(f"  Loaded {len(gliner_df):,} entities from {gliner_output}")

    # ── Step 2: Metadata Parsing ──────────────────────────────────────────
    print("\n" + "=" * 60)
    print("Step 2: Metadata Parsing")
    print("=" * 60)
    t0 = time.time()

    from extraction.metadata_parse import run_metadata_parsing
    metadata_df = run_metadata_parsing(df_all, metadata_output)

    t1 = time.time()
    print(f"  Time: {t1 - t0:.1f}s")

    # ── Step 3: Graph Assembly ────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("Step 3: Graph Assembly")
    print("=" * 60)
    t0 = time.time()

    from assembly.graph_builder import build_graph
    nodes_df, edges_df = build_graph(gliner_df, metadata_df)

    nodes_df.to_parquet(nodes_output, index=False)
    edges_df.to_parquet(edges_output, index=False)

    t1 = time.time()
    print(f"  Graph assembled: {len(nodes_df):,} nodes, {len(edges_df):,} edges")
    print(f"  Time: {t1 - t0:.1f}s")

    # ── Step 4: Gate 1 Evaluation ─────────────────────────────────────────
    print("\n" + "=" * 60)
    print("Step 4: Gate 1 Evaluation")
    print("=" * 60)
    t0 = time.time()

    from evaluation.topology_metrics import compute_gate1_metrics, generate_report
    metrics = compute_gate1_metrics(nodes_df, edges_df)
    generate_report(metrics, report_output)

    t1 = time.time()
    gate_status = "PASS" if metrics["gate1_pass"] else "FAIL"
    print(f"  Gate 1: {gate_status}")
    print(f"    Giant component: {metrics['giant_component_ratio']}")
    print(f"    Mean degree:     {metrics['mean_degree']}")
    print(f"    Schema violations: {metrics['schema_violations']}")
    print(f"  Time: {t1 - t0:.1f}s")

    # ── Summary ───────────────────────────────────────────────────────────
    t_total = time.time() - t_start
    print("\n" + "=" * 60)
    print("Pipeline Complete")
    print("=" * 60)
    print(f"  Total time: {t_total:.1f}s ({t_total / 60:.1f} min)")
    print(f"  Nodes: {len(nodes_df):,}")
    print(f"  Edges: {len(edges_df):,}")
    print(f"  Gate 1: {gate_status}")
    print(f"\n  Outputs saved to: {OUTPUTS_DIR}/")
    print(f"    - entities.parquet")
    print(f"    - relations.parquet")
    print(f"    - metrics_report.md")
    if not args.skip_gliner:
        print(f"    - gliner_extractions.parquet")
    print(f"    - metadata_parsed.parquet")


if __name__ == "__main__":
    main()
