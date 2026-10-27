#!/usr/bin/env python3
"""Subtitles (.srt) from the script + word timings, matching the rendered episode timeline.

Usage: python3 subtitles.py episode.json <script_dir> out.srt
Uses the exact script text (correct spelling of names), timed by the aligned narration.
"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cues import Chapter, norm

MAX_CHARS = 42      # per line
MAX_LINES = 2
MAX_DUR = 6.0


def fmt(t):
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def blocks(words):
    """Split a chapter's (word, start) list into subtitle blocks.
    Prefer sentence ends; when a block gets too long, cut at its last comma instead of mid-clause."""
    out, cur = [], []
    limit = MAX_CHARS * MAX_LINES - 6
    for i, (w, t) in enumerate(words):
        cur.append((w, t))
        text = " ".join(x for x, _ in cur)
        heading = re.match(r"^CHAPTER$", cur[0][0]) and len(cur) <= 3   # keep "CHAPTER FIVE. Title" together
        if len(text) > limit or t - cur[0][1] > MAX_DUR:
            # cut at the comma nearest the middle; without commas, before the newest word
            commas = [k for k, (x, _) in enumerate(cur[:-1]) if re.search(r"[,;:]$", x) and k >= 2]
            mid = len(cur) / 2
            k = min(commas, key=lambda k: abs(k + 1 - mid)) + 1 if commas else len(cur) - 1
            out.append(cur[:k]); cur = cur[k:]
            text = " ".join(x for x, _ in cur)
        if cur and re.search(r"([.?!]|\.\.\.)$", w) and not heading:
            out.append(cur); cur = []
    if cur:
        out.append(cur)
    return [b for b in out if b]


def two_lines(text):
    if len(text) <= MAX_CHARS:
        return text
    words = text.split()
    best, best_d = text, 1e9
    for k in range(1, len(words)):
        a, b = " ".join(words[:k]), " ".join(words[k:])
        if len(a) <= MAX_CHARS and len(b) <= MAX_CHARS and abs(len(a) - len(b)) < best_d:
            best, best_d = a + "\n" + b, abs(len(a) - len(b))
    if best == text:  # no split keeps both lines under the limit: take the most balanced one
        k = min(range(1, len(words)), key=lambda k: abs(len(" ".join(words[:k])) - len(" ".join(words[k:]))))
        best = " ".join(words[:k]) + "\n" + " ".join(words[k:])
    return best


def main(ep_path, script_dir, out_path):
    ep = json.load(open(ep_path))
    base = os.path.dirname(os.path.abspath(ep_path))
    offset, n, lines = 0.0, 0, []
    for chap in ep["chapters"]:
        name = os.path.splitext(os.path.basename(chap["audio"]))[0]
        c = Chapter(name, os.path.join(script_dir, f"{name}.txt"),
                    os.path.join(base, "a", "words", f"{name}.words.json"), os.path.join(base, chap["audio"]))
        raw = [w for w in open(os.path.join(script_dir, f"{name}.txt")).read().split() if norm(w)]
        assert len(raw) == len(c.t), name
        words_json = json.load(open(os.path.join(base, "a", "words", f"{name}.words.json")))
        speech_end = words_json[-1]["e"] if words_json else c.t[-1] + 1
        bl = blocks(list(zip(raw, c.t)))
        voice_start = words_json[0]["s"] if words_json and words_json[0]["e"] - words_json[0]["s"] > 0.02 else 0
        if voice_start < 0.3:  # recognizers often stamp the first word at 0: use the real onset
            import subprocess
            r = subprocess.run(["ffmpeg", "-hide_banner", "-i", os.path.join(base, chap["audio"]), "-t", "8",
                                "-af", "silencedetect=noise=-38dB:d=0.3", "-f", "null", "-"], capture_output=True, text=True).stderr
            m = re.search(r"silence_start: -?0[0-9.e-]*\s.*?silence_end: ([0-9.]+)", r, re.S)
            voice_start = float(m.group(1)) if m else 0
        lead = chap.get("lead_in", 0)
        starts = [max(b[0][1], voice_start - 0.1) if k == 0 else b[0][1] for k, b in enumerate(bl)]
        for k, b in enumerate(bl):
            start = starts[k]
            nxt = starts[k + 1] - 0.05 if k + 1 < len(bl) else speech_end + 0.3
            end = min(max(nxt, start + 0.8), start + MAX_DUR + 1.5)
            if k + 1 < len(bl):
                end = min(end, nxt)
            text = " ".join(w for w, _ in b)
            # chapter headings are read aloud: show them in title case, not shouted
            if re.match(r"^CHAPTER\b", text):
                text = text.title()
            n += 1
            lines.append(f"{n}\n{fmt(offset + lead + start)} --> {fmt(offset + lead + end)}\n{two_lines(text)}\n")
        offset += sum(s["dur"] for s in chap["shots"])
    open(out_path, "w").write("\n".join(lines))
    print(f"{n} legendas -> {out_path}")


if __name__ == "__main__":
    main(*sys.argv[1:4])
