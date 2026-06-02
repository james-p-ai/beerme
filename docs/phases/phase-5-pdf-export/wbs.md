# Phase 5 WBS — PDF export

PRD v1.7.0 · phase-5-pdf-export · Epic [#92](https://github.com/james-p-ai/beerme/issues/92)

| ID | GitHub | Title | Subagent | Size | Type | Status |
|----|--------|-------|----------|------|------|--------|
| P5-T1 | [#87](https://github.com/james-p-ai/beerme/issues/87) | Extract `collect_beer_leaves` to recommender | `/engine` | S | AFK | Done |
| P5-T2 | [#88](https://github.com/james-p-ai/beerme/issues/88) | Blurb max length for printable export | `/orion` | S | AFK | Done |
| P5-T3 | [#89](https://github.com/james-p-ai/beerme/issues/89) | PDF export + download button | `/voyager` | M | AFK | Done |
| P5-T4 | [#90](https://github.com/james-p-ai/beerme/issues/90) | Smoke script PDF path | human | S | HITL | Done |
| P5-T5 | [#91](https://github.com/james-p-ai/beerme/issues/91) | Phase 7 verify + handoff | `/verify` | S | HITL | Done |

## Acceptance summary

- **P5-T1:** `collect_beer_leaves(tree)` public; tests for nested + empty tree; `main.py` uses import
- **P5-T2:** `BLURB_MAX_CHARS` constant; prompt references limit; fixture test in `test_prompts.py`
- **P5-T3:** `format_recommendations_pdf()` returns valid PDF bytes; download button on results; pytest without live Ollama
- **P5-T4:** Smoke documents PDF download step; export modules import offline
- **P5-T5:** pytest green (26 tests); delta + handoff committed; PRD v1.7.0 sign-off
