#!/usr/bin/env python3
"""HyperFrames graphics for the Czech weapons-history channel ("parchment & blueprint" look).

Each entry of episodes/<ep>/graphics.json becomes one HyperFrames composition (HTML + GSAP), rendered
to MP4 by the hyperframes CLI (headless Chrome). The edit uses them as full-frame clips:
    {"type": "video", "src": "a/hf/<id>.mp4", "fit": "crop"}

Kinds (all text in Czech, fonts cover every diacritic):
  spec      technical data card: title, subtitle, rows [[label, value], ...], optional stamp and image
  compare   A vs B table: names [a, b], rows [[label, va, vb, better 0|1|null], ...]
  timeline  years along a drawn axis: events [[year, label], ...] (2-6)
  chapter   chapter card: num, title, sub
  quote     quote in serif italic: text, who
  stat      one big number that counts up: value (int), prefix, suffix, label, source
  map       Central Europe outline with Czechoslovakia filled and pins: pins [[name, lon, lat], ...]

Usage:
    python3 engine/hf_graphics.py episodes/cz01-vz58/graphics.json --assets <assets_ep_dir> --out <dir> [--only id1,id2]
    (--assets: folder holding the images an entry names in "img", e.g. ai/spec_vz58_1.jpg)
Needs node + npx (hyperframes@0.9.19 is fetched by npx) and a Chrome the CLI can find.
"""
import argparse, html, json, os, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.join(HERE, "hyperframes")
HF = os.environ.get("HYPERFRAMES_BIN", "npx --yes hyperframes@0.9.19").split()
E = html.escape

BASE_CSS = """
@font-face{font-family:Anton;src:url(fonts/Anton.ttf)}
@font-face{font-family:Oswald;src:url(fonts/Oswald.ttf);font-weight:200 700}
@font-face{font-family:Courier Prime;src:url(fonts/CourierPrime.ttf)}
@font-face{font-family:Courier Prime;src:url(fonts/CourierPrime-Bold.ttf);font-weight:700}
@font-face{font-family:EB Garamond;src:url(fonts/EBGaramond.ttf);font-weight:400 800}
:root{--paper:#e6dcc4;--ink:#1c1913;--muted:#6b5c42;--rust:#8f2b1d;--olive:#4d5a2a;--line:rgba(60,48,28,.11)}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1920px;height:1080px;overflow:hidden;background:var(--paper)}
#root{position:relative;width:1920px;height:1080px;overflow:hidden;color:var(--ink)}
#stage{position:absolute;inset:0;transform-origin:50% 50%}
.paper{position:absolute;inset:-60px;background:radial-gradient(ellipse at 50% 42%,#f1e8d2 0%,#e3d7ba 52%,#c6b48c 100%)}
.grid{position:absolute;inset:-60px;
 background-image:linear-gradient(var(--line) 1px,transparent 1px),linear-gradient(90deg,var(--line) 1px,transparent 1px),
 linear-gradient(rgba(60,48,28,.05) 1px,transparent 1px),linear-gradient(90deg,rgba(60,48,28,.05) 1px,transparent 1px);
 background-size:240px 240px,240px 240px,48px 48px,48px 48px}
.grain{position:absolute;inset:0;opacity:.32;mix-blend-mode:multiply}
.vig{position:absolute;inset:0;box-shadow:inset 0 0 280px rgba(70,45,15,.55);pointer-events:none}
.corner{position:absolute;width:70px;height:70px;border-color:rgba(40,30,15,.45);border-style:solid}
.c1{left:56px;top:56px;border-width:3px 0 0 3px}.c2{right:56px;top:56px;border-width:3px 3px 0 0}
.c3{left:56px;bottom:56px;border-width:0 0 3px 3px}.c4{right:56px;bottom:56px;border-width:0 3px 3px 0}
.lbl{font-family:'Courier Prime';font-weight:700;letter-spacing:.32em;text-transform:uppercase;color:var(--muted)}
.disp{font-family:Anton;text-transform:uppercase;line-height:.95;letter-spacing:.01em}
.stamp{position:absolute;font-family:'Courier Prime';font-weight:700;color:var(--rust);border:7px solid var(--rust);
 border-radius:14px;padding:14px 30px;font-size:44px;letter-spacing:.12em;text-transform:uppercase;opacity:0;mix-blend-mode:multiply}
"""

GRAIN = """<svg class="grain" width="1920" height="1080"><filter id="n"><feTurbulence type="fractalNoise" baseFrequency=".85"
 numOctaves="3" seed="7"/><feColorMatrix values="0 0 0 0 .35  0 0 0 0 .27  0 0 0 0 .15  0 0 0 .9 0"/></filter>
 <rect width="100%" height="100%" filter="url(#n)"/></svg>"""


def page(gid, dur, body, css, js):
    return f"""<!doctype html>
<html lang="cs"><head><meta charset="UTF-8"/><meta name="viewport" content="width=1920, height=1080"/>
<script src="gsap.min.js"></script><style>{BASE_CSS}{css}</style></head>
<body><div id="root" data-composition-id="{gid}" data-start="0" data-duration="{dur}" data-width="1920" data-height="1080">
<div id="stage" class="clip" data-start="0" data-duration="{dur}" data-track-index="0">
<div class="paper"></div><div class="grid" id="grid"></div>{GRAIN}
<div class="corner c1"></div><div class="corner c2"></div><div class="corner c3"></div><div class="corner c4"></div>
{body}
<div class="vig"></div></div></div>
<script>
const D={dur};
const tl=gsap.timeline({{paused:true}});
tl.fromTo("#stage",{{scale:1.0}},{{scale:1.045,duration:D,ease:"none"}},0);
tl.fromTo("#grid",{{x:0,y:0}},{{x:-48,y:-24,duration:D,ease:"none"}},0);
{js}
window.__timelines=window.__timelines||{{}};
window.__timelines["{gid}"]=tl;
tl.seek(0);
</script></body></html>"""


def stamp_js(sel, t):
    return (f'tl.fromTo("{sel}",{{opacity:0,scale:1.9,rotation:-14}},'
            f'{{opacity:.92,scale:1,rotation:-8,duration:.32,ease:"power4.in"}},{t:.2f});')


# ---------------------------------------------------------------- kinds
def k_spec(g, has_img):
    rows = g["rows"]
    left = 1010 if has_img else 330
    body = ""
    if has_img:
        body += '<div id="img" style="position:absolute;left:90px;top:170px;width:860px;height:700px;display:flex;align-items:center;justify-content:center">' \
                '<img src="img.jpg" style="max-width:860px;max-height:700px;filter:sepia(.25) contrast(1.05);mix-blend-mode:multiply"/></div>'
    body += f'<div class="lbl" id="hdr" style="position:absolute;left:{left}px;top:150px;font-size:28px">{E(g.get("label", "Technická data"))}</div>'
    body += f'<div class="disp" id="ttl" style="position:absolute;left:{left}px;top:200px;font-size:{g.get("size", 132)}px">{E(g["title"])}</div>'
    body += f'<div id="sub" style="position:absolute;left:{left}px;top:{200 + g.get("size", 132) + 18}px;font:italic 40px \'EB Garamond\';color:var(--muted)">{E(g.get("sub", ""))}</div>'
    y0 = 200 + g.get("size", 132) + 100
    w = 820 if has_img else 1260
    for i, (lab, val) in enumerate(rows):
        y = y0 + i * 84
        body += (f'<div class="row" id="r{i}" style="position:absolute;left:{left}px;top:{y}px;width:{w}px;height:72px;'
                 f'display:flex;align-items:flex-end;border-bottom:2px dashed rgba(60,48,28,.35)">'
                 f'<span class="lbl" style="font-size:24px;flex:1;padding-bottom:12px">{E(lab)}</span>'
                 f'<span style="font:600 46px Oswald;padding-bottom:6px">{E(val)}</span></div>')
    if g.get("stamp"):
        body += f'<div class="stamp" id="st" style="right:150px;bottom:110px">{E(g["stamp"])}</div>'
    js = 'tl.from("#hdr",{opacity:0,x:-30,duration:.5,ease:"power2.out"},.15);'
    js += 'tl.from("#ttl",{opacity:0,y:40,duration:.6,ease:"power3.out"},.3);'
    js += 'tl.from("#sub",{opacity:0,duration:.6},.7);'
    if has_img:
        js += 'tl.from("#img",{opacity:0,x:-60,scale:.96,duration:.9,ease:"power2.out"},0);'
    for i in range(len(rows)):
        js += f'tl.from("#r{i}",{{opacity:0,x:40,duration:.45,ease:"power2.out"}},{1.0 + i * .38:.2f});'
    if g.get("stamp"):
        js += stamp_js("#st", 1.2 + len(rows) * .38)
    return body, "", js


def k_compare(g, _):
    a, b = g["names"]
    rows = g["rows"]
    body = f'<div class="lbl" id="hdr" style="position:absolute;left:0;width:1920px;text-align:center;top:120px;font-size:28px">{E(g.get("label", "Srovnání"))}</div>'
    body += f'<div class="disp" id="na" style="position:absolute;left:160px;width:640px;text-align:center;top:180px;font-size:104px">{E(a)}</div>'
    body += f'<div class="disp" id="nb" style="position:absolute;right:160px;width:640px;text-align:center;top:180px;font-size:104px">{E(b)}</div>'
    body += ('<div id="vs" style="position:absolute;left:900px;top:190px;width:120px;height:120px;border-radius:60px;background:var(--rust);'
             'color:#f1e8d2;font:64px Anton;display:flex;align-items:center;justify-content:center">VS</div>')
    for i, r in enumerate(rows):
        lab, va, vb = r[0], r[1], r[2]
        best = r[3] if len(r) > 3 else None
        y = 390 + i * 104
        ua = 'border-bottom:7px solid var(--olive)' if best == 0 else 'border-bottom:7px solid transparent'
        ub = 'border-bottom:7px solid var(--olive)' if best == 1 else 'border-bottom:7px solid transparent'
        body += (f'<div id="r{i}" style="position:absolute;left:160px;width:1600px;top:{y}px;height:92px;display:flex;align-items:center;'
                 f'border-bottom:2px dashed rgba(60,48,28,.3)">'
                 f'<span style="width:640px;text-align:center"><b style="font:600 52px Oswald;{ua}">{E(va)}</b></span>'
                 f'<span class="lbl" style="width:320px;text-align:center;font-size:24px">{E(lab)}</span>'
                 f'<span style="width:640px;text-align:center"><b style="font:600 52px Oswald;{ub}">{E(vb)}</b></span></div>')
    js = ('tl.from("#hdr",{opacity:0,duration:.5},.1);tl.from("#na",{opacity:0,x:-80,duration:.6,ease:"power3.out"},.25);'
          'tl.from("#nb",{opacity:0,x:80,duration:.6,ease:"power3.out"},.25);'
          'tl.from("#vs",{opacity:0,scale:2.2,duration:.35,ease:"back.out(2)"},.7);')
    for i in range(len(rows)):
        js += f'tl.from("#r{i}",{{opacity:0,y:30,duration:.45,ease:"power2.out"}},{1.1 + i * .55:.2f});'
    return body, "", js


def k_timeline(g, _):
    ev = g["events"]
    n = len(ev)
    x0, x1, y = 200, 1720, 600
    body = f'<div class="lbl" id="hdr" style="position:absolute;left:200px;top:150px;font-size:28px">{E(g.get("label", "Časová osa"))}</div>'
    body += f'<div class="disp" id="ttl" style="position:absolute;left:200px;top:200px;font-size:96px">{E(g.get("title", ""))}</div>'
    body += f'<div id="axis" style="position:absolute;left:{x0}px;top:{y}px;width:{x1 - x0}px;height:6px;background:var(--ink);transform-origin:0 50%"></div>'
    for i, (yr, lab) in enumerate(ev):
        x = x0 + 60 + (x1 - x0 - 120) * (i / max(1, n - 1))
        body += (f'<div id="d{i}" style="position:absolute;left:{x - 22}px;top:{y - 19}px;width:44px;height:44px;border-radius:22px;'
                 f'background:var(--rust);border:6px solid var(--paper)"></div>'
                 f'<div class="disp" id="y{i}" style="position:absolute;left:{x - 200}px;width:400px;text-align:center;top:{y - 130}px;font-size:76px">{E(str(yr))}</div>'
                 f'<div id="l{i}" style="position:absolute;left:{x - 170}px;width:340px;text-align:center;top:{y + 52}px;'
                 f'font:700 30px/1.25 \'Courier Prime\';color:var(--ink)">{E(lab)}</div>')
    js = ('tl.from("#hdr",{opacity:0,duration:.4},.1);tl.from("#ttl",{opacity:0,y:30,duration:.5,ease:"power3.out"},.2);'
          'tl.from("#axis",{scaleX:0,duration:1.2+%s,ease:"power1.inOut"},.5);' % (0.35 * n))
    for i in range(n):
        t = 0.7 + (1.2 + .35 * n) * (i / max(1, n - 1)) * .92
        js += (f'tl.from("#d{i}",{{scale:0,duration:.3,ease:"back.out(3)"}},{t:.2f});'
               f'tl.from("#y{i}",{{opacity:0,y:30,duration:.4,ease:"power2.out"}},{t + .05:.2f});'
               f'tl.from("#l{i}",{{opacity:0,y:-15,duration:.4}},{t + .2:.2f});')
    return body, "", js


def k_chapter(g, _):
    body = (f'<div class="lbl" id="num" style="position:absolute;left:0;width:1920px;text-align:center;top:330px;font-size:40px;color:var(--rust)">'
            f'{E(g.get("num", ""))}</div>'
            f'<div class="disp" id="ttl" style="position:absolute;left:160px;width:1600px;text-align:center;top:400px;font-size:{g.get("size", 150)}px">{E(g["title"])}</div>'
            f'<div id="rule" style="position:absolute;left:660px;width:600px;top:{430 + g.get("size", 150) * (1 + g["title"].count(chr(10))) + 20}px;height:5px;background:var(--ink)"></div>'
            f'<div id="sub" style="position:absolute;left:0;width:1920px;text-align:center;top:{430 + g.get("size", 150) * (1 + g["title"].count(chr(10))) + 50}px;'
            f'font:italic 46px \'EB Garamond\';color:var(--muted)">{E(g.get("sub", ""))}</div>')
    css = "#ttl{white-space:pre-line}"
    js = ('tl.from("#num",{opacity:0,letterSpacing:"0.8em",duration:.8,ease:"power2.out"},.1);'
          'tl.from("#ttl",{opacity:0,scale:1.12,duration:.8,ease:"power3.out"},.35);'
          'tl.from("#rule",{scaleX:0,duration:.7,ease:"power2.inOut"},.9);tl.from("#sub",{opacity:0,y:20,duration:.6},1.2);')
    return body, css, js


def k_quote(g, _):
    words = g["text"].split()
    spans = " ".join(f'<span class="w">{E(w)}</span>' for w in words)
    body = ('<div id="qm" style="position:absolute;left:150px;top:40px;font:300px \'EB Garamond\';color:var(--rust)">“</div>'
            f'<div id="q" style="position:absolute;left:300px;width:1380px;top:330px;font:italic 500 {g.get("size", 68)}px/1.28 \'EB Garamond\'">{spans}</div>'
            f'<div class="lbl" id="who" style="position:absolute;right:260px;bottom:170px;font-size:30px">— {E(g.get("who", ""))}</div>')
    step = min(.12, 2.2 / max(1, len(words)))
    js = ('tl.from("#qm",{opacity:0,y:-40,duration:.5,ease:"power2.out"},.1);'
          f'tl.from("#q .w",{{opacity:0,y:12,duration:.35,stagger:{step:.3f},ease:"power1.out"}},.4);'
          f'tl.from("#who",{{opacity:0,x:30,duration:.5}},{.6 + step * len(words):.2f});')
    return body, "", js


def k_stat(g, _):
    v = int(g["value"])
    body = (f'<div class="lbl" id="hdr" style="position:absolute;left:0;width:1920px;text-align:center;top:250px;font-size:30px">{E(g.get("kicker", ""))}</div>'
            f'<div class="disp" id="num" style="position:absolute;left:0;width:1920px;text-align:center;top:310px;font-size:300px">'
            f'{E(g.get("prefix", ""))}<span id="cnt">0</span>{E(g.get("suffix", ""))}</div>'
            f'<div id="lab" style="position:absolute;left:260px;width:1400px;text-align:center;top:660px;font:600 60px Oswald;text-transform:uppercase">{E(g["label"])}</div>'
            f'<div class="lbl" id="src" style="position:absolute;left:0;width:1920px;text-align:center;top:790px;font-size:22px">{E(g.get("source", ""))}</div>')
    js = (f'const C={{v:0}};const fmt=x=>Math.round(x).toString().replace(/\\B(?=(\\d{{3}})+(?!\\d))/g,"\\u00a0");'
          f'tl.from("#hdr",{{opacity:0,duration:.4}},.1);tl.from("#num",{{opacity:0,scale:.85,duration:.5,ease:"power3.out"}},.2);'
          f'tl.fromTo(C,{{v:0}},{{v:{v},duration:1.8,ease:"power2.out",onUpdate:()=>{{document.getElementById("cnt").textContent=fmt(C.v)}}}},.3);'
          f'tl.from("#lab",{{opacity:0,y:30,duration:.5}},1.6);tl.from("#src",{{opacity:0,duration:.5}},2.0);')
    return body, "", js


def k_map(g, _):
    svg = map_svg(g)
    body = (f'<div id="map" style="position:absolute;left:0;top:0">{svg}</div>'
            f'<div id="tbox" style="position:absolute;left:110px;top:100px;padding:26px 40px 30px;background:rgba(236,226,202,.93);'
            f'border:3px solid rgba(28,25,19,.75);box-shadow:8px 8px 0 rgba(28,25,19,.18)">'
            f'<div class="lbl" id="hdr" style="font-size:26px">{E(g.get("label", "Mapa"))}</div>'
            f'<div class="disp" id="ttl" style="font-size:86px;margin-top:8px">{E(g.get("title", ""))}</div></div>')
    js = ('tl.from("#hdr",{opacity:0,duration:.4},.1);tl.from("#ttl",{opacity:0,y:25,duration:.5},.2);'
          'tl.from("#map .nb",{opacity:0,duration:1.0},.2);tl.from("#map .cs",{opacity:0,duration:.8},.9);')
    for i in range(len(g.get("pins", []))):
        js += f'tl.from("#p{i}",{{opacity:0,scale:0,transformOrigin:"50% 100%",duration:.35,ease:"back.out(3)"}},{1.6 + i * .45:.2f});'
    return body, "", js


# ---------------------------------------------------------------- map (Natural Earth 1:50m, public domain)
NE = os.path.join(KIT, "ne_central_europe.json")


def map_svg(g):
    data = json.load(open(NE))
    lon0, lon1, lat0, lat1 = g.get("bbox", [10.0, 24.5, 46.6, 52.4])
    import math
    W, H = 1920, 1080
    # keep aspect: scale both axes with the same factor in projected units
    ya = math.log(math.tan(math.pi / 4 + math.radians(lat0) / 2)); yb = math.log(math.tan(math.pi / 4 + math.radians(lat1) / 2))
    s = min((W - 300) / math.radians(lon1 - lon0), (H - 260) / (yb - ya))
    ox = (W - s * math.radians(lon1 - lon0)) / 2 + 120
    oy = (H - s * (yb - ya)) / 2 + 60

    def P(lon, lat):
        y = math.log(math.tan(math.pi / 4 + math.radians(lat) / 2))
        return ox + s * math.radians(lon - lon0), oy + s * (yb - y)

    hi = set(g.get("highlight", ["CZE", "SVK"]))
    out = [f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
    for f in data:
        d = ""
        for ring in f["rings"]:
            d += "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in (P(*pt) for pt in ring)) + "Z"
        if f["iso"] in hi:
            out.append(f'<path class="cs" d="{d}" fill="rgba(143,43,29,.78)" stroke="#1c1913" stroke-width="3"/>')
        else:
            out.append(f'<path class="nb" d="{d}" fill="rgba(60,48,28,.08)" stroke="rgba(28,25,19,.55)" stroke-width="2"/>')
    for f in data:
        if f.get("name_cs") and f["iso"] not in hi and f.get("label"):
            x, y = P(*f["label"])
            out.append(f'<text class="nb" x="{x:.0f}" y="{y:.0f}" text-anchor="middle" font-family="Courier Prime" font-weight="700" '
                       f'font-size="26" letter-spacing="5" fill="rgba(60,48,28,.7)">{E(f["name_cs"].upper())}</text>')
    for i, pin in enumerate(g.get("pins", [])):
        name, lon, lat = pin[:3]
        side = pin[3] if len(pin) > 3 else "r"  # label side: r | l | b | t
        x, y = P(lon, lat)
        tx, ty, anchor = {"r": (x + 24, y + 14, "start"), "l": (x - 24, y + 14, "end"),
                          "b": (x, y + 62, "middle"), "t": (x, y - 30, "middle")}[side]
        out.append(f'<g id="p{i}"><circle cx="{x:.0f}" cy="{y:.0f}" r="14" fill="#1c1913" stroke="#f1e8d2" stroke-width="5"/>'
                   f'<text x="{tx:.0f}" y="{ty:.0f}" text-anchor="{anchor}" font-family="Oswald" font-weight="700" font-size="46" '
                   f'fill="#1c1913" stroke="#efe6d0" stroke-width="10" paint-order="stroke">{E(name)}</text></g>')
    out.append("</svg>")
    return "".join(out)


KINDS = {"spec": k_spec, "compare": k_compare, "timeline": k_timeline, "chapter": k_chapter, "quote": k_quote, "stat": k_stat, "map": k_map}


def build(g, assets, out_dir):
    gid = g["id"]
    proj = os.path.join(out_dir, "_proj", gid)
    shutil.rmtree(proj, ignore_errors=True)
    os.makedirs(proj)
    shutil.copytree(os.path.join(KIT, "fonts"), os.path.join(proj, "fonts"))
    shutil.copy(os.path.join(KIT, "gsap.min.js"), proj)
    has_img = False
    if g.get("img"):
        src = os.path.join(assets or ".", g["img"])
        if os.path.exists(src):
            shutil.copy(src, os.path.join(proj, "img.jpg")); has_img = True
        else:
            print(f"  aviso: imagem {src} não existe, cartela sem imagem", flush=True)
    body, css, js = KINDS[g["kind"]](g, has_img)
    dur = float(g.get("dur", 8))
    open(os.path.join(proj, "index.html"), "w").write(page(gid.replace("_", "-"), dur, body, css, js))
    json.dump({"name": gid}, open(os.path.join(proj, "meta.json"), "w"))
    return proj


def render(proj, mp4):
    cmd = HF + ["render", proj, "-o", mp4, "--fps", "24", "--crf", "21", "--quiet"]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0 or not os.path.exists(mp4):
        raise RuntimeError(f"hyperframes falhou: {r.stdout[-800:]} {r.stderr[-800:]}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("spec")
    ap.add_argument("--assets", default="")
    ap.add_argument("--out", required=True)
    ap.add_argument("--only", default="")
    ap.add_argument("--html-only", action="store_true")
    a = ap.parse_args()
    items = json.load(open(a.spec))
    only = {x for x in a.only.split(",") if x}
    os.makedirs(a.out, exist_ok=True)
    fails = 0
    for g in items:
        if only and g["id"] not in only:
            continue
        proj = build(g, a.assets, a.out)
        if a.html_only:
            print(f"{g['id']}: {proj}"); continue
        mp4 = os.path.join(a.out, g["id"] + ".mp4")
        try:
            render(proj, mp4)
            print(f"{g['id']}: ok ({g['kind']}, {g.get('dur', 8)}s)", flush=True)
        except Exception as e:  # keep going: one bad card should not cost the others
            fails += 1
            print(f"{g['id']}: FALHOU {e}", flush=True)
    shutil.rmtree(os.path.join(a.out, "_proj"), ignore_errors=True) if not a.html_only else None
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
