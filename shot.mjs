// Captures screenshots used as figures in the report.
import { pathToFileURL } from "node:url";
import path from "node:path";
import fs from "node:fs";

const pkg = process.env.PLAYWRIGHT_PKG;
const { chromium } = await import(pathToFileURL(path.join(pkg, "index.mjs")).href);

const target = process.argv[2];
const out = process.argv[3];
const width = Number(process.argv[4] ?? 1280);
const height = Number(process.argv[5] ?? 900);
const fullPage = process.argv[6] === "full";

fs.mkdirSync(path.dirname(out), { recursive: true });
const browser = await chromium.launch();
const page = await browser.newPage({
  viewport: { width, height },
  deviceScaleFactor: 2,
  colorScheme: "light",
});
await page.goto(target, { waitUntil: "networkidle" });
// Hide the Next.js dev-tools indicator so the capture matches production.
await page.addStyleTag({
  content: "nextjs-portal,[data-nextjs-dev-tools-button],#__next-build-watcher{display:none!important}",
});
await page.waitForTimeout(1200);
// Wait for client-side data to land when the page fetches it.
try { await page.waitForFunction(() => !document.body.innerText.includes("Loading notes"), { timeout: 15000 }); } catch {}
await page.waitForTimeout(800);
await page.screenshot({ path: out, fullPage });
await browser.close();
console.log(`captured: ${out}`);
