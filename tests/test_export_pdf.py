"""Tests for PDF export."""

from app.export_pdf import format_recommendations_pdf
from app.recommender import BeerLeaf, StyleNode
from app.taste_profile import TasteProfile


def test_format_recommendations_pdf_returns_valid_pdf():
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

    pdf_bytes = format_recommendations_pdf(profile, tree, blurbs)

    assert pdf_bytes.startswith(b"%PDF")
    assert len(pdf_bytes) > 500
