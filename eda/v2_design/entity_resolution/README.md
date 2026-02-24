# Entity Resolution Exploration

Systematic evaluation of entity resolution strategies to determine what was feasible,
what was risky, and what the production ER pipeline should look like.

## Context

After schema enforcement, the v2 graph had clean entity types but massive duplication:
"FORKLIFT", "Forklift", "Fork Lift", "FLT" all appeared as separate EQUIPMENT nodes.
This exploration tested multiple ER approaches to understand the merging landscape
before building `pipeline_v2/er_prep/` and `pipeline_v2/er_execution/`.

## Analysis Flow

```
Schema-filtered entities (65K nodes)
    │
    ├─ fuzzy_match_candidates.py ──► 11,381 candidate pairs (rapidfuzz, threshold 0.9)
    │
    ├─ test_er_approaches.py ──► 5 strategies evaluated on real data
    │
    ├─ merge_simulation.py ──► Transitive closure impact simulation
    │
    ├─ label_pairs.py ──► Weak label generation for Splink training
    │   └─ review_priority_batch.py ──► Risk-scored human review batch
    │
    ├─ splink_pilot.py ──► Basic probabilistic linkage (Jaro-Winkler)
    │   └─ splink_pilot_labeled.py ──► Enhanced with domain features + weak labels
    │
    ├─ type_cluster_diagnostics.py ──► Per-type cluster analysis (strict vs loose)
    │
    └─ equipment_taxonomy.json ──► 31 canonical equipment classes
```

## Key Findings

### The Sobering Reality (test_er_approaches.py)

| Finding | Number | Implication |
|---------|--------|-------------|
| Equipment false positive rate | **81.3%** | Most high-similarity equipment pairs have different part numbers |
| Safe conservative merges | **515** | Only 0.6% degree improvement |
| Merges needed for degree 4.0 | **~44,500** | Conservative ER covers 1.2% of the gap |
| Cross-country location pairs | **21** | Naive location matching creates false links |

**Bottom line:** Entity resolution alone cannot close the connectivity gap. The v2 pipeline
gets its connectivity from metadata edges (OCCURRED_AT, REPORTED_BY, etc.), not from ER.

### Fuzzy Matching (fuzzy_match_candidates.py)

- 11,381 candidate pairs at similarity >= 0.9
- 81.4% scored >= 0.95 (high confidence)
- But high similarity != correct match for equipment (numbers matter)

### Merge Simulation (merge_simulation.py)

- 1,027 high-confidence pairs (>= 0.95, num_jaccard >= 0.8)
- Transitive closure: 857 nodes merged
- Degree improvement: 1.625 -> 1.644 (+0.12%)
- Verdict: **marginal impact from conservative merging**

### Splink Pilots

- **Basic (splink_pilot.py):** Conservative blocking (type + first_char) too restrictive;
  only 56 entities absorbed from 2,000-entity sample.
- **Enhanced (splink_pilot_labeled.py):** Adding equipment_class, stopword removal, and
  numeric/unit extraction features significantly improved linkage quality.

### Cluster Diagnostics (type_cluster_diagnostics.py)

| Setting | Total Merges | Largest Cluster | Risk |
|---------|-------------|----------------|------|
| Strict (0.95, num_jaccard 0.8) | 889 | 18 (equipment) | Low |
| Loose (0.90, num_jaccard 0.5) | ~2,500 | ~55 (location) | Medium-high |

### Number-Based Filtering is Critical

The single most important finding: **entities with numeric identifiers must be matched
on numbers, not just text similarity.** "Pump 1A" and "Pump 2A" score 0.95 similarity
but are completely different equipment. The `num_jaccard >= 0.8` guard catches this.

## Decision Impact

These findings shaped the production ER pipeline (`pipeline_v2/er_execution/`):
- **Deterministic normalization first** (case, whitespace, suffix stripping)
- **Strict number matching** for equipment entities
- **Domain features** (equipment_class from taxonomy) for Splink blocking
- **Gate 2 thresholds** include overmerge detection (max cluster size cap)
- **Metadata edges carry connectivity**, not ER — ER is for deduplication quality

## Files

| File | Purpose |
|------|---------|
| `fuzzy_match_candidates.py` | Candidate pair mining (rapidfuzz) |
| `fuzzy_match_candidates.csv` | 11,381 candidate pairs |
| `fuzzy_match_candidates_training.csv` | Training-formatted candidates |
| `test_er_approaches.py` | 5-strategy ER evaluation |
| `er_approaches_test_results.json` | Strategy comparison results |
| `merge_simulation.py` | Transitive closure impact simulation |
| `merge_simulation*.json` | Results at different thresholds |
| `splink_pilot.py` | Basic Splink feasibility pilot |
| `splink_pilot*.json` | Pilot results (various blocking configs) |
| `splink_pilot_labeled.py` | Enhanced Splink with domain features |
| `splink_pilot_labeled*.json` | Enhanced pilot results |
| `label_pairs.py` | Weak label + review sample generator |
| `pairwise_labels_*.csv` | Generated labels and review batches |
| `review_priority_batch.py` | Risk-scored human review batch |
| `type_cluster_diagnostics.py` | Per-type cluster analysis |
| `type_cluster_diagnostics_*.csv/json` | Strict and loose results |
| `equipment_taxonomy.json` | 31 canonical equipment classes |
