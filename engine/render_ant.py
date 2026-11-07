#!/usr/bin/env python3
"""Abaixo de Zero (Antarctica channel, Portuguese) look on top of the Aussie engine (render_aus.py).

Same timeline, audio mix, split render and CLI as render_aus.py; what changes:
  * palette: night navy + ice blue + white, orange accent for numbers and alerts
  * graphics never sit on black: an animated ice plate (navy glow, topographic contour lines, drifting snow)
  * Portuguese UI: FONTE:, INSCREVA-SE / INSCRITO, channel bug "ABAIXO DE ZERO"
  * highlight layouts: compare (two values side by side), fact (place card), map (photo + pulsing marker)
  * more transitions: flash (white), blur (defocus dissolve), rise (vertical push) on top of
    fade | slide | zoom | wipe | whip, varied automatically
  * cooler grade

Usage: python3 render_ant.py episode.json [--preview] | --part k/n out.mp4 | --audio mix.wav | --join ...
"""
import math, os, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render_aus as A
from PIL import Image, ImageDraw, ImageFilter

R, B = A.R, A.B
B.update({"red": (255, 122, 26), "red_dark": (190, 80, 10), "yellow": (143, 211, 255), "white": (242, 246, 248),
          "black": (8, 20, 34), "ink": (8, 20, 34), "grey": (160, 182, 200), "orange": (255, 122, 26), "ice": (143, 211, 255)})
A.CHANNEL = os.environ.get("AUS_CHANNEL", "") or "ABAIXO DE ZERO"
font, ease, wrap = A.font, A.ease, A.wrap
layer, fade_col, paste_scaled, pop, tag, sized = A.layer, A.fade_col, A.paste_scaled, A.pop, A.tag, A.sized


# ---------------------------------------------------------------- ice plate (replaces the dark studio)
_plate = {}


def ice_plate(ctx, seed=0):
    key = (ctx.W, seed % 4)
    if key not in _plate:
        W, H = int(ctx.W * 1.3), int(ctx.H * 1.3)
        small = Image.new("RGB", (W // 4, H // 4), (8, 20, 34))
        g = ImageDraw.Draw(small)
        for y in range(small.height):   # vertical gradient: deep navy to a colder blue at the bottom
            k = y / small.height
            g.line([(0, y), (small.width, y)], fill=(int(8 + 10 * k), int(20 + 30 * k), int(34 + 46 * k)))
        spots = [((143, 211, 255), (0.2, 0.3)), ((70, 140, 210), (0.85, 0.75))]
        if seed % 2:
            spots = [((70, 140, 210), (0.15, 0.8)), ((143, 211, 255), (0.8, 0.25))]
        for col, (fx, fy) in spots:
            glow = Image.new("RGB", small.size, (0, 0, 0))
            ImageDraw.Draw(glow).ellipse([small.width * (fx - 0.35), small.height * (fy - 0.45),
                                          small.width * (fx + 0.35), small.height * (fy + 0.45)], fill=col)
            glow = glow.filter(ImageFilter.GaussianBlur(small.width // 7))
            small = Image.blend(small, glow, 0.14)
        im = small.resize((W, H), Image.BICUBIC)
        d = ImageDraw.Draw(im)
        rnd = random.Random(seed)
        # topographic contour lines, like a radar map of the bedrock under the ice
        cx, cy = W * rnd.uniform(0.3, 0.7), H * rnd.uniform(0.35, 0.65)
        for r in range(1, 26):
            rr = r * ctx.px(58)
            pts = []
            for a in range(0, 361, 6):
                t = math.radians(a)
                wob = 1 + 0.13 * math.sin(3 * t + r * 0.7) + 0.07 * math.sin(5 * t - r)
                pts.append((cx + math.cos(t) * rr * wob * 1.25, cy + math.sin(t) * rr * wob))
            d.line(pts, fill=(28, 52, 76), width=max(1, ctx.px(2)))
        _plate[key] = im
    return _plate[key]


_flakes = {}


def snow(ctx, seed=0):
    if seed not in _flakes:
        rnd = random.Random(100 + seed)
        _flakes[seed] = [(rnd.random(), rnd.random(), rnd.uniform(0.6, 2.2), rnd.uniform(0.02, 0.07), rnd.random() * 6.28)
                         for _ in range(110)]
    return _flakes[seed]


def ice_frame(ctx, i, n, seed=0):
    im = ice_plate(ctx, seed)
    t = i / max(1, n - 1)
    ox = (im.width - ctx.W) * (0.15 + 0.7 * t) if seed % 2 == 0 else (im.width - ctx.W) * (0.85 - 0.7 * t)
    oy = (im.height - ctx.H) * (0.5 + 0.25 * math.sin(t * math.pi))
    fr = im.transform((ctx.W, ctx.H), Image.EXTENT, (ox, oy, ox + ctx.W, oy + ctx.H), Image.BICUBIC)
    d = ImageDraw.Draw(fr, "RGBA")
    sec = i / ctx.fps
    for x0, y0, size, speed, ph in snow(ctx, seed):   # slow falling snow, sub-pixel positions, no flicker
        y = ((y0 + sec * speed) % 1.0) * ctx.H
        x = (x0 + 0.012 * math.sin(sec * 0.7 + ph)) % 1.0 * ctx.W
        r = ctx.px(size * 2)
        d.ellipse([x - r, y - r, x + r, y + r], fill=(235, 245, 255, 120))
    return fr


A.studio_frame = ice_frame


def source_line(ctx, d, text):
    if text:
        d.text((ctx.px(90), ctx.px(60)), "FONTE: " + text.upper(), font=font("body", ctx.px(26)), fill=B["grey"] + (255,))


A.source_line = source_line


def channel_bug(ctx, d):
    f = font("impact", ctx.px(30))
    w = d.textlength(A.CHANNEL.upper(), font=f)
    d.text((ctx.W - w - ctx.px(70), ctx.px(52)), A.CHANNEL.upper(), font=f, fill=B["ice"] + (255,))


A.channel_bug = channel_bug


# ---------------------------------------------------------------- CTA in Portuguese
def shot_cta(ctx, s, n):
    tmp = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    head = s.get("text", "").upper()
    fh, _ = sized(ctx, tmp, head, "impact", 96, ctx.W * 0.84)
    sub = s.get("sub", "")
    fs = font("body", ctx.px(40)); fb = font("impact", ctx.px(84))
    bw, bh = ctx.px(620), ctx.px(150)

    def button(text, col):
        im = Image.new("RGBA", (bw, bh), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        d.rounded_rectangle([0, 0, bw - 1, bh - 1], radius=ctx.px(20), fill=col + (255,))
        tw = d.textlength(text, font=fb)
        d.text(((bw - tw) / 2, ctx.px(24)), text, font=fb, fill=B["white"])
        return im
    btn, pressed = button("INSCREVA-SE", (220, 30, 30)), button("INSCRITO", (90, 100, 112))
    bell = Image.new("RGBA", (ctx.px(150), ctx.px(150)), (0, 0, 0, 0))
    dl = ImageDraw.Draw(bell); c = ctx.px(75)
    dl.ellipse([0, 0, ctx.px(150) - 1, ctx.px(150) - 1], fill=B["ice"] + (255,))
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
        d.text(((ctx.W - w) / 2, ctx.px(360)), sub, font=fs, fill=fade_col(B["ice"], k2))
        sc = pop(i, int(ctx.fps * 0.3), ctx.fps)
        if press_at <= i < press_at + ctx.fps * 0.15:
            sc *= 0.95
        paste_scaled(L, pressed if i >= press_at else btn, ctx.W / 2 - ctx.px(110), ctx.px(640), sc)
        paste_scaled(L, bell, ctx.W / 2 + ctx.px(320), ctx.px(640), pop(i, int(ctx.fps * 0.55), ctx.fps))
        channel_bug(ctx, d)
        return L
    return A.graphic(ctx, s, n, draw, seed=s.get("seed", 2))


# ---------------------------------------------------------------- highlight layouts
def shot_compare(ctx, s, n):
    """Two values side by side. s: title, left [label, value, note], right [...], source."""
    tmp = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    ft = font("impact", ctx.px(70)); fl = font("impact", ctx.px(56)); fn = font("body", ctx.px(36))
    title = s.get("title", "").upper()
    cols = [s["left"], s["right"]]
    fv = [sized(ctx, tmp, str(c[1]), "impact", 170, ctx.W * 0.4)[0] for c in cols]
    colors = [B["ice"], B["orange"] if s.get("accent", "right") == "right" else B["white"]]
    if s.get("accent") == "left":
        colors = [B["orange"], B["ice"]]

    def draw(i):
        L = layer(ctx); d = ImageDraw.Draw(L)
        k = ease(min(1, i / (ctx.fps * 0.3)))
        w = d.textlength(title, font=ft)
        d.text(((ctx.W - w) / 2, ctx.px(150)), title, font=ft, fill=fade_col(B["white"], k))
        d.line([(ctx.W / 2, ctx.px(330)), (ctx.W / 2, ctx.px(330) + ctx.px(520) * k)], fill=B["ice"] + (160,), width=ctx.px(4))
        for j, c in enumerate(cols):
            kk = ease((i - ctx.fps * (0.35 + 0.45 * j)) / (ctx.fps * 0.45))
            if kk <= 0:
                continue
            cx = ctx.W * (0.27 if j == 0 else 0.73)
            lab = str(c[0]).upper()
            lw = d.textlength(lab, font=fl)
            d.text((cx - lw / 2, ctx.px(360)), lab, font=fl, fill=fade_col(B["grey"], kk))
            vt = str(c[1])
            vw = d.textlength(vt, font=fv[j])
            d.text((cx - vw / 2, ctx.px(450) + (1 - kk) * ctx.px(50)), vt, font=fv[j], fill=fade_col(colors[j], kk))
            if len(c) > 2 and c[2]:
                nw = d.textlength(c[2], font=fn)
                d.text((cx - nw / 2, ctx.px(700)), c[2], font=fn, fill=fade_col(B["white"], kk))
        source_line(ctx, d, s.get("source")); channel_bug(ctx, d)
        return L
    return A.graphic(ctx, s, n, draw, seed=s.get("seed", 3))


def shot_fact(ctx, s, n):
    """Place / discovery card over its photo (blurred, darkened): name, tag, 2-4 rows of facts."""
    over = 1.15
    W2, H2 = int(ctx.W * over), int(ctx.H * over)
    img = R.load_image(ctx, s["bg"], W2, H2, (0.5, 0.5))
    dark = img.filter(ImageFilter.GaussianBlur(ctx.px(10)))
    dark = Image.blend(dark, Image.new("RGB", dark.size, B["black"]), 0.55)
    sharp = img
    fn = font("impact", ctx.px(96)); fk = font("body", ctx.px(34)); fv = font("impact", ctx.px(54))
    rows = s.get("rows", [])
    tg = tag(ctx, s["tag"], color=B["orange"], size=36) if s.get("tag") else None
    pw = int(ctx.W * 0.42)

    def frame(i):
        t = i / max(1, n - 1)
        z = 1.0 + 0.08 * t
        cw, ch = W2 / z, H2 / z
        box = (W2 / 2 - cw / 2, H2 / 2 - ch / 2, W2 / 2 + cw / 2, H2 / 2 + ch / 2)
        fr = dark.transform((ctx.W, ctx.H), Image.EXTENT, box, Image.BICUBIC)
        # the photo itself, sharp, in a framed window on the right
        win = sharp.transform((int(ctx.W * 0.46), int(ctx.H * 0.62)), Image.EXTENT, box, Image.BICUBIC)
        k = ease(min(1, i / (ctx.fps * 0.45)))
        wx = int(ctx.W * 0.5 + (1 - k) * ctx.px(120)); wy = int(ctx.H * 0.19)
        fr.paste(win, (wx, wy))
        d = ImageDraw.Draw(fr, "RGBA")
        d.rectangle([wx, wy, wx + win.width, wy + win.height], outline=B["ice"] + (255,), width=ctx.px(4))
        x, y = ctx.px(110), ctx.px(220)
        if tg is not None:
            fr.paste(tg, (x, y - tg.height - ctx.px(16)), tg)
        for line in wrap(d, s["name"].upper(), fn, pw):
            d.text((x, y + (1 - k) * ctx.px(30)), line, font=fn, fill=fade_col(B["white"], k))
            y += ctx.px(104)
        d.rectangle([x, y + ctx.px(10), x + ctx.px(200) * k, y + ctx.px(20)], fill=B["orange"] + (255,))
        y += ctx.px(60)
        for j, (key, val) in enumerate(rows):
            kk = ease((i - ctx.fps * (0.5 + 0.3 * j)) / (ctx.fps * 0.35))
            if kk <= 0:
                continue
            d.text((x, y), str(key).upper(), font=fk, fill=fade_col(B["grey"], kk))
            d.text((x, y + ctx.px(40)), str(val), font=fv, fill=fade_col(B["ice"], kk))
            y += ctx.px(120)
        source_line(ctx, d, s.get("source")); channel_bug(ctx, d)
        return fr
    for i in range(n):
        yield frame(i)


def shot_map(ctx, s, n):
    """Photo/map with slow push toward a pulsing marker and a label. s: src, x, y (0..1), label, sub."""
    over = 1.25
    W2, H2 = int(ctx.W * over), int(ctx.H * over)
    img = R.load_image(ctx, s["src"], W2, H2, (0.5, 0.5))
    mx, my = s.get("x", 0.5), s.get("y", 0.5)
    fl = font("impact", ctx.px(60)); fs = font("body", ctx.px(34))
    for i in range(n):
        t = ease(i / max(1, n - 1)) * 0.9 + 0.1 * i / max(1, n - 1)
        z = 1.0 + 0.35 * t
        cw, ch = W2 / z, H2 / z
        cx = W2 / 2 + (mx * W2 - W2 / 2) * t * 0.8
        cy = H2 / 2 + (my * H2 - H2 / 2) * t * 0.8
        cx = min(max(cx, cw / 2), W2 - cw / 2); cy = min(max(cy, ch / 2), H2 - ch / 2)
        box = (cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2)
        fr = img.transform((ctx.W, ctx.H), Image.EXTENT, box, Image.BICUBIC)
        px_ = (mx * W2 - box[0]) / cw * ctx.W
        py_ = (my * H2 - box[1]) / ch * ctx.H
        d = ImageDraw.Draw(fr, "RGBA")
        k = ease(min(1, i / (ctx.fps * 0.4)))
        ph = (i / ctx.fps) % 1.4 / 1.4
        rr = ctx.px(18 + 70 * ph)
        d.ellipse([px_ - rr, py_ - rr, px_ + rr, py_ + rr], outline=B["orange"] + (int(230 * (1 - ph)),), width=ctx.px(5))
        r0 = ctx.px(16) * k
        d.ellipse([px_ - r0, py_ - r0, px_ + r0, py_ + r0], fill=B["orange"] + (255,), outline=B["white"] + (255,), width=ctx.px(3))
        if s.get("label") and k > 0:
            lab = s["label"].upper()
            lw = d.textlength(lab, font=fl)
            lx = px_ + ctx.px(40) if px_ < ctx.W * 0.62 else px_ - ctx.px(40) - lw - ctx.px(40)
            ly = py_ - ctx.px(48)
            d.rectangle([lx, ly, lx + lw + ctx.px(40), ly + ctx.px(78)], fill=B["black"] + (int(215 * k),))
            d.rectangle([lx, ly, lx + ctx.px(8), ly + ctx.px(78)], fill=B["orange"] + (255,))
            d.text((lx + ctx.px(22), ly + ctx.px(6)), lab, font=fl, fill=fade_col(B["white"], k))
            if s.get("sub"):
                d.text((lx + ctx.px(22), ly + ctx.px(88)), s["sub"], font=fs, fill=fade_col(B["ice"], k))
        channel_bug(ctx, d)
        yield fr


R.SHOTS.update({"cta": shot_cta, "compare": shot_compare, "fact": shot_fact, "map": shot_map})

# ---------------------------------------------------------------- transitions
A.TRANS_DUR.update({"flash": 0.4, "blur": 0.55, "rise": 0.45})
_base_transition = A.transition
GRAPHICS = {"rank", "stat", "bars", "price", "questions", "cta", "statement", "title", "compare", "fact"}
CYCLE_FOOTAGE = ["fade", "slide", "blur", "zoom", "fade", "whip", "rise", "flash", "fade", "wipe"]
CYCLE_GRAPHIC = ["zoom", "slide", "wipe", "rise", "blur"]


def pick_trans(prev_s, s, k):
    if s.get("trans"):
        return s["trans"]
    if prev_s is None:
        return None
    if s["type"] in GRAPHICS or prev_s["type"] in GRAPHICS:
        return CYCLE_GRAPHIC[k % len(CYCLE_GRAPHIC)]
    return CYCLE_FOOTAGE[k % len(CYCLE_FOOTAGE)]


def transition(ctx, kind, a, b, t):
    e = ease(t)
    W, H = ctx.W, ctx.H
    if kind == "flash":   # white flash: up to white, then the new shot comes out of it
        white = Image.new("RGB", (W, H), (250, 252, 255))
        return Image.blend(a, white, min(1, e * 2)) if e < 0.5 else Image.blend(white, b, min(1, (e - 0.5) * 2))
    if kind == "blur":    # defocus dissolve
        r = ctx.px(28) * math.sin(math.pi * e)
        mix = Image.blend(a, b, e)
        if r >= 1:
            small = mix.resize((W // 4, H // 4), Image.BILINEAR).filter(ImageFilter.GaussianBlur(max(1, r / 4)))
            mix = Image.blend(mix, small.resize((W, H), Image.BILINEAR), min(1, math.sin(math.pi * e) * 1.2))
        return mix
    if kind == "rise":    # the new shot pushes the old one up
        out = a.transform((W, H), Image.AFFINE, (1, 0, 0, 0, 1, e * H * 0.3), Image.BICUBIC)
        bb = b.transform((W, H), Image.AFFINE, (1, 0, 0, 0, 1, -(1 - e) * H), Image.BICUBIC)
        m = Image.new("L", (W, H), 0)
        ImageDraw.Draw(m).rectangle([0, (1 - e) * H, W, H], fill=255)
        out.paste(bb, (0, 0), m)
        if 0 < e < 1:
            ImageDraw.Draw(out).rectangle([0, (1 - e) * H - ctx.px(10), W, (1 - e) * H], fill=B["ice"])
        return out
    return _base_transition(ctx, kind, a, b, t)


A.pick_trans, A.transition = pick_trans, transition


def grade_vf(ep):
    g = ep.get("grade", {})
    return (f"eq=contrast={g.get('contrast', 1.05)}:saturation={g.get('saturation', 0.95)}:gamma={g.get('gamma', 1.0)},"
            f"colorbalance=rs=-0.02:bs=0.04:rm=-0.01:bm=0.02,"
            f"noise=alls={g.get('grain', 2)}:allf=t,vignette=angle=PI/5,format=yuv420p")


A.grade_vf = grade_vf

if __name__ == "__main__":
    a = sys.argv
    if "--part" in a:
        k, n = map(int, a[a.index("--part") + 1].split("/"))
        A.render_part(a[1], k - 1, n, a[a.index("--part") + 2], preview="--preview" in a)
    elif "--audio" in a:
        A.render_audio(a[1], a[a.index("--audio") + 1])
    elif "--join" in a:
        i = a.index("--join")
        wav, out = a[i + 1], a[i + 2]
        rest = a[i + 3:]
        dl = None
        if "--delivery" in rest:
            j = rest.index("--delivery"); dl = rest[j + 1]; rest = rest[:j] + rest[j + 2:]
        A.join(a[1], rest, wav, out, dl)
    else:
        A.render(a[1], preview="--preview" in a)
