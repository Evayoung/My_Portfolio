"""GitHub section widget for NeoPortfolio.

Renders two components:
- github_compact_widget()  → compact 4-stat strip for the homepage
- github_full_section()    → full stats + repo cards for the CV page
"""

from __future__ import annotations

from fasthtml.common import A, Div, H2, H3, P, Section, Span

try:
    from ..content import GITHUB_URL
    from ..services.github_service import GitHubRepo, get_github_repos, get_github_snapshot
except ImportError:
    from content import GITHUB_URL
    from services.github_service import GitHubRepo, get_github_repos, get_github_snapshot


# ── Language colour map ───────────────────────────────────────────────────────

_LANG_COLOURS: dict[str, str] = {
    "Python": "#3572A5",
    "JavaScript": "#f1e05a",
    "TypeScript": "#2b7489",
    "HTML": "#e34c26",
    "CSS": "#563d7c",
    "Shell": "#89e051",
    "Go": "#00ADD8",
    "Rust": "#dea584",
    "Java": "#b07219",
    "Kotlin": "#A97BFF",
    "Swift": "#ffac45",
    "Dart": "#00B4AB",
    "C": "#555555",
    "C++": "#f34b7d",
    "C#": "#178600",
    "Ruby": "#701516",
}

_DEFAULT_LANG_COLOUR = "#8e9bb5"


def _lang_dot(language: str) -> Span:
    colour = _LANG_COLOURS.get(language, _DEFAULT_LANG_COLOUR)
    return Span(
        Span(style=f"width:10px;height:10px;border-radius:50%;background:{colour};display:inline-block;margin-right:5px;"),
        language,
        style="display:inline-flex;align-items:center;font-size:0.75rem;color:#8fa3b8;",
    )


def _repo_card(repo: GitHubRepo) -> Div:
    return Div(
        A(
            Div(
                Div(
                    Span("📁", style="margin-right:6px;"),
                    Span(repo.name, cls="gh-repo-name"),
                    cls="d-flex align-items-center",
                ),
                P(repo.description or "No description provided.", cls="gh-repo-desc"),
                Div(
                    _lang_dot(repo.language) if repo.language else Span(""),
                    Div(
                        Span("⭐", style="margin-right:3px;"),
                        Span(str(repo.stars), style="margin-right:12px;font-size:0.75rem;color:#8fa3b8;"),
                        Span("🍴", style="margin-right:3px;"),
                        Span(str(repo.forks), style="font-size:0.75rem;color:#8fa3b8;"),
                    ),
                    cls="d-flex justify-content-between align-items-center mt-auto pt-3",
                ),
                cls="gh-repo-card-inner",
            ),
            href=repo.url,
            target="_blank",
            rel="noreferrer noopener",
            cls="gh-repo-link",
        ),
        cls="gh-repo-card",
    )


def _stat_cell(value: str, label: str) -> Div:
    return Div(
        Div(value, cls="gh-stat-value"),
        Span(label, cls="gh-stat-label"),
        cls="gh-stat-cell",
    )


# ── Public components ─────────────────────────────────────────────────────────

def github_compact_widget() -> Div:
    """4-stat bar for the homepage (repos, stars, followers, commits)."""
    snap = get_github_snapshot()
    is_live = snap.source == "github"
    return Div(
        Div(
            Div(
                Span("⬡", cls="gh-compact-icon"),
                Span("GitHub Activity", cls="gh-compact-label"),
                A(
                    f"/{snap.username}",
                    href=GITHUB_URL,
                    target="_blank",
                    rel="noreferrer",
                    cls="gh-compact-handle",
                ),
                cls="gh-compact-header",
            ),
            Div(
                _stat_cell(f"{snap.public_repos}+", "Public Repos"),
                _stat_cell(str(snap.followers), "Followers"),
                _stat_cell(str(snap.recent_commits), "Recent Commits"),
                _stat_cell("Python", "Primary Stack"),
                cls="gh-compact-stats",
            ),
            cls="gh-compact-inner",
        ),
        Span(
            "● Live" if is_live else "● Data unavailable without token",
            cls=f"gh-live-badge {'live' if is_live else 'offline'}",
        ),
        cls="gh-compact-widget",
        id="github-compact",
    )


def github_full_section() -> Section:
    """Full GitHub stats + repo grid for the CV page."""
    snap = get_github_snapshot()
    repos = get_github_repos(limit=6)

    repo_grid = Div(
        *[_repo_card(r) for r in repos],
        cls="gh-repo-grid",
    ) if repos else Div(
        P(
            "Repo data requires a GitHub token or becomes available once rate limits reset.",
            cls="gh-empty-note",
        ),
        cls="gh-repo-empty",
    )

    return Section(
        Div(
            # Section header
            Div(
                Span("OPEN SOURCE", cls="cv-kicker"),
                H2("GitHub Activity", cls="cv-section-title"),
                P(
                    "Public repositories and contribution stats pulled live from the GitHub API.",
                    cls="cv-section-desc",
                ),
                cls="gh-full-header",
            ),

            # Stats bar
            Div(
                _stat_cell(f"{snap.public_repos}", "Public Repos"),
                _stat_cell(str(snap.followers), "Followers"),
                _stat_cell(str(snap.following), "Following"),
                _stat_cell(str(snap.recent_commits), "Recent Commits"),
                cls="gh-full-stats",
            ),

            # Repo grid
            Div(
                H3("Featured Repositories", cls="gh-repos-title"),
                repo_grid,
                A(
                    "View all repositories on GitHub →",
                    href=GITHUB_URL,
                    target="_blank",
                    rel="noreferrer",
                    cls="gh-view-all",
                ),
                cls="gh-repos-section",
            ),

            cls="gh-full-inner",
        ),
        cls="gh-full-section content-section",
        id="github",
    )
