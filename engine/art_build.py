#!/usr/bin/env python3
"""Monta o episode.json do canal de arte a partir do plano de edição ancorado nas frases do roteiro.

episodes/<ep>/edit/plan.json:
  {"output": "X.mp4", "gap": 0.6, "chapters": [{"id": "ch00_hook", "shots": [{"cue": "primeiras palavras da frase", "type": ...}, ...]}]}
Cada plano começa quando a narração diz a frase de "cue" (sem "cue" = logo depois do plano anterior).

Com narração (pasta com narration_audio/<cap>.flac e words/<cap>.words.json, como o agente de narração publica):
  python3 engine/art_build.py <ep> --assets <pasta_do_episodio_no_branch_assets>
  -> junta os capítulos em edit/narration.flac e grava os tempos reais.
Sem narração: estima os tempos pelo texto (--wpm, padrão 150) para pré-visualizar a edição muda.
"""
import argparse, json, os, re, subprocess, unicodedata


def norm(s):
    s = unicodedata.normalize("NFD", s.lower().replace("’", "'"))
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.findall(r"[a-z0-9]+", s)


def find(tokens, cue, start):
    c = norm(cue)
    for n in (len(c), 4, 3):                      # tolera pequenas diferenças da transcrição
        n = min(n, len(c))
        for i in range(start, len(tokens) - n + 1):
            if tokens[i:i + n] == c[:n]:
                return i
    return None


def dur(path):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path]).strip())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("episode")
    ap.add_argument("--assets")
    ap.add_argument("--wpm", type=float, default=150)
    a = ap.parse_args()
    ep = os.path.join("episodes", a.episode)
    plan = json.load(open(os.path.join(ep, "edit", "plan.json")))
    gap = plan.get("gap", 0.6)
    shots, t0, audio, missing = [], 0.0, [], []
    for ch in plan["chapters"]:
        text = open(os.path.join(ep, "narration", ch["id"] + ".txt")).read()
        if a.assets:
            words = json.load(open(os.path.join(a.assets, "words", ch["id"] + ".words.json")))
            toks, times = [], []
            for w in words:
                for tk in norm(w["w"]):
                    toks.append(tk); times.append(w["s"])
            f = os.path.join(a.assets, "narration_audio", ch["id"] + ".flac")
            length = dur(f); audio.append(f)
        else:
            toks = norm(text)
            times = [i * 60.0 / a.wpm for i in range(len(toks))]
            length = len(toks) * 60.0 / a.wpm
        pos = 0
        for k, s in enumerate(ch["shots"]):
            s = dict(s)
            cue = s.pop("cue", None)
            if k == 0:
                s["at"] = round(t0, 2)
            elif cue:
                i = find(toks, cue, pos)
                if i is None:
                    missing.append(f'{ch["id"]}: {cue}')
                else:
                    pos = i
                    s["at"] = round(t0 + max(0.0, times[i] - 0.15), 2)
            shots.append(s)
        t0 += length + gap
    out = {"output": plan.get("output", a.episode + ".mp4"), "size": [1920, 1080], "fps": 30, "xfade": 0.35, "tail": 1.0, "shots": shots}
    if audio:
        lst = os.path.join(ep, "edit", "narration.txt")
        sil = os.path.join(ep, "edit", "_gap.flac")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono", "-t", str(gap), sil], check=True)
        with open(lst, "w") as fh:
            for f in audio:
                fh.write(f"file '{os.path.abspath(f)}'\nfile '{os.path.abspath(sil)}'\n")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-ar", "44100", "-ac", "1",
                        os.path.join(ep, "edit", "narration.flac")], check=True)
        out["audio"] = "narration.flac"
        if plan.get("music"):
            out["music"] = plan["music"]; out["music_gain"] = plan.get("music_gain", -24)
    else:
        out["_mudo"] = True
        # sem áudio: o último plano dura até o fim estimado
        shots.append({"type": "card", "src": shots[-1]["src"], "at": round(t0, 2), "dur": 1})
    json.dump(out, open(os.path.join(ep, "edit", "episode.json"), "w"), ensure_ascii=False, indent=1)
    print(f"{len(shots)} planos, {t0 / 60:.2f} min" + (" (tempos estimados, sem narração)" if not audio else ""))
    for m in missing:
        print("FRASE NÃO ENCONTRADA:", m)


if __name__ == "__main__":
    main()
