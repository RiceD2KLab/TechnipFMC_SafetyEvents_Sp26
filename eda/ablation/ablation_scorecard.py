#!/usr/bin/env python3
"""
Weighted scoring framework to rank pipeline ablation variants for production selection.

Reads a CSV of variant metrics (one row per variant), enforces hard gate criteria
(relation_precision >= 0.80, overmerge_rate <= 0.10, schema_violations == 0, and
json_validity >= 0.99 / evidence_coverage >= 0.90 for LLM-enriched variants),
then ranks gate-passing variants by a weighted score across 11 metrics covering
precision/recall, retrieval quality, graph connectivity, runtime, cost, and ER
safety. Outputs a ranked markdown table and a JSON summary. Supports
--fail-on-schema-drift for CI integration.

Key findings: at the time of authoring no variant had been run yet (template
state); the gate criteria define the minimum bar for production readiness, and
the weighted score determines selection among passing variants.

Decision: established the production readiness evaluation framework and the
two hard gates (relation_precision >= 0.80, overmerge_rate <= 0.10) that all
v2 pipeline variants must satisfy before being considered for deployment.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List, Tuple

import pandas as pd


REQUIRED_COLUMNS = [
    "variant_id",
    "variant_name",
    "uses_classifier",
    "uses_enrichment_llm",
    "relation_precision",
    "relation_recall",
    "retrieval_precision_at5",
    "retrieval_recall_at5",
    "avg_degree",
    "components_reduction_pct",
    "evidence_coverage",
    "json_validity",
    "total_runtime_hours",
    "estimated_cost_usd",
    "overmerge_rate",
    "max_cluster_size",
    "schema_violations",
]

NUMERIC_COLUMNS = [
    "uses_classifier",
    "uses_enrichment_llm",
    "relation_precision",
    "relation_recall",
    "retrieval_precision_at5",
    "retrieval_recall_at5",
    "avg_degree",
    "components_reduction_pct",
    "evidence_coverage",
    "json_validity",
    "total_runtime_hours",
    "estimated_cost_usd",
    "overmerge_rate",
    "max_cluster_size",
    "schema_violations",
]

METRIC_WEIGHTS: Dict[str, float] = {
    "relation_precision": 0.16,
    "relation_recall": 0.08,
    "retrieval_precision_at5": 0.16,
    "retrieval_recall_at5": 0.08,
    "evidence_coverage": 0.08,
    "avg_degree": 0.08,
    "components_reduction_pct": 0.06,
    "total_runtime_hours": 0.14,
    "estimated_cost_usd": 0.06,
    "overmerge_rate": 0.06,
    "max_cluster_size": 0.04,
}

MAXIMIZE_METRICS = {
    "relation_precision",
    "relation_recall",
    "retrieval_precision_at5",
    "retrieval_recall_at5",
    "evidence_coverage",
    "avg_degree",
    "components_reduction_pct",
}

MINIMIZE_METRICS = {
    "total_runtime_hours",
    "estimated_cost_usd",
    "overmerge_rate",
    "max_cluster_size",
}


def normalize(series: pd.Series, maximize: bool) -> pd.Series:
    min_v = series.min()
    max_v = series.max()
    if pd.isna(min_v) or pd.isna(max_v):
        return pd.Series([0.0] * len(series), index=series.index)
    if max_v == min_v:
        return pd.Series([1.0] * len(series), index=series.index)
    if maximize:
        return (series - min_v) / (max_v - min_v)
    return (max_v - series) / (max_v - min_v)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compute ablation scorecard.")
    parser.add_argument(
        "--runs-csv",
        default="eda/ablation_runs_template.csv",
        help="Input CSV containing one row per variant.",
    )
    parser.add_argument(
        "--out-md",
        default="eda/ablation_scorecard.md",
        help="Output markdown summary file.",
    )
    parser.add_argument(
        "--out-json",
        default="eda/ablation_scorecard.json",
        help="Output JSON summary file.",
    )
    parser.add_argument(
        "--fail-on-schema-drift",
        action="store_true",
        help="Exit non-zero when any variant row reports schema_violations > 0.",
    )
    return parser.parse_args()


def check_required_columns(df: pd.DataFrame) -> None:
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")


def coerce_numeric(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    for col in NUMERIC_COLUMNS:
        out[col] = pd.to_numeric(out[col], errors="coerce")
    return out


def gate_row(row: pd.Series) -> Tuple[bool, List[str]]:
    reasons: List[str] = []

    for col in REQUIRED_COLUMNS:
        if col in ("variant_id", "variant_name"):
            continue
        if pd.isna(row[col]):
            reasons.append(f"missing:{col}")

    if reasons:
        return False, reasons

    if row["schema_violations"] > 0:
        reasons.append("schema_violations>0")
    if row["relation_precision"] < 0.80:
        reasons.append("relation_precision<0.80")
    if row["overmerge_rate"] > 0.10:
        reasons.append("overmerge_rate>0.10")

    if row["uses_enrichment_llm"] >= 1:
        if row["json_validity"] < 0.99:
            reasons.append("json_validity<0.99")
        if row["evidence_coverage"] < 0.90:
            reasons.append("evidence_coverage<0.90")

    return len(reasons) == 0, reasons


def score_variants(df: pd.DataFrame) -> pd.DataFrame:
    scored = df.copy()
    scored["gate_pass"] = False
    scored["gate_reasons"] = ""
    scored["weighted_score"] = 0.0

    for idx, row in scored.iterrows():
        passed, reasons = gate_row(row)
        scored.at[idx, "gate_pass"] = passed
        scored.at[idx, "gate_reasons"] = ";".join(reasons)

    passing = scored[scored["gate_pass"]].copy()
    if passing.empty:
        return scored

    for metric, weight in METRIC_WEIGHTS.items():
        if metric in MAXIMIZE_METRICS:
            norm = normalize(passing[metric], maximize=True)
        else:
            norm = normalize(passing[metric], maximize=False)
        passing[f"norm_{metric}"] = norm
        passing["weighted_score"] += weight * norm

    passing["weighted_score"] = (passing["weighted_score"] * 100).round(2)
    scored.update(passing[["weighted_score"]])
    return scored


def as_markdown_table(df: pd.DataFrame) -> str:
    def fmt(value: object, digits: int = 3) -> str:
        if pd.isna(value):
            return "-"
        return f"{float(value):.{digits}f}"

    cols = [
        "variant_name",
        "gate_pass",
        "weighted_score",
        "relation_precision",
        "relation_recall",
        "retrieval_precision_at5",
        "retrieval_recall_at5",
        "total_runtime_hours",
        "estimated_cost_usd",
        "overmerge_rate",
        "gate_reasons",
    ]
    view = df[cols].copy()
    view = view.sort_values(by=["gate_pass", "weighted_score"], ascending=[False, False])

    lines = [
        "| Variant | Pass Gates | Score | Rel Prec | Rel Rec | Ret P@5 | Ret R@5 | Runtime (h) | Cost ($) | Overmerge | Gate Reasons |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for _, r in view.iterrows():
        lines.append(
            f"| {r['variant_name']} | {bool(r['gate_pass'])} | {float(r['weighted_score']):.2f} | "
            f"{fmt(r['relation_precision'])} | {fmt(r['relation_recall'])} | "
            f"{fmt(r['retrieval_precision_at5'])} | {fmt(r['retrieval_recall_at5'])} | "
            f"{fmt(r['total_runtime_hours'], 2)} | {fmt(r['estimated_cost_usd'], 2)} | "
            f"{fmt(r['overmerge_rate'])} | {r['gate_reasons'] or '-'} |"
        )
    return "\n".join(lines)


def write_outputs(scored: pd.DataFrame, out_md: Path, out_json: Path) -> None:
    scored_sorted = scored.sort_values(by=["gate_pass", "weighted_score"], ascending=[False, False]).copy()
    winners = scored_sorted[scored_sorted["gate_pass"]]
    winner_name = winners.iloc[0]["variant_name"] if not winners.empty else None

    md_lines = [
        "# Ablation Scorecard",
        "",
        f"- Winner: **{winner_name}**" if winner_name else "- Winner: **None (no variant passed gates)**",
        "",
        as_markdown_table(scored_sorted),
        "",
        "## Notes",
        "- `weighted_score` is only meaningful among gate-passing variants.",
        "- Any gate failure should be treated as production risk, even if some metrics are strong.",
    ]
    out_md.write_text("\n".join(md_lines), encoding="utf-8")

    payload = {
        "winner": winner_name,
        "rows": scored_sorted.to_dict(orient="records"),
    }
    out_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def main() -> None:
    args = parse_args()
    runs_csv = Path(args.runs_csv)
    out_md = Path(args.out_md)
    out_json = Path(args.out_json)

    df = pd.read_csv(runs_csv)
    check_required_columns(df)
    df = coerce_numeric(df)
    scored = score_variants(df)

    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    write_outputs(scored, out_md, out_json)

    if args.fail_on_schema_drift and (scored["schema_violations"].fillna(0) > 0).any():
        print("Schema drift detected in one or more variants.")
        raise SystemExit(2)

    ordered = scored.sort_values(by=["gate_pass", "weighted_score"], ascending=[False, False])
    print("Ablation ranking:")
    for _, row in ordered.iterrows():
        print(
            f"- {row['variant_name']}: gate_pass={bool(row['gate_pass'])}, "
            f"score={float(row['weighted_score']):.2f}, reasons={row['gate_reasons'] or '-'}"
        )
    print(f"Wrote: {out_md}")
    print(f"Wrote: {out_json}")


if __name__ == "__main__":
    main()
