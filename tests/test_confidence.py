"""Tests for taste profile confidence."""

from app.taste_profile import MIN_AXES, MIN_TURNS, TasteProfile, TASTE_AXES


def test_empty_profile_low_confidence():
    p = TasteProfile()
    assert p.confidence_score() < 0.5
    assert not p.is_ready()


def test_ready_after_enough_axes_and_turns():
    p = TasteProfile()
    for _ in range(MIN_TURNS):
        p.record_turn()
    for axis in list(TASTE_AXES)[:MIN_AXES]:
        p.apply_delta({axis: {"value": 0.7, "confidence": 0.8}})
    assert p.is_ready()
    assert p.confidence_score() >= 0.8


def test_apply_delta_clamps_values():
    p = TasteProfile()
    p.apply_delta({"bitterness": {"value": 1.5, "confidence": 1.2}})
    assert p.values["bitterness"] == 1.0
    assert p.axis_confidence["bitterness"] == 1.0


def test_roundtrip_dict():
    p = TasteProfile()
    p.record_turn()
    p.apply_delta({"sweetness": 0.2})
    p2 = TasteProfile.from_dict(p.to_dict())
    assert p2.turn_count == p.turn_count
    assert p2.values["sweetness"] == p.values["sweetness"]
