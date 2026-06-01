"""Ollama HTTP client."""

from __future__ import annotations

import json
import os
import re
from typing import Any

import httpx

DEFAULT_HOST = "http://localhost:11434"
DEFAULT_MODEL = "llama3.2:3b"


def ollama_host() -> str:
    return os.environ.get("OLLAMA_HOST", DEFAULT_HOST).rstrip("/")


def ollama_model() -> str:
    return os.environ.get("OLLAMA_MODEL", DEFAULT_MODEL)


def is_available(timeout: float = 3.0) -> bool:
    try:
        r = httpx.get(f"{ollama_host()}/api/tags", timeout=timeout)
        return r.status_code == 200
    except (httpx.HTTPError, OSError):
        return False


def list_models(timeout: float = 5.0) -> list[str]:
    r = httpx.get(f"{ollama_host()}/api/tags", timeout=timeout)
    r.raise_for_status()
    data = r.json()
    return [m.get("name", "") for m in data.get("models", [])]


def chat(
    messages: list[dict[str, str]],
    *,
    model: str | None = None,
    timeout: float = 120.0,
) -> str:
    payload = {
        "model": model or ollama_model(),
        "messages": messages,
        "stream": False,
        "format": "json",
    }
    r = httpx.post(f"{ollama_host()}/api/chat", json=payload, timeout=timeout)
    r.raise_for_status()
    content = r.json().get("message", {}).get("content", "")
    return content if isinstance(content, str) else str(content)


def parse_json_response(text: str) -> dict[str, Any]:
    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{[\s\S]*\}", text)
        if match:
            return json.loads(match.group(0))
        raise


def chat_json(
    messages: list[dict[str, str]],
    *,
    retries: int = 1,
    model: str | None = None,
) -> dict[str, Any]:
    last_err: Exception | None = None
    for attempt in range(retries + 1):
        try:
            raw = chat(messages, model=model)
            return parse_json_response(raw)
        except (json.JSONDecodeError, httpx.HTTPError, KeyError) as e:
            last_err = e
            if attempt < retries:
                messages = messages + [
                    {"role": "user", "content": "Your last reply was invalid JSON. Reply with JSON only."}
                ]
    raise RuntimeError(f"Ollama JSON parse failed after {retries + 1} attempts") from last_err
