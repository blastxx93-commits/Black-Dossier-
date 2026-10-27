#!/usr/bin/env python3
"""AI image agent (Replicate / Flux).

Reads episodes/<ep>/ai_prompts.json and generates N options per shot in the channel style.

    {"model": "black-forest-labs/flux-1.1-pro-ultra",
     "style": ", 1950s documentary photograph, black and white ...",
     "n": 2,
     "shots": [{"id": "ch00_apalachin_meeting", "prompt": "Stone farmhouse ...", "n": 2}]}

Writes <out>/<ep>/ai/<id>_<k>.jpg, ai_contact_sheet_<k>.jpg, ai_report.md.
Needs env REPLICATE_API_TOKEN (GitHub secret). Never prints the token.

Usage: python3 agent/gen_images.py ep01-apalachin [--out assets_out] [--only id1,id2] [--force]
"""
import argparse, io, json, os, sys, time
import requests
from PIL import Image

API = "https://api.replicate.com/v1"
DEFAULT_MODEL = "black-forest-labs/flux-1.1-pro-ultra"
GUARD = (" Nobody's face is recognizable; no real person's likeness; people only from behind or far away."
         " No text, no logos, no watermark.")


def session():
    tok = os.environ.get("REPLICATE_API_TOKEN", "").strip()
    if not tok:
        sys.exit("REPLICATE_API_TOKEN não configurado (GitHub > Settings > Secrets and variables > Actions).")
    s = requests.Session()
    s.headers.update({"Authorization": f"Bearer {tok}", "Content-Type": "application/json", "Prefer": "wait=60"})
    return s


def predict(s, model, inp):
    r = s.post(f"{API}/models/{model}/predictions", json={"input": inp}, timeout=120)
    if r.status_code == 429:
        time.sleep(15)
        r = s.post(f"{API}/models/{model}/predictions", json={"input": inp}, timeout=120)
    if r.status_code >= 400:
        raise RuntimeError(f"Replicate {r.status_code}: {r.text[:300]}")
    p = r.json()
    t0 = time.time()
    while p.get("status") not in ("succeeded", "failed", "canceled"):
        if time.time() - t0 > 300:
            raise RuntimeError("tempo esgotado esperando a imagem")
        time.sleep(3)
        p = s.get(p["urls"]["get"], timeout=60).json()
    if p["status"] != "succeeded":
        raise RuntimeError(f"falhou: {str(p.get('error'))[:300]}")
    out = p["output"]
    return out[0] if isinstance(out, list) else out


def contact_sheets(ep_dir, rows):
    from PIL import ImageDraw, ImageFont
    try:
        f = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 28)
    except OSError:
        f = ImageFont.load_default()
    tw, th, pad, lab = 480, 270, 16, 50
    sheets = []
    for k in range(0, len(rows), 6):
        chunk = rows[k:k + 6]
        cols = max(1, max(len(fs) for _, fs in chunk))
        sh = Image.new("RGB", (pad + cols * (tw + pad), pad + len(chunk) * (lab + th + pad)), (18, 16, 16))
        d = ImageDraw.Draw(sh)
        y = pad
        for sid, fs in chunk:
            d.text((pad, y + 8), sid, font=f, fill=(232, 222, 204)); y += lab
            for j, fp in enumerate(fs):
                im = Image.open(fp).convert("RGB"); im.thumbnail((tw, th))
                x = pad + j * (tw + pad)
                sh.paste(im, (x, y)); d.rectangle([x, y, x + 44, y + 38], fill=(196, 72, 62))
                d.text((x + 12, y + 4), str(j + 1), font=f, fill=(255, 255, 255))
            y += th + pad
        p = os.path.join(ep_dir, f"ai_contact_sheet_{k // 6 + 1}.jpg")
        sh.save(p, quality=85); sheets.append(p)
    return sheets


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("episode")
    ap.add_argument("--out", default="assets_out")
    ap.add_argument("--only", default="")
    ap.add_argument("--force", action="store_true", help="regera mesmo se a imagem já existir")
    ap.add_argument("--existing", default="", help="pasta ai/ já publicada, para pular o que já existe")
    a = ap.parse_args()
    spec = json.load(open(os.path.join("episodes", a.episode, "ai_prompts.json")))
    model = spec.get("model", DEFAULT_MODEL)
    style = spec.get("style", "")
    only = {x for x in a.only.split(",") if x}
    ep_dir = os.path.join(a.out, a.episode)
    ai_dir = os.path.join(ep_dir, "ai")
    os.makedirs(ai_dir, exist_ok=True)
    s = session()
    rows, log, cost_n = [], [], 0
    for sh in spec["shots"]:
        sid = sh["id"]
        if only and sid not in only:
            continue
        n = sh.get("n", spec.get("n", 1))
        if not a.force and a.existing and os.path.exists(os.path.join(a.existing, f"{sid}_1.jpg")):
            log.append(f"| `{sid}` | já existia, pulado |"); continue
        prompt = sh["prompt"].rstrip(". ") + style + GUARD
        files = []
        for k in range(1, n + 1):
            inp = {"prompt": prompt, "aspect_ratio": "16:9", "output_format": "jpg",
                   "safety_tolerance": 2, "raw": bool(spec.get("raw", True)), "seed": 1000 * k + len(sid)}
            try:
                url = predict(s, model, inp)
                img = Image.open(io.BytesIO(requests.get(url, timeout=120).content)).convert("RGB")
                fp = os.path.join(ai_dir, f"{sid}_{k}.jpg")
                img.save(fp, quality=92)
                files.append(fp); cost_n += 1
                print(f"{sid}_{k}: {img.size[0]}x{img.size[1]}", flush=True)
            except Exception as e:
                print(f"{sid}_{k}: ERRO {e}", flush=True)
                log.append(f"| `{sid}` opção {k} | erro: {str(e)[:120]} |")
        rows.append((sid, files))
        log.append(f"| `{sid}` | {len(files)} de {n} |")
    sheets = contact_sheets(ep_dir, [r for r in rows if r[1]])
    rep = "\n".join([f"# Imagens IA — {a.episode}", "", f"- Modelo: `{model}`", f"- Imagens geradas: {cost_n}",
                     f"- Folhas: {', '.join(os.path.basename(p) for p in sheets)}", "", "| plano | resultado |", "|---|---|"] + log) + "\n"
    open(os.path.join(ep_dir, "ai_report.md"), "w").write(rep)
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        open(os.environ["GITHUB_STEP_SUMMARY"], "a").write(rep)
    print(rep)


if __name__ == "__main__":
    main()
