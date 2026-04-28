"""GitHub proof stats for the public portfolio."""

from __future__ import annotations

import json
from dataclasses import dataclass
from functools import lru_cache
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

try:
    from ..config import settings
    from ..content import ABOUT_STATS, GITHUB_URL, StatItem
except ImportError:
    from config import settings
    from content import ABOUT_STATS, GITHUB_URL, StatItem


@dataclass(frozen=True)
class GitHubSnapshot:
    username: str
    public_repos: int
    followers: int
    following: int
    stars: int
    recent_commits: int
    source: str


def _derive_username() -> str:
    if settings.github_username.strip():
        return settings.github_username.strip()
    parsed = urlparse(GITHUB_URL)
    return parsed.path.strip("/").split("/")[0] if parsed.path.strip("/") else "Evayoung"


def _headers() -> dict[str, str]:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "neoportfolio-github-stats",
    }
    if settings.github_access_token.strip():
        headers["Authorization"] = f"Bearer {settings.github_access_token.strip()}"
    return headers


def _request(path: str) -> object:
    request = Request(f"https://api.github.com{path}", headers=_headers())
    with urlopen(request, timeout=8) as response:
        return json.loads(response.read().decode("utf-8"))


@lru_cache(maxsize=1)
def get_github_snapshot() -> GitHubSnapshot:
    username = _derive_username()
    try:
        profile = _request(f"/users/{username}")
        repos = _request(f"/users/{username}/repos?per_page=100&type=owner&sort=updated")
        events = _request(f"/users/{username}/events/public?per_page=100")
        if not isinstance(profile, dict) or not isinstance(repos, list) or not isinstance(events, list):
            raise ValueError("Unexpected GitHub payload.")
        stars = sum(int(repo.get("stargazers_count") or 0) for repo in repos if isinstance(repo, dict))
        recent_commits = sum(
            len((event.get("payload") or {}).get("commits") or [])
            for event in events
            if isinstance(event, dict) and event.get("type") == "PushEvent"
        )
        return GitHubSnapshot(
            username=username,
            public_repos=int(profile.get("public_repos") or 0),
            followers=int(profile.get("followers") or 0),
            following=int(profile.get("following") or 0),
            stars=stars,
            recent_commits=recent_commits,
            source="github",
        )
    except (HTTPError, URLError, TimeoutError, ValueError, KeyError, TypeError, json.JSONDecodeError):
        return GitHubSnapshot(
            username=username,
            public_repos=0,
            followers=0,
            following=0,
            stars=0,
            recent_commits=0,
            source="fallback",
        )


def get_about_stats() -> tuple[StatItem, ...]:
    snapshot = get_github_snapshot()
    if snapshot.source != "github":
        return ABOUT_STATS
    return (
        ABOUT_STATS[0],
        ABOUT_STATS[1],
        StatItem(f"{snapshot.public_repos}+", "GitHub Repos"),
        StatItem(str(snapshot.recent_commits), "Recent Commits"),
    )


# ── Repo listing ──────────────────────────────────────────────────────────────

@dataclass(frozen=True)
class GitHubRepo:
    name: str
    description: str
    url: str
    stars: int
    forks: int
    language: str
    is_fork: bool


@lru_cache(maxsize=1)
def get_github_repos(*, limit: int = 6) -> tuple[GitHubRepo, ...]:
    """Return top non-fork repos sorted by star count."""
    username = _derive_username()
    try:
        repos = _request(f"/users/{username}/repos?per_page=30&type=owner&sort=pushed")
        if not isinstance(repos, list):
            return ()
        public_owned = [r for r in repos if isinstance(r, dict) and not r.get("fork")]
        sorted_repos = sorted(public_owned, key=lambda r: int(r.get("stargazers_count") or 0), reverse=True)
        return tuple(
            GitHubRepo(
                name=str(r.get("name") or ""),
                description=str(r.get("description") or ""),
                url=str(r.get("html_url") or ""),
                stars=int(r.get("stargazers_count") or 0),
                forks=int(r.get("forks_count") or 0),
                language=str(r.get("language") or ""),
                is_fork=bool(r.get("fork")),
            )
            for r in sorted_repos[:limit]
        )
    except (HTTPError, URLError, TimeoutError, ValueError, KeyError, TypeError, json.JSONDecodeError):
        return ()

