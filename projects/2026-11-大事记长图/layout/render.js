// 用法：先在本目录 python3 -m http.server 8765 &，再 node render.js http://localhost:8765/sample_v2.html out/sample_v2.png（蒙版图必须走 http，file:// 会被 Chromium 拦）   （fonts/ 需指向下载好的 OFL 字体目录，见 README.md）
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const [src, out] = process.argv.slice(2);
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await p.goto(src.startsWith('http') ? src : 'file://' + path.resolve(src));
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(800);
  const fams = await p.evaluate(() => [...document.fonts].map(f => f.family + ':' + f.status));
  console.log('fonts', fams.join(' '));
  const h = await p.evaluate(() => document.body.offsetHeight);
  await p.screenshot({ path: out, fullPage: true, clip: { x: 0, y: 0, width: 1080, height: h } });
  console.log('height', h);
  await b.close();
})();
