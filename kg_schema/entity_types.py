"""L1 entity types, GLiNER config, incident properties, and chunking config."""
from __future__ import annotations

# ── Entity Types (7) ──────────────────────────────────────────────────────
ENTITY_TYPES: dict[str, dict[str, str]] = {
    "INCIDENT":            {"source": "header",   "description": "Hub node, one per record"},
    "EQUIPMENT":           {"source": "gliner",   "description": "Physical equipment, tools, machinery, vehicles"},
    "BODY_PART":           {"source": "gliner",   "description": "Anatomical body parts affected"},
    "INJURY_TYPE":         {"source": "gliner",   "description": "Type of injury, harm, or impact"},
    "LOCATION":            {"source": "metadata", "description": "Geographic: site, city, country, region"},
    "ORGANIZATION":        {"source": "metadata", "description": "Client or organizational unit"},
    "ROOT_CAUSE_CATEGORY": {"source": "metadata", "description": "CASE_CATEGORIZATION taxonomy (117 values)"},
    # v6: EVENT captures event-like nouns (leak, spill, fall, explosion,
    # rupture, ...) reclassified from BODY_PART/INJURY_TYPE/LOCATION drops
    # by the validation layer. L2 enrichment also produces EVENT entities;
    # they share the same type so L1 and L2 events merge naturally.
    "EVENT":               {"source": "validation", "description": "Physical event or failure occurrence"},
}

L1_ENTITY_TYPE_NAMES: frozenset[str] = frozenset(ENTITY_TYPES.keys())

# ── GLiNER Labels ─────────────────────────────────────────────────────────
# Descriptive labels improve zero-shot GLiNER recall.  The model matches
# spans against label text, so domain-specific phrasing captures more
# entities than generic one-word labels.
GLINER_LABELS: list[str] = [
    "equipment",                                          # → EQUIPMENT
    "body part or anatomical region",                     # → BODY_PART
    "type of injury, harm, or medical condition",         # → INJURY_TYPE
    "location, site, facility, or geographic area",       # → LOCATION
    "organization, company, or business unit",            # → ORGANIZATION
]

GLINER_TYPE_MAP: dict[str, str] = {
    "equipment":                                         "EQUIPMENT",
    "body part or anatomical region":                    "BODY_PART",
    "type of injury, harm, or medical condition":        "INJURY_TYPE",
    "location, site, facility, or geographic area":      "LOCATION",
    "organization, company, or business unit":           "ORGANIZATION",
}

# ── Incident Node Properties (NOT separate entity nodes) ─────────────────
INCIDENT_PROPERTIES: dict[str, dict[str, str]] = {
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

# ── GLiNER Chunking ──────────────────────────────────────────────────────
# GLiNER's model window is 384 subword tokens.  4.9% of narratives (1,143
# of 23,311) exceed this limit; 32.7% of those contain unique entity
# keywords only in the truncated tail (~588 missed instances).  Chunking
# with overlap recovers these without affecting short narratives.
CHUNK_MAX_TOKENS: int = 150   # subword tokens per chunk (< 384 model window limit)
CHUNK_OVERLAP: int = 30       # token overlap between consecutive chunks
# Note: max=150 chosen empirically.  Larger windows (350) cause GLiNER's
# confidence on minority entity types (BODY_PART, INJURY_TYPE) to collapse
# below threshold when surrounded by mechanical/operational context.  E.g.
# in #569346 "his jaw under the chin" extracts cleanly at 150 (jaw=0.56,
# chin=0.59) but is missed entirely at 350.  Smaller windows also reduce
# chunk-boundary artifacts like spurious cross-sentence spans.
