# Issue tracker: GitHub

Issues and PRDs for this repo live as **GitHub Issues** on **`james-p-ai/beerme`**. Use the `gh` CLI for all skill-driven issue operations.

**Board:** [BeerMe Kanban (Project 2)](https://github.com/users/james-p-ai/projects/2)

## Conventions

- **Create an issue**: `gh issue create --title "..." --body "..."`. Use a heredoc for multi-line bodies.
- **Read an issue**: `gh issue view <number> --comments`
- **List issues**: `gh issue list --state open --json number,title,body,labels`
- **Comment**: `gh issue comment <number> --body "..."`
- **Labels**: `gh issue edit <number> --add-label "..."` / `--remove-label "..."`
- **Close**: `gh issue close <number> --comment "..."`

Infer the repo from `git remote -v` when run inside the clone.

## Program board vs triage labels

Two label layers — do not conflate them:

| Layer | Purpose | Doc |
|-------|---------|-----|
| **Triage roles** | `needs-triage`, `ready-for-agent`, `ready-for-human`, etc. | `docs/agents/triage-labels.md` |
| **Program metadata** | `phase-*`, `prd:v*`, `priority:P*`, `ralph-ready`, `size:S` | Same file, BeerMe section |

Skills (`to-issues`, `triage`, `qa`) use **triage role** labels when publishing or moving issues. Phase epics and WBS live in `docs/phases/` and on the Project board.

## Kanban columns

Documented in `docs/github/KANBAN.md` and `docs/workflow/kanban.md`:

```
Backlog → Triage → Ready → In Progress → In Review → Done
                         ↘ Blocked ↗
```

Ralph batches: parent issue moves to **Verify** (board) until human approves → **Done**.

## When a skill says "publish to the issue tracker"

Create or update a GitHub issue on `james-p-ai/beerme` with labels from `docs/agents/triage-labels.md`.
