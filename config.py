"""Environment and project configuration for NeoPortfolio."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover
    def load_dotenv(*_args, **_kwargs) -> bool:
        return False


BASE_DIR = Path(__file__).resolve().parent
if not os.getenv("VERCEL"):
    load_dotenv(BASE_DIR / ".env")
    if not (BASE_DIR / ".env").exists():
        load_dotenv(BASE_DIR.parent / "neo-admin" / ".env")


@dataclass(frozen=True)
class Settings:
    secret_key: str = os.getenv("NEOPORTFOLIO_SECRET_KEY", "")
    session_cookie: str = "neoportfolio_session"
    use_cdn: bool = bool(os.getenv("VERCEL"))
    port: int = int(os.getenv("PORT", "5062"))
    supabase_url: str = os.getenv("SUPABASE_URL", "")
    supabase_anon_key: str = os.getenv("SUPABASE_ANON_KEY", "")
    supabase_service_role_key: str = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
    github_username: str = os.getenv("GITHUB_USERNAME", "Evayoung")
    github_access_token: str = os.getenv("GITHUB_ACCESS_TOKEN", "")


settings = Settings()


def _validate_production_settings() -> None:
    import warnings

    # Always warn about insecure defaults (not just on Vercel)
    if not settings.secret_key:
        warnings.warn(
            "NEOPORTFOLIO_SECRET_KEY is not set. Sessions are insecure. "
            "Set it in your .env file.",
            stacklevel=2,
        )

    if not os.getenv("VERCEL"):
        return

    # Production: raise errors
    if not settings.secret_key:
        raise RuntimeError("NEOPORTFOLIO_SECRET_KEY must be set to a secure value in production.")
    if settings.supabase_url in {"", "https://your-project-id.supabase.co"}:
        raise RuntimeError("SUPABASE_URL must be set in production.")
    if settings.supabase_anon_key in {"", "your-public-anon-key"}:
        raise RuntimeError("SUPABASE_ANON_KEY must be set in production.")
    if settings.supabase_service_role_key in {"", "your-service-role-key"}:
        raise RuntimeError("SUPABASE_SERVICE_ROLE_KEY must be set in production.")


_validate_production_settings()
