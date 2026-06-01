"""BeerMe Streamlit UI."""

from __future__ import annotations

import json
from typing import Any

import streamlit as st

from app import ollama_client
from app.prompts import EXTRACT_PROMPT, NEXT_QUESTION_PROMPT
from app.recommender import BeerLeaf, StyleNode, recommend_hierarchy
from app.taste_profile import TasteProfile

st.set_page_config(page_title="BeerMe", page_icon="🍺", layout="centered")


def _init_state() -> None:
    if "profile" not in st.session_state:
        st.session_state.profile = TasteProfile()
    if "phase" not in st.session_state:
        st.session_state.phase = "questioning"
    if "history" not in st.session_state:
        st.session_state.history: list[dict[str, str]] = []
    if "current_question" not in st.session_state:
        st.session_state.current_question = None


def _reset() -> None:
    st.session_state.profile = TasteProfile()
    st.session_state.phase = "questioning"
    st.session_state.history = []
    st.session_state.current_question = None


def _fetch_question(profile: TasteProfile) -> dict[str, Any]:
    ctx = {
        "profile": profile.to_dict(),
        "history": st.session_state.history,
    }
    messages = [
        {"role": "system", "content": NEXT_QUESTION_PROMPT},
        {"role": "user", "content": json.dumps(ctx)},
    ]
    return ollama_client.chat_json(messages)


def _apply_answer(profile: TasteProfile, answer: str) -> None:
    ctx = {"profile": profile.to_dict(), "answer": answer}
    messages = [
        {"role": "system", "content": EXTRACT_PROMPT},
        {"role": "user", "content": json.dumps(ctx)},
    ]
    data = ollama_client.chat_json(messages)
    delta = data.get("delta", data)
    profile.apply_delta(delta)
    profile.record_turn()


def _render_tree(nodes: list[StyleNode], depth: int = 0) -> None:
    for node in nodes:
        if isinstance(node, BeerLeaf):
            st.markdown(f"{'  ' * depth}- **{node.name}** ({node.brewery}) — score {node.score:.2f}")
        else:
            with st.expander(f"{'  ' * depth}{node.name} (score {node.score:.2f})", expanded=depth == 0):
                _render_tree(node.children, depth + 1)


def main() -> None:
    _init_state()
    profile: TasteProfile = st.session_state.profile

    st.title("BeerMe")
    st.caption("Local taste quiz → hierarchical beer picks (Ollama + catalog)")

    ok = ollama_client.is_available()
    st.sidebar.markdown("**Ollama**")
    if ok:
        models = ollama_client.list_models()
        st.sidebar.success(f"Connected · model `{ollama_client.ollama_model()}`")
        if models:
            st.sidebar.caption("Installed: " + ", ".join(models[:5]))
    else:
        st.sidebar.error("Ollama not reachable. Start Ollama and pull a model.")
        st.sidebar.code("ollama pull llama3.2:3b", language="bash")

    if st.sidebar.button("Reset session"):
        _reset()
        st.rerun()

    conf = profile.confidence_score()
    st.progress(conf, text=f"Session confidence: {conf:.0%}")
    st.sidebar.json(
        {a: round(profile.axis_confidence.get(a, 0), 2) for a in profile.values},
        expanded=False,
    )

    if st.session_state.phase == "results":
        st.subheader("Recommendations")
        if not ok:
            st.warning("Ollama offline — showing catalog ranking from profile only.")
        tree = recommend_hierarchy(profile)
        _render_tree(tree)
        if st.button("Ask more questions"):
            st.session_state.phase = "questioning"
            st.rerun()
        return

    if not ok:
        st.info("Connect Ollama to start the quiz.")
        return

    q = st.session_state.current_question
    if q is None:
        with st.spinner("Thinking of a question…"):
            try:
                q = _fetch_question(profile)
                st.session_state.current_question = q
            except Exception as e:
                st.error(f"Could not get question: {e}")
                return

    st.subheader(q.get("question", "What beers do you usually enjoy?"))
    choices = q.get("choices")
    answer: str | None = None
    if choices:
        answer = st.radio("Choose one", choices, key="choice_answer")
    else:
        answer = st.text_input("Your answer")

    if st.button("Submit answer", type="primary") and answer:
        st.session_state.history.append(
            {"question": q.get("question", ""), "answer": str(answer)}
        )
        with st.spinner("Updating your profile…"):
            try:
                _apply_answer(profile, str(answer))
            except Exception as e:
                st.error(f"Could not parse preferences: {e}")
                return
        st.session_state.current_question = None
        if profile.is_ready():
            st.session_state.phase = "results"
        st.rerun()


if __name__ == "__main__":
    main()
