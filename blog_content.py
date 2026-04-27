"""Blog post content — real articles by Olorundare Micheal Babawale."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BlogPost:
    slug: str
    title: str
    category: str          # "tutorial" | "opinion" | "project" | "deep-dive"
    summary: str
    content_html: str
    published: str         # "YYYY-MM-DD"
    read_minutes: int
    tags: tuple[str, ...]
    image: str = "/assets/images/hero-bg.jpg"


BLOG_CATEGORIES = (
    ("all",       "All"),
    ("project",   "Projects"),
    ("tutorial",  "Tutorials"),
    ("opinion",   "Opinion"),
    ("deep-dive", "Deep Dive"),
)

BLOG_POSTS = (

    BlogPost(
        slug="backendforge-multi-agent-fastapi",
        title="BackendForge: What Happens When 18 AI Agents Write Your FastAPI Backend",
        category="project",
        summary=(
            "I built a system where 18 specialised AI agents collaborate to design, code, "
            "document, and validate a FastAPI backend from a plain English specification. "
            "Here's what I learned."
        ),
        published="2025-11-10",
        read_minutes=8,
        tags=("FastAPI", "AI Agents", "Multi-Agent", "Automation", "Python"),
        image="/assets/images/hero-bg.jpg",
        content_html="""
<p>The question that started BackendForge was simple: <em>what if writing a backend was a management problem, not a coding problem?</em> Instead of sitting down and writing routes, schemas, and auth logic myself, what if I directed a team of AI agents — each with a clear specialisation — and let them build it?</p>

<h2>The Architecture</h2>
<p>BackendForge uses 18 collaborating agents, each assigned a single role:</p>
<ul>
  <li><strong>Schema Agent</strong> — designs Pydantic models from a product spec</li>
  <li><strong>Route Agent</strong> — generates CRUD and custom route handlers</li>
  <li><strong>Auth Agent</strong> — implements JWT auth, password hashing, and RBAC</li>
  <li><strong>Doc Agent</strong> — writes OpenAPI descriptions and README sections</li>
  <li><strong>Validation Agent</strong> — runs the generated code and reports errors</li>
  <li>…and 13 more, each owning a narrow domain</li>
</ul>
<p>An orchestration layer manages the task graph: each agent receives the output of the previous one, adds its contribution, and passes the updated package forward. The Validation Agent runs at the end and sends failures back to the relevant agent for self-correction.</p>

<h2>What Actually Works</h2>
<p>The schema and route generation are genuinely impressive. Given a spec like <em>"a multi-tenant SaaS with users, organisations, and subscription tiers"</em>, the Schema Agent produces correct, typed Pydantic models in seconds. The Route Agent follows correctly with matching CRUD endpoints.</p>
<p>The Auth Agent is more reliable than I expected — it consistently implements bcrypt hashing and JWT with expiry correctly.</p>

<h2>What Doesn't Work Yet</h2>
<p>Complex business logic is still fragile. The agents handle structure well but struggle with non-standard validation rules that require domain reasoning. This is where a human architect still needs to step in.</p>
<p>Test generation is also weak — the Test Agent produces coverage-superficial tests that pass without actually validating behaviour.</p>

<h2>Why It Matters</h2>
<p>BackendForge is not trying to replace backend engineers. It's trying to eliminate the <em>tedious scaffolding</em> — the boilerplate that burns the first 40% of every project's time budget. If a junior developer can generate a structurally correct, documented FastAPI starting point in 10 minutes instead of 3 days, that changes what's possible.</p>
<p>The project is ongoing. The next milestone is giving the orchestration layer memory so agents can negotiate decisions rather than just passing a document forward.</p>

<blockquote>
  <p>The future of backend development isn't AI writing code. It's AI handling structure so humans can focus on the decisions that actually require judgement.</p>
</blockquote>
""",
    ),

    BlogPost(
        slug="voice-first-offline-nigeria",
        title="Building Offline-First AI for Nigerian Classrooms: What No One Tells You",
        category="deep-dive",
        summary=(
            "The Voice-First Learning Assistant taught me more about real-world AI constraints "
            "than any online course. Here's how we built a system that still works when the "
            "internet disappears — which in Nigeria, is often."
        ),
        published="2025-10-15",
        read_minutes=10,
        tags=("FastAPI", "KivyMD", "Offline-First", "AI", "Accessibility", "Nigeria"),
        image="/assets/images/hero-bg2.jpg",
        content_html="""
<p>The brief for the Voice-First Learning Assistant was clear: build a system that delivers personalised, voice-driven educational content to visually impaired students in Nigeria. What wasn't in the brief — because nobody thinks to write it down — is that Nigerian classrooms have unreliable power, intermittent internet, and ambient noise that would defeat most commercial speech recognition systems.</p>

<h2>The Hybrid Architecture Decision</h2>
<p>Early prototypes used the Google Cloud Speech-to-Text API exclusively. They worked fine in demo conditions. They failed completely during a school visit where the wifi cut out for 40 minutes. We needed a fallback.</p>
<p>The final system uses a two-tier STT architecture:</p>
<ul>
  <li><strong>Primary</strong>: Google Cloud Speech-to-Text (en-NG locale) — highest accuracy when online</li>
  <li><strong>Fallback</strong>: Faster-Whisper running locally on-device — slower but network-independent</li>
</ul>
<p>The client detects connectivity and routes automatically. Accuracy dropped from 97% to 91% in offline mode. For a student whose alternative is no access at all, that's acceptable.</p>

<h2>The Nigerian Accent Problem</h2>
<p>Generic English STT models are trained on American and British speech. Nigerian English has distinct prosody, vowel shifts, and code-switching patterns. The first test with a standard model produced transcription errors on approximately 30% of student utterances.</p>
<p>Selecting Google's <code>en-NG</code> locale was the single biggest accuracy improvement — jumping from 70% to 94% accuracy on our test corpus of student speech. The Faster-Whisper model was fine-tuned on a small dataset of Nigerian-accented educational phrases to close the remaining gap.</p>

<h2>Non-Blocking TTS: The Listening Loop Problem</h2>
<p>Early versions had a subtle but severe bug: the TTS engine spoke to the student, and the microphone picked up the system's own voice as student input. The VAD (Voice Activity Detection) would then try to transcribe what the system just said — and respond to itself.</p>
<p>The fix was implementing non-blocking TTS via Python background threading. The microphone is gated during TTS playback and reopened when the audio stream completes. Combined with a configurable VAD sensitivity tuner, false triggers dropped to under 2% in field tests.</p>

<h2>Lessons for Offline-First AI Builders</h2>
<ol>
  <li>Design for your worst connectivity scenario first, not your best</li>
  <li>Use locale-specific models — generic models are built for someone else's users</li>
  <li>Background thread your audio I/O or you will create infinite loops</li>
  <li>YAML-based configuration for VAD parameters — teachers need to tune without redeploying</li>
</ol>
<p>The system is still in active development. The next phase is adaptive content difficulty using Bayesian student modelling. But the core offline-first architecture is stable. It works in rooms with no signal, 40-degree heat, and a classroom full of talking children. That's the real benchmark.</p>
""",
    ),

    BlogPost(
        slug="fasthtml-faststrap-real-experience",
        title="FastHTML + Faststrap: The Python Full-Stack I've Been Building For",
        category="opinion",
        summary=(
            "After years of React, Next.js, and JavaScript toolchains, I switched to FastHTML + "
            "Faststrap for my full-stack projects. This is my honest assessment after building "
            "multiple production apps with it."
        ),
        published="2025-09-20",
        read_minutes=7,
        tags=("FastHTML", "Faststrap", "Python", "Full-Stack", "HTMX"),
        image="/assets/images/hero-bg3.jpg",
        content_html="""
<p>For the first few years of my career, my full-stack stack was React on the frontend and FastAPI on the backend. It worked. It also meant maintaining two codebases in two languages, managing cross-origin auth, serialising data twice, and keeping TypeScript types in sync with Python Pydantic models.</p>
<p>When I found FastHTML, I was sceptical. A Python web framework that generates HTML components? That sounded like early 2000s PHP cgi-bin energy.</p>
<p>I was wrong.</p>

<h2>What FastHTML Actually Is</h2>
<p>FastHTML is not a template engine. It's a component framework where Python objects <em>are</em> the HTML. There's no template syntax to learn, no context processors, no Jinja2 escaping edge cases. You write Python, and you get HTML — typed, composable, and testable.</p>
<p>Faststrap adds Bootstrap 5 component abstractions on top: <code>Button()</code>, <code>Card()</code>, <code>Row()</code>, <code>Col()</code>, <code>Icon()</code> — all returning proper FastHTML elements with Bootstrap classes applied. It also includes SEO helpers, theme management, toggle groups, and effect utilities.</p>

<h2>The HTMX Advantage</h2>
<p>HTMX fills the gap that used to require React: partial page updates, out-of-band swaps, inline form submissions, polling. Combined with FastHTML's server-side rendering, the result is an interactive UI with no JavaScript framework — just HTML attributes that trigger HTTP requests.</p>
<p>For the Student EWS project (an academic monitoring system I built recently), the inline score entry works entirely via HTMX: click a cell, it becomes an input, blur saves the score, triggers a full recompute chain (GPA → risk → alerts), and swaps four separate DOM elements via OOB (out-of-band) updates. Zero JavaScript written.</p>

<h2>Where It Wins</h2>
<ul>
  <li><strong>No context switching</strong> — backend and frontend in one Python process</li>
  <li><strong>Vercel-ready</strong> — stateless ASGI, deploys cleanly</li>
  <li><strong>Composability</strong> — components are just Python functions, so testing is trivial</li>
  <li><strong>Faststrap's SEO module</strong> — <code>SEO()</code>, <code>PageMeta()</code>, <code>StructuredData()</code> out of the box</li>
</ul>

<h2>Where It Needs Work</h2>
<ul>
  <li>The ecosystem is small — fewer ready-made component libraries than React</li>
  <li>Complex client-side state (drag and drop, canvas, realtime collaboration) still needs JavaScript</li>
  <li>Debugging rendered HTML can be noisy when component trees are deep</li>
</ul>

<h2>My Verdict</h2>
<p>For Python developers building information-dense, server-rendered applications — dashboards, portals, SaaS products, data platforms — FastHTML + Faststrap is the most productive stack I've used. The code-to-working-product ratio is the best I've experienced in 5 years of professional development.</p>
<p>I'm building everything new with it, and I'm not going back.</p>
""",
    ),

    BlogPost(
        slug="steganography-aes-dct-lsb",
        title="AES-256 + DCT-LSB: Building Real Steganography That Actually Holds Up",
        category="deep-dive",
        summary=(
            "The Stego project was my final-year defence — and it taught me more about "
            "cryptography, signal processing, and the gap between academic security and "
            "production-grade security than anything else I've built."
        ),
        published="2025-08-05",
        read_minutes=9,
        tags=("Steganography", "AES-256", "DCT", "LSB", "PySide6", "Python", "Security"),
        image="/assets/images/hero-bg4.jpg",
        content_html="""
<p>Steganography — hiding data inside other data — sounds like a spy movie concept. But secure document embedding has real practical applications: whistleblower protection, watermarking, chain-of-custody verification for sensitive files. The Stego project was my final-year defence, but I built it as if it were going into production.</p>

<h2>Why a Hybrid DCT-LSB Approach?</h2>
<p>Pure LSB (Least Significant Bit) steganography is the simplest approach: replace the last bit of each pixel's colour value with a bit from your secret payload. It's nearly invisible, but it's also fragile — lossless compression and image reprocessing will destroy your hidden data.</p>
<p>DCT (Discrete Cosine Transform) domain steganography works differently: it embeds data in the frequency coefficients of an image, the same domain JPEG compression operates in. This makes the hidden data more resilient to compression, but at higher visual cost.</p>
<p>The hybrid approach I implemented works in two stages:</p>
<ol>
  <li>DCT embedding for the encryption key metadata and file header</li>
  <li>LSB embedding for the actual payload (using the DCT-embedded key for addressing)</li>
</ol>
<p>This gives the system JPEG resilience for the critical routing information while maintaining high payload capacity for the actual content.</p>

<h2>The AES-256 Layer</h2>
<p>The payload is encrypted with AES-256 in CBC mode before embedding. The key is derived from a user passphrase using PBKDF2 with a random salt. The salt is embedded in the image header using the DCT layer.</p>
<p>This means even if steganographic analysis detects that an image carries hidden data, decrypting it without the passphrase is computationally infeasible.</p>

<h2>The PySide6 Interface</h2>
<p>The GUI was built with PySide6 for cross-platform desktop operation. The interface has two modes:</p>
<ul>
  <li><strong>Embed mode</strong> — select a carrier image, select a file to hide, enter a passphrase, output is a modified image visually identical to the original</li>
  <li><strong>Extract mode</strong> — select a modified image, enter the passphrase, recover the original file</li>
</ul>
<p>The capacity indicator calculates how many bytes the carrier image can hold and warns the user if the payload is too large before they start the embedding process.</p>

<h2>What the Defence Panel Said</h2>
<p>The panel was most interested in the hybrid architecture decision — specifically why I chose to split the payload between DCT and LSB layers rather than using one approach consistently. The answer: because real-world images get reprocessed, shared on WhatsApp (which recompresses), printed and scanned. The critical routing data needed to survive that. The payload data just needed to survive the first transmission.</p>
<p>The project was awarded a distinction. More importantly, the system actually worked under conditions specifically designed to defeat it — compression, resampling, and colour space conversion.</p>

<blockquote>
  <p>Security systems should be designed for adversarial conditions, not optimal ones. That's the only test that matters.</p>
</blockquote>
""",
    ),
)

# ── Helpers ───────────────────────────────────────────────────────────────────
