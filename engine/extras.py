#!/usr/bin/env python3
"""SRT (Italian, from the script text, timed by the narration words) + image credits for IT01.
Usage: python3 extras_it01.py <assets_dir> <repo_episode_dir>"""
import csv, json, os, re, subprocess, sys
A, EP = sys.argv[1], sys.argv[2]
CH = [c["id"] for c in json.load(open(sys.argv[3]))["chapters"]] if len(sys.argv) > 3 else []
GAP = 0.45


def ts(t):
    ms = int(round(t * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"


subs, off = [], 0.0
for c in CH:
    words = json.load(open(os.path.join(A, "words", c + ".words.json")))
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                os.path.join(A, "narration_audio", c + ".flac")], capture_output=True, text=True).stdout)
    text = open(os.path.join(EP, "narration", c + ".txt")).read().split()
    n, m = len(text), len(words)
    i = 0
    while i < n:                       # chunks of up to 8 words, cut after punctuation when possible
        j = min(n, i + 8)
        for k in range(i + 3, j):
            if re.search(r"[.,;:?!]$", text[k - 1]):
                j = k if k - i >= 4 else j
        a = words[min(m - 1, int(i / n * m))]["s"]
        b = words[min(m - 1, int((j - 1) / n * m))]["e"]
        subs.append((off + a, off + max(b, a + 0.8), " ".join(text[i:j])))
        i = j
    off += dur + GAP
with open(os.path.join(A, "legendas_it.srt"), "w") as f:
    for k, (a, b, t) in enumerate(subs, 1):
        nxt = subs[k][0] if k < len(subs) else b
        f.write(f"{k}\n{ts(a)} --> {ts(min(b + 0.15, nxt - 0.02))}\n{t}\n\n")

used = {p for s in json.load(open(os.path.join(A, "episode.json")))["shots"] for p in s.get("images", []) + ([s["video"]] if s.get("video") else [])}
lines = []
import glob
rows = [r for f in sorted(glob.glob(os.path.join(A, "credits*.csv"))) + [os.path.join(A, "video_credits.csv")]
        if os.path.exists(f) for r in csv.DictReader(open(f))]
for r in rows:
    lic = r.get("license", "")
    if r["file"] not in used or re.search(r"public|cc0|pdm", lic, re.I):
        continue                                      # public domain: no attribution required
    author = " ".join(re.sub(r"<[^>]+>", "", r.get("author") or "autore sconosciuto").split())[:45]
    lines.append(f"{author} ({lic})")
txt = "Crediti immagini (Wikimedia Commons / Openverse): " + "; ".join(sorted(set(lines))) + \
      ". Le altre immagini sono di pubblico dominio."
open(os.path.join(A, "crediti_immagini.txt"), "w").write(txt + "\n")
print(len(subs), "legendas ·", len(set(lines)), "créditos ·", len(txt), "caracteres")
