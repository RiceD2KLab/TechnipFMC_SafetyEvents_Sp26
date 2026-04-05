"""L2 entity types, relation definitions, and gate classification."""
from __future__ import annotations

# ── Layer 2: Entity Types (9) ─────────────────────────────────────────────
L2_ENTITY_TYPES: frozenset[str] = frozenset({
    "Incident", "Event", "Equipment", "Location",
    "Person", "Injury", "Material", "Condition", "Action",
})

L2_ENTITY_TYPE_NAMES: list[str] = sorted(L2_ENTITY_TYPES)

# ── Layer 2: Relation Definitions ────────────────────────────────────────
# L2 edges are produced by LLM causal enrichment (post-ER, post-Gate 2).
# They are validated separately via Gate 3, never mixed into L1 validation.
L2_RELATIONS: dict[str, dict] = {
    "CAUSAL": {
        "description": "X caused or contributed to Y (source=cause, target=effect). "
                       "Subsumes the former CAUSED_BY, RESULTED_IN, and CONTRIBUTED_TO.",
        "allowed_source_types": L2_ENTITY_TYPES,
        "allowed_target_types": L2_ENTITY_TYPES,
    },
    "PRECEDED_BY": {
        "description": "X happened after Y in the causal chain",
        "allowed_source_types": L2_ENTITY_TYPES,
        "allowed_target_types": L2_ENTITY_TYPES,
    },
    "FAILED_CONTROL": {
        "description": "Control/barrier X failed to prevent Y",
        "allowed_source_types": L2_ENTITY_TYPES,
        "allowed_target_types": L2_ENTITY_TYPES,
    },
    "MITIGATED_BY": {
        "description": "Harm/event Y was successfully prevented or reduced by control/barrier X (source=event, target=control)",
        "allowed_source_types": L2_ENTITY_TYPES,
        "allowed_target_types": L2_ENTITY_TYPES,
    },
}

L2_ALLOWED_RELATIONS: frozenset[str] = frozenset(L2_RELATIONS.keys())

L2_RELATION_NAMES: list[str] = sorted(L2_ALLOWED_RELATIONS)

# ── Gate Classification ───────────────────────────────────────────────────
GATE_RELATIONS: frozenset[str] = frozenset({"CAUSAL"})
ADVISORY_RELATIONS: frozenset[str] = frozenset({"FAILED_CONTROL", "MITIGATED_BY", "PRECEDED_BY"})

# ── REMOVED from v1 (DO NOT GENERATE) ────────────────────────────────────
# "USED_IN"   — removed (100% EQUIPMENT→LOCATION rule artifacts)
# "CAUSED_BY" — removed from L1 (90.5% broken semantics; L2-only)
