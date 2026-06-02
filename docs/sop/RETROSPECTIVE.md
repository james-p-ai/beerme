# BeerMe SOP retrospective

| SOP step | Helped? | Note |
|----------|---------|------|
| Versioned PRD | Yes | v1.0→v1.7 traceable |
| Phase kickoff | Yes | Froze scope per phase |
| Ticket chats | Yes | Reduced drift |
| Phase delta | Yes | Showed PDF reuse of MD formatter |
| Handoff → ACR | Yes | PRD bumps structured |
| Kanban Verify | Yes | Ralph safety valve |
| Practical Office to-prd / to-issues | Yes | Faster issue bodies |
| Subagent routing (Phase 5 pilot) | Yes | Clean zone split on P5-T1–T3 |
| Canonical seven-phase SOP in repo | Yes | Single source for other projects |

## Friction

- `move_agent_to_root` may need retry if interrupted
- Ollama must be pre-pulled for demos
- PR #86 merge to protected `main` requires human approval
- Interactive Cursor rule attachment not automatable in CI

## Recommendation for team SOP

- Use **`docs/sop/ai-driven-development-sop.md`** as canonical; `prd-cycle-sop.full.md` as nested addendum
- Copy **`docs/sop/agent-doctrine-pilot.md`** checklist for greenfield repos
- Add subagents when LLM / engine / UI boundaries are real — not for tiny scripts
- Link **skills-map** subagent column from `docs/workflow/`
