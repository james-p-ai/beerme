"""Taste profile and session confidence (deterministic, not LLM)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

TASTE_AXES = (
    "bitterness",
    "sweetness",
    "body",
    "roast",
    "fruit",
    "sour",
    "hoppy",
    "malt",
    "abv_preference",
    "crispness",
)

MIN_TURNS = 4
MIN_AXES = 6
AXIS_CONFIDENCE_THRESHOLD = 0.6


@dataclass
class TasteProfile:
    values: dict[str, float] = field(default_factory=dict)
    axis_confidence: dict[str, float] = field(default_factory=dict)
    turn_count: int = 0

    def __post_init__(self) -> None:
        for axis in TASTE_AXES:
            self.values.setdefault(axis, 0.5)
            self.axis_confidence.setdefault(axis, 0.0)

    def apply_delta(self, delta: dict[str, Any]) -> None:
        """Merge LLM delta: {axis: {value?, confidence?}} or flat {axis: float}."""
        for axis, payload in delta.items():
            if axis not in TASTE_AXES:
                continue
            if isinstance(payload, dict):
                if "value" in payload and payload["value"] is not None:
                    num = _coerce_float(payload["value"])
                    if num is not None:
                        self.values[axis] = _clamp(num)
                if "confidence" in payload and payload["confidence"] is not None:
                    num = _coerce_float(payload["confidence"])
                    if num is not None:
                        self.axis_confidence[axis] = _clamp(num)
            elif isinstance(payload, (int, float)):
                self.values[axis] = _clamp(float(payload))
                self.axis_confidence[axis] = max(self.axis_confidence[axis], 0.5)

    def record_turn(self) -> None:
        self.turn_count += 1

    def confidence_score(self) -> float:
        """0–1 session readiness."""
        if self.turn_count < MIN_TURNS:
            return min(0.5, self.turn_count / MIN_TURNS * 0.5)
        strong = sum(
            1
            for a in TASTE_AXES
            if self.axis_confidence.get(a, 0) >= AXIS_CONFIDENCE_THRESHOLD
        )
        axis_part = min(1.0, strong / MIN_AXES)
        turn_part = min(1.0, self.turn_count / MIN_TURNS)
        return round(min(1.0, 0.4 * turn_part + 0.6 * axis_part), 3)

    def is_ready(self) -> bool:
        strong = sum(
            1
            for a in TASTE_AXES
            if self.axis_confidence.get(a, 0) >= AXIS_CONFIDENCE_THRESHOLD
        )
        return self.turn_count >= MIN_TURNS and strong >= MIN_AXES

    def axes_by_low_confidence(self) -> list[str]:
        return sorted(TASTE_AXES, key=lambda a: self.axis_confidence.get(a, 0))

    def asked_axes(self, history: list[dict[str, Any]]) -> set[str]:
        """Axes already covered this session — never ask again."""
        from app.prompts import QUESTION_TEXT_TO_AXIS

        asked: set[str] = set()
        for turn in history:
            asked.update(turn.get("targets_axes", []))
            axis = QUESTION_TEXT_TO_AXIS.get(turn.get("question", "").strip())
            if axis:
                asked.add(axis)
        return asked

    def blocked_axes(
        self,
        history: list[dict[str, Any]],
        *,
        refining: bool = False,
    ) -> set[str]:
        asked = self.asked_axes(history)
        if not refining:
            return asked
        return {
            axis
            for axis in asked
            if self.axis_confidence.get(axis, 0) >= AXIS_CONFIDENCE_THRESHOLD
        }

    def preferred_next_axis(self, blocked: set[str]) -> str | None:
        for axis in self.axes_by_low_confidence():
            if axis not in blocked:
                return axis
        return None

    def apply_bitterness_scale(self, answer: str) -> bool:
        if answer == "I don't know":
            self.apply_delta({"bitterness": {"confidence": 0.2}})
            return True
        try:
            level = int(answer)
        except ValueError:
            return False
        if 1 <= level <= 10:
            self.apply_delta({"bitterness": {"value": level / 10, "confidence": 0.85}})
            return True
        return False

    def apply_bank_answer(self, axis: str, answer: str) -> bool:
        """Map a banked multiple-choice answer to profile delta without LLM."""
        if axis == "bitterness":
            return self.apply_bitterness_scale(answer)
        from app.prompts import choice_delta_for_answer

        delta = choice_delta_for_answer(axis, answer)
        if delta is None:
            return False
        self.apply_delta({axis: delta})
        return True

    def to_dict(self) -> dict[str, Any]:
        return {
            "values": dict(self.values),
            "axis_confidence": dict(self.axis_confidence),
            "turn_count": self.turn_count,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> TasteProfile:
        p = cls()
        p.values.update({k: float(v) for k, v in data.get("values", {}).items() if k in TASTE_AXES})
        p.axis_confidence.update(
            {k: float(v) for k, v in data.get("axis_confidence", {}).items() if k in TASTE_AXES}
        )
        p.turn_count = int(data.get("turn_count", 0))
        return p


def _clamp(x: float) -> float:
    return max(0.0, min(1.0, x))


def _coerce_float(value: Any) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None
