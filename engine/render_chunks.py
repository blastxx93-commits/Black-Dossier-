#!/usr/bin/env python3
"""Restart-safe render: renders episode.json in video-only chunks (skips chunks already done),
then joins them and muxes the full narration once (loudness -14 LUFS).

Usage: python3 engine/render_chunks.py <assets_dir>/episode.json <out.mp4> [--chunk 90]
"""
import argparse, json, os, subprocess, sys

ap = argparse.ArgumentParser()
ap.add_argument("spec")
ap.add_argument("out")
ap.add_argument("--chunk", type=float, default=90)
a = ap.parse_args()
spec = json.load(open(a.spec))
base = os.path.dirname(os.path.abspath(a.spec))
end = spec["end"]
work = os.path.join(base, "chunks")
os.makedirs(work, exist_ok=True)
museo = os.path.join(os.path.dirname(os.path.abspath(__file__)), "museo.py")
parts, t, k = [], 0.0, 0
while t < end - 1e-3:
    e = min(end, t + a.chunk)
    out = os.path.join(work, f"part{k:03d}.mp4")
    if not os.path.exists(out):
        s = dict(spec, start=t, end=e)
        s.pop("audio", None)
        sp = os.path.join(base, f"_chunk{k:03d}.json")
        json.dump(s, open(sp, "w"))
        tmp = out + ".tmp.mp4"
        subprocess.run([sys.executable, museo, sp, "--out", tmp], check=True)
        os.replace(tmp, out)
        os.remove(sp)
    print(f"parte {k}: {t:.0f}–{e:.0f}s ok", flush=True)
    parts.append(out)
    t, k = e, k + 1
lst = os.path.join(work, "list.txt")
open(lst, "w").write("".join(f"file '{p}'\n" for p in parts))
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst,
                "-i", os.path.join(base, spec["audio"]), "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                "-af", "loudnorm=I=-14:TP=-1.5:LRA=11,apad", "-c:a", "aac", "-b:a", "192k",
                "-t", f"{end:.3f}", a.out], check=True)
print("ok:", a.out)
