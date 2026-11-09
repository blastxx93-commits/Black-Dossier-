#!/usr/bin/env python3
"""ES05 Pegaso Z-102: el coche español que batió récords del mundo. Single-car story, theme "noir_oro" (gold on black, serif headlines).
    python3 build_es05.py <narration_dir> > episode.json   (run from the work folder)
Real photos first; 6 reviewed AI scenes fill the gaps (Jabbeke run, timekeepers, workshop, leopard seats, Mexico race, truck road).
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "engine"))
import aus_kit as A
from aus_kit import P, photo, stat, say, cta, title, ch, questions

PHOTOS = {
    "z102": ["m_z102", "m_z102_touring", "m_z102_engine", "m_z102_spider", "h_concours"],
    "touring": ["m_z102_touring", "m_z102"],
    "saoutchik": ["m_z102_saoutchik"], "cupula": ["m_z102_cupula"], "spider": ["m_z102_spider"],
    "tech": ["m_z102_engine", "h_concours", "h_ricart"],
    "z103": ["m_z103"],
    "hispano": ["m_hispano"], "aero": ["m_hispano_engine", "m_spad"],
    "trucks": ["m_mofletes", "m_barajas", "m_pegaso_truck", "ai:ai_truck_road"],
    "xk120": ["m_xk120"], "alfa": ["m_alfa_1930s"],
    "s1400": ["m_seat1400"], "biscuter": ["m_biscuter"], "s600": ["m_seat600"],
    "ricart": ["h_ricart", "ai:ai_workshop"], "trujillo": ["h_trujillo"],
    "jabbeke": ["ai:ai_jabbeke_run", "ai:ai_timekeepers", "h_jabbeke"],
    "race": ["h_le_mans_1952", "ai:ai_mexico_race", "h_carrera_panamericana"],
    "paris": ["h_paris_salon"], "concours": ["h_concours"], "museum": ["h_museum"],
    "leopard": ["ai:ai_leopard_seats"],
    "spain": ["m_pegaso_truck"], "mexico": ["ai:ai_mexico_race", "h_carrera_panamericana"],
}
CLIPS = json.load(open(os.path.join(HERE, "clips.json")))
GENERIC = CLIPS.pop("_generic", [])
FALLBACK = {k: ["z102"] for k in PHOTOS}
FALLBACK.update({"z102": ["touring", "concours"], "touring": ["z102"], "saoutchik": ["z102"], "cupula": ["saoutchik", "z102"],
                 "tech": ["z102"], "hispano": ["aero", "trucks"], "aero": ["hispano"], "trucks": ["z102"],
                 "alfa": ["ricart", "z102"], "ricart": ["alfa", "z102"], "jabbeke": ["touring", "z102"], "race": ["z102"],
                 "concours": ["z102"], "museum": ["concours", "z102"], "leopard": ["saoutchik"], "trujillo": ["cupula"], "spain": ["trucks"], "mexico": ["race"]})
RES = ["m_z102/7", "m_z102/5", "m_z102_touring/1", "m_z102_saoutchik/2", "m_z102_cupula/2", "m_z102_cupula/5",
       "m_z102_spider/2", "m_z103/3", "m_hispano/1", "m_hispano_engine/1", "m_spad/1", "m_mofletes/1", "m_barajas/1",
       "h_ricart/1", "m_alfa_1930s/1", "h_paris_salon/1", "m_xk120/1", "m_seat1400/3", "m_biscuter/1", "m_seat600/1",
       "h_concours/4", "h_museum/1"]
A.setup(sys.argv[1], os.path.join(HERE, "skip.json"), PHOTOS, CLIPS, GENERIC, FALLBACK, ["z102", "trucks"], reserved=RES)
A.THEME = "noir_oro"
A.CLIP_TARGET = 0.08
A.MAX_HOLD, A.KEEP = 12.0, 8.0
A.ARCHIVE_OK = True
A.SPLIT_BY_SUBJECT = True
chapters = []

c = ch("ch00_hook", 0.6)
c.at(0, photo("m_z102", 7, "in", cap="Pegaso Z-102|1951 – 1958"))
c.at("Un coche plateado acelera", P("jabbeke"))
c.at("Ese coche acaba de batir cuatro récords", stat("4", "récords oficiales · Jabbeke, 1953", "Real Automóvil Club de Bélgica", count=True))
c.at("Y no es italiano", P("touring"))
c.at("Es español", say("Es español.", "ESPAÑOL", 150))
c.at("Lo fabricaba una empresa de camiones", P("trucks"))
c.at("Lo diseñó un ingeniero", P("ricart"))
c.at("Lo compraron un barón millonario", P("saoutchik"))
c.at("Se llamaba Pegaso Z-102", title("Pegaso Z-102", "el coche español que batió récords del mundo", "1951 – 1958", "z102"))
questions(c, ["Quién lo diseñó", "Quién lo conducía", "Por qué desapareció"],
          ["De dónde salió", "quién lo conducía", "y por qué desapareció"])
chapters.append(c)

c = ch("ch01")
c.at(0, P("trucks"))
c.at("Era un país aislado", P("spain"))
c.at("En 1946 nació la Empresa Nacional de Autocamiones", stat("1946", "nace ENASA · Instituto Nacional de Industria", "ENASA", count=False))
c.at("se instaló en la antigua fábrica de Hispano-Suiza", photo("m_hispano", 1, "in", cap="Hispano-Suiza|Barcelona"))
c.at("Hispano-Suiza merece un vídeo propio", P("hispano"))
c.at("El rey Alfonso XIII", P("hispano"))
c.at("fabricó motores de avión V8", photo("m_hispano_engine", 1, "in", cap="Motor Hispano-Suiza V8|aviación"))
c.at("Por eso su emblema lleva una cigüeña", photo("m_spad", 1, "in", cap="SPAD XIII|motor Hispano-Suiza"))
c.at("Con el tiempo, la marca", P("hispano"))
c.at("La marca de los vehículos de ENASA", photo("h_museum", 1, "in", cap="Pegaso|el caballo alado"))
c.at("Y durante décadas, en España, Pegaso", P("trucks"))
c.at("El primer camión de la marca", photo("m_mofletes", 1, "in", cap="Pegaso «Mofletes»|1949"))
c.at("Unos años después llegaría el Barajas", photo("m_barajas", 1, "in", cap="Pegaso «Barajas»"))
c.at("Entre 1946 y 1990", stat("≈405.000", "vehículos Pegaso · Madrid, 1946–1990", "ENASA", count=False))
c.at("Pero dentro de esa empresa de camiones", P("z102"))
chapters.append(c)

c = ch("ch02")
c.at(0, photo("h_ricart", 1, "in", cap="Wifredo Ricart|1897 – 1974"))
c.at("En los años treinta, Ricart se marchó", photo("m_alfa_1930s", 1, "in", cap="Alfa Romeo|años 30 y 40"))
c.at("Allí trabajó en la división", P("alfa"))
c.at("La relación entre los dos no fue buena", say("Según algunas versiones, Ferrari le culpó de su salida.", "FERRARI", 100))
c.at("Las fechas y los detalles", P("alfa"))
c.at("Los ingenieros que trabajaron con Ricart", P("ricart"))
c.at("En 1946, Ricart volvió a España", P("ricart"))
c.at("Y entonces tuvo una idea", P("tech"))
c.at("Así nació el Pegaso Z-102", photo("m_z102", 5, "in", cap="Pegaso Z-102"))
chapters.append(c)

c = ch("ch03")
c.at(0, P("z102"))
c.at("El primer Z-102 que vio el público", photo("h_paris_salon", 1, "in", cap="Salón de París|años 50"))
c.at("Imagina la cara de los periodistas", P("z102"))
c.at("El motor era un V8 de aluminio", P("tech"))
c.at("Las primeras versiones tenían", stat("2,5 · 2,8 · 3,2", "litros · motor V8 de aluminio", "ENASA", count=False))
c.at("La caja de cambios tenía cinco marchas", P("tech"))
c.at("Muchas piezas se fabricaban casi a mano", P("z102"))
c.at("El chasis y la mecánica salían de Barcelona", photo("m_z102_touring", 1, "in", cap="Carrocería Touring|Superleggera"))
c.at("con su técnica Superleggera", P("touring"))
c.at("El carrocero francés Saoutchik", photo("m_z102_saoutchik", 2, "in", cap="Carrocería Saoutchik"))
c.at("Y la propia ENASA carrozó", stat("18 · 19", "carrocerías Saoutchik · carrocerías ENASA", "según la fuente", count=False))
c.at("Y también hubo carrocerías hechas en casa", photo("m_z102_spider", 2, "in", cap="Pegaso Z-102 Spider"))
c.at("Por eso no hay dos Pegaso iguales", P("z102"))
chapters.append(c)

c = ch("ch04")
c.at(0, P("concours"))
c.at("Los Pegaso acabaron en manos", P("z102"))
c.at("Uno de los más famosos fue un Z-102", P("saoutchik"))
c.at("Tenía los asientos tapizados en piel de leopardo", P("leopard"))
c.at("En 1953 ganó el Gran Premio de Elegancia", P("saoutchik"))
c.at("Otro de los más extraños es el llamado Cúpula", photo("m_z102_cupula", 2, "in", cap="Pegaso Z-102 «Cúpula»"))
c.at("Se construyeron dos", P("cupula"))
c.at("Rafael Trujillo", P("cupula"))
c.at("Según algunas fuentes, Touring hizo una carrocería única", P("touring"))
c.at("Hasta los propios materiales eran de lujo", P("saoutchik"))
c.at("Un barón con asientos de leopardo", say("Todo eso salió de una fábrica de camiones.", "CAMIONES", 110))
chapters.append(c)

c = ch("ch05")
c.at(0, P("race"))
c.at("Pegaso intentó correr en las veinticuatro horas de Le Mans", P("race"))
c.at("En México, en la legendaria Carrera Panamericana", P("mexico", photo_only=True))
c.at("Las fuentes no se ponen de acuerdo", P("race"))
c.at("Y entonces llegó Jabbeke", P("jabbeke"))
c.at("En aquella época, la autopista de Jabbeke", P("jabbeke"))
c.at("Y el veinticinco de septiembre de 1953", P("touring"))
c.at("Allí, en 1949, un Jaguar XK120", photo("m_xk120", 1, "in", cap="Jaguar XK120|Jabbeke, 1949"))
c.at("Jabbeke era, por así decirlo", P("xk120"))
c.at("Según se cuenta, hubo un primer intento", P("jabbeke"))
c.at("Batió cuatro récords oficiales", stat("≈244 km/h", "Pegaso Z-102 · Jabbeke, 25/09/1953", "RACB · según la fuente", count=False))
c.at("Con eso, el Pegaso Z-102 se convirtió", say("El coche de producción más rápido del mundo.", "RÁPIDO", 110))
c.at("Piénsalo un momento", photo("m_seat600", 1, "in", cap="SEAT 600|1957"))
c.at("Ese mismo año, 1953", photo("m_seat1400", 3, "in", cap="SEAT 1400|1953"))
c.at("y el Biscúter", photo("m_biscuter", 1, "in", cap="Biscúter|1953"))
c.at("Tres coches españoles del mismo año", P("z102"))
chapters.append(c)

c = ch("ch06", 2.5)
c.at(0, P("z102"))
c.at("La respuesta es sencilla: el dinero", P("tech"))
c.at("Entre 1951 y 1958 se fabricaron", stat("≈84", "Pegaso Z-102 fabricados · 1951–1958", "según la fuente", count=False))
c.at("Las cifras exactas cambian", P("z102"))
c.at("Pegaso intentó también una versión más grande", photo("m_z103", 3, "in", cap="Pegaso Z-103"))
c.at("En 1959, Wifredo Ricart dejó la dirección", P("ricart"))
c.at("Los camiones Pegaso siguieron", P("trucks"))
c.at("Llegaron modelos cada vez más grandes", P("trucks"))
c.at("Hoy, los Pegaso Z-102 que sobreviven", photo("h_concours", 4, "in"))
c.at("Aparecen en los concursos de elegancia", P("concours"))
c.at("Pero en España, si preguntas por la calle", P("trucks"))
c.at("Un coche español que batió récords del mundo", say("Un coche español que batió récords del mundo.", "RÉCORDS", 120))
c.at("Si te ha gustado el vídeo", cta("Suscríbete", "historias de coches clásicos"))
c.at("habías oído hablar alguna vez del Pegaso", cta("¿Conocías el Pegaso Z-102?", "cuéntamelo en los comentarios"))
chapters.append(c)

CTX = ["z102", "trucks", "ricart", "z102", "z102", "race", "z102"]
print(A.finish(chapters, "ES05_PEGASO.mp4", CTX, subtitles="ES05.ass"))
