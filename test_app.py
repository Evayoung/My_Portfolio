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
    assert "Please fill in your name" in response.text


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
