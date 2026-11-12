#!/usr/bin/env python3
"""Reels görsellerinden (01.jpg, 02.jpg, ...) yumuşak geçişli, sessiz ses kanallı bir MP4 üretir.

Kullanım: python3 make_reel.py <kare_klasörü> <çıktı.mp4> [--sure 3.5] [--gecis 0.5]
Instagram'da yayınlamadan önce uygulamadan müzik eklenebilir.
"""
import argparse
import glob
import os
import subprocess

p = argparse.ArgumentParser()
p.add_argument("klasor")
p.add_argument("cikti")
p.add_argument("--sure", type=float, default=3.5, help="Her karenin ekranda kalma süresi (sn)")
p.add_argument("--gecis", type=float, default=0.5, help="Geçiş süresi (sn)")
a = p.parse_args()

frames = sorted(glob.glob(os.path.join(a.klasor, "[0-9][0-9].jpg")))
if not frames:
    raise SystemExit("Kare bulunamadı.")
d, x = a.sure, a.gecis
cmd = ["ffmpeg", "-y", "-loglevel", "error"]
for f in frames:
    cmd += ["-loop", "1", "-t", str(d + x), "-framerate", "30", "-i", f]
total = len(frames) * d + x
cmd += ["-f", "lavfi", "-t", f"{total:.2f}", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100"]

# Her kareye hafif yakınlaşma (Ken Burns) ve ardından xfade zinciri.
parts = []
for i in range(len(frames)):
    parts.append(
        f"[{i}:v]scale=1188:2112,zoompan=z='min(zoom+0.0006,1.06)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
        f":d={int((d + x) * 30)}:s=1080x1920:fps=30,setsar=1,format=yuv420p[v{i}]"
    )
last = "v0"
for i in range(1, len(frames)):
    out = f"x{i}"
    parts.append(f"[{last}][v{i}]xfade=transition=fade:duration={x}:offset={i * d:.2f}[{out}]")
    last = out
cmd += [
    "-filter_complex", ";".join(parts),
    "-map", f"[{last}]", "-map", f"{len(frames)}:a",
    "-c:v", "libx264", "-profile:v", "high", "-pix_fmt", "yuv420p", "-r", "30", "-b:v", "6M",
    "-c:a", "aac", "-b:a", "128k", "-shortest", "-movflags", "+faststart", a.cikti,
]
subprocess.run(cmd, check=True)
print(a.cikti)
