# BeerMe Release Gates

Lightweight checkpoints for phase slices and merges. `/verify` subagent and **`release-readiness`** skill honor this doc.

Polaris-style merge blocking is **not** wired in CI for this solo demo repo — gates are checklist + human sign-off.

---

## PR gate (every merge to `main`)

| Check | Blocker if fail |
|-------|-----------------|
| `PYTHONPATH=. pytest -q` pass | Yes |
| Linked GitHub issue `#` in PR | Yes |
| No secrets in diff | Yes |
| Scope matches issue acceptance criteria | Yes |
| `/security-secrets-check` on diff | Yes |

---

## Phase slice gate (Phase 7)

| Check | Blocker if fail |
|-------|-----------------|
| Phase QA plan checklist passed | Yes |
| `bash scripts/qa/beerme-smoke.sh` (HITL issue) | Yes |
| No open P0/P1 for slice (or architect deferral) | Yes |
| PRD header/changelog updated if scope changed | Yes |
| `handoff-to-acr.md` + `delta-report.md` for phase close | Yes |

---

## Engine gate

- Session confidence computed in `taste_profile.py` only
- Recommender output traceable to `data/beers.json` / `data/style_tree.json`
- Tests cover new behaviors listed on issue

**Blockers:** invented beer names in rec path, confidence in LLM prompt, unmocked live Ollama in engine unit tests

---

## LLM gate

- JSON parse/retry covered by fixture tests where changed
- Prompt changes do not embed scoring rules or catalog IDs as hard-coded “answers”
- Model name documented in PRD or issue if changed

---

## Ralph batch gate

- Each story in `prd.json` has `passes: true` only after pytest acceptance path green
- Parent issue in **Verify** until human reviews diff
- `progress.txt` updated per iteration

---

## Explicitly N/A for BeerMe

- Tenant isolation (`tenant-isolation-check` skill) — single-user local app
- EKS / infra deploy gates — local Streamlit only

See `docs/workflow/external-skills.md` for skills not used in this repo.
