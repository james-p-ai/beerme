# Phase 4 Handoff to ACR

PRD v1.5.0 → **v1.6.0**

## Implemented

- **P4-T1 [#22](https://github.com/james-p-ai/beerme/issues/22):** Expanded [scripts/qa/beerme-smoke.sh](../../scripts/qa/beerme-smoke.sh) for full demo path (quiz, results tree, blurbs toggle, ask-more, reset, optional offline). Fixed ask-more bounce bug via `refining` mode in [app/taste_profile.py](../../app/taste_profile.py).
- **P4-T2 [#23](https://github.com/james-p-ai/beerme/issues/23):** MD export via [app/export_md.py](../../app/export_md.py); `st.download_button` on results screen.
- **Pre-QA stabilization:** Question bank in [app/prompts.py](../../app/prompts.py); axis dedup and banked answers in taste profile; `model_available()` in ollama client; [run.sh](../../run.sh) demo launcher.

## Open / deferred

- PDF export (stretch — out of scope for v1.6.0)
- Live beer APIs (Out of Scope)

## Recommended PRD updates

- Mark `phase-4-polish` complete; no active phase (demo-ready)
- Document question bank (deterministic) vs Ollama (extract + optional blurbs) under Implementation Decisions
- Document MD export under Implementation Decisions
- Testing Decisions: export unit test in `tests/test_export_md.py`; blurbs + full path HITL via smoke script
- Epic label `prd:v1.5.0` → `prd:v1.6.0` on [#1](https://github.com/james-p-ai/beerme/issues/1)

## Demo

```bash
ollama pull llama3.2:3b
./run.sh
```

Blurbs: sidebar toggle on results screen. Export: download button on results screen.

## Next

Product demo-ready. No Phase 5 unless new PRD scope.

## Architect sign-off

Recorded in [docs/prd/PRD.md](../../prd/PRD.md) — v1.6.0 sign-off block (2026-06-01, James Mair). New since v1.5.0: MD export, question bank, refining mode.
