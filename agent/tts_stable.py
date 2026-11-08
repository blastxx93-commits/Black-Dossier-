#!/usr/bin/env python3
"""Stable narration (Fish Audio): paragraph by paragraph, every paragraph checked before it is kept.

Why: generating a whole chapter in one request let the voice drift in pitch (up to ~4 semitones inside a chapter)
and occasionally insert 1–3 s of gibberish. Here each paragraph is synthesized on its own with low sampling
temperature, then:
  * transcribed (faster-whisper) and compared with the script: inserted words that are not in the text, or a
    stretch of the text that was not said, mean a glitch;
  * its median pitch is compared with the voice's target pitch (median of the first good paragraphs, or --pitch):
    more than --max-st semitones away means a tone change.
Owner rule (08/11/2026): always keep the FIRST generation of each paragraph (Fish re-generations tend to bring
the glitches). Problems are only reported in qa_narracao.md; --tries > 1 re-enables regeneration. Paragraphs are joined
with a short natural pause. Writes the same files as tts.py (narration_audio/*.flac, audio/*.mp3) plus
<ep>/qa_narracao.md (one line per paragraph: attempts, pitch, problems).

Usage: python3 agent/tts_stable.py <ep> --out ../out [--only ch01,ch02] [--lang pt] [--pitch 89]
Env: FISH_API_KEY, FISH_VOICE_ID, optional FISH_MODEL (default s2.1-pro).
"""
import argparse, difflib, glob, io, os, re, subprocess, sys, time, unicodedata, wave
import numpy as np
import requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tts import ffmpeg

SR = 44100


def norm(t):
    t = unicodedata.normalize("NFKD", t.lower())
    t = "".join(c for c in t if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]", "", t)


NUMWORDS = set("""zero um uma dois duas tres quatro cinco seis sete oito nove dez onze doze treze quatorze catorze quinze dezesseis
dezessete dezoito dezenove vinte trinta quarenta cinquenta sessenta setenta oitenta noventa cem cento duzentos duzentas trezentos
quatrocentos quinhentos seiscentos setecentos oitocentos novecentos mil milhao milhoes bilhao bilhoes virgula e por cento
graus negativos""".split())


def synth(key, voice, model, text, temperature, top_p):
    body = {"text": text, "reference_id": voice, "format": "wav", "sample_rate": SR, "normalize": True,
            "latency": "normal", "chunk_length": 300, "temperature": temperature, "top_p": top_p}
    for k in range(4):
        r = requests.post("https://api.fish.audio/v1/tts", json=body, timeout=600, headers={
            "Authorization": f"Bearer {key}", "Content-Type": "application/json", "model": model})
        if r.status_code == 200 and r.content[:4] == b"RIFF":
            return r.content
        if r.status_code in (429, 500, 502, 503):
            time.sleep(15 * (k + 1)); continue
        if r.status_code in (400, 422) and "temperature" in body:   # model without sampling options: plain request
            body.pop("temperature"); body.pop("top_p"); continue
        raise RuntimeError(f"Fish Audio {r.status_code}: {r.text[:300]}")
    raise RuntimeError("Fish Audio não respondeu")


def pcm(wav_bytes):
    w = wave.open(io.BytesIO(wav_bytes))
    x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    if w.getnchannels() == 2:
        x = x.reshape(-1, 2).mean(1)
    return x, w.getframerate()


def trim(x, sr, th=0.01):
    """Cut leading/trailing silence, keep 60 ms."""
    idx = np.where(np.abs(x) > th)[0]
    if not len(idx):
        return x
    a, b = max(0, idx[0] - int(0.06 * sr)), min(len(x), idx[-1] + int(0.06 * sr))
    return x[a:b]


def pitch(x, sr):
    import librosa
    y = librosa.resample(x, orig_sr=sr, target_sr=16000)
    f0, _, _ = librosa.pyin(y, fmin=60, fmax=300, sr=16000, frame_length=1024, hop_length=320)
    f0 = f0[~np.isnan(f0)]
    return float(np.median(f0)) if len(f0) > 20 else None


def glitches(model, x, sr, text, lang):
    import librosa
    y = librosa.resample(x, orig_sr=sr, target_sr=16000)
    segs, _ = model.transcribe(y, language=lang, beam_size=5, vad_filter=False, condition_on_previous_text=False)
    heard = [norm(w) for s in segs for w in s.text.split() if norm(w)]
    said = [norm(w) for w in text.split() if norm(w)]
    probs = []
    sm = difflib.SequenceMatcher(None, said, heard, autojunk=False)
    for op, a1, a2, b1, b2 in sm.get_opcodes():
        if op == "equal":
            continue
        s_part, h_part = said[a1:a2], heard[b1:b2]
        numeric = all(w in NUMWORDS or w.isdigit() for w in s_part) and all(any(c.isdigit() for c in w) or w in NUMWORDS for w in h_part)
        if numeric:
            continue                                   # "três mil" heard as "3000": not a problem
        if op == "insert" and len(h_part) >= 2:
            probs.append("som estranho: " + " ".join(h_part)[:50])
        elif op in ("replace", "delete") and len(s_part) >= 3 and (op == "delete" or len(h_part) <= len(s_part) // 2 + 1 or
                                                                  difflib.SequenceMatcher(None, " ".join(s_part), " ".join(h_part)).ratio() < 0.5):
            probs.append("trecho errado: " + " ".join(s_part)[:50])
    return probs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("episode")
    ap.add_argument("--out", default="assets_out")
    ap.add_argument("--only", default="")
    ap.add_argument("--lang", default="pt")
    ap.add_argument("--pitch", type=float, default=0, help="tom-alvo em Hz (0 = medido nos primeiros parágrafos)")
    ap.add_argument("--max-st", type=float, default=1.0, help="desvio máximo de tom em semitons")
    ap.add_argument("--tries", type=int, default=1,
                    help="tentativas por parágrafo; padrão 1: o dono pede sempre a 1ª geração da Fish (as regravações trazem bugs)")
    ap.add_argument("--temperature", type=float, default=0.5)
    ap.add_argument("--top-p", type=float, default=0.6)
    a = ap.parse_args()
    key, voice = os.environ.get("FISH_API_KEY", "").strip(), os.environ.get("FISH_VOICE_ID", "").strip()
    if not key or not voice:
        sys.exit("FISH_API_KEY e FISH_VOICE_ID precisam estar nos segredos do GitHub.")
    model = os.environ.get("FISH_MODEL", "").strip() or "s2.1-pro"
    from faster_whisper import WhisperModel
    asr = WhisperModel("small", device="cpu", compute_type="int8")
    only = {x for x in a.only.split(",") if x}
    texts = sorted(glob.glob(os.path.join("episodes", a.episode, "narration", "*.txt")))
    full = os.path.join(a.out, a.episode, "narration_audio"); small = os.path.join(a.out, a.episode, "audio")
    os.makedirs(full, exist_ok=True); os.makedirs(small, exist_ok=True)
    target = a.pitch or None
    ref = []
    qa = ["# Conferência da narração (parágrafo a parágrafo)", "",
          f"Temperatura {a.temperature}, top_p {a.top_p}, desvio máximo {a.max_st} semitom.", "",
          "| capítulo | parágrafo | tentativas | tom (Hz) | resultado |", "|---|---|---|---|---|"]
    ff = ffmpeg()
    for t in texts:
        name = os.path.splitext(os.path.basename(t))[0]
        if only and name not in only:
            continue
        paras = [p.strip() for p in open(t).read().split("\n\n") if p.strip()]
        parts = []
        for pi, ptxt in enumerate(paras, 1):
            best = None
            for k in range(1, a.tries + 1):
                x, sr = pcm(synth(key, voice, model, ptxt, a.temperature, a.top_p))
                x = trim(x, sr)
                probs = glitches(asr, x, sr, ptxt, a.lang)
                f0 = pitch(x, sr)
                dev = 12 * np.log2(f0 / target) if (f0 and target) else 0.0
                if abs(dev) > a.max_st:
                    probs.append(f"tom fora ({f0:.0f} Hz, {dev:+.1f} st)")
                score = len(probs) * 10 + abs(dev)
                if best is None or score < best[0]:
                    best = (score, x, f0, probs, k)
                if not probs:
                    break
                print(f"{name} §{pi} tentativa {k}: {'; '.join(probs)}", flush=True)
            _, x, f0, probs, k = best
            if f0 and not probs:
                ref.append(f0)
                if not a.pitch and len(ref) >= 3:
                    target = float(np.median(ref))
            elif f0 and target is None:
                target = f0
            qa.append(f"| {name} | {pi} | {k} | {f0 or 0:.0f} | {'ok' if not probs else '⚠ ' + '; '.join(probs)} |")
            parts.append(x)
            gap = 0.55 if ptxt.endswith(("?", "!")) or len(ptxt) > 300 else 0.45
            parts.append(np.zeros(int(gap * sr), dtype=np.float32))
        audio = np.concatenate(parts[:-1]) if parts else np.zeros(1, dtype=np.float32)
        tmp = os.path.join(full, name + ".wav")
        w = wave.open(tmp, "wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes((np.clip(audio, -1, 1) * 32767).astype(np.int16).tobytes()); w.close()
        subprocess.run([ff, "-v", "error", "-y", "-i", tmp, os.path.join(full, name + ".flac")], check=True)
        subprocess.run([ff, "-v", "error", "-y", "-i", tmp, "-ac", "1", "-ar", "16000", "-c:a", "libmp3lame", "-b:a", "48k",
                        os.path.join(small, name + ".mp3")], check=True)
        os.remove(tmp)
        print(f"{name}: {len(paras)} parágrafos, {len(audio) / sr:.0f}s, tom-alvo {target or 0:.0f} Hz", flush=True)
    open(os.path.join(a.out, a.episode, "qa_narracao.md"), "w").write("\n".join(qa) + "\n")
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        open(os.environ["GITHUB_STEP_SUMMARY"], "a").write("\n".join(qa) + "\n")
    print("\n".join(qa))


if __name__ == "__main__":
    main()
