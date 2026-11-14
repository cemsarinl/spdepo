#!/usr/bin/env python3
"""@buseninhakkin videolarını @saripartners'ta Sarı tasarımlı Reels olarak yeniden paylaşma aracı.

Kullanım:
  python3 repost.py kontrol                       # yeni (henüz işlenmemiş) videoları listeler
  python3 repost.py hazirla <medya_id> <tarih> <kisa-ad> "<kanca metni>"
                                                  # videoyu indirir, kanca metnini ekler, taslak klasörü kurar
  python3 repost.py isaretle <medya_id> [atlandi] # videoyu işlenmiş olarak kaydeder

Notlar:
- Video indirilmez. Gönderinin kapak görseli ve açıklamasından "ekran görüntüsü" tarzında Sarı tasarımlı
  bir kart çizilir, 8 saniyelik Reels'e dönüştürülür ve @saripartners'ta yayınlanır.
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
FIELDS = ("business_discovery.username(%s){name,profile_picture_url,media.limit(25){id,caption,media_type,media_product_type,"
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
        bd = json.loads(r.read())["business_discovery"]
    for m in bd["media"]["data"]:
        m["_ad"], m["_avatar"] = bd.get("name"), bd.get("profile_picture_url")
    return bd["media"]["data"]


def kontrol():
    s = state()
    yeni = [m for m in media() if m["media_type"] == "VIDEO" and m["id"] not in s["islenen"]
            and m["timestamp"][:10] >= s["baslangic"]]
    if not yeni:
        print("Yeni video yok.")
    for m in yeni:
        uygun = "uygun" if m.get("thumbnail_url") else "ATLANACAK (kapak görseli yok)"
        print(f"{m['id']}  {m['timestamp'][:10]}  ♥{m.get('like_count')}  {m['permalink']}  [{uygun}]")
        print("   " + (m.get("caption") or "").split("\n")[0][:160])
    return yeni


def hazirla(mid, tarih, ad, kanca):
    m = next((x for x in media() if x["id"] == mid), None)
    if not m or not m.get("thumbnail_url"):
        sys.exit("Gönderi bulunamadı ya da kapak görseli yok.")
    d = ROOT / "icerik" / f"{tarih}_repost-{ad}"
    (d / "gorseller").mkdir(parents=True, exist_ok=True)
    urllib.request.urlretrieve(m["thumbnail_url"], d / "kaynak_kapak.jpg")
    avatar = None
    if m.get("_avatar"):
        try:
            urllib.request.urlretrieve(m["_avatar"], d / "kaynak_avatar.jpg"); avatar = "kaynak_avatar.jpg"
        except OSError:
            pass  # profil fotoğrafı alınamazsa kartta baş harf gösterilir
    ilk = (m.get("caption") or "").split("\n")[0].strip()
    (d / "kart.json").write_text(json.dumps({
        "kanca": kanca, "kullanici": KAYNAK, "ad": m.get("_ad") or "", "aciklama": ilk,
        "kapak": "kaynak_kapak.jpg", "avatar": avatar,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    kart = d / "gorseller" / "01.jpg"
    subprocess.run(["node", str(ROOT / "render" / "post_card.js"), str(d / "kart.json"), str(kart)], check=True,
                   stdout=subprocess.DEVNULL)
    subprocess.run([sys.executable, str(ROOT / "render" / "make_reel.py"), str(d / "gorseller"), str(d / "reel.mp4"),
                    "--sure", "8", "--gecis", "0"], check=True, stdout=subprocess.DEVNULL)
    (d / "caption.txt").write_text(
        f"{ilk}\n\n🎥 Videonun tamamı @{KAYNAK} hesabında.\n\n"
        f"Bu paylaşım genel bilgilendirme amaçlıdır; hukuki görüş veya tavsiye niteliği taşımaz.\n\n"
        f"#BuSeninHakkın #SarıAvukatlıkOrtaklığı\n", encoding="utf-8")
    (d / "meta.json").write_text(json.dumps({
        "tarih": tarih, "saat": "10:00", "tur": "repost", "format": "reel",
        "durum": "taslak", "hukukcu_onayi": False, "kanca": kanca,
        "kaynak_medya_id": mid, "kaynak_permalink": m["permalink"], "kaynak_tarih": m["timestamp"],
        "alt_text": [f"Antrasit zemin üzerinde '{kanca}' başlığı ve @{KAYNAK} hesabındaki Reels gönderisinin kartı."],
        "dogrulanacak": ["Kanca metni videonun içeriğiyle örtüşüyor mu?"]
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
