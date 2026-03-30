#!/usr/bin/env python3
"""Run the NL translator over the golden set of dashboard queries.

Tests translation quality (NL -> QuerySpec) for all 44 golden set questions
without requiring graph execution. Optionally runs execute_query when
pipeline data is available.

Usage:
    # Translation only (default), Ollama
    python -m natural_language_query.run_golden_set

    # Save JSON report
    python -m natural_language_query.run_golden_set -o golden_set_results.json

    # Faster on CPU: use a smaller model (~30–60s per query vs 2–3 min for qwen3:8b)
    python -m natural_language_query.run_golden_set --model qwen2.5:3b -o results.json

    # Fastest: use a cloud API (seconds per query)
    python -m natural_language_query.run_golden_set --backend anthropic -o results.json

    # Run queries against the graph (requires pipeline/outputs data)
    python -m natural_language_query.run_golden_set --execute -o results.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from kg_schema import load_golden_set
from .translator import translate


# NLQ currently supports the original 44 queries (excludes IOGP-*).
# TODO: remove this filter once NLQ covers all 52 golden set queries.
_NLQ_EXCLUDE_PREFIXES = ("IOGP-",)


def _load_golden_set():
    """Load golden set from canonical CSV as list of (query_id, name, query_type) tuples."""
    return [
        (row["query_id"], row["name"], row["query_type"])
        for row in load_golden_set()
        if not row["query_id"].startswith(_NLQ_EXCLUDE_PREFIXES)
    ]


GOLDEN_SET = _load_golden_set()


def _serialize_spec(spec_dict):
    """Make QuerySpec dict JSON-serializable (sets -> lists)."""
    if spec_dict is None:
        return None
    out = {}
    for k, v in spec_dict.items():
        if isinstance(v, set):
            out[k] = list(v)
        else:
            out[k] = v
    return out


def run_golden_set(
    backend: str = "ollama",
    model: str | None = None,
    base_url: str = "http://localhost:11434",
    execute: bool = False,
    verbose: bool = True,
):
    """Run translator on every golden set query. Optionally execute against graph."""
    results = []
    graph_data = None
    if execute:
        try:
            from query_engine import load_data, QuerySpec, execute_query
            graph_data = load_data()
        except Exception as e:
            if verbose:
                print(f"Warning: could not load graph data for execution: {e}", file=sys.stderr)
            execute = False

    for query_id, query_text, family in GOLDEN_SET:
        if verbose:
            print(f"  {query_id} ({family}) ... ", end="", flush=True)
        r = translate(
            query_text,
            backend=backend,
            model=model,
            base_url=base_url,
            query_id=query_id,
        )
        success = r["query_spec"] is not None
        entry = {
            "query_id": query_id,
            "family": family,
            "query": query_text,
            "success": success,
            "strategy": r["query_spec"].get("strategy") if success else None,
            "output_mode": r["query_spec"].get("output_mode") if success else None,
            "confidence": r.get("confidence", 0),
            "latency_ms": r.get("latency_ms", 0),
            "clarification": r.get("clarification"),
            "query_spec": _serialize_spec(r["query_spec"]),
        }
        if execute and success and graph_data:
            try:
                G, entities_df, relations_df, metadata_df = graph_data
                spec = QuerySpec(**r["query_spec"])
                exec_out = execute_query(spec, G, entities_df, relations_df, metadata_df)
                entry["execution"] = {
                    "coverage": exec_out.get("coverage"),
                    "result_summary": exec_out.get("result_summary"),
                    "detail": exec_out.get("detail"),
                }
            except Exception as e:
                entry["execution"] = {"error": str(e)}
        results.append(entry)
        if verbose:
            status = "OK" if success else "FAIL"
            print(f"{status} ({r.get('latency_ms', 0):.0f}ms)")

    return results


def print_summary(results: list) -> None:
    """Print a short summary table to stdout."""
    n = len(results)
    passed = sum(1 for r in results if r["success"])
    total_ms = sum(r["latency_ms"] for r in results)
    print("\n" + "=" * 60)
    print("Golden Set NLQ Summary")
    print("=" * 60)
    print(f"  Total:    {n}")
    print(f"  Pass:     {passed} ({100 * passed / n:.1f}%)")
    print(f"  Fail:     {n - passed}")
    print(f"  Latency:  {total_ms / 1000:.1f}s total, {total_ms / n / 1000:.1f}s avg per query")
    print("=" * 60)
    by_family = {}
    for r in results:
        f = r["family"]
        if f not in by_family:
            by_family[f] = {"pass": 0, "total": 0}
        by_family[f]["total"] += 1
        if r["success"]:
            by_family[f]["pass"] += 1
    print("\nBy family:")
    for fam in ("Single-Hop", "Spot-check", "Aggregation", "Multi-Hop", "Global", "Conjunctive"):
        if fam in by_family:
            info = by_family[fam]
            print(f"  {fam}: {info['pass']}/{info['total']}")


def main():
    parser = argparse.ArgumentParser(
        description="Run NL translator on the golden set of dashboard queries",
    )
    parser.add_argument("--backend", default="ollama", choices=["ollama", "anthropic", "gemini"])
    parser.add_argument("--model", default=None, help="Model name (default per backend)")
    parser.add_argument("--base-url", default="http://localhost:11434", help="Ollama server URL")
    parser.add_argument("-o", "--output", default=None, help="Write results JSON to this path")
    parser.add_argument("--execute", action="store_true", help="Execute each query against pipeline graph (if data available)")
    parser.add_argument("-q", "--quiet", action="store_true", help="Less console output")
    args = parser.parse_args()

    print(f"Backend: {args.backend}  Model: {args.model or '(default)'}")
    if args.execute:
        print("Execute: yes (will run against graph when translation succeeds)")
    print(f"Running {len(GOLDEN_SET)} golden set queries...\n")
    results = run_golden_set(
        backend=args.backend,
        model=args.model,
        base_url=args.base_url,
        execute=args.execute,
        verbose=not args.quiet,
    )
    print_summary(results)
    if args.output:
        out_path = Path(args.output)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump({"queries": results}, f, indent=2)
        print(f"\nResults written to {out_path}")
    return 0 if all(r["success"] for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())
