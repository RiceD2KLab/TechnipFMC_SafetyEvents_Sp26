"""Gate 3 metrics for Layer 2 causal enrichment evaluation.

Uses the CAUSAL relation schema (source=cause, target=effect) with:
1. Direction-agnostic entity matching for CAUSAL edges (tries both alignments).
2. Precision@K: Per record, only the top-K predicted edges are scored
   where K = number of GT edges for that record.
3. Causal presence: Fraction of GT records where production has at least
   one matching CAUSAL edge.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple

# ── Preprocessing ────────────────────────────────────────────────────────────

_TYPE_WRAPPER_RE = re.compile(r'^[A-Za-z]+\("(.+?)"\)$')


def _strip_type_wrapper(s: str) -> str:
    """Strip LLM Type("...") wrappers like Event("fire") → fire."""
    return _TYPE_WRAPPER_RE.sub(r'\1', s.strip())


def _prepare_edge(edge: dict) -> dict:
    """Return a copy with Type() wrappers stripped from source/target."""
    out = dict(edge)
    out["source"] = _strip_type_wrapper(str(edge.get("source") or ""))
    out["target"] = _strip_type_wrapper(str(edge.get("target") or ""))
    return out


# ── Similarity ───────────────────────────────────────────────────────────────

# Common English stop-words to ignore in entity matching.
_STOPWORDS = frozenset({
    "a", "an", "the", "of", "in", "on", "for", "to", "was", "is", "are",
    "were", "by", "with", "and", "or", "at", "from", "into", "that", "this",
    "its", "it", "be", "been", "being", "had", "has", "have", "not", "no",
})


def _tokenize(s: str) -> Set[str]:
    """Lowercase, split on whitespace, remove stop-words."""
    return {t for t in s.lower().split() if t not in _STOPWORDS}


def _token_overlap(a: str, b: str) -> float:
    """Token overlap: |intersection| / min(|a|, |b|) after stop-word removal.

    Returns 1.0 if both empty, 0.0 if only one is empty.
    """
    tokens_a = _tokenize(a)
    tokens_b = _tokenize(b)
    if not tokens_a and not tokens_b:
        return 1.0
    if not tokens_a or not tokens_b:
        return 0.0
    return len(tokens_a & tokens_b) / min(len(tokens_a), len(tokens_b))


def _edge_similarity(pred: dict, gt: dict) -> float:
    """Similarity between two edges (0-1).

    CAUSAL edges use direction-agnostic matching: both (src↔src, tgt↔tgt)
    and (src↔tgt, tgt↔src) are tried, and the better alignment wins.

    Other relations: require same relation, compare source↔source
    and target↔target.
    Returns 0.0 if relations don't match.
    """
    p_rel = pred.get("relation", "")
    g_rel = gt.get("relation", "")
    if p_rel != g_rel:
        return 0.0

    pred_src = str(pred.get("source") or "")
    pred_tgt = str(pred.get("target") or "")
    gt_src = str(gt.get("source") or "")
    gt_tgt = str(gt.get("target") or "")

    direct = (_token_overlap(pred_src, gt_src)
              + _token_overlap(pred_tgt, gt_tgt)) / 2

    if p_rel == "CAUSAL":
        swapped = (_token_overlap(pred_src, gt_tgt)
                   + _token_overlap(pred_tgt, gt_src)) / 2
        return max(direct, swapped)

    return direct


def _edges_match(pred: dict, gt: dict, threshold: float) -> bool:
    """True if pred and gt edges match above threshold.

    For CAUSAL edges: direction-agnostic — tries both alignments and
    accepts if either has both entity overlaps >= threshold.
    For other relations: both source and target must meet threshold.
    """
    p_rel = pred.get("relation", "")
    g_rel = gt.get("relation", "")
    if p_rel != g_rel:
        return False

    if str(pred.get("record_no") or "") != str(gt.get("record_no") or ""):
        return False

    pred_src = str(pred.get("source") or "")
    pred_tgt = str(pred.get("target") or "")
    gt_src = str(gt.get("source") or "")
    gt_tgt = str(gt.get("target") or "")

    # Direct alignment
    if (_token_overlap(pred_src, gt_src) >= threshold
            and _token_overlap(pred_tgt, gt_tgt) >= threshold):
        return True

    # Direction-agnostic for CAUSAL (entity-set matching)
    if p_rel == "CAUSAL":
        if (_token_overlap(pred_src, gt_tgt) >= threshold
                and _token_overlap(pred_tgt, gt_src) >= threshold):
            return True

    return False


# ── Matching ─────────────────────────────────────────────────────────────────

def _greedy_match(
    predicted: List[dict],
    ground_truth: List[dict],
    threshold: float,
) -> Tuple[int, List[Tuple[dict, dict]]]:
    """Greedy bipartite matching: each GT edge matched at most once.

    Predicted edges are sorted by best similarity to any unmatched GT edge,
    highest first, to improve match quality over naive iteration order.
    """
    if not predicted or not ground_truth:
        return 0, []

    # Pre-compute similarity matrix
    scores: List[Tuple[float, int, int]] = []
    for pi, pred in enumerate(predicted):
        for gi, gt in enumerate(ground_truth):
            if not _edges_match(pred, gt, threshold):
                continue
            sim = _edge_similarity(pred, gt)
            scores.append((sim, pi, gi))

    # Sort by similarity descending → greedy assignment
    scores.sort(key=lambda x: x[0], reverse=True)

    gt_matched: Set[int] = set()
    pred_matched: Set[int] = set()
    matches: List[Tuple[dict, dict]] = []

    for sim, pi, gi in scores:
        if pi in pred_matched or gi in gt_matched:
            continue
        pred_matched.add(pi)
        gt_matched.add(gi)
        matches.append((predicted[pi], ground_truth[gi]))

    return len(matches), matches


def _select_top_k_per_record(
    pred_edges: List[dict],
    gt_edges: List[dict],
) -> List[dict]:
    """For each record, keep the top-K predicted edges (K = GT count).

    Edges are ranked by their maximum similarity to any GT edge in that
    record.  Records with fewer predictions than K keep all of them.
    Records with 0 GT edges (K=0) are skipped (no edges selected).
    """
    gt_by_record: Dict[str, List[dict]] = defaultdict(list)
    for e in gt_edges:
        gt_by_record[str(e.get("record_no") or "")].append(e)

    pred_by_record: Dict[str, List[dict]] = defaultdict(list)
    for e in pred_edges:
        pred_by_record[str(e.get("record_no") or "")].append(e)

    selected: List[dict] = []
    for rno, gt_list in gt_by_record.items():
        pred_list = pred_by_record.get(rno, [])
        k = len(gt_list)

        # Skip records with no GT edges (K=0)
        if k == 0:
            continue

        if len(pred_list) <= k:
            selected.extend(pred_list)
            continue

        # Rank by best similarity to any GT edge
        scored = []
        for pred in pred_list:
            best_sim = max((_edge_similarity(pred, gt) for gt in gt_list), default=0.0)
            scored.append((best_sim, pred))
        scored.sort(key=lambda x: x[0], reverse=True)
        selected.extend(edge for _, edge in scored[:k])

    return selected


# ── Evidence ─────────────────────────────────────────────────────────────────

def _evidence_f1(pred_evidence: str, gt_evidence: str) -> float:
    """Token-level F1 between predicted and GT evidence spans."""
    pred_tokens = set(pred_evidence.lower().split())
    gt_tokens = set(gt_evidence.lower().split())
    if not pred_tokens and not gt_tokens:
        return 1.0
    if not pred_tokens or not gt_tokens:
        return 0.0
    intersection = len(pred_tokens & gt_tokens)
    precision = intersection / len(pred_tokens)
    recall = intersection / len(gt_tokens)
    if precision + recall == 0:
        return 0.0
    return 2 * precision * recall / (precision + recall)


# ── Main metrics ─────────────────────────────────────────────────────────────

def compute_gate3_metrics(
    predicted_edges: List[dict],
    ground_truth_edges: List[dict],
    threshold: float = 0.45,
) -> Dict[str, Any]:
    """Compute Gate 3 metrics with causal normalisation and precision@K.

    Args:
        predicted_edges: List of predicted edge dicts
        ground_truth_edges: List of ground truth edge dicts
        threshold: Token overlap threshold [0, 1] for matching (default: 0.45)

    Returns:
        Dict with metrics and pass/fail status
    """
    # Validate threshold at entry point
    if not (0.0 <= threshold <= 1.0):
        raise ValueError(f"threshold must be in [0, 1], got {threshold}")

    # Returns a dict with:
    # - json_validity_rate
    # - causal_recall: TP / |GT| using all predicted edges
    # - precision_at_k: TP_k / |selected_k| using top-K per record
    # - causal_presence: fraction of GT records with ≥1 matched edge
    # - mean_evidence_f1: token-level F1 on matched evidence spans
    # - raw_precision: TP / |all pred in GT records| (for reference)
    # - per_original_relation: P/R by original relation labels
    required_keys = {"source", "source_type", "target", "target_type", "relation", "evidence"}

    # ── JSON validity ──
    valid_count = sum(
        1 for e in predicted_edges
        if isinstance(e, dict) and required_keys.issubset(e.keys())
    )
    total_predicted = len(predicted_edges)
    json_validity_rate = valid_count / total_predicted if total_predicted else 1.0

    # ── Prepare all edges (strip Type() wrappers) ──
    prep_pred = [_prepare_edge(e) for e in predicted_edges if isinstance(e, dict)]
    prep_gt = [_prepare_edge(e) for e in ground_truth_edges if isinstance(e, dict)]

    # Filter predictions to records present in GT
    gt_records = set(str(e.get("record_no") or "") for e in prep_gt)
    pred_in_gt = [e for e in prep_pred if str(e.get("record_no") or "") in gt_records]

    # ── Raw matching (all pred in GT records) ──
    tp_raw, matched_raw = _greedy_match(pred_in_gt, prep_gt, threshold)
    raw_precision = tp_raw / len(pred_in_gt) if pred_in_gt else 0.0
    causal_recall = tp_raw / len(prep_gt) if prep_gt else 0.0

    # ── Precision@K matching ──
    selected_k = _select_top_k_per_record(pred_in_gt, prep_gt)
    tp_k, matched_k = _greedy_match(selected_k, prep_gt, threshold)
    precision_at_k = tp_k / len(selected_k) if selected_k else 0.0
    recall_at_k = tp_k / len(prep_gt) if prep_gt else 0.0

    # ── Causal presence ──
    matched_records = set()
    for pred, gt in matched_raw:
        matched_records.add(str(gt.get("record_no") or ""))
    gt_record_count = len(gt_records)
    causal_presence = len(matched_records) / gt_record_count if gt_record_count else 0.0

    # ── Evidence F1 ──
    evidence_f1_scores = []
    for pred, gt in matched_raw:
        f1 = _evidence_f1(
            str(pred.get("evidence") or ""),
            str(gt.get("evidence") or ""),
        )
        evidence_f1_scores.append(f1)
    mean_evidence_f1 = (
        sum(evidence_f1_scores) / len(evidence_f1_scores)
        if evidence_f1_scores else 0.0
    )

    # ── Per-relation breakdown ──
    per_relation: Dict[str, Dict[str, Any]] = {}
    for rel in sorted(set(e.get("relation", "") for e in pred_in_gt + prep_gt)):
        if not rel:
            continue
        rel_pred = [e for e in pred_in_gt if e.get("relation") == rel]
        rel_gt = [e for e in prep_gt if e.get("relation") == rel]
        rel_tp, _ = _greedy_match(rel_pred, rel_gt, threshold)

        rel_prec = rel_tp / len(rel_pred) if rel_pred else (1.0 if not rel_gt else 0.0)
        rel_rec = rel_tp / len(rel_gt) if rel_gt else (1.0 if not rel_pred else 0.0)
        per_relation[rel] = {
            "precision": round(rel_prec, 4),
            "recall": round(rel_rec, 4),
            "predicted": len(rel_pred),
            "ground_truth": len(rel_gt),
            "true_positives": rel_tp,
        }

    # ── Gate 3 thresholds ──
    json_pass = json_validity_rate >= 0.99
    pk_pass = precision_at_k >= 0.50
    recall_pass = causal_recall >= 0.35
    evidence_pass = mean_evidence_f1 >= 0.60
    presence_pass = causal_presence >= 0.75
    gate3_pass = json_pass and pk_pass and recall_pass and evidence_pass and presence_pass

    return {
        "json_validity_rate": round(json_validity_rate, 4),
        "precision_at_k": round(precision_at_k, 4),
        "recall_at_k": round(recall_at_k, 4),
        "causal_recall": round(causal_recall, 4),
        "raw_precision": round(raw_precision, 4),
        "causal_presence": round(causal_presence, 4),
        "mean_evidence_f1": round(mean_evidence_f1, 4),
        "matching_threshold": threshold,
        "total_predicted": total_predicted,
        "predicted_in_gt_records": len(pred_in_gt),
        "selected_at_k": len(selected_k),
        "total_ground_truth": len(prep_gt),
        "true_positives_raw": tp_raw,
        "true_positives_at_k": tp_k,
        "gt_records_matched": len(matched_records),
        "gt_records_total": gt_record_count,
        "per_relation": per_relation,
        "thresholds": {
            "json_validity": 0.99,
            "precision_at_k": 0.50,
            "causal_recall": 0.35,
            "evidence_f1": 0.60,
            "causal_presence": 0.75,
        },
        "pass": {
            "json_validity": json_pass,
            "precision_at_k": pk_pass,
            "causal_recall": recall_pass,
            "evidence_f1": evidence_pass,
            "causal_presence": presence_pass,
            "gate3": gate3_pass,
        },
    }


# ── Report generation ────────────────────────────────────────────────────────

def generate_gate3_report(
    metrics: Dict[str, Any],
    output_path: Path,
) -> None:
    """Write a Markdown Gate 3 evaluation report."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    verdict = "PASS" if metrics["pass"]["gate3"] else "FAIL"
    p = metrics["pass"]

    lines = [
        "# Gate 3: Causal Enrichment Evaluation Report",
        "",
        f"## Verdict: **{verdict}**",
        "",
        f"Matching: causal-normalised, token overlap >= {metrics['matching_threshold']}, stop-words removed",
        "",
        "## Primary Metrics",
        "",
        "| Metric | Value | Threshold | Status |",
        "|--------|------:|-----------|--------|",
        f"| JSON validity | {metrics['json_validity_rate']:.1%} | >= 99% | {'PASS' if p['json_validity'] else 'FAIL'} |",
        f"| Precision@K | {metrics['precision_at_k']:.1%} | >= 50% | {'PASS' if p['precision_at_k'] else 'FAIL'} |",
        f"| Causal recall | {metrics['causal_recall']:.1%} | >= 35% | {'PASS' if p['causal_recall'] else 'FAIL'} |",
        f"| Evidence F1 | {metrics['mean_evidence_f1']:.1%} | >= 60% | {'PASS' if p['evidence_f1'] else 'FAIL'} |",
        f"| Causal presence | {metrics['causal_presence']:.1%} | >= 75% | {'PASS' if p['causal_presence'] else 'FAIL'} |",
        "",
        "## Counts",
        "",
        f"- Predicted edges (total): {metrics['total_predicted']:,}",
        f"- Predicted in GT records: {metrics['predicted_in_gt_records']}",
        f"- Selected at K (top-K per record): {metrics['selected_at_k']}",
        f"- Ground truth edges: {metrics['total_ground_truth']}",
        f"- True positives (raw): {metrics['true_positives_raw']}",
        f"- True positives (@K): {metrics['true_positives_at_k']}",
        f"- GT records matched: {metrics['gt_records_matched']}/{metrics['gt_records_total']}",
        f"- Raw precision (reference): {metrics['raw_precision']:.1%}",
        "",
        "## Per-Relation Breakdown",
        "",
        "| Relation | Precision | Recall | Pred | GT | TP |",
        "|----------|----------:|-------:|-----:|---:|---:|",
    ]

    for rel, data in sorted(metrics.get("per_relation", {}).items()):
        lines.append(
            f"| {rel} | {data['precision']:.1%} | {data['recall']:.1%} "
            f"| {data['predicted']} | {data['ground_truth']} | {data['true_positives']} |"
        )

    lines.extend([
        "",
        "## Raw Metrics",
        "",
        "```json",
        json.dumps(metrics, indent=2),
        "```",
        "",
    ])

    output_path.write_text("\n".join(lines), encoding="utf-8")


# ── CLI ──────────────────────────────────────────────────────────────────────

def _load_jsonl(path: Path) -> List[dict]:
    records: List[dict] = []
    with path.open("r", encoding="utf-8") as fp:
        for line in fp:
            line = line.strip()
            if line:
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return records


def main() -> None:
    parser = argparse.ArgumentParser(description="Gate 3 evaluation for L2 causal edges")
    parser.add_argument("--predicted", required=True, type=Path,
                        help="Predicted L2 edges (JSONL or directory with shard_*/l2_edges.jsonl)")
    parser.add_argument("--ground-truth", required=True, type=Path,
                        help="Ground truth edges (JSONL)")
    parser.add_argument("--threshold", type=float, default=0.45,
                        help="Token-overlap threshold for matching (default: 0.45)")
    parser.add_argument("--output", type=Path, default=None,
                        help="Output report path (default: alongside predicted)")
    args = parser.parse_args()

    # Load predicted edges
    if not args.predicted.exists():
        print(f"Error: Predicted file/directory not found: {args.predicted}", file=sys.stderr)
        sys.exit(1)
    if args.predicted.is_dir():
        predicted: List[dict] = []
        jsonl_files = list(args.predicted.glob("**/l2_edges.jsonl"))
        if not jsonl_files:
            print(f"Warning: No l2_edges.jsonl files found in {args.predicted}", file=sys.stderr)
        for jsonl in sorted(jsonl_files):
            predicted.extend(_load_jsonl(jsonl))
    else:
        predicted = _load_jsonl(args.predicted)

    if not args.ground_truth.exists():
        print(f"Error: Ground truth file not found: {args.ground_truth}", file=sys.stderr)
        sys.exit(1)
    gt = _load_jsonl(args.ground_truth)

    print(f"Predicted: {len(predicted)} edges")
    print(f"Ground truth: {len(gt)} edges")
    print(f"Threshold: {args.threshold}")

    metrics = compute_gate3_metrics(predicted, gt, threshold=args.threshold)

    if args.output is None:
        if args.predicted.is_dir():
            args.output = args.predicted / "gate3_report.md"
        else:
            args.output = args.predicted.with_name("gate3_report.md")

    generate_gate3_report(metrics, args.output)
    args.output.with_suffix(".json").write_text(
        json.dumps(metrics, indent=2) + "\n", encoding="utf-8",
    )

    verdict = "PASS" if metrics["pass"]["gate3"] else "FAIL"
    print(f"\nGate 3: {verdict}")
    print(f"  Precision@K:      {metrics['precision_at_k']:.1%}")
    print(f"  Causal recall:    {metrics['causal_recall']:.1%}")
    print(f"  Evidence F1:      {metrics['mean_evidence_f1']:.1%}")
    print(f"  Causal presence:  {metrics['causal_presence']:.1%}")
    print(f"  Raw precision:    {metrics['raw_precision']:.1%}")


if __name__ == "__main__":
    main()
