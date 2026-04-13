"""Telemetry utilities: deterministic diff between pipeline runs."""
from .generate_diff import generate_diff, DataDirDiff

__all__ = ["generate_diff", "DataDirDiff"]
