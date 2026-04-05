#!/usr/bin/env python3
"""Prepare a stratified subset for multi-model L2 enrichment comparison.

Samples 500 qualifying records and prints SLURM commands for each model.

Usage:
    python pipeline/enrichment/prepare_model_comparison.py \
        --nodes-csv pipeline/outputs/entities_pre_er.parquet \
        --edges-csv pipeline/outputs/relations_pre_er.parquet \
        --metadata-csv pipeline/outputs/metadata_parsed.parquet \
        --output comparison_subset_500.csv
"""
from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def _count_sentences(text: str) -> int:
    count = 0
    for char in text:
        if char in ".!?":
            count += 1
    return max(count, 1) if text.strip() else 0


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare model comparison subset.")
    parser.add_argument("--nodes-csv", required=True)
    parser.add_argument("--edges-csv", required=True)
    parser.add_argument("--metadata-csv", required=True)
    parser.add_argument("--output", default="comparison_subset_500.csv")
    parser.add_argument("--n-samples", type=int, default=500)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    def _read(p: str) -> pd.DataFrame:
        return pd.read_parquet(p) if p.endswith(".parquet") else pd.read_csv(p, low_memory=False)

    nodes_df = _read(args.nodes_csv)
    edges_df = _read(args.edges_csv)
    metadata_df = _read(args.metadata_csv)
    metadata_df["record_no"] = metadata_df["record_no"].astype(str)

    # Find narrative column
    narrative_col = None
    for col in ("narrative", "NARRATIVE", "full_text"):
        if col in metadata_df.columns:
            narrative_col = col
            break
    if narrative_col is None:
        raise ValueError(f"No narrative column found. Columns: {list(metadata_df.columns)}")

    # Build entity type count per record
    nodes_df["entity_id"] = nodes_df["entity_id"].astype(str)
    edges_df["source"] = edges_df["source"].astype(str)
    edges_df["target"] = edges_df["target"].astype(str)
    nodes_indexed = nodes_df.set_index("entity_id", drop=False)
    nodes_indexed = nodes_indexed[~nodes_indexed.index.duplicated(keep="first")]

    qualifying = []
    for _, row in metadata_df.iterrows():
        rno = str(row["record_no"])
        narr = str(row.get(narrative_col, ""))
        if _count_sentences(narr) < 2:
            continue
        inc_id = f"INCIDENT::{rno}"
        connected = edges_df[edges_df["source"] == inc_id]["target"].tolist()
        etypes = set()
        for eid in connected:
            if eid in nodes_indexed.index:
                et = str(nodes_indexed.loc[eid].get("entity_type", ""))
                if et and et != "INCIDENT":
                    etypes.add(et)
        if len(etypes) >= 2:
            qualifying.append(rno)

    qualifying_df = metadata_df[metadata_df["record_no"].isin(qualifying)].copy()
    print(f"Qualifying records: {len(qualifying_df)}")

    # Stratified sample by incident_type if available
    n = min(args.n_samples, len(qualifying_df))
    if "incident_type" in qualifying_df.columns:
        sampled = qualifying_df.groupby("incident_type", group_keys=False).apply(
            lambda g: g.sample(
                n=max(1, int(len(g) / len(qualifying_df) * n)),
                random_state=args.seed,
            ),
            include_groups=False,
        )
        # Trim or pad to exact n
        if len(sampled) > n:
            sampled = sampled.sample(n=n, random_state=args.seed)
        elif len(sampled) < n:
            remaining = qualifying_df[~qualifying_df.index.isin(sampled.index)]
            extra = remaining.sample(n=n - len(sampled), random_state=args.seed)
            sampled = pd.concat([sampled, extra])
    else:
        sampled = qualifying_df.sample(n=n, random_state=args.seed)

    subset = sampled[["record_no"]].copy()
    subset.to_csv(args.output, index=False)
    print(f"Wrote {len(subset)} records to {args.output}")

    # Print SLURM commands
    models = [
        ("qwen3:30b-a3b", "qwen3_30b_baseline"),
        ("qwen3.5:9b", "qwen35_9b_dense"),
        ("qwen3.5:35b-a3b", "qwen35_35b_moe"),
    ]
    print("\n# SLURM commands for model comparison:")
    for model, tag in models:
        out_dir = f"output/l2/comparison/{tag}"
        print(f"""
# {model} ({tag})
srun --partition=commons --gres=gpu:1 --time=04:00:00 --mem=64G \\
  bash -c '
    export OLLAMA_HOME=$SHARED_SCRATCH/$USER/.ollama
    $SHARED_SCRATCH/$USER/bin/ollama serve &
    sleep 10
    ollama pull {model}
    python pipeline/enrichment/run_l2_enrichment.py \\
      --nodes-csv pipeline/outputs/entities_pre_er.parquet \\
      --edges-csv pipeline/outputs/relations_pre_er.parquet \\
      --metadata-csv pipeline/outputs/metadata_parsed.parquet \\
      --output-dir {out_dir} \\
      --model {model} \\
      --prompt-variant full \\
      --subset-csv {args.output} \\
      --num-shards 1
  '
""")


if __name__ == "__main__":
    main()
