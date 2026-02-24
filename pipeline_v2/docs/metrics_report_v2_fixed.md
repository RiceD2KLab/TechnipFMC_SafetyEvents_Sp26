# V2 Pipeline Fix — Before/After Comparison Report

**Date:** 2026-02-19
**Dataset:** Test set (1,000 incidents, GLiNER threshold 0.5)
**Fixes applied:** IMPACT_TYPE demotion, NaN filtering, Unknown location filtering

---

## Gate 1 Results (After Fix)

| Metric | Value | Threshold | Pass? |
|--------|-------|-----------|-------|
| Schema violations | 0 | 0 | PASS |
| Giant component ratio | 1.0 | >= 0.85 | PASS |
| Mean degree | 4.616 | >= 2.0 | PASS |

**Gate 1 overall: PASS**

---

## Before/After Comparison (Test Set, 1,000 Incidents)

### Graph Topology

| Metric | Before Fix | After Fix | Delta |
|--------|:---------:|:---------:|:-----:|
| Nodes | 4,337 | 4,328 | **-9** |
| Edges | 11,373 | 9,988 | **-1,385** |
| Connected components | 1 | 1 | 0 |
| Giant component ratio | 1.0 | 1.0 | 0 |
| Mean degree | 5.245 | 4.616 | -0.629 |
| Median degree | 1 | 1 | 0 |
| Max degree | 592 | 391 | **-201** |

### Node Type Distribution

| Entity Type | Before | After | Delta | Notes |
|------------|------:|------:|------:|-------|
| EQUIPMENT | 1,072 | 1,072 | 0 | Unchanged (GLiNER only) |
| LOCATION | 1,035 | 1,031 | **-4** | "Unknown" locations filtered |
| INCIDENT | 1,000 | 1,000 | 0 | — |
| ORGANIZATION | 756 | 755 | **-1** | NaN org filtered |
| BODY_PART | 270 | 270 | 0 | Unchanged (GLiNER only) |
| INJURY_TYPE | 152 | 149 | **-3** | NaN + metadata IMPACT_TYPE entities removed |
| ROOT_CAUSE_CATEGORY | 52 | 51 | **-1** | NaN category filtered |

9 junk nodes removed (NaN values + "Unknown" locations + non-injury IMPACT_TYPE entities).

### Edge Type Distribution

| Relation Type | Before | After | Delta | Notes |
|--------------|------:|------:|------:|-------|
| OCCURRED_AT | 5,029 | 4,976 | **-53** | "Unknown" location edges filtered |
| REPORTED_BY | 1,971 | 1,924 | **-47** | NaN/null client edges filtered |
| INVOLVED | 1,370 | 1,370 | 0 | — |
| RESULTED_IN | 1,229 | 229 | **-1,000** | IMPACT_TYPE→INJURY_TYPE edges removed |
| CATEGORIZED_AS | 1,000 | 739 | **-261** | NaN category edges filtered |
| AFFECTED | 515 | 515 | 0 | — |
| LOCATED_IN | 259 | 235 | **-24** | "Unknown" hierarchy edges filtered |

**Total edges removed: 1,385** — of which 1,000 (72%) were the IMPACT_TYPE→INJURY_TYPE mapping.

---

## Mega-Hub Health Check

### Before Fix

| Entity Type | Mean Degree | Median | Max | Top Hub |
|------------|:----------:|:------:|:---:|---------|
| INCIDENT | 11.1 | 11 | 24 | — |
| INJURY_TYPE | 15.7 | 1 | **592** | "INJURY" (mega-hub) |
| ROOT_CAUSE_CATEGORY | 21.2 | — | ~170 | "NAN" (junk node) |

### After Fix

| Entity Type | Mean Degree | Median | Max | Top Hub |
|------------|:----------:|:------:|:---:|---------|
| INCIDENT | 9.8 | 9 | 21 | Healthy |
| EQUIPMENT | 1.3 | 1 | 47 | "forklift" (reasonable) |
| LOCATION | 5.3 | 1 | 391 | "Europe" (region-level, by design) |
| ORGANIZATION | 2.5 | 1 | 239 | "TECHNIPFMC PLC" (expected) |
| BODY_PART | 1.9 | 1 | 26 | "left hand" (reasonable) |
| INJURY_TYPE | 1.5 | 1 | **16** | "injuries" (healthy) |
| ROOT_CAUSE_CATEGORY | 14.5 | 8 | 62 | "Hazard ID & Risk Assessment" (expected) |

**Key result: INJURY_TYPE max degree dropped from 592 → 16** (97.3% reduction). The "INJURY" mega-hub is gone. No artificial mega-hubs remain. The remaining high-degree nodes (Europe=391, TECHNIPFMC PLC=239) are real structural hubs that represent genuine data patterns.

---

## Fix Summary

| Fix | What Changed | Impact |
|-----|-------------|--------|
| **IMPACT_TYPE demotion** | Removed IMPACT_TYPE→INJURY_TYPE entity mapping. IMPACT_TYPE is now stored as an incident node property only. | -1,000 edges, -3 nodes. Eliminated the "INJURY" mega-hub (592→16 max degree). |
| **NaN filtering** | Added `_is_valid_value()` guard that rejects `None`, `""`, `"nan"`, `"none"`, `"null"`, `"unknown"`. Applied to REPORTED_BY, CATEGORIZED_AS, OCCURRED_AT, and location hierarchy. | -385 edges, -6 nodes. Removed junk "NAN" nodes from ROOT_CAUSE_CATEGORY and INJURY_TYPE. |

---

## Comparison Against All Baselines

| Method | Nodes | Edges | Giant Component | Mean Degree |
|--------|------:|------:|:-:|:-:|
| spaCy (Fall 2025) | — | — | 0.807 | 3.15 |
| Plumber (Fall 2025) | — | — | 0.852 | 2.51 |
| Mistral 7B (Fall 2025) | 5,690 | 7,727 | 0.332 | 2.0 |
| GLiNER v1 (999 incidents) | 6,809 | 16,399 | 0.959 | 2.408 |
| GLiNER v2 pre-fix (1,000 incidents) | 4,337 | 11,373 | 1.0 | 5.245 |
| **GLiNER v2 post-fix (1,000 incidents)** | **4,328** | **9,988** | **1.0** | **4.616** |

Mean degree dropped from 5.245→4.616 but remains well above the 2.0 Gate 1 threshold. The decrease is entirely healthy — it reflects the removal of 1,000 spurious IMPACT_TYPE edges that inflated degree artificially.

---

## Recommendation: Full Re-Run Required

The test-set GLiNER output was accidentally overwritten (the full-run GLiNER extraction covering 19,820 incidents is lost). The fixes are validated on the 1,000-incident test set and all gates pass.

**Next step:** Re-run the full pipeline end-to-end:

```bash
.venv/bin/python pipeline_v2/run_gliner_pipeline.py --full
```

**Expected time:** ~90 minutes (GLiNER extraction dominates).

**Expected results (projected from test-set ratios):**

| Metric | Pre-fix (19,820) | Post-fix (projected) |
|--------|:----------------:|:-------------------:|
| Nodes | 58,845 | ~58,800 |
| Edges | 220,100 | ~198,000 |
| Giant component | 1.0 | ~0.999 |
| Mean degree | 7.481 | ~6.7 |
| INJURY_TYPE max degree | 9,122 | ~275 |

The giant component may dip slightly below 1.0 since the "NAN" ROOT_CAUSE_CATEGORY node (which bridged 1,887 incidents with missing categories) is now filtered. This is correct behavior — the 99.5%+ GC expected is genuine connectivity, not junk-node bridging.
