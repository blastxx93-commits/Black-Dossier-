"""Edit kit of the Era das Feras channel (episodes/fe*/edit/build_*.py), on top of aus_kit.py.

Adds the channel's layouts (render_feras.py) as one-line builders and, at the end, the cutting rhythm:
  * every cut gets a transition from a varied cycle (never the same kind twice in a row)
  * every transition gets its own sound, rotating through several whooshes/swipes so no two cuts sound alike
  * round / versus / verdict / score cards carry their signature sounds (bell, impact, shutter+thud, ticks+win/stinger)
  * HUD (round + score) stamped on the footage of each round
"""
import json, os, sys
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
    v = A.V(scene, cap, True) if not kw.get("photo_only") else None
    if v:   # photos exhausted: a fresh clip (or clip segment) of the scene is still real footage
        return v
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
    if i not in PINS and os.environ.get("FERAS_DRYRUN"):
        MISSING["pin:" + i] = 1
        return f"a/FALTA/{i}.jpg"
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


def versus(left_scene, left_name, left_stat, right_scene, right_name, right_stat, limg=None, rimg=None):
    return {"type": "versus", "left": {"src": pinned(limg) if limg else _src(left_scene), "name": left_name, "stat": left_stat},
            "right": {"src": pinned(rimg) if rimg else _src(right_scene), "name": right_name, "stat": right_stat},
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
            if s["type"] in GRAPHIC_IN or s.get("hfcard"):   # graphics already carry their signature sound
                continue
            opts = TRANS_SFX.get(kind, [None])
            name = opts[snd.get(kind, 0) % len(opts)]; snd[kind] = snd.get(kind, 0) + 1
            if name:
                s.setdefault("sfx", [])
                s["sfx"] = [fx(name, 0, -4)] + list(s["sfx"])
    return ep


# ---------------------------------------------------------------- HyperFrames cards (template "Dossiê Fóssil", fe04+)
HF_CARDS = [0]
HF_SFX = {"titulo": [("riser", 0, -6), ("impact", 0.6, -4)], "capitulo": [("whoosh_low", 0, -3), ("thud", 0.5, -2)],
          "rotulo": [("swipe", 0.3, -4)], "ficha": [("swipe", 0.1, -2), ("tick", 1.1), ("tick", 1.45), ("tick", 1.8), ("tick", 2.15)],
          "numero": [("riser", 0, -8), ("tick", 0.4), ("tick", 0.8), ("impact", 1.6, -6)], "mapa": [("whoosh_a", 0.1, -6), ("whoosh_low", 2.0, -4), ("impact", 3.6, -6)],
          "linha": [("swipe", 0.6, -4), ("thud", 2.0, -2)], "comparar": [("whoosh_b", 1.0, -3)], "frase": [("impact", 0.2, -4)],
          "escala": [("tick", 0.9), ("tick", 1.45), ("tick", 2.0), ("tick", 2.55)], "perguntas": [("riser", 0, -8)],
          "cta": [("whoosh_a", 0.2), ("bell", 1.9, -2)]}
# (longest a card may stay, length kept when it is split): info cards hold until read; titles stay snappy
HF_HOLD = {"versus": (8.0, 6.8), "placar": (6.0, 5.0), "veredito": (5.5, 4.6), "rodada": (6.0, 5.0), "mapa": (9.0, 7.5), "ficha": (8.5, 7.0), "escala": (8.0, 6.5), "linha": (8.0, 6.5), "numero": (7.0, 5.5),
           "perguntas": (9.0, 8.0), "titulo": (7.5, 6.5), "comparar": (7.0, 6.0), "cta": (6.5, 5.0)}
HF_IN = {"rodada": "blur", "versus": "cut", "veredito": "cut", "placar": "blur", "titulo": "cut", "capitulo": "flash", "mapa": "blur", "linha": "blur", "escala": "blur", "numero": "blur", "ficha": "slide",
         "comparar": "fade", "frase": "punch", "perguntas": "blur", "cta": "zoom", "rotulo": "fade"}


def _img(i):
    """'ai_x' / 'p_x/1' -> pinned reviewed file; 'scene:<name>' -> next photo of that scene."""
    if i.startswith("scene:"):
        return _src(i[6:])
    return pinned(i)


def hf(kind, **p):
    """A card of the HyperFrames graphics package (engine/hf_cards.py renders it as hf/<id>.mp4)."""
    HF_CARDS[0] += 1
    cid = f"hf{HF_CARDS[0]:02d}_{kind}"
    for k in ("img", "limg", "rimg"):
        if p.get(k):
            p[k] = _img(p[k])
    s = {"type": "video", "src": f"hf/{cid}.mp4", "fit": "crop", "start": 0, "trans": HF_IN.get(kind, "fade"),
         "max_hold": HF_HOLD.get(kind, (6.0, 4.6))[0], "keep": HF_HOLD.get(kind, (6.0, 4.6))[1],
         "hfcard": dict(p, kind=kind, id=cid), "sfx": [fx(n, *a) for n, *a in HF_SFX.get(kind, [])]}
    return s


def export_hf(ep, path):
    """Writes edit/hf_cards.json with the final duration of every card (+0.8 s so a transition never loops the clip)."""
    out = []
    for c in ep["chapters"]:
        for s in c["shots"]:
            if s.get("hfcard"):
                out.append(dict(s["hfcard"], dur=round(s["dur"] + 0.8, 3)))
    json.dump(out, open(path, "w"), ensure_ascii=False, indent=1)
    return out


# ---------------------------------------------------------------- per-episode look & sound (owner 15/11/2026)
# every episode can pick its own HyperFrames theme and the "cinema" sound kit: no whooshes, no hiss (tonal hits only)
THEME = [None]
CINEMA_TRANS_SFX = {"fade": [None, None, "hit_soft"], "slide": ["sub_drop", None, "tape"], "zoom": ["boom_deep", "sub_drop"],
                    "wipe": ["pulse", None], "whip": ["tape"], "flash": ["hit_soft", "glass"], "blur": [None, "shimmer"],
                    "punch": ["hit_soft"], "mono": ["tick_soft"]}
CINEMA_HF_SFX = {"titulo": [("braam", 0.4, -6), ("shimmer", 1.0, -10)], "rodada": [("boom_deep", 0, -4), ("ice_crack", 0.5, -6)],
                 "versus": [("sub_drop", 0, -4), ("braam", 0.7, -4)], "veredito": [("pulse", 0, -4), ("tick_soft", 0.6), ("boom_deep", 0.8, -2)],
                 "placar": [("tick_soft", 1.1), ("tick_soft", 1.4)], "ficha": [("glass", 0.1, -8)] + [("tick_soft", 1.1 + 0.32 * k) for k in range(4)],
                 "rotulo": [("glass", 0.35, -10)], "frase": [("hit_soft", 0.2, -4)], "escala": [("riser_tone", 0.3, -10)],
                 "mapa": [("sub_drop", 0.8, -6), ("ice_crack", 2.6, -6)], "perguntas": [("riser_tone", 0, -10)], "cta": [("glass", 0.2, -8), ("bell", 1.8, -6)]}


def use_cinema(theme):
    """Switch this episode to a HyperFrames theme + the tonal sound kit."""
    THEME[0] = theme
    K.SFX.update({n: (f"sfx/{n}.wav", g - SFX_DOWN) for n, g in {
        "sub_drop": -16, "boom_deep": -14, "hit_soft": -15, "pulse": -14, "shimmer": -22, "glass": -24, "tape": -18, "braam": -15,
        "riser_tone": -20, "tick_soft": -20, "ice_crack": -20, "win_brass": -16}.items()})
    TRANS_SFX.clear(); TRANS_SFX.update(CINEMA_TRANS_SFX)
    # 2.5D parallax camera on every other picture (owner: not a slideshow); the rest keep smooth classic moves
    MOTION_CYCLE[:] = ["parallax", "push", "parallax", "pan_l", "parallax", "pull", "parallax", "diag", "parallax", "pan_r", "parallax", "focus"]
    HF_SFX.clear(); HF_SFX.update(CINEMA_HF_SFX)


def placar_sfx(prev, now):
    up = "win_brass" if now[0] > prev[0] else ("braam" if now[1] > prev[1] else "pulse")
    return [fx("tick_soft", 1.1), fx(up, 1.4, -4)]


def export_hf_theme(ep, path):
    out = export_hf(ep, path)
    if THEME[0]:
        json.dump({"theme": THEME[0], "cards": out}, open(path, "w"), ensure_ascii=False, indent=1)
    return out
