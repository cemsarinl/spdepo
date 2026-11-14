#!/usr/bin/env python3
"""Belirli bir tarih aralığındaki taslaklardan onay paketi (ONAY.md + onay/*.jpg) üretir.

Kullanım: python3 onay_paketi.py 2026-11-16 2026-11-22
"""
import datetime as dt
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
GUN = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
AY = ["", "Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
SERI = {"haklariniz": "Haftanın Gündemi · Haklarınız", "hollanda": "Hollanda'daki Türkler", "ictihat": "İçtihat Notu", "acil": "Acil Gündem",
        "haftalik-hukuk": "Hukuk Gündemi", "ozel-gun": "Özel Günler", "sozluk": "Hukuk Sözlüğü",
        "rehber": "Alan Rehberi", "repost": "Bu Senin Hakkın", "soru": "Doğru mu, Yanlış mı?", "global": "Yurt Dışından"}
FMT = {"carousel": "Kaydırmalı", "tek-gorsel": "Tek görsel", "reel": "Reels"}


def tr(d):
    return f"{d.day} {AY[d.month]} {GUN[d.weekday()]}"


def main(bas, son):
    b, s = dt.date.fromisoformat(bas), dt.date.fromisoformat(son)
    od = ROOT / "onay"
    od.mkdir(exist_ok=True)
    for f in od.glob("*.jpg"):
        f.unlink()
    rows, body = [], []
    items = []
    for d in sorted((ROOT / "icerik").iterdir()):
        if (d / "meta.json").exists():
            m = json.loads((d / "meta.json").read_text(encoding="utf-8"))
            t = dt.date.fromisoformat(m["tarih"])
            if b <= t <= s:
                items.append((d, m, t))
    for i, (d, m, t) in enumerate(items, 1):
        imgs = sorted(map(str, (d / "gorseller").glob("[0-9][0-9].jpg")))
        img = od / f"{i:02d}_{d.name}.jpg"
        if m["format"] == "reel":
            geo, tile = "270x480+6+6", f"{len(imgs)}x"
        else:
            geo, tile = "400x500+6+6", f"{min(len(imgs), 3)}x"
        subprocess.run(["montage", *imgs, "-tile", tile, "-geometry", geo, "-background", "#E8E2D6", str(img)], check=True)
        rel = img.relative_to(ROOT).as_posix()
        seri, fmt = SERI.get(m["tur"], m["tur"]), FMT[m["format"]]
        rows.append(f"| {i} | {tr(t)} {m.get('saat', '')} | {seri} | {fmt} | [önizleme]({rel}) |")
        cap = (d / "caption.txt").read_text(encoding="utf-8").strip()
        body += [f"## {i}. {tr(t)} · {seri} · {fmt}", "", f"![{d.name}]({rel})", "", "**Açıklama metni:**", "", "```", cap, "```", ""]
        if m.get("kaynak_permalink"):
            body += [f"**Kaynak gönderi:** {m['kaynak_permalink']}", ""]
        if m.get("not"):
            body += [f"**Not:** {m['not']}", ""]
        body += ["**Kontrol edilecekler:**", ""] + [f"- [ ] {x}" for x in (m.get("dogrulanacak") or ["Genel kontrol"])]
        body += ["", f"**Durum:** {'✅ Onaylandı' if m.get('hukukcu_onayi') else '⏳ Onay bekliyor'}", "", "---", ""]
    head = [f"# Onay paketi: {tr(b)} – {tr(s)}", "",
            "Onaylamak için sohbete gönderilerin tarihlerini yazmanız yeterli, örneğin **\"16, 17 ve 18 Kasım'ı onaylıyorum\"**. "
            "Düzeltme isterseniz tarihi ve değişikliği yazın. Onaylanan gönderiler planlanan gün sabah 09:50'de yayınlanır.", "",
            "| # | Tarih | Seri | Format | Önizleme |", "|---|---|---|---|---|"]
    (ROOT / "ONAY.md").write_text("\n".join(head + rows + ["", ""] + body), encoding="utf-8")
    print("\n".join(rows))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(*sys.argv[1:])
