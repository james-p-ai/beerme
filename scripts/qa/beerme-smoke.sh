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

step "Start Ollama and run: cd ~/Projects/beerme && source .venv/bin/activate && streamlit run app/main.py"
step "Confirm sidebar shows Ollama connected"
capture LIKES_BITTER "Do you want bitter beers? (y/n)"
capture SAW_RECS "After 4+ answers, did recommendations appear? (y/n)"

printf '\n--- Captured ---\n'
printf 'LIKES_BITTER=%s\n' "$LIKES_BITTER"
printf 'SAW_RECS=%s\n' "$SAW_RECS"
