#!/usr/bin/env python3
"""Aussie car channel look on top of the Black Dossier engine.

Same timeline (shots anchored to words) and audio mix as render.py; the look and the cutting change:
near-black + bright yellow + alarm red, heavy condensed type, news-style tags, new shot types for a
car-market countdown, and dynamic transitions between every shot.

Channel rules built in:
  * nothing static: every shot moves (Ken Burns on photos, slow push + drifting background on graphics)
  * no shake: all motion is sub-pixel (affine transforms with float boxes), no wiggles
  * never a black screen: graphics sit on an animated studio background, no fades to black
  * transitions: fade | slide | zoom | wipe | whip (auto-varied when a shot does not set "trans")

Shot types added: rank, stat, bars, price, questions, cta (+ restyled title, statement, image captions).
Usage: python3 render_aus.py episode.json [--preview]      (render is resumable: re-run to continue)
"""
import json, math, os, re, shutil, subprocess, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render as R
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance

R.BRAND.update({
    "red": (225, 12, 6), "red_dark": (150, 8, 4), "yellow": (255, 212, 0),
    "white": (245, 245, 242), "black": (10, 10, 12), "ink": (10, 10, 12), "grey": (165, 165, 170),
})
B = R.BRAND
R.FONT_CANDIDATES["impact"] = ["fonts/InterDisplay-Black.otf", "fonts/Anton-Regular.ttf", "fonts/BebasNeue-Regular.ttf",
                               "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf",
                               "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]
R.FONT_CANDIDATES["body"] = ["fonts/Inter-SemiBold.otf", "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf",
                             "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]
font, ease, wrap = R.font, R.ease, R.wrap
CHANNEL = os.environ.get("AUS_CHANNEL", "")
# on-screen labels per channel language (env CHANNEL_LANG, set by the render workflow from episodes/<ep>/lang.txt)
LANG = os.environ.get("CHANNEL_LANG", "en").strip() or "en"
LBL = {"en": {"source": "SOURCE: ", "sub": "SUBSCRIBE", "subbed": "SUBSCRIBED"},
       "es": {"source": "FUENTE: ", "sub": "SUSCRÍBETE", "subbed": "SUSCRITO"}}.get(LANG) or {"source": "SOURCE: ", "sub": "SUBSCRIBE", "subbed": "SUBSCRIBED"}


# ---------------------------------------------------------------- motion helpers (sub-pixel, no jitter)
def push(ctx, im, t, z0=1.0, z1=1.045, dx=0.0, dy=0.0):
    """Smooth zoom/drift of a full frame. t 0..1. dx/dy in fractions of the spare margin (-1..1)."""
    z = z0 + (z1 - z0) * t
    if z <= 1.0001 and not dx and not dy:
        return im
    cw, ch = ctx.W / z, ctx.H / z
    cx = ctx.W / 2 + dx * (ctx.W - cw) / 2
    cy = ctx.H / 2 + dy * (ctx.H - ch) / 2
    return im.transform((ctx.W, ctx.H), Image.EXTENT, (cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2), Image.BICUBIC)


_studio = {}


def studio(ctx, seed=0):
    """Large dark studio plate: diagonal hairlines, yellow and red glows. Panned per frame."""
    key = (ctx.W, seed % 4)
    if key not in _studio:
        W, H = int(ctx.W * 1.3), int(ctx.H * 1.3)
        small = Image.new("RGB", (W // 4, H // 4), (12, 12, 15))
        g = ImageDraw.Draw(small)
        cols = [((255, 190, 0), (0.18, 0.25)), ((210, 10, 5), (0.85, 0.8))]
        if seed % 2:
            cols = [((210, 10, 5), (0.15, 0.75)), ((255, 190, 0), (0.85, 0.2))]
        for col, (fx, fy) in cols:
            glow = Image.new("RGB", small.size, (0, 0, 0))
            ImageDraw.Draw(glow).ellipse([small.width * (fx - 0.35), small.height * (fy - 0.45),
                                          small.width * (fx + 0.35), small.height * (fy + 0.45)], fill=col)
            glow = glow.filter(ImageFilter.GaussianBlur(small.width // 7))
            small = Image.blend(small, Image.composite(glow, small, Image.new("L", small.size, 255)), 0.16)
        im = small.resize((W, H), Image.BICUBIC)
        d = ImageDraw.Draw(im)
        step = ctx.px(46)
        for x in range(-H, W, step):
            d.line([(x, 0), (x + H, H)], fill=(24, 24, 28), width=max(1, ctx.px(2)))
        _studio[key] = im
    return _studio[key]


def studio_frame(ctx, i, n, seed=0):
    im = studio(ctx, seed)
    t = i / max(1, n - 1)
    ox = (im.width - ctx.W) * (0.15 + 0.7 * t) if seed % 2 == 0 else (im.width - ctx.W) * (0.85 - 0.7 * t)
    oy = (im.height - ctx.H) * (0.5 + 0.25 * math.sin(t * math.pi))
    return im.transform((ctx.W, ctx.H), Image.EXTENT, (ox, oy, ox + ctx.W, oy + ctx.H), Image.BICUBIC)


def overlay(base, layer):
    base.paste(layer, (0, 0), layer)
    return base


def layer(ctx):
    return Image.new("RGBA", (ctx.W, ctx.H), (0, 0, 0, 0))


def tag(ctx, text, color=None, size=40, fg=None):
    color = color or B["red"]
    f = font("impact", ctx.px(size))
    tw = int(ImageDraw.Draw(Image.new("RGBA", (1, 1))).textlength(text.upper(), font=f))
    pad = ctx.px(size * 0.38)
    im = Image.new("RGBA", (tw + pad * 2, int(ctx.px(size) * 1.32)), color + (255,))
    ImageDraw.Draw(im).text((pad, ctx.px(size * 0.1)), text.upper(), font=f, fill=(fg or B["white"]))
    return im


def sized(ctx, d, text, kind, size, max_w, floor=40):
    while size > floor:
        f = font(kind, ctx.px(size))
        if d.textlength(text, font=f) <= max_w:
            return f, size
        size -= 6
    return font(kind, ctx.px(floor)), floor


def pop(i, start, fps, dur=0.32):
    """0 -> 1 with a gentle settle (no bounce back and forth)."""
    k = (i - start) / max(1, fps * dur)
    if k <= 0:
        return 0.0
    if k >= 1:
        return 1.0
    return 1 - (1 - k) ** 3 + 0.06 * math.sin(k * math.pi)


def paste_scaled(fr, im, cx, cy, sc, alpha=1.0):
    if sc <= 0.01:
        return
    w, h = max(1, int(im.width * sc)), max(1, int(im.height * sc))
    s = im.resize((w, h), Image.BICUBIC)
    if alpha < 1 and s.mode == "RGBA":
        s.putalpha(s.split()[3].point(lambda a: int(a * alpha)))
    fr.paste(s, (int(round(cx - w / 2)), int(round(cy - h / 2))), s if s.mode == "RGBA" else None)


def fade_col(col, k):
    k = max(0.0, min(1.0, k))
    return tuple(int(c * k) for c in col) + (int(255 * k),)


def source_line(ctx, d, text):
    if text:
        d.text((ctx.px(90), ctx.px(60)), LBL["source"] + text.upper(), font=font("body", ctx.px(26)), fill=B["grey"] + (255,))


def channel_bug(ctx, d):
    if CHANNEL:
        f = font("impact", ctx.px(30))
        w = d.textlength(CHANNEL.upper(), font=f)
        d.text((ctx.W - w - ctx.px(70), ctx.px(52)), CHANNEL.upper(), font=f, fill=B["yellow"] + (255,))


def graphic(ctx, s, n, draw_layer, seed=0):
    """Common frame loop for graphic cards: drifting studio background + the card's layer, slow push."""
    for i in range(n):
        fr = studio_frame(ctx, i, n, seed)
        lay = draw_layer(i)
        fr = overlay(fr, lay)
        yield push(ctx, fr, ease(i / max(1, n - 1)), 1.0, 1.035)


# ---------------------------------------------------------------- captions on photos: red tag + white bar
def caption_layer(ctx, text):
    im = layer(ctx)
    d = ImageDraw.Draw(im)
    label, _, rest = text.partition("|")
    x, y = ctx.px(80), ctx.px(70)
    if rest:
        t = tag(ctx, label.strip(), size=34)
        im.paste(t, (x, y), t)
        y += t.height
        text = rest.strip()
    f = font("impact", ctx.px(52))
    tw = d.textlength(text.upper(), font=f)
    d.rectangle([x, y, x + tw + ctx.px(36), y + ctx.px(74)], fill=B["white"] + (255,))
    d.text((x + ctx.px(18), y + ctx.px(6)), text.upper(), font=f, fill=B["black"])
    return im


R.caption_layer = caption_layer


def shot_image(ctx, s, n):
    """Photo with Ken Burns (never static); optional caption slides in."""
    over = 1.2
    W2, H2 = int(ctx.W * over), int(ctx.H * over)
    img = R.load_image(ctx, s["src"], W2, H2, s.get("focus", (0.5, 0.5)))
    move = s.get("move", "in")
    z0, z1 = {"in": (1.0, 1.14), "out": (1.14, 1.0)}.get(move, (1.07, 1.1))
    dx0 = dy0 = dx1 = dy1 = 0.0
    if move == "left": dx0, dx1 = 0.7, -0.7
    if move == "right": dx0, dx1 = -0.7, 0.7
    if move == "up": dy0, dy1 = 0.7, -0.7
    if move == "down": dy0, dy1 = -0.7, 0.7
    cap = caption_layer(ctx, s["caption"]) if s.get("caption") else None
    for i in range(n):
        t = ease(i / max(1, n - 1)) * 0.85 + (i / max(1, n - 1)) * 0.15  # never fully stops
        z = z0 + (z1 - z0) * t
        cw, ch = W2 / z, H2 / z  # z=1 shows the whole (oversized) photo; >1 pushes in
        fx = dx0 + (dx1 - dx0) * t
        fy = dy0 + (dy1 - dy0) * t
        cx = W2 / 2 + fx * (W2 - cw) / 2
        cy = H2 / 2 + fy * (H2 - ch) / 2
        fr = img.transform((ctx.W, ctx.H), Image.EXTENT, (cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2), Image.BICUBIC)
        if cap:
            k = ease(min(1, i / (ctx.fps * 0.4)))
            c2 = cap if k >= 1 else cap.transform(cap.size, Image.AFFINE, (1, 0, (1 - k) * ctx.px(260), 0, 1, 0), Image.BICUBIC)
            fr.paste(c2, (0, 0), c2)
        yield fr


def shot_statement(ctx, s, n):
    size = s.get("size", 150)
    tmp = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    f = font("impact", ctx.px(size))
    lines = wrap(tmp, s["text"].upper(), f, ctx.W * 0.84)
    lh = int(ctx.px(size) * 1.08)
    y = (ctx.H - lh * len(lines)) // 2 - ctx.px(20)
    hl = s.get("highlight", "").upper()
    wl = tmp.textlength(lines[-1], font=f)
    uy = y + lh * len(lines) + ctx.px(14)

    def draw(i):
        L = layer(ctx); d = ImageDraw.Draw(L)
        for li, line in enumerate(lines):
            k = ease((i - li * ctx.fps * 0.1) / (ctx.fps * 0.35))
            w = d.textlength(line, font=f)
            x = (ctx.W - w) / 2
            for word in line.split(" "):
                col = B["yellow"] if hl and re.sub(r"[^\w$%]", "", word) in hl.split() else B["white"]
                d.text((x, y + li * lh + (1 - k) * ctx.px(50)), word, font=f, fill=fade_col(col, k))
                x += d.textlength(word + " ", font=f)
        t = ease((i - ctx.fps * 0.3) / (ctx.fps * 0.5))
        if t > 0:
            d.rectangle([(ctx.W - wl) / 2, uy, (ctx.W - wl) / 2 + wl * t, uy + ctx.px(12)], fill=B["yellow"] + (255,))
        channel_bug(ctx, d)
        return L
    return graphic(ctx, s, n, draw, seed=s.get("seed", 1))


def shot_title(ctx, s, n):
    """Title card over its own photo (s['bg'] counts as a used image), darkened, with Ken Burns."""
    over = 1.2
    W2, H2 = int(ctx.W * over), int(ctx.H * over)
    bg = R.load_image(ctx, s["bg"], W2, H2, tuple(s.get("bg_focus", (0.5, 0.5)))) if s.get("bg") else None
    if bg is not None:
        bg = ImageEnhance.Brightness(bg).enhance(0.42)
    tmp = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    title = s["title"].upper()
    f, size = sized(ctx, tmp, title, "impact", 170, ctx.W * 0.86)
    lines = wrap(tmp, title, f, ctx.W * 0.86)
    lh = int(ctx.px(size) * 1.04)
    y0 = int(ctx.H * 0.52 - lh * len(lines) / 2)
    sub = s.get("subtitle", "")
    tg = tag(ctx, s["tag"], size=46) if s.get("tag") else None
    fs = font("body", ctx.px(40))
    for i in range(n):
        t = i / max(1, n - 1)
        if bg is not None:
            z = 1.0 + 0.12 * t
            cw, ch = W2 / z / over, H2 / z / over
            fr = bg.transform((ctx.W, ctx.H), Image.EXTENT, (W2 / 2 - cw / 2, H2 / 2 - ch / 2, W2 / 2 + cw / 2, H2 / 2 + ch / 2), Image.BICUBIC)
        else:
            fr = studio_frame(ctx, i, n)
        L = layer(ctx); d = ImageDraw.Draw(L)
        for li, line in enumerate(lines):
            k = ease((i - li * ctx.fps * 0.12) / (ctx.fps * 0.4))
            w = d.textlength(line, font=f)
            col = B["yellow"] if li == len(lines) - 1 and len(lines) > 1 else B["white"]
            d.text(((ctx.W - w) / 2, y0 + li * lh + (1 - k) * ctx.px(60)), line, font=f, fill=fade_col(col, k))
        if sub:
            k = ease((i - ctx.fps * 0.8) / (ctx.fps * 0.4))
            w = d.textlength(sub, font=fs)
            d.text(((ctx.W - w) / 2, y0 + lh * len(lines) + ctx.px(30)), sub, font=fs, fill=fade_col(B["white"], k))
        fr = overlay(fr, L)
        if tg is not None:
            paste_scaled(fr, tg, ctx.W / 2, y0 - ctx.px(75), pop(i, int(ctx.fps * 0.6), ctx.fps))
        yield fr


def shot_rank(ctx, s, n):
    """Countdown card: big '#N', model name, the model photo in a yellow frame (Ken Burns inside)."""
    pw, ph = int(ctx.W * 0.5), int(ctx.H * 0.62)
    px_, py_ = ctx.W - pw - ctx.px(100), int(ctx.H * 0.17)
    photo = R.load_image(ctx, s["photo"], int(pw * 1.15), int(ph * 1.15), tuple(s.get("focus", (0.5, 0.5)))) \
        if s.get("photo") and os.path.exists(ctx.path(s["photo"])) else None
    tmp = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    fnum = font("impact", ctx.px(330))
    fname, nsize = sized(ctx, tmp, s["name"].upper(), "impact", 108, ctx.W * 0.38)
    name_lines = wrap(tmp, s["name"].upper(), fname, ctx.W * 0.38)
    tg = tag(ctx, s["tag"], size=36) if s.get("tag") else None
    fs = font("body", ctx.px(36))
    fc = font("body", ctx.px(20))
    sub = s.get("sub", "")
    credit = s.get("credit", "")
    for i in range(n):
        fr = studio_frame(ctx, i, n, seed=int(s["num"]))
        t = i / max(1, n - 1)
        if photo is not None:
            k = ease(min(1, i / (ctx.fps * 0.45)))
            z = 1.0 + 0.1 * t
            cw, ch = photo.width / z / 1.15, photo.height / z / 1.15
            cx, cy = photo.width / 2, photo.height / 2
            ph_im = photo.transform((pw, ph), Image.EXTENT, (cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2), Image.BICUBIC)
            ox = px_ + (1 - k) * ctx.px(200)
            d = ImageDraw.Draw(fr)
            d.rectangle([ox - ctx.px(10), py_ - ctx.px(10), ox + pw + ctx.px(10), py_ + ph + ctx.px(10)], fill=B["yellow"])
            fr.paste(ph_im, (int(round(ox)), py_))
            if credit:
                cwid = d.textlength(credit, font=fc)
                d.rectangle([ox + pw - cwid - ctx.px(20), py_ + ph - ctx.px(34), ox + pw, py_ + ph], fill=(0, 0, 0))
                d.text((ox + pw - cwid - ctx.px(10), py_ + ph - ctx.px(30)), credit, font=fc, fill=(205, 205, 205))
        L = layer(ctx); d = ImageDraw.Draw(L)
        k2 = ease(min(1, i / (ctx.fps * 0.35)))
        d.text((ctx.px(100) - (1 - k2) * ctx.px(120), py_ - ctx.px(40)), "#%s" % s["num"], font=fnum, fill=fade_col(B["yellow"], k2))
        ny = py_ + ctx.px(330)
        for li, line in enumerate(name_lines):
            k3 = ease((i - ctx.fps * (0.25 + li * 0.08)) / (ctx.fps * 0.35))
            d.text((ctx.px(100), ny + li * int(ctx.px(nsize) * 1.02)), line, font=fname, fill=fade_col(B["white"], k3))
        sy = ny + len(name_lines) * int(ctx.px(nsize) * 1.02) + ctx.px(20)
        if sub:
            k4 = ease((i - ctx.fps * 0.9) / (ctx.fps * 0.4))
            yy = sy + (tg.height + ctx.px(16) if tg is not None else 0)
            for li, line in enumerate(wrap(d, sub, fs, ctx.W * 0.36)):
                d.text((ctx.px(100), yy + li * ctx.px(48)), line, font=fs, fill=fade_col(B["white"], k4))
        channel_bug(ctx, d)
        fr = overlay(fr, L)
        if tg is not None:
            paste_scaled(fr, tg, ctx.px(100) + tg.width / 2, sy + tg.height / 2, pop(i, int(ctx.fps * 0.7), ctx.fps))
        yield push(ctx, fr, ease(t), 1.0, 1.025)


def _num(v):
    m = re.match(r"^([^\d\-]*)(-?[\d,]+(?:\.\d+)?)(.*)$", str(v))
    if not m:
        return None
    pre, num, suf = m.groups()
    dec = len(num.split(".")[1]) if "." in num else 0
    return pre, float(num.replace(",", "")), suf, dec, "," in num


def _fmt(parts, x):
    pre, val, suf, dec, comma = parts
    return f"{pre}{(f'{x:,.{dec}f}' if comma else f'{x:.{dec}f}')}{suf}"


def shot_stat(ctx, s, n):
    val = str(s["value"])
    parts = _num(val)
    color = B["red"] if s.get("color") == "red" else B["yellow"]
    tmp = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    f, size = sized(ctx, tmp, val, "impact", s.get("size", 300), ctx.W * 0.86)
    fl = font("impact", ctx.px(64))
    llines = wrap(tmp, s.get("label", "").upper(), fl, ctx.W * 0.8)
    tg = tag(ctx, s["tag"], size=40) if s.get("tag") else None
    count_frames = max(1, int(min(n * 0.5, ctx.fps * 1.2)))
    y = ctx.H * 0.5 - ctx.px(size) * 0.75

    def draw(i):
        L = layer(ctx); d = ImageDraw.Draw(L)
        t = ease(min(1, i / count_frames))
        txt = _fmt(parts, parts[1] * t) if parts and s.get("count", True) else val
        w = d.textlength(txt, font=f)
        k0 = ease(min(1, i / (ctx.fps * 0.25)))
        d.text(((ctx.W - w) / 2, y + (1 - k0) * ctx.px(40)), txt, font=f, fill=fade_col(color if t >= 1 else B["white"], k0))
        ly = y + ctx.px(size) * 1.12
        for li, line in enumerate(llines):
            k = ease((i - ctx.fps * 0.3) / (ctx.fps * 0.3))
            lw = d.textlength(line, font=fl)
            d.text(((ctx.W - lw) / 2, ly + li * ctx.px(74)), line, font=fl, fill=fade_col(B["white"], k))
        source_line(ctx, d, s.get("source")); channel_bug(ctx, d)
        if tg is not None:
            paste_scaled(L, tg, ctx.W / 2, y - ctx.px(40), pop(i, int(ctx.fps * 0.2), ctx.fps))
        return L
    return graphic(ctx, s, n, draw, seed=s.get("seed", 2))


def shot_bars(ctx, s, n):
    items = s["items"]
    vals = [float(str(it[1]).replace(",", "").replace("$", "")) for it in items]
    vmax = max(abs(v) for v in vals) or 1  # negative values (falls) draw by size, label keeps the sign
    tmp = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    ft = font("impact", ctx.px(80)); fl = font("impact", ctx.px(54)); fv = font("impact", ctx.px(64))
    x0 = ctx.px(110) + max(tmp.textlength(str(it[0]).upper(), font=fl) for it in items) + ctx.px(40)
    def _lbl(v):
        return f"{s.get('prefix', '')}{int(round(v)):,}{s.get('suffix', '')}" if float(v).is_integer() else f"{s.get('prefix', '')}{v:.1f}{s.get('suffix', '')}"
    lw = max(tmp.textlength(_lbl(v), font=fv) for v in vals)
    x1 = ctx.W - max(ctx.px(360), int(lw) + ctx.px(80))   # value labels never run off the frame
    top, bh = ctx.px(320), ctx.px(96)
    gap = min(ctx.px(60), (ctx.H - ctx.px(260) - top - bh * len(items)) // max(1, len(items) - 1)) if len(items) > 1 else 0
    dtag = tag(ctx, s["delta"], size=70) if s.get("delta") else None

    def draw(i):
        L = layer(ctx); d = ImageDraw.Draw(L)
        k = ease(min(1, i / (ctx.fps * 0.3)))
        d.text((ctx.px(110), ctx.px(150)), s.get("title", "").upper(), font=ft, fill=fade_col(B["white"], k))
        d.rectangle([ctx.px(110), ctx.px(250), ctx.px(110) + ctx.px(220) * k, ctx.px(262)], fill=B["yellow"] + (255,))
        for j, (it, v) in enumerate(zip(items, vals)):
            t = ease((i - ctx.fps * (0.3 + j * 0.35)) / (ctx.fps * 0.9))
            if t <= 0:
                continue
            yy = top + j * (bh + gap)
            col = B["red"] if len(it) > 2 and it[2] == "red" else B["yellow"]
            d.text((ctx.px(110), yy + ctx.px(14)), str(it[0]).upper(), font=fl, fill=B["white"] + (255,))
            w = max(0.0, (x1 - x0) * abs(v) / vmax * t)
            d.rectangle([x0, yy, x0 + w, yy + bh], fill=col + (255,))
            vt = f"{int(round(v * t)):,}" if float(v).is_integer() else f"{v * t:.1f}"
            d.text((x0 + w + ctx.px(24), yy + ctx.px(8)), f"{s.get('prefix', '')}{vt}{s.get('suffix', '')}", font=fv, fill=B["white"] + (255,))
        source_line(ctx, d, s.get("source")); channel_bug(ctx, d)
        if dtag is not None:
            paste_scaled(L, dtag, ctx.W - ctx.px(330), ctx.px(190), pop(i, int(ctx.fps * (0.6 + 0.35 * len(items))), ctx.fps))
        return L
    return graphic(ctx, s, n, draw, seed=s.get("seed", 3))


def shot_price(ctx, s, n):
    tmp = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    head = s.get("model", "").upper()
    fh, _ = sized(ctx, tmp, head, "impact", 90, ctx.W * 0.86)
    fo = font("impact", ctx.px(150)); fn = font("impact", ctx.px(230)); fs = font("body", ctx.px(36))
    old, new = s["old"], s["new"]
    stag = tag(ctx, s["save"], size=64) if s.get("save") else None

    def draw(i):
        L = layer(ctx); d = ImageDraw.Draw(L)
        k0 = ease(min(1, i / (ctx.fps * 0.3)))
        w = d.textlength(head, font=fh)
        d.text(((ctx.W - w) / 2, ctx.px(130)), head, font=fh, fill=fade_col(B["white"], k0))
        wo = d.textlength(old, font=fo)
        ox, oy = (ctx.W - wo) / 2, ctx.px(290)
        d.text((ox, oy), old, font=fo, fill=fade_col((205, 205, 205), k0))
        k = ease((i - ctx.fps * 0.5) / (ctx.fps * 0.4))
        if k > 0:
            d.line([ox - ctx.px(10), oy + ctx.px(95), ox - ctx.px(10) + (wo + ctx.px(20)) * k, oy + ctx.px(80)], fill=B["red"] + (255,), width=ctx.px(16))
        if s.get("old_note"):
            wn = d.textlength(s["old_note"], font=fs)
            d.text(((ctx.W - wn) / 2, oy + ctx.px(185)), s["old_note"], font=fs, fill=fade_col(B["grey"], k0))
        k2 = ease((i - ctx.fps * 0.9) / (ctx.fps * 0.4))
        if k2 > 0:
            wn = d.textlength(new, font=fn)
            d.text(((ctx.W - wn) / 2, ctx.px(560) + (1 - k2) * ctx.px(50)), new, font=fn, fill=fade_col(B["yellow"], k2))
            if s.get("new_note"):
                w2 = d.textlength(s["new_note"], font=fs)
                d.text(((ctx.W - w2) / 2, ctx.px(830)), s["new_note"], font=fs, fill=fade_col(B["white"], k2))
        source_line(ctx, d, s.get("source")); channel_bug(ctx, d)
        if stag is not None:
            paste_scaled(L, stag, ctx.W * 0.8, ctx.px(560), pop(i, int(ctx.fps * 1.3), ctx.fps))
        return L
    return graphic(ctx, s, n, draw, seed=s.get("seed", 0))


def shot_questions(ctx, s, n):
    qs = s["items"]
    f = font("impact", ctx.px(78))
    cards = []
    for q in qs:
        tw = int(ImageDraw.Draw(Image.new("RGB", (1, 1))).textlength(q.upper(), font=f))
        im = Image.new("RGBA", (tw + ctx.px(90), ctx.px(120)), B["white"] + (255,))
        dd = ImageDraw.Draw(im)
        dd.rectangle([0, 0, ctx.px(18), im.height], fill=B["red"])
        dd.text((ctx.px(50), ctx.px(14)), q.upper(), font=f, fill=B["black"])
        cards.append(im)
    gap = ctx.px(40)
    y0 = (ctx.H - sum(c.height for c in cards) - gap * (len(cards) - 1)) // 2
    starts = s.get("starts") or [int(k * max(ctx.fps * 0.5, n / (len(qs) + 1))) for k in range(len(qs))]

    def draw(i):
        L = layer(ctx); y = y0
        for k, c in enumerate(cards):
            paste_scaled(L, c, ctx.W / 2, y + c.height / 2, pop(i, int(starts[k]), ctx.fps))
            y += c.height + gap
        channel_bug(ctx, ImageDraw.Draw(L))
        return L
    return graphic(ctx, s, n, draw, seed=s.get("seed", 1))


def shot_cta(ctx, s, n):
    tmp = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    head = s.get("text", "").upper()
    fh, _ = sized(ctx, tmp, head, "impact", 96, ctx.W * 0.84)
    sub = s.get("sub", "")
    fs = font("body", ctx.px(40)); fb = font("impact", ctx.px(90))
    bw, bh = ctx.px(560), ctx.px(150)

    def button(text, col):
        im = Image.new("RGBA", (bw, bh), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        d.rounded_rectangle([0, 0, bw - 1, bh - 1], radius=ctx.px(20), fill=col + (255,))
        tw = d.textlength(text, font=fb)
        d.text(((bw - tw) / 2, ctx.px(20)), text, font=fb, fill=B["white"])
        return im
    btn, pressed = button(LBL["sub"], B["red"]), button(LBL["subbed"], (90, 90, 95))
    bell = Image.new("RGBA", (ctx.px(150), ctx.px(150)), (0, 0, 0, 0))
    dl = ImageDraw.Draw(bell); c = ctx.px(75)
    dl.ellipse([0, 0, ctx.px(150) - 1, ctx.px(150) - 1], fill=B["yellow"] + (255,))
    dl.pieslice([c - ctx.px(38), c - ctx.px(46), c + ctx.px(38), c + ctx.px(30)], 180, 360, fill=B["black"])
    dl.rectangle([c - ctx.px(38), c - ctx.px(8), c + ctx.px(38), c + ctx.px(26)], fill=B["black"])
    dl.rectangle([c - ctx.px(48), c + ctx.px(22), c + ctx.px(48), c + ctx.px(32)], fill=B["black"])
    dl.ellipse([c - ctx.px(10), c + ctx.px(32), c + ctx.px(10), c + ctx.px(50)], fill=B["black"])
    press_at = int(min(n * 0.45, ctx.fps * 2.5))

    def draw(i):
        L = layer(ctx); d = ImageDraw.Draw(L)
        k = ease(min(1, i / (ctx.fps * 0.35)))
        w = d.textlength(head, font=fh)
        d.text(((ctx.W - w) / 2, ctx.px(230) + (1 - k) * ctx.px(40)), head, font=fh, fill=fade_col(B["white"], k))
        k2 = ease((i - ctx.fps * 0.3) / (ctx.fps * 0.35))
        w = d.textlength(sub, font=fs)
        d.text(((ctx.W - w) / 2, ctx.px(360)), sub, font=fs, fill=fade_col(B["yellow"], k2))
        sc = pop(i, int(ctx.fps * 0.3), ctx.fps)
        if press_at <= i < press_at + ctx.fps * 0.15:
            sc *= 0.95  # one soft press, no shaking
        paste_scaled(L, pressed if i >= press_at else btn, ctx.W / 2 - ctx.px(100), ctx.px(640), sc)
        paste_scaled(L, bell, ctx.W / 2 + ctx.px(300), ctx.px(640), pop(i, int(ctx.fps * 0.55), ctx.fps))
        channel_bug(ctx, d)
        return L
    return graphic(ctx, s, n, draw, seed=s.get("seed", 2))


R.SHOTS.update({"image": shot_image, "statement": shot_statement, "title": shot_title, "rank": shot_rank,
                "stat": shot_stat, "bars": shot_bars, "price": shot_price, "questions": shot_questions, "cta": shot_cta})


# ---------------------------------------------------------------- transitions
TRANS_CYCLE = ["slide", "zoom", "wipe", "whip", "fade"]
TRANS_DUR = {"fade": 0.5, "slide": 0.45, "zoom": 0.45, "wipe": 0.5, "whip": 0.35}


def pick_trans(prev_s, s, k):
    if s.get("trans"):
        return s["trans"]
    if prev_s is None:
        return None
    graphics = {"rank", "stat", "bars", "price", "questions", "cta", "statement", "title"}
    if s["type"] == "rank":
        return "wipe"
    if s["type"] in graphics or prev_s["type"] in graphics:
        return TRANS_CYCLE[k % 4]
    return ["fade", "slide", "fade", "zoom", "fade", "whip"][k % 6]


def transition(ctx, kind, a, b, t):
    """a = last frame of previous shot, b = current frame of new shot, t 0..1 (eased inside)."""
    e = ease(t)
    W, H = ctx.W, ctx.H
    if kind == "fade":
        return Image.blend(a, b, e)
    if kind == "slide":
        out = a.transform((W, H), Image.AFFINE, (1, 0, e * W * 0.35, 0, 1, 0), Image.BICUBIC)
        out = Image.blend(out, Image.new("RGB", (W, H), B["black"]), 0.35 * e)
        bb = b.transform((W, H), Image.AFFINE, (1, 0, -(1 - e) * W, 0, 1, 0), Image.BICUBIC)
        m = Image.new("L", (W, H), 0)
        ImageDraw.Draw(m).rectangle([(1 - e) * W, 0, W, H], fill=255)
        out.paste(bb, (0, 0), m)
        ImageDraw.Draw(out).rectangle([(1 - e) * W - ctx.px(14), 0, (1 - e) * W, H], fill=B["yellow"]) if 0 < e < 1 else None
        return out
    if kind == "zoom":
        za = 1 + 0.25 * e
        aa = a.transform((W, H), Image.EXTENT, (W / 2 - W / za / 2, H / 2 - H / za / 2, W / 2 + W / za / 2, H / 2 + H / za / 2), Image.BICUBIC)
        zb = 1.18 - 0.18 * e
        bb = b.transform((W, H), Image.EXTENT, (W / 2 - W / zb / 2, H / 2 - H / zb / 2, W / 2 + W / zb / 2, H / 2 + H / zb / 2), Image.BICUBIC)
        return Image.blend(aa, bb, e)
    if kind == "wipe":
        # a yellow band sweeps diagonally; behind it the new shot
        x = -0.3 * W + e * 1.6 * W
        band = ctx.px(140)
        m = Image.new("L", (W, H), 0)
        ImageDraw.Draw(m).polygon([(0, 0), (x - band, 0), (x - band - H * 0.35, H), (0, H)], fill=255)
        out = a.copy(); out.paste(b, (0, 0), m)
        yb = Image.new("L", (W, H), 0)
        ImageDraw.Draw(yb).polygon([(x - band, 0), (x, 0), (x - H * 0.35, H), (x - band - H * 0.35, H)], fill=255)
        out.paste(Image.new("RGB", (W, H), B["yellow"]), (0, 0), yb)
        return out
    if kind == "whip":
        # fast horizontal pan with motion blur, cut in the middle
        if e < 0.5:
            k = e / 0.5
            src, off = a, -k * W * 0.5
        else:
            k = (1 - e) / 0.5
            src, off = b, k * W * 0.5
        im = src.transform((W, H), Image.AFFINE, (1, 0, -off, 0, 1, 0), Image.BICUBIC)
        r = int(ctx.px(90) * k) | 1
        if r > 1:
            small = im.resize((W // 4, H // 4), Image.BILINEAR)
            small = small.filter(ImageFilter.BoxBlur(max(1, r // 8)))
            blur = small.resize((W, H), Image.BILINEAR)
            im = Image.blend(im, blur, min(1, k * 1.3))
        return im
    return b


# ---------------------------------------------------------------- render (resumable, with transitions)
def grade_vf(ep):
    g = ep.get("grade", {})
    return (f"eq=contrast={g.get('contrast', 1.06)}:saturation={g.get('saturation', 1.08)}:gamma={g.get('gamma', 1.0)},"
            f"noise=alls={g.get('grain', 2)}:allf=t,vignette=angle=PI/5,format=yuv420p")


def render(ep_path, preview=False, seg_shots=16):
    ep = json.load(open(ep_path))
    base = os.path.dirname(os.path.abspath(ep_path))
    W, H = (960, 540) if preview else tuple(ep.get("size", [1920, 1080]))
    fps = ep.get("fps", 24)
    ctx = R.Ctx(W, H, fps, base)
    timeline, audio, total = R.build_timeline(ep, ctx)
    out = ctx.path(ep.get("output", "out.mp4"))
    if preview:
        out = out.replace(".mp4", "-preview.mp4")
    cache = os.path.join(base, ".render_cache" + ("_preview" if preview else ""))
    os.makedirs(cache, exist_ok=True)
    print(f"[render] {len(timeline)} planos, {total / 60:.2f} min, {W}x{H}@{fps}", flush=True)
    wav = os.path.join(cache, "mix.wav")
    if not os.path.exists(wav):
        tmp = tempfile.mkdtemp(prefix="aus_")
        R.mix_audio(ep, ctx, audio, timeline, total, wav + ".part.wav", tmp)
        os.replace(wav + ".part.wav", wav)
        shutil.rmtree(tmp, ignore_errors=True)
    vf = grade_vf(ep)
    segs = [list(range(i, min(i + seg_shots, len(timeline)))) for i in range(0, len(timeline), seg_shots)]
    files = []
    for k, idxs in enumerate(segs):
        fp = os.path.join(cache, f"seg_{k:03d}.mp4")
        last_png = os.path.join(cache, f"seg_{k:03d}_last.png")
        files.append(fp)
        if os.path.exists(fp) and os.path.exists(last_png):
            continue
        prev_png = os.path.join(cache, f"seg_{k - 1:03d}_last.png")
        prev_last = Image.open(prev_png).convert("RGB") if k and os.path.exists(prev_png) else None
        part = fp + ".part.mp4"
        p = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                              "-r", str(fps), "-i", "-", "-vf", vf, "-c:v", "libx264", "-preset", "veryfast",
                              "-crf", "16", "-an", part], stdin=subprocess.PIPE)
        last = prev_last
        for idx in idxs:
            s, nf, start = timeline[idx]
            prev_s = timeline[idx - 1][0] if idx else None
            kind = pick_trans(prev_s, s, idx)
            tf = int(TRANS_DUR.get(kind, 0) * fps) if kind and prev_last is not None else 0
            tf = min(tf, max(0, nf // 2))
            for i, fr in enumerate(R.SHOTS[s["type"]](ctx, s, nf)):
                if fr.size != (W, H):
                    fr = fr.resize((W, H), Image.BICUBIC)
                if fr.mode != "RGB":
                    fr = fr.convert("RGB")
                if i < tf:
                    fr = transition(ctx, kind, prev_last, fr, (i + 1) / (tf + 1))
                p.stdin.write(fr.tobytes())
                last = fr
            prev_last = last
        p.stdin.close(); p.wait()
        if p.returncode:
            sys.exit(f"ffmpeg falhou na parte {k}")
        os.replace(part, fp)
        last.save(last_png)
        print(f"[render] parte {k + 1}/{len(segs)} pronta", flush=True)
    lst = os.path.join(cache, "list.txt")
    open(lst, "w").write("".join(f"file '{f}'\n" for f in files))
    fvf = "format=yuv420p"
    if ep.get("subtitles"):
        sub = ctx.path(ep["subtitles"]).replace("\\", "/").replace(":", "\\:").replace("'", "\\'")
        fvf = f"subtitles='{sub}'" + (":original_size=1920x1080" if preview else "") + ",format=yuv420p"
    print("[render] juntando partes + audio + legendas...", flush=True)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst, "-i", wav, "-vf", fvf,
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "24" if preview else "19", "-c:a", "aac", "-b:a", "192k",
                    "-movflags", "+faststart", "-shortest", out + ".part.mp4"], check=True)
    os.replace(out + ".part.mp4", out)
    print(f"[render] pronto -> {out}", flush=True)
    return out


# ---------------------------------------------------------------- split render (cloud: one machine per part)
def _setup(ep_path, preview=False):
    ep = json.load(open(ep_path))
    base = os.path.dirname(os.path.abspath(ep_path))
    W, H = (960, 540) if preview else tuple(ep.get("size", [1920, 1080]))
    ctx = R.Ctx(W, H, ep.get("fps", 24), base)
    timeline, audio, total = R.build_timeline(ep, ctx)
    return ep, ctx, timeline, audio, total


def plan_parts(timeline, n):
    """Contiguous groups of shots with about the same number of frames each."""
    total = sum(nf for _, nf, _ in timeline)
    groups, cur, acc, k = [], [], 0, 1
    for i, (_, nf, _) in enumerate(timeline):
        cur.append(i); acc += nf
        if acc >= total * k / n and len(groups) < n - 1:
            groups.append(cur); cur = []; k += 1
    groups.append(cur)
    return groups


def _frames(ctx, timeline, idxs, prev_last):
    W, H, fps = ctx.W, ctx.H, ctx.fps
    for idx in idxs:
        s, nf, _ = timeline[idx]
        prev_s = timeline[idx - 1][0] if idx else None
        kind = pick_trans(prev_s, s, idx)
        tf = int(TRANS_DUR.get(kind, 0) * fps) if kind and prev_last is not None else 0
        tf = min(tf, max(0, nf // 2))
        last = prev_last
        for i, fr in enumerate(R.SHOTS[s["type"]](ctx, s, nf)):
            if fr.size != (W, H):
                fr = fr.resize((W, H), Image.BICUBIC)
            if fr.mode != "RGB":
                fr = fr.convert("RGB")
            if i < tf:
                fr = transition(ctx, kind, prev_last, fr, (i + 1) / (tf + 1))
            last = fr
            yield fr
        prev_last = last


def render_part(ep_path, k, n, out, preview=False):
    ep, ctx, timeline, audio, total = _setup(ep_path, preview)
    idxs = plan_parts(timeline, n)[k]
    prev_last = None
    if idxs and idxs[0] > 0:  # the shot before this part: only its last frame is needed for the transition
        for fr in _frames(ctx, timeline, [idxs[0] - 1], None):
            prev_last = fr
    nfr = sum(timeline[i][1] for i in idxs)
    print(f"[parte {k + 1}/{n}] planos {idxs[0]}–{idxs[-1]}, {nfr} quadros", flush=True)
    p = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{ctx.W}x{ctx.H}",
                          "-r", str(ctx.fps), "-i", "-", "-vf", grade_vf(ep), "-c:v", "libx264", "-preset", "veryfast",
                          "-crf", "17", "-an", out], stdin=subprocess.PIPE)
    done = 0
    for fr in _frames(ctx, timeline, idxs, prev_last):
        p.stdin.write(fr.tobytes()); done += 1
        if done % 480 == 0:
            print(f"[parte {k + 1}/{n}] {done}/{nfr}", flush=True)
    p.stdin.close(); p.wait()
    if p.returncode or done != nfr:
        sys.exit(f"parte {k + 1} falhou ({done}/{nfr} quadros)")
    print(f"[parte {k + 1}/{n}] pronta -> {out}", flush=True)


def render_audio(ep_path, out_wav):
    ep, ctx, timeline, audio, total = _setup(ep_path)
    tmp = tempfile.mkdtemp(prefix="aus_")
    R.mix_audio(ep, ctx, audio, timeline, total, out_wav, tmp)
    shutil.rmtree(tmp, ignore_errors=True)
    print(f"[audio] {total / 60:.2f} min -> {out_wav}", flush=True)


def join(ep_path, parts, wav, out, delivery=None):
    """Joins the parts + mix + burned subtitles. delivery: also write a ~3.2 Mbps copy (fits a 500 MB upload)."""
    ep = json.load(open(ep_path))
    base = os.path.dirname(os.path.abspath(ep_path))
    lst = out + ".list.txt"
    open(lst, "w").write("".join(f"file '{os.path.abspath(f)}'\n" for f in parts))
    fvf = "format=yuv420p"
    if ep.get("subtitles"):
        sub = os.path.join(base, ep["subtitles"]).replace("\\", "/").replace(":", "\\:").replace("'", "\\'")
        fvf = f"subtitles='{sub}':fontsdir='{os.path.join(HERE_AUS, 'fonts')}',format=yuv420p"
    # one decode + one subtitle pass feeding both encodes (full quality and the small delivery copy)
    if delivery:
        fc = f"[0:v]{fvf},split=2[full][small]"
        cmd = ["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst, "-i", wav, "-filter_complex", fc,
               "-map", "[full]", "-map", "1:a", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-c:a", "aac", "-b:a", "192k",
               "-movflags", "+faststart", "-shortest", out,
               "-map", "[small]", "-map", "1:a", "-c:v", "libx264", "-preset", "veryfast", "-b:v", "2600k", "-maxrate", "3200k",
               "-bufsize", "9000k", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-shortest", delivery]
    else:
        cmd = ["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst, "-i", wav, "-vf", fvf,
               "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-c:a", "aac", "-b:a", "192k",
               "-movflags", "+faststart", "-shortest", out]
    subprocess.run(cmd, check=True)
    print(f"[join] pronto -> {out}" + (f" e {delivery}" if delivery else ""), flush=True)


HERE_AUS = os.path.dirname(os.path.abspath(__file__))

if __name__ == "__main__":
    a = sys.argv
    if "--part" in a:                       # render_aus.py ep.json --part 3/6 out.mp4
        k, n = map(int, a[a.index("--part") + 1].split("/"))
        render_part(a[1], k - 1, n, a[a.index("--part") + 2], preview="--preview" in a)
    elif "--audio" in a:                    # render_aus.py ep.json --audio mix.wav
        render_audio(a[1], a[a.index("--audio") + 1])
    elif "--join" in a:                     # render_aus.py ep.json --join mix.wav out.mp4 [--delivery small.mp4] part1.mp4 ...
        i = a.index("--join")
        wav, out = a[i + 1], a[i + 2]
        rest = a[i + 3:]
        dl = None
        if "--delivery" in rest:
            j = rest.index("--delivery"); dl = rest[j + 1]; rest = rest[:j] + rest[j + 2:]
        join(a[1], rest, wav, out, dl)
    else:
        render(a[1], preview="--preview" in a)
