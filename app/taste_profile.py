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
                if "value" in payload:
                    self.values[axis] = _clamp(float(payload["value"]))
                if "confidence" in payload:
                    self.axis_confidence[axis] = _clamp(float(payload["confidence"]))
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
