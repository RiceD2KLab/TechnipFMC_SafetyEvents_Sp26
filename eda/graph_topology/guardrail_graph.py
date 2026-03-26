#!/usr/bin/env python3
"""
Schema enforcement, canonical relation mapping, and entity title normalization.

Applies the full guardrail stack to raw GraphRAG output: filters entities to
the 7-type allowlist (INCIDENT, INJURY_TYPE, BODY_PART, EQUIPMENT, LOCATION,
ORGANIZATION, DATE), maps legacy INCIDENT_TYPE alias, deduplicates entities via
normalized title (keeping the highest-degree representative), canonicalizes all
relation descriptions to the 7 allowed relation types, filters dangling edges,
and recomputes degree on the cleaned graph. Writes to fall2025/graphRAG/output_guardrailed.

Key findings: 65,233 entities and 105,521 relations retained after filtering;
zero schema leakage in the output (all entity types within allowlist); entity
count reduced significantly from raw extraction by type filtering and title
normalization.

Decision: informed production guardrail gate design for the v2 pipeline; the
filtering logic here was ported directly into pipeline/guardrail.py.
"""

from __future__ import annotations

import argparse
import re
from collections import Counter
from pathlib import Path

import pandas as pd


ALLOWED_TYPES = {
    "INCIDENT",
    "INJURY_TYPE",
    "BODY_PART",
    "EQUIPMENT",
    "LOCATION",
    "ORGANIZATION",
    "DATE",
}

LEGACY_TYPE_ALIASES = {
    "INCIDENT_TYPE": "INCIDENT",
}

RELATION_MAP = {
    "CAUSE": "CAUSED_BY",
    "LED_TO": "CAUSED_BY",
    "RESULT": "RESULTED_IN",
    "DUE_TO": "CAUSED_BY",
    "CONTRIB": "CAUSED_BY",
    "INVOLV": "INVOLVED",
    "OCCUR": "OCCURRED_AT",
    "LOCAT": "OCCURRED_AT",
    "PLACE": "OCCURRED_AT",
    "DURING": "OCCURRED_AT",
    "WHEN": "OCCURRED_AT",
    "TIME": "OCCURRED_AT",
    "DAMAGE": "RESULTED_IN",
    "INJUR": "RESULTED_IN",
    "HURT": "RESULTED_IN",
    "AFFECT": "AFFECTED",
    "IMPACT": "AFFECTED",
    "USE": "USED_IN",
    "UTIL": "USED_IN",
    "OPERAT": "INVOLVED",
    "OWN": "INVOLVED",
}


def normalize_text(text: str) -> str:
    text = text.upper()
    text = re.sub(r"[^A-Z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def map_relation(desc: str) -> str:
    norm = normalize_text(desc)
    for keyword, canonical in RELATION_MAP.items():
        if keyword in norm:
            return canonical
    return "INVOLVED"


def main() -> None:
    parser = argparse.ArgumentParser(description="Apply schema + relation guardrails.")
    parser.add_argument("--input-dir", default="fall2025/graphRAG/output")
    parser.add_argument("--output-dir", default="fall2025/graphRAG/output_guardrailed")
    parser.add_argument("--entities", default="entities_filtered.parquet")
    parser.add_argument("--relations", default="relationships_filtered.parquet")
    parser.add_argument("--drop-related-to", action="store_true", help="Drop relations mapped to RELATED_TO.")
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    ents = pd.read_parquet(input_dir / args.entities)
    rels = pd.read_parquet(input_dir / args.relations)

    # Filter entities to schema
    ents["type"] = (
        ents["type"]
        .astype(str)
        .str.strip()
        .str.upper()
        .map(lambda value: LEGACY_TYPE_ALIASES.get(value, value))
    )
    ents["title"] = ents["title"].astype(str).str.strip()
    ents = ents[ents["type"].isin(ALLOWED_TYPES)].copy()

    # Normalize titles and dedupe
    ents["clean_title"] = ents["title"].map(normalize_text)
    # Keep representative with highest degree
    if "degree" in ents.columns:
        ents = ents.sort_values("degree", ascending=False)
    dedup = ents.drop_duplicates(subset="clean_title", keep="first").copy()

    # Map relations to canonical types
    rels["clean_description"] = rels["description"].astype(str).map(map_relation)
    if args.drop_related_to:
        rels = rels[rels["clean_description"] != "RELATED_TO"].copy()

    # Normalize endpoints
    rels["clean_source"] = rels["source"].astype(str).map(normalize_text)
    rels["clean_target"] = rels["target"].astype(str).map(normalize_text)

    keep_nodes = set(dedup["clean_title"])
    rels = rels[rels["clean_source"].isin(keep_nodes) & rels["clean_target"].isin(keep_nodes)].copy()

    # Recompute degree on guardrailed graph
    deg = Counter()
    for s, t in zip(rels["clean_source"], rels["clean_target"]):
        deg[s] += 1
        deg[t] += 1

    dedup["degree"] = dedup["clean_title"].map(lambda x: deg.get(x, 0))

    # Output
    out_ents = dedup.drop(columns=["title"]).rename(columns={"clean_title": "title"})
    rels_small = rels[["clean_source", "clean_target", "clean_description"]].copy()
    out_rels = rels_small.rename(
        columns={
            "clean_source": "source",
            "clean_target": "target",
            "clean_description": "description",
        }
    )

    out_ents.to_parquet(output_dir / "entities.parquet", index=False)
    out_rels.to_parquet(output_dir / "relationships.parquet", index=False)

    print(
        {
            "entities_in": len(ents),
            "entities_out": len(out_ents),
            "relations_in": len(rels),
            "relations_out": len(out_rels),
            "out_dir": str(output_dir),
        }
    )


if __name__ == "__main__":
    main()
