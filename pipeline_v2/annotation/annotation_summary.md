# Annotation Set — Evaluation Plan

## 1. Selection Summary

### Filtering Criteria
Records were drawn from the full 23K incident dataset and filtered to:
- Narrative language: English (non-ASCII character ratio < 30%)
- Minimum narrative length: 30 whitespace tokens
- Causal language signal: at least 1 match from the 24-pattern causal regex set (see `generate_annotation_set.py`)

Records failing any criterion were excluded. After deduplication on `record_no`, the eligible pool was:

- **Total eligible:** 7,715
- **Total selected:** 200

Within the eligible pool, records were ranked by `causal_density` (causal matches / token count) and drawn greedily by stratum in the order defined in `STRATA`, without replacement.

### Distribution by Stratum

| Stratum | Count | Mean Causal Density | Mean Tokens |
|---------|------:|-------------------:|------------:|
| fire_explosion | 50 | 0.0344 | 60 |
| falls_slips | 40 | 0.0393 | 51 |
| dropped_objects | 30 | 0.0515 | 64 |
| transportation | 20 | 0.0484 | 48 |
| containment_loss | 20 | 0.0540 | 81 |
| high_causal_any | 40 | 0.0691 | 45 |

Strata are mutually exclusive: once a record is assigned to a stratum, it is ineligible for subsequent strata. `high_causal_any` captures the top-density records not already selected by a category stratum.

### Causal Language Statistics

- Mean causal matches per record: 2.6
- Median: 2
- Records with 5+ matches: 17

---

## 2. Annotator Assignment

Two annotators are assigned. Each annotator completes 100 records independently.

| Record Range | Annotator A | Annotator B | Purpose |
|--------------|-------------|-------------|---------|
| Records 1–80 | Assigned (unique) | Not assigned | Unique set A |
| Records 81–120 | Assigned | Assigned | Overlap set (40 records) |
| Records 121–200 | Not assigned | Assigned (unique) | Unique set B |

- Records 1–80: unique to Annotator A, drawn proportionally from the stratum distribution.
- Records 81–120: the **overlap set** — both annotators complete these 40 records independently, without consulting each other's responses.
- Records 121–200: unique to Annotator B, drawn from the remaining records proportionally from the stratum distribution.

The overlap set exists solely to measure inter-annotator agreement (Section 3). Annotators must not compare or discuss overlap records until after both have submitted.

---

## 3. Metric Definitions

### 3.1 Inter-Annotator Agreement — Cohen's Kappa

Computed on the 40-record overlap set only.

For each record in the overlap set, treat each relation type as a binary presence/absence decision:
- 1 if the annotator recorded at least one edge of that type for that record
- 0 otherwise

Compute Cohen's kappa separately for each relation type (CAUSED_BY, CONTRIBUTED_TO, LED_TO), then report the macro average across the three types.

**Interpretation thresholds:**

| Kappa | Interpretation | Action |
|-------|---------------|--------|
| >= 0.70 | Acceptable agreement | Proceed to LLM evaluation |
| 0.50–0.69 | Moderate agreement | Adjudicate all disagreements on the overlap set before proceeding |
| < 0.50 | Poor agreement | Revise annotation guidelines; re-annotate the overlap set from scratch |

Kappa >= 0.70 is a prerequisite for Gate 3 evaluation. If kappa falls below 0.70, adjudication must be completed and kappa re-computed before any precision/recall evaluation proceeds.

### 3.2 Precision (per relation type)

**Definition:**

    Precision = |LLM_edges ∩ Human_edges| / |LLM_edges|

where the intersection is the count of LLM-predicted edges that match at least one human-annotated edge.

**Edge matching rule:** An LLM edge matches a human edge if all three of the following hold:
1. Same `record_no`
2. Same `relation_type` (CAUSED_BY, CONTRIBUTED_TO, or LED_TO)
3. Token overlap between the LLM cause/factor span and the human cause/factor span is >= 0.50, normalized by the shorter span:

        overlap_ratio = |tokens(LLM_span) ∩ tokens(Human_span)| / min(|tokens(LLM_span)|, |tokens(Human_span)|)

Computed per relation type, then **macro-averaged** across the three types for the aggregate score.

### 3.3 Recall (per relation type)

**Definition:**

    Recall = |LLM_edges ∩ Human_edges| / |Human_edges|

Same matching criteria as Section 3.2. Computed per relation type, then macro-averaged.

### 3.4 Evidence Span Overlap

For each pair of matched edges (matched by the criteria in Section 3.2), compute token-level F1 between the LLM evidence span and the human evidence span:

    Precision_span = |tokens(LLM_evidence) ∩ tokens(Human_evidence)| / |tokens(LLM_evidence)|
    Recall_span    = |tokens(LLM_evidence) ∩ tokens(Human_evidence)| / |tokens(Human_evidence)|
    F1_span        = 2 * Precision_span * Recall_span / (Precision_span + Recall_span)

Report the mean F1_span across all matched edges. This metric is informational only and does not affect Gate 3 pass/fail.

---

## 4. Gate 3 Pass/Fail Criteria

All required metrics must pass for Gate 3 PASS. A single required metric below threshold constitutes Gate 3 FAIL.

| Metric | Threshold | Required? |
|--------|-----------|-----------|
| Cohen's kappa (overlap set, macro avg) | >= 0.70 | Yes (prerequisite — must pass before evaluating precision/recall) |
| Macro precision | >= 0.70 | Yes |
| Macro recall | >= 0.50 | Yes |
| Evidence span F1 (mean) | >= 0.60 | No (informational) |

**Failure diagnosis:**

- Kappa fails: adjudicate annotator disagreements on the overlap set, re-compute kappa, then proceed.
- Precision fails, recall passes: LLM is over-extracting. Tune the confidence threshold upward or tighten the prompt. Re-evaluate without re-annotation.
- Recall fails, precision passes: LLM is under-extracting. Review prompt design and model selection. Re-evaluate without re-annotation.
- Both precision and recall fail: review model output quality holistically before re-evaluating.

---

## 5. Contingency Plan

If Gate 3 fails after one round of tuning, the project falls back to the **L1-only graph** (no causal edges).

The L1 graph (entities + non-causal relations from GLiNER) has already passed Gate 1 and Gate 2 and is production-ready. Causal chain extraction (Layer 2) is a capability enhancement, not a blocker for L1 delivery.

In the fallback state:
- The 200-record annotation set is preserved as a future benchmark.
- Gate 3 remains open for re-evaluation when a stronger extraction model or revised prompt is available.
- The `caused_by_classifier.py` and `relation_extractor.py` components are retained but not integrated into the production pipeline.

---

## 6. Timeline

| Milestone | Target Date |
|-----------|-------------|
| Annotator A completes records 1–120 | TBD |
| Annotator B completes records 81–200 | TBD |
| Kappa computed; adjudication (if needed) | TBD |
| LLM evaluation run (Qwen3-30B-A3B on 200 records) | TBD |
| Precision/recall computed; Gate 3 decision | TBD |
