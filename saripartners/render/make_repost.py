#!/usr/bin/env python3
"""Bir videoyu Sarı tasarımlı kanca metniyle 1080x1920 Reels'e dönüştürür.

Kullanım:
  python3 make_repost.py <kaynak_video> "<kanca metni>" <çıktı.mp4> [--hesap buseninhakkin] [--kapak kapak.jpg]

Yapı:
- İlk 2,5 sn: Sarı tasarımında açılış kartı (video arkada hafifçe görünür, ses baştan başlar),
  ardından yumuşak geçişle video.
- Video boyunca: en üstte ince kanca şeridi (yüzü ve altyazıları kapatmaz).
- 9:16 olmayan videolar bulanık arka plan üzerine ortalanır. Ses korunur; yoksa sessiz kanal eklenir.
- Toplam boyut ~18 MB hedeflenir (jsDelivr 20 MB sınırı).
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
p = argparse.ArgumentParser()
p.add_argument("kaynak")
p.add_argument("kanca")
p.add_argument("cikti")
p.add_argument("--hesap", default="buseninhakkin")
p.add_argument("--kapak", help="Kapak görseli (açılış kartı) çıktısı, .jpg")
p.add_argument("--intro", type=float, default=2.5, help="Açılış kartı süresi (sn)")
a = p.parse_args()

info = json.loads(subprocess.run(
    ["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=codec_type",
     "-of", "json", a.kaynak], capture_output=True, text=True, check=True).stdout)
dur = float(info["format"]["duration"])
has_audio = any(s.get("codec_type") == "audio" for s in info.get("streams", []))
if dur > 900:
    sys.exit("Video 15 dakikadan uzun; Reels sınırı aşılıyor.")
vbit = max(1_200_000, min(6_000_000, int(18 * 8_000_000 / dur) - 128_000))
t = a.intro

with tempfile.TemporaryDirectory() as tmp:
    subprocess.run(["node", os.path.join(HERE, "repost_overlay.js"), a.kanca, a.hesap, tmp], check=True,
                   stdout=subprocess.DEVNULL)
    intro, bar = os.path.join(tmp, "intro.png"), os.path.join(tmp, "bar.png")
    fc = ("[0:v]split[a][b];"
          "[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30:2,eq=brightness=-0.15[bg];"
          "[b]scale=1080:1920:force_original_aspect_ratio=decrease[fg];"
          "[bg][fg]overlay=(W-w)/2:(H-h)/2[base];"
          f"[1:v]format=rgba,fade=t=in:st={t - 0.4}:d=0.4:alpha=1[barf];"
          "[base][barf]overlay=0:0[withbar];"
          f"[2:v]format=rgba,fade=t=out:st={t - 0.5}:d=0.5:alpha=1[introf];"
          f"[withbar][introf]overlay=0:0:enable='lte(t,{t})',format=yuv420p[v]")
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", a.kaynak,
           "-loop", "1", "-t", f"{dur:.2f}", "-framerate", "30", "-i", bar,
           "-loop", "1", "-t", f"{t:.2f}", "-framerate", "30", "-i", intro]
    if not has_audio:
        cmd += ["-f", "lavfi", "-t", f"{dur:.2f}", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100"]
    cmd += ["-filter_complex", fc, "-map", "[v]", "-map", "0:a:0" if has_audio else "3:a",
            "-c:v", "libx264", "-profile:v", "high", "-r", "30", "-b:v", str(vbit), "-maxrate", str(int(vbit * 1.3)),
            "-bufsize", str(vbit * 2), "-c:a", "aac", "-b:a", "128k", "-t", f"{dur:.2f}",
            "-movflags", "+faststart", a.cikti]
    subprocess.run(cmd, check=True)
    if a.kapak:
        # Kapak: açılış kartı, videonun ilk karesinin üzerine.
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", "0.6", "-i", a.cikti, "-frames:v", "1",
                        "-q:v", "2", a.kapak], check=True)
mb = os.path.getsize(a.cikti) / 1e6
print(f"{a.cikti} ({dur:.1f} sn, {mb:.1f} MB)")
if mb > 19.5:
    print("UYARI: dosya 20 MB'a yakın; jsDelivr servis etmeyebilir.", file=sys.stderr)
