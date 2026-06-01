#!/usr/bin/env bash
# Human-in-the-loop smoke test for BeerMe (from mattpocock hitl-loop template).
set -euo pipefail

step() {
  printf '\n>>> %s\n' "$1"
  read -r -p " [Enter when done] " _
}

capture() {
  local var="$1" question="$2" answer
  printf '\n>>> %s\n' "$question"
  read -r -p " > " answer
  printf -v "$var" '%s' "$answer"
}

step "Start Ollama and run: cd ~/work/projects/beerme && ./run.sh"
step "Confirm sidebar shows Ollama connected with model installed"
step "Answer 4+ banked questions — progress bar should rise; no duplicate axis topics"
capture SAW_RECS "Did recommendations appear after enough answers? (y/n)"
step "Expand style branches in the results tree and confirm beer names appear"
step "Enable sidebar 'Generate tasting notes (Ollama)' — wait for notes under beers"
capture SAW_BLURBS "Did tasting notes appear under recommended beers? (y/n)"
step "Click 'Ask more questions' — confirm a new question appears (not bounced to results)"
step "Click 'Reset session' in sidebar — confirm quiz restarts with empty profile"
capture OFFLINE_OK "Optional: stop Ollama, reload results — catalog ranking still shows? (y/n/skip)"

printf '\n--- Captured ---\n'
printf 'SAW_RECS=%s\n' "$SAW_RECS"
printf 'SAW_BLURBS=%s\n' "$SAW_BLURBS"
printf 'OFFLINE_OK=%s\n' "$OFFLINE_OK"
