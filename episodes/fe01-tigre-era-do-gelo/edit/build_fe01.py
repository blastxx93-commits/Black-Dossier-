#!/usr/bin/env python3
"""FE01 (Era das Feras): "Um Tigre Venceria Cada Fera da Era do Gelo?"
    python3 build_fe01.py <narration_dir> > episode.json      (run from the work folder: a/ = assets, audio/ = narration)

Rhythm (owner, 13/11/2026): very dynamic, ~3 s per shot, varied transitions with varied sounds, HUD with round and score,
every AI image and the narration reviewed before the edit (edit/skip.json = rejected files, edit/reviewed.json = approved photos/clips).
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "engine"))
import aus_kit as A
import feras_kit as F
from feras_kit import foot, label, serif, round_card, versus, verdict, score, measure, ficha, cta, hud

ai = lambda *ids: ["ai:ai_" + i for i in ids]
PHOTOS = {
    "hook": ai("mammoth_vs_tiger", "mammoth_lowangle", "tusks_close", "iceage_panorama", "blizzard_steppe", "tiger_eyes_snow", "iceage_glacier_valley", "iceage_sunset",
                 "iceage_blizzard_herd", "iceage_river", "hook_storm", "hook_valley", "hook_aurora"),
    "tigre": ai("tiger_taiga", "tiger_stalk", "tiger_leap", "tiger_roar", "tiger_paw", "tiger_claws", "tiger_ridge", "tiger_dusk",
                "tiger_river", "tiger_ambush", "tiger_walk_steppe", "tiger_rest", "tiger_profile_snow", "tiger_back_view",
                "tiger_jump_log", "tiger_shake_snow", "tiger_lying_eyes", "tiger_cliff_wind", "tiger_night_snow", "tiger_tracks_line",
                "tiger_mouth_close", "tiger_run_snow", "tiger_drink_ice", "tiger_glacier", "tiger_forest_dawn", "tiger_snow_close", "tiger_river_cross", "tiger_rock_sit", "tiger_stretch", "tiger_walk_fog", "tiger_grass_frost", "tiger_steppe_wide", "tiger_camtrap", "tiger_portrait_side", "tiger_yawn", "tiger_birch", "tiger_sunlit", "tiger_paws_walk", "tiger_look_back", "tiger_frozen_lake", "tiger_whiskers") + ["p_amur_tiger"],
    "lobo": ai("direwolf_portrait", "direwolf_pack", "direwolf_vs_tiger", "direwolf_circle", "direwolf_teeth", "direwolf_alone") + ["p_dire_wolf"],
    "alce": ai("megaloceros_portrait", "megaloceros_herd", "megaloceros_vs_tiger", "megaloceros_antlers", "megaloceros_forest",
               "megaloceros_charge", "megaloceros_snow") + ["p_megaloceros_skeleton", "p_gaur"],
    "bisao": ai("bison_portrait", "bison_herd", "bison_vs_tiger", "bison_charge", "bison_horns", "bison_snowstorm") + ["p_bison_painting"],
    "hiena": ai("hyena_portrait", "hyena_clan", "hyena_bones", "hyena_vs_tiger", "hyena_jaws", "hyena_den", "hyena_run", "hyena_howl", "hyena_watch", "hyena_carcass", "hyena_portrait2", "hyena_tracks") + ["p_cave_hyena"],
    "urso": ai("cavebear_portrait", "cavebear_den", "cavebear_vs_tiger", "cavebear_roar", "cavebear_skeleton", "cavebear_walk", "cavebear_cave", "cavebear_close", "cavebear_cub") + ["p_cave_bear_skeleton"],
    "leao": ai("cavelion_portrait", "cavelion_pride", "cavelion_vs_tiger", "cavelion_snarl", "cavelion_hunt", "cave_painting_lions", "cavelion_walk", "cavelion_rest", "cavelion_stare", "cavelion_steppe", "cavelion_roar", "cavelion_ambush")
            + ["p_cave_lion", "p_chauvet"],
    "smilodon": ai("smilodon_fangs", "smilodon_portrait", "smilodon_arms", "smilodon_vs_tiger", "smilodon_fight", "smilodon_cave_brazil",
                   "smilodon_tooth_break", "smilodon_skull", "smilodon_walk", "smilodon_rock",
                   "smilodon_jaws_open", "smilodon_hunt", "smilodon_rest", "smilodon_pampas", "smilodon_stare", "smilodon_crouch", "smilodon_savanna", "smilodon_snarl2", "smilodon_vs_tiger2") + ["p_smilodon_skeleton", "p_smilodon_skull"],
    "arctodus": ai("arctodus_portrait", "arctodus_upright", "arctodus_vs_tiger", "arctodus_carcass", "arctodus_paw", "arctodus_walk", "arctodus_head", "arctodus_scale", "arctodus_run", "arctodus_ridge", "arctodus_snow", "arctodus_close", "arctodus_vs_tiger2") + ["p_arctodus_skeleton"],
    "rino": ai("rhino_portrait", "rhino_sweep", "rhino_charge", "rhino_vs_tiger", "rhino_horn", "rhino_herd", "rhino_side") + ["p_woolly_rhino"],
    "mamute": ai("mammoth_herd_wall", "mammoth_calf", "mammoth_vs_tiger_far", "mammoth_stomp", "mammoth_walk", "mammoth_trumpet", "mammoth_herd_far", "mammoth_eye", "mammoth_tusks_front", "mammoth_family", "mammoth_trunk", "mammoth_sideview", "mammoth_dusk")
              + ["p_mammoth_skeleton"],
    "humano": ai("hunters_fire", "hunters_spears", "spear_points", "cave_painting_torch", "empty_steppe_thaw", "extinct_shadows", "human_footprints", "cave_entrance_snow", "hunters_far", "hunters_back", "hunter_hand_spear", "flint_knapping", "campfire_cave", "torch_cave", "bone_hut", "glacier_melt", "fossil_dig")
              + ["p_spear_points"],
    "final": ai("tiger_modern_forest", "tiger_final_look", "scoreboard_bg", "final_sunrise"),
}
CLIPS = json.load(open(os.path.join(HERE, "clips.json")))
GENERIC = CLIPS.pop("_generic", [])
FALLBACK = {k: ["tigre", "hook"] for k in PHOTOS}   # a round may show the tiger (the fighter) or the Ice Age landscape
FALLBACK.update({"tigre": ["final"], "hook": ["tigre"], "final": ["tigre"], "humano": ["hook", "final", "tigre"]})
A.setup(sys.argv[1], os.path.join(HERE, "skip.json"), PHOTOS, CLIPS, GENERIC, FALLBACK, ["tigre"])
A.CLIP_TARGET = 0.40
A.MAX_HOLD, A.KEEP = 5.6, 3.4       # very dynamic: nothing holds more than ~4.5 s
ch = A.ch
chapters = []


def beats(c, scene, phrases, cap_first=None):
    """One fresh shot of the scene on each phrase (the cutting rhythm between the layouts)."""
    for k, p in enumerate(phrases):
        c.at(p, label(scene, cap_first) if (k == 0 and cap_first) else foot(scene))


# ---------------------------------------------------------------- hook
c = ch("ch00_hook")
c.at(0, A.P("hook", move="out", photo_only=True))   # the mammoth facing the tiger, first frame
beats(c, "hook", ["Três metros e meio", "Presas de quatro metros", "E, na frente dele"])
c.at("Não um tigre qualquer", label("tigre", "O maior felino vivo|Tigre-siberiano"))
beats(c, "tigre", ["Agora imagine pegar", "vinte mil anos no passado"])
beats(c, "hook", ["Um mundo de neve", "mais pesado e mais perigoso"])
c.at("Dez rodadas", serif("hook", "Dez feras.", ["Dez rodadas", "Uma de cada vez"]))
beats(c, "tigre", ["Em algumas, o tigre"])
beats(c, "hook", ["Em outras, ele vira", "E uma dessas feras"])
c.at("vinte e oito centímetros", foot("smilodon"))
F.questions(c, ["Ele vence o Smilodon?", "Quantas rodadas ele aguenta?", "Qual é a rodada mais perigosa?"],
            ["Será que o tigre", "Quantas rodadas", "E por que a rodada"], "hook")
c.at("não é contra um monstro", foot("hook"))
c.at("Fique até o fim", foot("tigre"))
chapters.append(c)

# ---------------------------------------------------------------- ch01: the fighter
c = ch("ch01")
c.at(0, label("tigre", "Conheça o lutador|Tigre-siberiano"))
beats(c, "tigre", ["O tigre-siberiano, também chamado", "onde o inverno passa"])
c.at("Um macho adulto pesa", measure("tigre", "200 kg", "Peso médio|Macho adulto"))
c.at("Os maiores passam", measure("tigre", "300 kg", side="left"))
c.at("Do focinho à ponta", foot("tigre"))
c.at("A mordida tem força", foot("tigre"))
c.at("As garras retráteis", label("tigre", "Garras|Até 10 cm"))
c.at("E ele consegue saltar", foot("tigre"))
c.at("Mas a arma mais perigosa", serif("tigre", "A emboscada.", ["A arma mais perigosa"]))
beats(c, "tigre", ["Ele caça sozinho", "mirando a garganta", "A maioria das presas"])
c.at("E tem um detalhe", ficha("tigre", "Tigre-siberiano", "Panthera tigris altaica",
                              [["Peso", "200 a 300 kg"], ["Comprimento", "até 3 m"], ["Salto", "mais de 6 m"]]))
c.at("Fósseis mostram", foot("hook"))
beats(c, "tigre", ["Ou seja: ele já esteve lá"])
c.at("Placar zerado", score("final", [0, 0], [0, 0], "Dez feras pela frente"))
chapters.append(c)


# ---------------------------------------------------------------- rounds
def rnd(name, num, beast_name, sub, scene, stat_t, stat_b, ctx_scene=None):
    c = ch(name)
    hud(num, *SCORE)
    c.at(0, round_card(num, beast_name, sub, scene))
    return c


SCORE = [0, 0]


def close(c, phrase_v, scene_v, winner, phrase_s, new, sub=""):
    c.at(phrase_v, verdict(scene_v, winner))
    c.at(phrase_s, score("final" if winner == "tigre" else scene_v, list(SCORE), new, sub))
    SCORE[:] = new


# 1 dire wolf
c = rnd("ch02", 1, "Lobo-terrível", "até 70 kg · caçava em matilha", "lobo", "", "")
c.at("Esqueça o lobo comum", label("lobo", "Rodada 1|Lobo-terrível"))
c.at("Pesava até setenta quilos", measure("lobo", "70 kg"))
beats(c, "lobo", ["caçava cavalos"])
c.at("Num duelo um contra um", versus("tigre", "Tigre", "200 kg", "lobo", "Lobo-terrível", "70 kg"))
beats(c, "tigre", ["Uma patada bem dada"])
beats(c, "lobo", ["O problema é que", "Ele vivia em matilhas", "E cinco lobos famintos"])
beats(c, "tigre", ["Só que o tigre não precisa", "Ele precisa escolher", "e desaparece antes"])
close(c, "Veredito: vitória do tigre", "lobo", "tigre", "Um ponto no placar", [1, 0])
c.at("Mas a próxima fera", foot("alce"))
chapters.append(c)

# 2 giant elk
c = rnd("ch03", 2, "Alce-gigante", "Megaloceros · galhada de 3,5 m", "alce", "", "")
c.at("O Megaloceros foi", label("alce", "Rodada 2|Megaloceros"))
c.at("Mais de dois metros", measure("alce", "2 m", side="left"))
c.at("e uma galhada que podia", measure("alce", "3,5 m"))
beats(c, "alce", ["É a largura de um carro"])
c.at("De frente, essa galhada", versus("tigre", "Tigre", "200 kg", "alce", "Alce-gigante", "700 kg"))
beats(c, "alce", ["Um golpe de lado"])
c.at("Só que o tigre não ataca", serif("tigre", "Nunca de frente.", ["A regra do tigre"]))
c.at("Hoje, na Ásia", label("alce", "Presa real dos tigres|Gauro · mais de 1 tonelada"))
beats(c, "tigre", ["A técnica é sempre", "salto nas costas"])
beats(c, "alce", ["E a galhada gigante", "Pesada, ela atrapalha"])
close(c, "Veredito: vitória do tigre", "alce", "tigre", "Dois a zero", [2, 0])
c.at("Mas o próximo adversário", foot("bisao"))
chapters.append(c)

# 3 steppe bison
c = rnd("ch04", 3, "Bisão-da-estepe", "≈ 1 tonelada · chifres abertos", "bisao", "", "")
c.at("O bisão-da-estepe era", label("bisao", "Rodada 3|Bisão-da-estepe"))
beats(c, "bisao", ["Tão comum que aparece"])
c.at("desenhado por humanos", foot("bisao"))
c.at("Pesava perto de uma tonelada", measure("bisao", "1.000 kg"))
beats(c, "bisao", ["e um temperamento"])
c.at("Esse é o tipo de presa", versus("tigre", "Tigre", "200 kg", "bisao", "Bisão-da-estepe", "1.000 kg"))
beats(c, "bisao", ["Um coice ou uma chifrada"])
c.at("e um tigre ferido", serif("tigre", "é um tigre morto.", ["Um tigre ferido no inverno"]))
beats(c, "tigre", ["Mas os números", "O segredo é derrubar"])
close(c, "Veredito: vitória do tigre", "bisao", "tigre", "Três a zero", [3, 0], "Vitória apertada")
c.at("E é aqui que o jogo muda", foot("hiena"))
c.at("Ela quer roubar", foot("hiena"))
chapters.append(c)

# 4 cave hyena
c = rnd("ch05", 4, "Hiena-das-cavernas", "mais de 100 kg · vivia em clãs", "hiena", "", "")
c.at("Maior que qualquer hiena", label("hiena", "Rodada 4|Hiena-das-cavernas"))
c.at("pesava mais de cem quilos", measure("hiena", "100 kg"))
beats(c, "hiena", ["Ela quebrava ossos", "E vivia em clãs"])
c.at("Um contra um, o tigre", versus("tigre", "Tigre", "200 kg", "hiena", "Hiena-das-cavernas", "100 kg"))
c.at("Mas as hienas não precisam", serif("hiena", "Elas esperam.", ["As hienas não precisam vencer"]))
beats(c, "tigre", ["Depois de horas caçando"])
beats(c, "hiena", ["Aí chega o clã", "Ele vence cada briga"])
close(c, "Veredito: o tigre vence", "hiena", "tigre", "Quatro a zero", [4, 0], "Venceu a luta, perdeu o jantar")
c.at("Até aqui, ele parece", foot("tigre"))
c.at("Só que a próxima fera", foot("urso"))
chapters.append(c)

# 5 cave bear
c = rnd("ch06", 5, "Urso-das-cavernas", "mais de 500 kg · quase 3 m em pé", "urso", "", "")
c.at("O urso-das-cavernas era", label("urso", "Rodada 5|Urso-das-cavernas"))
c.at("Machos grandes podiam", measure("urso", "500 kg"))
c.at("Os cientistas encontraram", foot("urso"))
beats(c, "urso", ["onde ele passava o inverno"])
c.at("Ele era quase vegetariano", serif("urso", "não precisa comer carne.", ["Meia tonelada, acuado"]))
c.at("E aqui existe um dado real", label("tigre", "Rússia, hoje|Tigres atacam ursos"))
beats(c, "urso", ["Às vezes, entram na toca"])
beats(c, "tigre", ["Às vezes, o tigre vence"])
beats(c, "urso", ["E às vezes, o urso mata"])
c.at("Contra o urso-das-cavernas", versus("tigre", "Tigre", "200 kg", "urso", "Urso-das-cavernas", "500 kg"))
close(c, "Veredito: empate", "urso", "empate", "Quatro a zero", [4, 0], "Ninguém pontua")
c.at("Mas segure firme", foot("leao"))
c.at("Um felino", foot("leao"))
chapters.append(c)

# 6 cave lion (+ mid CTA)
c = ch("ch07")
hud(None, 0, 0)
c.at(0, cta("Curtindo essa batalha?", "Inscreva-se e ative o sininho · é de graça", "leao"))
c.at("Rodada seis", round_card(6, "Leão-das-cavernas", "mais de 300 kg · estepe aberta", "leao"))
hud(6, *SCORE)
c.at("O leão-das-cavernas dominou", label("leao", "Rodada 6|Leão-das-cavernas"))
c.at("Era maior que o leão", measure("leao", "300 kg"))
c.at("Ele aparece em pinturas", foot("leao"))
c.at("Agora sim, um duelo", versus("tigre", "Tigre", "200–300 kg", "leao", "Leão-das-cavernas", "300 kg"))
beats(c, "tigre", ["O tigre é melhor"])
beats(c, "leao", ["Mas o leão-das-cavernas vivia"])
c.at("Em campo aberto", serif("leao", "Campo aberto.", ["O duelo", "Frente a frente"]))
c.at("E se houver mais", foot("leao"))
close(c, "Veredito: vitória do leão-das-cavernas", "leao", "feras", "O primeiro ponto", [4, 1], "Primeiro ponto das feras")
c.at("E agora, a luta", foot("smilodon"))
chapters.append(c)

# 7 smilodon
c = rnd("ch08", 7, "Smilodon", "dentes de 28 cm · viveu no Brasil", "smilodon", "", "")
c.at("O tigre-dentes-de-sabre", label("smilodon", "Rodada 7|Smilodon populator"))
c.at("A espécie maior", foot("smilodon"))
c.at("onde fósseis já foram", label("smilodon", "Brasil|Cavernas de MG e BA"))
c.at("Ele podia passar", measure("smilodon", "300 kg", side="left"))
c.at("caninos de vinte e oito", measure("smilodon", "28 cm"))
c.at("Parece o fim do tigre", versus("tigre", "Tigre", "200 kg", "smilodon", "Smilodon", "300 kg"))
c.at("Mas os números escondem", serif("smilodon", "Uma surpresa.", ["Os números escondem"]))
beats(c, "smilodon", ["Aqueles dentes enormes", "Eles quebravam", "Por isso, o Smilodon", "E a mordida dele"])
beats(c, "tigre", ["O tigre é mais ágil"])
beats(c, "smilodon", ["Numa briga caótica"])
close(c, "Veredito: vitória do tigre", "smilodon", "tigre", "Cinco a um", [5, 1])
c.at("Só que, a partir daqui", foot("arctodus"))
chapters.append(c)

# 8 arctodus
c = rnd("ch09", 8, "Urso-de-cara-achatada", "Arctodus · até 900 kg", "arctodus", "", "")
c.at("Este foi um dos maiores", label("arctodus", "Rodada 8|Arctodus simus"))
c.at("Os machos maiores", measure("arctodus", "900 kg"))
c.at("Em pé, passava", measure("arctodus", "3 m", side="left"))
beats(c, "arctodus", ["De quatro, olhava", "Ele tinha pernas longas", "usava o próprio tamanho"])
c.at("Para o tigre, é como", versus("tigre", "Tigre", "200 kg", "arctodus", "Arctodus", "900 kg"))
beats(c, "tigre", ["Ele pode morder"])
beats(c, "arctodus", ["Um único golpe"])
close(c, "Veredito: vitória do urso-de-cara-achatada", "arctodus", "feras", "Cinco a dois", [5, 2])
c.at("E a próxima fera", foot("rino"))
c.at("Ela é coberta de pelos", foot("rino"))
chapters.append(c)

# 9 woolly rhino
c = rnd("ch10", 9, "Rinoceronte-lanoso", "≈ 2 toneladas · chifre de 1 m", "rino", "", "")
c.at("Coberto de pelo grosso", label("rino", "Rodada 9|Rinoceronte-lanoso"))
c.at("pesava em torno de duas", measure("rino", "2.000 kg"))
c.at("O chifre da frente", measure("rino", "1 m", side="left"))
beats(c, "rino", ["e ele usava esse chifre"])
c.at("Agora imagine esse chifre", foot("rino"))
c.at("O tigre até pode", versus("tigre", "Tigre", "200 kg", "rino", "Rinoceronte-lanoso", "2.000 kg"))
beats(c, "rino", ["Mas um adulto tem couro"])
c.at("Não existe emboscada", serif("rino", "duas toneladas.", ["Não existe emboscada que derrube"]))
close(c, "Veredito: vitória do rinoceronte-lanoso", "rino", "feras", "Cinco a três", [5, 3])
c.at("Falta uma fera", foot("mamute"))
c.at("O símbolo da Era do Gelo", foot("mamute"))
chapters.append(c)

# 10 mammoth
c = rnd("ch11", 10, "Mamute-lanoso", "6 toneladas · presas de 4 m", "mamute", "", "")
c.at("Seis toneladas", measure("mamute", "6.000 kg"))
c.at("Três metros e meio", measure("mamute", "3,5 m", side="left"))
c.at("Presas que passavam", label("mamute", "Rodada 10|Mamute-lanoso"))
beats(c, "mamute", ["O mamute-lanoso vivia", "e os adultos protegiam"])
c.at("Para o tigre, não há", versus("tigre", "Tigre", "200 kg", "mamute", "Mamute-lanoso", "6.000 kg"))
beats(c, "mamute", ["Nem os maiores predadores", "Uma pisada", "A única chance"])
close(c, "Veredito: vitória do mamute", "mamute", "feras", "Cinco a quatro", [5, 4])
hud(None, 0, 0)
c.at("E o placar das dez feras", score("final", [5, 4], [5, 4], "5 vitórias · 1 empate · 4 derrotas"))
c.at("Contra a Era do Gelo inteira", serif("tigre", "O tigre vence.", ["Contra a Era do Gelo inteira"]))
c.at("Mas lembra da rodada", foot("humano"))
c.at("Ela ainda não aconteceu", foot("humano"))
chapters.append(c)

# final round: humans
c = ch("ch12")
c.at(0, round_card("F", "O ser humano", "70 kg · sem garras · em grupo", "humano"))
c.at("O homem da Era do Gelo", foot("humano"))
beats(c, "humano", ["E, mesmo assim", "Lanças, fogo"])
c.at("Junto com o fim do frio", serif("humano", "Todos extintos.", ["O fim dos gigantes"]))
beats(c, "humano", ["Lobo-terrível, alce-gigante"])
c.at("Smilodon, urso-de-cara-achatada", foot("smilodon"))
c.at("Todos extintos", foot("humano"))
c.at("Dos onze lutadores", foot("final"))
c.at("E o tigre quase não chegou", foot("tigre"))
c.at("Hoje, graças à proteção", measure("final", "≈ 750", "Na natureza, hoje|Tigres-siberianos"))
c.at("O tigre venceu a Era do Gelo", serif("final", "Vai vencer a nossa?", ["O tigre venceu a Era do Gelo"]))
c.at("E você, concorda", foot("tigre"))
c.at("Se gostou, deixe", cta("Obrigado por assistir", "Deixe seu like e inscreva-se no Era das Feras", "final"))
chapters.append(c)

# ---------------------------------------------------------------- music: changes with the mood
MOODS = [("ch00_hook", 0, "tensao"), ("ch01", 0, "epico"), ("ch02", 0, "tensao"), ("ch04", 0, "epico"), ("ch06", 0, "tensao"),
         ("ch07", "Rodada seis", "tensao"), ("ch08", 0, "epico"), ("ch09", 0, "tensao"), ("ch11", 0, "epico"), ("ch12", 0, "drama")]
ctxs = ["hook", "tigre", "lobo", "alce", "bisao", "hiena", "urso", "leao", "smilodon", "arctodus", "rino", "mamute", "humano"]
ep = json.loads(A.finish(chapters, "FE01_Tigre_Era_do_Gelo.mp4", ctx=ctxs, music_gain=-26))
SCENE_OF = {"tigre": ["ai/ai_tiger_", "amur"], "hook": ["mammoth", "iceage", "blizzard", "tusks"], "lobo": ["wolf"],
            "alce": ["megaloceros", "gaur"], "bisao": ["bison"], "hiena": ["hyena"], "urso": ["cavebear", "cave_bear"],
            "leao": ["cavelion", "cave_lion", "chauvet", "painting_lions"], "smilodon": ["smilodon"], "arctodus": ["arctodus"],
            "rino": ["rhino"], "mamute": ["mammoth"], "humano": ["hunters", "spear", "cave_painting_torch", "thaw", "extinct"],
            "final": ["ai/ai_tiger_"]}
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
