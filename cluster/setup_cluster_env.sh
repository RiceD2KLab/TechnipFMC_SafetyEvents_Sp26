#!/bin/bash
# Setup Python virtual environment on Rice NOTS cluster.
#
# Run from a login node (ssh username@nots.rice.edu):
#   cd $WORK/TechnipFMC_SafetyEvents
#   INSTALL_OLLAMA=1 bash cluster/setup_cluster_env.sh
#
# NOTS storage rules:
#   $WORK        → login nodes only, persistent, 2TB group quota
#   $SHARED_SCRATCH → compute + login nodes, 14-day purge, no quota
#   $HOME        → both, but 10GB quota (too small)
#
# This script builds the venv and Ollama on $SHARED_SCRATCH so compute
# nodes can access them. If purged, re-run this script to rebuild.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${REPO_ROOT}"

# ── Configuration ────────────────────────────────────────────────────────
SCRATCH_BASE="${SHARED_SCRATCH}/${USER}"
VENV_DIR="${VENV_DIR:-${SCRATCH_BASE}/.venv_cluster}"
TORCH_VERSION="${TORCH_VERSION:-2.10.0}"
INSTALL_OLLAMA="${INSTALL_OLLAMA:-0}"

echo "=== Rice NOTS Cluster Environment Setup ==="
echo "REPO_ROOT:      ${REPO_ROOT}"
echo "SCRATCH_BASE:   ${SCRATCH_BASE}"
echo "VENV_DIR:       ${VENV_DIR}"
echo "TORCH_VERSION:  ${TORCH_VERSION}"

# ── Load modules ─────────────────────────────────────────────────────────
module purge
module load GCC/13.2.0
module load CUDA/12.6.0
module load Python/3.11.5
echo "Loaded modules:"
module list

# ── Create venv on $SHARED_SCRATCH ───────────────────────────────────────
mkdir -p "${SCRATCH_BASE}"

if [ -d "${VENV_DIR}" ]; then
  echo "Existing venv found at ${VENV_DIR}, reusing."
else
  echo "Creating venv at ${VENV_DIR}..."
  python3 -m venv "${VENV_DIR}"
fi
source "${VENV_DIR}/bin/activate"

python -m pip install --upgrade pip setuptools wheel

# ── Install PyTorch with CUDA ────────────────────────────────────────────
TORCH_INDEX_URL="https://download.pytorch.org/whl/cu126"
echo "Installing torch==${TORCH_VERSION} from ${TORCH_INDEX_URL}"
python -m pip install "torch==${TORCH_VERSION}" --index-url "${TORCH_INDEX_URL}"

# ── Install project dependencies ─────────────────────────────────────────
python -m pip install -r requirements_cluster.txt

# ── Verify ───────────────────────────────────────────────────────────────
python - <<'PY'
import torch
import transformers

print(f"torch={torch.__version__}, CUDA available={torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"  GPU: {torch.cuda.get_device_name(0)}")

assert transformers.__version__ == "4.57.3", (
    f"transformers pin mismatch: expected 4.57.3, got {transformers.__version__}"
)
print(f"transformers={transformers.__version__}")
print("Environment ready.")
PY

# ── Optional: Install Ollama for L2 enrichment ──────────────────────────
if [ "${INSTALL_OLLAMA}" = "1" ]; then
  OLLAMA_DIR="${SCRATCH_BASE}/bin"
  mkdir -p "${OLLAMA_DIR}"
  if [ -x "${OLLAMA_DIR}/ollama" ]; then
    echo "Ollama already installed at ${OLLAMA_DIR}/ollama"
  else
    echo "Installing Ollama to ${OLLAMA_DIR}..."
    curl -fsSL https://ollama.com/download/ollama-linux-amd64 -o "${OLLAMA_DIR}/ollama"
    chmod +x "${OLLAMA_DIR}/ollama"
  fi
  echo "Ollama: ${OLLAMA_DIR}/ollama"
fi

# ── Stage repo to $SHARED_SCRATCH ────────────────────────────────────────
SCRATCH_REPO="${SCRATCH_BASE}/TechnipFMC_SafetyEvents"
echo ""
echo "Syncing repo to ${SCRATCH_REPO} (compute nodes need this)..."
rsync -a --delete \
  --exclude '.git' \
  --exclude '.venv*' \
  --exclude '__pycache__' \
  --exclude '.codex_logs' \
  "${REPO_ROOT}/" "${SCRATCH_REPO}/"
echo "Repo staged: ${SCRATCH_REPO}"

echo ""
echo "=== Setup complete ==="
echo ""
echo "Paths for job submission (compute-visible):"
echo "  PYTHON_BIN:  ${VENV_DIR}/bin/python"
echo "  REPO:        ${SCRATCH_REPO}"
echo "  OLLAMA:      ${SCRATCH_BASE}/bin/ollama"
echo ""
echo "To submit L2 enrichment:"
echo "  cd ${SCRATCH_REPO}"
echo "  NODES_CSV=pipeline_v2/outputs/entities.parquet \\"
echo "  EDGES_CSV=pipeline_v2/outputs/relations.parquet \\"
echo "  METADATA_CSV=pipeline_v2/outputs/metadata_parsed.parquet \\"
echo "  sbatch cluster/submit_l2_enrichment.sbatch"
echo ""
echo "After jobs finish, copy results back to \$WORK:"
echo "  cp -r ${SCRATCH_REPO}/output/l2 ${REPO_ROOT}/output/l2"
