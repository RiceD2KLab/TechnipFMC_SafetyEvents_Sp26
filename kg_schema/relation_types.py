"""L1 relation type definitions."""
from __future__ import annotations

# ── Relation Types — Layer 1 Only ─────────────────────────────────────────
# Relation type is FULLY DETERMINED by target entity type.
RELATION_MAP: dict[str, str] = {
    "EQUIPMENT":           "INVOLVED",
    "BODY_PART":           "AFFECTED",
    "INJURY_TYPE":         "RESULTED_IN",
    "LOCATION":            "OCCURRED_AT",
    "ORGANIZATION":        "REPORTED_BY",
    "ROOT_CAUSE_CATEGORY": "CATEGORIZED_AS",
}

HIERARCHY_RELATION: str = "LOCATED_IN"  # finer → coarser (site → city → country → region)

ALLOWED_RELATIONS: frozenset[str] = frozenset({
    "INVOLVED", "AFFECTED", "RESULTED_IN", "OCCURRED_AT",
    "REPORTED_BY", "CATEGORIZED_AS", "LOCATED_IN",
})
