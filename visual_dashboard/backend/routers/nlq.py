"""FastAPI router for Natural Language Query endpoints."""

import csv
import io
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from fpdf import FPDF
from pydantic import BaseModel

# Add project root so we can import natural_language_query and query_engine
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from kg_loader import load_kg_data  # noqa: E402

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/nlq", tags=["natural-language-query"])

# ── Incidents CSV loader (cached) ────────────────────────────────────────

_INCIDENTS_CSV = _PROJECT_ROOT / "input" / "incidents.csv"
_incidents_cache: dict[str, str] | None = None


def _load_incidents_csv() -> dict[str, str]:
    """Load input/incidents.csv into a dict: record_no -> full text."""
    global _incidents_cache
    if _incidents_cache is not None:
        return _incidents_cache

    lookup: dict[str, str] = {}
    if _INCIDENTS_CSV.exists():
        with open(_INCIDENTS_CSV, encoding="utf-8", errors="replace") as f:
            reader = csv.DictReader(f)
            for row in reader:
                record_no = row.get("RECORD_NO_LOSS_POTENTIAL", "").strip()
                text = row.get("text", "").strip()
                if record_no:
                    lookup[record_no] = text
        logger.info("Loaded %d incident records from CSV", len(lookup))
    else:
        logger.warning("incidents.csv not found at %s", _INCIDENTS_CSV)

    _incidents_cache = lookup
    return lookup


# ── Pydantic models ──────────────────────────────────────────────────────


class NLQRequest(BaseModel):
    query: str


class ReferencedReport(BaseModel):
    incident_id: str
    incident_type: str | None = None
    description: str | None = None


class PDFExportRequest(BaseModel):
    title: str
    original_query: str
    summary: list[str]
    referenced_reports: list[ReferencedReport]


class NLQResponse(BaseModel):
    title: str
    original_query: str
    answer: str | None = None
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


def _generate_answer(exec_result: dict) -> str | None:
    """Extract the direct answer from execution results.

    Looks for "Top N:" aggregation data in the detail field, which represents
    the concrete answer to the user's query. Falls back to result_summary if
    no Top N block is found but the summary itself is substantive.
    """
    detail = exec_result.get("detail", "")
    detail_lines = detail.split("\n")

    for i, line in enumerate(detail_lines):
        stripped = line.strip()
        if stripped.startswith("Top ") and stripped.endswith(":"):
            data_items: list[str] = []
            for j in range(i + 1, len(detail_lines)):
                data_line = detail_lines[j].strip()
                if not data_line:
                    break
                data_items.append(data_line)
            if data_items:
                return stripped + "\n" + "\n".join(data_items)
            return stripped

    # Fallback: use result_summary if it contains a concrete "top:" mention
    result_summary = exec_result.get("result_summary", "")
    if result_summary and "top:" in result_summary.lower():
        return result_summary

    return None


def _generate_summary(reasoning: str | None, exec_result: dict) -> list[str]:
    """Generate supporting context bullet points from reasoning and execution result.

    The primary answer (Top N data) is handled separately by _generate_answer(),
    so this function focuses on contextual information.
    """
    bullets: list[str] = []

    result_summary = exec_result.get("result_summary", "")
    if result_summary:
        bullets.append(result_summary)

    if reasoning:
        sentences = [s.strip() for s in reasoning.split(".") if len(s.strip()) > 10]
        for sentence in sentences[:2]:
            if sentence not in bullets:
                bullets.append(sentence + ".")

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
    answer = _generate_answer(exec_result)
    summary = _generate_summary(reasoning, exec_result)

    return NLQResponse(
        title=title,
        original_query=query,
        answer=answer,
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


# ── PDF Export ────────────────────────────────────────────────────────────


class _ReportPDF(FPDF):
    """Custom PDF with TechnipFMC header/footer."""

    def header(self):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(59, 130, 246)  # blue-500
        self.cell(0, 8, "TechnipFMC Safety Analytics Platform", ln=True)
        self.set_draw_color(229, 231, 235)  # gray-200
        self.line(10, self.get_y(), self.w - 10, self.get_y())
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "", 8)
        self.set_text_color(156, 163, 175)  # gray-400
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")


def _parse_incident_text(raw: str) -> dict[str, str]:
    """Parse the structured text blob from incidents.csv into sections.

    The CSV stores newlines as literal two-char ``\\n`` sequences, so we
    normalise those to real newlines before splitting.
    """
    # Normalise literal \n to real newlines
    text = raw.replace("\\n", "\n")

    sections: dict[str, str] = {}
    current_key = ""
    current_lines: list[str] = []

    for line in text.split("\n"):
        stripped = line.strip()
        if stripped.startswith("INCIDENT_LABEL:"):
            sections["label"] = stripped.split(":", 1)[1].strip()
        elif stripped.startswith("NARRATIVE:"):
            if current_key and current_lines:
                sections[current_key] = "\n".join(current_lines).strip()
            current_key = "narrative"
            current_lines = []
        elif stripped.startswith("ENTITY_FACTS:"):
            if current_key and current_lines:
                sections[current_key] = "\n".join(current_lines).strip()
            current_key = "entity_facts"
            current_lines = []
        elif stripped.startswith("META_FACTS:"):
            if current_key and current_lines:
                sections[current_key] = "\n".join(current_lines).strip()
            current_key = "meta_facts"
            current_lines = []
        else:
            if stripped:
                current_lines.append(stripped)

    if current_key and current_lines:
        sections[current_key] = "\n".join(current_lines).strip()

    return sections


def _safe_text(text: str) -> str:
    """Replace characters that fpdf2 can't encode in latin-1."""
    return text.encode("latin-1", errors="replace").decode("latin-1")


@router.post("/export-pdf")
def export_pdf(request: PDFExportRequest):
    """Generate a PDF report for an NLQ result with full incident details."""
    incidents_lookup = _load_incidents_csv()

    pdf = _ReportPDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()

    # ── Title ─────────────────────────────────────────────────────────
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(17, 24, 39)  # gray-900
    pdf.multi_cell(0, 8, _safe_text(request.title))
    pdf.ln(2)

    # ── Query ─────────────────────────────────────────────────────────
    pdf.set_font("Helvetica", "I", 11)
    pdf.set_text_color(107, 114, 128)  # gray-500
    pdf.multi_cell(0, 6, _safe_text(f'Query: "{request.original_query}"'))
    pdf.ln(1)
    pdf.set_font("Helvetica", "", 9)
    pdf.cell(0, 5, f"Generated: {datetime.now(timezone.utc).strftime('%B %d, %Y at %H:%M UTC')}", ln=True)
    pdf.ln(4)

    # ── Summary ───────────────────────────────────────────────────────
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(17, 24, 39)
    pdf.cell(0, 8, "Summary", ln=True)
    pdf.set_draw_color(229, 231, 235)
    pdf.line(10, pdf.get_y(), pdf.w - 10, pdf.get_y())
    pdf.ln(3)

    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(55, 65, 81)  # gray-700
    for bullet in request.summary:
        pdf.cell(5)
        pdf.cell(5, 6, "-")
        pdf.multi_cell(0, 6, _safe_text(f"  {bullet}"))
        pdf.ln(1)
    pdf.ln(4)

    # ── Referenced Safety Reports ─────────────────────────────────────
    orig_l_margin = pdf.l_margin        # 10
    orig_r_margin = pdf.r_margin        # 10
    page_width = pdf.w                  # 210
    content_width = page_width - orig_l_margin - orig_r_margin  # 190
    body_margin = orig_l_margin + 8     # indented left margin for body text
    body_width = content_width - 16     # body text width (8 padding each side)

    if request.referenced_reports:
        pdf.set_font("Helvetica", "B", 12)
        pdf.set_text_color(17, 24, 39)
        pdf.cell(0, 8, f"Referenced Safety Reports ({len(request.referenced_reports)})", ln=True)
        pdf.set_draw_color(229, 231, 235)
        pdf.line(orig_l_margin, pdf.get_y(), page_width - orig_r_margin, pdf.get_y())
        pdf.ln(6)

        for i, report in enumerate(request.referenced_reports):
            raw_text = incidents_lookup.get(report.incident_id, "")
            sections = _parse_incident_text(raw_text) if raw_text else {}

            # ── Header line (bold, dark text — no background rect) ──
            label = sections.get("label", f"Incident {report.incident_id}")
            pdf.set_font("Helvetica", "B", 11)
            pdf.set_text_color(59, 130, 246)  # blue
            pdf.set_left_margin(orig_l_margin)
            pdf.set_x(orig_l_margin)
            pdf.multi_cell(content_width, 6, _safe_text(
                f"SER-{report.incident_id}  |  {label}"
            ))
            # Underline below header
            pdf.set_draw_color(59, 130, 246)
            pdf.line(orig_l_margin, pdf.get_y(), page_width - orig_r_margin, pdf.get_y())
            pdf.ln(4)

            # ── Body: shift margins inward ──
            pdf.set_left_margin(body_margin)
            pdf.set_right_margin(orig_r_margin + 8)

            # Narrative
            narrative = sections.get("narrative", "")
            if narrative:
                pdf.set_x(body_margin)
                pdf.set_font("Helvetica", "B", 9)
                pdf.set_text_color(30, 64, 175)  # blue-800
                pdf.cell(body_width, 6, "Narrative", ln=True)
                pdf.set_font("Helvetica", "", 9)
                pdf.set_text_color(55, 65, 81)
                pdf.set_x(body_margin)
                pdf.multi_cell(body_width, 4.5, _safe_text(narrative))
                pdf.ln(3)

            # Entity facts
            entity_facts = sections.get("entity_facts", "")
            if entity_facts:
                pdf.set_x(body_margin)
                pdf.set_font("Helvetica", "B", 9)
                pdf.set_text_color(30, 64, 175)
                pdf.cell(body_width, 6, "Incident Details", ln=True)
                pdf.set_font("Helvetica", "", 8.5)
                pdf.set_text_color(55, 65, 81)
                for fact_line in entity_facts.split("\n"):
                    fact_line = fact_line.strip().lstrip("- ")
                    if not fact_line:
                        continue
                    pdf.set_x(body_margin + 2)
                    pdf.cell(3, 4.5, "-")
                    pdf.multi_cell(body_width - 5, 4.5, _safe_text(f" {fact_line}"))
                pdf.ln(3)

            # Meta facts
            meta_facts = sections.get("meta_facts", "")
            if meta_facts:
                pdf.set_x(body_margin)
                pdf.set_font("Helvetica", "B", 9)
                pdf.set_text_color(30, 64, 175)
                pdf.cell(body_width, 6, "Additional Metadata", ln=True)
                pdf.set_font("Helvetica", "", 8.5)
                pdf.set_text_color(55, 65, 81)
                for meta_line in meta_facts.split("\n"):
                    meta_line = meta_line.strip().lstrip("- ")
                    if not meta_line:
                        continue
                    cleaned = meta_line.replace("META[", "").replace("]", "")
                    pdf.set_x(body_margin + 2)
                    pdf.cell(3, 4.5, "-")
                    pdf.multi_cell(body_width - 5, 4.5, _safe_text(f" {cleaned}"))
                pdf.ln(2)

            # ── Restore margins ──
            pdf.set_left_margin(orig_l_margin)
            pdf.set_right_margin(orig_r_margin)

            # Separator between reports (simple line, no rect)
            if i < len(request.referenced_reports) - 1:
                pdf.set_draw_color(209, 213, 219)  # gray-300
                pdf.line(orig_l_margin + 10, pdf.get_y(),
                         page_width - orig_r_margin - 10, pdf.get_y())
                pdf.ln(6)

    # ── Output ────────────────────────────────────────────────────────
    buf = io.BytesIO()
    buf.write(pdf.output())
    buf.seek(0)

    return StreamingResponse(
        buf,
        media_type="application/pdf",
        headers={"Content-Disposition": "inline; filename=safety_query_report.pdf"},
    )
