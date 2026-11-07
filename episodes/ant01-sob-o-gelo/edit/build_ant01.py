#!/usr/bin/env python3
"""ANT01 (Abaixo de Zero): "Por Que Os Cientistas Temem o Que Existe Sob a Antártida".
    python3 build_ant01.py <narration_dir> > episode.json      (run from the work folder: a/ = assets, audio/ = narration)

Channel rules (owner, 07/11/2026): high-quality real footage first, nothing repeated, movement on every image,
varied transitions, never a black screen, highlight layouts at the key moments, music that changes with the mood.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "engine"))
import aus_kit as A
from aus_kit import P, photo, stat, say, cta, ch, questions, fx
from cues import Chapter

# ---------------------------------------------------------------- scenes: photo folders + AI scenes, in order of preference
PHOTOS = {
    "gelo": ["p_antarctica_mosaic", "p_iceberg", "p_ice_shelf", "ai:ai_white_desert", "p_station_night", "p_aurora"],
    "escala": ["p_bedmap", "ai:ai_ice_weight", "ai:ai_archipelago", "ai:ai_pao_acucar_stack", "p_pao_acucar"],
    "vostok": ["p_vostok_station", "ai:ai_vostok_1957", "ai:ai_extreme_cold", "p_bellingshausen", "p_vostok_satellite"],
    "radar": ["ai:ai_radar_plane_1970s", "p_radar_echo", "ai:ai_radar_mirror", "p_ers1", "ai:ai_satellite_ice"],
    "lago": ["ai:ai_lake_under_ice", "p_vostok_lake_map", "ai:ai_breakthrough", "ai:ai_pressure_heat", "ai:ai_cutaway_continent"],
    "perfuracao": ["ai:ai_drill_dark", "p_vostok_core", "p_ice_core_lab", "ai:ai_drill_camp", "ai:ai_kerosene_hole",
                   "ai:ai_water_rising", "ai:ai_lab_sample"],
    "vida": ["ai:ai_vostok_lake_life", "ai:ai_microbe_rock", "p_tardigrade", "ai:ai_mercer_mud", "ai:ai_ancient_stream"],
    "rede": ["ai:ai_lakes_network", "ai:ai_lake_draining", "ai:ai_hidden_rivers", "p_whillans", "ai:ai_hot_drill_camp", "p_mercer"],
    "montanhas": ["p_gamburtsev", "ai:ai_seismic_1958", "ai:ai_dome_a", "p_dome_a", "p_agap", "ai:ai_gamburtsev_reveal",
                  "ai:ai_mountains_under_ice", "p_alps", "p_pico_neblina", "ai:ai_first_glaciers", "ai:ai_ice_dome_protect"],
    "abismo": ["ai:ai_denman_canyon", "p_denman", "p_dead_sea"],
    "cachoeira": ["p_blood_falls", "ai:ai_blood_falls_dusk", "p_taylor_glacier", "ai:ai_taylor_1911", "p_dry_valleys",
                  "ai:ai_dry_valley", "ai:ai_brine_under", "ai:ai_rust_reaction", "p_griffith_taylor"],
    "espaco": ["ai:ai_europa_ocean", "p_europa", "p_mars", "ai:ai_mars_impact", "ai:ai_rock_journey"],
    "scott": ["p_scott", "p_amundsen", "p_terra_nova", "p_scott_tent", "ai:ai_scott_sledge", "ai:ai_scott_rocks", "ai:ai_scott_tent"],
    "passado": ["p_glossopteris", "ai:ai_glossopteris_forest", "p_gondwana", "ai:ai_gondwana_globe", "p_cryolophosaurus",
                "ai:ai_cryolophosaurus", "p_kirkpatrick", "ai:ai_cretaceous_rainforest", "ai:ai_polar_dark_forest",
                "p_polarstern", "ai:ai_drill_seabed", "ai:ai_fossil_roots", "p_rainforest_nz"],
    "arquivo": ["ai:ai_snow_layers", "ai:ai_air_bubbles", "p_epica", "p_beyond_epica", "ai:ai_ice_ages", "p_allan_hills"],
    "meteorito": ["p_alh84001", "p_meteorite_ice", "ai:ai_meteorite_blue_ice", "ai:ai_microfossil"],
    "thwaites": ["p_thwaites", "p_thwaites_front", "ai:ai_thwaites_front", "ai:ai_ice_river", "ai:ai_bowl_bed",
                 "ai:ai_warm_water_under", "ai:ai_tide_intrusion", "p_icefin", "ai:ai_cork"],
    "litoral": ["p_rio", "p_santos", "p_salvador", "p_recife", "p_belem", "ai:ai_flooded_beach"],
    "brasil": ["p_ferraz", "ai:ai_ferraz_station", "p_king_george", "p_df"],
    "final": ["ai:ai_hidden_world_final", "ai:ai_camera_under_ice", "p_penguins"],
}
CLIPS = json.load(open(os.path.join(HERE, "clips.json")))
GENERIC = CLIPS.pop("_generic", [])
FALLBACK = {
    "escala": ["gelo"], "vostok": ["gelo", "radar"], "radar": ["vostok", "gelo"], "lago": ["rede", "perfuracao"],
    "perfuracao": ["lago", "vostok"], "vida": ["rede", "lago"], "rede": ["lago", "vida"], "montanhas": ["gelo", "abismo"],
    "abismo": ["montanhas", "gelo"], "cachoeira": ["gelo"], "espaco": ["meteorito"], "scott": ["gelo"],
    "passado": ["scott", "gelo"], "arquivo": ["perfuracao", "gelo"], "meteorito": ["arquivo", "espaco"],
    "thwaites": ["gelo", "litoral"], "litoral": ["thwaites"], "brasil": ["gelo", "final"], "final": ["gelo"], "gelo": ["final"],
}
A.setup(sys.argv[1], os.path.join(HERE, "skip.json"), PHOTOS, CLIPS, GENERIC, FALLBACK, ["gelo", "final"])
A.CLIP_TARGET = 0.45
A.MAX_HOLD, A.KEEP = 8.0, 5.0     # owner rule: 3–6 s per shot on average; clips can run their full 8 s
chapters = []


# ---------------------------------------------------------------- highlight layouts (render_ant.py)
def compare(title, left, right, source=None, accent="left"):
    s = {"type": "compare", "title": title, "left": left, "right": right, "accent": accent, "sfx": [fx("whoosh"), fx("pop", 0.8)]}
    if source: s["source"] = source
    return s


def fact(name, tag, scene, rows, source=None):
    bg = P(scene, photo_only=True)["src"]
    s = {"type": "fact", "name": name, "tag": tag, "bg": bg, "rows": rows, "sfx": [fx("whoosh"), fx("pop", 0.5)]}
    if source: s["source"] = source
    return s


def mapa(scene, x, y, label, sub=None):
    s = {"type": "map", "src": P(scene, photo_only=True)["src"], "x": x, "y": y, "label": label, "sfx": [fx("pop", 0.3)]}
    if sub: s["sub"] = sub
    return s


def big(value, label, source=None, red=False, count=False):
    return stat(value, label, source, red=red, count=count)


# ---------------------------------------------------------------- ch00 hook (fast cuts, 2.5–4 s)
c = ch("ch00_hook", 0.6)
c.at(0, P("gelo"))
c.at("Essa é a profundidade", big("3.769 m", "o buraco mais solitário da Terra", red=True))
c.at("Cinco de fevereiro de 2012", P("vostok", cap="Estação Vostok|5 de fevereiro de 2012"))
c.at("No lugar onde já se mediu", big("−89,2 °C", "a menor temperatura já medida na superfície da Terra", "OMM"))
c.at("uma equipe russa passou", P("perfuracao"))
c.at("Metro por metro", P("perfuracao"))
c.at("Até que, numa noite", P("perfuracao"))
c.at("Embaixo dela não havia rocha", say("Embaixo dela não havia rocha.", "ROCHA.", 130))
c.at("Havia água", P("lago"))
c.at("Um lago com mais que o dobro", P("lago"))
c.at("trancado no escuro", P("lago"))
c.at("Só que esse lago era só o começo", P("rede"))
c.at("Rios que correm no escuro", P("rede"))
c.at("Uma cordilheira do tamanho dos Alpes", P("montanhas"))
c.at("O ponto mais fundo", P("abismo"))
c.at("uma cachoeira que parece sangrar", P("cachoeira"))
c.at("Neste vídeo, a gente vai remover", P("gelo"))
questions(c, ["Água líquida no lugar mais frio do mundo?", "O que foi encontrado vivo lá embaixo?", "Por que os cientistas estão com medo?"],
          ["Como pode existir água líquida", "O que foi encontrado vivo", "E por que a descoberta"])
c.at("uma coisa que está acontecendo agora", P("thwaites"))
c.at("inclusive do Brasil", P("litoral"))
chapters.append(c)

# ---------------------------------------------------------------- ch01 escala
c = ch("ch01")
c.at(0, P("gelo"))
c.at("A Antártida tem cerca de quatorze milhões", compare("Área", ["Antártida", "14 mi km²", "98% sob o gelo"], ["Brasil", "8,5 mi km²", ""]))
c.at("a maior massa de gelo do planeta", P("gelo"))
c.at("A espessura média passa de dois quilômetros", P("escala"))
c.at("No ponto mais grosso", big("4.776 m", "a parte mais grossa da camada de gelo", "BedMachine"))
c.at("Mais alto que qualquer montanha", P("gelo"))
c.at("Ali está guardada perto de setenta por cento", big("70%", "da água doce da Terra"))
c.at("os oceanos subiriam cerca de cinquenta e oito metros", big("+58 m", "no nível dos oceanos se tudo derretesse", "BedMachine", red=True))
c.at("Altura de um prédio", P("litoral"))
c.at("Agora, um detalhe que quase ninguém conhece", P("escala"))
c.at("A crosta da Terra", P("escala"))
c.at("Em muitos lugares, o chão", P("escala"))
c.at("Seria um arquipélago", P("escala"))
c.at("Ou seja: quando você olha", P("gelo"))
c.at("Está vendo a tampa", say("Você está vendo a tampa.", "TAMPA.", 140))
c.at("O continente de verdade", P("gelo"))
c.at("A primeira pista apareceu", P("vostok"))
chapters.append(c)

# ---------------------------------------------------------------- ch02 vostok
c = ch("ch02")
c.at(0, P("vostok"))
c.at("O nome escolhido foi Vostok", P("vostok"))
c.at("A estação fica a quase", mapa("gelo", 0.62, 0.55, "Estação Vostok", "3.488 m de altitude"))
c.at("foi ali, em 21 de julho de 1983", big("−89,2 °C", "21 de julho de 1983 · Vostok", "OMM", red=True))
c.at("Nesse frio, o aço", P("vostok"))
c.at("Ninguém imaginaria", P("gelo"))
c.at("Mas os sinais foram aparecendo", P("radar"))
c.at("O radar atravessa o gelo", P("radar"))
c.at("Perto de Vostok, ele voltava liso", P("radar"))
c.at("Nos anos 1990, satélites", P("radar"))
c.at("Era o gelo flutuando", P("lago"))
c.at("Em 1996, cientistas russos", P("vostok", cap="1996|a confirmação"))
c.at("O Lago Vostok tem cerca de", fact("Lago Vostok", "confirmado em 1996", "lago",
     [["comprimento", "~250 km"], ["largura", "~50 km"], ["profundidade", "+800 m"], ["gelo por cima", "~3,7 km"]]))
c.at("Agora, a pergunta óbvia", say("Por que essa água não congela?", "CONGELA?", 120))
c.at("A primeira é a pressão", P("lago"))
c.at("A segunda é o calor", P("lago"))
c.at("A terceira é a própria camada", P("gelo"))
c.at("O resultado é um lago escuro", P("lago"))
c.at("será que existe alguma coisa viva", P("vida"))
chapters.append(c)

# ---------------------------------------------------------------- ch03 perfuração (tension)
c = ch("ch03")
c.at(0, P("perfuracao"))
c.at("Cada camada é neve", P("arquivo"))
c.at("Quando o lago foi confirmado", P("perfuracao"))
c.at("Não por falta de tecnologia", say("Não por falta de tecnologia. Por medo.", "MEDO.", 120))
c.at("O problema era o que estava dentro", P("perfuracao"))
c.at("Seria como abrir um cofre", P("perfuracao"))
c.at("Durante mais de uma década", P("perfuracao"))
c.at("A solução russa foi engenhosa", P("lago"))
c.at("Depois, essa água congelaria", P("perfuracao"))
c.at("Na noite de 5 de fevereiro de 2012", big("3.769,3 m", "5 de fevereiro de 2012 · a broca chega à água", "Nature", red=True))
c.at("E, exatamente como previsto", P("perfuracao"))
c.at("As amostras foram analisadas", P("perfuracao"))
c.at("Em 2013, pesquisadores russos", P("vida"))
c.at("Mas logo surgiram dúvidas", P("perfuracao"))
c.at("Até hoje, não existe prova", say("Até hoje, nenhuma prova definitiva.", "NENHUMA", 120))
c.at("Só que, enquanto todos olhavam", P("rede"))
c.at("E dentro dela, a vida", P("vida"))
chapters.append(c)

# ---------------------------------------------------------------- ch04 rede de lagos e vida
c = ch("ch04")
c.at(0, big("675", "lagos escondidos sob o gelo da Antártida", "Livingstone et al., 2022", count=True))
c.at("Alguns são do tamanho de uma lagoa", P("rede"))
c.at("E muitos deles não estão parados", P("rede"))
c.at("Em 2006, cientistas analisando", P("radar"))
c.at("A quase trezentos quilômetros", P("rede"))
c.at("Bilhões de toneladas de água", P("rede"))
c.at("Isso mudou completamente", P("gelo"))
c.at("Por baixo dela existe um sistema", P("rede"))
c.at("Em janeiro de 2013", fact("Lago Whillans", "perfurado em jan/2013", "rede", [["gelo por cima", "~800 m"], ["broca", "água quente esterilizada"]]))
c.at("O que eles encontraram foi vida", P("vida"))
c.at("Cada mililitro de água", big("130 mil", "células por mililitro de água", "Christner et al., Nature 2014"))
c.at("Como eles sobrevivem", P("vida"))
c.at("Esses micróbios tiram energia", P("vida"))
c.at("Um ecossistema inteiro", P("vida"))
c.at("A surpresa seguinte foi ainda maior", P("rede", cap="Lago Mercer|2019"))
c.at("Na lama do fundo", P("vida"))
c.at("e de um tardígrado", P("vida"))
c.at("Esses animais estavam mortos", P("vida"))
c.at("A hipótese mais aceita", P("vida"))
c.at("Ou seja: o subsolo", P("gelo"))
c.at("Até a rocha", P("montanhas"))
chapters.append(c)

# ---------------------------------------------------------------- ch05 montanhas e abismos
c = ch("ch05")
c.at(0, P("montanhas"))
c.at("O método é simples", P("montanhas"))
c.at("Numa região chamada Domo A", mapa("gelo", 0.55, 0.5, "Domo A", "o ponto mais alto do gelo"))
c.at("Os cientistas tinham acabado", P("montanhas"))
c.at("Por quase cinquenta anos", P("montanhas"))
c.at("O que apareceu nas telas", P("montanhas"))
c.at("As Gamburtsev têm cerca de", fact("Montanhas Gamburtsev", "descobertas em 1958", "montanhas",
     [["extensão", "~1.200 km"], ["picos", "2.700 a 3.400 m"], ["gelo por cima", "centenas de metros"]]))
c.at("Vales profundos, encostas íngremes", P("montanhas"))
c.at("Mesmo nos picos mais altos", P("montanhas"))
c.at("Aí surgiu um enigma", P("montanhas"))
c.at("Como uma cordilheira tão velha", say("Velha demais para ter cara de nova.", "NOVA.", 120))
c.at("A explicação mais aceita", P("montanhas"))
c.at("Há cerca de trinta e quatro milhões", P("montanhas"))
c.at("A camada que hoje cobre", P("gelo"))
c.at("E se o gelo esconde montanhas", P("abismo"))
c.at("O fundo dele está a três mil e quinhentos", big("−3.500 m", "o fundo do cânion da Geleira Denman", "Morlighem et al., 2019", red=True))
c.at("Para comparar", compare("Abaixo do nível do mar", ["Mar Morto", "−430 m", "margem"], ["Cânion da Denman", "−3.500 m", "8x mais fundo"], accent="right"))
c.at("É o ponto mais baixo", P("abismo"))
c.at("Montanhas, abismos, lagos e rios", P("gelo"))
c.at("Mas existe um lugar na Antártida", P("cachoeira"))
chapters.append(c)

# ---------------------------------------------------------------- ch06 CTA + cachoeira de sangue
c = ch("ch06")
c.at(0, cta("Gostando dessa descida?", "Inscreva-se e ative o sininho · é de graça"))
c.at("Agora, vamos para a cachoeira de sangue", P("cachoeira"))
c.at("Em 1911, uma expedição britânica", mapa("cachoeira", 0.5, 0.5, "Vales Secos de McMurdo"))
c.at("São vales enormes", P("cachoeira"))
c.at("A paisagem lembra tanto Marte", P("espaco"))
c.at("O geólogo da expedição", P("cachoeira"))
c.at("Da parede de gelo branco", P("cachoeira"))
c.at("Hoje ela leva o nome dele", P("cachoeira", cap="Geleira Taylor|Vales Secos de McMurdo"))
c.at("A primeira explicação", P("cachoeira"))
c.at("Debaixo da Geleira Taylor", P("cachoeira"))
c.at("cerca de duas vezes e meia", big("2,5x", "mais salgada que o mar", "Mikucki et al., Science 2009"))
c.at("Enquanto está presa sob o gelo", P("cachoeira"))
c.at("o ferro reage", P("cachoeira"))
c.at("Tem mais", P("vida"))
c.at("Pelas estimativas, eles estão isolados", big("1,5 milhão", "de anos isolados sob a geleira", "Mikucki et al., Science 2009"))
c.at("Anos depois, levantamentos", P("cachoeira"))
c.at("A Cachoeira de Sangue virou", P("cachoeira"))
c.at("Debaixo do gelo das luas", P("espaco"))
c.at("Mas o subsolo antártico", P("gelo"))
chapters.append(c)

# ---------------------------------------------------------------- ch07 Scott e a Antártida verde
c = ch("ch07")
c.at(0, P("scott", cap="Expedição Terra Nova|1912"))
c.at("Chegaram lá apenas para descobrir", P("scott"))
c.at("Na volta, famintos", P("scott"))
c.at("Carregam junto cerca de dezesseis quilos", big("16 kg", "de pedras arrastadas no trenó", "Natural History Museum"))
c.at("Scott e os dois últimos companheiros", P("scott"))
c.at("Quando a equipe de resgate", P("scott"))
c.at("eram fósseis de plantas", P("passado"))
c.at("A Glossopteris viveu", P("passado"))
c.at("Inclusive aqui no Brasil", P("passado"))
c.at("A Antártida fazia parte", P("passado"))
c.at("Depois vieram os dinossauros", P("passado"))
c.at("Ganhou o nome de Criolofossauro", P("passado"))
c.at("A descoberta mais impressionante", P("passado"))
c.at("Dentro dela havia uma rede de raízes", P("passado"))
c.at("Eram restos de uma floresta", P("passado"))
c.at("Essa floresta crescia a cerca de", big("900 km", "do Polo Sul · há 90 milhões de anos", "Klages et al., Nature 2020"))
c.at("Num lugar que passava quatro meses", P("passado"))
c.at("Mesmo assim, a temperatura média", big("~12 °C", "de média anual perto do Polo Sul", "Klages et al., Nature 2020"))
c.at("Então, se a Antártida já foi floresta", P("gelo"))
chapters.append(c)

# ---------------------------------------------------------------- ch08 o gelo como arquivo
c = ch("ch08")
c.at(0, P("arquivo"))
c.at("Essas bolhas são amostras", P("arquivo"))
c.at("Em 2004, um projeto europeu", P("arquivo", cap="EPICA|Domo C"))
c.at("As análises mostraram", big("800 mil anos", "de clima registrados no gelo", "EPICA, 2004"))
c.at("Em janeiro de 2025", big("1,2 milhão", "de anos · Beyond EPICA, 2025", "comunicado de 09/01/2025"))
c.at("Em outros lugares, como as colinas", P("arquivo"))
c.at("Mas o gelo guarda coisas", P("meteorito"))
c.at("Eles caem no planeta inteiro", P("meteorito"))
c.at("Dezenas de milhares de meteoritos", P("meteorito"))
c.at("Um deles virou um dos maiores mistérios", P("meteorito"))
c.at("Anos depois, a análise revelou", P("espaco"))
c.at("caiu na Antártida há uns treze mil anos", P("espaco"))
c.at("Em 1996, cientistas da NASA", P("meteorito", cap="ALH84001|meteorito de Marte"))
c.at("O presidente dos Estados Unidos", P("espaco"))
c.at("Mas a pergunta nunca foi totalmente", say("A pergunta nunca foi encerrada.", "ENCERRADA.", 120))
c.at("Lagos escondidos, montanhas soterradas", P("gelo"))
c.at("Só que existe um problema", P("thwaites"))
c.at("E a parte mais importante", P("thwaites"))
chapters.append(c)

# ---------------------------------------------------------------- ch09 Thwaites (climax)
c = ch("ch09")
c.at(0, P("rede"))
c.at("A água na base funciona como lubrificante", P("thwaites"))
c.at("O gelo da Antártida está sempre em movimento", P("thwaites"))
c.at("Por muito tempo, isso ficou em equilíbrio", P("gelo"))
c.at("A Antártida está perdendo mais gelo", say("A Antártida está perdendo mais gelo do que ganha.", "PERDENDO", 110))
c.at("E o ponto mais preocupante tem nome", fact("Geleira Thwaites", "oeste da Antártida", "thwaites",
     [["área", "~192 mil km² (≈ Paraná)"], ["apelido", "geleira do Juízo Final"]], "ITGC"))
c.at("Lembra que o peso do gelo", P("thwaites"))
c.at("Boa parte da geleira", P("thwaites"))
c.at("É como uma tigela", P("thwaites"))
c.at("Na frente da Thwaites", P("thwaites"))
c.at("Em 2024, um estudo", P("thwaites", cap="2024|água do mar sob o gelo na maré alta"))
c.at("Muito mais do que se imaginava", P("thwaites"))
c.at("A Thwaites sozinha guarda", big("+65 cm", "no nível do mar só com a Thwaites", "ITGC / BedMachine", red=True))
c.at("Mas o maior problema", P("thwaites"))
c.at("que somado poderia elevar", big("+3 m", "com o gelo do oeste da Antártida", "ITGC", red=True))
c.at("Ninguém sabe dizer exatamente", P("gelo"))
c.at("Mas mesmo algumas dezenas de centímetros", P("litoral"))
c.at("No Brasil, são milhões de pessoas", P("litoral", cap="Rio de Janeiro"))
c.at("Santos, Salvador, Recife e Belém", P("litoral"))
c.at("Essa é a grande reviravolta", say("O perigo está no que ninguém vê.", "NINGUÉM", 120))
c.at("Mas o que vai decidir o futuro", P("thwaites"))
c.at("na água, na rocha", P("final"))
chapters.append(c)

# ---------------------------------------------------------------- ch10 fechamento + CTA final (sem gancho para outro vídeo)
c = ch("ch10", 1.5)
c.at(0, P("brasil"))
c.at("Desde 1984, o país tem", fact("Estação Antártica Comandante Ferraz", "Brasil na Antártida", "brasil",
     [["desde", "1984"], ["onde", "Ilha Rei George"]], "Marinha do Brasil / PROANTAR"))
c.at("Vista de cima, a Antártida parece vazia", P("gelo"))
c.at("Mas, por baixo dessa tampa", P("final"))
c.at("lagos maiores que cidades", P("lago"))
c.at("montanhas do tamanho dos Alpes", P("montanhas"))
c.at("E a gente só começou a enxergar", P("final"))
c.at("Agora eu quero saber de você", {"type": "questions", "items": ["Lago Vostok?", "Montanhas Gamburtsev?", "Cachoeira de Sangue?"],
                                                         "sfx": [fx("pop")]})
c.at("E se este vídeo te mostrou", cta("Obrigado por assistir", "Deixe seu like e inscreva-se no Abaixo de Zero"))
chapters.append(c)

# ---------------------------------------------------------------- music: the track changes with the mood (owner rule)
MOODS = [  # (chapter, phrase or 0, mood)
    ("ch00_hook", 0, "tensao"), ("ch00_hook", "Só que esse lago era só o começo", "misterio"),
    ("ch01", 0, "maravilha"), ("ch02", 0, "frio"), ("ch02", "Mas os sinais foram aparecendo", "misterio"),
    ("ch03", "Não por falta de tecnologia", "tensao"), ("ch03", "As amostras foram analisadas", "misterio"),
    ("ch04", 0, "maravilha"), ("ch05", 0, "epico"), ("ch05", "E se o gelo esconde montanhas", "tensao"),
    ("ch06", "Agora, vamos para a cachoeira", "misterio"), ("ch07", 0, "drama"), ("ch07", "A Glossopteris viveu", "maravilha"),
    ("ch08", 0, "misterio"), ("ch08", "Só que existe um problema", "tensao"), ("ch09", 0, "tensao"),
    ("ch10", 0, "reflexivo"),
]
GAIN = {"tensao": -26, "epico": -27, "misterio": -27, "drama": -28, "maravilha": -28, "frio": -28, "reflexivo": -28}

ep = json.loads(A.finish(chapters, "ANT01_Sob_o_Gelo.mp4", ctx=["gelo", "gelo", "vostok", "perfuracao", "rede", "montanhas",
                                                                  "cachoeira", "passado", "arquivo", "thwaites", "final"]))   # sem legendas gravadas no vídeo (pedido do dono, 07/11/2026)
starts, t = {}, 0.0
for chap in ep["chapters"]:
    starts[os.path.splitext(os.path.basename(chap["audio"]))[0]] = t
    t += sum(s["dur"] for s in chap["shots"])
total = t
marks = []
for name, phrase, mood in MOODS:
    if phrase == 0:
        marks.append((starts[name], mood)); continue
    probe = Chapter(name, f"{sys.argv[1]}/{name}.txt", f"a/words/{name}.words.json", f"audio/{name}.flac")
    sec = probe.find(phrase)
    if sec is None:
        sys.exit(f"trilha: frase não encontrada em {name}: {phrase}")
    marks.append((starts[name] + max(0.0, sec - 1.0), mood))   # the change lands just before the line
music = []
for k, (st, mood) in enumerate(marks):
    en = marks[k + 1][0] if k + 1 < len(marks) else total
    music.append({"file": f"musica/{mood}.mp3", "start": round(max(0.0, st - 1.2), 2), "end": round(min(total, en + 1.2), 2),
                  "gain": GAIN[mood], "fade_in": 2.0 if k else 0.5, "fade_out": 2.4 if k + 1 < len(marks) else 5})
ep["music"] = music
sys.stderr.write(f"trilha: {len(music)} trocas de clima, {total / 60:.1f} min\n")
print(json.dumps(ep, indent=1, ensure_ascii=False))
