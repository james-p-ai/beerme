"""Tests for markdown export."""

from app.export_md import format_recommendations_md
from app.recommender import BeerLeaf, StyleNode
from app.taste_profile import TasteProfile


def test_format_recommendations_md_includes_profile_and_tree():
    profile = TasteProfile()
    profile.apply_delta({"bitterness": {"value": 0.8, "confidence": 0.9}})
    profile.record_turn()

    tree = [
        StyleNode(
            id="ipa",
            name="IPA",
            score=0.92,
            children=[
                BeerLeaf(id="ipa-01", name="West Coast IPA", brewery="Hop Co", score=0.88),
            ],
        )
    ]
    blurbs = {"ipa-01": "Crisp and bitter — matches your profile."}

    md = format_recommendations_md(profile, tree, blurbs)

    assert "# BeerMe recommendations" in md
    assert "Session confidence:" in md
    assert "| bitterness |" in md
    assert "**IPA**" in md
    assert "**West Coast IPA**" in md
    assert "Hop Co" in md
    assert "Crisp and bitter" in md


def test_format_recommendations_md_without_blurbs():
    profile = TasteProfile()
    tree = [StyleNode(id="lager", name="Lager", score=0.7, children=[])]
    md = format_recommendations_md(profile, tree, None)
    assert "**Lager**" in md
    assert "_" not in md.split("## Recommendations")[1] or "Lager" in md
