"""Tests for hierarchical recommender."""

from app.recommender import BeerLeaf, StyleNode, collect_beer_leaves, recommend_hierarchy
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


def test_collect_beer_leaves_empty_tree():
    assert collect_beer_leaves([]) == []


def test_collect_beer_leaves_nested_style_and_beer():
    tree = [
        StyleNode(
            id="ipa",
            name="IPA",
            score=0.9,
            children=[
                BeerLeaf(id="ipa-01", name="West Coast IPA", brewery="Hop Co", score=0.88),
                StyleNode(
                    id="ipa-hazy",
                    name="Hazy IPA",
                    score=0.85,
                    children=[
                        BeerLeaf(id="ipa-02", name="Juicy Haze", brewery="Cloud Brew", score=0.82),
                    ],
                ),
            ],
        )
    ]
    leaves = collect_beer_leaves(tree)
    assert len(leaves) == 2
    assert {leaf.id for leaf in leaves} == {"ipa-01", "ipa-02"}
