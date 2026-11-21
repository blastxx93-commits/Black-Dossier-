#!/usr/bin/env python3
""""Museo" render engine — white museum-dossier style (Italian channel).

Every shot is a board on a light background:
  top      : block TITLE (caps) + subtitle (date / place) + small source line
  center   : 1–3 images with a gentle Ken Burns move, or a beige document card
  overlays : black label box sliding in, small black tag, green IMPACT word that pops in

Usage:
  python3 engine/museo.py episodes/<ep>/edit/hook.json [--preview] [--out out.mp4]

JSON:
{
 "fps": 30, "audio": "path.flac" (optional), "words": "path.words.json" (optional), "start": 0, "end": 30,
 "shots": [
  {"cue": "29 giugno" | "t": 0.0,            # start: phrase in the narration (needs words) or seconds
   "title": "MONTE SAN MICHELE, 1916", "sub": "Carso · 29 giugno 1916", "src": "Museo Storico ...",
   "images": ["a.jpg", "b.jpg"], "move": "in|out|left|right",
   "label": ["NUBE DI GAS", "cloro e fosgene"], "tag": "ARCHIVIO",
   "impact": "SOFFOCARE", "impact_at": 1.2,
   "doc": {"head": "TELEGRAMMA", "lines": ["...", "..."], "stamp": "SEGRETO"}}
 ]}
"""
import argparse, json, math, os, re, subprocess, sys, unicodedata
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = {"black": "InterDisplay-Black.otf", "bold": "Inter-Bold.otf", "med": "Inter-Medium.otf", "reg": "Inter-Regular.otf"}
BG = (243, 242, 238)
INK = (20, 20, 20)
GREY = (120, 120, 118)
GREEN = (46, 204, 96)
PAPER = (236, 228, 205)
_fc = {}


def font(kind, size):
    k = (kind, size)
    if k not in _fc:
        _fc[k] = ImageFont.truetype(os.path.join(HERE, "fonts", "museo", FONTS[kind]), size)
    return _fc[k]


def ease(x):
    x = max(0.0, min(1.0, x))
    return 1 - (1 - x) ** 3


def back(x):  # overshoot ease for the pop
    x = max(0.0, min(1.0, x))
    c = 1.7
    return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2


def norm(w):
    w = unicodedata.normalize("NFKD", w.lower())
    return re.sub(r"[^a-z0-9]", "", "".join(c for c in w if not unicodedata.combining(c)))


def find_cue(words, phrase, after=0.0):
    target = [norm(x) for x in phrase.split() if norm(x)]
    seq = [norm(w["w"]) for w in words]
    for i in range(len(seq) - len(target) + 1):
        if words[i]["s"] + 1e-3 >= after and seq[i:i + len(target)] == target:
            return words[i]["s"]
    raise SystemExit(f"Frase de corte não encontrada na narração: \"{phrase}\"")


class Ctx:
    def __init__(self, W, H, base):
        self.W, self.H, self.k, self.base = W, H, W / 1920, base
        self.cache = {}

    def p(self, v):
        return int(round(v * self.k))

    def clip(self, path, w, h, fps):
        """All frames of a clip, scaled/cropped to w x h (decoded once)."""
        key = (path, w, h)
        if key not in self.cache:
            clips = [k for k in self.cache if isinstance(k, tuple)]
            for k in clips[:-1]:
                del self.cache[k]                        # keep at most 2 clips in memory (crossfades)
            full = path if os.path.isabs(path) else os.path.join(self.base, path)
            raw = subprocess.run(["ffmpeg", "-v", "error", "-i", full, "-vf",
                                  f"fps={fps},scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},format=rgb24",
                                  "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
            n = len(raw) // (w * h * 3)
            self.cache[key] = [Image.frombytes("RGB", (w, h), raw[i * w * h * 3:(i + 1) * w * h * 3]) for i in range(n)]
        return self.cache[key]

    def img(self, path):
        if path not in self.cache:
            full = path if os.path.isabs(path) else os.path.join(self.base, path)
            self.cache[path] = Image.open(full).convert("RGB")
        return self.cache[path]


def text_c(d, ctx, y, s, f, fill, spacing=0):
    w = d.textlength(s, font=f) + spacing * max(0, len(s) - 1)
    x = (ctx.W - w) / 2
    if spacing:
        for ch in s:
            d.text((x, y), ch, font=f, fill=fill)
            x += d.textlength(ch, font=f) + spacing
    else:
        d.text((x, y), s, font=f, fill=fill)


def shadowed(canvas, im, x, y, ctx):
    sh = Image.new("RGBA", (im.width + ctx.p(40), im.height + ctx.p(40)), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rectangle([ctx.p(20), ctx.p(26), im.width + ctx.p(20), im.height + ctx.p(26)], fill=(0, 0, 0, 55))
    sh = sh.filter(ImageFilter.GaussianBlur(ctx.p(12)))
    canvas.alpha_composite(sh, (x - ctx.p(20), y - ctx.p(20)))
    canvas.paste(im, (x, y))


def smooth(x):
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)


def kenburns(src, w, h, t, move, dur=5.0):
    """Crop of src with aspect w:h, moving smoothly (no jitter: float crop box). t in 0..1.
    The move is clearly visible: about 2.5% zoom per second (12–24%) plus a pan on left/right."""
    sw, sh = src.size
    ar = w / h
    cw, ch = (sw, sw / ar) if sw / sh < ar else (sh * ar, sh)
    zoom = max(0.12, min(0.24, 0.025 * dur))
    e = 0.15 * t + 0.85 * smooth(t)                  # keeps moving from the first to the last frame
    z = {"in": 1 + zoom * e, "out": 1 + zoom * (1 - e)}.get(move, 1 + zoom)
    cw2, ch2 = cw / z, ch / z
    cx, cy = sw / 2, sh / 2
    slack_x, slack_y = (cw - cw2) / 2, (ch - ch2) / 2
    if move == "left":
        cx += slack_x * (1 - 2 * e)
    elif move == "right":
        cx -= slack_x * (1 - 2 * e)
    elif move == "in":
        cy -= slack_y * 0.5 * e                      # drift slightly up while pushing in
    elif move == "out":
        cy += slack_y * 0.5 * (1 - e)
    box = (cx - cw2 / 2, cy - ch2 / 2, cx + cw2 / 2, cy + ch2 / 2)
    return src.resize((w, h), Image.LANCZOS, box=box)


def layout(ctx, imgs):
    """Return list of (x, y, w, h) frames for 1–3 images inside the center area."""
    top, bot, side = ctx.p(215), ctx.p(950), ctx.p(220)
    area_w, area_h = ctx.W - 2 * side, bot - top
    gap = ctx.p(46)
    n = len(imgs)
    ars = [min(1.9, max(0.6, im.width / im.height)) for im in imgs]
    h = area_h if n == 1 else int(area_h * (0.78 if n == 2 else 0.62))
    ws = [int(h * a) for a in ars]
    tot = sum(ws) + gap * (n - 1)
    if tot > area_w:
        s = (area_w - gap * (n - 1)) / sum(ws)
        ws, h = [int(w * s) for w in ws], int(h * s)
        tot = sum(ws) + gap * (n - 1)
    x = (ctx.W - tot) // 2
    y = top + (area_h - h) // 2
    out = []
    for w in ws:
        out.append((x, y, w, h))
        x += w + gap
    return out


def draw_doc(canvas, ctx, doc, t_in):
    d = ImageDraw.Draw(canvas)
    w, h = ctx.p(980), ctx.p(640)
    x = (ctx.W - w) // 2
    y = ctx.p(250) + int(ctx.p(120) * (1 - ease(t_in / 0.6)))
    card = Image.new("RGB", (w, h), PAPER)
    cd = ImageDraw.Draw(card)
    cd.text((ctx.p(56), ctx.p(48)), doc.get("head", "DOCUMENTO"), font=font("bold", ctx.p(34)), fill=INK)
    cd.line([ctx.p(56), ctx.p(100), w - ctx.p(56), ctx.p(100)], fill=(150, 140, 115), width=ctx.p(2))
    yy = ctx.p(130)
    for ln in doc.get("lines", []):
        cd.text((ctx.p(56), yy), ln, font=font("reg", ctx.p(30)), fill=(55, 50, 40))
        yy += ctx.p(52)
    if doc.get("stamp"):
        st = Image.new("RGBA", (ctx.p(340), ctx.p(120)), (0, 0, 0, 0))
        sd = ImageDraw.Draw(st)
        sd.rounded_rectangle([4, 4, st.width - 4, st.height - 4], radius=ctx.p(12), outline=(180, 30, 30, 210), width=ctx.p(6))
        f = font("black", ctx.p(48))
        sd.text(((st.width - sd.textlength(doc["stamp"], font=f)) / 2, ctx.p(28)), doc["stamp"], font=f, fill=(180, 30, 30, 210))
        st = st.rotate(-12, expand=True, resample=Image.BICUBIC)
        card.paste(st, (w - st.width - ctx.p(40), h - st.height - ctx.p(30)), st)
    shadowed(canvas, card, x, y, ctx)
    return (x, y, w, h)


def render_shot(ctx, s, t, dur):
    """Frame of shot s at local time t (seconds)."""
    c = Image.new("RGBA", (ctx.W, ctx.H), BG + (255,))
    d = ImageDraw.Draw(c)
    # header
    a = ease(t / 0.35)
    if s.get("title"):
        f = font("black", ctx.p(54))
        hdr = Image.new("RGBA", (ctx.W, ctx.p(200)), (0, 0, 0, 0))
        hd = ImageDraw.Draw(hdr)
        text_c(hd, ctx, ctx.p(52), s["title"], f, INK + (int(255 * a),), spacing=ctx.p(2))
        if s.get("sub"):
            text_c(hd, ctx, ctx.p(124), s["sub"], font("med", ctx.p(26)), GREY + (int(255 * a),))
        if s.get("src"):
            text_c(hd, ctx, ctx.p(160), s["src"], font("reg", ctx.p(19)), (165, 165, 160, int(255 * a)))
        c.alpha_composite(hdr, (0, int(ctx.p(14) * (1 - a))))
    frames = []
    if s.get("doc"):
        frames = [draw_doc(c, ctx, s["doc"], t)]
    elif s.get("video"):
        x0, y0, w0, h0 = layout(ctx, [Image.new("RGB", (16, 9))])[0]
        frs = ctx.clip(s["video"], w0, h0, ctx.fps)
        pic = frs[min(len(frs) - 1, int(t * ctx.fps))] if frs else Image.new("RGB", (w0, h0), (60, 60, 60))
        if s.get("bw", True):
            pic = pic.convert("L").convert("RGB")
        e = ease(t / 0.4)
        border = ctx.p(10)
        framed = Image.new("RGB", (w0 + 2 * border, h0 + 2 * border), (255, 255, 255))
        framed.paste(pic, (border, border))
        layer = Image.new("RGBA", (ctx.W, ctx.H), (0, 0, 0, 0))
        shadowed(layer, framed, x0 - border, y0 - border, ctx)
        if e < 1:
            layer.putalpha(layer.getchannel("A").point(lambda v: int(v * e)))
        c.alpha_composite(layer)
        frames = [(x0, y0, w0, h0)]
    elif s.get("images"):
        imgs = [ctx.img(p) for p in s["images"]]
        frames = layout(ctx, imgs)
        move = s.get("move", "in")
        for i, (im, (x, y, w, h)) in enumerate(zip(imgs, frames)):
            ti = t - i * 0.45                              # images enter one after another
            if ti < 0:
                continue
            e = ease(ti / 0.4)
            sc = 0.96 + 0.04 * e
            pic = kenburns(im, w, h, min(1, t / max(dur, 0.1)), move if i % 2 == 0 else {"in": "out", "out": "in"}.get(move, move), dur)
            border = ctx.p(10)
            framed = Image.new("RGB", (w + 2 * border, h + 2 * border), (255, 255, 255))
            framed.paste(pic, (border, border))
            fw, fh = int(framed.width * sc), int(framed.height * sc)
            framed = framed.resize((fw, fh), Image.BICUBIC)
            layer = Image.new("RGBA", (ctx.W, ctx.H), (0, 0, 0, 0))
            shadowed(layer, framed, x - border + (w + 2 * border - fw) // 2, y - border + (h + 2 * border - fh) // 2, ctx)
            if e < 1:
                layer.putalpha(layer.getchannel("A").point(lambda v: int(v * e)))
            c.alpha_composite(layer)
    d = ImageDraw.Draw(c)
    # tag (top-left of the first frame)
    if s.get("tag") and frames and t > 0.3:
        x, y, w, h = frames[0]
        f = font("bold", ctx.p(20))
        tw = d.textlength(s["tag"], font=f)
        d.rectangle([x - ctx.p(10), y - ctx.p(52), x - ctx.p(10) + tw + ctx.p(24), y - ctx.p(20)], fill=INK)
        d.text((x + ctx.p(2), y - ctx.p(49)), s["tag"], font=f, fill=(255, 255, 255))
    # label box (slides in from the right, bottom-right of the last frame)
    if s.get("label") and frames:
        lt = t - s.get("label_at", 0.8)
        if lt > 0:
            x, y, w, h = frames[-1]
            l1, l2 = (s["label"] + [""])[:2]
            f1, f2 = font("bold", ctx.p(26)), font("reg", ctx.p(21))
            bw = int(max(d.textlength(l1, font=f1), d.textlength(l2, font=f2)) + ctx.p(48))
            bh = ctx.p(92) if l2 else ctx.p(60)
            bx = min(ctx.W - bw - ctx.p(40), x + w - bw // 2) + int(ctx.p(60) * (1 - ease(lt / 0.3)))
            by = y + h - bh - ctx.p(30)
            box = Image.new("RGBA", (bw, bh), (18, 18, 18, int(240 * ease(lt / 0.3))))
            bd = ImageDraw.Draw(box)
            bd.rectangle([0, 0, ctx.p(6), bh], fill=(200, 40, 40, 255))
            bd.text((ctx.p(24), ctx.p(14)), l1, font=f1, fill=(255, 255, 255))
            if l2:
                bd.text((ctx.p(24), ctx.p(52)), l2, font=f2, fill=(200, 200, 200))
            c.alpha_composite(box, (bx, by))
    # impact word (smooth pop, no shake)
    if s.get("impact"):
        it = t - s.get("impact_at", 1.0)
        if it > 0:
            f = font("black", ctx.p(130))
            word = s["impact"]
            tw = int(d.textlength(word, font=f)) + ctx.p(40)
            lay = Image.new("RGBA", (tw, ctx.p(190)), (0, 0, 0, 0))
            ld = ImageDraw.Draw(lay)
            ld.text((ctx.p(24), ctx.p(14)), word, font=f, fill=(0, 0, 0, 70))
            ld.text((ctx.p(16), ctx.p(6)), word, font=f, fill=GREEN)
            sc = 1.25 - 0.25 * back(it / 0.28)
            lay = lay.resize((max(1, int(lay.width * sc)), max(1, int(lay.height * sc))), Image.BICUBIC)
            c.alpha_composite(lay, (ctx.p(90), ctx.H - ctx.p(225) - (lay.height - ctx.p(190)) // 2))
    # thin footer rule like the reference
    d.line([ctx.p(40), ctx.H - ctx.p(34), ctx.p(330), ctx.H - ctx.p(34)], fill=(200, 200, 196), width=ctx.p(2))
    out = c.convert("RGB")
    if s.get("doc"):                                  # documents: slow continuous push-in (float box = no jitter)
        z = 1 + 0.06 * (0.15 * min(1, t / max(dur, .1)) + 0.85 * smooth(t / max(dur, .1)))
        bw, bh = ctx.W / z, ctx.H / z
        out = out.resize((ctx.W, ctx.H), Image.BICUBIC, box=((ctx.W - bw) / 2, (ctx.H - bh) / 2 + (ctx.H - bh) * 0.1,
                                                              (ctx.W + bw) / 2, (ctx.H + bh) / 2 + (ctx.H - bh) * 0.1))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("spec")
    ap.add_argument("--preview", action="store_true")
    ap.add_argument("--out", default="")
    a = ap.parse_args()
    spec = json.load(open(a.spec))
    base = os.path.dirname(os.path.abspath(a.spec))
    W, H = (960, 540) if a.preview else (1920, 1080)
    fps = spec.get("fps", 30)
    ctx = Ctx(W, H, base)
    ctx.fps = fps
    words = json.load(open(os.path.join(base, spec["words"]))) if spec.get("words") else None
    shots = spec["shots"]
    t0 = spec.get("start", 0.0)
    for s in shots:
        s["_t"] = s["t"] if "t" in s else find_cue(words, s["cue"]) - 0.15
    end = spec.get("end") or (words[-1]["e"] + 0.8)
    for i, s in enumerate(shots):
        s["_end"] = shots[i + 1]["_t"] if i + 1 < len(shots) else end
    out = a.out or os.path.splitext(a.spec)[0] + (".preview.mp4" if a.preview else ".mp4")
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(fps), "-i", "-"]
    if spec.get("audio"):
        cmd += ["-ss", str(t0), "-t", str(end - t0), "-i", os.path.join(base, spec["audio"])]
    cmd += ["-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p"]
    if spec.get("audio"):
        cmd += ["-c:a", "aac", "-b:a", "192k", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11,apad", "-t", f"{end - t0:.3f}"]
    cmd += [out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    XF = 0.3
    n = int((end - t0) * fps)
    for fi in range(n):
        t = t0 + fi / fps
        idx = max(i for i, s in enumerate(shots) if s["_t"] <= t + 1e-6) if t >= shots[0]["_t"] else 0
        s = shots[idx]
        fr = render_shot(ctx, s, t - s["_t"], s["_end"] - s["_t"])
        if idx > 0 and t - s["_t"] < XF:                    # crossfade from the previous shot
            pv = shots[idx - 1]
            prev = render_shot(ctx, pv, t - pv["_t"], pv["_end"] - pv["_t"])
            fr = Image.blend(prev, fr, ease((t - s["_t"]) / XF))
        p.stdin.write(fr.tobytes())
        if fi % (fps * 5) == 0:
            print(f"{t:6.1f}s / {end:.1f}s", flush=True)
    p.stdin.close()
    p.wait()
    print("ok:", out)


if __name__ == "__main__":
    main()
