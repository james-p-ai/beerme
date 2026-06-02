# Cursor Usage Guide — BeerMe

How to use this repo with Cursor and the [AI-Driven Development SOP](docs/sop/prd-cycle-sop.full.md) seven-phase pipeline.

## 1. Load doctrine first

Start every session with:

- `@AGENTS.md` — non-negotiables, domain zones, workflow
- `@CONTEXT.md` — domain glossary (taste profile, session confidence, catalog, etc.)
- `@docs/prd/PRD.md` — when doing phase or PRD-scoped work
- `@docs/github/KANBAN.md` — board columns and phase filters

For phase planning add `@docs/phases/{phase}/kickoff.md`.

## 2. Invoke domain subagents

| Subagent | Command | Agent file |
|----------|---------|------------|
| LLM layer | `/orion …` | `.cursor/agents/orion.md` |
| Engine | `/engine …` | `.cursor/agents/engine.md` |
| UI | `/voyager …` | `.cursor/agents/voyager.md` |
| Verify (readonly) | `/verify …` | `.cursor/agents/verify.md` |

Example:

```text
/engine Plan issue #NN taste_profile behavior. Read @CONTEXT.md. Plan mode only.
```

Project rules in `.cursor/rules/` apply automatically for master doctrine; globs attach LLM/engine/DoD rules on matching paths.

## 3. Planning session (Phase 5–6)

1. Switch to **Plan** mode (or planning prompt from issue body).
2. Attach `@AGENTS.md` + `@CONTEXT.md` + issue `#`.
3. Require: owning zone, files, tests, risks, acceptance criteria.
4. **Do not edit code** until plan is accepted.

## 4. Implementation session (Phase 6)

1. Create branch: `feat/short-name` or `fix/issue-NN-slug`.
2. Route: `/orion`, `/engine`, or `/voyager` when ticket crosses zones; else default agent + **`/tdd`**.
3. One issue per chat; one subtask at a time.
4. Pre-PR: `/security-secrets-check`, `/review`, `/create-pr`.

## 5. Verify before phase close (Phase 7)

```text
/verify Validate phase [name]. @docs/cursor-teams/TASK_HANDOFF_TEMPLATE.md
```

Run `bash scripts/qa/beerme-smoke.sh`. File bugs with **`/qa`**. Loop 5 → 6 → 7 until QA passes.

## 6. Ralph AFK batches

See `docs/workflow/ralph-playbook.md`. After Ralph batch: human moves parent to **Verify** on board → `/verify` → **Done**.

## 7. Context limits

| Signal | Action |
|--------|--------|
| Meter ~50–70% at subtask stop | `/summarize` |
| Chat confused or >90% | `/handoff` → new chat |
| New ticket | **New chat always** |
| Post-cycle handoff file | optional `/caveman-compress` — see `docs/workflow/external-skills.md` |

## Skills vs subagents

- **Skills** (Practical-Office/cursor-skills): procedure — `to-issues`, `triage`, `tdd`, `handoff`, etc.
- **Subagents**: domain boundaries — LLM vs engine vs UI vs verify.

See `docs/workflow/skills-map.md` for phase → skill mapping.
