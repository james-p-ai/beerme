# GitHub setup

**Repo published:** https://github.com/james-p-ai/beerme

**23 issues** created with `priority:P0–P3`, `size:S/M/L`, phase milestones, and `ralph-ready` labels.

Full board guide: [docs/github/KANBAN.md](github/KANBAN.md)

## Finish the Kanban project (needs project scope)

```bash
gh auth refresh -s read:project,project
./scripts/github/bootstrap-kanban.sh
```

Or create a board manually at https://github.com/users/james-p-ai/projects and follow KANBAN.md.
