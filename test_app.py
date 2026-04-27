"""Smoke tests for NeoPortfolio."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import sys

from starlette.testclient import TestClient

APP_PATH = Path(__file__).with_name("app.py")
ROOT = APP_PATH.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
SPEC = importlib.util.spec_from_file_location("neoportfolio_app", APP_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)
app = MODULE.app

client = TestClient(app)


def test_core_routes_render() -> None:
    for route in [
        "/",
        "/blog",
        "/cv",
        "/book",
        "/robots.txt",
        "/sitemap.xml",
        "/portfolio-grid?filter=ai-ml",
        "/portfolio-controls?filter=security",
        "/service-detail?slug=ai-agent-design",
        "/project-preview?slug=backendforge",
        "/project-case-study?slug=backendforge",
        "/health",
    ]:
        response = client.get(route)
        assert response.status_code == 200


def test_home_contains_key_sections() -> None:
    response = client.get("/")
    html = response.text
    assert "Olorundare Micheal" in html
    assert "Full-Stack Developer" in html
    assert "About Me" in html
    assert "My Portfolio" in html
    assert "Testimonials" in html
    assert "CV Zone" in html
    assert "Let's Talk" in html


def test_filter_fragment_changes_projects() -> None:
    response = client.get("/portfolio-grid?filter=security")
    html = response.text
    assert "TrueTag" in html
    assert "BackendForge" not in html

    response = client.get("/portfolio-grid?filter=web")
    html = response.text
    assert "NeoPortfolio" in html
    assert "TrueTag" not in html


def test_portfolio_controls_use_faststrap_toggle_group() -> None:
    response = client.get("/portfolio-controls?filter=security")
    html = response.text
    assert 'data-fs-toggle-group="true"' in html
    assert 'hx-get="/portfolio-grid?filter=security"' in html
    assert 'portfolio-toggle-btn active' in html
    assert 'id="portfolio-grid"' in html


def test_unknown_filter_falls_back_to_all() -> None:
    response = client.get("/portfolio-controls?filter=frontend")
    html = response.text
    assert 'hx-get="/portfolio-grid?filter=all"' in html
    assert "BackendForge" in html


def test_contact_requires_fields() -> None:
    response = client.post("/contact", data={"name": "", "email": "", "message": ""})
    assert response.status_code == 200
    assert "A few details are missing" in response.text
    assert "project brief" in response.text


def test_contact_submission_offers_stateless_fallback_actions() -> None:
    response = client.post(
        "/contact",
        data={
            "name": "Jane Doe",
            "email": "jane@example.com",
            "subject": "Project Inquiry",
            "message": "I need a backend system for a new product.",
        },
    )
    html = response.text
    assert response.status_code == 200
    assert (
        "Message received" in html
        or "Ready to send" in html
        or "Delivery needs a fallback" in html
    )
    if "Message received" not in html:
        assert "Continue on WhatsApp" in html
        assert "Send by Email" in html


def test_inner_pages_include_shared_nav_and_key_content() -> None:
    pages = {
        "/blog": "From the Build Log",
        "/cv": "Curriculum Vitae",
        "/book": "Let's Talk About Your Project",
    }

    for route, marker in pages.items():
        response = client.get(route)
        html = response.text
        assert response.status_code == 200
        assert 'id="site-nav"' in html
        assert marker in html


def test_shared_nav_uses_compact_mo_logo_without_nested_brand_links() -> None:
    for route in ("/", "/blog", "/cv", "/book"):
        response = client.get(route)
        html = response.text
        assert response.status_code == 200
        assert 'class="mo-logo"' in html
        assert '<span class="brand-mark">' not in html
        assert '<a href="#hero" class="navbar-brand"><a ' not in html


def test_home_social_icons_render_as_real_links() -> None:
    response = client.get("/")
    html = response.text
    assert response.status_code == 200
    assert 'class="social-icon-link"' in html
    assert 'href="https://github.com/Evayoung"' in html
    assert 'href="https://linkedin.com/in/michealolorundare"' in html
    assert 'href="mailto:meshelleva@gmail.com"' in html


def test_cv_uses_neutral_custom_pills_instead_of_primary_badges() -> None:
    response = client.get("/cv")
    html = response.text
    assert response.status_code == 200
    assert 'class="cv-contact-chip"' in html
    assert 'class="cv-tool-badge"' in html
    assert 'class="cv-competency-pill"' in html
    assert 'text-bg-primary rounded-pill cv-contact-chip' not in html
    assert 'text-bg-primary rounded-pill cv-tool-badge' not in html
    assert 'text-bg-primary rounded-pill cv-competency-pill' not in html


def test_missing_content_pages_render_faststrap_empty_states() -> None:
    pages = {
        "/blog/does-not-exist": "Post not found",
        "/project/does-not-exist": "Project not found",
    }

    for route, marker in pages.items():
        response = client.get(route)
        html = response.text
        assert response.status_code == 200
        assert marker in html
        assert f'<h4 class="mb-2">{marker}</h4>' in html
        assert 'text-muted mb-4' in html


def test_forms_use_consistent_floating_label_markup() -> None:
    for route, field_id in (("/", "contact-message"), ("/book", "brief-description")):
        response = client.get(route)
        html = response.text
        assert response.status_code == 200
        assert 'class="form-floating' in html
        assert f'for="{field_id}"' in html
        assert 'contact-textarea mt-3' not in html


def test_inner_page_layouts_keep_responsive_column_classes() -> None:
    pages = {
        "/cv": ['col-lg-8', 'col-lg-4'],
        "/book": ['col-lg-7', 'col-lg-5', 'col-md-6', 'col-md-4'],
        "/blog": ['col-lg-4', 'col-md-6'],
    }

    for route, classes in pages.items():
        response = client.get(route)
        html = response.text
        assert response.status_code == 200
        for cls in classes:
            assert cls in html


def test_project_detail_uses_mobile_safe_detail_layout() -> None:
    response = client.get("/project/backendforge")
    html = response.text
    assert response.status_code == 200
    assert "project-detail-section" in html
    assert "project-detail-metrics case-study-metrics" in html
    assert "project-detail-copy" in html
    assert "project-detail-actions" in html


def test_print_cv_uses_structured_cv_content() -> None:
    response = client.get("/cv/print")
    html = response.text
    assert response.status_code == 200
    assert "Prompt Engineering for Developers" in html
    assert "Backend Lead" in html
    assert "Redis" in html


def test_booking_submission_offers_stateless_fallback_actions() -> None:
    response = client.post(
        "/book/submit",
        data={
            "name": "Jane Doe",
            "email": "jane@example.com",
            "whatsapp": "+2348000000000",
            "service": "backend-api",
            "budget": "250k-500k",
            "timeline": "1-4-weeks",
            "message": "I want to discuss a backend rebuild.",
        },
    )
    html = response.text
    assert response.status_code == 200
    assert (
        "Brief received" in html
        or "Brief prepared" in html
    )
    if "Brief received" not in html:
        assert "Send Brief on WhatsApp" in html
        assert "Send Brief by Email" in html


def test_seo_routes_publish_current_site_urls() -> None:
    robots = client.get("/robots.txt")
    sitemap = client.get("/sitemap.xml")

    assert robots.status_code == 200
    assert "https://olorundaremicheal.vercel.app/sitemap.xml" in robots.text

    assert sitemap.status_code == 200
    assert "<urlset" in sitemap.text
    assert "https://olorundaremicheal.vercel.app/blog" in sitemap.text
    assert "https://olorundaremicheal.vercel.app/project/backendforge" in sitemap.text


def test_pdf_download_route_serves_real_pdf_asset() -> None:
    response = client.get("/resume/download/pdf")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/pdf")
    assert response.content.startswith(b"%PDF")
    assert len(response.content) > 5000


def test_public_env_template_exists() -> None:
    root = Path(__file__).parent
    assert (root / ".env.example").exists()
