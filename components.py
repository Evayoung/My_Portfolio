"""Reusable UI composition for NeoPortfolio."""

from __future__ import annotations

from typing import Any

from fasthtml.common import *
from faststrap import (
    Button,
    Card,
    Col,
    Container,
    EmptyState,
    Feature,
    FeatureGrid,
    FloatingLabel,
    Icon,
    Modal,
    Navbar,
    PageMeta,
    PricingGroup,
    Progress,
    Row,
    SEO,
    Testimonial,
    TestimonialSection,
    ToggleGroup,
)
import json

try:
    from .content import (
        ABOUT_STATS, ABOUT_SUMMARY, CODE_SAMPLE, CV_HIGHLIGHTS, DEVELOPER_NAME,
        DEVELOPER_NAME_SHORT, DEVELOPER_ROLE, EMAIL, EXPERIENCE, GITHUB_URL,
        HERO_SUMMARY, JOURNEY_PARAGRAPHS, KEYWORDS_GLOBAL, LINKEDIN_URL, LOCATION,
        PHONE, PORTFOLIO_FILTERS, PRICING_TIERS, PROJECTS, ROLE_TITLES, SERVICES,
        SITE_URL, SOCIAL_LINKS, TECHNICAL_SKILLS, TESTIMONIALS, WHATSAPP,
    )
except ImportError:
    from content import (
        ABOUT_STATS, ABOUT_SUMMARY, CODE_SAMPLE, CV_HIGHLIGHTS, DEVELOPER_NAME,
        DEVELOPER_NAME_SHORT, DEVELOPER_ROLE, EMAIL, EXPERIENCE, GITHUB_URL,
        HERO_SUMMARY, JOURNEY_PARAGRAPHS, KEYWORDS_GLOBAL, LINKEDIN_URL, LOCATION,
        PHONE, PORTFOLIO_FILTERS, PRICING_TIERS, PROJECTS, ROLE_TITLES, SERVICES,
        SITE_URL, SOCIAL_LINKS, TECHNICAL_SKILLS, TESTIMONIALS, WHATSAPP,
    )


# ── Helpers ───────────────────────────────────────────────────────────────────

def _section_header(title: str, copy: str) -> Div:
    return Div(
        H2(title, cls="section-title text-center"),
        Div(cls="section-divider mx-auto"),
        P(copy, cls="section-copy text-center mx-auto"),
        cls="section-header",
    )


def floating_select_field(
    name: str,
    label: str,
    *options: Any,
    input_id: str,
    input_cls: str = "contact-input",
    wrapper_cls: str = "mt-3",
    **kwargs: Any,
) -> Div:
    select_cls = f"form-select {input_cls}".strip()
    wrapper = "form-floating"
    if wrapper_cls:
        wrapper = f"{wrapper} {wrapper_cls}"
    return Div(
        Select(*options, id=input_id, name=name, cls=select_cls, aria_label=label, **kwargs),
        Label(label, fr=input_id),
        cls=wrapper,
    )


def floating_textarea_field(
    name: str,
    label: str,
    *,
    input_id: str,
    placeholder: str = "",
    rows: int = 6,
    required: bool = False,
    input_cls: str = "contact-input contact-textarea",
    wrapper_cls: str = "mt-3",
    **kwargs: Any,
) -> Div:
    textarea_cls = f"form-control {input_cls}".strip()
    wrapper = "form-floating"
    if wrapper_cls:
        wrapper = f"{wrapper} {wrapper_cls}"
    return Div(
        Textarea(
            id=input_id,
            name=name,
            placeholder=placeholder or label,
            rows=rows,
            cls=textarea_cls,
            required=required,
            **kwargs,
        ),
        Label(label, fr=input_id),
        cls=wrapper,
    )


def _social_icon(icon: str, href: str, label: str, color: str) -> A:
    icon_name = {"linkedin": "linkedin", "envelope": "envelope", "email": "envelope"}.get(icon, icon)
    return Div(
        Icon(icon_name, cls="social-icon-glyph"),
        href=href,
        target="_blank" if href.startswith("http") else None,
        rel="noreferrer" if href.startswith("http") else None,
        cls="social-icon-link",
        style=f"--brand:{color};",
        aria_label=label,
        title=label,
    )


def _skill_row(skill: Any) -> Div:
    return Div(
        Div(
            Span(skill.name, cls="skill-name"),
            Span(skill.badge, cls="skill-badge"),
            cls="skill-row-top",
        ),
        Progress(skill.score, cls="skill-progress-track", height="0.6rem"),
        cls="skill-row reveal-block",
    )


def _experience_item(item: Any) -> Div:
    return Div(
        Span(cls="timeline-dot"),
        Div(
            Span(item.year, cls="timeline-year-pill"),
            H4(item.title, cls="timeline-role"),
            P(item.company, cls="timeline-company"),
            P(item.summary, cls="timeline-summary"),
            cls="timeline-content",
        ),
        cls="timeline-entry reveal-block",
    )


def _stat_card(stat: Any) -> Col:
    return Col(
        Card(
            Div(H3(stat.value, cls="stat-value"), P(stat.label, cls="stat-label"), cls="stat-card-inner"),
            cls="about-stat-card h-100 reveal-block",
        ),
        span=6,
    )


def _project_card(project: Any, span: str) -> Col:
    sizes = {
        "wide":  {"lg": 8, "md": 12},
        "tall":  {"lg": 4, "md": 12},
        "small": {"lg": 4, "md": 6},
        "large": {"lg": 8, "md": 6},
    }
    # Build hover overlay buttons
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
        # Always show GitHub button (links to profile if no project URL)
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
                # Hover action layer
                Div(
                    *hover_buttons,
                    cls="project-hover-layer",
                ),
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
                    A("Case Study →", href=f"/project/{project.slug}",
                      cls="btn project-action-btn project-action-outline btn-sm"),
                    cls="project-actions d-flex gap-2 mt-3",
                ),
                cls="project-card-body",
            ),
            cls=f"project-card project-card-{span} h-100 reveal-block",
        ),
        span=12, **sizes[span],
    )


def _resume_metrics(downloads: dict[str, int]) -> Div:
    return Div(
        Div(Span("PDF", cls="analytics-key"), Span(str(downloads["pdf"]), cls="analytics-value"), cls="analytics-row"),
        Div(Span("Web", cls="analytics-key"), Span(str(downloads["web"]), cls="analytics-value"), cls="analytics-row"),
        Div(Span("Print", cls="analytics-key"), Span(str(downloads["print"]), cls="analytics-value"), cls="analytics-row"),
        cls="analytics-list",
        id="download-metrics",
    )


# ── Portfolio grid and controls ───────────────────────────────────────────────

def portfolio_grid(active_filter: str) -> Div:
    items = PROJECTS if active_filter == "all" else tuple(
        p for p in PROJECTS if p.category == active_filter
    )
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
        for slug, label in PORTFOLIO_FILTERS
    ]
    active_index = next((i for i, (slug, _) in enumerate(PORTFOLIO_FILTERS) if slug == active_filter), 0)
    return Div(
        ToggleGroup(
            *buttons,
            values=[slug for slug, _ in PORTFOLIO_FILTERS],
            active_index=active_index,
            active_cls="active",
            hidden_input=False,
            cls="portfolio-toggle-group",
        ),
        portfolio_grid(active_filter),
        id="portfolio-controls-shell",
        cls="portfolio-controls-shell",
    )


# ── Navigation ────────────────────────────────────────────────────────────────

def _mo_logo() -> Span:
    """Stylised 'MO' monogram logo mark for shared navbar branding."""
    return Span(
        Span("M", cls="mo-logo-m"),
        Span("O", cls="mo-logo-o"),
        cls="mo-logo",
    )


def _shared_nav(
    current: str = "",
    *,
    home: bool = False,
    include_download: bool = False,
    always_visible: bool = False,
) -> Nav:
    links = (
        [
            ("Home", "#hero"),
            ("About", "#about"),
            ("Services", "#services"),
            ("Portfolio", "#portfolio"),
            ("Blog", "/blog"),
            ("CV", "/cv"),
            ("Contact", "#contact"),
        ]
        if home
        else [
            ("Home", "/"),
            ("Blog", "/blog"),
            ("CV", "/cv"),
            ("Book", "/book"),
            ("Contact", "/#contact"),
        ]
    )

    nav_links = Div(
        *[
            A(
                label,
                href=href,
                cls=f"nav-link-item{' active' if current and href == current else ''}",
            )
            for label, href in links
        ],
        cls="navbar-nav neo-nav-links ms-auto align-items-lg-center",
    )

    actions: list[Any] = []
    if include_download:
        actions.append(
            A(
                Icon("download", cls="me-2"),
                "Download PDF",
                href="/resume/download/pdf",
                cls="btn hero-primary-btn btn-sm d-none d-lg-inline-flex",
            )
        )
    actions.append(A("Book a Call", href="/book", cls="btn talk-button"))

    nav_cls = "neo-glass-nav"
    if always_visible:
        nav_cls += " is-always-visible"

    return Navbar(
        nav_links,
        Div(*actions, cls="neo-nav-actions d-flex align-items-center gap-2 flex-wrap ms-lg-3 mt-3 mt-lg-0"),
        brand=_mo_logo(),
        brand_href="#hero" if home else "/",
        variant="dark",
        expand="lg",
        id="site-nav",
        cls=nav_cls,
    )


def site_nav() -> Nav:
    return _shared_nav(home=True)


def shared_inner_nav(current: str = "", *, include_download: bool = False) -> Nav:
    return _shared_nav(current, include_download=include_download, always_visible=True)


# Exported alias used by blog/cv/booking pages
def _page_nav_full() -> Nav:
    return site_nav()


# ── Sections ──────────────────────────────────────────────────────────────────

def hero_section() -> Section:
    return Section(
        Div(id="page-loader", cls="page-loader"),
        Div(cls="hero-background"),
        Div(cls="hero-overlay"),
        Div(cls="hero-particles", id="hero-particles"),
        Container(
            Row(
                # ── Left: text content ──
                Col(
                    Div(
                        Span("Available for work", cls="hero-availability-badge"),
                        H1(
                            Span(DEVELOPER_NAME_SHORT.split()[0] + " ", cls="hero-name-first"),
                            Span(DEVELOPER_NAME_SHORT.split()[1], cls="hero-name-last"),
                            cls="hero-name",
                        ),
                        P(Span(ROLE_TITLES[0], id="hero-role"), cls="hero-role"),
                        P(HERO_SUMMARY, cls="hero-summary"),
                        Div(
                            A("View My Work",  href="#portfolio",         cls="btn hero-primary-btn cta-pulse"),
                            A("Download CV",   href="/resume/download/pdf", cls="btn hero-secondary-btn", data_download_format="pdf"),
                            A(Icon("whatsapp", cls="me-1"), "Book a Call", href="/book", cls="btn hero-tertiary-btn"),
                            cls="hero-action-row",
                        ),
                        Div(
                            *[_social_icon(icon, href, label, color) for icon, href, label, color in SOCIAL_LINKS],
                            cls="hero-social-row",
                        ),
                        A(Span(cls="scroll-indicator-inner"), href="#about", cls="scroll-indicator"),
                        cls="hero-text-content",
                    ),
                    span=12, lg=7, cls="d-flex align-items-center",
                ),
                # ── Right: avatar orb ──
                Col(
                    Div(
                        Div(
                            Div(cls="hero-orb-ring hero-orb-ring-1"),
                            Div(cls="hero-orb-ring hero-orb-ring-2"),
                            Div(cls="hero-orb-ring hero-orb-ring-3"),
                            Div(
                                Img(src="/assets/images/me-photo.jpg", alt=DEVELOPER_NAME, cls="hero-avatar"),
                                Div(cls="hero-avatar-glow"),
                                cls="hero-avatar-shell tilt-card",
                            ),
                            cls="hero-orb-frame",
                        ),
                        # Floating stat badges
                        Div(
                            Span("10+", cls="hero-float-num"),
                            Span("Projects", cls="hero-float-label"),
                            cls="hero-float-badge hero-float-badge-1",
                        ),
                        Div(
                            Span("5+", cls="hero-float-num"),
                            Span("Years Exp.", cls="hero-float-label"),
                            cls="hero-float-badge hero-float-badge-2",
                        ),
                        cls="hero-visual-shell",
                    ),
                    span=12, lg=5, cls="d-flex justify-content-center align-items-center mt-5 mt-lg-0",
                ),
                cls="g-4 align-items-center",
            ),
        ),
        id="hero",
        cls="hero-section",
    )


def about_section() -> Section:
    return Section(
        Container(
            _section_header("About Me", ABOUT_SUMMARY),
            Row(
                Col(
                    Div(
                        Card(
                            Div(
                                Pre(Code(CODE_SAMPLE, cls="code-snippet-code"), cls="code-snippet-bg"),
                                Div(
                                    H3("My Journey", cls="panel-title"),
                                    *[P(paragraph, cls="panel-copy") for paragraph in JOURNEY_PARAGRAPHS],
                                    cls="journey-copy-wrap",
                                ),
                                cls="holo-layer-card",
                            ),
                            cls="about-panel journey-panel reveal-block",
                        ),
                        Div(
                            H3("Experience", cls="subsection-title"),
                            Div(
                                NotStr('<svg viewBox="0 0 400 120" class="timeline-svg"><path d="M14 90 C80 16, 168 12, 236 64 S334 118, 392 40"></path></svg>'),
                            ),
                            Div(*[_experience_item(item) for item in EXPERIENCE], cls="timeline-list"),
                            cls="experience-block",
                        ),
                        cls="about-left-column",
                    ),
                    span=12, lg=6,
                ),
                Col(
                    Div(
                        Card(
                            H3("Technical Skills", cls="panel-title"),
                            Div(*[_skill_row(skill) for skill in TECHNICAL_SKILLS], cls="skills-list"),
                            cls="about-panel skills-panel reveal-block",
                        ),
                        Row(*[_stat_card(stat) for stat in ABOUT_STATS], cls="g-3 about-stats-row"),
                        cls="about-right-column",
                    ),
                    span=12, lg=6, cls="mt-4 mt-lg-0",
                ),
                cls="g-4",
            ),
        ),
        id="about",
        cls="content-section about-section",
    )


def services_section() -> Section:
    flow = (
        ("Discover", "Clarify the product signal, users, and technical constraints."),
        ("Design",   "Shape the system, interactions, and delivery plan together."),
        ("Build",    "Implement with clear milestones, quality checks, and polish."),
        ("Launch",   "Ship with metrics, fixes, and room to evolve safely."),
    )
    service_cards = [
        Card(
            Div(
                Div(
                    Feature(
                        service.title,
                        service.summary,
                        icon=service.icon,
                        icon_cls="service-icon-box service-symbol",
                        icon_wrapper_cls="service-icon-box",
                        title_cls="service-title",
                        description_cls="service-summary mb-0",
                    ),
                    cls="service-feature-block",
                ),
                P(service.lead, cls="service-lead-copy"),
                Button(
                    "Open Details",
                    type="button",
                    cls="btn service-action-btn mt-4",
                    data_bs_toggle="modal",
                    data_bs_target="#serviceModal",
                    hx_get=f"/service-detail?slug={service.slug}",
                    hx_target="#service-detail-body",
                    hx_swap="innerHTML",
                ),
                cls="h-100 d-flex flex-column",
            ),
            cls="service-card h-100 reveal-block",
        )
        for service in SERVICES
    ]
    pricing_cards = [
        Card(
            Div(
                H3(tier.title, cls="pricing-title"),
                P(tier.price, cls="pricing-price"),
                P(tier.highlight, cls="pricing-highlight"),
                Ul(*[Li(point, cls="pricing-point") for point in tier.points], cls="list-unstyled pricing-points"),
                A(
                    "Book a Consultation",
                    href="/book",
                    cls=f"btn {'hero-primary-btn' if index == 1 else 'hero-secondary-btn'} mt-4 w-100",
                ),
                cls="pricing-card-face",
            ),
            cls=f"pricing-card h-100 reveal-block{' pricing-card-featured' if index == 1 else ''}",
        )
        for index, tier in enumerate(PRICING_TIERS)
    ]
    return Section(
        Container(
            _section_header(
                "My Services",
                "Full-stack, AI, and consulting services for serious products — built in Python, shipped on time.",
            ),
            FeatureGrid(*service_cards, columns=2, row_cls="g-4 services-grid-row"),
            Div(
                H3("How I Work", cls="subsection-title text-center"),
                Row(
                    *[
                        Col(
                            Div(
                                Span(f"0{index}", cls="process-index"),
                                H4(title, cls="process-title"),
                                P(copy, cls="process-copy"),
                                cls="process-node reveal-block h-100",
                            ),
                            span=12, sm=6, lg=3,
                        )
                        for index, (title, copy) in enumerate(flow, start=1)
                    ],
                    cls="g-3 process-flow-row",
                ),
                cls="services-process-wrap",
            ),
            Div(
                PricingGroup(
                    *pricing_cards,
                    title="Engagement Options",
                    subtitle="Flexible collaboration models depending on scope, urgency, and how hands-on you need me to be.",
                    title_cls="subsection-title text-center",
                    subtitle_cls="section-copy text-center mx-auto",
                    row_cls="g-4",
                ),
                cls="pricing-section-wrap",
            ),
        ),
        id="services",
        cls="content-section services-section",
    )


def portfolio_section(active_filter: str) -> Section:
    return Section(
        Container(
            _section_header(
                "My Portfolio",
                "A selection of real projects — AI agents, biometric systems, SaaS platforms, and more.",
            ),
            portfolio_controls(active_filter),
            Div(
                A("View All Projects", href="#portfolio", cls="btn view-projects-btn"),
                cls="text-center portfolio-cta-wrap",
            ),
        ),
        id="portfolio",
        cls="content-section portfolio-section",
    )


def testimonials_section() -> Div:
    return Section(
        Div(
            TestimonialSection(
                *[
                    Testimonial(
                        quote=item.quote,
                        author=item.author,
                        role=f"{item.role} | {item.company}",
                        rating=5,
                        cls="testimonial-card reveal-block",
                    )
                    for item in TESTIMONIALS
                ],
                title="Testimonials",
                subtitle="From people I've built things with.",
                columns=3,
                title_cls="section-title",
                subtitle_cls="section-copy text-center mx-auto",
                row_cls="g-4",
                id="testimonials",
            ),
            cls="content-section testimonials-section",
        ),
    )


def cv_zone_section(downloads: dict[str, int]) -> Section:
    highlights = [
        Div(H4(title, cls="cv-highlight-title"), P(copy, cls="cv-highlight-copy"), cls="cv-highlight-card")
        for title, copy in CV_HIGHLIGHTS
    ]
    return Section(
        Container(
            _section_header("CV Zone", "Download my full CV, view it online, or see the full interactive version."),
            Row(
                Col(
                    Card(
                        H3("Resume Access", cls="panel-title"),
                        P("Download a concise PDF, view the full interactive CV, or open a print layout.", cls="panel-copy"),
                        Div(
                            A("Download PDF", href="/resume/download/pdf", cls="btn hero-primary-btn cv-action-btn", data_download_format="pdf"),
                            A("Full CV →",    href="/cv",                  cls="btn hero-secondary-btn cv-action-btn"),
                            A("Print Version", href="/cv/print", target="_blank", cls="btn hero-secondary-btn cv-action-btn"),
                            cls="cv-action-row",
                        ),
                        Div(Div(id="download-progress-bar", cls="download-progress-bar"), cls="download-progress-track"),
                        Div(
                            A(Icon("whatsapp", cls="me-2"), "Quick WhatsApp", href=f"https://wa.me/{WHATSAPP.replace('+','')}", target="_blank", rel="noreferrer", cls="btn cv-preview-btn mt-2"),
                            cls="mt-3",
                        ),
                        cls="cv-panel reveal-block",
                    ),
                    span=12, lg=7,
                ),
                Col(
                    Div(
                        Card(H3("Format Analytics", cls="panel-title"), _resume_metrics(downloads), cls="cv-metrics-card reveal-block"),
                        Div(*highlights, cls="cv-highlight-grid"),
                        cls="cv-side-stack",
                    ),
                    span=12, lg=5, cls="mt-4 mt-lg-0",
                ),
                cls="g-4",
            ),
        ),
        id="cv-zone",
        cls="content-section cv-zone-section",
    )


def contact_section() -> Section:
    icons = [
        Card(
            Div(
                Div(Icon("envelope", cls="contact-icon-glyph"), cls="contact-icon-box"),
                Div(H4("Email", cls="contact-info-title"), P(EMAIL, cls="contact-info-copy"), cls="contact-info-body"),
                cls="contact-info-row",
            ),
            cls="contact-info-card reveal-block",
        ),
        Card(
            Div(
                Div(Icon("whatsapp", cls="contact-icon-glyph"), cls="contact-icon-box"),
                Div(
                    H4("WhatsApp", cls="contact-info-title"),
                    A(WHATSAPP, href=f"https://wa.me/{WHATSAPP.replace('+','')}", target="_blank",
                      rel="noreferrer", cls="contact-info-copy"),
                    cls="contact-info-body",
                ),
                cls="contact-info-row",
            ),
            cls="contact-info-card reveal-block",
        ),
        Card(
            Div(
                Div(Icon("geo-alt", cls="contact-icon-glyph"), cls="contact-icon-box"),
                Div(H4("Location", cls="contact-info-title"), P(LOCATION, cls="contact-info-copy"), cls="contact-info-body"),
                cls="contact-info-row",
            ),
            Div(cls="map-marker marker-one"),
            Div(cls="map-marker marker-two"),
            cls="contact-info-card contact-map-card reveal-block",
        ),
    ]
    socials = [_social_icon(icon, href, label, color) for icon, href, label, color in SOCIAL_LINKS]
    form = Form(
        FloatingLabel(
            "name",
            label="Full Name",
            placeholder="John Doe",
            required=True,
            input_id="contact-name",
            input_cls="contact-input",
        ),
        Row(
            Col(
                FloatingLabel(
                    "email",
                    label="Email Address",
                    input_type="email",
                    placeholder="hello@example.com",
                    required=True,
                    input_id="contact-email",
                    input_cls="contact-input",
                ),
                span=12, md=6,
            ),
            Col(
                FloatingLabel(
                    "subject",
                    label="Subject",
                    placeholder="Project Discussion",
                    input_id="contact-subject",
                    input_cls="contact-input",
                ),
                span=12, md=6, cls="mt-3 mt-md-0",
            ),
            cls="g-3 mt-1",
        ),
        floating_textarea_field(
            "message",
            "Message",
            input_id="contact-message",
            placeholder="Tell me about your project...",
            rows=6,
            required=True,
        ),
        Button(
            Icon("send", cls="contact-submit-icon"),
            "Send Message",
            type="submit",
            cls="btn contact-submit-btn mt-4 cta-pulse",
        ),
        Div(id="contact-result", cls="mt-3"),
        hx_post="/contact",
        hx_target="#contact-result",
        hx_swap="innerHTML",
        cls="contact-form",
    )
    availability = Card(
        Div(
            Div(Span(cls="availability-dot"), H4("Available for Projects", cls="availability-title"), cls="availability-header"),
            P("Currently accepting new projects and collaborations. Average response time: within 24 hours.", cls="availability-copy"),
            Div(
                Div(Span("Timezone:", cls="availability-label"), Strong("WAT (UTC+1)", cls="availability-value"), cls="availability-meta-item"),
                Div(Span("Best Contact:", cls="availability-label"), Strong("WhatsApp / Email", cls="availability-value"), cls="availability-meta-item"),
                cls="availability-meta-grid",
            ),
            Div(*socials, cls="contact-social-row"),
            cls="availability-card-inner",
        ),
        cls="availability-card reveal-block",
    )
    return Section(
        Container(
            _section_header("Let's Talk", "Ready to build something? I respond to every serious inquiry within 24 hours."),
            Row(
                Col(
                    Card(H3("Send Me a Message", cls="panel-title contact-title"), form, cls="contact-form-card h-100 reveal-block"),
                    span=12, lg=6,
                ),
                Col(
                    Div(*icons, availability, cls="contact-side-column"),
                    span=12, lg=6, cls="mt-4 mt-lg-0",
                ),
                cls="g-4",
            ),
        ),
        id="contact",
        cls="content-section contact-section",
    )


def footer() -> Footer:
    return Footer(
        Container(
            Div(
                P(f"© 2025 {DEVELOPER_NAME_SHORT}. Built with FastHTML + Faststrap.", cls="footer-copy"),
                Div(
                    A("Blog",   href="/blog",  cls="footer-link"),
                    A("CV",     href="/cv",    cls="footer-link"),
                    A("Book",   href="/book",  cls="footer-link"),
                    A("GitHub", href=GITHUB_URL, target="_blank", rel="noreferrer", cls="footer-link"),
                    cls="footer-links d-flex gap-3",
                ),
                cls="d-flex flex-column flex-md-row justify-content-between align-items-center gap-3",
            ),
        ),
        cls="site-footer",
    )


# ── Modals ────────────────────────────────────────────────────────────────────

def service_modal() -> Div:
    return Modal(
        Div("Select a service to load details.", id="service-detail-body", cls="modal-fragment-shell"),
        modal_id="serviceModal",
        title="Service Details",
        size="lg",
        centered=True,
        content_cls="neo-modal-content",
        header_cls="border-0",
        close_cls="btn-close-white",
    )


def project_preview_modal() -> Div:
    return Modal(
        Div("Preview will load here.", id="project-preview-body", cls="modal-fragment-shell"),
        modal_id="projectPreviewModal",
        title="Project Preview",
        size="xl",
        centered=True,
        content_cls="neo-modal-content",
        header_cls="border-0",
        close_cls="btn-close-white",
    )


def case_study_modal() -> Div:
    return Modal(
        Div("Case study will load here.", id="case-study-body", cls="modal-fragment-shell"),
        modal_id="caseStudyModal",
        title="Case Study",
        size="xl",
        centered=True,
        scrollable=True,
        content_cls="neo-modal-content",
        header_cls="border-0",
        close_cls="btn-close-white",
    )


def cv_preview_modal() -> Div:
    cards = [
        Div(H4(title, cls="cv-highlight-title"), P(copy, cls="cv-highlight-copy"), cls="cv-highlight-card")
        for title, copy in CV_HIGHLIGHTS
    ]
    return Modal(
        Div(*cards, cls="cv-preview-grid"),
        modal_id="cvPreviewModal",
        title="Interactive CV Preview",
        size="lg",
        centered=True,
        content_cls="neo-modal-content",
        header_cls="border-0",
        close_cls="btn-close-white",
    )


# ── Page shell (home) ─────────────────────────────────────────────────────────

def page_shell(active_filter: str, downloads: dict[str, int]) -> tuple[Any, ...]:
    structured_data = {
        "@context": "https://schema.org",
        "@type": "Person",
        "name": DEVELOPER_NAME,
        "url": SITE_URL,
        "jobTitle": DEVELOPER_ROLE,
        "email": EMAIL,
        "sameAs": [GITHUB_URL, LINKEDIN_URL],
    }
    structured = Script(json.dumps(structured_data), type="application/ld+json")
    return (
        *PageMeta(
            title=f"{DEVELOPER_NAME_SHORT} | Full-Stack & AI Systems Architect",
            description=(
                "Portfolio of Olorundare Micheal Babawale — Full-Stack & AI Systems Architect "
                "from Ilorin, Nigeria. Building intelligent systems with FastAPI, FastHTML, and Python."
            ),
            keywords=KEYWORDS_GLOBAL,
            url=SITE_URL,
            twitter_creator="@evayoung",
        ),
        structured,
        site_nav(),
        Main(
            hero_section(),
            about_section(),
            services_section(),
            portfolio_section(active_filter),
            testimonials_section(),
            cv_zone_section(downloads),
            contact_section(),
            footer(),
            cls="neo-app",
        ),
        service_modal(),
        project_preview_modal(),
        case_study_modal(),
        cv_preview_modal(),
    )
