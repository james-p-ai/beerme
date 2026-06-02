# BeerMe — Cursor Agent Doctrine

Local Streamlit + Ollama beer taste quiz with hierarchical recommendations from a static catalog.

**Repo:** `james-p-ai/beerme` · **Board:** [BeerMe Kanban](https://github.com/users/james-p-ai/projects/2)

## Product vision

BeerMe asks flavor and preference questions, builds a **taste profile** over fixed axes, and when **session confidence** meets a threshold shows a **hierarchical recommendation tree** (style → substyle → catalog beers). AI helps with language and questions; **Python and the catalog decide what to recommend**.

## Non-negotiables

1. **LLM maps language → axis updates; Python computes session confidence** — never the reverse.
2. **Recommender outputs catalog IDs/names only** — no invented beers or styles.
3. **LLM may explain picks in prose** — must not change scores, catalog rows, or confidence math.
4. **Ollama calls live in `ollama_client.py`** — unit tests use fixtures; no live model in pytest for engine logic.
5. **One GitHub issue → one Cursor chat** — do not implement a whole phase in one session.
6. **Board wins** — no personal markdown backlogs; QA findings become issues.

## Domain ownership

| Zone | Subagent | Owns | Must not |
|------|----------|------|----------|
| **LLM** | `/orion` | `app/prompts.py`, `app/ollama_client.py`, JSON parse/retry | confidence math, catalog scoring, Streamlit layout |
| **Engine** | `/engine` | `app/taste_profile.py`, `app/recommender.py`, `data/*`, engine tests | UI, live Ollama in unit tests |
| **UI** | `/voyager` | `app/main.py`, `app/export_md.py`, session state UX | scoring formulas, prompt strings, catalog edits |
| **Verify** | `/verify` (readonly) | Phase 7 checklist, smoke gate, release readiness | feature implementation |

**Routing:** Pick subagent from ticket scope or primary file path. S-sized AFK tickets confined to one zone may use the default agent + `tdd` without a subagent.

## Build and verify

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=. pytest -q
./run.sh
bash scripts/qa/beerme-smoke.sh
```

Optional env: `OLLAMA_HOST`, `OLLAMA_MODEL` (default `llama3.2:3b`).

## Cursor workflow

1. Start every session with `@AGENTS.md` and `@CONTEXT.md`.
2. **Plan mode** for multi-file or high-risk tickets before code.
3. **One branch per issue**; PR title references `#issue`.
4. Phase 6: `/orion`, `/engine`, or `/voyager` when the ticket crosses zones; always **`tdd`** for implementation.
5. Pre-PR: `/security-secrets-check`, `/review`; `/create-pr` with Summary + Test plan.
6. Phase 7 / phase close: `/verify` (readonly) + `bash scripts/qa/beerme-smoke.sh`.
7. Long chats: `/handoff` → `docs/session-handoff.md` or `/summarize` at a subtask boundary.

Handoff template: `docs/cursor-teams/TASK_HANDOFF_TEMPLATE.md`. Release gates: `docs/cursor-teams/RELEASE_GATES.md`. Usage guide: `docs/cursor-teams/CURSOR_USAGE_GUIDE.md`.

## Agent skills

Practical Office Cursor skills (`to-issues`, `triage`, `tdd`, `diagnose`, `grill-with-docs`, etc.) read per-repo config under `docs/agents/`. Install once per machine from [Practical-Office/cursor-skills](https://github.com/Practical-Office/cursor-skills); run `setup-practical-ai-skills` only when changing tracker or label vocabulary.

### Issue tracker

GitHub Issues on **`james-p-ai/beerme`** via `gh`. Program Kanban: GitHub Project 2 + `docs/github/KANBAN.md`. See [`docs/agents/issue-tracker.md`](docs/agents/issue-tracker.md).

### Triage labels

Canonical triage vocabulary on GitHub Issues — separate from phase/program labels. See [`docs/agents/triage-labels.md`](docs/agents/triage-labels.md).

### Domain docs

Single-context: [`CONTEXT.md`](CONTEXT.md) at repo root; ADRs in `docs/adr/` when needed; PRD in `docs/prd/PRD.md`. See [`docs/agents/domain.md`](docs/agents/domain.md).

## Reference docs

| Document | Use |
|----------|-----|
| [`docs/cursor-teams/CURSOR_USAGE_GUIDE.md`](docs/cursor-teams/CURSOR_USAGE_GUIDE.md) | Session workflow |
| [`docs/workflow/skills-map.md`](docs/workflow/skills-map.md) | Seven-phase SOP → skills |
| [`docs/workflow/external-skills.md`](docs/workflow/external-skills.md) | Skills outside org repo |
| [Book-IQ/bookiqv1-rc AGENTS.md](https://github.com/Book-IQ/bookiqv1-rc/blob/main/AGENTS.md) | Mature monorepo reference (six teams) |
