"""vLLM OpenAI-compatible client for Layer 2 causal enrichment.

Drop-in replacement for ollama_client.call_ollama(). Uses vLLM's
OpenAI-compatible /v1/chat/completions endpoint with structured output
(guided JSON decoding) for the same grammar-constrained generation.

Start vLLM server before running:
    python -m vllm.entrypoints.openai.api_server \
        --model Qwen/Qwen3-30B-A3B \
        --max-model-len 4096 \
        --gpu-memory-utilization 0.90 \
        --enable-reasoning --reasoning-parser qwen3 \
        --port 8000
"""
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
    start = text.find("{")
    end = text.rfind("}")
    if start >= 0 and end > start:
        try:
            return json.loads(text[start : end + 1])
        except Exception:
            return None
    return None


def call_vllm(
    prompt: str,
    system: str,
    model: str = "Qwen/Qwen3-30B-A3B",
    host: str = "http://127.0.0.1:8000",
    schema: Optional[Dict[str, Any]] = None,
    temperature: float = 0.1,
    timeout_sec: int = 300,
    max_retries: int = 2,
    backoff_base: float = 2.0,
) -> dict:
    """Call vLLM's OpenAI-compatible /v1/chat/completions endpoint.

    Same signature as call_ollama() so it can be swapped in directly.
    Uses ``response_format`` for grammar-constrained JSON decoding when
    ``schema`` is provided.

    Raises ``RuntimeError`` after exhausting retries.
    """
    url = host.rstrip("/") + "/v1/chat/completions"
    payload: Dict[str, Any] = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
        "stream": False,
        "temperature": temperature,
        "max_tokens": 2048,
    }
    if schema is not None:
        payload["response_format"] = {
            "type": "json_schema",
            "json_schema": {
                "name": "causal_extraction",
                "schema": schema,
                "strict": True,
            },
        }

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
                # OpenAI format: choices[0].message.content
                content = (
                    parsed.get("choices", [{}])[0]
                    .get("message", {})
                    .get("content", "")
                )
                result = _extract_json_block(content)
                if result is not None:
                    return result
                last_error = ValueError(
                    f"Could not parse JSON from model output: {content[:200]}"
                )
        except (
            urllib.error.URLError,
            urllib.error.HTTPError,
            TimeoutError,
            json.JSONDecodeError,
            IndexError,
        ) as exc:
            last_error = exc

    raise RuntimeError(
        f"vLLM call failed after {max_retries + 1} attempts: {last_error}"
    )
