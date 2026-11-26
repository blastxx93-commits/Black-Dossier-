#!/usr/bin/env python3
"""FE07: "8 Animais Que Ninguém Deveria Tocar" — theme "sombrio", list format, 80%+ real footage.
Each chapter: a 'caso' card, then one real shot per paragraph sentence group (cues = start of each paragraph)."""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "engine"))
import aus_kit as A
import feras_kit as F
from feras_kit import foot, hf

F.use_cinema("sombrio")
F.MOTION_CYCLE[:] = ["parallax", "push", "pan_l", "parallax", "pull", "diag", "parallax", "pan_r", "focus"]
PHOTOS = {"lion": ["p_lion"], "scorp": ["p_scorp", "p_scorpuv"], "cater": ["p_lonomia", "p_cater", "ai:ai_lonomia_tree"], "ray": ["p_ray", "p_ray2"],
          "puffer": ["p_puffer", "p_fugu"], "frog": ["p_frog", "p_frog2"], "jelly": ["p_jelly", "p_vinegar"], "stone": ["p_stone", "p_stone2"], "dark": []}
CL = json.load(open(os.path.join(HERE, "clips.json")))
CLIPS = {"lion": CL["lion"] + CL["reef"][:5], "scorp": CL["scorp"], "cater": CL["cater"], "ray": CL["ray"] + CL["beach"][:4], "puffer": CL["puffer"] + ["v_puffer/1", "v_puffer/2"] + CL["reef"][5:10] + [c + "@4" for c in ["v_puffer/1", "v_puffer/2", "v_puffer/4"]],
         "frog": CL["frog"], "jelly": CL["jelly"], "stone": CL["reef"][10:] + CL["beach"][4:], "dark": CL["dark"]}
CLIPS = {k: v + [c + o for o in ("@2.8", "@5.6") for c in v if "@" not in c] for k, v in CLIPS.items()}   # last resort: a later moment of the same clip
FALLBACK = {k: ["dark"] for k in PHOTOS}
A.setup(sys.argv[1], os.path.join(HERE, "skip.json"), PHOTOS, CLIPS, CL["dark"], FALLBACK, ["dark"])
A.CLIP_TARGET = 0.75
A.MAX_HOLD, A.KEEP = 6.0, 4.0
ROUNDS = [
    ("ch01", 8, "Peixe-leão", "lion", [["Arma", "Espinhos venenosos"], ["Invasor", "Atlântico"]]),
    ("ch02", 7, "Escorpião-amarelo", "scorp", [["Acidentes", "100 mil+/ano"], ["Onde", "Cidades"]]),
    ("ch03", 6, "Taturana (Lonomia)", "cater", [["Veneno", "Anticoagulante"], ["Onde", "Sul do Brasil"]]),
    ("ch04", 5, "Arraia", "ray", [["Arma", "Ferrão serrilhado"], ["Onde", "Rios e mar"]]),
    ("ch05", 4, "Baiacu", "puffer", [["Toxina", "Tetrodotoxina"], ["Antídoto", "Não existe"]]),
    ("ch06", 3, "Sapo-dardo", "frog", [["Tamanho", "Ponta do dedo"], ["Veneno", "Da dieta"]]),
    ("ch07", 2, "Água-viva-caixa", "jelly", [["Tentáculos", "Até 3 m"], ["Olhos", "24"]]),
    ("ch08", 1, "Peixe-pedra", "stone", [["Espinhos", "13"], ["Título", "Peixe mais venenoso"]]),
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
c.at(0, foot("stone"))
for k, p in enumerate(cues("ch00_hook")[1:]):
    if p.startswith("Na natureza, os"):
        c.at(p, hf("frase", text="Os mais perigosos são *pequenos.*", img="scene:dark"))
    elif p.startswith("Hoje, você vai"):
        c.at(p, hf("titulo", kicker="Era das Feras", title="Não toque|nesses animais", sub="8 animais que ninguém deveria tocar", img="scene:frog", blurin=True))
    else:
        c.at(p, foot(["stone", "lion", "jelly", "frog", "scorp", "ray"][k % 6]))
chapters.append(c)
for name, num, title, scene, meta in ROUNDS:
    c = ch(name)
    cs = cues(name)
    if name == "ch05":   # subscribe call before the case
        c.at(0, hf("cta", img="scene:dark", text="Está gostando?", sub="Deixa o like e se inscreve no canal"))
        i = next(k for k, p in enumerate(cs) if p.startswith("Quando se sente"))
        c.at("Número quatro", hf("caso", num=num, name=title, meta=meta, img=f"scene:{scene}", label="Caso"))
        cs = cs[i:]
    else:
        c.at(0, hf("caso", num=num, name=title, meta=meta, img=f"scene:{scene}", label="Caso"))
        cs = cs[1:]
    for p in cs:
        if p.startswith(("E você, conhecia", "E se você")):
            c.at(p, hf("cta", img="scene:stone", text="Obrigado por assistir", sub="Deixa o like e se inscreve no Era das Feras")); break
        c.at(p, foot(scene))
    chapters.append(c)

ctxs = ["dark"] + [r[3] for r in ROUNDS]
ep = json.loads(A.finish(chapters, "FE07_8_Animais_Que_Ninguem_Deveria_Tocar.mp4", ctx=ctxs, music_gain=-24))
ep = F.cut_rhythm(ep, {k: [f"/{k}"] for k in PHOTOS})
F.export_hf_theme(ep, os.path.join(HERE, "hf_cards.json"))
t = 0.0; starts = []
for chap in ep["chapters"]:
    starts.append(t); t += sum(s["dur"] for s in chap["shots"])
moods = [(0, "horror"), (starts[1], "misterio"), (starts[3], "tensao"), (starts[5], "misterio"), (starts[7], "tensao"), (starts[8], "revelacao")]
ep["music"] = [{"file": f"musica/{m}.mp3", "start": round(max(0, a - 1.5), 2), "end": round(min(t, (moods[k + 1][0] if k + 1 < len(moods) else t) + 1.5), 2),
                "gain": -24, "fade_in": 3.0, "fade_out": 3.0} for k, (a, m) in enumerate(moods)]
vid = sum(s["dur"] for c in ep["chapters"] for s in c["shots"] if s["type"] == "video" and not s.get("hfcard"))
img = sum(s["dur"] for c in ep["chapters"] for s in c["shots"] if s["type"] == "image")
ai = sum(s["dur"] for c in ep["chapters"] for s in c["shots"] if s["type"] == "image" and "/ai/" in s["src"])
sys.stderr.write(f"{t / 60:.1f} min; real {(vid + img - ai) / max(1, vid + img):.0%} do tempo de cena (IA {ai:.0f}s)\n")
print(json.dumps(ep, indent=1, ensure_ascii=False))
