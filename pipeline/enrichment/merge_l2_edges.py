#!/usr/bin/env python3
"""Merge L2 causal edges into the L1 knowledge graph.

Reads L2 edge JSONL files (from sharded enrichment runs), creates new entity
nodes for L2-only entities, resolves entity IDs, and appends to the existing
entities and relations parquet files.

Usage:
    python pipeline/enrichment/merge_l2_edges.py \
        --l2-dir output/l2 \
        --entities-parquet pipeline/outputs/entities.parquet \
        --relations-parquet pipeline/outputs/relations.parquet \
        --output-dir pipeline/outputs/merged

Outputs:
    merged/entities.parquet   — L1 entities + new L2 entities
    merged/relations.parquet  — L1 relations + L2 causal edges
    merged/l2_merge_report.json — merge statistics
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd


def make_entity_id(entity_type: str, entity_value: str) -> str:
    """Mint an entity ID following the L1 convention: TYPE::VALUE."""
    normalized = entity_value.strip().upper()
    return f"{entity_type}::{normalized}"


def load_l2_edges(l2_dir: Path) -> list[dict]:
    """Load all L2 edge JSONL files from shard directories."""
    edges = []
    # Support both flat (l2_dir/l2_edges.jsonl) and sharded (l2_dir/shard_*/l2_edges.jsonl)
    jsonl_files = sorted(l2_dir.glob("**/l2_edges.jsonl"))
    if not jsonl_files:
        raise FileNotFoundError(f"No l2_edges.jsonl files found in {l2_dir}")

    for jf in jsonl_files:
        with jf.open("r", encoding="utf-8") as fp:
            for line in fp:
                line = line.strip()
                if not line:
                    continue
                try:
                    edges.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return edges


def merge_l2_into_graph(
    l2_edges: list[dict],
    entities_df: pd.DataFrame,
    relations_df: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    """Merge L2 edges into the L1 graph.

    Returns (merged_entities, merged_relations, stats).
    """
    # Build lookup of existing entity values -> entity_id (case-insensitive)
    existing_values: dict[tuple[str, str], str] = {}
    for _, row in entities_df.iterrows():
        key = (str(row["entity_type"]).upper(), str(row["value"]).strip().upper())
        existing_values[key] = str(row["entity_id"])

    # Secondary O(1) lookup: value -> entity_id (across all types)
    value_to_eid: dict[str, str] = {
        eval_: eid for (_, eval_), eid in existing_values.items()
    }

    # Track new entities to add
    new_entities: dict[str, dict] = {}  # entity_id -> row dict
    new_relations: list[dict] = []

    # L1 entity type mapping: map L2 types to nearest L1 type where possible
    # L2 types not in L1: Event, Condition, Action, Material, Person, Injury
    # These get added as new entity types in the graph.

    stats = {
        "l2_edges_input": len(l2_edges),
        "l2_edges_merged": 0,
        "l2_edges_skipped_duplicate": 0,
        "new_entities_created": 0,
        "existing_entities_reused": 0,
    }

    # Build existing relation keys for dedup check
    existing_rel_keys: set[tuple] = set(zip(
        relations_df["source"].astype(str),
        relations_df["target"].astype(str),
        relations_df["relation"].astype(str),
    ))

    for edge in l2_edges:
        record_no = str(edge.get("record_no") or "")
        source_val = str(edge.get("source") or "").strip()
        source_type = str(edge.get("source_type") or "").strip().upper()
        target_val = str(edge.get("target") or "").strip()
        target_type = str(edge.get("target_type") or "").strip().upper()
        relation = str(edge.get("relation") or "")
        evidence = str(edge.get("evidence") or "")
        confidence = edge.get("confidence")
        layer = edge.get("layer", "L2")

        if not source_val or not target_val or not relation:
            continue

        # Resolve source entity ID
        source_id = _resolve_entity_id(
            source_val, source_type, record_no,
            existing_values, value_to_eid, new_entities, stats,
        )

        # Resolve target entity ID
        target_id = _resolve_entity_id(
            target_val, target_type, record_no,
            existing_values, value_to_eid, new_entities, stats,
        )

        # Dedup check against existing relations
        rel_key = (source_id, target_id, relation)
        if rel_key in existing_rel_keys:
            stats["l2_edges_skipped_duplicate"] += 1
            continue

        existing_rel_keys.add(rel_key)
        new_relations.append({
            "source": source_id,
            "target": target_id,
            "relation": relation,
            "granularity": None,
            "layer": layer,
            "source_type": "l2_causal",
            "confidence": confidence if confidence is not None else 0.0,
            "evidence": evidence,
            "record_no": record_no,
        })
        stats["l2_edges_merged"] += 1

    # Build new entities DataFrame
    if new_entities:
        new_ent_df = pd.DataFrame(list(new_entities.values()))
        # Ensure all L1 columns exist (fill with NaN for L2-only entities)
        for col in entities_df.columns:
            if col not in new_ent_df.columns:
                new_ent_df[col] = None
        new_ent_df = new_ent_df[entities_df.columns]
        merged_entities = pd.concat([entities_df, new_ent_df], ignore_index=True)
    else:
        merged_entities = entities_df.copy()

    # Build new relations DataFrame
    if new_relations:
        new_rel_df = pd.DataFrame(new_relations)
        # Add evidence column to L1 relations if not present
        if "evidence" not in relations_df.columns:
            relations_df = relations_df.copy()
            relations_df["evidence"] = None
        if "record_no" not in relations_df.columns:
            relations_df = relations_df.copy()
            relations_df["record_no"] = None
        # Align columns
        for col in new_rel_df.columns:
            if col not in relations_df.columns:
                relations_df[col] = None
        for col in relations_df.columns:
            if col not in new_rel_df.columns:
                new_rel_df[col] = None
        new_rel_df = new_rel_df[relations_df.columns]
        merged_relations = pd.concat([relations_df, new_rel_df], ignore_index=True)
    else:
        merged_relations = relations_df.copy()

    stats["new_entities_created"] = len(new_entities)
    return merged_entities, merged_relations, stats


def _resolve_entity_id(
    value: str,
    entity_type: str,
    record_no: str,
    existing_values: dict[tuple[str, str], str],
    value_to_eid: dict[str, str],
    new_entities: dict[str, dict],
    stats: dict,
) -> str:
    """Resolve a free-text entity value to an entity_id.

    Checks existing L1 entities first, then mints a new ID if needed.
    Special case: "incident" (lowercase) resolves to INCIDENT::{record_no}.
    """
    # Special case: "incident" target means the hub INCIDENT node
    if value.lower() == "incident" and entity_type == "INCIDENT":
        return f"INCIDENT::{record_no}"

    # Check if entity already exists in L1 (exact type + value match)
    lookup_key = (entity_type, value.strip().upper())
    if lookup_key in existing_values:
        stats["existing_entities_reused"] += 1
        return existing_values[lookup_key]

    # Check L1 entities with any type (value match across types) — O(1) lookup
    eval_upper = value.strip().upper()
    if eval_upper in value_to_eid:
        stats["existing_entities_reused"] += 1
        return value_to_eid[eval_upper]

    # Mint a new entity ID
    entity_id = make_entity_id(entity_type, value)

    # Check if we already minted this one
    if entity_id in new_entities:
        stats["existing_entities_reused"] += 1
        return entity_id

    new_entities[entity_id] = {
        "entity_id": entity_id,
        "entity_type": entity_type,
        "value": value.strip(),
    }
    return entity_id


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Merge L2 causal edges into the L1 knowledge graph.")
    parser.add_argument("--l2-dir", required=True, help="Directory containing L2 JSONL output (with shard_* subdirs)")
    parser.add_argument("--entities-parquet", required=True, help="Path to L1 entities parquet")
    parser.add_argument("--relations-parquet", required=True, help="Path to L1 relations parquet")
    parser.add_argument("--output-dir", required=True, help="Output directory for merged parquet files")
    return parser.parse_args()


def main() -> None:
    args = _parse_args()

    l2_dir = Path(args.l2_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Loading L2 edges from {l2_dir}...")
    l2_edges = load_l2_edges(l2_dir)
    print(f"  Found {len(l2_edges)} L2 edges")

    print("Loading L1 graph...")
    entities_df = pd.read_parquet(args.entities_parquet)
    relations_df = pd.read_parquet(args.relations_parquet)
    print(f"  L1 entities: {len(entities_df):,}")
    print(f"  L1 relations: {len(relations_df):,}")

    print("Merging L2 edges into graph...")
    merged_entities, merged_relations, stats = merge_l2_into_graph(
        l2_edges, entities_df, relations_df,
    )

    # Save
    merged_entities.to_parquet(output_dir / "entities.parquet", index=False)
    merged_relations.to_parquet(output_dir / "relations.parquet", index=False)

    report_path = output_dir / "l2_merge_report.json"
    report_path.write_text(json.dumps(stats, indent=2) + "\n", encoding="utf-8")

    print(f"\nMerge complete:")
    print(f"  L2 edges input:       {stats['l2_edges_input']}")
    print(f"  L2 edges merged:      {stats['l2_edges_merged']}")
    print(f"  L2 edges skipped:     {stats['l2_edges_skipped_duplicate']}")
    print(f"  New entities created:  {stats['new_entities_created']}")
    print(f"  Entities reused:       {stats['existing_entities_reused']}")
    print(f"  Merged entities: {len(merged_entities):,} (was {len(entities_df):,})")
    print(f"  Merged relations: {len(merged_relations):,} (was {len(relations_df):,})")
    print(f"\nSaved to {output_dir}/")


if __name__ == "__main__":
    main()
