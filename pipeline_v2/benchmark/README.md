# Benchmark System

## 1. Overview

This is a CSV-driven benchmark system for the v2 safety knowledge graph. Adding a
query means adding a row to `benchmark_queries.csv`. No Python changes are required
unless the query logic cannot be expressed via CSV (see Section 5).

**30 total queries:**
- 22 are fully CSV-driven (strategies: entity_filter, meta_filter,
  narrative_filter, intersect, crosstab, spot_check)
- 8 use custom Python functions registered in `custom_queries.py`

**Query types covered:** Single-hop, Aggregation, Multi-hop, Global, Conjunctive

**Run command (from `pipeline_v2/`):**

```bash
python -m benchmark.run_benchmark
```

Output is written to `pipeline_v2/benchmark/benchmark_results.md`.

---

## 2. CSV Column Reference

The CSV is parsed into `QuerySpec` dataclass instances by `query_engine.load_queries()`.
All columns are present in every row; unused columns are left empty.

### `query_id`
- Required
- Format: string, conventionally `TYPE-NN` (e.g., `SH-01`, `MH-03`, `CJ-06`)
- Used as the key in the results dict and in the report

### `name`
- Required
- Free-form string description of the query
- Example: `Forklift incidents in 2022`

### `query_type`
- Required
- Valid values: `Single-hop`, `Aggregation`, `Multi-hop`, `Global`, `Conjunctive`
- Used in the ablation prediction table to group queries

### `strategy`
- Required
- Controls the execution path in `query_engine.execute_query()`
- Valid values:

| Value | Behavior |
|-------|----------|
| `entity_filter` | Filter incidents by entity type/value/relation in graph |
| `meta_filter` | Filter incidents by metadata fields (year, severity, etc.) |
| `narrative_filter` | Filter incidents by keyword match in narrative text |
| `intersect` | Apply multiple filters and intersect the incident sets |
| `crosstab` | Cross-tabulate two metadata fields directly (no incident set) |
| `spot_check` | Verify a specific incident's extracted entities against ground truth |
| `custom` | Delegate to a named Python function in CUSTOM_REGISTRY |

Note: `intersect` is not a separate code path — all strategies that specify multiple
filters (entity_filters + meta_filters + narrative_keywords in combination) produce an
intersection automatically. The label `intersect` in the CSV is documentation only.

### `entity_filters`
- Optional
- Format: semicolon-separated triples of `TYPE:regex:RELATION`
  - `TYPE`: entity type (see Section 3)
  - `regex`: Python regex matched against entity `value` field (case-insensitive)
  - `RELATION`: relation type (see Section 3)
- Multiple triples are ANDed (incident must match all)
- The regex may contain `|` for OR within one filter
- Example: `EQUIPMENT:fork\s*lift|flt|forklift:INVOLVED`
- Example (two filters): `EQUIPMENT:crane:INVOLVED;BODY_PART:back:AFFECTED`

### `meta_filters`
- Optional
- Format: semicolon-separated expressions of `field op value`
  - Spaces around the operator are required
- Supported operators: `==`, `!=`, `>=`, `<=`, `>`, `<`, `contains`
- `contains` performs a case-insensitive regex match; pipe `|` acts as OR
- `year` is a virtual field derived from `reported_date`
- Other field names must match columns in `metadata_parsed.parquet`
- Example: `year == 2022`
- Example: `severity_bin >= 4`
- Example: `work_process contains offshore|marine`
- Example (two filters): `work_process contains maintenance;severity_bin >= 3`

### `narrative_keywords`
- Optional
- Format: comma-separated keywords, default AND logic
- Prefix `ANY:` to switch to OR logic
- Matching is case-insensitive substring search against the `narrative` column
- Example (AND): `maintenance,fail` — incident narrative must contain both words
- Example (OR): `ANY:corrosion,fire` — narrative contains corrosion or fire

### `require_connected`
- Optional
- Format: `ENTITY_TYPE:RELATION`
- Post-filter: keeps only incidents that have at least one edge of the given type
- Example: `INJURY_TYPE:RESULTED_IN` — drop incidents with no injury extraction

### `output_mode`
- Required for non-custom, non-spot-check strategies
- Valid values:

| Value | Description |
|-------|-------------|
| `count_incidents` | Return the count of matching incidents |
| `aggregate` | Count entity values across matching incidents |
| `count_by_year` | Break down matching incidents by year and month |
| `pairs` | Count co-occurring entity pairs across incidents |
| `crosstab` | Cross-tabulate two metadata fields (ignores incident filter) |

### `output_target`
- Optional; format varies by `output_mode`

| output_mode | Format | Example |
|-------------|--------|---------|
| `count_incidents` | Leave empty | |
| `aggregate` | `ENTITY_TYPE:RELATION` | `BODY_PART:AFFECTED` |
| `aggregate` (with granularity filter) | `ENTITY_TYPE[granularity]:RELATION` | `LOCATION[country]:OCCURRED_AT` |
| `pairs` | `TYPE1:REL1,TYPE2:REL2` | `EQUIPMENT:INVOLVED,INJURY_TYPE:RESULTED_IN` |
| `crosstab` | `field1:field2` | `year:incident_type` or `business_unit:incident_type` |
| `spot_check` | `INCIDENT::ID:ENTITY_TYPE:RELATION` | `INCIDENT::29857:EQUIPMENT:INVOLVED` |

The `granularity` filter in aggregate mode matches the `granularity` node attribute
(values seen in data: `country`, `region`, `city`).

### `output_top_n`
- Optional, default: `10`
- Integer; limits results in `aggregate`, `count_by_year`, `pairs`, `crosstab`

### `coverage_thresholds`
- Optional, default: `1:0`
- Format: `full_threshold:partial_threshold`
- Scoring: result count >= full_threshold → PASS; >= partial_threshold → PARTIAL; else FAIL
- Example: `50:1` means a count of 50+ is PASS, 1-49 is PARTIAL, 0 is FAIL
- Example: `99999:1` means effectively nothing passes fully (used to flag L2-required queries)

### `diagnosis_rule`
- Optional, default: `auto`
- Valid values:

| Value | Meaning |
|-------|---------|
| `auto` | CLEAN if count > 0, DATA_SPARSE if count == 0 |
| `CLEAN` | Force clean regardless of count |
| `DATA_SPARSE` | Metadata coverage too low for reliable results |
| `ER_NEEDED` | Pre-ER surface form fragmentation is expected to reduce accuracy |
| `L2_REQUIRED` | Query needs causal edges (CAUSED_BY / CONTRIBUTED_TO) not present at L1 |
| `EXTRACTION_GAP` | Spot-check found missing entities (auto-set by spot_check logic) |

### `custom_fn`
- Required when `strategy == custom`, otherwise leave empty
- Must match a key in `CUSTOM_REGISTRY` in `custom_queries.py`
- Example: `louvain_communities`

### `ground_truth`
- Used only by `strategy == spot_check`
- Format: pipe-separated expected entity values (case-insensitive comparison)
- Example: `pry bar|rov|tms|lanyard`

### `notes`
- Optional, free-form
- Not used programmatically; for human annotation only
- Example: `Pre-ER variants are separate`

---

## 3. Graph Structure Reference

### Node ID Format

All node IDs follow the pattern `TYPE::normalized_name`:

```
EQUIPMENT::FORKLIFT
LOCATION::ASIA PACIFIC
INJURY_TYPE::LACERATION
INCIDENT::29857
```

### Entity Types

| Type | Description |
|------|-------------|
| `EQUIPMENT` | Physical equipment or tool involved in an incident |
| `LOCATION` | Geographic location (city, country, region) |
| `BODY_PART` | Body part affected by an injury |
| `INJURY_TYPE` | Type of injury sustained |
| `ROOT_CAUSE_CATEGORY` | Categorized root cause of the incident |
| `ORGANIZATION` | Company or organization associated with an incident |
| `INCIDENT` | An individual safety incident record |

### Relation Types

| Relation | Source | Target |
|----------|--------|--------|
| `INVOLVED` | INCIDENT | EQUIPMENT |
| `OCCURRED_AT` | INCIDENT | LOCATION |
| `RESULTED_IN` | INCIDENT | INJURY_TYPE |
| `REPORTED_BY` | INCIDENT | ORGANIZATION |
| `CATEGORIZED_AS` | INCIDENT | ROOT_CAUSE_CATEGORY |
| `AFFECTED` | INCIDENT | BODY_PART |
| `LOCATED_IN` | LOCATION | LOCATION (region hierarchy) |

All edges are directed from INCIDENT outward, except `LOCATED_IN`.

### Data Files

Located in `pipeline_v2/outputs/`:

| File | Description |
|------|-------------|
| `entities.parquet` | Columns: entity_id, entity_type, value, granularity (optional) |
| `relations.parquet` | Columns: source, target, relation |
| `metadata_parsed.parquet` | One row per incident; columns include record_no, reported_date, severity_bin, incident_type, work_process, business_unit, impact_type, narrative |

---

## 4. Adding a New Query (Step-by-Step)

### Example A: Simple entity_filter query

Goal: Count incidents involving electrical cable in the Americas.

Add this row to `benchmark_queries.csv`:

```
SH-07,Electrical cable incidents in Americas,Single-hop,intersect,EQUIPMENT:electrical cable|cable:INVOLVED,,,INJURY_TYPE:RESULTED_IN,count_incidents,,10,5:1,ER_NEEDED,,,
```

Column breakdown:
- `strategy`: `intersect` (two filters combined)
- `entity_filters`: `EQUIPMENT:electrical cable|cable:INVOLVED`
- `require_connected`: `INJURY_TYPE:RESULTED_IN` (only incidents with injury data)
- `output_mode`: `count_incidents`
- `coverage_thresholds`: `5:1`
- `diagnosis_rule`: `ER_NEEDED` (variant names expected)

### Example B: Custom Python query

Goal: Find incidents where the same equipment appears in two different years at the
same location, suggesting a recurring hazard.

1. Add a function to `custom_queries.py`:

```python
def recurring_hazard(spec, G, entities_df, relations_df, metadata_df, *, results=None):
    # ... implementation ...
    return {
        "coverage": "...",    # one of the Unicode pass/partial/fail symbols
        "diagnosis": "CLEAN",
        "result_summary": "...",
        "detail": "...",
    }
```

2. Register it in `CUSTOM_REGISTRY` at the bottom of `custom_queries.py`:

```python
CUSTOM_REGISTRY = {
    ...
    "recurring_hazard": recurring_hazard,
}
```

3. Add a row to `benchmark_queries.csv`:

```
GL-05,Recurring equipment hazards by location/year,Global,custom,,,,,,,10,,CLEAN,recurring_hazard,,
```

- `strategy`: `custom`
- `custom_fn`: `recurring_hazard` (must match the registry key exactly)
- All filter columns (`entity_filters`, `meta_filters`, etc.) are ignored by the engine
  for custom strategies; pass them through to your function via `spec` if needed.

---

## 5. Custom Function Registry

### Function Signature

```python
def my_function(
    spec,          # QuerySpec — access spec.output_top_n, spec.notes, etc.
    G,             # networkx.DiGraph — the full knowledge graph
    entities_df,   # pd.DataFrame — entity nodes (entity_id, entity_type, value, ...)
    relations_df,  # pd.DataFrame — edges (source, target, relation)
    metadata_df,   # pd.DataFrame — incident metadata
    *,
    results=None   # dict of prior query results (keyed by query_id); may be None
) -> dict:
    ...
    return {
        "coverage": "...",       # "\u2705" PASS, "\u26a0\ufe0f" PARTIAL, "\u274c" FAIL
        "diagnosis": "...",      # CLEAN, ER_NEEDED, DATA_SPARSE, L2_REQUIRED, etc.
        "result_summary": "...", # one-line summary shown in the report table
        "detail": "...",         # multi-line detail shown in the per-query section
    }
```

The `results` parameter allows a custom function to reference the output of queries
that ran earlier in the sequence. Query execution order follows CSV row order.

### How to Register

Add the function to `CUSTOM_REGISTRY` in `custom_queries.py`:

```python
CUSTOM_REGISTRY = {
    "function_name": function_name,
    ...
}
```

The key must exactly match the `custom_fn` value in the CSV row.

### Existing Custom Functions

| Registry Key | Query ID | Description |
|---|---|---|
| `louvain_communities` | GL-01 | Runs Louvain community detection on the graph (excluding region nodes) and reports the top 10 communities by size with type composition |
| `equipment_across_regions` | GL-02 | Finds equipment types appearing in 5 or more distinct regions, indicating global recurring hazards |
| `hub_centrality` | GL-04 | Computes degree centrality and PageRank for all non-incident nodes; reports top 20 by each metric |
| `containment_injury_offshore` | MH-01 | Multi-hop: finds incidents with a containment root cause, occurring offshore, that also have an injury extraction |
| `top_injury_per_equipment` | MH-04 | For the top 5 equipment types by incident count, reports the top 5 injury types per equipment |
| `severity_comparison` | MH-06 | Compares severity distributions for truck incidents vs. crane incidents |
| `causal_chain_check` | CJ-01 | Detects that no L2 causal edges exist; falls back to an approximate narrative x RCC intersection for corrosion-to-fire chains |
| `dual_risk_detection` | CJ-04 | Finds equipment/location/year combinations where both accidents and near-misses were recorded |

---

## 6. Output

Running the benchmark produces `pipeline_v2/benchmark/benchmark_results.md` with
four sections:

1. **Summary Table** — one row per query with coverage symbol, result summary, and
   diagnosis label
2. **Per-Query Details** — full output block for each query including counts, top-N
   lists, or crosstab tables
3. **Ablation Prediction Table** — projects how many queries would pass after entity
   resolution (ER) and after Layer 2 causal enrichment, grouped by query type
4. **Key Findings** — grouped lists of passing queries, ER-needed queries, L2-blocked
   queries, and data sparsity issues
