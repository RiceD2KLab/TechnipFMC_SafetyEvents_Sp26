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

### Distribution by Stratum

| Stratum | Count | Mean Causal Density | Mean Tokens |
|---------|------:|-------------------:|------------:|
| fire_explosion | 50 | 0.0344 | 60 |
| falls_slips | 40 | 0.0393 | 51 |
| dropped_objects | 30 | 0.0515 | 64 |
| transportation | 20 | 0.0484 | 48 |
| containment_loss | 20 | 0.0540 | 81 |
| high_causal_any | 40 | 0.0691 | 45 |

---

## 2. Annotator Assignment

Two LLM annotators were used. Each annotator completed all 200 records.

| Annotator | Backend | Edges Produced |
|-----------|---------|---------------:|
| Annotator A (Claude) | claude-sonnet-4-6 | 464 |
| Annotator B (Codex) | codex-v1 | 407 |

The overlap set (records 81-120, 40 records) is used for inter-annotator agreement.

---

## 3. Relation Schema

Annotations use the **L2 causal relation schema** (3 relation types):

| Relation | Description | Direction |
|----------|-------------|-----------|
| CAUSAL | X caused or contributed to Y | source=cause, target=effect |
| PRECEDED_BY | Temporal sequence with causal link | source=later, target=earlier |
| FAILED_CONTROL | Safety barrier failed to prevent Y | source=barrier, target=what it failed to prevent |

Entity types (9): Incident, Event, Equipment, Location, Person, Injury, Material, Condition, Action.

Output format: JSONL edges (one per line).

---

## 4. Metric Definitions

### 4.1 Inter-Annotator Agreement — Cohen's Kappa

Computed on the overlap set (records 81-120). For each record, each relation type
is binarised (1 if annotator produced at least one edge of that type, 0 otherwise).
Cohen's kappa computed per relation type.

**Note:** For high-prevalence relations (e.g., CAUSAL present in >95% of records),
kappa is unreliable. Raw agreement rate is the primary metric in that case.

### 4.2 Precision@K (per record)

For each record, only the top-K predicted edges are scored (K = number of GT edges
for that record). Edges are ranked by similarity to GT edges.

### 4.3 Recall (per relation type)

    Recall = |matched GT edges| / |GT edges|

Edge matching uses token-overlap with stop-word removal. For CAUSAL edges,
matching is **direction-agnostic** (tries both source↔source/target↔target and
source↔target/target↔source alignments).

### 4.4 Evidence Span F1

Token-level F1 between predicted and GT evidence spans. Informational only.

---

## 5. Gate 3 Pass/Fail Criteria

| Metric | Threshold | Required? |
|--------|-----------|-----------|
| IAA (CAUSAL raw agreement or kappa >= 0.70) | >= 95% agreement or kappa >= 0.70 | Yes (prerequisite) |
| Precision@K | >= 50% | Yes |
| Causal recall | >= 35% | Yes |
| Evidence span F1 | >= 60% | No (informational) |
| Causal presence | >= 75% | Yes |
| JSON validity | >= 99% | Yes |

---

## 6. Current Results

### Gate 3 vs Codex GT: **PASS**
- Precision@K: 63.3%
- Causal recall: 57.7%
- Evidence F1: 80.1%
- Causal presence: 78.6%

### Gate 3 vs Claude GT: **FAIL**
- Precision@K: 49.8%
- Causal recall: 44.2%
- Evidence F1: 75.9%
- Causal presence: 74.9%

### IAA: **PASS**
- CAUSAL raw agreement: 98.5% (kappa unreliable at this prevalence)
