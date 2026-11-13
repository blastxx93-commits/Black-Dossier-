#!/usr/bin/env python3
"""Sound-effect kit of the Era das Feras channel: synthesized, deterministic, no licences to worry about.

Writes <dir>/sfx/<name>.wav (48 kHz stereo). Transitions rotate between several whooshes so the ear never
hears the same one twice in a row; the round/verdict/score cards each have their own signature sound.

    whoosh_a / whoosh_b / whoosh_c / whoosh_low   four different swooshes (length, pitch, stereo pan sweep)
    swipe       short bright swish (slides)          whip      very fast air-cut (whip pans)
    riser       rising noise + tone, 1.6 s (before reveals)   reverse   reversed swell into a cut
    impact      deep cinematic boom (round cards, VS)        thud      short low thump (stamps, verdicts)
    bell        boxing-ring bell (round start)       tick      UI tick (score counting)
    shutter     camera shutter (black & white freeze)        stinger   dark brass-like chord hit (defeat)
    win         bright rising two-note hit (tiger wins)      heartbeat two beats (tension before verdict)
    growl       low rumbling growl (beast reveal)    snow      soft crunch of snow (atmosphere)

Usage: python3 engine/feras_audio.py <dir>
"""
import os, sys, wave
import numpy as np

SR = 48000
rng = np.random.default_rng(7)


def save(path, x, pan=None, peak=0.9):
    x = x / (np.abs(x).max() + 1e-9) * peak
    if pan is None:
        st = np.stack([x, x], 1)
    else:   # pan: array -1..1 over time (stereo movement)
        l, r = np.sqrt((1 - pan) / 2), np.sqrt((1 + pan) / 2)
        st = np.stack([x * l, x * r], 1) * 1.3
    st = np.clip(st, -1, 1)
    w = wave.open(path, "wb")
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((st * 32767).astype(np.int16).tobytes()); w.close()


def t_(d):
    return np.arange(int(SR * d)) / SR


def bandnoise(n, lo_a, hi_a):
    """Noise through a time-varying one-pole low-pass (coefficient goes lo_a -> hi_a -> lo_a)."""
    x = rng.standard_normal(n)
    a = lo_a + (hi_a - lo_a) * np.sin(np.pi * np.arange(n) / n) ** 2
    y = np.empty(n); s = 0.0
    for i in range(n):
        s += a[i] * (x[i] - s); y[i] = s
    return y


def hp(x, a=0.5):
    y = np.empty_like(x); s = 0.0
    for i, v in enumerate(x):
        s += a * (v - s); y[i] = v - s
    return y


def whoosh(d, lo, hi, shape=1.5, pan=(-0.8, 0.8)):
    t = t_(d); n = len(t)
    env = np.sin(np.pi * t / d) ** shape
    return bandnoise(n, lo, hi) * env, np.linspace(pan[0], pan[1], n)


def boom(d=1.6, f0=42, drop=40):
    t = t_(d)
    ph = 2 * np.pi * (f0 * t + drop * (1 - np.exp(-t * 18)) / 18)
    body = np.sin(ph) * np.exp(-t * 2.6)
    crack = bandnoise(len(t), 0.05, 0.6) * np.exp(-t * 35)
    return body + 0.45 * crack


def tone(f, d, decay, harm=(1, 0.5, 0.25)):
    t = t_(d)
    return sum(a * np.sin(2 * np.pi * f * (k + 1) * t) for k, a in enumerate(harm)) * np.exp(-t * decay)


def main(out):
    d = os.path.join(out, "sfx"); os.makedirs(d, exist_ok=True)
    w = lambda name, x, pan=None, peak=0.9: save(os.path.join(d, name + ".wav"), x, pan, peak)
    x, p = whoosh(0.75, 0.01, 0.22); w("whoosh_a", x, p)
    x, p = whoosh(0.55, 0.02, 0.35, 1.2, (0.8, -0.8)); w("whoosh_b", x, p)
    x, p = whoosh(1.0, 0.008, 0.14, 2.0, (-0.5, 0.5)); w("whoosh_c", x, p)
    x, p = whoosh(0.9, 0.004, 0.06, 1.8, (0, 0)); w("whoosh_low", x + 0.3 * np.sin(2 * np.pi * 70 * t_(0.9)) * np.sin(np.pi * t_(0.9) / 0.9) ** 2)
    x, p = whoosh(0.28, 0.08, 0.7, 1.0, (-1, 1)); w("swipe", hp(x, 0.3), p, 0.8)
    x, p = whoosh(0.18, 0.15, 0.9, 0.8, (1, -1)); w("whip", hp(x, 0.2), p, 0.8)
    # riser: noise opening up + a sine gliding up an octave, cut at the top
    t = t_(1.6); n = len(t); k = t / 1.6
    a = 0.005 + 0.4 * k ** 3
    y = np.empty(n); s = 0.0; nz = rng.standard_normal(n)
    for i in range(n):
        s += a[i] * (nz[i] - s); y[i] = s
    w("riser", (y * k ** 2 + 0.25 * np.sin(2 * np.pi * (110 * t + 55 * t * t / 1.6)) * k ** 2) * np.minimum(1, (1.6 - t) / 0.02))
    w("reverse", (bandnoise(int(SR * 1.2), 0.01, 0.3) * (t_(1.2) / 1.2) ** 3 + 0.4 * boom(1.2)[::-1]))
    w("impact", boom())
    w("thud", boom(0.5, 60, 25) * np.exp(-t_(0.5) * 6), peak=0.8)
    bell = tone(1180, 1.8, 2.2, (1, 0.6, 0.35, 0.2)) + tone(1590, 1.8, 2.8, (0.6, 0.3))
    w("bell", bell + np.concatenate([np.zeros(int(SR * 0.22)), bell[:-int(SR * 0.22)]]) * 0.8, peak=0.75)
    w("tick", tone(2400, 0.05, 90, (1,)) + 0.4 * bandnoise(int(SR * 0.05), 0.4, 0.9) * np.exp(-t_(0.05) * 120), peak=0.6)
    sh = bandnoise(int(SR * 0.09), 0.3, 0.9) * np.exp(-t_(0.09) * 50)
    w("shutter", np.concatenate([sh, np.zeros(int(SR * 0.05)), sh * 0.7]), peak=0.7)
    t = t_(1.8); chord = sum(np.sign(np.sin(2 * np.pi * f * t)) * 0.3 + np.sin(2 * np.pi * f * t) for f in (55, 65.4, 82.4, 110))
    y = np.empty_like(chord); s = 0.0
    for i, v in enumerate(chord):
        s += 0.04 * (v - s); y[i] = s
    w("stinger", y * np.exp(-t * 1.6) * np.minimum(1, t / 0.01) + 0.6 * boom(1.8))
    n1, n2 = tone(523, 0.9, 3, (1, 0.4, 0.2)), tone(784, 1.2, 2.5, (1, 0.4, 0.2))
    win = np.zeros(int(SR * 1.4)); win[:len(n1)] += n1; win[int(SR * 0.16):int(SR * 0.16) + len(n2)] += n2
    w("win", win + 0.5 * np.concatenate([boom(0.6, 70, 20), np.zeros(len(win) - int(SR * 0.6))]), peak=0.75)
    hb = boom(0.35, 48, 30) * np.exp(-t_(0.35) * 9)
    beat = np.zeros(int(SR * 1.5))
    for at, g in ((0, 1), (0.28, 0.7), (0.8, 1), (1.08, 0.7)):
        i = int(at * SR); beat[i:i + len(hb)] += hb[:len(beat) - i] * g
    w("heartbeat", beat, peak=0.8)
    t = t_(1.4); mod = 1 + 0.6 * np.sin(2 * np.pi * 11 * t) * rng.uniform(0.7, 1, len(t))
    gr = bandnoise(len(t), 0.004, 0.02) * mod + 0.5 * np.sin(2 * np.pi * (62 + 6 * np.sin(2 * np.pi * 3 * t)) * t)
    w("growl", gr * np.sin(np.pi * t / 1.4) ** 0.8)
    sn = np.zeros(int(SR * 0.9))
    for at in (0.0, 0.42):
        i = int(at * SR); c = hp(bandnoise(int(SR * 0.3), 0.1, 0.5), 0.4) * np.exp(-t_(0.3) * 14)
        sn[i:i + len(c)] += c
    w("snow", sn, peak=0.5)
    print(f"kit de efeitos em {d}: {sorted(os.listdir(d))}")


if __name__ == "__main__":
    main(sys.argv[1])
