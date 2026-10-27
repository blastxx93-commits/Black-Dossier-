"""Cue-sheet builder: anchors every shot to a phrase of the script.

The narration script (one .txt per chapter) is aligned to the word timestamps
from agent/transcribe.py, so each shot starts exactly when its phrase is spoken.

    from cues import Chapter
    ch = Chapter("ch01", script_txt, words_json, audio_wav)
    ch.at("To understand why", image("a/ai/x.jpg"))   # starts on that phrase
    ch.at(0, chapter_card)                             # or at a time in seconds
    episode["chapters"].append(ch.build())
"""
import difflib, json, re

LEAD = 0.12  # picture lands this many seconds before the word


def norm(t):
    t = t.lower().replace("’", "'")
    return re.sub(r"[^a-z0-9']", "", t)


def tokens(text):
    return [norm(w) for w in text.split() if norm(w)]


class Chapter:
    def __init__(self, name, script_path, words_path, audio_path, tail=0.8):
        self.name, self.audio, self.tail = name, audio_path, tail
        self.script = tokens(open(script_path).read())
        words = json.load(open(words_path))
        # zero-length words are the recognizer squeezing skipped speech: don't trust their times
        wtok = [norm(w["w"]) if w["e"] - w["s"] > 0.02 else "\x00" for w in words]
        self.end_time = words[-1]["e"] if words else 0
        # map script word index -> start time through sequence alignment
        sm = difflib.SequenceMatcher(None, self.script, wtok, autojunk=False)
        t = [None] * len(self.script)
        for a, b, n in sm.get_matching_blocks():
            for k in range(n):
                t[a + k] = words[b + k]["s"]
        known = [i for i, v in enumerate(t) if v is not None]
        self.matched = len(known) / max(1, len(self.script))
        for i in range(len(t)):  # interpolate words the recognizer heard differently
            if t[i] is None:
                lo = max([k for k in known if k < i], default=None)
                hi = min([k for k in known if k > i], default=None)
                if lo is None:
                    t[i] = 0.0
                elif hi is None:
                    t[i] = t[lo]
                else:
                    t[i] = t[lo] + (t[hi] - t[lo]) * (i - lo) / (hi - lo)
        self.t = t
        self.cursor = 0
        self.cues = []
        self.misses = []

    def find(self, phrase):
        p = tokens(phrase)
        for i in range(self.cursor, len(self.script) - len(p) + 1):
            if self.script[i:i + len(p)] == p:
                self.cursor = i + 1
                return self.t[i]
        self.misses.append(phrase)
        return None

    def at(self, when, shot):
        sec = when if isinstance(when, (int, float)) else self.find(when)
        if sec is None:
            return self
        if not isinstance(when, (int, float)):
            sec = max(0.0, sec - LEAD)
        self.cues.append((sec, shot))
        return self

    def build(self, audio_dur):
        cues = sorted(self.cues, key=lambda c: c[0])
        total = audio_dur + self.tail
        shots = []
        for k, (sec, shot) in enumerate(cues):
            nxt = cues[k + 1][0] if k + 1 < len(cues) else total
            s = dict(shot)
            s["dur"] = round(max(0.3, nxt - sec), 3)
            s["fixed"] = k + 1 < len(cues)
            shots.append(s)
        return {"audio": self.audio, "lead_in": 0, "tail": self.tail, "shots": shots}
