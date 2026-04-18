"""Blog page components — index and post detail."""

from __future__ import annotations

from typing import Any

from fasthtml.common import (
    A, Article, Aside, Div, Footer, H1, H2, H3, H4, I, Li, Main,
    Nav, NotStr, P, Section, Small, Span, Strong, Time, Title, Ul,
)
from faststrap import Button, Card, Col, Container, Icon, Row, SEO

try:
    from ..blog_content import BLOG_CATEGORIES, BLOG_MAP, BLOG_POSTS, BlogPost
    from ..content import (
        DEVELOPER_NAME, DEVELOPER_NAME_SHORT, DEVELOPER_ROLE,
        EMAIL, GITHUB_URL, LINKEDIN_URL, SITE_URL, SOCIAL_LINKS,
    )
except ImportError:
    from blog_content import BLOG_CATEGORIES, BLOG_MAP, BLOG_POSTS, BlogPost
    from content import (
        DEVELOPER_NAME, DEVELOPER_NAME_SHORT, DEVELOPER_ROLE,
        EMAIL, GITHUB_URL, LINKEDIN_URL, SITE_URL, SOCIAL_LINKS,
    )


# ── Shared nav (pages have a simpler top bar) ─────────────────────────────────

def _page_nav(current: str = "") -> Nav:
    links = [
        ("Home",    "/"),
        ("Blog",    "/blog"),
        ("CV",      "/cv"),
        ("Book",    "/book"),
        ("Contact", "/#contact"),
    ]
    return Nav(
        Container(
            Div(
                A(DEVELOPER_NAME_SHORT, href="/", cls="brand-mark"),
                Div(
                    *[
                        A(label, href=href,
                          cls=f"nav-link-item{'  active' if href == current else ''}")
                        for label, href in links
                    ],
                    cls="site-nav-links",
                ),
                A("Book a Call", href="/book", cls="btn talk-button ms-3"),
                cls="site-nav-shell",
            ),
        ),
        id="site-nav",
        cls="site-nav",
    )


def _page_footer() -> Footer:
    return Footer(
        Container(
            Div(
                Span(f"© 2025 {DEVELOPER_NAME_SHORT}.", cls="footer-copy"),
                Div(
                    A("Home", href="/", cls="footer-link"),
                    A("Blog", href="/blog", cls="footer-link"),
                    A("CV",   href="/cv",   cls="footer-link"),
                    A("Book", href="/book", cls="footer-link"),
                    cls="footer-links",
                ),
                cls="d-flex flex-column flex-md-row justify-content-between align-items-center gap-3",
            ),
        ),
        cls="site-footer",
    )


# ── Blog card ─────────────────────────────────────────────────────────────────

def blog_card(post: BlogPost, featured: bool = False) -> Col:
    cat_colors = {
        "project":   "#19C6F7",
        "tutorial":  "#6BE89A",
        "opinion":   "#FFB24D",
        "deep-dive": "#9EA8FF",
    }
    color = cat_colors.get(post.category, "#19C6F7")

    return Col(
        A(
            Card(
                Div(
                    Span(
                        post.category.replace("-", " ").upper(),
                        cls="blog-category-chip",
                        style=f"background:rgba({','.join(str(int(color.lstrip('#')[i:i+2], 16)) for i in (0,2,4))},0.12);"
                              f"color:{color};border:1px solid {color}30;",
                    ),
                    Span(
                        Icon("clock", cls="me-1"),
                        f"{post.read_minutes} min read",
                        cls="blog-read-time",
                    ),
                    cls="blog-card-chips d-flex justify-content-between align-items-center mb-3",
                ),
                H3(post.title, cls="blog-card-title"),
                P(post.summary, cls="blog-card-excerpt"),
                Div(
                    Small(
                        Icon("calendar3", cls="me-1"),
                        post.published,
                        cls="blog-card-date",
                    ),
                    Span(
                        *[Span(tag, cls="blog-tag-pill") for tag in post.tags[:3]],
                        cls="d-flex gap-1 flex-wrap",
                    ),
                    cls="blog-card-footer d-flex justify-content-between align-items-center mt-3 flex-wrap gap-2",
                ),
                cls=f"blog-card h-100 reveal-block{'  blog-card-featured' if featured else ''}",
            ),
            href=f"/blog/{post.slug}",
            cls="blog-card-link",
        ),
        cols=12, md=6, lg=4,
    )


# ── Blog index page ───────────────────────────────────────────────────────────

def blog_index_page(active_category: str = "all") -> tuple[Any, ...]:
    filtered = (
        BLOG_POSTS if active_category == "all"
        else tuple(p for p in BLOG_POSTS if p.category == active_category)
    )

    cat_buttons = [
        A(
            label,
            href=f"/blog?cat={slug}",
            cls=f"btn blog-filter-btn{'  active' if slug == active_category else ''}",
        )
        for slug, label in BLOG_CATEGORIES
    ]

    featured = next((p for p in filtered if p.category == "project"), filtered[0]) if filtered else None

    cards = [blog_card(p, featured=(p is featured)) for p in filtered]

    return (
        *SEO(
            title=f"Blog | {DEVELOPER_NAME_SHORT}",
            description=(
                "Real articles about full-stack Python development, AI agent systems, "
                "offline-first architecture, and building software in Nigeria."
            ),
            keywords=["FastHTML", "FastAPI", "AI", "Python", "blog", "developer"],
            url=f"{SITE_URL}/blog",
            og_type="website",
            twitter_creator="@evayoung",
        ),
        _page_nav("/blog"),
        Main(
            Section(
                Container(
                    Div(
                        H1("From the Build Log", cls="blog-index-title"),
                        P(
                            "Real articles from building production systems — AI agents, "
                            "offline-first apps, Python full-stack, and security engineering.",
                            cls="blog-index-sub",
                        ),
                        cls="blog-index-header text-center mb-5",
                    ),
                    Div(*cat_buttons, cls="blog-filter-row d-flex gap-2 flex-wrap justify-content-center mb-5"),
                    (
                        Row(*cards, cls="g-4")
                        if filtered
                        else Div(
                            H3("No posts in this category yet.", cls="text-center"),
                            P("Try another filter.", cls="text-center text-muted"),
                            cls="py-5",
                        )
                    ),
                ),
                cls="content-section blog-section",
            ),
            _page_footer(),
            cls="neo-app",
        ),
    )


# ── Blog post detail ──────────────────────────────────────────────────────────

def blog_post_page(slug: str) -> tuple[Any, ...]:
    post = BLOG_MAP.get(slug)
    if not post:
        return (
            Title("Post Not Found"),
            _page_nav("/blog"),
            Main(
                Container(
                    Div(
                        H1("Post Not Found", cls="text-center mt-5"),
                        P("This article doesn't exist (yet).", cls="text-center text-muted"),
                        A("← Back to Blog", href="/blog", cls="btn hero-secondary-btn mt-3 d-block mx-auto"),
                        cls="py-5 text-center",
                        style="max-width:600px;margin:0 auto;",
                    ),
                ),
                cls="neo-app",
            ),
        )

    # Related posts (excluding current)
    related = [p for p in BLOG_POSTS if p.slug != slug][:3]

    cat_colors = {
        "project":   "#19C6F7",
        "tutorial":  "#6BE89A",
        "opinion":   "#FFB24D",
        "deep-dive": "#9EA8FF",
    }
    cat_color = cat_colors.get(post.category, "#19C6F7")

    return (
        *SEO(
            title=f"{post.title} | {DEVELOPER_NAME_SHORT}",
            description=post.summary,
            keywords=list(post.tags) + ["Olorundare Micheal", "blog"],
            url=f"{SITE_URL}/blog/{post.slug}",
            article=True,
            og_type="article",
            published_time=f"{post.published}T00:00:00Z",
            author=DEVELOPER_NAME,
            section=post.category.replace("-", " ").title(),
            tags=list(post.tags),
            twitter_creator="@evayoung",
        ),
        _page_nav("/blog"),
        Main(
            Article(
                # ── Hero strip ──────────────────────────────────────────
                Div(
                    Div(cls="hero-overlay"),
                    Container(
                        Div(
                            A("← All Articles", href="/blog", cls="btn hero-secondary-btn btn-sm mb-4"),
                            Span(
                                post.category.replace("-", " ").upper(),
                                cls="blog-category-chip mb-3 d-inline-block",
                                style=f"background:rgba({','.join(str(int(cat_color.lstrip('#')[i:i+2], 16)) for i in (0,2,4))},0.15);"
                                      f"color:{cat_color};border:1px solid {cat_color}40;",
                            ),
                            H1(post.title, cls="post-headline"),
                            Div(
                                Div(
                                    Span(
                                        Icon("person-circle", cls="me-1"),
                                        DEVELOPER_NAME_SHORT,
                                        cls="post-author",
                                    ),
                                    Span(
                                        Icon("calendar3", cls="me-1"),
                                        post.published,
                                        cls="post-meta-item",
                                    ),
                                    Span(
                                        Icon("clock", cls="me-1"),
                                        f"{post.read_minutes} min read",
                                        cls="post-meta-item",
                                    ),
                                    cls="post-meta-row d-flex gap-4 flex-wrap",
                                ),
                                cls="mt-3",
                            ),
                            Div(
                                *[Span(tag, cls="blog-tag-pill") for tag in post.tags],
                                cls="d-flex gap-2 flex-wrap mt-3",
                            ),
                            cls="post-hero-content",
                        ),
                    ),
                    cls="post-hero-strip",
                    style=f"background-image: url('{post.image}');",
                ),

                # ── Article body ────────────────────────────────────────
                Container(
                    Row(
                        Col(
                            Div(
                                NotStr(post.content_html),
                                cls="post-body",
                            ),
                            cols=12, lg=8,
                        ),
                        Col(
                            Div(
                                # Author card
                                Card(
                                    Div(
                                        Div(
                                            "OM",
                                            cls="post-author-avatar",
                                        ),
                                        Div(
                                            Strong(DEVELOPER_NAME_SHORT),
                                            P(DEVELOPER_ROLE, cls="small text-muted mb-0"),
                                        ),
                                        cls="d-flex gap-3 align-items-center",
                                    ),
                                    P(
                                        "Full-Stack & AI Systems Architect building in Python. "
                                        "Based in Ilorin, Nigeria.",
                                        cls="small mt-3 mb-0",
                                    ),
                                    A("View Full CV →", href="/cv", cls="small neo-link mt-2 d-inline-block"),
                                    cls="post-author-card mb-4",
                                ),
                                # Tags
                                Card(
                                    H4("Tags", cls="small fw-bold mb-3"),
                                    Div(
                                        *[Span(tag, cls="blog-tag-pill") for tag in post.tags],
                                        cls="d-flex gap-2 flex-wrap",
                                    ),
                                    cls="post-sidebar-card mb-4",
                                ),
                                # Book CTA
                                Card(
                                    H4("Work Together", cls="small fw-bold mb-2"),
                                    P("Have a project in mind? Let's talk.", cls="small text-muted"),
                                    A(
                                        Icon("whatsapp", cls="me-2"),
                                        "Chat on WhatsApp",
                                        href="https://wa.me/2349029952120?text=Hi+Micheal%2C+I+read+your+blog+and+would+like+to+discuss+a+project.",
                                        cls="btn hero-primary-btn btn-sm w-100",
                                        target="_blank",
                                        rel="noreferrer",
                                    ),
                                    A("Or book a consultation →", href="/book", cls="small neo-link mt-2 d-inline-block"),
                                    cls="post-sidebar-card",
                                ),
                                cls="post-sidebar sticky-top",
                                style="top:90px;",
                            ),
                            cols=12, lg=4,
                            cls="mt-4 mt-lg-0",
                        ),
                        cls="g-4 mt-0",
                    ),
                    cls="post-body-container",
                ),

                # ── Related posts ───────────────────────────────────────
                Section(
                    Container(
                        H2("More from the Build Log", cls="section-title mb-4"),
                        Row(
                            *[blog_card(p) for p in related],
                            cls="g-4",
                        ),
                    ),
                    cls="content-section",
                ),
            ),
            _page_footer(),
            cls="neo-app",
        ),
    )
