"""
Layer 2 Causal Enrichment Prompts
FMC Safety Capstone - Spring 2026

Design principles:
- System prompt is static and cacheable across all 20k records
- User prompt varies only by narrative + entity list
- Evidence grounding is required, not optional
- Negative examples prevent over-extraction
- Schema is embedded in the prompt, not just passed as JSON schema
  (grammar-constrained decoding handles format; prompt handles semantics)
"""
from __future__ import annotations

# ── System Prompt (cacheable, ~300 tokens) ─────────────────────────────────────

SYSTEM_PROMPT = """You are a safety incident analyst extracting causal relationships from oil and gas safety incident reports at TechnipFMC.

TASK: Given a short incident narrative and a list of entities already identified, extract causal edges that are explicitly supported by the text.

RELATIONS (use exactly these strings):
- CAUSED_BY: direct cause of an event or injury
- RESULTED_IN: direct outcome or consequence
- CONTRIBUTED_TO: partial or enabling cause, not the primary cause
- PRECEDED_BY: temporal sequence with implied causal link
- FAILED_CONTROL: a safety barrier or control that did not prevent the incident

ENTITY TYPES (source and target must be one of these):
Incident, Event, Equipment, Location, Person, Injury, Material, Condition, Action

RULES — follow these exactly:
1. Only extract edges where you can quote a verbatim phrase from the narrative as evidence
2. Evidence must be 20 words or fewer and must appear in the narrative
3. Source and target must be specific named entities from the entity list or clearly named in the narrative — never generic categories like "the equipment" or "the worker"
4. If the narrative is ambiguous, prefer no edge over a speculative edge
5. A single incident can have 0 edges — do not force extraction
6. Do not chain inferences: if A caused B and B caused C, extract A→B and B→C separately, not A→C directly unless stated

WHAT NOT TO EXTRACT:
- Edges where causation is implied by general knowledge but not stated in the text
- Edges where source or target cannot be grounded to a specific named entity
- Duplicate edges with slightly different wording
- Temporal sequences that have no causal language (e.g. "then", "after" alone is not enough)

EXAMPLES OF CORRECT EXTRACTION:
Narrative: "The pressure relief valve failed to open due to corrosion, causing a hydrocarbon release."
→ Equipment("pressure relief valve") CAUSED_BY Condition("corrosion") — evidence: "failed to open due to corrosion"
→ Event("hydrocarbon release") CAUSED_BY Equipment("pressure relief valve") — evidence: "causing a hydrocarbon release"

EXAMPLES OF INCORRECT EXTRACTION (do not do this):
Narrative: "Worker was near the pump when it malfunctioned."
→ DO NOT extract: Person("worker") CAUSED_BY Equipment("pump") — no causal language, only proximity
→ DO NOT extract: Injury RESULTED_IN Equipment("pump") — no injury mentioned

Respond only with valid JSON. No explanation outside the JSON."""


# ── User Prompt Template (variable per record, ~150-300 tokens) ────────────────

USER_PROMPT_TEMPLATE = """NARRATIVE:
{narrative}

ENTITIES IDENTIFIED (use these exact strings as source/target where applicable):
{entity_block}

Extract causal edges supported by this narrative."""


def format_entity_block(entities: dict[str, list[str]]) -> str:
    """
    Format entity dict for prompt injection.
    Input: {"Equipment": ["pressure relief valve", "pump"], "Person": ["rigger"], ...}
    Output: clean bulleted block
    """
    lines = []
    for entity_type, names in entities.items():
        if names:
            for name in names:
                lines.append(f"- {entity_type}: {name}")
    return "\n".join(lines) if lines else "- (no entities pre-identified)"


def build_user_prompt(narrative: str, entities: dict[str, list[str]]) -> str:
    """Build the user prompt from a narrative and entity dict."""
    return USER_PROMPT_TEMPLATE.format(
        narrative=narrative.strip(),
        entity_block=format_entity_block(entities),
    )


# ── JSON Schema for grammar-constrained decoding ───────────────────────────────
# Passed to Ollama's format parameter or Bedrock's response_format

EXTRACTION_SCHEMA = {
    "type": "object",
    "required": ["causal_edges"],
    "properties": {
        "causal_edges": {
            "type": "array",
            "items": {
                "type": "object",
                "required": [
                    "source", "source_type",
                    "relation",
                    "target", "target_type",
                    "evidence",
                ],
                "properties": {
                    "source":      {"type": "string"},
                    "source_type": {
                        "type": "string",
                        "enum": [
                            "Incident", "Event", "Equipment", "Location",
                            "Person", "Injury", "Material", "Condition", "Action",
                        ],
                    },
                    "relation": {
                        "type": "string",
                        "enum": [
                            "CAUSED_BY", "RESULTED_IN", "CONTRIBUTED_TO",
                            "PRECEDED_BY", "FAILED_CONTROL",
                        ],
                    },
                    "target":      {"type": "string"},
                    "target_type": {
                        "type": "string",
                        "enum": [
                            "Incident", "Event", "Equipment", "Location",
                            "Person", "Injury", "Material", "Condition", "Action",
                        ],
                    },
                    "evidence": {
                        "type": "string",
                        "description": "Verbatim phrase from narrative, max 20 words",
                    },
                    "confidence": {
                        "type": "number",
                        "description": "Optional self-assessed confidence 0.0-1.0",
                    },
                },
                "additionalProperties": False,
            },
        },
    },
    "additionalProperties": False,
}


# ── Prompt variants for ablation ───────────────────────────────────────────────

# Minimal prompt — tests how much the schema alone does the work
SYSTEM_PROMPT_MINIMAL = """Extract causal relationships from oil and gas safety incident reports.

Relations: CAUSED_BY, RESULTED_IN, CONTRIBUTED_TO, PRECEDED_BY, FAILED_CONTROL
Entity types: Incident, Event, Equipment, Location, Person, Injury, Material, Condition, Action

Only extract edges with direct textual evidence. Return JSON only."""


# Chain-of-thought variant — for models that benefit from reasoning traces
# Use with DeepSeek-R1-Distill or Qwen3 thinking mode
SYSTEM_PROMPT_COT = """You are a safety incident analyst extracting causal relationships from oil and gas incident reports.

Think through the narrative step by step before extracting edges:
1. Identify what happened (the incident/event)
2. Identify what caused it (look for causal language: "due to", "caused by", "failed because", "resulted in")
3. Identify what it caused (look for consequence language: "causing", "resulting in", "leading to")
4. Check each potential edge: can you quote the exact phrase that supports it?
5. Discard any edge where you cannot quote supporting text

Relations: CAUSED_BY, RESULTED_IN, CONTRIBUTED_TO, PRECEDED_BY, FAILED_CONTROL
Entity types: Incident, Event, Equipment, Location, Person, Injury, Material, Condition, Action

After reasoning, respond with JSON only. No text after the JSON."""


PROMPT_VARIANTS = {
    "full": SYSTEM_PROMPT,
    "minimal": SYSTEM_PROMPT_MINIMAL,
    "cot": SYSTEM_PROMPT_COT,
}


# ── Usage examples ─────────────────────────────────────────────────────────────

EXAMPLE_NARRATIVE = (
    "During routine maintenance, the mechanical seal on pump P-204 failed due to "
    "incorrect reinstallation by the maintenance crew. This caused a hydrocarbon "
    "leak at the pump discharge flange. The area gas detector alarmed but the "
    "permit-to-work had not been suspended, allowing hot work to continue nearby."
)

EXAMPLE_ENTITIES = {
    "Equipment": ["mechanical seal", "pump P-204", "area gas detector"],
    "Person": ["maintenance crew"],
    "Event": ["hydrocarbon leak", "hot work"],
    "Location": ["pump discharge flange"],
    "Action": ["routine maintenance"],
    "Condition": ["incorrect reinstallation"],
    "Incident": ["permit-to-work violation"],
}

EXPECTED_EDGES = [
    {
        "source": "mechanical seal",
        "source_type": "Equipment",
        "relation": "CAUSED_BY",
        "target": "incorrect reinstallation",
        "target_type": "Condition",
        "evidence": "failed due to incorrect reinstallation by the maintenance crew",
    },
    {
        "source": "hydrocarbon leak",
        "source_type": "Event",
        "relation": "CAUSED_BY",
        "target": "mechanical seal",
        "target_type": "Equipment",
        "evidence": "caused a hydrocarbon leak at the pump discharge flange",
    },
    {
        "source": "permit-to-work violation",
        "source_type": "Incident",
        "relation": "FAILED_CONTROL",
        "target": "hot work",
        "target_type": "Event",
        "evidence": "permit-to-work had not been suspended, allowing hot work to continue",
    },
]
