# Ralph loop playbook (repeatable)

## When to use

- Ticket labeled `ralph-ready` and `ralph-batch`
- Work is **AFK**: one behavior, pytest-verifiable, no live Ollama/UI judgment

## Files

| File | Role |
|------|------|
| `scripts/ralph/prd-<batch>.json` | Stories with `passes` boolean |
| `scripts/ralph/ralph.sh` | Picks next story; optional `agent` CLI |
| `progress.txt` | Append-only learnings |

## One iteration

1. `PRD_JSON=scripts/ralph/prd-<batch>.json ./scripts/ralph/ralph.sh`
2. New Cursor chat + **tdd** skill — one story only
3. `PYTHONPATH=. pytest <acceptance from prd>`
4. Set `"passes": true` in prd JSON
5. Line in `progress.txt`
6. Small git commit
7. GitHub story issue comment; parent stays open until Verify

## Human gates

- **Verify** on Kanban before **Done**
- **HITL** (`ready-for-human`) for product/design/live LLM

## Run command

```bash
PRD_JSON=scripts/ralph/prd-ollama.json ./scripts/ralph/ralph.sh
```

Exit `COMPLETE` = all `passes: true`.
