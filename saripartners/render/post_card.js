#!/usr/bin/env node
// @buseninhakkin gönderisini "ekran görüntüsü" tarzında, Sarı tasarımlı 1080x1920 bir kart olarak çizer.
// Kullanım: node post_card.js <kart.json> <çıktı.png>
// kart.json: {kanca, kullanici, ad, aciklama, kapak (yerel dosya), avatar (yerel dosya, isteğe bağlı)}
const fs = require('fs');
const os = require('os');
const path = require('path');
const { chromium } = require('playwright');

const [specPath, out] = process.argv.slice(2);
const k = JSON.parse(fs.readFileSync(specPath, 'utf8'));
const ROOT = path.join(__dirname, '..');
const brand = JSON.parse(fs.readFileSync(path.join(ROOT, 'marka.json'), 'utf8'));
const C = brand.renkler;
const esc = s => String(s ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const fmt = s => esc(String(s).replace(/\\n/g, '\n')).replace(/\*(.+?)\*/g, '<em>$1</em>').replace(/\n/g, '<br>');
const file = p => 'file://' + path.resolve(path.dirname(specPath), p);

const html = `<!doctype html><html><head><meta charset="utf-8"><style>
@import url('file://${path.join(ROOT, 'marka', 'fonts', 'fonts.css')}');
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px}
body{background:${C.antrasit};color:${C.krem};font-family:'Manrope',sans-serif;position:relative;overflow:hidden;
  display:flex;flex-direction:column;justify-content:center;gap:40px;padding:250px 92px 440px}
body:before{content:'';position:absolute;inset:0;background:radial-gradient(900px 800px at 100% 8%, rgba(225,176,67,.16), transparent 70%),
  repeating-linear-gradient(135deg, rgba(255,255,255,.025) 0 1px, transparent 1px 14px)}
.wm{position:absolute;right:-30px;bottom:300px;font-family:'Playfair Display',serif;font-weight:700;font-size:420px;line-height:1;
  color:transparent;-webkit-text-stroke:2px rgba(244,239,228,.05)}
.badge,h1,.card,.cta{flex-shrink:0}
.badge{position:relative;align-self:flex-start;display:inline-flex;align-items:center;gap:14px;background:rgba(255,255,255,.1);
  border:1px solid rgba(255,255,255,.16);border-radius:999px;padding:14px 26px;font-size:26px;font-weight:600}
.badge i{width:12px;height:12px;border-radius:50%;background:${C.altin_acik};box-shadow:0 0 0 6px rgba(225,176,67,.2)}
h1{position:relative;font-family:'Playfair Display',serif;font-weight:700;font-size:84px;line-height:1.06;
  letter-spacing:-.015em;color:#fff}
h1 em{font-style:italic;color:${C.altin_acik}}
.card{position:relative;width:820px;align-self:center;margin:10px 0;background:#fff;border-radius:36px;overflow:hidden;color:${C.antrasit};
  box-shadow:0 40px 90px -30px rgba(0,0,0,.6), 0 0 0 1px rgba(255,255,255,.08);transform:rotate(-1.5deg)}
.hd{display:flex;align-items:center;gap:18px;padding:22px 26px}
.av{width:64px;height:64px;border-radius:50%;object-fit:cover;box-shadow:0 0 0 3px #fff, 0 0 0 5px ${C.altin}}
.ini{background:${C.altin};color:#fff;display:grid;place-items:center;font-family:'Playfair Display',serif;font-weight:700;font-size:34px}
.hd b{display:block;font-size:28px;font-weight:700}
.hd span{font-size:22px;color:${C.gri}}
.ph{position:relative;height:500px;background:#000}
.ph img{width:100%;height:100%;object-fit:cover;object-position:50% 30%}
.pl{position:absolute;left:50%;top:50%;width:120px;height:120px;margin:-60px 0 0 -60px;border-radius:50%;background:rgba(30,36,39,.55);
  border:3px solid rgba(255,255,255,.9);display:grid;place-items:center;color:#fff;font-size:48px;padding-left:8px}
.tag{position:absolute;left:20px;top:20px;background:rgba(30,36,39,.7);color:#fff;font-size:20px;font-weight:700;border-radius:10px;padding:8px 14px;letter-spacing:.04em}
.cp{padding:22px 26px 28px;font-size:26px;line-height:1.45;color:#3B4247;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}
.cp b{color:${C.antrasit}}
.cta{position:relative;display:flex;align-items:center;gap:18px;font-size:30px;font-weight:600}
.cta span{width:64px;height:64px;border-radius:50%;background:${C.altin_acik};color:${C.antrasit};display:grid;place-items:center;font-size:28px}
.cta em{font-style:normal;color:${C.altin_acik}}
.foot{position:absolute;right:92px;bottom:330px}
.chip{background:${C.krem_acik};border-radius:18px;padding:8px 16px;display:inline-block}
.chip img{height:72px;display:block;mix-blend-mode:multiply}
</style></head><body>
<div class="wm">Sarı</div>
<div class="badge"><i></i>Bu Senin Hakkın · Yeni video</div>
<h1>${fmt(k.kanca)}</h1>
<div class="card">
  <div class="hd">${k.avatar ? `<img class="av" src="${file(k.avatar)}">` : `<div class="av ini">${esc((k.ad || k.kullanici || '?').trim()[0])}</div>`}<div><b>${esc(k.kullanici)}</b><span>${esc(k.ad || '')}</span></div></div>
  <div class="ph"><img src="${file(k.kapak)}"><div class="tag">REELS</div><div class="pl">▶</div></div>
  <div class="cp"><b>${esc(k.kullanici)}</b> ${esc(k.aciklama)}</div>
</div>
<div class="cta"><span>▶</span><p>Videonun tamamı <em>@${esc(k.kullanici)}</em> hesabında</p></div>
<div class="foot"><div class="chip"><img src="file://${path.join(ROOT, brand.logo)}"></div></div>
</body></html>`;

(async () => {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'spc-'));
  const f = path.join(tmp, 'c.html');
  fs.writeFileSync(f, html);
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto('file://' + f, { waitUntil: 'load' });
  await p.evaluate(() => document.fonts.ready);
  const r = await p.evaluate(() => ({ top: document.querySelector('.badge').getBoundingClientRect().top,
    cta: document.querySelector('.cta').getBoundingClientRect().bottom }));
  if (r.top < 240 || r.cta > 1500) console.error('UYARI: içerik sığmıyor; kanca metnini kısaltın.');
  await p.screenshot({ path: out, type: out.endsWith('.png') ? 'png' : 'jpeg' });
  await b.close();
  fs.rmSync(tmp, { recursive: true, force: true });
  console.log(out);
})();
