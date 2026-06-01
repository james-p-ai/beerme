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


def test_blocked_axes_skips_covered_topics():
    p = TasteProfile()
    p.apply_delta({"bitterness": {"value": 0.8, "confidence": 0.9}})
    history = [{"question": "Bitter?", "answer": "Yes", "targets_axes": ["bitterness"]}]
    blocked = p.blocked_axes(history)
    assert "bitterness" in blocked
    assert p.preferred_next_axis(blocked) != "bitterness"


def test_blocked_axes_refining_allows_low_confidence_reask():
    p = TasteProfile()
    p.apply_delta({"bitterness": {"value": 0.5, "confidence": 0.3}})
    history = [{"question": "Bitter?", "answer": "5", "targets_axes": ["bitterness"]}]
    blocked = p.blocked_axes(history, refining=True)
    assert "bitterness" not in blocked
    next_axis = p.preferred_next_axis(blocked)
    assert next_axis is not None
    assert next_axis in {"bitterness", "sweetness"}


def test_preferred_next_axis_picks_unasked_axis():
    p = TasteProfile()
    p.apply_delta({"bitterness": {"value": 0.9, "confidence": 0.9}})
    history = [{"question": "x", "answer": "y", "targets_axes": ["bitterness"]}]
    blocked = p.blocked_axes(history)
    assert p.preferred_next_axis(blocked) != "bitterness"


def test_preferred_next_axis_none_when_all_asked():
    p = TasteProfile()
    history = [{"question": "", "answer": "", "targets_axes": [axis]} for axis in TASTE_AXES]
    blocked = p.blocked_axes(history)
    assert p.preferred_next_axis(blocked) is None


def test_asked_axes_backfill_from_question_text():
    from app.prompts import QUESTION_BANK

    p = TasteProfile()
    history = [
        {
            "question": QUESTION_BANK["bitterness"]["question"],
            "answer": "5",
            "targets_axes": [],
        }
    ]
    assert "bitterness" in p.asked_axes(history)


def test_apply_delta_ignores_null_fields():
    p = TasteProfile()
    p.apply_delta({"sweetness": {"value": None, "confidence": 0.8}})
    assert p.values["sweetness"] == 0.5
    assert p.axis_confidence["sweetness"] == 0.8


def test_bank_answer_maps_choice():
    from app.prompts import QUESTION_BANK

    p = TasteProfile()
    assert p.apply_bank_answer("hoppy", QUESTION_BANK["hoppy"]["choices"][0])
    assert p.values["hoppy"] == 0.85
    assert p.axis_confidence["hoppy"] == 0.85


def test_bitterness_scale_maps_answer():
    p = TasteProfile()
    p.apply_delta({"bitterness": {"value": 0.5, "confidence": 0.0}})
    assert p.apply_bitterness_scale("8")
    assert p.values["bitterness"] == 0.8
    assert p.axis_confidence["bitterness"] == 0.85

    p2 = TasteProfile()
    assert p2.apply_bitterness_scale("I don't know")
    assert p2.axis_confidence["bitterness"] == 0.2
