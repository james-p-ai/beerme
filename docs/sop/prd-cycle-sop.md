# PRD → ticket → handoff cycle SOP (caveman reference)

Compressed reference. **Canonical seven-phase SOP:** [ai-driven-development-sop.md](./ai-driven-development-sop.md). Full PRD-cycle text: [prd-cycle-sop.full.md](./prd-cycle-sop.full.md). BeerMe learnings: [verification-addendum.md](./verification-addendum.md). Agent pilot: [agent-doctrine-pilot.md](./agent-doctrine-pilot.md).

## Purpose

Versioned PRD drives phased tickets → engineer in Cursor (plan first) → phase handoff → ACR updates PRD → repeat.

## Core loop

1. Architect bumps PRD version + changelog  
2. Break into phases; phase kickoff approved  
3. Tickets with PRD version + owner  
4. Engineer: plan chat per phase, **new chat per ticket**, plan before code  
5. Track merges in phase plan  
6. Phase delta (planned vs actual)  
7. Phase handoff when stable  
8. ACR updates PRD  
9. Architect sign-off → next phase  

## DoR (ticket)

- Tied to PRD phase + version  
- Acceptance clear  
- Approved plan; tests identified  
- Behaviors listed for TDD (BeerMe)  

## DoD (ticket)

- Code in scope; pytest green  
- PR merged; deviations logged  

## DoD (phase)

- All tickets merged  
- Delta + handoff to ACR  
- PRD bumped  
- Architect sign-off  

## BeerMe extensions

| Tool | Use |
|------|-----|
| GitHub Kanban | Backlog → Verify → Done |
| Ralph | `scripts/ralph/`; Verify before Done |
| Practical Office `to-prd` | PRD draft / ACR |
| Practical Office `to-issues` | Vertical slice issues |
| Practical Office `tdd` | RED→GREEN per behavior |
| Subagents | `/orion`, `/engine`, `/voyager`, `/verify` per ticket zone |
| Session `handoff` | Not same as phase handoff |

## Rules

- Repo = source of record; chats ephemeral  
- Phase freeze in-scope PRD unless kickoff amended  
- Blocked >24h flag; >48h escalate  

Prompt blocks unchanged in full SOP file — copy from `prd-cycle-sop.full.md` when needed.
