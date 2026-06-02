# Triage label vocabulary

Skills read this file via `setup-practical-ai-skills`. **Triage role** labels are canonical across Practical Office repos. **BeerMe program** labels are local extensions.

## Triage roles (one state label per issue)

| Role in skills | GitHub label | Meaning |
|----------------|--------------|---------|
| needs-triage | `needs-triage` | Maintainer must evaluate |
| needs-info | `needs-info` | Waiting on reporter |
| ready-for-agent | `ready-for-agent` | AFK-ready; agent brief complete |
| ready-for-human | `ready-for-human` | Human judgment required |
| wontfix | `wontfix` | Will not action |

## Category (optional, one)

| Label | Use |
|-------|-----|
| `bug` | Defect |
| `enhancement` | Feature or improvement |

## BeerMe program metadata

Use on phase work — not a substitute for triage state.

| Label | Use |
|-------|-----|
| `prd:v1.6.0` | Pinned PRD version (update per phase) |
| `phase-1-foundation` … `phase-4-polish` | Phase milestone |
| `phase-5-*` | Future phases — create before filing slices |
| `priority:P0` … `priority:P3` | Priority |
| `size:S` / `size:M` / `size:L` | Ticket size (board: **S only** at kickoff) |
| `HITL` / `AFK` | Human vs agent-pickable (also in issue body) |
| `ralph-ready` | Eligible for Ralph loop |
| `ralph-batch` | Parent batch issue |
| `blocked` | Blocker documented on board |

## Mapping rules

- **`triage` skill** applies triage **role** labels only unless maintainer overrides.
- **`to-issues`** publishes AFK slices with `ready-for-agent` unless marked HITL.
- Do not use phase labels as triage state — an issue can be `ready-for-agent` and `phase-5-pdf-export` simultaneously.
