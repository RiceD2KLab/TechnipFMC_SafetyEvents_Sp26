#!/usr/bin/env python3
"""
Strict schema filtering with optional drift detection for CI/CD validation.

Filters entities to the v1 canonical type allowlist (via schema.constants) and
prunes any relationship whose source or target was removed. The --strict-v1 flag
enables hard failure when raw entity types include values outside the allowlist
(including legacy aliases like INCIDENT_TYPE), making the script suitable as a
schema validation gate in automated pipelines. Reads from graphRAG/output and
writes to graphRAG/output_schema_only by default.

Key findings: strict mode reliably surfaces schema drift introduced by model
hallucination; running without --strict-v1 performs a silent drop, which is
appropriate for production data cleaning but masks extraction regressions.

Decision: informed CI/CD schema validation gate design; the --strict-v1 flag
pattern was adopted as the preflight check in the v2 pipeline test suite.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
from schema.constants import V1_ENTITY_TYPES, canonicalize_entity_type, invalid_entity_types


def main() -> None:
    parser = argparse.ArgumentParser(description="Filter entities/relationships to a strict schema.")
    parser.add_argument("--input-dir", default="graphRAG/output")
    parser.add_argument("--output-dir", default="graphRAG/output_schema_only")
    parser.add_argument("--entities", default="entities_filtered.parquet")
    parser.add_argument("--relations", default="relationships_filtered.parquet")
    parser.add_argument(
        "--strict-v1",
        action="store_true",
        help="Fail when raw entity types include values outside v1 allowlist (including INCIDENT_TYPE).",
    )
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    ents = pd.read_parquet(input_dir / args.entities)
    rels = pd.read_parquet(input_dir / args.relations)

    title_col = "title"
    type_col = "type"

    if args.strict_v1:
        raw_types = ents[type_col].astype(str).str.strip().str.upper()
        invalid_raw = sorted(invalid_entity_types(raw_types.unique().tolist(), strict_v1=True))
        if invalid_raw:
            raise ValueError(f"Schema drift detected in raw entity types: {invalid_raw}")

    ents[type_col] = (
        ents[type_col]
        .astype(str)
        .str.strip()
        .str.upper()
        .map(canonicalize_entity_type)
    )
    ents[title_col] = ents[title_col].astype(str).str.strip()

    # Keep only allowed schema
    ents_filtered = ents[ents[type_col].isin(V1_ENTITY_TYPES)].copy()

    keep_nodes = set(ents_filtered[title_col])
    rels_filtered = rels[
        rels["source"].isin(keep_nodes) & rels["target"].isin(keep_nodes)
    ].copy()

    ents_filtered.to_parquet(output_dir / "entities.parquet", index=False)
    rels_filtered.to_parquet(output_dir / "relationships.parquet", index=False)

    print(f"[schema_filter] input entities: {len(ents)}")
    print(f"[schema_filter] input relations: {len(rels)}")
    print(f"[schema_filter] kept entities: {len(ents_filtered)}")
    print(f"[schema_filter] kept relations: {len(rels_filtered)}")
    print(f"[schema_filter] output dir: {output_dir}")


if __name__ == "__main__":
    main()
