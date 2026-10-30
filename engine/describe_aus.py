#!/usr/bin/env python3
"""YouTube description for the Aussie car channel, from the built episode.

    python3 describe_aus.py episode.json <assets_dir> meta.json > descricao.txt

meta.json: {"intro": "...", "chapters": ["Hook title", ...one per chapter...], "sources": ["...", ...],
            "tags_line": "#australia #cars ..."}
Chapter times come from the shot durations; credits list every attributed (CC) photo/clip actually used.
"""
import csv, glob, json, os, sys

ep, assets, meta = json.load(open(sys.argv[1])), sys.argv[2], json.load(open(sys.argv[3]))
cred = {}
for fn in glob.glob(os.path.join(assets, "credits*.csv")):
    for r in csv.DictReader(open(fn)):
        cred[r.get("file", "")] = r

out = [meta["intro"].strip(), "", "Real 2026 news. No rumours.", "", "CHAPTERS"]
t = 0.0
used = []
for title, chap in zip(meta["chapters"], ep["chapters"]):
    out.append(f"{int(t // 60)}:{int(t % 60):02d} {title}")
    for s in chap["shots"]:
        t += s["dur"]
        for k in ("src", "photo", "bg"):
            v = s.get(k)
            if isinstance(v, str):
                used.append(v[2:] if v.startswith("a/") else v)
out += ["", "Sources:"] + [f"- {x}" for x in meta["sources"]]
lines, stock = [], set()
for f in dict.fromkeys(used):
    r = cred.get(f)
    if not r:
        continue
    lic = r.get("license", "")
    if "CC" in lic or "Public" in lic:
        lines.append(f"- {r.get('title','').strip()} — {r.get('author','').strip()} ({lic}), {r.get('page','')}")
    else:
        stock.add(r.get("source", "").capitalize())
if lines:
    out += ["", "Photo credits (Wikimedia Commons):"] + sorted(set(lines))
src = ", ".join(sorted(s for s in stock if s)) or "Unsplash, Pixabay"
out += [f"Other photos and footage: {src} (free licences). Some scenes are AI-generated illustrations, not real events.",
        "Music: original track.", "", meta.get("tags_line", "")]
print("\n".join(out))
