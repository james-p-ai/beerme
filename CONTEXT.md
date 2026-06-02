# BeerMe domain glossary

| Term | Meaning |
|------|---------|
| **Taste profile** | User pref vector over taste axes (0–1 per axis). |
| **Taste axis** | One beer character dimension (bitterness, sweetness, body, etc.). |
| **Axis confidence** | Surety on one axis (0–1); not session confidence. |
| **Session confidence** | Aggregate: enough axes known to recommend (Python, not LLM). |
| **Catalog** | Static `beers.json` + `style_tree.json`; only beer name source in recs. |
| **Style node** | Hierarchy entry (e.g. IPA → West Coast IPA). |
| **Recommendation tree** | Ranked style + leaf beer hierarchy from catalog scoring. |
| **Question turn** | One banked quiz question + answer updates profile. |
| **Export snapshot** | Profile + recommendation tree + optional blurbs passed to MD/PDF formatters. |
| **Printable blurb** | Tasting note prose capped for PDF layout (`BLURB_MAX_CHARS`). |
