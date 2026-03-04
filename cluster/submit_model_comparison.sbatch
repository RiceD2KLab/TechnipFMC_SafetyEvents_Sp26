#!/bin/bash
#SBATCH --job-name=l2_compare
#SBATCH --output=slurm_output/l2_compare_%A_%a.out
#SBATCH --error=slurm_output/l2_compare_%A_%a.err
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=04:00:00
#SBATCH --partition=commons
#SBATCH --gres=gpu:1
#SBATCH --exclusive
#SBATCH --array=0-2

# ── Model comparison: 3 models x 500-record subset x full_v2 prompt ────
# Array index maps to model:
#   0 = qwen3:30b-a3b     (baseline, 18GB MoE)
#   1 = qwen3.5:9b         (dense, 6.6GB)
#   2 = qwen3.5:35b-a3b    (newer MoE, 24GB)

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

export PATH="${SCRATCH_BASE}/bin:${PATH}"
export LD_LIBRARY_PATH="${SCRATCH_BASE}/ollama_install/lib/ollama:${LD_LIBRARY_PATH:-}"

# ── Data paths (same as production run) ──────────────────────────────────
NODES_CSV="${NODES_CSV:-pipeline_v2/outputs/entities.parquet}"
EDGES_CSV="${EDGES_CSV:-pipeline_v2/outputs/relations.parquet}"
METADATA_CSV="${METADATA_CSV:-pipeline_v2/outputs/metadata_parsed.parquet}"
SUBSET_CSV="${SUBSET_CSV:-comparison_subset_500.csv}"
PYTHON_BIN="${PYTHON_BIN:-${SCRATCH_BASE}/.venv_cluster/bin/python}"

# ── Model selection by array index ───────────────────────────────────────
MODELS=("qwen3:30b-a3b" "qwen3.5:9b" "qwen3.5:35b-a3b")
TAGS=("qwen3_30b_baseline" "qwen35_9b_dense" "qwen35_35b_moe")

idx="${SLURM_ARRAY_TASK_ID:-0}"
MODEL="${MODELS[$idx]}"
TAG="${TAGS[$idx]}"
OUTPUT_DIR="output/l2/comparison/${TAG}"

TEMPERATURE="${TEMPERATURE:-0.3}"
TIMEOUT_SEC="${TIMEOUT_SEC:-300}"
MAX_RETRIES="${MAX_RETRIES:-2}"

# Unique port per array task
OLLAMA_PORT="$((11434 + idx))"
OLLAMA_HOST="http://127.0.0.1:${OLLAMA_PORT}"
OLLAMA_MODELS="${SCRATCH_BASE}/.ollama/models"

export OLLAMA_MODELS
export OLLAMA_HOST
export OLLAMA_NUM_PARALLEL=1

# ── Start Ollama server ─────────────────────────────────────────────────
echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] Model comparison: ${MODEL} (${TAG})"
echo "  OLLAMA_HOST=${OLLAMA_HOST}"
echo "  SUBSET_CSV=${SUBSET_CSV}"
echo "  GPU: $(nvidia-smi --query-gpu=name --format=csv,noheader 2>/dev/null || echo 'none')"
ollama serve &
OLLAMA_PID=$!

for i in $(seq 1 30); do
  if curl -sf "${OLLAMA_HOST}/api/tags" > /dev/null 2>&1; then
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

# ── Run L2 enrichment on subset ──────────────────────────────────────────
cmd=(
  "${PYTHON_BIN}" "pipeline_v2/enrichment/run_l2_enrichment.py"
  "--nodes-csv" "${NODES_CSV}"
  "--edges-csv" "${EDGES_CSV}"
  "--metadata-csv" "${METADATA_CSV}"
  "--output-dir" "${OUTPUT_DIR}"
  "--model" "${MODEL}"
  "--host" "${OLLAMA_HOST}"
  "--temperature" "${TEMPERATURE}"
  "--prompt-variant" "full_v2"
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

kill "${OLLAMA_PID}" 2>/dev/null || true
