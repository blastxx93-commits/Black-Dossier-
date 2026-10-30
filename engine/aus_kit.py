"""Shared edit kit for the Aussie car channel (episodes/aus*/edit/build_*.py).

An episode build only declares its scene pools and its cue sheet; this module does the rest:
  * photo pools: per scene, an ordered list of folders ("h_mechanic", "m_shark6") and AI scenes ("ai:ai_smash_repairer")
  * clip pools: per scene, hand-picked clips ("v_mechanic/3"); clips win while the clip share is under CLIP_TARGET
  * no repeats: every file once, and a content fingerprint so the same photo under two names is still caught
  * long holds split: any shot over MAX_HOLD keeps KEEP seconds and hands over to fresh footage of the chapter
  * channel checks: no black shots, no repeats, alignment and missing phrases reported

Usage in a build script:
    import aus_kit as A
    A.setup(script_dir=sys.argv[1], skip_file="skip.json", photos={...}, clips={...}, generic_clips=[...], fallback={...})
    c = A.ch("ch00_hook"); c.at(0, A.P("crash")); ...
    print(A.finish(chapters, "AUS02_BYD.mp4", ctx=["crash", ...]))
"""
import csv, glob, json, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cues import Chapter
import edit_kit as K

K.SFX.update({"hit": ("sfx/hit.wav", -16), "whoosh": ("sfx/whoosh.wav", -20), "pop": ("sfx/pop.wav", -22)})
fx = K.fx
CFG = {"script": ".", "skip": set(), "photos": {}, "clips": {}, "generic_clips": [], "fallback": {}, "any": [], "reserved": set()}
USED, HASHES, POOLS, CREDITS = set(), [], {}, {}
COUNT = {"img": 0, "vid": 0}
CLIP_TARGET = 0.40
MAX_HOLD, KEEP = 7.5, 5.0
MOVES = ["in", "left", "out", "right", "in", "up", "out", "down"]
_mv = [0]


def setup(script_dir, skip_file=None, photos=None, clips=None, generic_clips=None, fallback=None, any_pools=None, reserved=None):
    """reserved: ["m_dolphin/3", ...] photos kept for a specific line (photo()/rank()), never taken by a pool."""
    CFG.update(script=script_dir, photos=photos or {}, clips=clips or {}, generic_clips=generic_clips or [],
               fallback=fallback or {}, any=any_pools or [])
    if skip_file and os.path.exists(skip_file):
        CFG["skip"] = set(json.load(open(skip_file)))
    # reviewed.json (next to skip.json): every photo/clip I have actually looked at on a contact sheet.
    # Anything not listed is treated as skipped, so an unreviewed download can never reach a video.
    rev = os.path.join(os.path.dirname(skip_file or ""), "reviewed.json")
    CFG["reviewed"] = set(json.load(open(rev))) if os.path.exists(rev) else None
    for spec in reserved or []:
        folder, n = spec.split("/")
        CFG["reserved"].update(x[2:] for x in glob.glob(f"a/{folder}/{n}_*"))
    for fn in sorted(glob.glob("a/credits*.csv")):
        for r in csv.DictReader(open(fn)):
            CREDITS[r.get("file", "")] = r


# ---------------------------------------------------------------- fingerprints (no repeats by content)
def fingerprint(path):
    from PIL import Image
    p = os.path.join("a", path)
    try:
        if p.lower().endswith(".mp4"):
            raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", "3", "-i", p, "-frames:v", "1", "-vf", "scale=9:8,format=gray",
                                  "-f", "rawvideo", "-"], capture_output=True).stdout
            if len(raw) < 72:
                return None
            px = list(raw[:72])
        else:
            im = Image.open(p).convert("L").resize((9, 8), Image.LANCZOS)
            px = [im.getpixel((x, y)) for y in range(8) for x in range(9)]
    except Exception:
        return None
    return sum(1 << (r * 8 + c) for r in range(8) for c in range(8) if px[r * 9 + c] > px[r * 9 + c + 1])


def reviewed(path):
    r = CFG.get("reviewed")
    return r is None or path in r or path.startswith("ai/")


def claim(path):
    """True if the file is new (by name and by content), was reviewed, and marks it used."""
    if path in USED or not reviewed(path):
        return False
    h = fingerprint(path)
    if h is not None and any(bin(h ^ o).count("1") <= 6 for o in HASHES):
        return False
    USED.add(path)
    if h is not None:
        HASHES.append(h)
    return True


# ---------------------------------------------------------------- pools
def _folder_files(src):
    if src.startswith("ai:"):
        fs = sorted(glob.glob(f"a/ai/{src[3:]}_*.jpg"))
    else:
        fs = sorted(glob.glob(f"a/{src}/*.jpg") + glob.glob(f"a/{src}/*.png") + glob.glob(f"a/{src}/*.jpeg"))
    return [f[2:] for f in fs if f[2:] not in CFG["skip"]]


def _pool(scene):
    if scene not in POOLS:
        srcs = CFG["photos"].get(scene, [scene])
        POOLS[scene] = [f for s in srcs for f in _folder_files(s)]
    return POOLS[scene]


def _photo(scene, move=None, cap=None, **kw):
    for sc in [scene] + CFG["fallback"].get(scene, []) + CFG["any"] + list(CFG["photos"]):
        pl = _pool(sc)
        while pl:
            f = pl.pop(0)
            if f not in CFG["reserved"] and claim(f):
                COUNT["img"] += 1
                if move is None:
                    move = MOVES[_mv[0] % len(MOVES)]; _mv[0] += 1
                return K.img(f, move, cap=cap, **kw)
    sys.exit(f"Sem fotos novas para '{scene}' (e alternativas) — buscar mais imagens")


def _clip_file(spec):
    folder, n = spec.split("/")
    fs = [f[2:] for f in sorted(glob.glob(f"a/video/{folder}/{n}_*.mp4"))
          if not f.endswith(("_archive.mp4", "_commons.mp4"))]
    return fs[0] if fs and fs[0] not in CFG["skip"] else None


def V(scene, cap=None, generic=False):
    for spec in CFG["clips"].get(scene, []) + (CFG["generic_clips"] if generic else []):
        f = _clip_file(spec)
        if f and claim(f):
            COUNT["vid"] += 1
            return K.vid(f, cap=cap, fit="crop")
    return None


def P(scene, move=None, cap=None, photo_only=False, generic=False, **kw):
    """Footage for a scene: a matching clip while the clip share is under target, else the next fresh photo."""
    tot = COUNT["img"] + COUNT["vid"]
    if not photo_only and (tot == 0 or COUNT["vid"] / tot < CLIP_TARGET):
        v = V(scene, cap, generic)
        if v:
            return v
    try:
        return _photo(scene, move, cap, **kw)
    except SystemExit:
        # photos exhausted: any unused clip of the scene (or a generic one) is still fresh footage
        v = V(scene, cap, True)
        if v:
            return v
        raise


def M(folder, n):
    """A specific photo by its number on the contact sheet (model shots); counts as used."""
    fs = [x[2:] for x in sorted(glob.glob(f"a/{folder}/{n}_*")) if x.lower().endswith((".jpg", ".jpeg", ".png"))]
    if not fs:
        sys.exit(f"Foto {folder}/{n} não existe")
    CFG["reserved"].discard(fs[0])
    claim(fs[0]) or sys.stderr.write(f"aviso: {fs[0]} parecida com outra já usada\n")
    COUNT["img"] += 1
    return fs[0]


def photo(folder, n, move="in", cap=None):
    return K.img(M(folder, n), move, cap=cap)


def credit(path):
    r = CREDITS.get(path, {})
    a = (r.get("author") or "").strip()
    return f"Photo: {a[:40]} · {(r.get('license') or '').strip()}" if a else ""


# ---------------------------------------------------------------- graphics
def rank(num, name, folder, n, tag=None, sub=None):
    f = M(folder, n)
    s = {"type": "rank", "num": num, "name": name, "photo": "a/" + f, "credit": credit(f), "trans": "wipe",
         "sfx": [fx("whoosh"), fx("hit", 0.15, -6)]}
    if tag: s["tag"] = tag
    if sub: s["sub"] = sub
    return s


def stat(value, label, source=None, red=False, tag=None, count=True):
    s = {"type": "stat", "value": value, "label": label, "count": count, "sfx": [fx("pop", 0.05)]}
    if source: s["source"] = source
    if red: s["color"] = "red"
    if tag: s["tag"] = tag
    return s


def bars(title, items, delta=None, source=None, prefix="", suffix=""):
    s = {"type": "bars", "title": title, "items": items, "sfx": [fx("whoosh", 0, -4)], "prefix": prefix, "suffix": suffix}
    if delta: s["delta"] = delta
    if source: s["source"] = source
    return s


def price(model, old, new, old_note=None, new_note=None, save=None, source=None):
    s = {"type": "price", "model": model, "old": old, "new": new, "sfx": [fx("pop", 0.6), fx("pop", 1.0)]}
    for k, v in (("old_note", old_note), ("new_note", new_note), ("save", save), ("source", source)):
        if v: s[k] = v
    return s


def say(text, hl="", size=140):
    return {"type": "statement", "text": text, "highlight": hl, "size": size, "sfx": [fx("hit", 0, -4)]}


def cta(text, sub):
    return {"type": "cta", "text": text, "sub": sub, "sfx": [fx("whoosh"), fx("pop", 1.2)]}


def title(t, sub, tag, bg_scene):
    return {"type": "title", "title": t, "subtitle": sub, "tag": tag, "bg": P(bg_scene, photo_only=True)["src"],
            "trans": "zoom", "sfx": [fx("whoosh"), fx("hit", 0.6, -4)]}


def ch(name, tail=0.8):
    s = CFG["script"]
    return Chapter(name, f"{s}/{name}.txt", f"a/words/{name}.words.json", f"audio/{name}.flac", tail=tail)


def questions(c, items, phrases):
    ts = [c.find(p) for p in phrases]
    if None in ts:
        sys.exit(f"{c.name}: frase das perguntas não encontrada: {phrases}")
    t0 = max(0.0, ts[0] - 0.12)
    c.cues.append((t0, {"type": "questions", "items": items, "starts": [int((t - 0.12 - t0) * 24) for t in ts],
                        "sfx": [fx("pop", t - 0.12 - t0) for t in ts]}))


# ---------------------------------------------------------------- finish
def finish(chapters, output, ctx, subtitles=None, music_gain=-29):  # -29 dB: bed sits well under the voice
    """Builds episode JSON: timings from the narration, long holds split, channel checks. Returns the JSON text."""
    ep = K.build_episode(chapters, output, music="trilha.wav", music_gain=music_gain, final_fade=0)
    ep["size"] = [1920, 1080]
    if subtitles:
        ep["subtitles"] = subtitles
    misses = [m for c in chapters for m in c.misses]
    if misses:
        sys.exit(f"FRASES NÃO ENCONTRADAS NA NARRAÇÃO: {misses}")
    splits = 0
    for ci, chap in enumerate(ep["chapters"]):
        out = []
        for s in chap["shots"]:
            while s["dur"] > MAX_HOLD and s["type"] not in ("questions", "title"):
                first = dict(s, dur=KEEP, fixed=True)
                nxt = dict(P(ctx[ci], generic=True), dur=round(s["dur"] - KEEP, 3), fixed=s.get("fixed", False))
                out.append(first); s = nxt; splits += 1
            out.append(s)
        chap["shots"] = out
    seen = {}
    for ci, chap in enumerate(ep["chapters"]):
        for s in chap["shots"]:
            for k in ("src", "photo", "bg"):
                if s.get(k):
                    if s[k] in seen:
                        sys.exit(f"IMAGEM REPETIDA: {s[k]} (cap. {seen[s[k]]} e {ci})")
                    seen[s[k]] = ci
    vid = sum(s["dur"] for c in ep["chapters"] for s in c["shots"] if s["type"] == "video")
    img = sum(s["dur"] for c in ep["chapters"] for s in c["shots"] if s["type"] == "image")
    n = sum(len(c["shots"]) for c in ep["chapters"])
    sys.stderr.write(f"{n} planos ({splits} divididos), {len(seen)} arquivos diferentes; "
                     f"clipes {vid / max(1, vid + img):.0%} do tempo de imagem\n")
    return json.dumps(ep, indent=1)
