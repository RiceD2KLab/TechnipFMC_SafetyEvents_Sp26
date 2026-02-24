#!/usr/bin/env python3
"""Layer 2 causal enrichment runner.

Reads nodes, edges, and metadata (narratives) from CSV or Parquet, calls a
local LLM via Ollama to extract causal relationships, validates them, and
outputs L2 edges as JSONL. Can run on L1 outputs directly or post-ER data.

Usage:
    python pipeline_v2/enrichment/run_l2_enrichment.py \
        --nodes-csv pipeline_v2/outputs/entities.parquet \
        --edges-csv pipeline_v2/outputs/relations.parquet \
        --metadata-csv pipeline_v2/outputs/metadata_parsed.parquet \
        --output-dir output/l2 \
        --model qwen3:8b
"""
from __future__ import annotations

import argparse
import json
import logging
import sys
import time
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from enrichment.ollama_client import call_ollama
from enrichment.vllm_client import call_vllm
from enrichment.prompts import (
    EXTRACTION_SCHEMA,
    PROMPT_VARIANTS,
    build_user_prompt,
)
from enrichment.validate import validate_causal_edges

logger = logging.getLogger(__name__)

try:
    from tqdm import tqdm
except ImportError:
    def tqdm(iterable, **kwargs):  # type: ignore[misc]
        return iterable


def _timestamp_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _count_sentences(text: str) -> int:
    """Rough sentence count based on terminal punctuation."""
    count = 0
    for char in text:
        if char in ".!?":
            count += 1
    return max(count, 1) if text.strip() else 0


def _build_entity_dict(
    nodes_df: pd.DataFrame,
    record_no: str,
    edges_df: pd.DataFrame,
) -> Dict[str, List[str]]:
    """Build {entity_type: [values]} for a single incident from its edges."""
    inc_id = f"INCIDENT::{record_no}"
    # Find all entity IDs connected to this incident
    connected = edges_df[edges_df["source"] == inc_id]["target"].tolist()
    entities: Dict[str, List[str]] = defaultdict(list)
    for eid in connected:
        try:
            row = nodes_df.loc[eid]
        except KeyError:
            continue
        etype = str(row.get("entity_type", ""))
        value = str(row.get("value", ""))
        if etype and value and etype != "INCIDENT":
            entities[etype].append(value)
    return dict(entities)


def _distinct_entity_types(entities: Dict[str, List[str]]) -> int:
    """Count distinct entity types with at least one value."""
    return sum(1 for vals in entities.values() if vals)


def _load_existing_jsonl(path: Path) -> List[dict]:
    """Load existing JSONL records for resume support."""
    if not path.exists():
        return []
    records: List[dict] = []
    with path.open("r", encoding="utf-8") as fp:
        for line in fp:
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return records


def _append_jsonl(path: Path, rows: List[dict], mode: str = "a") -> None:
    """Append rows to JSONL file."""
    if not rows:
        return
    with path.open(mode, encoding="utf-8") as fp:
        for row in rows:
            fp.write(json.dumps(row, ensure_ascii=True) + "\n")


def _mock_ollama(
    prompt: str,
    system: str,
    **kwargs: Any,
) -> dict:
    """Mock Ollama backend that returns empty edges for dry-run testing."""
    return {"causal_edges": []}


def run_l2_enrichment(
    nodes_df: pd.DataFrame,
    edges_df: pd.DataFrame,
    metadata_df: pd.DataFrame,
    output_path: Path,
    model: str = "qwen3:8b",
    host: str = "http://127.0.0.1:11434",
    temperature: float = 0.1,
    prompt_variant: str = "full",
    shard_index: int = 0,
    num_shards: int = 1,
    resume: bool = True,
    timeout_sec: int = 120,
    max_retries: int = 2,
    mock: bool = False,
    backend: str = "ollama",
) -> pd.DataFrame:
    """Run Layer 2 causal enrichment on post-ER graph data.

    Returns a DataFrame of validated L2 edges.
    """
    output_path = Path(output_path)
    output_path.mkdir(parents=True, exist_ok=True)

    system_prompt = PROMPT_VARIANTS.get(prompt_variant, PROMPT_VARIANTS["full"])

    # Identify qualifying records
    record_nos = sorted(metadata_df["record_no"].astype(str).unique())
    if num_shards > 1:
        record_nos = record_nos[shard_index::num_shards]

    # Build entity lookup (nodes_df indexed by entity_id for O(1) lookups)
    nodes_indexed = nodes_df.set_index("entity_id", drop=False) if "entity_id" in nodes_df.columns else nodes_df
    nodes_indexed = nodes_indexed[~nodes_indexed.index.duplicated(keep="first")]

    # Build narrative lookup from metadata
    narrative_col = None
    for col in ("narrative", "NARRATIVE", "full_text"):
        if col in metadata_df.columns:
            narrative_col = col
            break
    if narrative_col is None:
        raise ValueError(f"No narrative column found in metadata. Columns: {list(metadata_df.columns)}")

    narratives: Dict[str, str] = {}
    for _, row in metadata_df.iterrows():
        rno = str(row["record_no"])
        narratives[rno] = str(row.get(narrative_col, ""))

    # Resume support
    jsonl_path = output_path / "l2_edges.jsonl"
    processed_ids: Set[str] = set()
    existing_records: List[dict] = []
    if resume:
        existing_records = _load_existing_jsonl(jsonl_path)
        for rec in existing_records:
            rid = str(rec.get("record_no", ""))
            if rid:
                processed_ids.add(rid)

    # Build entity_id -> value lookup for L1 deduplication
    eid_to_value: Dict[str, str] = {}
    if "entity_id" in nodes_df.columns and "value" in nodes_df.columns:
        for _, nrow in nodes_df.iterrows():
            eid_to_value[str(nrow["entity_id"])] = str(nrow.get("value", ""))

    # Build L1 edge keys using entity *values* (not IDs) for comparison with L2 edges
    l1_edge_keys: Set[tuple] = set()
    for _, row in edges_df.iterrows():
        src_val = eid_to_value.get(str(row.get("source", "")), str(row.get("source", "")))
        tgt_val = eid_to_value.get(str(row.get("target", "")), str(row.get("target", "")))
        key = (src_val.lower(), tgt_val.lower(), str(row.get("relation", "")))
        l1_edge_keys.add(key)

    # Filter qualifying records
    qualifying: List[str] = []
    for rno in record_nos:
        if rno in processed_ids:
            continue
        narrative = narratives.get(rno, "")
        if _count_sentences(narrative) < 2:
            continue
        entities = _build_entity_dict(nodes_indexed, rno, edges_df)
        if _distinct_entity_types(entities) < 2:
            continue
        qualifying.append(rno)

    logger.info(
        "L2 enrichment: %d qualifying records (shard %d/%d, %d already processed)",
        len(qualifying), shard_index, num_shards, len(processed_ids),
    )

    jsonl_mode = "a" if resume and jsonl_path.exists() else "w"
    all_l2_edges: List[dict] = list(existing_records)
    stats = {"total": 0, "llm_calls": 0, "edges_produced": 0, "edges_rejected": 0, "errors": 0}

    if mock:
        infer_fn = _mock_ollama
    elif backend == "vllm":
        infer_fn = call_vllm
    else:
        infer_fn = call_ollama

    for rno in tqdm(qualifying, desc="L2 enrichment", unit="record"):
        narrative = narratives[rno]
        entities = _build_entity_dict(nodes_indexed, rno, edges_df)
        user_prompt = build_user_prompt(narrative, entities)

        stats["total"] += 1
        stats["llm_calls"] += 1
        t0 = time.time()

        try:
            if mock:
                result = infer_fn(prompt=user_prompt, system=system_prompt)
            else:
                result = infer_fn(
                    prompt=user_prompt,
                    system=system_prompt,
                    model=model,
                    host=host,
                    schema=EXTRACTION_SCHEMA,
                    temperature=temperature,
                    timeout_sec=timeout_sec,
                    max_retries=max_retries,
                )
        except Exception as exc:
            logger.warning("LLM call failed for record %s: %s", rno, exc)
            stats["errors"] += 1
            continue

        call_seconds = time.time() - t0
        raw_edges = result.get("causal_edges", result.get("edges", []))

        # Validate
        valid_edges = validate_causal_edges(raw_edges, entities, narrative)
        stats["edges_rejected"] += len(raw_edges) - len(valid_edges)

        # Deduplicate against L1 (compare by lowercase values)
        deduped: List[dict] = []
        for edge in valid_edges:
            key = (edge["source"].lower(), edge["target"].lower(), edge["relation"])
            if key not in l1_edge_keys:
                deduped.append(edge)
            else:
                stats["edges_rejected"] += 1

        # Tag and write
        batch_records: List[dict] = []
        for edge in deduped:
            record = {
                "record_no": rno,
                "source": edge["source"],
                "source_type": edge["source_type"],
                "target": edge["target"],
                "target_type": edge["target_type"],
                "relation": edge["relation"],
                "evidence": edge["evidence"],
                "confidence": edge.get("confidence"),
                "layer": "L2",
                "_meta": {
                    "model": model if not mock else "mock",
                    "prompt_variant": prompt_variant,
                    "llm_call_seconds": round(call_seconds, 3),
                    "created_at_utc": _timestamp_utc(),
                    "shard_index": shard_index,
                    "num_shards": num_shards,
                },
            }
            batch_records.append(record)
            stats["edges_produced"] += 1

        _append_jsonl(jsonl_path, batch_records, mode=jsonl_mode)
        jsonl_mode = "a"
        all_l2_edges.extend(batch_records)

    # Write metrics
    metrics = {
        **stats,
        "config": {
            "model": model if not mock else "mock",
            "prompt_variant": prompt_variant,
            "temperature": temperature,
            "shard_index": shard_index,
            "num_shards": num_shards,
        },
        "run_finished_at_utc": _timestamp_utc(),
    }
    (output_path / "l2_metrics.json").write_text(
        json.dumps(metrics, indent=2) + "\n", encoding="utf-8"
    )
    logger.info("L2 enrichment complete: %s", json.dumps(stats))

    if all_l2_edges:
        return pd.DataFrame(all_l2_edges)
    return pd.DataFrame(columns=[
        "record_no", "source", "source_type", "target", "target_type",
        "relation", "evidence", "confidence", "layer",
    ])


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Layer 2 causal enrichment runner.",
    )
    parser.add_argument("--nodes-csv", required=True, help="Path to nodes CSV or Parquet")
    parser.add_argument("--edges-csv", required=True, help="Path to edges CSV or Parquet")
    parser.add_argument("--metadata-csv", required=True, help="Path to metadata CSV or Parquet (must contain narratives)")
    parser.add_argument("--output-dir", required=True, help="Output directory for L2 edges")
    parser.add_argument("--model", default=None,
                        help="Model name (default: qwen3:30b-a3b for ollama, Qwen/Qwen3-30B-A3B for vllm)")
    parser.add_argument("--host", default=None,
                        help="Server URL (default: localhost:11434 for ollama, localhost:8000 for vllm)")
    parser.add_argument("--temperature", type=float, default=0.1)
    parser.add_argument("--prompt-variant", choices=["full", "minimal", "cot"], default="full")
    parser.add_argument("--shard-index", type=int, default=0)
    parser.add_argument("--num-shards", type=int, default=1)
    parser.add_argument("--timeout-sec", type=int, default=120)
    parser.add_argument("--max-retries", type=int, default=2)
    parser.add_argument("--resume", dest="resume", action="store_true", default=True)
    parser.add_argument("--no-resume", dest="resume", action="store_false")
    parser.add_argument("--backend", choices=["ollama", "vllm"], default="ollama",
                        help="LLM serving backend (ollama or vllm)")
    parser.add_argument("--mock", action="store_true", help="Use mock backend (dry-run)")
    parser.add_argument(
        "--ground-truth", default="",
        help="Path to ground truth edges CSV/JSONL. If provided, runs Gate 3 evaluation after enrichment.",
    )
    return parser.parse_args()


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    args = _parse_args()

    # Resolve backend-specific defaults for model and host
    _defaults = {
        "ollama": {"model": "qwen3:30b-a3b", "host": "http://127.0.0.1:11434"},
        "vllm":   {"model": "Qwen/Qwen3-30B-A3B-GPTQ-Int4", "host": "http://127.0.0.1:8000"},
    }
    if args.model is None:
        args.model = _defaults[args.backend]["model"]
    if args.host is None:
        args.host = _defaults[args.backend]["host"]

    def _read_df(path: str) -> pd.DataFrame:
        if path.endswith(".parquet"):
            return pd.read_parquet(path)
        return pd.read_csv(path, low_memory=False)

    nodes_df = _read_df(args.nodes_csv)
    edges_df = _read_df(args.edges_csv)
    metadata_df = _read_df(args.metadata_csv)

    # Normalize record_no to string
    for df in (nodes_df, edges_df, metadata_df):
        if "record_no" in df.columns:
            df["record_no"] = df["record_no"].astype(str)

    result_df = run_l2_enrichment(
        nodes_df=nodes_df,
        edges_df=edges_df,
        metadata_df=metadata_df,
        output_path=Path(args.output_dir),
        model=args.model,
        host=args.host,
        temperature=args.temperature,
        prompt_variant=args.prompt_variant,
        shard_index=args.shard_index,
        num_shards=args.num_shards,
        resume=args.resume,
        timeout_sec=args.timeout_sec,
        max_retries=args.max_retries,
        mock=args.mock,
        backend=args.backend,
    )
    print(f"L2 enrichment produced {len(result_df)} edges")

    # Gate 3 evaluation (optional)
    if args.ground_truth:
        from evaluation.gate3_metrics import compute_gate3_metrics, generate_gate3_report

        gt_path = Path(args.ground_truth)
        if gt_path.suffix == ".jsonl":
            gt_edges = _load_existing_jsonl(gt_path)
        else:
            gt_edges = pd.read_csv(gt_path, low_memory=False).to_dict(orient="records")

        predicted = result_df.to_dict(orient="records") if not result_df.empty else []
        metrics = compute_gate3_metrics(predicted, gt_edges)
        report_path = Path(args.output_dir) / "gate3_report.md"
        generate_gate3_report(metrics, report_path)

        verdict = "PASS" if metrics["pass"]["gate3"] else "FAIL"
        print(f"Gate 3: {verdict} (precision={metrics['causal_precision']:.2%}, recall={metrics['causal_recall']:.2%})")
        (Path(args.output_dir) / "gate3_metrics.json").write_text(
            json.dumps(metrics, indent=2) + "\n", encoding="utf-8",
        )


if __name__ == "__main__":
    main()
