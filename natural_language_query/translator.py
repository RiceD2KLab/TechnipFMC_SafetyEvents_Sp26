"""NL → QuerySpec translator.

Calls an LLM (Ollama local, Anthropic, Gemini, or Amazon Bedrock) to convert a natural
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

    # Amazon Bedrock (set AWS_BEARER_TOKEN_BEDROCK or IAM credentials + region)
    result = translate(
        "How many forklift incidents in 2022?",
        backend="bedrock",
        model="us.anthropic.claude-haiku-4-5-20251001-v1:0",
    )

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
from pathlib import Path
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

    # content blocks match the Messages API; stubs omit some kwargs (response_format).
    message = client.messages.create(
        model=model,
        max_tokens=1024,
        temperature=temperature,
        system=system_prompt,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": USER_PROMPT_TEMPLATE.format(query=query)},
                ],
            }
        ],
        response_format={"type": "json_object"},
    )  # type: ignore[call-overload]
    return message.content[0].text


def _call_gemini(query: str, model: str, temperature: float, system_prompt: str) -> str:
    """Call Google Gemini API (``google-genai`` package; module ``google.genai``)."""
    import importlib

    genai = importlib.import_module("google.genai")
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


def _load_nl_query_dotenv() -> None:
    """Load ``natural_language_query/.env`` so Bedrock works from any entry point.

    Only ``eval_harness_bedrock`` used to call ``load_dotenv``; using
    ``eval_harness --backend bedrock``, Streamlit, or ``translate()`` directly
    never loaded ``.env``, which produces NoCredentialsError even when the file
    exists.
    """
    try:
        from dotenv import load_dotenv  # type: ignore[import-untyped]
    except ImportError:
        return
    env_path = Path(__file__).resolve().parent / ".env"
    if env_path.is_file():
        load_dotenv(env_path)


def _ensure_bedrock_bearer_token() -> None:
    """Map custom env name to the variable boto3 expects for Bedrock API keys."""
    if os.environ.get("AWS_BEARER_TOKEN_BEDROCK"):
        return
    legacy = os.environ.get("AWS_BEDROCK_KEY")
    if legacy:
        os.environ["AWS_BEARER_TOKEN_BEDROCK"] = legacy


def _bedrock_converse_via_http_bearer(
    region: str,
    model: str,
    bearer: str,
    user_text: str,
    system_prompt: str,
    temperature: float,
) -> dict:
    """Call Converse with ``Authorization: Bearer`` (AWS-documented path).

    Some boto3/botocore builds still raise ``NoCredentialsError`` for
    ``bedrock-runtime`` even when ``AWS_BEARER_TOKEN_BEDROCK`` is set; HTTP
    avoids the SigV4 credential chain entirely.
    """
    import requests
    from urllib.parse import quote

    model_path = quote(model, safe=":/.-")
    url = (
        f"https://bedrock-runtime.{region}.amazonaws.com/"
        f"model/{model_path}/converse"
    )
    payload = {
        "messages": [
            {
                "role": "user",
                "content": [{"text": user_text}],
            },
        ],
        "system": [{"text": system_prompt}],
        # Many Bedrock models reject requests that set both temperature and topP.
        "inferenceConfig": {
            "maxTokens": 1024,
            "temperature": temperature,
        },
    }
    timeout_sec = int(os.environ.get("BEDROCK_TIMEOUT_SEC", "120"))
    resp = requests.post(
        url,
        json=payload,
        headers={
            "Authorization": f"Bearer {bearer}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        timeout=timeout_sec,
    )
    if resp.status_code >= 400:
        try:
            body = resp.json()
            msg = body.get("message", body)
        except Exception:
            msg = (resp.text or "")[:500]
        raise RuntimeError(f"Bedrock HTTP {resp.status_code}: {msg}")
    return resp.json()


def _bedrock_collect_text_from_content(content: list) -> str:
    """Join all plain-text segments from a Converse ``content`` array.

    Models may return multiple blocks (e.g. reasoning then text); older code
    only read ``content[0]``, which can be empty non-text blocks.
    """
    if not content:
        return ""
    parts = []
    for block in content:
        if not isinstance(block, dict):
            continue
        if block.get("text"):
            parts.append(block["text"])
    return "".join(parts)


def _call_bedrock(
    query: str,
    model: str,
    temperature: float,
    system_prompt: str,
) -> str:
    """Call Amazon Bedrock Runtime (Converse API).

    Auth (pick one):
    - Bedrock API key: set ``AWS_BEARER_TOKEN_BEDROCK`` (or ``AWS_BEDROCK_KEY`` as alias).
      Uses the REST Converse API with a Bearer header (reliable across boto3 versions).
    - IAM: ``AWS_ACCESS_KEY_ID`` / ``AWS_SECRET_ACCESS_KEY`` (and optional session token)
      uses boto3/SigV4.

    Region: ``AWS_REGION`` or ``AWS_DEFAULT_REGION`` (defaults to us-east-1 if unset).
    """
    import boto3
    from botocore.exceptions import ClientError

    _load_nl_query_dotenv()
    _ensure_bedrock_bearer_token()
    _tok = os.environ.get("AWS_BEARER_TOKEN_BEDROCK")
    if _tok:
        os.environ["AWS_BEARER_TOKEN_BEDROCK"] = _tok.strip()

    region = (
        os.environ.get("AWS_REGION")
        or os.environ.get("AWS_DEFAULT_REGION")
        or "us-east-1"
    )

    bearer = (os.environ.get("AWS_BEARER_TOKEN_BEDROCK") or "").strip()
    has_iam = bool(
        os.environ.get("AWS_ACCESS_KEY_ID")
        and os.environ.get("AWS_SECRET_ACCESS_KEY")
    )
    if not bearer and not has_iam:
        env_path = Path(__file__).resolve().parent / ".env"
        raise RuntimeError(
            "Bedrock: no credentials in the process environment. "
            f"Expected AWS_BEARER_TOKEN_BEDROCK (or IAM keys) after loading {env_path}. "
            "Install python-dotenv, put variables in that file, and retry — or export them "
            "in the shell before running Python."
        )

    user_text = USER_PROMPT_TEMPLATE.format(query=query)

    if bearer:
        response = _bedrock_converse_via_http_bearer(
            region=region,
            model=model,
            bearer=bearer,
            user_text=user_text,
            system_prompt=system_prompt,
            temperature=temperature,
        )
    else:
        client = boto3.client("bedrock-runtime", region_name=region)
        try:
            response = client.converse(
                modelId=model,
                messages=[
                    {
                        "role": "user",
                        "content": [{"text": user_text}],
                    },
                ],
                system=[{"text": system_prompt}],
                inferenceConfig={
                    "maxTokens": 1024,
                    "temperature": temperature,
                },
            )
        except ClientError as e:
            err = e.response.get("Error") or {}
            code = err.get("Code", type(e).__name__)
            msg = err.get("Message", str(e))
            raise RuntimeError(f"Bedrock Converse failed ({code}): {msg}") from e

    blocks = (
        response.get("output", {})
        .get("message", {})
        .get("content", [])
    )
    text = _bedrock_collect_text_from_content(blocks)
    if not text.strip():
        stop = response.get("stopReason", "?")
        raise RuntimeError(
            f"Bedrock returned no text (stopReason={stop!r}). "
            f"Check modelId matches this region/account, and model access is enabled in the console."
        )
    return text


BACKENDS = {
    "ollama": _call_ollama,
    "anthropic": _call_anthropic,
    "gemini": _call_gemini,
    "bedrock": _call_bedrock,
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
        backend: "ollama", "anthropic", "gemini", or "bedrock".
        model: Model name. Defaults per backend:
               ollama="qwen3:8b", anthropic="claude-sonnet-4-5-20250514",
               gemini="gemini-2.5-flash",
               bedrock="us.anthropic.claude-haiku-4-5-20251001-v1:0".
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
        # US cross-region inference profile (on-demand base id is rejected for Converse).
        "bedrock": "us.anthropic.claude-haiku-4-5-20251001-v1:0",
    }
    if model is None:
        model = default_models.get(backend, "qwen3:8b")

    call_fn = BACKENDS[backend]
    # Use a compact system prompt for small local models to reduce timeouts and schema drift.
    system_prompt = SYSTEM_PROMPT
    if backend == "ollama" and any(s in (model or "").lower() for s in ("qwen2.5:3b", "3b")):
        system_prompt = SYSTEM_PROMPT_OLLAMA_COMPACT
    if backend == "bedrock":
        system_prompt = (
            system_prompt
            + "\n\n## JSON OUTPUT (required)\n"
            "Return exactly one JSON object. Start with `{`. Do not use markdown code fences. "
            "Include every top-level field the NLQueryOutput schema expects (use null only where allowed)."
        )

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
