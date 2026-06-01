# Issue tracker: GitHub

Issues and PRDs for this repo live as GitHub issues. Use the `gh` CLI for all operations.

## Conventions

- **Create an issue**: `gh issue create --title "..." --body "..."`
- **Read an issue**: `gh issue view <number> --comments`
- **List issues**: `gh issue list --state open`
- **Comment**: `gh issue comment <number> --body "..."`
- **Labels**: `gh issue edit <number> --add-label "..."` / `--remove-label "..."`
- **Close**: `gh issue close <number>`

Infer the repo from `git remote -v` when run inside the clone.

## Kanban

Use GitHub Projects v2 board with columns: Backlog → Ready → In Progress → Verify → Done.

See `docs/workflow/kanban.md`.
