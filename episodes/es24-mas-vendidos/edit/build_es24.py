#!/usr/bin/env python3
"""ES24 El auto más vendido de tu país. Race template. Regra: imagem = narração."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "engine"))
import aus_kit as A
from aus_kit import P, photo, stat, say, cta, title, ch

PHOTOS = {k: ["m_" + k] + (["m_r4b"] if k == "r4" else ["m_tsurub"] if k == "tsuru" else []) for k in ["seat600", "seat127", "r5", "r9", "r19", "clio", "fiesta", "vocho", "tsuru", "fiat600",
                                    "falcon", "r12", "504", "duna", "r4", "131", "sprint", "323"]}
CLIPS = json.load(open(os.path.join(HERE, "clips.json")))
GENERIC = CLIPS.pop("_generic", [])
FALLBACK = {k: [] for k in PHOTOS}
RES = ["m_vocho/12_commons", "m_r12/14_commons", "m_seat127/10_openverse", "m_seat600/1_commons", "m_tsuru/10_openverse",
       "m_r4/13_commons", "m_323/4_commons"]
A.setup(sys.argv[1], os.path.join(HERE, "skip.json"), PHOTOS, CLIPS, GENERIC, FALLBACK, [], reserved=[r.rsplit("_", 1)[0] for r in RES])
A.THEME = "race"; A.CLIP_TARGET = 0.0; A.MAX_HOLD, A.KEEP = 12.0, 8.0
A.ARCHIVE_OK = True; A.STRICT_POOLS = True; A.SPLIT_BY_SUBJECT = True
chapters = []

c = ch("ch00_hook", 0.6)
c.at(0, photo("m_vocho", 12, "in", cap="Volkswagen Sedán|México"))
c.at("En Argentina, un auto francés", photo("m_r12", 14, "in", cap="Renault 12|Argentina"))
c.at("Y en España, un pequeño utilitario", photo("m_seat127", 10, "in", cap="SEAT 127|España"))
c.at("Cada país tiene su auto", P("r5"))
c.at("Hoy vas a viajar", title("El más vendido", "de tu país, década por década", "España · México · Argentina · Colombia", "seat600"))
c.at("Prepárate, porque es muy probable", P("falcon"))
c.at("Y una advertencia", P("504"))
chapters.append(c)

c = ch("ch01")
c.at(0, P("seat600"))
c.at("Los años sesenta tienen un rey", photo("m_seat600", 1, "in", cap="SEAT 600|años 60"))
c.at("Según las fuentes, SEAT fabricó", stat("≈800.000", "SEAT 600 fabricados (1957 – 1973)", "según las fuentes", count=False))
c.at("Y durante esos años", P("seat600"))
c.at("Pero en los años setenta", P("seat127"))
c.at("Según los registros de ventas, el 127", stat("1973 – 1979", "SEAT 127 · número uno en España", "según los registros", count=False))
c.at("El 127 era moderno", P("seat127"))
c.at("En esos años, además", P("fiesta"))
c.at("Pero el 127 aguantó", P("seat127"))
c.at("Los años ochenta fueron franceses", P("r5"))
c.at("En mil novecientos ochenta y tres", P("r9"))
c.at("Y Renault siguió mandando", P("r19"))
c.at("Y a principios de los noventa", P("clio"))
c.at("Es decir, durante muchos años", P("r5"))
chapters.append(c)

c = ch("ch02")
c.at(0, say("¿Desde dónde nos estás viendo?", "VIENDO", 120))
c.at("Y si todavía no estás suscrito", cta("Suscríbete", "historias de autos clásicos", tv=True))
c.at("Cruzamos el océano", P("vocho"))
c.at("Ese año, según una de esas fuentes", stat("≈22 %", "de los autos de México eran un Vocho (1968)", "según las fuentes", count=False))
c.at("Durante los años setenta y ochenta", P("vocho"))
c.at("Pero en los años ochenta llegó un rival", photo("m_tsuru", 10, "in", cap="Nissan Tsuru|México, desde 1984"))
c.at("Para muchos mexicanos fue una sorpresa", P("tsuru"))
c.at("Pero todas coinciden en algo", stat("+2.400.000", "Nissan Tsuru vendidos en México (1984 – 2017)", "según las fuentes", count=False))
c.at("Y en segundo lugar, aparece el Vocho", P("vocho"))
c.at("Y el Tsuru también tuvo", P("tsuru"))
c.at("Así que la historia del auto más vendido de México", P("vocho"))
chapters.append(c)

c = ch("ch03")
c.at(0, P("fiat600"))
c.at("En los años sesenta, el gran protagonista", P("fiat600"))
c.at("Pero en Argentina había otro auto", P("falcon"))
c.at("Y entonces aparece un auto francés", P("r12"))
c.at("Y según un registro de ventas", stat("1984 – 1988", "Renault 12 · el más vendido de Argentina", "según las fuentes", count=False))
c.at("¿Por qué tuvo tanto éxito?", P("r12"))
c.at("Pero hay otro auto que no podemos olvidar", P("504"))
c.at("Y alcanzó el primer puesto", stat("9 veces", "Peugeot 504 · número uno en Argentina", "según las fuentes", count=False))
c.at("Fue el auto del médico", P("504"))
c.at("Y en los noventa", P("duna"))
c.at("Así que en Argentina no hubo un solo rey", P("falcon"))
c.at("Hay quien defiende al Renault 12", P("r12"))
c.at("Y hay quien nunca olvidará el Peugeot 504", P("504"))
chapters.append(c)

c = ch("ch04")
c.at(0, P("r4"))
c.at("En Colombia, hablar del auto más popular", photo("m_r4", 13, "in", cap="Renault 4|Colombia, desde 1970"))
c.at("Y lo más impresionante", P("r4"))
c.at("Pero el Renault 4 tuvo rivales", P("131"))
c.at("En los años ochenta, el gran duelo", P("sprint"))
c.at("Y luego estaba la familia Renault", P("r9"))
c.at("Y a finales de los ochenta llegó un japonés", photo("m_323", 4, "in", cap="Mazda 323|Colombia"))
c.at("Y hay un detalle importante", P("r4"))
c.at("Así que la historia de Colombia", P("323"))
chapters.append(c)

c = ch("ch05", 2.5)
c.at(0, P("seat600"))
c.at("El Vocho, un alemán hecho en México", P("vocho"))
c.at("El Renault 12 y el Peugeot 504", P("504"))
c.at("Y el Renault 4, un francés", P("r4"))
c.at("La segunda: todos eran autos sencillos", P("r12"))
c.at("Y hay otra coincidencia curiosa", P("seat127"))
c.at("Y la tercera: muchos de ellos duraron", P("vocho"))
c.at("Y ahora te pregunto a ti", P("falcon"))
c.at("Y si has llegado hasta aquí", cta("Gracias por llegar al final", "suscríbete y déjame tu opinión", tv=True, remote=True))
chapters.append(c)

CTX = ["vocho", "seat127", "vocho", "r12", "r4", "seat600"]
print(A.finish(chapters, "ES24_MAS_VENDIDOS.mp4", CTX, subtitles="ES24.ass"))
