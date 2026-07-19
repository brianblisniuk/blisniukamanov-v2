// Renders my pages to PNG using the bundled Chromium.
// Usage: node screenshot.js
const path = require("path");
const fs = require("fs");
const { chromium } = require("playwright");

const repo = "/home/user/sitio";
const outDir = path.join(repo, "_compare");
fs.mkdirSync(outDir, { recursive: true });

const pages = [
  { name: "01-home-desktop",            file: "index.html",          width: 1280, full: true },
  { name: "02-destinations-desktop",    file: "destinations.html",   width: 1280, full: true },
  { name: "03-journeys-desktop",        file: "journeys.html",       width: 1280, full: true },
  { name: "04-home-mobile",             file: "index.html",          width: 414,  full: true },
  { name: "05-small-group-desktop",     file: "small-group.html",    width: 1280, full: true },
  { name: "06-small-group-mobile",      file: "small-group.html",    width: 414,  full: true },
  { name: "07-destinations-mobile",     file: "destinations.html",   width: 414,  full: true },
  { name: "08-europe-desktop",          file: "europe.html",         width: 1280, full: true },
  { name: "09-europe-mobile",           file: "europe.html",         width: 414,  full: true },
  { name: "10-contact-desktop",         file: "contact.html",        width: 1280, full: true },
  { name: "11-contact-mobile",          file: "contact.html",        width: 414,  full: true },
  { name: "12-gracias-desktop",         file: "gracias.html",        width: 1280, full: true },
  { name: "13-catalogos-desktop",       file: "catalogos.html",      width: 1280, full: true },
  { name: "14-terminos-desktop",        file: "terminos.html",       width: 1280, full: true },
  { name: "15-heritage-desktop",        file: "heritage.html",       width: 1280, full: true },
  { name: "16-filantropia-desktop",     file: "filantropia.html",    width: 1280, full: true },
  { name: "17-africa-desktop",          file: "africa.html",         width: 1280, full: true },
  // Los 10 viajes del calendario 2026-2027 (orden cronológico)
  { name: "20-uzbekistan-desktop",      file: "uzbekistan-ruta-seda.html",   width: 1280, full: true },
  { name: "21-piamonte-desktop",        file: "piamonte-tartufo.html",       width: 1280, full: true },
  { name: "22-piamonte-mobile",         file: "piamonte-tartufo.html",       width: 414,  full: true },
  { name: "23-namibia-desktop",         file: "namibia-dunas.html",          width: 1280, full: true },
  { name: "24-laponia-desktop",         file: "laponia-auroras.html",        width: 1280, full: true },
  { name: "25-bahia-desktop",           file: "bahia-otro-carnaval.html",    width: 1280, full: true },
  { name: "26-japon-desktop",           file: "japon-mono-no-aware.html",    width: 1280, full: true },
  { name: "27-butan-desktop",           file: "butan-nepal-himalaya.html",   width: 1280, full: true },
  { name: "28-marruecos-desktop",       file: "marruecos-imperial.html",     width: 1280, full: true },
  { name: "29-croacia-desktop",         file: "croacia-islas-dalmatas.html", width: 1280, full: true },
  { name: "30-alaska-salvaje-desktop",  file: "alaska-salvaje.html",         width: 1280, full: true },
];

(async () => {
  const browser = await chromium.launch({
    executablePath: "/opt/pw-browsers/chromium-1194/chrome-linux/chrome",
    args: ["--no-sandbox", "--disable-setuid-sandbox"],
  });
  const ctx = await browser.newContext({ deviceScaleFactor: 1 });

  for (const p of pages) {
    const url = "file://" + path.join(repo, p.file);
    const page = await ctx.newPage();
    await page.setViewportSize({ width: p.width, height: 900 });
    console.log("→", p.name, url);
    await page.goto(url, { waitUntil: "networkidle", timeout: 45000 }).catch((e) => {
      console.warn("  networkidle timeout, falling back:", e.message);
    });
    // Force scroll-reveal animations to show + scroll once to trigger lazy bits
    await page.evaluate(() => {
      document.querySelectorAll(".reveal").forEach((el) => el.classList.add("in"));
      window.scrollTo(0, document.body.scrollHeight);
    });
    await page.waitForTimeout(400);
    await page.evaluate(() => window.scrollTo(0, 0));
    await page.waitForTimeout(800);
    const out = path.join(outDir, p.name + ".png");
    await page.screenshot({ path: out, fullPage: p.full });
    console.log("  saved", out);
    await page.close();
  }

  await browser.close();
  console.log("Done.");
})();
