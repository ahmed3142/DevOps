// Screenshots a figure fragment (or any HTML file) to PNG for visual checking.
// Usage: node preview.mjs figures/fig1-value-stream.html out/fig1.png
import { pathToFileURL } from "node:url";
import path from "node:path";
import fs from "node:fs";

const pkg = process.env.PLAYWRIGHT_PKG;
const { chromium } = await import(pathToFileURL(path.join(pkg, "index.mjs")).href);

const src = process.argv[2];
const out = process.argv[3] ?? "out/preview.png";
fs.mkdirSync(path.dirname(out), { recursive: true });

const body = fs.readFileSync(src, "utf-8");
const css = fs.readFileSync("styles.css", "utf-8");

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 700, height: 900 }, deviceScaleFactor: 2 });
await page.setContent(
  `<style>${css}</style><div style="width:658px;padding:12px;background:#fff">${body}</div>`,
  { waitUntil: "networkidle" },
);
const el = await page.$("figure");
await (el ?? page).screenshot({ path: out });
await browser.close();
console.log(`preview: ${out}`);
