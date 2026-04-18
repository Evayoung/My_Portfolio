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
        "/portfolio-grid?filter=ai-ml",
        "/portfolio-controls?filter=frontend",
        "/service-detail?slug=ai-agent-design",
        "/project-preview?slug=ecommerce-platform",
        "/project-case-study?slug=ml-dashboard",
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
    response = client.get("/portfolio-grid?filter=devops")
    html = response.text
    assert "Cloud Infrastructure Automation" in html
    assert "AI-Powered E-Commerce Platform" not in html

    response = client.get("/portfolio-grid?filter=frontend")
    html = response.text
    assert "Real-Time Collaboration Tool" in html
    assert "Cloud Infrastructure Automation" not in html


def test_portfolio_controls_use_faststrap_toggle_group() -> None:
    response = client.get("/portfolio-controls?filter=frontend")
    html = response.text
    assert 'data-fs-toggle-group="true"' in html
    assert 'hx-get="/portfolio-grid?filter=frontend"' in html
    assert 'portfolio-toggle-btn active' in html
    assert 'id="portfolio-grid"' in html


def test_contact_requires_fields() -> None:
    response = client.post("/contact", data={"name": "", "email": "", "message": ""})
    assert response.status_code == 200
    assert "Please fill in your name" in response.text
