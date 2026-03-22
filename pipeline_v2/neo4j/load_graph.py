"""
Neo4j graph loader for the TechnipFMC Safety Events knowledge graph.

Usage:
    NEO4J_PASSWORD=<pw> python pipeline_v2/neo4j/load_graph.py \\
        --uri bolt://localhost:7687 --user neo4j \\
        [--entities PATH] [--relations PATH] \\
        [--wipe] [--batch-size 500]

Password can be set via NEO4J_PASSWORD env var (preferred) or --password flag.
"""

import argparse
import math
import os
import sys
from pathlib import Path
from typing import Any  # used by _clean return type

import pandas as pd
from neo4j import GraphDatabase

# ---------------------------------------------------------------------------
# Path defaults — resolved relative to this file's location so the script
# works regardless of cwd.
# ---------------------------------------------------------------------------
_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
_DEFAULT_ENTITIES = _REPO_ROOT / "pipeline_v2" / "outputs" / "entities.parquet"
_DEFAULT_RELATIONS = _REPO_ROOT / "pipeline_v2" / "outputs" / "relations.parquet"

# ---------------------------------------------------------------------------
# Property columns that map directly to node properties (beyond id/type/value)
# ---------------------------------------------------------------------------
_ENTITY_OPTIONAL_PROPS = [
    "incident_type", "severity", "severity_bin", "likelihood", "impact_type",
    "work_process", "risk_color", "business_unit", "reported_date",
    "event_datetime", "client", "case_categorization", "operating_center",
    "loc_site", "loc_city", "loc_country", "loc_region",
]

# ---------------------------------------------------------------------------
# Relation type → Cypher MERGE template
# Each template receives $batch (list of dicts with source, target, and props).
# ---------------------------------------------------------------------------
_REL_CYPHER: dict[str, str] = {t: f"""
UNWIND $batch AS row
MATCH (src:Entity {{entity_id: row.source}})
MATCH (tgt:Entity {{entity_id: row.target}})
MERGE (src)-[r:{t}]->(tgt)
  ON CREATE SET r.layer = row.layer, r.confidence = row.confidence,
                r.evidence = row.evidence, r.record_no = row.record_no,
                r.granularity = row.granularity
RETURN count(r) AS created
""" for t in [
    "OCCURRED_AT", "REPORTED_BY", "INVOLVED", "CATEGORIZED_AS",
    "AFFECTED", "RESULTED_IN", "LOCATED_IN",
    "CAUSAL", "PRECEDED_BY", "FAILED_CONTROL", "MITIGATED_BY",
]}

_INDEXES = [
    "CREATE INDEX IF NOT EXISTS FOR (n:Entity) ON (n.entity_id)",
    "CREATE INDEX IF NOT EXISTS FOR (n:Entity) ON (n.entity_type)",
    "CREATE INDEX IF NOT EXISTS FOR (n:Entity) ON (n.value)",
    "CREATE FULLTEXT INDEX entity_value_ft IF NOT EXISTS FOR (n:Entity) ON EACH [n.value]",
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _clean(value: Any) -> Any:
    """Convert NaN / float nan to None for Neo4j compatibility."""
    if value is None:
        return None
    if isinstance(value, float) and math.isnan(value):
        return None
    # pandas NaT / NA
    try:
        if pd.isna(value):
            return None
    except (TypeError, ValueError):
        pass
    return value


def _batches(df: pd.DataFrame, size: int):
    for i in range(0, len(df), size):
        yield df.iloc[i : i + size]


# ---------------------------------------------------------------------------
# Loading functions
# ---------------------------------------------------------------------------

def wipe_graph(session) -> None:
    print("Wiping graph (batched) ...")
    while True:
        result = session.run(
            "MATCH (n) WITH n LIMIT 10000 DETACH DELETE n RETURN count(*) AS deleted"
        )
        deleted = result.single()["deleted"]
        if deleted == 0:
            break
        print(f"  deleted {deleted:,} nodes ...")
    print("  done.")


def create_indexes(session) -> None:
    print("Creating indexes ...")
    for stmt in _INDEXES:
        try:
            session.run(stmt)
        except Exception as exc:
            print(f"  [warn] index skipped: {exc}")
    print("  done.")


def load_entities(session, df: pd.DataFrame, batch_size: int, apoc: bool) -> int:
    total = 0
    n_batches = math.ceil(len(df) / batch_size)
    print(f"Loading {len(df):,} entities in {n_batches} batches ...")

    opt_cols = [c for c in _ENTITY_OPTIONAL_PROPS if c in df.columns]
    for i, chunk in enumerate(_batches(df, batch_size), 1):
        batch = []
        for row in chunk.to_dict("records"):
            props = {
                "entity_id": row["entity_id"],
                "entity_type": _clean(row.get("entity_type")),
                "value": _clean(row.get("value")),
            }
            for col in opt_cols:
                v = _clean(row.get(col))
                if v is not None:
                    props[col] = v
            batch.append(props)

        result = session.run(
            """
            UNWIND $batch AS props
            MERGE (n:Entity {entity_id: props.entity_id})
            SET n += props
            RETURN count(n) AS cnt
            """,
            batch=batch,
        )
        total += result.single()["cnt"]

        if apoc:
            _add_secondary_labels(session, chunk)

        if i % 10 == 0 or i == n_batches:
            print(f"  entity batches: {i}/{n_batches}  nodes merged: {total:,}")

    return total


def _add_secondary_labels(session, chunk: pd.DataFrame) -> None:
    """Add entity_type as a secondary label via APOC (best-effort)."""
    by_type: dict[str, list[str]] = {}
    for row in chunk.to_dict("records"):
        etype = str(row.get("entity_type") or "")
        if etype:
            by_type.setdefault(etype, []).append(row["entity_id"])

    for etype, ids in by_type.items():
        try:
            session.run(
                """
                MATCH (n:Entity) WHERE n.entity_id IN $ids
                CALL apoc.create.addLabels(n, [$label]) YIELD node
                RETURN count(node)
                """,
                ids=ids,
                label=etype,
            )
        except Exception:
            pass  # APOC not available; silently skip


def _detect_apoc(session) -> bool:
    try:
        session.run("CALL apoc.help('version') YIELD name RETURN name LIMIT 1")
        return True
    except Exception:
        return False


def load_relations(session, df: pd.DataFrame, batch_size: int) -> tuple[int, int]:
    """Returns (loaded, skipped)."""
    total_loaded = 0
    total_skipped = 0

    rel_col = "relation"
    known_types = set(_REL_CYPHER.keys())
    unknown = set(df[rel_col].dropna().unique()) - known_types
    if unknown:
        print(f"  [warn] unknown relation types (will skip): {unknown}")

    for rel_type, group in df.groupby(rel_col):
        if rel_type not in _REL_CYPHER:
            total_skipped += len(group)
            continue

        cypher = _REL_CYPHER[rel_type]
        n_batches = math.ceil(len(group) / batch_size)
        print(f"  relation {rel_type}: {len(group):,} edges, {n_batches} batches")

        for i, chunk in enumerate(_batches(group, batch_size), 1):
            batch = [
                {
                    "source": row["source"],
                    "target": row["target"],
                    "layer": _clean(row.get("layer")),
                    "confidence": _clean(row.get("confidence")),
                    "evidence": _clean(row.get("evidence")),
                    "record_no": _clean(row.get("record_no")),
                    "granularity": _clean(row.get("granularity")),
                }
                for row in chunk.to_dict("records")
            ]

            try:
                result = session.run(cypher, batch=batch)
                total_loaded += result.single()["created"]
            except Exception as exc:
                print(f"    [warn] batch {i} failed ({exc}); skipping {len(batch)} edges")
                total_skipped += len(batch)

            if i % 10 == 0 or i == n_batches:
                print(f"    batches: {i}/{n_batches}")

    return total_loaded, total_skipped


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main(argv=None) -> None:
    parser = argparse.ArgumentParser(description="Load safety KG into Neo4j")
    parser.add_argument("--uri", default="bolt://localhost:7687")
    parser.add_argument("--user", default="neo4j")
    parser.add_argument("--password", default=None,
                        help="Neo4j password (prefer NEO4J_PASSWORD env var)")
    parser.add_argument("--entities", type=Path, default=_DEFAULT_ENTITIES)
    parser.add_argument("--relations", type=Path, default=_DEFAULT_RELATIONS)
    parser.add_argument("--wipe", action="store_true", default=False,
                        help="Drop all nodes/edges before loading")
    parser.add_argument("--batch-size", type=int, default=500)
    args = parser.parse_args(argv)

    password = args.password or os.environ.get("NEO4J_PASSWORD")
    if not password:
        print("[error] Password required: use --password or set NEO4J_PASSWORD env var",
              file=sys.stderr)
        sys.exit(1)

    print(f"Connecting to {args.uri} ...")
    driver = GraphDatabase.driver(args.uri, auth=(args.user, password))

    try:
        driver.verify_connectivity()
    except Exception as exc:
        print(f"[error] Cannot connect to Neo4j: {exc}", file=sys.stderr)
        sys.exit(1)

    print(f"Reading entities from {args.entities} ...")
    entities_df = pd.read_parquet(args.entities)
    print(f"  {len(entities_df):,} entity rows")

    print(f"Reading relations from {args.relations} ...")
    relations_df = pd.read_parquet(args.relations)
    print(f"  {len(relations_df):,} relation rows")

    with driver.session() as session:
        apoc = _detect_apoc(session)
        print(f"APOC available: {apoc}")

        if args.wipe:
            wipe_graph(session)

        create_indexes(session)
        n_nodes = load_entities(session, entities_df, args.batch_size, apoc)
        n_rels, n_skipped = load_relations(session, relations_df, args.batch_size)

    driver.close()

    print("\n--- Summary ---")
    print(f"  Nodes merged : {n_nodes:,}")
    print(f"  Edges merged : {n_rels:,}")
    if n_skipped:
        print(f"  Edges skipped: {n_skipped:,}")
    print("Done.")


if __name__ == "__main__":
    main()
