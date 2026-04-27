"""FastHTML app entrypoint for NeoPortfolio — Olorundare Micheal Babawale."""

from __future__ import annotations

from pathlib import Path

from fasthtml.common import FastHTML, Link, Meta, Script, serve

from faststrap import add_bootstrap, mount_assets

try:
    from .config import settings
    from .routes import setup_routes
    from .theme import NEOPORTFOLIO_THEME, setup_theme_defaults
except ImportError:
    from config import settings
    from routes import setup_routes
    from theme import NEOPORTFOLIO_THEME, setup_theme_defaults

BASE_DIR = Path(__file__).parent

app = FastHTML(secret_key=settings.secret_key, session_cookie=settings.session_cookie)

add_bootstrap(
    app,
    theme=NEOPORTFOLIO_THEME,
    mode="dark",
    use_cdn=settings.use_cdn,
)
setup_theme_defaults()

if not settings.use_cdn:
    mount_assets(app, str(BASE_DIR / "assets"), url_path="/assets")

# ── Global head additions ──────────────────────────────────────────────────────
app.hdrs = app.hdrs + [
    # Preconnect for faster font loading
    Link(rel="preconnect", href="https://fonts.googleapis.com"),
    Link(rel="preconnect", href="https://fonts.gstatic.com", crossorigin="anonymous"),
    # Typography: Space Grotesk (headings) + Inter (body)
    Link(
        rel="stylesheet",
        href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@300;400;500;600&display=swap",
    ),
    # Theme colour (browser chrome on mobile)
    Meta(name="theme-color", content="#07111F"),
    # Author
    Meta(name="author", content="Olorundare Micheal Babawale"),
    # Custom stylesheet
    Link(rel="stylesheet", href="/assets/custom.css?v=20260426b"),
    # Custom JS (deferred)
    Script(src="/assets/custom.js?v=20260415", defer=True),
]

setup_routes(app, BASE_DIR / "assets")

if __name__ == "__main__":
    serve(port=settings.port)
