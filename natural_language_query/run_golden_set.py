#!/usr/bin/env python3
"""Run the NL translator over every row in ``kg_schema/golden_set.csv``.

Loads the canonical CSV via ``kg_schema.load_golden_set()`` (currently ~258 queries).

Execution policy:
  * ``--backend bedrock`` — loads Parquet from ``pipeline/outputs/`` (or ``--data-dir``)
    and runs ``execute_query`` on each successful translation unless ``--no-execute``.
  * Other backends — translation only unless you pass ``--execute``.

Usage:
    # All CSV rows, Ollama (default)
    python -m natural_language_query.run_golden_set

    # Exclude IOGP-* rows only (~230 queries), legacy subset
    python -m natural_language_query.run_golden_set --skip-iogp

    # First 20 rows only (smoke test)
    python -m natural_language_query.run_golden_set --limit 20

    # Save JSON report
    python -m natural_language_query.run_golden_set -o golden_set_results.json

    # Amazon Bedrock + run each translated query on the KG (default for --backend bedrock)
    python -m natural_language_query.run_golden_set --backend bedrock --temperature 0 -o results.json

    # Bedrock, translation only (no graph load / execute_query)
    python -m natural_language_query.run_golden_set --backend bedrock --no-execute -o results.json

    # Other backends: opt in to execution with --execute
    python -m natural_language_query.run_golden_set --execute -o results.json

    # Override parquet location (defaults to pipeline/outputs/)
    python -m natural_language_query.run_golden_set --backend bedrock --data-dir path/to/outputs

    # Same -o path each run overwrites the file; add timestamp to the filename instead
    python -m natural_language_query.run_golden_set --backend bedrock -o bedrock_nlq.json --timestamp-output
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

from kg_schema import GOLDEN_SET_CSV, load_golden_set
from .translator import translate


def iter_golden_queries(
    *,
    skip_iogp: bool = False,
    offset: int = 0,
    limit: int | None = None,
) -> list[tuple[str, str, str]]:
    """Rows from ``kg_schema/golden_set.csv`` as (query_id, natural_language, query_type).

    ``skip_iogp``: when True, drop ``query_id`` values starting with ``IOGP-`` (~28 rows).
    ``offset`` / ``limit``: slice the list after filtering (for chunked or smoke runs).
    """
    rows = load_golden_set()
    out: list[tuple[str, str, str]] = []
    for row in rows:
        qid = row["query_id"]
        if skip_iogp and qid.startswith("IOGP-"):
            continue
        out.append((qid, row["name"], row["query_type"]))
    if offset:
        out = out[offset:]
    if limit is not None:
        out = out[:limit]
    return out


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
    skip_iogp: bool = False,
    offset: int = 0,
    limit: int | None = None,
    temperature: float = 0.1,
    data_dir: Path | str | None = None,
):
    """Run translator on golden set rows. Optionally execute against graph."""
    queries = iter_golden_queries(
        skip_iogp=skip_iogp, offset=offset, limit=limit,
    )
    results = []
    graph_data = None
    if execute:
        from query_engine import (
            CUSTOM_REGISTRY,
            QuerySpec,
            execute_query,
            load_data,
        )
        try:
            graph_data = load_data(data_dir)
        except Exception as e:
            if verbose:
                print(
                    f"ERROR: graph execution requested but data could not be loaded: {e}",
                    file=sys.stderr,
                )
            raise RuntimeError(
                "Execution requires entities.parquet, relations.parquet, and "
                "metadata_parsed.parquet (default: pipeline/outputs/). "
                "Build the pipeline first or pass --data-dir."
            ) from e

    for query_id, query_text, family in queries:
        if verbose:
            print(f"  {query_id} ({family}) ... ", end="", flush=True)
        r = translate(
            query_text,
            backend=backend,
            model=model,
            base_url=base_url,
            query_id=query_id,
            temperature=temperature,
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
                exec_out = execute_query(
                    spec,
                    G,
                    entities_df,
                    relations_df,
                    metadata_df,
                    custom_registry=CUSTOM_REGISTRY,
                )
                entry["execution"] = {
                    "coverage": exec_out.get("coverage"),
                    "diagnosis": exec_out.get("diagnosis"),
                    "validation": exec_out.get("validation"),
                    "result_summary": exec_out.get("result_summary"),
                    "detail": exec_out.get("detail"),
                    "elapsed": exec_out.get("elapsed"),
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
    print("\nBy family (query_type from CSV):")
    for fam in sorted(by_family.keys()):
        info = by_family[fam]
        print(f"  {fam}: {info['pass']}/{info['total']}")

    ran = [r for r in results if "execution" in r]
    if ran:
        errs = sum(1 for r in ran if "error" in r.get("execution", {}))
        ok = len(ran) - errs
        print("\nGraph execution (translated queries only)")
        print(f"  Ran:   {len(ran)}")
        print(f"  Ok:    {ok}")
        print(f"  Errors: {errs}")


def main():
    parser = argparse.ArgumentParser(
        description="Run NL translator on every row in kg_schema/golden_set.csv",
    )
    parser.add_argument(
        "--backend",
        default="ollama",
        choices=["ollama", "anthropic", "gemini", "bedrock"],
    )
    parser.add_argument("--model", default=None, help="Model name (default per backend)")
    parser.add_argument("--base-url", default="http://localhost:11434", help="Ollama server URL")
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.1,
        help="LLM temperature (use 0 with Bedrock for reproducibility)",
    )
    parser.add_argument(
        "--skip-iogp",
        action="store_true",
        help="Exclude query_id prefixes IOGP- (~28 rows); default is all CSV rows",
    )
    parser.add_argument(
        "--offset",
        type=int,
        default=0,
        help="Skip this many rows after filtering (chunked runs)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Process at most this many rows after offset (smoke / partial run)",
    )
    parser.add_argument(
        "-o",
        "--output",
        default=None,
        help="Write results JSON to this path (overwrites if the file exists)",
    )
    parser.add_argument(
        "--timestamp-output",
        action="store_true",
        help="With -o, write to a new file each run: <name>_<YYYYMMDD_HHMMSS>.<ext> "
        "so prior results are kept",
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Execute each translated query against the KG (parquet → NetworkX)",
    )
    parser.add_argument(
        "--no-execute",
        action="store_true",
        help="Skip graph execution (Bedrock default is to execute; use this for translation-only)",
    )
    parser.add_argument(
        "--data-dir",
        default=None,
        help="Directory with entities.parquet, relations.parquet, metadata_parsed.parquet "
        "(default: pipeline/outputs/)",
    )
    parser.add_argument("-q", "--quiet", action="store_true", help="Less console output")
    args = parser.parse_args()

    if args.backend == "bedrock":
        execute = not args.no_execute
    else:
        execute = args.execute
    if args.no_execute and args.execute:
        print(
            "Note: --no-execute takes precedence over --execute.",
            file=sys.stderr,
        )
        execute = False

    preview = iter_golden_queries(
        skip_iogp=args.skip_iogp, offset=args.offset, limit=args.limit,
    )
    print(f"Backend: {args.backend}  Model: {args.model or '(default)'}  Temp: {args.temperature}")
    print(f"CSV:     {GOLDEN_SET_CSV}")
    if args.skip_iogp:
        print("Filter:  excluding IOGP-*")
    if args.offset or args.limit is not None:
        print(f"Slice:   offset={args.offset} limit={args.limit!r}")
    if execute:
        dd = args.data_dir or "pipeline/outputs/ (default)"
        print(f"Execute: yes — Parquet → NetworkX from {dd}")
    else:
        print("Execute: no (translation / QuerySpec only)")
    print(f"Running {len(preview)} golden set queries...\n")
    try:
        results = run_golden_set(
            backend=args.backend,
            model=args.model,
            base_url=args.base_url,
            execute=execute,
            verbose=not args.quiet,
            skip_iogp=args.skip_iogp,
            offset=args.offset,
            limit=args.limit,
            temperature=args.temperature,
            data_dir=args.data_dir,
        )
    except RuntimeError as e:
        print(str(e), file=sys.stderr)
        return 1
    print_summary(results)
    if args.output:
        out_path = Path(args.output)
        if args.timestamp_output:
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            out_path = out_path.with_name(
                f"{out_path.stem}_{ts}{out_path.suffix or '.json'}"
            )
        payload = {
            "meta": {
                "golden_set_csv": str(GOLDEN_SET_CSV),
                "row_count": len(results),
                "skip_iogp": args.skip_iogp,
                "offset": args.offset,
                "limit": args.limit,
                "backend": args.backend,
                "model": args.model,
                "temperature": args.temperature,
                "execute": execute,
                "data_dir": args.data_dir,
                "output_path": str(out_path.resolve()),
                "timestamp_output": args.timestamp_output,
            },
            "queries": results,
        }
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
        print(f"\nResults written to {out_path.resolve()}")
    return 0 if all(r["success"] for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())
