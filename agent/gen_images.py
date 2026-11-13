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


CF_ACCOUNT = os.environ.get("CF_ACCOUNT_ID", "").strip()
CF_TOKEN = os.environ.get("CF_API_TOKEN", "").strip()
FREE = os.environ.get("FREE_IMAGES", "").strip() == "1"   # use the free generators first (Cloudflare, Pollinations)
CF_OFF = [False]


def _hd(img):
    """Free generators return ~1024-1440 px: crop to 16:9 and upscale once with Lanczos for the 1080p edit."""
    w, h = img.size
    if abs(w / h - 16 / 9) > 0.02:
        nh = int(w * 9 / 16)
        if nh <= h:
            img = img.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))
        else:
            nw = int(h * 16 / 9); img = img.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
    if img.width < 1920:
        img = img.resize((1920, 1080), Image.LANCZOS)
    return img


def cloudflare_image(prompt, seed):
    """Cloudflare Workers AI, Flux-1 Schnell (free daily allowance). Needs CF_ACCOUNT_ID + CF_API_TOKEN."""
    import base64
    if CF_OFF[0]:
        raise RuntimeError("Cloudflare desligado nesta execução (sem cota)")
    url = f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT}/ai/run/@cf/black-forest-labs/flux-1-schnell"
    r = requests.post(url, json={"prompt": prompt[:2000], "steps": 8, "seed": seed},
                      headers={"Authorization": f"Bearer {CF_TOKEN}"}, timeout=180)
    if r.status_code == 429 or "neurons" in r.text.lower() and r.status_code >= 400:
        CF_OFF[0] = True
    if r.status_code >= 400:
        raise RuntimeError(f"Cloudflare {r.status_code}: {r.text[:200]}")
    data = (r.json().get("result") or {}).get("image")
    if not data:
        raise RuntimeError(f"Cloudflare sem imagem: {r.text[:200]}")
    return _hd(Image.open(io.BytesIO(base64.b64decode(data))).convert("RGB"))


def pollinations_image(prompt, seed):
    """Pollinations (free, no key): Flux at 1920x1088, a few seconds each; retried, then gives up."""
    from urllib.parse import quote
    url = (f"https://image.pollinations.ai/prompt/{quote(prompt[:1500])}"
           f"?width=1920&height=1088&model=flux&nologo=true&private=true&enhance=false&seed={seed}")
    for k in range(4):
        try:
            r = requests.get(url, timeout=240)
            if r.status_code == 200 and r.headers.get("content-type", "").startswith("image"):
                return _hd(Image.open(io.BytesIO(r.content)).convert("RGB"))
            err = f"{r.status_code}: {r.text[:120]}"
        except Exception as e:
            err = str(e)[:120]
        time.sleep(15 * (k + 1))
    raise RuntimeError(f"Pollinations falhou: {err}")


def free_image(prompt, seed):
    errs = []
    if CF_ACCOUNT and CF_TOKEN:
        try:
            return cloudflare_image(prompt, seed), "cloudflare"
        except Exception as e:
            errs.append(str(e)[:100])
    try:
        return pollinations_image(prompt, seed), "pollinations"
    except Exception as e:
        errs.append(str(e)[:100])
    raise RuntimeError(" / ".join(errs))


def session():
    tok = os.environ.get("REPLICATE_API_TOKEN", "").strip()
    if not tok:
        if GEMINI_KEY or FREE:
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
    ap.add_argument("--attempt", type=int, default=0, help="muda a semente (regerar uma reprovada com outra variação)")
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
                if FREE:
                    try:
                        img, used = free_image(prompt, 1000 * k + len(sid) + 7 * a.attempt)
                        print(f"{sid}_{k}: gerada no {used}", flush=True)
                    except Exception as e:
                        if s is None and not GEMINI_KEY:
                            raise
                        print(f"{sid}_{k}: geradores grátis falharam ({str(e)[:120]})", flush=True)
                if img is None and GEMINI_KEY:
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
    rep = "\n".join([f"# Imagens IA — {a.episode}", "", f"- Modelo: `{'grátis (Cloudflare/Pollinations)' if FREE else (GEMINI_MODEL if GEMINI_KEY else model)}`", f"- Imagens geradas: {cost_n}",
                     f"- Folhas: {', '.join(os.path.basename(p) for p in sheets)}", "", "| plano | resultado |", "|---|---|"] + log) + "\n"
    open(os.path.join(ep_dir, "ai_report.md"), "w").write(rep)
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        open(os.environ["GITHUB_STEP_SUMMARY"], "a").write(rep)
    print(rep)


if __name__ == "__main__":
    main()
