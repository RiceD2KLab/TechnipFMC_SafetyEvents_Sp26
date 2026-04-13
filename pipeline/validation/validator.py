"""Core validation logic for v6.

Takes a gliner_extractions DataFrame (columns: span, type, score, start,
end, record_no, source) and returns a validated DataFrame with noise rows
dropped and mis-typed rows reclassified. Also returns a change log and
summary stats.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

import pandas as pd

from pipeline.ontology.taxonomies import BODY_PART_REGIONS, BODY_PART_NOISE
from pipeline.ontology.enricher import _bucket_body_part
from .injury_taxonomy import is_valid_injury_type
from .equipment_rules import (
    is_person_role,
    is_generic_position,
    looks_like_equipment,
    looks_like_event,
)

Action = Literal["keep", "drop", "reclassify"]


@dataclass
class ValidationResult:
    """Result of validating a gliner_extractions DataFrame."""
    validated: pd.DataFrame
    dropped: pd.DataFrame           # original rows that were dropped, with 'reason' column
    reclassified: pd.DataFrame      # original rows that changed type, with 'old_type'/'new_type'/'reason'
    stats: dict = field(default_factory=dict)


def _validate_span(span: str, entity_type: str) -> tuple[Action, str | None, str]:
    """Validate a single (span, type) pair.

    Returns (action, new_type_if_reclassify, reason).
    """
    if not isinstance(span, str) or not span.strip():
        return "drop", None, "empty_span"

    # Universal filters that apply regardless of type
    if is_person_role(span):
        return "drop", None, "person_role"

    if entity_type == "BODY_PART":
        # Allow-list wins: anatomy check is first so legitimate terms like
        # "back" / "side" that ALSO appear in GENERIC_POSITIONS are kept.
        if span.strip().lower() in BODY_PART_NOISE:
            return "drop", None, "body_part_noise_explicit"
        region, _lat, is_noise = _bucket_body_part(span)
        if not is_noise and region is not None:
            return "keep", None, "anatomy_matched"
        # Anatomy check failed. Now apply exclusion lists before
        # considering reclassification.
        if is_generic_position(span):
            return "drop", None, "body_part_generic_position"
        # Try reclassification: EVENT first (more specific semantics),
        # then EQUIPMENT (broader catch-all).
        if looks_like_event(span):
            return "reclassify", "EVENT", "body_part_reclassified_as_event"
        if looks_like_equipment(span):
            return "reclassify", "EQUIPMENT", "body_part_reclassified_as_equipment"
        # Drop — unknown anatomy AND not equipment/event-looking
        return "drop", None, "body_part_unclassified"

    if entity_type == "EQUIPMENT":
        # Reject generic positions and role nouns (person_role already handled above)
        if is_generic_position(span):
            return "drop", None, "equipment_generic_position"
        # EQUIPMENT is intentionally permissive — the type is a catch-all for
        # machinery/tools/structures. We only reject clearly non-equipment strings.
        return "keep", None, "equipment_permissive_keep"

    if entity_type == "INJURY_TYPE":
        if is_valid_injury_type(span):
            return "keep", None, "injury_taxonomy_matched"
        # Try rescue-reclassification: EVENT first (leak, spill, fall, ...)
        # then EQUIPMENT for mechanical-noun mis-tags. Both preserve
        # information that would otherwise be dropped.
        if looks_like_event(span):
            return "reclassify", "EVENT", "injury_reclassified_as_event"
        if looks_like_equipment(span):
            return "reclassify", "EQUIPMENT", "injury_reclassified_as_equipment"
        return "drop", None, "injury_not_in_taxonomy"

    if entity_type == "LOCATION":
        # GLiNER-extracted LOCATIONs are often micro-locations (walkway, cabin)
        # or mis-tagged events/equipment. Reject generic positions, try
        # EVENT then EQUIPMENT rescue, otherwise keep as-is.
        if is_generic_position(span):
            return "drop", None, "location_generic_position"
        if looks_like_event(span):
            return "reclassify", "EVENT", "location_reclassified_as_event"
        if looks_like_equipment(span):
            return "reclassify", "EQUIPMENT", "location_reclassified_as_equipment"
        return "keep", None, "location_permissive_keep"

    if entity_type == "ORGANIZATION":
        # Reject generic roles and single-token "team"/"crew" style nouns
        lowered = span.strip().lower()
        generic_org = {"team", "crew", "client", "contractor", "subcontractor",
                       "company", "organization", "organisation", "the team"}
        if lowered in generic_org:
            return "drop", None, "organization_generic"
        return "keep", None, "organization_keep"

    # Unknown type — keep as-is, let graph builder handle it
    return "keep", None, f"unknown_type_{entity_type}"


def validate_extractions(gliner_df: pd.DataFrame) -> ValidationResult:
    """Apply v6 validation rules to a gliner_extractions DataFrame.

    Input columns:  span, type, score, start, end, record_no, source
    Output DataFrame has the same columns; rows may have 'type' changed
    (reclassification) or be removed entirely (drop).

    The change log tracks every drop and reclassification with a reason.
    """
    if len(gliner_df) == 0:
        return ValidationResult(
            validated=gliner_df.copy(),
            dropped=gliner_df.iloc[0:0].copy(),
            reclassified=gliner_df.iloc[0:0].copy(),
            stats={"input": 0, "kept": 0, "dropped": 0, "reclassified": 0},
        )

    # Work in numpy arrays for speed — 160k rows × dict lookups would be
    # noticeable if we used .iterrows()
    spans = gliner_df["span"].tolist()
    types = gliner_df["type"].tolist()

    new_types: list[str] = []
    actions: list[str] = []
    reasons: list[str] = []

    # Deterministic: build a small cache so identical (span, type) pairs
    # don't get re-validated. ~30% hit rate expected.
    cache: dict[tuple[str, str], tuple[Action, str | None, str]] = {}

    for span, etype in zip(spans, types):
        key = (span if isinstance(span, str) else "", etype if isinstance(etype, str) else "")
        if key in cache:
            action, new_type, reason = cache[key]
        else:
            action, new_type, reason = _validate_span(
                key[0], key[1]
            )
            cache[key] = (action, new_type, reason)

        if action == "reclassify" and new_type is not None:
            new_types.append(new_type)
        else:
            new_types.append(etype)
        actions.append(action)
        reasons.append(reason)

    # Assemble validated df
    work = gliner_df.copy()
    work["_action"] = actions
    work["_reason"] = reasons
    work["_new_type"] = new_types

    validated_mask = work["_action"].isin(["keep", "reclassify"])
    dropped_mask = work["_action"] == "drop"
    reclassified_mask = work["_action"] == "reclassify"

    validated = work.loc[validated_mask].copy()
    # Apply reclassification by overwriting the type column
    validated["type"] = validated["_new_type"]
    validated = validated.drop(columns=["_action", "_reason", "_new_type"])

    dropped = work.loc[dropped_mask, list(gliner_df.columns) + ["_reason"]].copy()
    dropped = dropped.rename(columns={"_reason": "reason"})

    reclassified = work.loc[reclassified_mask, list(gliner_df.columns) + ["_new_type", "_reason"]].copy()
    reclassified = reclassified.rename(columns={
        "type": "old_type",
        "_new_type": "new_type",
        "_reason": "reason",
    })

    # ── Stats ────────────────────────────────────────────────────────────
    input_n = len(gliner_df)
    kept_n = int(validated_mask.sum()) - int(reclassified_mask.sum())
    dropped_n = int(dropped_mask.sum())
    reclassified_n = int(reclassified_mask.sum())

    # Per-type drop reasons
    drop_reasons_by_type: dict[str, dict[str, int]] = {}
    for etype, reason in zip(work.loc[dropped_mask, "type"], work.loc[dropped_mask, "_reason"]):
        drop_reasons_by_type.setdefault(etype, {}).setdefault(reason, 0)
        drop_reasons_by_type[etype][reason] += 1

    # Per-type reclassification summary
    reclassified_by_direction: dict[str, int] = {}
    for old, new in zip(work.loc[reclassified_mask, "type"],
                         work.loc[reclassified_mask, "_new_type"]):
        key = f"{old}→{new}"
        reclassified_by_direction[key] = reclassified_by_direction.get(key, 0) + 1

    # Type count delta
    type_before = gliner_df["type"].value_counts().to_dict()
    type_after = validated["type"].value_counts().to_dict()
    type_delta = {
        t: {"before": type_before.get(t, 0), "after": type_after.get(t, 0),
            "delta": type_after.get(t, 0) - type_before.get(t, 0)}
        for t in set(type_before) | set(type_after)
    }

    stats = {
        "input": input_n,
        "kept": kept_n,
        "dropped": dropped_n,
        "reclassified": reclassified_n,
        "output": len(validated),
        "drop_rate_pct": round(100 * dropped_n / max(input_n, 1), 2),
        "drop_reasons_by_type": drop_reasons_by_type,
        "reclassified_by_direction": reclassified_by_direction,
        "type_delta": type_delta,
    }

    return ValidationResult(
        validated=validated,
        dropped=dropped,
        reclassified=reclassified,
        stats=stats,
    )
