#!/usr/bin/env python3
"""Race template (owner's choice 19/11/2026): renders an aus_kit episode.json with HyperFrames.

Fast, aggressive "racing channel" look: whip-in cuts with smear + white flash, punch-ins every ~2.4 s inside long
photo holds, speed lines, slanted condensed type (Anton), red #e10600 accent, slam-in rank cards with screen shake,
location chips, HUD with the current list position.

Visuals are rendered by HyperFrames (npx hyperframes, needs Node + Chromium); narration, music and sfx are mixed with
ffmpeg and the subtitles (.ass) are burned in afterwards, so the audio chain stays identical to render_aus.py.

    python3 engine/hf_race.py <workdir> [--episode episode.json] [--out OUT.mp4] [--from S --to E] [--hf DIR]
workdir: the usual edit folder (a/ -> assets, audio/, sfx/, trilha.wav, episode.json, subtitles .ass).
--hf: folder where the hyperframes npm package is installed (default: engine/../.hf, installed on first use).
"""
import argparse, csv, html, json, os, re, shutil, subprocess, sys
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
W, H, FPS = 1920, 1080, 24
RED = "#e10600"


def sh(cmd, **kw):
    print("+", " ".join(cmd)[:200], flush=True)
    return subprocess.run(cmd, check=True, **kw)


def credits_map(wd):
    out = {}
    for name in ("credits.csv", "video_credits.csv"):
        p = os.path.join(wd, "a", name)
        if os.path.exists(p):
            for r in csv.DictReader(open(p)):
                out["a/" + r["file"]] = r
    return out


def credit_text(cr, src):
    r = cr.get(src, {})
    a = (r.get("author") or "").strip()
    lic = (r.get("license") or "").strip()
    if not a and not lic:
        return ""
    return html.escape((f"Foto: {a[:40]} · {lic}" if a else lic))


def esc(s):
    return html.escape(str(s or ""))


class Comp:
    def __init__(self, proj, wd, cr):
        self.proj, self.wd, self.cr = proj, wd, cr
        self.els, self.js, self.n, self.assets = [], [], 0, {}

    def asset(self, src):
        """copy/resize an image or video into the project, return its relative path"""
        if src in self.assets:
            return self.assets[src]
        full = os.path.join(self.wd, src)
        ext = os.path.splitext(src)[1].lower()
        name = f"assets/m{len(self.assets):04d}{'.jpg' if ext in ('.jpg', '.jpeg', '.png', '.webp') else ext}"
        dst = os.path.join(self.proj, name)
        if ext in (".jpg", ".jpeg", ".png", ".webp"):
            im = Image.open(full).convert("RGB")
            im.thumbnail((2400, 2400))
            im.save(dst, quality=88)
        else:
            shutil.copy(full, dst)
        self.assets[src] = name
        return name

    def id(self, p):
        self.n += 1
        return f"{p}{self.n}"

    def at(self, code):
        self.js.append(code)

    # ------------------------------------------------------------------ shots
    def image(self, s, t, d, k):
        i = self.id("im")
        src = self.asset(s["src"])
        cred = credit_text(self.cr, s["src"])
        self.els.append(f'<div class="clip" id="{i}" style="opacity:0"><div class="ph" id="{i}p" style="background-image:url({src})"></div>'
                        f'<div class="ph ghost" id="{i}g" style="background-image:url({src})"></div>'
                        + (f'<div class="credit">{cred}</div>' if cred else "") + '</div>')
        dr = 1 if k % 2 == 0 else -1
        mv = s.get("move", "in")
        self.at(f'tl.set("#{i}",{{opacity:1}},{t:.3f});tl.set("#{i}",{{opacity:0}},{t + d:.3f});')
        self.at(f'tl.fromTo("#{i}p",{{x:{260 * dr},scale:1.2}},{{x:0,scale:1.05,duration:.35,ease:"expo.out"}},{t:.3f});')
        self.at(f'tl.fromTo("#{i}g",{{opacity:.55,x:{120 * dr}}},{{opacity:0,x:0,duration:.3}},{t:.3f});')
        self.flash(t, dr)
        # punch-ins inside long holds keep the cut rhythm fast
        beats = max(1, int(d // 2.4))
        seg = d / beats
        for b in range(beats):
            a = t + .35 + b * seg
            dur = seg - (.35 if b == 0 else 0)
            sc0, sc1 = (1.05, 1.13) if mv != "out" else (1.15, 1.05)
            if b:
                sc0 += .04 * (b % 2); sc1 += .04 * (b % 2)
                self.at(f'tl.set("#{i}p",{{scale:{sc0:.3f},x:{(-90 if b % 2 else 90) * dr}}},{a:.3f});')
                self.at(f'tl.fromTo("#speed",{{opacity:.5,x:0}},{{opacity:0,x:{-300 * dr},duration:.25}},{a:.3f});')
            xs = {"left": 80, "right": -80}.get(mv, -50 * dr)
            ys = {"up": -50, "down": 50}.get(mv, 0)
            self.at(f'tl.to("#{i}p",{{scale:{sc1:.3f},x:"+={xs}",y:"+={ys}",duration:{max(.1, dur - .05):.3f},ease:"none"}},{a:.3f});')
        if s.get("caption"):
            a, _, b = s["caption"].partition("|")
            c = self.id("cap")
            self.els.append(f'<div class="chip" id="{c}" style="left:96px;top:84px;opacity:0">{esc(a)}</div>'
                            f'<div class="tag" id="{c}t" style="left:104px;top:164px;opacity:0">{esc(b)}</div>')
            self.at(f'tl.fromTo("#{c}",{{x:-500,opacity:0}},{{x:0,opacity:1,duration:.3,ease:"power4.out"}},{t + .25:.3f});'
                    f'tl.fromTo("#{c}t",{{opacity:0}},{{opacity:1,duration:.3}},{t + .45:.3f});'
                    f'tl.to(["#{c}","#{c}t"],{{opacity:0,duration:.2}},{t + min(d, 5.5) - .2:.3f});')

    def video(self, s, t, d, k):
        i = self.id("vd")
        src = self.asset(s["src"])
        cred = esc((self.cr.get(s["src"], {}).get("license") or "").strip())
        self.els.append(f'<div class="clip" id="{i}" style="opacity:0"><video class="vid" id="{i}v" src="{src}" muted '
                        f'data-start="{t:.3f}" data-duration="{d:.3f}" data-media-start="{s.get("start", 0)}"></video>'
                        + (f'<div class="credit">{cred}</div>' if cred else "") + '</div>')
        self.at(f'tl.set("#{i}",{{opacity:1}},{t:.3f});tl.set("#{i}",{{opacity:0}},{t + d:.3f});'
                f'tl.fromTo("#{i}v",{{scale:1.15}},{{scale:1.04,duration:{d:.3f},ease:"none"}},{t:.3f});')
        self.flash(t, 1)

    def rank(self, s, t, d, k):
        i = self.id("rk")
        src = self.asset(s["photo"])
        name = s["name"].split()
        n1, n2 = (name[0], " ".join(name[1:])) if len(name) > 1 else ("", name[0])
        cred = esc(s.get("credit", ""))
        self.els.append(f'''<div class="clip card" id="{i}" style="opacity:0">
  <div class="ph" id="{i}p" style="background-image:url({src});opacity:.42"></div><div class="grade"></div>
  <div class="bar" id="{i}b" style="top:820px"></div>
  <div class="num" id="{i}n" style="left:110px;top:150px">{int(s["num"]):02d}</div>
  <div class="big" id="{i}a" style="left:660px;top:300px;font-size:140px">{esc(n1)}</div>
  <div class="big" id="{i}c" style="left:660px;top:440px;font-size:{190 if len(n2) < 13 else 130}px;color:{RED}">{esc(n2)}</div>
  <div class="tag" id="{i}t" style="left:680px;top:690px">{esc(s.get("tag", ""))}</div>
  <div class="tag small" id="{i}s" style="left:680px;top:740px">{esc(s.get("sub", ""))}</div>
  {f'<div class="credit">{cred}</div>' if cred else ""}</div>''')
        self.at(f'''tl.set("#{i}",{{opacity:1,x:0}},{t:.3f});
tl.fromTo("#{i}p",{{scale:1.3}},{{scale:1.05,duration:{d:.3f},ease:"power2.out"}},{t:.3f});
tl.fromTo("#{i}b",{{x:-2600}},{{x:0,duration:.35,ease:"power4.out"}},{t + .05:.3f});
tl.fromTo("#{i}n",{{scale:2.6,opacity:0}},{{scale:1,opacity:1,duration:.28,ease:"power4.in"}},{t + .15:.3f});
tl.fromTo("#{i}a",{{x:300,opacity:0}},{{x:0,opacity:1,duration:.3,ease:"power3.out"}},{t + .6:.3f});
tl.fromTo("#{i}c",{{x:500,opacity:0}},{{x:0,opacity:1,duration:.3,ease:"power3.out"}},{t + .75:.3f});
tl.fromTo(["#{i}t","#{i}s"],{{opacity:0,y:20}},{{opacity:1,y:0,duration:.3}},{t + 1.0:.3f});
tl.to("#{i}",{{x:-1920,duration:.25,ease:"power3.in"}},{t + d - .25:.3f});tl.set("#{i}",{{opacity:0}},{t + d:.3f});
''')
        self.shake(t + .43)
        h = self.id("hud")
        self.els.append(f'<div class="hud" id="{h}" style="opacity:0">#{int(s["num"]):02d} · {esc(s["name"].upper())}</div>')
        if self.hud:
            self.at(f'tl.set("#{self.hud[-1]}",{{opacity:0}},{t:.3f});')
        self.at(f'tl.set("#{h}",{{opacity:1}},{t + d:.3f});')
        self.hud.append(h)

    def stat(self, s, t, d, k):
        i = self.id("st")
        v = esc(s["value"])
        fs = 330 if len(s["value"]) <= 6 else (230 if len(s["value"]) <= 10 else 160)
        self.els.append(f'''<div class="clip card" id="{i}" style="opacity:0">
  <div class="bar" id="{i}b" style="top:700px;height:26px"></div>
  <div class="big center" id="{i}v" style="top:{450 - fs // 2}px;font-size:{fs}px">{v}</div>
  <div class="tag center" id="{i}l" style="top:760px">{esc(s["label"])}</div>
  <div class="src" id="{i}s">{("FUENTE: " + esc(s.get("source"))) if s.get("source") else ""}</div></div>''')
        self.at(f'''tl.set("#{i}",{{opacity:1}},{t:.3f});tl.set("#{i}",{{opacity:0}},{t + d:.3f});
tl.fromTo("#{i}b",{{x:-2600}},{{x:0,duration:.3,ease:"power4.out"}},{t:.3f});
tl.fromTo("#{i}v",{{scale:3,opacity:0}},{{scale:1,opacity:1,duration:.22,ease:"power4.in"}},{t + .1:.3f});
tl.fromTo("#{i}l",{{opacity:0,y:20}},{{opacity:1,y:0,duration:.3}},{t + .45:.3f});
tl.fromTo("#speed",{{opacity:.8,x:0}},{{opacity:0,x:-800,duration:1.2}},{t + .3:.3f});''')
        self.shake(t + .32)

    def statement(self, s, t, d, k):
        i = self.id("sm")
        hl = set(w for w in re.sub(r"[^\w\s]", " ", (s.get("highlight") or "").upper()).split())
        words = []
        for w in s["text"].upper().split():
            core = re.sub(r"[^\w]", "", w)
            words.append(f'<span style="color:{RED}">{esc(w)}</span>' if core and core in hl else esc(w))
        fs = 150 if len(s["text"]) < 28 else (118 if len(s["text"]) < 46 else 92)
        self.els.append(f'<div class="clip card" id="{i}" style="opacity:0"><div class="stripe2" id="{i}b"></div>'
                        f'<div class="big center wrap" id="{i}x" style="top:330px;font-size:{fs}px">{" ".join(words)}</div></div>')
        self.at(f'''tl.set("#{i}",{{opacity:1}},{t:.3f});tl.set("#{i}",{{opacity:0}},{t + d:.3f});
tl.fromTo("#{i}b",{{scaleX:0}},{{scaleX:1,duration:.3,ease:"power4.out"}},{t:.3f});
tl.fromTo("#{i}x",{{scale:1.8,opacity:0}},{{scale:1,opacity:1,duration:.25,ease:"power4.in"}},{t + .05:.3f});''')
        self.shake(t + .3)

    def title(self, s, t, d, k):
        i = self.id("tt")
        bg = self.asset(s["bg"]) if s.get("bg") else ""
        self.els.append(f'''<div class="clip card" id="{i}" style="opacity:0">
  {f'<div class="ph" id="{i}p" style="background-image:url({bg});opacity:.5"></div>' if bg else ''}<div class="grade"></div>
  <div class="bar" id="{i}b" style="top:760px"></div>
  <div class="big" id="{i}x" style="left:110px;top:330px;font-size:{170 if len(s["title"]) < 22 else 125}px">{esc(s["title"])}</div>
  <div class="chip" id="{i}s" style="left:118px;top:580px">{esc(s.get("subtitle", ""))}</div>
  <div class="tag" id="{i}g" style="left:124px;top:680px">{esc(s.get("tag", ""))}</div></div>''')
        self.at(f'''tl.set("#{i}",{{opacity:1}},{t:.3f});tl.set("#{i}",{{opacity:0}},{t + d:.3f});
{f'tl.fromTo("#{i}p",{{scale:1.25}},{{scale:1.05,duration:{d:.3f}}},{t:.3f});' if bg else ''}
tl.fromTo("#{i}b",{{x:-2600}},{{x:0,duration:.35,ease:"power4.out"}},{t:.3f});
tl.fromTo("#{i}x",{{x:-1400}},{{x:0,duration:.35,ease:"expo.out"}},{t + .1:.3f});
tl.fromTo("#{i}s",{{opacity:0,scale:.6}},{{opacity:1,scale:1,duration:.25,ease:"back.out(3)"}},{t + .45:.3f});
tl.fromTo("#{i}g",{{opacity:0}},{{opacity:1,duration:.3}},{t + .6:.3f});''')
        self.shake(t + .45)

    def questions(self, s, t, d, k):
        i = self.id("qs")
        rows = "".join(f'<div class="q" id="{i}q{j}"><span class="qn">{j + 1:02d}</span>{esc(x)}</div>' for j, x in enumerate(s["items"]))
        self.els.append(f'<div class="clip card" id="{i}" style="opacity:0"><div class="qs">{rows}</div></div>')
        self.at(f'tl.set("#{i}",{{opacity:1}},{t:.3f});tl.set("#{i}",{{opacity:0}},{t + d:.3f});')
        for j, st in enumerate(s.get("starts", [0] * len(s["items"]))):
            self.at(f'tl.fromTo("#{i}q{j}",{{x:-900,opacity:0}},{{x:0,opacity:1,duration:.3,ease:"power4.out"}},{t + st / FPS:.3f});')

    def cta(self, s, t, d, k):
        i = self.id("ct")
        self.els.append(f'''<div class="clip card" id="{i}" style="opacity:0"><div class="bar" id="{i}b" style="top:470px;height:180px"></div>
  <div class="big center" id="{i}x" style="top:440px;font-size:200px">{esc(s["text"].upper())}</div>
  <div class="tag center" id="{i}s" style="top:700px">{esc(s.get("sub", ""))}</div></div>''')
        self.at(f'''tl.set("#{i}",{{opacity:1}},{t:.3f});tl.set("#{i}",{{opacity:0}},{t + d:.3f});
tl.fromTo("#{i}b",{{x:-2600}},{{x:0,duration:.3,ease:"power4.out"}},{t:.3f});
tl.fromTo("#{i}x",{{scale:2.5,opacity:0}},{{scale:1,opacity:1,duration:.25,ease:"power4.in"}},{t + .1:.3f});
tl.fromTo("#{i}s",{{opacity:0}},{{opacity:1,duration:.3}},{t + .5:.3f});''')
        self.shake(t + .35)

    # ------------------------------------------------------------------ fx
    def flash(self, t, dr):
        self.at(f'tl.fromTo("#flash",{{opacity:.7}},{{opacity:0,duration:.16}},{t:.3f});'
                f'tl.fromTo("#speed",{{opacity:.8,x:0}},{{opacity:0,x:{-400 * dr},duration:.35}},{t:.3f});')

    def shake(self, t):
        self.at(f'tl.fromTo("#stage",{{x:0}},{{x:14,duration:.04,yoyo:true,repeat:5}},{t:.3f});tl.set("#stage",{{x:0}},{t + .25:.3f});')


CSS = f"""
@font-face {{ font-family: Anton; src: url(assets/Anton-Regular.ttf); }}
@font-face {{ font-family: InterB; src: url(assets/Inter-Bold.otf); }}
html, body {{ margin: 0; background: #000; }}
#root {{ position: relative; width: {W}px; height: {H}px; overflow: hidden; background: #0a0a0a; }}
#stage {{ position: absolute; inset: 0; }}
.clip {{ position: absolute; inset: 0; overflow: hidden; }}
.card {{ background: #0a0a0a; }}
.ph {{ position: absolute; inset: -7%; background-size: cover; background-position: center; }}
.vid {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }}
.ghost {{ opacity: 0; mix-blend-mode: screen; }}
.grade {{ position: absolute; inset: 0; background: radial-gradient(ellipse at center, rgba(0,0,0,0) 45%, rgba(0,0,0,.7) 100%); }}
#vig {{ position: absolute; inset: 0; background: radial-gradient(ellipse at center, rgba(0,0,0,0) 55%, rgba(0,0,0,.55) 100%); pointer-events: none; }}
#speed {{ position: absolute; inset: 0; opacity: 0; background: repeating-linear-gradient(90deg, rgba(255,255,255,0) 0 140px, rgba(255,255,255,.18) 140px 146px, rgba(255,255,255,0) 146px 380px); }}
#flash {{ position: absolute; inset: 0; background: #fff; opacity: 0; }}
.bar {{ position: absolute; left: -200px; height: 110px; width: 2600px; background: {RED}; transform: rotate(-8deg); }}
.stripe2 {{ position: absolute; left: 0; right: 0; top: 520px; height: 14px; background: {RED}; transform-origin: left center; }}
.num {{ position: absolute; font-family: Anton; color: #fff; font-size: 500px; line-height: 1; letter-spacing: -10px; transform: skewX(-10deg); }}
.big {{ position: absolute; font-family: Anton; color: #fff; text-transform: uppercase; transform: skewX(-10deg); white-space: nowrap; line-height: 1.02; text-shadow: 0 6px 24px rgba(0,0,0,.6); }}
.center {{ left: 0; width: {W}px; text-align: center; }}
.wrap {{ white-space: normal; left: 160px; width: {W - 320}px; }}
.tag {{ position: absolute; font-family: InterB; color: #fff; font-size: 30px; letter-spacing: 8px; text-transform: uppercase; }}
.tag.small {{ font-size: 24px; letter-spacing: 5px; color: rgba(255,255,255,.75); text-transform: none; }}
.chip {{ position: absolute; background: {RED}; color: #fff; font-family: Anton; font-size: 46px; padding: 6px 22px; transform: skewX(-10deg); text-transform: uppercase; }}
#stripe {{ position: absolute; left: 0; top: 0; bottom: 0; width: 16px; background: {RED}; }}
.hud {{ position: absolute; right: 70px; top: 60px; font-family: InterB; color: rgba(255,255,255,.9); font-size: 22px; letter-spacing: 6px; opacity: 0;
        background: rgba(0,0,0,.45); padding: 8px 16px; border-left: 6px solid {RED}; }}
.credit {{ position: absolute; left: 40px; bottom: 20px; font-family: InterB; font-size: 15px; color: rgba(255,255,255,.65); }}
.src {{ position: absolute; right: 70px; bottom: 50px; font-family: InterB; font-size: 20px; letter-spacing: 4px; color: rgba(255,255,255,.6); }}
.qs {{ position: absolute; left: 200px; top: 300px; }}
.q {{ font-family: Anton; color: #fff; font-size: 92px; text-transform: uppercase; transform: skewX(-10deg); margin-bottom: 26px; }}
.qn {{ background: {RED}; padding: 0 18px; margin-right: 30px; }}
"""


def build(wd, ep, proj, t_from=0.0, t_to=None):
    os.makedirs(os.path.join(proj, "assets"), exist_ok=True)
    for f in ("Anton-Regular.ttf", "Inter-Bold.otf"):
        shutil.copy(os.path.join(HERE, "fonts", f), os.path.join(proj, "assets", f))
    c = Comp(proj, wd, credits_map(wd))
    c.hud = []
    t, k, total = 0.0, 0, 0.0
    for ch in ep["chapters"]:
        for s in ch["shots"]:
            d = float(s["dur"])
            if (t_to is None or t < t_to) and t + d > t_from:
                getattr(c, s["type"], c.image)(s, t - t_from, d, k)
            t += d; k += 1
    total = (t_to if t_to is not None else t) - t_from
    shutil.copy(gsap_path(), os.path.join(proj, "assets", "gsap.min.js"))
    page = f"""<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>
<div id="root" data-composition-id="root" data-width="{W}" data-height="{H}" data-fps="{FPS}" data-duration="{total:.3f}">
<div id="stage">{''.join(c.els)}<div id="vig"></div><div id="speed"></div></div>
<div id="stripe"></div><div id="flash"></div></div>
<script src="assets/gsap.min.js"></script><script>
const tl = gsap.timeline({{ paused: true, defaults: {{ immediateRender: false }} }});
{chr(10).join(c.js)}
tl.set({{}}, {{}}, {total:.3f});
window.__timelines = window.__timelines || {{}}; window.__timelines["root"] = tl;
</script></body></html>"""
    open(os.path.join(proj, "index.html"), "w").write(page)
    return total


HF = os.environ.get("HF_DIR") or os.path.join(HERE, "..", ".hf")


def ensure_hf():
    if not os.path.exists(os.path.join(HF, "node_modules", "hyperframes")):
        os.makedirs(HF, exist_ok=True)
        sh(["npm", "init", "-y"], cwd=HF, stdout=subprocess.DEVNULL)
        sh(["npm", "i", "hyperframes@0.9.13", "gsap@3.12.5"], cwd=HF)
        subprocess.run(["npx", "hyperframes", "telemetry", "disable"], cwd=HF, capture_output=True)


def gsap_path():
    ensure_hf()
    return os.path.join(HF, "node_modules", "gsap", "dist", "gsap.min.js")


def mix_audio(wd, ep, out_wav, t_from, total):
    """narration per chapter + sfx + music, the same placement render_aus uses"""
    inputs, filters, t, n = [], [], 0.0, 0
    for ch in ep["chapters"]:
        dur = sum(float(s["dur"]) for s in ch["shots"])
        st = t + float(ch.get("lead_in", 0)) - t_from
        if st + dur > 0 and st < total:
            inputs += ["-i", os.path.join(wd, ch["audio"])]
            filters.append(f"[{n}:a]aresample=48000,aformat=channel_layouts=stereo,atrim=start={max(0, -st):.3f},adelay={max(0, st) * 1000:.0f}|{max(0, st) * 1000:.0f}[a{n}]")
            n += 1
        tt = t
        for s in ch["shots"]:
            for fx in s.get("sfx", []):
                at = tt + float(fx.get("at", 0)) - t_from
                if 0 <= at < total and os.path.exists(os.path.join(wd, fx["file"])):
                    inputs += ["-i", os.path.join(wd, fx["file"])]
                    filters.append(f"[{n}:a]aresample=48000,aformat=channel_layouts=stereo,volume={fx.get('gain', -20)}dB,adelay={at * 1000:.0f}|{at * 1000:.0f}[a{n}]")
                    n += 1
            tt += float(s["dur"])
        t += dur
    for m in ep.get("music", []):
        mp = os.path.join(wd, m["file"])
        if os.path.exists(mp):
            inputs += ["-stream_loop", "-1", "-i", mp]
            filters.append(f"[{n}:a]aresample=48000,aformat=channel_layouts=stereo,atrim=start={t_from:.3f}:duration={total:.3f},asetpts=PTS-STARTPTS,"
                           f"volume={m.get('gain', -29)}dB,afade=t=out:st={max(0, total - 4):.3f}:d=4[a{n}]")
            n += 1
    mix = "".join(f"[a{i}]" for i in range(n))
    filters.append(f"{mix}amix=inputs={n}:normalize=0,atrim=duration={total:.3f},loudnorm=I=-14:TP=-1.5:LRA=11[out]")
    sh(["ffmpeg", "-v", "error", "-y"] + inputs + ["-filter_complex", ";".join(filters), "-map", "[out]", "-ar", "48000", out_wav])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("workdir")
    ap.add_argument("--episode", default="episode.json")
    ap.add_argument("--out", default="")
    ap.add_argument("--from", dest="t_from", type=float, default=0.0)
    ap.add_argument("--to", dest="t_to", type=float, default=None)
    ap.add_argument("--workers", default="4")
    ap.add_argument("--quality", default="standard")
    a = ap.parse_args()
    wd = os.path.abspath(a.workdir)
    ep = json.load(open(os.path.join(wd, a.episode)))
    out = os.path.abspath(a.out or os.path.join(wd, ep["output"]))
    proj = os.path.join(wd, "hf_project")
    shutil.rmtree(proj, ignore_errors=True)
    total = build(wd, ep, proj, a.t_from, a.t_to)
    ensure_hf()
    silent = os.path.join(wd, "hf_visual.mp4")
    sh(["npx", "--prefix", HF, "hyperframes", "render", "-q", a.quality, "-w", a.workers, "-f", str(FPS), "-o", silent], cwd=proj)
    wav = os.path.join(wd, "hf_mix.wav")
    mix_audio(wd, ep, wav, a.t_from, total)
    subs = os.path.join(wd, ep.get("subtitles", "")) if ep.get("subtitles") else ""
    vf = []
    if subs and os.path.exists(subs) and a.t_from == 0:
        vf = ["-vf", f"subtitles={subs}:fontsdir={os.path.join(HERE, 'fonts')}"]
    sh(["ffmpeg", "-v", "error", "-y", "-i", silent, "-i", wav] + vf +
       ["-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out])
    print("->", out)


if __name__ == "__main__":
    main()
