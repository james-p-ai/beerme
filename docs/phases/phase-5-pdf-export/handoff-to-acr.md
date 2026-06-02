# Phase 5 Handoff to ACR

PRD v1.6.0 → **v1.7.0**

## Implemented

- **P5-T1:** `collect_beer_leaves()` in [app/recommender.py](../../app/recommender.py); tests in [tests/test_recommender.py](../../tests/test_recommender.py).
- **P5-T2:** `BLURB_MAX_CHARS` + printable constraint in [app/prompts.py](../../app/prompts.py); [tests/test_prompts.py](../../tests/test_prompts.py).
- **P5-T3:** PDF export via [app/export_pdf.py](../../app/export_pdf.py) (fpdf2); second `st.download_button` in [app/main.py](../../app/main.py); [tests/test_export_pdf.py](../../tests/test_export_pdf.py).
- **P5-T4:** Expanded [scripts/qa/beerme-smoke.sh](../../scripts/qa/beerme-smoke.sh) — offline export import + PDF download step.
- **Process:** Canonical [docs/sop/ai-driven-development-sop.md](../../sop/ai-driven-development-sop.md), [agent-doctrine-pilot.md](../../sop/agent-doctrine-pilot.md), agent routing smoke in [verification-addendum.md](../../sop/verification-addendum.md).

## Open / deferred

- Live beer APIs (Out of Scope)
- Interactive Cursor subagent routing smoke (human follow-up after PR #86 merge to main)

## Recommended PRD updates

- Mark `phase-5-pdf-export` complete
- Document PDF export under Implementation Decisions (done in v1.7.0 header)
- Testing Decisions: `test_export_pdf.py`, `test_prompts.py` added
- Epic label `prd:v1.7.0`

## Demo

```bash
pip install -r requirements.txt
ollama pull llama3.2:3b
./run.sh
```

Export: MD and PDF download buttons on results screen.

## Next

Demo-ready at v1.7.0. Run smoke HITL; merge agent doctrine PR #86 if not yet on main.

## Architect sign-off

Recorded in [docs/prd/PRD.md](../../prd/PRD.md) — v1.7.0 sign-off block (2026-06-02, James Mair). New since v1.6.0: PDF export, printable blurb constraint, agent doctrine pilot artifacts.
