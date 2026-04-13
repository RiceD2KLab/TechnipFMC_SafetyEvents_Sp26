"""v6 validation layer: allow-list filter over GLiNER extractions.

Reads gliner_extractions.parquet, applies per-type allow-lists, drops or
reclassifies mis-tagged spans. Emits a validated parquet + a change report.

Runs as a post-extraction, pre-graph-assembly step.
"""
from .validator import validate_extractions, ValidationResult

__all__ = ["validate_extractions", "ValidationResult"]
