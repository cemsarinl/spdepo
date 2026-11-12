#!/usr/bin/env python3
"""Check an Instagram caption against platform limits and best practices.

Usage:
    python3 caption_check.py --file caption.txt
    echo "caption text" | python3 caption_check.py
    python3 caption_check.py --text "caption" --json

Exit code 1 if any ERROR is found, else 0.
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
        add("ERROR", "Caption is empty.")
    if chars > MAX_CHARS:
        add("ERROR", f"{chars} characters; Instagram's limit is {MAX_CHARS} (over by {chars - MAX_CHARS}).")
    if len(hashtags) > MAX_HASHTAGS:
        add("ERROR", f"{len(hashtags)} hashtags; hard limit is {MAX_HASHTAGS}.")
    elif len(hashtags) > max_hashtags:
        add("WARN", f"{len(hashtags)} hashtags; aim for {max_hashtags} or fewer relevant tags.")
    if len(mentions) > MAX_MENTIONS:
        add("ERROR", f"{len(mentions)} @mentions; limit is {MAX_MENTIONS}.")

    dupes = sorted({h for h in lowered if lowered.count(h) > 1})
    if dupes:
        add("WARN", "Duplicate hashtags: " + ", ".join("#" + d for d in dupes))
    spam = sorted(set(lowered) & SPAM_TAGS)
    if spam:
        add("WARN", "Spammy hashtags that can limit reach: " + ", ".join("#" + s for s in spam))
    if "​" in text or "﻿" in text:
        add("WARN", "Contains zero-width characters; they can break formatting.")
    if re.search(r"https?://", text):
        add("WARN", "URLs in captions are not clickable; use 'link in bio' or a Story link sticker.")

    first_line = text.strip().splitlines()[0] if text.strip() else ""
    if first_line.startswith(("#", "@")):
        add("WARN", "Caption opens with a hashtag/mention; lead with the hook instead.")
    visible = text.strip()[:FOLD_CHARS]
    if len(first_line) > FOLD_CHARS:
        add("WARN", f"First line is {len(first_line)} chars; only ~{FOLD_CHARS} show before '…more'.")

    return {
        "ok": not any(i["level"] == "ERROR" for i in issues),
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
    src.add_argument("--file", help="Path to a caption text file")
    src.add_argument("--text", help="Caption text")
    p.add_argument("--max-hashtags", type=int, default=RECOMMENDED_HASHTAGS,
                   help=f"Soft target for hashtag count (default {RECOMMENDED_HASHTAGS})")
    p.add_argument("--json", action="store_true", help="Output JSON")
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
        print(f"Characters: {r['characters']}/{MAX_CHARS} ({r['remaining']} left)")
        print(f"Hashtags:   {r['hashtags']}  |  Mentions: {r['mentions']}  |  Lines: {r['lines']}")
        print(f"Visible before '…more': {r['visible_before_more']!r}")
        for i in r["issues"]:
            print(f"{i['level']}: {i['message']}")
        print("RESULT: " + ("OK" if r["ok"] else "FAIL"))
    sys.exit(0 if r["ok"] else 1)


if __name__ == "__main__":
    main()
