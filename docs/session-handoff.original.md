# BeerMe session handoff

Use this to continue work in a fresh chat. Canonical sources stay in repo — do not duplicate; reference by path.

## Product state (2026-06-01)

- **PRD:** v1.6.0 — demo-ready, all phases shipped. See [docs/prd/PRD.md](prd/PRD.md).
- **Architect sign-off:** recorded in PRD header block (MD export, question bank, refining mode approved vs v1.5.0).
- **Epic #1:** closed, Done on [BeerMe Kanban](https://github.com/users/james-p-ai/projects/2).
- **Phase tickets:** #2–#23 all closed. No open phase work for v1.6.0 scope.
- **Latest commits:** `2c1e78a` (Kanban doc), `571754a` (architect sign-off), `6664a3e` (Phase 4 polish).

## What shipped in Phase 4

1. **Question bank** — deterministic axis questions from `QUESTION_BANK` in `app/prompts.py`; banked answers map to profile without LLM. Ollama only for extract fallback + optional blurbs.
2. **Refining mode** — "Ask more questions" re-opens axes below confidence threshold (`refining` flag in session state).
3. **MD export** — `app/export_md.py`, download button on results screen.
4. **Demo ergonomics** — `./run.sh`, expanded `scripts/qa/beerme-smoke.sh`, `model_available()` in ollama client.
5. **QA bug fixed** — ask-more no longer bounces straight to results.

## Remaining human gate

Run manual smoke (not pytest):

```bash
ollama pull llama3.2:3b
./run.sh
bash scripts/qa/beerme-smoke.sh
```

Pass smoke → product done for v1.6.0 scope.

## Out of scope (do not expand without new PRD)

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

21 tests passing as of Phase 4 close.

## Suggested skills for next session

| Task | Skill |
|------|-------|
| New product scope | `to-prd` |
| Break plan into tickets | `to-issues` |
| Implement a ticket | `tdd` |
| Interactive bug filing | `qa` |
| Session summary | `handoff` |
| Compress this file for tokens | `caveman-compress` |

## Likely next work (if any)

- Run smoke test and file issues if bugs found (`qa` skill).
- New PRD version + Phase 5 kickoff for PDF export or other scope (`to-prd`, `to-issues`).
- Maintenance only until new PRD.
