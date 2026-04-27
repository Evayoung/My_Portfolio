"""Modal compositions for the public site."""

from __future__ import annotations

from fasthtml.common import *
from faststrap import Modal

try:
    from ..content import CV_HIGHLIGHTS
except ImportError:
    from content import CV_HIGHLIGHTS


def service_modal() -> Div:
    return Modal(
        Div("Select a service to load details.", id="service-detail-body", cls="modal-fragment-shell"),
        modal_id="serviceModal",
        title="Service Details",
        size="lg",
        centered=True,
        content_cls="neo-modal-content",
        header_cls="border-0",
        close_cls="btn-close-white",
    )


def project_preview_modal() -> Div:
    return Modal(
        Div("Preview will load here.", id="project-preview-body", cls="modal-fragment-shell"),
        modal_id="projectPreviewModal",
        title="Project Preview",
        size="xl",
        centered=True,
        content_cls="neo-modal-content",
        header_cls="border-0",
        close_cls="btn-close-white",
    )


def case_study_modal() -> Div:
    return Modal(
        Div("Case study will load here.", id="case-study-body", cls="modal-fragment-shell"),
        modal_id="caseStudyModal",
        title="Case Study",
        size="xl",
        centered=True,
        scrollable=True,
        content_cls="neo-modal-content",
        header_cls="border-0",
        close_cls="btn-close-white",
    )


def cv_preview_modal() -> Div:
    cards = [
        Div(H4(title, cls="cv-highlight-title"), P(copy, cls="cv-highlight-copy"), cls="cv-highlight-card")
        for title, copy in CV_HIGHLIGHTS
    ]
    return Modal(
        Div(*cards, cls="cv-preview-grid"),
        modal_id="cvPreviewModal",
        title="Interactive CV Preview",
        size="lg",
        centered=True,
        content_cls="neo-modal-content",
        header_cls="border-0",
        close_cls="btn-close-white",
    )
