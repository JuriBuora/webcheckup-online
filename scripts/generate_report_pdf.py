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
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
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


FONTS_DIR = Path(__file__).resolve().parent / "fonts"
BODY_FONT = "Helvetica"
BODY_FONT_BOLD = "Helvetica-Bold"
BODY_FONT_ITALIC = "Helvetica-Oblique"


def register_fonts() -> None:
    """Embed Liberation Sans so accented characters outside WinAnsi (Polish,
    Romanian, Nordic diacritics) render correctly instead of turning into
    garbled boxes with the PDF base-14 Helvetica. Falls back to Helvetica
    (ASCII/Western-European accents only) if the bundled font is missing."""
    global BODY_FONT, BODY_FONT_BOLD, BODY_FONT_ITALIC
    regular = FONTS_DIR / "LiberationSans-Regular.ttf"
    bold = FONTS_DIR / "LiberationSans-Bold.ttf"
    italic = FONTS_DIR / "LiberationSans-Italic.ttf"
    if not (regular.exists() and bold.exists() and italic.exists()):
        return
    pdfmetrics.registerFont(TTFont("LiberationSans", str(regular)))
    pdfmetrics.registerFont(TTFont("LiberationSans-Bold", str(bold)))
    pdfmetrics.registerFont(TTFont("LiberationSans-Italic", str(italic)))
    pdfmetrics.registerFontFamily(
        "LiberationSans",
        normal="LiberationSans",
        bold="LiberationSans-Bold",
        italic="LiberationSans-Italic",
        boldItalic="LiberationSans-Bold",
    )
    BODY_FONT = "LiberationSans"
    BODY_FONT_BOLD = "LiberationSans-Bold"
    BODY_FONT_ITALIC = "LiberationSans-Italic"


register_fonts()

PAGEBREAK_MARKER = "<!-- pagebreak -->"
UNFILLED_PLACEHOLDER_RE = re.compile(r"{{[^{}]+}}")

LANG_STRINGS = {
    "it": {
        "cover_title": "Check-up Sito Web",
        "cover_subtitle": "Sicurezza, Fiducia e Visibilità",
        "page_label": "Pagina",
        "missing_image": "Screenshot non trovato",
        "default_pdf_title": "Check-up Sito Web - Report completo",
        "default_subject": "Analisi esterna e non invasiva del sito web",
        "front_matter_labels": {
            "client": "Cliente",
            "site": "Sito analizzato",
            "date": "Data",
            "type": "Tipo di controllo",
        },
        "default_type": "Analisi esterna e non invasiva",
    },
    "en": {
        "cover_title": "Website Check-up",
        "cover_subtitle": "Security, Trust and Visibility",
        "page_label": "Page",
        "missing_image": "Screenshot not found",
        "default_pdf_title": "Website Check-up - Full report",
        "default_subject": "External, non-invasive website analysis",
        "front_matter_labels": {
            "client": "Client",
            "site": "Website analyzed",
            "date": "Date",
            "type": "Type of check",
        },
        "default_type": "External, non-invasive analysis",
    },
    "pl": {
        "cover_title": "Check-up Strony Www",
        "cover_subtitle": "Bezpieczeństwo, Zaufanie i Widoczność",
        "page_label": "Strona",
        "missing_image": "Nie znaleziono zrzutu ekranu",
        "default_pdf_title": "Check-up Strony Www - Raport pełny",
        "default_subject": "Zewnętrzna, nieinwazyjna analiza strony internetowej",
        "front_matter_labels": {
            "client": "Klient",
            "site": "Analizowana strona",
            "date": "Data",
            "type": "Rodzaj kontroli",
        },
        "default_type": "Analiza zewnętrzna i nieinwazyjna",
    },
    "ro": {
        "cover_title": "Verificare Site Web",
        "cover_subtitle": "Securitate, Incredere si Vizibilitate",
        "page_label": "Pagina",
        "missing_image": "Captura de ecran negasita",
        "default_pdf_title": "Verificare Site Web - Raport complet",
        "default_subject": "Analiza externa si neinvaziva a site-ului web",
        "front_matter_labels": {
            "client": "Client",
            "site": "Site analizat",
            "date": "Data",
            "type": "Tip de verificare",
        },
        "default_type": "Analiza externa si neinvaziva",
    },
}

# Reverse lookup so front matter is recognized regardless of which language
# label the document actually uses (a document doesn't have to match --lang).
_FRONT_MATTER_LABEL_TO_KEY = {
    label: key
    for strings in LANG_STRINGS.values()
    for key, label in strings["front_matter_labels"].items()
}
_FRONT_MATTER_RE = re.compile(
    r"\*\*(" + "|".join(re.escape(label) for label in _FRONT_MATTER_LABEL_TO_KEY) + r"):\*\*\s*(.+)"
)


def escape_inline(text: str) -> str:
    """Escape minimal HTML and support a small Markdown inline subset."""
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"`([^`]+)`", r'<font name="Courier">\1</font>', text)
    return text


def strip_markdown_link(text: str) -> str:
    return re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)


def extract_front_matter(markdown: str) -> dict[str, str]:
    """Return a dict keyed by canonical field name (client/site/date/type),
    recognizing the front-matter label in any supported language."""
    fields: dict[str, str] = {}
    for line in markdown.splitlines()[:30]:
        match = _FRONT_MATTER_RE.match(line)
        if match:
            key = _FRONT_MATTER_LABEL_TO_KEY[match.group(1)]
            fields[key] = strip_markdown_link(match.group(2).strip())
    return fields


def find_unfilled_placeholders(markdown: str) -> list[str]:
    return sorted(set(UNFILLED_PLACEHOLDER_RE.findall(markdown)))


def build_styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    return {
        "cover_title": ParagraphStyle(
            "CoverTitle",
            parent=base["Title"],
            fontName=BODY_FONT_BOLD,
            fontSize=26,
            leading=31,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#153f32"),
            spaceAfter=18,
        ),
        "cover_sub": ParagraphStyle(
            "CoverSub",
            parent=base["Normal"],
            fontName=BODY_FONT,
            fontSize=13,
            leading=18,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#4c5f58"),
            spaceAfter=8,
        ),
        "h1": ParagraphStyle(
            "H1",
            parent=base["Heading1"],
            fontName=BODY_FONT_BOLD,
            fontSize=20,
            leading=25,
            textColor=colors.HexColor("#153f32"),
            spaceBefore=12,
            spaceAfter=10,
        ),
        "h2": ParagraphStyle(
            "H2",
            parent=base["Heading2"],
            fontName=BODY_FONT_BOLD,
            fontSize=15,
            leading=19,
            textColor=colors.HexColor("#1f6b58"),
            spaceBefore=10,
            spaceAfter=7,
        ),
        "h3": ParagraphStyle(
            "H3",
            parent=base["Heading3"],
            fontName=BODY_FONT_BOLD,
            fontSize=12,
            leading=15,
            textColor=colors.HexColor("#9a5a16"),
            spaceBefore=8,
            spaceAfter=5,
        ),
        "body": ParagraphStyle(
            "Body",
            parent=base["BodyText"],
            fontName=BODY_FONT,
            fontSize=9.4,
            leading=13.2,
            textColor=colors.HexColor("#26312d"),
            spaceAfter=6,
        ),
        "bullet": ParagraphStyle(
            "Bullet",
            parent=base["BodyText"],
            fontName=BODY_FONT,
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
            fontName=BODY_FONT,
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
            fontName=BODY_FONT_ITALIC,
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
            fontName=BODY_FONT,
            fontSize=8,
            leading=10,
            textColor=colors.HexColor("#6d7975"),
        ),
        "table_header": ParagraphStyle(
            "TableHeader",
            parent=base["BodyText"],
            fontName=BODY_FONT_BOLD,
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
                ("FONTNAME", (0, 0), (-1, 0), BODY_FONT_BOLD),
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


def add_image(
    story: list,
    image_ref: str,
    alt: str,
    markdown_path: Path,
    styles: dict[str, ParagraphStyle],
    lang_strings: dict[str, str],
) -> None:
    image_path = (markdown_path.parent / image_ref).resolve()
    if not image_path.exists():
        missing_label = lang_strings["missing_image"]
        story.append(Paragraph(f"[{missing_label}: {escape_inline(image_ref)}]", styles["small"]))
        return

    story.append(Paragraph(escape_inline(alt), styles["small"]))
    story.append(Spacer(1, 5))
    image = Image(str(image_path))
    image.drawWidth, image.drawHeight = image_size(image_path)
    story.append(image)
    story.append(Spacer(1, 8))


def build_story(
    markdown_path: Path,
    styles: dict[str, ParagraphStyle],
    text: str | None = None,
    lang: str = "it",
) -> list:
    text = text if text is not None else markdown_path.read_text(encoding="utf-8")
    lang_strings = LANG_STRINGS.get(lang, LANG_STRINGS["it"])
    fields = extract_front_matter(text)
    client = fields.get("client", "[Cliente]")
    site = fields.get("site", "[Sito]")
    report_date = fields.get("date", "[Data]")
    audit_type = fields.get("type", lang_strings["default_type"])
    cover_title = lang_strings["cover_title"]
    cover_subtitle = lang_strings["cover_subtitle"]

    story: list = []
    story.append(Spacer(1, 2.5 * cm))
    story.append(Paragraph(cover_title, styles["cover_title"]))
    story.append(Paragraph(cover_subtitle, styles["cover_sub"]))
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
            add_image(story, image_match.group(2), image_match.group(1), markdown_path, styles, lang_strings)
            continue

        if line.startswith("# "):
            continue
        if line.startswith("## "):
            title = line[3:]
            if title == cover_subtitle:
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


def footer_factory(title: str, author: str, subject: str, page_label: str = "Pagina"):
    def footer(canvas, doc) -> None:
        canvas.saveState()
        canvas.setTitle(title)
        canvas.setAuthor(author)
        canvas.setSubject(subject)
        canvas.setCreator("Website Trust & Security Mini-Audit Service")
        canvas.setProducer("ReportLab")
        canvas.setFont(BODY_FONT, 8)
        canvas.setFillColor(colors.HexColor("#6d7975"))
        canvas.drawString(doc.leftMargin, 1.1 * cm, title)
        canvas.drawRightString(A4[0] - doc.rightMargin, 1.1 * cm, f"{page_label} {doc.page}")
        canvas.restoreState()

    return footer


def generate_pdf(
    markdown_path: Path,
    output_path: Path,
    title: str,
    author: str,
    subject: str,
    allow_placeholders: bool,
    lang: str = "it",
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

    lang_strings = LANG_STRINGS.get(lang, LANG_STRINGS["it"])
    styles = build_styles()
    story = build_story(markdown_path, styles, text=markdown_text, lang=lang)
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
    footer = footer_factory(title, author, subject, page_label=lang_strings["page_label"])
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
        "--lang",
        choices=sorted(LANG_STRINGS.keys()),
        default="it",
        help="Report language: controls the cover title/subtitle, page footer label and "
        "default PDF title/subject. Default: it (unchanged historical behavior).",
    )
    parser.add_argument(
        "--title",
        default=None,
        help="PDF metadata title and footer title. Defaults to the --lang-appropriate title.",
    )
    parser.add_argument("--author", default="Juri Buora", help="PDF metadata author.")
    parser.add_argument(
        "--subject",
        default=None,
        help="PDF metadata subject. Defaults to the --lang-appropriate subject.",
    )
    parser.add_argument(
        "--allow-placeholders",
        action="store_true",
        help="Allow draft PDFs even if {{PLACEHOLDERS}} are still present.",
    )
    args = parser.parse_args()

    lang_strings = LANG_STRINGS.get(args.lang, LANG_STRINGS["it"])
    title = args.title or lang_strings["default_pdf_title"]
    subject = args.subject or lang_strings["default_subject"]

    output = args.output or args.markdown.with_suffix(".pdf")
    generate_pdf(
        args.markdown,
        output,
        title,
        args.author,
        subject,
        args.allow_placeholders,
        lang=args.lang,
    )
    print(output)


if __name__ == "__main__":
    main()
