# BeerMe PRD

## Version header

| Field | Value |
|-------|-------|
| **Version** | v1.3.0 |
| **Date** | 2026-06-01 |
| **Author** | James Mair |
| **Summary of changes** | Phase 3 complete: catalog, recommender, hierarchical UI. See changelog. |
| **Active phase(s)** | phase-3-catalog-recs (complete); next: polish / demo |

## Changelog

### v1.3.0 (2026-06-01) — ACR after Phase 3

- Shipped static catalog (~40 beers), `recommender.py`, expandable results tree in Streamlit.
- LLM blurbs optional; recommendations always from catalog IDs.
- Deferred: export PDF, live beer APIs.

### v1.2.0 (2026-06-01) — ACR after Phase 2

- Taste profile with 10 axes; session confidence in Python (min 4 turns, 6 axes ≥ 0.6).
- Ollama JSON question/extract contract; one retry on parse failure.
- Pinned model: `llama3.2:3b`.

### v1.1.0 (2026-06-01) — ACR after Phase 1

- Repo scaffold, `ollama_client` health check, Streamlit shell with connection status.
- Env: `OLLAMA_HOST`, `OLLAMA_MODEL` (default `llama3.2:3b`).

### v1.0.0 (2026-06-01) — Initial

- Local taste quiz → hierarchical beer recommendations via Ollama + deterministic scoring.

---

## Problem Statement

Beer drinkers struggle to pick styles and specific beers that match nuanced taste preferences. Shelf labels and style names do not map cleanly to what someone likes (bitterness vs sweetness vs body, etc.).

## Solution

BeerMe runs locally: asks short flavor questions powered by Ollama, builds a structured taste profile, and when session confidence is high enough shows a **hierarchical** list of styles and catalog beers to try—never inventing beers outside the static catalog.

## User Stories

1. As a curious drinker, I want to answer simple taste questions, so that I can discover beers without knowing style jargon.
2. As a user, I want the app to stop asking when it is confident enough, so that I am not quizzed forever.
3. As a user, I want recommendations grouped by style family, so that I can explore from broad to specific.
4. As a user, I want every suggested beer to exist in the app catalog, so that I can trust names are real.
5. As a host, I want the app to run offline except Ollama, so that I can demo without cloud APIs.
6. As a developer, I want confidence computed in code, so that LLM cannot falsely claim readiness.
7. As a user, I want to reset and start over, so that I can try another preference path.
8. As a user, I want to see progress toward confidence, so that I know how many questions remain roughly.

## Implementation Decisions

- **Stack:** Python 3.11+, Streamlit UI, Ollama at `http://localhost:11434`, static JSON catalog.
- **Taste axes (10):** bitterness, sweetness, body, roast, fruit, sour, hoppy, malt, abv_preference, crispness.
- **Profile merge:** LLM returns JSON deltas; Python clamps 0–1 and updates per-axis confidence.
- **Session confidence:** `min_axes=6` with per-axis confidence ≥ 0.6, `min_turns=4`.
- **Ollama contract:** `next_question` and `extract_preferences` JSON schemas in `app/prompts.py`.
- **Recommendations:** Dot-product style scoring on tree; top 3 branches expanded to beers.
- **Modules:** `taste_profile`, `recommender`, `ollama_client`, `main` (Streamlit).

## Testing Decisions

- Test **public behavior** via `taste_profile` and `recommender` APIs only.
- Fixtures in `tests/fixtures/` for catalog; no live Ollama in unit tests.
- `ollama_client`: parse/retry with recorded JSON fixtures.
- Streamlit: manual Verify column / `scripts/qa/beerme-smoke.sh`.

## Out of Scope

- Accounts, payments, cloud deploy, live Untappp/API beer data, training custom models.

## Further Notes

- See `docs/workflow/` for SOP, Kanban, Ralph, and mattpocock skills map.
- GitHub PRD epic mirrors this doc; `docs/prd/PRD.md` is canonical for versioning.
