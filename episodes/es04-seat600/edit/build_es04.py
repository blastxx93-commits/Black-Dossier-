#!/usr/bin/env python3
"""ES04 El SEAT 600: el coche que cambió España. Single-car story, theme "retro60" (warm 60s film, Bebas Neue).
    python3 build_es04.py <narration_dir> > episode.json   (run from the work folder)
Real photos only (no AI scene passed review this time).
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "engine"))
import aus_kit as A
from aus_kit import P, photo, stat, say, cta, title, ch, questions

S600 = ["m_600n", "m_600d", "m_600e", "m_600_2", "m_600_3", "m_600_rear", "m_600_interior", "m_600_doors", "m_600_engine"]
PHOTOS = {
    "s600": S600,
    "n": ["m_600n", "m_600_2"], "d": ["m_600d", "m_600_3"], "e": ["m_600e"],
    "inside": ["m_600_interior", "m_600_doors", "m_600_engine", "m_600_rear"],
    "variants": ["m_seat800", "m_600_furgoneta", "m_600_rally"],
    "fiat": ["m_fiat600", "h_giacosa", "m_fiat500"], "world": ["m_zastava750", "m_fitito", "m_jagst"],
    "s1400": ["m_seat1400"], "micro": ["m_biscuter"], "later": ["m_seat850"],
    "factory": ["h_zona_franca", "h_seat_museum"],
    "era": ["h_marin_cars", "h_spain_1960_photo", "h_traffic_spain", "h_marin_600"],
    "life": ["h_marin_600", "h_marin_family", "h_marin_cars", "h_spain_beach", "h_marin_beach"],
    "beach": ["h_spain_beach", "h_marin_beach"],
    "legacy": ["h_fuengirola", "h_seat600_meeting", "h_montmelo"],
    "money": ["h_peseta"],
}
CLIPS = json.load(open(os.path.join(HERE, "clips.json")))
GENERIC = CLIPS.pop("_generic", [])
FALLBACK = {k: ["s600"] for k in PHOTOS}
FALLBACK.update({"s600": ["life"], "fiat": ["world", "s600"], "world": ["fiat", "s600"], "era": ["life", "s600"],
                 "life": ["era", "s600"], "beach": ["life"], "legacy": ["s600"], "money": ["s600"], "factory": ["s600"]})
RES = ["m_600n/1", "m_600n/2", "m_600d/1", "m_600e/2", "m_seat800/1", "m_fiat600/1", "h_giacosa/3", "m_seat1400/3", "m_biscuter/1",
       "h_fuengirola/1", "m_600_doors/1", "m_zastava750/1", "m_fitito/1", "m_jagst/1", "m_600_rally/1", "h_montmelo/4"]
A.setup(sys.argv[1], os.path.join(HERE, "skip.json"), PHOTOS, CLIPS, GENERIC, FALLBACK, ["s600", "life"], reserved=RES)
A.THEME = "retro60"
A.CLIP_TARGET = 0.10
A.MAX_HOLD, A.KEEP = 12.0, 8.0
A.ARCHIVE_OK = True
A.SPLIT_BY_SUBJECT = True
chapters = []

c = ch("ch00_hook", 0.6)
c.at(0, photo("m_600n", 1, "in", cap="Barcelona|27 de junio de 1957"))
c.at("Nadie en aquella fábrica sabe", P("factory"))
c.at("Ese coche costaba una fortuna", P("money", photo_only=True))
c.at("Y hubo quien esperó hasta dos años", say("Hasta dos años de espera.", "DOS AÑOS", 140))
c.at("Con él, millones de españoles vieron el mar", P("beach"))
c.at("Descubrieron las carreteras", P("life"))
c.at("Hoy vas a conocer la historia del SEAT 600", title("El SEAT 600", "el coche que cambió España", "1957 – 1973", "s600"))
questions(c, ["Colas de dos años", "Un secreto sobre su origen", "La frase de la última pancarta"],
          ["Te contaré por qué", "Te contaré un secreto", "Y al final, te contaré la frase"])
chapters.append(c)

c = ch("ch01")
c.at(0, P("era"))
c.at("Era un país pobre", P("era"))
c.at("Hasta 1952, los españoles", stat("1 / 55", "un vehículo por cada 55 habitantes · 1960", "estudio académico", count=False))
c.at("El nueve de mayo de 1950", P("factory"))
c.at("El reparto del dinero", stat("51% · 42% · 7%", "INI · seis bancos · Fiat", "SEAT, 1950", count=False))
c.at("Y aquí va una curiosidad", stat("600.000.000", "pesetas de capital inicial de SEAT", "SEAT, 1950", count=False))
c.at("SEAT construyó su fábrica", P("factory"))
c.at("Y el trece de noviembre de 1953", photo("m_seat1400", 3, "in", cap="SEAT 1400|1953"))
c.at("Pero para un trabajador normal", P("s1400"))
c.at("Mientras tanto, la gente que quería moverse", photo("m_biscuter", 1, "in", cap="Biscúter|1953"))
c.at("España necesitaba otra cosa", P("era"))
c.at("Y ese coche ya existía", photo("m_fiat600", 1, "in", cap="Fiat 600|Turín, 1955"))
chapters.append(c)

c = ch("ch02")
c.at(0, P("fiat"))
c.at("Se presentó en el Salón de Ginebra", photo("h_giacosa", 3, "in"))
c.at("Ese es el secreto", say("El coche que motorizó España nació en Turín.", "TURÍN", 110))
c.at("Y no fue solo España", photo("m_zastava750", 1, "in", cap="Zastava 750|«Fića» · Yugoslavia"))
c.at("En Argentina, el Fiat 600", photo("m_fitito", 1, "in", cap="Fiat 600|«Fitito» · Argentina"))
c.at("En Alemania incluso", photo("m_jagst", 1, "in", cap="NSU-Fiat Jagst"))
c.at("Pero que nadie se engañe", P("s600"))
c.at("Veintisiete de junio de 1957", photo("m_600n", 2, "in", cap="SEAT 600|70.000 pesetas"))
c.at("El primer Seiscientos que se matriculó", say("Matrícula B-141141", "B-141141", 130))
c.at("Para hacerse una idea", P("money", photo_only=True))
c.at("Poco después de salir a la venta", stat("30.000", "personas en lista de espera", "Tinsa / Mapfre", count=False))
c.at("En 1960, había llegado a los dos años", P("n"))
c.at("Y el coche, ¿qué ofrecía?", P("inside"))
c.at("Y aquellas famosas puertas suicidas", photo("m_600_doors", 1, "in", cap="Puertas «suicidas»"))
c.at("Para los fabricantes de microcoches", P("micro"))
c.at("No era rápido", P("s600"))
chapters.append(c)

c = ch("ch03")
c.at(0, P("life"))
c.at("Por primera vez, una familia", P("life"))
c.at("Los veranos de los años sesenta", P("beach"))
c.at("Una historiadora lo resumía así", P("beach"))
c.at("El Seiscientos llegó en plena transformación", P("era"))
c.at("Fue el coche más vendido de España", stat("1958–1966", "coche más vendido de España (y en 1968)", "SEAT", count=False))
c.at("Algunas estimaciones van todavía más lejos", stat("1 / 9", "un vehículo por cada 9 habitantes · 1974", "estudio académico", count=False))
c.at("Con él llegaron también cosas nuevas", P("era"))
c.at("Un museo de automoción de Salamanca", P("life"))
c.at("Y como era sencillo", P("inside"))
c.at("Tenía también sus manías", P("s600"))
chapters.append(c)

c = ch("ch04")
c.at(0, P("n"))
c.at("En 1963 llegó el 600 D", photo("m_600d", 1, "in", cap="SEAT 600 D|1963 · 767 cc"))
c.at("Hubo incluso una versión de cuatro puertas", photo("m_seat800", 1, "in", cap="SEAT 800|cuatro puertas"))
c.at("El SEAT 800 se lanzó en 1964", P("variants"))
c.at("A finales de los sesenta llegó el 600 E", photo("m_600e", 2, "in", cap="SEAT 600 E|puertas normales"))
c.at("La última evolución fue el 600 L Especial", P("e"))
c.at("En total, según la fuente", photo("m_600_rally", 1, "in"))
c.at("Pero los años setenta traían otra España", P("later"))
chapters.append(c)

c = ch("ch05")
c.at(0, P("factory"))
c.at("Por la cadena de montaje avanza", P("e"))
c.at("Hacía ya meses que SEAT", P("factory"))
c.at("Los trabajadores lo saben", P("s600"))
c.at("Naciste príncipe y mueres rey", say("«Naciste príncipe y mueres rey»", "REY", 110))
c.at("Y hay un detalle casi poético", P("s600"))
c.at("¿Cuántos se fabricaron?", stat("≈800.000", "SEAT 600 fabricados · 1957–1973", "SEAT", count=False))
chapters.append(c)

c = ch("ch06", 2.5)
c.at(0, P("legacy"))
c.at("Durante décadas, los Seiscientos siguieron", P("s600"))
c.at("Hoy, el Seiscientos tiene incluso monumentos", photo("h_fuengirola", 1, "in", cap="Fuengirola|2008"))
c.at("La de Fuengirola se inauguró en 2008", P("legacy"))
c.at("Y en 2017, para celebrar", photo("h_montmelo", 4, "in", cap="Montmeló|9 de septiembre de 2017"))
c.at("Setecientos ochenta y siete Seiscientos", stat("787", "SEAT 600 juntos · Récord Guinness", "Guinness World Records", count=True))
c.at("Al circuito acudieron", P("legacy"))
c.at("Setecientos ochenta y siete coches con más de cuarenta años", P("legacy"))
c.at("Para la mayoría de sus dueños", P("s600"))
c.at("Esa es la verdadera historia del Seiscientos", P("life"))
c.at("Nació príncipe. Y murió rey.", say("Nació príncipe. Y murió rey.", "REY", 140))
c.at("Si te ha gustado el vídeo", cta("Suscríbete", "historias de coches clásicos"))
c.at("¿tu familia tuvo un Seiscientos?", cta("¿Tu familia tuvo un Seiscientos?", "cuéntamelo en los comentarios"))
chapters.append(c)

CTX = ["s600", "era", "s600", "life", "s600", "s600", "legacy"]
print(A.finish(chapters, "ES04_SEAT600.mp4", CTX, subtitles="ES04.ass"))
