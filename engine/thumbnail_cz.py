#!/usr/bin/env python3
"""Thumbnail for the Czech weapons-history channel, in the reference channel's look:
the weapon (AI render or real photo) on aged parchment with faint blueprint lines, and 2-3 huge black words on top.

    python3 engine/thumbnail_cz.py <image> "ODMÍTLI KALAŠNIKOV" out.jpg [--cutout] [--year 1958]

<image>: ideally an AI render already on parchment with empty space at the top (ai_prompts "thumb_a").
--cutout: the image is a real photo on a busy background: it is placed in a framed, sepia "archive print"
          on a generated parchment instead of filling the frame.
"""
import argparse, os
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps, ImageEnhance

HERE = os.path.dirname(os.path.abspath(__file__))
ANTON = os.path.join(HERE, "hyperframes", "fonts", "Anton.ttf")
COURIER = os.path.join(HERE, "hyperframes", "fonts", "CourierPrime-Bold.ttf")
W, H = 1280, 720
INK = (24, 21, 16)


def parchment():
    im = Image.new("RGB", (W, H), (230, 220, 196))
    g = Image.radial_gradient("L").resize((W, H))  # 0 centre -> 255 edge
    edge = Image.new("RGB", (W, H), (176, 152, 108))
    im = Image.composite(edge, im, g.point(lambda v: int(v * 0.8)))
    d = ImageDraw.Draw(im)
    for x in range(0, W, 32):
        d.line([(x, 0), (x, H)], fill=(214, 202, 174), width=1)
    for y in range(0, H, 32):
        d.line([(0, y), (W, y)], fill=(214, 202, 174), width=1)
    return im


def fit_text(d, text, max_w, max_h):
    size = max_h
    while size > 20:
        f = ImageFont.truetype(ANTON, size)
        b = d.textbbox((0, 0), text, font=f)
        if b[2] - b[0] <= max_w:
            return f, b
        size -= 4
    return f, b


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("image")
    ap.add_argument("words")
    ap.add_argument("out")
    ap.add_argument("--cutout", action="store_true")
    ap.add_argument("--year", default="")
    a = ap.parse_args()
    src = Image.open(a.image).convert("RGB")
    if a.cutout:
        im = parchment()
        ph = ImageOps.fit(src, (int(W * 0.78), int(H * 0.58)), Image.LANCZOS)
        ph = ImageEnhance.Color(ph).enhance(0.35)
        ph = Image.blend(ph, Image.new("RGB", ph.size, (150, 120, 80)), 0.18)
        frame = Image.new("RGB", (ph.width + 24, ph.height + 24), (245, 238, 220))
        frame.paste(ph, (12, 12))
        sh = Image.new("RGBA", (frame.width + 40, frame.height + 40), (0, 0, 0, 0))
        ImageDraw.Draw(sh).rectangle([20, 20, frame.width + 20, frame.height + 20], fill=(40, 30, 15, 120))
        sh = sh.filter(ImageFilter.GaussianBlur(12))
        x, y = (W - frame.width) // 2, H - frame.height - 36
        im.paste(sh, (x - 10, y - 4), sh)
        im.paste(frame, (x, y))
    else:
        im = ImageOps.fit(src, (W, H), Image.LANCZOS, centering=(0.5, 0.62))
    d = ImageDraw.Draw(im)
    text = a.words.upper()
    f, b = fit_text(d, text, W - 80, 170)
    tw = b[2] - b[0]
    x, y = (W - tw) // 2 - b[0], 26 - b[1]
    # soft paper halo so the words read on any background, then the ink
    halo = Image.new("L", (W, H), 0)
    ImageDraw.Draw(halo).text((x, y), text, font=f, fill=255, stroke_width=16, stroke_fill=255)
    halo = halo.filter(ImageFilter.GaussianBlur(14))
    im = Image.composite(Image.new("RGB", (W, H), (236, 227, 204)), im, halo.point(lambda v: int(v * 0.55)))
    d = ImageDraw.Draw(im)
    d.text((x, y), text, font=f, fill=INK)
    if a.year:
        fy = ImageFont.truetype(COURIER, 34)
        d.text((W - 40, H - 30), a.year, font=fy, fill=(143, 43, 29), anchor="rs")
    im.save(a.out, quality=92)
    print(a.out)


if __name__ == "__main__":
    main()
