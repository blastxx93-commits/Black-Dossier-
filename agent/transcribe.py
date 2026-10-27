#!/usr/bin/env python3
"""Word-level timestamps for each narration file (faster-whisper).

Usage: python3 agent/transcribe.py <audio_dir> <out_dir> [--model small.en]
Writes <out_dir>/<name>.words.json: [{"w": "Apalachin", "s": 12.34, "e": 12.91}, ...]
"""
import argparse, glob, json, os
from faster_whisper import WhisperModel

ap = argparse.ArgumentParser()
ap.add_argument("audio_dir")
ap.add_argument("out_dir")
ap.add_argument("--model", default="small.en")
a = ap.parse_args()
os.makedirs(a.out_dir, exist_ok=True)
model = WhisperModel(a.model, device="cpu", compute_type="int8")
for path in sorted(glob.glob(os.path.join(a.audio_dir, "*.mp3")) + glob.glob(os.path.join(a.audio_dir, "*.wav"))):
    name = os.path.splitext(os.path.basename(path))[0]
    segs, info = model.transcribe(path, language="en", word_timestamps=True, beam_size=5,
                                  vad_filter=False, condition_on_previous_text=True)
    words = []
    for seg in segs:
        for w in seg.words or []:
            words.append({"w": w.word.strip(), "s": round(w.start, 3), "e": round(w.end, 3)})
    json.dump(words, open(os.path.join(a.out_dir, f"{name}.words.json"), "w"), indent=0)
    print(f"{name}: {len(words)} palavras, {info.duration:.1f}s", flush=True)
