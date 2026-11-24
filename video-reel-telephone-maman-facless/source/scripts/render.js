const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const FPS = 30;
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await page.goto('file://' + __dirname + '/index.html');
  await page.evaluate(() => document.fonts.ready);
  const TOTAL = await page.evaluate(() => window.TOTAL);
  const N = Math.ceil(FPS * TOTAL);
  fs.mkdirSync(__dirname + '/frames', { recursive: true });
  const sfx = await page.evaluate(() => window.SFX);
  fs.writeFileSync(__dirname + '/sfx.json', JSON.stringify(sfx));
  for (let i = 0; i < N; i++) {
    const t = i / FPS;
    await page.evaluate(x => window.render(x), t);
    await page.screenshot({ path: `${__dirname}/frames/${String(i).padStart(5, '0')}.jpg`, type: 'jpeg', quality: 90 });
    if (i % 300 === 0) console.log('frame', i, 'of', N);
  }
  console.log('DONE');
  await browser.close();
})().catch(e => { console.error('ERR', e); process.exit(1); });
