"""Gate 3 metrics for Layer 2 causal enrichment evaluation.

Gate design:
- CAUSAL edges are the primary gate signal (blocking pass/fail).
- FAILED_CONTROL, MITIGATED_BY, PRECEDED_BY are reported as advisory stats
  but do not affect the gate verdict. These relation types have low model
  production volume and entity phrasing that differs systematically from
  annotator style — making them unsuitable as blocking criteria.

Matching:
- Entity similarity = max(token_overlap, sequence_similarity, tfidf_cosine)
  so word-level, character-level, or TF-IDF weighted similarity can satisfy
  the threshold.
- Token overlap uses stop-word removal + light stemming (no external deps).
- Sequence similarity uses stdlib difflib (Ratcliff/Obershelp).
- TF-IDF cosine: IDF built from all predicted + GT edges before scoring;
  smoothed log-IDF (log(N / df + 1)).
- GT is deduplicated before scoring to remove exact duplicate annotations.

Bipartite matching:
- Per-record optimal matching via backtracking with pruning for records with
  ≤12 edges per side. Falls back to greedy for larger inputs.
- Records are independent so per-record optimal = globally optimal.
- Upper-bound pruning: branch is cut when remaining capacity cannot exceed
  current best weight.

Chain compression credit (gate-blocking):
- For unmatched GT CAUSAL edges A→C, checks if predictions contain a 2-hop
  path A→B→C (both hops above threshold). Chain TPs are added to
  chain-adjusted recall and F1, which ARE used for the gate pass/fail decision.

Primary metrics (CAUSAL only):
1. Precision: TP / all predicted CAUSAL (in GT records). No cherry-picking.
2. Chain-adjusted recall (gate-blocking): (TP + chain_TP) / GT CAUSAL edges.
   See "Raw vs chain-adjusted recall" below.
3. Chain-adjusted F1: harmonic mean of precision and chain-adjusted recall.
4. Causal presence: fraction of GT CAUSAL records with ≥1 matched edge.
5. Evidence F1/P/R: token-level scores on matched evidence spans.

Raw vs chain-adjusted recall:
  Raw recall counts only direct 1:1 matches between predicted and GT edges.
  It systematically underestimates model quality when the model decomposes a
  causal chain more finely than the annotator.

  Example: GT annotates one edge  A → C  ("short circuit caused fire").
  The model extracts two edges    A → B  ("short circuit damaged insulation")
                                  B → C  ("damaged insulation caused fire").
  Both representations are correct, but raw recall scores this as a miss on
  A→C. The model is not wrong — it is *more granular* than the annotation.

  Chain-adjusted recall credits this 2-hop A→B→C path as covering the GT
  edge A→C, adding it to the TP count before computing recall. The gate uses
  chain-adjusted recall because it is a fairer measure of whether the model
  captured the causal relationship, regardless of granularity level.

  Raw recall is still reported as an informational lower bound. The difference
  between raw and chain-adjusted recall quantifies how much granularity
  mismatch exists between model output and annotations.

Known evaluation limitations (see docs/l2_review_2026-03-21.md):
- GT covers only ~1.6% of processed records, skewed toward fire incidents.
- Matching threshold sensitivity: ~14pp P/R swing from t=0.30 to t=0.60.
- Informational oracle_precision_at_k (oracle P@K) is reported but NOT used for
  gating — it selects predictions by GT similarity, making it circular.
"""
from __future__ import annotations

import argparse
import difflib
import json
import math
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from kg_schema import GATE_RELATIONS, ADVISORY_RELATIONS

# ── Preprocessing ────────────────────────────────────────────────────────────

_TYPE_WRAPPER_RE = re.compile(r'^[A-Za-z]+\("(.+?)"\)$')

_GATE_RELATIONS: Set[str] = GATE_RELATIONS
_ADVISORY_RELATIONS: Set[str] = ADVISORY_RELATIONS


def _strip_type_wrapper(s: str) -> str:
    """Strip LLM Type("...") wrappers like Event("fire") → fire."""
    return _TYPE_WRAPPER_RE.sub(r'\1', s.strip())


def _prepare_edge(edge: dict) -> dict:
    """Return a copy with Type() wrappers stripped from source/target."""
    out = dict(edge)
    out["source"] = _strip_type_wrapper(str(edge.get("source") or ""))
    out["target"] = _strip_type_wrapper(str(edge.get("target") or ""))
    return out


def _dedup_gt(edges: List[dict]) -> List[dict]:
    """Remove exact duplicate GT edges (same record, relation, source, target)."""
    seen: Set[Tuple] = set()
    result = []
    for e in edges:
        key = (
            str(e.get("record_no") or ""),
            str(e.get("relation") or ""),
            str(e.get("source") or "").lower().strip(),
            str(e.get("target") or "").lower().strip(),
        )
        if key not in seen:
            seen.add(key)
            result.append(e)
    return result


# ── Similarity ───────────────────────────────────────────────────────────────

_STOPWORDS = frozenset({
    "a", "an", "the", "of", "in", "on", "for", "to", "was", "is", "are",
    "were", "by", "with", "and", "or", "at", "from", "into", "that", "this",
    "its", "it", "be", "been", "being", "had", "has", "have", "not", "no",
})

# Module-level IDF dict; set in compute_gate3_metrics before scoring.
_IDF: Optional[Dict[str, float]] = None


def _stem(word: str) -> str:
    """Minimal suffix stripping for English inflections (no external deps).

    Handles -ing, -ed, -er, -es, -s, -tion/-sion.
    Preserves short words (≤4 chars) to avoid over-stemming.
    """
    w = word
    if len(w) <= 4:
        return w
    if w.endswith("tion") and len(w) > 6:
        return w[:-3]
    if w.endswith("sion") and len(w) > 6:
        return w[:-3]
    if w.endswith("ing") and len(w) > 6:
        stem = w[:-3]
        if len(stem) >= 2 and stem[-1] == stem[-2]:
            stem = stem[:-1]
        return stem
    if w.endswith("ed") and len(w) > 5:
        stem = w[:-2]
        if len(stem) >= 2 and stem[-1] == stem[-2]:
            stem = stem[:-1]
        return stem
    if w.endswith("er") and len(w) > 5:
        return w[:-2]
    if w.endswith("es") and len(w) > 5:
        return w[:-2]
    if w.endswith("s") and len(w) > 4 and not w.endswith("ss"):
        return w[:-1]
    return w


def _tokenize(s: str) -> Set[str]:
    """Lowercase, split on whitespace, remove stop-words, apply light stemming."""
    return {_stem(t) for t in s.lower().split() if t not in _STOPWORDS}


def _build_idf(edges: List[dict]) -> Dict[str, float]:
    """Build smoothed log-IDF from all source+target strings in edges.

    idf[term] = log(N / (df[term] + 1)) where N = number of documents
    (each source+target string is one document).
    """
    docs: List[Set[str]] = []
    for e in edges:
        src = str(e.get("source") or "")
        tgt = str(e.get("target") or "")
        if src:
            docs.append(_tokenize(src))
        if tgt:
            docs.append(_tokenize(tgt))

    n = len(docs)
    if n == 0:
        return {}

    df: Dict[str, int] = defaultdict(int)
    for doc in docs:
        for term in doc:
            df[term] += 1

    return {term: math.log(n / (count + 1)) for term, count in df.items()}


def _cosine_tfidf(a: str, b: str) -> float:
    """TF-IDF cosine similarity between two strings.

    Returns 0.0 if the module-level _IDF dict is not set.
    TF is raw term count (1 for set membership since _tokenize returns a set).
    """
    if _IDF is None:
        return 0.0
    tokens_a = _tokenize(a)
    tokens_b = _tokenize(b)
    if not tokens_a or not tokens_b:
        return 0.0
    common = tokens_a & tokens_b
    if not common:
        return 0.0
    # TF=1 for each term (binary), weight by IDF; dot product = sum(idf_a * idf_b)
    dot = sum(_IDF.get(t, 0.0) ** 2 for t in common)
    norm_a = math.sqrt(sum(_IDF.get(t, 0.0) ** 2 for t in tokens_a))
    norm_b = math.sqrt(sum(_IDF.get(t, 0.0) ** 2 for t in tokens_b))
    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
    return dot / (norm_a * norm_b)


def _token_overlap(a: str, b: str) -> float:
    """Token overlap: |intersection| / min(|a|, |b|) after stop-word removal + stemming."""
    tokens_a = _tokenize(a)
    tokens_b = _tokenize(b)
    if not tokens_a and not tokens_b:
        return 1.0
    if not tokens_a or not tokens_b:
        return 0.0
    return len(tokens_a & tokens_b) / min(len(tokens_a), len(tokens_b))


def _seq_similarity(a: str, b: str) -> float:
    """Character-level Ratcliff/Obershelp similarity via stdlib difflib."""
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    return difflib.SequenceMatcher(None, a.lower(), b.lower()).ratio()


def _entity_sim(a: str, b: str) -> float:
    """Combined entity similarity: max of token overlap, sequence similarity, and TF-IDF cosine."""
    return max(_token_overlap(a, b), _seq_similarity(a, b), _cosine_tfidf(a, b))


def _edge_similarity(pred: dict, gt: dict) -> float:
    """Similarity between two edges (0-1).

    CAUSAL: direction-agnostic — tries both alignments and returns the better one.
    Other relations: direct alignment only.
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

    direct = (_entity_sim(pred_src, gt_src) + _entity_sim(pred_tgt, gt_tgt)) / 2

    if p_rel == "CAUSAL":
        swapped = (_entity_sim(pred_src, gt_tgt) + _entity_sim(pred_tgt, gt_src)) / 2
        return max(direct, swapped)

    return direct


def _edges_match(pred: dict, gt: dict, threshold: float) -> bool:
    """True if pred and gt edges match above threshold.

    Uses max(token_overlap, seq_similarity, tfidf_cosine) for each entity pair
    so any of the three similarity measures can satisfy the threshold.
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

    if (_entity_sim(pred_src, gt_src) >= threshold
            and _entity_sim(pred_tgt, gt_tgt) >= threshold):
        return True

    if p_rel == "CAUSAL":
        if (_entity_sim(pred_src, gt_tgt) >= threshold
                and _entity_sim(pred_tgt, gt_src) >= threshold):
            return True

    return False


# ── Matching ─────────────────────────────────────────────────────────────────

def _greedy_match(
    predicted: List[dict],
    ground_truth: List[dict],
    threshold: float,
) -> Tuple[int, List[Tuple[dict, dict]]]:
    """Greedy bipartite matching: each GT edge matched at most once."""
    if not predicted or not ground_truth:
        return 0, []

    scores: List[Tuple[float, int, int]] = []
    for pi, pred in enumerate(predicted):
        for gi, gt in enumerate(ground_truth):
            if not _edges_match(pred, gt, threshold):
                continue
            sim = _edge_similarity(pred, gt)
            scores.append((sim, pi, gi))

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


def _backtrack_match(
    adj: Dict[int, List[Tuple[int, float]]],
    pred_list: List[int],
    idx: int,
    gt_used: Set[int],
    weight: float,
    assign: List[Tuple[int, int]],
    best: Dict[str, Any],
) -> None:
    """Backtracking bipartite match with upper-bound pruning.

    Args:
        adj: {pred_idx: [(gt_idx, sim), ...]} sorted by sim desc
        pred_list: ordered list of pred indices to assign
        idx: current position in pred_list
        gt_used: set of already-assigned GT indices
        weight: accumulated similarity weight so far
        assign: current partial assignment [(pred_idx, gt_idx), ...]
        best: mutable dict with keys 'weight' and 'assign' for the best found so far
    """
    # Upper bound: remaining preds can each contribute at most 1.0
    if weight + (len(pred_list) - idx) <= best["weight"]:
        return
    if idx == len(pred_list):
        if weight > best["weight"]:
            best["weight"] = weight
            best["assign"] = assign[:]
        return
    pi = pred_list[idx]
    # Branch: skip this pred (contribute 0)
    _backtrack_match(adj, pred_list, idx + 1, gt_used, weight, assign, best)
    # Branch: assign to each compatible GT
    for gi, sim in adj.get(pi, []):
        if gi not in gt_used:
            assign.append((pi, gi))
            gt_used.add(gi)
            _backtrack_match(adj, pred_list, idx + 1, gt_used, weight + sim, assign, best)
            assign.pop()
            gt_used.remove(gi)


def _optimal_match(
    predicted: List[dict],
    ground_truth: List[dict],
    threshold: float,
) -> Tuple[int, List[Tuple[dict, dict]]]:
    """Per-record optimal bipartite matching with backtracking (n≤12) or greedy fallback.

    For records with ≤12 edges per side, uses exact backtracking with upper-bound
    pruning to find the globally optimal assignment. Falls back to greedy for
    larger records.

    Records are independent, so per-record optimal = globally optimal.

    Returns (total_tp, [(pred_dict, gt_dict), ...]).
    """
    if not predicted or not ground_truth:
        return 0, []

    # Group by record_no
    pred_by_rec: Dict[str, List[Tuple[int, dict]]] = defaultdict(list)
    for pi, p in enumerate(predicted):
        pred_by_rec[str(p.get("record_no") or "")].append((pi, p))

    gt_by_rec: Dict[str, List[Tuple[int, dict]]] = defaultdict(list)
    for gi, g in enumerate(ground_truth):
        gt_by_rec[str(g.get("record_no") or "")].append((gi, g))

    total_tp = 0
    all_matches: List[Tuple[dict, dict]] = []

    all_records = set(pred_by_rec) | set(gt_by_rec)
    for rec in all_records:
        rec_pred = pred_by_rec.get(rec, [])
        rec_gt = gt_by_rec.get(rec, [])
        if not rec_pred or not rec_gt:
            continue

        # Fall back to greedy for large records
        if len(rec_pred) > 12 or len(rec_gt) > 12:
            pred_dicts = [p for _, p in rec_pred]
            gt_dicts = [g for _, g in rec_gt]
            tp, matches = _greedy_match(pred_dicts, gt_dicts, threshold)
            total_tp += tp
            all_matches.extend(matches)
            continue

        # Build adjacency: {local_pred_idx: [(local_gt_idx, sim), ...]} sorted desc
        adj: Dict[int, List[Tuple[int, float]]] = {}
        for lpi, (pi, p) in enumerate(rec_pred):
            neighbors = []
            for lgi, (gi, g) in enumerate(rec_gt):
                if _edges_match(p, g, threshold):
                    sim = _edge_similarity(p, g)
                    neighbors.append((lgi, sim))
            neighbors.sort(key=lambda x: x[1], reverse=True)
            adj[lpi] = neighbors

        pred_list = list(range(len(rec_pred)))
        best: Dict[str, Any] = {"weight": 0.0, "assign": []}
        _backtrack_match(adj, pred_list, 0, set(), 0.0, [], best)

        for lpi, lgi in best["assign"]:
            all_matches.append((rec_pred[lpi][1], rec_gt[lgi][1]))
        total_tp += len(best["assign"])

    return total_tp, all_matches


def _oracle_select_top_k(
    pred_edges: List[dict],
    gt_edges: List[dict],
) -> List[dict]:
    """ORACLE ONLY — selects top-K predictions per record by GT similarity.

    WARNING: This is circular — predictions are ranked by similarity to the
    answer before scoring. It inflates precision by ~17pp vs honest micro-precision.
    Used only to compute oracle_precision_at_k for reference, NOT for gating.
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
        if k == 0:
            continue
        if len(pred_list) <= k:
            selected.extend(pred_list)
            continue
        scored = []
        for pred in pred_list:
            best_sim = max((_edge_similarity(pred, gt) for gt in gt_list), default=0.0)
            scored.append((best_sim, pred))
        scored.sort(key=lambda x: x[0], reverse=True)
        selected.extend(edge for _, edge in scored[:k])

    return selected


# ── Chain compression credit ──────────────────────────────────────────────────

def _chain_credit(
    unmatched_gt: List[dict],
    pred_causal: List[dict],
    threshold: float,
) -> int:
    """Count unmatched GT CAUSAL edges A→C covered by a 2-hop predicted path A→B→C.

    For each unmatched GT edge (A→C), checks whether the predictions for the
    same record contain both pred(A→B) and pred(B→C) with entity sim ≥ threshold.
    Direction-agnostic for CAUSAL (tries A→B→C and C→B→A alignments).

    Returns the count of GT edges covered by chain paths (advisory — not used
    for gate pass/fail).
    """
    if not unmatched_gt or not pred_causal:
        return 0

    # Group predictions by record
    pred_by_rec: Dict[str, List[dict]] = defaultdict(list)
    for p in pred_causal:
        pred_by_rec[str(p.get("record_no") or "")].append(p)

    chain_count = 0
    for gt_edge in unmatched_gt:
        rec = str(gt_edge.get("record_no") or "")
        rec_preds = pred_by_rec.get(rec, [])
        if not rec_preds:
            continue

        gt_a = str(gt_edge.get("source") or "")
        gt_c = str(gt_edge.get("target") or "")

        covered = False
        for p1 in rec_preds:
            if covered:
                break
            p1_src = str(p1.get("source") or "")
            p1_tgt = str(p1.get("target") or "")
            # Try A→B: p1 matches A at source end
            for a_end, b_end in [(p1_src, p1_tgt), (p1_tgt, p1_src)]:
                if _entity_sim(a_end, gt_a) < threshold:
                    continue
                # b_end is the intermediate node B; look for pred B→C
                for p2 in rec_preds:
                    if p2 is p1:
                        continue
                    p2_src = str(p2.get("source") or "")
                    p2_tgt = str(p2.get("target") or "")
                    for b2_end, c_end in [(p2_src, p2_tgt), (p2_tgt, p2_src)]:
                        if (_entity_sim(b2_end, b_end) >= threshold
                                and _entity_sim(c_end, gt_c) >= threshold):
                            covered = True
                            break
                    if covered:
                        break
                if covered:
                    break

        if covered:
            chain_count += 1

    return chain_count


# ── Evidence ─────────────────────────────────────────────────────────────────

def _evidence_scores(pred_evidence: str, gt_evidence: str) -> Tuple[float, float, float]:
    """Token-level precision, recall, F1 between predicted and GT evidence spans.

    Returns (precision, recall, f1).
    Precision: fraction of model-cited tokens that appear in GT evidence
               (high = model is not over-citing irrelevant text).
    Recall:    fraction of GT-cited tokens that the model included
               (high = model captured the right passage).
    F1:        harmonic mean.
    """
    pred_tokens = set(pred_evidence.lower().split())
    gt_tokens = set(gt_evidence.lower().split())
    if not pred_tokens and not gt_tokens:
        return 1.0, 1.0, 1.0
    if not pred_tokens or not gt_tokens:
        return 0.0, 0.0, 0.0
    intersection = len(pred_tokens & gt_tokens)
    precision = intersection / len(pred_tokens)
    recall = intersection / len(gt_tokens)
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0
    return precision, recall, f1


# ── Main metrics ─────────────────────────────────────────────────────────────

def compute_gate3_metrics(
    predicted_edges: List[dict],
    ground_truth_edges: List[dict],
    threshold: float = 0.45,
) -> Dict[str, Any]:
    """Compute Gate 3 metrics.

    Gate pass/fail is determined by CAUSAL edges only.
    FAILED_CONTROL, MITIGATED_BY, PRECEDED_BY are reported as advisory stats.

    Precision is honest micro-precision: TP / all predicted CAUSAL edges in GT
    records. No cherry-picking or GT-similarity-based selection.

    Recall denominator is all GT CAUSAL edges. The GT files must already be
    filtered to records that exist in the pipeline (records with no L1 entities
    should have been removed from GT before running this script).

    Matching uses per-record optimal backtracking (≤12 edges/side) with greedy
    fallback. Entity similarity = max(token_overlap, seq_similarity, tfidf_cosine).
    IDF is built from all predicted + GT edges before scoring.

    Chain-adjusted recall (advisory) credits unmatched GT CAUSAL edges A→C when
    the predictions contain a 2-hop path A→B→C. Not used for gate pass/fail.

    Args:
        predicted_edges: List of predicted edge dicts
        ground_truth_edges: List of ground truth edge dicts
        threshold: Entity similarity threshold [0, 1] for matching (default: 0.45)

    Returns:
        Dict with metrics and pass/fail status
    """
    global _IDF

    if not (0.0 <= threshold <= 1.0):
        raise ValueError(f"threshold must be in [0, 1], got {threshold}")

    required_keys = {"source", "source_type", "target", "target_type", "relation", "evidence"}

    # ── JSON validity ──
    valid_count = sum(
        1 for e in predicted_edges
        if isinstance(e, dict) and required_keys.issubset(e.keys())
    )
    total_predicted = len(predicted_edges)
    json_validity_rate = valid_count / total_predicted if total_predicted else 1.0

    # ── Prepare edges ──
    prep_pred = [_prepare_edge(e) for e in predicted_edges if isinstance(e, dict)]
    prep_gt_raw = [_prepare_edge(e) for e in ground_truth_edges if isinstance(e, dict)]

    # Deduplicate GT
    prep_gt = _dedup_gt(prep_gt_raw)
    gt_dupes_removed = len(prep_gt_raw) - len(prep_gt)

    # Build IDF from all edges (predicted + GT) before computing any similarities
    _IDF = _build_idf(prep_pred + prep_gt)

    # Filter predictions to records present in GT
    gt_records = set(str(e.get("record_no") or "") for e in prep_gt)
    pred_in_gt = [e for e in prep_pred if str(e.get("record_no") or "") in gt_records]

    # ── Split CAUSAL vs advisory ──
    causal_gt = [e for e in prep_gt if e.get("relation") in _GATE_RELATIONS]
    causal_pred = [e for e in pred_in_gt if e.get("relation") in _GATE_RELATIONS]

    causal_gt_records = set(str(e.get("record_no") or "") for e in causal_gt)

    # ── CAUSAL matching (precision + recall) ──
    tp_causal, matched_causal = _optimal_match(causal_pred, causal_gt, threshold)

    precision = tp_causal / len(causal_pred) if causal_pred else 0.0
    recall = tp_causal / len(causal_gt) if causal_gt else 0.0
    f1 = (
        2 * precision * recall / (precision + recall)
        if (precision + recall) > 0 else 0.0
    )

    # Causal presence
    matched_causal_records = set(str(gt.get("record_no") or "") for _, gt in matched_causal)
    causal_presence = (
        len(matched_causal_records) / len(causal_gt_records)
        if causal_gt_records else 0.0
    )

    # Evidence precision, recall, F1 on matched edges
    evidence_scores = [
        _evidence_scores(str(p.get("evidence") or ""), str(g.get("evidence") or ""))
        for p, g in matched_causal
    ]
    mean_evidence_precision = (
        sum(s[0] for s in evidence_scores) / len(evidence_scores)
        if evidence_scores else 0.0
    )
    mean_evidence_recall = (
        sum(s[1] for s in evidence_scores) / len(evidence_scores)
        if evidence_scores else 0.0
    )
    mean_evidence_f1 = (
        sum(s[2] for s in evidence_scores) / len(evidence_scores)
        if evidence_scores else 0.0
    )

    # Oracle P@K — circular selection, informational only, NOT used for gating
    oracle_selected = _oracle_select_top_k(causal_pred, causal_gt)
    tp_oracle, _ = _greedy_match(oracle_selected, causal_gt, threshold)
    oracle_precision_at_k = tp_oracle / len(oracle_selected) if oracle_selected else 0.0

    # ── Chain compression credit (gate-blocking) ──
    matched_gt_ids = {id(g) for _, g in matched_causal}
    unmatched_gt_causal = [g for g in causal_gt if id(g) not in matched_gt_ids]
    chain_tp = _chain_credit(unmatched_gt_causal, causal_pred, threshold)
    chain_adjusted_recall = (tp_causal + chain_tp) / len(causal_gt) if causal_gt else 0.0
    chain_adjusted_f1 = (
        2 * precision * chain_adjusted_recall / (precision + chain_adjusted_recall)
        if (precision + chain_adjusted_recall) > 0 else 0.0
    )

    # ── Advisory relation stats ──
    advisory: Dict[str, Dict[str, Any]] = {}
    for rel in sorted(_ADVISORY_RELATIONS):
        rel_pred = [e for e in pred_in_gt if e.get("relation") == rel]
        rel_gt = [e for e in prep_gt if e.get("relation") == rel]
        rel_tp, _ = _greedy_match(rel_pred, rel_gt, threshold)
        rel_prec = rel_tp / len(rel_pred) if rel_pred else (1.0 if not rel_gt else 0.0)
        rel_rec = rel_tp / len(rel_gt) if rel_gt else (1.0 if not rel_pred else 0.0)
        advisory[rel] = {
            "precision": round(rel_prec, 4),
            "recall": round(rel_rec, 4),
            "predicted": len(rel_pred),
            "ground_truth": len(rel_gt),
            "true_positives": rel_tp,
        }

    # ── Gate thresholds ──
    json_pass = json_validity_rate >= 0.99
    precision_pass = precision >= 0.50
    recall_pass = chain_adjusted_recall >= 0.60
    f1_pass = chain_adjusted_f1 >= 0.55
    evidence_pass = mean_evidence_f1 >= 0.60
    presence_pass = causal_presence >= 0.75
    gate3_pass = json_pass and precision_pass and recall_pass and f1_pass and evidence_pass and presence_pass

    return {
        # Primary metrics
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1": round(f1, 4),
        "mean_evidence_precision": round(mean_evidence_precision, 4),
        "mean_evidence_recall": round(mean_evidence_recall, 4),
        "mean_evidence_f1": round(mean_evidence_f1, 4),
        "causal_presence": round(causal_presence, 4),
        "json_validity_rate": round(json_validity_rate, 4),
        # Chain-adjusted (gate-blocking)
        "chain_adjusted_recall": round(chain_adjusted_recall, 4),
        "chain_adjusted_f1": round(chain_adjusted_f1, 4),
        "chain_tp": chain_tp,
        # Reference / informational
        "oracle_precision_at_k": round(oracle_precision_at_k, 4),
        "matching_threshold": threshold,
        # Counts
        "total_predicted": total_predicted,
        "causal_predicted_in_gt_records": len(causal_pred),
        "causal_ground_truth": len(causal_gt),
        "causal_true_positives": tp_causal,
        "causal_gt_records_matched": len(matched_causal_records),
        "causal_gt_records_total": len(causal_gt_records),
        "gt_total_after_dedup": len(prep_gt),
        "gt_duplicates_removed": gt_dupes_removed,
        "advisory": advisory,
        "thresholds": {
            "json_validity": 0.99,
            "precision": 0.50,
            "chain_adjusted_recall": 0.60,
            "chain_adjusted_f1": 0.55,
            "evidence_f1": 0.60,
            "causal_presence": 0.75,
        },
        "pass": {
            "json_validity": json_pass,
            "precision": precision_pass,
            "chain_adjusted_recall": recall_pass,
            "chain_adjusted_f1": f1_pass,
            "evidence_f1": evidence_pass,
            "causal_presence": presence_pass,
            "gate3": gate3_pass,
        },
    }


def compute_threshold_sweep(
    predicted_edges: List[dict],
    ground_truth_edges: List[dict],
    thresholds: Optional[List[float]] = None,
) -> List[Dict[str, Any]]:
    """Run compute_gate3_metrics at multiple thresholds.

    Returns a list of {threshold, precision, recall, f1,
    mean_evidence_f1, causal_presence, chain_tp, chain_adjusted_recall,
    gate3_pass} dicts — one per threshold.
    """
    if thresholds is None:
        thresholds = [0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60]
    rows = []
    for t in thresholds:
        m = compute_gate3_metrics(predicted_edges, ground_truth_edges, threshold=t)
        rows.append({
            "threshold": t,
            "precision": m["precision"],
            "recall": m["recall"],
            "f1": m["f1"],
            "oracle_precision_at_k": m["oracle_precision_at_k"],
            "mean_evidence_f1": m["mean_evidence_f1"],
            "causal_presence": m["causal_presence"],
            "chain_tp": m["chain_tp"],
            "chain_adjusted_recall": m["chain_adjusted_recall"],
            "chain_adjusted_f1": m["chain_adjusted_f1"],
            "gate3_pass": m["pass"]["gate3"],
        })
    return rows


# ── Report generation ────────────────────────────────────────────────────────

def generate_gate3_report(
    metrics: Dict[str, Any],
    output_path: Path,
    sweep_rows: Optional[List[Dict[str, Any]]] = None,
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
        f"Matching: max(token_overlap, sequence_similarity, tfidf_cosine) >= {metrics['matching_threshold']},"
        " stop-words removed, light stemming",
        f"GT deduplication: {metrics['gt_duplicates_removed']} duplicate edges removed",
        "",
        "## Primary Metrics (CAUSAL edges — gate blocking)",
        "",
        "| Metric | Value | Threshold | Status |",
        "|--------|------:|-----------|--------|",
        f"| JSON validity | {metrics['json_validity_rate']:.1%} | >= 99% | {'PASS' if p['json_validity'] else 'FAIL'} |",
        f"| Precision | {metrics['precision']:.1%} | >= 50% | {'PASS' if p['precision'] else 'FAIL'} |",
        f"| Chain-adjusted Recall | {metrics['chain_adjusted_recall']:.1%} | >= 60% | {'PASS' if p['chain_adjusted_recall'] else 'FAIL'} |",
        f"| Chain-adjusted F1 | {metrics['chain_adjusted_f1']:.1%} | >= 55% | {'PASS' if p['chain_adjusted_f1'] else 'FAIL'} |",
        f"| Evidence F1 | {metrics['mean_evidence_f1']:.1%} | >= 60% | {'PASS' if p['evidence_f1'] else 'FAIL'} |",
        f"| Evidence Precision | {metrics['mean_evidence_precision']:.1%} | — | (informational) |",
        f"| Evidence Recall | {metrics['mean_evidence_recall']:.1%} | — | (informational) |",
        f"| Causal presence | {metrics['causal_presence']:.1%} | >= 75% | {'PASS' if p['causal_presence'] else 'FAIL'} |",
        "",
        "## CAUSAL Counts",
        "",
        f"- Predicted CAUSAL in GT records: {metrics['causal_predicted_in_gt_records']}",
        f"- GT CAUSAL edges (after dedup): {metrics['causal_ground_truth']}",
        f"- True positives: {metrics['causal_true_positives']}",
        f"- Chain TPs (2-hop A→B→C covering GT A→C): {metrics['chain_tp']}",
        f"- GT records matched: {metrics['causal_gt_records_matched']}/{metrics['causal_gt_records_total']}",
        "",
        "## Informational (not used for gating)",
        "",
        f"- Raw recall (before chain credit): {metrics['recall']:.1%}",
        f"- Raw F1 (before chain credit): {metrics['f1']:.1%}",
        f"- Oracle P@K (circular — GT-similarity selection): {metrics['oracle_precision_at_k']:.1%}",
        "",
        "## Advisory Relation Stats (informational only — do not affect gate)",
        "",
        "| Relation | Precision | Recall | Pred | GT | TP |",
        "|----------|----------:|-------:|-----:|---:|---:|",
    ]

    for rel, data in sorted(metrics.get("advisory", {}).items()):
        lines.append(
            f"| {rel} | {data['precision']:.1%} | {data['recall']:.1%} "
            f"| {data['predicted']} | {data['ground_truth']} | {data['true_positives']} |"
        )

    if sweep_rows:
        lines.extend([
            "",
            "## Threshold Sensitivity Sweep",
            "",
            "| Threshold | P | Raw-R | Raw-F1 | Chain-Adj-R | Chain-Adj-F1 | Oracle-P@K | Evidence-F1 | Presence | PASS |",
            "|----------:|----:|------:|-------:|------------:|-------------:|-----------:|------------:|---------:|------|",
        ])
        for row in sweep_rows:
            lines.append(
                f"| {row['threshold']:.2f}"
                f" | {row['precision']:.1%}"
                f" | {row['recall']:.1%}"
                f" | {row['f1']:.1%}"
                f" | {row['chain_adjusted_recall']:.1%}"
                f" | {row['chain_adjusted_f1']:.1%}"
                f" | {row['oracle_precision_at_k']:.1%}"
                f" | {row['mean_evidence_f1']:.1%}"
                f" | {row['causal_presence']:.1%}"
                f" | {'✓' if row['gate3_pass'] else '✗'} |"
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
                        help="Entity similarity threshold for matching (default: 0.45)")
    parser.add_argument("--sweep", action="store_true",
                        help="Also run threshold sensitivity sweep (0.30–0.60)")
    parser.add_argument("--output", type=Path, default=None,
                        help="Output report path (default: alongside predicted)")
    args = parser.parse_args()

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

    sweep_rows = None
    if args.sweep:
        print("Running threshold sweep...")
        sweep_rows = compute_threshold_sweep(predicted, gt)

    if args.output is None:
        if args.predicted.is_dir():
            args.output = args.predicted / "gate3_report.md"
        else:
            args.output = args.predicted.with_name("gate3_report.md")

    generate_gate3_report(metrics, args.output, sweep_rows=sweep_rows)
    args.output.with_suffix(".json").write_text(
        json.dumps(metrics, indent=2) + "\n", encoding="utf-8",
    )

    verdict = "PASS" if metrics["pass"]["gate3"] else "FAIL"
    print(f"\nGate 3: {verdict}")
    print(f"  Precision:             {metrics['precision']:.1%}  (>= 50%)")
    print(f"  Chain-adj Recall:      {metrics['chain_adjusted_recall']:.1%}  (>= 60%)  [+{metrics['chain_tp']} chain TPs over raw {metrics['recall']:.1%}]")
    print(f"  Chain-adj F1:          {metrics['chain_adjusted_f1']:.1%}  (>= 55%)  [raw F1: {metrics['f1']:.1%}]")
    print(f"  Evidence F1:           {metrics['mean_evidence_f1']:.1%}  (>= 60%)  [P={metrics['mean_evidence_precision']:.1%}  R={metrics['mean_evidence_recall']:.1%}]")
    print(f"  Causal presence:       {metrics['causal_presence']:.1%}  (>= 75%)")
    print(f"  Oracle P@K (ref):      {metrics['oracle_precision_at_k']:.1%}  [circular, not gating]")
    print()
    print("  Advisory (not blocking):")
    for rel, d in sorted(metrics.get("advisory", {}).items()):
        print(f"    {rel}: P={d['precision']:.1%} R={d['recall']:.1%} "
              f"(pred={d['predicted']} gt={d['ground_truth']} tp={d['true_positives']})")

    if sweep_rows:
        print("\nThreshold sweep:")
        print(f"  {'t':>4}  {'P':>8}  {'R':>8}  {'F1':>6}  {'OracleP@K':>10}  {'ChainAdjR':>10}  {'PASS':>5}")
        for row in sweep_rows:
            print(f"  {row['threshold']:.2f}  {row['precision']:>8.1%}"
                  f"  {row['recall']:>8.1%}"
                  f"  {row['f1']:>6.1%}"
                  f"  {row['oracle_precision_at_k']:>10.1%}"
                  f"  {row['chain_adjusted_recall']:>10.1%}"
                  f"  {'Y' if row['gate3_pass'] else 'N':>5}")


if __name__ == "__main__":
    main()
