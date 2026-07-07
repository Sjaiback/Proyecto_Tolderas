(function () {
  "use strict";

  const data = window.__BRAND__ || {};
  const $ = (sel, scope) => (scope || document).querySelector(sel);
  const $$ = (sel, scope) => Array.from((scope || document).querySelectorAll(sel));
  const fineHover = matchMedia("(hover: hover) and (pointer: fine)").matches;

  function safe(fn, name) {
    try { fn(); } catch (error) { console.warn("[" + name + "]", error); }
  }

  function initSplash() {
    const splash = $("[data-splash]");
    if (!splash) return;
    const hide = () => splash.classList.add("is-out");
    if (document.readyState === "complete") setTimeout(hide, 500);
    else window.addEventListener("load", () => setTimeout(hide, 450), { once: true });
    setTimeout(hide, 4000);
  }

  function initHeader() {
    const header = $("[data-header]");
    const toggle = $("[data-menu-toggle]");
    const nav = $("[data-nav]");
    if (!header) return;
    const sync = () => header.classList.toggle("is-scrolled", scrollY > 20);
    sync();
    window.addEventListener("scroll", sync, { passive: true });
    if (toggle) {
      toggle.addEventListener("click", () => {
        const open = header.classList.toggle("is-open");
        toggle.setAttribute("aria-label", open ? "Cerrar menu" : "Abrir menu");
      });
    }
    if (nav) {
      nav.addEventListener("click", (event) => {
        if (event.target.closest("a")) header.classList.remove("is-open");
      });
    }
  }

  function initSmoothAnchors() {
    document.addEventListener("click", (event) => {
      const link = event.target.closest('a[href^="#"]');
      if (!link) return;
      const id = link.getAttribute("href");
      if (!id || id === "#") return;
      const target = $(id);
      if (!target) return;
      event.preventDefault();
      window.scrollTo({
        top: target.getBoundingClientRect().top + scrollY - 74,
        behavior: matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth"
      });
    });
  }

  function initReveals() {
    const items = $$(".reveal");
    if (!items.length) return;
    if (!("IntersectionObserver" in window)) {
      items.forEach((item) => item.classList.add("is-revealed"));
      return;
    }
    const io = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add("is-revealed");
        io.unobserve(entry.target);
      });
    }, { threshold: 0.03, rootMargin: "0px 0px -2% 0px" });
    items.forEach((item) => io.observe(item));
    setTimeout(() => {
      items.forEach((item) => {
        if (!item.classList.contains("is-revealed") && item.getBoundingClientRect().top < innerHeight) {
          item.classList.add("is-revealed");
        }
      });
    }, 6000);
  }

  function initTilt() {
    if (!fineHover) return;
    $$(".tilt-card").forEach((card) => {
      if (card.dataset.tiltBound) return;
      card.dataset.tiltBound = "1";
      card.addEventListener("mousemove", (event) => {
        const rect = card.getBoundingClientRect();
        const x = (event.clientX - rect.left) / rect.width - .5;
        const y = (event.clientY - rect.top) / rect.height - .5;
        card.style.transform = "rotateX(" + (-y * 6).toFixed(2) + "deg) rotateY(" + (x * 7).toFixed(2) + "deg) translateY(-4px)";
      });
      card.addEventListener("mouseleave", () => {
        card.style.transform = "";
      });
    });
  }

  function initTracking() {
    const form = $("[data-track-form]");
    const result = $("[data-track-result]");
    if (!form || !result) return;
    form.addEventListener("submit", (event) => {
      event.preventDefault();
      const input = $("#codigo", form);
      const code = (input && input.value ? input.value : "").trim().toUpperCase();
      result.animate([{ opacity: .25, transform: "translateY(8px)" }, { opacity: 1, transform: "none" }], {
        duration: 320,
        easing: "cubic-bezier(.16,1,.3,1)"
      });
      const kicker = $(".result-kicker", result);
      if (kicker) kicker.textContent = code === data.sampleOrder.code ? "Pedido " + code : "Codigo de demo: ER-2407";
    });
  }

  function initTabs() {
    const shell = $(".app-shell");
    if (!shell) return;
    const buttons = $$("[data-tab]", shell);
    const panels = $$("[data-panel]", shell);
    buttons.forEach((button) => {
      button.addEventListener("click", () => {
        const id = button.getAttribute("data-tab");
        buttons.forEach((item) => item.classList.toggle("active", item === button));
        panels.forEach((panel) => panel.classList.toggle("is-active", panel.getAttribute("data-panel") === id));
      });
    });
  }

  function initHeroMotion() {
    const stage = $(".fabric-stage");
    if (!stage || !fineHover) return;
    window.addEventListener("mousemove", (event) => {
      const x = (event.clientX / innerWidth - .5) * 18;
      const y = (event.clientY / innerHeight - .5) * 18;
      stage.style.transform = "translate3d(" + x.toFixed(1) + "px," + y.toFixed(1) + "px,0)";
    }, { passive: true });
  }

  function initStarGallery() {
    const gallery = $("[data-star-gallery]");
    if (!gallery) return;
    const stage = $(".gallery-stage", gallery);
    const cards = $$("[data-gallery-card]", gallery);
    const prev = $("[data-gallery-prev]", gallery);
    const next = $("[data-gallery-next]", gallery);
    if (!stage || cards.length < 2) return;

    const mobile = matchMedia("(max-width: 719px)");
    let rotation = 0;
    let raf = 0;
    let lastTick = performance.now();
    const angle = 360 / cards.length;

    function radius() {
      return Math.min(560, Math.max(320, gallery.clientWidth * .42));
    }

    function render() {
      if (mobile.matches) return;
      stage.style.transform = "rotateY(" + rotation.toFixed(2) + "deg)";
      cards.forEach((card, index) => {
        const itemAngle = index * angle;
        const relative = (itemAngle + rotation + 360) % 360;
        const normalized = Math.abs(relative > 180 ? 360 - relative : relative);
        const opacity = Math.max(.28, 1 - normalized / 170);
        card.style.transform = "translate(-50%, -50%) rotateY(" + itemAngle + "deg) translateZ(" + radius() + "px)";
        card.style.opacity = opacity.toFixed(2);
        card.style.filter = normalized > 95 ? "saturate(.72) brightness(.72)" : "";
      });
    }

    function tick(now) {
      const delta = now - lastTick;
      lastTick = now;
      rotation += delta * .006;
      render();
      raf = requestAnimationFrame(tick);
    }

    function step(direction) {
      rotation += angle * direction;
      render();
    }

    function syncMode() {
      cancelAnimationFrame(raf);
      if (mobile.matches) {
        stage.style.transform = "";
        cards.forEach((card) => {
          card.style.transform = "";
          card.style.opacity = "";
          card.style.filter = "";
        });
        return;
      }
      lastTick = performance.now();
      render();
      raf = requestAnimationFrame(tick);
    }

    if (prev) prev.addEventListener("click", () => step(1));
    if (next) next.addEventListener("click", () => step(-1));
    mobile.addEventListener("change", syncMode);
    window.addEventListener("resize", render, { passive: true });
    syncMode();
  }

  function boot() {
    safe(initSplash, "initSplash");
    safe(initHeader, "initHeader");
    safe(initSmoothAnchors, "initSmoothAnchors");
    safe(initReveals, "initReveals");
    safe(initTilt, "initTilt");
    safe(initTracking, "initTracking");
    safe(initTabs, "initTabs");
    safe(initHeroMotion, "initHeroMotion");
    safe(initStarGallery, "initStarGallery");
    document.documentElement.classList.add("is-ready");
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot, { once: true });
  } else {
    boot();
  }
})();
