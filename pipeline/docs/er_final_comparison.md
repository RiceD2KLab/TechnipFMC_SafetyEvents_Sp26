# ER Final Comparison Report

**Generated:** 2026-02-19
**Pipeline:** Deterministic ER + schema violation fix + query patches

---

## Three-Column Comparison

| ID | Query | Pre-ER | Post-ER (fixed) | Change |
|----|-------|:------:|:---------------:|--------|
| SH-01 | Forklift 2022 | ✅ 73 inc, 171 variants | ✅ 71 inc, merged | variants consolidated |
| SH-02 | Equipment for #29857 | ⚠️ missing TMS | ⚠️ missing TMS | unchanged (extraction gap) |
| SH-03 | Body parts in crane | ✅ top: left hand (17) | ✅ top: finger (35) | **body parts consolidated** |
| SH-04 | Valve locations | ✅ 37 countries | ✅ 36 countries | minor cleanup |
| SH-05 | Offshore injuries | ✅ 153 injury types | ✅ 124 injury types | **-29 deduped types** |
| SH-06 | Shell Offshore | ✅ 51 variants | ✅ 47 variants | -4 org variants |
| AG-01 | RCC dropped objects | ✅ top: Mech - Stored energy | ✅ top: Stored energy (367) | **RCC consolidated** |
| AG-02 | High-sev countries | ✅ 22 countries | ✅ 22 countries | unchanged |
| AG-03 | Top equipment | ✅ 15,158 types, forklift=734 | ✅ 13,446 types, forklift=771 | **-1,712 types, +37 forklift** |
| AG-04 | Incident × BU | ⚠️ 75% null | ⚠️ 75% null | unchanged (data gap) |
| AG-05 | Fall/slip trend | ✅ 4 RCC categories | ✅ 2 RCC categories | **RCC deduplicated** |
| AG-06 | Severity × impact | ✅ 3 impact types | ✅ 3 impact types | unchanged |
| MH-01 | Containment→injury | ⚠️ 1 incident | ⚠️ 1 incident | unchanged (sparse) |
| MH-02 | Equip fail maintenance | ✅ 19 pairs | ✅ 18 pairs | minor dedup |
| MH-03 | Vessel + back + client | ❌ 0 results | ⚠️ 1 result | **❌→⚠️ (broadened)** |
| MH-04 | Injury per equipment | ✅ | ✅ | consolidation |
| MH-05 | Hand + pipe + APAC | ✅ 6 | ✅ 6 | unchanged |
| MH-06 | Trucks vs cranes sev | ✅ | ✅ | unchanged |
| MH-07 | Scaffold near-misses | ✅ 36 cities | ✅ 33 cities, 121 NMs | **zObsolete cleaned, +6 NMs** |
| MH-08 | Hydraulic valve→injury | ⚠️ 3 inc, 0 injuries | ⚠️ 3 inc, 0 injuries | unchanged |
| GL-01 | Louvain clusters | ✅ 37 communities | ✅ 64 communities | more granular |
| GL-02 | Equipment × regions | ✅ 123 global | ✅ 144 global | **+21 cross-region equip** |
| GL-03 | Temporal trend | ✅ | ✅ | unchanged |
| GL-04 | Hub centrality | ✅ | ✅ | hubs consolidated |
| CJ-01 | Corrosion→fire (L2) | ❌ 0 causal | ❌ 0 causal | unchanged (needs L2) |
| CJ-02 | Crane+back+offshore+sev | ⚠️ 0 | ⚠️ 0 | unchanged (sparse) |
| CJ-03 | Maint+pipe+env+ME | ⚠️ 0 | ⚠️ 0 | unchanged (sparse) |
| CJ-04 | Equipment dual-risk | ✅ 548 | ✅ 539 | minor dedup |
| CJ-05 | Procedural→dropped (L2) | ⚠️ 4 approx | ⚠️ 4 approx | **regression fixed** |
| CJ-06 | Falls+vehicle+construction | ✅ 15 | ✅ 16 | +1 from schema fix |

---

## Score Change

| Query Type | Pre-ER | Post-ER (fixed) | Delta |
|-----------|:------:|:---------------:|:-----:|
| Single-hop (6) | 5/6 | 5/6 | 0 |
| Aggregation (6) | 5/6 | 5/6 | 0 |
| Multi-hop (8) | 5/8 | 5/8 | 0 |
| Global (4) | 4/4 | 4/4 | 0 |
| Conjunctive (6) | 2/6 | 2/6 | 0 |
| **TOTAL** | **21/30** | **21/30** | **0** |

**MH-03 upgraded from ❌ FAIL to ⚠️ PARTIAL** (vessel broadening found 1 result). The binary score stays 21/30 because the benchmark counts ⚠️ as partial, not full pass. However, the pre-ER graph had 2 ❌ and 7 ⚠️; the post-ER fixed graph has 1 ❌ and 7 ⚠️ — a net improvement of 1 fewer failure.

---

## Key Metrics for Presentation

### 1. Topology Improvement

| Metric | Pre-ER | Post-ER | Delta |
|--------|:------:|:-------:|:-----:|
| Nodes | 61,545 | 56,408 | **-5,137 (-8.3%)** |
| Edges | 202,141 | 199,902 | -2,239 (-1.1%) |
| Mean degree | 6.57 | 7.09 | **+0.52 (+7.9%)** |
| Giant component | 100% | 99.96% | -0.04pp |
| Schema violations | 2,123* | **0** | **all fixed** |

*Schema violations were introduced by multi-type resolution and fixed in a separate pass.

### 2. Entity Compression Ratios

| Entity Type | Pre-ER | Post-ER | Compression | Notes |
|-------------|:------:|:-------:|:-----------:|-------|
| ROOT_CAUSE_CATEGORY | 117 | 73 | **37.6%** | Prefix normalization (largest ratio) |
| LOCATION | 12,810 | 10,744 | 16.1% | zObsolete cleanup + ER merging |
| INJURY_TYPE | 1,700 | 1,465 | 13.8% | Severity qualifier stripping |
| BODY_PART | 2,630 | 2,315 | 12.0% | Laterality merging |
| EQUIPMENT | 15,158 | 13,446 | 11.3% | Plural/variant normalization |
| ORGANIZATION | 9,310 | 8,557 | 8.1% | Legal suffix + abbreviation |

### 3. Specific Query Improvements

**AG-01 — ROOT_CAUSE_CATEGORY consolidation (biggest win):**
- Pre-ER: "Mechanical - Stored energy (dropped objects)" (265) and "Stored energy (dropped objects)" (102) were separate — misleading split
- Post-ER: Single "Stored energy (dropped objects)" with **367** consolidated occurrences
- Same pattern fixed for all 44 prefix-duplicate categories

**SH-03 — Body part ranking correction:**
- Pre-ER: "left hand" (17) was top body part in crane incidents because "left hand", "right hand", "hand" were separate entities
- Post-ER: "finger" (35) is top, "left hand" (31) second — schema fix enabled correct AFFECTED edge routing, laterality merge consolidated hand variants
- This is a more accurate picture of crane injury patterns

**AG-03 — Equipment deduplication:**
- Equipment types reduced 15,158 → 13,446 (-1,712)
- Forklift: 734 → 771 incidents (+37 from variant merging: "FLT", "fork lift", "forklifts")
- Getting closer to EDA ground truth rankings

**MH-07 — Location cleanup:**
- "zObsolete - Trinidad" → "Trinidad", "zObsolete - Batam" → "Batam"
- Scaffold near-misses: 115 → 121 (schema fix enabled more INVOLVED edges to route correctly)
- Cities: 36 → 33 (cleaner, no obsolete prefixes)

**GL-02 — Cross-region equipment visibility:**
- Equipment spanning 5+ regions: 123 → 144
- New entrants like "manlift" (7 regions) — previously fragmented across variant spellings

**MH-03 — Vessel broadening (query fix, not ER):**
- Pre-ER: `^vessel$` exact match → 1 node, 3 incidents, 0 with back injury
- Post-ER: `vessel` contains match → 42 nodes, 63 incidents, 1 with back injury
- Still far below EDA ground truth (780) — most "vessel" references are in LOCATION entities (offshore vessels), not EQUIPMENT

### 4. What Remains Blocked

| Issue | Queries Affected | Root Cause | Fix Path |
|-------|-----------------|-----------|----------|
| **No causal edges** | CJ-01, CJ-05 | L1 graph has no CAUSED_BY/CONTRIBUTED_TO relations | Layer 2 causal enrichment |
| **Extraction gap** | SH-02 | GLiNER missed "TMS" in incident #29857 | Improve extraction model or post-process |
| **Data sparsity** | AG-04, CJ-02, CJ-03 | 75% business_unit null; 4-way intersections too narrow | Source data quality improvement |
| **MH-08 too specific** | MH-08 | "hydraulic valve" = only 2 nodes, 3 incidents | Extraction granularity; broader valve taxonomy |
| **MH-03 still thin** | MH-03 | Only 1 vessel+back co-occurrence in EQUIPMENT | Most vessels are LOCATION entities; need cross-type query |

### 5. Schema Violation Fix

- **2,123 edges** had mismatched relation types after multi-type resolution
- Top transitions: REPORTED_BY → OCCURRED_AT (632), OCCURRED_AT → REPORTED_BY (369), OCCURRED_AT → INVOLVED (218)
- After fix: **0 remaining violations**
- **423 duplicate edges** removed after relation type correction
- This fix directly improved SH-03 (body part routing), MH-07 (scaffold routing), GL-02 (equipment routing), and CJ-06 (+1 result)

---

## ER Pipeline Summary

| Phase | Action | Impact |
|-------|--------|--------|
| 1.1 | RCC prefix normalization | 117 → 73 categories |
| 1.2 | Garbage entity removal | -336 entities, -750 edges |
| 1.3 | Multi-type resolution | 813 entities reclassified |
| 1.4 | Organization normalization | 8 TECHNIPFMC/FLEXI variants merged |
| 1.5 | Location cleanup | 30 zObsolete prefixes stripped |
| 2 | High-similarity merge (sim ≥ 0.90) | 3,936 entities merged, max cluster=45 |
| 3 | Schema violation fix | 2,123 edges corrected, 423 deduped |
| **Total** | | **-5,137 entities (-8.3%), 0 schema violations** |

**Quality:** 100% spot-check precision (50/50), Gate 2 PASS

---

*Generated by pipeline/er_execution/ — ER comparison pipeline*
