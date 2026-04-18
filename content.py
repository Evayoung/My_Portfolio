"""Content models and real data for NeoPortfolio — Olorundare Micheal Babawale."""

from __future__ import annotations

from dataclasses import dataclass

# ── Personal constants ────────────────────────────────────────────────────────

DEVELOPER_NAME      = "Olorundare Micheal Babawale"
DEVELOPER_NAME_SHORT = "Micheal Olorundare"
DEVELOPER_ROLE      = "Full-Stack & AI Systems Architect"
EMAIL               = "meshelleva@gmail.com"
PHONE               = "+2348064676590"
WHATSAPP            = "+2349029952120"
LOCATION            = "Ilorin, Kwara State, Nigeria"
GITHUB_URL          = "https://github.com/Evayoung"
LINKEDIN_URL        = "https://linkedin.com/in/michealolorundare"
SITE_URL            = "https://micheal.dev"  # update when domain is live

# Forms — replace YOUR_FORM_ID with your real Formspree endpoint after signup at formspree.io
FORMSPREE_CONTACT_ID = "YOUR_CONTACT_FORM_ID"
FORMSPREE_BOOKING_ID = "YOUR_BOOKING_FORM_ID"

ROLE_TITLES = (
    "Full-Stack Developer",
    "AI Systems Architect",
    "API & Backend Engineer",
    "Open-Source Builder",
)

HERO_SUMMARY = (
    "Building intelligent, scalable systems at the intersection of Python, AI, and real-world impact. "
    "From autonomous AI agents and voice-first accessibility tools to secure biometric platforms and "
    "church data systems — I ship products that genuinely work."
)

ABOUT_SUMMARY = (
    "Versatile Full-Stack & AI Systems Architect with proven expertise in designing, deploying, "
    "and optimizing scalable intelligent systems across web, mobile, and distributed environments."
)

JOURNEY_PARAGRAPHS = (
    "I started as a statistics graduate curious about what code could do. That curiosity turned into "
    "a vocation: designing systems that solve real problems for real people — from visually impaired "
    "students in Nigerian classrooms to cooperative savings groups in Ilorin.",

    "Today I work across the full stack: FastAPI backends, Reflex and FastHTML frontends, KivyMD mobile "
    "apps, AI pipelines, and Linux-embedded systems. I'm especially interested in offline-first "
    "architecture, multi-agent AI automation, and making advanced technology accessible to underserved "
    "communities.",
)


# ── Data classes ──────────────────────────────────────────────────────────────

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


# ── Skills ────────────────────────────────────────────────────────────────────

TECHNICAL_SKILLS = (
    TechnicalSkill("Python / FastAPI",      97, "Backend"),
    TechnicalSkill("FastHTML / Faststrap",  95, "Full-Stack"),
    TechnicalSkill("AI & LLM Integration",  92, "AI/ML"),
    TechnicalSkill("PostgreSQL / SQLite",   90, "Database"),
    TechnicalSkill("Reflex (Full-Stack)",   88, "Full-Stack"),
    TechnicalSkill("PySide6 / PyQt6",       87, "Desktop"),
    TechnicalSkill("KivyMD (Mobile)",       85, "Mobile"),
    TechnicalSkill("Linux / Systemd",       78, "DevOps"),
)

EXPERIENCE = (
    ExperienceItem(
        "2024 – Present",
        "Full-Stack & AI Systems Architect",
        "Independent / Freelance",
        "Designing and shipping production-grade systems: AI agents, biometric platforms, church data "
        "infrastructure, SaaS products, and FastHTML-based web apps.",
    ),
    ExperienceItem(
        "2023 – Present",
        "Python & Software Tutor",
        "SuperProf & Certmart",
        "Teaching Python, software architecture, and AI literacy with tailored learning plans for "
        "students across experience levels.",
    ),
    ExperienceItem(
        "2024 – 2025",
        "Backend Lead",
        "University of Ilorin – Clinic & CBT Projects",
        "Delivered two institution-scale systems: a digital clinic management platform and a fingerprint "
        "biometric access control system for CBT centres.",
    ),
)

ABOUT_STATS = (
    StatItem("10+",  "Production Projects"),
    StatItem("5+",   "Years Experience"),
    StatItem("3",    "Active SaaS Products"),
    StatItem("2",    "Institutional Systems"),
)

# ── Services ──────────────────────────────────────────────────────────────────

SERVICES = (
    Service(
        "backend-api",
        "Backend Architecture & API Development",
        "Building reliable, scalable product foundations with FastAPI and modern data design.",
        "Production-grade REST APIs, auth systems, and cloud-ready services designed for growth.",
        (
            "FastAPI REST API design and implementation",
            "Authentication, RBAC, and secure data modelling",
            "Microservice architecture and monolith planning",
            "Deployment pipelines and observability hooks",
        ),
        "3 – 6 weeks",
        "From ₦250k",
        "code-slash",
    ),
    Service(
        "ai-agent-design",
        "AI Agent Design & Automation Systems",
        "Building intelligent multi-agent systems and LLM-powered automation for real workflows.",
        "Practical AI that runs in production — not just demos.",
        (
            "Multi-agent orchestration and workflow design",
            "RAG pipelines and tool-calling integration",
            "LLM fine-tuning and prompt engineering",
            "Automation dashboards and human-handoff flows",
        ),
        "2 – 5 weeks",
        "From ₦320k",
        "cpu",
    ),
    Service(
        "cross-platform-apps",
        "Cross-Platform Application Development",
        "Web, desktop, and mobile apps built with Python — one language, coherent architecture.",
        "From browser to phone to standalone desktop — all from a unified Python codebase.",
        (
            "FastHTML / Reflex full-stack web applications",
            "KivyMD Android/cross-platform mobile apps",
            "PySide6 / PyQt6 desktop GUI applications",
            "Offline-first architecture for low-connectivity environments",
        ),
        "3 – 8 weeks",
        "From ₦200k",
        "phone",
    ),
    Service(
        "consulting",
        "Technical Consulting & System Reviews",
        "Architecture audits, performance reviews, and research-backed technical direction.",
        "Engineering clarity: know what to build, how to build it, and what to avoid.",
        (
            "Architecture and product audits",
            "Performance and reliability reviews",
            "AI adoption roadmaps",
            "Technical documentation and knowledge transfer",
        ),
        "1 – 2 weeks",
        "From ₦80k",
        "chat-square",
    ),
)

PRICING_TIERS = (
    PricingTier(
        "Starter",
        "₦80k+",
        "Focused delivery for a single well-defined feature or audit.",
        ("Single endpoint or feature", "Documentation included", "1 revision cycle"),
    ),
    PricingTier(
        "Product",
        "₦250k+",
        "End-to-end delivery for a complete product or vertical.",
        ("Full-stack delivery", "Auth, data layer, UI", "Performance and UX pass"),
    ),
    PricingTier(
        "Partner",
        "Custom",
        "Ongoing technical collaboration for larger or long-running initiatives.",
        ("Architecture guidance", "AI or agent systems", "Iteration and support retainer"),
    ),
)

# ── Portfolio filters ─────────────────────────────────────────────────────────

PORTFOLIO_FILTERS = (
    ("all",        "All"),
    ("full-stack", "Full-Stack"),
    ("ai-ml",      "AI / ML"),
    ("security",   "Security"),
    ("mobile",     "Mobile"),
    ("desktop",    "Desktop"),
    ("web",        "Web"),
)

# ── Projects ──────────────────────────────────────────────────────────────────

PROJECTS = (
    Project(
        "backendforge",
        "BackendForge — Multi-Agent FastAPI Builder",
        "ai-ml",
        "An experimental system where 18 collaborating AI agents autonomously plan, write, "
        "and test FastAPI backends from natural language specifications.",
        "Assigned each of 18 AI agents a specialized role — schema design, route generation, "
        "auth planning, documentation, validation — then built an orchestration layer that "
        "coordinates them into a coherent backend build pipeline. The result: a system "
        "that can scaffold a production-ready FastAPI service with minimal human input.",
        ("Python", "FastAPI", "Multi-Agent AI", "LLM", "+2"),
        "/assets/images/hero-bg.jpg",
        95, 97,
        featured=True,
    ),
    Project(
        "voice-learning-assistant",
        "Voice-First Learning Assistant",
        "ai-ml",
        "A cross-platform accessible learning ecosystem delivering voice-driven education "
        "to visually impaired students in Nigeria, with hybrid offline/online capability.",
        "Designed a Four-Component architecture: Reflex web client, KivyMD mobile client "
        "(offline-capable), a FastAPI sync server, and a teacher admin dashboard. "
        "Engineered a hybrid STT engine (Google Cloud + Faster-Whisper fallback) achieving "
        "95%+ accuracy on Nigerian-accented speech, with non-blocking TTS via background threading.",
        ("FastAPI", "Reflex", "KivyMD", "Faster-Whisper", "+2"),
        "/assets/images/hero-bg2.jpg",
        93, 98,
        featured=True,
    ),
    Project(
        "student-ews",
        "Student Early Warning System (EWS)",
        "full-stack",
        "A production-grade academic monitoring platform for UNILORIN with a 10-rule risk "
        "classification engine, HTMX inline score entry, and role-based portals.",
        "Built a fully event-driven pipeline: score entry triggers GPA recomputation, "
        "risk reclassification (R01–R10), and real-time alert dispatch — all within a "
        "single FastHTML + FastAPI application. Admin, Lecturer, and Student portals each "
        "with tailored dashboards and HTMX-powered interactions.",
        ("FastHTML", "Faststrap", "SQLite", "HTMX", "+1"),
        "/assets/images/hero-bg3.jpg",
        92, 96,
        featured=True,
    ),
    Project(
        "qrive",
        "QRive — Verified Digital Hubs via QR",
        "full-stack",
        "A SaaS platform that verifies business identities through dynamic QR codes, "
        "with AI-powered content validation and trust scoring.",
        "Built with FastAPI + Reflex. Each registered hub gets a dynamic QR that aggregates "
        "verified social links, payment details, and identity proofs in a tamper-evident "
        "package. AI validates submitted content and assigns trust scores, reducing fraud.",
        ("FastAPI", "Reflex", "AI Validation", "PostgreSQL"),
        "/assets/images/hero-bg4.jpg",
        88, 94,
    ),
    Project(
        "truetag",
        "TrueTag — Product Authentication Backend",
        "security",
        "A production FastAPI backend that mints blockchain-linked tokens for product "
        "authentication and detects counterfeiting through geolocation scan analysis.",
        "Built for a startup authenticity platform. Each product receives a unique "
        "blockchain token. Scan events are logged with device + geolocation data. "
        "Duplicate scan patterns trigger fraud alerts automatically.",
        ("FastAPI", "Blockchain", "PostgreSQL", "Fraud Detection"),
        "/assets/images/hero-bg.jpg",
        90, 95,
    ),
    Project(
        "fingerprint-access",
        "Fingerprint Access Control — UNILORIN CBT",
        "security",
        "A biometric attendance and exam security platform for CBT centres at the "
        "University of Ilorin, reducing impersonation cases significantly.",
        "Built a FastAPI backend with fingerprint template management, fallback "
        "verification flows, and a Reflex admin dashboard. Role-based permissions "
        "allow invigilators, supervisors, and admins different levels of control.",
        ("FastAPI", "KivyMD", "Reflex", "Biometrics", "+1"),
        "/assets/images/hero-bg2.jpg",
        91, 96,
    ),
    Project(
        "stego",
        "Stego — Secure Image Steganography",
        "security",
        "A full-stack PySide6 desktop application implementing AES-256 + DCT-LSB hybrid "
        "steganography for embedding and extracting encrypted documents in images.",
        "Defended as a final-year project. Combines DCT domain steganography with LSB "
        "embedding and AES-256 encryption to achieve high payload capacity and "
        "perceptual fidelity. Supports text and arbitrary file embedding.",
        ("PySide6", "AES-256", "DCT-LSB", "Python"),
        "/assets/images/hero-bg3.jpg",
        89, 97,
        featured=True,
    ),
    Project(
        "clinic-management",
        "Clinic Management System — UNILORIN",
        "full-stack",
        "A digital health records platform replacing paper-based clinic workflows at the "
        "University of Ilorin, with QR-card access and role-based dashboards.",
        "Replaced a fully manual records system with secure digital health profiles. "
        "Students carry QR-encoded cards for instant record access. Role dashboards "
        "for students, doctors, pharmacists, and admins with tailored views.",
        ("FastAPI", "PostgreSQL", "QR Access", "RBAC"),
        "/assets/images/hero-bg4.jpg",
        87, 95,
    ),
    Project(
        "cooperative-thrift",
        "Thrift Contribution Management System",
        "full-stack",
        "A digital cooperative savings platform with automated withdrawal rotation, "
        "Paystack payment scheduling, and fair contribution calculations.",
        "Two-part system: FastAPI REST backend + Reflex frontend. Members track "
        "contributions, view rotation schedules, and receive payment reminders. "
        "Paystack integration handles automated disbursements.",
        ("FastAPI", "Reflex", "Paystack", "PostgreSQL"),
        "/assets/images/hero-bg.jpg",
        85, 93,
    ),
    Project(
        "church-platform",
        "DCLM Kwara — Church Data Platform",
        "full-stack",
        "A scalable data platform powering two mobile apps and a REST API across "
        "all Deeper Christian Life Ministry branches in Kwara State.",
        "FastAPI backend with custom RBAC handling state-level, zone-level, and "
        "branch-level data access. Enables gender- and age-based attendance analytics, "
        "newcomer registration, and real-time reporting dashboards for church leaders.",
        ("FastAPI", "KivyMD", "PostgreSQL", "RBAC", "+1"),
        "/assets/images/hero-bg2.jpg",
        86, 94,
    ),
    Project(
        "linux-image",
        "Custom Bootable Linux Image — Youyeetoo X1",
        "desktop",
        "An Ubuntu-based embedded OS image with autologin, persistent path config, "
        "and an integrated PyQt6 GUI for the Youyeetoo X1 hardware device.",
        "Engineered a lightweight minimal Ubuntu image from scratch. Resolved boot-loop "
        "issues via systemd service configuration, embedded a PyQt6 kiosk GUI as the "
        "primary interface, and delivered a production-ready fallback-friendly image "
        "tested on actual hardware.",
        ("Ubuntu", "PyQt6", "systemd", "Linux"),
        "/assets/images/hero-bg3.jpg",
        88, 96,
    ),
    Project(
        "neoportfolio",
        "NeoPortfolio — This Website",
        "web",
        "A stateless, Vercel-deployable developer portfolio with blog, full CV, "
        "and booking pages — built entirely with FastHTML + Faststrap.",
        "Designed and built this site as a showcase of what Python-native full-stack "
        "looks like. Zero JavaScript frameworks, no database. Every page is server-rendered, "
        "HTMX-enhanced, and fully stateless — ready for Vercel edge deployment.",
        ("FastHTML", "Faststrap", "HTMX", "Vercel"),
        "/assets/images/hero-bg4.jpg",
        90, 98,
    ),
)

# ── Testimonials ──────────────────────────────────────────────────────────────

TESTIMONIALS = (
    Testimonial(
        "Micheal doesn't just write code — he thinks through the whole system. "
        "He identified architectural problems we hadn't even noticed and fixed them cleanly.",
        "A. Salawu",
        "Project Supervisor",
        "University of Ilorin",
    ),
    Testimonial(
        "The fingerprint system he built for our CBT centre eliminated impersonation "
        "almost completely. Reliable, fast, and well-documented.",
        "B. Adesanya",
        "IT Coordinator",
        "CBT Centre, UNILORIN",
    ),
    Testimonial(
        "He translated a complex cooperative finance flow into something our members "
        "could actually use. Clean interface, no confusion.",
        "F. Adeyemi",
        "Cooperative Manager",
        "Ilorin Kwara",
    ),
)

# ── Code sample (real, not filler) ───────────────────────────────────────────

CODE_SAMPLE = """\
# BackendForge — orchestrating 18 AI agents
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
    ("Backend",   97),
    ("AI/ML",     92),
    ("Full-Stack", 94),
    ("Desktop",   87),
    ("Mobile",    85),
)

# ── CV Highlights (shown in modals / CV zones) ───────────────────────────────

CV_HIGHLIGHTS = (
    ("Specialisation", "Full-stack Python delivery, AI agent systems, cross-platform application architecture."),
    ("Strengths",      "Production-grade FastAPI, LLM integration, offline-first systems, secure authentication."),
    ("Approach",       "Build what actually works — clean architecture, real-world constraints, shipped on time."),
)

PERFORMANCE_ITEMS = (
    ("Architecture",   "Modular, testable backends designed for growth — not rewrites."),
    ("AI Integration", "LLMs wired into real workflows with guardrails, fallbacks, and evaluation checkpoints."),
    ("Delivery",       "Server-rendered FastHTML with HTMX — fast, stateless, Vercel-ready."),
)

SOCIAL_LINKS = (
    ("github",   GITHUB_URL,   "GitHub",   "#24292f"),
    ("linkedin", LINKEDIN_URL, "LinkedIn", "#0a66c2"),
    ("envelope", f"mailto:{EMAIL}", "Email", "#f8c73a"),
)

KEYWORDS_GLOBAL = [
    "Olorundare Micheal", "Full-Stack Developer", "AI Engineer", "FastAPI",
    "FastHTML", "Faststrap", "Python Developer", "Nigeria", "Ilorin",
    "Backend Developer", "AI Systems Architect", "KivyMD", "Reflex",
]
