# GitHub setup (run locally)

Repo is committed on `main`. Publish and seed Kanban:

```bash
cd ~/Projects/beerme
gh repo create beerme --public --source=. --remote=origin --push
```

## Labels

```bash
for l in needs-triage needs-info ready-for-agent ready-for-human wontfix bug enhancement \
  prd:v1.0.0 prd:v1.1.0 prd:v1.2.0 prd:v1.3.0 \
  phase-1-foundation phase-2-taste-engine phase-3-catalog-recs ralph size:S size:M size:L blocked; do
  gh label create "$l" --force 2>/dev/null || true
done
```

## Milestones + issues (Phase 1 example)

```bash
gh issue create --title "PRD Epic: BeerMe" --label "enhancement,prd:v1.3.0" \
  --body "Canonical PRD: docs/prd/PRD.md"

gh issue create --title "P1-T3 Ollama client" --label "enhancement,phase-1-foundation,ready-for-agent,size:M" \
  --body "See docs/phases/phase-1-foundation/kickoff.md"
```

Create a **Projects** board: Backlog → Ready → In Progress → Verify → Done.

Issue template: `.github/ISSUE_TEMPLATE/ticket.md`
