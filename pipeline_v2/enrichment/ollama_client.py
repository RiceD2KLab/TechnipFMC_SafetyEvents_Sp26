"""Ollama HTTP client for Layer 2 causal enrichment."""
from __future__ import annotations

import json
import time
import urllib.error
import urllib.request
from typing import Any, Dict, Optional


def _extract_json_block(text: str) -> Optional[dict]:
    """Try to parse JSON from raw LLM output, handling markdown fences."""
    text = text.strip()
    try:
        return json.loads(text)
    except Exception:
        pass
    # Try extracting from markdown code fence or raw braces
    start = text.find("{")
    end = text.rfind("}")
    if start >= 0 and end > start:
        try:
            return json.loads(text[start : end + 1])
        except Exception:
            return None
    return None


def call_ollama(
    prompt: str,
    system: str,
    model: str = "qwen3:8b",
    host: str = "http://127.0.0.1:11434",
    schema: Optional[Dict[str, Any]] = None,
    temperature: float = 0.1,
    timeout_sec: int = 120,
    max_retries: int = 2,
    backoff_base: float = 2.0,
) -> dict:
    """Call Ollama's /api/chat endpoint and return parsed JSON.

    Uses the ``format`` parameter for grammar-constrained JSON decoding when
    ``schema`` is provided.

    Raises ``RuntimeError`` after exhausting retries.
    """
    url = host.rstrip("/") + "/api/chat"
    payload: Dict[str, Any] = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
        "stream": False,
        "options": {"temperature": temperature},
    }
    if schema is not None:
        payload["format"] = schema

    last_error: Optional[Exception] = None
    for attempt in range(max_retries + 1):
        if attempt > 0:
            time.sleep(backoff_base ** attempt)
        request = urllib.request.Request(
            url=url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=timeout_sec) as response:
                raw = response.read().decode("utf-8")
                parsed = json.loads(raw)
                # /api/chat returns message.content
                content = parsed.get("message", {}).get("content", "")
                result = _extract_json_block(content)
                if result is not None:
                    return result
                last_error = ValueError(f"Could not parse JSON from model output: {content[:200]}")
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, json.JSONDecodeError) as exc:
            last_error = exc

    raise RuntimeError(
        f"Ollama call failed after {max_retries + 1} attempts: {last_error}"
    )
