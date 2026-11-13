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


def align(script, heard):
    """Para cada palavra do roteiro, o índice da palavra correspondente na transcrição (interpolado onde a transcrição diverge)."""
    import difflib
    m = [None] * len(script)
    for blk in difflib.SequenceMatcher(None, script, heard, autojunk=False).get_matching_blocks():
        for k in range(blk.size):
            m[blk.a + k] = blk.b + k
    known = [(i, v) for i, v in enumerate(m) if v is not None] or [(0, 0)]
    out = []
    for i in range(len(script)):
        prev = max((x for x in known if x[0] <= i), default=known[0], key=lambda x: x[0])
        nxt = min((x for x in known if x[0] >= i), default=known[-1], key=lambda x: x[0])
        if nxt[0] == prev[0]:
            out.append(prev[1])
        else:
            out.append(int(round(prev[1] + (nxt[1] - prev[1]) * (i - prev[0]) / (nxt[0] - prev[0]))))
    return [min(max(v, 0), len(heard) - 1) for v in out]


def find(tokens, cue, start):
    c = norm(cue)
    for i in range(start, len(tokens) - len(c) + 1):
        if tokens[i:i + len(c)] == c:
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
        script = norm(text)
        if a.assets:
            words = json.load(open(os.path.join(a.assets, "words", ch["id"] + ".words.json")))
            heard, htimes = [], []
            for w in words:
                for tk in norm(w["w"]):
                    heard.append(tk); htimes.append(w["s"])
            idx = align(script, heard)
            toks, times = script, [htimes[j] for j in idx]     # o roteiro é a referência; a transcrição só dá os tempos
            f = os.path.join(a.assets, "narration_audio", ch["id"] + (".wav" if os.path.exists(os.path.join(a.assets, "narration_audio", ch["id"] + ".wav")) else ".flac"))
            import soundfile as sf
            length = sf.info(f).duration; audio.append(f)
        else:
            toks = script
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
        import numpy as np, soundfile as sf       # pip install soundfile (lê qualquer FLAC/WAV, sem depender do ffmpeg)
        parts, sr = [], 44100
        for f in audio:
            d, sr = sf.read(f, always_2d=True)
            parts += [d.mean(axis=1), np.zeros(int(gap * sr))]
        sf.write(os.path.join(ep, "edit", "narration.wav"), np.concatenate(parts), sr, subtype="PCM_16")
        out["audio"] = "narration.wav"
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
