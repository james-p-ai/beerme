"""Tests for prompt contracts."""

from app.prompts import BLURB_MAX_CHARS, BLURB_PROMPT


def test_blurb_max_chars_constant_is_positive():
    assert BLURB_MAX_CHARS > 0


def test_blurb_prompt_includes_max_length_constraint():
    assert str(BLURB_MAX_CHARS) in BLURB_PROMPT
    assert "printable export" in BLURB_PROMPT.lower()
