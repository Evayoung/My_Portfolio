"""Standalone project detail page."""

from __future__ import annotations

from typing import Any

from fasthtml.common import *
from faststrap import Col, Container, EmptyState, Icon, Row, SEO

try:
    from ..content import DEVELOPER_NAME_SHORT, SITE_URL
    from ..ui.shared import inner_page_footer, shared_inner_nav
except ImportError:
    from content import DEVELOPER_NAME_SHORT, SITE_URL
    from ui.shared import inner_page_footer, shared_inner_nav


def project_detail_page(project: Any | None) -> Any:
    if not project:
        return (
            Title("Project Not Found"),
            shared_inner_nav("/"),
            Main(
                Container(
                    EmptyState(
                        title="Project not found",
                        description="This case study is missing or the link is no longer valid.",
                        cls="py-5",
                    ),
                    Div(
                        A("Back to Portfolio", href="/#portfolio", cls="btn hero-secondary-btn mt-3 d-block mx-auto"),
                        cls="text-center",
                    ),
                ),
                cls="neo-app",
            ),
        )

    return (
        *SEO(
            title=f"{project.title} | {DEVELOPER_NAME_SHORT}",
            description=project.summary,
            url=f"{SITE_URL}/project/{project.slug}",
            keywords=list(project.tech) + ["portfolio", "project"],
        ),
        shared_inner_nav("/"),
        Main(
            Section(
                Div(cls="hero-overlay"),
                Container(
                    Div(
                        Span(project.category.replace("-", " ").upper(), cls="modal-kicker"),
                        H1(project.title, cls="book-header-title mt-2"),
                        P(project.summary, cls="book-header-sub"),
                        Div(
                            *[Span(t, cls="project-tech-pill") for t in project.tech],
                            cls="d-flex gap-2 flex-wrap justify-content-center mt-3",
                        ),
                        A("All Projects", href="/#portfolio", cls="btn hero-secondary-btn mt-4"),
                        cls="text-center book-header-content",
                    ),
                ),
                cls="book-header-section",
            ),
            Section(
                Container(
                    Row(
                        Col(
                            Img(
                                src=project.image,
                                alt=project.title,
                                cls="project-image w-100 rounded-4 mb-4",
                                style="max-height:400px;object-fit:cover;",
                            ),
                            Div(
                                Div(
                                    Span("Complexity", cls="modal-meta-label"),
                                    Div(Div(cls="metric-bar-fill", style=f"width:{project.complexity}%;"), cls="metric-bar-track"),
                                    Span(f"{project.complexity}%", cls="metric-meta-value"),
                                    cls="metric-meta-card mb-3",
                                ),
                                Div(
                                    Span("Client Satisfaction", cls="modal-meta-label"),
                                    Div(Div(cls="metric-bar-fill", style=f"width:{project.satisfaction}%;"), cls="metric-bar-track"),
                                    Span(f"{project.satisfaction}%", cls="metric-meta-value"),
                                    cls="metric-meta-card",
                                ),
                                cls="project-detail-metrics case-study-metrics",
                            ),
                            span=12,
                            lg=6,
                            cls="project-detail-media-col",
                        ),
                        Col(
                            Div(
                                H2("Project Narrative", cls="cv-section-title"),
                                P(project.narrative, cls="panel-copy mb-4"),
                                H3("Tech Stack", cls="subsection-title"),
                                Div(*[Span(t, cls="project-tech-pill") for t in project.tech], cls="project-tech-row mb-4"),
                                Div(
                                    A(
                                        Icon("whatsapp", cls="me-2"),
                                        "Discuss This Project",
                                        href="https://wa.me/2349029952120?text=Hi+Micheal%2C+I+saw+your+project+and+would+love+to+discuss+something+similar.",
                                        target="_blank",
                                        rel="noreferrer",
                                        cls="btn hero-primary-btn w-100",
                                    ),
                                    A(
                                        "Book a Consultation ->",
                                        href="/book",
                                        cls="btn hero-secondary-btn w-100",
                                    ),
                                    cls="project-detail-actions",
                                ),
                                cls="project-detail-copy",
                            ),
                            span=12,
                            lg=6,
                            cls="project-detail-copy-col mt-4 mt-lg-0",
                        ),
                        cls="g-4",
                    ),
                ),
                cls="content-section project-detail-section",
            ),
            inner_page_footer(),
            cls="neo-app",
        ),
    )

