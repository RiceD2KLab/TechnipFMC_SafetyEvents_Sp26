# V2 Schema Pipeline — Metrics Report

## Gate 1 Results

| Metric | Value | Threshold | Pass? |
|--------|-------|-----------|-------|
| Schema violations | 0 | 0 | PASS |
| Giant component ratio | 1.0 | >= 0.85 | PASS |
| Mean degree | 6.569 | >= 2.0 | PASS |

**Gate 1 overall: PASS**

## Graph Summary

- **Nodes:** 61,545
- **Edges:** 202,141
- **Connected components:** 2

## Node Type Distribution

| Entity Type | Count |
|------------|------:|
| INCIDENT | 19,820 |
| EQUIPMENT | 15,158 |
| LOCATION | 12,810 |
| ORGANIZATION | 9,310 |
| BODY_PART | 2,630 |
| INJURY_TYPE | 1,700 |
| ROOT_CAUSE_CATEGORY | 117 |

## Edge Type Distribution

| Relation Type | Count |
|--------------|------:|
| OCCURRED_AT | 97,903 |
| REPORTED_BY | 42,372 |
| INVOLVED | 28,490 |
| CATEGORIZED_AS | 17,933 |
| AFFECTED | 10,423 |
| RESULTED_IN | 4,459 |
| LOCATED_IN | 561 |

## Comparison Against Baselines

| Method | Giant Component | Mean Degree |
|--------|:-:|:-:|
| spaCy (Fall 2025) | 0.807 | 3.15 |
| Plumber (Fall 2025) | 0.852 | 2.51 |
| Mistral 7B (Fall 2025) | 0.332 | 2.0 |
| GLiNER v1 (999-incident) | 0.959 | 2.408 |
| **GLiNER v2 (this run)** | **1.0** | **6.569** |

## Degree Statistics

- Mean: 6.569
- Median: 1
- Max: 7436
