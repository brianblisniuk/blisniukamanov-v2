// Functional QA — exercise every interactive feature and capture its state.
// Usage: PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers node functional-qa.js
const path = require("path");
const fs = require("fs");
const { chromium } = require("playwright");

const repo = "/home/user/sitio";
const outDir = path.join(repo, "_compare", "functional");
fs.mkdirSync(outDir, { recursive: true });

const report = [];
const log = (msg) => { console.log(msg); report.push(msg); };

const fileUrl = (rel) => "file://" + path.join(repo, rel);

(async () => {
  const browser = await chromium.launch({
    executablePath: "/opt/pw-browsers/chromium-1194/chrome-linux/chrome",
    args: ["--no-sandbox", "--disable-setuid-sandbox"],
  });

  const desktop = await browser.newContext({
    viewport: { width: 1280, height: 900 },
    deviceScaleFactor: 1,
  });
  const mobile = await browser.newContext({
    viewport: { width: 414, height: 896 },
    deviceScaleFactor: 1,
  });

  // ============================================================
  // 1) HOMEPAGE TABS
  // ============================================================
  log("\n=== 1) Homepage tabs ===");
  {
    const page = await desktop.newPage();
    await page.goto(fileUrl("index.html"));
    await page.evaluate(() => document.querySelectorAll(".reveal").forEach(el => el.classList.add("in")));
    await page.waitForTimeout(400);

    const tabs = await page.$$eval(".tabs .tab", els => els.map(el => ({
      key: el.dataset.tab, text: el.textContent.trim(), active: el.classList.contains("active")
    })));
    log(`  Tabs found: ${tabs.map(t => t.key).join(", ")}`);

    for (const t of tabs) {
      await page.click(`.tabs .tab[data-tab="${t.key}"]`);
      await page.waitForTimeout(500);
      // Verify panel state
      const panelStates = await page.$$eval(".tab-panel", panels => panels.map(p => ({
        key: p.dataset.panel,
        active: p.classList.contains("active"),
        visible: window.getComputedStyle(p).display !== "none",
        cardCount: p.querySelectorAll(".img-card").length,
      })));
      const activePanel = panelStates.find(p => p.active);
      const onlyOneVisible = panelStates.filter(p => p.visible).length === 1;
      log(`  click [${t.key}]: active panel=${activePanel?.key}, cards=${activePanel?.cardCount}, exactlyOneVisible=${onlyOneVisible}`);
      // Scroll active tab section into view + screenshot
      await page.evaluate(() => document.querySelector(".tabs").scrollIntoView({behavior:"instant", block:"start"}));
      await page.waitForTimeout(200);
      await page.screenshot({ path: path.join(outDir, `tab-${t.key}.png`), clip: { x: 0, y: 0, width: 1280, height: 900 } });
    }
    await page.close();
  }

  // ============================================================
  // 2) JOURNEYS FILTERS
  // ============================================================
  log("\n=== 2) Journey filters ===");
  {
    const page = await desktop.newPage();
    await page.goto(fileUrl("journeys.html"));
    await page.evaluate(() => document.querySelectorAll(".reveal").forEach(el => el.classList.add("in")));
    await page.waitForTimeout(400);

    const total = await page.$$eval(".j-card", els => els.length);
    log(`  Total cards: ${total}`);

    // Helper: count visible cards
    const visibleCount = async () => page.$$eval(".j-card", els =>
      els.filter(el => window.getComputedStyle(el).display !== "none").length
    );

    // Helper: open all details so filter links are clickable
    const openAllDetails = async () => {
      await page.$$eval(".filters details", els => els.forEach(d => d.open = true));
    };

    // Helper: click a filter link by its text
    const clickFilter = async (text) => {
      await openAllDetails();
      await page.evaluate((t) => {
        const links = Array.from(document.querySelectorAll(".filters .filter-list a"));
        const target = links.find(a => a.textContent.trim() === t);
        if (target) target.click();
        return !!target;
      }, text);
      await page.waitForTimeout(300);
    };

    const scrollToGrid = async () => {
      await page.evaluate(() => {
        const grid = document.querySelector(".journey-grid");
        if (grid) grid.scrollIntoView({ behavior: "instant", block: "start" });
      });
      await page.waitForTimeout(300);
    };

    // Test 1: Region Asia
    await clickFilter("Asia");
    const nAsia = await visibleCount();
    log(`  After Region=Asia: ${nAsia} of ${total} visible (expect 3: Uzbek, Japón, Bután)`);
    await scrollToGrid();
    await page.screenshot({ path: path.join(outDir, "filter-asia.png"), fullPage: false });
    await clickFilter("Asia"); // clear

    // Test 2: Duration 6-10
    await clickFilter("6–10 días");
    const nDur = await visibleCount();
    log(`  After Duration=6–10: ${nDur} of ${total} visible (expect Piamonte 8, Bahía 9, Croacia 9 = 3)`);
    await clickFilter("6–10 días"); // clear

    // Test 3: Combination Asia + Septiembre
    await clickFilter("Asia");
    await clickFilter("Septiembre");
    const combo = await visibleCount();
    log(`  After Asia + Septiembre: ${combo} visible (expect 1: Uzbekistán)`);
    await scrollToGrid();
    await page.screenshot({ path: path.join(outDir, "filter-asia-sep.png"), fullPage: false });

    // Test 4: Clear all
    await clickFilter("Asia");
    await clickFilter("Septiembre");
    const cleared = await visibleCount();
    log(`  After clearing: ${cleared} visible (expect ${total})`);

    await page.close();
  }

  // ============================================================
  // 3) JOURNEYS SEARCH via ?q=
  // ============================================================
  log("\n=== 3) Journey search (?q=) ===");
  {
    const page = await desktop.newPage();
    await page.goto(fileUrl("journeys.html") + "?q=tartufo");
    await page.evaluate(() => document.querySelectorAll(".reveal").forEach(el => el.classList.add("in")));
    await page.waitForTimeout(400);
    const visible = await page.$$eval(".j-card", els =>
      els.filter(el => window.getComputedStyle(el).display !== "none").length
    );
    log(`  Search ?q=tartufo: ${visible} visible (expect 1: Piamonte)`);
    await page.close();
  }

  // ============================================================
  // 4) MAP scroll-spy on viaje page
  // ============================================================
  log("\n=== 4) Viaje sticky map + scroll-spy ===");
  {
    const page = await desktop.newPage();
    await page.goto(fileUrl("piamonte-tartufo.html"));
    await page.waitForTimeout(2500); // wait for Leaflet CDN + tiles

    // Verify map exists
    const mapPresent = await page.evaluate(() => {
      const el = document.querySelector(".map-frame .leaflet-map");
      return el ? {
        width: el.offsetWidth,
        height: el.offsetHeight,
        hasLeaflet: !!el.querySelector(".leaflet-container, .leaflet-tile-pane"),
      } : null;
    });
    log(`  Map: ${JSON.stringify(mapPresent)}`);

    // Count days
    const days = await page.$$eval(".day[data-stop-index]", els => els.length);
    log(`  Days with data-stop-index: ${days}`);

    // Scroll to each day section and verify is-active toggles
    const dayBoxes = await page.$$(".day[data-stop-index]");
    for (let i = 0; i < Math.min(3, dayBoxes.length); i++) {
      await dayBoxes[i].scrollIntoViewIfNeeded();
      await page.waitForTimeout(700);
      const state = await page.evaluate((idx) => {
        const day = document.querySelectorAll(".day[data-stop-index]")[idx];
        const stopIdx = day?.dataset.stopIndex;
        const activeDay = document.querySelector(".day.is-active");
        const activeStop = document.querySelector(".map-stops li.active");
        return {
          scrolledDayIdx: idx,
          scrolledDayStopIdx: stopIdx,
          activeDayStopIdx: activeDay?.dataset.stopIndex,
          activeStopText: activeStop?.textContent?.trim()?.substring(0, 40),
        };
      }, i);
      log(`  Scroll to day[${i}]: ${JSON.stringify(state)}`);
    }
    await page.screenshot({ path: path.join(outDir, "viaje-piamonte-scrolled.png"), fullPage: false });
    await page.close();
  }

  // ============================================================
  // 5) MODAL — Hablá con un experto
  // ============================================================
  log("\n=== 5) Expert modal ===");
  {
    const page = await desktop.newPage();
    await page.goto(fileUrl("namibia-dunas.html"));
    await page.waitForTimeout(800);
    const fabPresent = await page.evaluate(() => !!document.querySelector(".js-expert-trigger"));
    log(`  FAB trigger present: ${fabPresent}`);
    if (fabPresent) {
      await page.click(".js-expert-trigger");
      await page.waitForTimeout(400);
      const modalState = await page.evaluate(() => {
        const m = document.getElementById("expertModal");
        const region = document.querySelector("#expertModal select[name='region']")?.value;
        const pais = document.querySelector("#expertModal input[name='pais']")?.value;
        return {
          isOpen: m?.classList.contains("open"),
          ariaHidden: m?.getAttribute("aria-hidden"),
          preselectedRegion: region,
          preselectedPais: pais,
          contextHidden: document.querySelector("#expertModal input[name='contexto']")?.value,
        };
      });
      log(`  Modal opened: ${JSON.stringify(modalState)}`);
      await page.screenshot({ path: path.join(outDir, "modal-namibia.png") });
      // Close via ESC
      await page.keyboard.press("Escape");
      await page.waitForTimeout(300);
      const closed = await page.evaluate(() => !document.getElementById("expertModal")?.classList.contains("open"));
      log(`  Modal closed via ESC: ${closed}`);
    }
    await page.close();
  }

  // ============================================================
  // 6) MOBILE DRAWER
  // ============================================================
  log("\n=== 6) Mobile drawer ===");
  {
    const page = await mobile.newPage();
    await page.goto(fileUrl("index.html"));
    await page.waitForTimeout(500);
    const triggerPresent = await page.evaluate(() => !!document.getElementById("menuTrigger"));
    log(`  Menu trigger present: ${triggerPresent}`);
    if (triggerPresent) {
      await page.click("#menuTrigger");
      await page.waitForTimeout(400);
      const drawerState = await page.evaluate(() => {
        const d = document.getElementById("mobileDrawer");
        return {
          isOpen: d?.classList.contains("open"),
          ariaHidden: d?.getAttribute("aria-hidden"),
          bodyOverflow: document.body.style.overflow,
        };
      });
      log(`  Drawer state: ${JSON.stringify(drawerState)}`);
      await page.screenshot({ path: path.join(outDir, "mobile-drawer.png") });
      await page.keyboard.press("Escape");
      await page.waitForTimeout(300);
      const closed = await page.evaluate(() => !document.getElementById("mobileDrawer")?.classList.contains("open"));
      log(`  Drawer closed via ESC: ${closed}`);
    }
    await page.close();
  }

  // ============================================================
  // 7) STICKY HEADER on scroll
  // ============================================================
  log("\n=== 7) Sticky header ===");
  {
    const page = await desktop.newPage();
    await page.goto(fileUrl("index.html"));
    await page.waitForTimeout(400);
    const initial = await page.evaluate(() => document.getElementById("siteHeader")?.classList.contains("scrolled"));
    await page.evaluate(() => window.scrollTo(0, 600));
    await page.waitForTimeout(400);
    const after = await page.evaluate(() => document.getElementById("siteHeader")?.classList.contains("scrolled"));
    log(`  Header scrolled class: initial=${initial}, after-scroll=${after} (expect true)`);
    await page.close();
  }

  // ============================================================
  // 8) DATES TABLE "Reservar" → toast
  // ============================================================
  log("\n=== 8) Reservar button toast ===");
  {
    const page = await desktop.newPage();
    await page.goto(fileUrl("croacia-islas-dalmatas.html"));
    await page.waitForTimeout(800);
    const reservar = await page.$('.dates-table a.link-arrow');
    if (reservar) {
      await reservar.click();
      await page.waitForTimeout(400);
      const toast = await page.evaluate(() => {
        const t = document.getElementById("toast");
        return t ? { visible: t.classList.contains("show"), text: t.textContent } : null;
      });
      log(`  Toast: ${JSON.stringify(toast)}`);
    } else {
      log("  WARN: no Reservar button");
    }
    await page.close();
  }

  // ============================================================
  // 9) FAB stack visibility on all pages
  // ============================================================
  log("\n=== 9) FAB stack visibility ===");
  {
    const samplePages = ["index.html", "journeys.html", "piamonte-tartufo.html", "contact.html"];
    for (const p of samplePages) {
      const page = await desktop.newPage();
      await page.goto(fileUrl(p));
      await page.waitForTimeout(600);
      const fab = await page.evaluate(() => {
        const stack = document.getElementById("fabStack");
        const wa = document.getElementById("waButton");
        const expert = document.querySelector(".js-expert-trigger");
        return { stackExists: !!stack, waLink: wa?.href?.substring(0, 50), expertExists: !!expert };
      });
      log(`  ${p}: ${JSON.stringify(fab)}`);
      await page.close();
    }
  }

  // ============================================================
  // 10) Footer link existence sanity
  // ============================================================
  log("\n=== 10) Footer links resolve ===");
  {
    const page = await desktop.newPage();
    await page.goto(fileUrl("index.html"));
    const footerHrefs = await page.$$eval(".site-footer a[href$='.html']", els => [...new Set(els.map(a => a.getAttribute("href")))]);
    log(`  Distinct footer hrefs: ${footerHrefs.join(", ")}`);
    for (const h of footerHrefs) {
      const exists = fs.existsSync(path.join(repo, h));
      log(`    ${h}: ${exists ? "✓" : "✗"}`);
    }
    await page.close();
  }

  await browser.close();
  fs.writeFileSync(path.join(outDir, "report.txt"), report.join("\n"));
  console.log("\nDone. Report saved to " + path.join(outDir, "report.txt"));
})();
