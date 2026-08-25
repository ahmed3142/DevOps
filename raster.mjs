// Rasterises the inline-SVG figures to PNG so they can be embedded in the DOCX.
import { pathToFileURL } from "node:url";
import path from "node:path";
import fs from "node:fs";

const { chromium } = await import(pathToFileURL(path.join(process.env.PLAYWRIGHT_PKG, "index.mjs")).href);
const browser = await chromium.launch();
fs.mkdirSync("shots", { recursive: true });

for (const name of ["fig1-value-stream", "fig2-pipeline", "fig3-architecture", "fig4-error-budget"]) {
  const src = fs.readFileSync(`figures/${name}.html`, "utf-8");
  const svg = src.slice(src.indexOf("<svg"), src.indexOf("</svg>") + 6);
  const page = await browser.newPage({ viewport: { width: 900, height: 600 }, deviceScaleFactor: 3 });
  await page.setContent(`<body style="margin:0;background:#fff">${svg.replace('width="100%"', 'width="880"')}</body>`);
  const el = await page.$("svg");
  await el.screenshot({ path: `shots/${name}.png` });
  await page.close();
  console.log(`rasterised: shots/${name}.png`);
}
await browser.close();
