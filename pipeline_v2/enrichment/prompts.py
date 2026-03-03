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

TASK: Given an incident narrative and a list of pre-identified entities, extract causal edges supported by the text. Use the entity list as a starting point, but also extract entities and events described in the narrative even if they are not in the list.

RELATIONS (use exactly these strings):
- CAUSAL: one thing caused, led to, or contributed to another (source=cause, target=effect). Covers direct cause, consequence, and contributing factors. Look for: "due to", "caused by", "because of", "resulted in", "causing", "leading to", "contributed to", "was a factor"
- PRECEDED_BY: temporal sequence with causal link (look for: "after", "following", "when")
- FAILED_CONTROL: a safety barrier that failed (look for: "failed to", "did not prevent", "was not")
- MITIGATED_BY: harm/event was prevented or reduced by a control or barrier (source=event, target=control). Look for: "prevented", "stopped", "contained", "caught", "PPE protected", "barrier held", "alarm alerted"

DIRECTION RULE: For CAUSAL edges, source is always the CAUSE and target is always the EFFECT.
- "fire due to corrosion" → source="corrosion", target="fire"
- "leak caused damage" → source="leak", target="damage"
- "rain contributed to slippery surface" → source="rain", target="slippery surface"

ENTITY TYPES (source and target must be one of these):
Incident, Event, Equipment, Location, Person, Injury, Material, Condition, Action

RULES:
1. Source and target should use descriptive phrases from the narrative (e.g., "short circuiting of wires for the heating element", not just "short circuit")
2. Avoid generic entities like "the worker", "the equipment", or "the incident" — use the specific name from the text
3. Evidence must be a phrase from the narrative (up to 25 words)
4. Extract ALL causal relationships you can find — most incident narratives contain at least one
5. Only return an empty list if the narrative has zero causal language (no "due to", "caused", "resulted", "failed", etc.)
6. Do not chain inferences: extract A→B and B→C separately, not A→C
7. Do not duplicate edges with different wording

EXAMPLES:
Narrative: "The pressure relief valve failed to open due to corrosion, causing a hydrocarbon release."
→ Condition("corrosion") CAUSAL Equipment("pressure relief valve failure") — evidence: "failed to open due to corrosion"
→ Equipment("pressure relief valve failure") CAUSAL Event("hydrocarbon release") — evidence: "causing a hydrocarbon release"

Narrative: "Fire started in electrical panel due to short circuiting of wires. The smoke detector in the room was not functioning."
→ Condition("short circuiting of wires") CAUSAL Event("fire") — evidence: "Fire started in electrical panel due to short circuiting of wires"
→ Event("fire") FAILED_CONTROL Equipment("smoke detector") — evidence: "smoke detector in the room was not functioning"

Narrative: "The gas leak was detected by the H2S monitor, which triggered the emergency shutdown and prevented any injuries."
→ Event("gas leak") MITIGATED_BY Equipment("H2S monitor") — evidence: "gas leak was detected by the H2S monitor"
→ Event("injuries") MITIGATED_BY Equipment("emergency shutdown") — evidence: "triggered the emergency shutdown and prevented any injuries"

Respond only with valid JSON. No explanation outside the JSON."""


# ── User Prompt Template (variable per record, ~150-300 tokens) ────────────────

USER_PROMPT_TEMPLATE = """NARRATIVE:
{narrative}

PRE-IDENTIFIED ENTITIES (use as source/target when relevant, but also extract new entities from the narrative):
{entity_block}

Extract all causal edges from this narrative. Most incidents have 1-3 causal relationships."""


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


def build_user_prompt(
    narrative: str,
    entities: dict[str, list[str]],
    variant: str = "full",
) -> str:
    """Build the user prompt from a narrative and entity dict."""
    template = USER_PROMPT_TEMPLATE_V2 if variant == "full_v2" else USER_PROMPT_TEMPLATE
    return template.format(
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
                            "CAUSAL", "PRECEDED_BY", "FAILED_CONTROL",
                            "MITIGATED_BY",
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
                        "description": "Phrase from narrative supporting this edge, max 25 words",
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

Relations: CAUSAL (source=cause, target=effect), PRECEDED_BY, FAILED_CONTROL, MITIGATED_BY (control that worked)
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

Relations: CAUSAL (source=cause, target=effect), PRECEDED_BY, FAILED_CONTROL, MITIGATED_BY (control that worked)
Entity types: Incident, Event, Equipment, Location, Person, Injury, Material, Condition, Action

After reasoning, respond with JSON only. No text after the JSON."""


# Full V2 — improved PRECEDED_BY/FAILED_CONTROL coverage + anti-tautology
SYSTEM_PROMPT_V2 = """You are a safety incident analyst extracting causal relationships from oil and gas safety incident reports at TechnipFMC.

TASK: Given an incident narrative and a list of pre-identified entities, extract causal edges supported by the text. Use the entity list as a starting point, but also extract entities and events described in the narrative even if they are not in the list.

RELATIONS (use exactly these strings):
- CAUSAL: one thing caused, led to, or contributed to another (source=cause, target=effect). Covers direct cause, consequence, and contributing factors. Look for: "due to", "caused by", "because of", "resulted in", "causing", "leading to", "contributed to", "was a factor"
- PRECEDED_BY: a temporal sequence with causal relevance — one event happened before and set the stage for another. Look for: "before", "prior to", "led to", "followed by", "then", "after", "earlier", "previously", "when", "during"
- FAILED_CONTROL: a safety barrier, procedure, or control that was supposed to prevent the incident but failed or was absent. Look for: "failed to", "did not prevent", "bypassed", "overridden", "inadequate", "missing", "not in place", "not functioning", "was not worn", "not followed"
- MITIGATED_BY: harm/event was prevented or reduced by a control or barrier (source=event, target=control). Look for: "prevented", "stopped", "contained", "caught", "PPE protected", "barrier held", "alarm alerted", "detected", "shut down", "isolated"

DIRECTION RULE: For CAUSAL edges, source is always the CAUSE and target is always the EFFECT.
- "fire due to corrosion" → source="corrosion", target="fire"
- "leak caused damage" → source="leak", target="damage"
- "rain contributed to slippery surface" → source="rain", target="slippery surface"

ENTITY TYPES (source and target must be one of these):
Incident, Event, Equipment, Location, Person, Injury, Material, Condition, Action

RULES:
1. Source and target should use descriptive phrases from the narrative (e.g., "short circuiting of wires for the heating element", not just "short circuit")
2. Avoid generic entities like "the worker", "the equipment", or "the incident" — use the specific name from the text
3. Evidence must be a phrase from the narrative (up to 25 words)
4. Extract ALL causal relationships you can find — most incident narratives contain at least one
5. Only return an empty list if the narrative has zero causal language (no "due to", "caused", "resulted", "failed", etc.)
6. Do not chain inferences: extract A→B and B→C separately, not A→C
7. Do not duplicate edges with different wording
8. Never create an edge where source and target describe the same event or concept. Each edge must connect two distinct entities.

EXAMPLES:
Narrative: "The pressure relief valve failed to open due to corrosion, causing a hydrocarbon release."
→ Condition("corrosion") CAUSAL Equipment("pressure relief valve failure") — evidence: "failed to open due to corrosion"
→ Equipment("pressure relief valve failure") CAUSAL Event("hydrocarbon release") — evidence: "causing a hydrocarbon release"

Narrative: "Fire started in electrical panel due to short circuiting of wires. The smoke detector in the room was not functioning."
→ Condition("short circuiting of wires") CAUSAL Event("fire") — evidence: "Fire started in electrical panel due to short circuiting of wires"
→ Event("fire") FAILED_CONTROL Equipment("smoke detector") — evidence: "smoke detector in the room was not functioning"

Narrative: "The crane operator moved the load before receiving the signal from the banksman. The load struck the scaffolding, and the safety net had been removed for maintenance."
→ Action("crane operator moved load before receiving signal") PRECEDED_BY Event("load struck scaffolding") — evidence: "moved the load before receiving the signal"
→ Action("crane operator moved load before receiving signal") CAUSAL Event("load struck scaffolding") — evidence: "The load struck the scaffolding"
→ Equipment("safety net") FAILED_CONTROL Event("load struck scaffolding") — evidence: "safety net had been removed for maintenance"

Narrative: "The gas leak was detected by the H2S monitor, which triggered the emergency shutdown and prevented any injuries."
→ Event("gas leak") MITIGATED_BY Equipment("H2S monitor") — evidence: "gas leak was detected by the H2S monitor"
→ Event("injuries") MITIGATED_BY Equipment("emergency shutdown") — evidence: "triggered the emergency shutdown and prevented any injuries"

Respond only with valid JSON. No explanation outside the JSON."""


USER_PROMPT_TEMPLATE_V2 = """NARRATIVE:
{narrative}

PRE-IDENTIFIED ENTITIES (use as source/target when relevant, but also extract new entities from the narrative):
{entity_block}

Extract all causal edges from this narrative. Look for temporal sequences (PRECEDED_BY), failed safety barriers (FAILED_CONTROL), and controls that worked (MITIGATED_BY), not just direct causes. Most incidents have 1-3 causal relationships."""


PROMPT_VARIANTS = {
    "full": SYSTEM_PROMPT,
    "full_v2": SYSTEM_PROMPT_V2,
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
        "source": "incorrect reinstallation",
        "source_type": "Condition",
        "relation": "CAUSAL",
        "target": "mechanical seal failure",
        "target_type": "Equipment",
        "evidence": "failed due to incorrect reinstallation by the maintenance crew",
    },
    {
        "source": "mechanical seal failure",
        "source_type": "Equipment",
        "relation": "CAUSAL",
        "target": "hydrocarbon leak",
        "target_type": "Event",
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
    {
        "source": "hydrocarbon leak",
        "source_type": "Event",
        "relation": "MITIGATED_BY",
        "target": "area gas detector",
        "target_type": "Equipment",
        "evidence": "area gas detector alarmed",
    },
]
