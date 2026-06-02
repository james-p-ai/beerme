"""PDF export for recommendation results."""

from __future__ import annotations

from io import BytesIO

from fpdf import FPDF

from app.export_md import format_recommendations_md
from app.recommender import StyleNode
from app.taste_profile import TasteProfile


def _plain_line(line: str) -> str:
    text = line.strip()
    if text.startswith("# "):
        return text[2:].replace("%", "%%")
    if text.startswith("## "):
        return text[3:].replace("%", "%%")
    if text.startswith("|") and text.endswith("|"):
        cells = [cell.strip() for cell in text.strip("|").split("|")]
        if all(set(cell) <= {"-", " "} for cell in cells):
            return ""
        return ", ".join(cell for cell in cells if cell).replace("%", "%%")
    return text.replace("**", "").replace("_", "").replace("—", "-").replace("%", "%%")


def format_recommendations_pdf(
    profile: TasteProfile,
    tree: list[StyleNode],
    blurbs: dict[str, str] | None = None,
) -> bytes:
    """Render profile summary and recommendation tree as PDF bytes."""
    md = format_recommendations_md(profile, tree, blurbs)
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Helvetica", size=10)
    for raw_line in md.splitlines():
        line = raw_line.strip()
        if not line:
            pdf.ln(3)
            continue
        plain = _plain_line(line)
        if not plain:
            continue
        if raw_line.startswith("# "):
            pdf.set_font("Helvetica", "B", size=14)
            pdf.multi_cell(0, 7, plain)
            pdf.set_font("Helvetica", size=10)
        elif raw_line.startswith("## "):
            pdf.set_font("Helvetica", "B", size=12)
            pdf.multi_cell(0, 6, plain)
            pdf.set_font("Helvetica", size=10)
        else:
            pdf.set_x(pdf.l_margin)
            pdf.multi_cell(0, 5, plain)
    buffer = BytesIO()
    pdf.output(buffer)
    return buffer.getvalue()
