"""Markdown export for recommendation results."""

from __future__ import annotations

from app.recommender import BeerLeaf, StyleNode
from app.taste_profile import TASTE_AXES, TasteProfile


def format_recommendations_md(
    profile: TasteProfile,
    tree: list[StyleNode],
    blurbs: dict[str, str] | None = None,
) -> str:
    """Render profile summary and recommendation tree as markdown."""
    lines: list[str] = ["# BeerMe recommendations", ""]

    conf = profile.confidence_score()
    lines.append(f"Session confidence: **{conf:.0%}**")
    lines.append("")
    lines.append("## Taste profile")
    lines.append("")
    lines.append("| Axis | Value | Confidence |")
    lines.append("|------|-------|------------|")
    for axis in TASTE_AXES:
        val = profile.values.get(axis, 0.5)
        ax_conf = profile.axis_confidence.get(axis, 0.0)
        lines.append(f"| {axis} | {val:.2f} | {ax_conf:.2f} |")
    lines.append("")

    lines.append("## Recommendations")
    lines.append("")
    _append_tree(lines, tree, blurbs, depth=0)
    lines.append("")
    return "\n".join(lines)


def _append_tree(
    lines: list[str],
    nodes: list[StyleNode | BeerLeaf],
    blurbs: dict[str, str] | None,
    *,
    depth: int,
) -> None:
    indent = "  " * depth
    for node in nodes:
        if isinstance(node, BeerLeaf):
            lines.append(f"{indent}- **{node.name}** ({node.brewery}) — score {node.score:.2f}")
            if blurbs and node.id in blurbs:
                lines.append(f"{indent}  _{blurbs[node.id]}_")
        else:
            lines.append(f"{indent}- **{node.name}** (score {node.score:.2f})")
            _append_tree(lines, node.children, blurbs, depth=depth + 1)
