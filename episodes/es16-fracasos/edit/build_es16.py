#!/usr/bin/env python3
"""ES16 Los coches que nadie quiso comprar. Race template.
    python3 build_es16.py <narration_dir> > episode.json   (run from the work folder)
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "engine"))
import aus_kit as A
from aus_kit import P, photo, rank, stat, say, cta, title, ch

PHOTOS = {
    "carab": ["m_carabela"], "ditella": ["m_ditella"], "autoar": ["m_autoar"], "cis": ["m_cisitalia"],
    "stude": ["m_studebaker"], "dart": ["m_dodgedart"], "authi": ["m_authi"], "vam": ["m_vam"],
    "just": ["m_justicialista"], "pegaso": ["m_pegaso"], "borg": ["m_borgward"], "fac": ["h_factory"],
    "mix": ["h_factory", "m_vam", "m_studebaker", "m_ditella"],
}
CLIPS = json.load(open(os.path.join(HERE, "clips.json")))
GENERIC = CLIPS.pop("_generic", [])
FALLBACK = {k: [] for k in PHOTOS}
FALLBACK.update({"autoar": ["cis"], "cis": ["autoar"], "mix": ["carab", "authi"]})
RES = ["m_borgward/1", "m_justicialista/11", "m_pegaso/5", "m_carabela/5", "m_ditella/2", "m_autoar/1", "m_studebaker/3",
       "m_dodgedart/4", "m_authi/2", "m_vam/7", "m_justicialista/1", "m_pegaso/11", "m_borgward/15"]
A.setup(sys.argv[1], os.path.join(HERE, "skip.json"), PHOTOS, CLIPS, GENERIC, FALLBACK, [], reserved=RES)
A.THEME = "race"
A.CLIP_TARGET = 0.0
A.MAX_HOLD, A.KEEP = 8.0, 5.5
A.ARCHIVE_OK = True
A.STRICT_POOLS = True
A.SPLIT_BY_SUBJECT = True
chapters = []

c = ch("ch00_hook", 0.6)
c.at(0, photo("m_borgward", 1, "in", cap="Borgward|Monterrey, 1967"))
c.at("En Argentina, el Estado", photo("m_justicialista", 11, "in", cap="IAME Justicialista|Argentina, 1953"))
c.at("Y en España, una empresa", photo("m_pegaso", 5, "in", cap="Pegaso Z-102|España, años 50"))
c.at("Fábricas enormes", P("borg"))
c.at("Y al final", say("Fracaso.", "FRACASO", 150))
c.at("Hoy vas a conocer", title("Nadie los quiso", "fracasos de Latinoamérica y España", "1951 – 1989", "mix"))
c.at("Y quédate hasta el final", P("borg"))
chapters.append(c)

c = ch("ch01")
c.at(0, P("mix"))
c.at("En México, por ejemplo", P("mix"))
c.at("Número diez", rank(10, "Kaiser Carabela", "m_carabela", 5, "Córdoba, Argentina · 1958", "un coche viejo desde el primer día"))
c.at("Pero tenía un problema serio", P("carab"))
c.at("Entre 1958 y 1961", stat("≈8.000", "Kaiser Carabela fabricados (1958 – 1961)", "según las fuentes", count=False))
c.at("Lo curioso es que la misma empresa", P("carab"))
c.at("Número nueve", rank(9, "Siam Di Tella 1500", "m_ditella", 2, "Argentina · 1960", "la empresa que se endeudó"))
c.at("Y entonces decidió dar el gran salto", P("ditella"))
c.at("Pero la aventura de los coches", P("ditella"))
chapters.append(c)

c = ch("ch02")
c.at(0, say("¿Desde dónde nos estás viendo?", "VIENDO", 120))
c.at("Y si todavía no estás suscrito", cta("Suscríbete", "historias de coches clásicos"))
c.at("Número ocho", rank(8, "Autoar", "m_autoar", 1, "Argentina · 1949", "el sueño italiano de Perón"))
c.at("Autoar fabricó vehículos utilitarios", P("cis"))
c.at("Número siete", rank(7, "Studebaker", "m_studebaker", 3, "Colombia · años 60", "ensamblados por Colmotores"))
c.at("Pero el proyecto tropezó", P("stude"))
c.at("Número seis", rank(6, "Barreiros · Dodge Dart", "m_dodgedart", 4, "Madrid · 1965", "las cuentas no salieron"))
c.at("En 1963 llegó a un acuerdo", P("dart"))
c.at("Pero las cuentas no salieron", P("dart"))
c.at("Número cinco", rank(5, "Authi", "m_authi", 2, "Pamplona · 1965 – 1975", "diez años y adiós"))
c.at("Pero el grupo británico", P("authi"))
chapters.append(c)

c = ch("ch03")
c.at(0, rank(4, "VAM", "m_vam", 7, "México", "el fabricante del Estado"))
c.at("Pero VAM nunca logró competir", P("vam"))
c.at("Número tres", rank(3, "IAME Justicialista", "m_justicialista", 1, "Argentina · 1953", "el coche de Perón"))
c.at("El proyecto era ambicioso", stat("178", "sedanes Justicialista fabricados (hasta 1955)", "Gustavo Feder", count=True))
c.at("Solo la camioneta", P("just"))
c.at("Y hubo incluso un Justicialista deportivo", P("just"))
chapters.append(c)

c = ch("ch04")
c.at(0, rank(2, "Pegaso Z-102", "m_pegaso", 11, "ENASA · 1951", "una obra de arte… y un mal negocio"))
c.at("Como coche, fue una obra de arte", stat("500.000 pts", "Pegaso Z-102 · un SEAT 600: ≈70.000", "según las fuentes", count=False))
c.at("Y aquí está la gran paradoja", P("pegaso"))
c.at("Número uno", rank(1, "Borgward México", "m_borgward", 15, "Nuevo León · 1967 – 1970", "una fábrica que duró tres años"))
c.at("Unos años después", P("borg"))
c.at("Pero el proyecto llegaba tarde", P("borg"))
c.at("El resultado fue un desastre", stat("2.267", "Borgward fabricados en México (1967 – 1970)", "Valdés y Garza Guajardo", count=True))
c.at("Hoy, los Borgward fabricados en México", P("borg"))
chapters.append(c)

c = ch("ch05", 2.5)
c.at(0, P("mix"))
c.at("Y hay una lección", P("mix"))
c.at("Y ahora te pregunto a ti", P("mix"))
c.at("Y si has llegado hasta aquí", cta("Gracias por llegar al final", "suscríbete y déjame tu opinión"))
chapters.append(c)

CTX = ["borg", "carab", "dart", "vam", "borg", "mix"]
print(A.finish(chapters, "ES16_FRACASOS.mp4", CTX, subtitles="ES16.ass"))
