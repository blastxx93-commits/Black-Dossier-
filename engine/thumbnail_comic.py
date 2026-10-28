"""Black Dossier thumbnail, style A (illustrated comic) — the 'B' in the A/B test is engine/thumbnail.py (realistic sepia).

The illustration comes from the image agent (ai_prompts.json with "guard": "fictional", "raw": false,
character on the left third, empty sky on the upper right). This script writes the title on the sky.

  python3 engine/thumbnail_comic.py --img ai/thumb_a_1.jpg --line1 "MAFIA" --line2 "1891 – 1992" --out pub/thumb_A.jpg
"""
import argparse
from PIL import Image, ImageDraw, ImageFont, ImageFilter

SERIF = "/usr/share/fonts/opentype/noto/NotoSerifCJK-Black.ttc"


def fit(d, t, maxw, size):
    while size > 20:
        f = ImageFont.truetype(SERIF, size, index=0)
        if d.textlength(t, font=f) <= maxw:
            return f
        size -= 4
    return f


def make(src, out, l1, l2, cx=905, y1=40, maxw=620):
    if len((l1 + " " + l2).split()) > 6:
        raise SystemExit("Texto longo demais para a thumbnail (máx. ~4 palavras + datas)")
    im = Image.open(src).convert("RGB")
    W, H = im.size
    h = min(H, int(W * 720 / 1280))
    im = im.crop((0, 0, W, h)).resize((1280, 720), Image.LANCZOS)
    txt = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(txt)
    f1 = fit(d, l1, maxw, 190); f2 = fit(d, l2, maxw, 96)
    b1 = d.textbbox((0, 0), l1, font=f1); b2 = d.textbbox((0, 0), l2, font=f2)
    x1 = cx - (b1[2] - b1[0]) / 2 - b1[0]; x2 = cx - (b2[2] - b2[0]) / 2 - b2[0]
    y2 = y1 + (b1[3] - b1[1]) + 18 + (b1[1] - b2[1])
    for x, y, t, f in ((x1, y1, l1, f1), (x2, y2, l2, f2)):
        d.text((x, y), t, font=f, fill=(12, 12, 14, 255))
    # soft light halo so the title reads over the skyline
    halo = txt.split()[3].filter(ImageFilter.MaxFilter(15)).filter(ImageFilter.GaussianBlur(14))
    glow = Image.new("RGBA", im.size, (235, 244, 252, 0)); glow.putalpha(halo.point(lambda v: min(255, int(v * 1.0))))
    im = Image.alpha_composite(Image.alpha_composite(im.convert("RGBA"), glow), txt).convert("RGB")
    im.save(out, quality=93)
    im.resize((320, 180), Image.LANCZOS).save(out.replace(".jpg", "_mini.jpg"), quality=90)
    print(out)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--img", required=True); ap.add_argument("--line1", required=True); ap.add_argument("--line2", default="")
    ap.add_argument("--out", required=True); ap.add_argument("--cx", type=int, default=905)
    ap.add_argument("--y", type=int, default=40); ap.add_argument("--maxw", type=int, default=620)
    a = ap.parse_args()
    make(a.img, a.out, a.line1, a.line2, a.cx, a.y, a.maxw)
