#!/usr/bin/env python3
"""Narration cleanup + quality check.

clean(): removes background noise, hum and echo/reverb tails from a TTS file and evens out the level.
check(): listens to the cleaned file (faster-whisper) and compares it with the script, word by word.
    Flags: skipped/added/garbled words, repeated phrases (TTS "stutter"), long silences, clipping,
    speech that is too fast/slow, and words cut at the start or end of the file.

Used by agent/tts.py (automatic re-take of bad chapters). Standalone:
    python3 agent/audio_qa.py <audio_dir> <narration_txt_dir> --lang it [--report qa.md]
"""
import argparse, difflib, glob, json, os, re, shutil, subprocess, unicodedata

# Filter chain (order matters):
#  highpass/lowpass  cut rumble and hiss outside the voice band
#  afftdn            spectral noise reduction, noise floor tracked over the whole file
#  agate             soft downward expander: shortens echo/reverb tails between words without chopping them
#  deesser           tames harsh "s" sounds that TTS sometimes exaggerates
#  acompressor       light leveling so no phrase jumps out
#  alimiter          hard ceiling: no clipping
CLEAN_CHAIN = ("highpass=f=70,lowpass=f=15000,"
               "afftdn=nr=14:nf=-48:tn=1,"
               "agate=threshold=0.015:ratio=2.5:range=0.12:attack=4:release=180,"
               "deesser=i=0.35,"
               "acompressor=threshold=-20dB:ratio=2.5:attack=8:release=200:makeup=2,"
               "alimiter=limit=0.89:level=false")

MAX_ERR = 0.06        # > 6% of script words wrong -> re-take
MAX_RUN = 3           # 3+ consecutive words missing/added/garbled -> re-take
MAX_SILENCE = 1.6     # seconds of dead air in the middle of a chapter
WPM_RANGE = (120, 205)


def ffmpeg():
    exe = shutil.which("ffmpeg")
    if exe:
        return exe
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()


def clean(src, dst):
    subprocess.run([ffmpeg(), "-v", "error", "-y", "-i", src, "-af", CLEAN_CHAIN, "-ar", "44100", dst], check=True)


# ---------- text normalization ----------
def _num_words(tok, lang):
    try:
        from num2words import num2words
        return num2words(int(tok), lang=lang).replace("-", " ").split()
    except Exception:
        return [tok]


def norm_words(text, lang):
    text = unicodedata.normalize("NFKD", text.lower())
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = re.sub(r"(\d)[.,](?=\d{3}\b)", r"\1", text)          # 1.000 -> 1000
    text = re.sub(r"[’'`]", " ", text)                          # l'arma -> l arma
    out = []
    for tok in re.findall(r"[a-z]+|\d+", text):
        out.extend(_num_words(tok, lang) if tok.isdigit() else [tok])
    # glue number words ("mille novecento sedici" vs "millenovecentosedici") by joining runs later in compare
    return out


def _squash(words):
    """Join everything into one string per word list for a char-level fallback."""
    return "".join(words)


# ---------- audio measurements ----------
def silences(path, min_len=MAX_SILENCE):
    r = subprocess.run([ffmpeg(), "-v", "info", "-i", path, "-af", f"silencedetect=n=-42dB:d={min_len}", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", r)]
    ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", r)]
    return list(zip(starts, ends))


def edge_silence(path, dur):
    """Seconds of quiet (< -45 dB) at the start and end of the file. Whisper timestamps are not precise enough."""
    r = subprocess.run([ffmpeg(), "-v", "info", "-i", path, "-af", "silencedetect=n=-45dB:d=0.01", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    st = [float(x) for x in re.findall(r"silence_start: ([-\d.]+)", r)]
    en = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", r)]
    lead = en[0] if st and st[0] <= 0.005 and en else 0.0
    tail = 0.0
    if st and (len(en) < len(st) or en[-1] >= dur - 0.02):   # trailing silence runs to the end of the file
        tail = dur - st[-1]
    return lead, tail


def stats(path):
    r = subprocess.run([ffmpeg(), "-v", "info", "-i", path, "-af", "astats=metadata=0,ebur128", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    peak = re.findall(r"Peak level dB: ([-\d.inf]+)", r)
    dur = re.findall(r"time=(\d+):(\d+):([\d.]+)", r)
    lufs = re.findall(r"I:\s+([-\d.]+) LUFS", r)
    d = 0.0
    if dur:
        h, m, s = dur[-1]
        d = int(h) * 3600 + int(m) * 60 + float(s)
    return {"peak_db": float(peak[-1]) if peak and peak[-1] not in ("-inf",) else -99.0,
            "duration": d, "lufs": float(lufs[-1]) if lufs else None}


# ---------- listening ----------
_MODEL = None


def model(name="medium"):
    global _MODEL
    if _MODEL is None:
        from faster_whisper import WhisperModel
        _MODEL = WhisperModel(name, device="cpu", compute_type="int8")
    return _MODEL


def listen(path, lang):
    import numpy as np
    pcm = subprocess.run([ffmpeg(), "-v", "error", "-i", path, "-ac", "1", "-ar", "16000", "-f", "f32le", "-"],
                         check=True, capture_output=True).stdout
    audio = np.frombuffer(pcm, dtype=np.float32)
    segs, _ = model().transcribe(audio, language=lang, word_timestamps=True, beam_size=5,
                                 vad_filter=False, condition_on_previous_text=False, temperature=0)
    words = []
    for seg in segs:
        for w in seg.words or []:
            words.append({"w": w.word.strip(), "s": round(w.start, 2), "e": round(w.end, 2)})
    return words


def _fmt(t):
    return f"{int(t // 60)}:{t % 60:04.1f}"


def check(audio_path, script_text, lang):
    """Returns (ok, problems:list[str], metrics:dict, heard_words)."""
    heard = listen(audio_path, lang)
    ref = norm_words(script_text, lang)
    hyp, hyp_t = [], []
    for w in heard:
        for x in norm_words(w["w"], lang):
            hyp.append(x); hyp_t.append(w["s"])
    problems, bad, worst_run = [], 0, 0
    sm = difflib.SequenceMatcher(a=ref, b=hyp, autojunk=False)
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "equal":
            continue
        a, b = ref[i1:i2], hyp[j1:j2]
        if op == "replace" and any(x.isdigit() for x in a + b) and abs(len(a) - len(b)) <= 6:
            continue                                         # number written vs spoken: formatting, not a TTS bug
        if op == "replace" and _squash(a) == _squash(b):      # same text, split differently (numbers, elisions)
            continue
        if op == "replace" and difflib.SequenceMatcher(a=_squash(a), b=_squash(b)).ratio() > 0.8:
            continue                                         # near-identical spelling: recognizer noise, not TTS
        n = max(len(a), len(b))
        bad += n
        worst_run = max(worst_run, n)
        t = hyp_t[j1] if j1 < len(hyp_t) else (hyp_t[-1] if hyp_t else 0)
        kind = {"delete": "PULOU", "insert": "ACRESCENTOU", "replace": "TROCOU"}[op]
        problems.append(f"{_fmt(t)} {kind}: roteiro \"{' '.join(a)}\" → ouvido \"{' '.join(b)}\"")
    err = bad / max(1, len(ref))

    # TTS stutter: same 3-word phrase twice in a row in what was heard, but not in the script
    ref_txt = " ".join(ref)
    for i in range(len(hyp) - 5):
        phrase = " ".join(hyp[i:i + 3])
        if hyp[i:i + 3] == hyp[i + 3:i + 6] and f"{phrase} {phrase}" not in ref_txt:
            problems.append(f"{_fmt(hyp_t[i])} GAGUEJOU: \"{phrase}\" repetido")
            worst_run = max(worst_run, MAX_RUN)

    st = stats(audio_path)
    dur = st["duration"] or (heard[-1]["e"] if heard else 0)
    gaps = [(s, e) for s, e in silences(audio_path) if s > 0.5 and e < dur - 0.5]
    for s, e in gaps:
        problems.append(f"{_fmt(s)} SILÊNCIO de {e - s:.1f}s no meio da fala")
    wpm = len(ref) / max(dur, 1) * 60
    if not WPM_RANGE[0] <= wpm <= WPM_RANGE[1]:
        problems.append(f"VELOCIDADE estranha: {wpm:.0f} palavras/min")
    if st["peak_db"] > -0.3:
        problems.append(f"CLIPPING: pico em {st['peak_db']:.1f} dBFS")
    lead, tail = edge_silence(audio_path, dur)
    if lead < 0.01:
        problems.append("INÍCIO cortado: o áudio já começa no meio de um som")
    if tail < 0.01:
        problems.append("FINAL cortado: o áudio termina no meio de um som")

    hard = err > MAX_ERR or worst_run >= MAX_RUN or gaps or st["peak_db"] > -0.3 \
        or not WPM_RANGE[0] <= wpm <= WPM_RANGE[1]
    metrics = {"erro_pct": round(err * 100, 1), "maior_trecho_errado": worst_run, "wpm": round(wpm),
               "duracao_s": round(dur, 1), "pico_db": st["peak_db"], "lufs": st["lufs"]}
    return (not hard), problems, metrics, heard


def report_line(name, ok, problems, metrics, take):
    head = f"### {name} — {'OK' if ok else 'REPROVADO'} (tentativa {take})\n" \
           f"erro {metrics['erro_pct']}% · {metrics['wpm']} wpm · {metrics['duracao_s']}s · pico {metrics['pico_db']} dB\n"
    return head + "".join(f"- {p}\n" for p in problems[:25]) + "\n"


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("audio_dir")
    ap.add_argument("text_dir")
    ap.add_argument("--lang", default="it")
    ap.add_argument("--report", default="")
    a = ap.parse_args()
    out, fails = "# Checagem da narração\n\n", 0
    for path in sorted(glob.glob(os.path.join(a.audio_dir, "*.flac")) + glob.glob(os.path.join(a.audio_dir, "*.wav"))):
        name = os.path.splitext(os.path.basename(path))[0]
        txt = os.path.join(a.text_dir, name + ".txt")
        if not os.path.exists(txt):
            continue
        ok, probs, m, _ = check(path, open(txt).read(), a.lang)
        fails += not ok
        line = report_line(name, ok, probs, m, 1)
        print(line, flush=True)
        out += line
    if a.report:
        open(a.report, "w").write(out)
    raise SystemExit(1 if fails else 0)
