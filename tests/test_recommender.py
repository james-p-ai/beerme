"""Tests for hierarchical recommender."""

from app.recommender import recommend_hierarchy
from app.taste_profile import TasteProfile


def test_recommend_returns_style_nodes():
    p = TasteProfile()
    for axis in ("bitterness", "hoppy", "sweetness", "body", "malt", "fruit"):
        p.apply_delta({axis: {"value": 0.8, "confidence": 0.9}})
    p.record_turn()
    tree = recommend_hierarchy(p, top_branches=2)
    assert len(tree) <= 2
    assert tree[0].name
    assert tree[0].score > 0


def test_hoppy_profile_prefers_ipa_branch():
    p = TasteProfile()
    for axis in ("bitterness", "hoppy", "sweetness", "body", "malt", "crispness"):
        p.apply_delta({axis: {"value": 0.95 if axis == "hoppy" else 0.5, "confidence": 0.9}})
    tree = recommend_hierarchy(p, top_branches=1)
    assert "IPA" in tree[0].name or tree[0].id == "ipa"
