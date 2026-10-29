#!/usr/bin/env python3
"""AI image agent (Google Gemini image models, or Replicate / Flux).

Reads episodes/<ep>/ai_prompts.json and generates N options per shot in the channel style.

    {"model": "black-forest-labs/flux-1.1-pro-ultra",
     "style": ", 1950s documentary photograph, black and white ...",
     "n": 2,
     "shots": [{"id": "ch00_apalachin_meeting", "prompt": "Stone farmhouse ...", "n": 2}]}

Writes <out>/<ep>/ai/<id>_<k>.jpg, ai_contact_sheet_<k>.jpg, ai_report.md.
Provider: Gemini when env GEMINI_API_KEY is set (model from env GEMINI_IMAGE_MODEL, default
gemini-2.5-flash-image), otherwise Replicate (env REPLICATE_API_TOKEN). If Gemini fails on a shot and a
Replicate token exists, that shot falls back to Replicate. Never prints a key.

Usage: python3 agent/gen_images.py ep01-apalachin [--out assets_out] [--only id1,id2] [--force]
"""
import argparse, io, json, os, sys, time
import requests
from PIL import Image

API = "https://api.replicate.com/v1"
DEFAULT_MODEL = "black-forest-labs/flux-1.1-pro-ultra"
GUARD = (" Nobody's face is recognizable; no real person's likeness; people only from behind or far away."
         " No text, no logos, no watermark.")
# thumbnails: an invented illustrated character may show his face, but never a real person's likeness
GUARD_FICTIONAL = (" The character is entirely fictional and must not resemble any real person, actor or film character."
                   " No text, no letters, no logos, no watermark.")


GEMINI_KEY = os.environ.get("GEMINI_API_KEY", "").strip()
GEMINI_MODEL = os.environ.get("GEMINI_IMAGE_MODEL", "").strip() or "gemini-2.5-flash-image"


GEMINI_OFF = [False]


def gemini_image(prompt, aspect="16:9"):
    """One image from the Gemini API (generateContent with an image response). Returns a PIL image.
    A quota error (429 after retries) switches Gemini off for the rest of the run."""
    import base64
    if GEMINI_OFF[0]:
        raise RuntimeError("Gemini desligado nesta execução (sem cota)")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"
    body = {"contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"responseModalities": ["IMAGE"], "imageConfig": {"aspectRatio": aspect}}}
    for k in range(3):
        r = requests.post(url, json=body, headers={"x-goog-api-key": GEMINI_KEY, "Content-Type": "application/json"}, timeout=180)
        if r.status_code in (429, 500, 503) and k < 2:
            time.sleep(20 * (k + 1)); continue
        if r.status_code == 429:
            GEMINI_OFF[0] = True
        if r.status_code >= 400:
            raise RuntimeError(f"Gemini {r.status_code}: {r.text[:300]}")
        for cand in r.json().get("candidates", []):
            for part in (cand.get("content") or {}).get("parts", []):
                data = (part.get("inlineData") or part.get("inline_data") or {}).get("data")
                if data:
                    img = Image.open(io.BytesIO(base64.b64decode(data))).convert("RGB")
                    if img.width < 1920:  # Gemini returns ~1344x768: upscale once for the 1080p edit
                        img = img.resize((1920, int(img.height * 1920 / img.width)), Image.LANCZOS)
                    return img
        raise RuntimeError(f"Gemini sem imagem na resposta: {r.text[:200]}")
    raise RuntimeError("Gemini não respondeu")


def session():
    tok = os.environ.get("REPLICATE_API_TOKEN", "").strip()
    if not tok:
        if GEMINI_KEY:
            return None
        sys.exit("Nenhuma chave de IA: configure GEMINI_API_KEY ou REPLICATE_API_TOKEN (GitHub > Settings > Secrets and variables > Actions).")
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
        guard = GUARD_FICTIONAL if sh.get("guard", spec.get("guard")) == "fictional" else GUARD
        prompt = sh["prompt"].rstrip(". ") + sh.get("style", style) + guard
        files = []
        for k in range(1, n + 1):
            inp = {"prompt": prompt, "aspect_ratio": "16:9", "output_format": "jpg",
                   "safety_tolerance": 2, "raw": bool(sh.get("raw", spec.get("raw", True))), "seed": 1000 * k + len(sid)}
            try:
                img = None
                if GEMINI_KEY:
                    try:
                        img = gemini_image(prompt)
                    except Exception as e:
                        if s is None:
                            raise
                        print(f"{sid}_{k}: Gemini falhou ({str(e)[:120]}), tentando Replicate", flush=True)
                if img is None:
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
    rep = "\n".join([f"# Imagens IA — {a.episode}", "", f"- Modelo: `{GEMINI_MODEL if GEMINI_KEY else model}`", f"- Imagens geradas: {cost_n}",
                     f"- Folhas: {', '.join(os.path.basename(p) for p in sheets)}", "", "| plano | resultado |", "|---|---|"] + log) + "\n"
    open(os.path.join(ep_dir, "ai_report.md"), "w").write(rep)
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        open(os.environ["GITHUB_STEP_SUMMARY"], "a").write(rep)
    print(rep)


if __name__ == "__main__":
    main()
