#!/usr/bin/env python3
"""Benchmark Query Runner — CSV-driven

Runs 258 benchmark queries against the safety knowledge graph.
Query definitions live in kg_schema/golden_set.csv; custom query logic
lives in custom_queries.py.

Output: pipeline/benchmark/benchmark_results.md

Usage:
    cd pipeline
    python -m benchmark.run_benchmark
"""

from pathlib import Path

from kg_schema import GOLDEN_SET_CSV
from .helpers import load_data
from .query_engine import load_queries, run_all_queries
from .custom_queries import CUSTOM_REGISTRY
from .report import generate_report

BASE = Path(__file__).resolve().parent
CSV_PATH = GOLDEN_SET_CSV
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
    generate_report(results, G, entities_df, metadata_df, REPORT_PATH, relations_df=relations_df)
    print("Done.")


if __name__ == "__main__":
    main()
