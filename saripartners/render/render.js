#!/usr/bin/env node
// Sarı Avukatlık Ortaklığı: Instagram görsel üreticisi (saripartners.com tasarım dili).
// Kullanım: node render.js <spec.json> [çıktı_klasörü]
//
// spec alanları:
//   format : "post" (1080x1350) | "reel" (1080x1920)
//   seri   : marka.json > seriler anahtarı (gundem, rehber, sozluk, soru, ozel, global)
//   etiket : rozet metni (varsayılan: seri adı), ör. "Miras Hukuku · Rehber"
//   tema   : "krem" (varsayılan) | "koyu"; slayt bazında "tema" ile değiştirilebilir
//   slaytlar: [...]
//
// Slayt tipleri:
//   kapak    {baslik, alt?, ipucu?}
//   ozel     {gun, ay, baslik, alt?}                    büyük tarihli özel gün kapağı
//   metin    {ust?, baslik, govde}
//   liste    {ust?, baslik, maddeler[] | kartlar[{baslik, govde}]}
//   kart     {ust?, baslik?, alinti, kaynak?}           madde/karar alıntısı
//   sozluk   {terim, okunus?, tanim, kaynak?}
//   soru     {ifade, cevap: "Doğru"|"Yanlış"|"Kısmen", aciklama}
//   kapanis  {baslik, govde?, not?}
//
// Metin biçimi: *italik altın* (başlıklarda vurgu), **kalın altın** (gövdede vurgu), \n satır sonu.
const fs = require('fs');
const os = require('os');
const path = require('path');
const { chromium } = require('playwright');

const ROOT = path.join(__dirname, '..');
const specPath = path.resolve(process.argv[2]);
const outDir = path.resolve(process.argv[3] || path.join(path.dirname(specPath), 'gorseller'));
const spec = JSON.parse(fs.readFileSync(specPath, 'utf8'));
const brand = JSON.parse(fs.readFileSync(path.join(ROOT, 'marka.json'), 'utf8'));
const C = brand.renkler;
const reel = spec.format === 'reel';
const W = 1080, H = reel ? 1920 : 1350;
const FONTS = 'file://' + path.join(ROOT, 'marka', 'fonts', 'fonts.css');
const LOGO = 'file://' + path.join(ROOT, brand.logo);
const seriAdi = brand.seriler[spec.seri] || '';
const etiket = spec.etiket || seriAdi;

const esc = s => String(s ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const fmt = s => esc(s)
  .replace(/\*\*(.+?)\*\*/g, '<b>$1</b>')
  .replace(/\*(.+?)\*/g, '<em>$1</em>')
  .replace(/\n/g, '<br>');
const nn = i => String(i).padStart(2, '0');

// Logodaki petekten türetilmiş altıgen motif (sivri uçlu altıgen).
function hex(cx, cy, r, stroke, op, fill = 'none') {
  const pts = [...Array(6)].map((_, k) => {
    const a = Math.PI / 180 * (60 * k - 90);
    return `${(cx + r * Math.cos(a)).toFixed(1)},${(cy + r * Math.sin(a)).toFixed(1)}`;
  }).join(' ');
  return `<polygon points="${pts}" fill="${fill}" stroke="${stroke}" stroke-width="2" opacity="${op}"/>`;
}
function honeycomb(dark) {
  const s = dark ? C.altin_acik : C.altin, r = 120, w = r * Math.sqrt(3);
  return `<svg class="hc" width="420" height="480" viewBox="0 0 420 480">
    ${hex(300, 130, r, s, dark ? .22 : .28)}${hex(300 - w / 2, 130 + r * 1.5, r, s, dark ? .16 : .2)}
    ${hex(300 + w / 2, 130 + r * 1.5, r, s, dark ? .1 : .12)}${hex(300, 130, r * .42, s, dark ? .5 : .55, s)}</svg>`;
}

function css(dark) {
  const bg = dark ? C.antrasit : C.krem;
  const ink = dark ? C.krem : C.antrasit;
  const sub = dark ? '#B9BCBE' : C.gri;
  const acc = dark ? C.altin_acik : C.altin;
  const P = reel ? { t: 400, b: 440 } : { t: 120, b: 150 };
  return `
  @import url('${FONTS}');
  *{box-sizing:border-box;margin:0;padding:0}
  html,body{width:${W}px;height:${H}px}
  body{background:${bg};color:${ink};font-family:'Manrope',sans-serif;-webkit-font-smoothing:antialiased;
       position:relative;overflow:hidden;padding:${P.t}px 92px ${P.b}px;display:flex;flex-direction:column;justify-content:center}
  body:before{content:'';position:absolute;inset:0;pointer-events:none;${spec.stil === 'vurucu' ? 'display:none;' : ''}
       background:radial-gradient(900px 700px at 100% 0%, ${dark ? 'rgba(225,176,67,.10)' : 'rgba(225,176,67,.22)'}, transparent 70%),
                  repeating-linear-gradient(135deg, ${dark ? 'rgba(255,255,255,.025)' : 'rgba(184,137,43,.05)'} 0 1px, transparent 1px 14px)}
  .hc{position:absolute;right:-40px;top:${reel ? 230 : -40}px}
  .wm{position:absolute;right:-30px;bottom:${reel ? 300 : 40}px;font-family:'Playfair Display',serif;font-weight:700;font-size:420px;
      line-height:1;color:transparent;-webkit-text-stroke:2px ${dark ? 'rgba(244,239,228,.06)' : 'rgba(30,36,39,.06)'};letter-spacing:-.02em}
  .badge{position:absolute;left:92px;top:${reel ? 290 : 64}px;display:inline-flex;align-items:center;gap:14px;
      background:${dark ? 'rgba(255,255,255,.08)' : 'rgba(255,255,255,.82)'};border:1px solid ${dark ? 'rgba(255,255,255,.12)' : 'rgba(184,137,43,.18)'};
      border-radius:999px;padding:14px 26px;font-size:24px;font-weight:600;color:${dark ? C.krem : C.antrasit};letter-spacing:.01em}
  .badge i{width:12px;height:12px;border-radius:50%;background:${acc};box-shadow:0 0 0 6px ${dark ? 'rgba(225,176,67,.18)' : 'rgba(184,137,43,.15)'}}
  .foot{position:absolute;left:92px;right:92px;bottom:${reel ? 310 : 56}px;display:flex;align-items:center;justify-content:space-between}
  .logo{height:${reel ? 84 : 76}px;display:block}
  .logo.m{mix-blend-mode:multiply}
  .chip{background:${C.krem_acik};border-radius:20px;padding:10px 18px}
  .count{font-size:24px;font-weight:600;color:${sub};display:flex;align-items:center;gap:14px}
  .count b{color:${acc};font-weight:700}
  .count:before{content:'';width:48px;height:2px;background:${acc}}
  .kick{font-size:26px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:${acc};margin-bottom:30px}
  h1,h2,.term{font-family:'Playfair Display',serif;font-weight:600;letter-spacing:-.015em;color:${ink}}
  h1{font-size:${reel ? 108 : 100}px;line-height:1.04}
  h2{font-size:${reel ? 76 : 68}px;line-height:1.1;margin-bottom:40px}
  h1 em,h2 em,.term em{font-style:italic;color:${acc}}
  .sub{font-size:36px;line-height:1.5;color:${sub};margin-top:44px;max-width:860px}
  .body{font-size:${reel ? 42 : 38}px;line-height:1.55;color:${sub}}
  .body b,.item b,.card b{color:${dark ? C.altin_acik : C.antrasit};font-weight:700;
      background:linear-gradient(transparent 62%, ${dark ? 'rgba(225,176,67,.25)' : 'rgba(225,176,67,.35)'} 62%)}
  .hint{margin-top:64px;display:inline-flex;align-items:center;gap:16px;font-size:28px;font-weight:600;color:${ink}}
  .hint span{width:64px;height:64px;border-radius:50%;background:${acc};color:#fff;display:grid;place-items:center;font-size:30px}
  .items{display:flex;flex-direction:column;gap:${reel ? 34 : 26}px}
  .item{display:flex;gap:30px;align-items:flex-start;font-size:${reel ? 40 : 36}px;line-height:1.45;color:${sub}}
  .num{flex:none;width:68px;height:68px;border-radius:50%;background:${acc};color:#fff;display:grid;place-items:center;
      font-family:'Playfair Display',serif;font-size:28px;box-shadow:0 0 0 8px ${dark ? 'rgba(225,176,67,.15)' : 'rgba(184,137,43,.14)'}}
  .item p{padding-top:8px}
  .card{background:${dark ? 'rgba(255,255,255,.06)' : '#fff'};border-radius:28px;padding:40px 44px;border-left:6px solid ${acc};
      box-shadow:${dark ? 'none' : '0 24px 60px -30px rgba(30,36,39,.25)'};font-size:${reel ? 38 : 34}px;line-height:1.5;color:${sub}}
  .card h3{font-family:'Playfair Display',serif;font-weight:600;font-size:${reel ? 44 : 40}px;color:${ink};margin-bottom:12px}
  .cards{display:flex;flex-direction:column;gap:24px}
  .quote{font-family:'Playfair Display',serif;font-style:italic;font-size:${reel ? 48 : 44}px;line-height:1.4;color:${ink}}
  .src{margin-top:28px;font-size:26px;font-weight:600;color:${acc};letter-spacing:.02em}
  .term{font-size:${reel ? 132 : 120}px;line-height:1}
  .say{font-size:30px;color:${sub};margin-top:20px;font-style:italic}
  .rule{width:96px;height:4px;background:${acc};margin:48px 0}
  .date{display:flex;align-items:flex-end;gap:28px;margin-bottom:48px}
  .date .d{font-family:'Playfair Display',serif;font-weight:700;font-size:${reel ? 300 : 260}px;line-height:.8;color:${acc}}
  .date .m{font-size:40px;font-weight:700;letter-spacing:.2em;text-transform:uppercase;padding-bottom:14px}
  .verdict{display:inline-flex;align-items:center;gap:14px;border-radius:999px;padding:14px 30px;font-size:30px;font-weight:800;
      letter-spacing:.08em;text-transform:uppercase;margin-bottom:36px;color:#fff;background:${acc}}
  /* --- vurucu stil --- */
  .q{font-size:${reel ? 48 : 44}px;font-weight:600;line-height:1.3;color:${sub};margin-bottom:28px}
  .big{font-family:'Manrope',sans-serif;font-weight:800;font-size:${reel ? 132 : 122}px;line-height:1.1;letter-spacing:-.03em;color:${ink}}
  .big b{color:${acc}}
  .after{margin-top:40px;font-size:${reel ? 46 : 42}px;font-weight:700;color:${acc}}
  .ans{display:flex;flex-direction:column;gap:${reel ? 56 : 48}px}
  .ans .h{font-weight:800;font-size:${reel ? 88 : 80}px;line-height:1;letter-spacing:-.02em;color:${ink}}
  .ans .h span{color:${acc}}
  .ans .d{margin-top:14px;font-size:${reel ? 40 : 36}px;line-height:1.35;color:${sub};font-weight:500}
  .steps{display:flex;flex-direction:column;gap:${reel ? 40 : 34}px}
  .steps div{font-size:${reel ? 54 : 50}px;font-weight:800;line-height:1.15;color:${ink};padding-left:44px;position:relative}
  .steps div:before{content:'';position:absolute;left:0;top:.42em;width:20px;height:20px;border-radius:50%;background:${acc}}
  .steps div small{display:block;font-size:${reel ? 34 : 30}px;font-weight:500;color:${sub};margin-top:6px}
  .src2{margin-top:56px;font-size:22px;line-height:1.45;color:${sub};opacity:.8;max-width:860px}
  .note{margin-top:48px;font-size:24px;line-height:1.5;color:${sub};max-width:820px;opacity:.85}
  `;
}

function slide(s, i, n) {
  const dark = (s.tema || spec.tema) === 'koyu';
  const kick = s.ust ? `<div class="kick">${fmt(s.ust)}</div>` : '';
  let inner = '';
  switch (s.tip) {
    case 'kapak':
      inner = `${kick}<h1>${fmt(s.baslik)}</h1>${s.alt ? `<p class="sub">${fmt(s.alt)}</p>` : ''}
        ${s.ipucu ? `<div class="hint">${esc(s.ipucu)}<span>→</span></div>` : ''}`; break;
    case 'ozel':
      inner = `<div class="date"><div class="d">${esc(s.gun)}</div><div class="m">${esc(s.ay)}</div></div>
        <h1>${fmt(s.baslik)}</h1>${s.alt ? `<p class="sub">${fmt(s.alt)}</p>` : ''}`; break;
    case 'metin':
      inner = `${kick}<h2>${fmt(s.baslik)}</h2><p class="body">${fmt(s.govde)}</p>`; break;
    case 'liste':
      inner = `${kick}<h2>${fmt(s.baslik)}</h2>` + (s.kartlar
        ? `<div class="cards">${s.kartlar.map(k => `<div class="card"><h3>${fmt(k.baslik)}</h3>${fmt(k.govde)}</div>`).join('')}</div>`
        : `<div class="items">${s.maddeler.map((m, k) => `<div class="item"><div class="num">${nn(k + 1)}</div><p>${fmt(m)}</p></div>`).join('')}</div>`);
      break;
    case 'kart':
      inner = `${kick}${s.baslik ? `<h2>${fmt(s.baslik)}</h2>` : ''}<div class="card"><div class="quote">“${fmt(s.alinti)}”</div>
        ${s.kaynak ? `<div class="src">${fmt(s.kaynak)}</div>` : ''}</div>`; break;
    case 'sozluk':
      inner = `<div class="term">${fmt(s.terim)}</div>
        ${s.okunus ? `<div class="say">${esc(s.okunus)}</div>` : ''}<div class="rule"></div>
        <p class="body">${fmt(s.tanim)}</p>${s.kaynak ? `<div class="src">${fmt(s.kaynak)}</div>` : ''}`; break;
    case 'soru':
      inner = s.cevap
        ? `<div><span class="verdict">${esc(s.cevap)}</span></div><h2>${fmt(s.ifade)}</h2><p class="body">${fmt(s.aciklama)}</p>`
        : `<div class="kick">Doğru mu, yanlış mı?</div><h1>“${fmt(s.ifade)}”</h1>${s.ipucu ? `<div class="hint">${esc(s.ipucu)}<span>→</span></div>` : ''}`;
      break;
    case 'vurgu':
      inner = `${s.soru ? `<div class="q">${fmt(s.soru)}</div>` : ''}<div class="big">${fmt(s.buyuk)}</div>
        ${s.sonra ? `<div class="after">${fmt(s.sonra)}</div>` : ''}`; break;
    case 'cevap':
      inner = `${s.soru ? `<div class="q">${fmt(s.soru)}</div>` : ''}<div class="ans">${s.cevaplar.map((c, k) =>
        `<div><div class="h"><span>${k + 1}.</span> ${fmt(c.baslik)}</div><div class="d">${fmt(c.aciklama)}</div></div>`).join('')}</div>`; break;
    case 'adimlar':
      inner = `${s.soru ? `<div class="q">${fmt(s.soru)}</div>` : ''}<div class="steps">${s.maddeler.map(m =>
        `<div>${fmt(m.baslik)}${m.aciklama ? `<small>${fmt(m.aciklama)}</small>` : ''}</div>`).join('')}</div>
        <div class="src2">${fmt(s.kaynak ? s.kaynak + ' ' : '')}${fmt(brand.yasal_not)}</div>`; break;
    case 'kapanis':
      inner = `<h2>${fmt(s.baslik)}</h2>${s.govde ? `<p class="body">${fmt(s.govde)}</p>` : ''}
        <p class="note">${fmt(s.not || brand.yasal_not)}</p>`; break;
    default: throw new Error('Bilinmeyen slayt tipi: ' + s.tip);
  }
  const logo = dark ? `<div class="chip"><img class="logo m" src="${LOGO}"></div>` : `<img class="logo m" src="${LOGO}">`;
  const count = n > 1 && !reel ? `<div class="count"><b>${nn(i + 1)}</b> / ${nn(n)}</div>` : '';
  return `<!doctype html><html><head><meta charset="utf-8"><style>${css(dark)}</style></head><body>
    ${spec.stil === 'vurucu' ? '' : honeycomb(dark) + '<div class="wm">Sarı</div>'}
    ${etiket ? `<div class="badge"><i></i>${esc(etiket)}</div>` : ''}
    <main>${inner}</main>
    <div class="foot">${logo}${count}</div></body></html>`;
}

(async () => {
  fs.mkdirSync(outDir, { recursive: true });
  for (const f of fs.readdirSync(outDir)) if (/^\d\d\.jpg$/.test(f)) fs.unlinkSync(path.join(outDir, f));
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'sp-'));
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
  const n = spec.slaytlar.length, files = [];
  for (let i = 0; i < n; i++) {
    const htmlFile = path.join(tmp, `${i}.html`);
    fs.writeFileSync(htmlFile, slide(spec.slaytlar[i], i, n));
    await page.goto('file://' + htmlFile, { waitUntil: 'load' });
    await page.evaluate(() => document.fonts.ready);
    // Taşma kontrolü: içerik rozet ile alt bilgi arasına sığmalı.
    const clash = await page.evaluate(() => {
      const m = document.querySelector('main').getBoundingClientRect();
      const f = document.querySelector('.foot').getBoundingClientRect();
      const b = document.querySelector('.badge')?.getBoundingClientRect();
      return m.bottom > f.top - 24 || (b && m.top < b.bottom + 24);
    });
    if (clash) console.error(`UYARI: ${path.basename(path.dirname(specPath))} ${i + 1}. slayt sığmıyor, metni kısaltın.`);
    const f = path.join(outDir, `${nn(i + 1)}.jpg`);
    await page.screenshot({ path: f, type: 'jpeg', quality: 93 });
    files.push(f);
  }
  await browser.close();
  fs.rmSync(tmp, { recursive: true, force: true });
  console.log(files.join('\n'));
})();
