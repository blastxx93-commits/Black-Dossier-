#!/usr/bin/env python3
"""Depth maps for the 2.5D parallax camera (render_feras motion "parallax").

For every image shot with motion "parallax" in this render part, estimates depth with Depth Anything V2 Small
(CPU, ~1 s per picture) and writes <image>.depth.png next to it (white = near). Images that already have one
are skipped. Anything that fails just leaves the shot without a depth map: the renderer then falls back to a
normal push-in, so a render never breaks because of this step.

    python3 engine/depth_maps.py <work>/episode.json [--part k/n]
"""
import json, os, sys


def shots_of_part(ep, part):
    shots = [s for c in ep["chapters"] for s in c["shots"]]
    if not part:
        return shots
    k, n = map(int, part.split("/"))
    total = sum(s["dur"] for s in shots); a, b = total * (k - 1) / n, total * k / n
    out, t = [], 0.0
    for s in shots:   # generous margins: the renderer's own split may pull a neighbour in
        if t + s["dur"] >= a - 2 and t <= b + 2:
            out.append(s)
        t += s["dur"]
    return out


def main(ep_path, part=None):
    wd = os.path.dirname(os.path.abspath(ep_path))
    ep = json.load(open(ep_path))
    todo = []
    for s in shots_of_part(ep, part):
        if s.get("type") == "image" and s.get("motion") == "parallax":
            p = os.path.join(wd, s["src"])
            if os.path.exists(p) and not os.path.exists(p + ".depth.png"):
                todo.append(p)
    if not todo:
        print("profundidade: nada a fazer"); return
    try:
        from transformers import pipeline
        from PIL import Image, ImageFilter
        pipe = pipeline("depth-estimation", model="depth-anything/Depth-Anything-V2-Small-hf", device=-1)
    except Exception as e:
        print(f"profundidade indisponível ({e}); as cenas usam aproximação normal"); return
    for p in todo:
        try:
            im = Image.open(p).convert("RGB")
            small = im.copy(); small.thumbnail((960, 960))
            d = pipe(small)["depth"].convert("L").resize(im.size, Image.BICUBIC).filter(ImageFilter.GaussianBlur(6))
            d.save(p + ".depth.png")
            print(f"profundidade: {os.path.basename(p)}", flush=True)
        except Exception as e:
            print(f"profundidade falhou em {p}: {e}", flush=True)


if __name__ == "__main__":
    a = sys.argv[1:]
    part = a[a.index("--part") + 1] if "--part" in a else None
    main(a[0], part)
