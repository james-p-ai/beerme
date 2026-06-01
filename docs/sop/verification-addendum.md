# SOP verification addendum (BeerMe pilot)

Learnings from running the PRD → ticket → handoff → ACR cycle on BeerMe.

## What worked

- **Dual PRD:** `docs/prd/PRD.md` canonical + GitHub epic for visibility
- **Phase folders:** `docs/phases/<phase>/kickoff|delta|handoff-to-acr.md`
- **Verify column:** Ralph/agent batches land in Verify before Done
- **TDD vertical slices:** One behavior per test; Ralph `prd.json` story = one cycle
- **Matt skills:** `setup-matt-pocock-skills` → `docs/agents/*`; `to-issues` for Kanban slices

## Minimum ticket size

- Streamlit + Ollama: split **JSON contract** (HITL) from **pure Python** (AFK/Ralph)
- S tickets: docs-only; M: one module; L: split before Ralph

## Solo ACR checklist

- ACR chat: **no code** — only PRD diff + changelog
- Use `to-prd` skill with handoff + delta attached

## Normative paths

```
docs/prd/PRD.md
docs/phases/{phase}/kickoff.md
docs/phases/{phase}/delta.md
docs/phases/{phase}/handoff-to-acr.md
docs/agents/
scripts/ralph/
```

## HITL

- `to-issues` marks HITL vs AFK
- `ready-for-human` triage label
- `scripts/qa/beerme-smoke.sh` for manual smoke
