# Rice NOTS Cluster Setup

Scripts for running the TechnipFMC Safety pipeline on the Rice NOTS HPC cluster.

## Prerequisites

- SSH access to `nots.rice.edu`
- Team allocation at `/rhf/allocations/dsci435/fmcsafetyevents_sp26/`

## Storage Layout

| Path | Visible from | Persistent | Use |
|------|-------------|-----------|-----|
| `/rhf/allocations/dsci435/fmcsafetyevents_sp26/` | Login + compute | Yes | Repo, data, outputs |
| `$SHARED_SCRATCH/$USER/` | Login + compute | No (14-day purge) | Venv, Ollama, model cache |
| `$HOME` | Login + compute | Yes | Dotfiles only (10GB limit) |
| `$WORK` | Login only | Yes | Not usable for compute jobs |

## Environment Setup

From a login node:

```bash
cd /rhf/allocations/dsci435/fmcsafetyevents_sp26/TechnipFMC_SafetyEvents
INSTALL_OLLAMA=1 bash cluster/setup_cluster_env.sh
```

This installs:
- Python venv at `$SHARED_SCRATCH/$USER/.venv_cluster` with `requirements_cluster.txt`
- PyTorch (CUDA 12.6)
- Ollama binary + symlink (if `INSTALL_OLLAMA=1`)

If scratch gets purged, re-run the script to rebuild.

### Module loads

```bash
module load GCC/13.2.0 CUDA/12.6.0
```

## Files

| File | Purpose |
|------|---------|
| `setup_cluster_env.sh` | One-time environment setup (venv, torch, ollama) |
| `submit_l2_enrichment.sbatch` | L2 causal enrichment via Ollama (4-shard array, qwen3:30b-a3b) |
| `submit_l2_vllm.sbatch` | L2 enrichment via vLLM backend (4-shard array, Qwen3-30B-A3B-GPTQ-Int4) |
| `build_transfer_bundle.py` | Local code-only tarball builder for refreshing the NOTS repo copy |
| `run_working_set_30k.sh` | Legacy 30k working-set wrapper retained for audit/reproduction |

## L2 Enrichment

The production L2 run uses 4-shard SLURM arrays with `--exclusive` to avoid GPU contention:

```bash
sbatch --export=ALL,\
NODES_CSV=pipeline/er_execution/outputs/entities_post_er_loc_dedup.parquet,\
EDGES_CSV=pipeline/er_execution/outputs/relations_post_er_loc_dedup.parquet,\
METADATA_CSV=pipeline/outputs/metadata_parsed.parquet,\
OUTPUT_DIR=output/l2 \
cluster/submit_l2_enrichment.sbatch
```

Key configuration (set in the sbatch file):
- **Model:** qwen3:30b-a3b (Ollama) or Qwen/Qwen3-30B-A3B-GPTQ-Int4 (vLLM)
- **Shards:** 4 (array 0-3), each gets `--exclusive` node
- **Wall time:** 24h
- **GPU:** `gpu:1` (any available type)
- **Resume:** Enabled — safe to restart interrupted jobs
- **Per-shard ports:** Base port + `SLURM_ARRAY_TASK_ID` to avoid bind conflicts

Output lands in `output/l2/shard_*/`. After all shards complete, merge with:

```bash
python pipeline/enrichment/merge_l2_edges.py \
  --l2-dir output/l2 \
  --entities-parquet pipeline/er_execution/outputs/entities_post_er_loc_dedup.parquet \
  --relations-parquet pipeline/er_execution/outputs/relations_post_er_loc_dedup.parquet \
  --output-dir pipeline/outputs/merged
```

The current dashboard/benchmark graph is the L1+L2 merged graph copied into
`pipeline/outputs/`.

### vLLM alternative

```bash
sbatch --export=ALL,\
NODES_CSV=pipeline/er_execution/outputs/entities_post_er_loc_dedup.parquet,\
EDGES_CSV=pipeline/er_execution/outputs/relations_post_er_loc_dedup.parquet,\
METADATA_CSV=pipeline/outputs/metadata_parsed.parquet,\
OUTPUT_DIR=output/l2_vllm \
cluster/submit_l2_vllm.sbatch
```

Same shard/resume behavior, uses vLLM's OpenAI-compatible server instead of Ollama.
Both backends write identical output format — they're interchangeable.

## GPU Selection

Use `gpu:1` (any GPU). Specific GPU types have massive queue imbalance on NOTS:
- Lovelace queue: 2400+ pending
- Volta / generic: ~10 pending

## Performance Notes

- **qwen3:30b-a3b on exclusive L40S:** ~25s/record
- **Without `--exclusive`:** Shards co-locate → port collisions + GPU contention → ~75s/record (3x slower)
- **L2 data:** 16,872 qualifying incidents (>=2 sentences + >=2 entity types) out of 19,820 total
