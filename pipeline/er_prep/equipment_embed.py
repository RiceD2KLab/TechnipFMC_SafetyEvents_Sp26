#!/usr/bin/env python3
"""Equipment ER via sentence-transformer embeddings.

Clusters EQUIPMENT canonical values using cosine similarity on
all-MiniLM-L6-v2 embeddings, then emits a merge map CSV for review
and optional auto-apply.

Usage:
    # Generate merge candidates (review first)
    python -m pipeline.er_prep.equipment_embed \
        --input pipeline/outputs/v6_post_er/entities.parquet \
        --output pipeline/er_prep/v6/equipment_embedding_merges.csv

    # Apply merges to entities + relations
    python -m pipeline.er_prep.equipment_embed \
        --input pipeline/outputs/v6_post_er/entities.parquet \
        --output pipeline/er_prep/v6/equipment_embedding_merges.csv \
        --apply \
        --entities-parquet pipeline/outputs/v6_merged/entities.parquet \
        --relations-parquet pipeline/outputs/v6_merged/relations.parquet
"""
from __future__ import annotations

import argparse
import time
from pathlib import Path

import numpy as np
import pandas as pd


def extract_equipment_canonicals(entities_path: Path) -> list[str]:
    """Return sorted list of unique EQUIPMENT canonical values."""
    df = pd.read_parquet(entities_path)
    eq = df[df["entity_type"] == "EQUIPMENT"]["value"].dropna().str.strip()
    return sorted(eq.unique().tolist())


def embed_values(values: list[str], batch_size: int = 512) -> np.ndarray:
    """Embed canonical values with all-MiniLM-L6-v2."""
    from sentence_transformers import SentenceTransformer

    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    embeddings = model.encode(
        values,
        batch_size=batch_size,
        show_progress_bar=True,
        normalize_embeddings=True,
    )
    return embeddings


def greedy_cluster(
    values: list[str],
    embeddings: np.ndarray,
    threshold: float = 0.92,
) -> list[tuple[str, list[str], float]]:
    """Greedy threshold clustering.

    Returns list of (representative, members, max_similarity) tuples.
    Representative = longest string in the cluster.
    Only returns clusters with 2+ members.
    """
    n = len(values)
    # Cosine similarity matrix (embeddings are already L2-normalized)
    sim_matrix = embeddings @ embeddings.T

    assigned = [False] * n
    clusters: list[tuple[str, list[str], float]] = []

    # Process by decreasing string length (longer = more descriptive = better rep)
    order = sorted(range(n), key=lambda i: -len(values[i]))

    for i in order:
        if assigned[i]:
            continue
        assigned[i] = True

        members = [i]
        max_sim = 0.0
        for j in range(n):
            if assigned[j] or i == j:
                continue
            s = float(sim_matrix[i, j])
            if s >= threshold:
                members.append(j)
                assigned[j] = True
                max_sim = max(max_sim, s)

        if len(members) > 1:
            # Pick longest as representative
            rep_idx = max(members, key=lambda idx: len(values[idx]))
            rep = values[rep_idx]
            member_vals = [values[m] for m in members]
            clusters.append((rep, member_vals, max_sim))

    return clusters


def build_merge_map(
    clusters: list[tuple[str, list[str], float]],
) -> pd.DataFrame:
    """Build a CSV-friendly merge map from clusters."""
    rows = []
    for rep, members, max_sim in clusters:
        for m in members:
            if m != rep:
                rows.append({
                    "old_canonical": m,
                    "new_canonical": rep,
                    "cluster_size": len(members),
                    "max_similarity": round(max_sim, 4),
                })
    return pd.DataFrame(rows)


def apply_merges(
    merge_df: pd.DataFrame,
    entities_path: Path,
    relations_path: Path,
) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    """Apply equipment merges to entities and relations parquets.

    Returns (merged_entities, merged_relations, stats).
    """
    ent_df = pd.read_parquet(entities_path)
    rel_df = pd.read_parquet(relations_path)

    # Build old -> new mapping for entity values AND entity IDs
    value_map = dict(zip(merge_df["old_canonical"], merge_df["new_canonical"]))
    id_map: dict[str, str] = {}
    for old_val, new_val in value_map.items():
        old_id = f"EQUIPMENT::{old_val.strip().upper()}"
        new_id = f"EQUIPMENT::{new_val.strip().upper()}"
        id_map[old_id] = new_id

    # Remap entity values and IDs
    ent_df = ent_df.copy()
    ent_df["entity_id"] = ent_df["entity_id"].map(lambda x: id_map.get(x, x))
    ent_df["value"] = ent_df.apply(
        lambda row: value_map.get(row["value"], row["value"])
        if row.get("entity_type") == "EQUIPMENT" else row["value"],
        axis=1,
    )

    # Deduplicate entities (keep first occurrence of each entity_id)
    before_ent = len(ent_df)
    ent_df = ent_df.drop_duplicates(subset=["entity_id"], keep="first")
    deduped_ents = before_ent - len(ent_df)

    # Remap relation source/target
    rel_df = rel_df.copy()
    rel_df["source"] = rel_df["source"].map(lambda x: id_map.get(x, x))
    rel_df["target"] = rel_df["target"].map(lambda x: id_map.get(x, x))

    # Deduplicate relations
    before_rel = len(rel_df)
    rel_df = rel_df.drop_duplicates(
        subset=["source", "target", "relation"], keep="first",
    )
    deduped_rels = before_rel - len(rel_df)

    stats = {
        "merges_applied": len(value_map),
        "entities_deduped": deduped_ents,
        "relations_deduped": deduped_rels,
        "final_entities": len(ent_df),
        "final_relations": len(rel_df),
    }
    return ent_df, rel_df, stats


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Equipment ER via sentence-transformer embeddings",
    )
    parser.add_argument(
        "--input", required=True,
        help="Path to entities parquet (source of EQUIPMENT canonicals)",
    )
    parser.add_argument(
        "--output", required=True,
        help="Path for merge map CSV output",
    )
    parser.add_argument(
        "--threshold", type=float, default=0.92,
        help="Cosine similarity threshold for clustering (default: 0.92)",
    )
    parser.add_argument("--apply", action="store_true",
                        help="Apply merges to entities/relations parquets")
    parser.add_argument("--entities-parquet",
                        help="Entities parquet to apply merges to")
    parser.add_argument("--relations-parquet",
                        help="Relations parquet to apply merges to")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"Extracting EQUIPMENT canonicals from {input_path}...")
    values = extract_equipment_canonicals(input_path)
    print(f"  Found {len(values)} unique EQUIPMENT canonicals")

    print(f"Embedding with all-MiniLM-L6-v2...")
    t0 = time.time()
    embeddings = embed_values(values)
    print(f"  Embedded in {time.time() - t0:.1f}s")

    print(f"Clustering at cosine >= {args.threshold}...")
    clusters = greedy_cluster(values, embeddings, threshold=args.threshold)
    merge_df = build_merge_map(clusters)

    print(f"  Clusters found: {len(clusters)}")
    print(f"  Total merges: {len(merge_df)}")
    print(f"  Unique canonicals after merge: {len(values) - len(merge_df)}")

    merge_df.to_csv(output_path, index=False)
    print(f"  Merge map saved to {output_path}")

    # Show sample clusters
    if clusters:
        print(f"\n  Sample clusters (top 10 by size):")
        for rep, members, sim in sorted(clusters, key=lambda c: -len(c[1]))[:10]:
            others = [m for m in members if m != rep][:3]
            suffix = f" +{len(members) - 4} more" if len(members) > 4 else ""
            print(f"    [{len(members)}] {rep!r} <- {others}{suffix}")

    if args.apply:
        if not args.entities_parquet or not args.relations_parquet:
            print("\nERROR: --apply requires --entities-parquet and --relations-parquet")
            return

        print(f"\nApplying {len(merge_df)} merges...")
        ent_df, rel_df, stats = apply_merges(
            merge_df,
            Path(args.entities_parquet),
            Path(args.relations_parquet),
        )
        # Overwrite in place
        ent_df.to_parquet(args.entities_parquet, index=False)
        rel_df.to_parquet(args.relations_parquet, index=False)
        print(f"  Merges applied: {stats['merges_applied']}")
        print(f"  Entities deduped: {stats['entities_deduped']}")
        print(f"  Relations deduped: {stats['relations_deduped']}")
        print(f"  Final entities: {stats['final_entities']:,}")
        print(f"  Final relations: {stats['final_relations']:,}")


if __name__ == "__main__":
    main()
