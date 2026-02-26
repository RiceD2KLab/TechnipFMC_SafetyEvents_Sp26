"""Validation for Layer 2 causal edges."""
from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import Dict, List, Set

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config.schema_v2 import L2_ALLOWED_RELATIONS, L2_ENTITY_TYPES

logger = logging.getLogger(__name__)

_VALID_ENTITY_TYPES: Set[str] = set(L2_ENTITY_TYPES)
# Case-insensitive lookup for entity type validation
_VALID_ENTITY_TYPES_LOWER: Dict[str, str] = {t.lower(): t for t in L2_ENTITY_TYPES}


def _safe_float(val: object, default: float = 0.5) -> float:
    """Safely cast to float, returning default on failure."""
    try:
        return float(val)  # type: ignore[arg-type]
    except (ValueError, TypeError):
        return default


def _entity_set_lower(entities: Dict[str, List[str]]) -> Dict[str, str]:
    """Build lowercase -> original mapping from entity dict."""
    mapping: Dict[str, str] = {}
    for values in entities.values():
        for val in values:
            mapping[val.lower().strip()] = val
    return mapping


def validate_causal_edges(
    edges: list[dict],
    entity_set: Dict[str, List[str]],
    narrative: str,
) -> list[dict]:
    """Filter invalid causal edges, returning only those that pass all checks.

    Checks:
    1. Source and target strings are grounded to known entity set (case-insensitive).
    2. Evidence string appears in the narrative (case-insensitive substring).
    3. Relation type is in the L2 allowed set.
    4. Source and target types are valid entity types.
    """
    if not edges:
        return []

    entity_lookup = _entity_set_lower(entity_set)
    narrative_lower = narrative.lower()
    valid: list[dict] = []

    for edge in edges:
        if not isinstance(edge, dict):
            logger.debug("Skipping non-dict edge: %s", edge)
            continue

        source = str(edge.get("source", "")).strip()
        target = str(edge.get("target", "")).strip()
        relation = str(edge.get("relation", "")).strip()
        evidence = str(edge.get("evidence", "")).strip()
        source_type = str(edge.get("source_type", "")).strip()
        target_type = str(edge.get("target_type", "")).strip()

        # Check relation type
        if relation not in L2_ALLOWED_RELATIONS:
            logger.debug("Invalid relation '%s' in edge: %s -> %s", relation, source, target)
            continue

        # Check source/target entity types (case-insensitive)
        if source_type.lower() not in _VALID_ENTITY_TYPES_LOWER:
            logger.debug("Invalid source_type '%s' for entity '%s'", source_type, source)
            continue
        if target_type.lower() not in _VALID_ENTITY_TYPES_LOWER:
            logger.debug("Invalid target_type '%s' for entity '%s'", target_type, target)
            continue

        # Check source grounding: entity set OR narrative substring
        if source.lower() not in entity_lookup and source.lower() not in narrative_lower:
            logger.debug("Source '%s' not in entity set or narrative", source)
            continue

        # Check target grounding: entity set OR narrative substring
        if target.lower() not in entity_lookup and target.lower() not in narrative_lower:
            logger.debug("Target '%s' not in entity set or narrative", target)
            continue

        # Check evidence grounding (case-insensitive substring match)
        if not evidence or evidence.lower() not in narrative_lower:
            logger.debug("Evidence not found in narrative: '%s'", evidence[:80])
            continue

        # Normalize: canonical entity casing, canonical type casing
        edge_clean = {
            "source": entity_lookup.get(source.lower(), source),
            "source_type": _VALID_ENTITY_TYPES_LOWER[source_type.lower()],
            "target": entity_lookup.get(target.lower(), target),
            "target_type": _VALID_ENTITY_TYPES_LOWER[target_type.lower()],
            "relation": relation,
            "evidence": evidence,
        }
        # Confidence is optional — include if present
        if "confidence" in edge:
            edge_clean["confidence"] = _safe_float(edge["confidence"])

        valid.append(edge_clean)

    return valid
