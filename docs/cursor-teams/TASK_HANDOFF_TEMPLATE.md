# Task Handoff Template

Copy for merge-ready tasks or before `/verify`. Link in PR description or save under `docs/phases/{phase}/tickets/`.

---

## Task name

`[short descriptive name]`

## Issue

`#NN` — [title](https://github.com/james-p-ai/beerme/issues/NN)

## Domain zone

`[ ] Orion (LLM)  [ ] Engine  [ ] Voyager (UI)  [ ] Multi-zone  [ ] Verify only`

## Branch

`feat/short-name` or `fix/issue-NN-slug`

## Related docs

- [ ] `AGENTS.md`
- [ ] `CONTEXT.md`
- [ ] `docs/prd/PRD.md` (version: _____)
- [ ] Issue body + agent brief comment
- [ ] Other: _______________

## Files changed

```
[git diff --stat or list paths]
```

## Summary

What was done and why (2–5 sentences).

## Tests run

```bash
PYTHONPATH=. pytest -q [paths]
bash scripts/qa/beerme-smoke.sh  # if applicable
```

## Risks

| Risk | Mitigation |
|------|------------|
| | |

## Out of scope (explicit)

- 

## Next agent / skill

- [ ] `/verify` for Phase 7
- [ ] `/tdd` for follow-up issue `#___`
- [ ] `/handoff` for session continuity
- [ ] `/create-pr` if not yet open

## Sign-off

- [ ] Implementer complete
- [ ] Human review / Verify (Phase 7)
