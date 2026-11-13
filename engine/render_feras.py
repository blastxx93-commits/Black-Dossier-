#!/usr/bin/env python3
"""Era das Feras (Portuguese "who would win" channel) look on top of the Aussie engine (render_aus.py).

Style taken from the reference video (Mundo Fósil): warm wildlife-documentary grade, ivory label tags with black
serif type, measurement bars over the animal ("200 kg"), serif title lines over the scene darkened and blurred,
small amber badges, black-and-white freeze before a verdict, punch-in close-ups. On top of it, retention devices
that the reference does not have:
  * round card   (RODADA 3 + beast name + 10-dot progress)        type "round"
  * versus       (split screen, names, weights, VS badge)           type "versus"
  * scoreboard   (TIGRE n x m FERAS, the changed number flips)      type "score"
  * verdict      (scene goes black and white, stamp pops)           type "verdict"
  * measure      (photo + animated scale bar and value)             type "measure"
  * serif        (2-3 lines: small italic intro + big serif line)   type "serif"
  * ficha        (fact sheet: photo window + rows)                  type "ficha"
  * HUD          any image/video shot with "hud": [round, tiger, beasts] shows a corner tracker
Graphics never sit on black: they use their own scene blurred and darkened ("bg"), or a warm foggy snow plate.
Transitions: fade, slide, zoom, wipe, whip (base) + flash, blur, punch, mono; the edit kit picks one per cut
and pairs it with a different sound effect each time (engine/feras_kit.py).

Usage: python3 render_feras.py episode.json [--preview] | --part k/n out.mp4 | --audio mix.wav | --join ...
"""
import math, os, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render_aus as A
from PIL import Image, ImageDraw, ImageFilter, ImageOps

R, B = A.R, A.B
B.update({"ivory": (242, 232, 213), "char": (20, 18, 16), "amber": (224, 122, 31), "gold": (242, 167, 27),
          "blood": (192, 41, 33), "white": (246, 242, 234), "black": (20, 18, 16), "ink": (20, 18, 16),
          "grey": (190, 180, 165), "red": (192, 41, 33), "red_dark": (130, 25, 18), "yellow": (242, 167, 27)})
R.FONT_CANDIDATES["serif"] = ["fonts/DMSerifDisplay-Regular.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"]
A.CHANNEL = os.environ.get("AUS_CHANNEL", "") or "ERA DAS FERAS"
font, ease, wrap = A.font, A.ease, A.wrap
layer, fade_col, paste_scaled, pop, sized = A.layer, A.fade_col, A.paste_scaled, A.pop, A.sized


def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


# ---------------------------------------------------------------- backgrounds: own scene blurred, or foggy snow plate
_bgcache = {}


def blurred_bg(ctx, src, darken=0.55, blur=14, mono=False):
    key = (src, ctx.W, darken, blur, mono)
    if key not in _bgcache:
        W2, H2 = int(ctx.W * 1.2), int(ctx.H * 1.2)
        im = R.load_image(ctx, src, W2, H2, (0.5, 0.5))
        small = im.resize((W2 // 4, H2 // 4), Image.BILINEAR).filter(ImageFilter.GaussianBlur(max(1, ctx.px(blur) // 4)))
        im = small.resize((W2, H2), Image.BICUBIC)
        if mono:
            im = ImageOps.grayscale(im).convert("RGB")
        _bgcache[key] = Image.blend(im, Image.new("RGB", im.size, B["char"]), darken)
    return _bgcache[key]


_plate = {}


def fog_plate(ctx, seed=0):
    key = (ctx.W, seed % 3)
    if key not in _plate:
        W, H = int(ctx.W * 1.3), int(ctx.H * 1.3)
        small = Image.new("RGB", (W // 4, H // 4))
        g = ImageDraw.Draw(small)
        for y in range(small.height):   # warm dusk sky to cold snow, like the Ice Age steppe of the channel
            k = y / small.height
            g.line([(0, y), (small.width, y)], fill=(int(46 + 30 * k), int(38 + 32 * k), int(34 + 38 * k)))
        rnd = random.Random(seed)
        for _ in range(7):
            fx, fy = rnd.random(), rnd.uniform(0.3, 1)
            glow = Image.new("RGB", small.size, (0, 0, 0))
            ImageDraw.Draw(glow).ellipse([small.width * (fx - 0.3), small.height * (fy - 0.2),
                                          small.width * (fx + 0.3), small.height * (fy + 0.2)], fill=(200, 190, 175))
            small = Image.blend(small, glow.filter(ImageFilter.GaussianBlur(small.width // 9)), 0.08)
        _plate[key] = small.resize((W, H), Image.BICUBIC)
    return _plate[key]


_flakes = {}


def snow_layer(ctx, d, sec, seed=0, alpha=110, count=90):
    if seed not in _flakes:
        rnd = random.Random(300 + seed)
        _flakes[seed] = [(rnd.random(), rnd.random(), rnd.uniform(0.6, 2.0), rnd.uniform(0.03, 0.08), rnd.random() * 6.28)
                         for _ in range(count)]
    for x0, y0, size, speed, ph in _flakes[seed]:
        y = ((y0 + sec * speed) % 1.0) * ctx.H
        x = (x0 + 0.015 * math.sin(sec * 0.6 + ph)) % 1.0 * ctx.W
        r = ctx.px(size * 2)
        d.ellipse([x - r, y - r, x + r, y + r], fill=(250, 248, 244, alpha))


def plate_frame(ctx, i, n, seed=0):
    im = fog_plate(ctx, seed)
    t = i / max(1, n - 1)
    ox = (im.width - ctx.W) * (0.2 + 0.6 * t)
    oy = (im.height - ctx.H) * 0.5
    fr = im.transform((ctx.W, ctx.H), Image.EXTENT, (ox, oy, ox + ctx.W, oy + ctx.H), Image.BICUBIC)
    snow_layer(ctx, ImageDraw.Draw(fr, "RGBA"), i / ctx.fps, seed)
    return fr


A.studio_frame = plate_frame


def bg_frame(ctx, s, i, n, mono=False):
    """Background of a graphic: its scene ("bg") blurred + darkened with a slow drift, else the snow plate."""
    if s.get("bg"):
        im = blurred_bg(ctx, s["bg"], s.get("darken", 0.55), mono=mono)
        t = i / max(1, n - 1)
        z = 1.0 + 0.06 * t
        cw, ch = im.width / 1.2 / z * 1.0, im.height / 1.2 / z
        cx, cy = im.width / 2 + (im.width - cw) * 0.3 * (t - 0.5), im.height / 2
        return im.transform((ctx.W, ctx.H), Image.EXTENT, (cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2), Image.BICUBIC)
    return plate_frame(ctx, i, n, s.get("seed", 0))


def graphic(ctx, s, n, draw_layer, mono=False):
    for i in range(n):
        fr = bg_frame(ctx, s, i, n, mono)
        lay = draw_layer(i)
        fr.paste(lay, (0, 0), lay)
        yield A.push(ctx, fr, ease(i / max(1, n - 1)), 1.0, 1.03)


A.graphic = lambda ctx, s, n, draw_layer, seed=0: graphic(ctx, s, n, draw_layer)


def channel_bug(ctx, d):
    f = font("body", ctx.px(26))
    w = d.textlength(A.CHANNEL, font=f)
    d.text((ctx.W - w - ctx.px(60), ctx.px(46)), A.CHANNEL, font=f, fill=B["ivory"] + (200,))


A.channel_bug = channel_bug


def source_line(ctx, d, text):
    if text:
        d.text((ctx.px(70), ctx.H - ctx.px(70)), "Fonte: " + text, font=font("body", ctx.px(24)), fill=B["grey"] + (230,))


A.source_line = source_line


# ---------------------------------------------------------------- ivory label (reference: "TIGRE SIBERIANO")
def label_img(ctx, text, size=44, fg=None, bgc=None, serif=True):
    f = font("serif" if serif else "impact", ctx.px(size))
    tw = int(ImageDraw.Draw(Image.new("RGBA", (1, 1))).textlength(text, font=f))
    padx, pady = ctx.px(size * 0.45), ctx.px(size * 0.16)
    im = Image.new("RGBA", (tw + 2 * padx, int(ctx.px(size) * 1.25) + 2 * pady), (bgc or B["ivory"]) + (240,))
    ImageDraw.Draw(im).text((padx, pady), text, font=f, fill=(fg or B["char"]))
    return im


def caption_layer(ctx, text):
    """'small|BIG' -> amber badge above an ivory label; plain text -> ivory label. Bottom-left, like the reference."""
    im = layer(ctx)
    small, _, big = text.partition("|")
    if not big:
        small, big = "", small
    lab = label_img(ctx, big.strip().upper(), 44)
    x, y = ctx.px(70), ctx.H - ctx.px(110) - lab.height
    im.paste(lab, (x, y), lab)
    if small.strip():
        b = label_img(ctx, small.strip().upper(), 28, fg=B["white"], bgc=B["amber"], serif=False)
        im.paste(b, (x, y - b.height - ctx.px(8)), b)
    return im


R.caption_layer = caption_layer
A.caption_layer = caption_layer


# ---------------------------------------------------------------- HUD: corner round tracker on footage
def hud_layer(ctx, hud):
    rnd, a, b = hud[:3]
    im = layer(ctx); d = ImageDraw.Draw(im)
    f1 = font("impact", ctx.px(26)); f2 = font("serif", ctx.px(40))
    txt = f"RODADA {rnd}/{hud[3] if len(hud) > 3 else 10}" if isinstance(rnd, int) else str(rnd).upper()
    sc = f"{a} × {b}"
    w1 = d.textlength(txt, font=f1); w2 = d.textlength(sc, font=f2)
    bw = max(w1, w2) + ctx.px(44)
    x0, y0 = ctx.W - bw - ctx.px(50), ctx.px(40)
    d.rounded_rectangle([x0, y0, x0 + bw, y0 + ctx.px(108)], radius=ctx.px(10), fill=B["char"] + (185,))
    d.rectangle([x0, y0, x0 + bw, y0 + ctx.px(6)], fill=B["amber"] + (255,))
    d.text((x0 + (bw - w1) / 2, y0 + ctx.px(14)), txt, font=f1, fill=B["ivory"] + (255,))
    d.text((x0 + (bw - w2) / 2, y0 + ctx.px(46)), sc, font=f2, fill=B["gold"] + (255,))
    return im


def with_hud(fn):
    def wrapped(ctx, s, n):
        hl = hud_layer(ctx, s["hud"]) if s.get("hud") else None
        for i, fr in enumerate(fn(ctx, s, n)):
            if hl is not None:
                fr = fr.convert("RGB") if fr.mode != "RGB" else fr
                if i < ctx.fps * 0.4:   # fades in
                    tmp = hl.copy(); tmp.putalpha(tmp.split()[3].point(lambda v, k=i / (ctx.fps * 0.4): int(v * k)))
                    fr.paste(tmp, (0, 0), tmp)
                else:
                    fr.paste(hl, (0, 0), hl)
            yield fr
    return wrapped


# ---------------------------------------------------------------- shots
def shot_serif(ctx, s, n):
    """Reference title card: 'El duelo / Frente a frente / Campo abierto.' over the scene darkened."""
    lines = s.get("lines", [])
    big = s.get("text", "")
    fs = font("serif", ctx.px(44)); fb, _ = sized(ctx, ImageDraw.Draw(Image.new("RGB", (1, 1))), big, "serif", s.get("size", 120), ctx.W * 0.86)

    def draw(i):
        L = layer(ctx); d = ImageDraw.Draw(L)
        y = ctx.H * 0.40 - len(lines) * ctx.px(52)
        x = ctx.W * 0.5
        for j, ln in enumerate(lines):
            k = ease(clamp((i - ctx.fps * 0.18 * j) / (ctx.fps * 0.35)))
            w = d.textlength(ln, font=fs)
            d.text((x - w / 2 + (j - 0.5) * ctx.px(60), y + (1 - k) * ctx.px(20)), ln, font=fs, fill=fade_col(B["ivory"], k))
            y += ctx.px(56)
        k = ease(clamp((i - ctx.fps * (0.18 * len(lines) + 0.1)) / (ctx.fps * 0.4)))
        w = d.textlength(big, font=fb)
        # letters settle from a slight spread (as in the reference)
        d.text((x - w / 2, y + ctx.px(10) + (1 - k) * ctx.px(26)), big, font=fb, fill=fade_col(B["white"], k))
        return L
    return graphic(ctx, s, n, draw)


def shot_round(ctx, s, n):
    """RODADA N + beast name + progress dots."""
    num, name, sub = s["num"], s.get("name", ""), s.get("sub", "")
    tmp = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    fn = font("serif", ctx.px(330)); fname, _ = sized(ctx, tmp, name, "serif", 120, ctx.W * 0.86)
    fsub = font("body", ctx.px(40)); ftag = font("impact", ctx.px(44))
    total = s.get("of", 10)

    def draw(i):
        L = layer(ctx); d = ImageDraw.Draw(L)
        k = ease(clamp(i / (ctx.fps * 0.35)))
        tag = "RODADA FINAL" if num == "F" else "RODADA"
        tw = d.textlength(tag, font=ftag)
        bx = (ctx.W - tw) / 2 - ctx.px(24)
        d.rectangle([bx, ctx.px(150), bx + tw + ctx.px(48), ctx.px(220)], fill=B["amber"] + (int(255 * k),))
        d.text((bx + ctx.px(24), ctx.px(156)), tag, font=ftag, fill=fade_col(B["white"], k))
        if num != "F":
            sc = pop(i, int(ctx.fps * 0.12), ctx.fps, 0.35)
            numim = Image.new("RGBA", (ctx.px(520), ctx.px(420)), (0, 0, 0, 0))
            dn = ImageDraw.Draw(numim); t = str(num)
            dn.text(((numim.width - dn.textlength(t, font=fn)) / 2, 0), t, font=fn, fill=B["gold"] + (255,))
            paste_scaled(L, numim, ctx.W / 2, ctx.px(430), 0.6 + 0.4 * sc, alpha=min(1, sc))
        k2 = ease(clamp((i - ctx.fps * 0.45) / (ctx.fps * 0.4)))
        w = d.textlength(name, font=fname)
        y = ctx.px(650) if num != "F" else ctx.px(420)
        d.text(((ctx.W - w) / 2, y + (1 - k2) * ctx.px(30)), name, font=fname, fill=fade_col(B["ivory"], k2))
        if sub:
            w = d.textlength(sub, font=fsub)
            d.text(((ctx.W - w) / 2, y + ctx.px(150)), sub, font=fsub, fill=fade_col(B["grey"], k2))
        if num != "F":
            gap = ctx.px(44); x0 = ctx.W / 2 - gap * (total - 1) / 2; yy = ctx.H - ctx.px(110)
            for j in range(total):
                r = ctx.px(9) if j + 1 != num else ctx.px(14)
                col = B["gold"] if j + 1 < num else (B["amber"] if j + 1 == num else B["grey"])
                a = 255 if j + 1 <= num else 110
                d.ellipse([x0 + j * gap - r, yy - r, x0 + j * gap + r, yy + r], fill=col + (int(a * k),))
        channel_bug(ctx, d)
        return L
    return graphic(ctx, s, n, draw)


def shot_versus(ctx, s, n):
    """Split screen: left = tiger, right = beast; diagonal seam, names and key number, VS badge."""
    W, H = ctx.W, ctx.H
    pw, ph = int(W * 0.62), int(H * 1.1)
    L_im = R.load_image(ctx, s["left"]["src"], pw, ph, tuple(s["left"].get("focus", (0.5, 0.45))))
    R_im = R.load_image(ctx, s["right"]["src"], pw, ph, tuple(s["right"].get("focus", (0.5, 0.45))))
    fname = font("serif", ctx.px(64)); fstat = font("impact", ctx.px(46)); fvs = font("serif", ctx.px(150))
    mask = Image.new("L", (W, H), 0)
    ImageDraw.Draw(mask).polygon([(W * 0.56, 0), (W, 0), (W, H), (W * 0.44, H)], fill=255)

    def frame(i):
        t = i / max(1, n - 1)
        k = ease(clamp(i / (ctx.fps * 0.45)))
        fr = Image.new("RGB", (W, H), B["char"])
        lx = int(-(1 - k) * W * 0.25 - t * ctx.px(30))
        fr.paste(L_im.crop((0, int((ph - H) / 2), pw, int((ph - H) / 2) + H)), (lx, 0))
        right = Image.new("RGB", (W, H), B["char"])
        rx = int(W - pw + (1 - k) * W * 0.25 + t * ctx.px(30))
        right.paste(R_im.crop((0, int((ph - H) / 2), pw, int((ph - H) / 2) + H)), (rx, 0))
        fr.paste(right, (0, 0), mask)
        d = ImageDraw.Draw(fr, "RGBA")
        d.line([(W * 0.56, 0), (W * 0.44, H)], fill=B["ivory"] + (255,), width=ctx.px(8))
        for side, data, x in (("l", s["left"], ctx.px(70)), ("r", s["right"], None)):
            kk = ease(clamp((i - ctx.fps * (0.35 if side == "l" else 0.55)) / (ctx.fps * 0.35)))
            if kk <= 0:
                continue
            nm = data["name"].upper(); st = data.get("stat", "")
            lab = label_img(ctx, nm, 48)
            sx = x if x is not None else W - ctx.px(70) - lab.height * 0 - lab.width
            y = H - ctx.px(230)
            lab2 = lab.copy(); lab2.putalpha(lab2.split()[3].point(lambda v: int(v * kk)))
            fr.paste(lab2, (int(sx), int(y + (1 - kk) * ctx.px(30))), lab2)
            if st:
                sw = d.textlength(st, font=fstat)
                tx = sx if x is not None else W - ctx.px(70) - sw
                d.text((tx, y + lab.height + ctx.px(12)), st, font=fstat, fill=fade_col(B["gold"], kk))
        sc = pop(i, int(ctx.fps * 0.75), ctx.fps, 0.3)
        if sc > 0:
            badge = Image.new("RGBA", (ctx.px(260), ctx.px(260)), (0, 0, 0, 0))
            db = ImageDraw.Draw(badge)
            db.ellipse([0, 0, badge.width - 1, badge.height - 1], fill=B["amber"] + (255,), outline=B["ivory"] + (255,), width=ctx.px(8))
            tw = db.textlength("VS", font=fvs)
            db.text(((badge.width - tw) / 2, ctx.px(30)), "VS", font=fvs, fill=B["white"])
            paste_scaled(fr, badge, W / 2, H / 2, 0.5 + 0.5 * sc)
        channel_bug(ctx, d)
        return fr
    for i in range(n):
        yield frame(i)


def shot_score(ctx, s, n):
    """TIGRE a × b FERAS; prev -> new: the number that changed flips at 0.6 s with a gold/red flash."""
    a0, b0 = s.get("prev", [0, 0]); a1, b1 = s["now"]
    fn = font("serif", ctx.px(260)); fl = font("impact", ctx.px(58)); fx_ = font("serif", ctx.px(150))
    fsub = font("body", ctx.px(40))
    sub = s.get("sub", "")

    def draw(i):
        L = layer(ctx); d = ImageDraw.Draw(L)
        k = ease(clamp(i / (ctx.fps * 0.3)))
        flip = clamp((i - ctx.fps * 0.6) / (ctx.fps * 0.25))
        cw = ctx.px(600); ch_ = ctx.px(420); x0 = (ctx.W - cw * 2 - ctx.px(80)) / 2; y0 = ctx.px(250)
        la, lb = s.get("labels", ["TIGRE", "FERAS"])
        for j, (lab, v0, v1, col) in enumerate(((la, a0, a1, B["gold"]), (lb, b0, b1, B["blood"] if lb == "FERAS" else B["amber"]))):
            x = x0 + j * (cw + ctx.px(80))
            d.rounded_rectangle([x, y0, x + cw, y0 + ch_], radius=ctx.px(18), fill=B["char"] + (int(215 * k),),
                                outline=col + (int(255 * k),), width=ctx.px(5))
            lw = d.textlength(lab, font=fl)
            d.text((x + (cw - lw) / 2, y0 + ctx.px(26)), lab, font=fl, fill=fade_col(B["ivory"], k))
            changed = v0 != v1
            v = v1 if (flip >= 0.5 or not changed) else v0
            squash = abs(1 - 2 * flip) if changed and 0 < flip < 1 else 1.0
            t = str(v)
            num = Image.new("RGBA", (cw, ctx.px(300)), (0, 0, 0, 0))
            dn = ImageDraw.Draw(num)
            dn.text(((cw - dn.textlength(t, font=fn)) / 2, 0), t, font=fn, fill=(col if changed and flip >= 0.5 else B["white"]) + (255,))
            if squash < 1:
                num = num.resize((cw, max(1, int(num.height * squash))), Image.BICUBIC)
            L.paste(num, (int(x), int(y0 + ctx.px(110) + (ctx.px(300) - num.height) / 2)), num)
        w = d.textlength("×", font=fx_)
        d.text(((ctx.W - w) / 2, y0 + ctx.px(110)), "×", font=fx_, fill=fade_col(B["grey"], k))
        if sub:
            k2 = ease(clamp((i - ctx.fps * 0.9) / (ctx.fps * 0.3)))
            w = d.textlength(sub, font=fsub)
            d.text(((ctx.W - w) / 2, y0 + ch_ + ctx.px(60)), sub, font=fsub, fill=fade_col(B["ivory"], k2))
        channel_bug(ctx, d)
        return L
    return graphic(ctx, s, n, draw)


def shot_verdict(ctx, s, n):
    """The scene, moving, drains to black and white; then the verdict stamp pops (tiger gold / beasts red / draw ivory)."""
    over = 1.18
    W2, H2 = int(ctx.W * over), int(ctx.H * over)
    img = R.load_image(ctx, s["src"], W2, H2, tuple(s.get("focus", (0.5, 0.5))))
    gray = ImageOps.grayscale(img).convert("RGB")
    win = s.get("winner", "tigre")
    col = {"tigre": B["gold"], "feras": B["blood"], "empate": B["ivory"]}[win]
    text = s.get("text") or {"tigre": "VITÓRIA DO TIGRE", "feras": "VITÓRIA DA FERA", "empate": "EMPATE"}[win]
    fs = font("serif", ctx.px(110)); fsm = font("impact", ctx.px(36))
    tmp = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    tw = tmp.textlength(text, font=fs)
    st = Image.new("RGBA", (int(tw + ctx.px(160)), ctx.px(230)), (0, 0, 0, 0))
    ds = ImageDraw.Draw(st)
    ds.rectangle([0, 0, st.width - 1, st.height - 1], outline=col + (255,), width=ctx.px(10))
    ds.rectangle([ctx.px(16), ctx.px(16), st.width - ctx.px(17), st.height - ctx.px(17)], outline=col + (255,), width=ctx.px(3))
    sw = ds.textlength("VEREDITO", font=fsm)
    ds.text(((st.width - sw) / 2, ctx.px(28)), "VEREDITO", font=fsm, fill=col + (255,))
    ds.text(((st.width - tw) / 2, ctx.px(68)), text, font=fs, fill=col + (255,))
    st = st.rotate(s.get("angle", -6), resample=Image.BICUBIC, expand=True)
    t_mono, t_stamp = ctx.fps * 0.25, ctx.fps * 0.55
    for i in range(n):
        t = i / max(1, n - 1)
        z = 1.0 + 0.12 * t
        cw, ch = W2 / z, H2 / z
        box = (W2 / 2 - cw / 2, H2 / 2 - ch / 2, W2 / 2 + cw / 2, H2 / 2 + ch / 2)
        m = clamp((i - t_mono) / (ctx.fps * 0.2))
        src = Image.blend(img, gray, m) if 0 < m < 1 else (gray if m >= 1 else img)
        fr = src.transform((ctx.W, ctx.H), Image.EXTENT, box, Image.BICUBIC)
        if m > 0:
            fr = Image.blend(fr, Image.new("RGB", fr.size, B["char"]), 0.25 * m)
        sc = pop(i, int(t_stamp), ctx.fps, 0.22)
        if sc > 0:
            paste_scaled(fr, st, ctx.W / 2, ctx.H / 2, 1.6 - 0.6 * sc, alpha=min(1, sc * 1.3))
        d = ImageDraw.Draw(fr, "RGBA"); channel_bug(ctx, d)
        yield fr


def shot_measure(ctx, s, n):
    """Photo with Ken Burns + a vertical scale bar that grows to the value (reference: '200 kg' next to the tiger)."""
    base = A.shot_image(ctx, dict(s, type="image", caption=None), n)
    value = s["value"]; side = s.get("side", "right")
    f = font("serif", ctx.px(64))
    x = ctx.W * (0.82 if side == "right" else 0.18)
    y_top, y_bot = ctx.H * s.get("top", 0.12), ctx.H * s.get("bottom", 0.78)
    cap = caption_layer(ctx, s["caption"]) if s.get("caption") else None
    for i, fr in enumerate(base):
        fr = fr.convert("RGB")
        d = ImageDraw.Draw(fr, "RGBA")
        k = ease(clamp((i - ctx.fps * 0.2) / (ctx.fps * 0.7)))
        yk = y_bot - (y_bot - y_top) * k
        wcol = B["white"] + (230,)
        d.line([(x, y_bot), (x, yk)], fill=wcol, width=ctx.px(3))
        d.line([(x - ctx.px(16), y_bot), (x + ctx.px(16), y_bot)], fill=wcol, width=ctx.px(3))
        if k > 0.05:
            d.line([(x - ctx.px(16), yk), (x + ctx.px(16), yk)], fill=wcol, width=ctx.px(3))
        for j in range(1, 10):
            yy = y_bot - (y_bot - y_top) * j / 10
            if yy >= yk:
                d.line([(x - ctx.px(7), yy), (x + ctx.px(7), yy)], fill=B["white"] + (150,), width=ctx.px(2))
        k2 = ease(clamp((i - ctx.fps * 0.75) / (ctx.fps * 0.3)))
        if k2 > 0:
            tx = x + ctx.px(34) if side == "right" else x - ctx.px(34) - d.textlength(value, font=f)
            ty = (y_top + y_bot) / 2 - ctx.px(40)
            d.text((tx + ctx.px(3), ty + ctx.px(3)), value, font=f, fill=(0, 0, 0, int(140 * k2)))
            d.text((tx, ty), value, font=f, fill=fade_col(B["white"], k2))
        if cap:
            fr.paste(cap, (0, 0), cap)
        yield fr


def shot_ficha(ctx, s, n):
    """Fact sheet (reference: the Siberian tiger info page): name + rows on the left, sharp photo window on the right."""
    over = 1.15
    W2, H2 = int(ctx.W * over), int(ctx.H * over)
    img = R.load_image(ctx, s["bg"], W2, H2, tuple(s.get("focus", (0.5, 0.5))))
    fn = font("serif", ctx.px(92)); fk = font("body", ctx.px(30)); fv = font("serif", ctx.px(54)); fsci = font("serif", ctx.px(40))
    rows = s.get("rows", [])
    for i in range(n):
        t = i / max(1, n - 1)
        fr = bg_frame(ctx, s, i, n)
        z = 1.0 + 0.07 * t
        cw, ch = W2 / z, H2 / z
        box = (W2 / 2 - cw / 2, H2 / 2 - ch / 2, W2 / 2 + cw / 2, H2 / 2 + ch / 2)
        k = ease(clamp(i / (ctx.fps * 0.45)))
        win = img.transform((int(ctx.W * 0.44), int(ctx.H * 0.66)), Image.EXTENT, box, Image.BICUBIC)
        wx = int(ctx.W * 0.51 + (1 - k) * ctx.px(140)); wy = int(ctx.H * 0.17)
        d = ImageDraw.Draw(fr, "RGBA")
        d.rectangle([wx - ctx.px(10), wy - ctx.px(10), wx + win.width + ctx.px(10), wy + win.height + ctx.px(10)], fill=B["ivory"] + (255,))
        fr.paste(win, (wx, wy))
        x, y = ctx.px(100), ctx.px(190)
        for line in wrap(d, s["name"], fn, ctx.W * 0.4):
            d.text((x, y + (1 - k) * ctx.px(30)), line, font=fn, fill=fade_col(B["ivory"], k)); y += ctx.px(100)
        if s.get("sci"):
            d.text((x, y), s["sci"], font=fsci, fill=fade_col(B["grey"], k)); y += ctx.px(56)
        d.rectangle([x, y + ctx.px(8), x + ctx.px(220) * k, y + ctx.px(16)], fill=B["amber"] + (255,))
        y += ctx.px(50)
        for j, (key, val) in enumerate(rows):
            kk = ease(clamp((i - ctx.fps * (0.5 + 0.35 * j)) / (ctx.fps * 0.35)))
            if kk <= 0:
                continue
            d.text((x, y), key.upper(), font=fk, fill=fade_col(B["grey"], kk))
            d.text((x, y + ctx.px(36)), val, font=fv, fill=fade_col(B["gold"], kk))
            y += ctx.px(112)
        source_line(ctx, d, s.get("source")); channel_bug(ctx, d)
        yield fr


def shot_cta(ctx, s, n):
    tmp = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    head = s.get("text", "")
    fh, _ = sized(ctx, tmp, head, "serif", 100, ctx.W * 0.84)
    sub = s.get("sub", "")
    fs = font("body", ctx.px(40)); fb = font("impact", ctx.px(80))
    bw, bh = ctx.px(620), ctx.px(150)

    def button(text, col):
        im = Image.new("RGBA", (bw, bh), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        d.rounded_rectangle([0, 0, bw - 1, bh - 1], radius=ctx.px(20), fill=col + (255,))
        tw = d.textlength(text, font=fb)
        d.text(((bw - tw) / 2, ctx.px(26)), text, font=fb, fill=B["white"])
        return im
    btn, pressed = button("INSCREVA-SE", (214, 32, 32)), button("INSCRITO", (95, 90, 84))
    bell = Image.new("RGBA", (ctx.px(150), ctx.px(150)), (0, 0, 0, 0))
    dl = ImageDraw.Draw(bell); c = ctx.px(75)
    dl.ellipse([0, 0, ctx.px(150) - 1, ctx.px(150) - 1], fill=B["gold"] + (255,))
    dl.pieslice([c - ctx.px(38), c - ctx.px(46), c + ctx.px(38), c + ctx.px(30)], 180, 360, fill=B["char"])
    dl.rectangle([c - ctx.px(38), c - ctx.px(8), c + ctx.px(38), c + ctx.px(26)], fill=B["char"])
    dl.rectangle([c - ctx.px(48), c + ctx.px(22), c + ctx.px(48), c + ctx.px(32)], fill=B["char"])
    dl.ellipse([c - ctx.px(10), c + ctx.px(32), c + ctx.px(10), c + ctx.px(50)], fill=B["char"])
    press_at = int(min(n * 0.45, ctx.fps * 2.5))

    def draw(i):
        L = layer(ctx); d = ImageDraw.Draw(L)
        k = ease(min(1, i / (ctx.fps * 0.35)))
        w = d.textlength(head, font=fh)
        d.text(((ctx.W - w) / 2, ctx.px(230) + (1 - k) * ctx.px(40)), head, font=fh, fill=fade_col(B["white"], k))
        k2 = ease((i - ctx.fps * 0.3) / (ctx.fps * 0.35))
        w = d.textlength(sub, font=fs)
        d.text(((ctx.W - w) / 2, ctx.px(380)), sub, font=fs, fill=fade_col(B["ivory"], k2))
        sc = pop(i, int(ctx.fps * 0.3), ctx.fps)
        if press_at <= i < press_at + ctx.fps * 0.15:
            sc *= 0.95
        paste_scaled(L, pressed if i >= press_at else btn, ctx.W / 2 - ctx.px(110), ctx.px(640), sc)
        paste_scaled(L, bell, ctx.W / 2 + ctx.px(320), ctx.px(640), pop(i, int(ctx.fps * 0.55), ctx.fps))
        channel_bug(ctx, d)
        return L
    return graphic(ctx, s, n, draw)


def shot_questions(ctx, s, n):
    """Open questions of the hook, serif, one after the other, over the scene darkened."""
    qs = s["items"]
    f = font("serif", ctx.px(66))
    starts = s.get("starts") or [int(k * max(ctx.fps * 0.5, n / (len(qs) + 1))) for k in range(len(qs))]

    def draw(i):
        L = layer(ctx); d = ImageDraw.Draw(L)
        y = ctx.H / 2 - len(qs) * ctx.px(70)
        for q, st in zip(qs, starts):
            k = ease(clamp((i - st) / (ctx.fps * 0.35)))
            if k > 0:
                w = d.textlength(q, font=f)
                x = (ctx.W - w) / 2
                d.rectangle([x - ctx.px(30), y + ctx.px(14), x - ctx.px(16), y + ctx.px(74)], fill=B["amber"] + (int(255 * k),))
                d.text((x + (1 - k) * ctx.px(40), y), q, font=f, fill=fade_col(B["white"], k))
            y += ctx.px(140)
        channel_bug(ctx, d)
        return L
    return graphic(ctx, s, n, draw)


# ---------------------------------------------------------------- camera motion: varied, never a slideshow
def _smooth_noise(seed, t, f=0.35):
    """Smooth 1-D noise (sum of slow sines) -> -1..1, for a hand-held camera feel without jitter."""
    r = random.Random(seed)
    ph = [r.random() * 6.283 for _ in range(3)]
    return (math.sin(t * f * 6.283 + ph[0]) * 0.6 + math.sin(t * f * 2.7 * 6.283 + ph[1]) * 0.3
            + math.sin(t * f * 5.1 * 6.283 + ph[2]) * 0.1)


def _persp_coeffs(src_pts, dst_pts):
    import numpy as np
    m = []
    for (x, y), (u, v) in zip(dst_pts, src_pts):
        m.append([x, y, 1, 0, 0, 0, -u * x, -u * y]); m.append([0, 0, 0, x, y, 1, -v * x, -v * y])
    A_ = np.array(m, dtype=float); b = np.array(src_pts, dtype=float).reshape(8)
    return list(np.linalg.solve(A_, b))


MOTIONS = ["drift", "rotate", "focus", "punchin", "orbit", "dolly", "rise", "handheld"]


def shot_image_fx(ctx, s, n):
    """Photo with a camera move chosen per shot ("motion"); falls back to the classic Ken Burns ("move")."""
    mo = s.get("motion")
    if not mo or mo not in MOTIONS:
        yield from _plain_image(ctx, s, n); return
    over = 1.3
    W2, H2 = int(ctx.W * over), int(ctx.H * over)
    img = R.load_image(ctx, s["src"], W2, H2, tuple(s.get("focus", (0.5, 0.5))))
    cap = caption_layer(ctx, s["caption"]) if s.get("caption") else None
    seed = sum(map(ord, s["src"]))
    snow = s.get("snow")
    blur_small = None
    if mo == "focus":
        blur_small = img.resize((W2 // 6, H2 // 6), Image.BILINEAR).filter(ImageFilter.GaussianBlur(3)).resize((W2, H2), Image.BICUBIC)
    sec_n = n / ctx.fps
    for i in range(n):
        u = i / max(1, n - 1)
        t = ease(u) * 0.8 + u * 0.2
        sec = i / ctx.fps
        z, cx, cy, rot = 1.0, 0.0, 0.0, 0.0     # zoom (1 = whole oversize image), centre offset in -1..1 of the margin
        if mo == "drift":       # slow diagonal travel + gentle zoom
            z = 1.06 + 0.10 * t; cx = -0.6 + 1.2 * t; cy = 0.4 - 0.8 * t
        elif mo == "rotate":    # push in with a slight roll
            z = 1.08 + 0.16 * t; rot = (-1.6 + 3.2 * t) * (1 if seed % 2 else -1)
        elif mo == "focus":     # rack focus: out of focus to sharp while pushing in
            z = 1.04 + 0.10 * t
        elif mo == "punchin":   # slow push, then a quick step in at 45% (like a second camera), then slow again
            step = ease(clamp((u - 0.45) / 0.08))
            z = 1.05 + 0.05 * u + 0.18 * step
        elif mo == "orbit":     # fake 3-D: perspective swings as if the camera circled the subject
            z = 1.12 + 0.06 * t
        elif mo == "dolly":     # fast ease-out push at the start, then almost still (lands on the subject)
            k = 1 - (1 - min(1, sec / max(0.6, sec_n * 0.35))) ** 3
            z = 1.0 + 0.22 * k + 0.03 * u
        elif mo == "rise":      # crane up: travels from the bottom to the top of the picture
            z = 1.14; cy = 0.8 - 1.6 * t
        elif mo == "handheld":  # documentary hand-held: smooth wander, no shake
            z = 1.12 + 0.04 * t
            cx = 0.35 * _smooth_noise(seed, sec); cy = 0.35 * _smooth_noise(seed + 9, sec)
        if mo in ("drift", "rotate", "punchin", "dolly", "rise"):   # a breath of hand-held on top of every move
            cx += 0.06 * _smooth_noise(seed + 3, sec, 0.25); cy += 0.06 * _smooth_noise(seed + 5, sec, 0.25)
        cw, ch = W2 / z, H2 / z
        x0 = W2 / 2 + clamp(cx, -1, 1) * (W2 - cw) / 2 - cw / 2
        y0 = H2 / 2 + clamp(cy, -1, 1) * (H2 - ch) / 2 - ch / 2
        src = img
        if mo == "focus":
            b = 1 - ease(clamp(u / 0.45))
            src = Image.blend(img, blur_small, b) if b > 0.01 else img
        if mo == "orbit":
            sw = (0.5 - t) * 0.09 * (1 if seed % 2 else -1)   # perspective swing
            box = [(x0, y0), (x0 + cw, y0), (x0 + cw, y0 + ch), (x0, y0 + ch)]
            d_ = ch * sw
            src_pts = [(box[0][0], box[0][1] - d_), (box[1][0], box[1][1] + d_), (box[2][0], box[2][1] - d_), (box[3][0], box[3][1] + d_)]
            dst = [(0, 0), (ctx.W, 0), (ctx.W, ctx.H), (0, ctx.H)]
            fr = src.transform((ctx.W, ctx.H), Image.PERSPECTIVE, _persp_coeffs(src_pts, dst), Image.BICUBIC)
        elif rot:
            big = src.transform((int(ctx.W * 1.08), int(ctx.H * 1.08)), Image.EXTENT,
                                (x0 - cw * 0.04, y0 - ch * 0.04, x0 + cw * 1.04, y0 + ch * 1.04), Image.BICUBIC)
            big = big.rotate(rot, resample=Image.BICUBIC)
            ox, oy = (big.width - ctx.W) / 2, (big.height - ctx.H) / 2
            fr = big.crop((int(ox), int(oy), int(ox) + ctx.W, int(oy) + ctx.H))
        else:
            fr = src.transform((ctx.W, ctx.H), Image.EXTENT, (x0, y0, x0 + cw, y0 + ch), Image.BICUBIC)
        if snow:
            snow_layer(ctx, ImageDraw.Draw(fr, "RGBA"), sec, seed % 5, alpha=90)
        if s.get("leak") and 0.15 < u < 0.85:   # warm light leak sweeping across
            k = math.sin(math.pi * (u - 0.15) / 0.7)
            lk = Image.new("RGB", (ctx.W, ctx.H), (255, 170, 80))
            m = Image.new("L", (ctx.W // 8, ctx.H // 8), 0)
            lx = (u - 0.15) / 0.7 * (ctx.W // 8)
            ImageDraw.Draw(m).ellipse([lx - ctx.W // 20, -ctx.H // 16, lx + ctx.W // 20, ctx.H // 8 + ctx.H // 16], fill=int(110 * k))
            m = m.filter(ImageFilter.GaussianBlur(ctx.W // 80)).resize((ctx.W, ctx.H), Image.BILINEAR)
            fr = Image.composite(Image.blend(fr, lk, 0.5), fr, m)
        if cap:
            fr.paste(cap, (0, 0), cap)
        yield fr


_plain_image = R.SHOTS["image"]
R.SHOTS["image"] = shot_image_fx

R.SHOTS.update({"serif": shot_serif, "round": shot_round, "versus": shot_versus, "score": shot_score,
                "verdict": shot_verdict, "measure": shot_measure, "ficha": shot_ficha, "cta": shot_cta,
                "questions": shot_questions})
for k in ("image", "video", "measure"):
    R.SHOTS[k] = with_hud(R.SHOTS[k])

# ---------------------------------------------------------------- transitions
A.TRANS_DUR.update({"flash": 0.35, "blur": 0.5, "punch": 0.3, "mono": 0.6, "cut": 0})
_base_transition = A.transition


def pick_trans(prev_s, s, k):
    if prev_s is None:
        return None
    t = s.get("trans")
    return None if t == "cut" else (t or ["fade", "slide", "zoom", "whip"][k % 4])


def transition(ctx, kind, a, b, t):
    e = ease(t)
    W, H = ctx.W, ctx.H
    if kind == "flash":
        white = Image.new("RGB", (W, H), (255, 250, 240))
        return Image.blend(a, white, min(1, e * 2)) if e < 0.5 else Image.blend(white, b, min(1, (e - 0.5) * 2))
    if kind == "blur":
        r = math.sin(math.pi * e)
        mix = Image.blend(a, b, e)
        if r > 0.05:
            small = mix.resize((W // 6, H // 6), Image.BILINEAR).filter(ImageFilter.GaussianBlur(max(1, ctx.px(22) * r / 6)))
            mix = Image.blend(mix, small.resize((W, H), Image.BILINEAR), min(1, r * 1.2))
        return mix
    if kind == "punch":   # fast zoom into the old shot, the new one lands slightly over-scaled and settles
        za = 1 + 0.5 * e
        aa = a.transform((W, H), Image.EXTENT, (W / 2 - W / za / 2, H / 2 - H / za / 2, W / 2 + W / za / 2, H / 2 + H / za / 2), Image.BICUBIC)
        zb = 1.12 - 0.12 * e
        bb = b.transform((W, H), Image.EXTENT, (W / 2 - W / zb / 2, H / 2 - H / zb / 2, W / 2 + W / zb / 2, H / 2 + H / zb / 2), Image.BICUBIC)
        return aa if e < 0.45 else bb
    if kind == "mono":    # old shot drains to black and white, new shot fades in from grey to colour
        if e < 0.5:
            g = ImageOps.grayscale(a).convert("RGB")
            return Image.blend(a, g, e * 2)
        g = ImageOps.grayscale(b).convert("RGB")
        mid = Image.blend(ImageOps.grayscale(a).convert("RGB"), g, min(1, (e - 0.5) * 4))
        return Image.blend(mid, b, (e - 0.5) * 2)
    if kind in ("whip", "slide", "rise"):   # edge-safe: everything moves inside an over-scaled frame, no empty border
        def shift(im, dx, z=1.18):
            cw, ch = W / z, H / z
            x0 = (W - cw) / 2 - dx / z
            x0 = min(max(x0, 0), W - cw)
            return im.transform((W, H), Image.EXTENT, (x0, (H - ch) / 2, x0 + cw, (H + ch) / 2), Image.BICUBIC)
        if kind == "whip":
            src, off, k = (a, -e / 0.5, e / 0.5) if e < 0.5 else (b, (1 - e) / 0.5, (1 - e) / 0.5)
            im = shift(src, off * W * 0.15)
            if k > 0.05:
                small = im.resize((W // 4, H // 4), Image.BILINEAR).filter(ImageFilter.BoxBlur(max(1, int(ctx.px(90) * k) // 8)))
                im = Image.blend(im, small.resize((W, H), Image.BILINEAR), min(1, k * 1.3))
            return im
        out = shift(a, e * W * 0.15)
        bb = b
        m = Image.new("L", (W, H), 0)
        ImageDraw.Draw(m).rectangle([(1 - e) * W, 0, W, H], fill=255)
        out = out.copy(); out.paste(bb, (0, 0), m)
        if 0 < e < 1:
            ImageDraw.Draw(out).rectangle([(1 - e) * W - ctx.px(10), 0, (1 - e) * W, H], fill=B["ivory"])
        return out
    return _base_transition(ctx, kind, a, b, t)


A.pick_trans, A.transition = pick_trans, transition


def grade_vf(ep):
    g = ep.get("grade", {})
    return (f"eq=contrast={g.get('contrast', 1.05)}:saturation={g.get('saturation', 1.06)}:gamma={g.get('gamma', 1.0)},"
            f"colorbalance=rs=0.02:bs=-0.02:rh=0.015,"
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
