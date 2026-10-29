#!/usr/bin/env python3
"""Black Dossier render engine.

Builds a finished documentary video from an episode file (JSON):
narration per chapter, a shot list per chapter, music and sound effects.

Shot durations inside a chapter are weights: they are stretched or squeezed
so the chapter's pictures end exactly when its narration ends.

Usage:
    python3 render.py episode.json            # full render
    python3 render.py episode.json --preview  # 960x540, fast, for checks
"""
import json, math, os, random, subprocess, sys, shutil, tempfile
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- brand
BRAND = {
    "red": (196, 72, 62),
    "red_dark": (120, 30, 26),
    "paper": (232, 222, 204),
    "ink": (22, 18, 18),
    "white": (240, 234, 228),
    "black": (8, 7, 7),
}
FONT_CANDIDATES = {
    "type":  ["fonts/SpecialElite-Regular.ttf", "/usr/share/fonts/X11/Type1/c0419bt_.pfb",
              "/usr/share/texmf/fonts/opentype/public/lm/lmmono10-regular.otf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"],
    "impact": ["fonts/BebasNeue-Regular.ttf", "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf",
               "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"],
    "serif": ["fonts/serif.ttf", "/usr/share/texmf/fonts/opentype/public/lm/lmromandemi10-regular.otf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"],
    "mono":  ["fonts/IBMPlexMono-Regular.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"],
}
_font_cache = {}


def font(kind, size):
    key = (kind, size)
    if key in _font_cache:
        return _font_cache[key]
    for cand in FONT_CANDIDATES[kind]:
        p = cand if os.path.isabs(cand) else os.path.join(HERE, cand)
        if os.path.exists(p):
            try:
                f = ImageFont.truetype(p, size)
                _font_cache[key] = f
                return f
            except OSError:
                continue
    f = ImageFont.load_default(size)
    _font_cache[key] = f
    return f


def ease(t):  # smooth in-out
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


# ---------------------------------------------------------------- helpers
class Ctx:
    def __init__(self, W, H, fps, base):
        self.W, self.H, self.fps, self.base = W, H, fps, base
        self.s = W / 1920.0  # scale factor for all pixel sizes

    def px(self, v):
        return max(1, int(round(v * self.s)))

    def path(self, p):
        return p if os.path.isabs(p) else os.path.join(self.base, p)


def blank(ctx, color=BRAND["black"]):
    return Image.new("RGB", (ctx.W, ctx.H), color)


def paper_texture(ctx, seed=1):
    """Aged paper background for dossier / document shots."""
    rnd = random.Random(seed)
    w, h = ctx.W // 8, ctx.H // 8
    noise = Image.effect_noise((w, h), 28).resize((ctx.W, ctx.H), Image.BICUBIC)
    base = Image.new("RGB", (ctx.W, ctx.H), BRAND["paper"])
    tint = Image.merge("RGB", [noise.point(lambda v: int(v * 0.55 + 80)),
                               noise.point(lambda v: int(v * 0.5 + 70)),
                               noise.point(lambda v: int(v * 0.4 + 55))])
    img = Image.blend(base, tint, 0.18)
    d = ImageDraw.Draw(img)
    stains = Image.new("L", (ctx.W, ctx.H), 0)
    sd = ImageDraw.Draw(stains)
    for _ in range(5):  # soft, uneven age marks
        x, y, r = rnd.randint(0, ctx.W), rnd.randint(0, ctx.H), rnd.randint(ctx.px(120), ctx.px(380))
        sd.ellipse([x - r, y - r * 0.7, x + r, y + r * 0.7], fill=rnd.randint(18, 34))
    stains = stains.filter(ImageFilter.GaussianBlur(ctx.px(60)))
    img = Image.composite(Image.new("RGB", img.size, (150, 120, 85)), img, stains)
    return img.filter(ImageFilter.GaussianBlur(ctx.px(1)))


def load_image(ctx, src, cover_w, cover_h, focus=(0.5, 0.5)):
    """Cover-crop to the frame. focus = (x, y) 0..1: which part of the photo to keep
    when it has to be cut (e.g. (0.5, 0.2) keeps the top of a portrait-format photo)."""
    img = Image.open(ctx.path(src)).convert("RGB")
    return ImageOps.fit(img, (cover_w, cover_h), Image.LANCZOS, centering=tuple(focus))


def wrap(draw, text, fnt, max_w):
    lines = []
    for para in text.split("\n"):
        cur = ""
        for word in para.split(" "):
            test = (cur + " " + word).strip()
            if draw.textlength(test, font=fnt) <= max_w or not cur:
                cur = test
            else:
                lines.append(cur)
                cur = word
        lines.append(cur)
    return lines


def stamp(ctx, text, angle=-12, color=BRAND["red"], size=90):
    f = font("impact", ctx.px(size))
    tmp = Image.new("RGBA", (1, 1))
    tw = int(ImageDraw.Draw(tmp).textlength(text, font=f))
    pad = ctx.px(24)
    im = Image.new("RGBA", (tw + pad * 2, ctx.px(size) + pad * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle([2, 2, im.width - 3, im.height - 3], outline=color + (230,), width=ctx.px(7))
    d.text((pad, pad - ctx.px(size * 0.08)), text, font=f, fill=color + (230,))
    # worn ink: knock out random specks
    speck = Image.effect_noise(im.size, 90).point(lambda v: 0 if v > 175 else 255)
    a = im.split()[3]
    im.putalpha(Image.composite(a, Image.new("L", im.size, 0), speck))
    return im.rotate(angle, resample=Image.BICUBIC, expand=True)


# ---------------------------------------------------------------- shots
# Each shot is a function (ctx, shot, n_frames) -> generator of PIL frames.

def shot_black(ctx, s, n):
    f = blank(ctx)
    for _ in range(n):
        yield f


def shot_image(ctx, s, n):
    """Ken Burns move on a still. move: in | out | left | right | up | down | static"""
    over = 1.18
    W2, H2 = int(ctx.W * over), int(ctx.H * over)
    img = load_image(ctx, s["src"], W2, H2, s.get("focus", (0.5, 0.5)))
    move = s.get("move", "in")
    z0, z1 = {"in": (1.0, over * 0.9), "out": (over * 0.9, 1.0)}.get(move, (1.06, 1.06))
    dx0 = dy0 = dx1 = dy1 = 0.0
    slack = 0.5
    if move == "left": dx0, dx1 = slack, -slack
    if move == "right": dx0, dx1 = -slack, slack
    if move == "up": dy0, dy1 = slack, -slack
    if move == "down": dy0, dy1 = -slack, slack
    cap = caption_layer(ctx, s.get("caption")) if s.get("caption") else None
    for i in range(n):
        t = ease(i / max(1, n - 1))
        z = z0 + (z1 - z0) * t
        cw, ch = W2 / z, H2 / z  # crop size in source pixels... keeps aspect
        cw, ch = ctx.W * over / z, ctx.H * over / z
        fx = (dx0 + (dx1 - dx0) * t)
        fy = (dy0 + (dy1 - dy0) * t)
        cx = W2 / 2 + fx * (W2 - cw) / 2
        cy = H2 / 2 + fy * (H2 - ch) / 2
        box = (cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2)
        frame = img.transform((ctx.W, ctx.H), Image.EXTENT, box, Image.BICUBIC)
        if cap:
            frame.paste(cap, (0, 0), cap)
        yield frame


def caption_layer(ctx, text):
    """Lower-left archival caption: red rule + mono text."""
    im = Image.new("RGBA", (ctx.W, ctx.H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    f = font("mono", ctx.px(30))
    x, y = ctx.px(90), ctx.px(80)  # top-left: the bottom of the frame belongs to the subtitles
    tw = d.textlength(text.upper(), font=f)
    d.rectangle([x - ctx.px(18), y - ctx.px(14), x + tw + ctx.px(18), y + ctx.px(48)], fill=(0, 0, 0, 150))
    d.rectangle([x - ctx.px(18), y - ctx.px(14), x - ctx.px(12), y + ctx.px(48)], fill=BRAND["red"] + (255,))
    d.text((x, y), text.upper(), font=f, fill=BRAND["white"])
    return im


def shot_typewriter(ctx, s, n):
    """Text typed letter by letter, with blinking cursor. Over a darkened scene ("bg") so the screen is never black."""
    text = s["text"]
    f = font("type", ctx.px(s.get("size", 64)))
    base = blank(ctx)
    if s.get("bg"):
        from PIL import ImageEnhance, ImageFilter
        bgi = load_image(ctx, ctx.path(s["bg"]), ctx.W, ctx.H, tuple(s.get("bg_focus", (0.5, 0.5)))).convert("RGB")
        base = ImageEnhance.Brightness(bgi.filter(ImageFilter.GaussianBlur(ctx.px(3)))).enhance(0.40)
    d0 = ImageDraw.Draw(base)
    lines = wrap(d0, text, f, ctx.W * 0.8)
    full = "\n".join(lines)
    lh = int(ctx.px(s.get("size", 64)) * 1.35)
    y0 = (ctx.H - lh * len(lines)) // 2
    type_frames = max(1, int(n * 0.6))
    for i in range(n):
        k = int(len(full) * min(1, i / type_frames))
        shown = full[:k]
        im = base.copy()
        d = ImageDraw.Draw(im)
        for li, line in enumerate(shown.split("\n")):
            target = lines[li]
            lx = (ctx.W - d.textlength(target, font=f)) / 2
            d.text((lx, y0 + li * lh), line, font=f, fill=BRAND["white"])
        if (i // int(ctx.fps * 0.5)) % 2 == 0:
            last = shown.split("\n")
            li = len(last) - 1
            lx = (ctx.W - d.textlength(lines[li], font=f)) / 2 + d.textlength(last[-1], font=f)
            d.rectangle([lx + ctx.px(6), y0 + li * lh + ctx.px(6), lx + ctx.px(30), y0 + li * lh + lh - ctx.px(14)], fill=BRAND["red"])
        yield im


def shot_statement(ctx, s, n):
    """Big hard-cut statement: white impact type on black, red underline."""
    f = font("impact", ctx.px(s.get("size", 150)))
    im = blank(ctx)
    d = ImageDraw.Draw(im)
    lines = wrap(d, s["text"].upper(), f, ctx.W * 0.86)
    lh = int(ctx.px(s.get("size", 150)) * 1.05)
    y = (ctx.H - lh * len(lines)) // 2
    for li, line in enumerate(lines):
        w = d.textlength(line, font=f)
        d.text(((ctx.W - w) / 2, y + li * lh), line, font=f, fill=BRAND["white"])
    w = d.textlength(lines[-1], font=f)
    uy = y + lh * len(lines) + ctx.px(18)
    for i in range(n):
        fr = im.copy()
        t = ease(i / max(1, int(ctx.fps * 0.6)))
        dd = ImageDraw.Draw(fr)
        dd.rectangle([(ctx.W - w) / 2, uy, (ctx.W - w) / 2 + w * t, uy + ctx.px(10)], fill=BRAND["red"])
        yield fr


def shot_title(ctx, s, n):
    """Episode title card on paper, with stamp."""
    bg = paper_texture(ctx, seed=7)
    d = ImageDraw.Draw(bg)
    fs = font("type", ctx.px(46))
    title = s["title"].upper()
    size = 170
    ft = font("impact", ctx.px(size))
    while d.textlength(title, font=ft) > ctx.W * 0.86 and size > 60:  # never let the title run off the frame
        size -= 6
        ft = font("impact", ctx.px(size))
    tw = d.textlength(title, font=ft)
    d.text(((ctx.W - tw) / 2, ctx.H * 0.33), title, font=ft, fill=BRAND["ink"])
    sub = s.get("subtitle", "")
    sw = d.textlength(sub, font=fs)
    d.text(((ctx.W - sw) / 2, ctx.H * 0.58), sub, font=fs, fill=BRAND["red_dark"])
    d.text((ctx.px(80), ctx.px(60)), "BLACK DOSSIER", font=font("type", ctx.px(34)), fill=BRAND["ink"])
    d.text((ctx.W - ctx.px(420), ctx.px(60)), s.get("file", "FILE No. 001"), font=font("type", ctx.px(34)), fill=BRAND["ink"])
    st = stamp(ctx, s.get("stamp", "CLASSIFIED"), size=80)
    land = int(ctx.fps * 0.9)
    for i in range(n):
        fr = bg.copy()
        if i >= land:
            k = min(1.0, (i - land) / (ctx.fps * 0.15))
            sc = 1.6 - 0.6 * ease(k)
            sti = st.resize((int(st.width * sc), int(st.height * sc)), Image.BICUBIC)
            fr.paste(sti, (int(ctx.W * 0.72 - sti.width / 2), int(ctx.H * 0.74 - sti.height / 2)), sti)
        yield vignette_soft(ctx, fr)


def shot_chapter(ctx, s, n):
    """Chapter card: FILE 0X + title, slides in from left over black."""
    f1 = font("type", ctx.px(40))
    f2 = font("impact", ctx.px(120))
    for i in range(n):
        im = blank(ctx)
        d = ImageDraw.Draw(im)
        t = ease(i / (ctx.fps * 0.8))
        off = int((1 - t) * -ctx.px(120))
        a = int(255 * t)
        x = ctx.px(140) + off
        d.text((x, ctx.H * 0.36), "FILE %02d" % int(s["num"]), font=f1, fill=BRAND["red"])
        d.rectangle([x, ctx.H * 0.36 + ctx.px(62), x + ctx.px(140) * t, ctx.H * 0.36 + ctx.px(68)], fill=BRAND["red"])
        lines = wrap(d, s["title"].upper(), f2, ctx.W * 0.78)
        for li, line in enumerate(lines):
            col = tuple(int(c * a / 255) for c in BRAND["white"])
            d.text((x, ctx.H * 0.36 + ctx.px(90) + li * ctx.px(118)), line, font=f2, fill=col)
        yield im


def silhouette(pw, ph):
    """Unknown-subject placeholder: man in a fedora, drawn large then downsampled for smooth edges."""
    k = 3
    W, H = pw * k, ph * k
    im = Image.new("RGB", (W, H), (58, 54, 51))
    g = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(g)
    cx = W / 2
    d.ellipse([cx - W * .44, H * .60, cx + W * .44, H * 1.30], fill=255)        # shoulders
    d.rectangle([cx - W * .08, H * .52, cx + W * .08, H * .64], fill=255)       # neck
    d.ellipse([cx - W * .15, H * .26, cx + W * .15, H * .57], fill=255)         # head
    d.ellipse([cx - W * .30, H * .265, cx + W * .30, H * .325], fill=255)       # hat brim
    d.rounded_rectangle([cx - W * .16, H * .13, cx + W * .16, H * .30], radius=W * .06, fill=255)  # crown
    d.rectangle([cx - W * .16, H * .262, cx + W * .16, H * .272], fill=150)     # hat band
    g = g.filter(ImageFilter.GaussianBlur(k))
    im.paste((24, 21, 21), (0, 0, W, H), g)
    t = Image.new("L", (W, H), 0)                                                 # faint "?" watermark
    ImageDraw.Draw(t).text((cx, H * .40), "?", fill=40, anchor="mm", font=font("impact", int(H * .18)))
    im.paste((70, 64, 60), (0, 0, W, H), t)
    return im.resize((pw, ph), Image.LANCZOS)


def shot_dossier(ctx, s, n):
    """Character file: photo clipped to a folder, name, role, optional stamp."""
    bg = paper_texture(ctx, seed=hash(s["name"]) % 1000)
    d = ImageDraw.Draw(bg)
    pw, ph = ctx.px(520), ctx.px(660)
    px_, py_ = ctx.px(180), (ctx.H - ph) // 2
    if s.get("photo"):
        photo = load_image(ctx, s["photo"], pw, ph, s.get("focus", (0.5, 0.3)))
        photo = ImageOps.grayscale(photo).convert("RGB")
    else:
        photo = silhouette(pw, ph)
    shadow = Image.new("RGBA", (pw + ctx.px(40), ph + ctx.px(40)), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rectangle([ctx.px(20), ctx.px(26), pw + ctx.px(20), ph + ctx.px(26)], fill=(0, 0, 0, 120))
    shadow = shadow.filter(ImageFilter.GaussianBlur(ctx.px(12)))
    bg.paste(shadow, (px_ - ctx.px(20), py_ - ctx.px(20)), shadow)
    bg.paste(ImageOps.expand(photo, border=ctx.px(14), fill=(245, 242, 236)), (px_ - ctx.px(14), py_ - ctx.px(14)))
    d.rectangle([px_ + pw * 0.4, py_ - ctx.px(40), px_ + pw * 0.6, py_ + ctx.px(10)], fill=(150, 150, 155))  # clip
    tx = px_ + pw + ctx.px(110)
    d.text((tx, py_ + ctx.px(10)), s.get("label", "SUBJECT"), font=font("type", ctx.px(34)), fill=BRAND["red_dark"])
    fn = font("impact", ctx.px(118))
    for li, line in enumerate(wrap(d, s["name"].upper(), fn, ctx.W - tx - ctx.px(100))):
        d.text((tx, py_ + ctx.px(60) + li * ctx.px(116)), line, font=fn, fill=BRAND["ink"])
    fy = py_ + ctx.px(320)
    for li, (k, v) in enumerate(s.get("fields", {}).items()):
        d.text((tx, fy + li * ctx.px(58)), f"{k.upper()}:", font=font("type", ctx.px(32)), fill=BRAND["red_dark"])
        d.text((tx + ctx.px(260), fy + li * ctx.px(58)), str(v), font=font("type", ctx.px(32)), fill=BRAND["ink"])
    st = stamp(ctx, s["stamp"], size=70) if s.get("stamp") else None
    land = int(ctx.fps * 1.2)
    for i in range(n):
        t = i / max(1, n - 1)
        z = 1.0 + 0.05 * ease(t)
        fr = bg.resize((int(ctx.W * z), int(ctx.H * z)), Image.BICUBIC).crop(
            (int((ctx.W * z - ctx.W) / 2), int((ctx.H * z - ctx.H) / 2), int((ctx.W * z + ctx.W) / 2), int((ctx.H * z + ctx.H) / 2)))
        if st and i >= land:
            k = min(1.0, (i - land) / (ctx.fps * 0.15))
            sc = 1.6 - 0.6 * ease(k)
            sti = st.resize((int(st.width * sc), int(st.height * sc)), Image.BICUBIC)
            fr.paste(sti, (int(px_ + pw * 0.55 - sti.width / 2), int(py_ + ph * 0.82 - sti.height / 2)), sti)
        yield vignette_soft(ctx, fr)


def shot_counter(ctx, s, n):
    """Number counting up, label underneath."""
    f = font("impact", ctx.px(300))
    fl = font("type", ctx.px(48))
    a, b = s.get("from", 0), s["to"]
    pre, suf = s.get("prefix", ""), s.get("suffix", "")
    for i in range(n):
        t = ease(min(1, i / (n * 0.55)))
        v = int(round(a + (b - a) * t))
        im = blank(ctx)
        d = ImageDraw.Draw(im)
        txt = f"{pre}{v:,}{suf}"
        w = d.textlength(txt, font=f)
        d.text(((ctx.W - w) / 2, ctx.H * 0.22), txt, font=f, fill=BRAND["white"] if t < 1 else BRAND["red"])
        lab = s.get("label", "").upper()
        w2 = d.textlength(lab, font=fl)
        d.text(((ctx.W - w2) / 2, ctx.H * 0.66), lab, font=fl, fill=BRAND["white"])
        yield im


def shot_document(ctx, s, n):
    """Typed memo on paper with a slow push-in. Always labelled DRAMATIZATION."""
    bg = paper_texture(ctx, seed=3)
    d = ImageDraw.Draw(bg)
    ft = font("type", ctx.px(40))
    x, y = ctx.px(260), ctx.px(150)
    for li, line in enumerate(wrap(d, s["text"], ft, ctx.W - ctx.px(520))):
        d.text((x, y + li * ctx.px(58)), line, font=ft, fill=BRAND["ink"])
    d.text((ctx.W - ctx.px(380), ctx.H - ctx.px(80)), "DRAMATIZATION", font=font("mono", ctx.px(26)), fill=(120, 100, 90))
    st = stamp(ctx, s["stamp"], size=64) if s.get("stamp") else None
    if st:
        bg.paste(st, (ctx.W - st.width - ctx.px(240), ctx.px(120)), st)
    sh = dict(s, src=None)
    for i in range(n):
        t = ease(i / max(1, n - 1))
        z = 1.0 + 0.08 * t
        fr = bg.resize((int(ctx.W * z), int(ctx.H * z)), Image.BICUBIC).crop(
            (int((ctx.W * z - ctx.W) / 2), int(ctx.H * (z - 1) * 0.2), int((ctx.W * z + ctx.W) / 2), int(ctx.H * (z - 1) * 0.2) + ctx.H))
        yield vignette_soft(ctx, fr)


def shot_timeline(ctx, s, n):
    """Horizontal timeline; points appear in order. items: [[label, text, strike?], ...]"""
    items = s["items"]
    fl = font("impact", ctx.px(64))
    ft = font("type", ctx.px(34))
    y = ctx.H // 2
    x0, x1 = ctx.px(330), ctx.W - ctx.px(330)
    for i in range(n):
        im = blank(ctx)
        d = ImageDraw.Draw(im)
        prog = ease(min(1, i / (n * 0.7)))
        d.rectangle([x0, y - ctx.px(3), x0 + (x1 - x0) * prog, y + ctx.px(3)], fill=(110, 100, 98))
        for k, it in enumerate(items):
            px_ = x0 + (x1 - x0) * (k / max(1, len(items) - 1))
            appear = (k / max(1, len(items))) * 0.7
            if prog < appear + 0.01 and k > 0:
                continue
            d.ellipse([px_ - ctx.px(16), y - ctx.px(16), px_ + ctx.px(16), y + ctx.px(16)], fill=BRAND["red"])
            w = d.textlength(it[0], font=fl)
            d.text((px_ - w / 2, y - ctx.px(130)), it[0], font=fl, fill=BRAND["white"])
            lines = wrap(d, it[1], ft, ctx.px(380))
            for li, line in enumerate(lines):
                w2 = d.textlength(line, font=ft)
                d.text((px_ - w2 / 2, y + ctx.px(40) + li * ctx.px(44)), line, font=ft, fill=(200, 190, 186))
            if len(it) > 2 and it[2] and i > n * 0.8:
                d.line([px_ - ctx.px(170), y - ctx.px(95), px_ + ctx.px(170), y - ctx.px(95)], fill=BRAND["red"], width=ctx.px(8))
        yield im


def shot_video(ctx, s, n):
    """Archival / stock clip.
    fit: "blur" (default) keeps the whole picture and fills the sides with a blurred copy (4:3 film);
         "crop" fills the frame by cropping. Short clips loop instead of freezing; "speed" < 1 slows it."""
    W, H, fps = ctx.W, ctx.H, ctx.fps
    speed = s.get("speed", 1.0)
    slow = f"setpts={1 / speed:.4f}*PTS," if speed != 1.0 else ""
    if s.get("fit", "blur") == "crop":
        vf = f"{slow}scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={fps}"
    else:
        vf = (f"{slow}fps={fps},split[a][b];"
              f"[a]scale={W // 4}:{H // 4}:force_original_aspect_ratio=increase,crop={W // 4}:{H // 4},"
              f"boxblur=8:2,scale={W}:{H},eq=brightness=-0.12[bg];"
              f"[b]scale={W}:{H}:force_original_aspect_ratio=decrease[fg];"
              f"[bg][fg]overlay=(W-w)/2:(H-h)/2")
    cmd = ["ffmpeg", "-v", "error", "-stream_loop", "-1", "-ss", str(s.get("start", 0)), "-i", ctx.path(s["src"]),
           "-filter_complex" if ";" in vf else "-vf", vf,
           "-frames:v", str(n), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    size = W * H * 3
    last = blank(ctx)
    cap = caption_layer(ctx, s["caption"]) if s.get("caption") else None
    for _ in range(n):
        buf = p.stdout.read(size)
        if len(buf) == size:
            last = Image.frombytes("RGB", (W, H), buf)
            if cap:
                last.paste(cap, (0, 0), cap)
        yield last
    p.stdout.close(); p.wait()


SHOTS = {"black": shot_black, "image": shot_image, "typewriter": shot_typewriter, "statement": shot_statement,
         "title": shot_title, "chapter": shot_chapter, "dossier": shot_dossier, "counter": shot_counter,
         "document": shot_document, "timeline": shot_timeline, "video": shot_video}

_vig = {}


def vignette_soft(ctx, im):
    if im.size != (ctx.W, ctx.H):  # zoom crops can round 1 px off
        im = im.resize((ctx.W, ctx.H), Image.BICUBIC)
    key = (ctx.W, ctx.H)
    if key not in _vig:
        m = Image.new("L", (ctx.W // 4, ctx.H // 4), 0)
        ImageDraw.Draw(m).ellipse([-ctx.W // 16, -ctx.H // 16, ctx.W // 4 + ctx.W // 16, ctx.H // 4 + ctx.H // 16], fill=255)
        _vig[key] = m.filter(ImageFilter.GaussianBlur(ctx.W // 40)).resize((ctx.W, ctx.H), Image.BICUBIC)
    return Image.composite(im, Image.new("RGB", im.size, (30, 22, 20)), _vig[key])


# ---------------------------------------------------------------- audio
def probe_dur(path):
    out = subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path])
    return float(out.strip())


def build_timeline(ep, ctx):
    """Returns list of (shot, n_frames, start_sec) and chapter audio list with offsets."""
    timeline, audio = [], []
    t = 0.0
    for ch in ep["chapters"]:
        lead = ch.get("lead_in", 0.0)  # seconds of picture before the voice starts
        tail = ch.get("tail", 0.6)     # breath after the chapter's last line
        if ch.get("audio"):
            a_dur = probe_dur(ctx.path(ch["audio"]))
            audio.append((ctx.path(ch["audio"]), t + lead))
            total = lead + a_dur + tail
        else:
            total = sum(s.get("dur", 3) for s in ch["shots"])
        weights = sum(s.get("dur", 3) for s in ch["shots"]) or 1
        fixed = sum(s["dur"] for s in ch["shots"] if s.get("fixed"))
        flex_w = sum(s.get("dur", 3) for s in ch["shots"] if not s.get("fixed")) or 1
        frames_left = int(round(total * ctx.fps))
        for k, s in enumerate(ch["shots"]):
            if s.get("fixed"):
                nf = int(round(s["dur"] * ctx.fps))
            else:
                nf = int(round((total - fixed) * s.get("dur", 3) / flex_w * ctx.fps))
            if k == len(ch["shots"]) - 1:
                nf = frames_left
            nf = max(1, nf)
            frames_left -= nf
            timeline.append((s, nf, t))
            t += nf / ctx.fps
    return timeline, audio, t


def mix_audio(ep, ctx, audio, timeline, total, out_wav, tmp):
    inputs, filters, labels = [], [], []
    # narration
    for idx, (p, off) in enumerate(audio):
        inputs += ["-i", p]
        ms = int(off * 1000)
        filters.append(f"[{idx}:a]aresample=48000,aformat=channel_layouts=stereo,adelay={ms}|{ms}[n{idx}]")
        labels.append(f"[n{idx}]")
    n = len(audio)
    if labels:
        filters.append("".join(labels) + f"amix=inputs={len(labels)}:normalize=0,apad=whole_dur={total:.3f}[voice]")
    else:
        filters.append(f"anullsrc=r=48000:cl=stereo,atrim=0:{total:.3f}[voice]")
    # sfx placed on shots
    sfx_lbl = []
    for (s, nf, start) in timeline:
        for fx in s.get("sfx", []) if isinstance(s.get("sfx"), list) else ([s["sfx"]] if s.get("sfx") else []):
            fx = fx if isinstance(fx, dict) else {"file": fx}
            inputs += ["-i", ctx.path(fx["file"])]
            ms = int((start + fx.get("at", 0)) * 1000)
            filters.append(f"[{n}:a]aresample=48000,aformat=channel_layouts=stereo,volume={fx.get('gain', -6)}dB,adelay={ms}|{ms}[s{n}]")
            sfx_lbl.append(f"[s{n}]")
            n += 1
    # music beds with ducking under the voice
    mus_lbl = []
    for m in ep.get("music", []):
        inputs += ["-stream_loop", "-1", "-i", ctx.path(m["file"])]
        st, en = m.get("start", 0), m.get("end", total)
        ms = int(st * 1000)
        filters.append(f"[{n}:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{en - st:.3f},"
                       f"afade=t=in:d={m.get('fade_in', 2)},afade=t=out:st={max(0, en - st - m.get('fade_out', 3)):.3f}:d={m.get('fade_out', 3)},"
                       f"volume={m.get('gain', -16)}dB,adelay={ms}|{ms}[m{n}]")
        mus_lbl.append(f"[m{n}]")
        n += 1
    if mus_lbl:
        filters.append("[voice]asplit=2[voice1][vkey]")
        filters.append("".join(mus_lbl) + f"amix=inputs={len(mus_lbl)}:normalize=0[mus]")
        filters.append("[mus][vkey]sidechaincompress=threshold=0.03:ratio=6:attack=40:release=500[duck]")
        bed = ["[voice1]", "[duck]"]
    else:
        bed = ["[voice]"]
    filters.append("".join(bed + sfx_lbl) + f"amix=inputs={len(bed) + len(sfx_lbl)}:normalize=0,atrim=0:{total:.3f},"
                   "loudnorm=I=-14:TP=-1.5:LRA=11[out]")
    script = os.path.join(tmp, "audio_graph.txt")
    open(script, "w").write(";\n".join(filters))
    cmd = ["ffmpeg", "-y", "-v", "error"] + inputs + ["-filter_complex_script", script, "-map", "[out]", "-ar", "48000", out_wav]
    subprocess.check_call(cmd)


# ---------------------------------------------------------------- main
def render(ep_path, preview=False):
    ep = json.load(open(ep_path))
    base = os.path.dirname(os.path.abspath(ep_path))
    W, H = (960, 540) if preview else tuple(ep.get("size", [1920, 1080]))
    fps = ep.get("fps", 24)
    ctx = Ctx(W, H, fps, base)
    timeline, audio, total = build_timeline(ep, ctx)
    out = ctx.path(ep.get("output", "out.mp4"))
    if preview:
        out = out.replace(".mp4", "-preview.mp4")
    tmp = tempfile.mkdtemp(prefix="bd_")
    print(f"[render] {len(timeline)} shots, {total/60:.2f} min, {W}x{H}@{fps}", flush=True)

    wav = os.path.join(tmp, "mix.wav")
    mix_audio(ep, ctx, audio, timeline, total, wav, tmp)

    grade = ep.get("grade", {})
    vf = (f"eq=contrast={grade.get('contrast', 1.08)}:saturation={grade.get('saturation', 0.72)}:gamma={grade.get('gamma', 0.97)},"
          f"colorbalance=rs=0.04:bs=-0.03:rh=0.02:bh=-0.02,"
          f"noise=alls={grade.get('grain', 9)}:allf=t,vignette=angle=PI/4.5")
    if ep.get("subtitles"):
        sub = ctx.path(ep["subtitles"]).replace("\\", "/").replace(":", "\\:").replace("'", "\\'")
        vf += f",subtitles='{sub}'" + (":original_size=1920x1080" if preview else "")
    vf += ",format=yuv420p"
    vcmd = ["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(fps), "-i", "-",
            "-i", wav, "-vf", vf, "-c:v", "libx264", "-preset", "veryfast" if preview else "medium",
            "-crf", "26" if preview else "18", "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", "-shortest", out]
    p = subprocess.Popen(vcmd, stdin=subprocess.PIPE)
    prev_last = None
    done = 0
    total_frames = sum(nf for _, nf, _ in timeline)
    for (s, nf, start) in timeline:
        xf = int(s.get("xfade", 0.5 if s["type"] == "image" else 0) * fps)
        gen = SHOTS[s["type"]](ctx, s, nf)
        for i, fr in enumerate(gen):
            if fr.size != (W, H):
                fr = fr.resize((W, H), Image.BICUBIC)
            if prev_last is not None and i < xf:
                fr = Image.blend(prev_last, fr, ease((i + 1) / (xf + 1)))
            if i < s.get("fade_in", 0) * fps:
                fr = Image.blend(blank(ctx), fr, (i + 1) / (s["fade_in"] * fps + 1))
            if nf - i <= s.get("fade_out", 0) * fps:
                fr = Image.blend(blank(ctx), fr, (nf - i) / (s["fade_out"] * fps + 1))
            p.stdin.write(fr.tobytes())
            last = fr
        prev_last = last
        done += nf
        print(f"[render] {done}/{total_frames} frames", flush=True)
    p.stdin.close()
    p.wait()
    shutil.rmtree(tmp, ignore_errors=True)
    print(f"[render] done -> {out}")
    return out


def render_resumable(ep_path, seg_shots=20, final_preset="veryfast", final_crf="21"):
    """Render in segments cached on disk, so an interrupted render resumes where it stopped.
    Subtitles and the audio mix are applied in one final pass over the joined segments."""
    ep = json.load(open(ep_path))
    base = os.path.dirname(os.path.abspath(ep_path))
    W, H = tuple(ep.get("size", [1920, 1080]))
    fps = ep.get("fps", 24)
    ctx = Ctx(W, H, fps, base)
    timeline, audio, total = build_timeline(ep, ctx)
    out = ctx.path(ep.get("output", "out.mp4"))
    cache = os.path.join(base, ".render_cache")
    os.makedirs(cache, exist_ok=True)
    print(f"[render] {len(timeline)} shots, {total/60:.2f} min, {W}x{H}@{fps} (por partes)", flush=True)
    wav = os.path.join(cache, "mix.wav")
    if not os.path.exists(wav):
        tmp = tempfile.mkdtemp(prefix="bd_")
        mix_audio(ep, ctx, audio, timeline, total, wav + ".part.wav", tmp)
        os.replace(wav + ".part.wav", wav)
        shutil.rmtree(tmp, ignore_errors=True)
    grade = ep.get("grade", {})
    vf = (f"eq=contrast={grade.get('contrast', 1.08)}:saturation={grade.get('saturation', 0.72)}:gamma={grade.get('gamma', 0.97)},"
          f"colorbalance=rs=0.04:bs=-0.03:rh=0.02:bh=-0.02,"
          f"noise=alls={grade.get('grain', 9)}:allf=t,vignette=angle=PI/4.5,format=yuv420p")
    segs = [timeline[i:i + seg_shots] for i in range(0, len(timeline), seg_shots)]
    total_frames = sum(nf for _, nf, _ in timeline)
    done = 0
    files = []
    for k, seg in enumerate(segs):
        fp = os.path.join(cache, f"seg_{k:03d}.mp4")
        last_png = os.path.join(cache, f"seg_{k:03d}_last.png")
        files.append(fp)
        nfr = sum(nf for _, nf, _ in seg)
        if os.path.exists(fp) and os.path.exists(last_png):
            done += nfr
            print(f"[render] parte {k + 1}/{len(segs)} ja pronta", flush=True)
            continue
        prev_png = os.path.join(cache, f"seg_{k - 1:03d}_last.png")
        prev_last = Image.open(prev_png).convert("RGB") if k and os.path.exists(prev_png) else None
        part = fp + ".part.mp4"
        vcmd = ["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(fps), "-i", "-",
                "-vf", vf, "-c:v", "libx264", "-preset", "veryfast", "-crf", "14", "-an", part]
        p = subprocess.Popen(vcmd, stdin=subprocess.PIPE)
        last = None
        for (s, nf, start) in seg:
            xf = int(s.get("xfade", 0.5 if s["type"] == "image" else 0) * fps)
            for i, fr in enumerate(SHOTS[s["type"]](ctx, s, nf)):
                if fr.size != (W, H):
                    fr = fr.resize((W, H), Image.BICUBIC)
                if prev_last is not None and i < xf:
                    fr = Image.blend(prev_last, fr, ease((i + 1) / (xf + 1)))
                if i < s.get("fade_in", 0) * fps:
                    fr = Image.blend(blank(ctx), fr, (i + 1) / (s["fade_in"] * fps + 1))
                if nf - i <= s.get("fade_out", 0) * fps:
                    fr = Image.blend(blank(ctx), fr, (nf - i) / (s["fade_out"] * fps + 1))
                p.stdin.write(fr.tobytes())
                last = fr
            prev_last = last
            done += nf
            print(f"[render] {done}/{total_frames} frames", flush=True)
        p.stdin.close(); p.wait()
        os.replace(part, fp)
        last.save(last_png)
        print(f"[render] parte {k + 1}/{len(segs)} salva", flush=True)
    lst = os.path.join(cache, "list.txt")
    open(lst, "w").write("".join(f"file '{f}'\n" for f in files))
    fvf = "format=yuv420p"
    if ep.get("subtitles"):
        sub = ctx.path(ep["subtitles"]).replace("\\", "/").replace(":", "\\:").replace("'", "\\'")
        fvf = f"subtitles='{sub}',format=yuv420p"
    print("[render] juntando partes + audio + legendas...", flush=True)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst, "-i", wav, "-vf", fvf,
                    "-c:v", "libx264", "-preset", final_preset, "-crf", final_crf, "-c:a", "aac", "-b:a", "192k",
                    "-movflags", "+faststart", "-shortest", out + ".part.mp4"], check=True)
    os.replace(out + ".part.mp4", out)
    print(f"[render] done -> {out}")
    return out


if __name__ == "__main__":
    if "--resume" in sys.argv:
        render_resumable(sys.argv[1])
    else:
        render(sys.argv[1], preview="--preview" in sys.argv)
