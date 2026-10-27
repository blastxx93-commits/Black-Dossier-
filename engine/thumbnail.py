#!/usr/bin/env python3
"""Black Dossier thumbnail: fixed channel template (see REGRAS-DO-CANAL.md, item 5).

    python3 engine/thumbnail.py --photo a/x.jpg --face-x 0.52 --line1 "HE" --line2 "TALKED." \
        --footer "1963" --file 2 --stamp "TOP SECRET" --out pub/thumbnail.jpg

Photo on the right (sepia), dark panel on the left, 2 lines of text (white + yellow, max 4 words),
red rule, typewriter footer, "BLACK DOSSIER · FILE 00X" on top, red stamp bottom-right.
"""
import argparse, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render as R
from PIL import Image, ImageDraw, ImageEnhance

W, H = 1280, 720
YELLOW = (229, 196, 40)


def make(photo, face_x, face_y, line1, line2, footer, file_no, stamp, out, zoom=1.15):
    ctx = R.Ctx(W, H, 24, ".")
    src = Image.open(photo).convert("L")
    s = H * zoom / src.height
    src = src.resize((int(src.width * s), int(src.height * s)), Image.LANCZOS)
    bg = Image.new("L", (W, H), 10)
    # put the subject's face at ~74% of the width, never under the text
    bg.paste(src, (int(W * 0.74 - src.width * face_x), int(H * 0.40 - src.height * face_y)))
    bg = ImageEnhance.Contrast(bg.convert("RGB")).enhance(1.3)
    r, g, b = bg.split()
    bg = Image.merge("RGB", (r.point(lambda v: min(255, int(v * 1.05))), g, b.point(lambda v: int(v * 0.88))))
    grad = Image.linear_gradient("L").rotate(90, expand=True).resize((W, H)).point(
        lambda v: int(250 * max(0, 1 - v / 200)))
    bg = Image.composite(Image.new("RGB", (W, H), (8, 7, 7)), bg, grad)
    bg = R.vignette_soft(ctx, bg)
    d = ImageDraw.Draw(bg)
    x = 56
    size = 150
    f = R.font("impact", size)
    while max(d.textlength(line1, font=f), d.textlength(line2, font=f)) > W * 0.58 and size > 90:
        size -= 6
        f = R.font("impact", size)
    d.text((x, 150), line1.upper(), font=f, fill=(240, 234, 228))
    d.text((x, 150 + int(size)), line2.upper(), font=f, fill=YELLOW)
    ry = 150 + 2 * int(size) + 28
    d.rectangle([x, ry, x + 300, ry + 8], fill=R.BRAND["red"])
    d.text((x, ry + 34), footer.upper(), font=R.font("type", 40), fill=(232, 222, 204))
    d.text((x, 48), f"BLACK DOSSIER  ·  FILE {int(file_no):03d}", font=R.font("type", 30), fill=R.BRAND["red"])
    if stamp:
        st = R.stamp(ctx, stamp.upper(), angle=-12, size=56)
        bg.paste(st, (W - st.width - 50, H - st.height - 40), st)
    bg.save(out, quality=92)
    bg.resize((320, 180), Image.LANCZOS).save(os.path.splitext(out)[0] + "_mini.jpg", quality=85)
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--photo", required=True)
    ap.add_argument("--face-x", type=float, default=0.5, help="face position in the photo, 0..1 (left→right)")
    ap.add_argument("--face-y", type=float, default=0.3)
    ap.add_argument("--line1", required=True)
    ap.add_argument("--line2", required=True)
    ap.add_argument("--footer", default="")
    ap.add_argument("--file", type=int, required=True)
    ap.add_argument("--stamp", default="CLASSIFIED")
    ap.add_argument("--zoom", type=float, default=1.15)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    if len((a.line1 + " " + a.line2).split()) > 4:
        sys.exit("Regra do canal: no máximo 4 palavras na thumbnail.")
    print(make(a.photo, a.face_x, a.face_y, a.line1, a.line2, a.footer, a.file, a.stamp, a.out, a.zoom))
