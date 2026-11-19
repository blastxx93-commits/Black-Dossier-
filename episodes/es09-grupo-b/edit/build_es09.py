#!/usr/bin/env python3
"""ES09 Grupo B. Countdown list, theme "revista". Real photos only (no usable free clips; Replicate without credit).
Tragedies (Portugal 1986, Toivonen 1986): intact cars and portraits only, never the crash.
    python3 build_es09.py <narration_dir> > episode.json   (run from the work folder)
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "engine"))
import aus_kit as A
from aus_kit import P, photo, rank, stat, say, cta, title, ch, questions

PHOTOS = {
    "r5": ["m_r5turbo"], "copa": ["m_r5copa"], "manta": ["m_manta400"], "celica": ["m_celica_tct"],
    "metro": ["m_metro6r4"], "rs200": ["m_rs200"], "l037": ["m_lancia037"], "quattro": ["m_quattro", "h_pikes"],
    "mouton": ["h_mouton", "h_pikes"], "t16": ["m_205t16"], "s4": ["m_deltas4", "h_toivonen"], "bx": ["m_bx4tc"],
    "p959": ["m_porsche959"], "crowd": ["h_rally_crowd"], "gb": ["m_group_b", "m_lancia037", "m_quattro", "m_205t16"],
}
CLIPS = json.load(open(os.path.join(HERE, "clips.json")))
GENERIC = CLIPS.pop("_generic", [])
FALLBACK = {k: ["gb"] for k in PHOTOS}
FALLBACK.update({"gb": ["quattro", "t16"], "copa": ["r5"], "r5": ["copa", "gb"], "mouton": ["quattro"], "crowd": ["gb"],
                 "s4": ["gb"], "p959": ["gb"], "bx": ["gb"]})
RES = ["m_r5turbo/6", "m_r5copa/2", "m_manta400/2", "m_celica_tct/2", "m_metro6r4/4", "m_metro6r4/1", "m_rs200/8",
       "m_lancia037/3", "m_quattro/1", "m_205t16/2", "m_deltas4/4", "m_bx4tc/2", "m_porsche959/3", "h_mouton/3",
       "h_toivonen/1", "h_pikes/5", "h_rally_crowd/6"]
A.setup(sys.argv[1], os.path.join(HERE, "skip.json"), PHOTOS, CLIPS, GENERIC, FALLBACK, ["gb", "quattro"], reserved=RES)
A.THEME = "revista"
A.CLIP_TARGET = 0.0
A.MAX_HOLD, A.KEEP = 11.0, 7.0
A.ARCHIVE_OK = True
A.SPLIT_BY_SUBJECT = True
chapters = []

c = ch("ch00_hook", 0.6)
c.at(0, photo("h_rally_crowd", 6, "in", cap="Mundial de Rallies|años 80"))
c.at("Y entonces se oye", P("quattro"))
c.at("Esto no es una película", P("gb"))
c.at("Solo duró unas pocas temporadas", say("Tan brutales que los prohibieron.", "PROHIBIERON", 120))
c.at("Hoy vas a conocer los diez coches", title("Grupo B", "los coches de rally más brutales", "1982 – 1986", "gb"))
questions(c, ["Un Grupo B vendido en España", "Turbo y compresor a la vez", "El que nunca llegó a correr"],
          ["Uno de ellos tiene una versión de calle", "Otro llevaba a la vez", "Y el número uno"])
chapters.append(c)

c = ch("ch01")
c.at(0, P("gb"))
c.at("Con el nuevo Grupo B, bastaba", stat("200", "unidades de calle para homologar un Grupo B", "FIA", count=True))
c.at("Eso significaba que las marcas", P("gb"))
c.at("En apenas cuatro años", stat("300 → 500+", "caballos · 1982 – 1986", "según la fuente", count=False))
c.at("Porque esa es la otra parte", P("crowd"))
c.at("Era espectacular", P("gb"))
c.at("Número diez", rank(10, "Renault 5 Turbo", "m_r5turbo", 6, "Francia · 1980", "el utilitario que fue al gimnasio"))
c.at("Con él, el piloto francés Jean Ragnotti", P("r5"))
c.at("Y aquí viene la parte española", photo("m_r5copa", 2, "in", cap="Renault 5 Copa Turbo|España, 1982 – 1984"))
c.at("Si tu padre o tu tío", P("copa"))
chapters.append(c)

c = ch("ch02")
c.at(0, rank(9, "Opel Manta 400", "m_manta400", 2, "Alemania · 1983", "tracción trasera y sin turbo"))
c.at("No era el más rápido", P("manta"))
c.at("Número ocho", rank(8, "Toyota Celica TCT", "m_celica_tct", 2, "Japón · 1984", "el rey del Safari"))
c.at("Toyota preparó un Celica", P("celica"))
c.at("Fue el primer gran aviso", P("celica"))
c.at("Número siete", rank(7, "MG Metro 6R4", "m_metro6r4", 4, "Reino Unido · 1985", "el coche de la abuela con un V6"))
c.at("Coge un Metro", photo("m_metro6r4", 1, "in", cap="Austin Metro|el original"))
c.at("Su nombre lo explica todo", P("metro"))
c.at("Un utilitario familiar", P("metro"))
chapters.append(c)

c = ch("ch03")
c.at(0, rank(6, "Ford RS200", "m_rs200", 8, "Reino Unido · 1986", "diseñado desde cero"))
c.at("Pero su historia en el Mundial", P("rs200"))
c.at("Aquel día, muchos entendieron", say("Las máquinas habían crecido demasiado rápido.", "DEMASIADO", 100))
c.at("Tras la prohibición del Grupo B, el RS200", P("rs200"))
c.at("Número cinco", rank(5, "Lancia 037", "m_lancia037", 3, "Italia · 1982", "el último campeón de tracción trasera"))
c.at("En teoría, no tenía nada que hacer", P("l037"))
c.at("Detrás de aquella victoria", P("l037"))
chapters.append(c)

c = ch("ch04")
c.at(0, rank(4, "Audi Quattro", "m_quattro", 1, "Alemania · 1980", "la tracción total que lo cambió todo"))
c.at("En cuanto empezó a correr", P("quattro"))
c.at("Y hay una historia que merece", photo("h_mouton", 3, "in", cap="Michèle Mouton|Audi Quattro"))
c.at("Pero la evolución final", P("quattro"))
c.at("Después de la prohibición, el alemán Walter Röhrl", photo("h_pikes", 5, "in", cap="Pikes Peak|Audi Sport Quattro S1"))
c.at("Número tres", rank(3, "Peugeot 205 T16", "m_205t16", 2, "Francia · 1984", "campeón en 1985 y 1986"))
c.at("Peugeot coge la silueta", P("t16"))
c.at("El 205 Turbo 16 ganó", P("t16"))
c.at("Pero también tuvo su lado oscuro", P("t16"))
c.at("Y aquí viene otro detalle", P("t16"))
chapters.append(c)

c = ch("ch05")
c.at(0, rank(2, "Lancia Delta S4", "m_deltas4", 4, "Italia · 1985", "turbo y compresor a la vez"))
c.at("El Delta S4 era probablemente el más rápido", photo("h_toivonen", 1, "in", cap="Lancia Delta S4|Henri Toivonen"))
c.at("Pero en mayo de 1986", say("Tour de Córcega · mayo de 1986", "1986", 120))
c.at("La reacción fue inmediata", P("s4"))
c.at("Hoy el Delta S4 es el símbolo", P("s4"))
chapters.append(c)

c = ch("ch06", 2.5)
c.at(0, photo("m_bx4tc", 2, "in", cap="Citroën BX 4TC|1986"))
c.at("Para homologarlo, Citroën", P("bx"))
c.at("Y hay algo más", P("gb"))
c.at("Y llegamos al número uno", rank(1, "Porsche 959", "m_porsche959", 3, "Alemania · 1985", "nació para el Grupo B… y nunca lo corrió"))
c.at("Pero el desarrollo fue tan largo", P("p959"))
c.at("Así que Porsche hizo lo que haría cualquiera", P("p959"))
c.at("Y la versión de calle se convirtió", P("p959"))
c.at("Piénsalo", P("p959"))
c.at("Así terminó el Grupo B", P("gb"))
c.at("Y ahora te pregunto a ti", P("gb"))
c.at("Y si te ha gustado el vídeo", cta("Suscríbete", "historias de coches clásicos"))
chapters.append(c)

CTX = ["gb", "r5", "manta", "rs200", "quattro", "s4", "p959"]
print(A.finish(chapters, "ES09_GRUPO_B.mp4", CTX, subtitles="ES09.ass"))
