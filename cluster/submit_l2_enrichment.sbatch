#!/bin/bash
#SBATCH --job-name=l2_enrich
#SBATCH --output=slurm_output/l2_enrich_%A_%a.out
#SBATCH --error=slurm_output/l2_enrich_%A_%a.err
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=08:00:00
#SBATCH --partition=commons
#SBATCH --gres=gpu:ampere:1
#SBATCH --array=0-3

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${REPO_ROOT}"

mkdir -p slurm_output

# ── Load modules ─────────────────────────────────────────────────────────
module purge
module load GCC/13.2.0
module load CUDA/12.6.0

# Ollama binary (installed by setup_cluster_env.sh with INSTALL_OLLAMA=1)
export PATH="${WORK:-$HOME}/bin:${PATH}"

# ── Configuration ────────────────────────────────────────────────────────
: "${NODES_CSV:?Set NODES_CSV to nodes CSV or Parquet path}"
: "${EDGES_CSV:?Set EDGES_CSV to edges CSV or Parquet path}"
: "${METADATA_CSV:?Set METADATA_CSV to metadata CSV or Parquet path (with narratives)}"

MODEL="${MODEL:-qwen3:8b}"
PROMPT_VARIANT="${PROMPT_VARIANT:-full}"
OUTPUT_DIR="${OUTPUT_DIR:-output/l2}"
TEMPERATURE="${TEMPERATURE:-0.1}"
TIMEOUT_SEC="${TIMEOUT_SEC:-120}"
MAX_RETRIES="${MAX_RETRIES:-2}"
NUM_SHARDS="${NUM_SHARDS:-4}"
RESUME="${RESUME:-1}"
PYTHON_BIN="${PYTHON_BIN:-${WORK:-.}/.venv_cluster/bin/python}"
OLLAMA_HOST="${OLLAMA_HOST:-http://127.0.0.1:11434}"

shard_index="${SLURM_ARRAY_TASK_ID:-0}"

is_truthy() {
  case "$(printf '%s' "$1" | tr '[:upper:]' '[:lower:]')" in
    1|true|yes|y) return 0 ;;
    *) return 1 ;;
  esac
}

# ── Start Ollama server ─────────────────────────────────────────────────
echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] Starting Ollama server..."
ollama serve &
OLLAMA_PID=$!

# Health check: wait for Ollama to be ready
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

# Conditional pull: only pull if model is not already available
if ! ollama list | grep -q "${MODEL}"; then
  echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] Pulling model: ${MODEL}"
  ollama pull "${MODEL}"
else
  echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] Model already available: ${MODEL}"
fi

# ── Run L2 enrichment ───────────────────────────────────────────────────
cmd=(
  "${PYTHON_BIN}" "pipeline_v2/enrichment/run_l2_enrichment.py"
  "--nodes-csv" "${NODES_CSV}"
  "--edges-csv" "${EDGES_CSV}"
  "--metadata-csv" "${METADATA_CSV}"
  "--output-dir" "${OUTPUT_DIR}/shard_${shard_index}"
  "--model" "${MODEL}"
  "--host" "${OLLAMA_HOST}"
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

# Clean up Ollama
kill "${OLLAMA_PID}" 2>/dev/null || true
