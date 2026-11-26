#!/usr/bin/env python3
"""ES18 El último Vocho del mundo se hizo en México. Race template.
    python3 build_es18.py <narration_dir> > episode.json   (run from the work folder)
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "engine"))
import aus_kit as A
from aus_kit import P, photo, stat, say, cta, title, ch

PHOTOS = {"vocho": ["m_vocho"], "taxi": ["m_vochotaxi"], "ult": ["m_ultima"], "b50": ["m_beetle50"],
          "motor": ["m_beetlemotor"], "mix": ["m_vocho", "m_beetle50"]}
CLIPS = json.load(open(os.path.join(HERE, "clips.json")))
GENERIC = CLIPS.pop("_generic", [])
FALLBACK = {k: [] for k in PHOTOS}
FALLBACK.update({"ult": ["vocho"], "taxi": ["vocho"], "motor": ["b50"], "b50": ["vocho"], "vocho": ["ult", "taxi", "b50"]})
RES = ["m_ultima/2_openverse.jpg", "m_vochotaxi/10_openverse.jpg", "m_beetle50/11_commons.jpg", "m_ultima/4_openverse.jpg"]
A.setup(sys.argv[1], os.path.join(HERE, "skip.json"), PHOTOS, CLIPS, GENERIC, FALLBACK, [], reserved=[r.rsplit("_", 1)[0] for r in RES])
A.THEME = "race"
A.CLIP_TARGET = 0.0
A.MAX_HOLD, A.KEEP = 16.0, 11.0
A.ARCHIVE_OK = True
A.STRICT_POOLS = True
A.SPLIT_BY_SUBJECT = True
chapters = []

c = ch("ch00_hook", 0.6)
c.at(0, photo("m_ultima", 2, "in", cap="Volkswagen Sedán|Puebla, 30 de julio de 2003"))
c.at("Durante casi setenta años", photo("m_beetle50", 11, "in", cap="Volkswagen|años 50"))
c.at("Pero al final, el último país", P("vocho"))
c.at("Hoy vas a conocer", title("El último Vocho", "la historia del auto más mexicano", "1954 – 2003", "vocho"))
c.at("Por qué todo México", P("taxi"))
c.at("Y por qué, cuando el resto", P("ult"))
chapters.append(c)

c = ch("ch01")
c.at(0, P("b50"))
c.at("Su diseño era único", P("motor"))
c.at("Después de la Segunda Guerra Mundial", P("b50"))
c.at("Para entender cómo llegó a México", P("vocho"))
c.at("Según las fuentes, una de las primeras", stat("1954", "los primeros Volkswagen en México", "según las fuentes", count=False))
c.at("Durante esos primeros años", P("b50"))
c.at("Pero las cosas cambiaron muy rápido", P("vocho"))
c.at("En mil novecientos sesenta y dos", stat("1962", "planta de ensamblaje en Xalostoc", "según las fuentes", count=False))
c.at("Pero Xalostoc se quedaba pequeña", P("vocho"))
c.at("La construcción de la planta de Puebla", stat("23 · 10 · 1967", "primer Vocho fabricado en Puebla", "según las fuentes", count=False))
c.at("Nadie lo sabía entonces", P("vocho"))
chapters.append(c)

c = ch("ch02")
c.at(0, say("¿Desde dónde nos estás viendo?", "VIENDO", 120))
c.at("Y si todavía no estás suscrito", cta("Suscríbete", "historias de autos clásicos", tv=True))
c.at("En España lo llamaban", say("«Vocho»", "VOCHO", 200))
c.at("¿Por qué tuvo tanto éxito", P("vocho"))
c.at("Su motor estaba refrigerado", P("motor"))
c.at("Las piezas eran baratas", P("vocho"))
c.at("Por eso el Vocho se convirtió", P("vocho"))
c.at("Mientras tanto, en el resto del mundo", stat("≈1.300.000", "escarabajos fabricados en 1971 (récord mundial)", "según las fuentes", count=False))
c.at("Pero en México, el Vocho estaba", P("taxi"))
chapters.append(c)

c = ch("ch03")
c.at(0, P("taxi"))
c.at("La respuesta fue el Vocho", photo("m_vochotaxi", 10, "in", cap="Taxi vocho|Ciudad de México"))
c.at("Para hacerlo más cómodo", P("taxi"))
c.at("Con los años, los taxis vocho", P("taxi"))
c.at("Y fuera de la capital", P("vocho"))
c.at("Mientras tanto, en Europa", P("b50"))
c.at("Pero México no lo dejó", stat("1978 – 1985", "Vochos de Puebla exportados a Europa", "Motorpasión", count=False))
c.at("Piénsalo un momento", P("b50"))
c.at("Según las fuentes, a partir de mediados", P("vocho"))
c.at("Un auto alemán", P("vocho"))
chapters.append(c)

c = ch("ch04")
c.at(0, P("vocho"))
c.at("Volkswagen intentó mantenerlo", P("motor"))
c.at("Pero no era suficiente", stat("≈30.000", "Vochos al año hacia 2003", "según algunas fuentes", count=False))
c.at("Así que Volkswagen tomó una decisión", stat("3.000", "unidades de la Última Edición", "Volkswagen", count=True))
c.at("La Última Edición venía", P("ult"))
c.at("Y entonces llegó el día", photo("m_ultima", 4, "in", cap="Último Sedán del mundo|30 de julio de 2003"))
c.at("La despedida fue emocionante", P("ult"))
c.at("Ese último Vocho no se vendió", P("ult"))
c.at("En total, según las fuentes", stat("≈1.700.000", "Vochos fabricados en México", "según las fuentes", count=False))
chapters.append(c)

c = ch("ch05", 2.5)
c.at(0, P("taxi"))
c.at("Fue el final de una época", P("vocho"))
c.at("¿Por qué el Vocho significó", P("vocho"))
c.at("Y hay un dato que lo resume", stat("36 años", "fabricando el Vocho en Puebla (1967 – 2003)", "según las fuentes", count=False))
c.at("Un auto que nació en Alemania", P("vocho"))
c.at("Y ahora te pregunto a ti", P("taxi"))
c.at("Y si has llegado hasta aquí", cta("Gracias por llegar al final", "suscríbete y déjame tu opinión", tv=True, remote=True))
chapters.append(c)

CTX = ["ult", "vocho", "vocho", "taxi", "ult", "vocho"]
print(A.finish(chapters, "ES18_ULTIMO_VOCHO.mp4", CTX, subtitles="ES18.ass"))
