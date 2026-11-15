#!/usr/bin/env python3
"""FE05 (Era das Feras): "Urso Polar vs. os Maiores Ursos da Pré-História" — theme "gelo", cinema sound kit, 2.5D camera.
    python3 build_fe05.py <narration_dir> > episode.json   (run from the work folder)"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "engine"))
import aus_kit as A
import feras_kit as F
from feras_kit import foot, hf

F.use_cinema("gelo")
ai = lambda *n: ["ai:ai_%02d" % k for k in n]
PHOTOS = {
    "polar": ai(27, 28, 30) + ["p_polar", "p_polar2"],
    "gelo": ["p_seaice"],
    "amphi": ai(1, 2, 3) + ["p_amphicyon"],
    "agrio": ai(6, 7, 8) + ["p_agrio"],
    "cave": ai(11, 12, 13, 14, 32) + ["p_cavebear", "p_bearcave"],
    "short": ai(16, 17, 18, 19) + ["p_arctodus"],
    "arcto": ai(21, 22, 23, 26) + ["p_arctotherium"],
    "duelo": ai(4, 5, 10, 15, 20, 25),
    "mioceno": ai(35), "plioceno": ai(36), "pampa": ai(37) + ["p_pampas"], "fossil": ai(31),
}
CL = json.load(open(os.path.join(HERE, "clips.json")))
CLIPS = {"polar": CL["polar"] + CL["presa"], "gelo": CL["gelo"], "amphi": CL["brown"][:3], "agrio": CL["brown"][3:6] + CL["savana"][3:5],
         "cave": CL["brown"][6:9], "short": CL["brown"][9:12] + CL["eragelo"], "arcto": CL["brown"][12:], "mioceno": CL["savana"][:3],
         "plioceno": CL["savana"][5:], "derrete": CL["derrete"]}
GENERIC = CL["gelo"]
FALLBACK = {k: ["gelo", "polar"] for k in PHOTOS}
FALLBACK.update({"amphi": ["mioceno", "duelo"], "agrio": ["plioceno", "duelo"], "cave": ["duelo", "gelo"], "short": ["duelo", "gelo"],
                 "arcto": ["pampa", "duelo"], "pampa": ["arcto"], "fossil": ["cave"], "derrete": ["gelo", "polar"]})
PIN_IDS = ["ai_27", "ai_28", "ai_30", "ai_02", "ai_07", "ai_13", "ai_18", "ai_23", "ai_22", "ai_26", "ai_05", "ai_10", "ai_15", "ai_20", "ai_25", "ai_04"]
A.setup(sys.argv[1], os.path.join(HERE, "skip.json"), PHOTOS, CLIPS, GENERIC, FALLBACK, ["gelo"])
F.pin(*PIN_IDS)
A.CLIP_TARGET = 0.45
A.MAX_HOLD, A.KEEP = 6.8, 4.4
ch = A.ch
chapters = []
SC = [0, 0]
PB = {"kicker": "Hoje", "name": "Urso polar"}


def rodada(c, num, name, when, sub, img):
    c.at(0, hf("rodada", num=num, name=name, when=when, sub=sub, img=img, of=5))


def vs(c, phrase, limg, rimg, rname, rkick, peso, alt):
    c.at(phrase, hf("versus", limg=limg, rimg=rimg,
                    left=dict(PB, stats=[["Peso", "700 kg", 300], ["Em pé", "3 m", 280]]),
                    right={"kicker": rkick, "name": rname, "stats": [["Peso", peso[0], peso[1]], ["Em pé", alt[0], alt[1]]]}))


def veredito(c, phrase, img, result, text, now, sub=""):
    """Returns the score card that follows a verdict (the verdict card itself is placed by the caller)."""
    s = hf("placar", img="scene:gelo", prev=list(SC), now=list(now), sub=sub)
    s["sfx"] = F.placar_sfx(SC, now)
    SC[:] = now
    return s


# ---------------------------------------------------------------- hook
c = ch("ch00_hook")
c.at(0, hf("frase", text="*700* quilos.", img="ai_27", blurin=True))
c.at("Três metros de altura", foot("polar"))
c.at("Um faro capaz", foot("polar"))
c.at("O urso polar é o maior", hf("rotulo", img="scene:polar", kicker="O maior carnívoro terrestre", name="Urso polar", sci="Ursus maritimus"))
c.at("Nenhum animal caça", foot("polar"))
c.at("Mas ele chegou tarde demais", hf("frase", text="Ele chegou *tarde* demais.", img="scene:gelo"))
c.at("Muito antes dele", foot("short"))
c.at("Um deles, em pé", foot("arcto"))
c.at("E esse gigante não vivia", hf("mapa", kicker="Onde ele viveu", title="América do Sul", sub="O maior urso de todos os tempos", lon=-58.4, lat=-34.6))
c.at("Hoje, o urso polar vai enfrentar", foot("duelo"))
c.at("Cinco rodadas", hf("frase", text="5 rodadas. 5 *gigantes.*", img="scene:duelo"))
c.at("E eu já adianto", foot("arcto"))
c.at("não é nenhum que você conhece", hf("titulo", kicker="Era das Feras", title="Urso polar|vs. gigantes", sub="Os maiores ursos que já existiram", img="ai_30", blurin=True))
chapters.append(c)

c = ch("ch01")
c.at(0, foot("polar"))
c.at("Um macho adulto", hf("ficha", img="scene:polar", kicker="O competidor", name="Urso polar", sci="Ursus maritimus",
                         rows=[["Peso", "400–700 kg"], ["Em pé", "3 m"], ["Faro", "+1 km"], ["Dieta", "Focas"]]))
c.at("Ele nada por dias", foot("polar"))
c.at("O faro dele", foot("polar"))
c.at("Depois espera", foot("gelo"))
c.at("Quando a foca sobe", foot("polar"))
c.at("E tem um detalhe", hf("frase", text="A pele dele é *preta.*", img="scene:polar"))
c.at("Os pelos são transparentes", foot("polar"))
c.at("As patas dianteiras", foot("polar"))
c.at("E ele aguenta", foot("gelo"))
c.at("Força, faro", foot("polar"))
c.at("As regras são simples", foot("duelo"))
c.at("Agora, vamos ver", foot("gelo"))
chapters.append(c)

c = ch("ch02")
rodada(c, 1, "Anficião", "Há 15 milhões de anos", "O cão-urso · Europa e América do Norte", "ai_02")
c.at("O primeiro adversário", foot("amphi"))
c.at("As maiores espécies", foot("amphi"))
c.at("O mundo dele", foot("mioceno"))
c.at("Imagina o encontro", foot("amphi"))
vs(c, "Mas o urso polar tem vantagem", "scene:polar", "ai_05", "Anficião", "15 milhões de anos", ("500 kg", 210), ("2,5 m", 230))
c.at("Veredito: vitória do urso polar", hf("veredito", img="ai_04", result="win", text="Vitória do|urso polar"))
c.at("Um a zero", veredito(c, "", "ai_04", "win", "", [1, 0]))
c.at("Só que o próximo", foot("agrio"))
chapters.append(c)

c = ch("ch03")
rodada(c, 2, "Agriotério", "Há 4 milhões de anos", "O urso buldogue · África, Eurásia e América", "ai_07")
c.at("Esse é o Agriotério", foot("agrio"))
c.at("O focinho curto", foot("agrio"))
c.at("Ele foi um dos ursos", foot("plioceno"))
c.at("O crânio do Agriotério", foot("agrio"))
vs(c, "Aqui a luta fica equilibrada", "scene:polar", "ai_10", "Agriotério", "4 milhões de anos", ("700 kg", 300), ("3 m", 280))
c.at("Numa luta assim", foot("duelo"))
c.at("Veredito: empate", hf("veredito", img="ai_10", result="tie", text="Empate"))
c.at("O placar fica", veredito(c, "", "ai_10", "tie", "", [1, 0], "1 empate"))
c.at("E daqui para frente", foot("cave"))
chapters.append(c)

c = ch("ch04")
rodada(c, 3, "Urso-das-cavernas", "Há 50 mil anos", "Europa da Era do Gelo", "ai_13")
c.at("Os machos podiam", foot("cave"))
c.at("O crânio de um macho", foot("cave"))
c.at("Ele dividia a Europa", foot("cave"))
vs(c, "Um gigante vegetariano", "ai_30", "ai_15", "Urso-das-cavernas", "50 mil anos", ("500 kg", 210), ("2,7 m", 250))
c.at("Mesmo assim", foot("cave"))
c.at("Veredito: vitória do urso polar", hf("veredito", img="ai_15", result="win", text="Vitória do|urso polar"))
c.at("Dois a zero", veredito(c, "", "ai_15", "win", "", [2, 0], "1 empate"))
c.at("Antes da próxima rodada", hf("cta", img="scene:gelo", text="Está curtindo?", sub="Deixa o like e se inscreve no canal"))
chapters.append(c)

c = ch("ch05")
rodada(c, 4, "Urso-de-cara-achatada", "Há 20 mil anos", "América do Norte", "ai_18")
c.at("Em pé, ele passava", hf("escala", img="scene:short", kicker="Em pé", title="Quem é mais alto?",
                             rows=[["Humano", 1.75, "hum"], ["Urso polar", 3.0], ["Cara-achatada", 3.4, "top"]]))
c.at("Durante muito tempo", foot("short"))
c.at("O mundo dele", foot("short"))
c.at("O focinho curto", foot("short"))
vs(c, "Mas, numa briga", "scene:polar", "ai_20", "Cara-achatada", "20 mil anos", ("900 kg", 380), ("3,4 m", 320))
c.at("Imagina os dois", foot("duelo"))
c.at("Veredito: vitória do urso-de-cara-achatada", hf("veredito", img="ai_20", result="loss", text="Vitória do|cara-achatada"))
c.at("Dois a um", veredito(c, "", "ai_20", "loss", "", [2, 1], "1 empate"))
c.at("E ele nem é o maior", foot("arcto"))
chapters.append(c)

c = ch("ch06")
rodada(c, 5, "Arctotério", "Há 1 milhão de anos", "Pampas da Argentina · a final", "ai_23")
c.at("O maior urso que já existiu", hf("rotulo", img="ai_22", kicker="O maior urso da história", name="Arctotério", sci="Arctotherium angustidens", enemy=True))
c.at("Para ter uma ideia", foot("arcto"))
c.at("Os ursos chegaram", foot("pampa"))
c.at("Parentes menores dele", foot("arcto"))
c.at("O mais curioso", foot("arcto"))
vs(c, "Na luta final", "scene:polar", "ai_25", "Arctotério", "1 milhão de anos", ("1.600 kg", 600), ("3,6 m", 340))
c.at("Contra um urso", foot("duelo"))
c.at("Veredito: vitória do Arctotério", hf("veredito", img="ai_26", result="loss", text="Vitória do|Arctotério"))
c.at("Placar final", veredito(c, "", "ai_26", "loss", "", [2, 2], "1 empate · placar final"))
chapters.append(c)

c = ch("ch07")
c.at(0, foot("polar"))
c.at("O Anficião, o Agriotério", foot("fossil"))
c.at("O urso-de-cara-achatada e o Arctotério", foot("short"))
c.at("E o urso polar também é jovem", foot("polar"))
c.at("Hoje, o maior adversário", foot("derrete"))
c.at("Sem o gelo do mar", foot("derrete"))
c.at("Os gigantes do passado", hf("frase", text="O verdadeiro rival é o *clima.*", img="scene:derrete"))
c.at("E você, concorda", foot("polar"))
c.at("Se curtiu", hf("cta", img="scene:polar", text="Obrigado por assistir", sub="Deixa o like e se inscreve no Era das Feras"))
chapters.append(c)

MOODS = [("ch00_hook", 0, "tensao"), ("ch01", 0, "frio"), ("ch02", 0, "epico"), ("ch04", 0, "tensao"), ("ch05", 0, "epico"),
         ("ch06", 0, "tensao"), ("ch07", 0, "drama")]
ctxs = ["polar", "polar", "amphi", "agrio", "cave", "short", "arcto", "polar"]
SCENE_OF = {"polar": ["ai_27", "ai_28", "ai_30", "p_polar"], "gelo": ["p_seaice"], "amphi": ["ai_01", "ai_02", "ai_03"], "agrio": ["ai_06", "ai_07", "ai_08"],
            "cave": ["ai_11", "ai_12", "ai_13", "ai_14"], "short": ["ai_16", "ai_17", "ai_18", "ai_19"], "arcto": ["ai_21", "ai_22", "ai_23"],
            "duelo": ["ai_04", "ai_05", "ai_10", "ai_15"], "pampa": ["ai_37", "p_pampas"], "derrete": ["ai_30"]}
ep = json.loads(A.finish(chapters, "FE05_Urso_Polar_vs_Ursos_Gigantes.mp4", ctx=ctxs, music_gain=-25))
ep = F.cut_rhythm(ep, SCENE_OF)
F.export_hf_theme(ep, os.path.join(HERE, "hf_cards.json"))
starts, t = {}, 0.0
for chap, c in zip(ep["chapters"], chapters):
    starts[c.name] = t; t += sum(s["dur"] for s in chap["shots"])
total = t; marks = []
for name, phrase, mood in MOODS:
    c = next(x for x in chapters if x.name == name); off = 0.0
    if phrase:
        c.cursor = 0; off = c.find(phrase) or 0.0
    marks.append((starts[name] + off, mood))
music = []
for k, (st, mood) in enumerate(marks):
    en = marks[k + 1][0] if k + 1 < len(marks) else total
    music.append({"file": f"musica/{mood}.mp3", "start": round(max(0.0, st - 1.5), 2), "end": round(min(total, en + 1.5), 2),
                  "gain": -25, "fade_in": 3.0, "fade_out": 3.0})
ep["music"] = music
sys.stderr.write(f"trilha: {len(music)} trechos, {total / 60:.1f} min; frases não achadas: {[m for c in chapters for m in c.misses]}\n")
print(json.dumps(ep, indent=1, ensure_ascii=False))
