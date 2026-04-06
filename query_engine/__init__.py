"""Reusable query engine for the TechnipFMC Safety Knowledge Graph.

Provides QuerySpec, query loading, execution, and graph helper functions.
Every consumer (benchmark runner, NL translator, dashboard, API) imports
from here.

Usage:
    from query_engine import load_data, load_queries, execute_query, CUSTOM_REGISTRY

    G, entities_df, relations_df, metadata_df = load_data()
    specs = load_queries("kg_schema/golden_set.csv")
    result = execute_query(specs[0], G, entities_df, relations_df, metadata_df,
                           custom_registry=CUSTOM_REGISTRY)
"""
from __future__ import annotations

from query_engine.engine import (
    QuerySpec,
    execute_query,
    load_queries,
    run_all_queries,
)
from query_engine.helpers import (
    find_entities_by_value,
    get_entities_for_incident,
    get_incident_property,
    get_incidents_for_entity,
    get_neighbors,
    incidents_for_entity_filter,
    incidents_for_meta_filter,
    incidents_matching_narrative,
    load_data,
    parse_year,
    parse_yearmonth,
    safe_get_node_value,
)
from query_engine.custom_queries import CUSTOM_REGISTRY

__all__ = [
    "QuerySpec", "load_queries", "execute_query", "run_all_queries",
    "load_data", "CUSTOM_REGISTRY",
    "find_entities_by_value", "get_entities_for_incident",
    "get_incident_property", "get_incidents_for_entity", "get_neighbors",
    "incidents_for_entity_filter", "incidents_for_meta_filter",
    "incidents_matching_narrative",
    "parse_year", "parse_yearmonth", "safe_get_node_value",
]
