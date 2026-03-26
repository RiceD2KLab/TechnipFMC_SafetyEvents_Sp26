#!/usr/bin/env python3
"""Compute and report statistics for Layer 2 causal enrichment runs.

Reads L2 output shards (l2_edges.jsonl + l2_metrics.json) and produces
a Markdown report with relation distributions, entity type distributions,
per-shard breakdowns, and timing stats.

Usage:
    python pipeline/enrichment/compute_l2_stats.py \
        --l2-dir output/l2/qwen3_30b_a3b_ollama \
        --output pipeline/enrichment/l2_results_qwen3_30b_a3b.md
"""
from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, List


def _load_jsonl(path: Path) -> List[dict]:
    records: List[dict] = []
    with path.open("r", encoding="utf-8") as fp:
        for line in fp:
            line = line.strip()
            if line:
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return records


def collect_shard_data(l2_dir: Path) -> Dict[str, Any]:
    """Collect all edges and metrics from shard directories."""
    all_edges: List[dict] = []
    shard_metrics: List[dict] = []
    shard_dirs = sorted(l2_dir.glob("shard_*"))

    if not shard_dirs:
        # Single-shard run (files directly in l2_dir)
        edges_path = l2_dir / "l2_edges.jsonl"
        metrics_path = l2_dir / "l2_metrics.json"
        if edges_path.exists():
            all_edges = _load_jsonl(edges_path)
        if metrics_path.exists():
            shard_metrics.append(json.loads(metrics_path.read_text(encoding="utf-8")))
    else:
        for sd in shard_dirs:
            edges_path = sd / "l2_edges.jsonl"
            metrics_path = sd / "l2_metrics.json"
            if edges_path.exists():
                all_edges.extend(_load_jsonl(edges_path))
            if metrics_path.exists():
                shard_metrics.append(json.loads(metrics_path.read_text(encoding="utf-8")))

    return {
        "edges": all_edges,
        "shard_metrics": shard_metrics,
        "shard_dirs": [sd.name for sd in shard_dirs],
    }


def compute_stats(data: Dict[str, Any]) -> Dict[str, Any]:
    """Compute aggregate statistics from collected shard data."""
    edges = data["edges"]
    shard_metrics = data["shard_metrics"]

    # Aggregate metrics from shards
    total_records = sum(m.get("total", 0) for m in shard_metrics)
    total_llm_calls = sum(m.get("llm_calls", 0) for m in shard_metrics)
    total_edges_produced = sum(m.get("edges_produced", 0) for m in shard_metrics)
    total_edges_rejected = sum(m.get("edges_rejected", 0) for m in shard_metrics)
    total_errors = sum(m.get("errors", 0) for m in shard_metrics)

    # Relation distribution
    relation_counts = Counter(e.get("relation", "UNKNOWN") for e in edges)

    # Entity type distributions (source and target)
    source_type_counts = Counter(e.get("source_type", "UNKNOWN") for e in edges)
    target_type_counts = Counter(e.get("target_type", "UNKNOWN") for e in edges)

    # Unique records
    unique_records = set(str(e.get("record_no", "")) for e in edges)

    # Edges per record
    edges_per_record: Dict[str, int] = defaultdict(int)
    for e in edges:
        edges_per_record[str(e.get("record_no", ""))] += 1
    epr_values = list(edges_per_record.values()) if edges_per_record else [0]
    avg_epr = sum(epr_values) / len(epr_values) if epr_values else 0

    # Timing from _meta
    call_times = []
    for e in edges:
        meta = e.get("_meta", {})
        t = meta.get("llm_call_seconds")
        if t is not None:
            call_times.append(float(t))

    # Per-shard breakdown
    per_shard = []
    for m in shard_metrics:
        cfg = m.get("config", {})
        per_shard.append({
            "shard": cfg.get("shard_index", "?"),
            "records": m.get("total", 0),
            "edges": m.get("edges_produced", 0),
            "rejected": m.get("edges_rejected", 0),
            "errors": m.get("errors", 0),
            "finished": m.get("run_finished_at_utc", ""),
        })

    # Config from first shard
    config = shard_metrics[0].get("config", {}) if shard_metrics else {}

    return {
        "total_edges": len(edges),
        "total_records": total_records,
        "unique_records_with_edges": len(unique_records),
        "total_llm_calls": total_llm_calls,
        "total_edges_produced": total_edges_produced,
        "total_edges_rejected": total_edges_rejected,
        "total_errors": total_errors,
        "avg_edges_per_record": round(avg_epr, 2),
        "relation_counts": dict(relation_counts.most_common()),
        "source_type_counts": dict(source_type_counts.most_common()),
        "target_type_counts": dict(target_type_counts.most_common()),
        "timing": {
            "total_calls_with_timing": len(call_times),
            "mean_sec": round(sum(call_times) / len(call_times), 1) if call_times else 0,
            "min_sec": round(min(call_times), 1) if call_times else 0,
            "max_sec": round(max(call_times), 1) if call_times else 0,
        },
        "per_shard": per_shard,
        "config": config,
    }


def _pct(count: int, total: int) -> str:
    return f"{count / total:.1%}" if total else "—"


def generate_report(stats: Dict[str, Any], output_path: Path) -> None:
    """Generate a Markdown report from computed stats."""
    cfg = stats["config"]
    model = cfg.get("model", "unknown")
    variant = cfg.get("prompt_variant", "full")
    temp = cfg.get("temperature", "?")
    n_shards = cfg.get("num_shards", len(stats["per_shard"]))

    total = stats["total_edges"]

    lines = [
        f"# L2 Causal Enrichment Results — {model}",
        "",
        "## Run Configuration",
        "",
        f"- **Model:** `{model}`",
        f"- **Prompt variant:** {variant}",
        f"- **Temperature:** {temp}",
        f"- **Shards:** {n_shards}",
        "",
        "## Summary",
        "",
        f"| Metric | Value |",
        f"|--------|-------|",
        f"| Total edges | {stats['total_edges']:,} |",
        f"| Records processed | {stats['total_records']:,} |",
        f"| Records with edges | {stats['unique_records_with_edges']:,} |",
        f"| LLM calls | {stats['total_llm_calls']:,} |",
        f"| Edges rejected (validation) | {stats['total_edges_rejected']:,} |",
        f"| Errors | {stats['total_errors']:,} |",
        f"| Avg edges/record | {stats['avg_edges_per_record']} |",
        "",
        "## Relation Distribution",
        "",
        "| Relation | Count | % |",
        "|----------|------:|---:|",
    ]
    for rel, cnt in stats["relation_counts"].items():
        lines.append(f"| {rel} | {cnt:,} | {_pct(cnt, total)} |")

    lines.extend([
        "",
        "## Source Entity Types",
        "",
        "| Type | Count | % |",
        "|------|------:|---:|",
    ])
    for etype, cnt in stats["source_type_counts"].items():
        lines.append(f"| {etype} | {cnt:,} | {_pct(cnt, total)} |")

    lines.extend([
        "",
        "## Target Entity Types",
        "",
        "| Type | Count | % |",
        "|------|------:|---:|",
    ])
    for etype, cnt in stats["target_type_counts"].items():
        lines.append(f"| {etype} | {cnt:,} | {_pct(cnt, total)} |")

    # Timing
    t = stats["timing"]
    lines.extend([
        "",
        "## Timing",
        "",
        f"| Metric | Value |",
        f"|--------|-------|",
        f"| Mean call time | {t['mean_sec']}s |",
        f"| Min call time | {t['min_sec']}s |",
        f"| Max call time | {t['max_sec']}s |",
        f"| Calls with timing data | {t['total_calls_with_timing']:,} |",
    ])

    # Per-shard
    if stats["per_shard"]:
        lines.extend([
            "",
            "## Per-Shard Breakdown",
            "",
            "| Shard | Records | Edges | Rejected | Errors | Finished (UTC) |",
            "|------:|--------:|------:|---------:|-------:|----------------|",
        ])
        for s in stats["per_shard"]:
            lines.append(
                f"| {s['shard']} | {s['records']:,} | {s['edges']:,} "
                f"| {s['rejected']:,} | {s['errors']:,} | {s['finished']} |"
            )

    lines.append("")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Report written to {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Compute L2 enrichment stats")
    parser.add_argument(
        "--l2-dir", required=True, type=Path,
        help="Root directory of L2 output (contains shard_* subdirs)",
    )
    parser.add_argument(
        "--output", type=Path, default=None,
        help="Output markdown path (default: <l2-dir>/l2_results.md)",
    )
    args = parser.parse_args()

    if args.output is None:
        args.output = args.l2_dir / "l2_results.md"

    data = collect_shard_data(args.l2_dir)
    if not data["edges"]:
        print("No edges found. Check --l2-dir path.")
        return

    stats = compute_stats(data)
    generate_report(stats, args.output)

    # Also dump raw stats as JSON
    json_path = args.output.with_suffix(".json")
    json_path.write_text(json.dumps(stats, indent=2) + "\n", encoding="utf-8")
    print(f"Raw stats written to {json_path}")


if __name__ == "__main__":
    main()
