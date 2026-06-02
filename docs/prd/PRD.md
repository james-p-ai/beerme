# BeerMe PRD

## Version header


| Field                  | Value                                                                                |
| ---------------------- | ------------------------------------------------------------------------------------ |
| **Version**            | v1.7.0                                                                               |
| **Date**               | 2026-06-02                                                                           |
| **Author**             | James Mair                                                                           |
| **Summary of changes** | Phase 5 active: PDF export + agent doctrine pilot. See changelog.                   |
| **Active phase(s)**    | phase-5-pdf-export (active)                                                          |


## Architect sign-off (v1.7.0)

| Field | Value |
|-------|-------|
| **PRD version** | v1.7.0 |
| **Signed by** | James Mair (architect) |
| **Date** | 2026-06-02 |
| **Baseline** | v1.6.0 (Phase 4 complete — demo-ready) |

Reviewed Phase 5 handoff ([docs/phases/phase-5-pdf-export/handoff-to-acr.md](../phases/phase-5-pdf-export/handoff-to-acr.md)) and delta. The following **new or materially changed user-facing capabilities** since v1.6.0 are approved:

| Capability | Status | Notes |
|------------|--------|-------|
| **PDF export** | Approved | Download recommendations as `.pdf` from results screen alongside MD export. |
| **Printable blurb** | Approved | Blurb prompt capped for PDF layout; blurbs unchanged in recommendations logic. |

**Sign-off:** Phase 5 complete. PRD v1.7.0 adds PDF export to demo-ready release.


## Architect sign-off (v1.6.0)

| Field | Value |
|-------|-------|
| **PRD version** | v1.6.0 |
| **Signed by** | James Mair (architect) |
| **Date** | 2026-06-01 |
| **Baseline** | v1.5.0 (Phase 3 complete — blurbs, catalog recs, LLM-generated questions) |

Reviewed Phase 4 handoff ([docs/phases/phase-4-polish/handoff-to-acr.md](../phases/phase-4-polish/handoff-to-acr.md)) and delta. The following **new or materially changed user-facing capabilities** since v1.5.0 are approved for demo release:

| Capability | Status | Notes |
|------------|--------|-------|
| **MD export** | Approved | Download recommendations as `.md` from results screen ([#23](https://github.com/james-p-ai/beerme/issues/23)). |
| **Question bank** | Approved | Deterministic axis questions + banked answers replace Ollama question generation. Ollama retained for extract fallback and optional blurbs only. Unplanned deviation — improves demo stability. |
| **Refining mode** | Approved | "Ask more questions" re-opens low-confidence axes instead of bouncing to results. |

No other net-new product scope beyond v1.5.0. QA ([#22](https://github.com/james-p-ai/beerme/issues/22)) complete; smoke script is the remaining human verification gate.

**Sign-off:** Phase 4 complete. PRD v1.6.0 is the canonical demo-ready release.


## Changelog

### v1.7.0 (2026-06-02) — ACR after Phase 5 PDF export + agent pilot

- Phase 5 (`phase-5-pdf-export`): PDF download on results screen (`app/export_pdf.py`, fpdf2).
- `collect_beer_leaves()` public helper in `app/recommender.py` for export and blurb batching.
- `BLURB_MAX_CHARS` constraint in `BLURB_PROMPT` for printable export layout.
- Agent doctrine pilot: tickets routed to `/engine`, `/orion`, `/voyager`, `/verify` per WBS.
- Phase 5 handoff: `docs/phases/phase-5-pdf-export/handoff-to-acr.md`.

### v1.6.0 (2026-06-01) — ACR after Phase 4 polish

- Closed [#22](https://github.com/james-p-ai/beerme/issues/22) P4-T1: expanded smoke script; fixed ask-more bounce via refining mode.
- Closed [#23](https://github.com/james-p-ai/beerme/issues/23) P4-T2: MD export download on results (`app/export_md.py`).
- Question bank: deterministic axis questions from `QUESTION_BANK`; Ollama used for preference extract (fallback) and optional blurbs only.
- `model_available()` check; `./run.sh` demo launcher.
- Phase 4 handoff: `docs/phases/phase-4-polish/handoff-to-acr.md`.

### v1.5.0 (2026-06-01) — ACR after Phase 3 completion (P3-T4)

- Shipped [#21](https://github.com/james-p-ai/beerme/issues/21) P3-T4: optional sidebar toggle for batch LLM tasting notes on results tree; catalog IDs only, prose from Ollama.
- `BLURB_PROMPT` contract in `app/prompts.py`; blurbs cached per results set in session state.
- Phase 3 (`phase-3-catalog-recs`) closed; Phase 4 kickoff at `docs/phases/phase-4-polish/kickoff.md`.
- Next: [#22](https://github.com/james-p-ai/beerme/issues/22) QA session, [#23](https://github.com/james-p-ai/beerme/issues/23) export.

### v1.4.0 (2026-06-01) — ACR after Ralph Ollama JSON batch

- Closed Ralph batch [#14](https://github.com/james-p-ai/beerme/issues/14): `parse_json_response` (plain + embedded JSON) and `chat_json` one-retry on invalid JSON — all mocked, no live Ollama.
- `scripts/ralph/prd-ollama.json` stories `ollama-01`–`ollama-03` all `passes: true`; merged via PR #84.
- GitHub Kanban bootstrap (`scripts/github/bootstrap-kanban.sh`), `docs/github/KANBAN.md`, Ralph playbook linked from README.
- Phase 3 core complete; [#21](https://github.com/james-p-ai/beerme/issues/21) (LLM blurbs) still deferred.
- Phase 4 polish tickets [#22](https://github.com/james-p-ai/beerme/issues/22) (QA session), [#23](https://github.com/james-p-ai/beerme/issues/23) (export) open in Backlog.

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

BeerMe runs locally: asks short flavor questions from a deterministic question bank, builds a structured taste profile, and when session confidence is high enough shows a **hierarchical** list of styles and catalog beers to try—never inventing beers outside the static catalog. Ollama powers optional preference extraction fallback and tasting-note blurbs.

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
- **Question bank:** One question per taste axis from `QUESTION_BANK` in `app/prompts.py`; targets lowest-confidence unasked axis; banked multiple-choice answers map to profile deltas without LLM. Refining mode (after "Ask more questions") re-opens axes below confidence threshold.
- **Ollama contract:** `extract_preferences` and `blurbs` JSON schemas in `app/prompts.py`; `chat_json` retries once on parse failure. Extract used when banked answer mapping fails.
- **LLM blurbs (optional):** Sidebar toggle on results; one batch call with catalog beer metadata + profile; response keys validated ⊆ requested catalog IDs; recommendations unchanged (deterministic scoring).
- **MD export:** Results screen download button; `format_recommendations_md()` renders profile table + recommendation tree + optional blurbs.
- **PDF export:** Results screen download button; `format_recommendations_pdf()` renders same content as printable PDF bytes (fpdf2).
- **Printable blurb:** `BLURB_MAX_CHARS` in `app/prompts.py`; blurbs truncated at render time for PDF if needed.
- **Recommendations:** Dot-product style scoring on tree; top 3 branches expanded to beers.
- **Modules:** `taste_profile`, `recommender`, `ollama_client`, `export_md`, `export_pdf`, `main` (Streamlit).

## Testing Decisions

- Test **public behavior** via `taste_profile`, `recommender`, and `export_md` APIs only.
- Fixtures in `tests/fixtures/` for catalog; no live Ollama in unit tests.
- `ollama_client`: unit tests in `tests/test_ollama_client.py` — plain JSON, embedded JSON, markdown fence, invalid raises, `chat_json` retry; no live server.
- `taste_profile` / `recommender` / `export_md` / `export_pdf`: public API + fixtures only.
- Streamlit + live Ollama (blurbs, full quiz path): manual only — `scripts/qa/beerme-smoke.sh`.
- Ralph AFK stories: acceptance = single pytest node from `scripts/ralph/prd-<batch>.json`; human Verify gate on Kanban before Done.

## Out of Scope

- Accounts, payments, cloud deploy, live Untappp/API beer data, training custom models.

## Further Notes

- See `docs/workflow/` for SOP, Kanban, Ralph, and skills map.
- GitHub PRD epic mirrors this doc; `docs/prd/PRD.md` is canonical for versioning.
- Kanban + issue bootstrap: docs/github/KANBAN.md, ./scripts/github/bootstrap-kanban.sh.
- Ralph loop: docs/workflow/ralph-playbook.md; run PRD_JSON=scripts/ralph/prd-ollama.json ./scripts/ralph/ralph.sh.
- Epic label on [#1](https://github.com/james-p-ai/beerme/issues/1): `prd:v1.7.0` (Phase 5 epic when filed).
- ready-for-human = HITL (product, live LLM, UI judgment); ralph-ready = AFK pytest stories.

