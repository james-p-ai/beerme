# GitHub Kanban

## Columns

| Column | Meaning |
|--------|---------|
| Backlog | Not ready |
| Ready | DoR met, can start |
| In Progress | WIP (limit 1–2 solo) |
| Verify | AI/Ralph done; human checks tests + diff |
| Done | Merged + closed issue |

## Mapping

- Phase → GitHub Milestone
- Ticket → Issue with `prd:vX.Y.Z` + phase label
- Ralph batch → label `ralph`, parent issue stays in Verify until you approve

Create board: GitHub → Projects → New project → Board → link `beerme` repo.
