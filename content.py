"""Content models and public site data for NeoPortfolio."""

from __future__ import annotations

from dataclasses import dataclass
import importlib.util
import json
from pathlib import Path
import sys
from urllib.request import Request, urlopen

try:
    from .config import settings
except ImportError:
    _config_path = Path(__file__).with_name("config.py")
    _config_spec = importlib.util.spec_from_file_location("neoportfolio_runtime_config", _config_path)
    _config_module = importlib.util.module_from_spec(_config_spec)
    assert _config_spec and _config_spec.loader
    sys.modules[_config_spec.name] = _config_module
    _config_spec.loader.exec_module(_config_module)
    settings = _config_module.settings


DEVELOPER_NAME = "Olorundare Micheal Babawale"
DEVELOPER_NAME_SHORT = "Micheal Olorundare"
DEVELOPER_ROLE = "Full-Stack & AI Systems Architect"
EMAIL = "meshelleva@gmail.com"
PHONE = "+2348064676590"
WHATSAPP = "+2349029952120"
LOCATION = "Ilorin, Kwara State, Nigeria"
GITHUB_URL = "https://github.com/Evayoung"
LINKEDIN_URL = "https://linkedin.com/in/michealolorundare"
SITE_URL = "https://olorundaremicheal.vercel.app"


def _best_read_key() -> str:
    return settings.supabase_service_role_key or settings.supabase_anon_key


def _supabase_is_configured() -> bool:
    return bool(settings.supabase_url and _best_read_key())


def _rest_request(path: str, query: str = "") -> object:
    url = f"{settings.supabase_url.rstrip('/')}/rest/v1/{path}{query}"
    key = _best_read_key()
    request = Request(
        url,
        headers={
            "apikey": key,
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
    )
    with urlopen(request, timeout=5) as response:
        raw = response.read()
        if not raw:
            return None
        return json.loads(raw.decode("utf-8"))


def _derive_short_name(full_name: str, site_name: str) -> str:
    if site_name.strip():
        return site_name.replace(" Portfolio", "").strip()
    return DEVELOPER_NAME_SHORT


def _load_live_identity() -> dict[str, str]:
    if not _supabase_is_configured():
        return {}
    try:
        site_rows = _rest_request("site_settings", "?select=site_name,site_url,contact_email,contact_phone,location,github_url,linkedin_url,seo_title,seo_description&limit=1")
        cv_rows = _rest_request("cv_meta", "?select=full_name,role,email,phone,whatsapp,location,github_url,linkedin_url&limit=1")
        site_row = site_rows[0] if isinstance(site_rows, list) and site_rows else {}
        cv_row = cv_rows[0] if isinstance(cv_rows, list) and cv_rows else {}
        full_name = cv_row.get("full_name") or DEVELOPER_NAME
        site_name = site_row.get("site_name") or ""
        return {
            "developer_name": full_name,
            "developer_name_short": _derive_short_name(full_name, site_name),
            "developer_role": cv_row.get("role") or DEVELOPER_ROLE,
            "email": cv_row.get("email") or site_row.get("contact_email") or EMAIL,
            "phone": cv_row.get("phone") or site_row.get("contact_phone") or PHONE,
            "whatsapp": cv_row.get("whatsapp") or WHATSAPP,
            "location": cv_row.get("location") or site_row.get("location") or LOCATION,
            "github_url": cv_row.get("github_url") or site_row.get("github_url") or GITHUB_URL,
            "linkedin_url": cv_row.get("linkedin_url") or site_row.get("linkedin_url") or LINKEDIN_URL,
            "site_url": site_row.get("site_url") or SITE_URL,
        }
    except Exception:
        return {}


_LIVE_IDENTITY = _load_live_identity()

DEVELOPER_NAME = _LIVE_IDENTITY.get("developer_name", DEVELOPER_NAME)
DEVELOPER_NAME_SHORT = _LIVE_IDENTITY.get("developer_name_short", DEVELOPER_NAME_SHORT)
DEVELOPER_ROLE = _LIVE_IDENTITY.get("developer_role", DEVELOPER_ROLE)
EMAIL = _LIVE_IDENTITY.get("email", EMAIL)
PHONE = _LIVE_IDENTITY.get("phone", PHONE)
WHATSAPP = _LIVE_IDENTITY.get("whatsapp", WHATSAPP)
LOCATION = _LIVE_IDENTITY.get("location", LOCATION)
GITHUB_URL = _LIVE_IDENTITY.get("github_url", GITHUB_URL)
LINKEDIN_URL = _LIVE_IDENTITY.get("linkedin_url", LINKEDIN_URL)
SITE_URL = _LIVE_IDENTITY.get("site_url", SITE_URL)

ROLE_TITLES = (
    "Full-Stack Developer",
    "AI Systems Architect",
    "API & Backend Engineer",
    "Open-Source Builder",
)

HERO_SUMMARY = (
    "I design and ship production-ready software at the intersection of Python, AI, and real-world operations. "
    "From multi-agent backend systems and offline-first accessibility tools to secure biometric platforms and "
    "data infrastructure, I build products that are meant to survive actual use."
)

ABOUT_SUMMARY = (
    "Full-Stack and AI Systems Architect with hands-on experience delivering reliable systems across "
    "web, mobile, desktop, and distributed environments."
)

JOURNEY_PARAGRAPHS = (
    "I started as a statistics graduate who was curious about what software could make possible. That curiosity "
    "grew into a career built around designing systems that solve real problems for real people - from visually "
    "impaired students in Nigerian classrooms to operational teams that need better data, security, and automation.",
    "Today I work across the full stack: FastAPI backends, FastHTML and Reflex frontends, KivyMD mobile "
    "applications, AI-assisted workflows, and Linux-based device systems. I care most about architecture that "
    "holds up under real constraints - offline use, low-connectivity environments, operational complexity, and "
    "the need to keep software maintainable after launch.",
)


@dataclass(frozen=True)
class TechnicalSkill:
    name: str
    score: int
    badge: str


@dataclass(frozen=True)
class ExperienceItem:
    year: str
    title: str
    company: str
    summary: str


@dataclass(frozen=True)
class StatItem:
    value: str
    label: str


@dataclass(frozen=True)
class Service:
    slug: str
    title: str
    summary: str
    lead: str
    deliverables: tuple[str, ...]
    timeline: str
    price: str
    icon: str


@dataclass(frozen=True)
class PricingTier:
    title: str
    price: str
    highlight: str
    points: tuple[str, ...]


@dataclass(frozen=True)
class Project:
    slug: str
    title: str
    category: str
    summary: str
    narrative: str
    tech: tuple[str, ...]
    image: str
    complexity: int
    satisfaction: int
    featured: bool = False


@dataclass(frozen=True)
class Testimonial:
    quote: str
    author: str
    role: str
    company: str


TECHNICAL_SKILLS = (
    TechnicalSkill("Python / FastAPI", 97, "Backend"),
    TechnicalSkill("FastHTML / Faststrap", 95, "Full-Stack"),
    TechnicalSkill("AI & LLM Integration", 92, "AI/ML"),
    TechnicalSkill("PostgreSQL / SQLite", 90, "Database"),
    TechnicalSkill("Reflex (Full-Stack)", 88, "Full-Stack"),
    TechnicalSkill("PySide6 / PyQt6", 87, "Desktop"),
    TechnicalSkill("KivyMD (Mobile)", 85, "Mobile"),
    TechnicalSkill("Linux / systemd", 78, "DevOps"),
)

EXPERIENCE = (
    ExperienceItem(
        "2024 - Present",
        "Full-Stack & AI Systems Architect",
        "Independent / Freelance",
        "Designing and shipping production-grade systems across AI automation, security workflows, data infrastructure, and Python-native full-stack products.",
    ),
    ExperienceItem(
        "2023 - Present",
        "Python & Software Tutor",
        "SuperProf & Certmart",
        "Teaching Python, software architecture, and AI literacy through practical delivery-focused learning plans.",
    ),
    ExperienceItem(
        "2024 - 2025",
        "Backend Lead",
        "University of Ilorin - Clinic & CBT Projects",
        "Delivered institution-scale systems including a digital clinic platform and biometric exam access controls.",
    ),
)

ABOUT_STATS = (
    StatItem("10+", "Production Projects"),
    StatItem("5+", "Years Experience"),
    StatItem("3", "Active SaaS Products"),
    StatItem("2", "Institutional Systems"),
)

SERVICES = (
    Service(
        "backend-api",
        "Backend Architecture & API Development",
        "Reliable backend foundations with FastAPI, clean data models, and operational clarity from day one.",
        "Production-grade APIs, authentication systems, and service architecture designed to grow without turning brittle.",
        (
            "FastAPI REST API design and implementation",
            "Authentication, RBAC, and secure data modelling",
            "Microservice architecture and monolith planning",
            "Deployment pipelines and observability hooks",
        ),
        "3 - 6 weeks",
        "From N250k",
        "code-slash",
    ),
    Service(
        "ai-agent-design",
        "AI Agent Design & Automation Systems",
        "LLM-powered products, multi-agent workflows, and automation systems designed around real business operations.",
        "Practical AI that is useful in production - with guardrails, structure, and handoff paths where needed.",
        (
            "Multi-agent orchestration and workflow design",
            "RAG pipelines and tool-calling integration",
            "LLM fine-tuning and prompt engineering",
            "Automation dashboards and human-handoff flows",
        ),
        "2 - 5 weeks",
        "From N320k",
        "cpu",
    ),
    Service(
        "cross-platform-apps",
        "Cross-Platform Application Development",
        "Web, desktop, and mobile applications built with Python-first architecture and consistent product logic.",
        "From browser to phone to standalone desktop, the goal is one coherent system instead of fragmented builds.",
        (
            "FastHTML / Reflex full-stack web applications",
            "KivyMD Android/cross-platform mobile apps",
            "PySide6 / PyQt6 desktop GUI applications",
            "Offline-first architecture for low-connectivity environments",
        ),
        "3 - 8 weeks",
        "From N200k",
        "phone",
    ),
    Service(
        "consulting",
        "Technical Consulting & System Reviews",
        "Architecture reviews, technical direction, and focused guidance for teams making important product decisions.",
        "Engineering clarity: what to build, how to sequence it, where the risks are, and what not to overengineer.",
        (
            "Architecture and product audits",
            "Performance and reliability reviews",
            "AI adoption roadmaps",
            "Technical documentation and knowledge transfer",
        ),
        "1 - 2 weeks",
        "From N80k",
        "chat-square",
    ),
)

PRICING_TIERS = (
    PricingTier(
        "Starter",
        "N80k+",
        "A focused engagement for a clearly defined feature, review, or technical decision.",
        ("Single endpoint or feature", "Documentation included", "1 revision cycle"),
    ),
    PricingTier(
        "Product",
        "N250k+",
        "End-to-end delivery for a product, platform, or high-value internal system.",
        ("Full-stack delivery", "Auth, data layer, UI", "Performance and UX pass"),
    ),
    PricingTier(
        "Partner",
        "Custom",
        "Ongoing technical partnership for larger, evolving, or operationally sensitive initiatives.",
        ("Architecture guidance", "AI or agent systems", "Iteration and support retainer"),
    ),
)

PORTFOLIO_FILTERS = (
    ("all", "All"),
    ("full-stack", "Full-Stack"),
    ("ai-ml", "AI / ML"),
    ("security", "Security"),
    ("mobile", "Mobile"),
    ("desktop", "Desktop"),
    ("web", "Web"),
)

PROJECTS = (
    Project(
        "backendforge",
        "BackendForge - Multi-Agent FastAPI Builder",
        "ai-ml",
        "An orchestration system where 18 specialised AI agents collaboratively plan, generate, and validate FastAPI backends from natural-language requirements.",
        "Each agent owns a narrow responsibility - schema design, routing, auth, documentation, validation, and more - while a coordinating layer manages sequencing, handoffs, and correction loops. The result is a backend build pipeline that reduces scaffolding effort without pretending human judgement is optional.",
        ("Python", "FastAPI", "Multi-Agent AI", "LLM", "+2"),
        "/assets/images/hero-bg.jpg",
        95,
        97,
        featured=True,
    ),
    Project(
        "voice-learning-assistant",
        "Voice-First Learning Assistant",
        "ai-ml",
        "A cross-platform accessibility platform delivering voice-driven learning to visually impaired students in Nigeria with hybrid offline and online support.",
        "Designed a four-part architecture spanning a Reflex web client, KivyMD mobile client, FastAPI sync server, and teacher dashboard. The speech layer combines Google Cloud STT with Faster-Whisper fallback so the system keeps working when connectivity becomes unreliable.",
        ("FastAPI", "Reflex", "KivyMD", "Faster-Whisper", "+2"),
        "/assets/images/hero-bg2.jpg",
        93,
        98,
        featured=True,
    ),
    Project(
        "student-ews",
        "Student Early Warning System (EWS)",
        "full-stack",
        "An academic monitoring platform for UNILORIN with risk classification, inline score workflows, and role-specific operational dashboards.",
        "Built an event-driven academic pipeline where score updates trigger GPA recomputation, risk reclassification, and alert refreshes inside a single FastHTML + FastAPI application. Admin, lecturer, and student portals each expose only the decisions and actions relevant to them.",
        ("FastHTML", "Faststrap", "SQLite", "HTMX", "+1"),
        "/assets/images/hero-bg3.jpg",
        92,
        96,
        featured=True,
    ),
    Project(
        "qrive",
        "QRive - Verified Digital Hubs via QR",
        "full-stack",
        "A SaaS identity-verification platform that uses dynamic QR codes, AI-assisted validation, and trust scoring to help businesses prove legitimacy.",
        "Built with FastAPI and Reflex. Each business hub receives a dynamic QR profile that aggregates verified links, payment details, and proof artifacts in a tamper-evident presentation layer while AI workflows help reduce low-quality or fraudulent submissions.",
        ("FastAPI", "Reflex", "AI Validation", "PostgreSQL"),
        "/assets/images/hero-bg4.jpg",
        88,
        94,
    ),
    Project(
        "truetag",
        "TrueTag - Product Authentication Backend",
        "security",
        "A product-authentication backend that mints blockchain-linked identifiers and flags suspicious scan activity through geolocation-aware fraud signals.",
        "Built for an authenticity platform where every product receives a unique token and every verification event is logged with scan context. Duplicate or geographically inconsistent scan patterns raise fraud alerts automatically.",
        ("FastAPI", "Blockchain", "PostgreSQL", "Fraud Detection"),
        "/assets/images/hero-bg.jpg",
        90,
        95,
    ),
    Project(
        "fingerprint-access",
        "Fingerprint Access Control - UNILORIN CBT",
        "security",
        "A biometric attendance and exam-security system for CBT centres at the University of Ilorin, built to reduce impersonation risk during high-stakes testing.",
        "Built a FastAPI backend with fingerprint template management, fallback verification flows, and a Reflex admin dashboard. Role-based permissions give invigilators, supervisors, and administrators different levels of operational control.",
        ("FastAPI", "KivyMD", "Reflex", "Biometrics", "+1"),
        "/assets/images/hero-bg2.jpg",
        91,
        96,
    ),
    Project(
        "stego",
        "Stego - Secure Image Steganography",
        "security",
        "A PySide6 desktop application implementing AES-256 and hybrid DCT-LSB steganography for securely hiding encrypted files inside images.",
        "Originally defended as a final-year project, then pushed further as an actual engineering exercise. The system balances payload capacity, perceptual fidelity, and extraction reliability while supporting both text and arbitrary file embedding.",
        ("PySide6", "AES-256", "DCT-LSB", "Python"),
        "/assets/images/hero-bg3.jpg",
        89,
        97,
        featured=True,
    ),
    Project(
        "clinic-management",
        "Clinic Management System - UNILORIN",
        "full-stack",
        "A digital health-records platform that replaces paper-based clinic workflows at the University of Ilorin with QR-linked access and role-aware dashboards.",
        "The system moves clinical record access, pharmacy coordination, and operational reporting into a secure digital workflow. QR-enabled student cards speed up record retrieval while tailored dashboards keep each role focused on the right information.",
        ("FastAPI", "PostgreSQL", "QR Access", "RBAC"),
        "/assets/images/hero-bg4.jpg",
        87,
        95,
    ),
    Project(
        "cooperative-thrift",
        "Thrift Contribution Management System",
        "full-stack",
        "A cooperative savings platform with contribution tracking, withdrawal rotation, and payment scheduling for thrift-based finance groups.",
        "Built as a FastAPI backend with a Reflex frontend. Members can monitor contributions, understand payout order clearly, and receive reminders while administrators manage schedules and disbursement logic with less spreadsheet overhead.",
        ("FastAPI", "Reflex", "Paystack", "PostgreSQL"),
        "/assets/images/hero-bg.jpg",
        85,
        93,
    ),
    Project(
        "church-platform",
        "DCLM Kwara - Church Data Platform",
        "full-stack",
        "A scalable data platform powering two mobile apps and a shared REST API across Deeper Christian Life Ministry branches in Kwara State.",
        "The platform uses custom RBAC across state, zone, and branch scopes while supporting attendance analytics, newcomer registration, and leadership dashboards. It was designed for distributed operational use rather than single-office administration.",
        ("FastAPI", "KivyMD", "PostgreSQL", "RBAC", "+1"),
        "/assets/images/hero-bg2.jpg",
        86,
        94,
    ),
    Project(
        "linux-image",
        "Custom Bootable Linux Image - Youyeetoo X1",
        "desktop",
        "A custom Ubuntu-based embedded OS image with autologin, persistent configuration, and a PyQt6 kiosk interface for the Youyeetoo X1 device.",
        "Built a lightweight image from scratch, resolved boot-loop issues through service-level Linux configuration, and embedded the PyQt6 interface as the primary hardware experience. The result was a device-ready image tested on real target hardware.",
        ("Ubuntu", "PyQt6", "systemd", "Linux"),
        "/assets/images/hero-bg3.jpg",
        88,
        96,
    ),
    Project(
        "neoportfolio",
        "NeoPortfolio - This Website",
        "web",
        "A stateless developer portfolio with a blog, branded CV, booking flow, and project detail pages, built entirely with FastHTML + Faststrap.",
        "This site is both a portfolio and a proof-of-approach: Python-native full-stack UI, server-rendered pages, HTMX-enhanced interaction, and zero dependency on a front-end JavaScript framework. It is designed to stay simple to host without looking technically limited.",
        ("FastHTML", "Faststrap", "HTMX", "Vercel"),
        "/assets/images/hero-bg4.jpg",
        90,
        98,
    ),
)

TESTIMONIALS = (
    Testimonial(
        "Micheal doesn't just write code - he studies the whole system. He surfaced architectural issues we had not seen yet and resolved them with surprising clarity.",
        "A. Salawu",
        "Project Supervisor",
        "University of Ilorin",
    ),
    Testimonial(
        "The fingerprint system he built for our CBT centre reduced impersonation concerns dramatically. It was reliable under pressure, fast to operate, and properly documented.",
        "B. Adesanya",
        "IT Coordinator",
        "CBT Centre, UNILORIN",
    ),
    Testimonial(
        "He turned a complicated cooperative finance workflow into something our members could actually understand and trust. The experience felt clean, simple, and usable.",
        "F. Adeyemi",
        "Cooperative Manager",
        "Ilorin Kwara",
    ),
)

CODE_SAMPLE = """\
# BackendForge - orchestrating 18 AI agents
async def build_api(spec: ProductSpec) -> FastAPIProject:
    schema   = await schema_agent.design(spec)
    routes   = await route_agent.generate(schema)
    auth     = await auth_agent.secure(routes)
    docs     = await doc_agent.write(routes, auth)
    return await validator_agent.certify(routes, auth, docs)
"""

HEATMAP_LEVELS = (
    3, 4, 2, 4, 4, 3, 2,
    1, 3, 4, 2, 4, 3, 2,
    2, 4, 4, 3, 2, 4, 4,
    3, 2, 1, 3, 4, 4, 2,
)

RADAR_SKILLS = (
    ("Backend", 97),
    ("AI/ML", 92),
    ("Full-Stack", 94),
    ("Desktop", 87),
    ("Mobile", 85),
)

CV_HIGHLIGHTS = (
    ("Specialisation", "Python-first product delivery, AI orchestration systems, and cross-platform application architecture."),
    ("Strengths", "Production-grade FastAPI, LLM integration, offline-first thinking, and secure system design."),
    ("Approach", "Build what will hold up in the real world - clear architecture, practical tradeoffs, and dependable delivery."),
)

PERFORMANCE_ITEMS = (
    ("Architecture", "Modular, testable backends designed for growth instead of rewrites."),
    ("AI Integration", "LLMs wired into real workflows with guardrails, fallbacks, and evaluation checkpoints."),
    ("Delivery", "Server-rendered FastHTML with HTMX - fast, stateless, and Vercel-ready."),
)

SOCIAL_LINKS = (
    ("github", GITHUB_URL, "GitHub", "#24292f"),
    ("linkedin", LINKEDIN_URL, "LinkedIn", "#0a66c2"),
    ("envelope", f"mailto:{EMAIL}", "Email", "#f8c73a"),
)

KEYWORDS_GLOBAL = [
    "Olorundare Micheal",
    "Full-Stack Developer",
    "AI Engineer",
    "FastAPI",
    "FastHTML",
    "Faststrap",
    "Python Developer",
    "Nigeria",
    "Ilorin",
    "Backend Developer",
    "AI Systems Architect",
    "KivyMD",
    "Reflex",
]
