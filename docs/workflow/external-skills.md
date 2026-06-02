# External skills (outside Practical-Office/cursor-skills)

These are **not** in [Practical-Office/cursor-skills](https://github.com/Practical-Office/cursor-skills). Install separately; document here so agents do not fork org skills into the repo.

## Personal / team skills (`~/.agents/skills/`)

| Skill | Purpose | SOP phase |
|-------|---------|-----------|
| `caveman-compress` | Compress natural-language `.md` files (handoff, large CONTEXT) | Post-cycle, long chats |
| `caveman-commit` | Ultra-compressed commit messages | Phase 6 commits |
| `caveman-review` | One-line PR review comments | Phase 6 review |
| `cavecrew` | Delegate to compressed subagents to save context | Long sessions (optional) |

**Not the same as** org skill `caveman` in cursor-skills — that is **communication mode** only, not file compression.

### caveman-compress example

```bash
cd ~/.agents/skills/caveman-compress
python3 -m scripts /absolute/path/to/docs/session-handoff.md
```

Creates `.original.md` backup; overwrites target with compressed prose. **Never** run on code or config.

## Cursor built-ins

| Command | Purpose |
|---------|---------|
| `/summarize` | Compress in-chat context (not files on disk) |

## Explicitly skip for BeerMe

| Skill | Reason |
|-------|--------|
| `tenant-isolation-check` | No multi-tenant scope |
| BookIQ subagents (`/atlas`, `/titan`, …) | Monorepo only — BeerMe uses `/orion`, `/engine`, `/voyager`, `/verify` |

## Legacy (remove if present)

| Item | Replacement |
|------|-------------|
| `setup-matt-pocock-skills` symlink | `setup-practical-ai-skills` |
| `~/.cursor/skills-mattpocock` clone | Practical-Office/cursor-skills |
