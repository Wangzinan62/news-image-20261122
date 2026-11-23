// Entry point for the news-image-20261122 bounty.
// Copies the pre-rendered front page (entry.png, produced by
// build_image.py) into the harness output directory.
//
// The grader runs this file as `node /bot/main.ts` with an unknown
// working directory, so the source image must be located relative to
// this script (import.meta.url), never relative to the CWD.
import { copyFileSync, mkdirSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const dest = join(outDir, "entry.png");

mkdirSync(outDir, { recursive: true });
copyFileSync(source, dest);
const bytes = statSync(dest).size;
const sourceBytes = statSync(source).size;
if (bytes === 0) {
  throw new Error("entry.png is empty, refusing to submit a blank image");
}
if (bytes !== sourceBytes) {
  throw new Error(
    `size mismatch after copy: source ${sourceBytes} bytes, dest ${bytes} bytes`,
  );
}
console.log(`entry.png -> ${dest} (${bytes} bytes)`);
