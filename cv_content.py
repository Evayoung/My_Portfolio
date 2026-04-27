"""Structured CV data for NeoPortfolio."""

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


EDUCATION = (
    EducationItem(
        "BSc. Statistics",
        "University of Ilorin",
        "2015 - 2019",
        "Built a strong foundation in quantitative analysis, probability, and data modelling that now informs systems thinking, AI evaluation, and backend architecture decisions.",
    ),
)


WORK_HISTORY = (
    WorkItem(
        "Full-Stack & AI Systems Architect",
        "Independent / Freelance",
        "2023 - Present",
        "Ilorin, Nigeria (Remote)",
        (
            "Designed and delivered 10+ production systems spanning web, mobile, desktop, and embedded environments.",
            "Built BackendForge, a multi-agent AI orchestration system where 18 specialised agents collaboratively scaffold FastAPI backends from natural-language specifications.",
            "Developed the Voice-First Learning Assistant, a four-part accessibility platform with hybrid offline speech recognition for low-connectivity classroom use.",
            "Architected biometric access control for UNILORIN CBT centres, helping reduce impersonation risk and streamline candidate verification.",
            "Delivered QRive, a FastAPI + Reflex SaaS platform for AI-assisted business identity verification through secure QR workflows.",
            "Built the TrueTag authentication backend with blockchain token minting and geolocation-aware fraud detection for product verification.",
        ),
    ),
    WorkItem(
        "Backend Lead - Clinic Management System",
        "University of Ilorin",
        "2025",
        "Ilorin, Nigeria",
        (
            "Led backend delivery for a secure digital clinic platform that replaced paper-based medical records with a FastAPI + PostgreSQL workflow.",
            "Implemented QR-card access and role-based dashboards for students, doctors, pharmacists, and administrators.",
            "Supported a production deployment used by the university clinic to improve record access and operational visibility.",
        ),
    ),
    WorkItem(
        "Platform Architect - Church Data Infrastructure",
        "Deeper Christian Life Ministry, Kwara State",
        "2024 - Present",
        "Ilorin, Nigeria",
        (
            "Designed and maintain a scalable data platform powering two mobile applications and a shared REST API across state branches.",
            "Implemented custom RBAC with state, zone, and branch-level permission scopes to support distributed governance safely.",
            "Built attendance analytics, newcomer registration flows, and real-time reporting dashboards for operational oversight.",
        ),
    ),
    WorkItem(
        "Python & Software Development Tutor",
        "SuperProf & Certmart",
        "2023 - Present",
        "Remote",
        (
            "Teach Python, FastAPI, software architecture, and AI literacy to learners across beginner to intermediate levels.",
            "Design tailored learning plans that emphasise practical coding, system design, and real-world deployment habits.",
            "Mentor students as they move from first principles into building complete, production-oriented applications.",
        ),
    ),
)


CERTIFICATIONS = (
    Certification(
        "Prompt Engineering for Developers",
        "DeepLearning.AI",
        "2024",
    ),
    Certification(
        "AI for Everyone",
        "Coursera / DeepLearning.AI",
        "2023",
    ),
    Certification(
        "FastAPI - Full Course for Beginners",
        "freeCodeCamp",
        "2022",
    ),
    Certification(
        "Python for Everybody Specialisation",
        "Coursera / University of Michigan",
        "2021",
    ),
)


TOOLS_GRID = (
    ToolCategory("Languages", ("Python", "SQL", "JavaScript", "Bash", "Solidity")),
    ToolCategory("Frameworks", ("FastAPI", "FastHTML", "Faststrap", "Reflex", "KivyMD")),
    ToolCategory("Desktop / GUI", ("PySide6", "PyQt6", "KivyMD", "Tkinter")),
    ToolCategory("AI / ML", ("OpenAI API", "Faster-Whisper", "Piper-TTS", "LangChain", "RAG")),
    ToolCategory("Data / Infra", ("PostgreSQL", "SQLite", "Redis", "Docker", "systemd")),
    ToolCategory("Other", ("HTMX", "Paystack", "Blockchain / Web3", "Git / GitHub", "Linux")),
)


LANGUAGES = (
    ("English", "Fluent", 95),
    ("Yoruba", "Native", 100),
)


CORE_SKILLS = (
    "AI integration and LLM-powered product workflows",
    "Prompt engineering and model adaptation",
    "Full-stack product development across web, mobile, and desktop",
    "Software architecture and modular system design",
    "REST API engineering with FastAPI",
    "Offline-first and distributed application design",
    "Database modelling and query optimisation",
    "Authentication, RBAC, and secure backend design",
    "Multi-agent orchestration and automation systems",
    "Biometric, device, and embedded-system integration",
)


COMPETENCIES = (
    "Analytical Problem-Solving",
    "Scalable Software Planning",
    "Ethical AI Design",
    "Technical Communication",
    "Team Collaboration & Mentorship",
    "Continuous Learning",
)


CV_META = {
    "name": "Olorundare Micheal Babawale",
    "role": "Full-Stack & AI Systems Architect",
    "email": "meshelleva@gmail.com",
    "phone": "+2348064676590",
    "whatsapp": "+2349029952120",
    "location": "Ilorin, Kwara State, Nigeria",
    "github": "https://github.com/Evayoung",
    "linkedin": "https://linkedin.com/in/michealolorundare",
    "summary": (
        "Full-Stack and AI Systems Architect focused on designing practical, production-ready software across "
        "web, mobile, desktop, and distributed environments. Strong in FastAPI backend engineering, modular "
        "system design, data modelling, and AI integration, with hands-on experience building multi-agent "
        "automation, offline-first accessibility tools, biometric platforms, and operational data systems. "
        "Known for translating complex product ideas into reliable technical architecture with a clear focus "
        "on usability, maintainability, and real-world deployment."
    ),
}
