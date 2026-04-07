"""FastAPI router for Natural Language Query endpoints."""

import logging
import sys
from pathlib import Path

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# Add project root so we can import natural_language_query and query_engine
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from kg_loader import load_kg_data  # noqa: E402

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/nlq", tags=["natural-language-query"])


# ── Pydantic models ──────────────────────────────────────────────────────


class NLQRequest(BaseModel):
    query: str


class ReferencedReport(BaseModel):
    incident_id: str
    incident_type: str | None = None
    description: str | None = None


class NLQResponse(BaseModel):
    title: str
    original_query: str
    summary: list[str]
    referenced_reports: list[ReferencedReport]
    confidence: float
    clarification: str | None = None
    result_summary: str
    detail: str
    reasoning: str | None = None
    latency_ms: float
    elapsed: str


# ── Helpers ───────────────────────────────────────────────────────────────


def _collect_matched_incidents(spec, G, entities_df, metadata_df) -> list[str]:
    """Re-run the filtering from the QuerySpec to collect matched incident IDs.

    The query engine executes the filters internally but doesn't expose the
    matched incident set in its return value, so we replicate the lightweight
    filtering here using the same helpers.
    """
    from query_engine import (
        incidents_for_entity_filter,
        incidents_for_meta_filter,
        incidents_matching_narrative,
        get_entities_for_incident,
    )

    incident_sets: list[set[str]] = []

    for etype, regex, relation in spec.entity_filters:
        incs, _ = incidents_for_entity_filter(G, entities_df, etype, regex, relation)
        incident_sets.append(incs)

    for field_name, op, value in spec.meta_filters:
        incs = incidents_for_meta_filter(metadata_df, field_name, op, value)
        incident_sets.append(incs)

    if spec.narrative_keywords:
        match_all = not spec.match_any_keyword
        narr_records = incidents_matching_narrative(
            metadata_df, spec.narrative_keywords, match_all=match_all,
        )
        incident_sets.append({f"INCIDENT::{r}" for r in narr_records})

    if not incident_sets:
        return []
    elif len(incident_sets) == 1:
        incidents = incident_sets[0]
    else:
        incidents = incident_sets[0]
        for s in incident_sets[1:]:
            incidents = incidents & s

    if spec.require_connected:
        req_type, req_rel = spec.require_connected
        incidents = {
            inc_id for inc_id in incidents
            if get_entities_for_incident(G, inc_id, entity_type=req_type, relation_type=req_rel)
        }

    return sorted(incidents)[:10]


def _build_referenced_reports(incident_ids: list[str], G) -> list[ReferencedReport]:
    """Look up metadata for a list of INCIDENT::* node IDs."""
    reports: list[ReferencedReport] = []
    for inc_id in incident_ids:
        record_no = inc_id.split("::")[-1] if "::" in inc_id else inc_id
        if inc_id in G:
            node_data = G.nodes[inc_id]
            reports.append(ReferencedReport(
                incident_id=record_no,
                incident_type=node_data.get("incident_type"),
                description=str(node_data.get("value", ""))[:120],
            ))
        else:
            reports.append(ReferencedReport(incident_id=record_no))
    return reports


def _generate_title(query: str, reasoning: str | None, result_summary: str) -> str:
    """Generate a human-friendly title from LLM reasoning."""
    if reasoning:
        first_sentence = reasoning.split(".")[0].strip()
        if len(first_sentence) > 10:
            return first_sentence[0].upper() + first_sentence[1:]
    return f"Analysis: {query[:80]}"


def _generate_summary(reasoning: str | None, exec_result: dict) -> list[str]:
    """Generate summary bullet points from reasoning and execution result."""
    bullets: list[str] = []

    result_summary = exec_result.get("result_summary", "")
    if result_summary:
        bullets.append(result_summary)

    if reasoning:
        sentences = [s.strip() for s in reasoning.split(".") if len(s.strip()) > 10]
        for sentence in sentences[:2]:
            if sentence not in bullets:
                bullets.append(sentence + ".")

    # Extract "Top N:" header AND the data lines that follow it
    detail = exec_result.get("detail", "")
    detail_lines = detail.split("\n")
    for i, line in enumerate(detail_lines):
        stripped = line.strip()
        if stripped.startswith("Top ") and stripped.endswith(":"):
            # Collect the data lines below the header into a single bullet
            data_items: list[str] = []
            for j in range(i + 1, len(detail_lines)):
                data_line = detail_lines[j].strip()
                if not data_line:
                    break
                data_items.append(data_line)
            if data_items:
                bullets.append(stripped + " " + ", ".join(data_items))
            else:
                bullets.append(stripped)
            break

    return bullets[:5]


# ── Endpoint ──────────────────────────────────────────────────────────────


@router.post("/query", response_model=NLQResponse)
def run_nlq(request: NLQRequest):
    """Translate NL query -> QuerySpec -> execute against KG -> return results."""
    query = request.query.strip()
    if not query:
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    G, entities_df, relations_df, metadata_df = load_kg_data()

    # Step 1: Translate NL -> QuerySpec via Bedrock LLM
    from natural_language_query.translator import translate
    from query_engine import QuerySpec, execute_query, CUSTOM_REGISTRY

    try:
        translate_result = translate(
            query,
            backend="bedrock",
            temperature=0.1,
            max_retries=1,
        )
    except Exception as e:
        logger.exception("NLQ translation failed")
        raise HTTPException(
            status_code=502,
            detail=f"LLM translation service error: {e}",
        )

    if translate_result["query_spec"] is None:
        raise HTTPException(
            status_code=422,
            detail=translate_result.get("clarification", "Could not parse query."),
        )

    spec_dict = translate_result["query_spec"]
    reasoning = None
    nl_output = translate_result.get("nl_output")
    if nl_output:
        reasoning = getattr(nl_output, "reasoning", None)

    # Step 2: Execute QuerySpec against the KG
    try:
        spec = QuerySpec(**spec_dict)
        exec_result = execute_query(
            spec, G, entities_df, relations_df, metadata_df,
            custom_registry=CUSTOM_REGISTRY,
        )
    except Exception as e:
        logger.exception("Query execution failed")
        raise HTTPException(status_code=500, detail=f"Query execution failed: {e}")

    # Step 3: Build response — collect matched incidents for referenced reports
    matched_incidents = _collect_matched_incidents(spec, G, entities_df, metadata_df)
    referenced_reports = _build_referenced_reports(matched_incidents, G)
    title = _generate_title(query, reasoning, exec_result.get("result_summary", ""))
    summary = _generate_summary(reasoning, exec_result)

    return NLQResponse(
        title=title,
        original_query=query,
        summary=summary,
        referenced_reports=referenced_reports,
        confidence=translate_result["confidence"],
        clarification=translate_result.get("clarification"),
        result_summary=exec_result.get("result_summary", ""),
        detail=exec_result.get("detail", ""),
        reasoning=reasoning,
        latency_ms=translate_result["latency_ms"],
        elapsed=exec_result.get("elapsed", ""),
    )
