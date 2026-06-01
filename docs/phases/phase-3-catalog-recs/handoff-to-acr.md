# Phase 3 Handoff to ACR

PRD v1.4.0 → **v1.5.0**

## Implemented

- `data/beers.json`, `data/style_tree.json`
- `recommend_hierarchy()` with tests
- Results view with expandable style tree
- P3-T4: `BLURB_PROMPT` in `app/prompts.py`; sidebar toggle "Generate tasting notes (Ollama)"; one batch `chat_json` call for visible catalog beers; blurbs validated against catalog IDs only

## Open / deferred to Phase 4

- Export recommendations ([#23](https://github.com/james-p-ai/beerme/issues/23))
- Live beer APIs (Out of Scope)

## Recommended PRD updates

- Mark phase-3-catalog-recs complete
- Add blurb contract under Ollama / Implementation Decisions
- Testing Decisions: blurbs HITL manual only ([#22](https://github.com/james-p-ai/beerme/issues/22)); dedupe duplicate `ollama_client` bullets
- Epic label `prd:v1.4.0` → `prd:v1.5.0` on [#1](https://github.com/james-p-ai/beerme/issues/1)

## Demo

```bash
ollama pull llama3.2:3b
PYTHONPATH=. streamlit run app/main.py
```

Blurbs require Ollama connected and sidebar toggle enabled on the results screen.

## Next

phase-4-polish — [#22](https://github.com/james-p-ai/beerme/issues/22) QA session, then [#23](https://github.com/james-p-ai/beerme/issues/23) export
