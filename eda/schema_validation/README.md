# Schema Validation Evidence

Empirical analysis of 23,311 records that justified every change from the v1 schema
to the v2 schema used in `kg_schema/`.

## Context

The v1 schema had 7 entity types and 6 relation types. Several were problematic:
USED_IN relations were rule artifacts, CAUSED_BY was unreliable at L1, and
INCIDENT_TYPE as an entity would create a mega-hub with degree 9,400. This analysis
provided the hard numbers to justify each change.

## v1 -> v2 Schema Changes (with evidence)

| Change | Evidence | Section in Report |
|--------|----------|-------------------|
| Remove `USED_IN` relation | 100% are EQUIPMENT->LOCATION co-occurrence artifacts, not narrative evidence | Analysis 1 |
| Remove `CAUSED_BY` from L1 | Cannot distinguish cause from correlation at extraction time | Analysis 2 |
| Demote `INCIDENT_TYPE` to property | "Accident" alone would have degree 9,400 (1,884x mean); 29.1% null | Analysis 3 |
| Demote `IMPACT_TYPE` to property | Same mega-hub problem; test set showed degree 592 for "INJURY" | Analysis 4 |
| Add `CATEGORIZED_AS` relation | Maps INCIDENT->ROOT_CAUSE_CATEGORY; 70.9% coverage | Analysis 5 |
| Add `REPORTED_BY` relation | Maps INCIDENT->ORGANIZATION (client); 82.3% coverage | Analysis 6 |
| Add `LOCATED_IN` relation | Country->Region->SubRegion hierarchy; 93.8% coverage | Analysis 7 |
| Add NaN/Unknown filtering | "NAN" as ROOT_CAUSE_CATEGORY bridged 1,887 incidents artificially | Analysis 8 |

## Files

| File | Purpose |
|------|---------|
| `schema_validation_analysis.py` | Reproducible analysis script (953 lines, 8 analyses) |
| `schema_validation_evidence.md` | 478-line evidence report with tables and statistics |

## How to Reproduce

```bash
# Requires input/incidents.csv and v1 GLiNER extraction output
cd /path/to/repo
python eda/schema_validation/schema_validation_analysis.py
```

The script reads from `input/incidents.csv` and the v1 extraction artifacts,
then generates the evidence report with all 8 analyses.
