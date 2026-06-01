"""Tests for Ollama client parsing (no live server required)."""

import pytest

from app.ollama_client import parse_json_response


def test_parse_plain_json():
    assert parse_json_response('{"question": "hi"}') == {"question": "hi"}


def test_parse_json_embedded_in_text():
    raw = 'Here you go:\n{"delta": {"bitterness": 0.5}}\n'
    assert parse_json_response(raw)["delta"]["bitterness"] == 0.5


def test_parse_invalid_raises():
    with pytest.raises(Exception):
        parse_json_response("not json at all")
