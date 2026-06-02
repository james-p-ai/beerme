# SOP verification addendum (BeerMe pilot)

Learnings from running the PRD → ticket → handoff → ACR cycle on BeerMe.

## What worked

- **Dual PRD:** `docs/prd/PRD.md` canonical + GitHub epic for visibility
- **Phase folders:** `docs/phases/<phase>/kickoff|delta|handoff-to-acr.md`
- **Verify column:** Ralph/agent batches land in Verify before Done
- **TDD vertical slices:** One behavior per test; Ralph `prd.json` story = one cycle
- **Practical Office skills:** `setup-practical-ai-skills` → `docs/agents/*`; `to-issues` for Kanban slices

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

## Agent doctrine routing smoke (2026-06-02)

Structural verification on branch `feat/agent-doctrine-and-subagents` (PR #86). Full interactive Cursor smoke requires human session; automated checks below passed during Phase 5 pilot prep.

| Check | Result | Notes |
|-------|--------|-------|
| `.cursor/agents/orion.md` | Pass | LLM zone declared |
| `.cursor/agents/engine.md` | Pass | Deterministic zone declared |
| `.cursor/agents/voyager.md` | Pass | UI/export zone declared |
| `.cursor/agents/verify.md` | Pass | `readonly: true` in frontmatter |
| `00-beerme-master-doctrine.mdc` | Pass | `alwaysApply: true` |
| `01-llm-boundary.mdc` globs | Pass | `app/ollama_client.py`, `app/prompts.py` |
| `02-deterministic-engine.mdc` globs | Pass | `app/taste_profile.py`, `app/recommender.py`, `data/**`, engine tests |
| `03-definition-of-done.mdc` globs | Pass | `app/**`, `tests/**`, `scripts/**` |

**Human follow-up:** Open Cursor on `app/prompts.py` and confirm `01-llm-boundary` attaches; invoke `/verify` and confirm no file edits. Merge PR #86 to `main` when ready.

## Phase 5 PDF pilot (2026-06-02)

See `docs/sop/agent-doctrine-pilot.md` and `docs/phases/phase-5-pdf-export/`.
