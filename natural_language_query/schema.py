"""Pydantic schema for NL → QuerySpec translation.

The LLM outputs an NLQueryOutput (JSON). The bridge function converts
it to the existing benchmark QuerySpec dataclass so execute_query()
works unchanged.
"""

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, field_validator

from kg_schema import ENTITY_TYPES, ALLOWED_RELATIONS


# ── Enums built from kg_schema (single source of truth) ─────────────────

class Strategy(str, Enum):
    entity_filter = "entity_filter"
    meta_filter = "meta_filter"
    narrative_filter = "narrative_filter"
    intersect = "intersect"
    crosstab = "crosstab"
    custom = "custom"
    out_of_scope = "out_of_scope"


EntityType = Enum("EntityType", {k: k for k in ENTITY_TYPES}, type=str)
Relation = Enum("Relation", {r: r for r in ALLOWED_RELATIONS}, type=str)


class MetaOp(str, Enum):
    eq = "=="
    neq = "!="
    gt = ">"
    gte = ">="
    lt = "<"
    lte = "<="
    contains = "contains"


class OutputMode(str, Enum):
    count_incidents = "count_incidents"
    aggregate = "aggregate"
    count_by_year = "count_by_year"
    crosstab = "crosstab"
    list_incidents = "list_incidents"


# ── LLM output schema ───────────────────────────────────────────────────

class EntityFilter(BaseModel):
    """A single entity filter: type + regex pattern + relation."""
    entity_type: EntityType
    pattern: str = Field(
        description="Regex pattern to match entity values. "
        "Use | for alternatives, e.g. 'forklift|fork lift|flt'."
    )
    relation: Relation = Field(
        description="The relation connecting INCIDENT to this entity type."
    )


class MetaFilter(BaseModel):
    """A single metadata filter: field + operator + value."""
    field: str = Field(
        description="Metadata column name. Common fields: "
        "year, severity_bin, incident_type (accident|near_miss|first_aid), "
        "work_process, business_unit, impact_type, country."
    )
    op: MetaOp
    value: str = Field(
        description="Value to compare against. "
        "For year: '2022'. For severity_bin: '4'. "
        "For incident_type: 'accident'. For work_process: use 'contains'."
    )


class AggregateTarget(BaseModel):
    """What to aggregate/count by."""
    entity_type: EntityType
    relation: Relation
    granularity: Optional[str] = Field(
        default=None,
        description="Sub-field granularity. For LOCATION: 'country', "
        "'region', 'city'. Leave null for default."
    )


class CrosstabTarget(BaseModel):
    """Two metadata fields to cross-tabulate."""
    row_field: str
    col_field: str


class NLQueryOutput(BaseModel):
    """The structured output the LLM must produce.

    This gets converted to the existing QuerySpec dataclass.
    """
    strategy: Strategy = Field(
        description="Which execution strategy to use."
    )
    entity_filters: list[EntityFilter] = Field(
        default_factory=list,
        description="Entity-based filters. Each one narrows the incident set."
    )
    meta_filters: list[MetaFilter] = Field(
        default_factory=list,
        description="Metadata-based filters (year, severity, type, etc.)."
    )
    narrative_keywords: list[str] = Field(
        default_factory=list,
        description="Keywords to search in incident narratives. "
        "Use only when entities/metadata don't capture the concept."
    )
    match_any_keyword: bool = Field(
        default=False,
        description="If true, match ANY keyword (OR). "
        "If false, match ALL keywords (AND)."
    )
    output_mode: OutputMode = Field(
        default=OutputMode.count_incidents,
        description="How to present results."
    )
    aggregate_target: Optional[AggregateTarget] = Field(
        default=None,
        description="Required when output_mode is 'aggregate'. "
        "Specifies what entity type to aggregate by."
    )
    crosstab_target: Optional[CrosstabTarget] = Field(
        default=None,
        description="Required when output_mode is 'crosstab'. "
        "Specifies the two metadata fields."
    )
    custom_fn: Optional[str] = Field(
        default=None,
        description="When strategy is 'custom', the name of the custom query function "
        "(e.g. 'top_injury_per_equipment', 'severity_comparison'). Leave null otherwise."
    )
    output_top_n: Optional[int] = Field(
        default=10,
        ge=1,
        le=50,
        description="Number of top results to return for aggregations. Use 10 if unsure."
    )
    confidence: float = Field(
        default=0.9,
        ge=0.0,
        le=1.0,
        description="Your confidence that this query spec correctly "
        "captures the user's intent. Set < 0.7 if unsure."
    )
    clarification: Optional[str] = Field(
        default=None,
        description="If confidence < 0.7, explain what's ambiguous "
        "and suggest how the user could rephrase."
    )
    reasoning: Optional[str] = Field(
        default=None,
        description="Brief explanation of why you chose this strategy "
        "and these filters."
    )

    @field_validator("strategy", mode="before")
    @classmethod
    def coerce_strategy(cls, v):
        """Coerce common LLM mistakes: 'aggregate' and 'count_by_year' are output_modes."""
        if v == "aggregate":
            return "entity_filter"  # aggregation is expressed via output_mode
        if v == "count_by_year":
            return "meta_filter"  # temporal trend is output_mode count_by_year
        return v

    @field_validator("output_top_n", mode="before")
    @classmethod
    def default_output_top_n(cls, v):
        """Coerce None to 10 so LLM omitting the field still validates."""
        if v is None:
            return 10
        return v


# ── Bridge to existing QuerySpec ─────────────────────────────────────────

def to_query_spec(nl: NLQueryOutput, query_id: str = "NL-00",
                  name: str = "NL query") -> dict:
    """Convert NLQueryOutput to the kwargs dict that matches
    the existing benchmark QuerySpec dataclass.

    Returns a dict you can pass to QuerySpec(**result).
    """
    # Build entity_filters as list of (type, regex, relation) tuples
    entity_filters = [
        (ef.entity_type.value, ef.pattern, ef.relation.value)
        for ef in nl.entity_filters
    ]

    # Build meta_filters as list of (field, op, value) tuples
    meta_filters = [
        (mf.field, mf.op.value, mf.value)
        for mf in nl.meta_filters
    ]

    # Determine strategy: upgrade to intersect if multiple filter types
    strategy = nl.strategy.value
    filter_type_count = sum([
        len(entity_filters) > 0,
        len(meta_filters) > 0,
        len(nl.narrative_keywords) > 0,
    ])
    if filter_type_count > 1 and strategy not in ("crosstab", "custom",
                                                    "out_of_scope"):
        strategy = "intersect"

    # Build output_target string for aggregate mode
    output_target = ""
    if nl.output_mode == OutputMode.aggregate and nl.aggregate_target:
        at = nl.aggregate_target
        if at.granularity:
            output_target = (
                f"{at.entity_type.value}[{at.granularity}]"
                f":{at.relation.value}"
            )
        else:
            output_target = f"{at.entity_type.value}:{at.relation.value}"
    elif nl.output_mode == OutputMode.crosstab and nl.crosstab_target:
        ct = nl.crosstab_target
        output_target = f"{ct.row_field}:{ct.col_field}"
    elif nl.output_mode == OutputMode.count_by_year:
        output_target = "year"

    # Map output_mode to the CSV convention
    output_mode = nl.output_mode.value

    return {
        "query_id": query_id,
        "name": name,
        "query_type": "NL",
        "strategy": strategy,
        "entity_filters": entity_filters,
        "meta_filters": meta_filters,
        "narrative_keywords": nl.narrative_keywords,
        "match_any_keyword": nl.match_any_keyword,
        "require_connected": None,
        "output_mode": output_mode,
        "output_target": output_target,
        "output_top_n": nl.output_top_n or 10,
        "coverage_thresholds": (1, 0),
        "diagnosis_rule": "auto",
        "custom_fn": (nl.custom_fn or "").strip(),
        "ground_truth": set(),
        "notes": nl.reasoning or "",
        "expected_count": None,
    }
