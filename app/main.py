"""BeerMe Streamlit UI."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import streamlit as st

from app import ollama_client
from app.prompts import BLURB_PROMPT, EXTRACT_PROMPT, NEXT_QUESTION_PROMPT
from app.recommender import BeerLeaf, StyleNode, recommend_hierarchy
from app.taste_profile import TasteProfile

st.set_page_config(page_title="BeerMe", page_icon="🍺", layout="centered")

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def _init_state() -> None:
    if "profile" not in st.session_state:
        st.session_state.profile = TasteProfile()
    if "phase" not in st.session_state:
        st.session_state.phase = "questioning"
    if "history" not in st.session_state:
        st.session_state.history: list[dict[str, str]] = []
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
    if "blurbs" not in st.session_state:
        st.session_state.blurbs: dict[str, str] = {}
    if "blurbs_for_ids" not in st.session_state:
        st.session_state.blurbs_for_ids: tuple[str, ...] | None = None


def _reset() -> None:
    st.session_state.profile = TasteProfile()
    st.session_state.phase = "questioning"
    st.session_state.history = []
    st.session_state.current_question = None
    st.session_state.blurbs = {}
    st.session_state.blurbs_for_ids = None


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


def _collect_beer_leaves(nodes: list[StyleNode]) -> list[BeerLeaf]:
    leaves: list[BeerLeaf] = []
    for node in nodes:
        if isinstance(node, BeerLeaf):
            leaves.append(node)
        else:
            leaves.extend(_collect_beer_leaves(node.children))
    return leaves


def _validate_blurbs(raw: dict[str, Any], allowed_ids: set[str]) -> dict[str, str]:
    blurbs = raw.get("blurbs", raw)
    if not isinstance(blurbs, dict):
        return {}
    return {k: str(v) for k, v in blurbs.items() if k in allowed_ids and v}


def _fetch_blurbs(profile: TasteProfile, leaves: list[BeerLeaf]) -> dict[str, str]:
    with open(DATA_DIR / "beers.json", encoding="utf-8") as f:
        catalog = {b["id"]: b for b in json.load(f)}

    allowed_ids = {leaf.id for leaf in leaves}
    beers = []
    for leaf in leaves:
        beer = catalog.get(leaf.id)
        if not beer:
            continue
        beers.append(
            {
                "id": beer["id"],
                "name": beer["name"],
                "brewery": beer.get("brewery", ""),
                "profile": beer.get("profile", {}),
            }
        )

    ctx = {"profile": profile.to_dict(), "beers": beers}
    messages = [
        {"role": "system", "content": BLURB_PROMPT},
        {"role": "user", "content": json.dumps(ctx)},
    ]
    data = ollama_client.chat_json(messages)
    return _validate_blurbs(data, allowed_ids)


def _render_tree(
    nodes: list[StyleNode],
    blurbs: dict[str, str] | None = None,
    depth: int = 0,
) -> None:
    for node in nodes:
        if isinstance(node, BeerLeaf):
            st.markdown(f"{'  ' * depth}- **{node.name}** ({node.brewery}) — score {node.score:.2f}")
            if blurbs and node.id in blurbs:
                st.caption(f"{'  ' * depth}{blurbs[node.id]}")
        else:
            with st.expander(f"{'  ' * depth}{node.name} (score {node.score:.2f})", expanded=depth == 0):
                _render_tree(node.children, blurbs, depth + 1)


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

    st.sidebar.checkbox(
        "Generate tasting notes (Ollama)",
        value=False,
        disabled=not ok,
        key="show_blurbs",
    )

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
        blurbs: dict[str, str] | None = None
        if st.session_state.show_blurbs and ok:
            leaves = _collect_beer_leaves(tree)
            ids = tuple(sorted(leaf.id for leaf in leaves))
            if ids and st.session_state.blurbs_for_ids != ids:
                with st.spinner("Generating tasting notes…"):
                    try:
                        st.session_state.blurbs = _fetch_blurbs(profile, leaves)
                        st.session_state.blurbs_for_ids = ids
                    except Exception as e:
                        st.warning(f"Could not generate tasting notes: {e}")
                        st.session_state.blurbs = {}
                        st.session_state.blurbs_for_ids = None
            blurbs = st.session_state.blurbs or None
        _render_tree(tree, blurbs)
        if st.button("Ask more questions"):
            st.session_state.phase = "questioning"
            st.session_state.blurbs = {}
            st.session_state.blurbs_for_ids = None
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
            st.session_state.blurbs = {}
            st.session_state.blurbs_for_ids = None
        st.rerun()


if __name__ == "__main__":
    main()
