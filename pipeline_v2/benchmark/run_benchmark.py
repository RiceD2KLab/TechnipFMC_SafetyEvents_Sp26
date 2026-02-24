#!/usr/bin/env python3
"""Benchmark Query Runner — CSV-driven

Runs 30 benchmark queries against the v2 safety knowledge graph.
Query definitions live in benchmark_queries.csv; custom query logic
lives in custom_queries.py.

Output: pipeline_v2/benchmark/benchmark_results.md

Usage:
    cd pipeline_v2
    python -m benchmark.run_benchmark
"""

from pathlib import Path

from .helpers import load_data
from .query_engine import load_queries, run_all_queries
from .custom_queries import CUSTOM_REGISTRY
from .report import generate_report

BASE = Path(__file__).resolve().parent
CSV_PATH = BASE / "benchmark_queries.csv"
REPORT_PATH = BASE / "benchmark_results.md"


def main():
    G, entities_df, relations_df, metadata_df = load_data()

    print(f"\nLoading queries from {CSV_PATH.name}...")
    specs = load_queries(CSV_PATH)
    print(f"  {len(specs)} queries loaded")

    print("\nRunning benchmark queries...")
    results = run_all_queries(
        specs, G, entities_df, relations_df, metadata_df,
        custom_registry=CUSTOM_REGISTRY)

    print("\n\nGenerating benchmark_results.md...")
    generate_report(results, G, entities_df, metadata_df, REPORT_PATH)
    print("Done.")


if __name__ == "__main__":
    main()
