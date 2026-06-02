# BeerMe session handoff

Use for fresh chat. Canonical sources in repo — reference by path, don't duplicate.

## Product state (2026-06-02)

- **PRD:** v1.7.0 — PDF export shipped; agent doctrine pilot complete. [docs/prd/PRD.md](prd/PRD.md)
- **Architect sign-off:** PRD header block — PDF export approved vs v1.6.0
- **Phase 5:** `phase-5-pdf-export` closed — see [handoff](phases/phase-5-pdf-export/handoff-to-acr.md)
- **Agent doctrine:** PR [#86](https://github.com/james-p-ai/beerme/pull/86) — merge to `main` when ready
- **Branch:** `feat/phase-5-pdf-export-sop-pilot` — code + SOP pilot

## Phase 5 shipped

1. **`collect_beer_leaves`** — public helper in recommender for export/blurb batching
2. **Printable blurb** — `BLURB_MAX_CHARS` in prompts
3. **PDF export** — `app/export_pdf.py` + download button (fpdf2)
4. **SOP canonical** — `docs/sop/ai-driven-development-sop.md` + agent pilot runbook
5. **Smoke** — PDF step + offline export import check

## Remaining human gate

```bash
pip install -r requirements.txt
ollama pull llama3.2:3b
./run.sh
bash scripts/qa/beerme-smoke.sh
```

Also: interactive Cursor routing smoke per `docs/sop/verification-addendum.md`.

## Key paths

| Artifact | Path |
|----------|------|
| PRD | `docs/prd/PRD.md` |
| Canonical SOP | `docs/sop/ai-driven-development-sop.md` |
| Agent pilot | `docs/sop/agent-doctrine-pilot.md` |
| Phase 5 handoff | `docs/phases/phase-5-pdf-export/handoff-to-acr.md` |
| Cursor usage | `docs/cursor-teams/CURSOR_USAGE_GUIDE.md` |
| Smoke script | `scripts/qa/beerme-smoke.sh` |

## Tests

```bash
PYTHONPATH=. pytest -q
```

26 tests after Phase 5 close.

## Suggested skills for next session

| Task | Skill |
|------|-------|
| Merge doctrine PR | human + `create-pr` |
| Interactive routing smoke | `/verify` readonly |
| New product scope | `to-prd` |
| Break plan into tickets | `to-issues` |
| Implement ticket | `tdd` + domain subagent |

## Likely next work

- Merge PR #86 (agent doctrine) and Phase 5 pilot PR
- Run full smoke HITL
- Copy agent pilot pattern to next greenfield repo
