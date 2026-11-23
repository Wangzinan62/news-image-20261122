// Entry point for the news-image-20261122 bounty.
// Copies the pre-rendered front page (entry.png, produced by
// build_image.py) into the harness output directory.
import { copyFileSync, statSync } from "node:fs";
import { join } from "node:path";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const dest = join(outDir, "entry.png");
copyFileSync("./entry.png", dest);
const bytes = statSync(dest).size;
if (bytes === 0) {
  throw new Error("entry.png is empty, refusing to submit a blank image");
}
console.log(`entry.png -> ${dest} (${bytes} bytes)`);
