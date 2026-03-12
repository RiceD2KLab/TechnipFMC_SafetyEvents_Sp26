"""FastAPI router for Knowledge Graph endpoints."""

import re
from fastapi import APIRouter, HTTPException, Query

from kg_loader import (
    load_kg_data,
    get_incident_display_map,
    find_entities_by_value,
    extract_subgraph,
    ENTITY_COLORS,
    ENTITY_TYPE_LABELS,
)
from graph_serializer import serialize_subgraph
from schemas import (
    SubgraphResponse,
    EntitySearchResponse,
    EntitySearchResult,
    IncidentListResponse,
    IncidentOption,
    EntityTypeListResponse,
    EntityTypeInfo,
)

router = APIRouter(prefix="/kg", tags=["knowledge-graph"])


@router.get("/incidents", response_model=IncidentListResponse)
def list_incidents():
    """Return all INCIDENT entities for the browse-incidents dropdown."""
    _, entities_df, _ = load_kg_data()
    display_map = get_incident_display_map(entities_df)
    incidents = [
        IncidentOption(label=label, entity_id=eid)
        for label, eid in display_map.items()
    ]
    return IncidentListResponse(incidents=incidents)


@router.get("/search", response_model=EntitySearchResponse)
def search_entities(
    entity_type: str | None = Query(None, description="Entity type filter (e.g. EQUIPMENT). Omit for all."),
    value_pattern: str = Query("", description="Regex pattern to match entity values."),
    max_results: int = Query(50, ge=1, le=200, description="Max results to return."),
):
    """Search entities by type and regex value pattern."""
    # Validate regex
    if value_pattern:
        try:
            re.compile(value_pattern)
        except re.error as e:
            raise HTTPException(status_code=400, detail=f"Invalid regex pattern: {e}")

    _, entities_df, _ = load_kg_data()
    raw = find_entities_by_value(
        entities_df,
        entity_type=entity_type,
        value_pattern=value_pattern,
        max_results=max_results,
    )
    results = [
        EntitySearchResult(entity_id=r[0], entity_type=r[1], value=r[2])
        for r in raw
    ]
    return EntitySearchResponse(results=results, total_count=len(results))


@router.get("/subgraph", response_model=SubgraphResponse)
def get_subgraph(
    node_id: str = Query(..., description="Entity ID to center on."),
    hops: int = Query(1, ge=1, le=2, description="Hop depth (1 or 2)."),
    entity_type_filter: list[str] | None = Query(None, description="Entity types to include. Omit for all."),
):
    """Extract and return a subgraph centered on a given node."""
    G, _, _ = load_kg_data()

    if node_id not in G:
        raise HTTPException(status_code=404, detail=f"Node '{node_id}' not found in graph.")

    et_filter = set(entity_type_filter) if entity_type_filter else None
    subgraph, was_truncated = extract_subgraph(
        G, node_id, hops=hops, entity_type_filter=et_filter,
    )

    response = serialize_subgraph(subgraph, node_id)
    response.truncated = was_truncated
    return response


@router.get("/entity-types", response_model=EntityTypeListResponse)
def list_entity_types():
    """Return the list of entity types with display labels and colors."""
    entity_types = [
        EntityTypeInfo(name=name, label=ENTITY_TYPE_LABELS[name], color=color)
        for name, color in ENTITY_COLORS.items()
    ]
    return EntityTypeListResponse(entity_types=entity_types)
