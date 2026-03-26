"""Canonical schema definitions for the TechnipFMC Safety Knowledge Graph.

Single source of truth for all entity types, relation types, and evaluation
asset paths.  Every component imports from here.
"""
from __future__ import annotations

from kg_schema.entity_types import (
    ENTITY_TYPES, L1_ENTITY_TYPE_NAMES,
    GLINER_LABELS, GLINER_TYPE_MAP,
    INCIDENT_PROPERTIES,
    CHUNK_MAX_TOKENS, CHUNK_OVERLAP,
)
from kg_schema.relation_types import (
    RELATION_MAP, HIERARCHY_RELATION, ALLOWED_RELATIONS,
)
from kg_schema.l2_types import (
    L2_ENTITY_TYPES, L2_ENTITY_TYPE_NAMES,
    L2_RELATIONS, L2_ALLOWED_RELATIONS, L2_RELATION_NAMES,
    GATE_RELATIONS, ADVISORY_RELATIONS,
)
from kg_schema.golden_set import (
    GOLDEN_SET_CSV,
    load_golden_set,
)

__all__ = [
    "ENTITY_TYPES", "L1_ENTITY_TYPE_NAMES",
    "GLINER_LABELS", "GLINER_TYPE_MAP",
    "INCIDENT_PROPERTIES",
    "CHUNK_MAX_TOKENS", "CHUNK_OVERLAP",
    "RELATION_MAP", "HIERARCHY_RELATION", "ALLOWED_RELATIONS",
    "L2_ENTITY_TYPES", "L2_ENTITY_TYPE_NAMES",
    "L2_RELATIONS", "L2_ALLOWED_RELATIONS", "L2_RELATION_NAMES",
    "GATE_RELATIONS", "ADVISORY_RELATIONS",
    "GOLDEN_SET_CSV",
    "load_golden_set",
]
