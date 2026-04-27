"""Portfolio grid and filtering UI."""

from __future__ import annotations

from fasthtml.common import *
from faststrap import Button, Card, Col, EmptyState, Icon, Row, ToggleGroup

try:
    from ..content import GITHUB_URL
    from ..services.content_service import get_portfolio_filters, list_projects
except ImportError:
    from content import GITHUB_URL
    from services.content_service import get_portfolio_filters, list_projects


def _project_card(project: Any, span: str) -> Col:
    sizes = {
        "wide": {"lg": 8, "md": 12},
        "tall": {"lg": 4, "md": 12},
        "small": {"lg": 4, "md": 6},
        "large": {"lg": 8, "md": 6},
    }

    hover_buttons = []
    if hasattr(project, "github_url") and project.github_url:
        hover_buttons.append(
            A(
                Icon("github", cls="me-2"),
                "GitHub",
                href=project.github_url,
                target="_blank",
                rel="noreferrer",
                cls="btn project-hover-btn project-hover-btn-github",
            )
        )
    else:
        hover_buttons.append(
            A(
                Icon("github", cls="me-2"),
                "GitHub",
                href=GITHUB_URL,
                target="_blank",
                rel="noreferrer",
                cls="btn project-hover-btn project-hover-btn-github",
                title="View on GitHub",
            )
        )

    if hasattr(project, "live_url") and project.live_url:
        hover_buttons.append(
            A(
                Icon("box-arrow-up-right", cls="me-2"),
                "Live Demo",
                href=project.live_url,
                target="_blank",
                rel="noreferrer",
                cls="btn project-hover-btn project-hover-btn-live",
            )
        )

    return Col(
        Card(
            Div(
                Img(src=project.image, alt=project.title, cls="project-image", loading="lazy"),
                Div(cls="project-image-overlay"),
                Div(*hover_buttons, cls="project-hover-layer"),
                cls="project-image-wrap",
            ),
            Div(
                Div(
                    Span(project.category.replace("-", " ").title(), cls="project-category-pill"),
                    Span("Featured", cls="project-featured-pill") if project.featured else "",
                    cls="project-meta-row",
                ),
                H3(project.title, cls="project-title"),
                P(project.summary, cls="project-summary"),
                Div(*[Span(item, cls="project-tech-pill") for item in project.tech], cls="project-tech-row"),
                Div(
                    Button(
                        "Preview",
                        type="button",
                        cls="btn project-action-btn btn-sm",
                        data_bs_toggle="modal",
                        data_bs_target="#projectPreviewModal",
                        hx_get=f"/project-preview?slug={project.slug}",
                        hx_target="#project-preview-body",
                        hx_swap="innerHTML",
                    ),
                    A("Case Study ->", href=f"/project/{project.slug}", cls="btn project-action-btn project-action-outline btn-sm"),
                    cls="project-actions d-flex gap-2 mt-3",
                ),
                cls="project-card-body",
            ),
            cls=f"project-card project-card-{span} h-100 reveal-block",
        ),
        span=12,
        **sizes[span],
    )


def portfolio_grid(active_filter: str) -> Div:
    items = list_projects(active_filter)
    spans = ("wide", "tall", "wide", "tall", "small", "large", "wide", "tall", "small", "large", "wide", "tall")
    if not items:
        return Div(
            EmptyState(
                title="No projects in this category yet.",
                description="Try another filter to explore the rest of the work.",
                cls="project-card portfolio-empty-card py-5",
            ),
            id="portfolio-grid",
            cls="portfolio-grid-shell",
        )
    return Div(
        Row(*[_project_card(p, spans[i % len(spans)]) for i, p in enumerate(items)], cls="g-4"),
        id="portfolio-grid",
        cls="portfolio-grid-shell",
    )


def portfolio_controls(active_filter: str) -> Div:
    portfolio_filters = get_portfolio_filters()
    buttons = [
        Button(
            label,
            type="button",
            variant="outline-secondary",
            cls=f"portfolio-toggle-btn{' active' if slug == active_filter else ''}",
            hx_get=f"/portfolio-grid?filter={slug}",
            hx_target="#portfolio-grid",
            hx_swap="outerHTML",
        )
        for slug, label in portfolio_filters
    ]
    active_index = next((i for i, (slug, _) in enumerate(portfolio_filters) if slug == active_filter), 0)
    return Div(
        ToggleGroup(
            *buttons,
            values=[slug for slug, _ in portfolio_filters],
            active_index=active_index,
            active_cls="active",
            hidden_input=False,
            cls="portfolio-toggle-group",
        ),
        portfolio_grid(active_filter),
        id="portfolio-controls-shell",
        cls="portfolio-controls-shell",
    )
