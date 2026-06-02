"""Hierarchical recommendations from static catalog."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from app.taste_profile import TasteProfile

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


@dataclass
class BeerLeaf:
    id: str
    name: str
    brewery: str
    score: float


@dataclass
class StyleNode:
    id: str
    name: str
    score: float
    children: list[StyleNode | BeerLeaf]


def _load_json(name: str) -> Any:
    with open(DATA_DIR / name, encoding="utf-8") as f:
        return json.load(f)


def _style_vector(style: dict[str, Any]) -> dict[str, float]:
    return {k: float(v) for k, v in style.get("profile", {}).items()}


def _dot(profile: TasteProfile, vec: dict[str, float]) -> float:
    total = 0.0
    for axis, val in vec.items():
        if axis in profile.values:
            # prefer high when user wants high on axis
            total += profile.values[axis] * val
    return total


def collect_beer_leaves(nodes: list[StyleNode | BeerLeaf]) -> list[BeerLeaf]:
    """Flatten a recommendation tree to catalog beer leaves."""
    leaves: list[BeerLeaf] = []
    for node in nodes:
        if isinstance(node, BeerLeaf):
            leaves.append(node)
        else:
            leaves.extend(collect_beer_leaves(node.children))
    return leaves


def recommend_hierarchy(
    profile: TasteProfile,
    *,
    top_branches: int = 3,
    beers_per_branch: int = 5,
) -> list[StyleNode]:
    tree = _load_json("style_tree.json")
    beers = {b["id"]: b for b in _load_json("beers.json")}

    def score_style(node: dict[str, Any]) -> float:
        return _dot(profile, _style_vector(node))

    def build(node: dict[str, Any], depth: int) -> StyleNode:
        children: list[StyleNode | BeerLeaf] = []
        child_styles = sorted(
            node.get("children", []),
            key=score_style,
            reverse=True,
        )
        if depth < 2 and child_styles:
            for ch in child_styles[:top_branches if depth == 0 else 99]:
                children.append(build(ch, depth + 1))
        beer_ids = node.get("beer_ids", [])
        scored_beers = []
        for bid in beer_ids:
            b = beers.get(bid)
            if not b:
                continue
            scored_beers.append(
                BeerLeaf(
                    id=bid,
                    name=b["name"],
                    brewery=b.get("brewery", ""),
                    score=_dot(profile, _style_vector(b)),
                )
            )
        scored_beers.sort(key=lambda x: x.score, reverse=True)
        limit = beers_per_branch if depth > 0 else beers_per_branch * 2
        children.extend(scored_beers[:limit])
        return StyleNode(
            id=node["id"],
            name=node["name"],
            score=score_style(node),
            children=children,
        )

    roots = sorted(tree["roots"], key=score_style, reverse=True)
    return [build(r, 0) for r in roots[:top_branches]]
