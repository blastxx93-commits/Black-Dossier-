#!/usr/bin/env python3
"""Builds a museo episode.json from an ordered shot list per chapter, cutting on the narration.

plan.json:
{"gap": 0.45, "chapters": [
   {"id": "ch00_hook", "shots": [
      {"img": "campo_de_fiori/1", "title": "...", "sub": "...", "src": "...", "label": [..], "impact": "..", "tag": ".."},
      {"img": ["a/1", "b/2"], ...},                       # 2–3 images side by side
      {"video": "video/v_x/1", ...},
      {"doc": {"head": "...", "lines": [...], "stamp": "..."}, "title": "..."}
   ]}]}

Cuts: each shot starts on a word that follows punctuation (a pause) when possible, with the
chapter's shots spread evenly (min 2.8 s, max ~7 s each). Images are given as "folder/N" and resolved
to the real file (N_commons.jpg / N_openverse.jpg). Refuses repeated images.

Usage: python3 engine/autoplan.py plan.json <assets_dir>   -> <assets_dir>/episode.json + full.flac
"""
import glob, json, os, re, subprocess, sys

plan, A = json.load(open(sys.argv[1])), sys.argv[2]
GAP = plan.get("gap", 0.45)


def resolve(p):
    if os.path.exists(os.path.join(A, p)):
        return p
    hits = sorted(glob.glob(os.path.join(A, p + "_*")))
    if not hits:
        sys.exit(f"Imagem não encontrada: {p}")
    return os.path.relpath(hits[0], A)


def dur_of(path):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                                capture_output=True, text=True).stdout)


shots, off, parts, seen = [], 0.0, [], {}
for ch in plan["chapters"]:
    cid = ch["id"]
    audio = os.path.join(A, "narration_audio", cid + ".flac")
    d = dur_of(audio)
    words = json.load(open(os.path.join(A, "words", cid + ".words.json")))
    pauses = [0.0] + [words[i + 1]["s"] for i in range(len(words) - 1) if re.search(r"[.,;:?!]$", words[i]["w"])]
    starts = [w["s"] for w in words]
    n = len(ch["shots"])
    step = d / n
    times, last = [0.0], 0.0
    for k in range(1, n):
        target = k * step
        lo, hi = last + 2.8, min(d - 2.8, target + step * 0.45)
        cand = [p for p in pauses if lo <= p <= hi] or [s for s in starts if lo <= s <= hi] or [max(lo, min(hi, target))]
        t = min(cand, key=lambda p: abs(p - target))
        times.append(t)
        last = t
    for t, s in zip(times, ch["shots"]):
        s = dict(s)
        if "img" in s:
            imgs = s.pop("img")
            s["images"] = [resolve(p) for p in ([imgs] if isinstance(imgs, str) else imgs)]
        if "video" in s and not s["video"].endswith(".mp4"):
            s["video"] = resolve(s["video"])
        for p in s.get("images", []) + ([s["video"]] if s.get("video") else []):
            if p in seen:
                sys.exit(f"Imagem repetida: {p} ({seen[p]} / {s.get('title')})")
            seen[p] = s.get("title")
        s.setdefault("move", ["in", "left", "out", "right"][len(shots) % 4])
        s.setdefault("src", "")
        s["t"] = round(off + max(0.0, t - (0.08 if t else 0)), 3)
        shots.append(s)
    parts.append(audio)
    off += d + GAP

# check card rule: no two document cards in a row
for a, b in zip(shots, shots[1:]):
    if a.get("doc") and b.get("doc"):
        print("AVISO: dois cartões seguidos:", a.get("title"), "/", b.get("title"))

cmd, fl = ["ffmpeg", "-v", "error", "-y"], ""
for i, p in enumerate(parts):
    cmd += ["-i", p]
    fl += f"[{i}:a]aformat=sample_rates=44100:channel_layouts=mono,apad=pad_dur={GAP}[a{i}];"
fl += "".join(f"[a{i}]" for i in range(len(parts))) + f"concat=n={len(parts)}:v=0:a=1[out]"
subprocess.run(cmd + ["-filter_complex", fl, "-map", "[out]", os.path.join(A, "full.flac")], check=True)
json.dump({"fps": 30, "audio": "full.flac", "start": 0, "end": round(off - GAP + 0.6, 2), "shots": shots},
          open(os.path.join(A, "episode.json"), "w"), indent=1, ensure_ascii=False)
docs = sum(1 for s in shots if s.get("doc"))
print(f"{len(shots)} planos · {docs} cartões · {len(seen)} imagens/clipes · {(off - GAP) / 60:.1f} min")
