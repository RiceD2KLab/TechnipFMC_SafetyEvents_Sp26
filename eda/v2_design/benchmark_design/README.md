# Benchmark Query Design

Data profiling of the full 23,311-record dataset to ground the design of the 30
benchmark queries in `pipeline_v2/benchmark/benchmark_queries.csv`.

## Context

Before writing benchmark queries, we needed to understand the actual data distribution:
which equipment appears most often, what body parts are injured, what causal action
verbs dominate narratives, and how incident categories are distributed. Without this
profiling, queries would be guesses — some would match thousands of records, others zero.

## Key Data Profiles

### Equipment (top 10 by entity frequency)
Vessel (11.2%), Equipment (10.0%), Crane (9.9%), Pipe (9.2%), Truck (7.4%),
Lifting (7.1%), Lift (7.0%), Forklift (5.7%), Vehicle (5.5%), Valve (5.3%)

### Injuries / Body Parts (top 6)
Back (15.7%), Injury (10.8%), Hand (9.9%), Cut (6.4%), Pain (5.5%), Finger (5.4%)

### Causal Action Verbs (top 7)
Fell (13.1%), Hit (9.5%), Injured (7.4%), Damaged (7.1%), Cut (6.4%),
Slipped (5.5%), Dropped (5.5%)

### Case Categorization (117 unique values, top 5)
Mechanical/Uncontrolled Objects (6.2%), Equipment Condition (5.2%),
Hazard Assessment (5.1%), Stored Energy/Dropped Objects (5.0%), Falls/Slips (4.4%)

## How This Informed the Benchmarks

- **Single-hop queries** (SH-*): Targeted high-frequency entities (forklift, crane)
  that should reliably return results
- **Aggregation queries** (AG-*): Used top root cause categories and equipment types
  for meaningful aggregations
- **Conjunctive queries** (CJ-*): Combined equipment + body part + severity to test
  intersection filtering — profiles showed which combos actually exist in the data
- **Coverage thresholds**: Set based on observed frequencies (e.g., forklift incidents
  in 2022 expected >=50 based on 5.7% equipment frequency)

## Files

| File | Purpose |
|------|---------|
| `query_design_exploration.py` | 947-line data profiling script (16 analyses) |
| `query_design_exploration.md` | Full profiling report with tables and distributions |

## How to Reproduce

```bash
cd /path/to/repo
python eda/v2_design/benchmark_design/query_design_exploration.py
```

Reads from `graphRAG/input/dev_sample.csv` and the v2 pipeline graph outputs.
