// 用法：node render.js sample_v1.html out/sample_v1.png   （fonts/ 需指向下载好的 OFL 字体目录，见 README.md）
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const [src, out] = process.argv.slice(2);
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await p.goto('file://' + path.resolve(src));
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(800);
  const fams = await p.evaluate(() => [...document.fonts].map(f => f.family + ':' + f.status));
  console.log('fonts', fams.join(' '));
  await p.screenshot({ path: out, fullPage: true });
  const h = await p.evaluate(() => document.body.scrollHeight);
  console.log('height', h);
  await b.close();
})();
