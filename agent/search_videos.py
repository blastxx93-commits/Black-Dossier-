#!/usr/bin/env python3
"""Black Dossier video agent: finds free-to-use archival footage and cuts short clips.

Reads episodes/<ep>/videos.json:
    {"defaults": {"n": 3, "clip": 12},
     "shots": [{"id": "kefauver_hearing", "query": "Kefauver hearing 1951", "alt": ["..."], "n": 3, "clip": 12}]}

Sources (no API keys):
    archive  - Internet Archive: Prelinger Archives, Universal Newsreels, FedFlix (US government works)
               and items whose license is public domain / CC0 / CC BY / CC BY-SA
    commons  - Wikimedia Commons videos (public domain / CC0 / CC BY / CC BY-SA)

For each candidate film it cuts a clip straight from the remote file (no full download),
skipping the opening titles. Writes:
    <out>/<ep>/video/<id>/<n>_<source>.mp4    1080p clip, no audio
    <out>/<ep>/video_credits.csv               source, license, title, page, start time
    <out>/<ep>/video_contact_sheet_<k>.jpg     3 frames per clip
    <out>/<ep>/video_report.md

Usage: python3 agent/search_videos.py ep01-apalachin [--out assets_out] [--only id1,id2]
"""
import argparse, csv, json, os, re, shutil, subprocess, sys, time
import requests
from PIL import Image, ImageDraw, ImageFont

UA = "BlackDossierVideoAgent/1.0 (YouTube documentary research; github.com/blastxx93-commits/Black-Dossier-)"
S = requests.Session()
S.headers["User-Agent"] = UA
PD_COLLECTIONS = {"prelinger", "universal_newsreels", "fedflix", "prelinger_library"}
OK_LIC = re.compile(r"publicdomain|/zero/|cc0|licenses/by/|licenses/by-sa/|public domain|pd\b|cc[ -]?by(?![ -]?nc)(?![ -]?nd)", re.I)
BAD_LIC = re.compile(r"-nc|-nd|noncommercial|noderiv|all rights reserved", re.I)
LOG = []
T0 = time.time()


def log(m):
    line = f"[{time.time() - T0:6.0f}s] {m}"
    LOG.append(line); print(line, flush=True)


def ffmpeg():
    exe = shutil.which("ffmpeg")
    if exe:
        return exe
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()


FF = ffmpeg()


def get_json(url, params=None):
    last = "?"
    for k in range(4):
        try:
            time.sleep(1.0)
            r = S.get(url, params=params, timeout=25)
            if r.status_code == 429:
                last = "429"; time.sleep(10 * (k + 1)); continue
            r.raise_for_status()
            return r.json()
        except Exception as e:
            last = e; time.sleep(2)
    log(f"  ! {url.split('/')[2]}: {str(last)[:140]}")
    return None


def strip_html(s):
    return re.sub(r"<[^>]+>", "", s or "").strip()


# ------------------------------------------------------------ sources
def _archive_query(query, rows):
    data = get_json("https://archive.org/advancedsearch.php", {
        "q": query, "fl[]": ["identifier", "title", "licenseurl", "collection", "year"],
        "rows": rows, "output": "json"})
    if data is None:
        return []
    if "error" in data:
        log(f"    archive erro: {str(data['error'])[:120]}")
    return data.get("response", {}).get("docs", [])


def search_archive(q, rows=8, years=None, collections=None, item=None):
    era = f" AND year:[{years[0]} TO {years[1]}]" if years else ""
    if item:
        docs = [{"identifier": item, "title": item, "collection": list(PD_COLLECTIONS)}]
        meta = get_json(f"https://archive.org/metadata/{item}")
        if meta:
            md = meta.get("metadata", {})
            docs = [{"identifier": item, "title": md.get("title", item), "collection": md.get("collection", []),
                     "licenseurl": md.get("licenseurl", "")}]
    else:
        cols = " OR ".join(collections or ["prelinger", "universal_newsreels", "fedflix"])
        docs = _archive_query(f"({q}) AND mediatype:movies AND collection:({cols}){era}", rows)
        if not collections:
            docs += _archive_query(f"({q}) AND mediatype:movies AND licenseurl:*publicdomain*{era}", 4)
    out, ids = [], set()
    for d in docs:
        if d["identifier"] in ids:
            continue
        ids.add(d["identifier"])
        cols = d.get("collection") or []
        cols = set(cols if isinstance(cols, list) else [cols])
        lic = d.get("licenseurl") or ""
        if BAD_LIC.search(lic) or not (cols & PD_COLLECTIONS or OK_LIC.search(lic)):
            continue
        meta = get_json(f"https://archive.org/metadata/{d['identifier']}")
        if not meta:
            continue
        vids = [f for f in meta.get("files", []) if f.get("name", "").lower().endswith(".mp4")]
        if not vids:
            vids = [f for f in meta.get("files", []) if f.get("name", "").lower().endswith((".ogv", ".mpeg", ".mpg", ".avi", ".mov"))]
        if not vids:
            continue
        vids.sort(key=lambda f: int(f.get("size") or 0))
        pick = [f for f in vids if int(f.get("size") or 0) < 1.5e9] or vids
        f = pick[-1]
        ln = str(f.get("length") or "")
        length = float(ln) if re.match(r"^[0-9.]+$", ln) else 0
        licname = ("Public domain (" + ", ".join(sorted(cols & PD_COLLECTIONS)) + ")") if cols & PD_COLLECTIONS else lic
        out.append({"source": "archive", "url": f"https://archive.org/download/{d['identifier']}/{requests.utils.quote(f['name'])}",
                    "title": (d.get("title") or "")[:150], "license": licname,
                    "page": f"https://archive.org/details/{d['identifier']}", "length": length})
    return out


def search_commons(q, rows=10, years=None, collections=None, item=None):
    if item:
        return []
    data = get_json("https://commons.wikimedia.org/w/api.php", {
        "action": "query", "format": "json", "generator": "search", "gsrsearch": f"{q} filetype:video",
        "gsrnamespace": 6, "gsrlimit": rows, "prop": "imageinfo", "iiprop": "url|size|extmetadata|mediatype"})
    out = []
    pages = (data or {}).get("query", {}).get("pages", {})
    for p in sorted(pages.values(), key=lambda p: p.get("index", 99)):
        ii = (p.get("imageinfo") or [{}])[0]
        md = ii.get("extmetadata", {})
        lic = strip_html(md.get("LicenseShortName", {}).get("value", ""))
        if not OK_LIC.search(lic) or BAD_LIC.search(lic) or not ii.get("url"):
            continue
        out.append({"source": "commons", "url": ii["url"], "title": p.get("title", "").replace("File:", "")[:150],
                    "license": lic, "page": ii.get("descriptionurl", ""), "length": float(ii.get("duration") or 0),
                    "author": strip_html(md.get("Artist", {}).get("value", ""))[:100]})
    return out


SOURCES = {"archive": search_archive, "commons": search_commons}


# ------------------------------------------------------------ clips
def ua(url):
    return ["-user_agent", UA] if url.startswith("http") else []


def probe_length(url):
    r = subprocess.run([FF, "-hide_banner", *ua(url), "-i", url], capture_output=True, text=True, timeout=60)
    m = re.search(r"Duration: (\d+):(\d+):([\d.]+)", r.stderr)
    return int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3)) if m else 0


def mean_brightness(path, t):
    r = subprocess.run([FF, "-v", "error", "-ss", f"{t}", "-i", path, "-frames:v", "1", "-vf", "scale=64:-2,format=gray",
                        "-f", "rawvideo", "-"], capture_output=True)
    return sum(r.stdout) / max(1, len(r.stdout))


def cut_clip(url, length, clip, out_path, where=0.35, _retry=0, at=None):
    if not length:
        length = probe_length(url)
    if at is not None:
        start = float(at)
    elif length and length < clip + 4:
        start = 0.0
        clip = max(3.0, length - 1)
    else:
        start = max(8.0, (length or 120) * where)  # skip leaders and title cards
    cmd = [FF, "-v", "error", "-y", *ua(url), "-ss", f"{start:.1f}", "-i", url, "-t", f"{clip}",
           "-an", "-vf", "scale=-2:1080:flags=lanczos,fps=24", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
           "-pix_fmt", "yuv420p", "-movflags", "+faststart", out_path]
    try:
        r = subprocess.run(cmd, timeout=300, capture_output=True, text=True)
    except Exception as e:
        log(f"    corte falhou: {str(e)[:120]}")
        return None
    if r.returncode != 0:
        log(f"    corte falhou ({url.split('/')[-1][:50]}): {r.stderr.strip()[-200:]}")
        return None
    if not os.path.exists(out_path):
        return None
    # reject clips that open dark (fades, leaders, night titles): retry later in the film
    dark = [t for t in (0.5, clip / 2, clip - 1) if mean_brightness(out_path, t) < 14]
    if dark and _retry < 2 and length and at is None:
        log(f"    trecho escuro em {start:.0f}s, tentando mais adiante")
        return cut_clip(url, length, clip, out_path, min(0.85, where + 0.2), _retry + 1)
    if len(dark) >= 2 or os.path.getsize(out_path) < 50_000:
        os.remove(out_path)
        return None
    return start


def frames(path, n=3):
    out = []
    for k in range(n):
        r = subprocess.run([FF, "-v", "error", "-ss", f"{1 + k * 3}", "-i", path, "-frames:v", "1", "-vf", "scale=320:-2",
                            "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True)
        if r.stdout:
            import io
            out.append(Image.open(io.BytesIO(r.stdout)).convert("RGB"))
    return out


def font(size):
    for p in ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def contact_sheets(ep_dir, rows):
    """One row per clip: label + 3 frames. 10 clips per sheet."""
    items = [(sid, fp) for sid, fs in rows for fp in fs]
    sheets, f = [], font(22)
    for k in range(0, len(items), 10):
        chunk = items[k:k + 10]
        W, rowh = 3 * 330 + 20, 200
        sh = Image.new("RGB", (W, len(chunk) * (rowh + 40) + 10), (18, 16, 16))
        d = ImageDraw.Draw(sh)
        y = 10
        for sid, fp in chunk:
            d.text((10, y), f"{sid}  ·  {os.path.basename(fp)}", font=f, fill=(232, 222, 204)); y += 32
            for j, im in enumerate(frames(fp)):
                im.thumbnail((320, rowh)); sh.paste(im, (10 + j * 330, y))
            y += rowh + 8
        p = os.path.join(ep_dir, f"video_contact_sheet_{k // 10 + 1}.jpg")
        sh.save(p, quality=82); sheets.append(p)
    return sheets


# ------------------------------------------------------------ main
def run(ep, out_root, only=None, budget_min=40):
    spec = json.load(open(os.path.join("episodes", ep, "videos.json")))
    dfl = spec.get("defaults", {})
    ep_dir = os.path.join(out_root, ep)
    os.makedirs(ep_dir, exist_ok=True)
    credits, rows, missing, skipped, seen = [], [], [], [], set()
    shots = [s for s in spec["shots"] if not only or s["id"] in only]
    log(f"{ep}: {len(shots)} planos de video")
    for s in shots:
        if time.time() - T0 > budget_min * 60:
            skipped.append(s["id"]); continue
        sid, want, clip = s["id"], s.get("n", dfl.get("n", 3)), s.get("clip", dfl.get("clip", 12))
        sdir = os.path.join(ep_dir, "video", sid)
        os.makedirs(sdir, exist_ok=True)
        files = []
        per_film = s.get("per_film", dfl.get("per_film", 1))
        queries = [s.get("query", s.get("item", ""))] + s.get("alt", [])
        for q in queries:
            if len(files) >= want:
                break
            cands = []
            srcs = ["archive"] if s.get("item") else s.get("sources", dfl.get("sources", list(SOURCES)))
            for src in srcs:
                res = SOURCES[src](q, years=s.get("years", dfl.get("years")),
                                   collections=s.get("collections", dfl.get("collections")), item=s.get("item"))
                log(f"  {sid} / {src}: {len(res)} filmes para {q!r}")
                cands += res
            for c in cands:
                if len(files) >= want:
                    break
                if c["url"] in seen:
                    continue
                seen.add(c["url"])
                # explicit times ("at"), or several points spread through the film ("per_film")
                if s.get("at"):
                    points = [("at", t) for t in s["at"]]
                elif per_film > 1:
                    points = [("where", 0.12 + 0.76 * k / (per_film - 1)) for k in range(per_film)]
                else:
                    points = [("where", s.get("where", 0.35))]
                for kind, v in points:
                    if len(files) >= want:
                        break
                    fp = os.path.join(sdir, f"{len(files) + 1}_{c['source']}.mp4")
                    start = cut_clip(c["url"], c.get("length", 0), clip, fp, v if kind == "where" else 0.35,
                                     at=v if kind == "at" else None)
                    if start is None:
                        continue
                    files.append(fp)
                    credits.append({"file": f"video/{sid}/{os.path.basename(fp)}", "shot": sid, "source": c["source"],
                                    "license": c["license"], "title": c["title"], "page": c["page"],
                                    "start_sec": round(start, 1), "author": c.get("author", ""), "query": q})
                    log(f"    + {os.path.basename(fp)} de {c['title'][:60]!r} a partir de {start:.0f}s")
        if not files:
            missing.append(sid)
        rows.append((sid, files))
    with open(os.path.join(ep_dir, "video_credits.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["file", "shot", "source", "license", "author", "title", "page", "start_sec", "query"])
        w.writeheader(); w.writerows(credits)
    sheets = contact_sheets(ep_dir, rows)
    lines = [f"# Videos — {ep}", "", f"- Planos: {len(shots)} · clipes: {len(credits)} · sem resultado: {len(missing)}",
             f"- Folhas: {', '.join(os.path.basename(p) for p in sheets)}"]
    if skipped:
        lines.append(f"- Limite de tempo; ficaram para depois: {', '.join(skipped)}")
    if missing:
        lines += ["", "## Sem video livre (usar foto/IA)", ""] + [f"- `{m}`" for m in missing]
    lines += ["", "| plano | clipes |", "|---|---|"] + [f"| `{sid}` | {len(f)} |" for sid, f in rows]
    rep = "\n".join(lines) + "\n"
    open(os.path.join(ep_dir, "video_report.md"), "w").write(rep)
    open(os.path.join(ep_dir, "video_log.txt"), "w").write("\n".join(LOG) + "\n")
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        open(os.environ["GITHUB_STEP_SUMMARY"], "a").write(rep)
    print(rep)


if __name__ == "__main__":
    import json
    ap = argparse.ArgumentParser()
    ap.add_argument("episode")
    ap.add_argument("--out", default="assets_out")
    ap.add_argument("--only", default="")
    ap.add_argument("--budget", type=float, default=40)
    a = ap.parse_args()
    run(a.episode, a.out, {x for x in a.only.split(",") if x} or None, a.budget)
