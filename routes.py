"""Route registration for NeoPortfolio."""

from __future__ import annotations

from pathlib import Path
from typing import Any
from urllib.parse import quote_plus

from fasthtml.common import *
from starlette.responses import FileResponse, HTMLResponse, JSONResponse

try:
    from .ui.home import page_shell
    from .ui.portfolio import portfolio_controls, portfolio_grid
    from .content import EMAIL, SITE_URL, WHATSAPP
    from .pages.blog import blog_index_page, blog_post_page
    from .pages.booking import booking_page
    from .pages.cv_page import cv_page
    from .pages.project_detail import project_detail_page
    from .route_fragments import (
        download_metrics_fragment,
        form_status_fragment,
        project_case_study_fragment,
        project_preview_fragment,
        resume_html,
        service_detail_fragment,
    )
    from .services.content_service import get_cv_meta, get_portfolio_filters, get_project, list_blog_posts, list_projects, list_services
    from .services.submission_service import submit_booking_request, submit_contact_inquiry
except ImportError:
    from ui.home import page_shell
    from ui.portfolio import portfolio_controls, portfolio_grid
    from content import EMAIL, SITE_URL, WHATSAPP
    from pages.blog import blog_index_page, blog_post_page
    from pages.booking import booking_page
    from pages.cv_page import cv_page
    from pages.project_detail import project_detail_page
    from route_fragments import (
        download_metrics_fragment,
        form_status_fragment,
        project_case_study_fragment,
        project_preview_fragment,
        resume_html,
        service_detail_fragment,
    )
    from services.content_service import get_cv_meta, get_portfolio_filters, get_project, list_blog_posts, list_projects, list_services
    from services.submission_service import submit_booking_request, submit_contact_inquiry

DOWNLOAD_COUNTS = {"pdf": 0, "web": 0, "print": 0}


def _service_map() -> dict[str, Any]:
    return {item.slug: item for item in list_services()}


def _project_map() -> dict[str, Any]:
    return {item.slug: item for item in list_projects()}


def _valid_filters() -> set[str]:
    return {slug for slug, _ in get_portfolio_filters()}


def _wa_link(message: str) -> str:
    return f"https://wa.me/{WHATSAPP.replace('+', '')}?text={quote_plus(message)}"


def _mailto_link(subject: str, body: str) -> str:
    return f"mailto:{EMAIL}?subject={quote_plus(subject)}&body={quote_plus(body)}"


def _contact_fallback_actions(name: str, email: str, subject: str, message: str) -> tuple[Any, Any]:
    subject_text = subject.strip() or "Portfolio inquiry"
    body = (
        f"Name: {name.strip()}\n"
        f"Email: {email.strip()}\n"
        f"Subject: {subject_text}\n\n"
        f"{message.strip()}"
    )
    whatsapp = A(
        "Continue on WhatsApp",
        href=_wa_link(body),
        target="_blank",
        rel="noreferrer",
        cls="btn hero-primary-btn btn-sm",
    )
    email_action = A(
        "Send by Email",
        href=_mailto_link(subject_text, body),
        cls="btn hero-secondary-btn btn-sm",
    )
    return whatsapp, email_action


def _booking_fallback_actions(
    name: str,
    email: str,
    whatsapp_number: str,
    service: str,
    budget: str,
    timeline: str,
    message: str,
) -> tuple[Any, Any]:
    subject_text = f"Consultation request from {name.strip()}"
    body = (
        f"Name: {name.strip()}\n"
        f"Email: {email.strip()}\n"
        f"WhatsApp: {whatsapp_number.strip() or 'Not provided'}\n"
        f"Service: {service.strip() or 'Not selected'}\n"
        f"Budget: {budget.strip() or 'Not selected'}\n"
        f"Timeline: {timeline.strip() or 'Not selected'}\n\n"
        f"Project brief:\n{message.strip()}"
    )
    whatsapp = A(
        "Send Brief on WhatsApp",
        href=_wa_link(body),
        target="_blank",
        rel="noreferrer",
        cls="btn hero-primary-btn btn-sm",
    )
    email_action = A(
        "Send Brief by Email",
        href=_mailto_link(subject_text, body),
        cls="btn hero-secondary-btn btn-sm",
    )
    return whatsapp, email_action


def setup_routes(app: Any, asset_dir: Path) -> None:
    """Register all application routes."""

    @app.get("/")
    def home(filter: str = "all") -> Any:
        active = filter if filter in _valid_filters() else "all"
        return page_shell(active, DOWNLOAD_COUNTS)

    @app.get("/blog")
    def blog_index(cat: str = "all") -> Any:
        return blog_index_page(cat)

    @app.get("/blog/{slug}")
    def blog_post(slug: str) -> Any:
        return blog_post_page(slug)

    @app.get("/cv")
    def cv() -> Any:
        return cv_page()

    @app.get("/cv/print")
    def cv_print() -> Any:
        return HTMLResponse(resume_html(get_cv_meta(), print_mode=True))

    @app.get("/book")
    def book() -> Any:
        return booking_page()

    @app.get("/project/{slug}")
    def project_detail(slug: str) -> Any:
        return project_detail_page(get_project(slug))

    @app.get("/portfolio-grid")
    def portfolio_grid_fragment(filter: str = "all") -> Any:
        active = filter if filter in _valid_filters() else "all"
        return portfolio_grid(active)

    @app.get("/portfolio-controls")
    def portfolio_controls_fragment(filter: str = "all") -> Any:
        active = filter if filter in _valid_filters() else "all"
        return portfolio_controls(active)

    @app.get("/service-detail")
    def service_detail(slug: str = "") -> Any:
        return service_detail_fragment(slug, _service_map())

    @app.get("/project-preview")
    def project_preview(slug: str = "") -> Any:
        return project_preview_fragment(slug, _project_map())

    @app.get("/project-case-study")
    def project_case_study(slug: str = "") -> Any:
        return project_case_study_fragment(slug, _project_map())

    @app.post("/contact")
    def contact(
        name: str = "",
        email: str = "",
        subject: str = "",
        message: str = "",
        company: str = "",
    ) -> Any:
        if company.strip():
            return form_status_fragment(
                "Thanks.",
                "Your message looks valid. I will reply through the details you shared if needed.",
            )
        if not name.strip() or not email.strip() or not message.strip():
            return form_status_fragment(
                "A few details are missing",
                "Please fill in your name, email, and project brief before sending.",
                tone="warning",
            )
        result = submit_contact_inquiry(name=name, email=email, subject=subject, message=message)
        if result.stored:
            return form_status_fragment(result.title, result.message, tone=result.tone)
        whatsapp_action, email_action = _contact_fallback_actions(name, email, subject, message)
        return form_status_fragment(
            result.title,
            result.message,
            tone=result.tone,
            primary_action=whatsapp_action,
            secondary_action=email_action,
        )

    @app.post("/book/submit")
    def booking_submit(
        name: str = "",
        email: str = "",
        whatsapp: str = "",
        service: str = "",
        budget: str = "",
        timeline: str = "",
        message: str = "",
        company: str = "",
    ) -> Any:
        if company.strip():
            return form_status_fragment(
                "Thanks.",
                "Your consultation request looks valid. I will reply through the details you shared if needed.",
            )
        if not name.strip() or not email.strip() or not message.strip():
            return form_status_fragment(
                "Project brief incomplete",
                "Please share your name, email, and project description before continuing.",
                tone="warning",
            )
        result = submit_booking_request(
            name=name,
            email=email,
            whatsapp=whatsapp,
            service=service,
            budget=budget,
            timeline=timeline,
            message=message,
        )
        if result.stored:
            return form_status_fragment(result.title, result.message, tone=result.tone)
        whatsapp_action, email_action = _booking_fallback_actions(
            name,
            email,
            whatsapp,
            service,
            budget,
            timeline,
            message,
        )
        return form_status_fragment(
            result.title,
            result.message,
            tone=result.tone,
            primary_action=whatsapp_action,
            secondary_action=email_action,
        )

    @app.post("/api/download-track")
    def track_download(format: str = "pdf") -> Any:
        key = format if format in DOWNLOAD_COUNTS else "pdf"
        DOWNLOAD_COUNTS[key] += 1
        return download_metrics_fragment(DOWNLOAD_COUNTS)

    @app.get("/resume/download/{format}")
    def resume_download(format: str) -> Any:
        if format == "pdf":
            import os as _os
            from pathlib import Path as _Path
            tmp_dir = _Path("/tmp") if _os.getenv("VERCEL") else (asset_dir / "generated")
            tmp_dir.mkdir(parents=True, exist_ok=True)
            pdf_path = tmp_dir / "neoportfolio_resume.pdf"
            try:
                try:
                    from .generate_resume_pdf import build_pdf
                except ImportError:
                    from generate_resume_pdf import build_pdf
                build_pdf(pdf_path)
            except Exception:  # noqa: BLE001 — fallback to pre-built if generation fails
                pdf_path = asset_dir / "neoportfolio_resume.pdf"
            if pdf_path.exists():
                return FileResponse(
                    pdf_path,
                    filename="Olorundare-Micheal-Babawale-CV.pdf",
                    media_type="application/pdf",
                )
            return JSONResponse({"error": "PDF could not be generated"}, status_code=500)
        if format == "web":
            return HTMLResponse(resume_html(get_cv_meta(), print_mode=False))
        if format == "print":
            return HTMLResponse(resume_html(get_cv_meta(), print_mode=True))
        return JSONResponse({"error": "Unsupported format"}, status_code=404)

    @app.get("/demo/preview")
    def demo_preview(project: str = "atlas") -> Any:
        accent = {"atlas": "#4BD4FF", "lattice": "#FFB24D", "flux": "#7BFFA8", "canopy": "#9EA8FF"}.get(project, "#4BD4FF")
        return HTMLResponse(
            f"""<!doctype html><html lang="en"><head><meta charset="utf-8" />
        <style>body{{margin:0;min-height:100vh;display:grid;place-items:center;background:linear-gradient(160deg,#030712,#0a162b);color:#ecf6ff;font-family:sans-serif;}}
        .panel{{width:min(92vw,700px);border:1px solid rgba(255,255,255,0.12);border-radius:24px;padding:22px;background:rgba(2,8,20,0.82);}}</style>
        </head><body><div class="panel"><h3 style="color:{accent}">Live Demo · {project.title()}</h3><p style="color:#c8d6f0">This is a live demo preview panel.</p></div></body></html>"""
        )

    @app.get("/health")
    def health() -> JSONResponse:
        return JSONResponse({"status": "healthy", "app": "neoportfolio"})

    @app.get("/robots.txt")
    def robots() -> HTMLResponse:
        return HTMLResponse(
            f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n",
            media_type="text/plain",
        )

    @app.get("/sitemap.xml")
    def sitemap() -> HTMLResponse:
        static_paths = ["/", "/blog", "/cv", "/book"]
        blog_paths = [f"/blog/{post.slug}" for post in list_blog_posts()]
        project_paths = [f"/project/{project.slug}" for project in list_projects()]
        urls = static_paths + blog_paths + project_paths
        items = "".join(
            f"<url><loc>{SITE_URL}{path}</loc></url>"
            for path in urls
        )
        xml = (
            '<?xml version="1.0" encoding="UTF-8"?>'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
            f"{items}"
            "</urlset>"
        )
        return HTMLResponse(xml, media_type="application/xml")
