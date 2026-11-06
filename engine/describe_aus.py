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

ES = meta.get("lang") == "es"
L = {"tag": "Historia real, con fuentes." if ES else "Real 2026 news. No rumours.", "ch": "CAPÍTULOS" if ES else "CHAPTERS",
     "src": "Fuentes:" if ES else "Sources:", "cred": "Créditos de las fotos (Wikimedia Commons):" if ES else "Photo credits (Wikimedia Commons):",
     "other": ("Otras fotos e imágenes de archivo: {} (licencias libres). Algunas escenas son ilustraciones generadas por IA, no hechos reales."
               if ES else "Other photos and footage: {} (free licences). Some scenes are AI-generated illustrations, not real events."),
     "music": "Música: pista original." if ES else "Music: original track.",
     "full": ("Créditos completos de cada foto, con enlace: en los primeros comentarios del vídeo." if ES
              else "Full photo credits with links: see the pinned comment.")}
out = [meta["intro"].strip(), "", meta.get("tagline", L["tag"]), "", L["ch"]]
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
out += ["", L["src"]] + [f"- {x}" for x in meta["sources"]]
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
if lines and meta.get("compact_credits"):
    # YouTube caps descriptions at 5,000 characters: authors grouped by licence here, full list (with links) in a side file
    by_lic = {}
    for f in dict.fromkeys(used):
        r = cred.get(f)
        if r and ("CC" in r.get("license", "") or "Public" in r.get("license", "")):
            by_lic.setdefault(r["license"].strip(), set()).add((r.get("author") or "?").strip()[:40])
    out += ["", L["cred"]] + [f"{lic}: " + ", ".join(sorted(a)) for lic, a in sorted(by_lic.items())]
    out += [L.get("full", "Full photo credits with links: see the pinned comment.")]
    side = meta.get("credits_file")
    if side:
        full = sorted(set(lines))
        open(side, "w").write("\n".join([L["cred"]] + full) + "\n")
        # YouTube comments cap at 10,000 characters: also write ready-to-paste parts
        parts, cur = [], []
        for ln in full:
            if cur and len("\n".join(cur + [ln])) > 9000:
                parts.append(cur); cur = []
            cur.append(ln)
        if cur:
            parts.append(cur)
        base = os.path.splitext(side)[0]
        for k, pt in enumerate(parts, 1):
            open(f"{base}_{k}.txt", "w").write(f"{L['cred']} ({k}/{len(parts)})\n" + "\n".join(pt) + "\n")
elif lines:
    out += ["", L["cred"]] + sorted(set(lines))
src = ", ".join(sorted(s for s in stock if s)) or "Unsplash, Pixabay"
out += [meta.get("other_line") or L["other"].format(src), L["music"], "", meta.get("tags_line", "")]
print("\n".join(out))
