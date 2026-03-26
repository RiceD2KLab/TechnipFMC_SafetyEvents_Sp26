# Cluster Execution Toolkit

## Goal
Run GLiNER extraction once, reuse generated parquet artifacts for downstream Splink/classifier/LLM ablations, and keep outputs reproducible under `runs/<run_label>/<variant_id>/...`.

Documentation index: [`docs/INDEX.md`](../docs/INDEX.md) | Full pipeline runbook: [`docs/operational_runbook.md`](../docs/operational_runbook.md)

## Stage Selection
- `cluster/launch_cluster_run.py` is the launcher for explicit stages:
  - `gliner`
  - `sidecar`
  - `splink`
  - `ablation`
- `cluster/run_working_set_30k.sh` is the deployment orchestrator for working-set execution:
  - `STAGE=gliner` (GLiNER only + strict checks)
  - `STAGE=sidecar` (sidecar only + strict checks against source GLiNER stage)
  - `STAGE=both` (GLiNER then sidecar, then strict checks)

## Decision Source
- Use `cluster/PRODUCTION_DECISIONS.md` as the authoritative policy.
- Frozen defaults:
  - GLiNER: `urchade/gliner_large-v2.1`, threshold `0.40`
  - Splink publish threshold: `0.95` (`0.90` diagnostic only)
- Enrichment Tier B model: `Qwen3 8B`
- Enrichment gates: JSON validity `>= 0.99`, evidence coverage `>= 0.90`
- Enrichment runner supports shard/merge for OSS (`ollama`) execution.

## Setup
```bash
bash cluster/setup_cluster_env.sh
```

## Local Wrapper
```bash
DATA_CSV=/path/to/incidents.csv SAMPLE_SIZE=1000 RUN_LABEL=wknd_eval_canary ALL=0 VARIANT_ID=baseline bash cluster/run_gliner_local.sh
```

Dev sample quick start (uses `input/incidents.csv` automatically):
```bash
USE_DEV_SAMPLE=1 ALL=1 RUN_LABEL=devsample_full VARIANT_ID=baseline PYTHON_BIN=.venv/bin/python bash cluster/run_gliner_local.sh
```

Optional GLiNER windowing/batching knobs:
- `WINDOW_SIZE` (default `2500`)
- `WINDOW_OVERLAP` (default `300`)
- `BATCH_SIZE` (default `64`)

Working-set orchestration (30k, strict drift checks, no gold labels required):
```bash
STAGE=gliner DATA_CSV=/path/to/incidents.csv SAMPLE_SIZE=30000 RUN_LABEL=wknd_eval_30k VARIANT_ID=baseline PYTHON_BIN=.venv/bin/python bash cluster/run_working_set_30k.sh
```
This script runs `scripts/selfcheck_schema_constants.py` before stage execution.

## SLURM Wrappers
Canary:
```bash
sbatch --export=ALL,DATA_CSV=/path/to/incidents.csv,SAMPLE_SIZE=1000,RUN_LABEL=wknd_eval_canary,ALL=0,VARIANT_ID=baseline cluster/submit_gliner_run.sbatch
```

Dev sample on cluster:
```bash
sbatch --export=ALL,USE_DEV_SAMPLE=1,RUN_LABEL=devsample_full,ALL=1,VARIANT_ID=baseline,PYTHON_BIN=.venv/bin/python cluster/submit_gliner_run.sbatch
```

10k:
```bash
sbatch --export=ALL,DATA_CSV=/path/to/incidents.csv,SAMPLE_SIZE=10000,RUN_LABEL=wknd_eval_10k,ALL=0,VARIANT_ID=baseline cluster/submit_gliner_run.sbatch
```

Full:
```bash
sbatch --export=ALL,DATA_CSV=/path/to/incidents.csv,SAMPLE_SIZE=1000,RUN_LABEL=wknd_eval_full,ALL=1,VARIANT_ID=baseline cluster/submit_gliner_run.sbatch
```

Splink pilot from reusable GLiNER parquet:
```bash
export RUN_LABEL=wknd_eval_full
export VARIANT_ID=baseline
export SOURCE_VARIANT_ID=baseline
export SAMPLE_SIZE=30000
export THRESHOLDS="0.95,0.90"
sbatch --export=ALL,RUN_LABEL,VARIANT_ID,SOURCE_VARIANT_ID,SAMPLE_SIZE,THRESHOLDS cluster/submit_splink_pilot.sbatch
```

Direct sidecar launch (no variant hooks required):
```bash
python3 cluster/launch_cluster_run.py sidecar \
  --run-label wknd_eval_30k \
  --variant-id llm_only \
  --source-variant-id baseline \
  --backend mock \
  --num-shards 1 \
  --shard-index 0 \
  --incidents-per-batch 16 \
  --resume \
  --allow-existing-run
```

Ablation scorecard:
```bash
sbatch --export=ALL,RUN_LABEL=wknd_eval_full,RUNS_CSV=/path/to/ablation_runs.csv,VARIANT_ID=scorecard,FAIL_ON_SCHEMA_DRIFT=1 cluster/submit_ablation_scorecard.sbatch
```

Graph artifact ablation scorecard (topology + schema diagnostics):
```bash
BASELINE_DIR=/path/to/runs/wknd_eval_full/baseline/gliner \
GLINER_ONLY_DIR=/path/to/runs/wknd_eval_full/gliner_only/gliner \
GLINER_RULES_DIR=/path/to/runs/wknd_eval_full/gliner_rules/gliner \
GLINER_RULES_CLASSIFIER_DIR=/path/to/runs/wknd_eval_full/classifier_only/classifier \
OUTPUT_DIR=runs/wknd_eval_full/scorecard_graph \
bash cluster/run_ablation_scorecard_graph.sh
```

Classifier / LLM hooks (reuses baseline GLiNER artifacts):
```bash
export RUN_LABEL=wknd_eval_full
export VARIANT_ID=classifier_only
export SOURCE_VARIANT_ID=baseline
export CLASSIFIER_CMD="python3 cluster/run_classifier_variant.py --source-gliner-dir {source_gliner_dir} --out-dir {classifier_dir} --promote-threshold 0.75 --suppress-threshold 0.25"
sbatch --export=ALL,RUN_LABEL,VARIANT_ID,SOURCE_VARIANT_ID,CLASSIFIER_CMD cluster/submit_variant_hooks.sbatch
```

```bash
export RUN_LABEL=wknd_eval_full
export VARIANT_ID=llm_only
export SOURCE_VARIANT_ID=baseline
export LLM_CMD="python3 cluster/run_enrichment_variant.py --source-gliner-dir {source_gliner_dir} --out-dir {llm_dir} {data_csv_arg} --backend ollama --tier-b-model qwen3:8b --tier-c-model mistral-small:latest --route-threshold-a 0.80 --route-threshold-b 0.55 --temperature 0.1 --max-incidents 0"
sbatch --export=ALL,RUN_LABEL,VARIANT_ID,SOURCE_VARIANT_ID,LLM_CMD cluster/submit_variant_hooks.sbatch
```

```bash
export RUN_LABEL=wknd_eval_full
export VARIANT_ID=classifier_plus_llm
export SOURCE_VARIANT_ID=baseline
export CLASSIFIER_CMD="python3 cluster/run_classifier_variant.py --source-gliner-dir {source_gliner_dir} --out-dir {classifier_dir} --promote-threshold 0.75 --suppress-threshold 0.25"
export LLM_CMD="python3 cluster/run_enrichment_variant.py --source-gliner-dir {source_gliner_dir} --out-dir {llm_dir} {data_csv_arg} --backend ollama --tier-b-model qwen3:8b --tier-c-model mistral-small:latest --route-threshold-a 0.80 --route-threshold-b 0.55 --temperature 0.1 --max-incidents 0"
sbatch --export=ALL,RUN_LABEL,VARIANT_ID,SOURCE_VARIANT_ID,CLASSIFIER_CMD,LLM_CMD cluster/submit_variant_hooks.sbatch
```

Sharded enrichment directly (recommended on NOTS for speed):
```bash
# 1) Launch shard array (example: 8 shards)
sbatch --array=0-7 --export=ALL,RUN_LABEL=wknd_eval_full,SOURCE_VARIANT_ID=baseline,VARIANT_ID=llm_only,NUM_SHARDS=8,BACKEND=ollama,TIER_B_MODEL=qwen3:8b,TIER_C_MODEL=mistral-small:latest,DATA_CSV=/path/to/incidents.csv,INCIDENTS_PER_BATCH=16,RESUME=1 cluster/submit_enrichment_sharded.sbatch
```

```bash
# 2) Merge shard outputs after array completes
sbatch --dependency=afterok:<ARRAY_JOB_ID> --export=ALL,MODE=merge,RUN_LABEL=wknd_eval_full,SOURCE_VARIANT_ID=baseline,VARIANT_ID=llm_only,NUM_SHARDS=8 cluster/submit_enrichment_sharded.sbatch
```

Dev sample sharded enrichment:
```bash
sbatch --array=0-7 --export=ALL,USE_DEV_SAMPLE=1,RUN_LABEL=devsample_full,SOURCE_VARIANT_ID=baseline,VARIANT_ID=llm_only,NUM_SHARDS=8,BACKEND=ollama,PYTHON_BIN=.venv/bin/python cluster/submit_enrichment_sharded.sbatch
```

Hosted-model comparison note (future):
- Bedrock/Nova comparison is intentionally not wired in the active runner path for this upload package.
- Keep current cluster path OSS-only for clean reproducibility and minimal operational dependencies.

## Reuse Behavior
- GLiNER wrapper writes:
  - `incident_triples.csv`
  - `entities_filtered.parquet`
  - `relationships_filtered.parquet`
  - plus native `entities.csv`, `relations.csv`, `triples.csv`, `metrics.json`, `pipeline_report.md`
- Re-running the same `RUN_LABEL` + `VARIANT_ID` skips extraction if the full artifact set exists.
- Use `FORCE_RERUN=1` (SBATCH/local env var) or `--force-rerun` to force regeneration.
- Variant hooks never regenerate GLiNER artifacts; they read from `runs/<RUN_LABEL>/<SOURCE_VARIANT_ID>/gliner/`.

## Timing Outputs
- GLiNER/Splink/Ablation manifests now include:
  - `stage_started_at_utc`
  - `stage_finished_at_utc`
  - `stage_duration_seconds`
- Variant hook manifest (`metadata/variant_hooks_manifest.json`) now includes per-stage timing under:
  - `classifier.duration_seconds`
  - `llm.duration_seconds`
- Classifier metrics (`classifier_metrics.json`) includes:
  - `run_duration_seconds`
- Enrichment metrics (`enrichment_metrics.json`) include:
  - `run_started_at_utc`
  - `run_finished_at_utc`
  - `run_duration_seconds`
  - Existing LLM-call timing remains (`llm_call_seconds`, `avg_llm_call_seconds`).

## Expected Time/Cost Delta (Planning Range)
Assumptions for first-pass planning:
- 100k incidents.
- Routed to LLM: 20%-40% (Tier B+C only).
- Average prompt+response token volume per called incident: low thousands of tokens or less.

Wall-clock (order-of-magnitude):
- Local OSS, single serial worker: likely many hours to >1 day depending on call volume/model.
- Local OSS, 8-shard GPU array: typically ~4x-10x faster than serial.
- If you later reintroduce hosted APIs, throughput may improve for hard tiers, but that path is intentionally disabled in this package.

Cost:
- Local OSS on cluster: no direct per-token API charge.
- Recommendation: keep baseline and enrichment on OSS for this run; add hosted comparison as a separate follow-up branch.

## If LLM Is Slow/Unstable
- Raise routing thresholds to shrink LLM volume (`--route-threshold-a`, `--route-threshold-b`).
- Cap workload per run with `--max-incidents`.
- Lower `--incidents-per-batch` if checkpoint writes or memory pressure become bottlenecks.
- `--incidents-per-batch` is a checkpoint cadence, not a single LLM request batch.
- Keep `--temperature 0.1`.
- Use `--backend mock` for pipeline dry-runs and throughput testing without model calls.

## Packaging
Code-only transfer bundle:
```bash
python cluster/build_transfer_bundle.py --bundle-label cluster_copy_ready
```

Run-artifact bundle (includes GLiNER parquet):
```bash
python cluster/package_run_artifacts.py --run-label wknd_eval_full --variant-id baseline --include-splink
```
