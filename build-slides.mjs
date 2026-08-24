// Renders slides.html to a 16:9 PDF sized to the .slide box (1280x720 px).
import { pathToFileURL } from "node:url";
import path from "node:path";
import fs from "node:fs";

const pkg = process.env.PLAYWRIGHT_PKG;
const { chromium } = await import(pathToFileURL(path.join(pkg, "index.mjs")).href);

const src = process.argv[2] ?? "slides.html";
const out = process.argv[3] ?? "out/DevOps_Presentation.pdf";
fs.mkdirSync(path.dirname(out), { recursive: true });

const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto(pathToFileURL(path.resolve(src)).href, { waitUntil: "networkidle" });
await page.pdf({
  path: out,
  width: "1280px",
  height: "720px",
  printBackground: true,
  margin: { top: "0", bottom: "0", left: "0", right: "0" },
});
await browser.close();
console.log(`built: ${out} (${Math.round(fs.statSync(out).size / 1024)} KB)`);
