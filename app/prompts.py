"""Ollama system prompts and JSON shapes."""

SYSTEM_BASE = """You help BeerMe learn a user's beer taste. Respond with JSON only, no markdown.
Taste axes (0-1): bitterness, sweetness, body, roast, fruit, sour, hoppy, malt, abv_preference, crispness."""

NEXT_QUESTION_PROMPT = SYSTEM_BASE + """
Given the profile JSON and conversation history, output:
{"question": "...", "targets_axes": ["bitterness"], "choices": ["option A", "option B"]}
choices is optional. Ask one clear question."""

EXTRACT_PROMPT = SYSTEM_BASE + """
Given the user's latest answer and profile, output preference deltas:
{"delta": {"bitterness": {"value": 0.7, "confidence": 0.8}, ...}}
Only include axes you can infer."""
