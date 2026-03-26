# ER Prep Summary

Generated: 2026-02-19

Input: 61,545 entities, 202,141 edges

---

## 1. Garbage Entity Filter

**336 entities flagged** → 750 edges affected

| Category | Count | Edges |
|----------|------:|------:|
| short_non_abbreviation (≤2 chars, not known abbr) | 279 | 898→663* |
| numeric_only | 31 | 52 |
| stop_word | 16 | 52→22* |
| single_char | 10 | 13 |

*Edge counts adjusted after adding BP and DP to known abbreviations list.

Known abbreviations preserved: HP, IP, UK, US, UV, AC, DC, CO, H2, O2, ER, BP, DP

Output: `garbage_entities.csv`

---

## 2. Multi-Type Resolution

**1,215 values** appear under 2+ entity types.

| Confidence | Count | Description |
|------------|------:|-------------|
| High (>80% majority) | 235 | Safe to auto-reclassify |
| Moderate (50-80%) | 536 | Reclassify with review flag |
| Ambiguous (<50%) | 444 | Needs manual review |

Outputs:
- `multitype_resolution.csv` — all 1,215 values with canonical type assignment
- `manual_review_needed.csv` — 444 ambiguous values needing human decision

---

## 3. Merge Candidates

**10,140 merge candidate pairs** found across all entity types.

| Entity Type | Candidates |
|-------------|----------:|
| EQUIPMENT | 2,946 |
| LOCATION | 3,914 |
| BODY_PART | 1,103 |
| INJURY_TYPE | 1,121 |
| ORGANIZATION | 979 |
| ROOT_CAUSE_CATEGORY | 77 |

### Top 10 Highest-Impact Merges

| Type | Entity A (degree) | Entity B (degree) | Score | Rule |
|------|-------------------|--------------------|------:|------|
| ORGANIZATION | TECHNIPFMC PLC (2,518) | TECHNIPFMC (1,821) | 1.000 | legal_suffix_strip |
| ORGANIZATION | TECHNIPFMC PLC (2,518) | TFMC (336) | 1.000 | exact_normalized |
| ORGANIZATION | TECHNIPFMC PLC (2,518) | TECHNIP FMC (145) | 0.952 | near_exact |
| ROOT_CAUSE_CATEGORY | Uncontrolled moving objects... (345) | Mechanical - Uncontrolled moving objects... (1,126) | 0.933 | substring_match |
| ROOT_CAUSE_CATEGORY | Hazard Identification & Risk Assessment (333) | Basic Organizational - Hazard ID & RA (973) | 0.772 | substring_match |
| ROOT_CAUSE_CATEGORY | Equipment condition (359) | Mechanical - Equipment condition (896) | 0.745 | substring_match |
| ROOT_CAUSE_CATEGORY | Falls, slips and trips... (190) | Work environment - Falls, slips... (991) | 0.893 | substring_match |
| ROOT_CAUSE_CATEGORY | Stored energy (dropped objects) (300) | Mechanical - Stored energy (dropped objects) (860) | 0.827 | substring_match |
| ORGANIZATION | FLEXI FRANCE (1,004) | FLEXI FRANCE SAS (11) | 0.857 | jaro_winkler |
| ROOT_CAUSE_CATEGORY | Hazardous liquids... (294) | Substances - Hazardous liquids... (743) | 0.911 | substring_match |

Outputs:
- `merge_candidates.csv` — all 10,140 pairs
- `merge_priorities.csv` — top 50 by combined degree

---

## 4. Splink Configurations

Ready for 5 entity types in `splink_config/`:

| Config | Blocking | Key Features |
|--------|----------|-------------|
| `equipment_config.py` | first_3_chars, token_set | Plural stripping, token-order invariance |
| `bodypart_config.py` | base_form, first_3_chars | Laterality stripping with conflict filter (left hand ≠ right hand) |
| `injury_config.py` | base_form, first_3_chars | Severity qualifier stripping, "injury" suffix removal |
| `organization_config.py` | first_5_chars, token_set | Legal suffix stripping, abbreviation expansion (TFMC→TECHNIPFMC) |
| `location_config.py` | granularity+first_3_chars | Same-granularity-only comparison, zObsolete prefix stripping |

All configs use Splink 4.x API (`SettingsCreator`, `DuckDBAPI`).
Auto-merge threshold: match_weight ≥ 6.0. Review threshold: 3.0–6.0.

---

## Execution Sequence (when ready)

1. Apply garbage filter (delete 336 entities + 750 edges)
2. Apply multi-type resolution (reclassify minority-type entities)
3. Run Splink per entity type (merge candidates above threshold)
4. Rebuild graph with merged entities
5. Recompute topology metrics
6. Rerun benchmark queries
