#!/usr/bin/env python3
"""
Annotate 200 selected records for Layer 2 causal ground truth.

Reads annotation_template.csv, produces causal annotations via one of three backends:
  - regex: sentence-level pattern matching (fast, no GPU, ~268 edges)
  - ollama: local LLM via Ollama (requires GPU + model)
  - mock: empty annotations for dry-run testing

Outputs:
  - annotation_llm.csv (filled annotation template)
  - l2_ground_truth.jsonl (Gate 3 compatible edge format)

Usage:
    python pipeline_v2/annotation/annotate_with_llm.py --backend regex
    python pipeline_v2/annotation/annotate_with_llm.py --backend ollama --model qwen3:8b
    python pipeline_v2/annotation/annotate_with_llm.py --backend mock
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR.parent))

from enrichment.ollama_client import call_ollama

# ── LLM Annotation Prompt ──────────────────────────────────────────────

ANNOTATION_SYSTEM_PROMPT = """You are an expert safety incident analyst annotating causal relationships in oil and gas incident reports for TechnipFMC.

Given an incident narrative and a list of pre-extracted entities, identify:

1. CAUSED_BY: The direct, proximate trigger(s) of the incident. Without this, the incident would not have occurred. Maximum 2.
2. CONTRIBUTED_TO: Background conditions or enabling factors that made the incident possible or worse (e.g., missing PPE, inadequate training, environmental conditions). Maximum 2.
3. LED_TO: Step-by-step causal chain within the incident (event -> outcome pairs). Maximum 3 steps.

RULES:
- Only annotate what the narrative explicitly states. Do not infer from metadata.
- Evidence must be a verbatim quote from the narrative (exact substring).
- Confidence: HIGH = explicit causal language ("caused by", "due to", "resulted in"), MEDIUM = strongly implied, LOW = ambiguous.
- If no causal relationship is present, return empty arrays.
- Do NOT paraphrase evidence -- copy exact text from the narrative.
- Prefer fewer, high-confidence annotations over many speculative ones.

Return JSON with this structure:
{
  "caused_by": [{"cause": str, "evidence": str, "confidence": "HIGH"|"MEDIUM"|"LOW"}],
  "contributed_to": [{"factor": str, "evidence": str, "confidence": "HIGH"|"MEDIUM"|"LOW"}],
  "led_to": [{"event": str, "outcome": str, "evidence": str, "confidence": "HIGH"|"MEDIUM"|"LOW"}]
}"""

ANNOTATION_USER_TEMPLATE = """NARRATIVE:
{narrative}

EXISTING ENTITIES:
{entities}

Annotate causal relationships from this narrative."""

ANNOTATION_SCHEMA = {
    "type": "object",
    "required": ["caused_by", "contributed_to", "led_to"],
    "properties": {
        "caused_by": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["cause", "evidence", "confidence"],
                "properties": {
                    "cause": {"type": "string"},
                    "evidence": {"type": "string"},
                    "confidence": {"type": "string", "enum": ["HIGH", "MEDIUM", "LOW"]},
                },
            },
        },
        "contributed_to": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["factor", "evidence", "confidence"],
                "properties": {
                    "factor": {"type": "string"},
                    "evidence": {"type": "string"},
                    "confidence": {"type": "string", "enum": ["HIGH", "MEDIUM", "LOW"]},
                },
            },
        },
        "led_to": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["event", "outcome", "evidence", "confidence"],
                "properties": {
                    "event": {"type": "string"},
                    "outcome": {"type": "string"},
                    "evidence": {"type": "string"},
                    "confidence": {"type": "string", "enum": ["HIGH", "MEDIUM", "LOW"]},
                },
            },
        },
    },
    "additionalProperties": False,
}

# ── Regex Annotation Backend ───────────────────────────────────────────

NEGATION_PHRASES = [
    "no injury", "no injuries", "no damage", "no material", "no one was",
    "no flame", "no fire", "fortunately", "no loss", "no harm",
    "there were no", "there was no", "without any injury", "without injury",
]

CIRCULAR_CAUSES = {"the incident", "incident", "the event", "this", "it"}


def _split_sentences(text: str) -> list[str]:
    parts = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in parts if s.strip() and len(s.strip()) > 5]


def _is_valid_sentence(sent: str) -> bool:
    sent_lower = sent.lower()
    if re.match(r'^(no\s+(injury|injuries|damage|one|person|material|fire|spill|environmental|flame|loss)|there\s+(were|was)\s+no|fortunately|luckily|no\s+loss)', sent_lower):
        return False
    for phrase in NEGATION_PHRASES:
        if phrase in sent_lower:
            return False
    return True


def _is_valid_cause(cause: str) -> bool:
    return cause.strip().lower() not in CIRCULAR_CAUSES and len(cause.strip()) > 3


def _truncate(text: str, max_words: int = 12) -> str:
    words = text.split()
    return ' '.join(words[:max_words]) if len(words) > max_words else text


def _try_extract(sentence: str, pattern: re.Pattern, extract_type: str) -> dict | None:
    m = pattern.search(sentence)
    if not m:
        return None
    groups = m.groups()
    if extract_type == "cause" and len(groups) >= 2:
        cause = groups[1].strip().rstrip('.')
        if not _is_valid_cause(cause):
            return None
        return {"type": "CAUSED_BY", "cause": _truncate(cause), "evidence": sentence}
    if extract_type == "chain" and len(groups) >= 2:
        event = groups[0].strip().rstrip(',')
        outcome = groups[1].strip().rstrip('.')
        return {"type": "LED_TO", "event": _truncate(event), "outcome": _truncate(outcome), "evidence": sentence}
    if extract_type == "contrib":
        factor = groups[0].strip().split('.')[0].split(',')[0].strip() if groups else sentence
        if not _is_valid_cause(factor):
            return None
        return {"type": "CONTRIBUTED_TO", "factor": _truncate(factor), "evidence": sentence}
    return None


# Cause patterns: X due to Y, X caused by Y, X because (of) Y, X as a result of Y
_CAUSE_PATTERNS = [
    (re.compile(r'(.+?)\s+due to\s+(.+)', re.I), "cause"),
    (re.compile(r'(.+?)\s+(?:was |were |been )?caused by\s+(.+)', re.I), "cause"),
    (re.compile(r'(.+?)\s+because\s+(?:of\s+)?(.+)', re.I), "cause"),
    (re.compile(r'(.+?)\s+as a result of\s+(.+)', re.I), "cause"),
    (re.compile(r'(.+?)\s+(?:was |were )?attributed to\s+(.+)', re.I), "cause"),
]

# Chain patterns: X resulting in Y, X causing Y, X led to Y
_CHAIN_PATTERNS = [
    (re.compile(r'(.+?),?\s+result(?:ing|ed)\s+in\s+(.+)', re.I), "chain"),
    (re.compile(r'(.+?),?\s+lead?(?:ing)?\s+to\s+(.+)', re.I), "chain"),
]

# Contrib patterns: failed to, inadequate, lack of, etc.
_CONTRIB_PATTERNS = [
    (re.compile(r'(.+?)\s+(?:failed to|did not|was not|were not|had not been)\s+(.+)', re.I), "contrib"),
    (re.compile(r'(inadequate|lack of|improper|poor|without|missing|absence of)\s*(.{5,60})', re.I), "contrib"),
]


def _regex_annotate(narrative: str) -> dict:
    """Sentence-level regex causal extraction."""
    if not narrative or len(narrative) < 20:
        return {"caused_by": [], "contributed_to": [], "led_to": []}

    sentences = [s for s in _split_sentences(narrative) if _is_valid_sentence(s)]
    caused_by, led_to, contributed_to = [], [], []
    used: set[str] = set()

    # Pass 1: CAUSED_BY
    for sent in sentences:
        if sent in used:
            continue
        for pattern, ptype in _CAUSE_PATTERNS:
            # Skip "X causing Y" overlap — that's a chain pattern
            if 'caused by' not in sent.lower() and 'due to' not in sent.lower() and \
               'because' not in sent.lower() and 'as a result of' not in sent.lower() and \
               'attributed to' not in sent.lower():
                continue
            result = _try_extract(sent, pattern, ptype)
            if result:
                caused_by.append({"cause": result["cause"], "evidence": result["evidence"], "confidence": "HIGH"})
                used.add(sent)
                break

    # Pass 2: LED_TO chains
    for sent in sentences:
        if sent in used:
            continue
        for pattern, ptype in _CHAIN_PATTERNS:
            result = _try_extract(sent, pattern, ptype)
            if result:
                led_to.append({"event": result["event"], "outcome": result["outcome"],
                               "evidence": result["evidence"], "confidence": "HIGH"})
                used.add(sent)
                break
        # Also catch "X causing Y" (not "caused by")
        if sent not in used:
            m = re.search(r'(.+?),?\s+(?:which )?caus(?:ing|ed)\s+(.+)', sent, re.I)
            if m and 'caused by' not in sent.lower():
                event = _truncate(m.group(1).strip().rstrip(','))
                outcome = _truncate(m.group(2).strip().rstrip('.'))
                led_to.append({"event": event, "outcome": outcome, "evidence": sent, "confidence": "HIGH"})
                used.add(sent)

    # Pass 3: CONTRIBUTED_TO
    for sent in sentences:
        if sent in used:
            continue
        # Skip sentences about no injury/damage for failed-control patterns
        if any(skip in sent.lower() for skip in ['there were no', 'there was no damage', 'no injuries']):
            continue
        for pattern, ptype in _CONTRIB_PATTERNS:
            result = _try_extract(sent, pattern, ptype)
            if result:
                contributed_to.append({"factor": result["factor"], "evidence": result["evidence"],
                                       "confidence": "MEDIUM"})
                used.add(sent)
                break

    return {"caused_by": caused_by[:2], "contributed_to": contributed_to[:2], "led_to": led_to[:3]}


# ── Common Helpers ─────────────────────────────────────────────────────

def _clean_narrative(text: str) -> str:
    text = text.replace("_x000D_", " ").replace("\r\n", " ").replace("\r", " ")
    return re.sub(r'\s+', ' ', text).strip()


def _format_entities(entities_json: str) -> str:
    try:
        entities = json.loads(entities_json)
    except (json.JSONDecodeError, TypeError):
        return "(no entities)"
    lines = [f"- {e.get('entity_type', '')}: {e.get('value', '')}" for e in entities]
    return "\n".join(lines) if lines else "(no entities)"


def _annotation_to_l2_edges(record_no: str, annotation: dict, narrative: str) -> list[dict]:
    """Convert annotation format to L2 causal_edges format for Gate 3."""
    narrative_lower = narrative.lower()
    edges = []

    for cb in annotation.get("caused_by", []):
        evidence = cb.get("evidence", "")
        if evidence and evidence.lower() in narrative_lower:
            edges.append({
                "record_no": record_no,
                "source": cb["cause"],
                "source_type": "Condition",
                "relation": "CAUSED_BY",
                "target": "incident",
                "target_type": "Incident",
                "evidence": evidence,
            })

    for ct in annotation.get("contributed_to", []):
        evidence = ct.get("evidence", "")
        if evidence and evidence.lower() in narrative_lower:
            edges.append({
                "record_no": record_no,
                "source": ct["factor"],
                "source_type": "Condition",
                "relation": "CONTRIBUTED_TO",
                "target": "incident",
                "target_type": "Incident",
                "evidence": evidence,
            })

    for lt in annotation.get("led_to", []):
        evidence = lt.get("evidence", "")
        if evidence and evidence.lower() in narrative_lower:
            edges.append({
                "record_no": record_no,
                "source": lt["event"],
                "source_type": "Event",
                "relation": "RESULTED_IN",
                "target": lt["outcome"],
                "target_type": "Event",
                "evidence": evidence,
            })

    return edges


def _fill_template_row(row: dict, annotation: dict, annotator_id: str) -> None:
    """Fill annotation template columns from annotation dict."""
    caused_by = annotation.get("caused_by", [])
    contributed_to = annotation.get("contributed_to", [])
    led_to = annotation.get("led_to", [])

    if caused_by:
        row["caused_by_1_cause"] = caused_by[0].get("cause", "")
        row["caused_by_1_evidence"] = caused_by[0].get("evidence", "")
        row["caused_by_1_confidence"] = caused_by[0].get("confidence", "")
    if len(caused_by) > 1:
        row["caused_by_2_cause"] = caused_by[1].get("cause", "")
        row["caused_by_2_evidence"] = caused_by[1].get("evidence", "")
        row["caused_by_2_confidence"] = caused_by[1].get("confidence", "")

    if contributed_to:
        row["contributed_to_1_factor"] = contributed_to[0].get("factor", "")
        row["contributed_to_1_evidence"] = contributed_to[0].get("evidence", "")
        row["contributed_to_1_confidence"] = contributed_to[0].get("confidence", "")
    if len(contributed_to) > 1:
        row["contributed_to_2_factor"] = contributed_to[1].get("factor", "")
        row["contributed_to_2_evidence"] = contributed_to[1].get("evidence", "")
        row["contributed_to_2_confidence"] = contributed_to[1].get("confidence", "")

    for j, lt in enumerate(led_to[:3], start=1):
        row[f"led_to_{j}_event"] = lt.get("event", "")
        row[f"led_to_{j}_outcome"] = lt.get("outcome", "")
        row[f"led_to_{j}_evidence"] = lt.get("evidence", "")
        row[f"led_to_{j}_confidence"] = lt.get("confidence", "")

    row["annotator_id"] = annotator_id


# ── Main ───────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description="Annotate selected records for L2 causal ground truth")
    parser.add_argument("--backend", choices=["ollama", "regex", "mock"], default="regex")
    parser.add_argument("--model", default="qwen3:8b")
    parser.add_argument("--host", default="http://127.0.0.1:11434")
    parser.add_argument("--temperature", type=float, default=0.1)
    parser.add_argument("--output-dir", default=str(SCRIPT_DIR))
    args = parser.parse_args()

    template_path = SCRIPT_DIR / "annotation_template.csv"
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    annotation_csv_path = output_dir / "annotation_llm.csv"
    gt_jsonl_path = output_dir / "l2_ground_truth.jsonl"

    with template_path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    print(f"Processing {len(rows)} records with backend={args.backend}...")

    annotator_id = {
        "regex": "regex-v1",
        "ollama": f"llm:{args.model}",
        "mock": "mock",
    }[args.backend]

    all_gt_edges: list[dict] = []
    annotated_rows: list[dict] = []
    stats = {"total": 0, "with_cause": 0, "with_chain": 0, "with_contrib": 0, "empty": 0, "errors": 0}

    for i, row in enumerate(rows):
        record_no = row["record_no"]
        narrative = _clean_narrative(row.get("narrative", ""))
        entities_raw = row.get("existing_entities", "")
        stats["total"] += 1

        if not narrative.strip():
            annotated_rows.append(row)
            stats["empty"] += 1
            continue

        try:
            if args.backend == "mock":
                annotation = {"caused_by": [], "contributed_to": [], "led_to": []}
            elif args.backend == "regex":
                annotation = _regex_annotate(narrative)
            else:
                user_prompt = ANNOTATION_USER_TEMPLATE.format(
                    narrative=narrative,
                    entities=_format_entities(entities_raw),
                )
                annotation = call_ollama(
                    prompt=user_prompt,
                    system=ANNOTATION_SYSTEM_PROMPT,
                    model=args.model,
                    host=args.host,
                    schema=ANNOTATION_SCHEMA,
                    temperature=args.temperature,
                    timeout_sec=180,
                    max_retries=2,
                )
        except Exception as exc:
            print(f"  [{i+1}/{len(rows)}] ERROR record {record_no}: {exc}")
            annotated_rows.append(row)
            stats["errors"] += 1
            continue

        _fill_template_row(row, annotation, annotator_id)
        annotated_rows.append(row)

        gt_edges = _annotation_to_l2_edges(record_no, annotation, narrative)
        all_gt_edges.extend(gt_edges)

        caused_by = annotation.get("caused_by", [])
        contributed_to = annotation.get("contributed_to", [])
        led_to = annotation.get("led_to", [])
        if caused_by:
            stats["with_cause"] += 1
        if led_to:
            stats["with_chain"] += 1
        if contributed_to:
            stats["with_contrib"] += 1
        if not any([caused_by, contributed_to, led_to]):
            stats["empty"] += 1

        if (i + 1) % 50 == 0:
            print(f"  [{i+1}/{len(rows)}] {stats['with_cause']} causes, {stats['with_chain']} chains so far")

    # Write outputs
    with annotation_csv_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(annotated_rows)

    with gt_jsonl_path.open("w", encoding="utf-8") as f:
        for edge in all_gt_edges:
            f.write(json.dumps(edge, ensure_ascii=True) + "\n")

    print(f"\nResults:")
    print(f"  Total: {stats['total']}")
    print(f"  CAUSED_BY: {stats['with_cause']} ({stats['with_cause']*100//max(stats['total'],1)}%)")
    print(f"  CONTRIBUTED_TO: {stats['with_contrib']} ({stats['with_contrib']*100//max(stats['total'],1)}%)")
    print(f"  LED_TO chain: {stats['with_chain']} ({stats['with_chain']*100//max(stats['total'],1)}%)")
    print(f"  Empty: {stats['empty']} ({stats['empty']*100//max(stats['total'],1)}%)")
    print(f"  Errors: {stats['errors']}")
    print(f"  Ground truth edges: {len(all_gt_edges)}")
    print(f"\nOutputs:")
    print(f"  {annotation_csv_path}")
    print(f"  {gt_jsonl_path}")


if __name__ == "__main__":
    main()
