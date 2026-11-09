#!/usr/bin/env python3
"""ES06 Los 10 coches de los dictadores. Countdown list, theme "periodico" (old newspaper: near-monochrome, black/white/red).
    python3 build_es06.py <narration_dir> > episode.json   (run from the work folder)
Tragedies (Trujillo 1961, Carrero 1973): only intact cars / portraits, never the attack, wreck or victims (channel rule).
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "engine"))
import aus_kit as A
from aus_kit import P, photo, rank, stat, say, cta, title, ch, questions

def ai(*names):
    """AI scenes that exist in the reviewed set only (re-generated ones may be missing)."""
    rev = json.load(open(os.path.join(HERE, "reviewed.json")))
    return ["ai:" + n for n in names if f"ai/{n}_1.jpg" in rev]

PHOTOS = {
    "zis": ["m_zis110", "h_kremlin"] + ai("ai_motorcade"), "stalin": ["h_stalin", "h_kremlin"],
    "hongqi": ai("ai_hongqi_factory") + ["m_hongqi"], "mao": ["h_mao", "m_hongqi"],
    "tito": ["m_tito_cadillac", "m_eldorado53"] + ai("ai_brioni_drive"), "titop": ["h_tito"],
    "shah": ["m_maserati5000"] + ai("ai_modena_workshop"), "shahp": ["h_shah"],
    "zil": ["m_zil111"] + ai("ai_havana_zil"), "cuba": ["h_castro", "h_havana_cars"], "havana": ["h_havana_cars"],
    "mb600": ["m_mb600"], "amin": ["h_idi_amin_car", "m_mb600"],
    "fleet": ["m_fleetwood70"] + ai("ai_franco_motorcade"), "salamanca": ["h_salamanca_museum"], "franco": ["h_franco", "h_el_pardo"],
    "cupula": ["m_pegaso_cupula"], "trujillo": ["h_trujillo", "h_santo_domingo"], "belair": ["m_belair57"],
    "dodge": ["m_dodge3700", "h_villaverde"], "carrero": ["h_carrero"],
    "rolls": ["m_phantom4"] + ai("ai_rolls_parade"), "guard": ["h_guardia_real"] + ai("ai_guard_garage"), "pardo": ["h_el_pardo"],
    "madrid": ["h_madrid_1950s", "h_el_pardo"], "parade": ["h_kremlin"],
    "limo": ["m_mb600", "m_zil111", "m_fleetwood70", "m_zis110"],
}
CLIPS = json.load(open(os.path.join(HERE, "clips.json")))
GENERIC = CLIPS.pop("_generic", [])
FALLBACK = {k: ["limo"] for k in PHOTOS}
FALLBACK.update({"limo": ["rolls", "mb600"], "stalin": ["zis"], "mao": ["hongqi"], "titop": ["tito"], "shahp": ["shah"],
                 "cuba": ["zil", "havana"], "havana": ["zil"], "amin": ["mb600"], "salamanca": ["fleet"], "franco": ["fleet", "rolls"],
                 "trujillo": ["cupula", "belair"], "belair": ["cupula"], "carrero": ["dodge"], "guard": ["rolls"], "pardo": ["guard", "rolls"],
                 "madrid": ["rolls"], "parade": ["limo"],
                 "fleet": ["franco", "salamanca", "mb600"], "cupula": ["trujillo", "belair"], "dodge": ["carrero", "madrid", "franco"],
                 "rolls": ["guard", "pardo", "madrid", "franco"], "zil": ["cuba", "havana"], "mb600": ["amin", "limo"],
                 "tito": ["titop"], "shah": ["shahp"], "hongqi": ["mao"], "zis": ["stalin", "parade"]})
RES = ["m_phantom4/4", "h_guardia_real/5", "h_guardia_real/3", "m_zis110/2", "m_hongqi/6", "m_tito_cadillac/1", "m_maserati5000/2",
       "m_zil111/3", "m_mb600/4", "m_fleetwood70/2", "m_pegaso_cupula/2", "m_dodge3700/1", "m_belair57/5", "h_salamanca_museum/2",
       "h_franco/2", "h_carrero/1", "h_trujillo/3", "h_tito/2", "h_shah/4", "h_castro/1", "h_mao/3", "h_stalin/3"]
A.setup(sys.argv[1], os.path.join(HERE, "skip.json"), PHOTOS, CLIPS, GENERIC, FALLBACK, ["limo", "rolls"], reserved=RES)
A.THEME = "periodico"
A.CLIP_TARGET = 0.08
A.MAX_HOLD, A.KEEP = 13.0, 9.0
A.ARCHIVE_OK = True
A.SPLIT_BY_SUBJECT = True
chapters = []

c = ch("ch00_hook", 0.6)
c.at(0, photo("h_guardia_real", 5, "in", cap="Madrid|19 de junio de 2014"))
c.at("Casi nadie se fija en el coche", P("guard"))
c.at("Pero ese coche tiene más de sesenta años", photo("m_phantom4", 4, "in", cap="Rolls-Royce Phantom IV|1952"))
c.at("Y su primer dueño no fue un rey", say("Su primer dueño fue un dictador.", "DICTADOR", 130))
c.at("Los hombres que mandaban sin elecciones", P("parade"))
c.at("Coches enormes, blindados", P("limo"))
c.at("Algunos de esos coches salieron de fábricas americanas", P("limo"))
c.at("Y dos de ellos se fabricaron en España", P("cupula"))
c.at("Y detrás de cada uno de esos coches", P("limo"))
c.at("Hoy vas a conocer los diez coches", title("Los coches de los dictadores", "lujo, blindaje y miedo", "1950 – 1979", "limo"))
questions(c, ["Un platillo volante español", "Un regalo del Kremlin", "El coche que hoy lleva al rey"],
          ["Del más curioso", "al más sorprendente", "Y el número uno"])
chapters.append(c)

c = ch("ch01")
c.at(0, rank(10, "ZIS-110", "m_zis110", 2, "Unión Soviética", "el coche de Stalin"))
c.at("Moscú, finales de los años cuarenta", P("stalin"))
c.at("La solución fue copiar", P("zis"))
c.at("Se fabricó hasta 1958", P("zis"))
c.at("Stalin tenía miedo de casi todo", photo("h_stalin", 3, "in", cap="Stalin|Yalta, 1945"))
c.at("Salía del Kremlin en una caravana", P("zis"))
c.at("Esa idea, la caravana de coches negros", P("parade"))
c.at("Número nueve", rank(9, "Hongqi CA72", "m_hongqi", 6, "China", "la «Bandera Roja» de Mao"))
c.at("China, 1958", photo("h_mao", 3, "in", cap="Mao Zedong"))
c.at("En la fábrica FAW de Changchun", P("hongqi"))
c.at("Lo llamaron Hongqi", say("Hongqi: «bandera roja».", "BANDERA ROJA", 120))
c.at("Lo curioso es que no está nada claro", P("mao"))
c.at("Lo que sí es seguro es que se fabricaron muy pocos", P("hongqi"))
chapters.append(c)

c = ch("ch02")
c.at(0, rank(8, "Cadillac Eldorado", "m_tito_cadillac", 1, "Yugoslavia", "el coche de Tito"))
c.at("Su líder, el mariscal Josip Broz Tito", photo("h_tito", 2, "in", cap="Josip Broz Tito"))
c.at("En 1953, un grupo de emigrantes croatas", P("tito"))
c.at("Tito se lo llevó a su refugio favorito", P("tito"))
c.at("Hoy el coche sigue allí", P("tito"))
c.at("Número siete", rank(7, "Maserati 5000 GT", "m_maserati5000", 2, "Irán", "el capricho del sha"))
c.at("Irán, finales de los cincuenta", photo("h_shah", 4, "in", cap="Mohammad Reza Pahlavi|sha de Irán"))
c.at("A finales de los cincuenta, según la historia de la marca", P("shah"))
c.at("El resultado fue el Maserati 5000 GT", P("shah"))
c.at("El sha llegó a reunir", P("shahp"))
c.at("En 1979, la revolución", P("shah"))
chapters.append(c)

c = ch("ch03")
c.at(0, rank(6, "ZIL-111", "m_zil111", 3, "Cuba", "el regalo del Kremlin a Fidel Castro"))
c.at("Cuba, principios de los años sesenta", P("cuba"))
c.at("Nikita Jrushchov, el líder soviético", P("zil"))
c.at("En aquellos años, la limusina soviética", P("havana"))
c.at("Imagínate la escena", P("zil"))
c.at("Pero la historia tiene un final inesperado", P("havana"))
c.at("Número cinco", rank(5, "Mercedes-Benz 600", "m_mb600", 4, "1963 – 1981", "el coche de los dictadores"))
c.at("Salón de Frankfurt, 1963", P("mb600"))
c.at("Para hacerse una idea de su categoría", P("mb600"))
c.at("Mercedes lo vendía a reyes", P("mb600"))
c.at("El ugandés Idi Amin", P("amin"))
c.at("Y luego está Kim Il-sung", say("Al menos diez Mercedes 600, comprados en secreto.", "EN SECRETO", 110))
c.at("El Mercedes 600 se fabricó hasta 1981", stat("< 3.000", "Mercedes-Benz 600 fabricados · 1963–1981", "Mercedes-Benz", count=False))
c.at("Hoy es uno de los clásicos más buscados", P("mb600"))
chapters.append(c)

c = ch("ch04")
c.at(0, P("limo"))
c.at("Y ahora llegamos a los cuatro primeros", say("Y aquí, España tiene mucho que decir.", "ESPAÑA", 120))
c.at("Número cuatro", rank(4, "Cadillac Fleetwood 75", "m_fleetwood70", 2, "España", "los Cadillac de Franco"))
c.at("En la España de los años cincuenta", photo("h_franco", 2, "in", cap="Francisco Franco"))
c.at("Uno de los que mejor se conservan", P("fleet"))
c.at("Hoy se puede ver en el Museo de la Automoción de Salamanca", photo("h_salamanca_museum", 2, "in", cap="Museo de la Automoción|Salamanca"))
c.at("Porque Franco, como Stalin", P("fleet"))
c.at("Número tres", rank(3, "Pegaso Z-102 Cúpula", "m_pegaso_cupula", 2, "Hecho en España", "el coche del dictador Trujillo"))
c.at("República Dominicana, años cincuenta", photo("h_trujillo", 3, "in", cap="Rafael Leónidas Trujillo"))
c.at("Entre sus coches había una joya", P("cupula"))
c.at("Y esa muerte también tiene un coche", photo("m_belair57", 5, "in", cap="Chevrolet Bel Air|1957"))
c.at("Según la prensa dominicana", stat("≈60", "impactos de bala · 30 de mayo de 1961", "prensa dominicana", count=False))
c.at("Un dictador que paseaba en un platillo volante", P("cupula"))
chapters.append(c)

c = ch("ch05")
c.at(0, rank(2, "Dodge 3700 GT", "m_dodge3700", 1, "Hecho en España", "el coche de Carrero Blanco"))
c.at("En junio de 1973", photo("h_carrero", 1, "in", cap="Luis Carrero Blanco"))
c.at("Carrero se movía por Madrid", P("dodge"))
c.at("Salía de la fábrica de Villaverde", P("dodge"))
c.at("El veinte de diciembre de 1973", say("20 de diciembre de 1973", "1973", 130))
c.at("Fue uno de los atentados más conocidos", P("dodge"))
c.at("El coche se conservó", P("dodge"))
chapters.append(c)

c = ch("ch06", 2.5)
c.at(0, rank(1, "Rolls-Royce Phantom IV", "m_phantom4", 7, "Reino Unido · 1950", "solo 18 en el mundo"))
c.at("Inglaterra, 1950", P("rolls"))
c.at("Entre 1950 y 1956 se fabricaron solo dieciocho", stat("18", "Rolls-Royce Phantom IV fabricados · 1950–1956", "Rolls-Royce", count=True))
c.at("Porque tres de esos dieciocho", stat("3 de 18", "Phantom IV para Francisco Franco · 1952", "Patrimonio Nacional", count=False))
c.at("Franco los usó durante más de veinte años", P("rolls"))
c.at("Y cuando murió, en 1975", P("rolls"))
c.at("Hoy esos coches se guardan", photo("h_guardia_real", 3, "in", cap="Guardia Real|El Pardo"))
c.at("Y siguen saliendo a la calle", P("guard"))
c.at("Piénsalo un momento", say("Del dictador… al rey.", "REY", 140))
c.at("Así de extraña es la historia", P("limo"))
c.at("Y ahora te pregunto a ti", P("rolls"))
c.at("Si te ha gustado el vídeo", cta("Suscríbete", "historias de coches clásicos"))
chapters.append(c)

CTX = ["limo", "zis", "tito", "zil", "fleet", "dodge", "rolls"]
print(A.finish(chapters, "ES06_DICTADORES.mp4", CTX, subtitles="ES06.ass"))
