# BeerMe

Local beer taste quiz: Ollama asks flavor questions → Python builds a taste profile → hierarchical recommendations from a static catalog.

Built to verify the [PRD → ticket → handoff → ACR cycle SOP](docs/sop/prd-cycle-sop.full.md).

**GitHub:** https://github.com/james-p-ai/beerme — [Issues](https://github.com/james-p-ai/beerme/issues) · [Kanban guide](docs/github/KANBAN.md)

## Quick start

```bash
cd ~/Projects/beerme
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
ollama pull llama3.2:3b
streamlit run app/main.py
```

Optional env: `OLLAMA_HOST`, `OLLAMA_MODEL` (default `llama3.2:3b`).

## Tests

```bash
PYTHONPATH=. pytest -q
```

## Ralph loop

Autonomous small-task loop for AFK-friendly work (e.g. `taste_profile` TDD).

| File | Purpose |
|------|---------|
| [scripts/ralph/prd.json](scripts/ralph/prd.json) | Stories with `passes` flag |
| [scripts/ralph/ralph.sh](scripts/ralph/ralph.sh) | Iteration driver + pytest gate |
| [progress.txt](progress.txt) | Append-only learnings |

### Ralph batches on GitHub

| Batch | Issue | prd file |
|-------|-------|----------|
| taste_profile (done) | [#6](https://github.com/james-p-ai/beerme/issues/6) | `scripts/ralph/prd.json` |
| Ollama JSON (open) | [#14](https://github.com/james-p-ai/beerme/issues/14) | `scripts/ralph/prd-ollama.json` |

```bash
PRD_JSON=scripts/ralph/prd-ollama.json ./scripts/ralph/ralph.sh
```

### How Ralph is set up

1. Break a GitHub ticket into stories in `prd.json` (one behavior each).
2. Set `maxIterations` (default 15).
3. Run `./scripts/ralph/ralph.sh` **or** manual mode: new Cursor chat per story, run `pytest`, set `passes: true`.
4. Move parent issue to Kanban **Verify** until you review diff + tests.
5. Without Cursor `agent` CLI, script exits with instructions (manual Ralph).

See [docs/workflow/kanban.md](docs/workflow/kanban.md).

## SOP & skills evidence index

| Artifact | Path |
|----------|------|
| PRD (canonical) | [docs/prd/PRD.md](docs/prd/PRD.md) |
| Phase 1 handoff | [docs/phases/phase-1-foundation/handoff-to-acr.md](docs/phases/phase-1-foundation/handoff-to-acr.md) |
| Phase 2 handoff | [docs/phases/phase-2-taste-engine/handoff-to-acr.md](docs/phases/phase-2-taste-engine/handoff-to-acr.md) |
| Phase 3 handoff | [docs/phases/phase-3-catalog-recs/handoff-to-acr.md](docs/phases/phase-3-catalog-recs/handoff-to-acr.md) |
| SOP addendum | [docs/sop/verification-addendum.md](docs/sop/verification-addendum.md) |
| Full SOP copy | [docs/sop/prd-cycle-sop.full.md](docs/sop/prd-cycle-sop.full.md) |
| Skills map | [docs/workflow/skills-map.md](docs/workflow/skills-map.md) |
| TDD workflow | [docs/workflow/tdd.md](docs/workflow/tdd.md) |
| Kanban | [docs/workflow/kanban.md](docs/workflow/kanban.md) |
| Agent config | [docs/agents/](docs/agents/) |
| Domain glossary | [CONTEXT.md](CONTEXT.md) |

## Matt Pocock skills (local)

Symlinked under `~/.cursor/skills/` from `~/.cursor/skills-mattpocock`. Repo configured via [AGENTS.md](AGENTS.md).

| Skill | Use |
|-------|-----|
| `setup-matt-pocock-skills` | Done — `docs/agents/*` |
| `to-prd` | PRD draft / ACR bumps |
| `to-issues` | Phase → GitHub issues |
| `tdd` | Ticket implementation |
| `triage` | Issue labels |
| `handoff` | Session handoff (not phase handoff) |
| `grill-me` | Plan review |
| `qa` | End-of-phase bug filing |

## Human verification

- **Plans:** Plan mode + `grill-me`
- **Code:** Kanban **Verify** column
- **Smoke:** `bash scripts/qa/beerme-smoke.sh`

## License

MIT (intern / demo project)
