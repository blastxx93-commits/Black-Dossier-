#!/usr/bin/env python3
"""ES02 Los 10 coches patrulla más rápidos de los años 50 y 60: full edit, shots anchored to phrases.
    python3 build_es02.py <narration_dir> > episode.json   (run from the work folder)
Editing style from the Aussie channel (aus_kit). Real photos/clips first; AI only where nothing real exists.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "engine"))
import aus_kit as A
from aus_kit import P, photo, stat, say, cta, title, ch, questions, rank

PHOTOS = {
    "p356": ["m_356_police", "m_356", "ai:ai_dutch_356"],
    "buick": ["m_buick55", "m_buick_police", "h_chp"],
    "giulia": ["m_giulia"],
    "sp250": ["m_sp250", "m_sp250_police"],
    "cafe": ["h_cafe_racer", "ai:ai_cafe_racers", "h_london_60s"],
    "stype": ["m_stype_police", "m_stype"],
    "mk2": ["m_mk2", "m_mk2_police", "ai:ai_getaway"],
    "spain": ["m_seat1400", "m_r10"],
    "polara65": ["m_polara65", "m_polara_chp"],
    "p911": ["m_911_police", "m_911targa"],
    "ferrari": ["m_ferrari_police", "m_ferrari_gte", "h_maranello"],
    "rome": ["h_rome_60s", "h_spanish_steps"],
    "polara69": ["m_polara69", "m_polara_chp", "ai:ai_proving_ground"],
    "usa": ["m_buick55", "m_polara65", "ai:ai_police_radio", "ai:ai_gc_motos"],
    "europe": ["h_autobahn", "h_london_60s", "h_rome_60s"],
    "tv": ["ai:ai_tv_1950s"],
    "radio": ["ai:ai_police_radio"],
}
CLIPS = json.load(open(os.path.join(HERE, "clips.json")))
GENERIC = CLIPS.pop("_generic", [])
FALLBACK = {"p356": ["p911", "europe"], "buick": ["usa"], "giulia": ["rome", "europe"], "sp250": ["cafe", "europe"],
            "cafe": ["sp250"], "stype": ["mk2"], "mk2": ["stype"], "spain": ["europe"], "polara65": ["usa", "polara69"],
            "p911": ["p356"], "ferrari": ["rome"], "rome": ["ferrari"], "polara69": ["polara65", "usa"], "usa": ["polara65"],
            "europe": ["p356"], "tv": ["buick"], "radio": ["usa"]}
RES = ["m_ferrari_police/1", "m_ferrari_police/3", "m_ferrari_police/2", "m_356_police/2", "m_356_police/4", "m_buick_police/1", "m_buick55/5",
       "m_giulia/3", "m_sp250_police/1", "m_sp250/1", "m_stype_police/4", "m_mk2/3", "m_seat1400/1", "m_r10/1",
       "m_polara65/1", "m_polara_chp/1", "m_911_police/5", "m_911targa/2", "m_ferrari_gte/6", "m_polara69/2", "h_spanish_steps/1",
       "h_maranello/4"]
A.setup(sys.argv[1], os.path.join(HERE, "skip.json"), PHOTOS, CLIPS, GENERIC, FALLBACK,
        ["europe", "usa", "p356", "mk2", "polara69"], reserved=RES)
A.CLIP_TARGET = 0.25
A.MAX_HOLD, A.KEEP = 12.0, 8.0
A.ARCHIVE_OK = True
chapters = []

# ---------------------------------------------------------------- hook: opens on the real Rome police Ferrari
c = ch("ch00_hook", 0.6)
c.at(0, photo("m_ferrari_police", 1, "in", cap="Roma|años 60"))
c.at("En las puertas lleva dos palabras", P("rome"))
c.at("Es un Ferrari", photo("m_ferrari_police", 3, "left", cap="Ferrari 250 GTE|Squadra Mobile"))
c.at("Durante años, ese Ferrari persiguió", P("rome"))
c.at("Pero ese Ferrari no es", say("No es el más rápido.", "MÁS RÁPIDO", 150))
c.at("En los años cincuenta y sesenta, los coches", P("europe"))
c.at("comprar coches de carreras", P("p911"))
c.at("Hoy vas a conocer", title("Los 10 coches patrulla más rápidos", "de los años 50 y 60", "1950 – 1969", "polara69"))
questions(c, ["Un regalo de Enzo Ferrari", "Cazar motoristas en Londres", "La estrella de la tele"],
          ["Uno lo regaló", "Otro se compró para cazar", "Otro salía en una serie"])
c.at("Y el número uno no es un deportivo europeo", P("polara69"))
chapters.append(c)

# ---------------------------------------------------------------- context · 10 Porsche 356 · 9 Buick Century
c = ch("ch01")
c.at(0, P("europe"))
c.at("Se construyeron autopistas nuevas", P("europe"))
c.at("Y los coches de la policía", P("usa"))
c.at("El problema era evidente", P("radio", photo_only=True))
c.at("Así empezó una carrera muy curiosa", P("europe"))
c.at("Una cosa más antes de empezar", P("p356"))
c.at("Y no era solo un problema de motores", P("usa"))
c.at("Número diez", rank(10, "Porsche 356", "m_356_police", 2, "≈160 km/h", "Rijkspolitie · Holanda y Alemania"))
c.at("A principios de los sesenta, los Países Bajos", P("europe"))
c.at("En noviembre de 1960", stat("17.600", "florines · el primer Porsche de la policía (1960)", "Rijkspolitie", count=False))
c.at("Ese mismo mes, Porsche entregó", P("p356"))
c.at("En 1962, los holandeses crearon", photo("m_356_police", 4, "in", cap="Rijkspolitie|años 60"))
c.at("Imagina la escena", P("p356"))
c.at("Fue el principio de una relación", stat("+500", "Porsche con los colores de la policía holandesa", "Porsche", count=False))
c.at("Número nueve", rank(9, "Buick Century", "m_buick55", 5, "≈172 km/h", "California Highway Patrol · 1955"))
c.at("California, 1955", P("buick"))
c.at("La patrulla encargó unos doscientos setenta", photo("m_buick_police", 1, "in", cap="Buick Century|patrulla de carreteras"))
c.at("La mitad llevaba cambio manual", P("buick"))
c.at("Pero el Century se hizo famoso", P("tv", photo_only=True))
c.at("Y no era un coche de atrezo", P("buick"))
c.at("La serie se emitió entre 1955 y 1959", say("«Diez-cuatro»: mensaje recibido.", "DIEZ-CUATRO", 120))
c.at("Millones de espectadores", P("buick"))
chapters.append(c)

# ---------------------------------------------------------------- 8 Giulia · 7 SP250
c = ch("ch02")
c.at(0, P("rome"))
c.at("Número ocho", rank(8, "Alfa Romeo Giulia Super", "m_giulia", 3, "≈177 km/h", "Polizia · Carabinieri"))
c.at("Alfa Romeo presentó el Giulia en 1962", P("giulia"))
c.at("En la Italia de los años sesenta, el Giulia", P("giulia"))
c.at("El Giulia Super rondaba", P("giulia"))
c.at("Y además se convirtió en una estrella de cine", P("rome"))
c.at("Las Volanti italianas", P("giulia"))
c.at("Número siete", rank(7, "Daimler SP250", "m_sp250", 1, "+190 km/h", "Policía Metropolitana de Londres"))
c.at("Principios de los años sesenta. Londres", P("cafe"))
c.at("Jóvenes en motos rápidas", P("cafe"))
c.at("La solución fue un deportivo", P("sp250"))
c.at("Cuando Daimler lo presentó en Nueva York", say("Se llamaba Dart… hasta que Dodge protestó.", "DART", 110))
c.at("Según la historia del modelo", stat("26", "Daimler SP250 para la Policía Metropolitana (1961–1964)", "historia del modelo", count=False))
c.at("Eran negros, sin rotular", photo("m_sp250_police", 1, "in", cap="SP250|negro, sin rotular"))
c.at("Hasta que sonaba la campana", P("sp250"))
c.at("El SP250 funcionó tan bien", P("sp250"))
chapters.append(c)

# ---------------------------------------------------------------- 6 S-Type · 5 Mk2
c = ch("ch03")
c.at(0, P("europe"))
c.at("Número seis", rank(6, "Jaguar S-Type", "m_stype_police", 4, "≈195 km/h", "Londres · 1967"))
c.at("El S-Type había aparecido en 1963", P("stype"))
c.at("En 1967, la Policía Metropolitana", stat("83", "Jaguar S-Type · los primeros patrullas blancos de Londres", "Policía Metropolitana", count=False))
c.at("Eran rápidos y elegantes", P("stype"))
c.at("Número cinco", rank(5, "Jaguar Mark 2", "m_mk2", 3, "≈200 km/h", "3.8 litros · 220 CV"))
c.at("El Mark 2 fue uno de los grandes símbolos", P("mk2"))
c.at("Su diseño, con la parte trasera estrecha", P("mk2"))
c.at("Varias policías británicas lo usaron", P("mk2"))
c.at("también era uno de los coches favoritos de los atracadores", P("mk2"))
c.at("Hoy, el Mark 2 es uno de los Jaguar", P("mk2"))
c.at("en España la historia era muy distinta", P("spain"))
chapters.append(c)

# ---------------------------------------------------------------- Spain segment (not ranked)
c = ch("ch04")
c.at(0, title("Mientras tanto, en España", "Guardia Civil de Tráfico", "1959", "spain"))
c.at("En 1959, una ley de circulación", stat("3.500", "hombres en la nueva Agrupación de Tráfico (1959)", "BOE", count=False))
c.at("Al principio, la Guardia Civil de Tráfico", P("spain"))
c.at("Aquí las fuentes no se ponen de acuerdo", photo("m_seat1400", 1, "in", cap="SEAT 1400|1953"))
c.at("Aquel SEAT 1400 había salido", P("spain"))
c.at("Otras fuentes, entre ellas", photo("m_r10", 1, "in", cap="Renault 10|FASA · Valladolid"))
c.at("Ninguno de los dos se acercaba", P("spain"))
c.at("Lo importante era estar ahí", P("spain"))
c.at("Y ahora, vamos con los cuatro", P("polara65"))
chapters.append(c)

# ---------------------------------------------------------------- 4 Polara 413 · 3 911 Targa
c = ch("ch05")
c.at(0, rank(4, "Dodge Polara 413", "m_polara65", 1, "≈208 km/h", "California · 1965"))
c.at("Volvemos a California", P("usa"))
c.at("Aquellas pruebas no eran un trámite", P("polara65"))
c.at("En 1965, el Dodge Polara", photo("m_polara_chp", 1, "in", cap="Dodge|patrulla de California"))
c.at("Era una berlina normal por fuera", P("polara65"))
c.at("Número tres", rank(3, "Porsche 911 Targa", "m_911targa", 2, "+210 km/h", "Rijkspolitie · desde 1967"))
c.at("Hemos visto que la Rijkspolitie", P("p911"))
c.at("Según la versión del motor", P("p911"))
c.at("¿Y por qué un Targa", photo("m_911_police", 5, "in"))
c.at("La relación entre Porsche", P("p911"))
chapters.append(c)

# ---------------------------------------------------------------- 2 Ferrari 250 GTE
c = ch("ch06")
c.at(0, rank(2, "Ferrari 250 GTE", "m_ferrari_police", 2, "≈230 km/h", "Squadra Mobile · Roma"))
c.at("A principios de los años sesenta, Roma", P("rome"))
c.at("Y entonces Enzo Ferrari decidió regalarle", P("ferrari"))
c.at("El 250 GTE era un gran turismo", photo("m_ferrari_gte", 6, "in"))
c.at("Los coches eran negros", P("ferrari"))
c.at("se entrenaron en Maranello", photo("h_maranello", 4, "in", cap="Maranello"))
c.at("Uno de ellos se hizo leyenda", say("Armando Spatafora", "SPATAFORA", 140))
c.at("Con Spatafora al volante", P("rome"))
c.at("Y de esos años nació una leyenda", photo("h_spanish_steps", 1, "in", cap="Plaza de España|Roma"))
c.at("Pero la historia inspiró una película", P("rome"))
c.at("El otro Ferrari de la policía", P("ferrari"))
c.at("Y aun así, no es el número uno", P("polara69"))
chapters.append(c)

# ---------------------------------------------------------------- 1 Polara 440 + end CTA
c = ch("ch07", 2.5)
c.at(0, rank(1, "Dodge Polara Pursuit", "m_polara69", 2, "≈241 km/h", "California · 1969"))
c.at("La Patrulla de Carreteras compra", stat("1.564", "Dodge Polara para la patrulla de California (1969)", "CHP", count=False))
c.at("Pero bajo el capó llevaba", P("polara69"))
c.at("En la pista de pruebas de Chrysler", stat("241 km/h", "149,6 mph · pista de Chrysler, Chelsea (Michigan)", "CHP / Chrysler", count=False))
c.at("Más rápido que el Ferrari de Roma", P("polara69"))
c.at("Para que te hagas una idea", P("polara69"))
c.at("Y ese récord no fue una anécdota", say("Récord durante décadas.", "DÉCADAS", 140))
c.at("Un coche de aspecto familiar", P("polara69"))
c.at("Así que ya lo sabes", P("p356"))
c.at("Unos lo hicieron con Porsche", P("mk2"))
c.at("Y los americanos lo hicieron a su manera", P("usa"))
c.at("Si te ha gustado el vídeo", cta("Suscríbete", "historias de coches clásicos"))
c.at("¿de cuál habrías intentado escapar?", cta("¿De cuál habrías intentado escapar?", "cuéntamelo en los comentarios"))
chapters.append(c)

CTX = ["europe", "europe", "rome", "europe", "spain", "polara65", "ferrari", "polara69"]
print(A.finish(chapters, "ES02_Patrullas_Rapidas.mp4", CTX, subtitles="ES02.ass"))
