// Renders report HTML to PDF via Playwright's Chromium so that the PDF
// carries a proper page-number footer. Falls back handled by build.sh.
import { chromium } from "playwright";
import { pathToFileURL } from "node:url";
import path from "node:path";
import fs from "node:fs";

const src = process.argv[2] ?? "report.html";
const out = process.argv[3] ?? "out/DevOps_Delivery_Strategy.pdf";
const footerLabel = process.argv[4] ?? "DevOps Delivery Strategy — Nimbus (Scenario B)";

if (!fs.existsSync(src)) {
  console.error(`source not found: ${src}`);
  process.exit(1);
}
fs.mkdirSync(path.dirname(out), { recursive: true });

const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto(pathToFileURL(path.resolve(src)).href, { waitUntil: "networkidle" });

await page.pdf({
  path: out,
  format: "A4",
  printBackground: true,
  displayHeaderFooter: true,
  headerTemplate: "<div></div>",
  footerTemplate: `<div style="font-family:Helvetica,Arial,sans-serif;font-size:8pt;color:#6b7280;width:100%;padding:0 18mm;display:flex;justify-content:space-between;">
      <span>${footerLabel}</span>
      <span>Page <span class="pageNumber"></span> of <span class="totalPages"></span></span>
    </div>`,
  margin: { top: "16mm", bottom: "16mm", left: "18mm", right: "18mm" },
});

await browser.close();
const kb = Math.round(fs.statSync(out).size / 1024);
console.log(`built: ${out} (${kb} KB)`);
