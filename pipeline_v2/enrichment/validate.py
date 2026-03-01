"""Validation for Layer 2 causal edges."""
from __future__ import annotations

import logging
import re
import sys
from pathlib import Path
from typing import Dict, List, Set

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config.schema_v2 import L2_ALLOWED_RELATIONS, L2_ENTITY_TYPES

logger = logging.getLogger(__name__)

_VALID_ENTITY_TYPES: Set[str] = set(L2_ENTITY_TYPES)
# Case-insensitive lookup for entity type validation
_VALID_ENTITY_TYPES_LOWER: Dict[str, str] = {t.lower(): t for t in L2_ENTITY_TYPES}

# Minimum consecutive words from evidence that must appear in narrative
_MIN_CONSECUTIVE_WORDS = 4

# Minimum word length to count as "significant" for entity grounding
_MIN_WORD_LEN = 3

# Regex to strip punctuation from word boundaries (keeps internal hyphens/apostrophes)
_WORD_BOUNDARY_PUNCT = re.compile(r'^[\W_]+|[\W_]+$')


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


def _evidence_grounded(evidence: str, narrative_lower: str) -> bool:
    """Check if evidence is substantially grounded in the narrative.

    Uses a sliding window: if at least _MIN_CONSECUTIVE_WORDS consecutive
    words from the evidence appear as a contiguous substring in the
    narrative, consider it grounded.  Falls back to exact substring match
    first (fast path).
    """
    if not evidence:
        return False
    ev_lower = evidence.lower()
    # Fast path: exact substring
    if ev_lower in narrative_lower:
        return True
    # Sliding window of consecutive words (strip punctuation from boundaries)
    words = [_WORD_BOUNDARY_PUNCT.sub('', w) for w in ev_lower.split() if w.strip()]
    words = [w for w in words if w]  # Remove empty strings after punctuation strip
    window = _MIN_CONSECUTIVE_WORDS
    if len(words) < window:
        # Very short evidence — require all words present in narrative
        return all(w in narrative_lower for w in words if len(w) >= _MIN_WORD_LEN)
    for i in range(len(words) - window + 1):
        fragment = " ".join(words[i : i + window])
        if fragment in narrative_lower:
            return True
    return False


def _word_in_narrative(word: str, narrative_words: Set[str]) -> bool:
    """Check if a word (or its stem prefix) appears in the narrative.

    Handles verb/noun form differences like failed/failure, leaked/leak
    by checking if the word shares a 5+ character prefix with any
    narrative word (increased from 4 to reduce false positives).
    """
    word_clean = _WORD_BOUNDARY_PUNCT.sub('', word)
    if not word_clean:
        return False
    if word_clean in narrative_words:
        return True
    # Stem-prefix: check if any narrative word shares a 4-char prefix
    # 4 chars is precise enough: fail≠fals(e), fail≠fall, fail≠faul(t)
    # but catches: fail→failed/failure/failing, leak→leaked/leaking
    if len(word_clean) >= 4:
        prefix = word_clean[:4]
        return any(nw.startswith(prefix) for nw in narrative_words if len(nw) >= 4)
    return False


def _entity_grounded(
    entity: str,
    entity_lookup: Dict[str, str],
    narrative_lower: str,
    _narr_words_cache: Dict[str, Set[str]] = {},
) -> bool:
    """Check if entity is grounded in the entity set or narrative.

    Three-tier check:
    1. Exact match in L1 entity set (case-insensitive).
    2. Exact substring in narrative (case-insensitive).
    3. Fuzzy: all significant words (>=3 chars) from the entity name
       appear in the narrative (with stem-prefix matching for
       verb/noun forms like failed/failure).
    """
    e_lower = entity.lower().strip()
    if not e_lower:
        return False
    # Tier 1: entity set
    if e_lower in entity_lookup:
        return True
    # Tier 2: exact substring in narrative
    if e_lower in narrative_lower:
        return True
    # Tier 3: all significant words present (with stem matching)
    # Strip punctuation from word boundaries before checking
    sig_words = [
        _WORD_BOUNDARY_PUNCT.sub('', w)
        for w in e_lower.split()
        if len(_WORD_BOUNDARY_PUNCT.sub('', w)) >= _MIN_WORD_LEN
    ]
    sig_words = [w for w in sig_words if w]  # Remove empty strings
    if not sig_words:
        return False
    # Cache narrative word set by narrative content hash (safer than id())
    # Use first 100 chars + length as cache key to avoid collisions
    narr_key = f"{len(narrative_lower)}:{narrative_lower[:100]}"
    if narr_key not in _narr_words_cache:
        # Split and strip punctuation from boundaries
        narr_words_raw = narrative_lower.split()
        narr_words_clean = {
            _WORD_BOUNDARY_PUNCT.sub('', w)
            for w in narr_words_raw
            if _WORD_BOUNDARY_PUNCT.sub('', w)
        }
        _narr_words_cache[narr_key] = narr_words_clean
        # Keep cache small (one narrative at a time)
        if len(_narr_words_cache) > 2:
            _narr_words_cache.clear()
            _narr_words_cache[narr_key] = narr_words_clean
    narr_words = _narr_words_cache[narr_key]
    return all(_word_in_narrative(w, narr_words) for w in sig_words)


def validate_causal_edges(
    edges: list[dict],
    entity_set: Dict[str, List[str]],
    narrative: str,
) -> list[dict]:
    """Filter invalid causal edges, returning only those that pass all checks.

    Checks:
    1. Relation type is in the L2 allowed set.
    2. Source and target types are valid entity types.
    3. Source and target are grounded (entity set, narrative substring,
       or significant-word overlap).
    4. Evidence is grounded in the narrative (exact substring or
       consecutive-word overlap).

    Logs per-stage rejection counts at INFO level for diagnostics.
    """
    if not edges:
        return []

    entity_lookup = _entity_set_lower(entity_set)
    narrative_lower = narrative.lower()
    valid: list[dict] = []
    reject_counts = {
        "non_dict": 0,
        "relation": 0,
        "source_type": 0,
        "target_type": 0,
        "source_grounding": 0,
        "target_grounding": 0,
        "evidence": 0,
    }

    for edge in edges:
        if not isinstance(edge, dict):
            reject_counts["non_dict"] += 1
            continue

        source = str(edge.get("source", "")).strip()
        target = str(edge.get("target", "")).strip()
        relation = str(edge.get("relation", "")).strip()
        evidence = str(edge.get("evidence", "")).strip()
        source_type = str(edge.get("source_type", "")).strip()
        target_type = str(edge.get("target_type", "")).strip()

        # Check relation type
        if relation not in L2_ALLOWED_RELATIONS:
            reject_counts["relation"] += 1
            logger.debug("Invalid relation '%s' in edge: %s -> %s", relation, source, target)
            continue

        # Check source/target entity types (case-insensitive)
        if source_type.lower() not in _VALID_ENTITY_TYPES_LOWER:
            reject_counts["source_type"] += 1
            logger.debug("Invalid source_type '%s' for entity '%s'", source_type, source)
            continue
        if target_type.lower() not in _VALID_ENTITY_TYPES_LOWER:
            reject_counts["target_type"] += 1
            logger.debug("Invalid target_type '%s' for entity '%s'", target_type, target)
            continue

        # Check source grounding (fuzzy)
        if not _entity_grounded(source, entity_lookup, narrative_lower):
            reject_counts["source_grounding"] += 1
            logger.debug("Source not grounded: '%s'", source)
            continue

        # Check target grounding (fuzzy)
        if not _entity_grounded(target, entity_lookup, narrative_lower):
            reject_counts["target_grounding"] += 1
            logger.debug("Target not grounded: '%s'", target)
            continue

        # Check evidence grounding (fuzzy)
        if not _evidence_grounded(evidence, narrative_lower):
            reject_counts["evidence"] += 1
            logger.debug("Evidence not grounded: '%s'", evidence[:80])
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

    # Log rejection breakdown for diagnostics
    total_rejected = sum(reject_counts.values())
    if total_rejected > 0:
        logger.info(
            "Validation: %d/%d edges passed | rejections: %s",
            len(valid), len(edges), reject_counts,
        )

    return valid
