"""Path to the golden set CSV and loader function."""
from __future__ import annotations

import csv
from pathlib import Path
from typing import Dict, List

_PKG_DIR = Path(__file__).resolve().parent

GOLDEN_SET_CSV: Path = _PKG_DIR / "golden_set.csv"


def load_golden_set() -> List[Dict[str, str]]:
    """Load all 52 golden set queries from the canonical CSV."""
    with GOLDEN_SET_CSV.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))
