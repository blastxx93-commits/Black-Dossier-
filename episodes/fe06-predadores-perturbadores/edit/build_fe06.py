#!/usr/bin/env python3
"""FE06: "10 Predadores Que Caçam de Forma Perturbadora" — theme "sombrio", list format, 80%+ real footage.
Each chapter: a 'caso' card, then one real shot per paragraph sentence group (cues = start of each paragraph)."""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "engine"))
import aus_kit as A
import feras_kit as F
from feras_kit import foot, hf

F.use_cinema("sombrio")
F.MOTION_CYCLE[:] = ["parallax", "push", "pan_l", "parallax", "pull", "diag", "parallax", "pan_r", "focus"]
PHOTOS = {"mantis": ["p_mantis", "p_mantisbird", "ai:ai_mantis_bird"], "wasp": ["p_jwasp"], "croc": ["p_croc"], "komodo": ["p_komodo", "p_komodoisland"],
          "orca": ["p_orca", "p_seal", "ai:ai_orca_wave"], "deep": ["p_angler", "ai:ai_angler"], "spider": ["p_spitting", "p_bolas"],
          "snake": ["p_anaconda"], "octo": ["p_octopus"], "cat": ["p_cat"], "dark": []}
CL = json.load(open(os.path.join(HERE, "clips.json")))
CL = {k: v + [c + "@4.5" for c in v] for k, v in CL.items()}   # each 8 s clip also gives a second segment
CLIPS = {"mantis": CL["mantis"] + CL["bird"], "wasp": CL["wasp"] + CL["roach"], "croc": CL["croc"] + CL["zebra"], "komodo": CL["komodo"],
         "orca": CL["orca"] + CL["seal"], "deep": CL["deep"], "spider": CL["spider"], "snake": CL["snake"] + CL["capi"], "octo": CL["octo"],
         "cat": CL["cat"], "dark": CL["dark"]}
FALLBACK = {k: ["dark"] for k in PHOTOS}
A.setup(sys.argv[1], os.path.join(HERE, "skip.json"), PHOTOS, CLIPS, CL["dark"], FALLBACK, ["dark"])
A.CLIP_TARGET = 0.8
A.MAX_HOLD, A.KEEP = 6.0, 4.0
ROUNDS = [  # chapter, number, name, scene, meta
    ("ch01", 10, "Louva-a-deus", "mantis", [["Arma", "Patas-armadilha"], ["Ataque", "< 0,1 s"]]),
    ("ch02", 9, "Vespa-joia", "wasp", [["Arma", "Veneno no cérebro"], ["Vítima", "Barata"]]),
    ("ch03", 8, "Crocodilo-de-água-salgada", "croc", [["Tamanho", "6+ m"], ["Técnica", "Rolo da morte"]]),
    ("ch04", 7, "Dragão-de-komodo", "komodo", [["Tamanho", "3 m"], ["Arma", "Veneno"]]),
    ("ch05", 6, "Orca", "orca", [["Habitat", "Todos os oceanos"], ["Técnica", "Caça em grupo"]]),
    ("ch06", 5, "Peixe-pescador", "deep", [["Profundidade", "1.000+ m"], ["Isca", "Luz própria"]]),
    ("ch07", 4, "Aranha-de-cuspe", "spider", [["Arma", "Cola + veneno"], ["Teia", "Não precisa"]]),
    ("ch08", 3, "Sucuri", "snake", [["Peso", "100+ kg"], ["Habitat", "Brasil"]]),
    ("ch09", 2, "Polvo", "octo", [["Cérebros", "9"], ["Arma", "Bico + saliva tóxica"]]),
    ("ch10", 1, "Gato doméstico", "cat", [["Vítimas/ano", "Bilhões"], ["Motivo", "Instinto"]]),
]
NARR = os.path.join(HERE, "..", "narration")


def cues(name):
    """Start words of every sentence (one shot per sentence, the long holds are split by the kit)."""
    t = open(os.path.join(NARR, name + ".txt")).read()
    out = []
    for s in re.split(r"(?<=[.!?])\s+", t.strip()):
        w = s.split()
        if len(w) >= 4:
            out.append(" ".join(w[:4]).rstrip(",.;:!?"))
    return out


ch = A.ch
chapters = []
c = ch("ch00_hook")
c.at(0, foot("wasp"))
for k, p in enumerate(cues("ch00_hook")[1:]):
    if p.startswith("Isso não é"):
        c.at(p, hf("frase", text="Isso não é um filme de *terror.*", img="scene:dark"))
    elif p.startswith("Hoje, você vai"):
        c.at(p, hf("titulo", kicker="Era das Feras", title="10 predadores|perturbadores", sub="Caçadores que parecem saídos de um filme de terror", img="scene:croc", blurin=True))
    else:
        c.at(p, foot(["wasp", "croc", "komodo", "snake", "octo", "cat"][k % 6]))
chapters.append(c)
for name, num, title, scene, meta in ROUNDS:
    c = ch(name)
    cs = cues(name)
    if name == "ch06":   # subscribe call before the case
        c.at(0, hf("cta", img="scene:dark", text="Curtindo o lado sombrio?", sub="Deixa o like e se inscreve no canal"))
        i = next(k for k, p in enumerate(cs) if p.startswith("O peixe-sapo"))
        c.at(cs[i], hf("caso", num=num, name=title, meta=meta, img=f"scene:{scene}", label="Caso"))
        cs = cs[i + 1:]
    else:
        c.at(0, hf("caso", num=num, name=title, meta=meta, img=f"scene:{scene}", label="Caso"))
        cs = cs[1:]
    for p in cs:
        if p.startswith(("E você, conhecia", "E se você")):
            c.at(p, hf("cta", img="scene:cat", text="Obrigado por assistir", sub="Deixa o like e se inscreve no Era das Feras")); break
        c.at(p, foot(scene))
    chapters.append(c)

ctxs = ["dark"] + [r[3] for r in ROUNDS]
ep = json.loads(A.finish(chapters, "FE06_10_Predadores_Perturbadores.mp4", ctx=ctxs, music_gain=-24))
ep = F.cut_rhythm(ep, {k: [f"/{k}"] for k in PHOTOS})
F.export_hf_theme(ep, os.path.join(HERE, "hf_cards.json"))
t = 0.0; starts = []
for chap in ep["chapters"]:
    starts.append(t); t += sum(s["dur"] for s in chap["shots"])
moods = [(0, "horror"), (starts[1], "misterio"), (starts[3], "tensao"), (starts[6], "misterio"), (starts[8], "tensao"), (starts[10], "revelacao")]
ep["music"] = [{"file": f"musica/{m}.mp3", "start": round(max(0, a - 1.5), 2), "end": round(min(t, (moods[k + 1][0] if k + 1 < len(moods) else t) + 1.5), 2),
                "gain": -24, "fade_in": 3.0, "fade_out": 3.0} for k, (a, m) in enumerate(moods)]
vid = sum(s["dur"] for c in ep["chapters"] for s in c["shots"] if s["type"] == "video" and not s.get("hfcard"))
img = sum(s["dur"] for c in ep["chapters"] for s in c["shots"] if s["type"] == "image")
ai = sum(s["dur"] for c in ep["chapters"] for s in c["shots"] if s["type"] == "image" and "/ai/" in s["src"])
sys.stderr.write(f"{t / 60:.1f} min; real {(vid + img - ai) / max(1, vid + img):.0%} do tempo de cena (IA {ai:.0f}s)\n")
print(json.dumps(ep, indent=1, ensure_ascii=False))
