#!/usr/bin/env python3
"""Narration agent (Fish Audio).

Reads episodes/<ep>/narration/<chapter>.txt and synthesizes one audio file per chapter
with the channel voice. Writes:
    <out>/<ep>/narration_audio/<chapter>.flac   full quality, used by the editor
    <out>/<ep>/audio/<chapter>.mp3              small mono copy, used by the transcription

Needs env FISH_API_KEY and FISH_VOICE_ID (GitHub secrets); optional FISH_MODEL (default s2.1-pro).
Every chapter is cleaned (noise/echo, agent/audio_qa.py). With --qa it is also listened to and compared
with the script; a chapter with skipped/garbled words, stutter, dead air or clipping is re-generated
(up to --takes times) and the best take is kept. Report: <out>/<ep>/qa_narracao.md

Usage: python3 agent/tts.py ep02-valachi [--out assets_out] [--only ch00_hook,ch03] [--speed 1.0] [--qa --lang it]
"""
import argparse, glob, os, shutil, subprocess, sys, time
import requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import audio_qa


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
    ap.add_argument("--qa", action="store_true", help="listen to every chapter and re-take the bad ones")
    ap.add_argument("--lang", default="en")
    ap.add_argument("--takes", type=int, default=3)
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
    report, failed = "# Checagem da narração\n\n", []
    for t in texts:
        name = os.path.splitext(os.path.basename(t))[0]
        if only and name not in only:
            continue
        text = open(t).read().strip()
        final = os.path.join(full, name + ".flac")
        best = None  # (score, take_path, ok, problems, metrics)
        for take in range(1, (a.takes if a.qa else 1) + 1):
            wav = synth(key, voice, model, text, a.speed)
            raw = os.path.join(full, f"{name}.raw.wav")
            open(raw, "wb").write(wav)
            cand = os.path.join(full, f"{name}.take{take}.flac")
            audio_qa.clean(raw, cand)
            os.remove(raw)
            if not a.qa:
                best = (0, cand, True, [], None)
                break
            ok, probs, m, _ = audio_qa.check(cand, text, a.lang)
            report += audio_qa.report_line(name, ok, probs, m, take)
            print(f"{name} tentativa {take}: {'OK' if ok else 'REPROVADO'} · erro {m['erro_pct']}% · "
                  f"{len(probs)} apontamentos", flush=True)
            score = m["erro_pct"] + 5 * len(probs)
            if best is None or score < best[0]:
                if best:
                    os.remove(best[1])
                best = (score, cand, ok, probs, m)
            else:
                os.remove(cand)
            if ok:
                break
        os.replace(best[1], final)
        if not best[2]:
            failed.append(name)
        subprocess.run([ff, "-v", "error", "-y", "-i", final, "-ac", "1", "-ar", "16000", "-c:a", "libmp3lame",
                        "-b:a", "48k", os.path.join(small, name + ".mp3")], check=True)
        print(f"{name}: {len(text.split())} palavras, {audio_qa.stats(final)['duration']:.0f}s", flush=True)
    if a.qa:
        report += ("\n**Capítulos ainda com defeito depois de todas as tentativas:** " + ", ".join(failed) + "\n") \
            if failed else "\n**Todos os capítulos aprovados.**\n"
        open(os.path.join(a.out, a.episode, "qa_narracao.md"), "w").write(report)
        if os.environ.get("GITHUB_STEP_SUMMARY"):
            open(os.environ["GITHUB_STEP_SUMMARY"], "a").write(report)
        if failed:
            sys.exit(f"Narração com defeito em: {', '.join(failed)} (ver qa_narracao.md)")

if __name__ == "__main__":
    main()
