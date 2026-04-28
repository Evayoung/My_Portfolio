"""Shared UI helpers, navigation, and shell fragments."""

from __future__ import annotations

from typing import Any

from fasthtml.common import *
from faststrap import Icon, Navbar
from faststrap.presets import LoadingButton

try:
    from ..content import DEVELOPER_NAME_SHORT, GITHUB_URL
except ImportError:
    from content import DEVELOPER_NAME_SHORT, GITHUB_URL


def section_header(title: str, copy: str) -> Div:
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


def social_icon(icon: str, href: str, label: str, color: str) -> A:
    icon_name = {"linkedin": "linkedin", "envelope": "envelope", "email": "envelope"}.get(icon, icon)
    return A(
        Icon(icon_name, cls="social-icon-glyph"),
        href=href,
        target="_blank" if href.startswith("http") else None,
        rel="noreferrer" if href.startswith("http") else None,
        cls="social-icon-link",
        style=f"--brand:{color};",
        aria_label=label,
        title=label,
    )


def mo_logo() -> Span:
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
        brand=mo_logo(),
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


def page_nav_full() -> Nav:
    return site_nav()


def inner_page_footer(*, inline: bool = False, include_book: bool = True) -> Footer:
    copyright_mark = chr(169)
    middle_dot = chr(183)
    links = [
        A("Home", href="/", cls="footer-link"),
        A("Blog", href="/blog", cls="footer-link"),
        A("CV", href="/cv", cls="footer-link"),
    ]
    if include_book:
        links.append(A("Book", href="/book", cls="footer-link"))

    if inline:
        footer_children: list[Any] = [f"{copyright_mark} 2025 {DEVELOPER_NAME_SHORT} {middle_dot} "]
        for idx, link in enumerate(links):
            footer_children.append(link)
            if idx < len(links) - 1:
                footer_children.append(f" {middle_dot} ")

        return Footer(
            Container(
                P(*footer_children, cls="footer-copy text-center"),
            ),
            cls="site-footer",
        )

    return Footer(
        Container(
            Div(
                Span(f"{copyright_mark} 2025 {DEVELOPER_NAME_SHORT}.", cls="footer-copy"),
                Div(
                    *links,
                    cls="footer-links",
                ),
                cls="d-flex flex-column flex-md-row justify-content-between align-items-center gap-3",
            ),
        ),
        cls="site-footer",
    )


def footer() -> Footer:
    copyright_mark = chr(169)
    return Footer(
        Container(
            Div(
                P(f"{copyright_mark} 2025 {DEVELOPER_NAME_SHORT}. Built with FastHTML + Faststrap.", cls="footer-copy"),
                Div(
                    A("Blog", href="/blog", cls="footer-link"),
                    A("CV", href="/cv", cls="footer-link"),
                    A("Book", href="/book", cls="footer-link"),
                    A("GitHub", href=GITHUB_URL, target="_blank", rel="noreferrer", cls="footer-link"),
                    cls="footer-links d-flex gap-3",
                ),
                cls="d-flex flex-column flex-md-row justify-content-between align-items-center gap-3",
            ),
        ),
        cls="site-footer",
    )


def loading_fragment_button(
    label: str,
    *,
    endpoint: str,
    target: str,
    icon: str | None = None,
    button_cls: str = "btn contact-submit-btn mt-4 cta-pulse",
    variant: str = "primary",
) -> Any:
    children: list[Any] = []
    if icon:
        children.append(Icon(icon, cls="contact-submit-icon"))
    children.append(label)
    return LoadingButton(
        *children,
        endpoint=endpoint,
        target=target,
        method="post",
        variant=variant,
        hx_include="closest form",
        cls=button_cls,
    )
