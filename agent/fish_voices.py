#!/usr/bin/env python3
"""Voice scout (Fish Audio): finds the most used public voices in a language and narrates a sample with each.

Used to pick the voice of a new channel (e.g. the Portuguese Antarctica channel) before narrating a full episode.
Writes <out>/vozes/<tag>/:
    voz_<n>.mp3      the sample text read by each voice
    vozes.md         table: n, voice name, id, uses, likes, languages (also in the run summary)
    vozes.json

Run from the "Gerar narração" workflow with voice_test=pt.
Usage: python3 agent/fish_voices.py --lang pt --n 6 --text episodes/ant01-sob-o-gelo/narration/ch00_hook.txt [--query narrador]
       [--ids id1,id2]   (narrate these voice ids too, e.g. ones found on fish.audio)
Env: FISH_API_KEY, optional FISH_MODEL (default s2.1-pro).
"""
import argparse, json, os, subprocess, sys, time
import requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tts import ffmpeg, synth

API = "https://api.fish.audio/model"


def search(key, lang, query, size):
    params = {"page_size": size, "page_number": 1, "language": lang, "sort_by": "task_count"}
    if query:
        params["title"] = query
    r = requests.get(API, params=params, headers={"Authorization": f"Bearer {key}"}, timeout=60)
    r.raise_for_status()
    items = r.json().get("items", [])
    # keep voices whose declared language really includes the one asked for
    return [m for m in items if lang in (m.get("languages") or [lang])]


def info(key, vid):
    r = requests.get(f"{API}/{vid}", headers={"Authorization": f"Bearer {key}"}, timeout=60)
    return r.json() if r.status_code == 200 else {"_id": vid, "title": "?"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lang", default="pt")
    ap.add_argument("--query", default="")
    ap.add_argument("--n", type=int, default=6)
    ap.add_argument("--ids", default="")
    ap.add_argument("--text", required=True)
    ap.add_argument("--out", default="assets_out")
    ap.add_argument("--tag", default="")
    a = ap.parse_args()
    key = os.environ.get("FISH_API_KEY", "").strip()
    if not key:
        sys.exit("FISH_API_KEY precisa estar nos segredos do GitHub.")
    model = os.environ.get("FISH_MODEL", "").strip() or "s2.1-pro"
    text = open(a.text).read().strip()
    voices = [info(key, v) for v in a.ids.split(",") if v.strip()]
    seen = {v.get("_id") for v in voices}
    for m in search(key, a.lang, a.query, max(a.n * 3, 20)):
        if len(voices) >= a.n + len(seen):
            break
        if m.get("_id") not in seen:
            voices.append(m); seen.add(m.get("_id"))
    d = os.path.join(a.out, "vozes", a.tag or a.lang)
    os.makedirs(d, exist_ok=True)
    ff, rows = ffmpeg(), []
    for n, v in enumerate(voices, 1):
        vid = v.get("_id")
        try:
            wav = synth(key, vid, model, text, 1.0)
        except Exception as e:
            print(f"voz {n} ({vid}): falhou: {e}", flush=True)
            continue
        tmp = os.path.join(d, f"voz_{n}.wav")
        open(tmp, "wb").write(wav)
        subprocess.run([ff, "-v", "error", "-y", "-i", tmp, "-c:a", "libmp3lame", "-b:a", "128k",
                        os.path.join(d, f"voz_{n}.mp3")], check=True)
        os.remove(tmp)
        rows.append({"n": n, "id": vid, "nome": v.get("title", "?"), "usos": v.get("task_count", 0),
                     "likes": v.get("like_count", 0), "idiomas": ",".join(v.get("languages") or []),
                     "segundos": round(len(wav) / 88200, 1)})
        print(f"voz {n}: {v.get('title')} ({vid})", flush=True)
        time.sleep(1)
    json.dump(rows, open(os.path.join(d, "vozes.json"), "w"), ensure_ascii=False, indent=1)
    md = [f"# Teste de vozes ({a.lang})", "", f"Texto: `{a.text}` · modelo {model}", "",
          "| # | voz | id | usos | likes | idiomas | duração |", "|---|---|---|---|---|---|---|"]
    md += [f"| {r['n']} | {r['nome']} | `{r['id']}` | {r['usos']} | {r['likes']} | {r['idiomas']} | {r['segundos']} s |" for r in rows]
    open(os.path.join(d, "vozes.md"), "w").write("\n".join(md) + "\n")
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        open(os.environ["GITHUB_STEP_SUMMARY"], "a").write("\n".join(md) + "\n")
    print("\n".join(md))


if __name__ == "__main__":
    main()
