"""Booking / consultation page — WhatsApp + project briefing form."""

from __future__ import annotations

from typing import Any

from fasthtml.common import (
    A, Button, Div, Footer, Form, H1, H2, H3, H4, Input,
    Main, Nav, Option, P, Section, Span, Strong,
)
from faststrap import Card, Col, Container, FloatingLabel, Icon, Row, SEO

try:
    from ..content import (
        DEVELOPER_NAME_SHORT, DEVELOPER_ROLE, EMAIL,
        LOCATION, SITE_URL, WHATSAPP,
    )
    from ..services.content_service import list_services
except ImportError:
    from content import (
        DEVELOPER_NAME_SHORT, DEVELOPER_ROLE, EMAIL,
        LOCATION, SITE_URL, WHATSAPP,
    )
    from services.content_service import list_services
try:
    from ..ui.shared import floating_select_field, floating_textarea_field, inner_page_footer, loading_fragment_button, shared_inner_nav
except ImportError:
    from ui.shared import floating_select_field, floating_textarea_field, inner_page_footer, loading_fragment_button, shared_inner_nav


def _book_nav() -> Nav:
    return shared_inner_nav("/book")


def booking_page() -> tuple[Any, ...]:
    services = list_services()
    service_options = [Option("Select a service...", value="", disabled=True, selected=True)]
    service_options += [Option(s.title, value=s.slug) for s in services]

    budget_options = [
        Option("Select budget range...", value="", disabled=True, selected=True),
        Option("Under N100k",            value="under-100k"),
        Option("N100k - N250k",          value="100k-250k"),
        Option("N250k - N500k",          value="250k-500k"),
        Option("N500k - N1M",            value="500k-1m"),
        Option("Above N1M",              value="above-1m"),
        Option("Prefer to discuss",      value="discuss"),
    ]

    timeline_options = [
        Option("Select timeline...", value="", disabled=True, selected=True),
        Option("ASAP (under 2 weeks)",   value="asap"),
        Option("1 - 4 weeks",            value="1-4-weeks"),
        Option("1 - 2 months",           value="1-2-months"),
        Option("3+ months",              value="3-plus-months"),
        Option("Ongoing / retainer",     value="ongoing"),
        Option("Flexible",               value="flexible"),
    ]

    wa_message = (
        "Hi+Micheal%2C+I%27d+like+to+book+a+consultation."
        "+I+found+you+through+your+portfolio+and+have+a+project+I%27d+love+to+discuss."
    )

    return (
        *SEO(
            title=f"Book a Consultation | {DEVELOPER_NAME_SHORT}",
            description=(
                "Book a technical consultation or send a project brief to Olorundare Micheal Babawale "
                "- Full-Stack & AI Systems Architect based in Ilorin, Nigeria."
            ),
            keywords=["hire developer", "book developer", "FastAPI consultant", "AI engineer Nigeria",
                      "project brief", "Micheal Olorundare"],
            url=f"{SITE_URL}/book",
        ),
        _book_nav(),
        Main(
            # ── Header ─────────────────────────────────────────────────────────
            Section(
                Div(cls="hero-overlay"),
                Container(
                    Div(
                        Span("CONSULTATION", cls="modal-kicker"),
                        H1("Let's Talk About Your Project", cls="book-header-title"),
                        P(
                            "Send a project brief below or reach out directly via WhatsApp. "
                            "I respond within 24 hours.",
                            cls="book-header-sub",
                        ),
                        cls="text-center book-header-content",
                    ),
                ),
                cls="book-header-section",
            ),

            # ── Quick connect strip ─────────────────────────────────────────────
            Section(
                Container(
                    Row(
                        # WhatsApp CTA
                        Col(
                            Card(
                                Div(
                                    Div(
                                        Icon("whatsapp", cls="book-icon-glyph"),
                                        cls="book-icon-box book-icon-wa",
                                    ),
                                    Div(
                                        H3("WhatsApp", cls="book-connect-title"),
                                        P("Quickest way to reach me. Start a conversation now.",
                                          cls="book-connect-copy"),
                                    ),
                                    cls="book-connect-row",
                                ),
                                A(
                                    Icon("whatsapp", cls="me-2"),
                                    "Chat Now",
                                    href=f"https://wa.me/{WHATSAPP.replace('+','')}?text={wa_message}",
                                    target="_blank", rel="noreferrer",
                                    cls="btn hero-primary-btn mt-4 w-100",
                                ),
                                P(WHATSAPP, cls="small text-muted mt-2 text-center"),
                                cls="book-connect-card h-100 reveal-block",
                            ),
                            span=12, md=4,
                        ),
                        # Email
                        Col(
                            Card(
                                Div(
                                    Div(
                                        Icon("envelope-fill", cls="book-icon-glyph"),
                                        cls="book-icon-box book-icon-email",
                                    ),
                                    Div(
                                        H3("Email", cls="book-connect-title"),
                                        P("For formal project briefs, proposals, or NDAs.",
                                          cls="book-connect-copy"),
                                    ),
                                    cls="book-connect-row",
                                ),
                                A(
                                    Icon("envelope", cls="me-2"),
                                    "Send Email",
                                    href=f"mailto:{EMAIL}?subject=Project+Inquiry",
                                    cls="btn hero-secondary-btn mt-4 w-100",
                                ),
                                P(EMAIL, cls="small text-muted mt-2 text-center"),
                                cls="book-connect-card h-100 reveal-block",
                            ),
                            span=12, md=4,
                        ),
                        # Availability
                        Col(
                            Card(
                                Div(
                                    Div(cls="availability-dot", style="width:10px;height:10px;margin-right:0;"),
                                    H3("Currently Available", cls="book-connect-title mb-0"),
                                    cls="book-connect-row align-items-center",
                                ),
                                P(
                                    "Accepting new projects and consulting engagements. "
                                    "Based in Ilorin, Nigeria (WAT, UTC+1).",
                                    cls="book-connect-copy mt-3",
                                ),
                                Div(
                                    Div(
                                        Span("Timezone:", cls="availability-label"),
                                        Strong("WAT (UTC+1)", cls="availability-value"),
                                        cls="availability-meta-item",
                                    ),
                                    Div(
                                        Span("Response:", cls="availability-label"),
                                        Strong("Within 24h", cls="availability-value"),
                                        cls="availability-meta-item",
                                    ),
                                    cls="availability-meta-grid mt-3",
                                ),
                                cls="book-connect-card h-100 reveal-block",
                            ),
                            span=12, md=4,
                        ),
                        cls="g-4",
                    ),
                ),
                cls="content-section book-connect-section",
            ),

            # ── Project briefing form ───────────────────────────────────────────
            Section(
                Container(
                    Row(
                        Col(
                            Card(
                                H2("Project Brief Form", cls="panel-title mb-1"),
                                P("Fill this out so I can understand your project before we talk.",
                                  cls="panel-copy mb-4"),

                                Form(
                                    Input(
                                        type="text",
                                        name="company",
                                        tabindex="-1",
                                        autocomplete="off",
                                        aria_hidden="true",
                                        cls="d-none",
                                    ),
                                    # Step 1 — Who are you?
                                    Div(
                                        Div("01", cls="brief-step-num"),
                                        H4("About You", cls="brief-step-title"),
                                        cls="brief-step-header",
                                    ),
                                    Row(
                                        Col(
                                            FloatingLabel(
                                                "name",
                                                label="Full Name",
                                                placeholder="Your full name",
                                                required=True,
                                                input_id="brief-name",
                                                input_cls="contact-input",
                                            ),
                                            span=12, md=6,
                                        ),
                                        Col(
                                            FloatingLabel(
                                                "email",
                                                label="Email",
                                                input_type="email",
                                                placeholder="your@email.com",
                                                required=True,
                                                input_id="brief-email",
                                                input_cls="contact-input",
                                            ),
                                            span=12, md=6,
                                        ),
                                        cls="g-3 mt-1",
                                    ),
                                    Div(
                                        FloatingLabel(
                                            "whatsapp",
                                            label="WhatsApp Number",
                                            placeholder="+234... (optional)",
                                            input_id="brief-whatsapp",
                                            input_cls="contact-input",
                                            cls="mt-3",
                                        ),
                                    ),

                                    # Step 2 — About the project
                                    Div(
                                        Div("02", cls="brief-step-num"),
                                        H4("About the Project", cls="brief-step-title"),
                                        cls="brief-step-header mt-4",
                                    ),
                                    Row(
                                        Col(
                                            floating_select_field(
                                                "service",
                                                "Service Needed",
                                                *service_options,
                                                input_id="brief-service",
                                            ),
                                            span=12, md=6,
                                        ),
                                        Col(
                                            floating_select_field(
                                                "budget",
                                                "Budget Range",
                                                *budget_options,
                                                input_id="brief-budget",
                                            ),
                                            span=12, md=6,
                                        ),
                                        cls="g-3",
                                    ),
                                    floating_select_field(
                                        "timeline",
                                        "Preferred Timeline",
                                        *timeline_options,
                                        input_id="brief-timeline",
                                    ),

                                    # Step 3 — Project description
                                    Div(
                                        Div("03", cls="brief-step-num"),
                                        H4("Tell Me More", cls="brief-step-title"),
                                        cls="brief-step-header mt-4",
                                    ),
                                    floating_textarea_field(
                                        "message",
                                        "Project Description",
                                        input_id="brief-description",
                                        placeholder=(
                                            "Describe your project - what it does, who it's for, "
                                            "and what the biggest challenge is. The more detail, "
                                            "the better I can help."
                                        ),
                                        rows=6,
                                        required=True,
                                    ),

                                    # Submit
                                    loading_fragment_button(
                                        "Send Project Brief",
                                        endpoint="/book/submit",
                                        target="#brief-result",
                                        icon="send",
                                    ),
                                    Div(id="brief-result", cls="mt-3"),
                                    action="/book/submit",
                                    method="post",
                                    hx_post="/book/submit",
                                    hx_target="#brief-result",
                                    hx_swap="innerHTML",
                                    cls="brief-form",
                                ),
                                cls="book-form-card h-100 reveal-block",
                            ),
                            span=12, lg=7,
                        ),

                        # Sidebar — what to expect
                        Col(
                            Div(
                                Card(
                                    H3("What to Expect", cls="cv-sidebar-title"),
                                    Div(
                                        *[
                                            Div(
                                                Div(num, cls="expect-num"),
                                                Div(
                                                    Strong(title),
                                                    P(body, cls="small text-muted mb-0"),
                                                    cls="",
                                                ),
                                                cls="expect-row",
                                            )
                                            for num, title, body in [
                                                ("1", "I'll review your brief",
                                                 "Usually within 24 hours of receiving it."),
                                                ("2", "Discovery call",
                                                 "15-30 minute conversation via WhatsApp or call to clarify requirements."),
                                                ("3", "Proposal & timeline",
                                                 "A written scope of work with milestones and delivery dates."),
                                                ("4", "We build",
                                                 "Weekly check-ins, shared progress, and clear communication throughout."),
                                            ]
                                        ],
                                        cls="expect-list",
                                    ),
                                    cls="cv-sidebar-card mb-4",
                                ),
                                Card(
                                    H3("Services & Rates", cls="cv-sidebar-title"),
                                    *[
                                        Div(
                                            Div(
                                                Strong(s.title, cls="small"),
                                                P(s.price, cls="small text-muted mb-0 ms-auto"),
                                                cls="d-flex justify-content-between",
                                            ),
                                            cls="book-service-row",
                                        )
                                        for s in services
                                    ],
                                    P(
                                        "All rates are starting prices for clearly scoped work. "
                                        "Complex or longer-running projects are quoted individually.",
                                        cls="small text-muted mt-3 mb-0",
                                    ),
                                    cls="cv-sidebar-card",
                                ),
                                cls="book-sidebar",
                            ),
                            span=12, lg=5,
                            cls="mt-4 mt-lg-0",
                        ),
                        cls="g-4",
                    ),
                ),
                cls="content-section book-form-section",
            ),
            inner_page_footer(inline=True, include_book=False),
            cls="neo-app",
        ),
    )

