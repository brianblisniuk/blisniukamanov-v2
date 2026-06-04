(function () {
  "use strict";

  /* ==========================================================
     CMS — load site settings and replace marked elements
     Runtime swap so editing content/site-settings.json from
     the Decap panel updates phone, email, hours, etc.
     ========================================================== */
  function applySiteSettings(s) {
    // data-cms="key" → replace textContent
    document.querySelectorAll("[data-cms]").forEach((el) => {
      const k = el.dataset.cms;
      if (s[k] != null) el.textContent = s[k];
    });
    // data-cms-href="key" → set href to the value (used for full URLs like maps)
    document.querySelectorAll("[data-cms-href]").forEach((el) => {
      const k = el.dataset.cmsHref;
      if (s[k] != null) el.setAttribute("href", s[k]);
    });
    // data-cms-tel="key" → href = "tel:" + value
    document.querySelectorAll("[data-cms-tel]").forEach((el) => {
      const k = el.dataset.cmsTel;
      if (s[k] != null) el.setAttribute("href", "tel:" + s[k]);
    });
    // data-cms-mailto="key" → href = "mailto:" + value
    document.querySelectorAll("[data-cms-mailto]").forEach((el) => {
      const k = el.dataset.cmsMailto;
      if (s[k] != null) el.setAttribute("href", "mailto:" + s[k]);
    });
    // Special: WhatsApp FAB
    const wa = document.getElementById("waButton");
    if (wa && s.whatsapp) {
      const greeting = s.whatsapp_greeting || "Hola.";
      wa.href = "https://onnqcdjkvpvpvtsorpup.supabase.co/functions/v1/go?to=wa&c=sitio&src=fab";
    }
  }
  fetch("content/site-settings.json", { cache: "no-store" })
    .then((r) => (r.ok ? r.json() : null))
    .then((s) => { if (s) applySiteSettings(s); })
    .catch(() => {});

  /* ==========================================================
     Floating action stack: WhatsApp + "Speak to expert" pill
     Both injected once site-wide
     ========================================================== */
  if (!document.getElementById("fabStack")) {
    const stack = document.createElement("div");
    stack.id = "fabStack";
    stack.className = "fab-stack";

    // "Hablá con un experto" pill (opens modal)
    const expert = document.createElement("button");
    expert.type = "button";
    expert.className = "expert-fab js-expert-trigger";
    expert.setAttribute("aria-haspopup", "dialog");
    expert.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/></svg><span>Hablá con un experto</span>';
    stack.appendChild(expert);

    // WhatsApp circular FAB
    const wa = document.createElement("a");
    wa.id = "waButton";
    wa.className = "whatsapp-fab";
    wa.href = "https://onnqcdjkvpvpvtsorpup.supabase.co/functions/v1/go?to=wa&c=sitio&src=fab";
    wa.target = "_blank";
    wa.rel = "noopener";
    wa.setAttribute("aria-label", "Chatear por WhatsApp");
    wa.innerHTML = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M17.5 14.4c-.3-.1-1.7-.8-2-.9-.3-.1-.5-.1-.7.1-.2.3-.8.9-1 1.1-.2.2-.4.2-.7.1-.3-.1-1.2-.5-2.4-1.5-.9-.8-1.5-1.7-1.7-2-.2-.3 0-.5.1-.6.1-.1.3-.4.4-.5.1-.2.2-.3.3-.5.1-.2 0-.4 0-.5-.1-.1-.7-1.6-.9-2.2-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.7.4-.2.3-.9.9-.9 2.2 0 1.3.9 2.5 1.1 2.7.1.2 1.9 2.9 4.6 4 .6.3 1.1.4 1.5.6.6.2 1.2.2 1.6.1.5-.1 1.7-.7 1.9-1.4.2-.7.2-1.3.2-1.4-.1-.1-.3-.2-.6-.3zM12 2C6.5 2 2 6.5 2 12c0 1.8.5 3.5 1.4 5L2 22l5.2-1.4c1.5.8 3.1 1.3 4.8 1.3 5.5 0 10-4.5 10-10S17.5 2 12 2zm0 18c-1.6 0-3.1-.4-4.4-1.2l-.3-.2-3.2.9.9-3.1-.2-.3C3.9 14.9 3.5 13.5 3.5 12c0-4.7 3.8-8.5 8.5-8.5s8.5 3.8 8.5 8.5-3.8 8.5-8.5 8.5z"/></svg>';
    stack.appendChild(wa);

    document.body.appendChild(stack);
  }

  /* ==========================================================
     "Hablá con un experto" modal — injected once
     ========================================================== */
  function ctxFromPage() {
    // Detect region/country from the page context
    const path = location.pathname.toLowerCase();
    if (path.includes("europe")) return { region: "Europa", country: "" };
    if (path.includes("piamonte"))      return { region: "Europa",       country: "Italia" };
    if (path.includes("croacia"))       return { region: "Mediterráneo", country: "Croacia" };
    if (path.includes("uzbekistan"))    return { region: "Asia Central", country: "Uzbekistán" };
    if (path.includes("namibia"))       return { region: "África",       country: "Namibia" };
    if (path.includes("laponia"))       return { region: "Ártico",       country: "Finlandia y Noruega" };
    if (path.includes("bahia"))         return { region: "Sudamérica",   country: "Brasil" };
    if (path.includes("japon-mono"))    return { region: "Asia",         country: "Japón" };
    if (path.includes("butan"))         return { region: "Himalaya",     country: "Bután y Nepal" };
    if (path.includes("marruecos"))     return { region: "Norte de África", country: "Marruecos" };
    if (path.includes("alaska"))        return { region: "Norteamérica", country: "Alaska" };
    if (path.includes("small-group")) return { region: "", country: "" };
    return { region: "", country: "" };
  }

  if (!document.getElementById("expertModal")) {
    const ctx = ctxFromPage();
    const ctxLabel = ctx.region ? "Consultar sobre " + ctx.region : "Hablá con un experto";

    const wrap = document.createElement("div");
    wrap.id = "expertModal";
    wrap.className = "modal-wrap";
    wrap.setAttribute("aria-hidden", "true");
    wrap.setAttribute("role", "dialog");
    wrap.setAttribute("aria-labelledby", "expertModalTitle");
    wrap.innerHTML = `
      <div class="modal-backdrop" data-close></div>
      <div class="modal-card">
        <button class="modal-close" data-close aria-label="Cerrar">×</button>
        <h2 id="expertModalTitle" class="modal-title">${ctxLabel}</h2>

        <form name="consulta-experto" method="POST" action="/gracias.html" class="modal-form">
          <p class="hidden-field"><label>No completar: <input name="bot-field" /></label></p>
          <input type="hidden" name="contexto" value="${location.pathname}" />
          <input type="hidden" name="intent" value="consulta" />
          <input type="hidden" name="salida" value="" />
          <input type="hidden" name="viaje" value="${ctx.country}" />

          <label class="field">
            <span>Tu nombre</span>
            <input type="text" name="nombre" required placeholder="Nombre y apellido" />
          </label>
          <label class="field">
            <span>Tu email</span>
            <input type="email" name="email" required placeholder="vos@email.com" />
          </label>
          <label class="field">
            <span>Teléfono (opcional)</span>
            <input type="tel" name="telefono" placeholder="+54 9 11 …" />
          </label>

          <fieldset class="radios m-radios">
            <legend>¿Sos asesor de viajes?</legend>
            <label><input type="radio" name="asesor" value="si" /> Sí</label>
            <label><input type="radio" name="asesor" value="no" checked /> No</label>
          </fieldset>

          <label class="field">
            <span>Elegí una región</span>
            <select name="region" required>
              <option value="">Seleccionar región</option>
              <option ${ctx.region==='África'?'selected':''}>África</option>
              <option ${ctx.region==='Asia'?'selected':''}>Asia</option>
              <option ${ctx.region==='Europa'?'selected':''}>Europa</option>
              <option ${ctx.region==='Sudamérica'?'selected':''}>Sudamérica</option>
              <option ${ctx.region==='Norteamérica'?'selected':''}>Norteamérica</option>
              <option ${ctx.region==='Oceanía'?'selected':''}>Oceanía</option>
              <option ${ctx.region==='Antártida y polos'?'selected':''}>Antártida y polos</option>
              <option ${ctx.region==='Oriente Próximo y Norte de África'?'selected':''}>Oriente Próximo y Norte de África</option>
              <option ${ctx.region==='Caribe'?'selected':''}>Caribe</option>
              <option>Aún no lo sé</option>
            </select>
          </label>

          <label class="field">
            <span>Elegí un país</span>
            <input type="text" name="pais" placeholder="Cualquiera" value="${ctx.country}" />
          </label>

          <label class="field">
            <span>Contanos sobre tu viaje ideal</span>
            <textarea name="mensaje" rows="4" placeholder="Fechas tentativas, intereses, viajeros…"></textarea>
          </label>

          <label class="check"><input type="checkbox" name="acepta_privacidad" value="si" required /> Acepto la <a href="privacidad.html" target="_blank">política de privacidad</a></label>
          <label class="check"><input type="checkbox" name="acepta_news" value="si" /> Quiero recibir novedades y otra información de Blisniuk &amp; Amanov</label>

          <button type="submit" class="btn btn-laurel modal-submit">Hablar con un experto</button>

          <p class="modal-legal">Al enviar este formulario nos autorizás a que te contactemos con respecto a esta consulta. Tus datos no se comparten con terceros. Podés darte de baja en cualquier momento.</p>
        </form>
      </div>
    `;
    document.body.appendChild(wrap);

    const fSalida = wrap.querySelector('[name="salida"]');
    const fIntent = wrap.querySelector('[name="intent"]');
    const fMensaje = wrap.querySelector('[name="mensaje"]');
    const fTitle = wrap.querySelector('#expertModalTitle');
    const open = (opts) => {
      opts = opts || {};
      if (opts.salida) {
        if (fSalida) fSalida.value = opts.salida;
        if (fIntent) fIntent.value = "reserva";
        if (fTitle) fTitle.textContent = "Reservar salida · " + opts.salida;
        if (fMensaje && !fMensaje.value) fMensaje.value = "Quiero reservar la salida del " + opts.salida + ".";
      } else {
        if (fSalida) fSalida.value = "";
        if (fIntent) fIntent.value = "consulta";
        if (fTitle) fTitle.textContent = ctxLabel;
      }
      wrap.classList.add("open");
      wrap.setAttribute("aria-hidden", "false");
      document.body.style.overflow = "hidden";
    };
    window.__openExpert = open;
    const close = () => {
      wrap.classList.remove("open");
      wrap.setAttribute("aria-hidden", "true");
      document.body.style.overflow = "";
    };

    document.addEventListener("click", (e) => {
      const trig = e.target.closest(".js-expert-trigger");
      if (trig) { e.preventDefault(); open(); return; }
      const closer = e.target.closest("[data-close]");
      if (closer && wrap.contains(closer)) { e.preventDefault(); close(); }
    });
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && wrap.classList.contains("open")) close();
    });
  }

  /* ==========================================================
     Sticky header shadow on scroll
     ========================================================== */
  const header = document.getElementById("siteHeader");
  const onScroll = () => {
    if (!header) return;
    if (window.scrollY > 8) header.classList.add("scrolled");
    else header.classList.remove("scrolled");
  };
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* ==========================================================
     Mobile drawer
     ========================================================== */
  const trigger = document.getElementById("menuTrigger");
  const drawer = document.getElementById("mobileDrawer");
  if (trigger && drawer) {
    const close = () => {
      trigger.classList.remove("open");
      drawer.classList.remove("open");
      drawer.setAttribute("aria-hidden", "true");
      document.body.style.overflow = "";
    };
    trigger.addEventListener("click", () => {
      const open = trigger.classList.toggle("open");
      drawer.classList.toggle("open", open);
      drawer.setAttribute("aria-hidden", String(!open));
      document.body.style.overflow = open ? "hidden" : "";
    });
    drawer.querySelectorAll("a").forEach((a) => a.addEventListener("click", close));
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape") close();
    });
    window.addEventListener("resize", () => { if (window.innerWidth > 800) close(); });
  }

  /* ==========================================================
     Spotlight crossfade with autoplay + manual controls.
     Each slide has a <video class="slide-media"> background.
     The text overlays live OUTSIDE the slides as siblings in
     .spotlight-content, so they always paint above any slide's
     ::before vignette. We sync the active text with the active
     slide so each rotation shows its own copy + CTA.
     ========================================================== */
  const slides = document.querySelectorAll("#spotlightFrame .slide");
  const texts = document.querySelectorAll("#spotlightFrame .spotlight-text");
  const slidePrev = document.getElementById("slidePrev");
  const slideNext = document.getElementById("slideNext");
  if (slides.length) {
    let idx = 0;
    let autoTimer;
    const playSlide = (i) => {
      const v = slides[i].querySelector("video.slide-media");
      if (!v) return;
      try { v.currentTime = 0; const p = v.play(); if (p && p.catch) p.catch(() => {}); } catch (e) {}
    };
    const pauseSlide = (i) => {
      const v = slides[i].querySelector("video.slide-media");
      if (v) { try { v.pause(); } catch (e) {} }
    };
    const go = (next) => {
      pauseSlide(idx);
      slides[idx].classList.remove("active");
      if (texts[idx]) texts[idx].classList.remove("active");
      idx = (next + slides.length) % slides.length;
      slides[idx].classList.add("active");
      if (texts[idx]) texts[idx].classList.add("active");
      playSlide(idx);
    };
    const restartAuto = () => {
      clearInterval(autoTimer);
      autoTimer = setInterval(() => go(idx + 1), 7000);
    };
    if (slidePrev) slidePrev.addEventListener("click", () => { go(idx - 1); restartAuto(); });
    if (slideNext) slideNext.addEventListener("click", () => { go(idx + 1); restartAuto(); });
    playSlide(0);
    restartAuto();
  }

  /* ==========================================================
     Tabs (homepage "Where to go" — swap visible cards)
     Also supports rec-tabs (filter tabs)
     ========================================================== */
  document.querySelectorAll(".tabs").forEach((group) => {
    const buttons = Array.from(group.querySelectorAll(".tab"));
    const panelKey = (b) => b.dataset.tab;
    const panels = Array.from(document.querySelectorAll(".tab-panel"));

    buttons.forEach((b) => b.addEventListener("click", () => {
      buttons.forEach((x) => x.classList.remove("active"));
      b.classList.add("active");
      const key = panelKey(b);
      panels.forEach((p) => {
        const match = p.dataset.panel === key;
        p.classList.toggle("active", match);
        if (match) {
          p.classList.add("just-tabbed");
          setTimeout(() => p.classList.remove("just-tabbed"), 600);
        }
      });
    }));
  });

  // Rec tabs (small-group page — visual feedback only)
  document.querySelectorAll(".rec-tabs").forEach((group) => {
    const tabs = Array.from(group.querySelectorAll(".rec-tab"));
    tabs.forEach((t) => t.addEventListener("click", () => {
      tabs.forEach((x) => x.classList.remove("active"));
      t.classList.add("active");
      const list = group.parentElement.querySelector(".rec-list");
      if (list) {
        list.style.opacity = "0";
        setTimeout(() => { list.style.opacity = "1"; }, 250);
      }
    }));
  });

  /* ==========================================================
     Filter button (toggles sidebar visibility on mobile)
     ========================================================== */
  document.querySelectorAll(".filter-button").forEach((btn) => {
    btn.addEventListener("click", () => {
      const filters = document.querySelector(".filters");
      if (filters) {
        filters.classList.toggle("filters--open");
        filters.scrollIntoView({ behavior: "smooth", block: "nearest" });
      }
    });
  });

  /* ==========================================================
     Filter sidebar — toggle + actually filter cards
     ========================================================== */
  const TEXT_TO_VALUE = {
    // Regiones
    "África": "africa", "Asia": "asia", "Europa": "europa",
    "Sudamérica": "sudamerica", "Norteamérica": "norteamerica",
    "Caribe": "caribe", "Oceanía": "oceania",
    "Australia y Nueva Zelanda": "oceania",
    "Antártida": "polos", "Polos": "polos",
    "Oriente Próximo": "oriente-medio",
    "Norte de África": "oriente-medio",
    "Océano Índico": "oriente-medio",
    "Pacífico Sur": "oceania",
    "Centroamérica": "sudamerica",
    // Estilo / Modalidad / Intereses
    "Pequeño grupo": "pequeno-grupo",
    "Salida privada": "privado",
    "Privado": "privado",
    "Safari": "safari",
    "Cruceros": "crucero",
    "Crucero": "crucero",
    "Expediciones": "pequeno-grupo",
    "Jet privado": "jet",
    "Familia": "familia",
    "Cultura": "cultura",
    "Cultura e historia": "cultura",
    "Vida salvaje": "vida-salvaje",
    "Vida salvaje y safaris": "vida-salvaje",
    "Naturaleza y vida salvaje": "vida-salvaje",
    "Gastronomía": "gastronomia",
    "Gastronomía y vinos": "gastronomia",
    "Activo": "activo",
    "Activo y aventura": "activo",
    "Festivales": "festivales",
    "Listo para reservar": "lista-para-reservar",
    "Cortos": "cortos",
    "Itinerarios cortos": "cortos",
    "Lugares Patrimonio": "patrimonio",
    // Meses
    "Enero": "enero", "Febrero": "febrero", "Marzo": "marzo",
    "Abril": "abril", "Mayo": "mayo", "Junio": "junio",
    "Julio": "julio", "Agosto": "agosto", "Septiembre": "septiembre",
    "Octubre": "octubre", "Noviembre": "noviembre", "Diciembre": "diciembre",
  };

  const SUMMARY_DIM = {
    "Regiones":         { kind: "region",   match: "any" },
    "Estilo de viaje":  { kind: "style",    match: "any" },
    "Modalidad":        { kind: "style",    match: "any" },
    "Intereses":        { kind: "style",    match: "any" },
    "Mes de salida":    { kind: "months",   match: "any" },
    "Año":              { kind: "year",     match: "any" },
    "Duración":         { kind: "duration", match: "range" },
  };

  const DURATION_RANGES = {
    "5 días o menos":  [0, 5],
    "6–10 días":        [6, 10],
    "6-10 días":        [6, 10],
    "11–15 días":       [11, 15],
    "11-15 días":       [11, 15],
    "16–20 días":       [16, 20],
    "16-20 días":       [16, 20],
    "21+ días":         [21, 999],
  };

  function getSummaryBase(summary) {
    return (summary.dataset.label || summary.textContent.replace(/\s*\(\d+\)\s*$/, "").trim());
  }

  function applyFilters() {
    const filters = {}; // {kind: Set of values}
    document.querySelectorAll(".filters .filter-list a.active").forEach((a) => {
      const det = a.closest("details");
      const summary = det && det.querySelector("summary");
      if (!summary) return;
      const baseLabel = getSummaryBase(summary);
      const dim = SUMMARY_DIM[baseLabel];
      if (!dim) return;
      const txt = a.textContent.trim();
      let val;
      if (dim.kind === "duration") {
        val = DURATION_RANGES[txt] || null;
      } else if (dim.kind === "year") {
        val = txt;
      } else {
        val = TEXT_TO_VALUE[txt] || txt.toLowerCase();
      }
      if (val == null) return;
      if (!filters[dim.kind]) filters[dim.kind] = { values: [], match: dim.match };
      filters[dim.kind].values.push(val);
    });

    const cards = document.querySelectorAll(".j-card");
    let visible = 0;
    cards.forEach((card) => {
      let show = true;
      Object.entries(filters).forEach(([kind, conf]) => {
        if (kind === "duration") {
          const d = parseInt(card.dataset.duration || "0", 10);
          const anyRangeMatches = conf.values.some(([lo, hi]) => d >= lo && d <= hi);
          if (!anyRangeMatches) show = false;
        } else if (kind === "year") {
          // we don't have year data — soft-pass; future: data-years="2026,2027"
          // any filter active here lets all cards through (no-op)
        } else {
          const cardVals = (card.dataset[kind] || "").split(",").map(s => s.trim()).filter(Boolean);
          const match = conf.values.some(v => cardVals.includes(v));
          if (!match) show = false;
        }
      });
      card.style.display = show ? "" : "none";
      if (show) visible++;
    });

    // Update result count
    const head = document.querySelector(".explorer-head p");
    if (head) {
      const total = cards.length;
      head.textContent = visible === total
        ? `Mostrando ${total} resultados`
        : `Mostrando ${visible} de ${total} resultados`;
    }

    // Show "no results" empty state
    let empty = document.getElementById("filterEmpty");
    const grid = document.querySelector(".journey-grid");
    if (visible === 0 && grid) {
      if (!empty) {
        empty = document.createElement("div");
        empty.id = "filterEmpty";
        empty.className = "filter-empty";
        empty.innerHTML = '<p>Ningún viaje coincide con los filtros seleccionados.</p><button class="btn btn-outline-dark" type="button" id="clearFilters">Limpiar filtros</button>';
        grid.parentElement.appendChild(empty);
        document.getElementById("clearFilters").addEventListener("click", () => {
          document.querySelectorAll(".filters .filter-list a.active").forEach((a) => a.classList.remove("active"));
          document.querySelectorAll(".filters summary").forEach((s) => {
            const base = getSummaryBase(s);
            s.dataset.label = base;
            s.textContent = base;
          });
          applyFilters();
        });
      }
      empty.style.display = "";
    } else if (empty) {
      empty.style.display = "none";
    }
  }

  document.querySelectorAll(".filters .filter-list a").forEach((a) => {
    a.addEventListener("click", (e) => {
      e.preventDefault();
      a.classList.toggle("active");
      const summary = a.closest("details")?.querySelector("summary");
      if (summary) {
        const active = a.closest(".filter-list").querySelectorAll("a.active").length;
        const baseLabel = getSummaryBase(summary);
        summary.dataset.label = baseLabel;
        summary.textContent = active > 0 ? `${baseLabel} (${active})` : baseLabel;
      }
      applyFilters();
    });
  });

  // Read query string ?q=... and pre-filter cards by title text
  const params = new URLSearchParams(window.location.search);
  const q = (params.get("q") || "").trim().toLowerCase();
  if (q) {
    document.querySelectorAll(".j-card").forEach((card) => {
      const title = card.querySelector("h3")?.textContent.toLowerCase() || "";
      const itin = card.querySelector(".j-itin")?.textContent.toLowerCase() || "";
      const match = title.includes(q) || itin.includes(q);
      card.style.display = match ? "" : "none";
    });
    const cards = document.querySelectorAll(".j-card");
    const visible = document.querySelectorAll('.j-card:not([style*="display: none"])').length;
    const head = document.querySelector(".explorer-head p");
    if (head) head.textContent = `Mostrando ${visible} resultados para "${q}"`;
  }

  /* ==========================================================
     Forms — newsletter: validate email client-side, then let Netlify
     Forms handle the actual submission (action="/gracias.html").
     If the form has no action/data-netlify, fall back to fake-submit.
     ========================================================== */
  document.querySelectorAll("form.newsletter, form.newsletter-form").forEach((form) => {
    form.addEventListener("submit", (e) => {
      const email = form.querySelector('input[type="email"]');
      if (!email || !email.value || !/.+@.+\..+/.test(email.value)) {
        e.preventDefault();
        showToast("Por favor ingresá un correo válido.", "error");
        return;
      }
      // If the form is wired to Netlify Forms, let it submit normally
      // (it will POST and redirect to action). Otherwise fake-submit.
      if (form.hasAttribute("data-netlify") && form.getAttribute("action")) return;
      e.preventDefault();
      form.querySelectorAll("input").forEach((i) => { if (i.type !== "hidden") i.value = ""; });
      showToast("¡Suscripción confirmada! Revisá tu correo.", "ok");
    });
  });

  /* ==========================================================
     Toast (small floating message)
     ========================================================== */
  function showToast(message, kind) {
    let toast = document.getElementById("toast");
    if (!toast) {
      toast = document.createElement("div");
      toast.id = "toast";
      toast.className = "toast";
      document.body.appendChild(toast);
    }
    toast.textContent = message;
    toast.dataset.kind = kind || "ok";
    toast.classList.add("show");
    clearTimeout(toast._t);
    toast._t = setTimeout(() => toast.classList.remove("show"), 3500);
  }

  /* ==========================================================
     Subnav scroll-spy (highlight current section in subnav)
     ========================================================== */
  const subnavLinks = document.querySelectorAll(".subnav a[href^='#']");
  if (subnavLinks.length && "IntersectionObserver" in window) {
    const sections = Array.from(subnavLinks)
      .map((l) => document.querySelector(l.getAttribute("href")))
      .filter(Boolean);
    if (sections.length) {
      const obs = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            subnavLinks.forEach((l) => l.classList.remove("active"));
            const link = document.querySelector(`.subnav a[href="#${entry.target.id}"]`);
            if (link) link.classList.add("active");
          }
        });
      }, { rootMargin: "-30% 0px -55% 0px" });
      sections.forEach((s) => obs.observe(s));
    }
  }

  /* ==========================================================
     Smooth anchor offset for sticky header
     ========================================================== */
  document.querySelectorAll('a[href^="#"]').forEach((a) => {
    a.addEventListener("click", (e) => {
      const id = a.getAttribute("href");
      if (!id || id === "#" || id.length < 2) return;
      const target = document.querySelector(id);
      if (!target) return;
      e.preventDefault();
      const headerH = header ? header.getBoundingClientRect().height : 80;
      const top = target.getBoundingClientRect().top + window.scrollY - headerH - 12;
      window.scrollTo({ top, behavior: "smooth" });
    });
  });

  /* ==========================================================
     Reveal on scroll
     ========================================================== */
  const targets = [
    ".section-head",
    ".intro-text",
    ".img-card",
    ".trip-kinds-text",
    ".philanthropy-text",
    ".philanthropy-image",
    ".stat",
    ".rec-card",
    ".j-card",
    ".tailormade",
    ".feature",
    ".rec-row",
    ".day",
    ".ext-card",
    ".lodge-card",
    ".review",
    ".highlight",
  ];
  const els = document.querySelectorAll(targets.join(","));
  els.forEach((el) => el.classList.add("reveal"));
  if ("IntersectionObserver" in window) {
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("in");
            io.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.08, rootMargin: "0px 0px -40px 0px" }
    );
    els.forEach((el) => io.observe(el));
  } else {
    els.forEach((el) => el.classList.add("in"));
  }

  /* ==========================================================
     "Reservar" buttons in dates table — open contact CTA
     ========================================================== */
  document.querySelectorAll(".dates-table a.link-arrow").forEach((a) => {
    a.addEventListener("click", (e) => {
      e.preventDefault();
      const row = a.closest("tr");
      const date = row?.cells?.[0]?.textContent?.trim() || "";
      if (window.__openExpert) { window.__openExpert({ salida: date }); }
      else { showToast(`Escribinos para reservar la salida del ${date}.`, "ok"); }
    });
  });

  /* ==========================================================
     Interactive route map (Leaflet + OpenStreetMap / Carto)
     Two independent concerns:
       (a) Scroll-spy that highlights the active day + map-stop as
           the user scrolls. Runs always, no Leaflet required.
       (b) Leaflet map rendering. If the CDN loads, the map is wired
           up and follows the active stop via flyTo.
     Decoupling them means the day/stops highlight works even when
     Leaflet fails to load (offline, blocked CDN, etc.).
     ========================================================== */
  // Per-frame state so Leaflet can attach to scroll-spy that's
  // already running by the time the library finishes loading.
  const routeFrames = [];

  function setupScrollSpy(frame, stops) {
    const section = frame.closest(".itinerary-sticky");
    if (!section) return null;
    const days = section.querySelectorAll(".day[data-stop-index]");
    const stopsList = section.querySelectorAll(".map-stops li");
    if (!days.length) return null;

    let currentIdx = -1;
    const state = { stops, days, stopsList, currentIdx, onChange: [] };

    const highlight = (idx) => {
      state.currentIdx = idx;
      stopsList.forEach((li, i) => li.classList.toggle("active", i === idx));
      days.forEach((d) => {
        const di = parseInt(d.dataset.stopIndex, 10);
        d.classList.toggle("is-active", di === idx);
      });
      state.onChange.forEach((cb) => cb(idx));
    };

    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            const idx = parseInt(entry.target.dataset.stopIndex, 10);
            if (!isNaN(idx) && idx !== state.currentIdx && idx < stops.length) {
              highlight(idx);
            }
          }
        });
      },
      { rootMargin: "-35% 0px -55% 0px", threshold: 0 }
    );
    days.forEach((d) => io.observe(d));
    return state;
  }

  function attachLeaflet(frame, stops, spyState) {
    if (typeof L === "undefined") return;
    const mapEl = document.createElement("div");
    mapEl.className = "leaflet-map";
    frame.innerHTML = "";
    frame.appendChild(mapEl);

    const map = L.map(mapEl, {
      zoomControl: true,
      scrollWheelZoom: false,
      attributionControl: true,
      zoomSnap: 0.25,
    });

    L.tileLayer("https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png", {
      attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> · © <a href="https://carto.com/attributions">CARTO</a>',
      subdomains: "abcd",
      maxZoom: 19,
    }).addTo(map);

    const latlngs = stops.map((s) => [s.lat, s.lng]);
    const markers = stops.map((stop, i) => {
      const icon = L.divIcon({
        className: "route-marker",
        iconSize: [28, 28],
        iconAnchor: [14, 14],
        html: `<span data-i="${i}">${i + 1}</span>`,
      });
      return L.marker([stop.lat, stop.lng], { icon })
        .addTo(map)
        .bindPopup(`<strong>${i + 1}. ${stop.name}</strong>`);
    });

    L.polyline(latlngs, {
      color: "#3D5A3E",
      weight: 2.5,
      opacity: 0.9,
      dashArray: "6,8",
    }).addTo(map);

    const bounds = L.latLngBounds(latlngs);
    const fitAll = () => {
      if (latlngs.length > 1) map.fitBounds(bounds, { padding: [30, 30] });
      else map.setView(latlngs[0], 8);
    };
    fitAll();

    const refreshSize = () => { map.invalidateSize(); fitAll(); };
    setTimeout(refreshSize, 80);
    setTimeout(refreshSize, 400);
    window.addEventListener("resize", () => { map.invalidateSize(); });

    const targetZoom = () => {
      const z = map.getZoom();
      const fit = map.getBoundsZoom(bounds, false);
      return z <= fit + 0.3 ? Math.min(fit + 1.5, 8) : z;
    };

    const flyToStop = (idx) => {
      markers.forEach((m, i) => {
        if (!m._icon) return;
        m._icon.classList.toggle("route-marker-active", i === idx);
      });
      if (idx >= 0 && idx < stops.length) {
        map.flyTo([stops[idx].lat, stops[idx].lng], targetZoom(), {
          duration: 0.9,
          easeLinearity: 0.35,
        });
      }
    };

    if (spyState) {
      spyState.onChange.push(flyToStop);
      // Apply current state immediately if scroll-spy already activated a day
      if (spyState.currentIdx >= 0) flyToStop(spyState.currentIdx);
    }
  }

  function initRouteMaps() {
    document.querySelectorAll(".map-frame[data-stops]").forEach((frame) => {
      let stops;
      try { stops = JSON.parse(frame.dataset.stops); } catch (e) { return; }
      if (!Array.isArray(stops) || stops.length === 0) return;
      // Scroll-spy runs immediately, independent of Leaflet
      const spyState = setupScrollSpy(frame, stops);
      routeFrames.push({ frame, stops, spyState });
    });
  }

  function loadLeaflet() {
    if (typeof L !== "undefined") {
      routeFrames.forEach((f) => attachLeaflet(f.frame, f.stops, f.spyState));
      return;
    }
    const css = document.createElement("link");
    css.rel = "stylesheet";
    css.href = "https://unpkg.com/leaflet@1.9.4/dist/leaflet.css";
    document.head.appendChild(css);

    const script = document.createElement("script");
    script.src = "https://unpkg.com/leaflet@1.9.4/dist/leaflet.js";
    script.async = true;
    script.onload = () => {
      routeFrames.forEach((f) => attachLeaflet(f.frame, f.stops, f.spyState));
    };
    document.head.appendChild(script);
  }

  if (document.querySelector(".map-frame[data-stops]")) {
    initRouteMaps();   // scroll-spy now
    loadLeaflet();     // map asap (separate concern)
  }

})();

/* ==========================================================
   Newsletter pop-up modal (Sprint 2)
   - Aparece a los 20s O cuando el mouse sale por arriba (exit-intent)
   - Una sola vez por sesión; si se cierra/suscribe, no vuelve por 30 días
   - localStorage key: ba_newsletter_modal_v1 (timestamp del dismiss)
   ========================================================== */
(function() {
  var STORAGE_KEY = "ba_newsletter_modal_v1";
  var DISMISS_DAYS = 30;
  var SHOW_AFTER_MS = 20000;

  function getDismissedAt() {
    try { var v = localStorage.getItem(STORAGE_KEY); return v ? parseInt(v, 10) : 0; }
    catch (e) { return 0; }
  }
  function setDismissedAt() {
    try { localStorage.setItem(STORAGE_KEY, Date.now().toString()); } catch (e) {}
  }
  function shouldShow() {
    var t = getDismissedAt();
    if (!t) return true;
    var daysSince = (Date.now() - t) / 86400000;
    return daysSince >= DISMISS_DAYS;
  }
  if (!shouldShow()) return;

  // Construir DOM
  var modal = document.createElement("div");
  modal.className = "newsletter-modal";
  modal.setAttribute("role", "dialog");
  modal.setAttribute("aria-modal", "true");
  modal.innerHTML = ''
    + '<div class="newsletter-modal-card">'
    + '  <button class="newsletter-modal-close" aria-label="Cerrar">&times;</button>'
    + '  <span class="eyebrow">Newsletter</span>'
    + '  <h3>Una carta breve al mes</h3>'
    + '  <p class="lede">Un destino, una historia, una recomendación. Sin promociones agresivas, sin saturar tu bandeja.</p>'
    + '  <form name="newsletter-popup" method="POST" data-netlify="true" data-netlify-honeypot="bot-field" action="/gracias.html">'
    + '    <input type="hidden" name="form-name" value="newsletter-popup" />'
    + '    <p style="position:absolute;left:-9999px;"><label>No completar: <input name="bot-field" /></label></p>'
    + '    <input type="email" name="email" placeholder="Tu correo electrónico" required />'
    + '    <button class="btn btn-laurel" type="submit">Suscribirme</button>'
    + '    <span class="terms">Al suscribirte aceptas nuestros <a href="terminos.html">Términos</a> y <a href="privacidad.html">Política de privacidad</a>.</span>'
    + '  </form>'
    + '</div>';

  function attach() {
    if (!document.body) return;
    document.body.appendChild(modal);

    var shown = false;
    var timer;

    function show() {
      if (shown) return;
      shown = true;
      modal.classList.add("open");
      clearTimeout(timer);
      document.removeEventListener("mouseleave", onLeave);
    }
    function close() {
      modal.classList.remove("open");
      setDismissedAt();
    }
    function onLeave(e) { if (e.clientY <= 0) show(); }

    timer = setTimeout(show, SHOW_AFTER_MS);
    document.addEventListener("mouseleave", onLeave);

    modal.querySelector(".newsletter-modal-close").addEventListener("click", close);
    modal.addEventListener("click", function(e) { if (e.target === modal) close(); });
    document.addEventListener("keydown", function(e) {
      if (e.key === "Escape" && modal.classList.contains("open")) close();
    });
    modal.querySelector("form").addEventListener("submit", setDismissedAt);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", attach);
  } else {
    attach();
  }
})();


/* ==========================================================
   Newsletter -> backend B&A (endpoint publico Supabase)
   Captura el form del footer (#newsletter) y el del modal,
   en cualquier pagina. Reemplaza el submit de Netlify Forms.
   ========================================================== */
(function () {
  "use strict";
  var EP = "https://onnqcdjkvpvpvtsorpup.supabase.co/functions/v1/public-subscribe";
  var KEY = "sb_publishable_PcVUGfWVD_Aj_gE1H0Jr4g_fKrLn-Ua";
  function isNews(form) {
    if (!form || form.tagName !== "FORM") return false;
    return form.id === "newsletter" || (form.classList && form.classList.contains("newsletter")) || !!(form.closest && form.closest(".newsletter-modal"));
  }
  function done(form) {
    var msg = document.createElement("div");
    msg.className = "newsletter-done";
    msg.innerHTML = '<strong style="display:block; color:var(--white); font-family:var(--serif); font-size:22px; line-height:1.15; margin-bottom:6px;">Listo, te sumaste al Cuaderno B&amp;A.</strong><span class="terms">Te llega la próxima carta. Revisá tu correo.</span>';
    if (form.parentNode) form.parentNode.replaceChild(msg, form);
  }
  function handler(e) {
    var form = e.target;
    if (!isNews(form)) return;
    e.preventDefault();
    var hp = form.querySelector('[name="bot-field"]');
    var emailEl = form.querySelector('input[type="email"]');
    var email = emailEl ? (emailEl.value || "").trim() : "";
    if (!email) { if (emailEl) emailEl.focus(); return; }
    var nom = form.querySelector('input[placeholder*="ombre"]');
    var ape = form.querySelector('input[placeholder*="pellido"]');
    var name = [nom && nom.value, ape && ape.value].filter(Boolean).join(" ").trim();
    var btn = form.querySelector('button[type="submit"], button:not([type]), input[type="submit"]');
    if (btn) btn.disabled = true;
    fetch(EP, {
      method: "POST",
      headers: { "Content-Type": "application/json", "apikey": KEY },
      body: JSON.stringify({ email: email, name: name, hp: hp ? hp.value : "" })
    }).then(function (r) { return r.json().catch(function () { return {}; }); })
      .then(function (d) {
        if (d && d.ok) { done(form); }
        else { if (btn) btn.disabled = false; alert((d && d.error) || "No pudimos sumarte. Proba de nuevo."); }
      })
      .catch(function () { if (btn) btn.disabled = false; alert("No pudimos sumarte. Proba de nuevo."); });
  }
  document.addEventListener("submit", handler, true);
})();


/* ==========================================================
   Consulta -> backend B&A (CRM Leads, endpoint publico)
   Captura el form de contacto (.inquiry-form / name=consulta)
   y lo manda a public-lead. Redirige a la pagina de gracias.
   ========================================================== */
(function () {
  "use strict";
  var EP = "https://onnqcdjkvpvpvtsorpup.supabase.co/functions/v1/public-lead";
  var KEY = "sb_publishable_PcVUGfWVD_Aj_gE1H0Jr4g_fKrLn-Ua";
  function isLead(form) {
    if (!form || form.tagName !== "FORM") return false;
    return (form.classList && form.classList.contains("inquiry-form")) || (form.getAttribute("name") || "").indexOf("consulta") === 0;
  }
  function val(form, name) {
    var el = form.querySelector('[name="' + name + '"]');
    return el ? (el.value || "").trim() : "";
  }
  function handler(e) {
    var form = e.target;
    if (!isLead(form)) return;
    e.preventDefault();
    var emailEl = form.querySelector('input[type="email"], [name="email"]');
    var email = emailEl ? (emailEl.value || "").trim() : "";
    if (!email) { if (emailEl) emailEl.focus(); return; }
    var hp = form.querySelector('[name="bot-field"]');
    var asesorEl = form.querySelector('[name="asesor"]:checked');
    var q = new URLSearchParams(window.location.search || "");
    var body = {
      nombre: val(form, "nombre"), apellido: val(form, "apellido"), email: email,
      telefono: val(form, "telefono"),
      destino: val(form, "destino") || [val(form, "region"), val(form, "pais")].filter(Boolean).join(" · ") || val(form, "viaje"),
      tipo: val(form, "tipo") || val(form, "intent"),
      viajeros: val(form, "viajeros"),
      fecha: val(form, "fecha") || val(form, "salida"),
      presupuesto: val(form, "presupuesto"),
      mensaje: val(form, "mensaje"), asesor: asesorEl ? asesorEl.value : "", hp: hp ? hp.value : "",
      utm_source: q.get("utm_source") || "", utm_medium: q.get("utm_medium") || "", utm_campaign: q.get("utm_campaign") || "", utm_content: q.get("utm_content") || "", utm_term: q.get("utm_term") || "", referrer: document.referrer || ""
    };
    var btn = form.querySelector('button[type="submit"], button:not([type])');
    if (btn) btn.disabled = true;
    fetch(EP, { method: "POST", headers: { "Content-Type": "application/json", "apikey": KEY }, body: JSON.stringify(body) })
      .then(function (r) { return r.json().catch(function () { return {}; }); })
      .then(function (d) {
        if (d && d.ok) { window.location.href = form.getAttribute("action") || "/gracias.html"; }
        else { if (btn) btn.disabled = false; alert((d && d.error) || "No pudimos enviar la consulta. Proba de nuevo."); }
      })
      .catch(function () { if (btn) btn.disabled = false; alert("No pudimos enviar la consulta. Proba de nuevo."); });
  }
  document.addEventListener("submit", handler, true);
})();
