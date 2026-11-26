#!/usr/bin/env python3
"""ES20 Los 7 autos de Pablo Escobar. Race template. Regra 26/11: imagem = narração (sem pools mix).
    python3 build_es20.py <narration_dir> > episode.json   (run from the work folder)
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "engine"))
import aus_kit as A
from aus_kit import P, photo, rank, stat, say, cta, title, ch

PHOTOS = {"r4": ["m_r4", "m_r4b"], "r4c": ["m_r4copa"], "toca": ["m_tocancipa"], "med": ["m_medellin"], "rsr": ["m_rsr"],
          "935": ["m_935"], "356": ["m_356"], "nap": ["m_napoles", "m_napoles2"], "hipo": ["m_hipo"], "bonnie": ["m_bonnie"],
          "ford36": ["m_ford36"], "cad": ["m_cadillac30"], "sl": ["m_300sl"], "600": ["m_600"]}
CLIPS = json.load(open(os.path.join(HERE, "clips.json")))
GENERIC = CLIPS.pop("_generic", [])
FALLBACK = {k: [] for k in PHOTOS}
FALLBACK.update({"r4c": ["r4"], "toca": ["r4c", "r4"], "hipo": ["nap"], "bonnie": ["ford36"], "med": ["nap"], "rsr": ["935"], "935": ["rsr"]})
RES = ["m_napoles/6", "m_napoles/1", "m_r4/13", "m_rsr/4", "m_356/11", "m_ford36/2", "m_cadillac30/12", "m_300sl/10", "m_600/4", "m_napoles/13"]
A.setup(sys.argv[1], os.path.join(HERE, "skip.json"), PHOTOS, CLIPS, GENERIC, FALLBACK, [], reserved=RES)
A.THEME = "race"
A.CLIP_TARGET = 0.0
A.MAX_HOLD, A.KEEP = 16.0, 11.0
A.ARCHIVE_OK = True
A.STRICT_POOLS = True
A.SPLIT_BY_SUBJECT = True
chapters = []

c = ch("ch00_hook", 0.6)
c.at(0, photo("m_napoles", 6, "in", cap="Hacienda Nápoles|Puerto Triunfo, Antioquia"))
c.at("Su dueño les contaba", P("bonnie"))
c.at("Pero era mentira", P("ford36"))
c.at("El dueño de ese auto era Pablo Escobar", photo("m_napoles", 1, "in", cap="Hacienda Nápoles|la finca de Escobar"))
c.at("Hoy vas a conocer", title("Los autos de Escobar", "y lo que pasó con ellos", "Colombia · 1970 – 1993", "rsr"))
c.at("Desde el humilde Renault 4", P("r4"))
c.at("hasta el Porsche de carreras", P("rsr"))
c.at("Una advertencia antes de empezar", P("cad"))
chapters.append(c)

c = ch("ch01")
c.at(0, P("med"))
c.at("Número siete. El Renault 4", rank(7, "Renault 4", "m_r4", 13, "Colombia · años 70", "su primer auto"))
c.at("Según varias fuentes, el primer vehículo", P("r4"))
c.at("Pero Escobar no lo usaba", P("r4"))
c.at("Y el Renault 4 volvería", P("r4c"))
c.at("En febrero de mil novecientos setenta y nueve", P("toca"))
c.at("Allí se enfrentaban decenas", P("r4c"))
c.at("Las fuentes no se ponen de acuerdo", P("toca"))
c.at("Pero a Escobar el Renault 4", P("r4"))
chapters.append(c)

c = ch("ch02")
c.at(0, say("¿Desde dónde nos estás viendo?", "VIENDO", 120))
c.at("Y si todavía no estás suscrito", cta("Suscríbete", "historias de autos clásicos", tv=True))
c.at("Número seis. El Porsche 911 RSR", P("rsr"))
c.at("Este es, sin duda", rank(6, "Porsche 911 RSR", "m_rsr", 4, "IROC · 1974", "su auto de carreras"))
c.at("En mil novecientos setenta y cuatro, en Estados Unidos", stat("15", "Porsche 911 RSR para la IROC (1974)", "según las fuentes", count=True))
c.at("Los pilotos venían de todas partes", P("rsr"))
c.at("Y entonces, según las fuentes, Tunstall", P("rsr"))
c.at("Escobar llevó el Porsche a Colombia", P("935"))
c.at("El 935 era una bestia", P("935"))
c.at("Así que Escobar quería", P("rsr"))
c.at("Allí, según cuentan algunos relatos", P("rsr"))
chapters.append(c)

c = ch("ch03")
c.at(0, P("rsr"))
c.at("Después de Escobar, el auto siguió", P("rsr"))
c.at("Más tarde, el Porsche salió del país", P("rsr"))
c.at("En dos mil veintiuno", stat("≈2.200.000 US$", "precio pedido por el Porsche (2021)", "según las fuentes", count=False))
c.at("Para muchos coleccionistas", P("rsr"))
c.at("Número cinco. El Porsche 356", rank(5, "Porsche 356", "m_356", 11, "años 50 · 60", "el primer Porsche"))
c.at("Pero este Porsche no tuvo", P("356"))
c.at("Y lo que queda de él", P("nap"))
c.at("La Hacienda Nápoles estaba", P("nap"))
c.at("e hipopótamos", P("hipo"))
c.at("Y en la entrada, encima", P("nap"))
c.at("En esa finca, Escobar guardaba", P("nap"))
chapters.append(c)

c = ch("ch04")
c.at(0, rank(4, "Bonnie y Clyde", "m_ford36", 2, "Hacienda Nápoles", "el auto falso"))
c.at("Es la historia con la que empezamos", P("bonnie"))
c.at("Pero según las fuentes, era falso", P("bonnie"))
c.at("Y el de Escobar, según el relato", P("ford36"))
c.at("¿Y los agujeros de bala?", P("ford36"))
c.at("Número tres. El Cadillac", rank(3, "Cadillac años 30", "m_cadillac30", 12, "¿de Al Capone?", "no confirmado"))
c.at("Con este auto pasa algo parecido", P("cad"))
c.at("¿Es verdad? No está confirmado", P("cad"))
c.at("Número dos. El Mercedes-Benz 300 SL", rank(2, "Mercedes-Benz 300 SL", "m_300sl", 10, "años 50", "las alas de gaviota"))
c.at("Este sí era un auto de lujo", P("sl"))
c.at("Se fabricó a mediados", stat("≈1.400", "300 SL coupé «alas de gaviota»", "según las fuentes", count=False))
c.at("Tenía un motor de seis cilindros", P("sl"))
c.at("Según varias fuentes, Escobar tuvo uno", P("sl"))
chapters.append(c)

c = ch("ch05", 2.5)
c.at(0, rank(1, "Mercedes-Benz 600 Pullman", "m_600", 4, "1963 – 1981", "la limusina del poder"))
c.at("Si había un auto que representaba", P("600"))
c.at("Se fabricó entre mil novecientos sesenta y tres", P("600"))
c.at("Pero su final fue el más dramático", photo("m_napoles", 13, "in", cap="Hacienda Nápoles|restos de los autos de Escobar"))
c.at("Lo que quedó del Mercedes", P("nap"))
c.at("¿Y qué es hoy la Hacienda Nápoles?", P("nap"))
c.at("Así terminó la colección", P("rsr"))
c.at("Y ahora te pregunto a ti", P("nap"))
c.at("Y si has llegado hasta aquí", cta("Gracias por llegar al final", "suscríbete y déjame tu opinión", tv=True, remote=True))
chapters.append(c)

CTX = ["nap", "r4", "rsr", "nap", "ford36", "nap"]
print(A.finish(chapters, "ES20_ESCOBAR.mp4", CTX, subtitles="ES20.ass"))
