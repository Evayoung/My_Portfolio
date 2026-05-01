"""Submission storage helpers for the public portfolio."""

from __future__ import annotations

import json
from dataclasses import dataclass
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

try:
    from ..config import settings
except ImportError:
    from config import settings


@dataclass(frozen=True)
class SubmissionResult:
    success: bool
    tone: str
    title: str
    message: str
    stored: bool


def submission_write_is_configured() -> bool:
    return bool(settings.supabase_url and settings.supabase_service_role_key)


def _rest_request(path: str, payload: dict[str, object]) -> None:
    url = f"{settings.supabase_url.rstrip('/')}/rest/v1/{path}"
    request = Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        method="POST",
        headers={
            "apikey": settings.supabase_service_role_key,
            "Authorization": f"Bearer {settings.supabase_service_role_key}",
            "Content-Type": "application/json",
            "Prefer": "return=minimal",
        },
    )
    with urlopen(request, timeout=20):
        return None


def submit_contact_inquiry(*, name: str, email: str, subject: str, message: str) -> SubmissionResult:
    if not submission_write_is_configured():
        return SubmissionResult(
            success=False,
            tone="info",
            title="Ready to send",
            message="Direct inbox delivery is not connected in this public build yet, so use one of the options below to send the exact message you wrote.",
            stored=False,
        )

    payload = {
        "name": name.strip(),
        "email": email.strip(),
        "subject": subject.strip(),
        "message": message.strip(),
        "status": "new",
        "source": "portfolio",
    }

    try:
        _rest_request("contact_submissions", payload)
        return SubmissionResult(
            success=True,
            tone="success",
            title="Message received",
            message="Your inquiry has been delivered successfully. I’ll review it and reply through the contact details you shared.",
            stored=True,
        )
    except HTTPError as exc:
        exc.read()
        return SubmissionResult(
            success=False,
            tone="warning",
            title="Delivery needs a fallback",
            message="I couldn't store your message directly just now, so use the backup send options below instead and nothing gets lost.",
            stored=False,
        )
    except (URLError, TimeoutError, OSError, ValueError):
        return SubmissionResult(
            success=False,
            tone="warning",
            title="Delivery needs a fallback",
            message="I couldn't reach the inbox service just now, so use the backup send options below instead and nothing gets lost.",
            stored=False,
        )


def submit_booking_request(
    *,
    name: str,
    email: str,
    whatsapp: str,
    service: str,
    budget: str,
    timeline: str,
    message: str,
) -> SubmissionResult:
    if not submission_write_is_configured():
        return SubmissionResult(
            success=False,
            tone="info",
            title="Brief prepared",
            message="The booking flow is ready, but direct inbox delivery is still being wired. Send this exact brief through WhatsApp or email below so nothing gets lost.",
            stored=False,
        )

    payload = {
        "name": name.strip(),
        "email": email.strip(),
        "whatsapp": whatsapp.strip(),
        "service": service.strip(),
        "budget": budget.strip(),
        "timeline": timeline.strip(),
        "message": message.strip(),
        "status": "new",
        "source": "portfolio",
    }

    try:
        _rest_request("booking_requests", payload)
        return SubmissionResult(
            success=True,
            tone="success",
            title="Brief received",
            message="Your project brief has been delivered successfully. I’ll review it and get back to you with the next step.",
            stored=True,
        )
    except HTTPError as exc:
        exc.read()
        return SubmissionResult(
            success=False,
            tone="warning",
            title="Brief prepared",
            message="I couldn't store your brief directly just now, so use the backup send options below instead and nothing gets lost.",
            stored=False,
        )
    except (URLError, TimeoutError, OSError, ValueError):
        return SubmissionResult(
            success=False,
            tone="warning",
            title="Brief prepared",
            message="I couldn't reach the inbox service just now, so use the backup send options below instead and nothing gets lost.",
            stored=False,
        )
