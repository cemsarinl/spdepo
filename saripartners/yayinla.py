#!/usr/bin/env python3
"""Onaylanmış bir içerik klasörünü Instagram'da yayınlar.

Kullanım:
  python3 yayinla.py icerik/2026-11-16_belirsiz-alacak          # deneme (hiçbir şey göndermez)
  python3 yayinla.py icerik/2026-11-16_belirsiz-alacak --yes    # gerçekten yayınlar
  python3 yayinla.py --bugun [--yes]                            # bugünün tarihli, onaylı içeriklerini yayınlar

Kurallar:
- meta.json içinde "hukukcu_onayi": true ve "durum": "onaylandi" olmadan yayınlamaz.
- Görseller GitHub'daki herkese açık depodan jsDelivr ile servis edilir; bu yüzden içerik
  önce commit'lenip push'lanmış olmalıdır. URL, push'lanmış commit'e (SHA) sabitlenir.
- Başarılı yayından sonra meta.json'a permalink ve medya ID'si yazılır.
"""
import argparse
import datetime as dt
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
IG = REPO / "instagram-agent-skill" / "scripts" / "ig_api.py"
GH_REPO = "cemsarinl/spdepo"


def git(*args):
    return subprocess.run(["git", "-C", str(REPO), *args], check=True, capture_output=True, text=True).stdout.strip()


def pushed_sha(folder: Path) -> str:
    sha = git("rev-parse", "HEAD")
    remote = git("branch", "-r", "--contains", sha)
    if not remote:
        sys.exit("Son commit henüz push'lanmamış. Önce commit + push yapın; Instagram görselleri depodan çekecek.")
    if git("status", "--porcelain", "--", str(folder)):
        sys.exit(f"{folder} içinde commit'lenmemiş değişiklik var.")
    return sha


def url(sha, path: Path):
    rel = path.relative_to(REPO).as_posix()
    return f"https://cdn.jsdelivr.net/gh/{GH_REPO}@{sha}/{rel}"


def publish(folder: Path, yes: bool):
    meta_p = folder / "meta.json"
    meta = json.loads(meta_p.read_text(encoding="utf-8"))
    if meta.get("durum") == "yayinlandi":
        print(f"{folder.name}: zaten yayınlanmış ({meta.get('permalink')}).")
        return
    if not (meta.get("hukukcu_onayi") is True and meta.get("durum") == "onaylandi"):
        sys.exit(f"{folder.name}: onaylı değil (hukukcu_onayi=true ve durum=onaylandi gerekli).")
    sha = pushed_sha(folder)
    caption = folder / "caption.txt"
    imgs = sorted((folder / "gorseller").glob("[0-9][0-9].jpg"))
    fmt = meta["format"]
    if fmt == "carousel":
        cmd = ["publish-carousel", "--caption-file", str(caption)]
        for p in imgs:
            cmd += ["--media-url", url(sha, p)]
    elif fmt == "tek-gorsel":
        cmd = ["publish-image", "--image-url", url(sha, imgs[0]), "--caption-file", str(caption)]
        if meta.get("alt_text"):
            cmd += ["--alt-text", meta["alt_text"][0]]
    elif fmt == "reel":
        cmd = ["publish-reel", "--video-url", url(sha, folder / "reel.mp4"),
               "--cover-url", url(sha, imgs[0]), "--caption-file", str(caption)]
    else:
        sys.exit(f"Bilinmeyen format: {fmt}")
    if yes:
        cmd.append("--yes")
    env = dict(os.environ, IG_GRAPH_HOST=os.environ.get("IG_GRAPH_HOST", "graph.instagram.com"))
    r = subprocess.run([sys.executable, str(IG), *cmd], capture_output=True, text=True, env=env)
    print(r.stdout, end="")
    if r.returncode:
        sys.exit(r.stderr)
    if yes:
        info = json.loads(r.stdout)
        meta.update(durum="yayinlandi", medya_id=info.get("id"), permalink=info.get("permalink"),
                    yayin_zamani=info.get("timestamp"))
        meta_p.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Yayınlandı: {info.get('permalink')}")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("klasor", nargs="?")
    p.add_argument("--bugun", action="store_true", help="Bugün tarihli onaylı içerikleri yayınla")
    p.add_argument("--yes", action="store_true")
    a = p.parse_args()
    if a.bugun:
        today = dt.datetime.now(dt.timezone(dt.timedelta(hours=3))).date().isoformat()  # Türkiye saati
        due = [d for d in sorted((ROOT / "icerik").iterdir())
               if (d / "meta.json").exists() and json.loads((d / "meta.json").read_text(encoding="utf-8")).get("tarih") == today]
        if not due:
            print(f"{today} için planlanmış içerik yok.")
        for d in due:
            publish(d, a.yes)
    elif a.klasor:
        publish(Path(a.klasor).resolve(), a.yes)
    else:
        p.error("Bir klasör veya --bugun verin.")


if __name__ == "__main__":
    main()
