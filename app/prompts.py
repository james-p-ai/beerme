"""Ollama system prompts and JSON shapes."""

from __future__ import annotations

from typing import Any

SYSTEM_BASE = """You help BeerMe learn a user's beer taste. Respond with JSON only, no markdown.
Taste axes (0-1): bitterness, sweetness, body, roast, fruit, sour, hoppy, malt, abv_preference, crispness."""

NEXT_QUESTION_PROMPT = SYSTEM_BASE + """
Given profile JSON, conversation history, preferred_axis, blocked_axes, and style_example:

Rules:
- Plain everyday language. No brewer jargon (no "bittering agents", IBU, esters, phenols, mouthfeel).
- Ask about preferred_axis. Do NOT ask about any axis in blocked_axes — those topics are done.
- Match the tone of style_example: short, friendly, concrete.
- Always include choices: 2–4 specific options someone can tap without beer expertise.
- targets_axes must be [preferred_axis] only.

Output:
{"question": "...", "targets_axes": ["sweetness"], "choices": ["Yes", "A little", "No"]}"""

EXTRACT_PROMPT = SYSTEM_BASE + """
Given the user's latest answer and profile, output preference deltas:
{"delta": {"bitterness": {"value": 0.7, "confidence": 0.8}, ...}}
Only include axes you can infer. If the user picked a 1–10 scale, map value as n/10 with confidence ~0.85.
If they said they don't know, use low confidence (~0.2) and leave value near 0.5."""

BLURB_MAX_CHARS = 120

BLURB_PROMPT = SYSTEM_BASE + f"""
Given the user's taste profile and a list of catalog beers (id, name, brewery, profile),
write one short sentence per beer explaining why it fits. Use ONLY the beer ids provided.
Each blurb must be at most {BLURB_MAX_CHARS} characters — short enough for printable export.
Output: {{"blurbs": {{"ipa-01": "...", "stout-02": "..."}}}}"""

# Fallback questions when the LLM repeats a topic or uses bad wording.
BITTERNESS_SCALE_CHOICES = [str(n) for n in range(1, 11)] + ["I don't know"]

QUESTION_BANK: dict[str, dict[str, Any]] = {
    "bitterness": {
        "question": "On a scale of 1 to 10, how intense do you like the bitter taste in your beers?",
        "choices": BITTERNESS_SCALE_CHOICES,
    },
    "hoppy": {
        "question": "Do you enjoy beers with a strong hop character (piney or citrusy)?",
        "choices": ["Yes, the hoppier the better", "A little is fine", "Not really"],
    },
    "sweetness": {
        "question": "Do you like beers with a noticeable sweet or malty side?",
        "choices": ["Yes", "A little", "No, keep it dry"],
    },
    "body": {
        "question": "Do you prefer beers that feel light and easy to drink, or thicker and heavier?",
        "choices": ["Light and crisp", "Somewhere in the middle", "Full and heavy"],
    },
    "roast": {
        "question": "Do you like dark roasty flavors — coffee or chocolate notes?",
        "choices": ["Love that", "A hint is OK", "Not for me"],
    },
    "fruit": {
        "question": "Are you into fruity or citrusy beer flavors?",
        "choices": ["Yes", "Sometimes", "No"],
    },
    "sour": {
        "question": "How do you feel about sour or tart beers?",
        "choices": ["Love them", "Occasionally", "Avoid them"],
    },
    "malt": {
        "question": "Do you enjoy a rich bready, malty character in beer?",
        "choices": ["Yes", "A little", "Not really"],
    },
    "abv_preference": {
        "question": "Do you usually reach for lighter session beers or stronger ones?",
        "choices": ["Light and sessionable", "Middle of the road", "Stronger is better"],
    },
    "crispness": {
        "question": "Do you prefer a clean, crisp finish or a softer lingering finish?",
        "choices": ["Clean and crisp", "Balanced", "Soft and smooth"],
    },
}


def question_for_axis(axis: str) -> dict[str, Any]:
    template = QUESTION_BANK[axis]
    return {
        "question": template["question"],
        "targets_axes": [axis],
        "choices": list(template["choices"]),
    }


QUESTION_TEXT_TO_AXIS = {template["question"]: axis for axis, template in QUESTION_BANK.items()}

# Choice index → axis value (0 = low on axis, 2 = high on axis for most questions).
_HIGH_FIRST = (0.85, 0.5, 0.15)
_LOW_FIRST = (0.15, 0.5, 0.85)
_AXIS_CHOICE_VALUES: dict[str, tuple[float, float, float]] = {
    "body": _LOW_FIRST,
    "abv_preference": _LOW_FIRST,
}


def choice_delta_for_answer(axis: str, answer: str) -> dict[str, float] | None:
    bank = QUESTION_BANK.get(axis)
    if not bank:
        return None
    choices = bank["choices"]
    if answer not in choices:
        return None
    idx = choices.index(answer)
    if axis == "bitterness":
        return None
    if answer == "I don't know":
        return {"confidence": 0.2}
    values = _AXIS_CHOICE_VALUES.get(axis, _HIGH_FIRST)
    if idx >= len(values):
        return None
    return {"value": values[idx], "confidence": 0.85}
