#!/usr/bin/env python3
"""ES14 Los coches que tu abuelo tuvo (México, Colombia, Argentina, España). Race template.
    python3 build_es14.py <narration_dir> > episode.json   (run from the work folder)
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "engine"))
import aus_kit as A
from aus_kit import P, photo, rank, stat, say, cta, title, ch

PHOTOS = {
    "datsun": ["m_datsun"], "simca": ["m_simca"], "r12": ["m_r12"], "s600": ["m_seat600"], "f600": ["m_fiat600"],
    "r4": ["m_r4"], "falcon": ["m_falcon"], "vocho": ["m_vocho"], "taxi": ["h_vochotaxi"],
    "mix": ["m_r12", "m_simca", "m_datsun", "m_seat600"],
}
CLIPS = json.load(open(os.path.join(HERE, "clips.json")))
GENERIC = CLIPS.pop("_generic", [])
FALLBACK = {k: [] for k in PHOTOS}
FALLBACK.update({"s600": ["f600"], "f600": ["s600"], "taxi": ["vocho"], "vocho": ["taxi"], "mix": ["r4", "vocho"]})
RES = ["m_vocho/1", "m_fiat600/7", "m_r4/2", "m_datsun/1", "m_simca/2", "m_r12/1", "m_seat600/1", "m_fiat600/13",
       "m_r4/5", "m_falcon/3", "m_vocho/16", "h_vochotaxi/3"]
A.setup(sys.argv[1], os.path.join(HERE, "skip.json"), PHOTOS, CLIPS, GENERIC, FALLBACK, [], reserved=RES)
A.THEME = "race"
A.CLIP_TARGET = 0.0
A.MAX_HOLD, A.KEEP = 10.0, 7.0
A.ARCHIVE_OK = True
A.STRICT_POOLS = True
A.SPLIT_BY_SUBJECT = True
chapters = []

c = ch("ch00_hook", 0.6)
c.at(0, photo("m_vocho", 1, "in", cap="Volkswagen Sedán|México"))
c.at("El de tu abuelo", P("r12"))
c.at("El que te llevaba", P("s600"))
c.at("Algunos se fabricaron", P("falcon"))
c.at("Uno de ellos fue el taxi", photo("h_vochotaxi", 3, "in", cap="Vocho taxi|Ciudad de México"))
c.at("Otro se ganó el apodo", photo("m_r4", 2, "in", cap="Renault 4|«amigo fiel»"))
c.at("Y otro era tan pequeño", photo("m_fiat600", 7, "in", cap="Fiat 600|«Fitito»"))
c.at("Hoy vas a conocer", title("Los coches de tu abuelo", "Latinoamérica y España", "1957 – 2003", "mix"))
c.at("Y quédate hasta el final", P("vocho"))
chapters.append(c)

c = ch("ch01")
c.at(0, P("mix"))
c.at("Y así, grandes marcas", P("datsun"))
c.at("Número ocho", rank(8, "Datsun Bluebird", "m_datsun", 1, "Morelos, México · 1966", "el primer Nissan hecho en México"))
c.at("Según las fuentes, fue el primer", P("datsun"))
c.at("Entre 1966 y 1968", stat("≈10.500", "Datsun Bluebird fabricados en México (1966 – 1968)", "según las fuentes", count=False))
c.at("Número siete", rank(7, "Simca 1000", "m_simca", 2, "Colombia · 1969", "el primer coche popular"))
c.at("Para muchos colombianos", P("simca"))
c.at("Y aquí hay un detalle curioso", P("simca"))
chapters.append(c)

c = ch("ch02")
c.at(0, say("¿Desde dónde nos estás viendo?", "VIENDO", 120))
c.at("Y si todavía no estás suscrito", cta("Suscríbete", "historias de coches clásicos"))
c.at("Número seis", rank(6, "Renault 12", "m_r12", 1, "España · Argentina · Colombia", "el coche de la familia"))
c.at("En 1977, según las fuentes", P("r12"))
c.at("Era grande, cómodo", P("r12"))
c.at("Número cinco", rank(5, "SEAT 600", "m_seat600", 1, "Barcelona · 1957", "el coche que motorizó España"))
c.at("Las llevó a la playa", P("s600"))
c.at("Pero el Seiscientos tenía un hermano", P("f600"))
c.at("Número cuatro", rank(4, "Fiat 600", "m_fiat600", 13, "Argentina · 1960", "el «Fitito»"))
c.at("Fue el primer coche de miles", P("f600"))
chapters.append(c)

c = ch("ch03")
c.at(0, rank(3, "Renault 4", "m_r4", 5, "Envigado, Colombia · 1970", "el «amigo fiel»"))
c.at("En 1975, una campaña", P("r4"))
c.at("Se fabricó en Envigado", stat("≈97.000", "Renault 4 fabricados en Envigado", "según las fuentes", count=False))
c.at("Fue el coche del campesino", P("r4"))
c.at("Número dos", rank(2, "Ford Falcon", "m_falcon", 3, "Argentina · 1962", "treinta años en producción"))
c.at("El Falcon fue el coche", P("falcon"))
c.at("Y ahora sí", P("vocho"))
chapters.append(c)

c = ch("ch04")
c.at(0, rank(1, "Volkswagen Sedán", "m_vocho", 16, "Puebla, México · 1967", "el «Vocho»"))
c.at("En México lo llamaron", P("vocho"))
c.at("Y durante décadas, los vochos taxi", P("taxi"))
c.at("El Vocho se fabricó en Puebla", stat("+1.600.000", "Vochos fabricados en Puebla", "según las fuentes", count=False))
c.at("Hoy, en cualquier calle", P("vocho"))
chapters.append(c)

c = ch("ch05", 2.5)
c.at(0, P("mix"))
c.at("Y ahora te pregunto a ti", P("vocho"))
c.at("Y si has llegado hasta aquí", cta("Gracias por llegar al final", "suscríbete y déjame tu opinión"))
chapters.append(c)

CTX = ["vocho", "datsun", "r12", "r4", "vocho", "mix"]
print(A.finish(chapters, "ES14_ABUELO.mp4", CTX, subtitles="ES14.ass"))
