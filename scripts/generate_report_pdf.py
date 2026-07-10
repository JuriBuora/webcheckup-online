#!/usr/bin/env python3
"""Generate a polished PDF from an audit report Markdown file."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

try:
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import cm
    from reportlab.platypus import (
        Image,
        PageBreak,
        Paragraph,
        SimpleDocTemplate,
        Spacer,
        Table,
        TableStyle,
    )
except ModuleNotFoundError as exc:
    if (exc.name or "").startswith("reportlab"):
        raise SystemExit(
            "Missing dependency: reportlab. Use the bundled Codex Python at "
            "/Users/juribuora/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 "
            "or install it with: python3 -m pip install reportlab"
        ) from exc
    raise


PAGEBREAK_MARKER = "<!-- pagebreak -->"
UNFILLED_PLACEHOLDER_RE = re.compile(r"{{[^{}]+}}")


def escape_inline(text: str) -> str:
    """Escape minimal HTML and support a small Markdown inline subset."""
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"`([^`]+)`", r'<font name="Courier">\1</font>', text)
    return text


def strip_markdown_link(text: str) -> str:
    return re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)


def extract_front_matter(markdown: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for line in markdown.splitlines()[:30]:
        match = re.match(r"\*\*(Cliente|Sito analizzato|Data|Tipo di controllo):\*\*\s*(.+)", line)
        if match:
            fields[match.group(1)] = strip_markdown_link(match.group(2).strip())
    return fields


def find_unfilled_placeholders(markdown: str) -> list[str]:
    return sorted(set(UNFILLED_PLACEHOLDER_RE.findall(markdown)))


def build_styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    return {
        "cover_title": ParagraphStyle(
            "CoverTitle",
            parent=base["Title"],
            fontName="Helvetica-Bold",
            fontSize=26,
            leading=31,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#153f32"),
            spaceAfter=18,
        ),
        "cover_sub": ParagraphStyle(
            "CoverSub",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=13,
            leading=18,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#4c5f58"),
            spaceAfter=8,
        ),
        "h1": ParagraphStyle(
            "H1",
            parent=base["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=20,
            leading=25,
            textColor=colors.HexColor("#153f32"),
            spaceBefore=12,
            spaceAfter=10,
        ),
        "h2": ParagraphStyle(
            "H2",
            parent=base["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=15,
            leading=19,
            textColor=colors.HexColor("#1f6b58"),
            spaceBefore=10,
            spaceAfter=7,
        ),
        "h3": ParagraphStyle(
            "H3",
            parent=base["Heading3"],
            fontName="Helvetica-Bold",
            fontSize=12,
            leading=15,
            textColor=colors.HexColor("#9a5a16"),
            spaceBefore=8,
            spaceAfter=5,
        ),
        "body": ParagraphStyle(
            "Body",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=9.4,
            leading=13.2,
            textColor=colors.HexColor("#26312d"),
            spaceAfter=6,
        ),
        "bullet": ParagraphStyle(
            "Bullet",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=9.2,
            leading=12.8,
            leftIndent=13,
            firstLineIndent=-8,
            textColor=colors.HexColor("#26312d"),
            spaceAfter=4,
        ),
        "bullet_nested": ParagraphStyle(
            "BulletNested",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=9.0,
            leading=12.2,
            leftIndent=26,
            firstLineIndent=-8,
            textColor=colors.HexColor("#26312d"),
            spaceAfter=3,
        ),
        "quote": ParagraphStyle(
            "Quote",
            parent=base["BodyText"],
            fontName="Helvetica-Oblique",
            fontSize=9.2,
            leading=12.8,
            leftIndent=12,
            rightIndent=12,
            textColor=colors.HexColor("#44524d"),
            borderColor=colors.HexColor("#d6e7df"),
            borderWidth=0.5,
            borderPadding=8,
            backColor=colors.HexColor("#f3faf7"),
            spaceBefore=6,
            spaceAfter=8,
        ),
        "small": ParagraphStyle(
            "Small",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=8,
            leading=10,
            textColor=colors.HexColor("#6d7975"),
        ),
        "table_header": ParagraphStyle(
            "TableHeader",
            parent=base["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=8,
            leading=10,
            textColor=colors.white,
        ),
    }


def table_widths(column_count: int) -> list[float]:
    if column_count == 5:
        return [2.8 * cm, 3.2 * cm, 4.2 * cm, 3.8 * cm, 3.0 * cm]
    if column_count == 4:
        return [4.1 * cm, 4.1 * cm, 4.1 * cm, 4.1 * cm]
    if column_count == 3:
        return [4.7 * cm, 5.2 * cm, 6.4 * cm]
    if column_count == 2:
        return [7.8 * cm, 8.2 * cm]
    return [16.5 * cm / max(column_count, 1)] * max(column_count, 1)


def make_table(rows: list[list[str]], styles: dict[str, ParagraphStyle]) -> Table:
    rendered = [
        [
            Paragraph(
                escape_inline(cell.strip()),
                styles["table_header"] if row_index == 0 else styles["small"],
            )
            for cell in row
        ]
        for row_index, row in enumerate(rows)
    ]
    table = Table(rendered, colWidths=table_widths(len(rows[0])), repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#153f32")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#cfd8d3")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#fbfdfb")),
                (
                    "ROWBACKGROUNDS",
                    (0, 1),
                    (-1, -1),
                    [colors.HexColor("#fbfdfb"), colors.HexColor("#f4faf7")],
                ),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    return table


def image_size(path: Path) -> tuple[float, float]:
    probe = Image(str(path))
    image_width = probe.imageWidth
    image_height = probe.imageHeight

    filename = path.name.lower()
    if "mobile" in filename:
        max_width = 9.0 * cm
        max_height = 17.2 * cm
    elif "fullpage" in filename:
        max_width = 16.5 * cm
        max_height = 17.5 * cm
    else:
        max_width = 16.5 * cm
        max_height = 11.2 * cm

    ratio = min(max_width / image_width, max_height / image_height)
    return image_width * ratio, image_height * ratio


def add_image(story: list, image_ref: str, alt: str, markdown_path: Path, styles: dict[str, ParagraphStyle]) -> None:
    image_path = (markdown_path.parent / image_ref).resolve()
    if not image_path.exists():
        story.append(Paragraph(f"[Screenshot non trovato: {escape_inline(image_ref)}]", styles["small"]))
        return

    story.append(Paragraph(escape_inline(alt), styles["small"]))
    story.append(Spacer(1, 5))
    image = Image(str(image_path))
    image.drawWidth, image.drawHeight = image_size(image_path)
    story.append(image)
    story.append(Spacer(1, 8))


def build_story(markdown_path: Path, styles: dict[str, ParagraphStyle], text: str | None = None) -> list:
    text = text if text is not None else markdown_path.read_text(encoding="utf-8")
    fields = extract_front_matter(text)
    client = fields.get("Cliente", "[Cliente]")
    site = fields.get("Sito analizzato", "[Sito]")
    report_date = fields.get("Data", "[Data]")
    audit_type = fields.get("Tipo di controllo", "Analisi esterna e non invasiva")

    story: list = []
    story.append(Spacer(1, 2.5 * cm))
    story.append(Paragraph("Check-up Sito Web", styles["cover_title"]))
    story.append(Paragraph("Sicurezza, Fiducia e Visibilità", styles["cover_sub"]))
    story.append(Spacer(1, 0.4 * cm))
    story.append(Paragraph(escape_inline(client), styles["cover_sub"]))
    story.append(Paragraph(escape_inline(site), styles["cover_sub"]))
    story.append(Paragraph(escape_inline(f"{report_date} - {audit_type}"), styles["cover_sub"]))
    story.append(PageBreak())

    table_rows: list[list[str]] = []

    def flush_table() -> None:
        nonlocal table_rows
        if not table_rows:
            return
        story.append(make_table(table_rows, styles))
        story.append(Spacer(1, 8))
        table_rows = []

    for raw_line in text.splitlines():
        line = raw_line.rstrip()

        if line.strip() == PAGEBREAK_MARKER:
            flush_table()
            if story and not isinstance(story[-1], PageBreak):
                story.append(PageBreak())
            continue

        if line.startswith("<!--") and line.endswith("-->"):
            continue

        if not line.strip():
            flush_table()
            story.append(Spacer(1, 3))
            continue

        if line.strip() == "---":
            flush_table()
            story.append(Spacer(1, 8))
            continue

        if line.startswith("|") and line.endswith("|"):
            parts = [part.strip() for part in line.strip("|").split("|")]
            if all(set(part) <= set("-: ") and "-" in part for part in parts):
                continue
            table_rows.append(parts)
            continue

        flush_table()

        image_match = re.match(r"!\[(.*?)\]\((.*?)\)", line)
        if image_match:
            add_image(story, image_match.group(2), image_match.group(1), markdown_path, styles)
            continue

        if line.startswith("# "):
            continue
        if line.startswith("## "):
            title = line[3:]
            if title == "Sicurezza, Fiducia e Visibilità":
                continue
            story.append(Paragraph(escape_inline(title), styles["h1"]))
            continue
        if line.startswith("### "):
            story.append(Paragraph(escape_inline(line[4:]), styles["h2"]))
            continue

        bullet_match = re.match(r"^(\s*)-\s+(.+)", raw_line)
        if bullet_match:
            style = styles["bullet_nested"] if bullet_match.group(1) else styles["bullet"]
            story.append(Paragraph("• " + escape_inline(bullet_match.group(2)), style))
            continue

        number_match = re.match(r"^(\s*)(\d+\.\s+.+)", raw_line)
        if number_match:
            style = styles["bullet_nested"] if number_match.group(1) else styles["bullet"]
            story.append(Paragraph(escape_inline(number_match.group(2)), style))
            continue

        if line.startswith("> "):
            story.append(Paragraph(escape_inline(line[2:]), styles["quote"]))
            continue

        story.append(Paragraph(escape_inline(line), styles["body"]))

    flush_table()
    return story


def footer_factory(title: str, author: str, subject: str):
    def footer(canvas, doc) -> None:
        canvas.saveState()
        canvas.setTitle(title)
        canvas.setAuthor(author)
        canvas.setSubject(subject)
        canvas.setCreator("Website Trust & Security Mini-Audit Service")
        canvas.setProducer("ReportLab")
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.HexColor("#6d7975"))
        canvas.drawString(doc.leftMargin, 1.1 * cm, title)
        canvas.drawRightString(A4[0] - doc.rightMargin, 1.1 * cm, f"Pagina {doc.page}")
        canvas.restoreState()

    return footer


def generate_pdf(
    markdown_path: Path,
    output_path: Path,
    title: str,
    author: str,
    subject: str,
    allow_placeholders: bool,
) -> None:
    markdown_text = markdown_path.read_text(encoding="utf-8")
    placeholders = find_unfilled_placeholders(markdown_text)
    if placeholders and not allow_placeholders:
        placeholder_list = ", ".join(placeholders[:12])
        extra = "" if len(placeholders) <= 12 else f" (+{len(placeholders) - 12} altri)"
        raise SystemExit(
            "Refusing to generate a PDF with unfilled placeholders: "
            f"{placeholder_list}{extra}. "
            "Compila il report prima della generazione finale, oppure usa "
            "--allow-placeholders solo per bozze e controlli interni."
        )

    styles = build_styles()
    story = build_story(markdown_path, styles, text=markdown_text)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        rightMargin=1.7 * cm,
        leftMargin=1.7 * cm,
        topMargin=1.5 * cm,
        bottomMargin=1.7 * cm,
        title=title,
        author=author,
        subject=subject,
    )
    footer = footer_factory(title, author, subject)
    doc.build(story, onFirstPage=footer, onLaterPages=footer)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a PDF from an audit report Markdown file.")
    parser.add_argument("markdown", type=Path, help="Path to report-completo.md")
    parser.add_argument(
        "--output",
        type=Path,
        help="Output PDF path. Defaults to the Markdown filename with .pdf extension.",
    )
    parser.add_argument(
        "--title",
        default="Check-up Sito Web - Report completo",
        help="PDF metadata title and footer title.",
    )
    parser.add_argument("--author", default="Juri Buora", help="PDF metadata author.")
    parser.add_argument(
        "--subject",
        default="Analisi esterna e non invasiva del sito web",
        help="PDF metadata subject.",
    )
    parser.add_argument(
        "--allow-placeholders",
        action="store_true",
        help="Allow draft PDFs even if {{PLACEHOLDERS}} are still present.",
    )
    args = parser.parse_args()

    output = args.output or args.markdown.with_suffix(".pdf")
    generate_pdf(
        args.markdown,
        output,
        args.title,
        args.author,
        args.subject,
        args.allow_placeholders,
    )
    print(output)


if __name__ == "__main__":
    main()
