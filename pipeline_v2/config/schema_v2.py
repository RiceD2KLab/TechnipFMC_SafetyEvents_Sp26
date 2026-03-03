"""V2 Schema definitions for the Safety Knowledge Graph."""
from __future__ import annotations

# ── Entity Types (7) ──────────────────────────────────────────────────────
ENTITY_TYPES = {
    "INCIDENT":            {"source": "header",   "description": "Hub node, one per record"},
    "EQUIPMENT":           {"source": "gliner",   "description": "Physical equipment, tools, machinery, vehicles"},
    "BODY_PART":           {"source": "gliner",   "description": "Anatomical body parts affected"},
    "INJURY_TYPE":         {"source": "gliner",   "description": "Type of injury, harm, or impact"},
    "LOCATION":            {"source": "metadata", "description": "Geographic: site, city, country, region"},
    "ORGANIZATION":        {"source": "metadata", "description": "Client or organizational unit"},
    "ROOT_CAUSE_CATEGORY": {"source": "metadata", "description": "CASE_CATEGORIZATION taxonomy (117 values)"},
}

# ── GLiNER Labels ─────────────────────────────────────────────────────────
GLINER_LABELS = [
    "equipment",       # → EQUIPMENT
    "body part",       # → BODY_PART
    "injury type",     # → INJURY_TYPE
    "location",        # → LOCATION (supplementary to metadata-parsed locations)
    "organization",    # → ORGANIZATION (supplementary to metadata-parsed orgs)
]

GLINER_TYPE_MAP = {
    "equipment":     "EQUIPMENT",
    "body part":     "BODY_PART",
    "injury type":   "INJURY_TYPE",
    "location":      "LOCATION",
    "organization":  "ORGANIZATION",
}

# ── Incident Node Properties (NOT separate entity nodes) ─────────────────
INCIDENT_PROPERTIES = {
    "incident_type":   {"source": "INCIDENT_TYPE",         "type": "enum: Accident, Near Miss, null"},
    "severity":        {"source": "SEVERITY_DESC",         "type": "string (38 levels)"},
    "severity_bin":    {"source": "derived",               "type": "int 1-5"},
    "likelihood":      {"source": "LIKELIHOOD_RANGE",      "type": "ordinal 1-5"},
    "impact_type":     {"source": "IMPACT_TYPE",           "type": "categorical"},
    "work_process":    {"source": "WORK_PROCESS",          "type": "string"},
    "risk_color":      {"source": "RISK_COLOR",            "type": "enum: Green, Yellow, Red, null"},
    "business_unit":   {"source": "GENERAL_BUSINESS_UNIT", "type": "string or null"},
    "reported_date":   {"source": "REPORTED_DATE",         "type": "ISO-8601 date"},
    "event_datetime":  {"source": "EVENT_DATETIME",        "type": "ISO-8601 datetime or null"},
    "narrative":       {"source": "NARRATIVE",             "type": "text"},
}

# ── Relation Types — Layer 1 Only ─────────────────────────────────────────
# Relation type is FULLY DETERMINED by target entity type.
RELATION_MAP = {
    "EQUIPMENT":           "INVOLVED",
    "BODY_PART":           "AFFECTED",
    "INJURY_TYPE":         "RESULTED_IN",
    "LOCATION":            "OCCURRED_AT",
    "ORGANIZATION":        "REPORTED_BY",
    "ROOT_CAUSE_CATEGORY": "CATEGORIZED_AS",
}

HIERARCHY_RELATION = "LOCATED_IN"  # finer → coarser (site → city → country → region)

ALLOWED_RELATIONS = frozenset({
    "INVOLVED", "AFFECTED", "RESULTED_IN", "OCCURRED_AT",
    "REPORTED_BY", "CATEGORIZED_AS", "LOCATED_IN",
})

# ── GLiNER Chunking ──────────────────────────────────────────────────────
# GLiNER's model window is 384 subword tokens.  4.9% of narratives (1,143
# of 23,311) exceed this limit; 32.7% of those contain unique entity
# keywords only in the truncated tail (~588 missed instances).  Chunking
# with overlap recovers these without affecting short narratives.
CHUNK_MAX_TOKENS = 350   # subword tokens per chunk (< 384 model window limit)
CHUNK_OVERLAP = 50       # token overlap between consecutive chunks

# ── Layer 2: Causal Relation Types ───────────────────────────────────────
# L2 edges are produced by LLM causal enrichment (post-ER, post-Gate 2).
# They are validated separately via Gate 3, never mixed into L1 validation.

L2_ENTITY_TYPES = frozenset({
    "Incident", "Event", "Equipment", "Location",
    "Person", "Injury", "Material", "Condition", "Action",
})

L2_RELATIONS = {
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
}

L2_ALLOWED_RELATIONS = frozenset(L2_RELATIONS.keys())

# ── REMOVED from v1 (DO NOT GENERATE) ────────────────────────────────────
# "USED_IN"   — removed (100% EQUIPMENT→LOCATION rule artifacts)
# "CAUSED_BY" — removed from L1 (90.5% broken semantics; L2-only)
