#!/usr/bin/env bash
# Create GitHub repo, labels, milestones, issues, and BeerMe Kanban project.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
OWNER="${GITHUB_OWNER:-james-p-ai}"
REPO="${GITHUB_REPO:-beerme}"
PROJECT_TITLE="${PROJECT_TITLE:-BeerMe Kanban}"

echo "==> Owner: $OWNER / Repo: $REPO"

if ! git remote get-url origin &>/dev/null; then
  echo "==> Creating GitHub repository..."
  gh repo create "$REPO" --public --source=. --remote=origin --push
else
  echo "==> Pushing to origin..."
  git push -u origin main 2>/dev/null || git push -u origin HEAD
fi

create_label() {
  local name="$1" color="$2" desc="${3:-}"
  gh label create "$name" --color "$color" --description "$desc" --force 2>/dev/null || true
}

echo "==> Labels..."
create_label "priority:P0" "b60205" "Critical — do first"
create_label "priority:P1" "d93f0b" "High"
create_label "priority:P2" "fbca04" "Medium"
create_label "priority:P3" "0e8a16" "Low"
create_label "size:S" "c5def5" "Small"
create_label "size:M" "1d76db" "Medium"
create_label "size:L" "5319e7" "Large"
create_label "ralph-ready" "ededed" "AFK — run via Ralph loop"
create_label "ralph-batch" "f9d0c4" "Parent for Ralph story group"
create_label "ready-for-agent" "0052cc" "Fully specified for agent"
create_label "ready-for-human" "e99695" "Needs human judgment"
create_label "phase-1-foundation" "1d76db" "Phase 1"
create_label "phase-2-taste-engine" "5319e7" "Phase 2"
create_label "phase-3-catalog-recs" "0e8a16" "Phase 3"
create_label "phase-4-polish" "bfdadc" "Phase 4 / polish"
create_label "prd:v1.3.0" "ffffff" "PRD v1.3.0"

ensure_milestone() {
  local title="$1" desc="$2"
  local n
  n=$(gh api "repos/$OWNER/$REPO/milestones?state=all" --jq ".[] | select(.title==\"$title\") | .number" | head -1)
  if [[ -z "$n" ]]; then
    n=$(gh api "repos/$OWNER/$REPO/milestones" -f title="$title" -f description="$desc" --jq .number)
  fi
  echo "$title"
}

echo "==> Milestones..."
M1=$(ensure_milestone "Phase 1 — Foundation" "Scaffold, Ollama, Streamlit shell")
M2=$(ensure_milestone "Phase 2 — Taste engine" "Profile, Q&A, confidence")
M3=$(ensure_milestone "Phase 3 — Catalog & recs" "Catalog, recommender, UI")
M4=$(ensure_milestone "Phase 4 — Polish" "QA, export, Ralph expansions")

issue_exists() {
  gh issue list -R "$OWNER/$REPO" --search "in:title \"$1\"" --json title --jq 'length' | grep -qv '^0$'
}

issue() {
  local title="$1" body="$2" labels="$3" milestone="$4" state="${5:-open}"
  if issue_exists "$title"; then
    gh issue list -R "$OWNER/$REPO" --search "in:title \"$1\"" --json number --jq '.[0].number'
    return
  fi
  local url
  url=$(gh issue create -R "$OWNER/$REPO" --title "$title" --body "$body" --label "$labels" --milestone "$milestone")
  local num="${url##*/}"
  if [[ "$state" == "closed" ]]; then
    gh issue close "$num" --comment "Shipped in repo — tracked for Kanban / SOP evidence."
  fi
  echo "$num"
}

RALPH_BODY='## Ralph loop

Run from repo root:

```bash
./scripts/ralph/ralph.sh
```

Or manual: one Cursor chat per story; `pytest` acceptance; set `passes: true` in the linked `prd.json`.

**Verify column:** move parent to Verify after batch; you approve before Done.'

echo "==> Issues..."
EPIC=$(gh issue list -R "$OWNER/$REPO" --search "in:title \"[Epic] BeerMe PRD\"" --json number --jq '.[0].number // empty')
if [[ -z "$EPIC" ]]; then
EPIC=$(issue "[Epic] BeerMe PRD" \
  "Canonical PRD: \`docs/prd/PRD.md\` (v1.3.0). All phase tickets link here." \
  "enhancement,priority:P0,prd:v1.3.0" "" "open")
else
  echo "Epic already exists: #$EPIC"
fi

# Phase 1 — closed (shipped)
issue "[P1-T1] PRD v1.0 + phase kickoff" "SOP ticket. See \`docs/phases/phase-1-foundation/\`." \
  "enhancement,priority:P1,size:S,phase-1-foundation,ready-for-agent" "$M1" closed
issue "[P1-T2] Python project + dependencies" "requirements.txt, venv, .gitignore." \
  "enhancement,priority:P1,size:S,phase-1-foundation,ready-for-agent" "$M1" closed
issue "[P1-T3] Ollama client + health check" "app/ollama_client.py; parse tests." \
  "enhancement,priority:P1,size:M,phase-1-foundation,ready-for-agent" "$M1" closed
issue "[P1-T4] Streamlit shell + connection status" "app/main.py sidebar." \
  "enhancement,priority:P1,size:S,phase-1-foundation,ready-for-agent" "$M1" closed

# Phase 2 + Ralph batch (taste_profile — done)
P2T1=$(issue "[P2-T1] taste_profile + session confidence" \
  "Parent ticket. Ralph stories in linked issues. prd: \`scripts/ralph/prd.json\`." \
  "enhancement,priority:P1,size:M,phase-2-taste-engine,ralph-batch" "$M2" closed)

for story in "conf-01:Empty profile low confidence:test_empty_profile_low_confidence" \
  "conf-02:Ready after min turns and axes:test_ready_after_enough_axes_and_turns" \
  "conf-03:Delta values clamp 0-1:test_apply_delta_clamps_values" \
  "conf-04:Profile dict roundtrip:test_roundtrip_dict"; do
  IFS=: read -r sid title test <<< "$story"
  issue "[Ralph $sid] $title" "$RALPH_BODY

Parent: #$P2T1
Acceptance: \`pytest tests/test_confidence.py::$test\`
prd.json story: \`$sid\`" \
    "enhancement,priority:P1,size:S,phase-2-taste-engine,ralph-ready,ralph-batch" "$M2" closed
done

issue "[P2-T2] Prompts + Ollama JSON contract" "app/prompts.py; chat_json retry." \
  "enhancement,priority:P1,size:M,phase-2-taste-engine,ready-for-agent" "$M2" closed
issue "[P2-T3] Streamlit Q&A loop until confident" "Multi-turn questioning in main.py." \
  "enhancement,priority:P1,size:M,phase-2-taste-engine,ready-for-human" "$M2" closed
issue "[P2-T4] Session progress + axis display" "Sidebar confidence + progress bar." \
  "enhancement,priority:P2,size:S,phase-2-taste-engine,ready-for-agent" "$M2" closed

# Ralph batch — ollama (open for practice)
P2T2R=$(issue "[P2-T2 Ralph] Ollama JSON parsing batch" \
  "$RALPH_BODY

prd: \`scripts/ralph/prd-ollama.json\` — run after adding retry test." \
  "enhancement,priority:P2,size:M,phase-2-taste-engine,ralph-batch,ralph-ready" "$M4" open)

issue "[Ralph ollama-01] Parse plain JSON" "Parent: #$P2T2R
Acceptance: \`pytest tests/test_ollama_client.py::test_parse_plain_json\`" \
  "enhancement,priority:P2,size:S,phase-4-polish,ralph-ready" "$M4" open
issue "[Ralph ollama-02] Parse JSON embedded in text" "Parent: #$P2T2R" \
  "enhancement,priority:P2,size:S,phase-4-polish,ralph-ready" "$M4" open
issue "[Ralph ollama-03] chat_json retry on invalid JSON" "Parent: #$P2T2R — implement test + behavior" \
  "enhancement,priority:P2,size:S,phase-4-polish,ralph-ready" "$M4" open

# Phase 3
issue "[P3-T1] Catalog beers.json + style_tree.json" "~40 beers." \
  "enhancement,priority:P1,size:M,phase-3-catalog-recs,ready-for-agent" "$M3" closed
issue "[P3-T2] recommender.py + hierarchy tests" "app/recommender.py" \
  "enhancement,priority:P1,size:M,phase-3-catalog-recs,ready-for-agent" "$M3" closed
issue "[P3-T3] Results tree UI" "Expandable style tree in Streamlit." \
  "enhancement,priority:P1,size:M,phase-3-catalog-recs,ready-for-human" "$M3" closed
issue "[P3-T4] Optional LLM blurbs for picks" "Catalog IDs only; prose from Ollama." \
  "enhancement,priority:P3,size:S,phase-3-catalog-recs,ready-for-human" "$M3" open

# Phase 4 / polish
issue "[P4-T1] QA session (qa skill)" "Manual smoke: \`scripts/qa/beerme-smoke.sh\`" \
  "enhancement,priority:P2,size:M,phase-4-polish,ready-for-human" "$M4" open
issue "[P4-T2] Export recommendations (PDF/MD)" "Deferred from PRD v1.3.0." \
  "enhancement,priority:P3,size:S,phase-4-polish" "$M4" open

echo "==> GitHub Project..."
PROJECT_NUM=$(gh project list --owner "$OWNER" --format json --jq ".projects[] | select(.title==\"$PROJECT_TITLE\") | .number" | head -1)
if [[ -z "$PROJECT_NUM" ]]; then
  PROJECT_NUM=$(gh project create --owner "$OWNER" --title "$PROJECT_TITLE" --format json --jq .number)
fi
echo "Project number: $PROJECT_NUM"

gh project link "$PROJECT_NUM" --owner "$OWNER" --repo "$OWNER/$REPO" 2>/dev/null || true

# Custom fields Priority + Size (ignore if exist)
gh project field-create "$PROJECT_NUM" --owner "$OWNER" --name "Priority" --data-type SINGLE_SELECT \
  --single-select-options "P0,P1,P2,P3" 2>/dev/null || true
gh project field-create "$PROJECT_NUM" --owner "$OWNER" --name "Size" --data-type SINGLE_SELECT \
  --single-select-options "S,M,L" 2>/dev/null || true

echo "==> Adding open issues to project..."
gh issue list --repo "$OWNER/$REPO" --state all --json number,title,labels --limit 100 | jq -r '.[].number' | while read -r num; do
  gh project item-add "$PROJECT_NUM" --owner "$OWNER" --url "https://github.com/$OWNER/$REPO/issues/$num" 2>/dev/null || true
done

echo ""
echo "Done."
echo "  Repo:  https://github.com/$OWNER/$REPO"
echo "  Board: https://github.com/users/$OWNER/projects/$PROJECT_NUM"
echo "  Epic:  https://github.com/$OWNER/$REPO/issues/$EPIC"
