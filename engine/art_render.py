#!/usr/bin/env python3
"""Motor de edição do canal de arte (estilo "pintura explicada parte por parte").

Dois tipos de plano, como no canal de referência:
  detail  a pintura em tela cheia, recortada num detalhe, com movimento lento (zoom/pan) entre dois enquadramentos
  card    imagem inteira (retrato, mapa, gravura, outra obra ou a própria pintura) como "quadro" centralizado
          sobre um fundo escuro e desfocado, com sombra e um empurrão lento

Sem texto na tela, sem tela preta, cor fiel à obra (só uma vinheta leve). Cortes com dissolve curto.

episode.json:
{
  "output": "out.mp4", "size": [1920, 1080], "fps": 30,
  "audio": "narration.flac",            # opcional; com áudio, as durações são esticadas para caber na narração
  "music": "music.mp3", "music_gain": -24,   # opcional
  "xfade": 0.35,
  "shots": [
    {"type": "card",   "src": "img/obra.jpg", "dur": 5},
    {"type": "detail", "src": "img/obra.jpg", "from": [0.50, 0.40, 0.60], "to": [0.62, 0.30, 0.22], "dur": 6},
    {"type": "card",   "src": "img/retrato.jpg", "dur": 4, "crop": [0.1, 0.0, 0.9, 1.0]}
  ]
}
Enquadramento do detail: [cx, cy, w] = centro (fração da largura/altura da imagem) e largura do recorte
(fração da largura da imagem). A altura segue 16:9. "to" ausente = empurrão leve no mesmo ponto.
"at": segundos (opcional) fixa o início do plano na narração; sem "at", os planos se distribuem por "dur".

Uso: python3 engine/art_render.py episodes/<ep>/edit/episode.json [--preview] [--from 0 --to 60]
"""
import argparse, json, os, subprocess, sys
from PIL import Image, ImageFilter, ImageDraw

Image.MAX_IMAGE_PIXELS = None
_cache = {}


def ease(t):
    return t * t * (3 - 2 * t)


def load(path):
    if path not in _cache:
        _cache[path] = Image.open(path).convert("RGB")
    return _cache[path]


def frame_box(im, f):
    """[cx, cy, w] -> caixa 16:9 em pixels, presa dentro da imagem."""
    cx, cy, w = f
    bw = w * im.width
    bh = bw * 9 / 16
    if bh > im.height:
        bh = im.height
        bw = bh * 16 / 9
    if bw > im.width:
        bw = im.width
        bh = bw * 9 / 16
    x = min(max(cx * im.width - bw / 2, 0), im.width - bw)
    y = min(max(cy * im.height - bh / 2, 0), im.height - bh)
    return (x, y, x + bw, y + bh)


def shot_detail(s, n, W, H, base):
    im = load(os.path.join(base, s["src"]))
    a = s["from"]
    b = s.get("to") or [a[0], a[1], a[2] * 0.9]
    ba, bb = frame_box(im, a), frame_box(im, b)
    # pré-reduz a imagem quando o recorte é muito maior que a tela (mais rápido e mais limpo)
    small = min(ba[2] - ba[0], bb[2] - bb[0])
    k = max(1.0, small / (W * 1.5))
    src = im if k < 1.3 else im.resize((int(im.width / k), int(im.height / k)), Image.LANCZOS)
    r = src.width / im.width
    for i in range(n):
        t = ease(i / max(1, n - 1))
        box = tuple((ba[j] + (bb[j] - ba[j]) * t) * r for j in range(4))
        yield src.transform((W, H), Image.EXTENT, box, Image.BICUBIC)


def backdrop(im, W, H):
    """Fundo do card: a própria imagem, ampliada, desfocada e escurecida."""
    key = ("bg", id(im), W, H)
    if key not in _cache:
        s = max(W / im.width, H / im.height) * 1.25
        b = im.resize((max(1, int(im.width * s / 8)), max(1, int(im.height * s / 8))), Image.BILINEAR)
        b = b.filter(ImageFilter.GaussianBlur(10)).resize((int(im.width * s), int(im.height * s)), Image.BILINEAR)
        x, y = (b.width - W) // 2, (b.height - H) // 2
        b = b.crop((x, y, x + W, y + H))
        b = Image.blend(b, Image.new("RGB", (W, H), (14, 12, 10)), 0.72)
        _cache[key] = b
    return _cache[key]


def shot_card(s, n, W, H, base):
    im = load(os.path.join(base, s["src"]))
    if s.get("crop"):
        c = s["crop"]
        im = im.crop((int(c[0] * im.width), int(c[1] * im.height), int(c[2] * im.width), int(c[3] * im.height)))
    bg = backdrop(load(os.path.join(base, s.get("bg", s["src"]))), W, H)
    z0, z1 = s.get("zoom", [1.0, 1.05])
    fit = min(W * s.get("max_w", 0.78) / im.width, H * s.get("max_h", 0.86) / im.height)
    big = im.resize((max(2, int(im.width * fit * max(z0, z1))), max(2, int(im.height * fit * max(z0, z1)))), Image.LANCZOS)
    for i in range(n):
        t = ease(i / max(1, n - 1))
        z = (z0 + (z1 - z0) * t) / max(z0, z1)
        cw, ch = max(2, int(big.width * z)), max(2, int(big.height * z))
        card = big if z > 0.999 else big.resize((cw, ch), Image.BICUBIC)
        fr = bg.copy()
        x, y = (W - cw) // 2, (H - ch) // 2
        # sombra suave
        pad = int(H * 0.05)
        sh = Image.new("L", (cw + 2 * pad, ch + 2 * pad), 0)
        ImageDraw.Draw(sh).rectangle((pad, pad + pad // 3, pad + cw, pad + ch + pad // 3), fill=150)
        sh = sh.resize((sh.width // 6, sh.height // 6)).filter(ImageFilter.GaussianBlur(3)).resize(sh.size)
        fr.paste((0, 0, 0), (x - pad, y - pad), sh)
        fr.paste(card, (x, y))
        yield fr


SHOTS = {"detail": shot_detail, "card": shot_card}


def probe(path):
    out = subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path])
    return float(out.strip())


def timeline(ep, base):
    shots = ep["shots"]
    total = sum(s.get("dur", 4) for s in shots)
    audio = os.path.join(base, ep["audio"]) if ep.get("audio") else None
    anchored = any("at" in s for s in shots)
    if not audio and not anchored:
        return [(s, s.get("dur", 4)) for s in shots], total
    if not anchored:                               # sem âncoras: estica as durações para caber na narração
        target = probe(audio) + ep.get("tail", 1.5)
        return [(s, s.get("dur", 4) * target / total) for s in shots], target
    starts = [s.get("at") for s in shots]
    starts[0] = 0.0
    last = max(i for i, v in enumerate(starts) if v is not None)
    target = probe(audio) + ep.get("tail", 1.5) if audio else starts[last] + sum(s.get("dur", 4) for s in shots[last:])
    k = 0
    while k < len(shots):                          # planos sem "at" dividem o intervalo entre duas âncoras
        if starts[k] is None:
            j = k
            while j < len(shots) and starts[j] is None:
                j += 1
            t0, t1 = starts[k - 1], (starts[j] if j < len(shots) else target)
            w = [shots[m].get("dur", 4) for m in range(k - 1, j)]
            acc = 0
            for m in range(k, j):
                acc += w[m - k]
                starts[m] = t0 + (t1 - t0) * acc / sum(w)
            k = j
        else:
            k += 1
    return [(s, max(0.2, (starts[i + 1] if i + 1 < len(shots) else target) - starts[i])) for i, s in enumerate(shots)], target


def render(path, preview=False, t_from=None, t_to=None):
    ep = json.load(open(path))
    base = os.path.dirname(os.path.abspath(path))
    W, H = (1280, 720) if preview else tuple(ep.get("size", [1920, 1080]))
    fps = ep.get("fps", 30)
    tl, total = timeline(ep, base)
    out = os.path.join(base, ep.get("output", "out.mp4"))
    if preview:
        out = out.replace(".mp4", "-preview.mp4")
    xf = int(ep.get("xfade", 0.35) * fps)
    vf = "vignette=angle=PI/5.5,format=yuv420p"
    cmd = ["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(fps), "-i", "-"]
    amap = []
    if ep.get("audio"):
        ss = ["-ss", str(t_from)] if t_from else []
        cmd += ss + ["-i", os.path.join(base, ep["audio"])]
        if ep.get("music"):
            cmd += ["-stream_loop", "-1"] + ss + ["-i", os.path.join(base, ep["music"])]
            g = ep.get("music_gain", -24)
            amap = ["-filter_complex", f"[1:a]loudnorm=I=-14:TP=-1.5[v];[2:a]volume={g}dB[m];[v][m]amix=inputs=2:duration=first:normalize=0[a]",
                    "-map", "0:v", "-map", "[a]"]
        else:
            amap = ["-map", "0:v", "-map", "1:a", "-af", "loudnorm=I=-14:TP=-1.5"]
        amap += ["-c:a", "aac", "-b:a", "192k"]
    cmd += amap + ["-vf", vf, "-c:v", "libx264", "-preset", "veryfast" if preview else "medium", "-crf", "23" if preview else "18",
                   "-movflags", "+faststart", "-shortest", out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    t, prev, done = 0.0, None, 0
    for k, (s, dur) in enumerate(tl):
        f0, f1 = int(round(t * fps)), int(round((t + dur) * fps))
        t += dur
        if (t_to is not None and f0 / fps >= t_to) or (t_from is not None and f1 / fps <= t_from):
            prev = None
            continue
        n = max(1, f1 - f0)
        last = None
        for i, fr in enumerate(SHOTS[s["type"]](s, n, W, H, base)):
            if prev is not None and i < xf and not s.get("cut"):
                fr = Image.blend(prev, fr, ease((i + 1) / (xf + 1)))
            p.stdin.write(fr.tobytes())
            last = fr
        prev = last
        done += 1
        print(f"[art] plano {k + 1}/{len(tl)} ({dur:.1f}s)", flush=True)
    p.stdin.close()
    p.wait()
    print(f"[art] pronto -> {out} ({total / 60:.2f} min no total)")
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("episode")
    ap.add_argument("--preview", action="store_true", help="720p rápido")
    ap.add_argument("--from", dest="t_from", type=float)
    ap.add_argument("--to", dest="t_to", type=float)
    a = ap.parse_args()
    render(a.episode, a.preview, a.t_from, a.t_to)
