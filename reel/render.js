// Renderiza reel.html a MP4 vertical 1080x1920 (9:16).
// Uso: node reel/render.js [salida.mp4]
const { chromium } = require('playwright');
const { execFileSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const FPS = 30;
const out = process.argv[2] || path.join(__dirname, 'aquacore-reel.mp4');
const framesDir = fs.mkdtempSync(path.join(require('os').tmpdir(), 'reel-'));

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 540, height: 960 }, deviceScaleFactor: 2 });
  await page.goto('file://' + path.join(__dirname, 'reel.html') + '?render');
  const dur = await page.evaluate(() => window.DURATION);
  const n = Math.round(dur * FPS);
  for (let i = 0; i < n; i++) {
    await page.evaluate(t => window.render(t), i / FPS);
    await page.screenshot({ path: path.join(framesDir, `f${String(i).padStart(4, '0')}.png`) });
  }
  await browser.close();
  execFileSync('ffmpeg', ['-y', '-v', 'error', '-framerate', String(FPS), '-i', path.join(framesDir, 'f%04d.png'),
    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-movflags', '+faststart', out]);
  fs.rmSync(framesDir, { recursive: true, force: true });
  console.log('OK ->', out, `(${n} frames)`);
})();
