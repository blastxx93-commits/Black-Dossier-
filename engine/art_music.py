#!/usr/bin/env python3
"""Trilha original do canal de arte: cama lenta e sombria (cordas graves + notas de piano espaçadas), gerada por código.
Sem amostras de terceiros, então não há risco de direitos autorais nem de Content ID.

Uso: python3 engine/art_music.py saida.flac --minutes 10 [--seed 1] [--key 50]
  --key = nota MIDI da tônica (50 = ré; modo menor). Mude a semente para variar a melodia de um vídeo para outro.
"""
import argparse, subprocess, sys
import numpy as np

SR = 44100


def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def pad(freq, n, rng):
    """Corda sintética: 3 osciladores levemente desafinados, harmônicos suaves, vibrato lento."""
    t = np.arange(n) / SR
    out = np.zeros(n)
    for det in (-0.07, 0.0, 0.06):
        f = freq * 2 ** (det / 12)
        vib = 1 + 0.002 * np.sin(2 * np.pi * (0.15 + rng.random() * 0.2) * t + rng.random() * 6)
        ph = 2 * np.pi * np.cumsum(f * vib) / SR + rng.random() * 6
        for h, amp in ((1, 1.0), (2, 0.35), (3, 0.16), (4, 0.07)):
            out += amp * np.sin(h * ph)
    return out / 3


def env(n, a, r):
    e = np.ones(n)
    a, r = min(int(a * SR), n // 2), min(int(r * SR), n // 2)
    e[:a] = np.sin(np.linspace(0, np.pi / 2, a)) ** 2
    e[-r:] = np.cos(np.linspace(0, np.pi / 2, r)) ** 2
    return e


def piano(freq, n):
    t = np.arange(n) / SR
    s = sum(a * np.sin(2 * np.pi * freq * h * t) * np.exp(-t * (0.5 + 0.35 * h)) for h, a in ((1, 1), (2, 0.4), (3, 0.18), (4, 0.08)))
    s[:200] *= np.linspace(0, 1, 200)
    return s


def reverb(x, rng):
    """Cauda simples: soma de ecos difusos decrescentes."""
    y = x.copy()
    for d, g in ((0.031, 0.5), (0.047, 0.42), (0.071, 0.36), (0.113, 0.3), (0.167, 0.24), (0.241, 0.18), (0.353, 0.13), (0.521, 0.09)):
        k = int(d * SR * (1 + rng.random() * 0.1))
        y[k:] += g * x[:-k]
    return y


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--minutes", type=float, default=10)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--key", type=int, default=50)
    a = ap.parse_args()
    rng = np.random.default_rng(a.seed)
    k = a.key
    # i – VI – iv – V(sus→maior) – i – III – iv – v   (menor, lento, sem resolver de vez)
    prog = [(0, [0, 7, 12, 15, 19]), (-4, [0, 7, 12, 16, 19]), (-7, [0, 7, 12, 15, 19]), (-5, [0, 7, 12, 17, 19]),
            (0, [0, 7, 12, 15, 19]), (3, [0, 7, 12, 16, 19]), (-7, [0, 7, 12, 15, 19]), (-5, [0, 7, 12, 15, 19])]
    scale = [0, 2, 3, 5, 7, 8, 10]
    bar = 14.0
    N = int(a.minutes * 60 * SR)
    L, R = np.zeros(N + SR * 20), np.zeros(N + SR * 20)
    nb = int(np.ceil(a.minutes * 60 / bar))
    for b in range(nb):
        root, tones = prog[b % len(prog)]
        s0 = int(b * bar * SR)
        n = int((bar + 5) * SR)                       # sobrepõe 5 s no acorde seguinte
        e = env(n, 5.0, 6.0)
        for j, iv in enumerate(tones):
            m = k - 12 + root + iv
            sig = pad(hz(m), n, rng) * e * (0.5 if j == 0 else 0.3)
            pan = 0.5 + (j - 2) * 0.16
            L[s0:s0 + n] += sig * (1 - pan); R[s0:s0 + n] += sig * pan
        sub = np.sin(2 * np.pi * hz(k - 24 + root) * np.arange(n) / SR) * e * 0.35
        L[s0:s0 + n] += sub; R[s0:s0 + n] += sub
        # 1 a 3 notas de piano por compasso, sempre do acorde ou da escala, bem espaçadas
        t = 1.5 + rng.random() * 2
        while t < bar - 2:
            deg = rng.choice(tones[2:]) if rng.random() < 0.7 else rng.choice(scale) - root % 12 + 12
            m = k + 12 + root + int(deg) - 12 * int(rng.random() < 0.35)
            pn = int(7 * SR)
            p0 = s0 + int(t * SR)
            sig = piano(hz(m), pn) * (0.10 + rng.random() * 0.06)
            pan = 0.3 + rng.random() * 0.4
            L[p0:p0 + pn] += sig * (1 - pan); R[p0:p0 + pn] += sig * pan
            t += 3.5 + rng.random() * 5
    L, R = reverb(L, rng)[:N], reverb(R, rng)[:N]
    # filtro passa-baixa suave (média móvel dupla) para tirar o brilho digital
    ker = np.ones(9) / 9
    L, R = np.convolve(np.convolve(L, ker, "same"), ker, "same"), np.convolve(np.convolve(R, ker, "same"), ker, "same")
    fade = int(4 * SR)
    for ch in (L, R):
        ch[:fade] *= np.linspace(0, 1, fade); ch[-fade:] *= np.linspace(1, 0, fade)
    st = np.stack([L, R], 1)
    st = (st / np.abs(st).max() * 0.7 * 32767).astype("<i2")
    p = subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "s16le", "-ar", str(SR), "-ac", "2", "-i", "-",
                        "-af", "loudnorm=I=-20:TP=-2", a.out], input=st.tobytes())
    sys.exit(p.returncode)


if __name__ == "__main__":
    main()
