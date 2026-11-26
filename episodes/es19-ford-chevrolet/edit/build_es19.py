#!/usr/bin/env python3
"""ES19 Ford vs Chevrolet: la guerra que dividió Argentina. Race template.
    python3 build_es19.py <narration_dir> > episode.json   (run from the work folder)
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "engine"))
import aus_kit as A
from aus_kit import P, photo, stat, say, cta, title, ch

PHOTOS = {"cup": ["m_cupecita", "m_tcpublico", "m_galera"], "ford": ["m_ford40", "m_galvez"], "chev": ["m_chev40"],
          "falcon": ["m_falcon2", "m_falcontc"], "chevy": ["m_chevy2"], "torino": ["m_torinotc"], "dodge": ["m_dodgetc"],
          "trueno": ["m_trueno"], "fangio": ["m_fangiochev"], "mix": ["m_cupecita", "m_falcon2", "m_chevy2"]}
CLIPS = json.load(open(os.path.join(HERE, "clips.json")))
GENERIC = CLIPS.pop("_generic", [])
FALLBACK = {k: [] for k in PHOTOS}
FALLBACK.update({"ford": ["cup"], "chev": ["chevy", "cup"], "trueno": ["chevy"], "fangio": ["chev"], "chevy": ["chev"], "falcon": ["ford"], "cup": ["ford", "chev"], "mix": ["torino", "dodge", "ford"]})
RES = ["m_cupecita/10", "m_galvez/4", "m_galera/5", "m_trueno/2", "m_torinotc/11", "m_dodgetc/1", "m_falcon2/10"]
A.setup(sys.argv[1], os.path.join(HERE, "skip.json"), PHOTOS, CLIPS, GENERIC, FALLBACK, [], reserved=RES)
A.THEME = "race"
A.CLIP_TARGET = 0.0
A.MAX_HOLD, A.KEEP = 14.0, 10.0
A.ARCHIVE_OK = True
A.STRICT_POOLS = True
A.SPLIT_BY_SUBJECT = True
chapters = []

c = ch("ch00_hook", 0.6)
c.at(0, photo("m_cupecita", 10, "in", cap="Turismo Carretera|Argentina"))
c.at("Era una rivalidad", P("ford"))
c.at("Hoy vas a conocer", title("Ford vs Chevrolet", "la guerra del Turismo Carretera", "Argentina · 1937 – 1999", "cup"))
c.at("Quiénes fueron sus héroes", P("chev"))
chapters.append(c)

c = ch("ch01")
c.at(0, photo("m_galera", 5, "in", cap="Turismo Carretera|por las rutas argentinas"))
c.at("Y las carreras fueron cada vez", stat("+7.000 km", "Gran Premio de 1939", "Museo Fangio", count=False))
c.at("De aquellas carreras nació", P("cup"))
c.at("Los autos de aquella época", P("cup"))
c.at("Y fue en esos años", P("ford"))
c.at("Aquellos duelos entre", P("chev"))
c.at("Fangio se fue a Europa", P("fangio"))
chapters.append(c)

c = ch("ch02")
c.at(0, say("¿Desde dónde nos estás viendo?", "VIENDO", 120))
c.at("Y si todavía no estás suscrito", cta("Suscríbete", "historias de autos clásicos", tv=True))
c.at("Si hay un nombre que representa", photo("m_galvez", 4, "in", cap="Ford de Oscar Gálvez|museo"))
c.at("Y no solo ganaban campeonatos", stat("56", "victorias de Juan Gálvez con Ford", "estadísticas del TC", count=True))
c.at("Durante los años cincuenta", P("ford"))
c.at("Dante y Torcuato Emiliozzi", P("cup"))
c.at("Para los chevroletistas", P("chev"))
c.at("Al principio, al público", P("chevy"))
c.at("Chevrolet lo intentaba todo", P("chev"))
c.at("Hasta que llegó", say("1966", "1966", 220))
chapters.append(c)

c = ch("ch03")
c.at(0, P("chev"))
c.at("Bordeu fue campeón", stat("1966", "Chevrolet rompe el dominio de Ford", "según las fuentes", count=False))
c.at("Pero la historia no terminó ahí", photo("m_trueno", 2, "in", cap="Trueno Naranja|Chevrolet · Pairetti, 1968"))
c.at("Chevrolet había vuelto", P("trueno"))
c.at("la empresa argentina IKA", P("torino"))
c.at("Durante unos años", P("torino"))
c.at("Y ese orgullo llegó hasta Europa", photo("m_torinotc", 11, "in", cap="IKA Torino|84 Horas de Nürburgring, 1969"))
c.at("En esos años, además", P("trueno"))
c.at("Pero Ford no se quedó quieto", photo("m_falcon2", 10, "in", cap="Ford Falcon|Argentina"))
c.at("Según las fuentes, Héctor Gradassi", P("falcon"))
c.at("El Falcon se había convertido", P("falcon"))
chapters.append(c)

c = ch("ch04")
c.at(0, P("chevy"))
c.at("Y entonces apareció otro rival", photo("m_dodgetc", 1, "in", cap="Dodge|Turismo Carretera"))
c.at("Y Dodge no se detuvo", P("dodge"))
c.at("La guerra ya no era solo de dos", P("mix"))
c.at("Según las fuentes, Emilio Satriano", P("chevy"))
c.at("Y entonces llegó uno de los giros", P("falcon"))
c.at("Y con Chevrolet, según las fuentes", stat("1995 · 1996 · 1997", "Traverso campeón con Chevrolet", "según las fuentes", count=False))
c.at("Pero la historia de Traverso", P("falcon"))
c.at("Esa rivalidad se vivía", P("cup"))
c.at("Y cuando la carrera pasaba", P("cup"))
c.at("Con el tiempo, el Turismo Carretera", P("mix"))
chapters.append(c)

c = ch("ch05", 2.5)
c.at(0, P("mix"))
c.at("Si miramos los números", stat("Ford ≈46 · Chevrolet ≈23", "campeonatos del Turismo Carretera", "tablas históricas", count=False))
c.at("Pero si preguntas a un chevroletista", P("trueno"))
c.at("Porque esta guerra nunca", P("cup"))
c.at("Y ahora te pregunto a ti", P("mix"))
c.at("Y si has llegado hasta aquí", cta("Gracias por llegar al final", "suscríbete y déjame tu opinión", tv=True, remote=True))
chapters.append(c)

CTX = ["cup", "cup", "ford", "torino", "dodge", "mix"]
print(A.finish(chapters, "ES19_FORD_CHEVROLET.mp4", CTX, subtitles="ES19.ass"))
