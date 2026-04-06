# kg_schema

Single source of truth for the TechnipFMC Safety Knowledge Graph schema and evaluation assets.
All type definitions, relation constants, and golden set data live here and are imported by
downstream modules — nothing is duplicated across the pipeline.

---

## Purpose

Centralise every schema decision so that a change to an entity type, relation type, or
benchmark query propagates automatically to all consumers:

- `pipeline/extraction` — GLiNER labels and L1 type mappings
- `pipeline/enrichment` — L2 relation types and entity types
- `pipeline/assembly` — relation map and allowed relations
- `pipeline/evaluation` — gate/advisory relation classification, L2 relation names
- `pipeline/benchmark` — golden set CSV path
- `natural_language_query` — entity type and relation enums
- `event_similarity` — entity type validation for schema weights

---

## Structure

```
kg_schema/
├── __init__.py           # Re-exports everything for convenience
├── entity_types.py       # L1 entity types, GLiNER labels/map, incident properties, chunking
├── relation_types.py     # L1 relation map, hierarchy relation, allowed relations
├── l2_types.py           # L2 entity types, L2 relations, gate/advisory classification
├── golden_set.py         # CSV path + loader function
├── golden_set.csv        # 258 benchmark queries with full NL questions
└── README.md
```

---

## Schema Overview

### L1 — Extracted by GLiNER + metadata parsing

**Entity types (7)**

| Type | Source | Description |
|------|--------|-------------|
| `INCIDENT` | header | Hub node, one per record |
| `EQUIPMENT` | GLiNER | Physical equipment, tools, machinery, vehicles |
| `BODY_PART` | GLiNER | Anatomical body parts affected |
| `INJURY_TYPE` | GLiNER | Type of injury, harm, or impact |
| `LOCATION` | metadata | Geographic: site, city, country, region |
| `ORGANIZATION` | metadata | Client or organizational unit |
| `ROOT_CAUSE_CATEGORY` | metadata | CASE_CATEGORIZATION taxonomy (117 values) |

**Relation types (7)**

| Relation | Description |
|----------|-------------|
| `INVOLVED` | Incident -> Equipment |
| `AFFECTED` | Incident -> Body Part |
| `RESULTED_IN` | Incident -> Injury Type |
| `OCCURRED_AT` | Incident -> Location |
| `REPORTED_BY` | Incident -> Organization |
| `CATEGORIZED_AS` | Incident -> Root Cause Category |
| `LOCATED_IN` | Location -> Location (hierarchy) |

### L2 — Extracted by LLM enrichment (qwen3:30b-a3b)

**Entity types (9)**

`Action`, `Condition`, `Equipment`, `Event`, `Incident`, `Injury`, `Location`, `Material`, `Person`

**Relation types (4)**

| Relation | Direction | Description |
|----------|-----------|-------------|
| `CAUSAL` | source=cause -> target=effect | Causal link between events or conditions |
| `PRECEDED_BY` | event -> prior event | Temporal sequence without direct causation |
| `FAILED_CONTROL` | event/harm -> control that failed | A safeguard that did not prevent harm |
| `MITIGATED_BY` | event/harm -> control that worked | A safeguard that limited or prevented harm |

**Gate classification:** `CAUSAL` is gate-blocking; `FAILED_CONTROL`, `MITIGATED_BY`, `PRECEDED_BY` are advisory.

---

## Golden Set

### `golden_set.csv` — 258 benchmark queries

Each row contains the full natural language question in the `name` column, along with the
structured query spec (strategy, entity filters, meta filters, expected counts, etc.).

**Categories:** SH (58 single-hop), AG (26 aggregation), MH (44 multi-hop), GL (24 global),
CJ (31 conjunctive), SC (39 spot-check), IOGP (28 IOGP Life-Saving Rules).

**Strategies:** entity_filter, meta_filter, narrative_filter (with `~` bag-of-words support),
intersect, crosstab, spot_check, custom (37 functions including extraction gap analysis
and embedding similarity retrieval).

Used by:
- `pipeline/benchmark/run_benchmark.py` — automated benchmark execution
- `natural_language_query/run_golden_set.py` — NLQ translation testing
- `natural_language_query/eval_harness.py` — scoring criteria reference

---

## Usage

```python
from kg_schema import ENTITY_TYPES, L2_RELATIONS, ALLOWED_RELATIONS
from kg_schema import load_golden_set

# Iterate L1 entity types
for name, meta in ENTITY_TYPES.items():
    print(name, meta["source"])

# Load all 258 benchmark queries
queries = load_golden_set()   # returns list[dict]
```

Individual constants are also importable directly:

```python
from kg_schema.entity_types import GLINER_LABELS, GLINER_TYPE_MAP
from kg_schema.l2_types import GATE_RELATIONS, ADVISORY_RELATIONS
```

---

## Adding New Types

1. Add the type to the appropriate file (`entity_types.py`, `relation_types.py`, or `l2_types.py`).
2. Update `__init__.py` if the public API surface changes.
3. No other files need updating — all consumers import from this package.

For L1 entity types that require GLiNER extraction, also add an entry to `GLINER_LABELS`
and `GLINER_TYPE_MAP` in `entity_types.py`.
