"""Generate the branded PDF resume asset from structured CV content."""

from __future__ import annotations

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    HRFlowable,
    KeepTogether,
    ListFlowable,
    ListItem,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

try:
    from .content import SITE_URL
    from .services.content_service import (
        get_cv_meta,
        list_certifications,
        list_competencies,
        list_core_skills,
        list_education,
        list_languages,
        list_tool_categories,
        list_work_history,
    )
except ImportError:
    from content import SITE_URL
    from services.content_service import (
        get_cv_meta,
        list_certifications,
        list_competencies,
        list_core_skills,
        list_education,
        list_languages,
        list_tool_categories,
        list_work_history,
    )


BASE_DIR = Path(__file__).parent
OUTPUT_PATH = BASE_DIR / "assets" / "neoportfolio_resume.pdf"

NAVY = colors.HexColor("#07111F")
NAVY_SOFT = colors.HexColor("#112033")
CYAN = colors.HexColor("#46C8EE")
CYAN_SOFT = colors.HexColor("#DFF7FF")
PAGE_BG = colors.HexColor("#EDF3F8")
INK = colors.HexColor("#111827")
MUTED = colors.HexColor("#5F6F83")
LINE = colors.HexColor("#D7E5EF")
WHITE = colors.white


def styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    return {
        "name": ParagraphStyle(
            "ResumeName",
            parent=base["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=23,
            leading=26,
            textColor=WHITE,
            spaceAfter=8,
        ),
        "role": ParagraphStyle(
            "ResumeRole",
            parent=base["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=10.5,
            leading=13,
            textColor=CYAN,
        ),
        "contact": ParagraphStyle(
            "ResumeContact",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=8.1,
            leading=10.5,
            textColor=WHITE,
        ),
        "summary": ParagraphStyle(
            "ResumeSummary",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=9.1,
            leading=14.2,
            textColor=WHITE,
        ),
        "section": ParagraphStyle(
            "ResumeSection",
            parent=base["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=10.4,
            leading=12,
            textColor=NAVY,
            spaceAfter=5,
            textTransform="uppercase",
        ),
        "title": ParagraphStyle(
            "ResumeTitle",
            parent=base["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=9.5,
            leading=12,
            textColor=NAVY,
        ),
        "meta": ParagraphStyle(
            "ResumeMeta",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=8.2,
            leading=11,
            textColor=MUTED,
        ),
        "body": ParagraphStyle(
            "ResumeBody",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=8.5,
            leading=12.4,
            textColor=INK,
        ),
        "small": ParagraphStyle(
            "ResumeSmall",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=7.8,
            leading=10.4,
            textColor=MUTED,
        ),
        "footer": ParagraphStyle(
            "ResumeFooter",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=7.7,
            leading=10,
            textColor=MUTED,
            alignment=TA_CENTER,
        ),
        "pill": ParagraphStyle(
            "ResumePill",
            parent=base["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=8.1,
            leading=10,
            textColor=colors.HexColor("#0D6F8B"),
            alignment=TA_CENTER,
        ),
        "period": ParagraphStyle(
            "ResumePeriod",
            parent=base["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=7.8,
            leading=9.5,
            textColor=colors.HexColor("#0C7895"),
            alignment=TA_CENTER,
        ),
        "lang_right": ParagraphStyle(
            "ResumeLangRight",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=8,
            leading=10.5,
            textColor=MUTED,
            alignment=TA_RIGHT,
        ),
    }


def chip_table(items: list[str], style_map: dict[str, ParagraphStyle], columns: int = 2) -> Table:
    rows: list[list[Paragraph]] = []
    for idx in range(0, len(items), columns):
        chunk = items[idx : idx + columns]
        row = [Paragraph(item, style_map["contact"]) for item in chunk]
        if len(row) < columns:
            row += [Paragraph("", style_map["contact"]) for _ in range(columns - len(row))]
        rows.append(row)
    table = Table(rows, colWidths=[82 * mm, 82 * mm][:columns], hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.Color(1, 1, 1, alpha=0.05)),
                ("BOX", (0, 0), (-1, -1), 0.5, colors.Color(1, 1, 1, alpha=0.12)),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.Color(1, 1, 1, alpha=0.08)),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]
        )
    )
    return table


def section_heading(title: str, style_map: dict[str, ParagraphStyle]) -> list:
    return [
        Paragraph(title, style_map["section"]),
        HRFlowable(width="100%", thickness=1.2, lineCap="round", color=CYAN, spaceAfter=10),
    ]


def card(content: list, *, padding: int = 12) -> Table:
    table = Table([[content]], colWidths=[None], hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), WHITE),
                ("BOX", (0, 0), (-1, -1), 0.7, LINE),
                ("LEFTPADDING", (0, 0), (-1, -1), padding),
                ("RIGHTPADDING", (0, 0), (-1, -1), padding),
                ("TOPPADDING", (0, 0), (-1, -1), padding),
                ("BOTTOMPADDING", (0, 0), (-1, -1), padding),
            ]
        )
    )
    return table


def experience_card(item: object, style_map: dict[str, ParagraphStyle]) -> KeepTogether:
    item_top = Table(
        [[Paragraph(item.title, style_map["title"]), Paragraph(item.period, style_map["period"])]],
        colWidths=[112 * mm, 42 * mm],
    )
    item_top.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("ALIGN", (1, 0), (1, 0), "RIGHT"),
                ("BACKGROUND", (1, 0), (1, 0), CYAN_SOFT),
                ("BOX", (1, 0), (1, 0), 0.5, CYAN),
                ("LEFTPADDING", (0, 0), (0, 0), 0),
                ("RIGHTPADDING", (0, 0), (0, 0), 0),
                ("LEFTPADDING", (1, 0), (1, 0), 6),
                ("RIGHTPADDING", (1, 0), (1, 0), 6),
                ("TOPPADDING", (1, 0), (1, 0), 4),
                ("BOTTOMPADDING", (1, 0), (1, 0), 4),
            ]
        )
    )
    bullets = ListFlowable(
        [ListItem(Paragraph(bullet, style_map["body"])) for bullet in item.bullets],
        bulletType="bullet",
        leftPadding=12,
        bulletFontName="Helvetica-Bold",
        bulletColor=CYAN,
    )
    return KeepTogether(
        [
            card(
                [
                    item_top,
                    Spacer(1, 4),
                    Paragraph(f"{item.organisation} &middot; {item.location}", style_map["meta"]),
                    Spacer(1, 8),
                    bullets,
                ]
            ),
            Spacer(1, 10),
        ]
    )


def simple_stack(items: list[tuple[str, str, str | None]], style_map: dict[str, ParagraphStyle]) -> list:
    flowables: list = []
    for index, (title, subtitle, note) in enumerate(items):
        content = [
            Paragraph(title, style_map["title"]),
            Spacer(1, 3),
            Paragraph(subtitle, style_map["meta"]),
        ]
        if note:
            content.extend([Spacer(1, 5), Paragraph(note, style_map["small"])])
        flowables.append(card(content, padding=10))
        if index < len(items) - 1:
            flowables.append(Spacer(1, 8))
    return flowables


def pills_grid(values: list[str], style_map: dict[str, ParagraphStyle], column_width: float) -> list:
    rows: list[list[Paragraph]] = []
    for value in values:
        rows.append([Paragraph(value, style_map["pill"])])
    tables = []
    for paragraph in rows:
        table = Table([paragraph], colWidths=[column_width])
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), CYAN_SOFT),
                    ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#9ADDEF")),
                    ("LEFTPADDING", (0, 0), (-1, -1), 8),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                    ("TOPPADDING", (0, 0), (-1, -1), 4),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ]
            )
        )
        tables.extend([table, Spacer(1, 5)])
    return tables


def language_block(languages: list[tuple[str, str, int]], style_map: dict[str, ParagraphStyle]) -> list:
    blocks: list = []
    for index, (name, level, pct) in enumerate(languages):
        label_row = Table(
            [[Paragraph(name, style_map["title"]), Paragraph(level, style_map["lang_right"])]],
            colWidths=[52 * mm, 28 * mm],
        )
        label_row.setStyle(
            TableStyle(
                [
                    ("LEFTPADDING", (0, 0), (-1, -1), 0),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                ]
            )
        )
        bar = Table([["", ""]], colWidths=[pct * 0.8 * mm, (100 - pct) * 0.8 * mm], rowHeights=[4.5 * mm])
        bar.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (0, 0), CYAN),
                    ("BACKGROUND", (1, 0), (1, 0), colors.HexColor("#E6EEF4")),
                    ("LINEBEFORE", (0, 0), (0, 0), 0, WHITE),
                    ("LINEAFTER", (1, 0), (1, 0), 0, WHITE),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ]
            )
        )
        blocks.extend([label_row, bar])
        if index < len(languages) - 1:
            blocks.append(Spacer(1, 8))
    return blocks


def first_page(canvas, doc) -> None:
    canvas.saveState()
    canvas.setFillColor(PAGE_BG)
    canvas.rect(0, 0, A4[0], A4[1], stroke=0, fill=1)
    canvas.restoreState()


def later_pages(canvas, doc) -> None:
    first_page(canvas, doc)


def build_pdf(output_path: Path) -> None:
    cv_meta = get_cv_meta()
    work_history = list_work_history()
    education = list_education()
    certifications = list_certifications()
    core_skills = list_core_skills()
    competencies = list_competencies()
    tool_categories = list_tool_categories()
    languages = list_languages()
    s = styles()

    header_left = [
        Paragraph(cv_meta["name"], s["name"]),
        Paragraph(cv_meta["role"], s["role"]),
        Spacer(1, 8),
        Paragraph(cv_meta["summary"], s["summary"]),
        Spacer(1, 12),
        chip_table(
            [
                cv_meta["location"],
                cv_meta["phone"],
                cv_meta["email"],
                cv_meta["github"].replace("https://", ""),
                cv_meta["linkedin"].replace("https://", ""),
            ],
            s,
        ),
    ]
    brand_mark = Table(
        [[Paragraph("M", s["period"]), Paragraph("O", s["period"])]],
        colWidths=[16 * mm, 16 * mm],
        rowHeights=[16 * mm],
    )
    brand_mark.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), CYAN),
                ("TEXTCOLOR", (0, 0), (-1, -1), NAVY),
                ("BOX", (0, 0), (-1, -1), 1, NAVY_SOFT),
                ("INNERGRID", (0, 0), (-1, -1), 1, NAVY_SOFT),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]
        )
    )
    header = Table([[header_left, brand_mark]], colWidths=[150 * mm, 22 * mm])
    header.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), NAVY),
                ("BOX", (0, 0), (-1, -1), 0, NAVY),
                ("LEFTPADDING", (0, 0), (-1, -1), 16),
                ("RIGHTPADDING", (0, 0), (-1, -1), 16),
                ("TOPPADDING", (0, 0), (-1, -1), 16),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 16),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )

    experience_flowables = section_heading("Experience", s)
    for item in work_history:
        experience_flowables.append(experience_card(item, s))

    education_flowables = section_heading("Education", s) + simple_stack(
        [(item.degree, f"{item.institution} | {item.period}", item.note) for item in education],
        s,
    )
    certifications_flowables = section_heading("Certifications", s) + simple_stack(
        [(item.name, f"{item.issuer} | {item.year}", None) for item in certifications],
        s,
    )

    core_skills_flowables = section_heading("Core Skills", s) + [
        ListFlowable(
            [ListItem(Paragraph(skill, s["body"])) for skill in core_skills],
            bulletType="bullet",
            leftPadding=12,
            bulletFontName="Helvetica-Bold",
            bulletColor=CYAN,
        )
    ]
    tool_flowables = section_heading("Tools & Technologies", s)
    for category in tool_categories:
        tool_flowables.extend(
            [
                Paragraph(category.label, s["meta"]),
                Spacer(1, 4),
                Table(
                    [[Paragraph(", ".join(category.tools), s["body"])]],
                    colWidths=[None],
                    style=TableStyle(
                        [
                            ("BACKGROUND", (0, 0), (-1, -1), CYAN_SOFT),
                            ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#9ADDEF")),
                            ("LEFTPADDING", (0, 0), (-1, -1), 8),
                            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                            ("TOPPADDING", (0, 0), (-1, -1), 6),
                            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                        ]
                    ),
                ),
                Spacer(1, 7),
            ]
        )

    competencies_flowables = section_heading("Competencies", s) + pills_grid(list(competencies), s, 74 * mm)
    languages_flowables = section_heading("Languages", s) + language_block(list(languages), s)

    story = [
        header,
        Spacer(1, 14),
        *experience_flowables,
        Spacer(1, 8),
        *education_flowables,
        Spacer(1, 6),
        *certifications_flowables,
        Spacer(1, 6),
        *core_skills_flowables,
        Spacer(1, 6),
        *tool_flowables,
        Spacer(1, 6),
        *competencies_flowables,
        Spacer(1, 6),
        *languages_flowables,
        Spacer(1, 12),
        Paragraph(f"Portfolio: {SITE_URL.replace('https://', '')}", s["footer"]),
    ]

    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        leftMargin=10 * mm,
        rightMargin=10 * mm,
        topMargin=10 * mm,
        bottomMargin=10 * mm,
        title=f"{cv_meta['name']} CV",
        author=cv_meta["name"],
    )
    doc.build(story, onFirstPage=first_page, onLaterPages=later_pages)


def main() -> None:
    build_pdf(OUTPUT_PATH)
    print(f"Generated {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
