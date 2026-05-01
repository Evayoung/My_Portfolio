"""Public content-access layer for NeoPortfolio."""

from __future__ import annotations

import json
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

try:
    from ..blog_content import BLOG_CATEGORIES, BLOG_POSTS, BlogPost
    from ..config import settings
    from ..content import PORTFOLIO_FILTERS, PRICING_TIERS, PROJECTS, SERVICES, TESTIMONIALS, PricingTier, Project, Service, Testimonial
    from ..cv_content import (
        CERTIFICATIONS,
        COMPETENCIES,
        CORE_SKILLS,
        CV_META,
        EDUCATION,
        LANGUAGES,
        TOOLS_GRID,
        WORK_HISTORY,
        Certification,
        EducationItem,
        ToolCategory,
        WorkItem,
    )
except ImportError:
    from blog_content import BLOG_CATEGORIES, BLOG_POSTS, BlogPost
    from config import settings
    from content import PORTFOLIO_FILTERS, PRICING_TIERS, PROJECTS, SERVICES, TESTIMONIALS, PricingTier, Project, Service, Testimonial
    from cv_content import (
        CERTIFICATIONS,
        COMPETENCIES,
        CORE_SKILLS,
        CV_META,
        EDUCATION,
        LANGUAGES,
        TOOLS_GRID,
        WORK_HISTORY,
        Certification,
        EducationItem,
        ToolCategory,
        WorkItem,
    )


def _supabase_public_read_is_configured() -> bool:
    return bool(settings.supabase_url and settings.supabase_anon_key)


def _rest_request(path: str, *, params: dict[str, str] | None = None) -> object:
    query = f"?{urlencode(params)}" if params else ""
    url = f"{settings.supabase_url.rstrip('/')}/rest/v1/{path}{query}"
    request = Request(
        url,
        headers={
            "apikey": settings.supabase_anon_key,
            "Authorization": f"Bearer {settings.supabase_anon_key}",
            "Content-Type": "application/json",
        },
    )
    with urlopen(request, timeout=20) as response:
        raw = response.read()
        if not raw:
            return None
        return json.loads(raw.decode("utf-8"))


def _safe_load(loader, fallback):
    if not _supabase_public_read_is_configured():
        return fallback
    try:
        loaded = loader()
        return loaded if loaded else fallback
    except (HTTPError, URLError, TimeoutError, OSError, ValueError, KeyError, TypeError):
        return fallback


def get_portfolio_filters() -> tuple[tuple[str, str], ...]:
    return PORTFOLIO_FILTERS


def _project_from_row(row: dict[str, Any]) -> Project:
    tech_items = tuple(
        item["label"]
        for item in sorted(row.get("project_tech_stack") or [], key=lambda item: item.get("sort_order", 100))
        if item.get("label")
    )
    return Project(
        slug=row["slug"],
        title=row["title"],
        category=row["category"],
        summary=row["summary"],
        narrative=row["narrative"],
        tech=tech_items,
        image=row.get("image_url") or "/assets/images/hero-bg.jpg",
        complexity=int(row.get("complexity") or 0),
        satisfaction=int(row.get("satisfaction") or 0),
        featured=bool(row.get("featured")),
    )


def _load_projects() -> tuple[Project, ...]:
    rows = _rest_request(
        "projects",
        params={
            "select": "slug,title,category,summary,narrative,image_url,complexity,satisfaction,featured,sort_order,project_tech_stack(label,sort_order)",
            "published": "eq.true",
            "order": "sort_order.asc",
        },
    )
    if not isinstance(rows, list):
        return ()
    return tuple(_project_from_row(row) for row in rows)


def list_projects(category: str = "all") -> tuple[Project, ...]:
    projects = _safe_load(_load_projects, PROJECTS)
    if category == "all":
        return projects
    return tuple(project for project in projects if project.category == category)


def get_project(slug: str) -> Project | None:
    return next((project for project in list_projects() if project.slug == slug), None)


def _service_from_row(row: dict[str, Any]) -> Service:
    deliverables = tuple(
        item["label"]
        for item in sorted(row.get("service_deliverables") or [], key=lambda item: item.get("sort_order", 100))
        if item.get("label")
    )
    return Service(
        slug=row["slug"],
        title=row["title"],
        summary=row["summary"],
        lead=row["lead"],
        deliverables=deliverables,
        timeline=row.get("timeline") or "",
        price=row.get("price") or "",
        icon=row.get("icon") or "stars",
    )


def _load_services() -> tuple[Service, ...]:
    rows = _rest_request(
        "services",
        params={
            "select": "slug,title,summary,lead,timeline,price,icon,sort_order,service_deliverables(label,sort_order)",
            "visible": "eq.true",
            "order": "sort_order.asc",
        },
    )
    if not isinstance(rows, list):
        return ()
    return tuple(_service_from_row(row) for row in rows)


def list_services() -> tuple[Service, ...]:
    return _safe_load(_load_services, SERVICES)


def get_service(slug: str) -> Service | None:
    return next((service for service in list_services() if service.slug == slug), None)


def _pricing_tier_from_row(row: dict[str, Any]) -> PricingTier:
    points = tuple(
        item["label"]
        for item in sorted(row.get("pricing_points") or [], key=lambda item: item.get("sort_order", 100))
        if item.get("label")
    )
    return PricingTier(
        title=row["title"],
        price=row["price"],
        highlight=row["highlight"],
        points=points,
    )


def _load_pricing_tiers() -> tuple[PricingTier, ...]:
    rows = _rest_request(
        "pricing_tiers",
        params={
            "select": "title,price,highlight,sort_order,pricing_points(label,sort_order)",
            "visible": "eq.true",
            "order": "sort_order.asc",
        },
    )
    if not isinstance(rows, list):
        return ()
    return tuple(_pricing_tier_from_row(row) for row in rows)


def list_pricing_tiers() -> tuple[PricingTier, ...]:
    return _safe_load(_load_pricing_tiers, PRICING_TIERS)


def _testimonial_from_row(row: dict[str, Any]) -> Testimonial:
    return Testimonial(
        quote=row["quote"],
        author=row["author"],
        role=row.get("role") or "",
        company=row.get("company") or "",
    )


def _load_testimonials() -> tuple[Testimonial, ...]:
    rows = _rest_request(
        "testimonials",
        params={
            "select": "quote,author,role,company,sort_order",
            "visible": "eq.true",
            "order": "sort_order.asc",
        },
    )
    if not isinstance(rows, list):
        return ()
    return tuple(_testimonial_from_row(row) for row in rows)


def list_testimonials() -> tuple[Testimonial, ...]:
    return _safe_load(_load_testimonials, TESTIMONIALS)


def list_blog_categories() -> tuple[tuple[str, str], ...]:
    return BLOG_CATEGORIES


def _post_from_row(row: dict[str, Any]) -> BlogPost:
    tag_links = row.get("blog_post_tags") or []
    tags = tuple(
        link["blog_tags"]["label"]
        for link in tag_links
        if isinstance(link, dict) and isinstance(link.get("blog_tags"), dict) and link["blog_tags"].get("label")
    )
    published_at = row.get("published_at") or ""
    published = published_at[:10] if published_at else "Draft"
    return BlogPost(
        slug=row["slug"],
        title=row["title"],
        category=row["category"],
        summary=row["summary"],
        content_html=row["content_html"],
        published=published,
        read_minutes=int(row.get("read_minutes") or 0),
        tags=tags,
        image=row.get("image_url") or "/assets/images/hero-bg.jpg",
    )


def _load_blog_posts() -> tuple[BlogPost, ...]:
    rows = _rest_request(
        "blog_posts",
        params={
            "select": "slug,title,category,summary,content_html,image_url,read_minutes,published_at,blog_post_tags(blog_tags(label))",
            "published": "eq.true",
            "order": "published_at.desc",
        },
    )
    if not isinstance(rows, list):
        return ()
    return tuple(_post_from_row(row) for row in rows)


def list_blog_posts(category: str = "all") -> tuple[BlogPost, ...]:
    posts = _safe_load(_load_blog_posts, BLOG_POSTS)
    if category == "all":
        return posts
    return tuple(post for post in posts if post.category == category)


def get_blog_post(slug: str) -> BlogPost | None:
    return next((post for post in list_blog_posts() if post.slug == slug), None)


def list_latest_posts(limit: int = 3) -> tuple[BlogPost, ...]:
    return list_blog_posts()[:limit]


def _load_cv_meta() -> dict[str, str]:
    rows = _rest_request(
        "cv_meta",
        params={
            "select": "full_name,role,email,phone,whatsapp,location,github_url,linkedin_url,summary",
            "limit": "1",
        },
    )
    if not isinstance(rows, list) or not rows:
        return {}
    row = rows[0]
    return {
        "name": row.get("full_name") or "",
        "role": row.get("role") or "",
        "email": row.get("email") or "",
        "phone": row.get("phone") or "",
        "whatsapp": row.get("whatsapp") or "",
        "location": row.get("location") or "",
        "github": row.get("github_url") or "",
        "linkedin": row.get("linkedin_url") or "",
        "summary": row.get("summary") or "",
    }


def get_cv_meta() -> dict[str, str]:
    return _safe_load(_load_cv_meta, CV_META)


def _load_work_history() -> tuple[WorkItem, ...]:
    rows = _rest_request(
        "cv_work_history",
        params={
            "select": "title,organisation,period,location,bullets,sort_order",
            "order": "sort_order.asc",
        },
    )
    if not isinstance(rows, list):
        return ()
    return tuple(
        WorkItem(
            title=row["title"],
            organisation=row["organisation"],
            period=row["period"],
            location=row.get("location") or "",
            bullets=tuple(row.get("bullets") or []),
        )
        for row in rows
    )


def list_work_history() -> tuple[WorkItem, ...]:
    return _safe_load(_load_work_history, WORK_HISTORY)


def _load_education() -> tuple[EducationItem, ...]:
    rows = _rest_request(
        "cv_education",
        params={
            "select": "degree,institution,period,note,sort_order",
            "order": "sort_order.asc",
        },
    )
    if not isinstance(rows, list):
        return ()
    return tuple(
        EducationItem(
            degree=row["degree"],
            institution=row["institution"],
            period=row["period"],
            note=row.get("note") or "",
        )
        for row in rows
    )


def list_education() -> tuple[EducationItem, ...]:
    return _safe_load(_load_education, EDUCATION)


def _load_certifications() -> tuple[Certification, ...]:
    rows = _rest_request(
        "cv_certifications",
        params={
            "select": "name,issuer,year,credential_url,sort_order",
            "order": "sort_order.asc",
        },
    )
    if not isinstance(rows, list):
        return ()
    return tuple(
        Certification(
            name=row["name"],
            issuer=row["issuer"],
            year=row["year"],
            credential_url=row.get("credential_url") or "",
        )
        for row in rows
    )


def list_certifications() -> tuple[Certification, ...]:
    return _safe_load(_load_certifications, CERTIFICATIONS)


def _load_tool_categories() -> tuple[ToolCategory, ...]:
    rows = _rest_request(
        "cv_tool_categories",
        params={
            "select": "label,tools,sort_order",
            "order": "sort_order.asc",
        },
    )
    if not isinstance(rows, list):
        return ()
    return tuple(
        ToolCategory(
            label=row["label"],
            tools=tuple(row.get("tools") or []),
        )
        for row in rows
    )


def list_tool_categories() -> tuple[ToolCategory, ...]:
    return _safe_load(_load_tool_categories, TOOLS_GRID)


def _load_languages() -> tuple[tuple[str, str, int], ...]:
    rows = _rest_request(
        "cv_languages",
        params={
            "select": "label,proficiency_label,proficiency_score,sort_order",
            "order": "sort_order.asc",
        },
    )
    if not isinstance(rows, list):
        return ()
    return tuple(
        (
            row["label"],
            row["proficiency_label"],
            int(row.get("proficiency_score") or 0),
        )
        for row in rows
    )


def list_languages() -> tuple[tuple[str, str, int], ...]:
    return _safe_load(_load_languages, LANGUAGES)


def _load_core_skills() -> tuple[str, ...]:
    rows = _rest_request(
        "cv_core_skills",
        params={
            "select": "label,sort_order",
            "order": "sort_order.asc",
        },
    )
    if not isinstance(rows, list):
        return ()
    return tuple(row["label"] for row in rows if row.get("label"))


def list_core_skills() -> tuple[str, ...]:
    return _safe_load(_load_core_skills, CORE_SKILLS)


def _load_competencies() -> tuple[str, ...]:
    rows = _rest_request(
        "cv_competencies",
        params={
            "select": "label,sort_order",
            "order": "sort_order.asc",
        },
    )
    if not isinstance(rows, list):
        return ()
    return tuple(row["label"] for row in rows if row.get("label"))


def list_competencies() -> tuple[str, ...]:
    return _safe_load(_load_competencies, COMPETENCIES)
