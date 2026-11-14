#!/usr/bin/env node
// Repost Reels için Sarı tasarımında iki katman üretir (1080x1920 PNG):
//   intro.png : açılış kartı (ilk ~2,5 sn; aynı zamanda kapak)
//   bar.png   : video boyunca üstte kalan ince kanca şeridi (yüzü ve altyazıyı kapatmaz)
// Kullanım: node repost_overlay.js "<kanca metni>" <kaynak_hesap> <çıktı_klasörü>
// Kanca metninde *italik altın* vurgu ve \n satır sonu kullanılabilir. 2–6 kelime önerilir.
const fs = require('fs');
const os = require('os');
const path = require('path');
const { chromium } = require('playwright');

const [hookRaw, source, outDir] = process.argv.slice(2);
const hook = String(hookRaw || '').replace(/\\n/g, '\n');
if (!hook || !outDir) { console.error('Kullanım: node repost_overlay.js "<metin>" <hesap> <klasör>'); process.exit(1); }
const ROOT = path.join(__dirname, '..');
const brand = JSON.parse(fs.readFileSync(path.join(ROOT, 'marka.json'), 'utf8'));
const C = brand.renkler;
const FONTS = `@import url('file://${path.join(ROOT, 'marka', 'fonts', 'fonts.css')}');`;
const LOGO = 'file://' + path.join(ROOT, brand.logo);
const fmt = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
  .replace(/\*(.+?)\*/g, '<em>$1</em>');
const acc = '@' + String(source || 'buseninhakkin').replace(/^@/, '');

const base = `*{margin:0;padding:0;box-sizing:border-box}html,body{width:1080px;height:1920px;background:transparent}
body{position:relative;font-family:'Manrope',sans-serif;overflow:hidden}
em{font-style:italic;color:${C.altin_acik}}
.chip{background:${C.krem_acik};border-radius:18px;padding:8px 16px;display:inline-block}
.chip img{display:block;mix-blend-mode:multiply}`;

const intro = `<!doctype html><html><head><meta charset="utf-8"><style>${FONTS}${base}
body{background:rgba(30,36,39,.9)}
body:before{content:'';position:absolute;inset:0;background:radial-gradient(900px 800px at 100% 10%, rgba(225,176,67,.16), transparent 70%),
  repeating-linear-gradient(135deg, rgba(255,255,255,.025) 0 1px, transparent 1px 14px)}
.badge{position:absolute;left:92px;top:290px;display:inline-flex;align-items:center;gap:14px;background:rgba(255,255,255,.1);
  border:1px solid rgba(255,255,255,.16);border-radius:999px;padding:14px 26px;font-size:26px;font-weight:600;color:${C.krem}}
.badge i{width:12px;height:12px;border-radius:50%;background:${C.altin_acik};box-shadow:0 0 0 6px rgba(225,176,67,.2)}
main{position:absolute;left:92px;right:92px;top:0;bottom:0;display:flex;flex-direction:column;justify-content:center}
.bar{width:96px;height:6px;background:${C.altin_acik};margin-bottom:44px}
h1{font-family:'Playfair Display',serif;font-weight:700;font-size:118px;line-height:1.04;letter-spacing:-.015em;color:#fff}
.play{margin-top:64px;display:inline-flex;align-items:center;gap:18px;font-size:30px;font-weight:600;color:${C.krem}}
.play span{width:72px;height:72px;border-radius:50%;background:${C.altin_acik};display:grid;place-items:center;color:${C.antrasit};font-size:30px}
.wm{position:absolute;right:-30px;bottom:320px;font-family:'Playfair Display',serif;font-weight:700;font-size:420px;line-height:1;
  color:transparent;-webkit-text-stroke:2px rgba(244,239,228,.06)}
.foot{position:absolute;left:92px;bottom:330px}
</style></head><body><div class="wm">Sarı</div><div class="badge"><i></i>Bu Senin Hakkın · ${fmt(acc)}</div>
<main><div class="bar"></div><h1>${fmt(hook).replace(/\n/g, '<br>')}</h1><div class="play"><span>▶</span>İzleyin</div></main>
<div class="foot"><div class="chip"><img src="${LOGO}" style="height:80px"></div></div></body></html>`;

const one = fmt(hook).replace(/\n/g, ' ');
const bar = `<!doctype html><html><head><meta charset="utf-8"><style>${FONTS}${base}
.band{position:absolute;left:0;right:0;top:150px;height:132px;background:linear-gradient(90deg, rgba(30,36,39,.92), rgba(30,36,39,.82));
  display:flex;align-items:center;gap:28px;padding:0 40px 0 0;border-bottom:3px solid ${C.altin_acik}}
.band .acc{width:10px;align-self:stretch;background:${C.altin_acik}}
.band h2{flex:1;font-family:'Playfair Display',serif;font-weight:600;font-size:50px;line-height:1.1;color:#fff;white-space:nowrap;
  overflow:hidden;text-overflow:clip}
</style></head><body><div class="band"><div class="acc"></div><h2 id="h">${one}</h2>
<div class="chip"><img src="${LOGO}" style="height:56px"></div></div></body></html>`;

(async () => {
  fs.mkdirSync(outDir, { recursive: true });
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'spo-'));
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  for (const [name, html] of [['intro', intro], ['bar', bar]]) {
    const f = path.join(tmp, name + '.html');
    fs.writeFileSync(f, html);
    await p.goto('file://' + f);
    await p.evaluate(() => document.fonts.ready);
    if (name === 'bar') {
      // Tek satıra sığana kadar yazı boyutunu küçült.
      const size = await p.evaluate(() => {
        const h = document.getElementById('h'); let s = 50;
        while (h.scrollWidth > h.clientWidth && s > 30) { s -= 2; h.style.fontSize = s + 'px'; }
        return s;
      });
      if (size <= 30) console.error('UYARI: kanca metni şeride sığmıyor; kısaltın.');
    } else {
      const bottom = await p.evaluate(() => document.querySelector('.play').getBoundingClientRect().bottom);
      if (bottom > 1560) console.error('UYARI: açılış kartındaki metin çok uzun; kısaltın.');
    }
    await p.screenshot({ path: path.join(outDir, name + '.png'), omitBackground: true });
  }
  await b.close();
  fs.rmSync(tmp, { recursive: true, force: true });
  console.log(outDir);
})();
