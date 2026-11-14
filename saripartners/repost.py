#!/usr/bin/env python3
"""@buseninhakkin videolarını @saripartners'ta Sarı tasarımlı Reels olarak yeniden paylaşma aracı.

Kullanım:
  python3 repost.py kontrol                       # yeni (henüz işlenmemiş) videoları listeler
  python3 repost.py hazirla <medya_id> <tarih> <kisa-ad> "<kanca metni>"
                                                  # videoyu indirir, kanca metnini ekler, taslak klasörü kurar
  python3 repost.py isaretle <medya_id> [atlandi] # videoyu işlenmiş olarak kaydeder

Notlar:
- Instagram API'sinde yerleşik "repost" yoktur. Video indirilir, üzerine Sarı tasarımlı kanca
  metni eklenir ve @saripartners'ta yeni bir Reels olarak yayınlanır; açıklamada kaynak belirtilir.
- Telifli müzik içeren videolarda API video adresi vermez. Bu videolar atlanır.
- Taslaklar diğer içerikler gibi onaydan (hukukcu_onayi) geçmeden yayınlanmaz.
"""
import json
import subprocess
import sys
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STATE = ROOT / "repost" / "durum.json"
MARKA = json.loads((ROOT / "marka.json").read_text(encoding="utf-8"))
KAYNAK = MARKA.get("repost_kaynak", "buseninhakkin")
FIELDS = ("business_discovery.username(%s){media.limit(25){id,caption,media_type,media_product_type,"
          "permalink,timestamp,media_url,thumbnail_url,like_count,comments_count}}" % KAYNAK)


def state():
    if STATE.exists():
        return json.loads(STATE.read_text(encoding="utf-8"))
    return {"islenen": {}, "baslangic": "2026-11-01"}


def save(s):
    STATE.parent.mkdir(exist_ok=True)
    STATE.write_text(json.dumps(s, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def media():
    url = (f"https://{MARKA.get('graph_host', 'graph.facebook.com')}/v23.0/{MARKA['instagram_user_id']}?"
           + urllib.parse.urlencode({"fields": FIELDS}))
    with urllib.request.urlopen(url, timeout=60) as r:
        return json.loads(r.read())["business_discovery"]["media"]["data"]


def kontrol():
    s = state()
    yeni = [m for m in media() if m["media_type"] == "VIDEO" and m["id"] not in s["islenen"]
            and m["timestamp"][:10] >= s["baslangic"]]
    if not yeni:
        print("Yeni video yok.")
    for m in yeni:
        uygun = "uygun" if m.get("media_url") else "ATLANACAK (video adresi yok, muhtemelen telifli müzik)"
        print(f"{m['id']}  {m['timestamp'][:10]}  ♥{m.get('like_count')}  {m['permalink']}  [{uygun}]")
        print("   " + (m.get("caption") or "").split("\n")[0][:160])
    return yeni


def hazirla(mid, tarih, ad, kanca):
    m = next((x for x in media() if x["id"] == mid), None)
    if not m or not m.get("media_url"):
        sys.exit("Video bulunamadı ya da video adresi yok.")
    d = ROOT / "icerik" / f"{tarih}_repost-{ad}"
    (d / "gorseller").mkdir(parents=True, exist_ok=True)
    src = d / "kaynak.mp4"   # .gitignore ile depoya girmez
    urllib.request.urlretrieve(m["media_url"], src)
    subprocess.run([sys.executable, str(ROOT / "render" / "make_repost.py"), str(src), kanca, str(d / "reel.mp4"),
                    "--hesap", KAYNAK, "--kapak", str(d / "gorseller" / "01.jpg")], check=True)
    ilk = (m.get("caption") or "").split("\n")[0].strip()
    (d / "caption.txt").write_text(
        f"{ilk}\n\n🎥 Videonun tamamı ve daha fazlası için: @{KAYNAK}\n\n"
        f"Bu paylaşım genel bilgilendirme amaçlıdır; hukuki görüş veya tavsiye niteliği taşımaz.\n\n"
        f"#BuSeninHakkın #SarıAvukatlıkOrtaklığı\n", encoding="utf-8")
    (d / "meta.json").write_text(json.dumps({
        "tarih": tarih, "saat": "10:00", "tur": "repost", "format": "reel",
        "durum": "taslak", "hukukcu_onayi": False, "kanca": kanca,
        "kaynak_medya_id": mid, "kaynak_permalink": m["permalink"], "kaynak_tarih": m["timestamp"],
        "dogrulanacak": ["Kanca metni videonun içeriğiyle örtüşüyor mu?",
                         "Videoda telifli müzik varsa Instagram sesi kapatabilir; kontrol edin."]
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    s = state(); s["islenen"][mid] = {"durum": "taslak", "klasor": d.name}; save(s)
    print(d)


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[:1] == ["kontrol"]:
        kontrol()
    elif a[:1] == ["hazirla"] and len(a) == 5:
        hazirla(*a[1:])
    elif a[:1] == ["isaretle"] and len(a) >= 2:
        s = state(); s["islenen"][a[1]] = {"durum": a[2] if len(a) > 2 else "islendi"}; save(s); print("kaydedildi")
    else:
        sys.exit(__doc__)
