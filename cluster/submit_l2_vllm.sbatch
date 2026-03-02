#!/bin/bash
#SBATCH --job-name=l2_vllm
#SBATCH --output=slurm_output/l2_vllm_%A_%a.out
#SBATCH --error=slurm_output/l2_vllm_%A_%a.err
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=48G
#SBATCH --time=24:00:00
#SBATCH --partition=commons
#SBATCH --gres=gpu:1
#SBATCH --exclusive
#SBATCH --array=0-3

set -euo pipefail

# ── Paths ─────────────────────────────────────────────────────────────────
SCRATCH_BASE="${SHARED_SCRATCH}/${USER}"
REPO_ROOT="${SLURM_SUBMIT_DIR:-/rhf/allocations/dsci435/fmcsafetyevents_sp26/TechnipFMC_SafetyEvents}"
cd "${REPO_ROOT}"

mkdir -p slurm_output

# ── Load modules ─────────────────────────────────────────────────────────
module purge
module load GCC/13.2.0
module load CUDA/12.6.0

# ── Configuration ────────────────────────────────────────────────────────
: "${NODES_CSV:?Set NODES_CSV to nodes CSV or Parquet path}"
: "${EDGES_CSV:?Set EDGES_CSV to edges CSV or Parquet path}"
: "${METADATA_CSV:?Set METADATA_CSV to metadata CSV or Parquet path (with narratives)}"

MODEL="${MODEL:-Qwen/Qwen3-30B-A3B-GPTQ-Int4}"
PROMPT_VARIANT="${PROMPT_VARIANT:-full}"
OUTPUT_DIR="${OUTPUT_DIR:-output/l2_vllm}"
TEMPERATURE="${TEMPERATURE:-0.1}"
TIMEOUT_SEC="${TIMEOUT_SEC:-120}"
MAX_RETRIES="${MAX_RETRIES:-2}"
NUM_SHARDS="${NUM_SHARDS:-4}"
RESUME="${RESUME:-1}"
PYTHON_BIN="${PYTHON_BIN:-${SCRATCH_BASE}/.venv_vllm/bin/python}"
# Unique port per array task to avoid collisions when co-located
VLLM_PORT="${VLLM_PORT:-$((8000 + ${SLURM_ARRAY_TASK_ID:-0}))}"
VLLM_HOST="${VLLM_HOST:-http://127.0.0.1:${VLLM_PORT}}"
VLLM_MAX_MODEL_LEN="${VLLM_MAX_MODEL_LEN:-4096}"
VLLM_GPU_UTIL="${VLLM_GPU_UTIL:-0.90}"

shard_index="${SLURM_ARRAY_TASK_ID:-0}"

is_truthy() {
  case "$(printf '%s' "$1" | tr '[:upper:]' '[:lower:]')" in
    1|true|yes|y) return 0 ;;
    *) return 1 ;;
  esac
}

# ── Start vLLM server ────────────────────────────────────────────────────
echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] Starting vLLM server..."
echo "  VLLM_HOST=${VLLM_HOST}"
echo "  MODEL=${MODEL}"
echo "  MAX_MODEL_LEN=${VLLM_MAX_MODEL_LEN}"
echo "  GPU_UTIL=${VLLM_GPU_UTIL}"
echo "  GPU: $(nvidia-smi --query-gpu=name,memory.total --format=csv,noheader 2>/dev/null || echo 'none')"

# HuggingFace cache on scratch (not home)
export HF_HOME="${SCRATCH_BASE}/.cache/huggingface"
mkdir -p "${HF_HOME}"

"${PYTHON_BIN}" -m vllm.entrypoints.openai.api_server \
  --model "${MODEL}" \
  --max-model-len "${VLLM_MAX_MODEL_LEN}" \
  --gpu-memory-utilization "${VLLM_GPU_UTIL}" \
  --port "${VLLM_PORT}" &
VLLM_PID=$!

# Health check: wait for vLLM to load model and start serving
echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] Waiting for vLLM to load model..."
for i in $(seq 1 300); do
  if curl -sf "${VLLM_HOST}/v1/models" > /dev/null 2>&1; then
    echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] vLLM server ready (attempt ${i})"
    break
  fi
  if [ "$i" -eq 300 ]; then
    echo "ERROR: vLLM server failed to start after 300 attempts (10 min)" >&2
    kill "${VLLM_PID}" 2>/dev/null || true
    exit 1
  fi
  sleep 2
done

# ── Run L2 enrichment ───────────────────────────────────────────────────
cmd=(
  "${PYTHON_BIN}" "pipeline_v2/enrichment/run_l2_enrichment.py"
  "--nodes-csv" "${NODES_CSV}"
  "--edges-csv" "${EDGES_CSV}"
  "--metadata-csv" "${METADATA_CSV}"
  "--output-dir" "${OUTPUT_DIR}/shard_${shard_index}"
  "--model" "${MODEL}"
  "--host" "${VLLM_HOST}"
  "--backend" "vllm"
  "--temperature" "${TEMPERATURE}"
  "--prompt-variant" "${PROMPT_VARIANT}"
  "--shard-index" "${shard_index}"
  "--num-shards" "${NUM_SHARDS}"
  "--timeout-sec" "${TIMEOUT_SEC}"
  "--max-retries" "${MAX_RETRIES}"
)

if is_truthy "${RESUME}"; then
  cmd+=("--resume")
else
  cmd+=("--no-resume")
fi

echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] Starting L2 enrichment (shard ${shard_index}/${NUM_SHARDS})"
echo "Command: ${cmd[*]}"
"${cmd[@]}"

echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] Shard ${shard_index} complete"

# Clean up vLLM
kill "${VLLM_PID}" 2>/dev/null || true
