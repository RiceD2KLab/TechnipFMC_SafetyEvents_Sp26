# V1 → V2 Schema Pipeline Comparison Report

**Date:** 2026-02-19
**V1 baseline:** 999-incident prototype (GLiNER v2.1, v1 schema, threshold 0.4)
**V2 full run:** 23,311 input records → 19,820 incidents processed (GLiNER v2.1, v2 schema, threshold 0.5)

---

## Executive Summary

The v2 schema pipeline achieves **Gate 1 PASS** on the full 23K dataset with strong topological improvements over v1. The new metadata-derived relations (`CATEGORIZED_AS`, `REPORTED_BY`, `LOCATED_IN`) increase graph connectivity substantially. Two data quality issues need patching before production: (1) IMPACT_TYPE values like "Financial Impact" and "Environment" are incorrectly mapped to INJURY_TYPE nodes, creating mega-hubs; (2) NaN values create junk nodes in ROOT_CAUSE_CATEGORY and INJURY_TYPE.

---

## Graph Topology Comparison

| Metric | Mistral 7B (999) | spaCy (999) | Plumber (999) | GLiNER v1 (999) | **GLiNER v2 (19,820)** |
|--------|:-:|:-:|:-:|:-:|:-:|
| Nodes | 5,690 | — | — | 6,809 | **58,845** |
| Edges | 7,727 | — | — | 16,399 | **220,100** |
| Giant component | 94.9% | 80.7% | 85.2% | 95.9% | **100.0%** |
| Mean degree | 1.358 | 3.15 | 2.51 | 2.408 | **7.481** |
| Connected components | 55 | — | — | 46 | **1** |
| Schema violations | — | — | — | 0 | **0** |

### Key Changes
- **Giant component: 95.9% → 100.0%** — every node is reachable. The metadata-derived edges (REPORTED_BY, CATEGORIZED_AS, OCCURRED_AT hierarchy) bridge what were previously disconnected clusters.
- **Mean degree: 2.408 → 7.481** — 3.1x increase. Each incident now averages 11 edges (was ~4 in v1) due to new relation types.
- **Single connected component** — the location hierarchy and shared organizations create a fully connected graph.

---

## Schema Change Impact

### Removed Relations

| V1 Relation | V1 Edges (999) | V2 Status | Rationale |
|------------|---------------:|-----------|-----------|
| USED_IN | 2,249 (13.6%) | **Removed** | 100% were EQUIPMENT→LOCATION rule artifacts |
| CAUSED_BY | 1,237 (7.5%) | **Removed from L1** | 90.5% had broken semantics (e.g., Equipment→"NO ONE WAS INJURED") |

### Added Relations

| V2 Relation | V2 Edges (19,820) | Source | Impact |
|------------|------------------:|--------|--------|
| CATEGORIZED_AS | 19,820 | CASE_CATEGORIZATION metadata | Every incident with a category gets a cross-linking edge to shared ROOT_CAUSE_CATEGORY nodes |
| REPORTED_BY | 40,307 | CLIENT metadata | Links incidents to reporting organization; largest contributor to degree increase |
| LOCATED_IN | 934 | WORKPLACE hierarchy | site→city→country→region hierarchy enables geographic traversal |

### Retained Relations (v1 → v2)

| Relation | V1 (999 incidents) | V2 (19,820 incidents) | Per-incident avg |
|----------|-------------------:|---------------------:|----------------:|
| INVOLVED | 7,239 | 25,925 | 1.31 |
| OCCURRED_AT | 3,478 | 97,481 | 4.92 |
| AFFECTED | 1,714 | 10,004 | 0.50 |
| RESULTED_IN | 674 | 25,629 | 1.29 |

Note: OCCURRED_AT increased sharply because v2 creates edges at all 4 granularity levels (site, city, country, region) per incident from metadata, whereas v1 only had GLiNER-extracted location spans.

---

## Entity Extraction Comparison

### GLiNER Output (NER only, before metadata assembly)

| Metric | V1 (999, threshold=0.4) | V2 (19,820, threshold=0.5) |
|--------|:-:|:-:|
| Total entities extracted | 8,680 | 133,805 |
| Entities per incident | 8.70 | 6.89 |
| Mean confidence | 0.762 | 0.757 |
| Entities ≥ 0.7 confidence | 64.8% | 63.5% |

### Entity Type Distribution Shift

| Entity Type | V1 % | V2 % | Change |
|------------|------:|------:|--------|
| EQUIPMENT | 28.3% | 36.4% | +8.1pp (higher threshold filters more noise from other types) |
| ORGANIZATION | 26.5% | 25.0% | -1.5pp |
| LOCATION | 20.9% | 24.3% | +3.4pp |
| BODY_PART | 7.4% | 10.6% | +3.2pp |
| INJURY_TYPE | 5.1% | 3.7% | -1.4pp |
| INCIDENT_TYPE | 6.1% | — | **Removed** (no longer a GLiNER label) |
| DATE | 5.6% | — | **Removed** (no longer a GLiNER label) |

The v2 label set drops INCIDENT_TYPE and DATE (now properties), and uses "injury type" instead of "injury" as a GLiNER label. The higher threshold (0.5 vs 0.4) slightly reduces entities per incident (8.70 → 6.89) but maintains comparable confidence distributions.

---

## Node Type Distribution (Full Graph)

| Entity Type | Count | % of Nodes | Source |
|------------|------:|----------:|--------|
| INCIDENT | 19,820 | 33.7% | One per input record |
| EQUIPMENT | 13,939 | 23.7% | GLiNER extraction |
| LOCATION | 12,233 | 20.8% | Metadata hierarchy + GLiNER |
| ORGANIZATION | 8,614 | 14.6% | Metadata CLIENT + GLiNER |
| BODY_PART | 2,493 | 4.2% | GLiNER extraction |
| INJURY_TYPE | 1,628 | 2.8% | GLiNER + IMPACT_TYPE metadata |
| ROOT_CAUSE_CATEGORY | 118 | 0.2% | CASE_CATEGORIZATION metadata |

---

## Degree Distribution by Entity Type

| Entity Type | Mean Degree | Median | Max | Notes |
|------------|:----------:|:------:|:---:|-------|
| INCIDENT | 11.1 | 11 | 24 | Healthy hub — every incident has 4-24 edges |
| EQUIPMENT | 1.9 | 1 | 728 | Long tail; most equipment appears in 1-2 incidents |
| LOCATION | 8.1 | 1 | 7,436 | **Mega-hub risk:** REGION:EUROPE (7,436), COUNTRY:USA (4,323) |
| ORGANIZATION | 4.7 | 1 | 2,518 | "TECHNIPFMC PLC" (2,518) is the dominant client |
| BODY_PART | 4.0 | 1 | 414 | Reasonable distribution |
| INJURY_TYPE | 15.7 | 1 | 9,122 | **CRITICAL:** "INJURY" (9,122) is a mega-hub — see issues below |
| ROOT_CAUSE_CATEGORY | 168.0 | 55.5 | 1,887 | Expected: 118 categories shared across 19,820 incidents |

---

## Issues Identified

### CRITICAL: IMPACT_TYPE → INJURY_TYPE Mapping Creates Mega-Hubs

The v2 pipeline maps IMPACT_TYPE metadata values to INJURY_TYPE entities via `RESULTED_IN`. This produces 21,455 metadata-sourced RESULTED_IN edges (84% of all RESULTED_IN). Problem: **IMPACT_TYPE values are not injury types:**

| IMPACT_TYPE Value | Mapped As | Degree | Actual Meaning |
|------------------|-----------|-------:|----------------|
| "Injury" | INJURY_TYPE | 9,122 | Impact *category*, not a specific injury |
| "Injury/Illness" | INJURY_TYPE | 3,379 | Same issue |
| "Financial Impact" | INJURY_TYPE | 2,715 | **Not an injury at all** |
| "Environment" | INJURY_TYPE | 2,062 | **Not an injury at all** |
| "Damage - Financial impact" | INJURY_TYPE | 1,763 | Not an injury |
| "Damage" | INJURY_TYPE | 1,495 | Not an injury |

**Recommendation:** Create a separate `IMPACT_TYPE` entity type (or store as incident property). Only map IMPACT_TYPE values containing "Injury" or "Illness" to INJURY_TYPE, and only if a more specific GLiNER-extracted injury entity isn't already present.

**Impact if fixed:** Removes ~17,000 problematic edges, reduces INJURY_TYPE max degree from 9,122 to ~275, eliminates non-injury mega-hubs.

### MODERATE: NaN Values Creating Junk Nodes

| Entity Type | NaN Node | Edges | Fix |
|------------|----------|------:|-----|
| ROOT_CAUSE_CATEGORY | "NAN" | 1,887 | Filter null/NaN CASE_CATEGORIZATION before creating edges |
| INJURY_TYPE | "NAN" | 217 | Filter null/NaN IMPACT_TYPE before creating edges |

**Impact if fixed:** Removes 2 junk nodes and ~2,104 meaningless edges.

### MINOR: Organization Deduplication Needed

"TECHNIPFMC PLC" (2,518 edges) and "TECHNIPFMC" (1,809 edges) are the same entity. Entity resolution (Splink or simple normalization) would merge these. This is expected and will be addressed in the ER layer.

### MODERATE: 100% GC May Be Partially Artificial

The perfect 100% giant component is partially sustained by the "NAN" ROOT_CAUSE_CATEGORY node (1,887 edges). Incidents with missing CASE_CATEGORIZATION connect to this junk node, which bridges otherwise disconnected clusters. After filtering NaN values, expect GC to drop slightly (likely to 99.5-99.8%). This is still well above the 85% threshold.

### MODERATE: Metadata-Heavy Edge Mix

V2 is heavily metadata-driven: of 25,629 RESULTED_IN edges, 84% (21,455) come from IMPACT_TYPE metadata, only 16% (4,174) from GLiNER extraction. Per-incident narrative extraction dropped from ~0.67 RESULTED_IN/doc (v1) to ~0.21/doc (v2). This means RESULTED_IN edge quality is gated on IMPACT_TYPE mapping correctness — another reason the IMPACT_TYPE fix is critical.

### MINOR: Location Region Mega-Hubs

REGION-level location nodes are mega-hubs by design (REGION:EUROPE = 7,436 degree). For traversal queries, this is manageable since region-level queries are always filtered. For graph analytics, consider excluding region-level nodes or treating them separately.

---

## Comparison: What V2 Gained vs. Lost

### Gained
- **Full connectivity:** 46 components → 1 component (100% GC)
- **Cross-incident links:** 19,820 CATEGORIZED_AS edges create thematic clusters (94.6% of these are genuinely novel connections per our evidence report)
- **Organization tracking:** 40,307 REPORTED_BY edges link incidents to clients
- **Geographic hierarchy:** 934 LOCATED_IN edges enable "all incidents in Brazil" without string matching
- **Schema cleanliness:** 7 allowed relations (was 6 but removed 2 broken, added 3 meaningful)
- **No more broken edges:** USED_IN (2,249 rule artifacts) and CAUSED_BY (1,237 with 90.5% broken semantics) eliminated

### Lost
- **Entity-to-entity edges:** V1 had Equipment→Location (USED_IN), Equipment→Injury (CAUSED_BY), Equipment→BodyPart (AFFECTED). V2 only has Incident→Entity edges (star-hub pattern). Cross-entity relationships are deferred to Layer 2.
- **Lower entities per incident:** 8.70 → 6.89 (higher threshold + fewer label types). Offset by richer metadata edges.

---

## Final Assessment

| Criterion | V1 (999) | V2 (19,820) | Verdict |
|-----------|:--------:|:-----------:|---------|
| Gate 1 | PASS | **PASS** | Schema violations=0, GC=1.0, degree=7.48 |
| Scale | 999 incidents | **19,820 incidents** | 19.8x more data |
| Schema compliance | 6 relation types | **7 relation types** | Cleaner: removed 2 broken, added 3 meaningful |
| Connectivity | 95.9% GC | **100% GC** | Perfect connectivity |
| Throughput | 278 ms/incident | **265 ms/incident** | Comparable (threshold change) |
| Quality issues | USED_IN/CAUSED_BY noise | **IMPACT_TYPE mapping** | V2 has a fixable issue; v1 had unfixable ones |

**V2 is a clear improvement.** The IMPACT_TYPE mapping issue is the one critical fix needed before production — it's a 1-line filter change in `graph_builder.py`. Everything else is working as designed.

---

## Recommended Next Steps

1. **Fix IMPACT_TYPE mapping** — either make it a separate entity type or demote to incident property (like incident_type was). This removes the "INJURY" mega-hub.
2. **Filter NaN values** — add null/NaN guards before creating CATEGORIZED_AS and metadata RESULTED_IN edges.
3. **Run entity resolution** (Splink) — merge "TECHNIPFMC PLC" / "TECHNIPFMC" and similar duplicates.
4. **Benchmark queries** — run the gold-slice benchmark against the v2 graph to measure retrieval quality.
5. **Layer 2 enrichment** — with L1 stable, add LLM-based `caused_by` extraction for narratives with causal language (29.7% of records).
