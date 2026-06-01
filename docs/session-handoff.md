# BeerMe session handoff

Use for fresh chat. Canonical sources in repo — reference by path, don't duplicate.

## Product state (2026-06-01)

- **PRD:** v1.6.0 — demo-ready, all phases shipped. [docs/prd/PRD.md](prd/PRD.md)
- **Architect sign-off:** PRD header block — MD export, question bank, refining mode approved vs v1.5.0
- **Epic #1:** closed, Done on [BeerMe Kanban](https://github.com/users/james-p-ai/projects/2)
- **Phase tickets:** #2–#23 closed. No open v1.6.0 scope work
- **Latest commits:** `2c1e78a` Kanban doc, `571754a` architect sign-off, `6664a3e` Phase 4 polish

## Phase 4 shipped

1. **Question bank** — axis Qs from `QUESTION_BANK` in `app/prompts.py`; banked answers → profile without LLM. Ollama = extract fallback + optional blurbs only
2. **Refining mode** — "Ask more questions" re-opens axes below confidence threshold (`refining` session flag)
3. **MD export** — `app/export_md.py`, download button on results
4. **Demo ergonomics** — `./run.sh`, expanded `scripts/qa/beerme-smoke.sh`, `model_available()` in ollama client
5. **QA fix** — ask-more no longer bounce straight to results

## Remaining human gate

Manual smoke (not pytest):

```bash
ollama pull llama3.2:3b
./run.sh
bash scripts/qa/beerme-smoke.sh
```

Pass smoke → done for v1.6.0 scope.

## Out of scope (need new PRD)

PDF export, live beer APIs, accounts, cloud deploy.

## Key paths

| Artifact | Path |
|----------|------|
| PRD | `docs/prd/PRD.md` |
| Domain glossary | `CONTEXT.md` |
| Phase 4 handoff | `docs/phases/phase-4-polish/handoff-to-acr.md` |
| Kanban guide | `docs/github/KANBAN.md` |
| Smoke script | `scripts/qa/beerme-smoke.sh` |

## Tests

```bash
PYTHONPATH=. pytest -q
```

21 tests passing at Phase 4 close.

## Suggested skills for next session

| Task | Skill |
|------|-------|
| New product scope | `to-prd` |
| Break plan into tickets | `to-issues` |
| Implement ticket | `tdd` |
| Interactive bug filing | `qa` |
| Session summary | `handoff` |
| Compress this file | `caveman-compress` |

## Likely next work

- Run smoke, file bugs if any (`qa`)
- New PRD + Phase 5 kickoff for PDF etc (`to-prd`, `to-issues`)
- Maintenance until new PRD
