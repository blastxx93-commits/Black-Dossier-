#!/usr/bin/env python3
"""ES17 ¿Cuántos sueldos costaba un coche? Race template.
    python3 build_es17.py <narration_dir> > episode.json   (run from the work folder)
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "engine"))
import aus_kit as A
from aus_kit import P, photo, rank, stat, say, cta, title, ch

PHOTOS = {
    "bisc": ["m_biscuter"], "s600": ["m_seat600"], "dau": ["m_dauphine"], "2cv": ["m_2cv"], "vocho": ["m_vocho"],
    "r4": ["m_r4"], "s124": ["m_seat124"], "s1430": ["m_seat1430"], "s1400": ["m_seat1400"], "pegaso": ["m_pegaso"],
    "r5": ["m_r5"], "s127": ["m_seat127"],
    "mix": ["h_calle", "h_concesionario"],
}
CLIPS = json.load(open(os.path.join(HERE, "clips.json")))
GENERIC = CLIPS.pop("_generic", [])
FALLBACK = {k: [] for k in PHOTOS}
FALLBACK.update({"mix": ["dau", "s124"], "r5": ["s127"], "s127": ["r5"]})
RES = ["m_vocho/10", "m_seat1400/2", "m_pegaso/5", "m_biscuter/5", "m_seat600/1", "m_dauphine/7", "m_2cv/1",
       "m_vocho/1", "m_r4/9", "m_seat124/3", "m_seat1430/14", "m_seat1400/13", "m_pegaso/11"]
A.setup(sys.argv[1], os.path.join(HERE, "skip.json"), PHOTOS, CLIPS, GENERIC, FALLBACK, [], reserved=RES)
A.THEME = "race"
A.CLIP_TARGET = 0.0
A.MAX_HOLD, A.KEEP = 12.0, 8.0
A.ARCHIVE_OK = True
A.STRICT_POOLS = True
A.SPLIT_BY_SUBJECT = True
chapters = []

c = ch("ch00_hook", 0.6)
c.at(0, photo("m_vocho", 10, "in", cap="Volkswagen Sedán|México, años 60"))
c.at("En la España de los cincuenta", photo("m_seat1400", 2, "in", cap="SEAT 1400|Barcelona, 1953"))
c.at("Y había un deportivo español", photo("m_pegaso", 5, "in", cap="Pegaso Z-102|años 50"))
c.at("Hoy un coche nuevo cuesta", P("s600"))
c.at("Hoy vas a descubrir", title("¿Cuántos sueldos costaba?", "los coches de nuestros abuelos", "España · México · Colombia", "mix"))
c.at("Una advertencia antes de empezar", P("mix"))
chapters.append(c)

c = ch("ch01")
c.at(0, P("mix"))
c.at("Comprar un coche, además", P("mix"))
c.at("Número diez", rank(10, "Biscúter", "m_biscuter", 5, "Barcelona · 1953", "el más barato de España"))
c.at("Parece poco", stat("≈3 años", "de sueldo íntegro por un Biscúter", "El Debate", count=False))
c.at("¿Y un coche normal?", P("bisc"))
c.at("Número nueve", rank(9, "SEAT 600", "m_seat600", 1, "Madrid · 1957", "65.000 pesetas"))
c.at("Las fuentes no se ponen de acuerdo", P("s600"))
chapters.append(c)

c = ch("ch02")
c.at(0, say("¿Desde dónde nos estás viendo?", "VIENDO", 120))
c.at("Y si todavía no estás suscrito", cta("Suscríbete", "historias de coches clásicos"))
c.at("Y del Seiscientos hay algo más", P("s600"))
c.at("Número ocho", rank(8, "Renault Dauphine", "m_dauphine", 7, "FASA · 1958", "108.350 pesetas"))
c.at("Por eso el Dauphine", P("dau"))
c.at("Número siete", rank(7, "Citroën 2CV", "m_2cv", 1, "Vigo", "más caro de lo que parecía"))
c.at("Pero no era tan barato", stat("91.500 pts", "Citroën 2CV · +40 % que un SEAT 600", "Autofácil", count=False))
c.at("un cuarenta por ciento más", P("2cv"))
c.at("Aun así, se convirtió", P("2cv"))
c.at("Número seis", rank(6, "Volkswagen Sedán", "m_vocho", 1, "México · 1964", "años de salario mínimo"))
c.at("Con ese sueldo", stat("2 años y 7 meses – 4 años", "de salario mínimo íntegro por un Vocho", "Motorpasión México", count=False))
c.at("Sin comer, sin pagar renta", P("vocho"))
c.at("Por eso el Vocho", P("vocho"))
c.at("Y para que te hagas una idea", P("vocho"))
chapters.append(c)

c = ch("ch03")
c.at(0, rank(5, "Renault 4", "m_r4", 9, "Envigado, Colombia · 1970", "73.900 pesos"))
c.at("Para muchas familias colombianas", P("r4"))
c.at("Y hay un dato curioso", P("r4"))
c.at("Número cuatro", rank(4, "SEAT 124", "m_seat124", 3, "1968", "el doble que un Seiscientos"))
c.at("Era mucho dinero", P("s124"))
c.at("El 124 también fue", P("s124"))
c.at("Número tres", rank(3, "SEAT 1430", "m_seat1430", 14, "1969", "136.600 pesetas"))
c.at("Haz la cuenta", stat("+44 meses", "de salario mínimo por un SEAT 1430", "Motorpasión", count=False))
c.at("Por eso el 1430", P("s1430"))
chapters.append(c)

c = ch("ch04")
c.at(0, rank(2, "SEAT 1400", "m_seat1400", 13, "Barcelona · 1953", "el primer SEAT"))
c.at("Su precio, según las fuentes", stat("≈10 años", "de salario por un SEAT 1400 (según algunas fuentes)", "según la fuente", count=False))
c.at("Por eso el 1400", P("s1400"))
c.at("Y ahora sí", P("pegaso"))
c.at("Número uno", rank(1, "Pegaso Z-102", "m_pegaso", 11, "ENASA · años 50", "el más caro de todos"))
c.at("¿Cuánto costaba?", stat("500.000 pts", "Pegaso Z-102 · un SEAT 600: ≈70.000", "según las fuentes", count=False))
c.at("Es decir, con el dinero", P("pegaso"))
c.at("Por eso casi nadie lo compró", P("pegaso"))
c.at("Piénsalo un momento", P("bisc"))
chapters.append(c)

c = ch("ch05", 2.5)
c.at(0, P("mix"))
c.at("Y en los años setenta", P("r5"))
c.at("Y según el testimonio", P("s127"))
c.at("Para nuestros padres y abuelos", P("mix"))
c.at("Y si has llegado hasta aquí", cta("Gracias por llegar al final", "suscríbete y déjame tu opinión"))
chapters.append(c)

CTX = ["vocho", "bisc", "s600", "r4", "s1400", "mix"]
print(A.finish(chapters, "ES17_SUELDOS.mp4", CTX, subtitles="ES17.ass"))
