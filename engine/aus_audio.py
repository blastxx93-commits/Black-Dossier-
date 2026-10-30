#!/usr/bin/env python3
"""Synthesized sound kit for the Aussie car channel (deterministic, no files to download).

Writes into <dir>: sfx/whoosh.wav, sfx/hit.wav, sfx/pop.wav and trilha.wav (40 s loop, 96 bpm, minor
progression, pad + pulse bass + hats + kick). The music is a placeholder: swap trilha.wav for a licensed
track (YouTube Audio Library) when you have one.

Usage: python3 engine/aus_audio.py <dir>
"""
import os, sys, wave
import numpy as np

SR = 48000


def save(path, x):
    x = np.clip(x / (np.abs(x).max() + 1e-9) * 0.9, -1, 1)
    x = np.stack([x, x], 1)
    w = wave.open(path, "wb")
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((x * 32767).astype(np.int16).tobytes()); w.close()


def lp(x, a):
    """One-pole low-pass (vectorised with a scan in chunks for speed)."""
    y = np.empty_like(x); s = 0.0
    for i, v in enumerate(x):
        s += a * (v - s); y[i] = s
    return y


def main(out):
    os.makedirs(os.path.join(out, "sfx"), exist_ok=True)
    rng = np.random.default_rng(1)
    n = int(SR * 0.7); t = np.arange(n) / SR; noise = rng.standard_normal(n)
    a = 0.02 + 0.25 * np.sin(np.pi * t / 0.7) ** 2; y = np.zeros(n); s = 0
    for i in range(n):
        s += a[i] * (noise[i] - s); y[i] = s
    save(os.path.join(out, "sfx", "whoosh.wav"), y * np.sin(np.pi * t / 0.7) ** 1.5)
    n = int(SR * 1.2); t = np.arange(n) / SR
    boom = np.sin(2 * np.pi * (48 * t + 18 * (1 - np.exp(-t * 25)) / 25 * 25 / 6)) * np.exp(-t * 3.2)
    click = lp(rng.standard_normal(n), 0.3) * np.exp(-t * 60)
    save(os.path.join(out, "sfx", "hit.wav"), boom + 0.5 * click)
    n = int(SR * 0.15); t = np.arange(n) / SR
    save(os.path.join(out, "sfx", "pop.wav"), np.sin(2 * np.pi * (900 * t - 1500 * t * t)) * np.exp(-t * 40))
    bpm = 96; beat = 60 / bpm; bars = 16; L = int(SR * beat * 4 * bars)
    prog = [(57, 60, 64), (53, 57, 60), (48, 52, 55), (55, 59, 62)]
    f = lambda m: 440 * 2 ** ((m - 69) / 12)
    pad = np.zeros(L); bass = np.zeros(L); hat = np.zeros(L)
    for b in range(bars):
        ch = prog[b % 4]; s0 = int(b * 4 * beat * SR); s1 = int((b + 1) * 4 * beat * SR); tt = np.arange(s1 - s0) / SR
        env = np.minimum(1, tt / 0.8) * np.minimum(1, (tt[-1] - tt + 0.05) / 0.6)
        for m in ch:
            for det in (-0.08, 0.08):
                pad[s0:s1] += np.sin(2 * np.pi * f(m) * (1 + det / 100) * tt) * env * 0.18
        for k in range(8):
            a0 = s0 + int(k * beat / 2 * SR); a1 = min(s1, a0 + int(beat / 2 * SR)); tb = np.arange(a1 - a0) / SR
            bass[a0:a1] += np.sign(np.sin(2 * np.pi * f(ch[0] - 24) * tb)) * np.exp(-tb * 9) * 0.35
        for k in range(16):
            a0 = s0 + int(k * beat / 4 * SR); a1 = min(s1, a0 + int(0.04 * SR))
            hat[a0:a1] += rng.standard_normal(a1 - a0) * np.exp(-np.arange(a1 - a0) / SR * 120) * (0.12 if k % 2 else 0.05)
    bass = lp(bass, 0.08); hat = hat - lp(hat, 0.5)
    kick = np.zeros(L)
    for k in range(bars * 4):
        a0 = int(k * beat * SR); tk = np.arange(int(0.35 * SR)) / SR
        seg = np.sin(2 * np.pi * (50 * tk + 60 * (1 - np.exp(-tk * 30)) / 30)) * np.exp(-tk * 9)
        kick[a0:a0 + len(seg)] += seg[:L - a0] * 0.6
    save(os.path.join(out, "trilha.wav"), lp(pad, 0.12) * 0.9 + bass + hat + kick)
    print(f"kit de som em {out}")


if __name__ == "__main__":
    main(sys.argv[1])
