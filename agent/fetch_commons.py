#!/usr/bin/env python3
"""Baixa do Wikimedia Commons as imagens de um episódio do canal de arte e grava os créditos.

Lê episodes/<ep>/images.json: [{"file": "radeau.jpg", "title": "File:....jpg", "width": 3840}, ...]
Grava em <out>/ (padrão episodes/<ep>/edit/img) e escreve credits.json (licença + página de origem).
Larguras aceitas pelo Commons para miniaturas: 1280, 1920, 2560, 3840 (o original costuma ser recusado para robôs).

Uso: python3 agent/fetch_commons.py art-fr01-radeau [--out pasta]
"""
import argparse, json, os, subprocess, time, urllib.parse

UA = "ArtDocBot/1.0 (educational video research; single downloads)"


def api(params):
    u = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(params)
    for k in range(4):
        r = subprocess.run(["curl", "-sS", "-m", "40", "-A", UA, u], capture_output=True).stdout
        try:
            return json.loads(r)
        except Exception:
            time.sleep(20 * (k + 1))
    raise SystemExit("Commons não respondeu (limite de requisições?)")


def fetch(title, width, out):
    d = api(dict(action="query", titles=title, prop="imageinfo", iiprop="url|size|extmetadata", iiurlwidth=width,
                 iiextmetadatafilter="LicenseShortName|Artist", format="json"))
    i = list(d["query"]["pages"].values())[0]["imageinfo"][0]
    url = (i.get("thumburl") or i["url"]).split("?")[0].replace("thumb.wikimedia.org", "upload.wikimedia.org")
    code = ""
    for k in range(4):
        code = subprocess.run(["curl", "-sS", "-m", "300", "-A", UA, "-o", out, "-w", "%{http_code}", url],
                              capture_output=True, text=True).stdout
        if code == "200":
            break
        time.sleep(25 * (k + 1))
    lic = i["extmetadata"].get("LicenseShortName", {}).get("value")
    print(out, code, lic, flush=True)
    return dict(file=os.path.basename(out), title=title, license=lic, source=i["descriptionurl"])


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("episode")
    ap.add_argument("--out")
    a = ap.parse_args()
    ep = os.path.join("episodes", a.episode)
    out = a.out or os.path.join(ep, "edit", "img")
    os.makedirs(out, exist_ok=True)
    cred = []
    for it in json.load(open(os.path.join(ep, "images.json"))):
        cred.append(fetch(it["title"], it.get("width", 1920), os.path.join(out, it["file"])))
        time.sleep(6)
    json.dump(cred, open(os.path.join(ep, "credits.json"), "w"), ensure_ascii=False, indent=1)
