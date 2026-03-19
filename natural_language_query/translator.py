"""NL → QuerySpec translator.

Calls an LLM (Ollama local, Anthropic, or Gemini API) to convert a natural
language query into a structured NLQueryOutput, then bridges to QuerySpec.

Usage:
    from natural_language_query.translator import translate

    # Local Ollama (default)
    result = translate("How many forklift incidents in 2022?")

    # Anthropic API
    result = translate("How many forklift incidents in 2022?",
                       backend="anthropic", model="claude-sonnet-4-5-20250514")

    # Gemini API
    result = translate("How many forklift incidents in 2022?",
                       backend="gemini", model="gemini-2.5-flash")

    # Access the QuerySpec dict
    spec_dict = result["query_spec"]  # pass to QuerySpec(**spec_dict)
    confidence = result["confidence"]
    clarification = result["clarification"]
"""

from __future__ import annotations

import json
import os
import re
import time
from typing import Optional

from .prompt import SYSTEM_PROMPT, SYSTEM_PROMPT_OLLAMA_COMPACT, USER_PROMPT_TEMPLATE
from .schema import NLQueryOutput, to_query_spec


# ── LLM backends ─────────────────────────────────────────────────────────


def _call_ollama(
    query: str,
    model: str,
    base_url: str,
    temperature: float,
    system_prompt: str,
) -> str:
    """Call local Ollama endpoint."""
    import requests

    timeout_sec = int(os.environ.get("OLLAMA_TIMEOUT_SEC", "900"))
    payload = {
        "model": model,
        "prompt": USER_PROMPT_TEMPLATE.format(query=query),
        "system": system_prompt,
        "stream": False,
        "options": {
            "temperature": temperature,
            "num_predict": 256,
        },
    }

    # Try with format:"json" first; fall back without it for thinking models
    # (e.g. qwen3.5) that return empty responses with structured output mode.
    payload["format"] = "json"
    resp = requests.post(
        f"{base_url}/api/generate", json=payload, timeout=timeout_sec,
    )
    resp.raise_for_status()
    text = resp.json()["response"]
    if text.strip():
        return text

    # Retry without format constraint
    del payload["format"]
    resp = requests.post(
        f"{base_url}/api/generate", json=payload, timeout=timeout_sec,
    )
    resp.raise_for_status()
    return resp.json()["response"]


def _call_anthropic(query: str, model: str, temperature: float, system_prompt: str) -> str:
    """Call Anthropic Messages API."""
    import anthropic

    client = anthropic.Anthropic(
        api_key=os.environ.get("ANTHROPIC_API_KEY"),
    )

    message = client.messages.create(
        model=model,
        max_tokens=1024,
        temperature=temperature,
        system=system_prompt,
        messages=[
            {
                "role": "user",
                "content": USER_PROMPT_TEMPLATE.format(query=query),
            }
        ],
        # Ask Anthropic to return a single JSON object with no extra text
        response_format={"type": "json_object"},
    )
    return message.content[0].text


def _call_gemini(query: str, model: str, temperature: float, system_prompt: str) -> str:
    """Call Google Gemini API."""
    from google import genai

    client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))

    response = client.models.generate_content(
        model=model,
        contents=USER_PROMPT_TEMPLATE.format(query=query),
        config={
            "system_instruction": system_prompt,
            "temperature": temperature,
            "max_output_tokens": 1024,
            "response_mime_type": "application/json",
        },
    )
    return response.text


BACKENDS = {
    "ollama": _call_ollama,
    "anthropic": _call_anthropic,
    "gemini": _call_gemini,
}


# ── JSON parsing helpers ─────────────────────────────────────────────────


def _clean_json(raw: str) -> str:
    """Strip thinking tags, markdown fences, and leading/trailing junk."""
    # Remove <think>...</think> blocks (thinking models like qwen3.5)
    raw = re.sub(r"<think>.*?</think>", "", raw, flags=re.DOTALL)

    # Remove ```json ... ``` wrapping
    raw = re.sub(r"^```(?:json)?\s*", "", raw.strip())
    raw = re.sub(r"\s*```$", "", raw.strip())

    # Find the outermost { ... }
    start = raw.find("{")
    end = raw.rfind("}")
    if start != -1 and end != -1 and end > start:
        raw = raw[start : end + 1]

    return raw


def _normalize_for_schema(data: dict) -> dict:
    """Best-effort normalization to avoid hard failures on minor LLM slip-ups.

    This should only fix/drop obviously invalid values (e.g., empty relations),
    not invent semantics.
    """
    if not isinstance(data, dict):
        return data

    # Drop invalid/incomplete entity_filters entries rather than failing validation.
    efs = data.get("entity_filters")
    if isinstance(efs, list):
        entity_type_aliases = {
            # Natural-language aliases
            "CLIENT": "ORGANIZATION",
            "CUSTOMER": "ORGANIZATION",
            "COMPANY": "ORGANIZATION",
            "FIRM": "ORGANIZATION",
        }
        valid_entity_types = {
            "EQUIPMENT",
            "LOCATION",
            "BODY_PART",
            "INJURY_TYPE",
            "ROOT_CAUSE_CATEGORY",
            "ORGANIZATION",
            "INCIDENT",
        }
        valid_relations = {
            "INVOLVED",
            "OCCURRED_AT",
            "RESULTED_IN",
            "REPORTED_BY",
            "CATEGORIZED_AS",
            "AFFECTED",
            "LOCATED_IN",
        }

        cleaned_efs = []
        for ef in efs:
            if not isinstance(ef, dict):
                continue
            et = ef.get("entity_type")
            pat = ef.get("pattern")
            rel = ef.get("relation")
            if et is None or pat is None or rel is None:
                continue

            # Map common aliases (e.g., "client" -> ORGANIZATION)
            if isinstance(et, str):
                et_norm = et.strip().upper()
                et_norm = entity_type_aliases.get(et_norm, et_norm)
                if et_norm not in valid_entity_types:
                    # If it's not a known entity type, drop this filter.
                    continue
                ef["entity_type"] = et_norm

            if isinstance(rel, str) and not rel.strip():
                continue

            # Drop empty/invalid relation strings.
            if isinstance(rel, str):
                rel_norm = rel.strip().upper()
                if rel_norm not in valid_relations:
                    continue
                ef["relation"] = rel_norm

            cleaned_efs.append(ef)
        data["entity_filters"] = cleaned_efs

    # Drop invalid/incomplete meta_filters entries; map "=~" → "contains".
    mfs = data.get("meta_filters")
    if isinstance(mfs, list):
        valid_ops = {"==", "!=", ">", ">=", "<", "<=", "contains"}
        cleaned_mfs = []
        for mf in mfs:
            if not isinstance(mf, dict):
                continue
            field = mf.get("field")
            op = mf.get("op")
            value = mf.get("value")
            # Some models emit regex op; we only support contains for string match.
            if op == "=~":
                op = "contains"
            # Some models use a single '=' (common mistake) instead of '=='.
            if op == "=":
                op = "=="
            if field is None or op is None or value is None:
                continue
            if isinstance(op, str):
                op_norm = op.strip()
                if op_norm not in valid_ops:
                    continue
                mf["op"] = op_norm
            if isinstance(value, str):
                cleaned_mfs.append({"field": field, "op": op, "value": value})
            else:
                continue
        data["meta_filters"] = cleaned_mfs

    # Normalize crosstab_target: some small models emit it as a list or as
    # a different object shape. Since it's optional, we can safely drop it
    # when it's not a proper {row_field, col_field} object.
    ct = data.get("crosstab_target")
    if isinstance(ct, list):
        data["crosstab_target"] = None
    elif isinstance(ct, dict):
        if ct.get("row_field") is None or ct.get("col_field") is None:
            data["crosstab_target"] = None
        else:
            # Normalize key names if the model used different fields.
            # If it doesn't look right, drop it.
            if "row_field" not in ct or "col_field" not in ct:
                data["crosstab_target"] = None
            else:
                data["crosstab_target"] = {
                    "row_field": ct.get("row_field"),
                    "col_field": ct.get("col_field"),
                }

    # Normalize aggregate_target: if it's present but incomplete (nulls),
    # drop it. This avoids enum validation errors while keeping execution possible.
    at = data.get("aggregate_target")
    if isinstance(at, dict):
        if at.get("entity_type") is None or at.get("relation") is None:
            data["aggregate_target"] = None

    # If aggregate_target is present but relation missing/invalid, fill from entity_type.
    # This prevents frequent small-model mistakes (None/empty/unknown relation).
    at = data.get("aggregate_target")
    if isinstance(at, dict):
        et = at.get("entity_type")
        rel = at.get("relation")
        relation_by_entity_type = {
            "EQUIPMENT": "INVOLVED",
            "LOCATION": "OCCURRED_AT",
            "BODY_PART": "AFFECTED",
            "INJURY_TYPE": "RESULTED_IN",
            "ROOT_CAUSE_CATEGORY": "CATEGORIZED_AS",
            "ORGANIZATION": "REPORTED_BY",
            "INCIDENT": "INVOLVED",
        }
        if et in relation_by_entity_type and (rel is None or not str(rel).strip() or rel in {"HAS_INCIDENT", "INCIDENT_ID"}):
            at["relation"] = relation_by_entity_type[et]
            data["aggregate_target"] = at

    # Coerce confidence: some small models emit null.
    if "confidence" in data and data.get("confidence") is None:
        data["confidence"] = 0.9
    elif "confidence" in data:
        conf = data.get("confidence")
        # Accept numeric strings too.
        if isinstance(conf, str):
            try:
                data["confidence"] = float(conf)
            except ValueError:
                data["confidence"] = 0.9
        # If it's another non-null type, fallback.
        elif not isinstance(conf, (int, float)):
            data["confidence"] = 0.9

    return data


def _parse_and_validate(raw: str) -> NLQueryOutput:
    """Parse raw LLM output into validated NLQueryOutput."""
    cleaned = _clean_json(raw)

    # First, try strict JSON parsing
    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError:
        # Fallback: allow control characters like raw newlines inside strings.
        # This is not strictly valid JSON, but many LLMs emit it; Python can
        # still parse it with strict=False, which is good enough for schema validation.
        data = json.loads(cleaned, strict=False)

    if isinstance(data, dict):
        data = _normalize_for_schema(data)

    return NLQueryOutput.model_validate(data)


# ── Main translate function ──────────────────────────────────────────────


def translate(
    query: str,
    backend: str = "ollama",
    model: Optional[str] = None,
    base_url: str = "http://localhost:11434",
    temperature: float = 0.1,
    max_retries: int = 1,
    query_id: str = "NL-00",
) -> dict:
    """Translate a natural language query to a QuerySpec.

    Args:
        query: The natural language question.
        backend: "ollama", "anthropic", or "gemini".
        model: Model name. Defaults per backend:
               ollama="qwen3:8b", anthropic="claude-sonnet-4-5-20250514",
               gemini="gemini-2.5-flash".
        base_url: Ollama server URL (only used for ollama backend).
        temperature: LLM temperature (low = more deterministic).
        max_retries: Retries on parse failure (appends error to prompt).
        query_id: ID for the generated QuerySpec.

    Returns:
        dict with keys:
            query_spec: dict matching QuerySpec(**result) constructor
            nl_output: the validated NLQueryOutput object
            confidence: float 0-1
            clarification: str or None
            raw_response: the raw LLM text
            latency_ms: inference time in milliseconds
            backend: which backend was used
            model: which model was used
    """
    # Default models per backend
    default_models = {
        "ollama": "qwen3:8b",
        "anthropic": "claude-sonnet-4-5-20250514",
        "gemini": "gemini-2.5-flash",
    }
    if model is None:
        model = default_models.get(backend, "qwen3:8b")

    call_fn = BACKENDS[backend]
    # Use a compact system prompt for small local models to reduce timeouts and schema drift.
    system_prompt = SYSTEM_PROMPT
    if backend == "ollama" and any(s in (model or "").lower() for s in ("qwen2.5:3b", "3b")):
        system_prompt = SYSTEM_PROMPT_OLLAMA_COMPACT

    call_kwargs = {
        "query": query,
        "model": model,
        "temperature": temperature,
        "system_prompt": system_prompt,
    }
    if backend == "ollama":
        call_kwargs["base_url"] = base_url

    last_error = None
    raw_response = ""

    for attempt in range(1 + max_retries):
        t0 = time.time()

        # On retry, append the error to the query
        if attempt > 0 and last_error:
            call_kwargs["query"] = (
                f"{query}\n\n"
                f"[RETRY: Your previous response had a JSON error: "
                f"{last_error}. Please output ONLY valid JSON, with no text "
                f"before or after the JSON object, and escape any newlines "
                f"inside string values (use \\n).]"
            )

        try:
            raw_response = call_fn(**call_kwargs)
            latency_ms = (time.time() - t0) * 1000

            nl_output = _parse_and_validate(raw_response)

            spec_dict = to_query_spec(nl_output, query_id=query_id, name=query[:80])

            return {
                "query_spec": spec_dict,
                "nl_output": nl_output,
                "confidence": nl_output.confidence,
                "clarification": nl_output.clarification,
                "raw_response": raw_response,
                "latency_ms": latency_ms,
                "backend": backend,
                "model": model,
                "attempt": attempt + 1,
            }

        except json.JSONDecodeError as e:
            last_error = f"JSONDecodeError: {e}"
        except Exception as e:
            last_error = f"{type(e).__name__}: {e}"

    # All retries exhausted
    return {
        "query_spec": None,
        "nl_output": None,
        "confidence": 0.0,
        "clarification": f"Failed to parse LLM output after "
        f"{1 + max_retries} attempts: {last_error}",
        "raw_response": raw_response,
        "latency_ms": 0,
        "backend": backend,
        "model": model,
        "attempt": 1 + max_retries,
    }
