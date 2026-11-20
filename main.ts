// main.ts — news-image-20261119 round 1
// Runs draw.py (python3) and copies the rendered front page to /output/entry.png.
// Node 22, stdlib only. All paths resolve via import.meta.url so the program
// works from any working directory.
import { spawnSync } from "node:child_process";
import { copyFileSync, mkdirSync } from "node:fs";
import { fileURLToPath } from "node:url";
import path from "node:path";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const drawPy = path.join(scriptDir, "draw.py");
const entryPng = path.join(scriptDir, "entry.png");
const outDir = process.env.OUTPUT_DIR || "/output";
const outPng = path.join(outDir, "entry.png");

const run = spawnSync("python3", [drawPy], { cwd: scriptDir, stdio: "inherit" });
if (run.status !== 0) {
  console.error(`draw.py failed with exit code ${run.status}`);
  process.exit(run.status ?? 1);
}
mkdirSync(outDir, { recursive: true });
copyFileSync(entryPng, outPng);
console.log(`wrote ${outPng}`);
