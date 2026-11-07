#!/usr/bin/env python3
"""Finds narration chapters where the TTS voice glitched: a long stretch with sound but no recognizable words.

Fish Audio sometimes produces 20–40 s of mumbling/noise inside a chapter. The transcription then shows a big gap
between two words. Prints the bad chapter names, comma-separated (empty when all is fine).
Usage: python3 agent/check_narration.py <words_dir> [--max-gap 6]
"""
import glob, json, os, sys

d = sys.argv[1]
max_gap = float(sys.argv[sys.argv.index("--max-gap") + 1]) if "--max-gap" in sys.argv else 6.0
bad = []
for f in sorted(glob.glob(os.path.join(d, "*.words.json"))):
    w = json.load(open(f))
    gaps = [w[i + 1]["s"] - w[i]["e"] for i in range(len(w) - 1)]
    if w and (max(gaps or [0]) > max_gap or w[0]["s"] > max_gap):
        name = os.path.basename(f).split(".")[0]
        bad.append(name)
        sys.stderr.write(f"{name}: trecho de {max(gaps or [w[0]['s']]):.0f}s sem fala reconhecível\n")
print(",".join(bad))
