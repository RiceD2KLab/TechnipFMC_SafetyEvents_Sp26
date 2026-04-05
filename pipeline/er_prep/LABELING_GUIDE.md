# Entity Pair Labeling Guide

## What This Is

The knowledge graph has ~61,000 entity nodes extracted from 19,820 safety incident reports. Many of these are duplicates with slightly different text: "Forklift" vs "Fork Lift" vs "FLT", or "left hand" vs "hand". We need human labels to tell us which pairs refer to the same real-world thing and which are genuinely different.

Your labels will train a probabilistic entity resolution model (Splink) that merges duplicates at scale.

## What You'll Label

**File to fill out:** `pairwise_labels_review_priority.csv` (200 pairs, ~30-45 min)

Each row is a candidate pair of entities. You fill in the `is_match` column:

| Value | Meaning |
|-------|---------|
| `1` | **Same entity** — these refer to the same real-world thing and should be merged |
| `0` | **Different entities** — these are genuinely distinct and must stay separate |

## How to Open and Edit

1. Open `pipeline/er_prep/pairwise_labels_review_priority.csv` in Excel or Google Sheets
2. The first column `is_match` is empty — that's what you fill in
3. Save as CSV when done (do not change any other columns)

## Columns Explained

| Column | What It Means |
|--------|---------------|
| `is_match` | **YOU FILL THIS IN.** 1 = same, 0 = different |
| `type` | Entity type (EQUIPMENT, LOCATION, ORGANIZATION, etc.) |
| `title_l` | Left entity text |
| `title_r` | Right entity text |
| `score` | Text similarity (0-1). Higher = more similar looking |
| `nums_l` / `nums_r` | Numbers extracted from each entity |
| `num_jaccard` | How much the numbers overlap (0 = totally different numbers, 1 = same numbers) |
| `num_mismatch` | `True` if the entities have different numbers |
| `risk_score` | How risky this pair is to get wrong (higher = more impactful) |

**You only need to look at `type`, `title_l`, `title_r`, and the number columns.** The rest is for the model.

## Decision Rules

### The #1 Rule: Numbers Matter

Entities with different identifying numbers are almost always **different things**, even if the text looks nearly identical.

| Pair | Numbers | Label | Why |
|------|---------|-------|-----|
| "Pump 1A" vs "Pump 2A" | 1A vs 2A | **0** (different) | Different pump units |
| "DEEP-C DREDGER (SD-038)" vs "DEEP-C DREDGER (SD-120)" | 038 vs 120 | **0** (different) | Different vessels |
| "COMPANY VEHICLE LD3704" vs "COMPANY VEHICLE LD3890" | 3704 vs 3890 | **0** (different) | Different vehicles |

**If `num_mismatch` is `True`, the answer is almost always `0`.**

### When to Label `1` (Same Entity)

- **Spelling/capitalization variants:** "forklift" vs "Fork Lift" vs "Forklift"
- **Abbreviation vs full name:** "ROV" vs "Remotely Operated Vehicle"
- **Punctuation differences:** "ROLLER PATHS" vs "ROLLER-PATHS"
- **Laterality stripped (body parts):** "left hand" vs "hand" — label `1` only if you believe these should be merged for analysis purposes (we track laterality as a modifier, not a separate entity)
- **Legal suffix differences (orgs):** "TECHNIPFMC PLC" vs "TECHNIPFMC"

### When to Label `0` (Different Entity)

- **Different numbers/identifiers** (see rule above)
- **Different equipment units:** "Crane 1" vs "Crane 2"
- **Different locations with similar names:** "Production Shop 2" vs "Production Shop 02" — check if the numbers match (here 2 == 02, so this is `1`)
- **Genuinely different things:** "back" (body part) vs "back deck" (location)

### When You're Unsure

If a pair is genuinely ambiguous, label it `0` (don't merge). It's safer to leave duplicates separate than to wrongly merge different things. The pipeline has a guardrail that catches over-merging, but it can't undo a bad merge.

## Examples

| type | title_l | title_r | is_match | Reasoning |
|------|---------|---------|----------|-----------|
| EQUIPMENT | ROLLER PATHS | ROLLER-PATHS | **1** | Same thing, punctuation difference |
| EQUIPMENT | DEEP-C DREDGER (SD-038) | DEEP-C DREDGER (SD-120) | **0** | Different vessel IDs |
| ORGANIZATION | LLC VELESTOY | LLC VELESSTROY | **1** | Likely same org, typo |
| LOCATION | DECK | DECK 'B' | **0** | Different deck sections |
| BODY_PART | left ancle | ancle | **1** | Same body part, laterality stripped |
| EQUIPMENT | STBD AIR CONDITION COMPRESSOR UNIT 2 | STBD AIR CONDITION COMPRESSOR UNIT 1 | **0** | Different unit numbers |
| LOCATION | PRODUCTION SHOP 2 | PRODUCTION SHOP 02 | **1** | Same number (2 == 02) |

## After Labeling

Save the CSV and notify the team. The labeled file is consumed by:
```
pipeline/er_prep/splink_config/  (Splink model training configs)
```

With 200 labeled pairs, Splink can learn entity-type-specific merge thresholds that outperform the current fixed 0.90 similarity cutoff. The model uses your labels plus the similarity scores, number overlap, and blocking features to predict matches across all 10,140 candidate pairs.

## Priority File vs Full File

| File | Pairs | What It Contains |
|------|-------|------------------|
| `pairwise_labels_review_priority.csv` | 200 | **Start here.** Highest-risk pairs where the model is most uncertain |
| `pairwise_labels_review.csv` | 500 | Broader sample across all entity types. Label after priority batch if time permits |
| `merge_candidates.csv` | 10,140 | All candidates — the model predicts these after training on your labels |

## Time Estimate

- Priority batch (200 pairs): **30-45 minutes**
- Full batch (500 pairs): **1-2 hours**
- Most pairs with `num_mismatch=True` are instant `0` decisions
