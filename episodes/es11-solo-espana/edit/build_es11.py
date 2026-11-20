#!/usr/bin/env python3
"""ES11 Los coches que solo existieron en España. Countdown; rendered with the Race template (engine/hf_race.py).
    python3 build_es11.py <narration_dir> > episode.json   (run from the work folder)
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "engine"))
import aus_kit as A
from aus_kit import P, photo, rank, stat, say, cta, title, ch, questions

PHOTOS = {
    "s800": ["m_seat800"], "s600": ["m_seat600"], "mini": ["m_mini1275c"], "authi": ["h_authi"], "dodge": ["m_dodge3700"],
    "dint": ["h_spain70"], "vic": ["m_victoria"], "ado": ["m_adoaust"], "s133": ["m_seat133"], "boca": ["m_bocanegra"],
    "pegaso": ["m_pegaso"], "r7": ["m_r7"], "r5": ["m_r5"], "fasa": ["h_fasa"], "conc": ["h_concentracion"],
    "mix": ["m_seat800", "m_bocanegra", "m_r7", "m_dodge3700", "m_victoria", "m_seat133"],
}
CLIPS = json.load(open(os.path.join(HERE, "clips.json")))
GENERIC = CLIPS.pop("_generic", [])
FALLBACK = {k: ["mix"] for k in PHOTOS}
FALLBACK.update({"mix": ["s600", "r5"], "s800": ["s600"], "s600": ["s800"], "mini": ["authi"], "authi": ["mini", "vic"],
                 "dodge": ["dint"], "dint": ["dodge"], "vic": ["ado"], "ado": ["vic"], "s133": ["s600"], "boca": ["mix"],
                 "r7": ["r5", "fasa", "mix"], "r5": ["r7", "mix"], "fasa": ["r7", "r5", "mix"], "conc": ["s600"], "pegaso": ["mix"]})
RES = ["m_seat800/4", "m_mini1275c/3", "m_dodge3700/2", "m_victoria/1", "m_seat133/4", "m_bocanegra/12", "m_bocanegra/9",
       "m_r7/1", "m_pegaso/3", "m_seat800/7"]
A.setup(sys.argv[1], os.path.join(HERE, "skip.json"), PHOTOS, CLIPS, GENERIC, FALLBACK, ["mix", "s600"], reserved=RES)
A.THEME = "race"
A.CLIP_TARGET = 0.0
A.MAX_HOLD, A.KEEP = 8.0, 5.5
A.ARCHIVE_OK = True
A.SPLIT_BY_SUBJECT = True
chapters = []

c = ch("ch00_hook", 0.6)
c.at(0, photo("m_bocanegra", 9, "in", cap="SEAT 1200 Sport|España, 1976"))
c.at("Ves Volkswagen", P("mix"))
c.at("Coches que solo se fabricaban aquí", say("Solo existieron en España.", "ESPAÑA", 130))
c.at("Uno era un Seiscientos", P("s800"))
c.at("Otro, un coche inglés", P("vic"))
c.at("Otro, un deportivo", P("boca"))
c.at("Y el número uno", P("r7"))
c.at("Hoy vas a conocer", title("Solo existieron en España", "7 coches que el mundo no conoció", "1964 – 1983", "mix"))
c.at("Porque alguno escapó", P("s133"))
chapters.append(c)

c = ch("ch01")
c.at(0, P("s600"))
c.at("Y eso tuvo una consecuencia curiosa", P("mix"))
c.at("Número siete", rank(7, "SEAT 800", "m_seat800", 4, "Barcelona · 1964 – 1967", "el Seiscientos de cuatro puertas"))
c.at("La solución la encontró", P("s800"))
c.at("Se fabricó entre 1964", stat("≈18.000", "unidades del SEAT 800", "según las fuentes", count=False))
c.at("Hoy el SEAT 800", photo("m_seat800", 7, "in", cap="SEAT 800|cuatro puertas"))
c.at("Número seis", rank(6, "Mini 1275 C", "m_mini1275c", 3, "Pamplona · 1968 – 1970", "el «Cooper» español"))
c.at("En Inglaterra", P("mini"))
c.at("Se fabricó entre 1968", P("mini"))
chapters.append(c)

c = ch("ch02")
c.at(0, rank(5, "Dodge 3700 GT", "m_dodge3700", 2, "Madrid · 1971 – 1977", "el coche oficial"))
c.at("En 1971, la fábrica", P("dodge"))
c.at("Se fabricó hasta 1977", P("dodge"))
c.at("Pero más allá", P("dint"))
c.at("Número cuatro", rank(4, "Austin Victoria", "m_victoria", 1, "Pamplona · 1972 – 1975", "el inglés con otra cara"))
c.at("Así que Authi encargó", P("ado"))
c.at("Lo llamaron Austin Victoria", P("vic"))
c.at("Duró poco", P("vic"))
chapters.append(c)

c = ch("ch03")
c.at(0, P("mix"))
c.at("Número tres", rank(3, "SEAT 133", "m_seat133", 4, "Barcelona · 1974", "el que se escapó a Argentina"))
c.at("El 133 fue un coche", P("s133"))
c.at("Porque este coche sí logró", P("s133"))
c.at("Número dos", rank(2, "SEAT 1200 Sport", "m_bocanegra", 12, "Terrassa · 1975 – 1979", "el «Bocanegra»"))
c.at("La respuesta llegó", P("boca"))
c.at("Según las fuentes", stat("+19.000", "SEAT 1200/1430 Sport fabricados", "según las fuentes", count=False))
c.at("Fue el coche de los jóvenes", P("boca"))
c.at("una mención de honor", photo("m_pegaso", 3, "in", cap="Pegaso Z-102|mención de honor"))
c.at("Pero el número uno", P("r7"))
chapters.append(c)

c = ch("ch04")
c.at(0, rank(1, "Renault Siete", "m_r7", 1, "Valladolid · 1974", "el francés que Francia no quiso"))
c.at("Valladolid, 1974", P("r5"))
c.at("En Francia, Renault", P("fasa"))
c.at("El Siete fue", P("r7"))
c.at("Y funcionó", stat("≈160.000", "Renault Siete fabricados en Valladolid", "según las fuentes", count=False))
c.at("Lo más curioso", P("r7"))
chapters.append(c)

c = ch("ch05", 2.5)
c.at(0, P("mix"))
c.at("Cuando España se abrió", P("mix"))
c.at("Hoy son piezas", P("conc"))
c.at("Y ahora te pregunto a ti", P("mix"))
c.at("Y si te ha gustado el vídeo", cta("Suscríbete", "historias de coches clásicos"))
chapters.append(c)

CTX = ["mix", "s800", "dodge", "s133", "r7", "mix"]
print(A.finish(chapters, "ES11_SOLO_ESPANA.mp4", CTX, subtitles="ES11.ass"))
