#!/usr/bin/env python3
"""ES12 Las marcas de coches españolas que desaparecieron. Countdown; rendered with the Race template (engine/hf_race.py).
    python3 build_es12.py <narration_dir> > episode.json   (run from the work folder)
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "engine"))
import aus_kit as A
from aus_kit import P, photo, rank, stat, say, cta, title, ch, questions

PHOTOS = {
    "sava": ["m_sava"], "ptv": ["m_ptv"], "bisc": ["m_biscuter"], "dkw": ["m_dkw_f1000"], "vitoria": ["h_vitoria"],
    "authi": ["m_authi"], "barr": ["m_barreiros"], "dart": ["m_dodgedart"], "simca": ["m_simca1000"],
    "santana": ["m_santana"], "linares": ["h_linares"], "pegaso": ["m_pegaso_truck"], "z102": ["m_pegaso_z102"],
    "hispano": ["h_hispano"],
    "mix": ["m_pegaso_truck", "m_santana", "m_biscuter", "m_dkw_f1000", "m_authi", "m_sava"],
}
CLIPS = json.load(open(os.path.join(HERE, "clips.json")))
GENERIC = CLIPS.pop("_generic", [])
FALLBACK = {k: ["mix"] for k in PHOTOS}
FALLBACK.update({"mix": ["z102", "hispano"], "ptv": ["bisc"], "bisc": ["ptv"], "dkw": ["vitoria"], "vitoria": ["dkw"],
                 "barr": ["dart", "simca"], "dart": ["simca", "barr"], "simca": ["dart", "barr"], "santana": ["linares"],
                 "linares": ["santana"], "pegaso": ["z102", "hispano"], "z102": ["pegaso"], "hispano": ["pegaso"]})
RES = ["m_pegaso_z102/3", "m_sava/1", "m_ptv/3", "m_biscuter/14", "m_dkw_f1000/12", "m_authi/2", "m_barreiros/1",
       "m_santana/10", "m_pegaso_truck/9", "m_dodgedart/9", "m_simca1000/3", "h_hispano/1", "h_vitoria/6"]
A.setup(sys.argv[1], os.path.join(HERE, "skip.json"), PHOTOS, CLIPS, GENERIC, FALLBACK, ["mix", "pegaso"], reserved=RES)
A.THEME = "race"
A.CLIP_TARGET = 0.0
A.MAX_HOLD, A.KEEP = 6.0, 4.0
A.ARCHIVE_OK = True
A.SPLIT_BY_SUBJECT = True
chapters = []

c = ch("ch00_hook", 0.6)
c.at(0, photo("m_pegaso_z102", 3, "in", cap="Pegaso Z-102|Barcelona, 1953"))
c.at("Camiones que recorrían", P("pegaso"))
c.at("Microcoches que se vendían", P("bisc"))
c.at("Todoterrenos que se exportaban", P("santana"))
c.at("Y furgonetas que se convirtieron", P("dkw"))
c.at("Todas esas marcas eran españolas", say("Todas desaparecieron.", "DESAPARECIERON", 140))
c.at("Algunas cerraron por falta de dinero", P("mix"))
c.at("Una de ellas acabó convertida", P("vitoria"))
c.at("Hoy vas a conocer las marcas", title("Marcas españolas desaparecidas", "de dónde salieron y qué pasó con ellas", "1946 – 2011", "mix"))
questions(c, ["La que acabó siendo Mercedes", "La que acabó siendo Volkswagen", "El fundador que terminó en Cuba"],
          ["De dónde salieron", "qué fabricaban", "Y quédate hasta el final"])
chapters.append(c)

c = ch("ch01")
c.at(0, P("mix"))
c.at("Número ocho", rank(8, "SAVA", "m_sava", 1, "Valladolid · 1957 – 1969", "los camiones de Valladolid"))
c.at("Eran los vehículos del pequeño transportista", P("sava"))
c.at("Pero el mercado de los camiones", P("sava"))
c.at("Número siete", rank(7, "PTV", "m_ptv", 3, "Manresa · años 50", "el microcoche catalán"))
c.at("Durante unos años", P("ptv"))
c.at("Pero en 1957 llegó el SEAT 600", P("ptv"))
c.at("Número seis", rank(6, "Autonacional · Biscúter", "m_biscuter", 14, "Barcelona · años 50", "el «zapatilla»"))
c.at("El Biscúter era casi un juguete", P("bisc"))
c.at("Como el PTV", P("bisc"))
chapters.append(c)

c = ch("ch02")
c.at(0, rank(5, "IMOSA", "m_dkw_f1000", 12, "Vitoria · 1950", "la furgoneta DKW F1000"))
c.at("En los años sesenta, Imosa lanzó", P("dkw"))
c.at("Pero la propiedad de la empresa", P("dkw"))
c.at("Pero aquí viene lo sorprendente", photo("h_vitoria", 6, "in", cap="Mercedes-Benz|Vitoria, hoy"))
c.at("Número cuatro", rank(4, "AUTHI", "m_authi", 2, "Pamplona · 1965 – 1975", "los coches británicos de Navarra"))
c.at("Authi no se limitó a copiar", P("authi"))
c.at("Pero a principios de los setenta", P("authi"))
c.at("Y aquí está el giro", say("Hoy es una fábrica de Volkswagen.", "VOLKSWAGEN", 120))
chapters.append(c)

c = ch("ch03")
c.at(0, P("mix"))
c.at("Número tres", rank(3, "BARREIROS", "m_barreiros", 1, "Madrid · 1954 – 1969", "el hombre que desafió a todos"))
c.at("Aquella idea lo convirtió", P("barr"))
c.at("Pero Barreiros quería más", photo("m_dodgedart", 9, "in", cap="Dodge Dart|Barreiros, Villaverde"))
c.at("Así llegaron a España el Simca 1000", P("simca"))
c.at("La marca Barreiros desapareció", P("dart"))
c.at("se fue a Cuba", say("Murió en La Habana en 1992.", "LA HABANA", 120))
c.at("Número dos", rank(2, "SANTANA", "m_santana", 10, "Linares · 1956 – 2011", "el Land Rover español"))
c.at("Durante décadas, los Santana", P("santana"))
c.at("Durante mucho tiempo fue el gran motor", P("santana"))
chapters.append(c)

c = ch("ch04")
c.at(0, rank(1, "PEGASO", "m_pegaso_truck", 9, "ENASA · 1946 – 1994", "el caballo alado"))
c.at("Su historia empieza en 1946", photo("h_hispano", 1, "in", cap="Hispano-Suiza|Barcelona"))
c.at("Durante más de cuarenta años", P("pegaso"))
c.at("Y en los años cincuenta", P("z102"))
c.at("Pegaso llegó a fabricar", P("pegaso"))
c.at("Hoy, en muchas carreteras", P("pegaso"))
chapters.append(c)

c = ch("ch05", 2.5)
c.at(0, P("mix"))
c.at("Pero hay algo curioso", P("vitoria"))
c.at("Y ahora te pregunto a ti", P("mix"))
c.at("Y si te ha gustado el vídeo", cta("Suscríbete", "historias de coches clásicos"))
chapters.append(c)

CTX = ["mix", "sava", "dkw", "barr", "pegaso", "mix"]
print(A.finish(chapters, "ES12_MARCAS.mp4", CTX, subtitles="ES12.ass"))
