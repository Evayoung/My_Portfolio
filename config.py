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
load_dotenv(BASE_DIR / ".env")
if not (BASE_DIR / ".env").exists():
    load_dotenv(BASE_DIR.parent / "neo-admin" / ".env")


@dataclass(frozen=True)
class Settings:
    secret_key: str = os.getenv("NEOPORTFOLIO_SECRET_KEY", "neoportfolio-secret-2025")
    session_cookie: str = "neoportfolio_session"
    use_cdn: bool = bool(os.getenv("VERCEL"))
    port: int = int(os.getenv("PORT", "5062"))
    supabase_url: str = os.getenv("SUPABASE_URL", "")
    supabase_anon_key: str = os.getenv("SUPABASE_ANON_KEY", "")
    supabase_service_role_key: str = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")


settings = Settings()
