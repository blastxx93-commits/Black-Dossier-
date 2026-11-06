#!/usr/bin/env python3
"""Narration agent (Fish Audio or ElevenLabs).

Reads episodes/<ep>/narration/<chapter>.txt and synthesizes one audio file per chapter
with the channel voice. Writes:
    <out>/<ep>/narration_audio/<chapter>.flac   full quality, used by the editor
    <out>/<ep>/audio/<chapter>.mp3              small mono copy, used by the transcription

Provider "fish" (default): env FISH_API_KEY, FISH_VOICE_ID, optional FISH_MODEL (default s2.1-pro).
Provider "eleven": env ELEVENLABS_API_KEY, ELEVEN_VOICE_ID (default Charlie, Australian male),
optional ELEVEN_MODEL (default eleven_multilingual_v2). Long texts are sent in paragraph chunks with
request stitching (previous/next text) so the delivery stays continuous.
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


ELEVEN_FMT = ["pcm_44100"]


def mp3_to_pcm(data):
    """MP3 bytes -> raw 44.1 kHz mono s16le PCM (same layout as ElevenLabs pcm_44100)."""
    return subprocess.run([ffmpeg(), "-v", "error", "-i", "pipe:0", "-ac", "1", "-ar", "44100", "-f", "s16le", "-"],
                          input=data, capture_output=True, check=True).stdout


def eleven_synth(key, voice, model, text):
    """ElevenLabs TTS, returns 44.1 kHz 16-bit PCM WAV bytes. Splits on paragraphs (<= ~2,400 chars per call)."""
    import io, wave
    paras = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks, cur = [], ""
    for p in paras:
        if cur and len(cur) + len(p) > 2400:
            chunks.append(cur); cur = p
        else:
            cur = (cur + "\n\n" + p) if cur else p
    if cur:
        chunks.append(cur)
    pcm = b""
    for i, ch in enumerate(chunks):
        body = {"text": ch, "model_id": model,
                "voice_settings": {"stability": 0.45, "similarity_boost": 0.8, "style": 0.25, "use_speaker_boost": True}}
        if i:
            body["previous_text"] = chunks[i - 1][-1000:]
        if i + 1 < len(chunks):
            body["next_text"] = chunks[i + 1][:1000]
        for k in range(4):
            r = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{voice}?output_format={ELEVEN_FMT[0]}", json=body,
                              headers={"xi-api-key": key, "Content-Type": "application/json"}, timeout=600)
            if r.status_code == 403 and "output_format" in r.text and ELEVEN_FMT[0] != "mp3_44100_192":
                # PCM is Pro-tier only: fall back to the best MP3 the plan allows and decode it
                ELEVEN_FMT[0] = "mp3_44100_192"; continue
            if r.status_code == 200 and r.content:
                pcm += r.content if ELEVEN_FMT[0].startswith("pcm") else mp3_to_pcm(r.content); break
            if r.status_code in (429, 500, 502, 503) and k < 3:
                time.sleep(20 * (k + 1)); continue
            raise RuntimeError(f"ElevenLabs {r.status_code}: {r.text[:300]}")
    out = io.BytesIO()
    w = wave.open(out, "wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(44100); w.writeframes(pcm); w.close()
    return out.getvalue()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("episode")
    ap.add_argument("--out", default="assets_out")
    ap.add_argument("--only", default="")
    ap.add_argument("--speed", type=float, default=1.0)
    a = ap.parse_args()
    provider = os.environ.get("TTS_PROVIDER", "").strip() or "fish"
    if provider == "eleven":
        key = os.environ.get("ELEVENLABS_API_KEY", "").strip()
        voice = os.environ.get("ELEVEN_VOICE_ID", "").strip() or "IKne3meq5aSn9XLyUdCD"
        model = os.environ.get("ELEVEN_MODEL", "").strip() or "eleven_multilingual_v2"
        if not key:
            sys.exit("ELEVENLABS_API_KEY precisa estar nos segredos do GitHub.")
    else:
        key, voice = os.environ.get("FISH_API_KEY", "").strip(), os.environ.get("FISH_VOICE_ID", "").strip()
        if not key or not voice:
            sys.exit("FISH_API_KEY e FISH_VOICE_ID precisam estar nos segredos do GitHub.")
        model = os.environ.get("FISH_MODEL", "").strip() or "s2.1-pro"
    print(f"provedor: {provider}, modelo: {model}", flush=True)
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
        wav = eleven_synth(key, voice, model, text) if provider == "eleven" else synth(key, voice, model, text, a.speed)
        tmp = os.path.join(full, name + ".wav")
        open(tmp, "wb").write(wav)
        subprocess.run([ff, "-v", "error", "-y", "-i", tmp, os.path.join(full, name + ".flac")], check=True)
        subprocess.run([ff, "-v", "error", "-y", "-i", tmp, "-ac", "1", "-ar", "16000", "-c:a", "libmp3lame",
                        "-b:a", "48k", os.path.join(small, name + ".mp3")], check=True)
        os.remove(tmp)
        print(f"{name}: {len(text.split())} palavras, {len(wav) / 88200:.0f}s", flush=True)


if __name__ == "__main__":
    main()
