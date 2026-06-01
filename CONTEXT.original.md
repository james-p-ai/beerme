# BeerMe domain glossary

| Term | Meaning |
|------|---------|
| **Taste profile** | User preference vector over fixed taste axes (0–1 per axis). |
| **Taste axis** | One dimension of beer character (e.g. bitterness, sweetness, body). |
| **Axis confidence** | How sure we are about one axis value (0–1); distinct from overall session confidence. |
| **Session confidence** | Aggregate score: enough axes known to recommend (computed in Python, not by LLM). |
| **Catalog** | Static `beers.json` + `style_tree.json`; only source for beer names in recommendations. |
| **Style node** | Entry in the hierarchy (e.g. IPA → West Coast IPA). |
| **Recommendation tree** | Ranked hierarchy of styles and leaf beers from catalog scoring. |
| **Question turn** | One LLM-generated question + user answer updating the profile. |
