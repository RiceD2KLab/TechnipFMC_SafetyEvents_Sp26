# Graph Topology Analysis

Exploratory analysis of the raw GraphRAG Mistral 7B output to understand graph health
and establish the schema enforcement strategy for the v2 pipeline.

## Context

The Fall 2025 capstone produced a knowledge graph via Mistral 7B extraction. Before
designing the v2 pipeline, we needed to understand what the raw graph looked like:
how noisy were the relations, how many entity types leaked through, and what happened
to connectivity when we enforced a strict schema.

## Analysis Flow

```
Raw Mistral output (83K nodes, 156K edges, 3,380 relation types)
    │
    ├─ graph_diagnostics.py ──► Baseline health metrics
    │
    ├─ clean_graph_topology.py ──► Canonical relation mapping + entity dedup
    │                               Output: graphRAG/output_cleaned/
    │
    ├─ schema_filter.py ──► Strict 7-type entity filter
    │                        Output: graphRAG/output_schema_only/
    │
    ├─ guardrail_graph.py ──► Schema enforcement + normalization
    │                          Output: graphRAG/output_guardrailed/
    │
    └─ litmus_test.py ──► Quick go/no-go feasibility check
```

## Key Findings

1. **Relation chaos:** 3,380 unique relation types in the raw Mistral output compressed
   to 13 canonical types after mapping. This confirmed that deterministic relation
   assignment (v2's `RELATION_MAP`) would eliminate the noise entirely.

2. **Schema leakage:** 14,926 entities (18%) had types outside the 7-type schema.
   After filtering, the graph dropped from 83K to 65K nodes but schema violations
   went to zero.

3. **Hub-dominated topology:** The top 1% of nodes by degree (>=24) held the graph
   together. Removing them fragmented the graph into 7,028 components. This informed
   the v2 decision to keep INCIDENT as a mandatory star-center node.

4. **Degree baseline:** Raw avg degree 1.87, post-guardrail 1.62. Both below the
   Gate 1 threshold of 2.0, confirming that metadata-derived edges (OCCURRED_AT,
   REPORTED_BY, CATEGORIZED_AS) were necessary to reach adequate connectivity.

5. **Litmus verdict:** Graph connectivity = sparse (avg degree < 2.0), relation
   cleanliness = messy (>50 unique types). Both flags pointed to "schema enforcement
   + metadata enrichment" as the priority path.

## Decision Impact

These findings directly informed three v2 pipeline design choices:
- **Deterministic relations** via `RELATION_MAP` (no free-text relation extraction)
- **Mandatory metadata edges** (OCCURRED_AT, REPORTED_BY, CATEGORIZED_AS, LOCATED_IN)
- **Gate 1 thresholds** (GC >= 0.85, mean degree >= 2.0, schema violations = 0)

## Files

| File | Purpose |
|------|---------|
| `graph_diagnostics.py` | Comprehensive graph health metrics |
| `graph_diagnostics.json` | Raw output metrics |
| `graph_diagnostics_guardrailed.json` | Post-guardrail metrics |
| `graph_diagnostics_schema_only.json` | Post-schema-filter metrics |
| `clean_graph_topology.py` | Relation canonicalization + entity dedup |
| `guardrail_graph.py` | Full schema enforcement pipeline |
| `schema_filter.py` | Strict entity type filter with drift detection |
| `litmus_test.py` | Quick feasibility go/no-go check |
