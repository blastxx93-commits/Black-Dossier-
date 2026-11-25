"""Markup of the HyperFrames theme "gelo" (fe05+): duel arena, condensed type, glacial blue, snow particles.
Kinds: titulo, rodada, versus, veredito, placar, ficha, rotulo, frase, escala, mapa (world), perguntas, cta."""
import html, json, os

E = html.escape
HF = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hf")


def masked(text):
    return " ".join(f'<span class="mask"><span>{E(w)}</span></span>' for w in text.split())


def fx(c, snow=True, n=46):
    s = '<div class="cold"></div><div class="vig"></div>'
    if snow and c.get("snow", True):
        s += '<div class="snow">' + "".join(f'<i style="width:{2 + (k * 7) % 5}px;height:{2 + (k * 7) % 5}px;opacity:{0.35 + (k % 5) * 0.12:.2f}"></i>' for k in range(n)) + "</div>"
    return s + '<div class="sweep"></div><div class="scan"></div><div class="grain"></div>'


def bg(c, key="_img", tint="full"):
    return (f'<div class="bg"><img src="{c[key]}"></div>' if c.get(key) else "") + f'<div class="tint {tint}"></div>'


WORLD = None


def mapa(c):
    global WORLD
    WORLD = WORLD or json.load(open(os.path.join(HF, "vendor", "world.json")))
    k = 1920 / 360
    px, py = 960 + c["lon"] * k, 540 - c["lat"] * k
    c["px"], c["py"] = round(px, 1), round(py, 1)
    paths = "".join(f'<path d="{x["d"]}"/>' for x in WORLD["countries"])
    pin = f'<div class="ring" style="left:{px:.0f}px;top:{py:.0f}px"></div>' * 2 + f'<div class="pin" style="left:{px:.0f}px;top:{py:.0f}px"></div>'
    return (f'<div class="stage"><svg viewBox="0 0 1920 1080">{paths}</svg>{pin}</div><div class="tint" style="background:linear-gradient(0deg,rgba(6,17,28,.9),rgba(6,17,28,0) 55%)"></div>'
            f'<div class="info"><span class="chip">{E(c["kicker"])}</span><h3 class="disp">{masked(c["title"])}</h3><div class="sub">{E(c.get("sub", ""))}</div></div>'
            + fx(c, snow=False))


def body(c):
    k = c["kind"]
    if k == "titulo":
        t1, _, t2 = c["title"].partition("|")
        h = masked(t1) + (f'<br><span class="l2">{masked(t2)}</span>' if t2 else "")
        return bg(c, tint="side") + fx(c) + (f'<div class="box"><span class="chip">{E(c["kicker"])}</span><h1 class="disp">{h}</h1>'
                                             f'<div class="line"></div><div class="sub">{E(c.get("sub", ""))}</div></div>')
    if k == "rodada":
        pips = "".join(f'<b class="{"on" if i < c["num"] else ""}"></b>' for i in range(c.get("of", 5)))
        return (f'<div class="pane"><div class="bg"><img src="{c["_img"]}"></div><div class="tint"></div></div>'
                f'<div class="num">{c["num"]}<span class="fill">{c["num"]}</span></div>'
                f'<div class="box"><div class="lab">{E(c.get("label", "Rodada"))}</div><h2 class="disp">{masked(c["name"])}</h2>'
                f'<span class="chip red">{E(c["when"])}</span><div class="era">{E(c.get("sub", ""))}</div></div><div class="pips">{pips}</div>' + fx(c))
    if k == "versus":
        def side(s, im, d):
            stats = "".join(f'<div class="stat"><span class="k">{E(a)}</span><span class="bar" style="width:{max(40, b)}px"></span><span class="v">{E(v)}</span></div>'
                            for a, v, b in d["stats"])
            return (f'<div class="side {s}"><span class="chip{"" if s == "l" else " red"}">{E(d["kicker"])}</span>'
                    f'<h3 class="disp">{masked(d["name"])}</h3>{stats}</div>')
        return (f'<div class="pane l"><div class="bg"><img src="{c["_limg"]}"></div><div class="tint"></div></div>'
                f'<div class="pane r"><div class="bg"><img src="{c["_rimg"]}"></div><div class="tint"></div></div><div class="seam"></div>'
                f'<div class="vs">VS</div>' + side("l", "_limg", c["left"]) + side("r", "_rimg", c["right"]) + fx(c, snow=False))
    if k == "veredito":
        cls = {"win": "", "loss": "loss", "tie": "tie"}[c["result"]]
        return bg(c, tint="full") + fx(c, snow=False) + (f'<div class="flash"></div><div class="stamp {cls}"><div class="k">{E(c.get("kicker", "Veredito"))}</div>'
                                                         f'<div class="t">{E(c["text"]).replace("|", "<br>")}</div></div>')
    if k == "placar":
        (a0, b0), (a1, b1) = c["prev"], c["now"]
        dg = lambda o, n: f'<div class="digit"><span class="o">{o}</span><span class="n">{n}</span></div>'
        return (bg(c, tint="full") + fx(c) + f'<div class="box"><div class="col l"><div class="who">{E(c.get("left", "Urso polar"))}</div>{dg(a0, a1)}</div>'
                f'<div class="col r"><div class="who">{E(c.get("right", "Feras"))}</div>{dg(b0, b1)}</div></div><div class="mid">×</div>'
                f'<div class="sub">{E(c.get("sub", ""))}</div>')
    if k == "ficha":
        rows = "".join(f'<div class="row"><span class="k">{E(a)}</span><span class="v">{E(b)}</span></div>' for a, b in c["rows"])
        return (f'<div class="pane bg"><img src="{c["_img"]}"></div><div class="tint" style="background:linear-gradient(90deg,rgba(6,17,28,0) 40%,rgba(6,17,28,.9) 70%)"></div>'
                + fx(c) + f'<div class="panel"><span class="chip">{E(c.get("kicker", "Ficha"))}</span><h3 class="disp">{masked(c["name"])}</h3>'
                f'<div class="sci">{E(c.get("sci", ""))}</div>{rows}</div>')
    if k == "rotulo":
        side = " r" if c.get("side") == "right" else ""
        sci = f'<div class="sci">{E(c["sci"])}</div>' if c.get("sci") else ""
        return bg(c, tint="") + fx(c) + (f'<div class="lt{side}"><span class="chip{" red" if c.get("enemy") else ""}">{E(c["kicker"])}</span>'
                                        f'<div class="name disp">{masked(c["name"])}</div><div class="line"></div>{sci}</div>')
    if k == "frase":
        ws = "".join(f'<span class="w{" em" if w.startswith("*") else ""}">{E(w.strip("*"))}</span>' for w in c["text"].split())
        return bg(c, tint="full") + fx(c) + f'<div class="box"><p>{ws}</p></div>'
    if k == "escala":
        mx = max(r[1] for r in c["rows"])
        cols = "".join(f'<div class="c {r[2] if len(r) > 2 else ""}"><div class="v">{str(r[1]).replace(".", ",")} m</div>'
                       f'<div class="b" style="height:{r[1] / mx * 560:.0f}px"></div><div class="n">{E(r[0])}</div></div>' for r in c["rows"])
        return (bg(c, tint="full") + fx(c) + f'<div class="ttl"><span class="chip">{E(c["kicker"])}</span><h3 class="disp">{masked(c["title"])}</h3></div>'
                f'<div class="floor"></div><div class="cols">{cols}</div>')
    if k == "caso":
        meta = "".join(f'<span>{E(a)}: <b>{E(b)}</b></span>' for a, b in c.get("meta", []))
        return bg(c, tint="side") + fx(c, n=24) + (f'<div class="num">{c["num"]}</div><div class="box"><div class="lab">{E(c.get("label", "Caso"))} nº {c["num"]}</div>'
                                                  f'<h2 class="disp">{masked(c["name"])}</h2><div class="meta">{meta}</div></div>')
    if k == "mapa":
        return mapa(c)
    if k == "perguntas":
        qs = "".join(f'<div class="q"><span class="i">{i + 1:02d}</span><span class="t">{masked(t)}</span></div>' for i, t in enumerate(c["items"]))
        return bg(c, tint="full") + fx(c) + f'<div class="box">{qs}</div>'
    if k == "cta":
        bell = ('<svg class="bell" viewBox="0 0 24 24" fill="#eaf4fb"><path d="M12 22a2.5 2.5 0 0 0 2.45-2h-4.9A2.5 2.5 0 0 0 12 22zm7-6V11a7 7 0 0 0-5.5-6.84V3.5a1.5 1.5 0 0 0-3 0v.66A7 7 0 0 0 5 11v5l-2 2v1h18v-1z"/></svg>')
        return bg(c, tint="full") + fx(c) + (f'<div class="box"><h3 class="disp">{masked(c["text"])}</h3><div class="btn">{bell}INSCREVA-SE</div>'
                                             f'<div class="sub">{E(c.get("sub", ""))}</div></div>')
    raise SystemExit(f"tipo de cartela desconhecido no tema gelo: {k}")
