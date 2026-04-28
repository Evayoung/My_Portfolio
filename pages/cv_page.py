"""Full interactive CV page — Olorundare Micheal Babawale."""

from __future__ import annotations

from typing import Any

from fasthtml.common import (
    A, Div, Footer, H1, H2, H3, H4, I, Li, Main, Nav,
    P, Section, Small, Span, Strong, Td, Th, Tr, Table,
    Tbody, Thead, Ul, Script
)
from faststrap import Button, Card, Col, Container, Icon, PageMeta, Progress, Row, SEO
import json

try:
    from ..content import (
        DEVELOPER_NAME, DEVELOPER_NAME_SHORT, DEVELOPER_ROLE, EMAIL,
        GITHUB_URL, LINKEDIN_URL, PHONE, SITE_URL, WHATSAPP, LOCATION,
    )
    from ..services.content_service import (
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
    from content import (
        DEVELOPER_NAME, DEVELOPER_NAME_SHORT, DEVELOPER_ROLE, EMAIL,
        GITHUB_URL, LINKEDIN_URL, PHONE, SITE_URL, WHATSAPP, LOCATION,
    )
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
try:
    from ..ui.shared import inner_page_footer, shared_inner_nav
    from ..ui.github_widget import github_full_section
except ImportError:
    from ui.shared import inner_page_footer, shared_inner_nav
    from ui.github_widget import github_full_section


def _cv_nav() -> Nav:
    return shared_inner_nav("/cv", include_download=True)


def _work_item(item: Any) -> Div:
    return Div(
        Div(
            Div(cls="cv-timeline-dot"),
            cls="cv-timeline-track",
        ),
        Div(
            Div(
                Div(
                    H3(item.title, cls="cv-role-title"),
                    Span(item.period, cls="cv-period-pill"),
                    cls="d-flex justify-content-between align-items-start flex-wrap gap-2",
                ),
                Div(
                    Icon("building", cls="me-1 small"),
                    Strong(item.organisation),
                    Span(" | ", cls="text-muted"),
                    Span(item.location, cls="text-muted small"),
                    cls="cv-org-line mt-1",
                ),
                Ul(
                    *[Li(bullet, cls="cv-bullet") for bullet in item.bullets],
                    cls="cv-bullet-list mt-3",
                ),
                cls="cv-work-body",
            ),
            cls="cv-work-content reveal-block",
        ),
        cls="cv-timeline-entry",
    )


def _tool_category(cat: Any) -> Div:
    return Div(
        H4(cat.label, cls="cv-tool-category"),
        Div(
            *[Span(tool, cls="cv-tool-badge") for tool in cat.tools],
            cls="cv-tool-pills",
        ),
        cls="cv-tool-block reveal-block",
    )


def cv_page() -> tuple[Any, ...]:
    cv_meta = get_cv_meta()
    work_history = list_work_history()
    education = list_education()
    certifications = list_certifications()
    tool_categories = list_tool_categories()
    languages = list_languages()
    core_skills = list_core_skills()
    competencies = list_competencies()

    structured_data = {
        "@context": "https://schema.org",
        "@type": "Person",
        "name": DEVELOPER_NAME,
        "url": SITE_URL,
        "jobTitle": DEVELOPER_ROLE,
        "email": EMAIL,
        "telephone": PHONE,
        "address": {
            "@type": "PostalAddress",
            "addressLocality": "Ilorin",
            "addressRegion": "Kwara State",
            "addressCountry": "NG",
        },
        "sameAs": [GITHUB_URL, LINKEDIN_URL],
    }
    structured = Script(json.dumps(structured_data), type="application/ld+json")

    return (
        *PageMeta(
            title=f"Curriculum Vitae | {DEVELOPER_NAME_SHORT}",
            description=cv_meta["summary"][:160],
            keywords=["CV", "resume", "portfolio", "FastAPI", "Python", "AI", "Nigeria", "Ilorin", "developer"],
            url=f"{SITE_URL}/cv",
            twitter_creator="@evayoung",
        ),
        structured,
        _cv_nav(),
        Main(
            # ── Header band ─────────────────────────────────────────────────────
            Section(
                Div(cls="hero-overlay"),
                Container(
                    Div(
                        H1(DEVELOPER_NAME, cls="cv-header-name"),
                        P(DEVELOPER_ROLE, cls="cv-header-role"),
                        Div(
                            Span(Icon("geo-alt", cls="me-1"), LOCATION, cls="cv-contact-chip"),
                            Span(Icon("telephone", cls="me-1"), PHONE, cls="cv-contact-chip"),
                            Span(Icon("envelope", cls="me-1"), EMAIL, cls="cv-contact-chip"),
                            A(
                                Span(Icon("github", cls="me-1"), "GitHub", cls="cv-contact-chip"),
                                href=GITHUB_URL,
                                target="_blank",
                                rel="noreferrer",
                                cls="cv-contact-link",
                            ),
                            A(
                                Span(Icon("linkedin", cls="me-1"), "LinkedIn", cls="cv-contact-chip"),
                                href=LINKEDIN_URL,
                                target="_blank",
                                rel="noreferrer",
                                cls="cv-contact-link",
                            ),
                            cls="cv-contact-grid mt-4",
                        ),
                        Div(
                            A(Icon("download", cls="me-2"), "Download PDF",
                              href="/resume/download/pdf",
                              cls="btn hero-primary-btn"),
                            A(Icon("printer", cls="me-2"), "Print Version",
                              href="/cv/print",
                              target="_blank",
                              cls="btn hero-secondary-btn"),
                            A(Icon("whatsapp", cls="me-2"), "WhatsApp",
                              href=f"https://wa.me/{WHATSAPP.replace('+','')}",
                              target="_blank", rel="noreferrer",
                              cls="btn hero-secondary-btn"),
                            cls="d-flex gap-3 flex-wrap mt-4",
                        ),
                        cls="cv-header-content text-center",
                    ),
                ),
                cls="cv-header-section",
            ),

            # ── Body ────────────────────────────────────────────────────────────
            Section(
                Container(
                    Row(
                        # Left column — main content
                        Col(
                            # Professional Summary
                            Div(
                                H2("Professional Summary", cls="cv-section-title"),
                                P(cv_meta["summary"], cls="cv-summary-text reveal-block"),
                                cls="cv-section mb-5",
                            ),

                            # Work History
                            Div(
                                H2("Experience", cls="cv-section-title"),
                                Div(
                                    *[_work_item(item) for item in work_history],
                                    cls="cv-timeline",
                                ),
                                cls="cv-section mb-5",
                            ),

                            Row(
                                Col(
                                    Div(
                                        H2("Education", cls="cv-section-title"),
                                        Div(
                                            *[
                                                Div(
                                                    Div(cls="cv-timeline-dot cv-timeline-dot-edu"),
                                                    Div(
                                                        H3(edu.degree, cls="cv-role-title"),
                                                        P(edu.institution, cls="cv-org-line"),
                                                        Span(edu.period, cls="cv-period-pill"),
                                                        P(edu.note, cls="cv-edu-note mt-2"),
                                                        cls="cv-work-body reveal-block",
                                                    ),
                                                    cls="cv-timeline-entry",
                                                )
                                                for edu in education
                                            ],
                                            cls="cv-timeline",
                                        ),
                                        cls="cv-section mb-4",
                                    ),
                                    Div(
                                        H2("Certifications", cls="cv-section-title"),
                                        Div(
                                            *[
                                                Div(
                                                    Div(
                                                        Icon("award", cls="cv-cert-icon"),
                                                        cls="cv-cert-icon-box",
                                                    ),
                                                    Div(
                                                        Strong(cert.name),
                                                        P(f"{cert.issuer} | {cert.year}", cls="small text-muted mb-0"),
                                                        cls="",
                                                    ),
                                                    cls="cv-cert-row reveal-block",
                                                )
                                                for cert in certifications
                                            ],
                                            cls="cv-cert-list",
                                        ),
                                        cls="cv-section",
                                    ),
                                    span=12, lg=7,
                                ),
                                Col(
                                    Div(
                                        H2("Tools & Technologies", cls="cv-section-title"),
                                        Div(
                                            *[_tool_category(cat) for cat in tool_categories],
                                            cls="cv-tools-grid",
                                        ),
                                        cls="cv-section",
                                    ),
                                    span=12, lg=5, cls="mt-4 mt-lg-0",
                                ),
                                cls="g-4 mb-5",
                            ),

                            span=12, lg=8,
                        ),

                        # Right sidebar — skills + meta
                        Col(
                            Div(
                                # Core Skills
                                Card(
                                    H3("Core Skills", cls="cv-sidebar-title"),
                                    Ul(
                                        *[Li(skill, cls="cv-skill-item") for skill in core_skills],
                                        cls="cv-skill-list",
                                    ),
                                    cls="cv-sidebar-card mb-4",
                                ),

                                # Competencies
                                Card(
                                    H3("Competencies", cls="cv-sidebar-title"),
                                    Div(
                                        *[Span(c, cls="cv-competency-pill") for c in competencies],
                                        cls="d-flex flex-wrap gap-2",
                                    ),
                                    cls="cv-sidebar-card mb-4",
                                ),

                                # Languages
                                Card(
                                    H3("Languages", cls="cv-sidebar-title"),
                                    *[
                                        Div(
                                            Div(
                                                Span(lang, cls="fw-semibold small"),
                                                Span(level, cls="small text-muted"),
                                                cls="d-flex justify-content-between mb-1",
                                            ),
                                            Progress(pct, cls="skill-progress-track"),
                                            cls="mb-3",
                                        )
                                        for lang, level, pct in languages
                                    ],
                                    cls="cv-sidebar-card mb-4",
                                ),

                                # Contact CTA
                                Card(
                                    H3("Let's Build Together", cls="cv-sidebar-title"),
                                    P("Open to freelance projects, consulting, and collaborations.",
                                      cls="small text-muted mb-3"),
                                    A(
                                        Icon("whatsapp", cls="me-2"),
                                        "WhatsApp",
                                        href=f"https://wa.me/{WHATSAPP.replace('+','')}?text=Hi+Micheal%2C+I+saw+your+CV+and+would+like+to+discuss+a+project.",
                                        target="_blank", rel="noreferrer",
                                        cls="btn hero-primary-btn btn-sm w-100 mb-2",
                                    ),
                                    A(
                                        Icon("envelope", cls="me-2"),
                                        "Email Me",
                                        href=f"mailto:{EMAIL}",
                                        cls="btn hero-secondary-btn btn-sm w-100 mb-2",
                                    ),
                                    A("Book a Consultation ->", href="/book",
                                      cls="small neo-link d-block text-center"),
                                    cls="cv-sidebar-card",
                                ),

                                cls="cv-sidebar",
                            ),
                            span=12, lg=4,
                            cls="mt-4 mt-lg-0",
                        ),

                        cls="g-4",
                    ),
                ),
                cls="content-section cv-body-section",
            ),

            # ── GitHub Activity ──────────────────────────────────────────────────
            github_full_section(),

            # ── Footer ──────────────────────────────────────────────────────────
            inner_page_footer(inline=True),
            cls="neo-app",
        ),
    )

