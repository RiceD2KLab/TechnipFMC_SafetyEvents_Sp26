#!/usr/bin/env python3
"""Benchmark Query Runner — CSV-driven.

Runs 258 benchmark queries against the safety knowledge graph.
Query definitions live in kg_schema/golden_set.csv; custom query logic
lives in custom_queries.py.

Output: pipeline/benchmark/benchmark_results.md

Usage:
    python -m pipeline.benchmark.run_benchmark
    python -m pipeline.benchmark.run_benchmark --data-dir pipeline/outputs/benchmark_large --report-path pipeline/benchmark/benchmark_large_results.md
"""

import argparse
from pathlib import Path

from kg_schema import GOLDEN_SET_CSV
from query_engine import load_data, load_queries, run_all_queries, CUSTOM_REGISTRY
from .report import generate_report

BASE = Path(__file__).resolve().parent
CSV_PATH = GOLDEN_SET_CSV
REPORT_PATH = BASE / "benchmark_results.md"


def main():
    parser = argparse.ArgumentParser(description="Benchmark Runner")
    parser.add_argument("--data-dir", type=str, default=None,
                        help="Directory with entities/relations/metadata parquets")
    parser.add_argument("--report-path", type=str, default=None,
                        help="Output report path (default: pipeline/benchmark/benchmark_results.md)")
    args = parser.parse_args()

    data_dir = args.data_dir
    report_path = Path(args.report_path) if args.report_path else REPORT_PATH

    G, entities_df, relations_df, metadata_df = load_data(data_dir=data_dir)

    print(f"\nLoading queries from {CSV_PATH.name}...")
    specs = load_queries(CSV_PATH)
    print(f"  {len(specs)} queries loaded")

    print("\nRunning benchmark queries...")
    results = run_all_queries(
        specs, G, entities_df, relations_df, metadata_df,
        custom_registry=CUSTOM_REGISTRY)

    print("\n\nGenerating benchmark_results.md...")
    generate_report(results, G, entities_df, metadata_df, report_path, relations_df=relations_df)
    print("Done.")


if __name__ == "__main__":
    main()
