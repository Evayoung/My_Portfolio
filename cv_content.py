"""Structured CV data — Olorundare Micheal Babawale."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EducationItem:
    degree: str
    institution: str
    period: str
    note: str


@dataclass(frozen=True)
class WorkItem:
    title: str
    organisation: str
    period: str
    location: str
    bullets: tuple[str, ...]


@dataclass(frozen=True)
class Certification:
    name: str
    issuer: str
    year: str
    credential_url: str = ""


@dataclass(frozen=True)
class ToolCategory:
    label: str
    tools: tuple[str, ...]


# ── Education ─────────────────────────────────────────────────────────────────

EDUCATION = (
    EducationItem(
        "BSc. Statistics",
        "University of Ilorin",
        "2015 – 2019",
        "Foundation in quantitative analysis, probability, and data modelling — directly applicable to AI system design.",
    ),
)

# ── Work History ──────────────────────────────────────────────────────────────

WORK_HISTORY = (
    WorkItem(
        "Full-Stack & AI Systems Architect",
        "Independent / Freelance",
        "2023 – Present",
        "Ilorin, Nigeria (Remote)",
        (
            "Designed and shipped 10+ production systems spanning web, mobile, desktop, and embedded platforms",
            "Built BackendForge — a multi-agent AI system where 18 collaborating agents autonomously scaffold FastAPI backends",
            "Developed Voice-First Learning Assistant: a 4-component cross-platform system with hybrid offline STT",
            "Architected biometric access control for UNILORIN CBT centres, reducing impersonation cases",
            "Delivered QRive SaaS — a FastAPI + Reflex platform for AI-powered business identity verification via QR codes",
            "Built TrueTag product authentication backend with blockchain token minting and geolocation fraud detection",
        ),
    ),
    WorkItem(
        "Python & Software Development Tutor",
        "SuperProf & Certmart",
        "2023 – Present",
        "Remote",
        (
            "Teaching Python, FastAPI, software architecture, and AI literacy to students across experience levels",
            "Designed tailored learning plans emphasising practical coding, system design, and real-world deployment",
            "Mentored students in building production-grade applications from first principles",
        ),
    ),
    WorkItem(
        "Backend Lead — Clinic Management System",
        "University of Ilorin",
        "2025",
        "Ilorin, Nigeria",
        (
            "Replaced paper-based clinic records with a secure digital health platform using FastAPI and PostgreSQL",
            "Implemented QR-card access system and role-based dashboards for students, doctors, pharmacists, and admin",
            "Project deployed and actively used by the university clinic system",
        ),
    ),
    WorkItem(
        "Platform Architect — Church Data Infrastructure",
        "Deeper Christian Life Ministry, Kwara State",
        "2024 – Present",
        "Ilorin, Nigeria",
        (
            "Designed and maintain a scalable data platform powering two mobile apps and a REST API across state branches",
            "Implemented custom RBAC with state, zone, and branch-level permission scopes",
            "Built attendance analytics, newcomer registration, and real-time reporting dashboards",
        ),
    ),
)

# ── Certifications ────────────────────────────────────────────────────────────

CERTIFICATIONS = (
    Certification(
        "Python for Everybody Specialisation",
        "Coursera / University of Michigan",
        "2021",
    ),
    Certification(
        "FastAPI — Full Course for Beginners",
        "freeCodeCamp",
        "2022",
    ),
    Certification(
        "AI for Everyone",
        "Coursera / DeepLearning.AI",
        "2023",
    ),
    Certification(
        "Prompt Engineering for Developers",
        "DeepLearning.AI",
        "2024",
    ),
)

# ── Tool Categories (skills grid) ─────────────────────────────────────────────

TOOLS_GRID = (
    ToolCategory("Languages",       ("Python", "SQL", "JavaScript", "Bash", "Solidity")),
    ToolCategory("Frameworks",      ("FastAPI", "FastHTML", "Faststrap", "Reflex", "KivyMD")),
    ToolCategory("Desktop / GUI",   ("PySide6", "PyQt6", "KivyMD", "Tkinter")),
    ToolCategory("AI / ML",         ("OpenAI API", "Faster-Whisper", "Piper-TTS", "LangChain", "RAG")),
    ToolCategory("Data / Infra",    ("PostgreSQL", "SQLite", "Redis", "Docker", "systemd")),
    ToolCategory("Other",           ("HTMX", "Paystack", "Blockchain / Web3", "Git / GitHub", "Linux")),
)

# ── Language proficiency ──────────────────────────────────────────────────────

LANGUAGES = (
    ("English", "Fluent", 95),
    ("Yoruba",  "Native", 100),
)

# ── Professional skills list (for CV sidebar) ─────────────────────────────────

CORE_SKILLS = (
    "AI Integration & LLM-Driven Systems",
    "Model Fine-Tuning & Prompt Engineering",
    "Full-Stack Development (Web, Mobile, Desktop)",
    "Software Architecture & System Design",
    "RESTful API Engineering (FastAPI)",
    "Distributed & Offline-First Applications",
    "Database Modelling & Optimisation (SQL/NoSQL)",
    "Authentication & Role-Based Access Control",
    "Multi-Agent AI Orchestration",
    "Biometric & Embedded System Integration",
)

COMPETENCIES = (
    "Analytical Problem-Solving",
    "Scalable Software Planning",
    "Ethical AI Design",
    "Technical Communication",
    "Team Collaboration & Mentorship",
    "Continuous Learning",
)

# ── CV Meta (for <head> of the print CV page) ─────────────────────────────────

CV_META = {
    "name":       "Olorundare Micheal Babawale",
    "role":       "Full-Stack & AI Systems Architect",
    "email":      "meshelleva@gmail.com",
    "phone":      "+2348064676590",
    "whatsapp":   "+2349029952120",
    "location":   "Ilorin, Kwara State, Nigeria",
    "github":     "https://github.com/Evayoung",
    "linkedin":   "https://linkedin.com/in/michealolorundare",
    "summary": (
        "Versatile Full-Stack & AI Systems Architect with proven expertise in designing, deploying, "
        "and optimising scalable intelligent systems across web, mobile, and distributed environments. "
        "Adept at architecting secure, modular backends with FastAPI, emphasising clean API design, "
        "reliable data flow, and extensible microservices. Deeply skilled in AI integration, model "
        "fine-tuning, and prompt engineering, with hands-on experience adapting LLMs to domain-specific "
        "use cases. Experienced in autonomous agent design including MCP experimentation. Passionate about "
        "building ethical, human-centred, and open-source technology."
    ),
}
