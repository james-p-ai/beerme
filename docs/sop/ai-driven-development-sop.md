# AI-Driven Development SOP

## Purpose

This SOP defines a **seven-phase pipeline** for shipping software with AI coding assistants. Work moves in order from idea to QA, with optional team governance (phase kickoff, ACR, handoff) layered on without changing the core sequence.

**Primary ordering (always follow this sequence):**

```
1. Idea → 2. Research → 3. Prototype → 4. PRD → 5. Kanban → 6. Execution → 7. QA
                                                                              ↓
                                                                (new tickets → 5 → 6 → 7)
```

Phase 7 loops back to Phase 5 until QA passes. After a release slice is stable, optional **post-cycle** steps update the PRD and start the next idea.

This SOP is a team-level operating system for AI-assisted development, not a personal checklist.

**Tools:** **Cursor** runs the pipeline (repo, skills, board, code). Optionally use **ChatGPT** for **Phase 1 (Idea)** brainstorming and to **refine a Cursor prompt** when the built-in example or a skill output does not quite match what you need — then paste the refined prompt into Cursor.

**Agent and skill sources (install once, use every pipeline run):**

| Layer | Source | Role in this SOP |
| ----- | ------ | ---------------- |
| **Doctrine** | Project `AGENTS.md` | Non-negotiables, domain boundaries, team routing, release gates |
| **Skills** | [Practical-Office/cursor-skills](https://github.com/Practical-Office/cursor-skills) | Phase workflows: PRD, Kanban, TDD, QA, handoff, release checks |
| **Per-repo bridge** | `docs/agents/` (scaffolded by `setup-practical-ai-skills`) | Issue tracker, triage labels, domain glossary paths — skills read these, not chat memory |
| **Team subagents** (optional) | `.cursor/agents/*.md` | Route domain-boundary work in large monorepos; one subagent per ticket in Phase 6 |

**Reference implementations:**

| Repo | Pattern | When to copy |
| ---- | ------- | ------------ |
| [Book-IQ/bookiqv1-rc](https://github.com/Book-IQ/bookiqv1-rc) | Six-team subagents + multi-context monorepo doctrine | Hard domain boundaries (ledger, AI, infra, QA) |
| [james-p-ai/beerme](https://github.com/james-p-ai/beerme) | Single-repo, four domain subagents + verify, GitHub project board | Solo or small team; vertical-slice Kanban on one app |

---

## Scope

### In scope

- New features, products, and substantial enhancements
- Work that benefits from research, prototyping, a PRD, Kanban tickets, agent execution, and human QA
- PRD-driven phases with board tracking and feedback loops

### Out of scope

- Emergency hotfixes (start at Phase 1 with a narrow idea; skip to Execution if fix is obvious)
- Pure infra with no product intent (separate addendum)
- Single-line typo fixes (Idea → Execution only, no PRD/Kanban ceremony)

---

## Phase overview

| # | Phase | Goal | Primary artifact | Skills (Practical Office) | Optional subagent |
| --- | --- | --- | --- | --- | --- |
| **1** | Idea | Name the problem or opportunity | Idea note or issue | `grill-with-docs`, `zoom-out` | — |
| **2** | Research | Resolve unknowns before building | `docs/research/{topic}.md` | `zoom-out`, `diagnose`, explore | Domain agent if repo defines one |
| **3** | Prototype | Validate approach and taste | Throwaway prototype + decision notes | `prototype`, `design-an-interface` | UX/domain agent |
| **4** | PRD | Lock end-state product intent | Versioned PRD + glossary updates | `to-prd`, `grill-with-docs`, `ubiquitous-language` | Architect chat (human) |
| **5** | Kanban | Break PRD into dependency-linked tickets | Board + `docs/phases/{phase}/wbs.md` | `to-issues`, `triage`, `request-refactor-plan` | — |
| **6** | Execution | Implement tickets from the board | Merged PRs, Done column | `tdd`, `diagnose`, `review`, `task-handoff`, `handoff`, `create-pr`, `security-secrets-check`, `tenant-isolation-check` | Team subagent per domain |
| **7** | QA | Human verification; feed fixes back to board | QA plan + new issues | `qa`, `release-readiness`, `tenant-isolation-check` | QA/release agent (e.g. Polaris) |

**Post-cycle** (after Phase 7 passes): Phase Delta Report, handoff to ACR, PRD bump, architect sign-off. Skills: `handoff`, `task-handoff`, `caveman-compress`, `improve-codebase-architecture` (deferred debt).

**One-time setup** (before Phase 1): Install cursor-skills on the machine; run `setup-practical-ai-skills` once per repo; commit root `AGENTS.md` + `docs/agents/*`. Optional: `setup-pre-commit` after repo scaffold exists.

---

## Governance roles (optional layer)

These roles sit across phases; they do not reorder them.

| Role | Responsibility |
| ---- | -------------- |
| **Architect** | Owns PRD intent, approves PRD versions, signs off phases |
| **Engineering lead** | Owns board quality, kickoff gate, WIP limits |
| **Engineer / operator** | Runs Cursor sessions per phase |
| **ACR** | Turns completed work into next PRD revision |
| **Reviewer / tech lead** | PR review, scope compliance; invoke `review` skill before merge |

---

## Agent and skill setup

Install before running the seven-phase pipeline. Skills live on the machine; doctrine and bridge docs live in the repo.

### 1. Install Practical Office skills (once per machine)

```bash
git clone https://github.com/Practical-Office/cursor-skills.git
cd cursor-skills
./scripts/install.sh
```

- Symlinks every skill → `~/.cursor/skills/<name>/`
- Optional project copy: `./scripts/install.sh --project` (from app repo root)
- Update: `git pull && ./scripts/install.sh`
- Do **not** put org skills under `~/.cursor/skills-cursor/` (Cursor built-ins)

### 2. Scaffold per-repo agent config (once per app)

In Cursor, invoke **`setup-practical-ai-skills`** (manual only — `disable-model-invocation`).

Creates or updates:

- `docs/agents/issue-tracker.md` — which tracker, repo, `gh` conventions
- `docs/agents/triage-labels.md` — `ready-for-agent`, `ready-for-human`, etc.
- `docs/agents/domain.md` — where glossary / CONTEXT / ADRs live
- `## Agent skills` section in root `AGENTS.md` or `CLAUDE.md`

Skills like `to-issues`, `triage`, and `tdd` read `docs/agents/` — keep Kanban program docs (`docs/build/`, phase WBS) separate from GitHub triage labels.

### 3. Commit project doctrine (`AGENTS.md`)

Use [Book-IQ/bookiqv1-rc AGENTS.md](https://github.com/Book-IQ/bookiqv1-rc/blob/main/AGENTS.md) as the **mature monorepo** template. Use [james-p-ai/beerme AGENTS.md](https://github.com/james-p-ai/beerme/blob/main/AGENTS.md) as the **small single-app** template.

Every repo should include:

- Product vision and non-negotiables (what AI must never do)
- Build/test commands and scope rules
- Pointers to `docs/agents/`, release gates, handoff templates

Monorepos additionally need:

- Domain boundaries (which service/module owns writes)
- Team subagents in `.cursor/agents/` with `/name` routing
- Cursor workflow: context pack → plan mode for high-risk → one branch per task → handoff → QA agent → PR

### 4. BookIQ agent doctrine and subagents

**Canonical repo:** `Book-IQ/bookiqv1-rc` — v2 code under `services/`; deploys to AWS EKS. Read legacy code from `legacy/` only; do not commit v2 work to standalone `bookiq-*` repos.

#### Six teams

| Team | Domain | Invoke | SOP phases |
| ---- | ------ | ------ | ----------- |
| **Atlas** | AWS EKS, DevOps, security foundation | `/atlas` | Phase 6 — infra, CI, secrets, deploy |
| **Titan** | Ledger, controls, CPA-grade accounting core | `/titan` | Phase 6 — business logic, deterministic rules, audit |
| **Orion** | OMI, AI orchestration, LLM governance | `/orion` | Phases 3–6 — prompts, extraction, citations; **no silent writes** to domain stores |
| **Odyssey** | Integrations, ingestion, jobs, sync | `/odyssey` | Phases 2, 6 — external APIs, sync workers |
| **Voyager** | Frontend, UX, owner & reviewer experience | `/voyager` | Phases 3, 6 — UI, UX polish |
| **Polaris** | QA, E2E, UAT, release control, trust gates | `/polaris` | Phase 6 exit + Phase 7; **may block merge** |

Subagent definitions live in `.cursor/agents/{atlas,titan,orion,odyssey,voyager,polaris}.md`. Each file declares mission, owned domains, explicit non-ownership, and required boundaries.

#### Global non-negotiables (BookIQ)

1. **AI proposes; humans and deterministic accounting decide.**
2. **Ledger math is deterministic** (Decimal-safe, balanced double-entry).
3. **Ledger Service is the only writer** to `journal_entries`, `journal_lines`, `chart_of_accounts`, and `period_locks`.
4. **AI must never silently post** to the ledger or create chart-of-accounts rows.
5. **Every financial mutation must be audit-logged.**
6. **Every dollar OMI states must cite** a source row, journal line, report row, transaction, invoice, bill, payment, or reconciliation record.
7. **Every LLM call must be logged** with tenant, user context, model, prompt version/hash, tool calls, output hash, tokens, latency, and redaction metadata.
8. **Every tenant-scoped service must honor selected tenant context** (no primary-tenant fallback).
9. **Plaid and external OAuth tokens encrypted at rest**; no raw external tokens in browser responses.
10. **Closed periods are locked.**
11. **QBO push requires dry-run, explicit approval, and audit.**
12. **No production release** without E2E, UAT, tenant isolation, security, accounting, and AI safety gates (Polaris).

#### Domain boundaries (encode in every BookIQ task)

| Boundary | Rule | Owners |
| -------- | ---- | ------ |
| AI accounting | Orion may suggest, explain, summarize, cite read-only data — not write JEs, J-lines, CoA, period locks, or QBO writes | Orion + Titan |
| Tenant isolation | `X-Tenant-ID` mandatory; cross-tenant reads/writes are release blockers | All backend + Polaris |
| Security | No secrets in Git; PII redacted before external LLM; least-privilege on EKS | Atlas + Odyssey |
| Deterministic ledger | Titan Ledger Service owns all financial truth mutations; trial balance, reconciliation, period close | Titan |
| Citations | OMI monetary answers require structured citations before display | Orion validates; Voyager shows; Polaris tests |
| Release | Definition of done: `docs/cursor-teams/RELEASE_GATES.md` + `.cursor/rules/08-definition-of-done.mdc` | Polaris |

#### BookIQ Cursor workflow

1. Read `docs/cursor-teams/CONTEXT_PACK.md`, `REPOSITORY_POLICY.md`, and relevant `team-guides/`.
2. Plan mode for multi-file or high-risk work.
3. One branch or worktree per team task.
4. Implement with owning team subagent (`/titan`, `/orion`, etc.).
5. Handoff → **Polaris validation** → PR review → merge.

**General rule:** one ticket → one chat → one subagent (if used). Subagents enforce doctrine; skills enforce procedure.

**Build program vs GitHub triage:** BookIQ keeps program Kanban in `docs/build/MASTER_BUILD_BOARD.md` separate from GitHub Issues triage labels. Skills read `docs/agents/issue-tracker.md` for the GitHub layer.

### 5. BeerMe process (single-repo pattern)

BeerMe is the **reference single-app implementation** of this SOP — four domain subagents (`/orion`, `/engine`, `/voyager`, `/verify`), single-context doctrine, GitHub project board. Agent doctrine landed in [PR #86](https://github.com/james-p-ai/beerme/pull/86); Phase 5 PDF export pilot exercises subagent routing per ticket.

| Artifact | Location |
| -------- | -------- |
| PRD | `docs/prd/PRD.md` |
| Domain glossary | `CONTEXT.md` |
| Kanban guide | `docs/github/KANBAN.md` |
| Issue tracker setup | `docs/agents/issue-tracker.md` |
| Triage labels | `docs/agents/triage-labels.md` |
| Agent entrypoint | `AGENTS.md` — non-negotiables, domain zones, workflow |
| Subagents | `.cursor/agents/{orion,engine,voyager,verify}.md` |
| Cursor rules | `.cursor/rules/*.mdc` — master doctrine + glob boundaries |
| Cursor teams docs | `docs/cursor-teams/` — usage guide, release gates, handoff template |
| Agent doctrine pilot runbook | `docs/sop/agent-doctrine-pilot.md` |
| Phase handoffs | `docs/phases/{phase}/handoff-to-acr.md` |
| Phase WBS | `docs/phases/{phase}/wbs.md` |
| Session handoff | `docs/session-handoff.md` |

#### When to add subagents

| Project shape | Subagents | Rules |
| ------------- | --------- | ----- |
| Single app (BeerMe) | 3 domain + 1 verify (`/orion`, `/engine`, `/voyager`, `/verify`) | 4 `.mdc` files |
| Monorepo (BookIQ) | 6 teams + Polaris | 8+ rules + CONTEXT_PACK |

Add subagents when **hard domain boundaries** exist (LLM vs deterministic core vs UI vs QA). Skip subagents for tiny scripts or docs-only repos — default agent + skills is enough.

**Board:** [BeerMe Kanban](https://github.com/users/james-p-ai/projects/2)  
**Repo:** `james-p-ai/beerme`

#### BeerMe subagents (Phase 5+)

| Subagent | Domain | Owned paths |
| -------- | ------ | ----------- |
| `/orion` | LLM layer | `app/ollama_client.py`, `app/prompts.py` |
| `/engine` | Deterministic core | `app/taste_profile.py`, `app/recommender.py`, `data/*` |
| `/voyager` | UI + export UX | `app/main.py`, `app/export_md.py`, `app/export_pdf.py` |
| `/verify` | QA (readonly) | pytest, smoke, release gates — no feature code |

One ticket → one chat → one subagent when the ticket crosses a zone boundary.

#### BeerMe phase model (v1.6.0 reference)

| Phase | Epic / theme | Handoff |
| ----- | ------------ | ------- |
| Phase 1 — Foundation | Epic #1 | `docs/phases/phase-1-foundation/handoff-to-acr.md` |
| Phase 2 — Taste engine | taste profile, axes, confidence | `docs/phases/phase-2-taste-engine/handoff-to-acr.md` |
| Phase 3 — Catalog + recs | catalog, style tree, scoring | `docs/phases/phase-3-catalog-recs/handoff-to-acr.md` |
| Phase 4 — Polish | question bank, refining, MD export | `docs/phases/phase-4-polish/handoff-to-acr.md` |
| Phase 5 — PDF export | PDF download, export helpers, agent pilot | `docs/phases/phase-5-pdf-export/handoff-to-acr.md` |

For Phase 6+, create a new phase epic before filing slice issues.

#### BeerMe label schema

Align with `docs/agents/triage-labels.md`:

**Category (one):** `bug` | `enhancement`

**Triage state (one):** `needs-triage` | `needs-info` | `ready-for-agent` | `ready-for-human` | `wontfix`

**Phase metadata (required on phase work):**

| Field | Example |
| ----- | ------- |
| Phase label | `phase-5-pdf-export` |
| PRD version | `prd-v1.7.0` or `prd:v1.6.0` |
| Priority | `P0` … `P3` or `priority:P0` |
| Type | `HITL` or `AFK` |
| Work group | `P5-M1` (optional) |

Use domain terms from `CONTEXT.md` in every issue body (taste profile, taste axis, session confidence, catalog, style node, question turn, etc.).

#### BeerMe Kanban columns

```
Backlog → Triage → Ready → In Progress → In Review → Done
                         ↘ Blocked ↗
```

| Column | BeerMe rule |
| ------ | ----------- |
| **Backlog** | Filed from `to-issues`; not kickoff-approved |
| **Triage** | Has `needs-triage` or missing metadata |
| **Ready** | `ready-for-agent` or `ready-for-human`; DoR complete |
| **In Progress** | WIP 1–2 per human; agent session = 1 issue |
| **In Review** | PR open; reference issue # in PR title/body |
| **Blocked** | Blocker comment; 24h/48h escalation per SOP |
| **Done** | PR merged; `PYTHONPATH=. pytest -q` green for touched areas |

Filter board by **phase label** or **phase epic** to see one phase at a time.

#### BeerMe phase flow (Phases 5–7 of this SOP)

0. **PRD bump** — architect updates `docs/prd/PRD.md` header (version, active phase, changelog)
1. **Kickoff draft** — `docs/phases/phase-N-{name}/kickoff.md`
2. **Decompose** — `/to-issues` with PRD + kickoff + `CONTEXT.md` + triage labels; quiz before publish
3. **WBS snapshot** — `docs/phases/phase-N-{name}/wbs.md` committed
4. **Kickoff approval gate** — phase epic on board; all slices S-sized; dependencies valid
5. **Execution** — one chat per issue; `/tdd`; PR title `feat(scope): … (#NN)`
6. **Board sync** — weekly planning chat updates WBS from GitHub project 2
7. **Phase close** — `delta-report.md` + `handoff-to-acr.md` → ACR → PRD bump

#### BeerMe smoke and human gates

Some slices are **HITL** by nature — file as explicit board issues, not hidden in chat:

- Manual smoke: `ollama pull llama3.2:3b`, `./run.sh`, `bash scripts/qa/beerme-smoke.sh`
- Architect sign-off in PRD header
- Demo-ready checklist before phase close

#### BeerMe Ralph loop (optional AFK pattern)

For batch agent runs, BeerMe uses a Ralph-style loop on labeled issues (`ralph-ready`):

1. Pick open `ralph-ready` issue in **Ready**
2. Implement one story from `scripts/ralph/prd.json`
3. Run `pytest`; set story `passes: true`
4. Move parent to **Verify** on board
5. Human approves → **Done**

Filter: `is:open label:ralph-ready`. One issue per agent session.

#### BeerMe anti-patterns

- Personal markdown backlog instead of board — **board wins**
- Horizontal tickets ("add all tests for phase") — use vertical slices
- Skipping `CONTEXT.md` terms in issues — agents drift on vocabulary
- One long Cursor chat for whole phase — one chat per issue
- Closing phase before smoke HITL issue Done
- M/L issues on board at kickoff — split first

Full detail: `beerme-kanban-playbook.md` in repo or team docs folder.

### 6. Skill invocation modes

| Mode | Skills | How |
| ---- | ------ | --- |
| **Auto** | `tdd`, `to-prd`, `to-issues`, `triage`, `qa`, `diagnose`, `prototype`, `grill-with-docs`, `handoff`, `review`, … | Agent loads when description matches task |
| **Manual only** | `setup-practical-ai-skills`, `zoom-out`, `ubiquitous-language`, `task-handoff`, `create-pr`, `security-secrets-check`, `tenant-isolation-check`, `release-readiness` | Type `/skill-name` — agent will not auto-pick |

---

## Practical Office skills — full inventory

Source: [Practical-Office/cursor-skills](https://github.com/Practical-Office/cursor-skills). Install once per machine; skills symlink to `~/.cursor/skills/<name>/`.

### Pipeline skills (use every cycle)

| Skill | Purpose | Typical phase | Invoke |
| ----- | ------- | ------------- | ------ |
| `setup-practical-ai-skills` | Scaffold `docs/agents/` + `## Agent skills` block | Setup | Manual only |
| `setup-pre-commit` | Husky + lint-staged + typecheck + tests at commit | Setup | Manual |
| `grill-with-docs` | Interview on ambiguities; update CONTEXT/ADRs inline | 1, 4 | Auto |
| `grill-me` | Stress-test a plan without doc updates | 1, 4 | Auto |
| `zoom-out` | Codebase-wide module map and orientation | 1, 2 | Manual |
| `diagnose` | Reproduce → minimise → hypothesise → fix loop | 2, 6 | Auto / manual |
| `prototype` | Throwaway terminal or UI validation | 3 | Auto |
| `design-an-interface` | Radically different UI variations on one route | 3 | Auto |
| `to-prd` | Synthesize PRD from conversation + repo context | 4 | Auto |
| `ubiquitous-language` | Formal domain glossary | 4 | Manual |
| `to-issues` | PRD/plan → vertical-slice GitHub issues | 5 | Auto |
| `triage` | Issue state machine with triage roles | 5, 7 | Auto |
| `request-refactor-plan` | Interview → single refactor issue | 5 | Auto |
| `tdd` | Red → green → refactor implementation | 6 | Auto |
| `review` | Standards + spec review since a branch/commit | 6 | Auto |
| `task-handoff` | Structured handoff for multi-session tickets | 6 | Manual |
| `handoff` | Compact session summary for next chat | 6, post-cycle | Auto |
| `create-pr` | `gh pr create` with Summary + Test plan | 6 | Manual |
| `security-secrets-check` | Scan diff for leaked secrets | 6 | Manual |
| `tenant-isolation-check` | Multi-tenant boundary review | 6, 7 | Manual |
| `qa` | Conversational bug filing with domain language | 7 | Auto |
| `release-readiness` | Pre-merge/release gate checklist | 7 | Manual |
| `improve-codebase-architecture` | Deepening/refactor opportunities from CONTEXT | Post-cycle | Auto |
| `write-a-skill` | Author new Cursor skills | Any | Auto |

### Token-efficiency skills (optional; not in Practical-Office repo)

| Skill | Purpose | When |
| ----- | ------- | ---- |
| `caveman-compress` | Compress natural-language `.md` memory files | Post-cycle handoffs, large CONTEXT loads |
| `caveman-commit` | Ultra-compressed commit messages | Commits |
| `caveman-review` | One-line PR review comments | Review |
| `/summarize` | Cursor built-in — compress in-chat context | Long ticket chats at ~50–70% meter |

### Integration skills (outside core pipeline)

Not required for the seven-phase SOP. Use when the task explicitly involves these tools:

- **Notion workspace** — `search`, `create-task`, `tasks-plan`, `tasks-build`, `spec-to-implementation`, …
- **Figma** — `figma-use`, `figma-generate-design`, `figma-generate-diagram`, …
- **Datadog** — `ddsetup`, `ddconfig`, observability MCP tools

---

## Phase 1: Idea

**Goal:** Development starts with a reason to invoke the AI — a product concept, feature, bug fix, refactor, or experiment. Capture it before research or code.

### Entry criteria

- A person or stakeholder has a problem, opportunity, or task worth pursuing

### Activities

1. Open a dedicated idea chat (do not mix with implementation).
2. State the idea in one paragraph: who it helps, what changes, why now.
3. Classify scope:
   - **Product** — needs full pipeline (Phases 2–7)
   - **Focused** — bug, small feature, refactor (may skip Research and/or Prototype)
4. Record the idea:
   - GitHub issue titled `Idea: …`, or
   - `docs/ideas/{slug}.md`, or
   - Conversation handoff note for next session

### Exit criteria

- Idea is written down with clear enough scope to decide: research needed or not?
- Decision logged: full pipeline vs short path (which later phases to skip)

### Example prompt

```text
/grill-with-docs

I want to explore [idea]. One-paragraph problem statement + open questions.
Do not write code or a PRD yet.
```

For codebase-wide orientation before research: `/zoom-out` (manual).

### Short-path skips

| Idea type | Typical skip |
| --------- | ------------ |
| Obvious bug with known fix | Research, Prototype, PRD → go to Kanban (single issue) or Execution |
| Tiny refactor | Research, Prototype, PRD |
| New product or major feature | None — run full pipeline |

---

## Phase 2: Research

**Goal:** When the idea involves unknowns — external APIs, unfamiliar domains, legal constraints, performance limits — investigate before prototyping or PRD. Cache findings so agents reuse them.

### Entry criteria

- Phase 1 complete
- At least one open question that code exploration or docs alone cannot answer quickly

### Activities

1. Open a research chat scoped to the unknowns list from Phase 1.
2. Investigate: codebase (explore), `/zoom-out` for module map, official docs, APIs, prior art in repo ADRs.
3. For production bugs blocking research: `/diagnose` (reproduce → hypothesise → fix path — still no feature code).
4. Write **`docs/research/{topic}.md`** with:
   - Question being answered
   - Findings (facts, links, constraints)
   - Recommendations (proceed / pivot / blocked)
   - Open questions remaining
5. Update `CONTEXT.md` or ADRs if terminology or decisions crystallize.

### Exit criteria

- No blocking unknowns remain for prototyping or PRD, or remaining unknowns are explicitly accepted as PRD risks
- `research.md` (or equivalent) committed and linked from the idea issue

### Example prompt

```text
Research phase for [idea].

Open questions:
[list from Phase 1]

1. Explore this repo for prior art.
2. Summarize external constraints for [API / domain].
3. Write docs/research/[topic].md with findings and recommendations.
4. List what still requires a prototype vs what we can put in the PRD.

Do not prototype or write production code.
```

**Skip:** If Phase 1 classified the work as a short path with no unknowns, skip to Phase 3 or 4.

---

## Phase 3: Prototype

**Goal:** Before committing to production implementation, validate what you are building and impose taste — especially UI, state models, and interaction feel. Prototypes answer questions; they are not the shipment.

### Entry criteria

- Phase 2 complete (or skipped with documented reason)
- At least one decision that is cheaper to validate in throwaway code than in a PRD argument

### Activities

1. Invoke the **`prototype`** skill (or `/design-an-interface` for UI-only taste comparisons).
2. Pick branch:
   - **Logic** — terminal app, state machine, data model
   - **UI** — multiple variations on a throwaway route
3. Run prototype locally; iterate with the human until decisions land.
4. Capture the verdict (what we learned, what we rejected) in:
   - Prototype `NOTES.md`, or
   - Issue comment, or
   - Inline PRD draft notes
5. Either delete throwaway code or commit it clearly marked `PROTOTYPE` for agent reference during Phase 6.

### Exit criteria

- Key design questions answered (look, feel, state model, API shape)
- Verdict written down; prototype deleted or marked throwaway
- Human sign-off: "ready to describe end state in PRD"

### Example prompt

```text
/prototype

Question: [what we're validating from research or idea]

Build throwaway [UI variations | terminal state explorer]. One command to run. No tests. Surface full state after each action.

When done, summarize the verdict: what we ship vs what we rejected.
```

**Skip:** Skip when the change is mechanical (bug fix, copy change) or when research already proved the approach with no taste judgment needed.

---

## Phase 4: PRD

**Goal:** Describe the end state of the product slice: problem, solution, user stories, implementation and testing decisions, out of scope. Decisions must be solid before Kanban decomposition.

### Entry criteria

- Phase 3 complete (or skipped)
- Prototype verdict and research docs available to the agent

### Activities

#### 4a. Draft PRD

1. Open a PRD chat with: idea issue, `docs/research/*`, prototype notes, `CONTEXT.md` (or `docs/agents/domain.md` paths).
2. Run **`to-prd`** to synthesize a draft PRD (or write manually using team template).
3. Run **`/ubiquitous-language`** if the domain needs a formal glossary → `UBIQUITOUS_LANGUAGE.md` or update `CONTEXT.md`.
4. Save versioned PRD, e.g. `docs/prd/PRD.md`, with header block:
   - Version (e.g. v1.4.0)
   - Date, Author, Summary of changes
   - Active phase(s) enabled by this version

#### 4b. Grill (mandatory for product work)

Before approving the PRD, run **`grill-with-docs`**:

- Agent interviews you on every ambiguous branch
- Updates `CONTEXT.md` and ADRs inline as decisions land
- Surfaces conflicts with research or prototype verdict

Do not proceed to Kanban until grilling resolves blocking ambiguities.

#### 4c. Approve PRD

- Architect approves version and scope
- Changelog entry: what changed, why, affected phases
- Publish PRD issue on tracker if team uses one

### Exit criteria

- Approved, versioned PRD committed
- Glossary and ADRs consistent with PRD language
- No unresolved blocking questions (or explicitly listed as Phase 5/6 risks)

### Example prompt — grill

```text
/grill-with-docs

Stress-test docs/prd/PRD.md v[X.Y.Z] against CONTEXT.md, research docs, and prototype verdict.

Ask one question at a time. Update CONTEXT.md when we decide. Stop when PRD is ready for to-issues.
```

**Team extension:** Large PRDs ship in phases (e.g. Phase 1 Foundation, Phase 2 Taste Engine). Each phase gets its own kickoff in Phase 5 — but Phase 4 must list phases and goals in the PRD first.

---

## Phase 5: Kanban

**Goal:** Break the approved PRD (or active PRD phase) into small vertical-slice tickets on a Kanban board with blocking relationships, assignees, and priorities. The board becomes the live implementation plan.

### Entry criteria

- Approved PRD version
- Active phase identified (for multi-phase PRDs)

### Activities

#### 5a. Phase kickoff (team extension)

Draft `docs/phases/{phase-name}/kickoff.md`:

- PRD version, phase goal, in/out of scope, risks
- Link to board and future WBS

Kickoff is draft until board passes approval gate below.

#### 5b. Decompose with Cursor (`to-issues`)

1. Phase planning chat — one per phase.
2. Invoke **`to-issues`** against PRD + kickoff + assignment docs.
3. Rules for every ticket:
   - **Vertical slice** — end-to-end tracer bullet, not horizontal layer
   - **Size S only** on board; split M/L before approval
   - **Type:** HITL (human judgment) or AFK (agent-pickable)
   - **Priority:** P0–P3
   - **Assignee:** human or agent
   - **Blocked by:** issue refs (publish in dependency order)
   - **Labels:** phase, `prd-vX.Y.Z`, work group optional
4. Quiz human on granularity and dependencies before publishing.
5. Publish issues to tracker; link to phase epic.
6. Triage: **`triage`** → `ready-for-agent` or `ready-for-human` (labels must match `docs/agents/triage-labels.md`).
7. Refactor-only tracks: **`/request-refactor-plan`** → interview → single GitHub issue before Phase 6.

#### 5c. WBS snapshot

Commit `docs/phases/{phase-name}/wbs.md`:

- Work groups and exit criteria
- Dependency order
- Issue index table

#### 5d. Kickoff approval gate

Architect + engineering lead approve when:

- All in-scope work is on the board
- Metadata complete; dependencies valid; no cycles
- No M/L issues remain
- WBS committed

### Board model

**Source of truth:** Kanban board. WBS and kickoff are references.

**Columns:** Backlog → Triage → Ready → In Progress → In Review → Done  
                         ↘ Blocked ↗

| Column | Meaning |
| ------ | ------- |
| **Backlog** | Filed, not kickoff-approved |
| **Triage** | Needs labels, sizing, or triage |
| **Ready** | Definition of Ready met |
| **In Progress** | WIP limited (1–2 per human, 1 per agent session) |
| **In Review** | PR open |
| **Blocked** | Blocker documented; 24h/48h escalation |
| **Done** | Merged and verified |

### Definition of Ready (ticket)

- On board, linked to phase epic
- Phase + PRD version + priority + assignee + type
- Valid Blocked by (or none)
- Size S; acceptance criteria in body
- HITL: plan approved | AFK: `ready-for-agent`

### Exit criteria

- Board approved at kickoff gate
- At least one issue in Ready to start Phase 6

### Example prompt

```text
/to-issues

PRD: docs/prd/PRD.md (vX.Y.Z). Phase: [name]. Kickoff: docs/phases/[phase]/kickoff.md.

Vertical slices only, size S. HITL/AFK, P0–P3, assignees, Blocked by, phase labels.
Quiz me before publishing to GitHub.
```

---

## Phase 6: Execution

**Goal:** Implement tickets from the Kanban board — by human engineers, coding agents, or both — until all in-scope execution tickets for the current slice are Done.

### Entry criteria

- Phase 5 kickoff approved
- Issues in Ready column

### Activities

#### 6a. Pull model (human)

1. **One new chat per ticket** — never one chat for whole phase.
2. From phase planning chat, pull your Ready queue (assignee filter, respect Blocked by, P0 first).
3. **Route domain work:** if repo defines team subagents (BookIQ pattern), invoke `/[team]` for that ticket's boundary — e.g. `/voyager` for UI tickets; `/polaris` implements verification only, not features.
4. **Plan before code:** investigate repo; 3–8 subtasks; validate plan against issue scope. Risky or multi-session tickets: `/task-handoff` (prefer repo `TASK_HANDOFF_TEMPLATE.md`).
5. **Build:** `/tdd` — red → green → refactor; one subtask at a time.
6. **Debug:** `/diagnose` for bugs or perf regressions on the ticket.
7. **Pre-PR gates:** `/security-secrets-check` on diff; `/review` vs issue + plan; multi-tenant apps: `/tenant-isolation-check`.
8. **Open PR:** `/create-pr` (Summary, Test plan, `#issue` ref).
9. Move issue Ready → In Progress → In Review → Done on merge.
10. Small commits; persist mini-specs: `docs/phases/{phase}/tickets/{n}-mini-spec.md`.
11. After merge: sync board + WBS. Context pressure: `/summarize` or `/handoff`.

#### 6b. Execution loop (agent / AFK / "Ralph loop")

For autonomous away-from-keyboard runs:

```text
EXECUTION LOOP — repeat until no eligible work:

1. Query board: Ready + ready-for-agent + unblocked + current phase label
2. If none: STOP (proceed to Phase 7 or wait for human)
3. Pick highest-priority issue
4. New chat scoped to that issue only (+ team subagent if repo defines routing)
5. Plan → `/tdd` implement → `/security-secrets-check` → `/create-pr` → In Review
6. Human or CI merges → Done
7. GOTO 1
```

**HITL** issues (`ready-for-human`) are never picked by the autonomous loop — only humans.

BeerMe Ralph variant: filter `ralph-ready` label; implement one story; human moves to Verify → Done.

#### 6c. Plan and build prompts

**Plan:**

```text
Issue #[N]: [title + body]. PRD excerpt: [paste]. Plan only — 3–8 subtasks, files, tests. No code.
```

**Build:**

```text
/tdd

Implement subtask [k] only from approved plan. Stay in issue scope. Stop when subtask done.
```

#### 6d. Review checklist

- PR maps to issue # and phase
- Matches plan; no scope creep (`review` skill or human)
- `/security-secrets-check` clean; multi-tenant: `/tenant-isolation-check` if applicable
- Tests verify acceptance criteria
- Deviations noted for delta report

### Exit criteria

- All in-scope execution tickets for the phase/slice are Done
- Tests passing; no open regressions on merged work
- Board reflects Done state

**Proceed to Phase 7: QA.** Do not close the product slice until QA passes.

---

## Phase 7: QA

**Goal:** After execution, a human verifies the work. QA surfaces gaps, bugs, and polish issues. Findings become new Kanban tickets and re-enter Phase 5 → 6 → 7 until pass.

### Entry criteria

- Phase 6 execution complete for current slice
- Build is runnable and test suite green at repo level

### Activities

#### 7a. Generate QA plan

Agent produces a QA plan from PRD acceptance criteria, user stories, and what shipped:

```text
Execution complete for phase [name]. PRD vX.Y.Z.

Generate a QA plan for a human tester:
- Prerequisites (env, commands, test accounts)
- Checklist mapped to PRD user stories
- Edge cases from research and prototype verdict
- Explicit out-of-scope reminders

Do not file issues yet.
```

Save as `docs/phases/{phase}/qa-plan.md` or attach to phase epic.

#### 7b. Human QA session

1. Human runs QA plan (manual smoke, exploratory testing, demo script).
2. Invoke **`/qa`** for conversational bug filing — durable issues, domain language, user-focused acceptance criteria.
3. **Release gate:** `/release-readiness` (honor repo `.cursor/rules/RELEASE_GATES.md` or `AGENTS.md` gates if present); team QA subagent (BookIQ: `/polaris`) for merge-blocking verification.
4. File each finding as a new GitHub issue on the board:
   - Label `bug` or `enhancement`
   - Triage to `ready-for-agent` or `ready-for-human`
   - Set priority, phase label, Blocked by if needed
   - Column: Backlog or Ready (if small and clear)

BeerMe smoke: `bash scripts/qa/beerme-smoke.sh` as explicit HITL issue before phase close.

#### 7c. QA loop (mandatory)

**Phase 7 findings → Phase 5 (new/refined tickets) → Phase 6 → Phase 7 again**

Repeat until:

- QA plan checklist fully passed
- No open P0/P1 bugs for the slice
- Human sign-off recorded (issue comment, PRD note, or sign-off issue moved to Done)

#### 7d. Human gates (HITL tickets)

Some verification cannot be delegated:

- Production-like smoke scripts
- Architect demo sign-off
- Accessibility or compliance review

File these as explicit HITL issues during Phase 5 and complete them in Phase 7.

### Exit criteria

- QA plan passed; sign-off documented
- All QA-generated tickets either Done or explicitly deferred to a future PRD phase
- Board stable for the slice

---

## Post-cycle: handoff, ACR, and next idea

After Phase 7 passes, run team closure (does not replace Phases 1–7 ordering on the next slice):

1. **Phase Delta Report** — `docs/phases/{phase}/delta-report.md`: planned vs. actual issues; unplanned work; deferred items
2. **Phase handoff** — `/handoff` or `/task-handoff` → `docs/phases/{phase}/handoff-to-acr.md`. Optionally `/caveman-compress` on saved handoff for agent consumption.
3. **ACR → PRD update** — ACR receives kickoff, delta, handoff. Updates PRD, bumps version, changelog. Architect signs off.
4. **Close phase epic** — Move phase epic to Done on board.
5. **Next cycle** — New work starts again at Phase 1: Idea (or Phase 4 if same PRD, new phase only).

---

## Full cycle diagram

```
 1 Idea → 2 Research → 3 Prototype → 4 PRD → 5 Kanban → 6 Execution → 7 QA
              ↑ skip?        ↑ skip?         grill          ↑              ↑
              └──────────────┴─────────────────┘              │              │
                                                              │         QA fail:
                                                              │    new tickets on board
                                                              └──────────────┘
                                                                    │
                                                                    ↓
                                                              (back to 5 → 6 → 7)

 7 QA pass → post-cycle (delta, handoff, ACR, PRD bump) → next Idea (or Phase 4 for new PRD phase)
```

---

## Definition of Done

### Ticket (Phase 6)

- Implemented within issue scope; tests pass
- PR merged; issue Done on board

### QA slice (Phase 7)

- QA plan passed; sign-off recorded
- No open P0/P1 for slice (or deferred with architect approval)

### Phase / release slice (post-cycle)

- Phases 1–7 complete for agreed scope
- Delta report + handoff to ACR
- PRD updated and signed off

---

## Working rules

1. Never skip phase order without documenting the skip in the idea issue or kickoff.
2. Research → `docs/research/`; PRD → versioned doc; plan → board + WBS; chats → ephemeral.
3. One planning chat per phase; one implementation chat per ticket.
4. Plan before build in Phase 6; validate AI plans against repo and issue scope.
5. QA always loops to Kanban — never "fix in chat" without a ticket.
6. Blocked >24h: Blocked column + comment. >48h: escalate.
7. Board wins over personal markdown backlogs.
8. Context limits — watch the meter; compress or hand off before quality drops (see below).
9. **Doctrine first** — `@AGENTS.md` + `docs/agents/` at session start; skills read repo config, not prior chat.
10. **Subagents for boundaries** — team `.cursor/agents/` when domains split (BookIQ pattern); skills for procedure.
11. **BeerMe pattern** — single-context repos skip subagents; use board + `CONTEXT.md` + phase labels instead.

---

## Context limits and chat continuity

Long agent chats fill the model context window. When full, answers get worse (missed rules, repeated mistakes, scope drift) even before the session hard-stops.

### How to tell you're running out

| Signal | What it means |
| ------ | ------------- |
| Context meter (bottom-right of chat) | % of the current model's window in use. Limit is model-specific. |
| ~50–70% at a natural stop (subtask done, plan approved) | Good time to proactively compress or hand off — don't wait for 100%. |
| ~90–100% | High risk of degradation; compress or start a fresh chat with a handoff artifact. |
| "Summarizing chat context…" banner | Cursor auto-compressed older turns to stay under the limit. |
| Quality drop | Agent ignores issue scope, re-explores repo, contradicts earlier decisions, or hallucinates paths — treat as context pressure even if the meter looks OK. |

**Rule of thumb:** One planning chat per phase; one implementation chat per ticket (Working rule 3). If a single chat outgrows that, you waited too long — split earlier next time.

### Option A — Stay in the same chat (`/summarize`)

Use when you want to keep the thread but free context (same feature, same ticket, mid-flight).

```text
/summarize
```

Cursor summarizes older messages in place. Run at a task boundary — not in the middle of a half-finished change.

Note: Cursor's built-in command is **`/summarize`**. It is not the same as `/caveman-compress` (files on disk, below).

### Option B — Continue in a new chat (handoff + optional caveman-compress)

**Step 1 — Capture session state:**

```text
/handoff

Next session: [e.g. Issue #17 — chat_json retry test, or Phase 7 smoke QA]

Do not duplicate PRD, kickoff, WBS, or issue bodies — reference paths only.
```

**Step 2 — Shrink the handoff file (optional):**

```text
/caveman-compress docs/session-handoff.md
```

**Step 3 — Fresh chat:**

```text
Continue from docs/session-handoff.md (or paste handoff from temp).

Issue #[N]: [title]. PRD: docs/prd/PRD.md vX.Y.Z. Plan only / implement subtask [k] — stay in issue scope.
```

### When to use which

| Situation | Action |
| --------- | ------ |
| Same ticket, same chat, meter ~50–70%, at a stop point | `/summarize` |
| Same ticket but chat already confused or >90% | `handoff` → new chat |
| New ticket (Phase 6 rule) | **New chat always** |
| Post-cycle or long phase close | `handoff` → `caveman-compress` on saved handoff → archive in repo |
| Loading big docs into every chat | `caveman-compress` on memory files — not a substitute for issue-scoped chats |

### What persists without compression

Chats are **ephemeral**. Durable truth stays in the repo and board: PRD, kickoff, WBS, issues, commits, `docs/research/*`, delta/handoff markdown.

---

## Cursor skills map (quick reference)

Full inventory: [Practical Office skills — full inventory](#practical-office-skills--full-inventory) above.

| Phase | Skills | Invoke |
| ----- | ------ | ------ |
| **Setup** | `setup-practical-ai-skills`, `setup-pre-commit`, `write-a-skill` | Manual `/setup-…` |
| **1 Idea** | `grill-with-docs`, `zoom-out` | `grill-with-docs` auto; `/zoom-out` manual |
| **2 Research** | `zoom-out`, `diagnose`, explore | `/zoom-out`, `/diagnose` manual; explore built-in |
| **3 Prototype** | `prototype`, `design-an-interface` | Auto or `/prototype` |
| **4 PRD** | `to-prd`, `grill-with-docs`, `ubiquitous-language` | Auto; `/ubiquitous-language` manual |
| **5 Kanban** | `to-issues`, `triage`, `request-refactor-plan` | Auto |
| **6 Execution** | `tdd`, `diagnose`, `review`, `task-handoff`, `handoff`, `create-pr`, `security-secrets-check`, `tenant-isolation-check` | Mix — see Agent setup §6 |
| **7 QA** | `qa`, `release-readiness`, `tenant-isolation-check` | `/qa` auto; gates manual |
| **Post-cycle** | `handoff`, `task-handoff`, `caveman-compress`, `improve-codebase-architecture` | Manual for compress/architecture |
| **Any long chat** | `/summarize`, `handoff`, `caveman-compress` | Cursor built-in + skills |

### Doctrine and subagents

| Artifact | When to use |
| -------- | ----------- |
| Root `AGENTS.md` | Every session — non-negotiables, boundaries, workflow |
| `docs/agents/*` | Every skill that touches issues, triage, or domain terms |
| `.cursor/agents/*` subagents | Phase 6+ when ticket crosses a domain boundary (BookIQ) |
| `CONTEXT_PACK.md` / `CONTEXT.md` | Phase 2–4 grounding; updated by `grill-with-docs` |
| `RELEASE_GATES.md` | Phase 7 + `/release-readiness` before merge |

---

## Related documents

| Document | Use |
| -------- | --- |
| [Practical-Office/cursor-skills](https://github.com/Practical-Office/cursor-skills) | Install skills; `setup-practical-ai-skills` scaffolds `docs/agents/` |
| [Book-IQ/bookiqv1-rc AGENTS.md](https://github.com/Book-IQ/bookiqv1-rc/blob/main/AGENTS.md) | Monorepo doctrine: six teams, boundaries, release gates, Cursor workflow |
| [james-p-ai/beerme](https://github.com/james-p-ai/beerme) | Single-repo reference: board, labels, Ralph loop, smoke gates |
| `beerme-kanban-playbook.md` | BeerMe labels, board URL, phase flow, anti-patterns |
| `docs/github/KANBAN.md` (BeerMe) | Board bootstrap, Ralph sections, issue index |
| `prd-to-ticket-to-handoff-cycle-sop-kanban.md` | Deep detail on Kanban columns, WIP, kickoff gate |
| `prd-to-ticket-to-handoff-cycle-sop-revised.md` | Original PRD-centric SOP (pre–seven-phase) |
