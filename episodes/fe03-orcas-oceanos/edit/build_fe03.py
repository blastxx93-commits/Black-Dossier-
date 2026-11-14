#!/usr/bin/env python3
"""FE03 (Era das Feras): "As Orcas Sobreviveriam em Cada Oceano da História?"
    python3 build_fe03.py <narration_dir> > episode.json      (run from the work folder: a/ = assets, audio/ = narration)
Owner (14/11/2026): more real footage, smooth professional camera, no shake.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "engine"))
import aus_kit as A
import feras_kit as F
from feras_kit import foot, label, serif, round_card, versus, verdict, score, measure, ficha, cta, hud

ai = lambda *ids: ["ai:ai_" + i for i in ids]
PHOTOS = {
    "orca": ai("orca_breach", "orca_portrait", "orca_pod_hunt", "orca_family", "orca_spyhop", "orca_fin", "orca_dive", "orca_sunset",
               "orca_pod_surface", "orca_echolocation", "orca_brain", "orca_ice", "orca_wave", "o_jump", "o_under", "o_head", "o_pod_dawn", "o_calf", "o_tail", "o_fin_mist", "o_hunt_fish", "o_deep", "o_sunrise", "o2_breath", "o2_side_surface", "o2_pod_under", "o2_eye", "o2_fluke_dive", "o2_play", "o2_cold_fog", "o2_jump_sunset", "o2_herd_seal", "o2_aerial") + ["p_orca"],
    "mar": ai("ocean_surface", "deep_ocean", "cretaceous_sea", "miocene_sea", "m_blue", "m_dark", "m_waves", "m_storm"),
    "cambrian": ai("anomalocaris", "trilobites", "cambrian_reef", "orca_vs_anomalocaris") + ["p_anomalocaris", "p_trilobite"],
    "devonian": ai("dunkleosteus_portrait", "devonian_reef", "orca_vs_dunkleosteus", "dk_side", "dk_front", "dk_reef", "devonian_corals", "devonian_fish") + ["p_dunkleosteus"],
    "triassic": ai("ichthyosaur_eye", "ichthyosaur_swim", "thalattoarchon", "orca_vs_ichthyosaur", "ichthyo_pod", "ichthyo_surface", "thalatto_side") + ["p_ichthyosaur"],
    "jurassic": ai("liopleurodon", "liopleurodon_head", "ammonites", "lio_side", "lio_below", "jurassic_ammonite_reef") + ["p_liopleurodon"],
    "cretaceous": ai("mosasaurus_jaws", "orca_vs_mosasaurus", "mosa_side", "mosa_head", "mosa_deep", "mosa_hunt", "cretaceous_storm", "cr_archelon", "cr_ammonites", "cr_sea_dusk", "cr_deep_shadow", "cr_bones", "cr_reef") + ["p_mosasaurus"],
    "eocene": ai("basilosaurus_portrait", "basilosaurus_swim", "basi_side", "basi_surface", "basi_head", "basi_hunt", "eocene_warm") + ["p_basilosaurus"],
    "megalodon": ai("megalodon_portrait", "megalodon_jaws", "megalodon_whale", "megalodon_below", "orca_vs_megalodon", "greatwhite", "mg_side", "mg_front", "mg_scale", "mg_deep", "mg_tooth_hand") + ["p_megalodon"],
    "livyatan": ai("livyatan_portrait", "livyatan_hunt", "orca_vs_livyatan", "fossil_cliff", "lv_side", "lv_head", "lv_deep", "lv_skull", "peru_desert") + ["p_livyatan"],
    "pliocene": ai("pliocene_cold", "orca_ice", "orca_wave", "pl_ice", "pl_seals", "pl_greatwhite", "pl_orca_ice", "pl_orcas_hunt", "pl_whale_cold", "pl_coast"),
    "hoje": ai("orca_today_boat", "ship_noise", "orca_family", "h_ship", "h_orcas_city", "h_research", "h_underwater_noise"),
}
CL = json.load(open(os.path.join(HERE, "clips.json")))
CLIPS = {"orca": CL["orca"], "mar": CL["deep"] + CL["surface"], "cambrian": CL["reef"][:2], "devonian": CL["fish"][:2],
         "triassic": CL["deep"][4:6], "jurassic": CL["deep"][6:8], "cretaceous": CL["surface"][:2],
         "eocene": CL["whale"][:3], "megalodon": CL["shark"], "livyatan": CL["whale"][3:], "pliocene": CL["ice"], "hoje": CL["today"]}
GENERIC = CL["deep"] + CL["surface"] + CL["fish"] + CL["reef"]
FALLBACK = {k: ["mar", "orca"] for k in PHOTOS}
FALLBACK.update({"orca": ["mar", "pliocene", "hoje"], "mar": ["orca"], "hoje": ["orca", "mar"], "cretaceous": ["mar", "orca", "jurassic"], "megalodon": ["mar", "orca", "pliocene"]})
PIN_IDS = ["ai_anomalocaris", "ai_dunkleosteus_portrait", "ai_thalattoarchon", "ai_liopleurodon", "ai_mosasaurus_jaws",
           "ai_basilosaurus_portrait", "ai_megalodon_portrait", "ai_livyatan_portrait", "ai_orca_portrait", "ai_orca_breach",
           "ai_livyatan_hunt", "ai_megalodon_whale", "ai_orca_pod_hunt", "ai_pliocene_cold",
           "ai_o_head", "ai_o_under", "ai_o2_side_surface", "ai_o_jump", "ai_o2_eye", "ai_o_deep", "ai_o2_breath",            "ai_orca_vs_dunkleosteus", "ai_thalatto_side", "ai_lio_side", "ai_orca_vs_mosasaurus", "ai_basi_side", "ai_mg_side", "ai_lv_deep", "ai_basi_hunt", "ai_devonian_fish"]
A.setup(sys.argv[1], os.path.join(HERE, "skip.json"), PHOTOS, CLIPS, GENERIC, FALLBACK, ["mar"])
F.pin(*PIN_IDS)
A.CLIP_TARGET = 0.45          # owner: more real footage
A.MAX_HOLD, A.KEEP = 7.0, 4.2
F.HUD_TOTAL[0] = 9
ch = A.ch
chapters = []
SC = [0, 0]   # [orca, feras]


def beats(c, scene, phrases):
    for p in phrases:
        c.at(p, foot(scene))


def rnd(name, num, era, sub, scene):
    c = ch(name)
    hud(num, *SC)
    c.at(0, round_card(num, era, sub, scene))
    return c


def close(c, phrase_v, scene, winner, text, phrase_s, new, sub="", img=None):
    c.at(phrase_v, verdict(scene, winner, text, img))
    c.at(phrase_s, score("orca", list(SC), new, sub))
    SC[:] = new


# ---------------------------------------------------------------- hook
c = ch("ch00_hook")
c.at(0, foot("megalodon"))
c.at("Não foi", serif("megalodon", "Não foi.", ["O mais perigoso do oceano?"]))
c.at("Existiu uma fera", foot("livyatan"))
c.at("Ela não caçava peixes", foot("mar"))
c.at("E viveu no mesmo mar", foot("megalodon"))
c.at("Hoje, o maior predador", label("orca", "O rei dos mares hoje|Orca"))
beats(c, "orca", ["Ela caça tubarões-brancos", "Caça baleias maiores", "E não tem nenhum inimigo"])
c.at("Então vamos fazer", foot("mar"))
c.at("Quinhentos milhões de anos", serif("mar", "Nove monstros.", ["500 milhões de anos", "Nove eras"]))
c.at("Uma orca de seis toneladas", foot("orca"))
F.questions(c, ["Ela vence o Megalodon?", "Quem o Megalodon temia?", "Quando a orca vira presa?"],
            ["Ela vence o Megalodon", "Quem é a fera", "E em qual era"], "mar")
c.at("Prepare-se para mergulhar", foot("mar"))
chapters.append(c)

# ---------------------------------------------------------------- competitor
c = ch("ch01")
c.at(0, label("orca", "A competidora|Orca"))
c.at("A orca não é uma baleia", foot("orca"))
c.at("Um macho adulto pode", measure("orca", "9 m · 6 t", "Macho adulto|Orca", img="ai_orca_portrait"))
c.at("A barbatana nas costas", foot("orca"))
c.at("Ela nada a mais", foot("orca"))
c.at("E tem um dos maiores", foot("orca"))
c.at("Mas a arma mais perigosa", serif("orca", "É o grupo.", ["A arma mais perigosa"]))
c.at("Orcas vivem e caçam", foot("orca"))
c.at("Há grupos que criam ondas", foot("pliocene"))
c.at("E há grupos que caçam", foot("megalodon"))
c.at("Ela respira ar", ficha("orca", "Orca", "Orcinus orca", [["Tamanho", "até 9 m"], ["Peso", "≈ 6 t"], ["Velocidade", "50+ km/h"]]))
c.at("Guarde esses dois detalhes", foot("orca"))
c.at("Placar zerado", score("orca", [0, 0], [0, 0], "Orca × feras do passado"))
chapters.append(c)

# ---------------------------------------------------------------- rounds
c = rnd("ch02", 1, "Cambriano", "≈ 500 milhões de anos", "cambrian")
beats(c, "cambrian", ["É a época da explosão"])
c.at("E o maior predador", label("cambrian", "Rodada 1|Anomalocaris"))
c.at("Ele tinha dois braços", foot("cambrian"))
c.at("Mas as maiores estimativas", measure("cambrian", "≈ 1 m", img="ai_anomalocaris"))
c.at("Os cientistas encontraram", foot("cambrian"))
c.at("A orca é nove vezes", versus("orca", "Orca", "9 m", "cambrian", "Anomalocaris", "≈ 1 m", limg="ai_o_head"))
c.at("O problema é outro", foot("mar"))
c.at("Para conseguir", foot("orca"))
close(c, "Veredito: vitória da orca", "cambrian", "tigre", "VITÓRIA DA ORCA", "Um a zero", [1, 0])
c.at("E a próxima era", foot("devonian"))
chapters.append(c)

c = rnd("ch03", 2, "Devoniano", "a era dos peixes", "devonian")
c.at("O Dunkleosteus tinha", label("devonian", "Rodada 2|Dunkleosteus"))
c.at("Estudos mostram", foot("devonian"))
c.at("Por muito tempo", measure("devonian", "3–4 m", img="ai_dunkleosteus_portrait"))
c.at("Contra uma orca", versus("orca", "Orca", "9 m", "devonian", "Dunkleosteus", "3–4 m", limg="ai_o_under", rimg="ai_orca_vs_dunkleosteus"))
c.at("A orca pode atacar", foot("orca"))
close(c, "Veredito: vitória da orca", "devonian", "tigre", "VITÓRIA DA ORCA", "Dois a zero", [2, 0], img="ai_devonian_fish")
c.at("E a próxima fera", foot("triassic"))
chapters.append(c)

c = rnd("ch04", 3, "Triássico", "os répteis voltam ao mar", "triassic")
beats(c, "triassic", ["Os répteis voltaram", "Alguns tinham os maiores"])
c.at("Os maiores ictiossauros", foot("triassic"))
c.at("O predador perigoso", measure("triassic", "≈ 8 m", "Rodada 3|Thalattoarchon", img="ai_thalattoarchon"))
c.at("O fóssil dele", foot("triassic"))
c.at("Oito metros contra nove", versus("orca", "Orca", "9 m", "triassic", "Thalattoarchon", "8 m", limg="ai_o2_side_surface", rimg="ai_thalatto_side"))
c.at("Só que o Thalattoarchon", foot("orca"))
c.at("Enquanto uma distrai", foot("orca"))
close(c, "Veredito: vitória da orca", "triassic", "tigre", "VITÓRIA DA ORCA", "Três a zero", [3, 0], "Graças ao grupo")
c.at("E na próxima era", foot("jurassic"))
chapters.append(c)

c = rnd("ch05", 4, "Jurássico", "Liopleurodon", "jurassic")
c.at("O Liopleurodon ficou famoso", serif("jurassic", "Um mito de 25 metros.", ["O Liopleurodon"]))
c.at("As estimativas atuais", measure("jurassic", "6–7 m", img="ai_liopleurodon"))
c.at("Ainda assim", foot("jurassic"))
c.at("Mas seis metros contra nove", versus("orca", "Orca", "9 m", "jurassic", "Liopleurodon", "6–7 m", limg="ai_o_jump", rimg="ai_lio_side"))
close(c, "Veredito: vitória da orca", "jurassic", "tigre", "VITÓRIA DA ORCA", "Quatro a zero", [4, 0])
c.at("Até aqui, ela parece", foot("orca"))
c.at("E o rei dela", foot("cretaceous"))
chapters.append(c)

c = rnd("ch06", 5, "Cretáceo", "o mar dos monstros", "cretaceous")
c.at("O Mosassauro", label("cretaceous", "Rodada 5|Mosassauro"))
c.at("Duas fileiras extras", measure("cretaceous", "12–15 m", img="ai_mosasaurus_jaws"))
c.at("Fósseis mostram", foot("cretaceous"))
c.at("Pela primeira vez", versus("orca", "Orca", "9 m", "cretaceous", "Mosassauro", "12–15 m", limg="ai_o2_eye", rimg="ai_orca_vs_mosasaurus"))
c.at("E o Mosassauro tinha outra", foot("cretaceous"))
c.at("Uma orca sozinha", foot("orca"))
c.at("Mas um grupo de orcas", foot("orca"))
close(c, "Veredito: empate", "cretaceous", "empate", "EMPATE", "Quatro a zero", [4, 0], "Ninguém pontua", img="ai_orca_pod_hunt")
c.at("E a próxima fera", foot("eocene"))
chapters.append(c)

c = ch("ch07")
hud(None, 0, 0)
c.at(0, cta("Curtindo esse mergulho?", "Inscreva-se e ative o sininho · é de graça", "orca"))
c.at("Rodada seis", round_card(6, "Eoceno", "a baleia-serpente", "eocene"))
hud(6, *SC)
c.at("O Basilosaurus", measure("eocene", "até 18 m", "Rodada 6|Basilosaurus", img="ai_basilosaurus_portrait"))
c.at("Fósseis de outras baleias", foot("eocene"))
c.at("E aqui está o problema", serif("eocene", "a orca é uma baleia.", ["E aqui está o problema"]))
c.at("Com o dobro do comprimento", versus("orca", "Orca", "9 m", "eocene", "Basilosaurus", "18 m", limg="ai_o_deep", rimg="ai_basi_side"))
close(c, "Veredito: vitória do Basilosaurus", "eocene", "feras", "VITÓRIA DA FERA", "Quatro a um", [4, 1], "Primeiro ponto das feras", img="ai_basi_hunt")
c.at("E agora, o monstro", foot("megalodon"))
chapters.append(c)

c = rnd("ch08", 7, "Mioceno", "Megalodon · 15–20 m", "megalodon")
c.at("O maior tubarão", measure("megalodon", "15–20 m", img="ai_megalodon_portrait"))
c.at("Os dentes do Megalodon", label("megalodon", "Até 17 cm|Dente do Megalodon"))
c.at("Eles são encontrados", foot("megalodon"))
c.at("E alguns estudos", foot("megalodon"))
c.at("Hoje, orcas caçam", foot("orca"))
c.at("Mas um Megalodon tem", versus("orca", "Orca", "9 m", "megalodon", "Megalodon", "15–20 m", limg="ai_o2_breath", rimg="ai_mg_side"))
close(c, "Veredito: vitória do Megalodon", "megalodon", "feras", "VITÓRIA DA FERA", "Quatro a dois", [4, 2], img="ai_megalodon_whale")
c.at("Mas lembra do que eu prometi", serif("livyatan", "nem o Megalodon queria encontrar.", ["Uma fera que"]))
chapters.append(c)

c = rnd("ch09", 8, "Mioceno", "Livyatan · o cachalote assassino", "livyatan")
c.at("Um cachalote assassino", label("livyatan", "Rodada 8|Livyatan"))
c.at("Os dentes do Livyatan", measure("livyatan", "35+ cm", "Dentes|Livyatan", img="ai_livyatan_portrait"))
c.at("E ele caçava baleias", foot("livyatan"))
c.at("Livyatan e Megalodon", versus("megalodon", "Megalodon", "15–20 m", "livyatan", "Livyatan", "13–18 m", rimg="ai_lv_deep"))
c.at("Mas uma coisa é certa", foot("orca"))
close(c, "Veredito: vitória do Livyatan", "livyatan", "feras", "VITÓRIA DA FERA", "Quatro a três", [4, 3], img="ai_livyatan_hunt")
c.at("Falta uma era", foot("pliocene"))
chapters.append(c)

c = rnd("ch10", 9, "Plioceno", "o oceano esfria", "pliocene")
c.at("O planeta está esfriando", foot("pliocene"))
c.at("O Megalodon some", foot("megalodon"))
c.at("Uma das teorias", foot("megalodon"))
c.at("E num oceano frio", foot("orca"))
c.at("A gordura grossa", foot("orca"))
c.at("Exatamente as qualidades", foot("orca"))
close(c, "Veredito: vitória da orca", "pliocene", "tigre", "VITÓRIA DA ORCA", "O placar final", [5, 3],
      "5 vitórias · 1 empate · 3 derrotas", img="ai_pliocene_cold")
c.at("Mas existe uma última", foot("hoje"))
chapters.append(c)
hud(None, 0, 0)

c = ch("ch11")
c.at(0, round_card("F", "O oceano de hoje", "o único inimigo da orca", "hoje"))
c.at("A orca venceu o Anomalocaris", foot("orca"))
c.at("Mas alguns grupos", foot("hoje"))
c.at("A comida delas diminuiu", foot("hoje"))
c.at("O predador que nem", serif("hoje", "as mudanças que nós fizemos no mar.", ["O predador que nem o Mosassauro derrubaria"]))
c.at("A orca venceu a pré-história", foot("orca"))
c.at("E você, concorda", foot("orca"))
c.at("Se gostou, deixe", cta("Obrigado por assistir", "Deixe seu like e inscreva-se no Era das Feras", "orca"))
c.at("Muito obrigado por assistir", foot("orca"))
chapters.append(c)

MOODS = [("ch00_hook", 0, "tensao"), ("ch01", 0, "epico"), ("ch02", 0, "tensao"), ("ch05", 0, "epico"), ("ch06", 0, "tensao"),
         ("ch07", "Rodada seis", "tensao"), ("ch08", 0, "tensao"), ("ch10", 0, "epico"), ("ch11", 0, "drama")]
ctxs = ["mar", "orca", "cambrian", "devonian", "triassic", "jurassic", "cretaceous", "eocene", "megalodon", "livyatan", "pliocene", "hoje"]
SCENE_OF = {"orca": ["ai/ai_o_", "ai/ai_o2_", "orca_dive", "orca_fin", "orca_breach", "orca_sunset", "orca_pod_surface", "orca_portrait", "p_orca"], "mar": ["ocean_surface", "deep_ocean", "ai/ai_m_"], "cambrian": ["anomalocaris", "trilobite", "cambrian"],
            "devonian": ["dunkleosteus", "devonian", "orca_vs_dunk"], "triassic": ["ichthyosaur", "thalattoarchon"], "jurassic": ["liopleurodon", "ammonite"],
            "cretaceous": ["mosasaurus", "cretaceous", "ai/ai_cr_"], "eocene": ["basilosaurus", "basi_", "eocene"], "megalodon": ["megalodon", "greatwhite", "ai/ai_mg_"],
            "livyatan": ["livyatan", "fossil_cliff", "ai/ai_lv_"], "pliocene": ["pliocene", "orca_ice", "orca_wave"], "hoje": ["today", "ship", "orca_family"]}
ep = json.loads(A.finish(chapters, "FE03_Orcas_Oceanos.mp4", ctx=ctxs, music_gain=-26))
for chap in ep["chapters"]:
    for s in chap["shots"]:
        if s["type"] == "score":
            s["labels"] = ["ORCA", "FERAS"]
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
