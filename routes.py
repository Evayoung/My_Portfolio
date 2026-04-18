"""Route registration for NeoPortfolio — updated with blog, cv, booking, and project pages."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from fasthtml.common import *
from starlette.responses import FileResponse, HTMLResponse, JSONResponse

try:
    from .components import page_shell, portfolio_controls, portfolio_grid, _page_nav_full
    from .content import PROJECTS, SERVICES, DEVELOPER_NAME, CV_META
    from .pages.blog import blog_index_page, blog_post_page
    from .pages.cv_page import cv_page
    from .pages.booking import booking_page
except ImportError:
    from components import page_shell, portfolio_controls, portfolio_grid, _page_nav_full
    from content import PROJECTS, SERVICES, DEVELOPER_NAME
    from cv_content import CV_META
    from pages.blog import blog_index_page, blog_post_page
    from pages.cv_page import cv_page
    from pages.booking import booking_page

DOWNLOAD_COUNTS = {"pdf": 0, "web": 0, "print": 0}

SERVICE_MAP = {item.slug: item for item in SERVICES}
PROJECT_MAP = {item.slug: item for item in PROJECTS}

VALID_FILTERS = {"all", "full-stack", "frontend", "ai-ml", "devops", "mobile",
                 "blockchain", "security", "desktop", "web"}


def _download_metrics_fragment() -> Div:
    return Div(
        Div(Span("PDF", cls="analytics-key"), Span(str(DOWNLOAD_COUNTS["pdf"]), cls="analytics-value"), cls="analytics-row"),
        Div(Span("Web", cls="analytics-key"), Span(str(DOWNLOAD_COUNTS["web"]), cls="analytics-value"), cls="analytics-row"),
        Div(Span("Print", cls="analytics-key"), Span(str(DOWNLOAD_COUNTS["print"]), cls="analytics-value"), cls="analytics-row"),
        cls="analytics-list",
        id="download-metrics",
    )


def _resume_html(print_mode: bool = False) -> str:
    """Return a polished print/web-ready CV HTML page."""
    print_class = "print-mode" if print_mode else ""
    print_script = "<script>window.print()</script>" if print_mode else ""
    meta = CV_META
    return f"""
    <!doctype html>
    <html lang="en" data-bs-theme="light">
      <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>{meta['name']} — CV</title>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet" />
        <style>
          *{{ box-sizing:border-box; margin:0; padding:0; }}
          body {{ font-family: 'Inter', Georgia, serif; background: #f5f7fb; color: #111827; }}
          .sheet {{ max-width: 860px; margin: 0 auto; padding: 40px 20px; }}
          .card {{ background: white; border-radius: 16px; padding: 36px 40px; box-shadow: 0 20px 50px rgba(15,23,42,0.08); }}
          h1 {{ font-family: 'Space Grotesk', sans-serif; font-size: 2.2rem; font-weight: 700; color: #07111F; margin-bottom: 4px; }}
          h2 {{ font-family: 'Space Grotesk', sans-serif; font-size: 1rem; font-weight: 700; color: #07111F; margin: 24px 0 10px; text-transform: uppercase; letter-spacing: 0.05em; border-bottom: 2px solid #19C6F7; padding-bottom: 6px; }}
          h3 {{ font-size: 0.95rem; font-weight: 600; color: #111827; margin-bottom: 2px; }}
          .role {{ color: #19C6F7; font-weight: 600; font-size: 1rem; margin-bottom: 8px; }}
          .meta {{ color: #6b7280; font-size: 0.82rem; margin-bottom: 20px; display: flex; gap: 20px; flex-wrap: wrap; }}
          .summary {{ font-size: 0.88rem; line-height: 1.7; color: #374151; background: #f0f9ff; border-left: 3px solid #19C6F7; padding: 12px 16px; border-radius: 6px; margin-bottom: 0; }}
          .grid {{ display: grid; gap: 14px; grid-template-columns: 1fr 1fr; margin-top: 8px; }}
          .work-item {{ margin-bottom: 20px; }}
          .work-title {{ font-weight: 600; font-size: 0.92rem; color: #111827; }}
          .work-org {{ font-size: 0.82rem; color: #6b7280; margin: 2px 0 8px; }}
          .work-bullets {{ font-size: 0.82rem; color: #374151; padding-left: 16px; line-height: 1.6; }}
          .work-bullets li {{ margin-bottom: 4px; }}
          .period {{ font-size: 0.75rem; background: rgba(25,198,247,0.1); color: #0891b2; padding: 2px 8px; border-radius: 999px; font-weight: 600; border: 1px solid rgba(25,198,247,0.25); }}
          .tool-block {{ margin-bottom: 10px; }}
          .tool-label {{ font-weight: 600; font-size: 0.82rem; color: #374151; margin-bottom: 4px; }}
          .tool-pills {{ display: flex; flex-wrap: wrap; gap: 5px; }}
          .pill {{ font-size: 0.73rem; background: #f0f9ff; color: #0891b2; border-radius: 5px; padding: 2px 8px; border: 1px solid rgba(25,198,247,0.2); }}
          .cert-item {{ font-size: 0.82rem; color: #374151; margin-bottom: 6px; }}
          .lang-item {{ display: flex; gap: 8px; font-size: 0.82rem; margin-bottom: 4px; }}
          .print-mode .card {{ box-shadow: none; border-radius: 0; }}
          @media print {{
            body {{ background: white; }}
            .sheet {{ padding: 0; }}
            .card {{ box-shadow: none; border-radius: 0; }}
            h2 {{ break-after: avoid; }}
            .work-item {{ break-inside: avoid; }}
          }}
        </style>
      </head>
      <body class="{print_class}">
        <div class="sheet">
          <div class="card">
            <h1>{meta['name']}</h1>
            <p class="role">{meta['role']}</p>
            <p class="meta">
              <span>📍 {meta['location']}</span>
              <span>📞 {meta['phone']}</span>
              <span>✉ {meta['email']}</span>
              <span>🐙 github.com/Evayoung</span>
              <span>💼 linkedin.com/in/michealolorundare</span>
            </p>
            <p class="summary">{meta['summary']}</p>

            <h2>Experience</h2>
            <div class="work-item">
              <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:6px;margin-bottom:4px;">
                <span class="work-title">Full-Stack &amp; AI Systems Architect</span>
                <span class="period">2023 – Present</span>
              </div>
              <p class="work-org">Independent / Freelance · Ilorin, Nigeria (Remote)</p>
              <ul class="work-bullets">
                <li>Designed and shipped 10+ production systems spanning web, mobile, desktop, and embedded platforms</li>
                <li>Built BackendForge — a multi-agent system where 18 AI agents autonomously scaffold FastAPI backends</li>
                <li>Developed Voice-First Learning Assistant with hybrid offline STT achieving 95%+ accuracy on Nigerian accents</li>
                <li>Architected biometric access control for UNILORIN CBT centres</li>
                <li>Delivered QRive SaaS — AI-powered business identity verification platform</li>
              </ul>
            </div>
            <div class="work-item">
              <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:6px;margin-bottom:4px;">
                <span class="work-title">Python &amp; Software Development Tutor</span>
                <span class="period">2023 – Present</span>
              </div>
              <p class="work-org">SuperProf &amp; Certmart · Remote</p>
              <ul class="work-bullets">
                <li>Teaching Python, FastAPI, software architecture, and AI literacy</li>
                <li>Designed tailored learning plans for practical coding and system design</li>
              </ul>
            </div>
            <div class="work-item">
              <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:6px;margin-bottom:4px;">
                <span class="work-title">Platform Architect — Church Data Infrastructure</span>
                <span class="period">2024 – Present</span>
              </div>
              <p class="work-org">Deeper Christian Life Ministry, Kwara State · Ilorin, Nigeria</p>
              <ul class="work-bullets">
                <li>Designed and maintain a scalable platform powering two mobile apps and a REST API across all Kwara branches</li>
                <li>Custom RBAC with state, zone, and branch-level scopes; real-time attendance analytics</li>
              </ul>
            </div>

            <h2>Education</h2>
            <p><strong>BSc. Statistics</strong> — University of Ilorin (2015 – 2019)</p>

            <h2>Skills</h2>
            <div class="grid">
              <div>
                <div class="tool-block"><div class="tool-label">Frameworks</div><div class="tool-pills"><span class="pill">FastAPI</span><span class="pill">FastHTML</span><span class="pill">Faststrap</span><span class="pill">Reflex</span><span class="pill">KivyMD</span></div></div>
                <div class="tool-block"><div class="tool-label">AI / ML</div><div class="tool-pills"><span class="pill">OpenAI API</span><span class="pill">Faster-Whisper</span><span class="pill">LangChain</span><span class="pill">RAG</span></div></div>
                <div class="tool-block"><div class="tool-label">Desktop</div><div class="tool-pills"><span class="pill">PySide6</span><span class="pill">PyQt6</span></div></div>
              </div>
              <div>
                <div class="tool-block"><div class="tool-label">Data / Infra</div><div class="tool-pills"><span class="pill">PostgreSQL</span><span class="pill">SQLite</span><span class="pill">Docker</span><span class="pill">Linux</span></div></div>
                <div class="tool-block"><div class="tool-label">Languages</div><div class="tool-pills"><span class="pill">Python</span><span class="pill">SQL</span><span class="pill">JavaScript</span><span class="pill">Bash</span></div></div>
                <div class="tool-block"><div class="tool-label">Other</div><div class="tool-pills"><span class="pill">HTMX</span><span class="pill">Paystack</span><span class="pill">Blockchain</span></div></div>
              </div>
            </div>

            <h2>Languages</h2>
            <div class="lang-item"><strong>English</strong> — Fluent</div>
            <div class="lang-item"><strong>Yoruba</strong> — Native</div>
          </div>
        </div>
        {print_script}
      </body>
    </html>
    """


def _service_detail_fragment(slug: str) -> Any:
    service = SERVICE_MAP.get(slug)
    if not service:
        return Div("Service details unavailable.", cls="alert alert-warning")
    return Div(
        Span("Service Details", cls="modal-kicker"),
        H3(service.title, cls="modal-headline"),
        P(service.lead, cls="modal-lead"),
        P(service.summary, cls="modal-copy"),
        Div(*[Div(Span("›", cls="modal-bullet"), Span(item), cls="modal-list-item") for item in service.deliverables], cls="modal-list"),
        Div(
            Div(Span("Timeline", cls="modal-meta-label"), Strong(service.timeline)),
            Div(Span("Investment", cls="modal-meta-label"), Strong(service.price)),
            cls="modal-meta-grid",
        ),
        cls="modal-content-stack",
    )


def _project_preview_fragment(slug: str) -> Any:
    project = PROJECT_MAP.get(slug)
    if not project:
        return Div("Preview unavailable.", cls="alert alert-warning")
    return Div(
        Div(
            Img(src=project.image, alt=project.title, cls="modal-preview-image"),
            Div(cls="modal-preview-overlay"),
            Div(Span("PROJECT SHOWCASE", cls="modal-preview-badge"), cls="modal-preview-top"),
            cls="modal-preview-shell",
        ),
        Div(
            H3(project.title, cls="modal-headline"),
            P(project.summary, cls="modal-copy"),
            Div(*[Span(item, cls="project-tech-pill") for item in project.tech], cls="project-tech-row"),
            A("View Case Study →", href=f"/project/{project.slug}", cls="btn hero-secondary-btn btn-sm mt-3"),
            cls="mt-4",
        ),
        cls="modal-content-stack",
    )


def _project_case_study_fragment(slug: str) -> Any:
    project = PROJECT_MAP.get(slug)
    if not project:
        return Div("Case study unavailable.", cls="alert alert-warning")
    return Div(
        Span(project.category.replace("-", " ").title(), cls="modal-kicker"),
        H3(project.title, cls="modal-headline"),
        P(project.narrative, cls="modal-copy"),
        Div(
            Div(
                Span("Complexity", cls="modal-meta-label"),
                Div(Div(cls="metric-bar-fill", style=f"width:{project.complexity}%;"), cls="metric-bar-track"),
                Span(f"{project.complexity}%", cls="metric-meta-value"),
                cls="metric-meta-card",
            ),
            Div(
                Span("Client Satisfaction", cls="modal-meta-label"),
                Div(Div(cls="metric-bar-fill", style=f"width:{project.satisfaction}%;"), cls="metric-bar-track"),
                Span(f"{project.satisfaction}%", cls="metric-meta-value"),
                cls="metric-meta-card",
            ),
            cls="case-study-metrics",
        ),
        Div(*[Span(item, cls="project-tech-pill") for item in project.tech], cls="project-tech-row mt-4"),
        cls="modal-content-stack",
    )


def setup_routes(app: Any, asset_dir: Path) -> None:
    """Register all application routes."""

    # ── Home ──────────────────────────────────────────────────────────────────

    @app.get("/")
    def home(filter: str = "all") -> Any:
        active = filter if filter in VALID_FILTERS else "all"
        return page_shell(active, DOWNLOAD_COUNTS)

    # ── Blog ──────────────────────────────────────────────────────────────────

    @app.get("/blog")
    def blog_index(cat: str = "all") -> Any:
        return blog_index_page(cat)

    @app.get("/blog/{slug}")
    def blog_post(slug: str) -> Any:
        return blog_post_page(slug)

    # ── CV ────────────────────────────────────────────────────────────────────

    @app.get("/cv")
    def cv() -> Any:
        return cv_page()

    @app.get("/cv/print")
    def cv_print() -> Any:
        return HTMLResponse(_resume_html(print_mode=True))

    # ── Booking ───────────────────────────────────────────────────────────────

    @app.get("/book")
    def book() -> Any:
        return booking_page()

    # ── Project standalone case study ─────────────────────────────────────────

    @app.get("/project/{slug}")
    def project_detail(slug: str) -> Any:
        from pages.blog import _page_nav, _page_footer
        project = PROJECT_MAP.get(slug)
        if not project:
            return (Title("Project Not Found"), _page_nav("/"), Main(
                Container(
                    H1("Project Not Found", cls="text-center mt-5"),
                    A("← Back to Portfolio", href="/#portfolio", cls="btn hero-secondary-btn mt-3 d-block mx-auto"),
                    cls="py-5",
                ),
                cls="neo-app",
            ))
        from faststrap import Card, Col, Row, Container, SEO
        from content import SITE_URL, DEVELOPER_NAME_SHORT
        return (
            *SEO(
                title=f"{project.title} | {DEVELOPER_NAME_SHORT}",
                description=project.summary,
                url=f"{SITE_URL}/project/{project.slug}",
                keywords=list(project.tech) + ["portfolio", "project"],
            ),
            _page_nav("/"),
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
                            A("← All Projects", href="/#portfolio", cls="btn hero-secondary-btn mt-4"),
                            cls="text-center book-header-content",
                        ),
                    ),
                    cls="book-header-section",
                ),
                Section(
                    Container(
                        Row(
                            Col(
                                Img(src=project.image, alt=project.title,
                                    cls="project-image w-100 rounded-4 mb-4",
                                    style="max-height:400px;object-fit:cover;"),
                                Div(
                                    Div(
                                        Span("Complexity", cls="modal-meta-label"),
                                        Div(Div(cls="metric-bar-fill", style=f"width:{project.complexity}%;"),
                                            cls="metric-bar-track"),
                                        Span(f"{project.complexity}%", cls="metric-meta-value"),
                                        cls="metric-meta-card mb-3",
                                    ),
                                    Div(
                                        Span("Client Satisfaction", cls="modal-meta-label"),
                                        Div(Div(cls="metric-bar-fill", style=f"width:{project.satisfaction}%;"),
                                            cls="metric-bar-track"),
                                        Span(f"{project.satisfaction}%", cls="metric-meta-value"),
                                        cls="metric-meta-card",
                                    ),
                                ),
                                cols=12, lg=6,
                            ),
                            Col(
                                H2("Project Narrative", cls="cv-section-title"),
                                P(project.narrative, cls="panel-copy mb-4"),
                                H3("Tech Stack", cls="subsection-title"),
                                Div(*[Span(t, cls="project-tech-pill") for t in project.tech], cls="project-tech-row mb-4"),
                                A(Icon("whatsapp", cls="me-2"), "Discuss This Project",
                                  href="https://wa.me/2349029952120?text=Hi+Micheal%2C+I+saw+your+project+and+would+love+to+discuss+something+similar.",
                                  target="_blank", rel="noreferrer",
                                  cls="btn hero-primary-btn"),
                                A("Book a Consultation →", href="/book", cls="btn hero-secondary-btn ms-2"),
                                cols=12, lg=6,
                                cls="mt-4 mt-lg-0",
                            ),
                            cls="g-4",
                        ),
                    ),
                    cls="content-section",
                ),
                _page_footer(),
                cls="neo-app",
            ),
        )

    # ── HTMX fragments ────────────────────────────────────────────────────────

    @app.get("/portfolio-grid")
    def portfolio_grid_fragment(filter: str = "all") -> Any:
        active = filter if filter in VALID_FILTERS else "all"
        return portfolio_grid(active)

    @app.get("/portfolio-controls")
    def portfolio_controls_fragment(filter: str = "all") -> Any:
        active = filter if filter in VALID_FILTERS else "all"
        return portfolio_controls(active)

    @app.get("/service-detail")
    def service_detail(slug: str = "") -> Any:
        return _service_detail_fragment(slug)

    @app.get("/project-preview")
    def project_preview(slug: str = "") -> Any:
        return _project_preview_fragment(slug)

    @app.get("/project-case-study")
    def project_case_study(slug: str = "") -> Any:
        return _project_case_study_fragment(slug)

    # ── Contact ───────────────────────────────────────────────────────────────

    @app.post("/contact")
    def contact(name: str = "", email: str = "", subject: str = "", message: str = "") -> Any:
        if not name.strip() or not email.strip() or not message.strip():
            return Div("Please fill in your name, email, and project brief.", cls="alert alert-warning")
        return Div(
            Strong("Message received."),
            P(
                f"Thanks {name.strip()}, I will get back to you at {email.strip()} soon"
                + (f" regarding {subject.strip()}." if subject.strip() else "."),
                cls="mb-0 mt-2",
            ),
            cls="alert alert-success",
        )

    # ── Resume download ───────────────────────────────────────────────────────

    @app.post("/api/download-track")
    def track_download(format: str = "pdf") -> Any:
        key = format if format in DOWNLOAD_COUNTS else "pdf"
        DOWNLOAD_COUNTS[key] += 1
        return _download_metrics_fragment()

    @app.get("/resume/download/{format}")
    def resume_download(format: str) -> Any:
        pdf_path = asset_dir / "neoportfolio_resume.pdf"
        if format == "pdf" and pdf_path.exists():
            return FileResponse(pdf_path, filename="Olorundare-Micheal-Babawale-CV.pdf", media_type="application/pdf")
        if format == "web":
            return HTMLResponse(_resume_html(print_mode=False))
        if format == "print":
            return HTMLResponse(_resume_html(print_mode=True))
        return JSONResponse({"error": "Unsupported format"}, status_code=404)

    # ── Demo preview ──────────────────────────────────────────────────────────

    @app.get("/demo/preview")
    def demo_preview(project: str = "atlas") -> Any:
        accent = {"atlas": "#4BD4FF", "lattice": "#FFB24D", "flux": "#7BFFA8", "canopy": "#9EA8FF"}.get(project, "#4BD4FF")
        return HTMLResponse(f"""<!doctype html><html lang="en"><head><meta charset="utf-8" />
        <style>body{{margin:0;min-height:100vh;display:grid;place-items:center;background:linear-gradient(160deg,#030712,#0a162b);color:#ecf6ff;font-family:sans-serif;}}
        .panel{{width:min(92vw,700px);border:1px solid rgba(255,255,255,0.12);border-radius:24px;padding:22px;background:rgba(2,8,20,0.82);}}</style>
        </head><body><div class="panel"><h3 style="color:{accent}">Live Demo · {project.title()}</h3><p style="color:#c8d6f0">This is a live demo preview panel.</p></div></body></html>""")

    # ── Health ────────────────────────────────────────────────────────────────

    @app.get("/health")
    def health() -> JSONResponse:
        return JSONResponse({"status": "healthy", "app": "neoportfolio"})
