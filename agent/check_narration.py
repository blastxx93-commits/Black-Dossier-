#!/usr/bin/env python3
"""Narration QA (owner rule 19/11/2026): catch TTS glitches before editing.

Usage: python3 agent/check_narration.py <assets_ep_dir> <narration_txt_dir>
Reads <assets_ep_dir>/words/<ch>.words.json (Whisper word timings of the generated audio) and
<assets_ep_dir>/narration_audio/<ch>.* and flags, per chapter:
  * gaps   - more than MAX_GAP seconds with no recognised speech between two words (noise, babble, dead air)
  * tail   - audio running on more than MAX_TAIL seconds after the last recognised word
  * drift  - script words missing from / added to the transcript in a run of 4+ words (skipped or invented speech)
  * clip   - peaks at full scale (distortion)
Prints a report and the list of chapters to regenerate (narrate.yml with only=...). Exit code 1 if any.
"""
import difflib, glob, json, os, re, subprocess, sys, unicodedata

MAX_GAP, MAX_TAIL, MAX_RUN = 2.6, 3.0, 4


def norm(w):
    return re.sub(r"[^a-z0-9]", "", unicodedata.normalize("NFKD", w.lower()).encode("ascii", "ignore").decode())


def duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                         capture_output=True, text=True).stdout.strip()
    return float(out or 0)


def peak(path):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", path, "-af", "volumedetect", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    m = re.search(r"max_volume: (-?[\d.]+) dB", r)
    return float(m.group(1)) if m else -99


def main(ep, txt_dir):
    bad = []
    for wpath in sorted(glob.glob(os.path.join(ep, "words", "*.words.json"))):
        ch = os.path.basename(wpath).replace(".words.json", "")
        words = json.load(open(wpath))
        audio = (glob.glob(os.path.join(ep, "narration_audio", ch + ".*")) or [None])[0]
        issues = []
        for a, b in zip(words, words[1:]):
            if b["s"] - a["e"] > MAX_GAP:
                issues.append(f"gap {b['s'] - a['e']:.1f}s at {a['e']:.1f}s (after «{a['w']}»)")
        if audio:
            d = duration(audio)
            if words and d - words[-1]["e"] > MAX_TAIL:
                issues.append(f"tail {d - words[-1]['e']:.1f}s of audio after the last word")
            if peak(audio) >= -0.1:
                issues.append("clip: peaks at 0 dBFS")
        tp = os.path.join(txt_dir, ch + ".txt")
        if os.path.exists(tp):
            script = [norm(x) for x in open(tp).read().split() if norm(x)]
            heard = [norm(x["w"]) for x in words if norm(x["w"])]
            sm = difflib.SequenceMatcher(None, script, heard, autojunk=False)
            for op, i1, i2, j1, j2 in sm.get_opcodes():
                if op != "equal" and max(i2 - i1, j2 - j1) >= MAX_RUN:
                    t = words[min(j1, len(words) - 1)]["s"] if words else 0
                    issues.append(f"drift ({op}) near {t:.1f}s: script «{' '.join(script[i1:i2])[:60]}» / heard «{' '.join(heard[j1:j2])[:60]}»")
        print(f"{ch}: {'OK' if not issues else 'PROBLEM'}")
        for i in issues:
            print("   -", i)
        if issues:
            bad.append(ch)
    print("REGENERATE:", ",".join(bad) if bad else "none")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
