# Benchmark System

## 1. Overview

This is a CSV-driven benchmark system for the v2 safety knowledge graph. Adding a
query means adding a row to `kg_schema/golden_set.csv`. No Python changes are required
unless the query logic cannot be expressed via CSV (see Section 5).

**258 total queries across 7 categories:**
- 213 are fully CSV-driven (strategies: entity_filter, meta_filter,
  narrative_filter, intersect, crosstab, spot_check)
- 37 use custom Python functions registered in `query_engine/custom_queries.py`
- 58+ metadata-verifiable queries have `expected_count` for ground truth validation
- 39 spot-check queries verify per-record extraction quality across equipment,
  body parts, injury types, locations, and organizations
- 8 extraction-gap queries compare narrative mentions vs entity extraction
- 8 embedding-similarity queries test semantic retrieval via text/KG embeddings

**Query types covered:** Single-hop, Aggregation, Multi-hop, Global, Conjunctive

**Run command (from `pipeline/`):**

```bash
python -m benchmark.run_benchmark
```

Output is written to `pipeline/benchmark/benchmark_results.md`.

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
| `traverse` | Walk the graph along a path pattern and collect endpoints (see below) |
| `custom` | Delegate to a named Python function in CUSTOM_REGISTRY |

Note: `intersect` is not a separate code path — all strategies that specify multiple
filters (entity_filters + meta_filters + narrative_keywords in combination) produce an
intersection automatically. The label `intersect` in the CSV is documentation only.

#### `traverse` strategy

Walks the graph following a typed path pattern specified in `output_target`:

```
START_TYPE:pattern>RELATION>NODE_TYPE>RELATION>...>COLLECT_TYPE
```

Each `>` is a hop.  Odd positions are relation types, even positions are entity
types to filter on.  The walk follows edges in both directions (forward successors
and reverse predecessors), so `INJURY_TYPE:fracture>RESULTED_IN>INCIDENT` works
even though RESULTED_IN edges point from INCIDENT to INJURY_TYPE.

**L1 examples (through incident hub):**
- `EQUIPMENT:crane>INVOLVED>INCIDENT>RESULTED_IN>INJURY_TYPE`
- `BODY_PART:hand>AFFECTED>INCIDENT>CATEGORIZED_AS>ROOT_CAUSE_CATEGORY`

**L2 examples (causal chain traversal):**
- `EQUIPMENT:.*>CAUSAL>EVENT>CAUSAL>INJURY` — equipment → event → injury chains
- `CONDITION:corros>CAUSAL>EVENT` — what events does corrosion cause?

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
- Matching is case-insensitive against the `narrative` column
- **Exact mode (default):** substring match — `scaffold fall` matches only that exact phrase
- **Bag-of-words mode (`~` prefix):** all words must appear anywhere in the narrative —
  `~scaffold fall` matches "fell from scaffold", "scaffold fell", "fall from the scaffold"
- Example (AND): `maintenance,fail` — narrative must contain both words
- Example (OR): `ANY:corrosion,fire` — narrative contains corrosion or fire
- Example (BOW): `ANY:~scaffold fall,~scaffold fell` — narrative contains scaffold+fall or scaffold+fell in any order

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
| `CLEAN` | Query works correctly; results reflect true graph state |
| `DATA_SPARSE` | Dataset genuinely has no matching data (not an extraction failure) |
| `ER_NEEDED` | Pre-ER surface form fragmentation is expected to reduce accuracy |
| `L2_REQUIRED` | Query needs L2 causal edges (CAUSAL, FAILED_CONTROL, etc.) |
| `EXTRACTION_GAP` | Narrative contains the information but GLiNER failed to extract it |
| `KNOWN_SPARSE` | Conjunction is too specific for the dataset size; 0 results is correct |

### `custom_fn`
- Required when `strategy == custom`, otherwise leave empty
- Must match a key in `CUSTOM_REGISTRY` in `query_engine/custom_queries.py`
- Example: `louvain_communities`

### `ground_truth`
- Used only by `strategy == spot_check`
- Format: pipe-separated expected entity values (case-insensitive comparison)
- Example: `pry bar|rov|tms|lanyard`

### `notes`
- Optional, free-form
- Not used programmatically; for human annotation only
- Example: `Pre-ER variants are separate`

### `expected_count`
- Optional
- Integer ground truth count computed from `metadata_parsed.parquet` or manual verification
- Used by the validation scoring engine to compare graph results against known answers
- Scoring logic:
  - Within 10% of expected: `VALIDATED`
  - Within 25% of expected: `CLOSE` (acceptable for GLiNER-dependent queries)
  - Over 25% divergence: `DRIFT` (indicates extraction or pipeline issue)
  - No expected_count: `—` (not validated)
- For metadata-verifiable queries (filters on year, severity, work_process), the expected
  count is deterministic. For GLiNER-dependent queries, some drift is expected since the
  NER model may extract more or fewer entities than a simple text grep.

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

Located in `pipeline/outputs/`:

| File | Description |
|------|-------------|
| `entities.parquet` | Columns: entity_id, entity_type, value, granularity (optional) |
| `relations.parquet` | Columns: source, target, relation |
| `metadata_parsed.parquet` | One row per incident; columns include record_no, reported_date, severity_bin, incident_type, work_process, business_unit, impact_type, narrative |

---

## 4. Adding a New Query (Step-by-Step)

### Example A: Simple entity_filter query

Goal: Count incidents involving electrical cable in the Americas.

Add this row to `kg_schema/golden_set.csv`:

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

1. Add a function to `query_engine/custom_queries.py`:

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

3. Add a row to `kg_schema/golden_set.csv`:

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

Add the function to `CUSTOM_REGISTRY` in `query_engine/custom_queries.py`:

```python
CUSTOM_REGISTRY = {
    "function_name": function_name,
    ...
}
```

The key must exactly match the `custom_fn` value in the CSV row.

### Existing Custom Functions (37 total)

**Graph structure & analysis:**
| Registry Key | Query ID | Description |
|---|---|---|
| `louvain_communities` | GL-01 | Louvain community detection; top 10 by size with type composition |
| `equipment_across_regions` | GL-02 | Equipment types appearing in 5+ regions (global recurring hazards) |
| `hub_centrality` | GL-04 | Degree centrality + PageRank for non-incident nodes |
| `equipment_bodypart_cooccurrence` | GL-05 | Most common (equipment, body_part) pairs across all incidents |
| `client_safety_comparison` | GL-06 | Severity/type profiles for top 5 clients |
| `seasonal_patterns` | GL-07 | Monthly incident frequency patterns |
| `rcc_by_region` | GL-08 | Top root causes by geographic region |

**Multi-hop & conjunctive:**
| Registry Key | Query ID | Description |
|---|---|---|
| `containment_injury_offshore` | MH-01 | Containment RCC + offshore + injury → equipment list |
| `top_injury_per_equipment` | MH-04 | Top 5 injuries for each of top 5 equipment types |
| `severity_comparison` | MH-06 | Severity distribution: truck vs crane |
| `dual_risk_detection` | CJ-04 | Equipment/location/year with both accidents AND near-misses |

**L2 causal analysis:**
| Registry Key | Query ID | Description |
|---|---|---|
| `causal_chain_check` | CJ-01 | L2 causal edges for fire/explosion; corrosion intersection |
| `procedural_dropped_injury` | CJ-05 | Procedural violation → dropped object → injury chain |
| `corrosion_effects` | CJ-07 | Corrosion-source CAUSAL edges categorized by effect type |
| `loto_failures_l2` | IOGP-05 | FAILED_CONTROL edges in LOTO/electrical incidents |
| `mitigated_by_analysis` | CJ-21 | MITIGATED_BY edges: what controls worked |
| `failed_control_overview` | CJ-22 | FAILED_CONTROL edges: what barriers failed |
| `preceded_by_analysis` | CJ-23 | PRECEDED_BY edges: common temporal sequences |
| `causal_factors_dropped` | CJ-24 | Causal factors for dropped-object incidents |
| `causal_factors_vehicle` | CJ-25 | Causal factors for vehicle incidents |
| `causal_factors_fracture` | CJ-26 | Causal factors leading to fracture injuries |

**Extraction gap analysis:**
| Registry Key | Query ID | Description |
|---|---|---|
| `extraction_gap_burn` | GL-09 | Narrative mentions "burn" but no INJURY_TYPE extracted |
| `extraction_gap_fracture` | GL-10 | Narrative mentions "fracture" but no INJURY_TYPE extracted |
| `extraction_gap_crane` | GL-11 | Narrative mentions "crane" but no EQUIPMENT extracted |
| `extraction_gap_forklift` | GL-12 | Narrative mentions "forklift" but no EQUIPMENT extracted |
| `extraction_gap_severity_injury` | GL-13 | Severity >= 4 but no INJURY_TYPE edge |
| `extraction_gap_injury_bodypart` | GL-14 | Impact = Injury but no BODY_PART edge |
| `extraction_gap_short_narrative` | GL-15 | Narrative < 100 chars with no entity extraction |
| `extraction_gap_foreign_language` | GL-16 | Non-English narratives with reduced extraction rates |

**Embedding similarity:**
| Registry Key | Query ID | Description |
|---|---|---|
| `similarity_seed_incident` | GL-17 | Top-10 similar to #29857 via text embeddings |
| `similarity_seed_incident_2` | GL-18 | Top-10 similar to #569346 via text embeddings |
| `similarity_hit_rate_forklift` | GL-19 | Equipment hit rate for forklift seed retrieval |
| `similarity_hit_rate_crane` | GL-20 | Equipment hit rate for crane seed retrieval |
| `similarity_method_agreement` | GL-21 | Text vs Node2Vec top-10 overlap analysis |
| `similarity_text_query` | GL-22 | Free-text semantic search: scaffold/guardrail query |
| `similarity_text_query_2` | GL-23 | Free-text semantic search: crane/sling query |
| `similarity_severity_equipment` | GL-24 | Equipment patterns in high-severity neighborhoods |

---

## 6. Spot-Check Queries

Spot-check queries (SC-01 through SC-35) verify extraction quality on individual
incident records where the ground truth was determined by reading the narrative.

Five entity types are tested:
- **Equipment** (SC-01 to SC-11, SC-14, SC-17–SC-21, SC-29, SC-31, SC-33–SC-34): verify `EQUIPMENT:INVOLVED`
- **Body parts** (SC-04b, SC-06b, SC-07b, SC-09b, SC-12, SC-15, SC-19, SC-32): verify `BODY_PART:AFFECTED`
- **Injury types** (SC-13, SC-16, SC-22–SC-25, SC-30, SC-35): verify `INJURY_TYPE:RESULTED_IN`
- **Locations** (SC-26, SC-27): verify `LOCATION:OCCURRED_AT`
- **Organizations** (SC-28): verify `ORGANIZATION:REPORTED_BY`

The `ground_truth` column contains pipe-separated expected values; the engine compares
graph extractions against them and flags missing or extra entities. Diagnosis is
`EXTRACTION_GAP` when narrative contains the entity text but GLiNER failed to extract it.

---

## 7. Regression Snapshots

Each benchmark run saves a `benchmark_snapshot.json` alongside the report. On the next
run, the report includes a **Regression Diff** section comparing the current results
against the previous snapshot.

The diff reports:
- Coverage changes (e.g., pass → fail)
- Diagnosis changes
- Validation changes
- New or removed queries

This enables detecting regressions after pipeline changes (schema updates, GLiNER model
changes, data refreshes) without manual comparison.

---

## 8. Output

Running the benchmark produces `pipeline/benchmark/benchmark_results.md` with
up to five sections:

1. **Summary Table** — one row per query with coverage symbol, result summary,
   diagnosis label, and validation status
2. **Per-Query Details** — full output block for each query including counts, top-N
   lists, or crosstab tables
3. **Ablation Prediction Table** — projects how many queries would pass after entity
   resolution (ER) and after Layer 2 causal enrichment, grouped by query type
4. **Key Findings** — grouped lists of passing queries, ER-needed queries, L2-blocked
   queries, and data sparsity issues
5. **Regression Diff** — (if a previous snapshot exists) changes since the last run
