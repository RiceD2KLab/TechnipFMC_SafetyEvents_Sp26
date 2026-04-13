#!/usr/bin/env python3
"""CLI for standalone validation of gliner_extractions.parquet.

This is used by run_gliner_pipeline.py (via import) and can also be run
standalone for ad-hoc validation of existing extractions.

Usage:
    python -m pipeline.validation.run_validation \
        --input pipeline/outputs/v5/gliner_extractions.parquet \
        --output pipeline/outputs/v6/gliner_extractions_validated.parquet
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from .validator import validate_extractions, ValidationResult


def write_report(result: ValidationResult, output_path: Path) -> None:
    """Write a human-readable Markdown report of validation results."""
    s = result.stats
    lines = []
    lines.append("# Validation Report (v6)\n")
    lines.append(f"- **Input rows:** {s['input']:,}")
    lines.append(f"- **Output rows:** {s['output']:,}")
    lines.append(f"- **Kept unchanged:** {s['kept']:,}")
    lines.append(f"- **Reclassified:** {s['reclassified']:,}")
    lines.append(f"- **Dropped:** {s['dropped']:,} ({s['drop_rate_pct']}%)\n")

    lines.append("## Per-type count delta\n")
    lines.append("| Type | Before | After | Δ |")
    lines.append("|---|---:|---:|---:|")
    for t in sorted(s["type_delta"].keys()):
        d = s["type_delta"][t]
        sign = "+" if d["delta"] >= 0 else ""
        lines.append(f"| {t} | {d['before']:,} | {d['after']:,} | {sign}{d['delta']:,} |")
    lines.append("")

    lines.append("## Reclassifications\n")
    if s["reclassified_by_direction"]:
        for direction, count in sorted(s["reclassified_by_direction"].items(),
                                        key=lambda x: -x[1]):
            lines.append(f"- `{direction}`: {count:,}")
    else:
        lines.append("- (none)")
    lines.append("")

    lines.append("## Drop reasons by type\n")
    for etype in sorted(s["drop_reasons_by_type"].keys()):
        lines.append(f"### {etype}\n")
        reasons = s["drop_reasons_by_type"][etype]
        for reason, count in sorted(reasons.items(), key=lambda x: -x[1]):
            lines.append(f"- `{reason}`: {count:,}")
        lines.append("")

    if len(result.dropped) > 0:
        lines.append("## Sample dropped rows (20 random)\n")
        sample = result.dropped.sample(n=min(20, len(result.dropped)), random_state=42)
        for _, row in sample.iterrows():
            lines.append(f"- `{row['type']}` :: {row['span']!r} — {row['reason']}")
        lines.append("")

    if len(result.reclassified) > 0:
        lines.append("## Sample reclassified rows (20 random)\n")
        sample = result.reclassified.sample(n=min(20, len(result.reclassified)), random_state=42)
        for _, row in sample.iterrows():
            lines.append(f"- `{row['old_type']}` → `{row['new_type']}` :: {row['span']!r} — {row['reason']}")
        lines.append("")

    output_path.write_text("\n".join(lines))


def main() -> None:
    ap = argparse.ArgumentParser(description="v6 validation")
    ap.add_argument("--input", type=str, required=True,
                    help="Path to gliner_extractions.parquet")
    ap.add_argument("--output", type=str, required=True,
                    help="Path to write validated parquet")
    ap.add_argument("--report", type=str, default=None,
                    help="Path to write Markdown report (default: <output_dir>/validation_report.md)")
    ap.add_argument("--dropped", type=str, default=None,
                    help="Path to write dropped-rows CSV for manual review")
    args = ap.parse_args()

    input_path = Path(args.input).resolve()
    output_path = Path(args.output).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    report_path = (
        Path(args.report).resolve()
        if args.report
        else output_path.parent / "validation_report.md"
    )

    print(f"Loading {input_path}")
    gliner_df = pd.read_parquet(input_path)
    print(f"  {len(gliner_df):,} rows")

    print("Running validation...")
    result = validate_extractions(gliner_df)
    s = result.stats
    print(f"  input={s['input']:,}  kept={s['kept']:,}  "
          f"reclassified={s['reclassified']:,}  dropped={s['dropped']:,} "
          f"({s['drop_rate_pct']}%)")

    result.validated.to_parquet(output_path, index=False)
    print(f"Wrote validated parquet → {output_path}")

    write_report(result, report_path)
    print(f"Wrote report → {report_path}")

    if args.dropped:
        result.dropped.to_csv(args.dropped, index=False)
        print(f"Wrote dropped rows → {args.dropped}")

    # Also emit a stats JSON adjacent to the parquet for downstream consumers
    stats_path = output_path.parent / "validation_stats.json"
    stats_path.write_text(json.dumps(s, indent=2, default=str))


if __name__ == "__main__":
    main()
