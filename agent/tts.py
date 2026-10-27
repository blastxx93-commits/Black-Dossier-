#!/usr/bin/env python3
"""Narration agent (Fish Audio).

Reads episodes/<ep>/narration/<chapter>.txt and synthesizes one audio file per chapter
with the channel voice. Writes:
    <out>/<ep>/narration_audio/<chapter>.flac   full quality, used by the editor
    <out>/<ep>/audio/<chapter>.mp3              small mono copy, used by the transcription

Needs env FISH_API_KEY and FISH_VOICE_ID (GitHub secrets); optional FISH_MODEL (default s2.1-pro).
Usage: python3 agent/tts.py ep02-valachi [--out assets_out] [--only ch00_hook,ch03] [--speed 1.0]
"""
import argparse, glob, os, shutil, subprocess, sys, time
import requests


def ffmpeg():
    exe = shutil.which("ffmpeg")
    if exe:
        return exe
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()


def synth(key, voice, model, text, speed):
    body = {"text": text, "reference_id": voice, "format": "wav", "sample_rate": 44100,
            "normalize": True, "latency": "normal", "chunk_length": 300}
    if speed != 1.0:
        body["prosody"] = {"speed": speed}
    for k in range(3):
        r = requests.post("https://api.fish.audio/v1/tts", json=body, timeout=600, headers={
            "Authorization": f"Bearer {key}", "Content-Type": "application/json", "model": model})
        if r.status_code == 200 and r.content[:4] == b"RIFF":
            return r.content
        if r.status_code in (429, 500, 502, 503):
            time.sleep(20 * (k + 1)); continue
        raise RuntimeError(f"Fish Audio {r.status_code}: {r.text[:300]}")
    raise RuntimeError("Fish Audio não respondeu depois de 3 tentativas")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("episode")
    ap.add_argument("--out", default="assets_out")
    ap.add_argument("--only", default="")
    ap.add_argument("--speed", type=float, default=1.0)
    a = ap.parse_args()
    key, voice = os.environ.get("FISH_API_KEY", "").strip(), os.environ.get("FISH_VOICE_ID", "").strip()
    if not key or not voice:
        sys.exit("FISH_API_KEY e FISH_VOICE_ID precisam estar nos segredos do GitHub.")
    model = os.environ.get("FISH_MODEL", "").strip() or "s2.1-pro"
    only = {x for x in a.only.split(",") if x}
    texts = sorted(glob.glob(os.path.join("episodes", a.episode, "narration", "*.txt")))
    if not texts:
        sys.exit(f"Nenhum roteiro em episodes/{a.episode}/narration/")
    full = os.path.join(a.out, a.episode, "narration_audio")
    small = os.path.join(a.out, a.episode, "audio")
    os.makedirs(full, exist_ok=True); os.makedirs(small, exist_ok=True)
    ff = ffmpeg()
    for t in texts:
        name = os.path.splitext(os.path.basename(t))[0]
        if only and name not in only:
            continue
        text = open(t).read().strip()
        wav = synth(key, voice, model, text, a.speed)
        tmp = os.path.join(full, name + ".wav")
        open(tmp, "wb").write(wav)
        subprocess.run([ff, "-v", "error", "-y", "-i", tmp, os.path.join(full, name + ".flac")], check=True)
        subprocess.run([ff, "-v", "error", "-y", "-i", tmp, "-ac", "1", "-ar", "16000", "-c:a", "libmp3lame",
                        "-b:a", "48k", os.path.join(small, name + ".mp3")], check=True)
        os.remove(tmp)
        print(f"{name}: {len(text.split())} palavras, {len(wav) / 88200:.0f}s", flush=True)


if __name__ == "__main__":
    main()
