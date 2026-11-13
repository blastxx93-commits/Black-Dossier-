#!/usr/bin/env python3
"""FE02 (Era das Feras): "Pastor Alemão ou Malinois: Qual Sobreviveria a Cada Era Pré-Histórica?"
    python3 build_fe02.py <narration_dir> > episode.json      (run from the work folder: a/ = assets, audio/ = narration)
Score = rounds survived: [Pastor, Malinois] (the HUD shows PASTOR × MALINOIS).
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "engine"))
import aus_kit as A
import feras_kit as F
from feras_kit import foot, label, serif, round_card, versus, verdict, score, measure, ficha, cta, hud

ai = lambda *ids: ["ai:ai_" + i for i in ids]
PHOTOS = {
    "caes": ai("dogs_portal", "dogs_final_look", "dogs_hide_ferns", "dogs_nose_wind", "dogs_snow", "dog_family", "dogs_walk_ferns", "dogs_sit_rock", "dogs_run_plain", "dogs_drink_stream", "dogs_alert_night", "dogs_mist", "dogs_back_view", "dogs_close_faces", "dogs_rain", "dogs_tracks", "dogs_dusk_ridge", "dogs_forest_path", "dogs_lying_grass", "dogs_jump_log", "dogs_fog_field", "dogs_wading") + ["p_gs", "p_malinois"],
    "pastor": ai("gs_portrait", "gs_bark", "gs_permian", "gs_sniff_smoke", "gs_panting_heat", "gs_run", "gs_close_eyes", "gs_alert", "gs_coat", "gs_stand_rock", "gs_sniff_ground", "gs_tired") + ["p_gs"],
    "malinois": ai("ml_portrait", "ml_leap", "ml_jungle_heat", "ml_run", "ml_alert", "ml_jump", "ml_sit", "ml_sniff") + ["p_malinois"],
    "carbon": ai("carbon_swamp", "carbon_fire", "meganeura", "arthropleura", "dogs_meganeura", "dogs_arthropleura", "carbon_trees", "carbon_ferns", "carbon_water") + ["p_meganeura", "p_arthropleura"],
    "permian": ai("permian_desert", "inostrancevia_portrait", "inostrancevia_teeth", "inostrancevia_ambush", "extinction_volcano", "permian_dunes", "permian_conifers", "inostrancevia_walk", "inostrancevia_hide", "permian_river") + ["p_inostrancevia"],
    "triassic": ai("triassic_plain", "coelophysis", "dogs_coelophysis", "postosuchus_portrait", "triassic_forest", "triassic_river", "coelophysis_head", "coelophysis_run", "postosuchus_walk", "triassic_dawn", "triassic_storm") + ["p_coelophysis"],
    "jurassic": ai("jurassic_forest", "allosaurus_portrait", "allosaurus_dogs", "dilophosaurus", "jurassic_ferns", "jurassic_river", "allosaurus_head", "allosaurus_walk", "sauropod_far", "jurassic_sunset", "allosaurus_footprint") + ["p_allosaurus"],
    "cretaceous": ai("trex_vs_dogs", "trex_portrait", "trex_head", "trex_chase", "velociraptor", "velociraptor_vs_gs", "cretaceous_forest", "asteroid", "trex_walk", "trex_roar", "cretaceous_plain", "cretaceous_river")
                  + ["p_trex", "p_velociraptor"],
    "paleocene": ai("paleocene_jungle", "titanoboa", "titanoboa_river", "paleocene_river2", "paleocene_canopy", "titanoboa_head", "titanoboa_swim", "paleocene_bank", "jungle_heat", "ml_shade") + ["p_titanoboa"],
    "miocene": ai("miocene_grassland", "amphicyon", "amphicyon_dogs", "miocene_plain", "miocene_river", "amphicyon_head", "amphicyon_walk", "amphicyon_ridge", "gs_bark2", "miocene_dusk") + ["p_amphicyon"],
    "terror": ai("terrorbird", "terrorbird_head", "terrorbird_dogs", "terrorbird_walk", "terrorbird_strike", "terrorbird_legs", "brazil_lake", "brazil_savanna", "terrorbird_ridge", "terrorbird_eye") + ["p_terrorbird"],
    "iceage": ai("iceage_snow", "direwolf", "direwolf_pack", "greywolf", "iceage_forest", "iceage_blizzard", "direwolf_head", "direwolf_howl", "direwolf_run", "direwolf_tracks", "iceage_sunrise") + ["p_dire_wolf"],
    "final": ai("wolf_human_fire", "human_wolf_hand", "fossil_footprint", "dog_family", "cave_entrance", "wolf_cave", "hunter_back_wolf", "puppy_wolf", "modern_dogs_field", "cave_painting_dog", "dog_sleep_fire"),
}
CLIPS = json.load(open(os.path.join(HERE, "clips.json")))
CLIPS = {"caes": CLIPS["gs"] + CLIPS["ml"] + CLIPS["dogs"], "pastor": CLIPS["gs"], "malinois": CLIPS["ml"], "carbon": CLIPS["carbon"],
         "permian": CLIPS["permian"], "triassic": CLIPS["triassic"], "jurassic": CLIPS["jurassic"], "cretaceous": CLIPS["cretaceous"],
         "paleocene": CLIPS["paleocene"], "miocene": CLIPS["miocene"], "terror": CLIPS["terror"], "iceage": CLIPS["iceage"], "final": CLIPS["final"]}
FALLBACK = {k: ["caes", "pastor", "malinois"] for k in PHOTOS}
FALLBACK.update({"caes": ["pastor", "malinois"], "pastor": ["caes"], "malinois": ["caes"], "final": ["caes", "iceage", "pastor", "malinois"]})
A.setup(sys.argv[1], os.path.join(HERE, "skip.json"), PHOTOS, CLIPS, [], FALLBACK, ["caes"])
A.CLIP_TARGET = 0.30
A.MAX_HOLD, A.KEEP = 7.6, 4.2
F.HUD_TOTAL[0] = 9
ch = A.ch
chapters = []
SC = [0, 0]   # [Pastor, Malinois]


def beats(c, scene, phrases):
    for p in phrases:
        c.at(p, foot(scene))


def rnd(name, num, era, sub, scene):
    c = ch(name)
    hud(num, *SC)
    c.at(0, round_card(num, era, sub, scene))
    return c


def close(c, phrase_v, scene, winner, text, phrase_s, new, sub=""):
    c.at(phrase_v, verdict(scene, winner, text))
    c.at(phrase_s, score("caes", list(SC), new, sub))
    SC[:] = new


# ---------------------------------------------------------------- hook
c = ch("ch00_hook")
c.at(0, label("pastor", "Paleoceno · 30 °C|Pastor Alemão"))
beats(c, "paleocene", ["Faz mais de trinta graus"])
c.at("a pelagem grossa", foot("pastor"))
c.at("Chega à margem do rio", foot("paleocene"))
c.at("E alguma coisa se move", foot("paleocene"))
c.at("Algo com treze metros", serif("paleocene", "Treze metros.", ["Debaixo da água"]))
c.at("Poucos milhões de anos antes", foot("cretaceous"))
c.at("E saiu vivo", foot("cretaceous"))
c.at("Essa é a viagem", foot("caes"))
c.at("O Pastor Alemão e o Malinois", versus("pastor", "Pastor Alemão", "30–40 kg", "malinois", "Malinois", "25–30 kg"))
beats(c, "carbon", ["dos insetos gigantes"])
c.at("Nove eras", serif("caes", "Nove chances de não voltar.", ["Nove eras"]))
c.at("E o resultado não é", foot("cretaceous"))
c.at("O cão mais forte", foot("pastor"))
c.at("E o Tiranossauro", foot("cretaceous"))
c.at("Então, antes de continuar", serif("caes", "Escolha o seu lado.", ["Antes de continuar"]))
c.at("Pastor Alemão ou Malinois", foot("caes"))
c.at("Guarde essa resposta", foot("caes"))
chapters.append(c)

# ---------------------------------------------------------------- ch01 competitors
c = ch("ch01")
c.at(0, label("caes", "Os competidores|Pastor × Malinois"))
c.at("O Pastor Alemão é um dos", label("pastor", "Competidor 1|Pastor Alemão"))
c.at("Um macho adulto pesa", measure("pastor", "30–40 kg"))
c.at("um faro que pode", foot("pastor"))
c.at("É inteligente, forte", foot("pastor"))
c.at("O Malinois parece", label("malinois", "Competidor 2|Malinois"))
c.at("Pesa entre vinte e cinco", measure("malinois", "25–30 kg", side="left"))
c.at("É o cão escolhido", foot("malinois"))
c.at("Os dois correm perto", ficha("caes", "Pastor × Malinois", "Canis lupus familiaris",
                                  [["Velocidade", "≈ 50 km/h"], ["Faro", "milhares × o nosso"], ["Origem", "Alemanha · Bélgica"]]))
c.at("A diferença está no corpo", foot("pastor"))
c.at("O Malinois é mais leve", foot("malinois"))
c.at("E essa diferença", serif("caes", "vai decidir mais de uma rodada.", ["E essa diferença"]))
c.at("Placar zerado", score("caes", [0, 0], [0, 0], "Pastor × Malinois · rodadas sobrevividas"))
chapters.append(c)

# ---------------------------------------------------------------- rounds
c = rnd("ch02", 1, "Carbonífero", "≈ 300 milhões de anos · insetos gigantes", "carbon")
beats(c, "carbon", ["O ar é diferente", "E com tanto oxigênio"])
c.at("A Meganeura", measure("carbon", "70 cm", "Asas|Meganeura"))
c.at("A Arthropleura", measure("carbon", "2 m", "Comprimento|Arthropleura", side="left"))
c.at("Parece um filme", foot("carbon"))
c.at("Mas aqui vai a surpresa", serif("carbon", "não caçavam cães.", ["A surpresa"]))
beats(c, "carbon", ["A Arthropleura comia", "Para os nossos competidores"])
c.at("O perigo real é outro", foot("carbon"))
c.at("E aqui o faro", foot("pastor"))
close(c, "Veredito: os dois sobrevivem", "carbon", "empate", "OS DOIS SOBREVIVEM", "Um a um", [1, 1])
c.at("Mas a próxima era", foot("permian"))
chapters.append(c)

c = rnd("ch03", 2, "Permiano", "Inostrancevia · dentes de sabre", "permian")
c.at("Quem manda aqui", label("permian", "Rodada 2|Inostrancevia"))
c.at("cerca de três metros e meio", measure("permian", "3,5 m"))
c.at("Ela caçava de emboscada", foot("permian"))
c.at("Contra uma emboscada", serif("permian", "os primeiros segundos.", ["Contra uma emboscada"]))
c.at("O Malinois é feito para isso", foot("malinois"))
c.at("O Pastor também é rápido", foot("pastor"))
c.at("Numa emboscada, meio segundo", versus("pastor", "Pastor Alemão", "mais pesado", "malinois", "Malinois", "mais rápido"))
close(c, "Veredito: o Malinois sobrevive", "permian", "feras", "PASTOR CAI", "Dois a um", [1, 2], "O Malinois na frente")
c.at("E agora o mundo vai acabar", foot("permian"))
chapters.append(c)

c = rnd("ch04", 3, "Triássico", "os primeiros dinossauros", "triassic")
beats(c, "triassic", ["O planeta se recuperou"])
c.at("Um dos primeiros era", label("triassic", "Rodada 3|Coelophysis"))
c.at("Três metros de comprimento", measure("triassic", "20–30 kg"))
c.at("E aqui acontece uma inversão", serif("triassic", "os cães são os caçadores.", ["Uma inversão"]))
c.at("Dois cães atléticos", foot("caes"))
c.at("O predador perigoso", foot("triassic"))
c.at("Mas o faro salva", foot("pastor"))
close(c, "Veredito: os dois sobrevivem", "triassic", "tigre", "OS DOIS SOBREVIVEM", "Três a dois", [2, 3])
c.at("E a próxima era", foot("jurassic"))
chapters.append(c)

c = rnd("ch05", 4, "Jurássico", "Alossauro · 8 m · 2 t", "jurassic")
c.at("Agora os dinossauros", foot("jurassic"))
c.at("O Alossauro", measure("jurassic", "2 t"))
c.at("O Dilofossauro", foot("jurassic"))
c.at("Para um cão de trinta quilos", versus("caes", "Cão", "30 kg", "jurassic", "Alossauro", "2.000 kg"))
c.at("Mas existe uma regra", serif("jurassic", "Não compensa.", ["Uma regra da natureza"]))
c.at("E os cães ainda têm", foot("caes"))
c.at("e o vento conta", foot("jurassic"))
close(c, "Veredito: os dois sobrevivem", "jurassic", "tigre", "OS DOIS SOBREVIVEM", "Quatro a três", [3, 4])
c.at("E agora, a rodada", foot("cretaceous"))
chapters.append(c)

c = rnd("ch06", 5, "Cretáceo", "Tiranossauro rex · 12 m · 8 t", "cretaceous")
c.at("Doze metros", measure("cretaceous", "12 m"))
c.at("A mordida mais forte", foot("cretaceous"))
c.at("Mas antes dele, uma surpresa", serif("cretaceous", "do tamanho de um peru.", ["O Velociraptor de verdade"]))
c.at("Pesava uns quinze quilos", foot("cretaceous"))
c.at("Contra um Pastor Alemão", foot("cretaceous"))
c.at("Agora, o Tiranossauro", versus("caes", "Cães", "≈ 50 km/h", "cretaceous", "T. rex", "≈ 20 km/h"))
c.at("Só que os cientistas", foot("cretaceous"))
c.at("Os nossos dois cães", foot("caes"))
close(c, "Veredito: os dois sobrevivem", "cretaceous", "tigre", "OS DOIS SOBREVIVEM", "Cinco a quatro", [4, 5], "Sobreviveram ao rei")
c.at("Mas lembra do que eu prometi", foot("cretaceous"))
c.at("É a próxima", foot("paleocene"))
chapters.append(c)

c = ch("ch07")
hud(None, 0, 0)
c.at(0, cta("Curtindo essa viagem?", "Inscreva-se e ative o sininho · é de graça", "caes"))
c.at("Rodada seis", round_card(6, "Paleoceno", "30 °C · Titanoboa", "paleocene"))
hud(6, *SC)
c.at("Um asteroide acabou", foot("cretaceous"))
c.at("Na floresta tropical", foot("paleocene"))
c.at("E nos rios vivia", label("paleocene", "Rodada 6|Titanoboa"))
c.at("Uma cobra com cerca de treze", measure("paleocene", "13 m"))
c.at("Mas o maior inimigo", serif("paleocene", "É o calor.", ["O maior inimigo"]))
c.at("Cães não suam", foot("pastor"))
c.at("E o Pastor Alemão tem", foot("pastor"))
c.at("Com sede, ele vai até o rio", foot("paleocene"))
c.at("O Malinois, de pelo curto", foot("malinois"))
close(c, "Veredito: o Malinois sobrevive", "paleocene", "feras", "PASTOR CAI", "Seis a quatro", [4, 6], "A rodada mais mortal")
c.at("E a próxima fera", foot("miocene"))
chapters.append(c)

c = rnd("ch08", 7, "Mioceno", "Amphicyon · o cão-urso", "miocene")
c.at("Conheça o Amphicyon", label("miocene", "Rodada 7|Cão-urso"))
c.at("Algumas espécies podiam passar", measure("miocene", "300+ kg"))
c.at("Ele era onívoro", foot("miocene"))
c.at("Numa luta, os dois cães", versus("pastor", "Pastor Alemão", "40 kg", "miocene", "Amphicyon", "300+ kg"))
c.at("E aqui o Pastor Alemão", foot("pastor"))
close(c, "Veredito: os dois sobrevivem", "miocene", "tigre", "OS DOIS SOBREVIVEM", "Sete a cinco", [5, 7])
c.at("E a próxima rodada acontece aqui", foot("terror"))
chapters.append(c)

c = rnd("ch09", 8, "Aves do terror", "Paraphysornis · fóssil em SP", "terror")
c.at("Durante milhões de anos", foot("terror"))
c.at("Aves que não voavam", foot("terror"))
c.at("O Paraphysornis brasiliensis", label("terror", "Tremembé · SP|Paraphysornis"))
c.at("A técnica dessas aves", serif("terror", "como um machado.", ["A técnica"]))
c.at("Mas o Paraphysornis era robusto", foot("terror"))
c.at("Contra dois cães ágeis", foot("caes"))
close(c, "Veredito: os dois sobrevivem", "terror", "tigre", "OS DOIS SOBREVIVEM", "Oito a seis", [6, 8])
c.at("Falta uma era", foot("iceage"))
chapters.append(c)

c = rnd("ch10", 9, "Era do Gelo", "lobo-terrível · em matilha", "iceage")
c.at("O lobo-terrível", measure("iceage", "70 kg"))
c.at("Muita gente acha", foot("iceage"))
c.at("Mas um estudo genético", serif("iceage", "não é o avô dos cães.", ["Estudo genético de 2021"]))
c.at("E isso não ajuda", versus("malinois", "Malinois", "30 kg", "iceage", "Lobo-terrível", "70 kg · matilha"))
c.at("Uma matilha inteira", foot("iceage"))
c.at("Veredito: nenhum dos dois", verdict("iceage", "feras", "NENHUM SOBREVIVE"))
c.at("O placar final", score("caes", [6, 8], [6, 8], "Malinois 8 × 6 Pastor Alemão"))
c.at("Mas falta contar", foot("final"))
chapters.append(c)
hud(None, 0, 0)

c = ch("ch11")
c.at(0, round_card("F", "A aliança", "lobo + humano", "final"))
c.at("Os lobos que deram origem", foot("iceage"))
c.at("E quase todos esses gigantes", foot("iceage"))
c.at("Os lobos cinzentos fizeram", foot("final"))
c.at("Há mais de quinze mil anos", measure("final", "15.000 anos"))
c.at("O humano oferecia", foot("final"))
c.at("O lobo-terrível foi extinto", foot("iceage"))
c.at("No fim, a maior arma", serif("caes", "Foi a gente.", ["A maior arma dos cães"]))
c.at("E você, concorda", foot("caes"))
c.at("Se gostou, deixe", cta("Obrigado por assistir", "Deixe seu like e inscreva-se no Era das Feras", "caes"))
c.at("Muito obrigado por assistir", foot("caes"))
chapters.append(c)

MOODS = [("ch00_hook", 0, "tensao"), ("ch01", 0, "epico"), ("ch02", 0, "tensao"), ("ch05", 0, "epico"), ("ch06", 0, "tensao"),
         ("ch07", "Rodada seis", "tensao"), ("ch08", 0, "epico"), ("ch10", 0, "tensao"), ("ch11", 0, "drama")]
ctxs = ["caes", "caes", "carbon", "permian", "triassic", "jurassic", "cretaceous", "paleocene", "miocene", "terror", "iceage", "final"]
SCENE_OF = {"caes": ["dogs_", "dog_family", "p_gs", "p_malinois"], "pastor": ["gs_", "p_gs"], "malinois": ["ml_", "p_malinois"],
            "carbon": ["carbon", "meganeura", "arthropleura"], "permian": ["permian", "inostrancevia", "extinction"],
            "triassic": ["triassic", "coelophysis", "postosuchus"], "jurassic": ["jurassic", "allosaurus", "dilophosaurus"],
            "cretaceous": ["cretaceous", "trex", "velociraptor"], "paleocene": ["paleocene", "titanoboa"], "miocene": ["miocene", "amphicyon"],
            "terror": ["terror"], "iceage": ["iceage", "direwolf", "dire_wolf", "greywolf"], "final": ["wolf_human", "human_wolf", "dog_family"]}
ep = json.loads(A.finish(chapters, "FE02_Pastor_Malinois.mp4", ctx=ctxs, music_gain=-26))
# HUD labels: PASTOR × MALINOIS instead of tiger × beasts
for chap in ep["chapters"]:
    for s in chap["shots"]:
        if s["type"] == "score":
            s["labels"] = ["PASTOR", "MALINOIS"]
ep = F.cut_rhythm(ep, SCENE_OF)
starts, t = {}, 0.0
for chap, c in zip(ep["chapters"], chapters):
    starts[c.name] = t
    t += sum(s["dur"] for s in chap["shots"])
total = t
marks = []
for name, phrase, mood in MOODS:
    c = next(x for x in chapters if x.name == name)
    off = 0.0
    if phrase:
        c.cursor = 0; off = c.find(phrase) or 0.0
    marks.append((starts[name] + off, mood))
music = []
for k, (st, mood) in enumerate(marks):
    en = marks[k + 1][0] if k + 1 < len(marks) else total
    if music and music[-1]["file"] == f"musica/{mood}.mp3":
        music[-1]["end"] = round(min(total, en + 1.2), 2); continue
    music.append({"file": f"musica/{mood}.mp3", "start": round(max(0.0, st - 1.2), 2), "end": round(min(total, en + 1.2), 2),
                  "gain": -26, "fade_in": 2.4, "fade_out": 2.4})
ep["music"] = music
sys.stderr.write(f"trilha: {len(music)} trechos, {total / 60:.1f} min\n")
print(json.dumps(ep, indent=1, ensure_ascii=False))
