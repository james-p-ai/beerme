# Agent doctrine pilot runbook (BeerMe Phase 5)

How BeerMe validated Practical AI agent doctrine (PR #86) on real tickets. Copy this checklist for greenfield single-app repos.

## Prerequisites

1. Install [Practical-Office/cursor-skills](https://github.com/Practical-Office/cursor-skills) on the machine.
2. Run **`setup-practical-ai-skills`** once; commit `docs/agents/*` and `AGENTS.md`.
3. Add scaled doctrine:
   - `AGENTS.md` — vision, non-negotiables, build commands, workflow
   - `.cursor/agents/` — one file per domain zone + readonly verify
   - `.cursor/rules/` — `alwaysApply` master + glob boundaries
   - `docs/cursor-teams/` — usage guide, release gates, handoff template
4. Merge doctrine PR before filing phase tickets.

## Greenfield checklist

| Step | Artifact | Skill / agent |
|------|----------|---------------|
| 1 | Canonical SOP in repo | `docs/sop/ai-driven-development-sop.md` |
| 2 | PRD bump for new scope | `to-prd` |
| 3 | Phase kickoff + WBS | human + `to-issues` |
| 4 | GitHub issues with triage labels | `triage` |
| 5 | One chat per ticket | `/orion`, `/engine`, or `/voyager` + `tdd` |
| 6 | Pre-PR gates | `review`, `security-secrets-check`, `create-pr` |
| 7 | Phase close | `/verify` (readonly), smoke HITL, handoff → ACR |

## BeerMe Phase 5 ticket → subagent map

| Ticket | Subagent | Files | Type |
|--------|----------|-------|------|
| P5-T1 | `/engine` | `app/recommender.py`, `tests/test_recommender.py` | AFK |
| P5-T2 | `/orion` | `app/prompts.py`, `tests/test_prompts.py` | AFK |
| P5-T3 | `/voyager` | `app/export_pdf.py`, `app/main.py`, `tests/test_export_pdf.py` | AFK |
| P5-T4 | human | `scripts/qa/beerme-smoke.sh` | HITL |
| P5-T5 | `/verify` | readonly — pytest, smoke, release gates | HITL |

## Session prompt template

```text
/engine Implement P5-T1 per issue #NN. Read @AGENTS.md @CONTEXT.md @docs/phases/phase-5-pdf-export/kickoff.md. Use /tdd. One issue only.
```

Replace `/engine` with the owning subagent from the WBS.

## What to record after pilot

- Update `docs/sop/verification-addendum.md` — routing smoke + ticket learnings
- Update `docs/sop/RETROSPECTIVE.md` — subagents vs solo-agent sessions
- Phase `delta.md` + `handoff-to-acr.md` → ACR → PRD sign-off

## When not to copy BeerMe subagents

- Docs-only or script repos — skills + `AGENTS.md` only
- Hard multi-service monorepo — use BookIQ six-team pattern instead

See [AI-Driven Development SOP §5](ai-driven-development-sop.md) for the decision table.
