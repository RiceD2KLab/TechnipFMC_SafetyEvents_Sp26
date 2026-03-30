# Query Engine

Reusable query engine for the TechnipFMC Safety Knowledge Graph. This is the
shared module that the benchmark runner, NLQ translator, dashboard, and any
future consumer imports from.

## Quick Start

```python
from query_engine import load_data, load_queries, execute_query, CUSTOM_REGISTRY

# Load the graph
G, entities_df, relations_df, metadata_df = load_data()

# Load and run all 258 benchmark queries
specs = load_queries("kg_schema/golden_set.csv")
for spec in specs:
    result = execute_query(spec, G, entities_df, relations_df, metadata_df,
                           custom_registry=CUSTOM_REGISTRY)
    print(f"{spec.query_id} {result['coverage']} {result['result_summary']}")
```

## Run a single query

```python
from query_engine import load_data, QuerySpec, execute_query

G, ent, rel, meta = load_data()

# Build a QuerySpec directly
spec = QuerySpec(
    query_id="test-01",
    name="Crane incidents in 2022",
    query_type="Single-hop",
    strategy="intersect",
    entity_filters=[("EQUIPMENT", "crane", "INVOLVED")],
    meta_filters=[("year", "==", "2022")],
    narrative_keywords=[],
    match_any_keyword=False,
    require_connected=None,
    output_mode="count_incidents",
    output_target="",
    output_top_n=10,
    coverage_thresholds=(1, 0),
    diagnosis_rule="auto",
    custom_fn="",
    ground_truth=set(),
    notes="",
    expected_count=None,
)

result = execute_query(spec, G, ent, rel, meta)
print(result["result_summary"])  # "155 incidents"
```

## Graph helpers

All graph traversal utilities are importable directly:

```python
from query_engine import (
    find_entities_by_value,       # regex search over entity values
    get_entities_for_incident,    # get neighbors of an incident node
    get_incidents_for_entity,     # reverse: entity -> incidents
    incidents_for_entity_filter,  # combined find + get_incidents
    incidents_for_meta_filter,    # filter by metadata fields
    incidents_matching_narrative,  # keyword search in narrative text
    safe_get_node_value,          # safely read node 'value' attribute
)
```

### Narrative keyword matching

Keywords support two modes:

- **Exact** (default): `"confined space"` matches only that exact substring
- **Bag-of-words** (`~` prefix): `"~scaffold fall"` matches any narrative
  containing both "scaffold" and "fall" in any order — so "fell from scaffold",
  "scaffold fell", "fall from the scaffold" all match

## Strategies

The query engine supports 8 execution strategies:

| Strategy | What it does |
|----------|-------------|
| `entity_filter` | Filter incidents by entity type + regex + relation |
| `meta_filter` | Filter by metadata fields (year, severity, work_process, etc.) |
| `narrative_filter` | Keyword search in incident narratives |
| `intersect` | Combine entity + meta + narrative filters (AND logic) |
| `crosstab` | Cross-tabulate two metadata fields |
| `spot_check` | Verify extraction for a specific incident against ground truth |
| `traverse` | Walk the graph along a typed path pattern |
| `custom` | Delegate to a registered Python function |

### Traverse strategy

Real graph traversal — not set intersection. Specify a path in `output_target`:

```
START_TYPE:pattern>RELATION>NODE_TYPE>RELATION>...>COLLECT_TYPE
```

Examples:
```python
# L1: What injuries are connected to cranes?
"EQUIPMENT:crane>INVOLVED>INCIDENT>RESULTED_IN>INJURY_TYPE"

# L1: What equipment is connected to fractures? (reverse direction works)
"INJURY_TYPE:fracture>RESULTED_IN>INCIDENT>INVOLVED>EQUIPMENT"

# L2: What do corrosion conditions cause?
"CONDITION:corros>CAUSAL>EVENT"

# L2: 3-hop causal chain
"EQUIPMENT:.*>CAUSAL>EVENT>CAUSAL>INJURY"
```

## Custom functions

37 registered functions covering graph analysis, L2 causal chains, extraction
gap detection, and embedding similarity. See `custom_queries.py` for the full
registry. Each function receives `(spec, G, entities_df, relations_df,
metadata_df)` and returns a result dict.

## Loading data from a custom directory

```python
from query_engine import load_data

# Default: pipeline/outputs/
G, ent, rel, meta = load_data()

# Custom path (e.g., merged_v4)
G, ent, rel, meta = load_data(data_dir="pipeline/outputs/merged_v4")
```

## Files

```
query_engine/
├── __init__.py          # Public API — import everything from here
├── engine.py            # QuerySpec dataclass, load_queries, execute_query
├── helpers.py           # Graph helpers: load_data, traversal utilities
├── custom_queries.py    # 37 custom functions + CUSTOM_REGISTRY
└── README.md
```
