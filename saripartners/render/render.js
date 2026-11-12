#!/usr/bin/env node
// Bir içerik spesifikasyonundan (spec.json) Instagram görselleri üretir.
// Kullanım: node render.js <spec.json> [çıktı_klasörü]
// spec.format: "post" (1080x1350, 4:5) veya "reel" (1080x1920, 9:16)
// Slayt tipleri: kapak, metin, liste, kapanis
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const specPath = path.resolve(process.argv[2]);
const outDir = path.resolve(process.argv[3] || path.dirname(specPath));
const spec = JSON.parse(fs.readFileSync(specPath, 'utf8'));
const brand = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'marka.json'), 'utf8'));
const C = brand.renkler;
const W = 1080, H = spec.format === 'reel' ? 1920 : 1350;
const reel = spec.format === 'reel';

const esc = s => String(s ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
  .replace(/\*\*(.+?)\*\*/g, '<b>$1</b>').replace(/\n/g, '<br>');

function slideHtml(s, i, n) {
  const light = s.acik === true;
  const bg = light ? C.zemin_acik : C.zemin;
  const fg = light ? C.metin_koyu : C.metin;
  const pad = reel ? '220px 96px 260px' : '110px 96px';
  let inner = '';
  if (s.tip === 'kapak') {
    inner = `
      ${s.ust ? `<div class="kicker">${esc(s.ust)}</div>` : ''}
      <h1 class="cover">${esc(s.baslik)}</h1>
      ${s.alt ? `<p class="sub">${esc(s.alt)}</p>` : ''}
      ${s.ipucu ? `<div class="hint">${esc(s.ipucu)} →</div>` : ''}`;
  } else if (s.tip === 'metin') {
    inner = `
      ${s.ust ? `<div class="kicker">${esc(s.ust)}</div>` : ''}
      <h2>${esc(s.baslik)}</h2>
      <p class="body">${esc(s.govde)}</p>`;
  } else if (s.tip === 'liste') {
    inner = `
      ${s.ust ? `<div class="kicker">${esc(s.ust)}</div>` : ''}
      <h2>${esc(s.baslik)}</h2>
      <ul>${(s.maddeler || []).map(m => `<li>${esc(m)}</li>`).join('')}</ul>`;
  } else if (s.tip === 'kapanis') {
    inner = `
      <h2 class="end">${esc(s.baslik)}</h2>
      ${s.govde ? `<p class="body">${esc(s.govde)}</p>` : ''}
      <p class="note">${esc(s.not || brand.yasal_not)}</p>`;
  }
  const counter = n > 1 && !reel ? `<div class="count">${i + 1}/${n}</div>` : '';
  return `<!doctype html><html><head><meta charset="utf-8"><style>
    *{box-sizing:border-box;margin:0;padding:0}
    html,body{width:${W}px;height:${H}px;background:${bg};color:${fg};-webkit-font-smoothing:antialiased}
    body{font-family:'${brand.font_govde}',sans-serif;padding:${pad};display:flex;flex-direction:column;justify-content:${reel || s.tip === 'kapak' || s.tip === 'kapanis' ? 'center' : 'flex-start'};position:relative}
    .bar{position:absolute;left:96px;top:${reel ? 150 : 60}px;width:72px;height:8px;background:${C.vurgu}}
    .brand{position:absolute;left:96px;bottom:${reel ? 170 : 56}px;font-weight:700;letter-spacing:.24em;font-size:24px;color:${light ? C.metin_koyu : C.vurgu}}
    .count{position:absolute;right:96px;bottom:${reel ? 170 : 56}px;font-size:24px;color:${C.soluk};font-weight:600}
    .kicker{font-size:28px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:${C.vurgu};margin-bottom:36px}
    h1,h2{font-family:'${brand.font_baslik}',serif;font-weight:700;line-height:1.08;letter-spacing:-.01em}
    h1.cover{font-size:${reel ? 104 : 96}px}
    h2{font-size:${reel ? 76 : 68}px;margin-bottom:44px}
    h2.end{font-size:${reel ? 84 : 76}px}
    .sub{font-size:38px;line-height:1.35;margin-top:44px;color:${light ? '#3B4560' : '#D5DAE5'}}
    .body{font-size:${reel ? 44 : 40}px;line-height:1.45;color:${light ? '#2A334A' : '#E6E9F0'}}
    .body b,li b{color:${C.vurgu};font-weight:700}
    ul{list-style:none}
    li{font-size:${reel ? 42 : 38}px;line-height:1.4;padding-left:56px;position:relative;margin-bottom:30px;color:${light ? '#2A334A' : '#E6E9F0'}}
    li:before{content:'';position:absolute;left:0;top:.5em;width:24px;height:24px;background:${C.vurgu}}
    .hint{margin-top:64px;font-size:30px;font-weight:600;color:${C.vurgu}}
    .note{margin-top:56px;font-size:24px;line-height:1.45;color:${C.soluk};max-width:820px}
  </style></head><body><div class="bar"></div>${inner}<div class="brand">${esc(brand.ad)}</div>${counter}</body></html>`;
}

(async () => {
  fs.mkdirSync(outDir, { recursive: true });
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
  const n = spec.slaytlar.length;
  const files = [];
  for (let i = 0; i < n; i++) {
    await page.setContent(slideHtml(spec.slaytlar[i], i, n), { waitUntil: 'load' });
    await page.evaluate(() => document.fonts.ready);
    // Taşma kontrolü: içerik sayfaya sığmıyorsa hata ver.
    const overflow = await page.evaluate(() => document.body.scrollHeight > window.innerHeight + 1);
    if (overflow) console.error(`UYARI: ${i + 1}. slayt taşıyor, metni kısalt.`);
    const f = path.join(outDir, `${String(i + 1).padStart(2, '0')}.jpg`);
    await page.screenshot({ path: f, type: 'jpeg', quality: 92 });
    files.push(f);
  }
  await browser.close();
  console.log(files.join('\n'));
})();
