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
        HRFlowable,
        Image,
        PageBreak,
        Paragraph,
        SimpleDocTemplate,
        Spacer,
        Table,
        TableStyle,
    )
    from reportlab.graphics.shapes import Drawing, Rect, String
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

# Usable content width inside the page margins (leftMargin == rightMargin == 1.7 cm).
CONTENT_WIDTH = A4[0] - 3.4 * cm

# Localized caption for the homepage thumbnail shown on the cover.
PREVIEW_LABEL = {
    "it": "Anteprima homepage",
    "en": "Homepage preview",
    "pl": "Podgląd strony głównej",
    "ro": "Previzualizare pagina principala",
}

# Preferred cover screenshot filenames, best first. The renderer picks the
# first one present in a "screenshots/" folder next to the report Markdown.
COVER_SCREENSHOT_CANDIDATES = (
    "homepage-desktop-viewport.png",
    "homepage-desktop.png",
    "homepage-desktop-fullpage.png",
)

LANG_STRINGS = {
    "it": {
        "cover_title": "WebCheckup",
        "cover_subtitle": "Sicurezza, Fiducia e Visibilità",
        "page_label": "Pagina",
        "missing_image": "Screenshot non trovato",
        "default_pdf_title": "WebCheckup - Report completo",
        "default_subject": "Analisi esterna e non invasiva del sito web",
        "front_matter_labels": {
            "client": "Cliente",
            "site": "Sito analizzato",
            "date": "Data",
            "type": "Tipo di controllo",
        },
        "default_type": "Analisi esterna e non invasiva",
        "priority_chart_title": "Panoramica delle priorità",
    },
    "en": {
        "cover_title": "WebCheckup",
        "cover_subtitle": "Security, Trust and Visibility",
        "page_label": "Page",
        "missing_image": "Screenshot not found",
        "default_pdf_title": "WebCheckup - Full report",
        "default_subject": "External, non-invasive website analysis",
        "front_matter_labels": {
            "client": "Client",
            "site": "Website analyzed",
            "date": "Date",
            "type": "Type of check",
        },
        "default_type": "External, non-invasive analysis",
        "priority_chart_title": "Priority overview",
    },
    "pl": {
        "cover_title": "WebCheckup",
        "cover_subtitle": "Bezpieczeństwo, Zaufanie i Widoczność",
        "page_label": "Strona",
        "missing_image": "Nie znaleziono zrzutu ekranu",
        "default_pdf_title": "WebCheckup - Raport pełny",
        "default_subject": "Zewnętrzna, nieinwazyjna analiza strony internetowej",
        "front_matter_labels": {
            "client": "Klient",
            "site": "Analizowana strona",
            "date": "Data",
            "type": "Rodzaj kontroli",
        },
        "default_type": "Analiza zewnętrzna i nieinwazyjna",
        "priority_chart_title": "Przegląd priorytetów",
    },
    "ro": {
        "cover_title": "WebCheckup",
        "cover_subtitle": "Securitate, Incredere si Vizibilitate",
        "page_label": "Pagina",
        "missing_image": "Captura de ecran negasita",
        "default_pdf_title": "WebCheckup - Raport complet",
        "default_subject": "Analiza externa si neinvaziva a site-ului web",
        "front_matter_labels": {
            "client": "Client",
            "site": "Site analizat",
            "date": "Data",
            "type": "Tip de verificare",
        },
        "default_type": "Analiza externa si neinvaziva",
        "priority_chart_title": "Prezentare generala a prioritatilor",
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


# Severity palette shared by priority badges, colour-coded table cells and the
# priority-overview chart. Keyed by the lowercase priority word in every
# supported language so a document written in any --lang still colours cleanly.
PRIORITY_HIGH = "#c0392b"
PRIORITY_MEDIUM = "#d98a1f"
PRIORITY_LOW = "#2f8f6b"
PRIORITY_COLORS = {
    # Italian
    "alta": PRIORITY_HIGH, "media": PRIORITY_MEDIUM, "bassa": PRIORITY_LOW,
    # English
    "high": PRIORITY_HIGH, "medium": PRIORITY_MEDIUM, "low": PRIORITY_LOW,
    # Polish
    "wysoki": PRIORITY_HIGH, "sredni": PRIORITY_MEDIUM, "średni": PRIORITY_MEDIUM,
    "niski": PRIORITY_LOW,
    # Romanian
    "ridicata": PRIORITY_HIGH, "medie": PRIORITY_MEDIUM, "scazuta": PRIORITY_LOW,
}
# Canonical bucket (high/medium/low) for each priority word, so the chart can
# group and order mixed-language documents consistently.
_PRIORITY_BUCKET = {
    "alta": "high", "high": "high", "wysoki": "high", "ridicata": "high",
    "media": "medium", "medium": "medium", "sredni": "medium",
    "średni": "medium", "medie": "medium",
    "bassa": "low", "low": "low", "niski": "low", "scazuta": "low",
}


def priority_color(text: str) -> str | None:
    """Return the hex colour for a priority word, or None if unrecognized."""
    return PRIORITY_COLORS.get(text.strip().lower())


# Inline priority-label words (the "**Priorità:** Alta" line inside each
# finding) across supported languages. When a body line carries one of these
# labels, the trailing severity word is coloured to match the badge palette.
PRIORITY_LABEL_WORDS = ("Priorità", "Priorita", "Priority", "Prioritate", "Priorytet")
_PRIORITY_WORD_RE = re.compile(
    r"\b(" + "|".join(re.escape(word) for word in PRIORITY_COLORS) + r")\b",
    re.IGNORECASE,
)


def colorize_inline_priority(escaped_line: str) -> str:
    """Colour standalone severity words in an already-escaped line. Only call
    this for lines that contain a priority label, so ordinary prose that merely
    mentions e.g. 'media' is left untouched."""

    def wrap(match: re.Match) -> str:
        word = match.group(0)
        colour = priority_color(word)
        if not colour:
            return word
        return f'<font color="{colour}"><b>{word}</b></font>'

    return _PRIORITY_WORD_RE.sub(wrap, escaped_line)


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
        "cover_title_hero": ParagraphStyle(
            "CoverTitleHero",
            parent=base["Title"],
            fontName=BODY_FONT_BOLD,
            fontSize=30,
            leading=34,
            alignment=0,
            textColor=colors.white,
            spaceAfter=6,
        ),
        "cover_sub_hero": ParagraphStyle(
            "CoverSubHero",
            parent=base["Normal"],
            fontName=BODY_FONT,
            fontSize=13,
            leading=17,
            alignment=0,
            textColor=colors.HexColor("#bfe0d3"),
        ),
        "cover_caption": ParagraphStyle(
            "CoverCaption",
            parent=base["Normal"],
            fontName=BODY_FONT,
            fontSize=8,
            leading=11,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#7d8c86"),
            spaceBefore=4,
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
        "h4": ParagraphStyle(
            "H4",
            parent=base["BodyText"],
            fontName=BODY_FONT_BOLD,
            fontSize=9.8,
            leading=13,
            textColor=colors.HexColor("#3a4742"),
            spaceBefore=6,
            spaceAfter=2,
        ),
        "badge": ParagraphStyle(
            "Badge",
            parent=base["BodyText"],
            fontName=BODY_FONT_BOLD,
            fontSize=7.6,
            leading=9,
            alignment=TA_CENTER,
            textColor=colors.white,
        ),
        "cover_meta_label": ParagraphStyle(
            "CoverMetaLabel",
            parent=base["Normal"],
            fontName=BODY_FONT_BOLD,
            fontSize=9,
            leading=13,
            textColor=colors.HexColor("#7d8c86"),
        ),
        "cover_meta_value": ParagraphStyle(
            "CoverMetaValue",
            parent=base["Normal"],
            fontName=BODY_FONT,
            fontSize=10.5,
            leading=14,
            textColor=colors.HexColor("#26312d"),
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
    # Body cells whose text is a recognized priority word are rendered as a
    # coloured badge (white bold text on the severity colour) instead of plain
    # grey text, so scanning the priority column reads at a glance.
    priority_cells: list[tuple[int, int, str]] = []
    rendered: list[list[Paragraph]] = []
    for row_index, row in enumerate(rows):
        rendered_row: list[Paragraph] = []
        for col_index, cell in enumerate(row):
            value = cell.strip()
            colour = priority_color(value) if row_index > 0 else None
            if colour:
                priority_cells.append((col_index, row_index, colour))
                rendered_row.append(Paragraph(escape_inline(value), styles["badge"]))
            else:
                style = styles["table_header"] if row_index == 0 else styles["small"]
                rendered_row.append(Paragraph(escape_inline(value), style))
        rendered.append(rendered_row)

    table = Table(rendered, colWidths=table_widths(len(rows[0])), repeatRows=1)
    commands = [
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#153f32")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), BODY_FONT_BOLD),
        ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#cfd8d3")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
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
    for col_index, row_index, colour in priority_cells:
        commands.append(
            ("BACKGROUND", (col_index, row_index), (col_index, row_index), colors.HexColor(colour))
        )
    table.setStyle(TableStyle(commands))
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

    image = Image(str(image_path))
    image.drawWidth, image.drawHeight = image_size(image_path)

    # Thin border around the screenshot, centered, with the alt text as a
    # caption underneath — the same framed treatment as the cover thumbnail.
    frame = Table([[image]])
    frame.setStyle(
        TableStyle(
            [
                ("BOX", (0, 0), (-1, -1), 0.75, colors.HexColor("#cfd8d3")),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    holder = Table([[frame]], colWidths=[CONTENT_WIDTH])
    holder.setStyle(TableStyle([("ALIGN", (0, 0), (-1, -1), "CENTER")]))
    story.append(Spacer(1, 4))
    story.append(holder)
    if alt.strip():
        story.append(Paragraph(escape_inline(alt), styles["cover_caption"]))
    story.append(Spacer(1, 8))


def priority_counts_from_rows(rows: list[list[str]]) -> list[tuple[str, int, str]]:
    """Count findings per severity in a Markdown table.

    Returns (display_label, count, hex_colour) ordered high -> medium -> low.
    Counts at most one priority per row (the priority column), so a table with
    a single priority column yields one count per finding."""
    buckets: dict[str, list] = {}
    for row in rows[1:]:
        for cell in row:
            value = cell.strip()
            bucket = _PRIORITY_BUCKET.get(value.lower())
            if bucket:
                entry = buckets.setdefault(bucket, [value, 0, PRIORITY_COLORS[value.lower()]])
                entry[1] += 1
                break
    order = ["high", "medium", "low"]
    return [tuple(buckets[b]) for b in order if b in buckets]


def make_priority_chart(counts: list[tuple[str, int, str]], title: str) -> Drawing:
    """A compact horizontal bar chart summarizing findings by severity."""
    row_h = 21.0
    top_pad = 24.0
    label_w = 3.2 * cm
    count_gutter = 0.9 * cm
    bar_area = CONTENT_WIDTH - label_w - count_gutter
    height = top_pad + row_h * len(counts) + 4
    drawing = Drawing(CONTENT_WIDTH, height)
    drawing.add(
        String(
            0, height - 13, title,
            fontName=BODY_FONT_BOLD, fontSize=10.5,
            fillColor=colors.HexColor("#153f32"),
        )
    )
    max_count = max((c for _, c, _ in counts), default=1) or 1
    for index, (label, count, colour_hex) in enumerate(counts):
        baseline = height - top_pad - index * row_h
        drawing.add(
            String(
                0, baseline - 3, label,
                fontName=BODY_FONT, fontSize=9,
                fillColor=colors.HexColor("#3a4742"),
            )
        )
        drawing.add(
            Rect(
                label_w, baseline - 8, bar_area, 12,
                rx=3, ry=3, fillColor=colors.HexColor("#eef3f0"), strokeColor=None,
            )
        )
        bar_width = max(bar_area * count / max_count, 14)
        drawing.add(
            Rect(
                label_w, baseline - 8, bar_width, 12,
                rx=3, ry=3, fillColor=colors.HexColor(colour_hex), strokeColor=None,
            )
        )
        drawing.add(
            String(
                label_w + bar_width + 6, baseline - 3, str(count),
                fontName=BODY_FONT_BOLD, fontSize=9,
                fillColor=colors.HexColor(colour_hex),
            )
        )
    return drawing


def find_cover_screenshot(markdown_path: Path) -> Path | None:
    """Return a homepage screenshot to show on the cover, if one exists in a
    sibling 'screenshots/' folder. Returns None when nothing suitable is found."""
    screenshots_dir = markdown_path.parent / "screenshots"
    if not screenshots_dir.is_dir():
        return None
    for candidate in COVER_SCREENSHOT_CANDIDATES:
        path = screenshots_dir / candidate
        if path.exists():
            return path
    return None


def build_cover(
    story: list,
    styles: dict[str, ParagraphStyle],
    cover_title: str,
    cover_subtitle: str,
    client: str,
    site: str,
    report_date: str,
    audit_type: str,
    front_labels: dict[str, str],
    screenshot_path: Path | None,
    lang: str,
) -> None:
    """A designed cover: green hero band, a labelled meta card with a severity
    accent bar, and an optional framed homepage thumbnail."""
    story.append(Spacer(1, 1.3 * cm))

    hero = Table(
        [[[Paragraph(cover_title, styles["cover_title_hero"]),
           Paragraph(cover_subtitle, styles["cover_sub_hero"])]]],
        colWidths=[CONTENT_WIDTH],
    )
    hero.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#153f32")),
                ("LEFTPADDING", (0, 0), (-1, -1), 24),
                ("RIGHTPADDING", (0, 0), (-1, -1), 24),
                ("TOPPADDING", (0, 0), (-1, -1), 26),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 26),
            ]
        )
    )
    story.append(hero)
    story.append(Spacer(1, 0.55 * cm))

    meta_rows = [
        [Paragraph(front_labels["client"].upper(), styles["cover_meta_label"]),
         Paragraph(escape_inline(client), styles["cover_meta_value"])],
        [Paragraph(front_labels["site"].upper(), styles["cover_meta_label"]),
         Paragraph(escape_inline(site), styles["cover_meta_value"])],
        [Paragraph(front_labels["date"].upper(), styles["cover_meta_label"]),
         Paragraph(escape_inline(report_date), styles["cover_meta_value"])],
        [Paragraph(front_labels["type"].upper(), styles["cover_meta_label"]),
         Paragraph(escape_inline(audit_type), styles["cover_meta_value"])],
    ]
    meta = Table(meta_rows, colWidths=[3.6 * cm, CONTENT_WIDTH - 3.6 * cm])
    meta.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f4faf7")),
                ("LINEBEFORE", (0, 0), (0, -1), 3, colors.HexColor("#2f8f6b")),
                ("LINEBELOW", (0, 0), (-1, -2), 0.4, colors.HexColor("#e0ece7")),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 13),
                ("RIGHTPADDING", (0, 0), (-1, -1), 13),
                ("TOPPADDING", (0, 0), (-1, -1), 9),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
            ]
        )
    )
    story.append(meta)

    if screenshot_path is not None:
        story.append(Spacer(1, 0.9 * cm))
        thumb = Image(str(screenshot_path))
        max_width = CONTENT_WIDTH - 3.0 * cm
        max_height = 9.5 * cm
        ratio = min(max_width / thumb.imageWidth, max_height / thumb.imageHeight)
        thumb.drawWidth = thumb.imageWidth * ratio
        thumb.drawHeight = thumb.imageHeight * ratio
        frame = Table([[thumb]])
        frame.setStyle(
            TableStyle(
                [
                    ("BOX", (0, 0), (-1, -1), 0.75, colors.HexColor("#cfd8d3")),
                    ("LEFTPADDING", (0, 0), (-1, -1), 5),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                    ("TOPPADDING", (0, 0), (-1, -1), 5),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ]
            )
        )
        holder = Table([[frame]], colWidths=[CONTENT_WIDTH])
        holder.setStyle(TableStyle([("ALIGN", (0, 0), (-1, -1), "CENTER")]))
        story.append(holder)
        story.append(Paragraph(PREVIEW_LABEL.get(lang, PREVIEW_LABEL["it"]), styles["cover_caption"]))

    story.append(PageBreak())


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
    build_cover(
        story,
        styles,
        cover_title,
        cover_subtitle,
        client,
        site,
        report_date,
        audit_type,
        lang_strings["front_matter_labels"],
        find_cover_screenshot(markdown_path),
        lang,
    )

    table_rows: list[list[str]] = []
    priority_chart_done = False

    def flush_table() -> None:
        nonlocal table_rows, priority_chart_done
        if not table_rows:
            return
        story.append(make_table(table_rows, styles))
        story.append(Spacer(1, 8))
        # After the first table that carries a priority column, add a
        # severity-overview bar chart so the reader sees the shape of the
        # findings at a glance.
        if not priority_chart_done:
            counts = priority_counts_from_rows(table_rows)
            if counts:
                story.append(make_priority_chart(counts, lang_strings["priority_chart_title"]))
                story.append(Spacer(1, 10))
                priority_chart_done = True
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
            story.append(
                HRFlowable(
                    width=2.4 * cm,
                    thickness=2.2,
                    color=colors.HexColor("#2f8f6b"),
                    spaceBefore=0,
                    spaceAfter=9,
                    hAlign="LEFT",
                )
            )
            continue
        if line.startswith("#### "):
            story.append(Paragraph(escape_inline(line[5:]), styles["h4"]))
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

        escaped = escape_inline(line)
        if any(label in line for label in PRIORITY_LABEL_WORDS):
            escaped = colorize_inline_priority(escaped)
        story.append(Paragraph(escaped, styles["body"]))

    flush_table()
    return story


def footer_factory(title: str, author: str, subject: str, page_label: str = "Pagina"):
    def footer(canvas, doc) -> None:
        canvas.saveState()
        canvas.setTitle(title)
        canvas.setAuthor(author)
        canvas.setSubject(subject)
        canvas.setCreator("WebCheckup")
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
