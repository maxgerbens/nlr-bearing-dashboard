import { readFileSync, writeFileSync } from "node:fs";
import { Graphviz } from "@hpcc-js/wasm-graphviz";
import puppeteer from "puppeteer-core";

const CHROME = "/Users/maxgerbens/.cache/puppeteer/chrome/mac_arm-149.0.7827.22/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing";
const diagrams = ["c4_1_context", "c4_2_container", "c4_3_component"];

const graphviz = await Graphviz.load();
const browser = await puppeteer.launch({ executablePath: CHROME, args: ["--no-sandbox"] });

for (const name of diagrams) {
  const dot = readFileSync(`${name}.dot`, "utf8");
  const svg = graphviz.dot(dot, "svg");
  writeFileSync(`${name}.svg`, svg);

  const page = await browser.newPage();
  await page.setViewport({ width: 1600, height: 1200, deviceScaleFactor: 2 });
  const html = `<!doctype html><meta charset="utf8"><body style="margin:0;background:white;display:inline-block">${svg}</body>`;
  await page.setContent(html, { waitUntil: "networkidle0" });
  const el = await page.$("svg");
  await el.screenshot({ path: `${name}.png` });
  await page.close();
  console.log(`rendered ${name}.png`);
}

await browser.close();
