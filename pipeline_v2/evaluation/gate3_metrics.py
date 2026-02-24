"""Gate 3 metrics for Layer 2 causal enrichment evaluation."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple


def _edge_key(edge: dict) -> Tuple[str, str, str]:
    """Create a comparable key from an edge dict."""
    return (
        str(edge.get("source", "")).strip().lower(),
        str(edge.get("target", "")).strip().lower(),
        str(edge.get("relation", "")).strip(),
    )


def compute_gate3_metrics(
    predicted_edges: List[dict],
    ground_truth_edges: List[dict],
) -> Dict[str, Any]:
    """Compute Gate 3 metrics for L2 causal edges.

    Metrics:
    - json_validity_rate: fraction of predicted edges that are well-formed dicts
          with all required keys. Gate 3 threshold: >= 0.99.
    - causal_precision: fraction of predicted edges that match ground truth.
          Gate 3 threshold: >= 0.70.
    - causal_recall: fraction of ground truth edges recovered by predictions.
          Gate 3 threshold: >= 0.50.

    Returns dict with metrics and pass/fail verdict.
    """
    required_keys = {"source", "source_type", "target", "target_type", "relation", "evidence"}

    # JSON validity: check structure
    valid_count = 0
    for edge in predicted_edges:
        if isinstance(edge, dict) and required_keys.issubset(edge.keys()):
            valid_count += 1

    total_predicted = len(predicted_edges)
    json_validity_rate = valid_count / total_predicted if total_predicted else 1.0

    # Precision and recall based on (source, target, relation) keys
    pred_keys: Set[Tuple[str, str, str]] = set()
    for edge in predicted_edges:
        if isinstance(edge, dict):
            pred_keys.add(_edge_key(edge))

    gt_keys: Set[Tuple[str, str, str]] = set()
    for edge in ground_truth_edges:
        if isinstance(edge, dict):
            gt_keys.add(_edge_key(edge))

    if not pred_keys and not gt_keys:
        precision = 1.0
        recall = 1.0
    elif not pred_keys:
        precision = 1.0
        recall = 0.0
    elif not gt_keys:
        precision = 0.0
        recall = 1.0
    else:
        true_positives = pred_keys & gt_keys
        precision = len(true_positives) / len(pred_keys)
        recall = len(true_positives) / len(gt_keys)

    # Gate 3 thresholds
    json_pass = json_validity_rate >= 0.99
    precision_pass = precision >= 0.70
    recall_pass = recall >= 0.50
    gate3_pass = json_pass and precision_pass and recall_pass

    return {
        "json_validity_rate": round(json_validity_rate, 4),
        "causal_precision": round(precision, 4),
        "causal_recall": round(recall, 4),
        "total_predicted": total_predicted,
        "total_ground_truth": len(gt_keys),
        "true_positives": len(pred_keys & gt_keys) if pred_keys and gt_keys else 0,
        "thresholds": {
            "json_validity": 0.99,
            "precision": 0.70,
            "recall": 0.50,
        },
        "pass": {
            "json_validity": json_pass,
            "precision": precision_pass,
            "recall": recall_pass,
            "gate3": gate3_pass,
        },
    }


def generate_gate3_report(
    metrics: Dict[str, Any],
    output_path: Path,
) -> None:
    """Write a Markdown Gate 3 evaluation report."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    verdict = "PASS" if metrics["pass"]["gate3"] else "FAIL"
    p = metrics["pass"]

    report = f"""\
# Gate 3: Causal Enrichment Evaluation Report

## Verdict: **{verdict}**

## Metrics

| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|
| JSON validity rate | {metrics['json_validity_rate']:.2%} | >= 99% | {'PASS' if p['json_validity'] else 'FAIL'} |
| Causal precision | {metrics['causal_precision']:.2%} | >= 70% | {'PASS' if p['precision'] else 'FAIL'} |
| Causal recall | {metrics['causal_recall']:.2%} | >= 50% | {'PASS' if p['recall'] else 'FAIL'} |

## Counts

- Predicted edges: {metrics['total_predicted']}
- Ground truth edges: {metrics['total_ground_truth']}
- True positives: {metrics['true_positives']}

## Raw Metrics

```json
{json.dumps(metrics, indent=2)}
```
"""
    output_path.write_text(report, encoding="utf-8")
