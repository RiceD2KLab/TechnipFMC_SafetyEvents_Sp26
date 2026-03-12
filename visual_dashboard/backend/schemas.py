"""Pydantic models for KG API request/response schemas."""

from pydantic import BaseModel
from typing import Any


class GraphNode(BaseModel):
    id: str
    entity_type: str
    value: str
    x: float
    y: float
    is_center: bool
    properties: dict[str, Any]


class GraphEdge(BaseModel):
    source: str
    target: str
    relation: str
    confidence: float | None = None
    source_type: str | None = None


class SubgraphStats(BaseModel):
    node_count: int
    edge_count: int
    entity_type_counts: dict[str, int]
    relation_type_counts: dict[str, int]


class SubgraphResponse(BaseModel):
    nodes: list[GraphNode]
    edges: list[GraphEdge]
    stats: SubgraphStats
    truncated: bool
    center_node_id: str


class EntitySearchResult(BaseModel):
    entity_id: str
    entity_type: str
    value: str


class EntitySearchResponse(BaseModel):
    results: list[EntitySearchResult]
    total_count: int


class IncidentOption(BaseModel):
    label: str
    entity_id: str


class IncidentListResponse(BaseModel):
    incidents: list[IncidentOption]


class EntityTypeInfo(BaseModel):
    name: str
    label: str
    color: str


class EntityTypeListResponse(BaseModel):
    entity_types: list[EntityTypeInfo]


class HealthResponse(BaseModel):
    status: str
    graph_loaded: bool
    node_count: int
    edge_count: int
