#!/usr/bin/env bash
# BeerMe Ralph loop — one story per iteration, pytest gate.
# Requires: Cursor Agent CLI (`agent`) OR run stories manually per README.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
PRD_JSON="${PRD_JSON:-$ROOT/scripts/ralph/prd.json}"
PROGRESS="$ROOT/progress.txt"
MAX_ITER="${MAX_ITER:-15}"

cd "$ROOT"

if [[ ! -f "$PRD_JSON" ]]; then
  echo "Missing $PRD_JSON"
  exit 1
fi

pick_story() {
  python3 - "$PRD_JSON" << 'PY'
import json, sys
data = json.load(open(sys.argv[1]))
for s in data.get("userStories", []):
    if not s.get("passes"):
        print(s["id"])
        print(s.get("acceptance", ""))
        break
PY
}

iter=0
while [[ $iter -lt $MAX_ITER ]]; do
  mapfile -t lines < <(pick_story)
  if [[ ${#lines[@]} -eq 0 ]]; then
    echo "COMPLETE: all stories pass"
    exit 0
  fi
  story_id="${lines[0]}"
  acceptance="${lines[1]:-}"
  iter=$((iter + 1))
  echo "=== Ralph iteration $iter / $MAX_ITER — story $story_id ==="
  echo "Acceptance: $acceptance"
  echo ""
  echo "Manual mode: open a new Cursor chat and implement ONLY this story (TDD)."
  echo "Then run: pytest $acceptance"
  echo "Mark passes:true in scripts/ralph/prd.json and append learnings to progress.txt"
  echo ""
  if command -v agent >/dev/null 2>&1; then
    prompt="Implement Ralph story $story_id only. TDD vertical slice. Run: pytest $acceptance. Update scripts/ralph/prd.json passes for this story."
    agent -p "$prompt" --workspace "$ROOT" || true
    if [[ -n "$acceptance" ]] && pytest -q "$acceptance"; then
      python3 - "$PRD_JSON" "$story_id" << 'PY'
import json, sys
path, sid = sys.argv[1], sys.argv[2]
data = json.load(open(path))
for s in data["userStories"]:
    if s["id"] == sid:
        s["passes"] = True
json.dump(data, open(path, "w"), indent=2)
print(f"Marked {sid} passes=true")
PY
      echo "$(date -Iseconds) $story_id done" >> "$PROGRESS"
    fi
  else
    echo "No 'agent' CLI — stopping after printing story (install Cursor CLI or run manually)."
    exit 2
  fi
done

echo "Stopped: max iterations ($MAX_ITER) reached"
exit 1
