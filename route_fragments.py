"""Standalone route fragment builders and printable CV helpers."""

from __future__ import annotations

from html import escape
from typing import Any

from fasthtml.common import *

try:
    from .services.content_service import (
        list_certifications,
        list_competencies,
        list_core_skills,
        list_education,
        list_languages,
        list_tool_categories,
        list_work_history,
    )
except ImportError:
    from services.content_service import (
        list_certifications,
        list_competencies,
        list_core_skills,
        list_education,
        list_languages,
        list_tool_categories,
        list_work_history,
    )


def download_metrics_fragment(download_counts: dict[str, int]) -> Div:
    return Div(
        Div(Span("PDF", cls="analytics-key"), Span(str(download_counts["pdf"]), cls="analytics-value"), cls="analytics-row"),
        Div(Span("Web", cls="analytics-key"), Span(str(download_counts["web"]), cls="analytics-value"), cls="analytics-row"),
        Div(Span("Print", cls="analytics-key"), Span(str(download_counts["print"]), cls="analytics-value"), cls="analytics-row"),
        cls="analytics-list",
        id="download-metrics",
    )


def form_status_fragment(
    title: str,
    message: str,
    *,
    tone: str = "success",
    primary_action: Any | None = None,
    secondary_action: Any | None = None,
) -> Div:
    tone_cls = {
        "success": "alert alert-success",
        "warning": "alert alert-warning",
        "danger": "alert alert-danger",
        "info": "alert alert-info",
    }.get(tone, "alert alert-success")
    actions = [action for action in (primary_action, secondary_action) if action is not None]
    return Div(
        H4(title, cls="alert-heading h6 mb-2"),
        P(message, cls="mb-0"),
        Div(*actions, cls="d-flex flex-wrap gap-2 mt-3") if actions else "",
        cls=tone_cls,
    )


def _display_url(url: str) -> str:
    return url.replace("https://", "").replace("http://", "").rstrip("/")


def resume_html(cv_meta: dict[str, str], print_mode: bool = False) -> str:
    print_class = "print-mode" if print_mode else ""
    print_script = "<script>window.print()</script>" if print_mode else ""
    work_history = list_work_history()
    education = list_education()
    certifications = list_certifications()
    competencies = list_competencies()
    core_skills = list_core_skills()
    tool_categories = list_tool_categories()
    languages = list_languages()

    work_items_html = "".join(
        f"""
        <article class="experience-item">
          <div class="item-topline">
            <div>
              <h3 class="work-title">{escape(item.title)}</h3>
              <p class="work-org">{escape(item.organisation)} <span class="org-sep">&middot;</span> {escape(item.location)}</p>
            </div>
            <span class="period">{escape(item.period)}</span>
          </div>
          <ul class="work-bullets">
            {"".join(f"<li>{escape(bullet)}</li>" for bullet in item.bullets)}
          </ul>
        </article>
        """
        for item in work_history
    )
    education_html = "".join(
        f"""
        <div class="stack-item">
          <p class="stack-title">{escape(item.degree)}</p>
          <p class="stack-sub">{escape(item.institution)} <span class="org-sep">&middot;</span> {escape(item.period)}</p>
          <p class="edu-note">{escape(item.note)}</p>
        </div>
        """
        for item in education
    )
    certifications_html = "".join(
        f"""
        <div class="stack-item compact">
          <p class="stack-title">{escape(item.name)}</p>
          <p class="stack-sub">{escape(item.issuer)} <span class="org-sep">&middot;</span> {escape(item.year)}</p>
        </div>
        """
        for item in certifications
    )
    skills_grid_html = "".join(
        "".join(
            f"""
            <div class="tool-block">
              <div class="tool-label">{escape(category.label)}</div>
              <div class="tool-pills">
                {"".join(f'<span class="pill">{escape(tool)}</span>' for tool in category.tools)}
              </div>
            </div>
            """
            for category in tool_categories
        )
    )
    core_skills_html = "".join(f"<li>{escape(skill)}</li>" for skill in core_skills)
    competencies_html = "".join(f'<span class="competency-pill">{escape(item)}</span>' for item in competencies)
    languages_html = "".join(
        f"""
        <div class="lang-item">
          <div class="lang-top">
            <strong>{escape(name)}</strong>
            <span>{escape(level)}</span>
          </div>
          <div class="lang-track"><span style="width:{pct}%;"></span></div>
        </div>
        """
        for name, level, pct in languages
    )

    return f"""
    <!doctype html>
    <html lang="en" data-bs-theme="light">
      <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>{escape(cv_meta['name'])} - CV</title>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet" />
        <style>
          @page {{ size: A4; margin: 10mm; }}
          * {{ box-sizing:border-box; margin:0; padding:0; }}
          :root {{
            --navy:#07111F;
            --navy-soft:#112033;
            --cyan:#46c8ee;
            --cyan-soft:#dff7ff;
            --line:#d7e5ef;
            --ink:#111827;
            --muted:#5f6f83;
            --paper:#ffffff;
            --page:#edf3f8;
          }}
          body {{ font-family:'Inter', 'Segoe UI', sans-serif; background:var(--page); color:var(--ink); }}
          .sheet {{ width:100%; max-width:900px; margin:0 auto; padding:14px; }}
          .resume-shell {{
            background:var(--paper);
            border-radius:24px;
            overflow:hidden;
            box-shadow:0 24px 60px rgba(7,17,31,0.12);
            border:1px solid rgba(7,17,31,0.06);
          }}
          .resume-header {{
            padding:34px 34px 26px;
            background:linear-gradient(135deg, var(--navy), #0b1728 58%, #13233b);
            color:#f7fbff;
            position:relative;
          }}
          .resume-header::after {{
            content:"";
            position:absolute;
            inset:auto 34px 0 34px;
            height:1px;
            background:linear-gradient(90deg, rgba(70,200,238,0.55), rgba(70,200,238,0.08));
          }}
          .header-top {{
            display:flex;
            justify-content:space-between;
            gap:20px;
            align-items:flex-start;
          }}
          .identity h1 {{
            font-family:'Space Grotesk', 'Segoe UI', sans-serif;
            font-size:2.2rem;
            line-height:1.04;
            letter-spacing:-0.03em;
            margin-bottom:10px;
          }}
          .role-pill {{
            display:inline-flex;
            align-items:center;
            gap:8px;
            padding:7px 14px;
            border-radius:999px;
            background:rgba(70,200,238,0.12);
            border:1px solid rgba(70,200,238,0.28);
            color:var(--cyan);
            font-size:0.86rem;
            font-weight:700;
          }}
          .brand-mark {{
            display:flex;
            gap:6px;
            padding:8px;
            border-radius:16px;
            border:1px solid rgba(70,200,238,0.28);
            background:rgba(255,255,255,0.03);
          }}
          .brand-mark span {{
            width:38px;
            height:38px;
            display:grid;
            place-items:center;
            border-radius:11px;
            font-family:'Space Grotesk', 'Segoe UI', sans-serif;
            font-weight:700;
            font-size:1.05rem;
            color:var(--navy);
            background:var(--cyan);
          }}
          .summary-card {{
            margin-top:18px;
            padding:16px 18px;
            border-radius:18px;
            background:rgba(255,255,255,0.055);
            border:1px solid rgba(255,255,255,0.09);
            line-height:1.72;
            color:rgba(247,251,255,0.88);
            font-size:0.9rem;
          }}
          .contact-grid {{
            display:flex;
            flex-wrap:wrap;
            gap:10px;
            margin-top:18px;
          }}
          .contact-chip {{
            display:inline-flex;
            align-items:center;
            padding:7px 12px;
            border-radius:999px;
            border:1px solid rgba(255,255,255,0.12);
            background:rgba(255,255,255,0.05);
            font-size:0.78rem;
            color:rgba(247,251,255,0.88);
          }}
          .resume-body {{
            display:grid;
            grid-template-columns:1.38fr 0.92fr;
            gap:28px;
            padding:28px 30px 30px;
          }}
          .section-title {{
            font-family:'Space Grotesk', 'Segoe UI', sans-serif;
            font-size:0.98rem;
            font-weight:700;
            color:var(--navy);
            text-transform:uppercase;
            letter-spacing:0.08em;
            margin-bottom:14px;
            padding-bottom:7px;
            border-bottom:2px solid rgba(70,200,238,0.28);
          }}
          .main-column section + section,
          .side-column section + section {{ margin-top:22px; }}
          .experience-item {{
            padding:15px 16px 16px;
            border:1px solid var(--line);
            border-radius:16px;
            background:linear-gradient(180deg, #ffffff, #f9fcfe);
            margin-bottom:14px;
            break-inside:avoid;
          }}
          .item-topline {{
            display:flex;
            justify-content:space-between;
            gap:12px;
            align-items:flex-start;
            margin-bottom:8px;
          }}
          .work-title,
          .stack-title {{
            font-size:0.94rem;
            font-weight:700;
            color:var(--navy);
          }}
          .work-org,
          .stack-sub {{
            margin-top:3px;
            color:var(--muted);
            font-size:0.8rem;
            line-height:1.45;
          }}
          .org-sep {{ color:#94a7ba; }}
          .period {{
            flex-shrink:0;
            display:inline-flex;
            padding:6px 10px;
            border-radius:999px;
            background:var(--cyan-soft);
            border:1px solid rgba(70,200,238,0.35);
            color:#0c7895;
            font-size:0.73rem;
            font-weight:700;
          }}
          .work-bullets {{
            padding-left:16px;
            color:#2d3b4e;
            font-size:0.82rem;
            line-height:1.62;
          }}
          .work-bullets li + li {{ margin-top:5px; }}
          .panel {{
            border:1px solid var(--line);
            border-radius:16px;
            padding:15px 16px;
            background:#fbfdff;
          }}
          .stack-item + .stack-item {{
            margin-top:10px;
            padding-top:10px;
            border-top:1px solid rgba(17,24,39,0.08);
          }}
          .stack-item.compact + .stack-item.compact {{
            margin-top:8px;
            padding-top:8px;
          }}
          .edu-note {{
            margin-top:5px;
            color:var(--muted);
            line-height:1.58;
            font-size:0.79rem;
          }}
          .skills-list {{
            list-style:none;
            display:grid;
            gap:8px;
            padding:0;
          }}
          .skills-list li {{
            position:relative;
            padding-left:14px;
            font-size:0.81rem;
            line-height:1.48;
            color:#2d3b4e;
          }}
          .skills-list li::before {{
            content:"";
            position:absolute;
            left:0;
            top:0.54em;
            width:5px;
            height:5px;
            border-radius:999px;
            background:var(--cyan);
          }}
          .tool-block + .tool-block {{ margin-top:11px; }}
          .tool-label {{
            font-size:0.74rem;
            font-weight:700;
            color:#0c7895;
            text-transform:uppercase;
            letter-spacing:0.08em;
            margin-bottom:7px;
          }}
          .tool-pills,
          .competency-grid {{
            display:flex;
            flex-wrap:wrap;
            gap:6px;
          }}
          .pill,
          .competency-pill {{
            display:inline-flex;
            align-items:center;
            padding:4px 9px;
            border-radius:999px;
            font-size:0.72rem;
            font-weight:600;
            border:1px solid rgba(70,200,238,0.24);
            background:var(--cyan-soft);
            color:#0d6f8b;
          }}
          .lang-item + .lang-item {{ margin-top:10px; }}
          .lang-top {{
            display:flex;
            justify-content:space-between;
            gap:10px;
            font-size:0.8rem;
            color:#2d3b4e;
            margin-bottom:5px;
          }}
          .lang-track {{
            height:8px;
            border-radius:999px;
            background:#e6eef4;
            overflow:hidden;
          }}
          .lang-track span {{
            display:block;
            height:100%;
            border-radius:inherit;
            background:linear-gradient(90deg, var(--cyan), #2aaed7);
          }}
          .footer-note {{
            margin-top:18px;
            padding-top:14px;
            border-top:1px solid rgba(17,24,39,0.08);
            font-size:0.76rem;
            color:#6f8092;
          }}
          .print-mode .resume-shell {{ box-shadow:none; border-radius:0; border:0; }}
          @media print {{
            body {{ background: white; }}
            .sheet {{ max-width:none; padding:0; }}
            .resume-shell {{ box-shadow:none; border-radius:0; border:0; }}
          }}
          @media (max-width: 820px) {{
            .resume-body {{ grid-template-columns:1fr; }}
            .header-top {{ flex-direction:column; }}
            .brand-mark {{ align-self:flex-start; }}
          }}
        </style>
      </head>
      <body class="{print_class}">
        <div class="sheet">
          <div class="resume-shell">
            <header class="resume-header">
              <div class="header-top">
                <div class="identity">
                  <h1>{escape(cv_meta['name'])}</h1>
                  <p class="role-pill">{escape(cv_meta['role'])}</p>
                </div>
                <div class="brand-mark" aria-hidden="true">
                  <span>M</span>
                  <span>O</span>
                </div>
              </div>
              <p class="summary-card">{escape(cv_meta['summary'])}</p>
              <div class="contact-grid">
                <span class="contact-chip">{escape(cv_meta['location'])}</span>
                <span class="contact-chip">{escape(cv_meta['phone'])}</span>
                <span class="contact-chip">{escape(cv_meta['email'])}</span>
                <span class="contact-chip">{escape(_display_url(cv_meta['github']))}</span>
                <span class="contact-chip">{escape(_display_url(cv_meta['linkedin']))}</span>
              </div>
            </header>
            <div class="resume-body">
              <main class="main-column">
                <section>
                  <h2 class="section-title">Experience</h2>
                  {work_items_html}
                </section>
              </main>
              <aside class="side-column">
                <section class="panel">
                  <h2 class="section-title">Education</h2>
                  {education_html}
                </section>
                <section class="panel">
                  <h2 class="section-title">Certifications</h2>
                  {certifications_html}
                </section>
                <section class="panel">
                  <h2 class="section-title">Core Skills</h2>
                  <ul class="skills-list">{core_skills_html}</ul>
                </section>
                <section class="panel">
                  <h2 class="section-title">Tools & Technologies</h2>
                  {skills_grid_html}
                </section>
                <section class="panel">
                  <h2 class="section-title">Competencies</h2>
                  <div class="competency-grid">{competencies_html}</div>
                </section>
                <section class="panel">
                  <h2 class="section-title">Languages</h2>
                  {languages_html}
                </section>
              </aside>
            </div>
            <div class="resume-body" style="padding-top:0;">
              <div class="footer-note">
                Portfolio: {escape(_display_url('https://olorundaremicheal.vercel.app'))}
              </div>
            </div>
          </div>
        </div>
        {print_script}
      </body>
    </html>
    """


def service_detail_fragment(slug: str, service_map: dict[str, Any]) -> Any:
    service = service_map.get(slug)
    if not service:
        return Div("Service details unavailable.", cls="alert alert-warning")
    return Div(
        Span("Service Details", cls="modal-kicker"),
        H3(service.title, cls="modal-headline"),
        P(service.lead, cls="modal-lead"),
        P(service.summary, cls="modal-copy"),
        Div(*[Div(Span(">", cls="modal-bullet"), Span(item), cls="modal-list-item") for item in service.deliverables], cls="modal-list"),
        Div(
            Div(Span("Timeline", cls="modal-meta-label"), Strong(service.timeline)),
            Div(Span("Investment", cls="modal-meta-label"), Strong(service.price)),
            cls="modal-meta-grid",
        ),
        cls="modal-content-stack",
    )


def project_preview_fragment(slug: str, project_map: dict[str, Any]) -> Any:
    project = project_map.get(slug)
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
            A("View Case Study ->", href=f"/project/{project.slug}", cls="btn hero-secondary-btn btn-sm mt-3"),
            cls="mt-4",
        ),
        cls="modal-content-stack",
    )


def project_case_study_fragment(slug: str, project_map: dict[str, Any]) -> Any:
    project = project_map.get(slug)
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
