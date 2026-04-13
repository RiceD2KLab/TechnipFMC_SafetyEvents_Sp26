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
    # v6: EVENT captures event nouns (leak, spill, fall, explosion, ...)
    # that were previously mis-tagged as INJURY_TYPE or dropped. Linked to
    # the incident via INVOLVED. L2 also produces EVENT entities; L1 and
    # L2 EVENT rows share the same type/relation and merge naturally.
    "EVENT":               "INVOLVED",
}

HIERARCHY_RELATION: str = "LOCATED_IN"  # finer → coarser (site → city → country → region)

ALLOWED_RELATIONS: frozenset[str] = frozenset({
    "INVOLVED", "AFFECTED", "RESULTED_IN", "OCCURRED_AT",
    "REPORTED_BY", "CATEGORIZED_AS", "LOCATED_IN",
})
