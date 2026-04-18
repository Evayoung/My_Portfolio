const roleTitles = ["Full-Stack Developer", "AI Systems Architect", "Backend API Engineer", "Open-Source Builder"];

function initLoader() {
  const loader = document.getElementById("page-loader");
  if (!loader) return;
  window.addEventListener("load", () => loader.classList.add("is-hidden"));
}

function initRoleMorph() {
  const node = document.getElementById("hero-role");
  if (!node) return;
  let index = 0;
  window.setInterval(() => {
    index = (index + 1) % roleTitles.length;
    node.animate([{ opacity: 1, transform: "translateY(0)" }, { opacity: 0, transform: "translateY(-10px)" }], { duration: 180, easing: "ease" }).onfinish = () => {
      node.textContent = roleTitles[index];
      node.animate([{ opacity: 0, transform: "translateY(10px)" }, { opacity: 1, transform: "translateY(0)" }], { duration: 220, easing: "ease-out" });
    };
  }, 2400);
}

function initScrollNav() {
  const nav = document.getElementById("site-nav");
  if (!nav) return;
  // Show immediately if we are already scrolled or on mobile
  const sync = () => nav.classList.toggle("is-visible", window.scrollY > 20 || window.innerWidth < 992);
  // Small delay on first load to allow the slide-in animation to play
  window.setTimeout(sync, 80);
  window.addEventListener("scroll", sync, { passive: true });
  window.addEventListener("resize", sync);
}

function initActiveNavLink() {
  // Highlight nav links that match the current page path (works for both old and Faststrap navbar)
  const path = window.location.pathname.split("/")[1] || "";
  document.querySelectorAll(".nav-link-item, .neo-nav-links a").forEach((link) => {
    const href = link.getAttribute("href") || "";
    const linkPart = href.replace(/^#/, "").replace(/^\//, "").split("/")[0];
    if (path && linkPart === path) link.classList.add("active");
  });
}

function initHtmxReveal() {
  // Re-run reveal observer after any HTMX swap
  document.addEventListener("htmx:afterSettle", () => initReveal());
}

function initReveal() {
  const nodes = document.querySelectorAll(".reveal-block");
  if (!nodes.length) return;
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) entry.target.classList.add("is-visible");
    });
  }, { threshold: 0.15 });
  nodes.forEach((node) => observer.observe(node));
}

function initHeroMotion() {
  const particles = document.getElementById("hero-particles");
  const tilt = document.querySelector(".tilt-card");
  if (!particles && !tilt) return;
  window.addEventListener("pointermove", (event) => {
    const x = `${(event.clientX / window.innerWidth) * 100}%`;
    const y = `${(event.clientY / window.innerHeight) * 100}%`;
    if (particles) {
      particles.style.setProperty("--px", x);
      particles.style.setProperty("--py", y);
    }
    if (tilt) {
      const dx = (event.clientX / window.innerWidth - 0.5) * 10;
      const dy = (event.clientY / window.innerHeight - 0.5) * -10;
      tilt.style.transform = `rotateX(${dy}deg) rotateY(${dx}deg)`;
    }
  });
  if (tilt) {
    window.addEventListener("pointerleave", () => {
      tilt.style.transform = "rotateX(0deg) rotateY(0deg)";
    });
  }
}

function initDownloadTracking() {
  const progress = document.getElementById("download-progress-bar");
  document.querySelectorAll("[data-download-format]").forEach((link) => {
    link.addEventListener("click", () => {
      const format = link.getAttribute("data-download-format");
      if (progress) {
        progress.classList.remove("is-running");
        requestAnimationFrame(() => progress.classList.add("is-running"));
        window.setTimeout(() => progress.classList.remove("is-running"), 900);
      }
      fetch("/api/download-track", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: new URLSearchParams({ format }),
      })
        .then((response) => response.text())
        .then((html) => {
          const target = document.getElementById("download-metrics");
          if (target) target.outerHTML = html;
        })
        .catch(() => undefined);
    });
  });
}

initLoader();
initRoleMorph();
initScrollNav();
initActiveNavLink();
initReveal();
initHeroMotion();
initDownloadTracking();
initHtmxReveal();
