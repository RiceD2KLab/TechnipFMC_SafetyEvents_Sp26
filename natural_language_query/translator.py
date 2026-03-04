"""NL → QuerySpec translator.

Calls an LLM (Ollama local, Anthropic, or Gemini API) to convert a natural
language query into a structured NLQueryOutput, then bridges to QuerySpec.

Usage:
    from nl_query.translator import translate

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

from .prompt import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE
from .schema import NLQueryOutput, to_query_spec


# ── LLM backends ─────────────────────────────────────────────────────────


def _call_ollama(query: str, model: str, base_url: str, temperature: float) -> str:
    """Call local Ollama endpoint."""
    import requests

    payload = {
        "model": model,
        "prompt": USER_PROMPT_TEMPLATE.format(query=query),
        "system": SYSTEM_PROMPT,
        "stream": False,
        "options": {
            "temperature": temperature,
            "num_predict": 1024,
        },
    }

    # Try with format:"json" first; fall back without it for thinking models
    # (e.g. qwen3.5) that return empty responses with structured output mode.
    payload["format"] = "json"
    resp = requests.post(
        f"{base_url}/api/generate", json=payload, timeout=120,
    )
    resp.raise_for_status()
    text = resp.json()["response"]
    if text.strip():
        return text

    # Retry without format constraint
    del payload["format"]
    resp = requests.post(
        f"{base_url}/api/generate", json=payload, timeout=120,
    )
    resp.raise_for_status()
    return resp.json()["response"]


def _call_anthropic(query: str, model: str, temperature: float) -> str:
    """Call Anthropic Messages API."""
    import anthropic

    client = anthropic.Anthropic(
        api_key=os.environ.get("ANTHROPIC_API_KEY"),
    )

    message = client.messages.create(
        model=model,
        max_tokens=1024,
        temperature=temperature,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": USER_PROMPT_TEMPLATE.format(query=query),
            }
        ],
    )
    return message.content[0].text


def _call_gemini(query: str, model: str, temperature: float) -> str:
    """Call Google Gemini API."""
    from google import genai

    client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))

    response = client.models.generate_content(
        model=model,
        contents=USER_PROMPT_TEMPLATE.format(query=query),
        config={
            "system_instruction": SYSTEM_PROMPT,
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


def _parse_and_validate(raw: str) -> NLQueryOutput:
    """Parse raw LLM output into validated NLQueryOutput."""
    cleaned = _clean_json(raw)
    data = json.loads(cleaned)
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
    call_kwargs = {"query": query, "model": model, "temperature": temperature}
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
                f"{last_error}. Please output ONLY valid JSON.]"
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
