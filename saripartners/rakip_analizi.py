#!/usr/bin/env python3
"""Benzer hukuki bilgilendirme hesaplarını Instagram Business Discovery verisiyle karşılaştırır.

Kullanım:
  python3 rakip_analizi.py                 # rakip/hesaplar.json listesindeki hesapları analiz eder
  python3 rakip_analizi.py hesap1 hesap2   # verilen hesapları dener (listeye eklemez)

Çıktı: rakip/son_analiz.json ve rakip/son_analiz.md (karşılaştırma tablosu ve en iyi gönderiler).
Not: Business Discovery yalnızca herkese açık İşletme/İçerik Üreticisi hesaplarını okuyabilir.
"""
import datetime as dt
import json
import statistics as st
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MARKA = json.loads((ROOT / "marka.json").read_text(encoding="utf-8"))
OUT = ROOT / "rakip"
FIELDS = ("business_discovery.username({u}){{username,name,biography,followers_count,media_count,"
          "media.limit(40){{media_type,media_product_type,like_count,comments_count,timestamp,caption,permalink}}}}")


def fetch(u):
    url = (f"https://{MARKA.get('graph_host', 'graph.facebook.com')}/v23.0/{MARKA['instagram_user_id']}?"
           + urllib.parse.urlencode({"fields": FIELDS.format(u=u)}))
    try:
        with urllib.request.urlopen(url, timeout=60) as r:
            return json.loads(r.read())["business_discovery"]
    except urllib.error.HTTPError as e:
        return {"hata": json.loads(e.read().decode() or "{}").get("error", {}).get("message", str(e))}


def analyse(bd):
    media = bd.get("media", {}).get("data", [])
    now = dt.datetime.now(dt.timezone.utc)
    ts = [dt.datetime.strptime(m["timestamp"], "%Y-%m-%dT%H:%M:%S%z") for m in media]
    last30 = sum(1 for t in ts if (now - t).days <= 30)
    span = max(1, (ts[0] - ts[-1]).days) if len(ts) > 1 else 1
    likes = [m.get("like_count") or 0 for m in media]
    comments = [m.get("comments_count") or 0 for m in media]
    fol = bd.get("followers_count") or 1
    fmt = {}
    for m in media:
        k = "Reels" if m.get("media_product_type") == "REELS" else {"CAROUSEL_ALBUM": "Kaydırmalı", "IMAGE": "Görsel"}.get(m["media_type"], m["media_type"])
        fmt[k] = fmt.get(k, 0) + 1
    by_fmt = {}
    for m in media:
        k = "Reels" if m.get("media_product_type") == "REELS" else {"CAROUSEL_ALBUM": "Kaydırmalı", "IMAGE": "Görsel"}.get(m["media_type"], m["media_type"])
        by_fmt.setdefault(k, []).append((m.get("like_count") or 0) + (m.get("comments_count") or 0))
    top = sorted(media, key=lambda m: (m.get("like_count") or 0) + 3 * (m.get("comments_count") or 0), reverse=True)[:3]
    caps = [len(m.get("caption") or "") for m in media]
    return {
        "kullanici": bd.get("username"), "ad": bd.get("name"), "takipci": bd.get("followers_count"),
        "gonderi": bd.get("media_count"), "son30_gun_gonderi": last30,
        "haftalik_ort": round(len(media) / span * 7, 1),
        "ort_begeni": round(st.mean(likes), 1) if likes else 0, "medyan_begeni": st.median(likes) if likes else 0,
        "ort_yorum": round(st.mean(comments), 1) if comments else 0,
        "etkilesim_orani_%": round((st.mean(likes) + st.mean(comments)) / fol * 100, 2) if likes else 0,
        "format": fmt, "format_ort_etkilesim": {k: round(st.mean(v)) for k, v in by_fmt.items()},
        "ort_aciklama_uzunlugu": round(st.mean(caps)) if caps else 0,
        "en_iyi": [{"etkilesim": (m.get("like_count") or 0) + (m.get("comments_count") or 0),
                    "tarih": m["timestamp"][:10], "ilk_satir": (m.get("caption") or "").split("\n")[0][:110],
                    "link": m.get("permalink")} for m in top],
        "bio": (bd.get("biography") or "")[:160],
    }


def main(users):
    OUT.mkdir(exist_ok=True)
    res, errs = [], {}
    for u in users:
        bd = fetch(u)
        if "hata" in bd:
            errs[u] = bd["hata"][:120]
            continue
        res.append(analyse(bd))
    res.sort(key=lambda r: r["takipci"] or 0, reverse=True)
    stamp = dt.date.today().isoformat()
    (OUT / "son_analiz.json").write_text(json.dumps({"tarih": stamp, "hesaplar": res, "okunamayan": errs},
                                                    ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    L = [f"# Benzer hesaplar: karşılaştırma ({stamp})", "",
         "| Hesap | Takipçi | Son 30 gün | Haftalık | Ort. beğeni | Ort. yorum | Etkileşim % | Format (son 40) | Ort. açıklama |",
         "|---|---|---|---|---|---|---|---|---|"]
    for r in res:
        f = ", ".join(f"{k} {v}" for k, v in r["format"].items())
        L.append(f"| @{r['kullanici']} | {r['takipci']:,} | {r['son30_gun_gonderi']} | {r['haftalik_ort']} | {r['ort_begeni']} | "
                 f"{r['ort_yorum']} | {r['etkilesim_orani_%']} | {f} | {r['ort_aciklama_uzunlugu']} kr |".replace(",", "."))
    L += ["", "## Formatlara göre ortalama etkileşim (beğeni + yorum)", ""]
    for r in res:
        L.append(f"- **@{r['kullanici']}:** " + ", ".join(f"{k} {v}" for k, v in r["format_ort_etkilesim"].items()))
    L += ["", "## En çok etkileşim alan gönderiler", ""]
    for r in res:
        L.append(f"**@{r['kullanici']}**")
        for t in r["en_iyi"]:
            L.append(f"- {t['etkilesim']} · {t['tarih']} · {t['ilk_satir']} ([link]({t['link']}))")
        L.append("")
    if errs:
        L += ["## Okunamayan hesaplar", ""] + [f"- @{k}: {v}" for k, v in errs.items()]
    (OUT / "son_analiz.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1:])
    else:
        main(json.loads((ROOT / "rakip" / "hesaplar.json").read_text(encoding="utf-8"))["hesaplar"])
