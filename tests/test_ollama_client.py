"""Tests for Ollama client parsing (no live server required)."""

from unittest.mock import patch

import pytest

from app.ollama_client import chat_json, parse_json_response


def test_parse_plain_json():
    assert parse_json_response('{"question": "hi"}') == {"question": "hi"}


def test_parse_json_embedded_in_text():
    raw = 'Here you go:\n{"delta": {"bitterness": 0.5}}\n'
    assert parse_json_response(raw)["delta"]["bitterness"] == 0.5


def test_parse_invalid_raises():
    with pytest.raises(Exception):
        parse_json_response("not json at all")


def test_chat_json_retries_on_invalid():
    calls: list[list[dict[str, str]]] = []

    def fake_chat(messages, *, model=None, timeout=120.0):
        calls.append([dict(m) for m in messages])
        if len(calls) == 1:
            return "not json"
        return '{"ok": true}'

    with patch("app.ollama_client.chat", side_effect=fake_chat):
        result = chat_json([{"role": "user", "content": "hi"}], retries=1)

    assert result == {"ok": True}
    assert len(calls) == 2
    assert calls[1][-1]["content"] == "Your last reply was invalid JSON. Reply with JSON only."
