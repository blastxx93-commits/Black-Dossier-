#!/usr/bin/env python3
"""FE04 (Era das Feras): "O Primeiro Dinossauro do Brasil" — investigation format, HyperFrames graphics package.
    python3 build_fe04.py <narration_dir> > episode.json      (run from the work folder: a/ = assets, audio/ = narration)
Also writes edit/hf_cards.json (cards rendered by engine/hf_cards.py in the render workflow).
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "engine"))
import aus_kit as A
import feras_kit as F
from feras_kit import foot, hf

ai = lambda *ids: ["ai:ai_" + i for i in ids]
fa = lambda *n: ai(*[f"fauna_{k:02d}" for k in n])
la = lambda *n: ai(*[f"land_{k:02d}" for k in n])
PHOTOS = {
    "stauri": ai("stauri_run", "stauri_hunt") + fa(1, 2, 3, 4, 5, 6, 7, 8, 9) + ["p_stauri"] + ai(*[f"more2_st_{k:02d}" for k in range(1, 9)]) + ai("more_st_01", "more_st_02", "more_st_03", "more_st_04", "more_st_05", "more_st_06", "more_st_07", "more_st_08", "more_st_09", "more_st_10"),
    "presto": ai("presto_hero", "presto_jaws", "stauri_vs_presto") + fa(10, 11, 12) + ["p_presto"],
    "hyper": ai("hyper_herd") + fa(13, 14, 15) + ["p_hyper"],
    "cyno": fa(16, 17, 18) + ["p_exaeretodon"],
    "tri": la(1, 2, 3, 4, 7, 26, 27) + fa(35) + ["p_horsetail", "p_araucaria"],
    "pangea": la(8) + ["p_pangea"],
    "chuva": la(5, 6),
    "dig": ai("hook_dig") + la(9, 21, 24) + ["p_fossil_dig", "p_red_rock"] + ai("more_dig_01", "more_dig_02", "more_dig_03", "more_dig_04"),
    "museu": la(14, 15, 16) + ["p_fossil_museum", "p_colbert"],
    "navio": la(13),
    "ceu": la(12) + ["p_cruzeiro"],
    "satur": ai("saturnalia") + fa(22, 23) + ["p_saturnalia"] + ai("more_sa_01", "more_sa_02", "more_sa_03", "more_sa_04"),
    "buri": ai("buriolestes") + fa(24, 25, 26) + ["p_buriolestes", "p_ixalerpeton"] + ai("more2_bu_01") + ai("more_bu_01", "more_bu_02", "more_bu_03", "more_bu_04", "more_bu_05"),
    "gnatho": ai("gnatho_hunt") + fa(19, 20, 21) + ["p_gnatho"] + ai("more2_gn_01", "more2_gn_02") + ai("more_gn_01", "more_gn_02", "more_gn_03", "more_gn_04", "more_gn_05"),
    "ciencia": la(17, 22, 23) + ["p_ct_scan"],
    "macro": ai("macro_neck") + fa(27, 28) + la(25) + ai("more2_ma_01", "more2_ma_02") + ai("more_ma_01", "more_ma_02", "more_ma_03", "more_ma_04", "more_ma_05"),
    "argentina": fa(33, 34) + ["p_herrera", "p_eoraptor", "p_ischigualasto", "p_nyasa"],
    "extincao": la(18, 19, 20) + ["p_trap"],
    "gigantes": ai("dino_takeover") + fa(29, 30, 31, 32) + ["p_sauropod_mount", "p_trex"],
    "rs": la(10, 11) + ["p_rs_landscape", "p_ufsm", "p_araucaria", "p_paleorrota", "p_agudo", "p_polesine", "p_cappa", "p_santamaria2"] + ai("more_rs_01", "more_rs_02", "more_rs_03", "more_rs_04", "more_rs_05", "more_rs_06"),
}
CL = json.load(open(os.path.join(HERE, "clips.json")))
CLIPS = {"tri": CL["rio"] + CL["plantas"] + CL["seco"], "chuva": CL["cheia"], "presto": CL["croc"], "hyper": CL["lagarto"][:2],
         "cyno": CL["lagarto"][2:], "extincao": CL["vulcao"], "ceu": CL["ceu"], "ciencia": CL["lab"], "rs": CL["rs"],
         "gigantes": CL["aves"], "pangea": CL["espaco"]}
GENERIC = CL["rio"] + CL["plantas"] + CL["seco"]
FALLBACK = {k: ["tri"] for k in PHOTOS}
FALLBACK.update({"stauri": ["tri", "dig"], "presto": ["tri"], "gnatho": ["stauri", "tri"], "satur": ["buri", "tri"], "buri": ["satur", "tri"],
                 "macro": ["satur", "tri"], "museu": ["dig"], "navio": ["museu", "dig"], "ceu": ["tri"], "ciencia": ["dig", "museu"],
                 "argentina": ["tri", "stauri"], "extincao": ["chuva", "tri"], "gigantes": ["tri"], "rs": ["dig"], "dig": ["rs"],
                 "chuva": ["tri"], "pangea": ["tri"], "cyno": ["tri", "hyper"], "hyper": ["tri", "cyno"], "tri": ["chuva"]})
PIN_IDS = ["ai_stauri_hero", "ai_stauri_portrait", "ai_gnatho_hero", "ai_macro_trio", "ai_presto_hero", "p_herrera/2",
           "p_colbert/1", "p_ixalerpeton/1", "p_nyasa/1", "ai_hyper_herd", "p_rs_landscape/2", "ai_dino_takeover"]
A.setup(sys.argv[1], os.path.join(HERE, "skip.json"), PHOTOS, CLIPS, GENERIC, FALLBACK, ["tri"])
A.CFG["reviewed"] = set(json.load(open(os.path.join(HERE, "reviewed.json"))))
F.pin(*PIN_IDS)
A.CLIP_TARGET = 0.30
A.MAX_HOLD, A.KEEP = 6.5, 4.0
ch = A.ch
chapters = []


def cap(c, num, title, scene):
    c.at(0, hf("capitulo", num=f"{num:02d}", title=title, img=f"scene:{scene}", move="push"))


def beats(c, scene, phrases):
    for p in phrases:
        c.at(p, foot(scene))


# ---------------------------------------------------------------- hook
c = ch("ch00_hook")
c.at(0, foot("dig"))
c.at("num barranco de terra vermelha", foot("rs"))
c.at("um homem encontrou alguns ossos", foot("dig"))
c.at("Eles foram embalados", foot("navio"))
c.at("Durante trinta e quatro anos", hf("frase", text="34 anos sem *resposta.*", img="scene:museu"))
c.at("Quando finalmente estudaram", foot("museu"))
c.at("Eles pertenciam a um dos", foot("stauri"))
c.at("Porque o Brasil não é só", foot("tri"))
c.at("Pode ser um dos lugares", hf("frase", text="Onde *tudo* começou.", img="scene:tri"))
c.at("Só que esses dinossauros pioneiros", foot("stauri"))
c.at("Eram pequenos, magros", foot("stauri"))
c.at("E viviam cercados", foot("presto"))
c.at("Então como esses bichos", hf("perguntas", img="scene:tri", items=[
    "Como bichos tão pequenos dominaram o planeta?", "Quem era o verdadeiro predador do Sul?", "Que segredo estava escondido nos ossos?"]))
c.at("Fica até o final", hf("titulo", kicker="Era das Feras", title="O Primeiro Dinossauro do Brasil",
                            sub="Rio Grande do Sul · 233 milhões de anos atrás", img="ai_stauri_hero", blurin=True))
chapters.append(c)

# ---------------------------------------------------------------- the world
c = ch("ch01")
cap(c, 1, "O mundo de 233 milhões de anos atrás", "tri")
c.at("O mapa do mundo era outro", foot("pangea"))
c.at("Todos os continentes", foot("pangea"))
c.at("O Rio Grande do Sul não tinha mar", foot("tri"))
c.at("O clima era quente", foot("tri"))
c.at("Rios largos e rasos", foot("tri"))
c.at("e quando vinham as chuvas", foot("chuva"))
c.at("Era nessas enchentes", foot("chuva"))
c.at("É por isso que hoje", foot("dig"))
c.at("E aqui vem a primeira surpresa", hf("frase", text="Os dinossauros *não mandavam.*", img="scene:tri"))
c.at("Eles tinham acabado de aparecer", foot("stauri"))
c.at("Eram raros, pequenos", foot("stauri"))
chapters.append(c)

# ---------------------------------------------------------------- the masters of the Triassic
c = ch("ch02")
cap(c, 2, "Os donos do Triássico", "hyper")
c.at("Os mais comuns eram", hf("rotulo", img="ai_hyper_herd", kicker="O animal mais comum", name="Hiperodápedon", sci="Hyperodapedon · rincossauro"))
c.at("Pareciam um porco", foot("hyper"))
c.at("Em alguns sítios", foot("hyper"))
c.at("Eles eram o gado", foot("hyper"))
c.at("Junto com eles viviam", hf("rotulo", img="scene:cyno", kicker="Parentes dos mamíferos", name="Cinodontes", side="right"))
c.at("Eles são parentes distantes", foot("cyno"))
c.at("Ou seja, parentes distantes de você", foot("cyno"))
c.at("E acima de todos", foot("presto"))
c.at("Alguns milhões de anos antes", hf("rotulo", img="ai_presto_hero", kicker="O terror do Triássico", name="Prestossuco", sci="Prestosuchus chiniquensis · até 7 m"))
c.at("que andava com as pernas retas", foot("presto"))
c.at("E os parentes dele continuaram", foot("presto"))
c.at("Agora imagina ser um dinossauro", hf("escala", kicker="Comparação de tamanho", title="Quem era maior?",
                                          rows=[["Humano", 1.75, "h"], ["Estauricossauro", 2.1], ["Prestossuco", 7]]))
c.at("Muitas vezes, você era", hf("frase", text="Muitas vezes, você era a *caça.*", img="scene:presto"))
chapters.append(c)

# ---------------------------------------------------------------- the discovery
c = ch("ch03")
cap(c, 3, "Os ossos de Santa Maria", "dig")
c.at("o paleontólogo brasileiro", foot("dig"))
c.at("Perto de Santa Maria", hf("mapa", kicker="Onde foi achado", title="Santa Maria · RS",
                                sub="Região central do Rio Grande do Sul, um dos lugares com dinossauros mais antigos do mundo", lon=-53.81, lat=-29.69))
c.at("Os ossos foram para o museu", foot("navio"))
c.at("E ficaram lá", foot("museu"))
c.at("o paleontólogo americano", hf("rotulo", img="p_colbert/1", kicker="Paleontólogo americano", name="Edwin Colbert", sci="Estudou os ossos em 1970"))
c.at("Aquilo não era um réptil", foot("stauri"))
c.at("Era um dinossauro", foot("stauri"))
c.at("Ele deu o nome", hf("rotulo", img="scene:ceu", kicker="Lagarto do Cruzeiro do Sul", name="Estauricossauro", sci="Staurikosaurus pricei · 1970"))
c.at("E o sobrenome", foot("dig"))
c.at("O primeiro dinossauro famoso", hf("frase", text="Batizado com o nome de uma *estrela.*", img="scene:ceu"))
c.at("E o fóssil original", foot("museu"))
chapters.append(c)

# ---------------------------------------------------------------- Staurikosaurus
c = ch("ch04")
cap(c, 4, "O caçador do Cruzeiro do Sul", "stauri")
c.at("Ele tinha pouco mais de dois metros", hf("ficha", img="scene:stauri", kicker="Ficha", name="Estauricossauro", sci="Staurikosaurus pricei",
                                               rows=[["Comprimento", "~2 m"], ["Peso", "~30 kg"], ["Viveu", "233 mi de anos"], ["Achado", "Santa Maria, RS"]],
                                               source="Estimativas: Colbert (1970) e estudos posteriores"))
c.at("A boca era cheia", foot("stauri"))
c.at("E a mandíbula tinha", foot("stauri"))
c.at("Ele era um caçador rápido", foot("stauri"))
c.at("Provavelmente perseguia", foot("stauri"))
c.at("Nada de enfrentar", foot("stauri"))
c.at("E tem um detalhe curioso", hf("comparar", limg="p_herrera/2", rimg="ai_stauri_portrait", lkick="Parente próximo",
                                    lname="Herrerassauro", rkick="Reconstrução", rname="Estauricossauro"))
c.at("Mas o Estauricossauro estava longe", foot("stauri"))
c.at("E o que apareceu depois", foot("gnatho"))
chapters.append(c)

# ---------------------------------------------------------------- Saturnalia
c = ch("ch05")
c.at(0, hf("cta", img="scene:tri", text="Está curtindo a história?", sub="Deixa o like e se inscreve no canal"))
c.at("uma equipe encontrou outro dinossauro", foot("satur"))
c.at("Como a descoberta aconteceu", foot("satur"))
c.at("Saturnália tupiniquim", hf("rotulo", img="scene:satur", kicker="Achado no carnaval de 1999", name="Saturnália", sci="Saturnalia tupiniquim"))
c.at("Ele tinha mais ou menos", foot("satur"))
c.at("E isso é importante", foot("gigantes"))
c.at("aqueles gigantes de pescoço longo", foot("gigantes"))
c.at("Ou seja, a família", hf("frase", text="Os maiores começaram do tamanho de um *cachorro.*", img="scene:satur"))
chapters.append(c)

# ---------------------------------------------------------------- Buriolestes
c = ch("ch06")
cap(c, 5, "O ancestral carnívoro", "buri")
c.at("No município de São João", foot("rs"))
c.at("os pesquisadores encontraram o Buriolestes", hf("rotulo", img="scene:buri", kicker="São João do Polêsine · 2016", name="Buriolestes", sci="Buriolestes schultzi"))
c.at("Ele também era", foot("buri"))
c.at("Só que o Buriolestes", foot("buri"))
c.at("Ele era carnívoro", hf("frase", text="Ele era *carnívoro.*", img="scene:buri"))
c.at("Isso significa", foot("gigantes"))
c.at("Só milhões de anos depois", foot("gigantes"))
c.at("E no mesmo bloco de rocha", hf("rotulo", img="p_ixalerpeton/1", kicker="Primo dos pterossauros", name="Ixalérpeton", sci="Ixalerpeton polesinensis", side="right"))
c.at("Dois ramos diferentes da família", foot("buri"))
chapters.append(c)

# ---------------------------------------------------------------- Gnathovorax
c = ch("ch07")
cap(c, 6, "Mandíbula voraz", "gnatho")
c.at("Um parente próximo", hf("ficha", img="ai_gnatho_hero", kicker="Ficha", name="Gnatovórax", sci="Gnathovorax cabreirai",
                              rows=[["Comprimento", "~3 m"], ["Apresentado", "2019"], ["Achado", "São João do Polêsine, RS"], ["Destaque", "crânio completo"]]))
c.at("Lembra que do Estauricossauro", foot("gnatho"))
c.at("Ele é considerado", foot("gnatho"))
c.at("Com ele, os cientistas", foot("gnatho"))
c.at("E não pararam nos ossos", foot("ciencia"))
c.at("As áreas ligadas", foot("ciencia"))
c.at("É o cérebro de um caçador", foot("gnatho"))
c.at("Pela primeira vez", foot("gnatho"))
chapters.append(c)

# ---------------------------------------------------------------- Macrocollum
c = ch("ch08")
cap(c, 7, "O primeiro pescoço longo", "macro")
c.at("Os pesquisadores encontraram três esqueletos", foot("macro"))
c.at("O nome quer dizer", hf("rotulo", img="ai_macro_trio", kicker="Agudo, RS · 2018", name="Macrocolo", sci="Macrocollum itaquii · ~3,5 m"))
c.at("O Macrocolo viveu", hf("numero", img="scene:macro", value=225, unit="milhões de anos", label="o dinossauro de pescoço longo mais antigo já encontrado"))
c.at("É o primeiro passo", foot("gigantes"))
c.at("E tem mais", foot("macro"))
c.at("Se isso estiver certo", foot("macro"))
c.at("Mas tem uma pergunta", hf("frase", text="Os mais antigos do *mundo?*", img="scene:tri"))
chapters.append(c)

# ---------------------------------------------------------------- the oldest?
c = ch("ch09")
cap(c, 8, "Os mais antigos do mundo?", "dig")
c.at("cientistas dataram cristais", foot("ciencia"))
c.at("Esses cristais funcionam", foot("ciencia"))
c.at("E o resultado foi", hf("numero", img="scene:dig", value=233, unit="milhões de anos", label="idade das rochas dos primeiros dinossauros gaúchos"))
c.at("Isso coloca os fósseis", hf("linha", kicker="Linha do tempo", title="Entre os primeiros do planeta", ma=233,
                                  label="233 milhões de anos", sub="Rio Grande do Sul · Triássico"))
c.at("Um pouco mais antigos até", foot("argentina"))
c.at("como o Eorraptor", foot("argentina"))
c.at("Existem candidatos mais antigos", hf("rotulo", img="p_nyasa/1", kicker="Tanzânia · candidato", name="Niassassauro", sci="Nyasasaurus parringtoni"))
c.at("Mas os fósseis dele são poucos", foot("argentina"))
c.at("Então o título", foot("stauri"))
c.at("Mas o Brasil está", foot("rs"))
chapters.append(c)

# ---------------------------------------------------------------- how they won
c = ch("ch10")
cap(c, 9, "Como eles venceram", "chuva")
c.at("A primeira pista", foot("chuva"))
c.at("Os cientistas chamam", foot("chuva"))
c.at("Muitos animais sofreram", foot("tri"))
c.at("E segundo várias pesquisas", foot("stauri"))
c.at("A segunda pista", foot("extincao"))
c.at("No fim do Triássico", foot("extincao"))
c.at("e causou uma das maiores extinções", foot("extincao"))
c.at("Grande parte dos parentes", foot("presto"))
c.at("E os dinossauros sobreviveram", hf("frase", text="E os dinossauros *sobreviveram.*", img="scene:stauri"))
c.at("Com os rivais fora do caminho", foot("gigantes"))
c.at("Os pequenos corredores", hf("rotulo", img="ai_dino_takeover", kicker="Mais de 130 milhões de anos", name="A era dos dinossauros"))
chapters.append(c)

# ---------------------------------------------------------------- the secret
c = ch("ch11")
cap(c, 10, "O segredo nos ossos", "stauri")
c.at("O Tiranossauro", foot("gigantes"))
c.at("todos vieram de animais pequenos", foot("stauri"))
c.at("E a história continua", foot("rs"))
c.at("A região central do estado", hf("rotulo", img="p_rs_landscape/2", kicker="Geoparque mundial da UNESCO", name="Quarta Colônia", sci="Região central do Rio Grande do Sul"))
c.at("Pesquisadores da Universidade", foot("rs"))
c.at("O próximo dinossauro", foot("dig"))
c.at("esperando alguém passar", foot("dig"))
c.at("E você, sabia", foot("stauri"))
c.at("Escreve aqui nos comentários", foot("rs"))
c.at("E se você curtiu", hf("cta", img="scene:stauri", text="Obrigado por assistir", sub="Deixa o like e se inscreve no Era das Feras"))
chapters.append(c)

MOODS = [("ch00_hook", 0, "tensao"), ("ch01", 0, "epico"), ("ch02", 0, "tensao"), ("ch03", 0, "drama"), ("ch04", 0, "tensao"),
         ("ch05", 0, "epico"), ("ch07", 0, "tensao"), ("ch09", 0, "drama"), ("ch10", 0, "tensao"), ("ch10", "E os dinossauros sobreviveram", "epico"),
         ("ch11", 0, "drama")]
ctxs = ["dig", "tri", "hyper", "dig", "stauri", "satur", "buri", "gnatho", "macro", "argentina", "extincao", "rs"]
SCENE_OF = {"tri": ["ai_land_0", "ai_land_26", "p_horsetail", "p_araucaria"], "dig": ["hook_dig", "fossil_dig", "red_rock", "ai_land_09", "ai_land_21"],
            "museu": ["ai_land_14", "ai_land_15", "ai_land_16", "fossil_museum"], "presto": ["presto"], "hyper": ["hyper", "fauna_13", "fauna_14"],
            "cyno": ["fauna_16", "fauna_17", "fauna_18", "exaeretodon"], "ceu": ["ai_land_12", "cruzeiro"], "stauri": ["stauri", "fauna_0"],
            "satur": ["saturnalia", "fauna_22", "fauna_23"], "buri": ["buriolestes", "fauna_24", "fauna_25"], "gnatho": ["gnatho", "fauna_19", "fauna_2"],
            "macro": ["macro", "fauna_27", "fauna_28"], "chuva": ["ai_land_05", "ai_land_06"]}
ep = json.loads(A.finish(chapters, "FE04_Primeiro_Dinossauro_Brasil.mp4", ctx=ctxs, music_gain=-26))
ep = F.cut_rhythm(ep, SCENE_OF)
F.export_hf(ep, os.path.join(HERE, "hf_cards.json"))
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
miss = [m for c in chapters for m in c.misses]
sys.stderr.write(f"trilha: {len(music)} trechos, {total / 60:.1f} min; frases não achadas: {miss}\n")
print(json.dumps(ep, indent=1, ensure_ascii=False))
