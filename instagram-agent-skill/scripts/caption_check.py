#!/usr/bin/env python3
"""Bir Instagram açıklamasını platform limitlerine ve iyi uygulamalara göre kontrol eder.

Kullanım:
    python3 caption_check.py --file caption.txt
    echo "caption text" | python3 caption_check.py
    python3 caption_check.py --text "caption" --json

Herhangi bir HATA varsa çıkış kodu 1, yoksa 0.
"""
import argparse
import json
import re
import sys

MAX_CHARS = 2200
MAX_HASHTAGS = 30
MAX_MENTIONS = 20
RECOMMENDED_HASHTAGS = 5
FOLD_CHARS = 125

HASHTAG_RE = re.compile(r"(?<![\w&])#(\w+)", re.UNICODE)
MENTION_RE = re.compile(r"(?<![\w@])@([A-Za-z0-9._]{1,30})")
SPAM_TAGS = {
    "followforfollow", "follow4follow", "f4f", "like4like", "l4l",
    "likeforlike", "followback", "instafollow", "tagsforlikes", "followme",
}


def check(text: str, max_hashtags: int = RECOMMENDED_HASHTAGS) -> dict:
    issues = []

    def add(level, msg):
        issues.append({"level": level, "message": msg})

    chars = len(text)
    hashtags = HASHTAG_RE.findall(text)
    mentions = MENTION_RE.findall(text)
    lowered = [h.lower() for h in hashtags]

    if not text.strip():
        add("HATA", "Açıklama boş.")
    if chars > MAX_CHARS:
        add("HATA", f"{chars} karakter; Instagram sınırı {MAX_CHARS} ({chars - MAX_CHARS} fazla).")
    if len(hashtags) > MAX_HASHTAGS:
        add("HATA", f"{len(hashtags)} hashtag; kesin sınır {MAX_HASHTAGS}.")
    elif len(hashtags) > max_hashtags:
        add("UYARI", f"{len(hashtags)} hashtag; en fazla {max_hashtags} alakalı etiket hedefle.")
    if len(mentions) > MAX_MENTIONS:
        add("HATA", f"{len(mentions)} @etiket; sınır {MAX_MENTIONS}.")

    dupes = sorted({h for h in lowered if lowered.count(h) > 1})
    if dupes:
        add("UYARI", "Tekrarlanan hashtag'ler: " + ", ".join("#" + d for d in dupes))
    spam = sorted(set(lowered) & SPAM_TAGS)
    if spam:
        add("UYARI", "Erişimi düşürebilecek spam hashtag'ler: " + ", ".join("#" + s for s in spam))
    if "​" in text or "﻿" in text:
        add("UYARI", "Sıfır genişlikli karakterler içeriyor; biçimi bozabilir.")
    if re.search(r"https?://", text):
        add("UYARI", "Açıklamadaki linkler tıklanamaz; 'link profilde' veya hikaye link çıkartması kullan.")

    first_line = text.strip().splitlines()[0] if text.strip() else ""
    if first_line.startswith(("#", "@")):
        add("UYARI", "Açıklama hashtag/@etiket ile başlıyor; bunun yerine kancayla başla.")
    visible = text.strip()[:FOLD_CHARS]
    if len(first_line) > FOLD_CHARS:
        add("UYARI", f"İlk satır {len(first_line)} karakter; '…devamı' öncesinde yalnızca ~{FOLD_CHARS} karakter görünür.")

    return {
        "ok": not any(i["level"] == "HATA" for i in issues),
        "characters": chars,
        "remaining": MAX_CHARS - chars,
        "hashtags": len(hashtags),
        "mentions": len(mentions),
        "lines": text.count("\n") + 1 if text else 0,
        "visible_before_more": visible,
        "issues": issues,
    }


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    src = p.add_mutually_exclusive_group()
    src.add_argument("--file", help="Açıklama metin dosyasının yolu")
    src.add_argument("--text", help="Açıklama metni")
    p.add_argument("--max-hashtags", type=int, default=RECOMMENDED_HASHTAGS,
                   help=f"Hashtag sayısı için önerilen üst sınır (varsayılan {RECOMMENDED_HASHTAGS})")
    p.add_argument("--json", action="store_true", help="JSON çıktısı ver")
    a = p.parse_args()

    if a.file:
        with open(a.file, encoding="utf-8") as f:
            text = f.read()
    elif a.text is not None:
        text = a.text
    else:
        text = sys.stdin.read()
    text = text.rstrip("\n")

    r = check(text, a.max_hashtags)
    if a.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        print(f"Karakter:  {r['characters']}/{MAX_CHARS} ({r['remaining']} kaldı)")
        print(f"Hashtag:   {r['hashtags']}  |  @Etiket: {r['mentions']}  |  Satır: {r['lines']}")
        print(f"'…devamı' öncesi görünen: {r['visible_before_more']!r}")
        for i in r["issues"]:
            print(f"{i['level']}: {i['message']}")
        print("SONUÇ: " + ("GEÇTİ" if r["ok"] else "KALDI"))
    sys.exit(0 if r["ok"] else 1)


if __name__ == "__main__":
    main()
