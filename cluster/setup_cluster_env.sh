#!/bin/bash
# Setup Python virtual environment on Rice NOTS cluster.
#
# Run from a login node (ssh username@nots.rice.edu):
#   bash cluster/setup_cluster_env.sh
#
# This script:
#   1. Loads GCC + CUDA modules via the NOTS module system
#   2. Creates a Python venv in $WORK (avoids $HOME quota)
#   3. Installs PyTorch with CUDA support + project dependencies
#   4. Optionally installs Ollama for L2 enrichment
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${REPO_ROOT}"

# ── Configuration ────────────────────────────────────────────────────────
VENV_DIR="${VENV_DIR:-${WORK:-.}/.venv_cluster}"
TORCH_VERSION="${TORCH_VERSION:-2.10.0}"
INSTALL_OLLAMA="${INSTALL_OLLAMA:-0}"

echo "=== Rice NOTS Cluster Environment Setup ==="
echo "VENV_DIR:       ${VENV_DIR}"
echo "TORCH_VERSION:  ${TORCH_VERSION}"

# ── Load modules ─────────────────────────────────────────────────────────
module purge
module load GCC/13.2.0
module load CUDA/12.6.0
module load Python/3.11.5
echo "Loaded modules:"
module list

# ── Create venv ──────────────────────────────────────────────────────────
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
  OLLAMA_DIR="${WORK:-$HOME}/bin"
  mkdir -p "${OLLAMA_DIR}"
  if command -v "${OLLAMA_DIR}/ollama" &>/dev/null; then
    echo "Ollama already installed at ${OLLAMA_DIR}/ollama"
  else
    echo "Installing Ollama to ${OLLAMA_DIR}..."
    curl -fsSL https://ollama.com/download/ollama-linux-amd64 -o "${OLLAMA_DIR}/ollama"
    chmod +x "${OLLAMA_DIR}/ollama"
    echo "Ollama installed. Add to PATH: export PATH=${OLLAMA_DIR}:\$PATH"
  fi
fi

echo ""
echo "=== Setup complete ==="
echo "Activate with: source ${VENV_DIR}/bin/activate"
echo "Submit jobs from: ${REPO_ROOT}/cluster/"
