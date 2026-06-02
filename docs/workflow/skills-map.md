# Practical Office skills + seven-phase SOP map

Source: [Practical-Office/cursor-skills](https://github.com/Practical-Office/cursor-skills) (25 skills). Install once per machine:

```bash
git clone https://github.com/Practical-Office/cursor-skills.git
cd cursor-skills && ./scripts/install.sh
```

Per-repo bridge: `docs/agents/*` (from **`setup-practical-ai-skills`**). External/personal skills: `docs/workflow/external-skills.md`.

## By pipeline phase

| Phase | Goal | Skills | Subagent (BeerMe) | Invoke |
|-------|------|--------|-------------------|--------|
| **Setup** | Machine + repo config | `setup-practical-ai-skills`, `setup-pre-commit` | — | Manual `/setup-…` |
| **1 Idea** | Name opportunity | `grill-with-docs`, `zoom-out` | — | Auto; `/zoom-out` manual |
| **2 Research** | Resolve unknowns | `zoom-out`, `diagnose`, explore | domain if defined | Manual where noted |
| **3 Prototype** | Validate taste | `prototype`, `design-an-interface` | `/voyager` or `/orion` | Auto or `/prototype` |
| **4 PRD** | Lock intent | `to-prd`, `grill-with-docs`, `ubiquitous-language` | — | Auto; `/ubiquitous-language` manual |
| **5 Kanban** | Vertical slices on board | `to-issues`, `triage`, `request-refactor-plan` | — | Auto |
| **6 Execution** | Implement tickets | `tdd`, `diagnose`, `review`, `task-handoff`, `handoff`, `create-pr`, `security-secrets-check` | `/orion`, `/engine`, `/voyager` | Mix — see below |
| **7 QA** | Human verify → new issues | `qa`, `release-readiness` | `/verify` (readonly) | `/qa` auto; gates manual |
| **Post-cycle** | ACR, PRD bump | `handoff`, `task-handoff`, `improve-codebase-architecture` | — | Manual |

## BeerMe execution loop

| SOP step | Skill / subagent |
|----------|------------------|
| Session start | `@AGENTS.md`, `@CONTEXT.md` |
| LLM ticket | `/orion` + `tdd` |
| Engine ticket | `/engine` + `tdd` |
| UI ticket | `/voyager` + `tdd` or `prototype` |
| Ralph AFK batch | `tdd` per story; board **Verify** |
| Pre-PR | `security-secrets-check`, `review`, `create-pr` |
| Phase close | `/verify` + `release-readiness` + smoke HITL |
| Session swap | `handoff` → `docs/session-handoff.md` |
| Phase handoff (SOP) | `docs/phases/{phase}/handoff-to-acr.md` (not `handoff` skill alone) |
| ACR PRD bump | `to-prd` in architect chat |

## Manual-only skills (type explicitly)

`setup-practical-ai-skills`, `zoom-out`, `ubiquitous-language`, `task-handoff`, `create-pr`, `security-secrets-check`, `release-readiness`

## N/A for BeerMe

`tenant-isolation-check` — single-user local app. See `external-skills.md`.

## Update skills

```bash
cd cursor-skills && git pull && ./scripts/install.sh
```

Remove legacy `~/.cursor/skills/setup-matt-pocock-skills` symlink if present — use `setup-practical-ai-skills`.
