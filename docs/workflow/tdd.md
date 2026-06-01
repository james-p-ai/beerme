# TDD on BeerMe tickets

## Rules (mattpocock `tdd` skill)

1. Vertical slices only: one test → one minimal impl → green.
2. Test public interfaces (`confidence_score`, `recommend_hierarchy`).
3. List **behaviors to test** on GitHub issue before RED.

## Issue template section

```markdown
## TDD behaviors
- [ ] behavior 1
- [ ] behavior 2
```

## DoD

`pytest` passes for listed behaviors (or exception documented in mini-spec).
