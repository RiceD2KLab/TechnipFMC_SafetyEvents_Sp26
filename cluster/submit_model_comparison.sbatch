#!/bin/bash
#SBATCH --job-name=l2_compare
#SBATCH --output=slurm_output/l2_compare_%A_%a.out
#SBATCH --error=slurm_output/l2_compare_%A_%a.err
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=48G
#SBATCH --time=04:00:00
#SBATCH --partition=commons
#SBATCH --gres=gpu:1
#SBATCH --exclusive
#SBATCH --array=0-2

# ── Model comparison: 3 models x 500-record subset x full prompt ────
#
# Supports two backends via BACKEND env var:
#   BACKEND=ollama (default)  — uses Ollama server + Ollama model tags
#   BACKEND=vllm              — uses vLLM OpenAI-compat server + HF model IDs
#
# Additional env vars:
#   OUTPUT_BASE  — override output directory base
#
# Usage:
#   sbatch cluster/submit_model_comparison.sbatch                  # Ollama (all 3)
#   BACKEND=vllm sbatch cluster/submit_model_comparison.sbatch     # vLLM (all 3)
#   sbatch --array=1-2 cluster/submit_model_comparison.sbatch      # Qwen 3.5 only
#
# Array index maps to model:
#   0 = qwen3:30b-a3b / Qwen/Qwen3-30B-A3B-GPTQ-Int4     (baseline MoE)
#   1 = qwen3.5:9b    / Qwen/Qwen3.5-9B                   (dense 9B)
#   2 = qwen3.5:35b-a3b / Qwen/Qwen3.5-35B-A3B-GPTQ-Int4 (newer MoE)

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

# ── Backend selection ────────────────────────────────────────────────────
BACKEND="${BACKEND:-ollama}"

# ── Data paths (same as production run) ──────────────────────────────────
NODES_CSV="${NODES_CSV:-pipeline_v2/outputs/entities.parquet}"
EDGES_CSV="${EDGES_CSV:-pipeline_v2/outputs/relations.parquet}"
METADATA_CSV="${METADATA_CSV:-pipeline_v2/outputs/metadata_parsed.parquet}"
SUBSET_CSV="${SUBSET_CSV:-comparison_subset_500.csv}"

TEMPERATURE="${TEMPERATURE:-0.3}"
TIMEOUT_SEC="${TIMEOUT_SEC:-300}"
MAX_RETRIES="${MAX_RETRIES:-2}"

idx="${SLURM_ARRAY_TASK_ID:-0}"

# ── Model selection by array index (per backend) ────────────────────────
if [ "${BACKEND}" = "vllm" ]; then
  MODELS=(
    "Qwen/Qwen3-30B-A3B-GPTQ-Int4"
    "Qwen/Qwen3.5-9B"
    "Qwen/Qwen3.5-35B-A3B-GPTQ-Int4"
  )
  TAGS=("qwen3_30b_baseline_vllm" "qwen35_9b_dense_vllm" "qwen35_35b_moe_vllm")
  PYTHON_BIN="${PYTHON_BIN:-${SCRATCH_BASE}/.venv_vllm/bin/python}"
  OUTPUT_BASE="${OUTPUT_BASE:-output/l2/comparison_vllm}"
else
  MODELS=("qwen3:30b-a3b" "qwen3.5:9b" "qwen3.5:35b-a3b")
  TAGS=("qwen3_30b_baseline" "qwen35_9b_dense" "qwen35_35b_moe")
  PYTHON_BIN="${PYTHON_BIN:-${SCRATCH_BASE}/.venv_cluster/bin/python}"
  OUTPUT_BASE="${OUTPUT_BASE:-output/l2/comparison}"
fi

MODEL="${MODELS[$idx]}"
TAG="${TAGS[$idx]}"
OUTPUT_DIR="${OUTPUT_BASE}/${TAG}"

# ── Server startup ───────────────────────────────────────────────────────

start_ollama() {
  export PATH="${SCRATCH_BASE}/bin:${PATH}"
  export LD_LIBRARY_PATH="${SCRATCH_BASE}/ollama_install/lib/ollama:${LD_LIBRARY_PATH:-}"

  OLLAMA_PORT="$((11434 + idx))"
  HOST="http://127.0.0.1:${OLLAMA_PORT}"
  OLLAMA_MODELS="${SCRATCH_BASE}/.ollama/models"

  export OLLAMA_MODELS OLLAMA_HOST="${HOST}" OLLAMA_NUM_PARALLEL=1

  echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] Model comparison (ollama): ${MODEL} (${TAG})"
  echo "  HOST=${HOST}"
  echo "  GPU: $(nvidia-smi --query-gpu=name --format=csv,noheader 2>/dev/null || echo 'none')"

  ollama serve &
  SERVER_PID=$!

  for i in $(seq 1 30); do
    if curl -sf "${HOST}/api/tags" > /dev/null 2>&1; then
      echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] Ollama server ready (attempt ${i})"
      break
    fi
    if [ "$i" -eq 30 ]; then
      echo "ERROR: Ollama server failed to start after 30 attempts" >&2
      exit 1
    fi
    sleep 2
  done

  if ! ollama list | grep -q "${MODEL}"; then
    echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] Pulling model: ${MODEL}"
    ollama pull "${MODEL}"
  else
    echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] Model already available: ${MODEL}"
  fi
}

start_vllm() {
  VLLM_PORT="$((8000 + idx))"
  HOST="http://127.0.0.1:${VLLM_PORT}"
  VLLM_MAX_MODEL_LEN="${VLLM_MAX_MODEL_LEN:-8192}"
  VLLM_GPU_UTIL="${VLLM_GPU_UTIL:-0.85}"

  export HF_HOME="${SCRATCH_BASE}/.cache/huggingface"
  mkdir -p "${HF_HOME}"

  echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] Model comparison (vllm): ${MODEL} (${TAG})"
  echo "  HOST=${HOST}"
  echo "  MAX_MODEL_LEN=${VLLM_MAX_MODEL_LEN}"
  echo "  GPU_UTIL=${VLLM_GPU_UTIL}"
  echo "  GPU: $(nvidia-smi --query-gpu=name,memory.total --format=csv,noheader 2>/dev/null || echo 'none')"

  "${PYTHON_BIN}" -m vllm.entrypoints.openai.api_server \
    --model "${MODEL}" \
    --max-model-len "${VLLM_MAX_MODEL_LEN}" \
    --gpu-memory-utilization "${VLLM_GPU_UTIL}" \
    --enforce-eager \
    --port "${VLLM_PORT}" &
  SERVER_PID=$!

  echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] Waiting for vLLM to load model..."
  for i in $(seq 1 300); do
    if curl -sf "${HOST}/v1/models" > /dev/null 2>&1; then
      echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] vLLM server ready (attempt ${i})"
      break
    fi
    if [ "$i" -eq 300 ]; then
      echo "ERROR: vLLM server failed to start after 300 attempts (10 min)" >&2
      kill "${SERVER_PID}" 2>/dev/null || true
      exit 1
    fi
    sleep 2
  done
}

if [ "${BACKEND}" = "vllm" ]; then
  start_vllm
else
  start_ollama
fi

echo "  SUBSET_CSV=${SUBSET_CSV}"

# ── Run L2 enrichment on subset ──────────────────────────────────────────
cmd=(
  "${PYTHON_BIN}" "pipeline_v2/enrichment/run_l2_enrichment.py"
  "--nodes-csv" "${NODES_CSV}"
  "--edges-csv" "${EDGES_CSV}"
  "--metadata-csv" "${METADATA_CSV}"
  "--output-dir" "${OUTPUT_DIR}"
  "--model" "${MODEL}"
  "--host" "${HOST}"
  "--backend" "${BACKEND}"
  "--temperature" "${TEMPERATURE}"
  "--prompt-variant" "full"
  "--subset-csv" "${SUBSET_CSV}"
  "--num-shards" "1"
  "--shard-index" "0"
  "--timeout-sec" "${TIMEOUT_SEC}"
  "--max-retries" "${MAX_RETRIES}"
  "--resume"
)

echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] Starting L2 enrichment: ${MODEL}"
echo "Command: ${cmd[*]}"
"${cmd[@]}"

echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] ${TAG} complete"

kill "${SERVER_PID}" 2>/dev/null || true
