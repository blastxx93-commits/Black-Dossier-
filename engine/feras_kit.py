"""Edit kit of the Era das Feras channel (episodes/fe*/edit/build_*.py), on top of aus_kit.py.

Adds the channel's layouts (render_feras.py) as one-line builders and, at the end, the cutting rhythm:
  * every cut gets a transition from a varied cycle (never the same kind twice in a row)
  * every transition gets its own sound, rotating through several whooshes/swipes so no two cuts sound alike
  * round / versus / verdict / score cards carry their signature sounds (bell, impact, shutter+thud, ticks+win/stinger)
  * HUD (round + score) stamped on the footage of each round
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aus_kit as A
import edit_kit as K

K.SFX.update({n: (f"sfx/{n}.wav", g) for n, g in {
    "whoosh_a": -21, "whoosh_b": -21, "whoosh_c": -22, "whoosh_low": -19, "swipe": -22, "whip": -20, "riser": -21,
    "reverse": -21, "impact": -15, "thud": -16, "bell": -20, "tick": -22, "shutter": -18, "stinger": -17, "win": -18,
    "heartbeat": -15, "growl": -18, "snow": -24}.items()})
fx = K.fx

# transition kind -> sounds that fit it (rotated)
TRANS_SFX = {"fade": [None, "whoosh_c", None], "slide": ["swipe", "whoosh_b"], "zoom": ["whoosh_a", "whoosh_low"],
             "wipe": ["swipe", "whoosh_a"], "whip": ["whip"], "flash": ["impact", "reverse"], "blur": ["whoosh_c", "whoosh_low"],
             "punch": ["whoosh_b", "thud"], "mono": ["shutter"]}
CYCLE = ["fade", "slide", "punch", "blur", "zoom", "fade", "whip", "wipe", "flash", "blur", "slide", "zoom", "fade", "punch", "mono"]
GRAPHIC_IN = {"round": "flash", "versus": "whip", "verdict": "punch", "score": "zoom", "serif": "blur", "questions": "blur",
              "cta": "zoom", "ficha": "slide"}
HUD = [None]


def hud(rnd, a, b):
    """From here on every footage shot shows the round tracker (None to hide)."""
    HUD[0] = None if rnd is None else [rnd, a, b]


def _src(scene):
    return A.P(scene, photo_only=True)["src"]


def foot(scene, cap=None, move=None):
    s = A.P(scene, move=move, cap=cap)
    if HUD[0]:
        s["hud"] = list(HUD[0])
    return s


def label(scene, text, move=None):
    """Footage with the ivory label of the reference ('small|BIG')."""
    return foot(scene, cap=text, move=move)


def serif(scene, text, lines=(), size=120):
    return {"type": "serif", "bg": _src(scene), "text": text, "lines": list(lines), "size": size}


def round_card(num, name, sub, scene):
    return {"type": "round", "num": num, "name": name, "sub": sub, "bg": _src(scene),
            "sfx": [fx("bell", 0.05), fx("impact", 0.1, -3)]}


def versus(left_scene, left_name, left_stat, right_scene, right_name, right_stat):
    return {"type": "versus", "left": {"src": _src(left_scene), "name": left_name, "stat": left_stat},
            "right": {"src": _src(right_scene), "name": right_name, "stat": right_stat},
            "sfx": [fx("whip"), fx("impact", 0.75, -2), fx("growl", 0.9, -4)]}


def verdict(scene, winner, text=None):
    s = {"type": "verdict", "src": _src(scene), "winner": winner,
         "sfx": [fx("heartbeat", 0, -2), fx("shutter", 0.25), fx("thud", 0.55, 2),
                 fx({"tigre": "win", "feras": "stinger", "empate": "riser"}[winner], 0.6)]}
    if text:
        s["text"] = text
    return s


def score(scene, prev, now, sub=""):
    up = "win" if now[0] > prev[0] else ("stinger" if now[1] > prev[1] else "thud")
    return {"type": "score", "bg": _src(scene), "prev": list(prev), "now": list(now), "sub": sub,
            "sfx": [fx("tick", 0.2), fx("tick", 0.4), fx(up, 0.6, -3)]}


def measure(scene, value, cap=None, side="right", top=0.12, bottom=0.8):
    s = {"type": "measure", "src": _src(scene), "value": value, "side": side, "top": top, "bottom": bottom,
         "move": "in", "sfx": [fx("riser", 0, -6), fx("tick", 0.95)]}
    if cap:
        s["caption"] = cap
    if HUD[0]:
        s["hud"] = list(HUD[0])
    return s


def ficha(scene, name, sci, rows, source=None):
    s = {"type": "ficha", "bg": _src(scene), "name": name, "sci": sci, "rows": rows,
         "sfx": [fx("swipe")] + [fx("tick", 0.5 + 0.35 * k) for k in range(len(rows))]}
    if source:
        s["source"] = source
    return s


def cta(text, sub, scene):
    return {"type": "cta", "text": text, "sub": sub, "bg": _src(scene), "sfx": [fx("whoosh_a"), fx("tick", 1.2), fx("tick", 2.5)]}


def questions(c, items, phrases, scene):
    A.questions(c, items, phrases)
    t, s = c.cues[-1]
    s["bg"] = _src(scene)
    s["sfx"] = [fx("riser", 0, -8)] + [dict(x, file="sfx/tick.wav", gain=-20) for x in s["sfx"]]


def cut_rhythm(ep):
    """Transitions + their sounds on every cut, varied. Runs on the finished episode JSON."""
    k = 0; last = None; snd = {}
    first = True
    for chap in ep["chapters"]:
        for s in chap["shots"]:
            if first:
                first = False; continue
            kind = s.get("trans") or GRAPHIC_IN.get(s["type"])
            if not kind:
                kind = CYCLE[k % len(CYCLE)]; k += 1
                if kind == last:
                    kind = CYCLE[k % len(CYCLE)]; k += 1
            s["trans"] = kind; last = kind
            if s["type"] in GRAPHIC_IN:   # graphics already carry their signature sound
                continue
            opts = TRANS_SFX.get(kind, [None])
            name = opts[snd.get(kind, 0) % len(opts)]; snd[kind] = snd.get(kind, 0) + 1
            if name:
                s.setdefault("sfx", [])
                s["sfx"] = [fx(name, 0, -1)] + list(s["sfx"])
    return ep
