"""Era das Feras graphics package rendered with HyperFrames (engine/hf/*).

Every card of an episode (title, chapter, lower third over footage, fact sheet, counter, map, timeline, comparison,
kinetic phrase, scale bars, questions, subscribe) is laid out on ONE HyperFrames composition, one after the other,
rendered once (Chrome + GSAP, parallel workers) and cut into one MP4 per card (hf/<id>.mp4) that the episode
renderer plays as a normal clip shot.

  python3 engine/hf_cards.py <workdir> <cards.json>      (cards.json = [{"id","kind","dur",...}, ...])

Card fields per kind (img = path relative to the workdir, e.g. "a/ai/ai_stauri_hero_0.jpg"):
  titulo   kicker, title, sub, img            capitulo  num, title, kicker, img
  rotulo   img, kicker, name, sci?, side?     ficha     img, kicker?, name, sci, rows[[k,v]], source?
  numero   img, value, from?, decimals?, unit, label         mapa  kicker, title, sub, state?, lon, lat
  linha    kicker, title, ma, label           comparar  limg, rimg, lkick, lname, rkick, rname
  frase    img, text (word in *stars* = accent)              escala  kicker, title, rows[[name, metres, "human"?]]
  perguntas img, items[], at[]?               cta       img, text, sub
Optional on any card with a picture: move (push|pull|left|right|up), blurin, leak=false.
"""
import html, json, math, os, re, shutil, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

HERE = os.path.dirname(os.path.abspath(__file__))
HF = os.path.join(HERE, "hf")
FPS = 30
E = html.escape


def masked(text):
    return " ".join(f'<span class="mask"><span>{E(w)}</span></span>' for w in text.split())


def layers(c, shade="left"):
    s = ""
    if c.get("img"):
        s += f'<div class="bg"><img src="{c["_img"]}"></div>'
    s += f'<div class="shade {shade}"></div><div class="vig"></div><div class="grain"></div><div class="leak"></div>'
    return s


def _path_len_bbox(p):
    toks = re.findall(r"[a-zA-Z]|-?[\d.]+(?:e-?\d+)?", p)
    x = y = sx = sy = 0.0; cmd = None; i = 0; L = 0.0; pts = []
    while i < len(toks):
        t = toks[i]
        if t.isalpha():
            cmd = t; i += 1
            if cmd in "zZ":
                L += math.hypot(sx - x, sy - y); x, y = sx, sy; continue
        a, b = float(toks[i]), float(toks[i + 1]); i += 2
        nx, ny = (x + a, y + b) if cmd.islower() else (a, b)
        if cmd in "mM":
            sx, sy = nx, ny; cmd = "l" if cmd == "m" else "L"
        else:
            L += math.hypot(nx - x, ny - y)
        x, y = nx, ny; pts.append((x, y))
    return L, pts


BR = None


def mapa(c):
    global BR
    BR = BR or json.load(open(os.path.join(HF, "vendor", "brazil.json")))
    st = c.get("state", "rs")
    k = min(940 / 613, 980 / 639)
    paths = ""
    for s in BR["states"]:
        L, _ = _path_len_bbox(s["path"])
        paths += f'<path class="st" data-len="{L:.0f}" d="{s["path"]}"/>'
        if s["id"] == st:
            hl = s["path"]; c["hlLen"] = round(L); c["bb"] = BR["bbox"][st]
    paths += f'<path class="hl" d="{hl}"/>'
    c["k"] = k
    # Brazil's extremes (lon -73.99..-34.79, lat 5.27..-33.75) span the map's viewBox
    px = (c["lon"] + 73.99) / 39.2 * 612 * k
    py = (5.27 - c["lat"]) / 39.02 * 638.5 * k
    pin = f'<div class="ring" style="left:{px:.0f}px;top:{py:.0f}px"></div>' * 2 + f'<div class="pin" style="left:{px:.0f}px;top:{py:.0f}px"></div>'
    return (f'<div class="backdrop"></div><div class="stage"><svg viewBox="0 0 613 639">{paths}</svg>{pin}</div>'
            f'<div class="info"><div class="kick">{E(c["kicker"])}</div><h3>{masked(c["title"])}</h3>'
            f'<div class="sub">{E(c["sub"])}</div><div class="rule"></div></div><div class="vig"></div><div class="grain"></div>')


ERAS = [("Triássico", 252, 201, "#c4532d"), ("Jurássico", 201, 145, "#e2a64a"), ("Cretáceo", 145, 66, "#cdbd9e"), ("Hoje", 66, 0, "#7d7466")]


def linha(c):
    W = 1640; span = 252.0
    eras = "".join(f'<div class="era" style="width:{(a - b) / span * W:.1f}px;background:{col}">{E(n) if a - b > 40 else ""}</div>'
                   for n, a, b, col in ERAS)
    ticks = "".join(f'<div class="tick" style="left:{140 + (span - m) / span * W:.0f}px">{m} mi</div>' for m in (252, 201, 145, 66))
    ticks += f'<div class="tick" style="left:{140 + W - 10}px">hoje</div>'
    mx = 140 + (span - c["ma"]) / span * W
    lab = (f'<div class="mlab" style="left:{mx + 26:.0f}px;transform:none;text-align:left">' if mx < 420
           else f'<div class="mlab" style="left:{mx:.0f}px">')
    return (f'<div class="backdrop"></div><div class="ttl"><div class="kick">{E(c["kicker"])}</div><h3>{masked(c["title"])}</h3></div>'
            f'<div class="bar">{eras}</div>{ticks}<div class="mark" style="left:{mx - 2:.0f}px"></div>'
            + lab + f'<b>{E(c["label"])}</b><span>{E(c.get("sub", ""))}</span></div>'
            f'<div class="vig"></div><div class="grain"></div>')


def body(c):
    k = c["kind"]
    if k == "titulo":
        return layers(c, "left") + (f'<div class="box"><div class="kick">{E(c["kicker"])}</div><h1>{masked(c["title"])}</h1>'
                                    f'<div class="rule"></div><div class="sub">{E(c.get("sub", ""))}</div></div>')
    if k == "capitulo":
        return layers(c, "left") + (f'<div class="num">{E(c["num"])}</div><div class="box"><div class="kick">{E(c.get("kicker", "Capítulo"))}</div>'
                                    f'<h2>{masked(c["title"])}</h2><div class="rule"></div></div>')
    if k == "rotulo":
        side = " r" if c.get("side") == "right" else ""
        sci = f'<div class="sci">{E(c["sci"])}</div>' if c.get("sci") else ""
        return layers(c, "low") + (f'<div class="lt{side}"><span class="tag">{E(c["kicker"])}</span><div class="name">{masked(c["name"])}</div>'
                                   f'<div class="rule"></div>{sci}</div>')
    if k == "ficha":
        rows = "".join(f'<div class="row"><span class="k">{E(a)}</span><span class="v">{E(b)}</span></div>' for a, b in c["rows"])
        src = f'<div class="src">{E(c["source"])}</div>' if c.get("source") else ""
        return (f'<div class="media bg"><img src="{c["_img"]}"></div><div class="vig"></div>'
                f'<div class="panel"><div class="kick">{E(c.get("kicker", "Ficha"))}</div><h3>{masked(c["name"])}</h3>'
                f'<div class="sci">{E(c["sci"])}</div>{rows}{src}</div><div class="grain"></div><div class="leak"></div>')
    if k == "numero":
        return layers(c, "full") + (f'<div class="box"><div class="val">0</div><div class="unit">{E(c["unit"])}</div>'
                                    f'<div class="rule"></div><div class="lab">{E(c.get("label", ""))}</div></div>')
    if k == "mapa":
        return mapa(c)
    if k == "linha":
        return linha(c)
    if k == "comparar":
        return (f'<div class="half l"><img src="{c["_limg"]}"></div><div class="half r"><img src="{c["_rimg"]}"></div><div class="div"></div>'
                f'<div class="vig"></div><div class="lab l"><span class="tag">{E(c["lkick"])}</span><div class="name">{E(c["lname"])}</div></div>'
                f'<div class="lab r"><span class="tag">{E(c["rkick"])}</span><div class="name">{E(c["rname"])}</div></div><div class="grain"></div>')
    if k == "frase":
        ws = "".join(f'<span class="w{" em" if w.startswith("*") else ""}">{E(w.strip("*"))}</span>' for w in c["text"].split())
        return layers(c, "full") + f'<div class="box"><p>{ws}</p></div>'
    if k == "escala":
        mx = max(r[1] for r in c["rows"])
        rows = "".join(f'<div class="row{" hum" if len(r) > 2 else ""}"><div class="n">{E(r[0])}</div>'
                       f'<div class="b" style="width:{r[1] / mx * 1000:.0f}px"></div><div class="v">{str(r[1]).replace(".", ",")} m</div></div>'
                       for r in c["rows"])
        return (f'<div class="backdrop" style="position:absolute;inset:0;background:radial-gradient(ellipse at 30% 40%,#2f1a12 0%,#120e0c 60%,#0a0908 100%)"></div>'
                f'<div class="ttl"><div class="kick">{E(c["kicker"])}</div><h3>{masked(c["title"])}</h3></div><div class="rows">{rows}</div>'
                f'<div class="vig"></div><div class="grain"></div>')
    if k == "perguntas":
        qs = "".join(f'<div class="q"><span class="i">{i + 1:02d}</span><span class="t">{masked(t)}</span></div>' for i, t in enumerate(c["items"]))
        return layers(c, "full") + f'<div class="box">{qs}</div>'
    if k == "cta":
        bell = ('<svg class="bell" viewBox="0 0 24 24" fill="#f1e6d0"><path d="M12 22a2.5 2.5 0 0 0 2.45-2h-4.9A2.5 2.5 0 0 0 12 22zm7-6V11a7 7 0 0 0-5.5-6.84V3.5a1.5 1.5 0 0 0-3 0v.66A7 7 0 0 0 5 11v5l-2 2v1h18v-1z"/></svg>')
        return layers(c, "center") + (f'<div class="box"><h3>{masked(c["text"])}</h3><div class="btn">{bell}INSCREVA-SE</div>'
                                      f'<div class="sub">{E(c.get("sub", ""))}</div></div>')
    raise SystemExit(f"tipo de cartela desconhecido: {k}")


def media(proj, wd, src, n):
    """Copies a picture into the project, shrunk to 1920 px wide (keeps the render light)."""
    from PIL import Image
    out = f"m/{n}.jpg"
    im = Image.open(os.path.join(wd, src)).convert("RGB")
    if im.width > 2200:
        im = im.resize((2200, round(im.height * 2200 / im.width)), Image.LANCZOS)
    im.save(os.path.join(proj, out), quality=92)
    return out


def grain(path):
    import random
    from PIL import Image
    rnd = random.Random(7)
    im = Image.new("L", (256, 256))
    im.putdata([max(0, min(255, int(rnd.gauss(128, 40)))) for _ in range(256 * 256)])
    im.convert("RGB").save(path)


def build(wd, cards, proj, theme=None):
    """theme: None = "Dossiê Fóssil" (engine/hf/cards.*); otherwise engine/hf/themes/<theme>/ + engine/hf_theme_<theme>.py"""
    global body
    if os.path.exists(proj):
        shutil.rmtree(proj)
    os.makedirs(os.path.join(proj, "m")); os.makedirs(os.path.join(proj, "fonts"))
    for f in ("DMSerifDisplay-Regular.ttf", "Inter-SemiBold.otf", "Inter-Bold.otf", "InterDisplay-Black.otf", "BebasNeue-Regular.ttf", "Oswald-SemiBold.ttf"):
        shutil.copy(os.path.join(HERE, "fonts", f), os.path.join(proj, "fonts", f))
    src = os.path.join(HF, "themes", theme) if theme else HF
    for f in ("cards.css", "cards.js"):
        shutil.copy(os.path.join(src, f), os.path.join(proj, f))
    if theme:
        import importlib
        body = importlib.import_module(f"hf_theme_{theme}").body
    shutil.copy(os.path.join(HF, "vendor", "gsap.min.js"), os.path.join(proj, "gsap.min.js"))
    grain(os.path.join(proj, "grain.png"))
    t = 0.0; divs = []; data = []
    for i, c in enumerate(cards):
        c = dict(c)
        for key in ("img", "limg", "rimg"):
            if c.get(key):
                c["_" + key] = media(proj, wd, c[key], f"{i}{key}")
        d = round(c["dur"] * FPS) / FPS
        c["start"] = round(t, 4); c["dur"] = d
        b = body(c)
        divs.append(f'<div id="c{i}" class="clip card {c["kind"]}" data-start="{c["start"]}" data-duration="{d}" data-track-index="0">{b}</div>')
        data.append({k: v for k, v in c.items() if not k.startswith("_") and k not in ("rows", "items", "text", "title", "sub")})
        t += d
    total = round(t, 4)
    page = f"""<!doctype html>
<html lang="pt-BR"><head><meta charset="UTF-8"><link rel="stylesheet" href="cards.css"><script src="gsap.min.js"></script></head>
<body><div id="root" data-composition-id="root" data-width="1920" data-height="1080" data-fps="{FPS}" data-start="0" data-duration="{total}">
{chr(10).join(divs)}
<script>window.CARDS = {json.dumps(data, ensure_ascii=False)};</script>
<script src="cards.js"></script>
</div></body></html>"""
    open(os.path.join(proj, "index.html"), "w").write(page)
    json.dump({"$schema": "https://hyperframes.heygen.com/schema/hyperframes.json", "paths": {"assets": "m"}},
              open(os.path.join(proj, "hyperframes.json"), "w"))
    json.dump({"id": "feras-cards", "name": "feras-cards"}, open(os.path.join(proj, "meta.json"), "w"))
    return [(c["id"], round(sum(round(x["dur"] * FPS) / FPS for x in cards[:i]), 4), round(c["dur"] * FPS) / FPS) for i, c in enumerate(cards)]


def render(proj, out, quality="high"):
    hf = os.environ.get("HYPERFRAMES", "npx --yes hyperframes@0.9.46").split()
    subprocess.run(hf + ["telemetry", "disable"], cwd=proj, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(hf + ["render", "-o", os.path.abspath(out), "-q", quality, "--fps", str(FPS), "--quiet"], cwd=proj, check=True)
    if not os.path.exists(out):
        raise SystemExit(f"HyperFrames não gerou {out}")


def split(full, spans, outdir):
    os.makedirs(outdir, exist_ok=True)
    for cid, t0, d in spans:
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t0:.4f}", "-i", full, "-t", f"{d:.4f}", "-an",
                        "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p", "-r", str(FPS),
                        os.path.join(outdir, f"{cid}.mp4")], check=True)


if __name__ == "__main__":
    wd, spec = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])
    cards = json.load(open(spec)); theme = None
    if isinstance(cards, dict):
        theme, cards = cards.get("theme"), cards["cards"]
    proj = os.path.join(wd, "hfproj")
    spans = build(wd, cards, proj, theme)
    full = os.path.join(proj, "cards.mp4")
    render(proj, full, os.environ.get("HF_QUALITY", "standard"))
    split(full, spans, os.path.join(wd, "hf"))
    print(f"{len(spans)} cartelas HyperFrames -> {os.path.join(wd, 'hf')}")
