"""Submission storage helpers for the public portfolio."""

from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

try:
    from ..config import settings
except ImportError:
    from config import settings

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class SubmissionResult:
    success: bool
    tone: str
    title: str
    message: str
    stored: bool


def submission_write_is_configured() -> bool:
    return bool(settings.supabase_url and settings.supabase_anon_key)


_EMAIL_PATTERN = re.compile(r"^[^\s@]+@[^\s@.]+(?:\.[^\s@.]+)+$")


def validate_contact_submission(*, name: str, email: str, subject: str, message: str) -> str:
    name, email, subject, message = name.strip(), email.strip(), subject.strip(), message.strip()
    if not name or len(name) > 120:
        return "Enter your name using no more than 120 characters."
    if len(email) > 254 or not _EMAIL_PATTERN.fullmatch(email):
        return "Enter a valid email address using no more than 254 characters."
    if len(subject) > 160:
        return "Keep the subject under 160 characters."
    if not message or len(message) > 5000:
        return "Enter a message using no more than 5,000 characters."
    return ""


def validate_booking_submission(
    *, name: str, email: str, whatsapp: str, service: str, budget: str, timeline: str, message: str,
) -> str:
    name, email, whatsapp = name.strip(), email.strip(), whatsapp.strip()
    service, budget, timeline, message = service.strip(), budget.strip(), timeline.strip(), message.strip()
    if not name or len(name) > 120:
        return "Enter your name using no more than 120 characters."
    if len(email) > 254 or not _EMAIL_PATTERN.fullmatch(email):
        return "Enter a valid email address using no more than 254 characters."
    if len(whatsapp) > 40:
        return "Keep the WhatsApp number under 40 characters."
    if any(len(value) > 120 for value in (service, budget, timeline)):
        return "Keep service, budget, and timeline details under 120 characters each."
    if not message or len(message) > 5000:
        return "Enter your project brief using no more than 5,000 characters."
    return ""


def _rest_request(path: str, payload: dict[str, object]) -> None:
    url = f"{settings.supabase_url.rstrip('/')}/rest/v1/{path}"
    key = settings.supabase_anon_key
    request = Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        method="POST",
        headers={
            "apikey": key,
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "Prefer": "return=minimal",
        },
    )
    with urlopen(request, timeout=20):
        return None


def submit_contact_inquiry(*, name: str, email: str, subject: str, message: str) -> SubmissionResult:
    validation_error = validate_contact_submission(name=name, email=email, subject=subject, message=message)
    if validation_error:
        logger.info("Public submission rejected by validation", extra={"submission_kind": "contact"})
        return SubmissionResult(False, "warning", "Check your message", validation_error, False)
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
        "email": email.strip().lower(),
        "subject": subject.strip(),
        "message": message.strip(),
    }

    try:
        _rest_request("contact_submissions", payload)
        logger.info("Public submission stored", extra={"submission_kind": "contact"})
        return SubmissionResult(
            success=True,
            tone="success",
            title="Message received",
            message="Your inquiry has been delivered successfully. I’ll review it and reply through the contact details you shared.",
            stored=True,
        )
    except HTTPError as exc:
        exc.read()
        logger.warning(
            "Public submission rejected by Supabase",
            extra={"submission_kind": "contact", "http_status": exc.code},
        )
        return SubmissionResult(
            success=False,
            tone="warning",
            title="Delivery needs a fallback",
            message="I couldn't store your message directly just now, so use the backup send options below instead and nothing gets lost.",
            stored=False,
        )
    except (URLError, TimeoutError, OSError, ValueError):
        logger.warning("Public submission delivery failed", extra={"submission_kind": "contact"})
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
    validation_error = validate_booking_submission(
        name=name, email=email, whatsapp=whatsapp, service=service, budget=budget, timeline=timeline, message=message,
    )
    if validation_error:
        logger.info("Public submission rejected by validation", extra={"submission_kind": "booking"})
        return SubmissionResult(False, "warning", "Check your project brief", validation_error, False)
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
        "email": email.strip().lower(),
        "whatsapp": whatsapp.strip(),
        "service": service.strip(),
        "budget": budget.strip(),
        "timeline": timeline.strip(),
        "message": message.strip(),
    }

    try:
        _rest_request("booking_requests", payload)
        logger.info("Public submission stored", extra={"submission_kind": "booking"})
        return SubmissionResult(
            success=True,
            tone="success",
            title="Brief received",
            message="Your project brief has been delivered successfully. I’ll review it and get back to you with the next step.",
            stored=True,
        )
    except HTTPError as exc:
        exc.read()
        logger.warning(
            "Public submission rejected by Supabase",
            extra={"submission_kind": "booking", "http_status": exc.code},
        )
        return SubmissionResult(
            success=False,
            tone="warning",
            title="Brief prepared",
            message="I couldn't store your brief directly just now, so use the backup send options below instead and nothing gets lost.",
            stored=False,
        )
    except (URLError, TimeoutError, OSError, ValueError):
        logger.warning("Public submission delivery failed", extra={"submission_kind": "booking"})
        return SubmissionResult(
            success=False,
            tone="warning",
            title="Brief prepared",
            message="I couldn't reach the inbox service just now, so use the backup send options below instead and nothing gets lost.",
            stored=False,
        )
