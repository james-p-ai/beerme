# BeerMe Kanban on GitHub

**Repo:** https://github.com/james-p-ai/beerme

## Issues (tickets)

| Section | Milestone | Labels | Status |
|---------|-----------|--------|--------|
| Epic | — | `priority:P0`, `prd:v1.3.0` | [#1](https://github.com/james-p-ai/beerme/issues/1) |
| Phase 1 | Phase 1 — Foundation | `size:S/M`, `phase-1-foundation` | #2–#5 closed (shipped) |
| Phase 2 + Ralph (confidence) | Phase 2 — Taste engine | `ralph-ready`, `ralph-batch` | #6–#13 closed |
| **Ralph: Ollama JSON** | Phase 4 — Polish | `ralph-ready` | [#14](https://github.com/james-p-ai/beerme/issues/14) parent, #15–#17 stories |
| Phase 3 remainder | Phase 3 — Catalog & recs | `ready-for-human` | [#21](https://github.com/james-p-ai/beerme/issues/21) open |
| Polish | Phase 4 — Polish | `priority:P2/P3` | [#22](https://github.com/james-p-ai/beerme/issues/22), [#23](https://github.com/james-p-ai/beerme/issues/23) |

Filter open Ralph work: https://github.com/james-p-ai/beerme/issues?q=is%3Aopen+label%3Aralph-ready

## Priority & size

On each issue via labels:

- **Priority:** `priority:P0` … `priority:P3`
- **Size:** `size:S`, `size:M`, `size:L`

## Ralph loop sections

| Batch | Parent issue | `prd.json` | Run |
|-------|--------------|------------|-----|
| taste_profile (done) | #6 | `scripts/ralph/prd.json` | stories `passes: true` |
| Ollama JSON (practice) | #14 | `scripts/ralph/prd-ollama.json` | `PRD_JSON=scripts/ralph/prd-ollama.json ./scripts/ralph/ralph.sh` |

Workflow: pick open `ralph-ready` issue → implement one story → `pytest` → set `passes: true` → parent to **Verify** on board → you approve → **Done**.

## Create the Project board (one-time)

`gh` needs project scope:

```bash
gh auth refresh -s read:project,project
```

Then:

```bash
./scripts/github/bootstrap-kanban.sh
```

Or manually:

1. https://github.com/users/james-p-ai/projects → **New project** → Board
2. Link repository **beerme**
3. Columns: **Backlog** | **Ready** | **In Progress** | **Verify** | **Done**
4. Add custom fields **Priority** (P0–P3) and **Size** (S/M/L) if desired
5. **Add all issues** from the repo
6. Drag closed Phase 1–3 tickets to **Done**
7. Put #14–#17 in **Ready** or **In Progress** for Ralph practice
8. Open tickets #21–#23 in **Backlog**

## Re-run issue bootstrap

Idempotent (skips existing titles):

```bash
./scripts/github/bootstrap-kanban.sh
```
