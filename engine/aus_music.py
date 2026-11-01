#!/usr/bin/env python3
"""Synthesized, copyright-free background music with several styles (channel rule 01/11/2026: vary the music).

Each style builds a ~3-minute track made of 4 different sections (different chord progressions, instrument
layers and drum patterns), so a 16-minute video doesn't loop the same 40 seconds. Deterministic per seed.

    python3 engine/aus_music.py <out.wav> <style> [seed]
Styles: dark (original channel bed), drive, tension, pulse, doc
"""
import sys, wave
import numpy as np

SR = 48000
try:
    from scipy.signal import lfilter
except Exception:  # pragma: no cover
    lfilter = None


def lp(x, a):
    if lfilter is not None:
        return lfilter([a], [1, a - 1], x)
    y = np.empty_like(x); s = 0.0
    for i, v in enumerate(x):
        s += a * (v - s); y[i] = s
    return y


def hp(x, a):
    return x - lp(x, a)


def f(m):
    return 440 * 2 ** ((m - 69) / 12)


STYLES = {
    # bpm, root midi, chord sets per section (semitone offsets of triads from root), layers
    "dark":    dict(bpm=96,  root=57, minor=True, sections=[[0, -4, -9, -2], [0, -2, -4, -5], [-4, -9, -2, 0], [0, -5, -4, -2]],
                    pad=1.0, bass="pulse8", arp=0.0, kick="four", hat="16", pluck=0.0),
    "drive":   dict(bpm=118, root=52, minor=True, sections=[[0, -4, 3, -2], [0, 3, -2, -4], [-4, 3, -2, 0], [0, -2, -4, -4]],
                    pad=0.6, bass="octave", arp=0.5, kick="four", hat="off8", pluck=0.0),
    "tension": dict(bpm=84,  root=50, minor=True, sections=[[0, 0, 1, 0], [0, -2, 1, -2], [3, 1, 0, -2], [0, 1, 3, 1]],
                    pad=1.1, bass="drone", arp=0.0, kick="half", hat="8", pluck=0.35),
    "pulse":   dict(bpm=108, root=55, minor=False, sections=[[0, -3, 5, 7], [-3, 5, 0, 7], [5, 7, -3, 0], [0, 7, -3, 5]],
                    pad=0.7, bass="pulse8", arp=0.45, kick="four", hat="16", pluck=0.0),
    "doc":     dict(bpm=76,  root=53, minor=True, sections=[[0, -4, -9, -5], [-4, -9, -5, 0], [0, -2, -4, -5], [-9, -5, -4, 0]],
                    pad=0.9, bass="soft", arp=0.0, kick="sparse", hat="none", pluck=0.55),
}


def triad(root, minor):
    return (root, root + (3 if minor else 4), root + 7)


def build(style, seed=1):
    S = STYLES[style]
    rng = np.random.default_rng(seed)
    beat = 60 / S["bpm"]; bar = 4 * beat; bars_per_sec = 20
    nsec = len(S["sections"]); L = int(SR * bar * bars_per_sec * nsec)
    pad = np.zeros(L); bass = np.zeros(L); hat = np.zeros(L); kick = np.zeros(L); arp = np.zeros(L); pl = np.zeros(L)
    detune = rng.uniform(0.05, 0.12)
    for si, sec in enumerate(S["sections"]):
        # each section adds/drops layers for variety
        layer = [(1, 0, 1, 1), (1, 1, 1, 1), (0.8, 1, 0, 1), (1, 1, 1, 0.6)][si % 4]   # pad, arp/pluck, hats, kick scale
        for b in range(bars_per_sec):
            gb = si * bars_per_sec + b
            off = sec[b % 4]
            m0 = S["root"] + off
            ch = triad(m0, S["minor"] if style != "pulse" else (off in (-3,)))
            s0 = int(gb * bar * SR); s1 = int((gb + 1) * bar * SR); tt = np.arange(s1 - s0) / SR
            env = np.minimum(1, tt / 0.7) * np.minimum(1, (tt[-1] - tt + 0.05) / 0.5)
            for m in ch:
                for det in (-detune, detune):
                    pad[s0:s1] += np.sin(2 * np.pi * f(m) * (1 + det / 100) * tt) * env * 0.16 * S["pad"] * layer[0]
            # bass
            if S["bass"] == "drone":
                bass[s0:s1] += np.sin(2 * np.pi * f(ch[0] - 24) * tt) * env * 0.5
            elif S["bass"] == "soft":
                for k in range(2):
                    a0 = s0 + int(k * 2 * beat * SR); a1 = min(s1, a0 + int(2 * beat * SR)); tb = np.arange(a1 - a0) / SR
                    bass[a0:a1] += np.sin(2 * np.pi * f(ch[0] - 24) * tb) * np.exp(-tb * 1.5) * 0.5
            else:
                for k in range(8):
                    a0 = s0 + int(k * beat / 2 * SR); a1 = min(s1, a0 + int(beat / 2 * SR)); tb = np.arange(a1 - a0) / SR
                    note = ch[0] - 24 + (12 if (S["bass"] == "octave" and k % 2) else 0)
                    bass[a0:a1] += np.sign(np.sin(2 * np.pi * f(note) * tb)) * np.exp(-tb * 9) * 0.32
            # arpeggio
            if S["arp"] and layer[1]:
                seq = [ch[0] + 12, ch[1] + 12, ch[2] + 12, ch[1] + 12]
                for k in range(16):
                    a0 = s0 + int(k * beat / 4 * SR); a1 = min(s1, a0 + int(beat / 4 * SR)); tb = np.arange(a1 - a0) / SR
                    arp[a0:a1] += np.sign(np.sin(2 * np.pi * f(seq[k % 4]) * tb)) * np.exp(-tb * 14) * 0.07 * S["arp"]
            # piano-like pluck melody
            if S["pluck"] and layer[1]:
                for k in range(4):
                    if rng.random() < 0.7:
                        a0 = s0 + int(k * beat * SR); a1 = min(L, a0 + int(1.6 * SR)); tb = np.arange(a1 - a0) / SR
                        n = ch[rng.integers(0, 3)] + 12 * rng.integers(1, 3)
                        pl[a0:a1] += (np.sin(2 * np.pi * f(n) * tb) + 0.3 * np.sin(4 * np.pi * f(n) * tb)) * np.exp(-tb * 3) * 0.18 * S["pluck"]
            # hats
            hs = {"16": (16, 4), "8": (8, 2), "off8": (8, 2), "none": (0, 1)}[S["hat"]]
            for k in range(hs[0]):
                if S["hat"] == "off8" and k % 2 == 0:
                    continue
                a0 = s0 + int(k * bar / hs[0] * SR); a1 = min(s1, a0 + int(0.04 * SR))
                hat[a0:a1] += rng.standard_normal(a1 - a0) * np.exp(-np.arange(a1 - a0) / SR * 120) * (0.12 if k % 2 else 0.06) * layer[2]
            # kick
            ks = {"four": [0, 1, 2, 3], "half": [0, 2], "sparse": [0] if b % 2 == 0 else []}[S["kick"]]
            for k in ks:
                a0 = s0 + int(k * beat * SR); tk = np.arange(int(0.35 * SR)) / SR
                seg = np.sin(2 * np.pi * (50 * tk + 60 * (1 - np.exp(-tk * 30)) / 30)) * np.exp(-tk * 9)
                kick[a0:a0 + len(seg)] += seg[:L - a0] * 0.6 * layer[3]
    mix = lp(pad, 0.12) * 0.9 + lp(bass, 0.08) + hp(hat, 0.5) + kick + lp(arp, 0.3) + pl
    # 2 s crossfade-friendly ends (render loops the track)
    return mix


def save(path, x):
    x = x / (np.sqrt((x ** 2).mean()) + 1e-9) * 0.16      # same loudness for every style (the original bed's level)
    x = np.clip(x, -0.95, 0.95)
    x = np.stack([x, x], 1)
    w = wave.open(path, "wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((x * 32767).astype(np.int16).tobytes()); w.close()


if __name__ == "__main__":
    out, style = sys.argv[1], sys.argv[2]
    seed = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    save(out, build(style, seed))
    print(f"trilha '{style}' (seed {seed}) -> {out}")
