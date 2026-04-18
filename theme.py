"""Theme tokens and Faststrap defaults for NeoPortfolio."""

from __future__ import annotations

from faststrap import create_theme, set_component_defaults

BRAND = {
    "primary": "#19C6F7",
    "secondary": "#FFB24D",
    "success": "#6BE89A",
    "info": "#6E8BFF",
    "warning": "#F6C15B",
    "danger": "#FF6B7B",
    "light": "#ECF6FF",
    "dark": "#07111F",
}

NEOPORTFOLIO_THEME = create_theme(
    primary=BRAND["primary"],
    secondary=BRAND["secondary"],
    success=BRAND["success"],
    info=BRAND["info"],
    warning=BRAND["warning"],
    danger=BRAND["danger"],
    light=BRAND["light"],
    dark=BRAND["dark"],
)


def setup_theme_defaults() -> None:
    """Apply shared Faststrap component defaults."""
    set_component_defaults("Button", variant="primary", size="md")
    set_component_defaults("Badge", pill=True)
    set_component_defaults("Card", cls="border-0 shadow-sm")
