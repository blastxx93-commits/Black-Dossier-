"""Shared shot builders for Black Dossier edits (used by episodes/*/edit/build_*.py)."""
import json, os, subprocess, sys

SFX = {"type": ("sfx/typewriter.wav", -24), "hit": ("sfx/hit.wav", -20),
       "whoosh": ("sfx/whoosh.wav", -27), "stamp": ("sfx/stamp.wav", -19)}
PHOTOS = {}  # name -> (path under a/, focus) for dossier cards; filled by each episode


def fx(name, at=0.0, extra=0):
    f, g = SFX[name]
    return {"file": f, "gain": g + extra, "at": at}


def img(path, move="in", cap=None, focus=None, **kw):
    s = {"type": "image", "src": "a/" + path, "move": move}
    if cap: s["caption"] = cap
    if focus: s["focus"] = focus
    s.update(kw)
    return s


def ai(name, move="in", **kw):
    return img("ai/" + name, move, **kw)


def vid(path, cap=None, speed=1.0, start=0, fit="blur", **kw):
    """Archival clip. Clips are short; the engine loops them if the shot is longer."""
    s = {"type": "video", "src": "a/" + path, "fit": fit, "start": start, "xfade": 0.35}
    if speed != 1.0: s["speed"] = speed
    if cap: s["caption"] = cap
    s.update(kw)
    return s


def typer(text, size=60, sound=True):
    s = {"type": "typewriter", "text": text, "size": size}
    if sound: s["sfx"] = [fx("type", 0.1)]
    return s


def say(text, size=150, hit=True):
    s = {"type": "statement", "text": text, "size": size}
    if hit: s["sfx"] = [fx("hit")]
    return s


def doc(text, stamp=None):
    s = {"type": "document", "text": text}
    if stamp: s["stamp"] = stamp
    return s


def card(num, title):
    return {"type": "chapter", "num": num, "title": title, "sfx": [fx("whoosh")]}


def subscribe(text="SUBSCRIBE", sub="New file every week"):
    """CTA card in the channel style (after the hook and at the end)."""
    return {"type": "title", "title": text, "subtitle": sub, "file": "BLACK DOSSIER", "stamp": "OPEN FILE",
            "sfx": [fx("whoosh"), fx("stamp", 0.9)]}


def black():
    return {"type": "black"}


def counter(to, label, prefix="", suffix=""):
    return {"type": "counter", "to": to, "label": label, "prefix": prefix, "suffix": suffix}


def timeline(items):
    return {"type": "timeline", "items": items}


def title(t, sub, file, stamp, **kw):
    s = {"type": "title", "title": t, "subtitle": sub, "file": file, "stamp": stamp,
         "sfx": [fx("whoosh"), fx("stamp", 0.9)]}
    s.update(kw)
    return s


def dossier(name, label="SUBJECT", stamp=None, **fields):
    s = {"type": "dossier", "name": name, "label": label,
         "fields": {k.replace("_", " "): v for k, v in fields.items()}, "sfx": [fx("whoosh")]}
    if name in PHOTOS:
        s["photo"] = "a/" + PHOTOS[name][0]
        s["focus"] = PHOTOS[name][1]
    if stamp:
        s["stamp"] = stamp
        s["sfx"].append(fx("stamp", 1.2))
    return s


def audio_dur(p):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                          "-of", "csv=p=0", p]).strip())


def check_no_repeats(ep, allow=()):
    """Rule of the channel: no image, clip or AI scene may appear twice in an episode."""
    seen, dup = {}, []
    for ci, c in enumerate(ep["chapters"]):
        for s in c["shots"]:
            for k in ("src", "photo"):
                f = s.get(k)
                if not f or f in allow:
                    continue
                if f in seen:
                    dup.append(f"{f}  (cap. {seen[f]} e cap. {ci})")
                else:
                    seen[f] = ci
    return dup


def build_episode(chapters, output, music="trilha.wav", music_gain=-21, final_fade=1.5, allow_repeat=()):
    out = {"output": output, "fps": 24,
           "music": [{"file": music, "start": 0, "gain": music_gain, "fade_in": 4, "fade_out": 5}],
           "chapters": []}
    for c in chapters:
        out["chapters"].append(c.build(audio_dur(c.audio)))
        sys.stderr.write(f"{c.name}: {len(c.cues)} planos, alinhamento {c.matched:.0%}"
                         + (f", NAO ACHEI: {c.misses}" if c.misses else "") + "\n")
    out["chapters"][-1]["shots"][-1]["fade_out"] = final_fade
    dup = check_no_repeats(out, allow_repeat)
    if dup:
        sys.exit("IMAGENS REPETIDAS (regra do canal):\n  " + "\n  ".join(dup))
    return out
