// 长图分段截图再拼接（Chromium 单张截图高度有限）。用法：node render_long.js URL out.png
const { chromium } = require('playwright');
const { execFileSync } = require('child_process');
(async () => {
  const [url, out] = process.argv.slice(2);
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 2000 }, deviceScaleFactor: 1 });
  await p.goto(url, { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(1000);
  const H = await p.evaluate(() => document.body.scrollHeight);
  const parts = [];
  for (let y = 0, i = 0; y < H; y += 4000, i++) {
    const h = Math.min(4000, H - y), f = `${out}.part${i}.png`;
    await p.screenshot({ path: f, fullPage: true, clip: { x: 0, y, width: 1080, height: h } });
    parts.push(f);
  }
  await b.close();
  execFileSync('python3', ['-c', `
import sys
from PIL import Image
fs=sys.argv[2:]; ims=[Image.open(f) for f in fs]
out=Image.new('RGB',(1080,sum(i.height for i in ims))); y=0
for i in ims: out.paste(i,(0,y)); y+=i.height
out.save(sys.argv[1]); print('saved', out.size)
import os
[os.remove(f) for f in fs]`, out, ...parts], { stdio: 'inherit' });
})();
