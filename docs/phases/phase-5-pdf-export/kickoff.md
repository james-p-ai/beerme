# Phase 5 Kickoff — PDF export + agent pilot

| Field | Value |
|-------|-------|
| PRD Version | v1.7.0 |
| Phase | phase-5-pdf-export |
| Goal | PDF download on results screen; validate subagent routing on real tickets |

## In scope

- **P5-T1 [#87](https://github.com/james-p-ai/beerme/issues/87):** Extract `collect_beer_leaves()` to recommender — `/engine`
- **P5-T2 [#88](https://github.com/james-p-ai/beerme/issues/88):** Printable blurb max-length in `BLURB_PROMPT` — `/orion`
- **P5-T3 [#89](https://github.com/james-p-ai/beerme/issues/89):** PDF export module + download button — `/voyager`
- **P5-T4 [#90](https://github.com/james-p-ai/beerme/issues/90):** Smoke script PDF path — HITL
- **P5-T5 [#91](https://github.com/james-p-ai/beerme/issues/91):** Phase 7 verify + handoff — `/verify` (readonly)

Epic: [#92](https://github.com/james-p-ai/beerme/issues/92)

## Out of scope

- Live beer APIs, accounts, cloud deploy
- Shared export refactor beyond minimal duplication control

## Assignment matrix

| Ticket | Size | Type | Subagent | Depends on |
|--------|------|------|----------|------------|
| P5-T1 collect_beer_leaves | S | AFK | `/engine` | — |
| P5-T2 blurb max length | S | AFK | `/orion` | — |
| P5-T3 PDF export | M | AFK | `/voyager` | P5-T1 |
| P5-T4 smoke PDF | S | HITL | human | P5-T3 |
| P5-T5 phase verify | S | HITL | `/verify` | P5-T4 |

## Execution order

1. **P5-T1** — engine helper (parallel with T2)
2. **P5-T2** — orion prompt constraint
3. **P5-T3** — voyager PDF + UI
4. **P5-T4** — human smoke
5. **P5-T5** — verify + phase close

## Session conventions

- Branch: `feat/p5-tN-short-slug`
- PR title: `feat(export): … (#NN)`
- Each session: `@AGENTS.md` + `@CONTEXT.md` + issue `#` + `/tdd` + domain subagent
- Pre-PR: `/review`, `/security-secrets-check`, `/create-pr`

## Agent pilot intent

This phase validates [docs/sop/agent-doctrine-pilot.md](../../sop/agent-doctrine-pilot.md). Do **not** implement multiple tickets in one chat.
