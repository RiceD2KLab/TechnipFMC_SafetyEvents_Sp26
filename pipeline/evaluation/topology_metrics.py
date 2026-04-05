"""Step 4: Gate 1 topology metrics and report generation."""
from __future__ import annotations

from pathlib import Path
from typing import Any

import networkx as nx
import pandas as pd

from kg_schema import ALLOWED_RELATIONS

BASELINES = {
    "spaCy (Fall 2025)":        {"giant_component": 0.807, "mean_degree": 3.15},
    "Plumber (Fall 2025)":      {"giant_component": 0.852, "mean_degree": 2.51},
    "Mistral 7B (Fall 2025)":   {"giant_component": 0.332, "mean_degree": 2.00},
    "GLiNER v1 (999-incident)": {"giant_component": 0.959, "mean_degree": 2.408},
}


def compute_gate1_metrics(
    nodes_df: pd.DataFrame,
    edges_df: pd.DataFrame,
) -> dict[str, Any]:
    """Compute graph topology metrics for Gate 1 evaluation.

    Gate 1 thresholds:
      - Schema violations = 0
      - Giant component ratio >= 0.85
      - Mean degree >= 2.0
    """
    G = nx.Graph()
    for _, node in nodes_df.iterrows():
        G.add_node(node["entity_id"])
    for _, edge in edges_df.iterrows():
        G.add_edge(edge["source"], edge["target"])

    n_nodes = G.number_of_nodes()
    n_edges = G.number_of_edges()

    type_counts = nodes_df["entity_type"].value_counts().to_dict()
    relation_counts = edges_df["relation"].value_counts().to_dict() if not edges_df.empty else {}

    violations = edges_df[~edges_df["relation"].isin(ALLOWED_RELATIONS)] if not edges_df.empty else pd.DataFrame()
    n_violations = len(violations)

    if n_nodes > 0:
        components = list(nx.connected_components(G))
        largest = max(components, key=len)
        giant_component_ratio = len(largest) / n_nodes
        n_components = len(components)
    else:
        giant_component_ratio = 0.0
        n_components = 0

    degrees = [d for _, d in G.degree()]
    mean_degree = sum(degrees) / len(degrees) if degrees else 0.0
    median_degree = sorted(degrees)[len(degrees) // 2] if degrees else 0
    max_degree = max(degrees) if degrees else 0

    gate1_pass = (n_violations == 0) and (giant_component_ratio >= 0.85) and (mean_degree >= 2.0)

    return {
        "n_nodes": n_nodes,
        "n_edges": n_edges,
        "n_components": n_components,
        "giant_component_ratio": round(giant_component_ratio, 4),
        "mean_degree": round(mean_degree, 3),
        "median_degree": median_degree,
        "max_degree": max_degree,
        "schema_violations": n_violations,
        "gate1_pass": gate1_pass,
        "type_counts": type_counts,
        "relation_counts": relation_counts,
    }


def generate_report(metrics: dict[str, Any], output_path: Path) -> str:
    """Generate metrics_report.md and write to output_path."""
    m = metrics
    gc = m["giant_component_ratio"]
    md = m["mean_degree"]
    sv = m["schema_violations"]

    report = f"""# V2 Schema Pipeline — Metrics Report

## Gate 1 Results

| Metric | Value | Threshold | Pass? |
|--------|-------|-----------|-------|
| Schema violations | {sv} | 0 | {"PASS" if sv == 0 else "FAIL"} |
| Giant component ratio | {gc} | >= 0.85 | {"PASS" if gc >= 0.85 else "FAIL"} |
| Mean degree | {md} | >= 2.0 | {"PASS" if md >= 2.0 else "FAIL"} |

**Gate 1 overall: {"PASS" if m["gate1_pass"] else "FAIL"}**

## Graph Summary

- **Nodes:** {m["n_nodes"]:,}
- **Edges:** {m["n_edges"]:,}
- **Connected components:** {m["n_components"]:,}

## Node Type Distribution

| Entity Type | Count |
|------------|------:|
"""
    for etype, count in sorted(m["type_counts"].items(), key=lambda x: -x[1]):
        report += f"| {etype} | {count:,} |\n"

    report += """
## Edge Type Distribution

| Relation Type | Count |
|--------------|------:|
"""
    for rel, count in sorted(m["relation_counts"].items(), key=lambda x: -x[1]):
        report += f"| {rel} | {count:,} |\n"

    report += """
## Comparison Against Baselines

| Method | Giant Component | Mean Degree |
|--------|:-:|:-:|
"""
    for name, bl in BASELINES.items():
        report += f"| {name} | {bl['giant_component']} | {bl['mean_degree']} |\n"
    report += f"| **GLiNER v2 (this run)** | **{gc}** | **{md}** |\n"

    report += f"""
## Degree Statistics

- Mean: {m["mean_degree"]}
- Median: {m["median_degree"]}
- Max: {m["max_degree"]}
"""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding="utf-8")
    return report
