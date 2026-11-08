#!/usr/bin/env python3
"""Evens out the narrator's tone between paragraphs, keeping the first Fish generation (owner rule).

The TTS voice drifts in pitch from one paragraph to the next (up to ~4 semitones between neighbours). For each chapter:
  * paragraph boundaries come from the script (blank lines) aligned to the word timings (words/<ch>.words.json);
  * the median pitch of each paragraph is measured (pYIN);
  * a paragraph further than --keep semitones from the voice's target pitch is shifted toward it (only the excess),
    with ffmpeg's rubberband filter: formants preserved (same timbre), duration unchanged (word timings stay valid).
Rewrites narration_audio/<ch>.flac and audio/<ch>.mp3 in place; writes tom_corrigido.md.

Usage: python3 agent/fix_tone.py <ep> <ep_out_dir> [--target 0] [--keep 0.6]
"""
import argparse, glob, json, os, subprocess, sys, tempfile
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "engine"))
from cues import Chapter


def load(path, sr=44100):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32).copy()


def pitch(x, sr):
    import librosa
    y = librosa.resample(x, orig_sr=sr, target_sr=16000)
    f0, _, _ = librosa.pyin(y, fmin=60, fmax=300, sr=16000, frame_length=1024, hop_length=320)
    f0 = f0[~np.isnan(f0)]
    return float(np.median(f0)) if len(f0) > 20 else None


def shift(x, sr, st):
    with tempfile.TemporaryDirectory() as d:
        a, b = os.path.join(d, "a.f32"), os.path.join(d, "b.f32")
        x.astype(np.float32).tofile(a)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(sr), "-ac", "1", "-i", a,
                        "-af", f"rubberband=pitch={2 ** (st / 12):.6f}:formant=preserved:pitchq=quality:transients=smooth",
                        "-f", "f32le", "-ar", str(sr), "-ac", "1", b], check=True)
        y = np.fromfile(b, dtype=np.float32)
    n = len(x)
    return y[:n] if len(y) >= n else np.pad(y, (0, n - len(y)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("episode")
    ap.add_argument("out")
    ap.add_argument("--target", type=float, default=0)
    ap.add_argument("--keep", type=float, default=0.6, help="desvio aceito sem correção, em semitons")
    a = ap.parse_args()
    sr = 44100
    chapters = sorted(glob.glob(os.path.join("episodes", a.episode, "narration", "*.txt")))
    data = []
    for t in chapters:
        name = os.path.splitext(os.path.basename(t))[0]
        flac = os.path.join(a.out, "narration_audio", name + ".flac")
        words = os.path.join(a.out, "words", name + ".words.json")
        if not (os.path.exists(flac) and os.path.exists(words)):
            continue
        x = load(flac, sr)
        c = Chapter(name, t, words, flac)
        paras = [p for p in open(t).read().split("\n\n") if p.strip()]
        # word index where each paragraph starts -> time (the aligned script timings)
        starts, k = [], 0
        from cues import tokens
        for p in paras:
            starts.append(c.t[k] if k < len(c.t) else c.t[-1])
            k += len(tokens(p))
        bounds = [max(0, int((s - 0.15) * sr)) for s in starts] + [len(x)]
        bounds[0] = 0
        segs = [(bounds[i], bounds[i + 1]) for i in range(len(paras))]
        f0s = [pitch(x[s:e], sr) for s, e in segs]
        data.append((name, flac, x, segs, f0s))
    allf = [f for d in data for f in d[4] if f]
    target = a.target or float(np.median(allf))
    rep = ["# Correção de tom da narração", "", f"Tom-alvo {target:.1f} Hz · desvio aceito ±{a.keep} semitom", "",
           "| capítulo | parágrafo | tom antes | ajuste | tom depois |", "|---|---|---|---|---|"]
    for name, flac, x, segs, f0s in data:
        y = x.copy()
        for i, ((s, e), f0) in enumerate(zip(segs, f0s), 1):
            if not f0:
                continue
            dev = 12 * np.log2(f0 / target)
            if abs(dev) <= a.keep:
                rep.append(f"| {name} | {i} | {f0:.0f} Hz ({dev:+.1f}) | — | {f0:.0f} Hz |")
                continue
            st = -(dev - np.sign(dev) * a.keep)
            seg = shift(x[s:e], sr, st)
            fade = min(int(0.03 * sr), (e - s) // 4)   # tiny crossfade at the joins: no clicks
            if fade > 0:
                ramp = np.linspace(0, 1, fade, dtype=np.float32)
                seg[:fade] = seg[:fade] * ramp + x[s:s + fade] * (1 - ramp)
                seg[-fade:] = seg[-fade:] * ramp[::-1] + x[e - fade:e] * (1 - ramp[::-1])
            y[s:e] = seg
            after = pitch(seg, sr)
            rep.append(f"| {name} | {i} | {f0:.0f} Hz ({dev:+.1f}) | {st:+.1f} st | {after or 0:.0f} Hz |")
        tmp = flac + ".tmp.wav"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(sr), "-ac", "1", "-i", "-", tmp],
                       input=np.clip(y, -1, 1).astype(np.float32).tobytes(), check=True)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmp, flac], check=True)
        mp3 = os.path.join(a.out, "audio", name + ".mp3")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmp, "-ac", "1", "-ar", "16000", "-c:a", "libmp3lame", "-b:a", "48k", mp3],
                       check=True)
        os.remove(tmp)
        print(f"{name}: ok", flush=True)
    open(os.path.join(a.out, "tom_corrigido.md"), "w").write("\n".join(rep) + "\n")
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        open(os.environ["GITHUB_STEP_SUMMARY"], "a").write("\n".join(rep) + "\n")
    print("\n".join(rep))


if __name__ == "__main__":
    main()
