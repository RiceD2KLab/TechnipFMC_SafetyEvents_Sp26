# V2 Schema Pipeline — Metrics Report

## Gate 1 Results

| Metric | Value | Threshold | Pass? |
|--------|-------|-----------|-------|
| Schema violations | 0 | 0 | PASS |
| Giant component ratio | 1.0 | >= 0.85 | PASS |
| Mean degree | 6.42 | >= 2.0 | PASS |

**Gate 1 overall: PASS**

## Graph Summary

- **Nodes:** 77,435
- **Edges:** 248,549
- **Connected components:** 2

## Node Type Distribution

| Entity Type | Count |
|------------|------:|
| EQUIPMENT | 24,465 |
| INCIDENT | 19,820 |
| LOCATION | 16,672 |
| ORGANIZATION | 9,835 |
| BODY_PART | 3,594 |
| INJURY_TYPE | 2,932 |
| ROOT_CAUSE_CATEGORY | 117 |

## Edge Type Distribution

| Relation Type | Count |
|--------------|------:|
| OCCURRED_AT | 108,640 |
| INVOLVED | 54,865 |
| REPORTED_BY | 44,646 |
| CATEGORIZED_AS | 17,933 |
| AFFECTED | 12,854 |
| RESULTED_IN | 9,054 |
| LOCATED_IN | 557 |

## Comparison Against Baselines

| Method | Giant Component | Mean Degree |
|--------|:-:|:-:|
| spaCy (Fall 2025) | 0.807 | 3.15 |
| Plumber (Fall 2025) | 0.852 | 2.51 |
| Mistral 7B (Fall 2025) | 0.332 | 2.0 |
| GLiNER v1 (999-incident) | 0.959 | 2.408 |
| **GLiNER v2 (this run)** | **1.0** | **6.42** |

## Degree Statistics

- Mean: 6.42
- Median: 1
- Max: 7436
