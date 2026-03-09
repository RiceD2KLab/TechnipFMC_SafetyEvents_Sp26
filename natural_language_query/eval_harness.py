#!/usr/bin/env python3
"""Evaluation harness for NL → QuerySpec translation.

Loads benchmark queries from CSV as ground truth, runs NL paraphrases
through the translator, and scores field-level accuracy.

Usage:
    # Test against local Ollama (default)
    python -m natural_language_query.eval_harness

    # Test against Anthropic API
    python -m natural_language_query.eval_harness --backend anthropic --model claude-sonnet-4-5-20250514

    # Test against Gemini API
    python -m natural_language_query.eval_harness --backend gemini --model gemini-2.5-flash

    # Test a single query interactively
    python -m natural_language_query.eval_harness --interactive

    # Use custom paraphrases file
    python -m natural_language_query.eval_harness --paraphrases path/to/paraphrases.json
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from collections import defaultdict
from pathlib import Path

from .translator import translate
from .paraphrases import PARAPHRASES


# ── Ground truth from benchmark CSV ──────────────────────────────────────

# These are the expected translations for non-spot-check, non-custom queries.
# Each maps query_id → the key fields we check.
# Derived directly from benchmark_queries.csv.

GROUND_TRUTH = {
    "SH-01": {
        "strategy": "intersect",
        "has_entity_filter": True,
        "entity_types": ["EQUIPMENT"],
        "entity_pattern_must_match": "forklift",
        "has_meta_filter": True,
        "meta_fields": ["year"],
        "output_mode": "count_incidents",
    },
    "SH-03": {
        "strategy": "entity_filter",
        "has_entity_filter": True,
        "entity_types": ["EQUIPMENT"],
        "entity_pattern_must_match": "crane",
        "has_meta_filter": False,
        "output_mode": "aggregate",
        "agg_entity_type": "BODY_PART",
    },
    "SH-04": {
        "strategy": "entity_filter",
        "has_entity_filter": True,
        "entity_types": ["EQUIPMENT"],
        "entity_pattern_must_match": "valve",
        "has_meta_filter": False,
        "output_mode": "aggregate",
        "agg_entity_type": "LOCATION",
    },
    "SH-05": {
        "strategy": "meta_filter",
        "has_entity_filter": False,
        "has_meta_filter": True,
        "meta_fields": ["work_process"],
        "output_mode": "aggregate",
        "agg_entity_type": "INJURY_TYPE",
    },
    "SH-06": {
        "strategy": "entity_filter",
        "has_entity_filter": True,
        "entity_types": ["ORGANIZATION"],
        "entity_pattern_must_match": "shell",
        "has_meta_filter": False,
        "output_mode": "count_incidents",
    },
    "AG-01": {
        "strategy": "narrative_filter",
        "has_entity_filter": False,
        "has_meta_filter": False,
        "has_narrative": True,
        "narrative_must_contain": "dropped",
        "output_mode": "aggregate",
        "agg_entity_type": "ROOT_CAUSE_CATEGORY",
    },
    "AG-02": {
        "strategy": "meta_filter",
        "has_entity_filter": False,
        "has_meta_filter": True,
        "meta_fields": ["severity_bin"],
        "output_mode": "aggregate",
        "agg_entity_type": "LOCATION",
    },
    "AG-03": {
        "strategy": "entity_filter",
        "has_entity_filter": False,
        "has_meta_filter": False,
        "output_mode": "aggregate",
        "agg_entity_type": "EQUIPMENT",
    },
    "AG-05": {
        "strategy": "narrative_filter",
        "has_narrative": True,
        "narrative_must_contain": "fall",
        "output_mode": "count_by_year",
    },
    "AG-06": {
        "strategy": "crosstab",
        "output_mode": "crosstab",
    },
    "MH-02": {
        "strategy": "intersect",
        "has_narrative": True,
        "narrative_must_contain": "maintenance",
        "output_mode": "aggregate",
        "agg_entity_type": "INJURY_TYPE",
    },
    "MH-05": {
        "strategy": "intersect",
        "has_entity_filter": True,
        "entity_types": ["BODY_PART", "EQUIPMENT"],
        "output_mode": "count_incidents",
    },
    "MH-06": {
        "strategy": "entity_filter",
        "has_entity_filter": True,
        "entity_types": ["EQUIPMENT"],
        "output_mode": "aggregate",
    },
    "CJ-06": {
        "strategy": "intersect",
        "has_narrative": True,
        "output_mode": "count_incidents",
    },
}


# ── Scoring functions ────────────────────────────────────────────────────

def score_query(result: dict, truth: dict) -> dict:
    """Score a single NL translation against ground truth.

    Returns dict of {check_name: bool} for each applicable check.
    """
    scores = {}

    if result["query_spec"] is None:
        # Total failure
        return {"parse_success": False}

    scores["parse_success"] = True
    spec = result["query_spec"]
    nl = result["nl_output"]

    # Strategy check (flexible: intersect is ok if truth says entity_filter
    # with additional filters)
    if "strategy" in truth:
        predicted = spec["strategy"]
        expected = truth["strategy"]
        # Accept intersect when expected is entity/meta/narrative with
        # multiple filter types
        if expected in ("entity_filter", "meta_filter",
                        "narrative_filter"):
            scores["strategy"] = (
                predicted == expected or predicted == "intersect"
            )
        else:
            scores["strategy"] = predicted == expected

    # Entity filter presence
    if "has_entity_filter" in truth:
        has_ef = len(spec["entity_filters"]) > 0
        scores["has_entity_filter"] = has_ef == truth["has_entity_filter"]

    # Entity types used
    if "entity_types" in truth:
        predicted_types = {ef[0] for ef in spec["entity_filters"]}
        expected_types = set(truth["entity_types"])
        scores["entity_types"] = expected_types.issubset(predicted_types)

    # Entity pattern matches expected string
    if "entity_pattern_must_match" in truth:
        target = truth["entity_pattern_must_match"].lower()
        any_match = any(
            target in ef[1].lower()
            for ef in spec["entity_filters"]
        )
        scores["entity_pattern"] = any_match

    # Meta filter presence
    if "has_meta_filter" in truth:
        has_mf = len(spec["meta_filters"]) > 0
        scores["has_meta_filter"] = has_mf == truth["has_meta_filter"]

    # Meta fields used
    if "meta_fields" in truth:
        predicted_fields = {mf[0] for mf in spec["meta_filters"]}
        expected_fields = set(truth["meta_fields"])
        scores["meta_fields"] = expected_fields.issubset(predicted_fields)

    # Narrative presence
    if "has_narrative" in truth:
        has_narr = len(spec["narrative_keywords"]) > 0
        scores["has_narrative"] = has_narr == truth["has_narrative"]

    # Narrative must contain keyword
    if "narrative_must_contain" in truth:
        target = truth["narrative_must_contain"].lower()
        any_match = any(
            target in kw.lower()
            for kw in spec["narrative_keywords"]
        )
        # Also accept if it ended up as an entity filter pattern
        if not any_match:
            any_match = any(
                target in ef[1].lower()
                for ef in spec["entity_filters"]
            )
        scores["narrative_keyword"] = any_match

    # Output mode
    if "output_mode" in truth:
        scores["output_mode"] = spec["output_mode"] == truth["output_mode"]

    # Aggregate target entity type
    if "agg_entity_type" in truth and nl and nl.aggregate_target:
        scores["agg_entity_type"] = (
            nl.aggregate_target.entity_type.value
            == truth["agg_entity_type"]
        )

    return scores


# ── Main evaluation loop ─────────────────────────────────────────────────

def run_evaluation(
    backend: str = "ollama",
    model: str | None = None,
    base_url: str = "http://localhost:11434",
    paraphrases: dict | None = None,
    verbose: bool = True,
) -> dict:
    """Run full evaluation across all ground truth queries.

    Returns summary statistics.
    """
    if paraphrases is None:
        paraphrases = PARAPHRASES

    all_scores = []
    per_query = {}
    total_latency = 0
    total_calls = 0

    for query_id, truth in GROUND_TRUTH.items():
        phrases = paraphrases.get(query_id, [])
        if not phrases:
            if verbose:
                print(f"  SKIP {query_id}: no paraphrases")
            continue

        query_scores = []
        for phrase in phrases:
            result = translate(
                phrase,
                backend=backend,
                model=model,
                base_url=base_url,
                query_id=query_id,
            )

            scores = score_query(result, truth)
            query_scores.append(scores)
            all_scores.append(scores)
            total_latency += result.get("latency_ms", 0)
            total_calls += 1

            if verbose:
                passed = sum(scores.values())
                total = len(scores)
                status = "PASS" if all(scores.values()) else "FAIL"
                print(
                    f"  {query_id} | {status} ({passed}/{total}) "
                    f"| {result.get('latency_ms', 0):.0f}ms "
                    f"| {phrase[:60]}"
                )
                if not all(scores.values()):
                    failures = [k for k, v in scores.items() if not v]
                    print(f"           FAILED: {failures}")

        per_query[query_id] = query_scores

    # ── Aggregate metrics ────────────────────────────────────────────
    if not all_scores:
        return {"error": "No test cases run"}

    # Per-check accuracy
    check_counts = defaultdict(lambda: {"pass": 0, "total": 0})
    for scores in all_scores:
        for check, passed in scores.items():
            check_counts[check]["total"] += 1
            if passed:
                check_counts[check]["pass"] += 1

    check_accuracy = {
        check: counts["pass"] / counts["total"]
        for check, counts in check_counts.items()
    }

    # Overall: all checks pass
    full_pass = sum(
        1 for s in all_scores if all(s.values())
    )
    full_pass_rate = full_pass / len(all_scores)

    # Parse success rate
    parse_success = sum(
        1 for s in all_scores if s.get("parse_success", False)
    )
    parse_rate = parse_success / len(all_scores)

    summary = {
        "total_queries": len(all_scores),
        "full_pass": full_pass,
        "full_pass_rate": full_pass_rate,
        "parse_success_rate": parse_rate,
        "check_accuracy": dict(check_accuracy),
        "avg_latency_ms": total_latency / max(total_calls, 1),
        "per_query": {
            qid: {
                "n_phrases": len(scores_list),
                "full_pass": sum(
                    1 for s in scores_list if all(s.values())
                ),
                "pass_rate": sum(
                    1 for s in scores_list if all(s.values())
                ) / len(scores_list),
            }
            for qid, scores_list in per_query.items()
        },
    }

    return summary


def print_report(summary: dict):
    """Print a formatted evaluation report."""
    print("\n" + "=" * 70)
    print("NL → QuerySpec Evaluation Report")
    print("=" * 70)

    print(f"\nTotal test cases: {summary['total_queries']}")
    print(f"Full pass rate:   {summary['full_pass_rate']:.1%} "
          f"({summary['full_pass']}/{summary['total_queries']})")
    print(f"Parse success:    {summary['parse_success_rate']:.1%}")
    print(f"Avg latency:      {summary['avg_latency_ms']:.0f}ms")

    print("\nPer-check accuracy:")
    for check, acc in sorted(summary["check_accuracy"].items()):
        bar = "█" * int(acc * 20) + "░" * (20 - int(acc * 20))
        print(f"  {check:25s} {bar} {acc:.1%}")

    print("\nPer-query breakdown:")
    for qid, info in sorted(summary["per_query"].items()):
        status = "✅" if info["pass_rate"] == 1.0 else (
            "⚠️" if info["pass_rate"] >= 0.5 else "❌"
        )
        print(
            f"  {qid:8s} {status} {info['full_pass']}/{info['n_phrases']} "
            f"({info['pass_rate']:.0%})"
        )


# ── Interactive mode ─────────────────────────────────────────────────────

def interactive_mode(backend: str, model: str | None, base_url: str):
    """Interactive REPL for testing individual queries."""
    print("NL Query Translator — Interactive Mode")
    print("Type a question, or 'quit' to exit.\n")

    while True:
        try:
            query = input("Query> ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if not query or query.lower() in ("quit", "exit", "q"):
            break

        result = translate(
            query, backend=backend, model=model, base_url=base_url
        )

        if result["query_spec"] is None:
            print(f"\n  FAILED: {result['clarification']}")
            print(f"  Raw: {result['raw_response'][:200]}")
        else:
            spec = result["query_spec"]
            nl = result["nl_output"]
            print(f"\n  Strategy:    {spec['strategy']}")
            print(f"  Entity filt: {spec['entity_filters']}")
            print(f"  Meta filt:   {spec['meta_filters']}")
            print(f"  Narrative:   {spec['narrative_keywords']}")
            print(f"  Output mode: {spec['output_mode']}")
            print(f"  Output tgt:  {spec['output_target']}")
            print(f"  Confidence:  {nl.confidence}")
            if nl.clarification:
                print(f"  Clarify:     {nl.clarification}")
            print(f"  Reasoning:   {nl.reasoning}")
            print(f"  Latency:     {result['latency_ms']:.0f}ms")
        print()


# ── CLI ──────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Evaluate NL → QuerySpec translation"
    )
    parser.add_argument(
        "--backend", default="ollama",
        choices=["ollama", "anthropic", "gemini"],
    )
    parser.add_argument("--model", default=None)
    parser.add_argument(
        "--base-url", default="http://localhost:11434",
        help="Ollama server URL",
    )
    parser.add_argument(
        "--interactive", "-i", action="store_true",
        help="Interactive query mode",
    )
    parser.add_argument(
        "--paraphrases", default=None,
        help="Path to custom paraphrases JSON file",
    )
    parser.add_argument(
        "--output", "-o", default=None,
        help="Save results JSON to this path",
    )

    args = parser.parse_args()

    if args.interactive:
        interactive_mode(args.backend, args.model, args.base_url)
        return

    # Load custom paraphrases if provided
    paraphrases = None
    if args.paraphrases:
        with open(args.paraphrases) as f:
            paraphrases = json.load(f)

    print(f"Backend: {args.backend}")
    print(f"Model:   {args.model or '(default)'}")
    print(f"Running evaluation...\n")

    summary = run_evaluation(
        backend=args.backend,
        model=args.model,
        base_url=args.base_url,
        paraphrases=paraphrases,
    )

    print_report(summary)

    if args.output:
        with open(args.output, "w") as f:
            json.dump(summary, f, indent=2)
        print(f"\nResults saved to {args.output}")


if __name__ == "__main__":
    main()
