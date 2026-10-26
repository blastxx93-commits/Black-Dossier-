#!/usr/bin/env python3
"""Black Dossier image agent.

Reads an episode's shot list (episodes/<ep>/shots.json), searches free-to-use
image sources for every shot, downloads the best candidates and writes:

    <out>/<ep>/<shot_id>/<n>_<source>.jpg   candidate images (max 2400 px)
    <out>/<ep>/credits.csv                  source, license, author, link per file
    <out>/<ep>/contact_sheet_<k>.jpg        numbered thumbnails to pick from (phone-friendly)
    <out>/<ep>/report.md                    what was found / missing

Sources (no API keys needed):
    commons  - Wikimedia Commons (public domain / CC0 / CC BY / CC BY-SA only)
    loc      - Library of Congress photos (skips items with a rights restriction)
    openverse- Openverse (licenses pdm, cc0, by, by-sa only)

Usage:
    python3 agent/search_images.py ep01-apalachin [--out assets_out] [--only id1,id2]

shots.json format:
    {"defaults": {"n": 4, "sources": ["commons", "loc", "openverse"]},
     "shots": [{"id": "hoover_portrait", "query": "J. Edgar Hoover",
                "alt": ["Hoover FBI director 1950s"], "n": 3, "note": "..."}]}
"""
import argparse, csv, hashlib, io, json, os, re, sys, time
import requests
from PIL import Image, ImageDraw, ImageFont, ImageOps

UA = "BlackDossierImageAgent/1.0 (YouTube documentary research; github.com/blastxx93-commits/Black-Dossier-)"
MIN_W = 800          # skip images narrower than this
MAX_SIDE = 2400      # downscale anything bigger
PER_SOURCE = 12      # results asked from each source per query
OK_LICENSE = re.compile(r"public\s*domain|pd[\s-]|^pd$|cc0|cc[\s-]?by(?![\s-]?nc)(?![\s-]?nd)|no known restriction", re.I)
BAD_LICENSE = re.compile(r"\bnc\b|non[\s-]?commercial|\bnd\b|no[\s-]?deriv|fair use|all rights reserved|copyright", re.I)

LOG = []
T0 = time.time()


def log(msg):
    line = f"[{time.time() - T0:6.0f}s] {msg}"
    LOG.append(line)
    print(line, flush=True)


S = requests.Session()
S.headers["User-Agent"] = UA


FAILS = {}           # consecutive failures per source host
DEAD = set()         # hosts switched off for the rest of the run
MAX_FAILS = 3


def get_json(url, params=None, tries=2):
    host = url.split("/")[2]
    if host in DEAD:
        return None
    last = "?"
    for k in range(tries):
        try:
            r = S.get(url, params=params, timeout=15)
            if r.status_code == 429:
                last = "429 rate limit"; time.sleep(8 * (k + 1)); continue
            r.raise_for_status()
            FAILS[host] = 0
            return r.json()
        except Exception as e:
            last = e
            time.sleep(2)
    FAILS[host] = FAILS.get(host, 0) + 1
    log(f"  ! {host}: {str(last)[:160]}")
    if FAILS[host] >= MAX_FAILS:
        DEAD.add(host)
        log(f"  ! {host} desligado nesta execucao ({MAX_FAILS} falhas seguidas)")
    return None


def strip_html(s):
    return re.sub(r"<[^>]+>", "", s or "").strip()


def license_ok(text):
    t = text or ""
    return bool(OK_LICENSE.search(t)) and not BAD_LICENSE.search(t)


# ------------------------------------------------------------ sources
def search_commons(q):
    data = get_json("https://commons.wikimedia.org/w/api.php", {
        "action": "query", "format": "json", "generator": "search",
        "gsrsearch": f"{q} filetype:bitmap", "gsrnamespace": 6, "gsrlimit": PER_SOURCE,
        "prop": "imageinfo", "iiprop": "url|size|extmetadata", "iiurlwidth": 1920})  # standard size: served from cache
    out = []
    pages = (data or {}).get("query", {}).get("pages", {})
    for p in sorted(pages.values(), key=lambda p: p.get("index", 99)):
        ii = (p.get("imageinfo") or [{}])[0]
        md = ii.get("extmetadata", {})
        lic = strip_html(md.get("LicenseShortName", {}).get("value", ""))
        if not license_ok(lic) or ii.get("width", 0) < MIN_W:
            continue
        out.append({"source": "commons", "url": ii.get("thumburl") or ii.get("url"),
                    "title": p.get("title", "").replace("File:", ""),
                    "license": lic, "author": strip_html(md.get("Artist", {}).get("value", ""))[:120],
                    "page": ii.get("descriptionurl", "")})
    return out


def search_loc(q):
    data = get_json("https://www.loc.gov/photos/", {"q": q, "fo": "json", "c": PER_SOURCE,
                                                    "fa": "original-format:photo, print, drawing"})
    out = []
    for it in (data or {}).get("results", []):
        imgs = [u.split("#")[0] for u in it.get("image_url", []) if u]
        if not imgs:
            continue
        rights = it.get("rights_advisory") or it.get("rights") or ""
        rights = " ".join(rights) if isinstance(rights, list) else str(rights)
        if rights and BAD_LICENSE.search(rights) and "no known" not in rights.lower():
            continue
        out.append({"source": "loc", "url": imgs[-1], "title": (it.get("title") or "")[:160],
                    "license": rights[:160] or "LoC - verificar direitos na pagina",
                    "author": ", ".join(it.get("contributor", [])[:2]) if isinstance(it.get("contributor"), list) else "",
                    "page": it.get("url") or it.get("id", "")})
    return out


def search_openverse(q):
    data = get_json("https://api.openverse.org/v1/images/", {"q": q, "license": "pdm,cc0,by,by-sa",
                                                            "page_size": PER_SOURCE, "mature": "false"})
    out = []
    for it in (data or {}).get("results", []):
        if (it.get("width") or MIN_W) < MIN_W:
            continue
        code = (it.get("license") or "").lower()
        lic = {"pdm": "Public Domain Mark", "cc0": "CC0"}.get(code, f"CC {code.upper()} {it.get('license_version') or ''}".strip())
        out.append({"source": "openverse", "url": it.get("url"), "title": (it.get("title") or "")[:160],
                    "license": lic, "author": (it.get("creator") or "")[:120],
                    "page": it.get("foreign_landing_url") or ""})
    return out


SOURCES = {"commons": search_commons, "loc": search_loc, "openverse": search_openverse}


# ------------------------------------------------------------ download
DL_FAILS = {}


def fetch_image(url):
    host = url.split("/")[2] if "//" in url else ""
    if DL_FAILS.get(host, 0) >= 4:       # host keeps failing: stop waiting on it
        return None
    for k in range(2):
        try:
            r = S.get(url, timeout=(8, 20))
            if r.status_code == 429:
                time.sleep(10 * (k + 1)); continue
            r.raise_for_status()
            im = Image.open(io.BytesIO(r.content))
            im = ImageOps.exif_transpose(im).convert("RGB")
            if im.width < MIN_W:
                return None
            if max(im.size) > MAX_SIDE:
                im.thumbnail((MAX_SIDE, MAX_SIDE), Image.LANCZOS)
            DL_FAILS[host] = 0
            return im
        except Exception:
            time.sleep(2 * (k + 1))
    DL_FAILS[host] = DL_FAILS.get(host, 0) + 1
    return None


def interleave(lists):
    """Round-robin across sources so one source does not crowd out the others."""
    out, i = [], 0
    while any(i < len(l) for l in lists):
        for l in lists:
            if i < len(l):
                out.append(l[i])
        i += 1
    return out


# ------------------------------------------------------------ contact sheet
def load_font(size):
    for p in ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def contact_sheets(ep_dir, rows, per_sheet=8):
    """One row per shot, up to 4 thumbs each, 8 shots per sheet. Portrait so it reads on a phone."""
    tw, th, pad, label_h = 360, 240, 16, 56
    f_big, f_small = load_font(30), load_font(24)
    sheets = []
    for k in range(0, len(rows), per_sheet):
        chunk = rows[k:k + per_sheet]
        W = pad + 4 * (tw + pad)
        H = pad + len(chunk) * (label_h + th + pad)
        sheet = Image.new("RGB", (W, H), (18, 16, 16))
        d = ImageDraw.Draw(sheet)
        y = pad
        for shot_id, files in chunk:
            d.text((pad, y + 10), shot_id, font=f_big, fill=(232, 222, 204))
            y += label_h
            if not files:
                d.text((pad, y + th // 2 - 15), "nada encontrado - mande uma imagem ou gere por IA",
                       font=f_small, fill=(196, 72, 62))
            for j, fp in enumerate(files[:4]):
                try:
                    im = ImageOps.fit(Image.open(fp).convert("RGB"), (tw, th), Image.LANCZOS)
                except Exception:
                    continue
                x = pad + j * (tw + pad)
                sheet.paste(im, (x, y))
                num = os.path.basename(fp).split("_")[0]
                d.rectangle([x, y, x + 54, y + 40], fill=(196, 72, 62))
                d.text((x + 10, y + 4), num, font=f_big, fill=(255, 255, 255))
            y += th + pad
        path = os.path.join(ep_dir, f"contact_sheet_{k // per_sheet + 1}.jpg")
        sheet.save(path, quality=82)
        sheets.append(path)
    return sheets


# ------------------------------------------------------------ main
def run(ep, out_root, only=None, budget_min=35):
    spec_path = os.path.join("episodes", ep, "shots.json")
    spec = json.load(open(spec_path))
    defaults = spec.get("defaults", {})
    ep_dir = os.path.join(out_root, ep)
    os.makedirs(ep_dir, exist_ok=True)
    credits, rows, missing, seen = [], [], [], set()
    shots = [s for s in spec["shots"] if not only or s["id"] in only]
    log(f"{ep}: {len(shots)} planos, limite {budget_min} min")
    skipped = []

    for s in shots:
        if time.time() - T0 > budget_min * 60:
            skipped.append(s["id"])
            continue
        sid, want = s["id"], s.get("n", defaults.get("n", 4))
        sources = s.get("sources", defaults.get("sources", list(SOURCES)))
        queries = [s["query"]] + s.get("alt", [])
        log(f"{sid}: {queries[0]!r}")
        shot_dir = os.path.join(ep_dir, sid)
        os.makedirs(shot_dir, exist_ok=True)
        files = []
        for q in queries:
            if len(files) >= want:
                break
            per = []
            for src in sources:
                if src in SOURCES:
                    t = time.time()
                    res = SOURCES[src](q)
                    log(f"    {src}: {len(res)} candidatos em {time.time() - t:.1f}s")
                    per.append(res)
            cands = interleave(per)
            for c in cands:
                if len(files) >= want:
                    break
                key = hashlib.sha1((c["url"] or "").encode()).hexdigest()
                if not c["url"] or key in seen:
                    continue
                seen.add(key)
                t = time.time()
                im = fetch_image(c["url"])
                if im is None:
                    log(f"    falhou download ({c['source']}) em {time.time() - t:.1f}s")
                    continue
                name = f"{len(files) + 1}_{c['source']}.jpg"
                fp = os.path.join(shot_dir, name)
                im.save(fp, quality=88)
                files.append(fp)
                credits.append({"file": f"{sid}/{name}", "shot": sid, "query": q, **c})
                time.sleep(0.5)
        if not files:
            missing.append(sid)
        rows.append((sid, files))
        log(f"  -> {len(files)} imagens")

    with open(os.path.join(ep_dir, "credits.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["file", "shot", "source", "license", "author", "title", "page", "url", "query"])
        w.writeheader()
        w.writerows(credits)
    sheets = contact_sheets(ep_dir, rows)

    lines = [f"# Imagens — {ep}", "",
             f"- Planos: {len(shots)} · imagens baixadas: {len(credits)} · sem resultado: {len(missing)}",
             f"- Folhas de contato: {', '.join(os.path.basename(p) for p in sheets)}"]
    if skipped:
        lines.append(f"- Limite de tempo atingido; ficaram para a próxima execução: {', '.join(skipped)}")
    if DEAD:
        lines.append(f"- Fontes que falharam e foram desligadas: {', '.join(sorted(DEAD))}")
    lines.append("")
    if missing:
        lines += ["## Sem resultado (gerar por IA ou enviar)", ""] + [f"- `{m}`" for m in missing] + [""]
    lines += ["## Por plano", "", "| plano | imagens |", "|---|---|"]
    lines += [f"| `{sid}` | {len(f)} |" for sid, f in rows]
    lines += ["", "Licenças e autores de cada arquivo estão em `credits.csv`. "
              "Itens da Library of Congress marcados 'verificar' precisam de uma olhada na página antes de usar."]
    report = "\n".join(lines) + "\n"
    open(os.path.join(ep_dir, "report.md"), "w").write(report)
    log(f"fim: {len(credits)} imagens")
    open(os.path.join(ep_dir, "agent_log.txt"), "w").write("\n".join(LOG) + "\n")
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        open(os.environ["GITHUB_STEP_SUMMARY"], "a").write(report)
    print(report)
    return len(credits)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("episode")
    ap.add_argument("--out", default="assets_out")
    ap.add_argument("--only", default="")
    ap.add_argument("--budget", type=float, default=35, help="minutos de busca antes de parar e publicar")
    a = ap.parse_args()
    run(a.episode, a.out, set(x for x in a.only.split(",") if x) or None, a.budget)
