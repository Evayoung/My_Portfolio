"""Generate the branded PDF resume asset from structured CV content."""

from __future__ import annotations

from pathlib import Path

from reportlab.lib import colors
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
NAVY_SOFT = colors.HexColor("#102033")
CYAN = colors.HexColor("#46C8EE")
CYAN_SOFT = colors.HexColor("#DFF7FF")
TEXT = colors.HexColor("#202C3A")
MUTED = colors.HexColor("#68788B")
LINE = colors.HexColor("#D8E4EC")
WHITE = colors.white


def styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    return {
        "name": ParagraphStyle(
            "ResumeName",
            parent=base["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=24,
            leading=26,
            textColor=NAVY,
        ),
        "role": ParagraphStyle(
            "ResumeRole",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=12.5,
            leading=15,
            textColor=colors.HexColor("#0D7E9D"),
        ),
        "contact": ParagraphStyle(
            "ResumeContact",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=8.8,
            leading=11,
            textColor=TEXT,
        ),
        "section": ParagraphStyle(
            "ResumeSection",
            parent=base["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=10.8,
            leading=12,
            textColor=WHITE,
            alignment=1,
        ),
        "body": ParagraphStyle(
            "ResumeBody",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=9.1,
            leading=14.2,
            textColor=TEXT,
        ),
        "small": ParagraphStyle(
            "ResumeSmall",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=8.3,
            leading=11.3,
            textColor=MUTED,
        ),
        "title": ParagraphStyle(
            "ResumeTitle",
            parent=base["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=9.7,
            leading=12.2,
            textColor=NAVY,
        ),
        "sub": ParagraphStyle(
            "ResumeSub",
            parent=base["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=8.6,
            leading=11,
            textColor=TEXT,
        ),
        "meta": ParagraphStyle(
            "ResumeMeta",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=8.3,
            leading=10.6,
            textColor=MUTED,
        ),
        "label": ParagraphStyle(
            "ResumeLabel",
            parent=base["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=8.2,
            leading=10,
            textColor=MUTED,
        ),
        "footer": ParagraphStyle(
            "ResumeFooter",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=7.7,
            leading=10,
            textColor=MUTED,
            alignment=1,
        ),
        "chip": ParagraphStyle(
            "ResumeChip",
            parent=base["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=7.9,
            leading=9.6,
            textColor=colors.HexColor("#0B6F8A"),
            alignment=1,
        ),
    }


def _section_banner(title: str, style_map: dict[str, ParagraphStyle]) -> Table:
    table = Table([[Paragraph(title, style_map["section"])]], colWidths=[170 * mm], hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), CYAN),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    return table


def _lines(raw: str) -> list[str]:
    return [line.strip() for line in raw.splitlines() if line.strip()]


def _chip_table(values: list[str], style_map: dict[str, ParagraphStyle], *, columns: int = 2) -> Table:
    rows: list[list[Paragraph]] = []
    for index in range(0, len(values), columns):
        chunk = values[index : index + columns]
        row = [Paragraph(value, style_map["chip"]) for value in chunk]
        if len(row) < columns:
            row.extend(Paragraph("", style_map["chip"]) for _ in range(columns - len(row)))
        rows.append(row)
    table = Table(rows, colWidths=[84 * mm] * columns, hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), CYAN_SOFT),
                ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#A1DFF0")),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#C5EBF5")),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    return table


def _two_column_skill_table(left_items: list[str], right_items: list[str], style_map: dict[str, ParagraphStyle]) -> Table:
    max_rows = max(len(left_items), len(right_items), 1)
    rows = []
    for index in range(max_rows):
        left = f"• {left_items[index]}" if index < len(left_items) else ""
        right = f"• {right_items[index]}" if index < len(right_items) else ""
        rows.append([Paragraph(left, style_map["body"]), Paragraph(right, style_map["body"])])
    table = Table(rows, colWidths=[82 * mm, 82 * mm], hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 3),
                ("RIGHTPADDING", (0, 0), (-1, -1), 3),
                ("TOPPADDING", (0, 0), (-1, -1), 2),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
            ]
        )
    )
    return table


def _experience_block(item: object, style_map: dict[str, ParagraphStyle]) -> KeepTogether:
    header = Table(
        [[
            Paragraph(f"<b>{item.period}</b>", style_map["sub"]),
            Paragraph(f"<b>{item.organisation}</b><br/>{item.title}", style_map["title"]),
        ]],
        colWidths=[52 * mm, 118 * mm],
        hAlign="LEFT",
    )
    header.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
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
            header,
            Spacer(1, 4),
            Paragraph(item.location, style_map["meta"]),
            Spacer(1, 6),
            bullets,
            Spacer(1, 10),
        ]
    )


def _stack_block(items: list[tuple[str, str, str | None]], style_map: dict[str, ParagraphStyle]) -> list:
    flowables: list = []
    for index, (title, subtitle, note) in enumerate(items):
        flowables.append(Paragraph(title, style_map["title"]))
        flowables.append(Paragraph(subtitle, style_map["meta"]))
        if note:
            flowables.append(Spacer(1, 3))
            flowables.append(Paragraph(note, style_map["body"]))
        if index < len(items) - 1:
            flowables.append(Spacer(1, 8))
            flowables.append(HRFlowable(width="100%", thickness=0.5, color=LINE, spaceAfter=8, spaceBefore=0))
    return flowables


def _contact_lines(cv_meta: dict[str, str], style_map: dict[str, ParagraphStyle]) -> list:
    details = [
        cv_meta["location"],
        cv_meta["phone"],
        cv_meta["email"],
        cv_meta["linkedin"].replace("https://", "").replace("http://", ""),
        cv_meta["github"].replace("https://", "").replace("http://", ""),
    ]
    return [Paragraph(detail, style_map["contact"]) for detail in details if detail]


def _footer(canvas, doc) -> None:
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(MUTED)
    canvas.drawCentredString(A4[0] / 2, 10 * mm, f"Page {doc.page}")
    canvas.restoreState()


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

    left_skills = list(core_skills)
    right_skills = list(competencies[: len(competencies) // 2]) if competencies else []
    if competencies:
        midpoint = max(1, (len(core_skills) + len(competencies)) // 2)
        combined = list(core_skills) + list(competencies)
        left_skills = combined[:midpoint]
        right_skills = combined[midpoint:]

    contact_block = _contact_lines(cv_meta, s)
    tool_values = [f"{category.label}: {', '.join(category.tools)}" for category in tool_categories]
    language_values = [f"{name} - {level}" for name, level, _pct in languages]

    story: list = [
        Paragraph(cv_meta["name"], s["name"]),
        Paragraph(cv_meta["role"], s["role"]),
        Spacer(1, 6),
        *contact_block,
        Spacer(1, 8),
        HRFlowable(width="100%", thickness=1, color=LINE, spaceAfter=10, spaceBefore=0),
        _section_banner("Professional Profile", s),
        Spacer(1, 8),
        Paragraph(cv_meta["summary"], s["body"]),
        Spacer(1, 12),
        _section_banner("Core Skills", s),
        Spacer(1, 8),
        _two_column_skill_table(left_skills, right_skills, s),
        Spacer(1, 12),
        _section_banner("Career Summary", s),
        Spacer(1, 10),
    ]

    for item in work_history:
        story.append(_experience_block(item, s))

    story.extend(
        [
            _section_banner("Education", s),
            Spacer(1, 8),
            *_stack_block(
                [(item.degree, f"{item.institution} | {item.period}", item.note) for item in education],
                s,
            ),
            Spacer(1, 12),
            _section_banner("Certifications", s),
            Spacer(1, 8),
            *_stack_block(
                [(item.name, f"{item.issuer} | {item.year}", None) for item in certifications],
                s,
            ),
            Spacer(1, 12),
            _section_banner("Tools & Technologies", s),
            Spacer(1, 8),
            _chip_table(tool_values, s, columns=1),
            Spacer(1, 12),
            _section_banner("Languages", s),
            Spacer(1, 8),
            _chip_table(language_values, s, columns=1),
            Spacer(1, 12),
            Paragraph(f"Portfolio: {SITE_URL.replace('https://', '')}", s["footer"]),
        ]
    )

    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        leftMargin=20 * mm,
        rightMargin=20 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm,
        title=f"{cv_meta['name']} CV",
        author=cv_meta["name"],
    )
    doc.build(story, onFirstPage=_footer, onLaterPages=_footer)


def main() -> None:
    build_pdf(OUTPUT_PATH)
    print(f"Generated {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
