#!/usr/bin/env python3
"""ES15 Coches de Latinoamérica que hoy valen una fortuna. Race template.
    python3 build_es15.py <narration_dir> > episode.json   (run from the work folder)
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "engine"))
import aus_kit as A
from aus_kit import P, photo, rank, stat, say, cta, title, ch

PHOTOS = {
    "f600": ["m_fiat600"], "vocho": ["m_vocho"], "r4": ["m_r4"], "falcon": ["m_falcon", "m_falcon2"],
    "torino": ["m_torino"], "chevy": ["m_chevy"], "barn": ["h_barn"],
    "mix": ["h_barn", "m_torino", "m_vocho"],
}
CLIPS = json.load(open(os.path.join(HERE, "clips.json")))
GENERIC = CLIPS.pop("_generic", [])
FALLBACK = {k: [] for k in PHOTOS}
FALLBACK.update({"mix": ["f600", "r4"], "barn": ["mix"]})
RES = ["m_chevy/10", "m_chevy/4", "m_fiat600/4", "m_vocho/1", "m_r4/3", "m_torino/1", "m_torino/3", "m_vocho/12"]
A.setup(sys.argv[1], os.path.join(HERE, "skip.json"), PHOTOS, CLIPS, GENERIC, FALLBACK, [], reserved=RES)
A.THEME = "race"
A.CLIP_TARGET = 0.0
A.MAX_HOLD, A.KEEP = 8.0, 5.5
A.ARCHIVE_OK = True
A.STRICT_POOLS = True
A.SPLIT_BY_SUBJECT = True
chapters = []

c = ch("ch00_hook", 0.6)
c.at(0, photo("m_chevy", 10, "in", cap="Chevrolet Chevy SS|Argentina"))
c.at("En México, un Vocho", photo("m_vocho", 12, "in", cap="Volkswagen Sedán|México"))
c.at("Y en Colombia, un Renault 4", photo("m_r4", 3, "in", cap="Renault 4|Colombia"))
c.at("Coches que tu abuelo", P("barn"))
c.at("Coches que nadie quería", P("barn"))
c.at("Hoy vas a conocer", title("Hoy valen una fortuna", "coches de Latinoamérica", "México · Colombia · Argentina", "mix"))
c.at("Una advertencia antes de empezar", P("torino"))
chapters.append(c)

c = ch("ch01")
c.at(0, rank(6, "Fiat 600", "m_fiat600", 4, "Argentina · 1960", "el «Fitito»"))
c.at("Durante décadas, nadie le dio valor", P("f600"))
c.at("En los anuncios de Mercado Libre", stat("2.800 – 16.000 US$", "Fiat 600 de 1965 · anuncios", "Mercado Libre", count=False))
c.at("Nada mal para el coche", P("f600"))
c.at("Número cinco", rank(5, "Volkswagen Sedán", "m_vocho", 1, "México", "el «Vocho»"))
c.at("Durante décadas fue tan común", P("vocho"))
c.at("Pero en una subasta organizada en Los Pinos", stat("360.000 MXN", "Vocho de 1951 · subasta en Los Pinos", "según la fuente", count=False))
c.at("Y en Estados Unidos", P("vocho"))
chapters.append(c)

c = ch("ch02")
c.at(0, say("¿Desde dónde nos estás viendo?", "VIENDO", 120))
c.at("Y si todavía no estás suscrito", cta("Suscríbete", "historias de coches clásicos"))
c.at("Número cuatro", rank(4, "Renault 4", "m_r4", 3, "Envigado, Colombia · 1970", "el «amigo fiel»"))
c.at("Hoy, según un sondeo", stat("hasta 60 millones COP", "Renault 4 con placa de clásico · anuncios", "Portafolio", count=False))
c.at("Y en Francia, una versión", stat("95.360 €", "Renault 4 Plein Air · Artcurial 2026", "Artcurial", count=False))
chapters.append(c)

c = ch("ch03")
c.at(0, rank(3, "Ford Falcon Sprint", "m_falcon", 7, "Argentina · años 70", "el Falcon deportivo"))
c.at("Hoy, en los anuncios", stat("13.000 – 20.000 US$", "Falcon Sprint · anuncios", "Mercado Libre", count=False))
c.at("Mucho más que un Falcon normal", P("falcon"))
c.at("Número dos", rank(2, "IKA Torino", "m_torino", 1, "Argentina · 1966", "el orgullo nacional"))
c.at("Y en 1969, tres Torino", photo("m_torino", 3, "in", cap="IKA Torino|84 horas de Nürburgring, 1969"))
c.at("Hoy el Torino es uno", P("torino"))
c.at("Según los anuncios recogidos", stat("10.000 – 29.000 US$", "Torino · anuncios", "iProfesional", count=False))
c.at("Y ahora sí", P("chevy"))
chapters.append(c)

c = ch("ch04")
c.at(0, rank(1, "Chevrolet Chevy SS", "m_chevy", 4, "Argentina", "el coupé del Turismo Carretera"))
c.at("Era el coche de los que querían", P("chevy"))
c.at("¿Cuánto valen?", stat("38.500 US$", "Chevy Coupé SS 1971 · anuncio 2022", "MDZ", count=False))
c.at("Y hoy, en los anuncios de Mercado Libre", stat("hasta 60.000 US$", "Chevy SS · anuncios", "Mercado Libre", count=False))
c.at("Sesenta mil dólares", P("chevy"))
chapters.append(c)

c = ch("ch05", 2.5)
c.at(0, P("mix"))
c.at("Así que, si en tu familia", P("barn"))
c.at("Y ahora te pregunto a ti", P("mix"))
c.at("Y si has llegado hasta aquí", cta("Gracias por llegar al final", "suscríbete y déjame tu opinión"))
chapters.append(c)

CTX = ["chevy", "f600", "r4", "falcon", "chevy", "mix"]
print(A.finish(chapters, "ES15_LATAM_FORTUNA.mp4", CTX, subtitles="ES15.ass"))
