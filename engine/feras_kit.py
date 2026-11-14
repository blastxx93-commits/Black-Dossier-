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

SFX_DOWN = 9   # owner (13/11/2026): transition sounds were too loud; everything 9 dB lower, transitions a further 3 dB
K.SFX.update({n: (f"sfx/{n}.wav", g - SFX_DOWN) for n, g in {
    "whoosh_a": -21, "whoosh_b": -21, "whoosh_c": -22, "whoosh_low": -19, "swipe": -22, "whip": -20, "riser": -21,
    "reverse": -21, "impact": -15, "thud": -16, "bell": -20, "tick": -22, "shutter": -18, "stinger": -17, "win": -18,
    "heartbeat": -15, "growl": -18, "snow": -24}.items()})
fx = K.fx
A.CFG["review_ai"] = True
_orig_photo = A._photo


def _photo_strict(scene, move=None, cap=None, **kw):
    """Owner rule (13/11/2026): never an image unrelated to the moment. A scene only borrows from the scenes listed
    in its own fallback (e.g. the wolf round from the tiger and the Ice Age landscape), never from another beast;
    when those run out the build stops and asks for more images instead of filling with anything."""
    allowed = [scene] + CFG_FALLBACK(scene)
    for sc in allowed:
        pl = A._pool(sc)
        while pl:
            f = pl.pop(0)
            if f not in A.CFG["reserved"] and A.claim(f):
                A.COUNT["img"] += 1
                if move is None:
                    move = A.MOVES[A._mv[0] % len(A.MOVES)]; A._mv[0] += 1
                return K.img(f, move, cap=cap, **kw)
    if os.environ.get("FERAS_DRYRUN"):   # count what is missing instead of stopping (planning only)
        MISSING[scene] = MISSING.get(scene, 0) + 1
        return K.img(f"FALTA/{scene}_{sum(MISSING.values())}.jpg", move or "in", cap=cap, **kw)
    sys.exit(f"Sem imagens novas e revisadas para '{scene}' (nem em {allowed[1:]}) — gerar mais cenas")


MISSING = {}


def CFG_FALLBACK(scene):
    return list(A.CFG["fallback"].get(scene, []))


A._photo = _photo_strict   # owner rule (13/11/2026): AI images too only after review (edit/reviewed.json)

# transition kind -> sounds that fit it (rotated)
TRANS_SFX = {"fade": [None, "whoosh_c", None], "slide": ["swipe", "whoosh_b"], "zoom": ["whoosh_a", "whoosh_low"],
             "wipe": ["swipe", "whoosh_a"], "whip": ["whip"], "flash": ["impact", "reverse"], "blur": ["whoosh_c", "whoosh_low"],
             "punch": ["whoosh_b", "thud"], "mono": ["shutter"]}
CYCLE = ["fade", "slide", "blur", "zoom", "fade", "wipe", "blur", "flash", "fade", "slide", "zoom", "fade", "mono", "blur"]
GRAPHIC_IN = {"round": "flash", "versus": "slide", "verdict": "blur", "score": "zoom", "serif": "blur", "questions": "blur",
              "cta": "zoom", "ficha": "slide"}
HUD = [None]


HUD_TOTAL = [10]


def hud(rnd, a, b):
    """From here on every footage shot shows the round tracker (None to hide)."""
    HUD[0] = None if rnd is None else [rnd, a, b, HUD_TOTAL[0]]


def _src(scene):
    return A.P(scene, photo_only=True)["src"]


PINS = {}


def pin(*ids):
    """Reserve specific reviewed images (ai ids like 'ai_trex_portrait' or 'p_trex/1') for exact layouts:
    the pools will never use them, and pinned(id) hands each one out once."""
    import glob
    for i in ids:
        fs = sorted(glob.glob(f"a/ai/{i}_*.jpg")) if i.startswith("ai_") else sorted(glob.glob(f"a/{i.split('/')[0]}/{i.split('/')[1]}_*"))
        if fs:
            PINS[i] = fs[0][2:]
            A.CFG["reserved"].add(fs[0][2:])


def pinned(i):
    f = PINS[i]
    A.CFG["reserved"].discard(f)
    A.claim(f) or sys.stderr.write(f"aviso: {f} já usada\n")
    return "a/" + f


def _bg(scene):
    """Background of a card (blurred + darkened): a placeholder resolved after the edit to a photo of the same
    scene already on screen, so cards do not eat fresh footage (no visible repeat: it is out of focus)."""
    _BGN[0] += 1
    return f"@bg:{scene}#{_BGN[0]}"


_BGN = [0]


def foot(scene, cap=None, move=None):
    s = A.P(scene, move=move, cap=cap)
    if HUD[0]:
        s["hud"] = list(HUD[0])
    return s


def label(scene, text, move=None):
    """Footage with the ivory label of the reference ('small|BIG')."""
    return foot(scene, cap=text, move=move)


def serif(scene, text, lines=(), size=120):
    return {"type": "serif", "bg": _bg(scene), "text": text, "lines": list(lines), "size": size}


def round_card(num, name, sub, scene):
    return {"type": "round", "num": num, "name": name, "sub": sub, "bg": _bg(scene), "of": HUD_TOTAL[0],
            "sfx": [fx("bell", 0.05), fx("impact", 0.1, -3)]}


def versus(left_scene, left_name, left_stat, right_scene, right_name, right_stat):
    return {"type": "versus", "left": {"src": _src(left_scene), "name": left_name, "stat": left_stat},
            "right": {"src": _src(right_scene), "name": right_name, "stat": right_stat},
            "sfx": [fx("whip"), fx("impact", 0.75, -2), fx("growl", 0.9, -4)]}


def verdict(scene, winner, text=None, img=None):
    s = {"type": "verdict", "src": pinned(img) if img else _src(scene), "winner": winner,
         "sfx": [fx("heartbeat", 0, -2), fx("shutter", 0.25), fx("thud", 0.55, 2),
                 fx({"tigre": "win", "feras": "stinger", "empate": "riser"}[winner], 0.6)]}
    if text:
        s["text"] = text
    return s


def score(scene, prev, now, sub=""):
    up = "win" if now[0] > prev[0] else ("stinger" if now[1] > prev[1] else "thud")
    return {"type": "score", "bg": _bg(scene), "prev": list(prev), "now": list(now), "sub": sub,
            "sfx": [fx("tick", 0.2), fx("tick", 0.4), fx(up, 0.6, -3)]}


def measure(scene, value, cap=None, side="right", top=0.12, bottom=0.8, img=None):
    s = {"type": "measure", "src": pinned(img) if img else _src(scene), "value": value, "side": side, "top": top, "bottom": bottom,
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
    return {"type": "cta", "text": text, "sub": sub, "bg": _bg(scene), "sfx": [fx("whoosh_a"), fx("tick", 1.2), fx("tick", 2.5)]}


def questions(c, items, phrases, scene):
    A.questions(c, items, phrases)
    t, s = c.cues[-1]
    s["bg"] = _bg(scene)
    s["sfx"] = [fx("riser", 0, -8)] + [dict(x, file="sfx/tick.wav", gain=-20) for x in s["sfx"]]


MOTION_CYCLE = ["push", "pan_l", "pull", "tilt_up", "diag", "pan_r", "push", "focus", "tilt_down", "pull", "pan_l", "diag"]
SNOWY = ("tiger", "mammoth", "rhino", "bison", "blizzard", "steppe", "direwolf", "cavelion", "hook", "snow")


def camera(ep):
    """A different camera move on every photo (never the same twice in a row), falling snow on snowy scenes,
    an occasional warm light leak; one clip in four in slow motion for weight."""
    m = v = 0; last = None
    for chap in ep["chapters"]:
        for s in chap["shots"]:
            if s["type"] == "image" and not s.get("motion"):
                mo = MOTION_CYCLE[m % len(MOTION_CYCLE)]; m += 1
                if mo == last:
                    mo = MOTION_CYCLE[m % len(MOTION_CYCLE)]; m += 1
                s["motion"] = last = mo
                if any(w in s["src"] for w in SNOWY) and m % 3 == 0:
                    s["snow"] = True
                if m % 9 == 4:
                    s["leak"] = True
            elif s["type"] == "video":
                v += 1
                pass   # no slow motion: duplicated frames stutter (owner: no shaky picture)
    return ep


def resolve_bg(ep, scene_of=None):
    """Fills the card backgrounds: a photo of the card's scene already used (the folder name or AI id carries the
    scene's words), rotating so consecutive cards differ; any used photo if the scene has none."""
    import itertools
    used = [s["src"] for c in ep["chapters"] for s in c["shots"] if s["type"] == "image"]
    pools = {}
    k = itertools.count()
    for c in ep["chapters"]:
        for s in c["shots"]:
            b = s.get("bg", "")
            if isinstance(b, str) and b.startswith("@bg:"):
                sc = b[4:].split("#")[0]
                keys = (scene_of or {}).get(sc, [sc])
                pool = pools.setdefault(sc, [u for u in used if any(w in u for w in keys)] or used)
                s["bg"] = pool[next(k) % len(pool)]
    return ep


def cut_rhythm(ep, scene_of=None):
    """Transitions + their sounds on every cut, varied. Runs on the finished episode JSON."""
    resolve_bg(ep, scene_of)
    camera(ep)
    ep["fps"] = 30   # smoother camera moves than 24 fps (owner: no shaky picture)
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
                s["sfx"] = [fx(name, 0, -4)] + list(s["sfx"])
    return ep
