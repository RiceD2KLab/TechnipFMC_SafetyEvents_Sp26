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

DEFAULT_DATA_PATH = PROJECT_ROOT / "input" / "incidents.csv"
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
    parser.add_argument("--threshold", type=float, default=0.40,
                        help="GLiNER confidence threshold (default: 0.40)")
    parser.add_argument("--model-name", type=str, default="urchade/gliner_large-v2.1",
                        help="HuggingFace GLiNER model (default: urchade/gliner_large-v2.1)")
    parser.add_argument("--output-dir", type=str, default=None,
                        help="Output directory (default: pipeline/outputs/)")
    args = parser.parse_args()

    data_path = Path(args.data_path) if args.data_path else DEFAULT_DATA_PATH
    output_dir = Path(args.output_dir) if args.output_dir else OUTPUTS_DIR
    output_dir.mkdir(parents=True, exist_ok=True)

    gliner_output = output_dir / "gliner_extractions.parquet"
    metadata_output = output_dir / "metadata_parsed.parquet"
    nodes_output = output_dir / "entities.parquet"
    edges_output = output_dir / "relations.parquet"
    report_output = output_dir / "metrics_report.md"

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
    from langdetect import detect, DetectorFactory, LangDetectException
    DetectorFactory.seed = 42  # deterministic detection

    def _detect_lang(text: str) -> str:
        """Detect language of narrative.  Returns ISO code or 'err'."""
        if not text or len(text.strip()) < 20:
            return "err"
        # Use first 600 chars — fast and reliable
        try:
            return detect(text[:600])
        except LangDetectException:
            return "err"

    def _split_bilingual(text: str) -> str:
        """If a narrative is bilingual (non-English followed by English
        translation), return just the English portion.

        Strategy:
          1. Check the LAST 500 chars are English.  If not, no recovery.
          2. Walk backward through sentences.  Detect language ON EACH
             SENTENCE INDIVIDUALLY (sentences < 30 chars are skipped as
             unreliable).  Stop at the first sentence that's clearly
             non-English; everything from the next sentence onward is the
             English portion.
          3. Require ≥300 chars of recovered English to be useful.
        """
        import re as _re
        if len(text) < 500:
            return ""
        try:
            if detect(text[-500:]) != "en":
                return ""
        except LangDetectException:
            return ""

        sentences = _re.split(r'(?<=[.!?])\s+', text.strip())
        if len(sentences) < 2:
            return ""

        # Walk backward; find the boundary where language switches.
        # `english_start_idx` = first index whose sentence is English (or
        # short/ambiguous and surrounded by English).
        english_start_idx = len(sentences)  # exclusive end
        for i in range(len(sentences) - 1, -1, -1):
            sent = sentences[i].strip()
            if len(sent) < 30:
                # Too short to detect reliably — defer judgement, keep walking
                english_start_idx = i
                continue
            try:
                lang = detect(sent)
            except LangDetectException:
                english_start_idx = i
                continue
            if lang == "en":
                english_start_idx = i
            else:
                # Hit a non-English sentence — stop here
                break

        recovered = " ".join(sentences[english_start_idx:]).strip()
        if len(recovered) < 300:
            return ""
        # Final validation on the recovered portion
        try:
            if detect(recovered[:600]) == "en":
                return recovered
        except LangDetectException:
            pass
        return ""

    df_all = df  # Keep full dataset for metadata parsing
    pre_filter_count = len(df)
    empty_narrative = 0
    non_english = 0
    bilingual_recovered = 0
    gliner_mask = []
    narratives_for_gliner: dict[int, str] = {}  # row index -> narrative text
    for idx, row in df.iterrows():
        narrative = parse_narrative(str(row.get("text", "")))
        if not narrative:
            gliner_mask.append(False)
            empty_narrative += 1
            continue
        lang = _detect_lang(narrative)
        if lang == "en":
            gliner_mask.append(True)
            narratives_for_gliner[idx] = narrative
        else:
            # Try to recover an English portion from bilingual narratives
            english_part = _split_bilingual(narrative)
            if english_part and len(english_part) >= 50:
                gliner_mask.append(True)
                narratives_for_gliner[idx] = english_part
                bilingual_recovered += 1
            else:
                gliner_mask.append(False)
                non_english += 1

    df_for_gliner = df[gliner_mask].copy()
    # Replace narrative text in df_for_gliner with the cleaned English-only version
    # so downstream extraction sees only English
    if bilingual_recovered > 0:
        # Rebuild text column wrapped in NARRATIVE: marker so parse_narrative still works
        new_texts = []
        for idx, row in df_for_gliner.iterrows():
            cleaned = narratives_for_gliner.get(idx, "")
            new_texts.append(f"NARRATIVE: {cleaned}")
        df_for_gliner = df_for_gliner.copy()
        df_for_gliner["text"] = new_texts

    filtered_count = pre_filter_count - len(df_for_gliner)
    print(f"  Total records: {pre_filter_count:,}")
    print(f"  Empty narratives: {empty_narrative:,}")
    print(f"  Non-English narratives: {non_english:,}")
    print(f"  Bilingual recovered (English portion only): {bilingual_recovered:,}")
    print(f"  Records for GLiNER: {len(df_for_gliner):,} ({filtered_count:,} filtered)")

    # ── Step 1: GLiNER Entity Extraction ──────────────────────────────────
    if not args.skip_gliner:
        print("\n" + "=" * 60)
        print("Step 1: GLiNER Entity Extraction")
        print("=" * 60)
        t0 = time.time()

        from extraction.gliner_extract import run_gliner_extraction
        gliner_df = run_gliner_extraction(df_for_gliner, gliner_output, threshold=args.threshold, model_name=args.model_name)

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
    print(f"\n  Outputs saved to: {output_dir}/")
    print(f"    - entities.parquet")
    print(f"    - relations.parquet")
    print(f"    - metrics_report.md")
    if not args.skip_gliner:
        print(f"    - gliner_extractions.parquet")
    print(f"    - metadata_parsed.parquet")


if __name__ == "__main__":
    main()
