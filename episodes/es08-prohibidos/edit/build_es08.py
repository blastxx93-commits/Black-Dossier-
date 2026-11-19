#!/usr/bin/env python3
"""ES08 Los 10 coches que hoy estarían prohibidos. Countdown list, theme "retro60".
    python3 build_es08.py <narration_dir> > episode.json   (run from the work folder)
Real material only (Replicate had no credit). Clips come from per-model Commons searches (v_*) when reviewed.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "engine"))
import aus_kit as A
from aus_kit import P, photo, rank, stat, say, cta, title, ch, questions

PHOTOS = {
    "bt46": ["m_bt46b", "h_lauda"], "lauda": ["h_lauda", "m_bt46b"], "anderstorp": ["h_anderstorp"],
    "r4": ["m_r4", "h_r4_interior"], "c2cv": ["m_2cv", "h_2cv_roof"],
    "bmw": ["m_2002turbo"], "cobra": ["m_cobra427"], "corvair": ["m_corvair"], "nader": ["h_nader"],
    "pinto": ["m_pinto"], "superbird": ["m_superbird"], "p917": ["m_porsche917", "h_lemans70"], "lemans": ["h_lemans70"],
    "chaparral": ["m_chaparral2j"], "amphi": ["m_amphicar"], "test": ["h_euroncap"],
    "old": ["m_r4", "m_2cv", "m_corvair", "m_pinto"], "fast": ["m_cobra427", "m_superbird", "m_porsche917", "m_2002turbo"],
}
CLIPS = json.load(open(os.path.join(HERE, "clips.json")))
GENERIC = CLIPS.pop("_generic", [])
FALLBACK = {k: ["fast"] for k in PHOTOS}
FALLBACK.update({"fast": ["old"], "old": ["fast"], "r4": ["c2cv", "old"], "c2cv": ["r4", "old"], "test": ["old"],
                 "corvair": ["nader", "old"], "nader": ["corvair"], "pinto": ["old"], "lauda": ["bt46"], "bt46": ["lauda", "fast"],
                 "anderstorp": ["bt46"], "lemans": ["p917"], "p917": ["lemans", "fast"], "chaparral": ["fast"], "amphi": ["old"]})
RES = ["m_bt46b/4", "m_r4/3", "m_2cv/2", "m_2002turbo/1", "m_cobra427/1", "m_corvair/2", "m_pinto/3", "m_superbird/4",
       "m_porsche917/2", "m_chaparral2j/2", "m_amphicar/4", "h_nader/1", "h_lemans70/1", "h_lauda/1", "m_bt46b/1"]
A.setup(sys.argv[1], os.path.join(HERE, "skip.json"), PHOTOS, CLIPS, GENERIC, FALLBACK, ["fast", "old"], reserved=RES)
A.THEME = "retro60"
A.CLIP_TARGET = 0.35
A.MAX_HOLD, A.KEEP = 11.0, 7.0
A.ARCHIVE_OK = True
A.SPLIT_BY_SUBJECT = True
chapters = []

c = ch("ch00_hook", 0.6)
c.at(0, photo("m_bt46b", 4, "in", cap="Anderstorp|17 de junio de 1978"))
c.at("Lleva en la parte de atrás un ventilador enorme", P("bt46"))
c.at("Dos horas después, ya no se ríen", say("Ganó. Y nunca volvió a correr.", "NUNCA", 120))
c.at("Pero antes hay nueve coches", P("fast"))
c.at("Un coche cuyo depósito", P("pinto"))
c.at("Otro que, según un abogado", P("corvair"))
c.at("Un deportivo tan rápido", P("p917"))
c.at("Y dos coches que fabricábamos aquí", P("r4"))
c.at("Hoy vas a conocer los diez coches", title("Hoy estarían prohibidos", "10 coches de los años 60 y 70", "1958 – 1978", "fast"))
questions(c, ["Un depósito que ardía", "Prohibido por ganar", "Dos coches españoles"],
          ["que hoy estarían prohibidos", "Y quédate hasta el final", "parece inventado"])
chapters.append(c)

c = ch("ch01")
c.at(0, P("test"))
c.at("Para que te hagas una idea", stat("1997", "primeras pruebas Euro NCAP", "Euro NCAP", count=False))
c.at("Número diez", rank(10, "Renault 4", "m_r4", 3, "FASA · Valladolid · 1964", "el «Cuatro Latas»"))
c.at("Valladolid, 1964", P("r4"))
c.at("La carrocería era de chapa fina", P("r4"))
c.at("Fue un coche maravilloso", P("r4"))
c.at("Número nueve", rank(9, "Citroën 2CV", "m_2cv", 2, "Vigo · desde 1958", "el «Dos Caballos»"))
c.at("El 2CV pesaba poco más de quinientos kilos", P("c2cv"))
c.at("Era un coche genial", P("c2cv"))
c.at("El último Dos Caballos", P("c2cv"))
c.at("Y ahora salimos de España", P("fast"))
chapters.append(c)

c = ch("ch02")
c.at(0, rank(8, "BMW 2002 Turbo", "m_2002turbo", 1, "Alemania · 1973", "el «turbo» escrito al revés"))
c.at("Pero lo que más llamó la atención", say("«TURBO» al revés, para leerlo por el retrovisor.", "RETROVISOR", 100))
c.at("La prensa alemana", P("bmw"))
c.at("Según las fuentes, BMW acabó quitando", stat("1.672", "BMW 2002 Turbo fabricados", "BMW", count=True))
c.at("Número siete", rank(7, "Shelby Cobra 427", "m_cobra427", 1, "EE. UU. · 1965", "siete litros sin protección"))
c.at("No tenía techo fijo", P("cobra"))
c.at("Hoy un Cobra 427 nuevo", P("cobra"))
chapters.append(c)

c = ch("ch03")
c.at(0, rank(6, "Chevrolet Corvair", "m_corvair", 2, "EE. UU. · 1960", "«Inseguro a cualquier velocidad»"))
c.at("En 1965, un joven abogado", photo("h_nader", 1, "in", cap="Ralph Nader"))
c.at("El libro fue un terremoto", P("corvair"))
c.at("En 1966, Estados Unidos aprobó", P("corvair"))
c.at("Y Ralph Nader se convirtió", P("nader"))
c.at("Número cinco", rank(5, "Ford Pinto", "m_pinto", 3, "EE. UU. · 1971", "el depósito que podía arder"))
c.at("Pero tenía un problema muy serio", P("pinto"))
c.at("Y aquí viene lo más polémico", P("pinto"))
c.at("En 1978, un jurado de California", stat("≈1.500.000", "Ford Pinto llamados a revisión · 1978", "NHTSA / Ford", count=False))
c.at("Antes de seguir", P("old"))
c.at("Y hasta aquí, coches peligrosos", say("Los prohibieron porque ganaban demasiado.", "GANABAN", 110))
chapters.append(c)

c = ch("ch04")
c.at(0, rank(4, "Plymouth Superbird", "m_superbird", 4, "EE. UU. · 1970", "el coche con alas"))
c.at("El resultado fue el Superbird", P("superbird"))
c.at("Para 1971, la NASCAR", P("superbird"))
c.at("Hoy, un morro puntiagudo", P("superbird"))
c.at("Número tres", rank(3, "Porsche 917", "m_porsche917", 2, "Le Mans · 1970", "expulsado de dos campeonatos"))
c.at("El 917 era tan dominante", photo("h_lemans70", 1, "in", cap="Porsche 917|Le Mans 1970"))
c.at("Y Porsche se lo llevó a América", P("p917"))
c.at("Allí volvió a arrasar", P("p917"))
chapters.append(c)

c = ch("ch05")
c.at(0, photo("m_amphicar", 4, "in", cap="Amphicar 770|Alemania, 1961"))
c.at("Se vendieron unos pocos miles", P("amphi"))
c.at("Hoy, un coche que tiene que ser a la vez barco", P("amphi"))
c.at("Número dos", rank(2, "Chaparral 2J", "m_chaparral2j", 2, "EE. UU. · 1970", "la primera aspiradora"))
c.at("Los ventiladores sacaban el aire", P("chaparral"))
c.at("Pero tenía problemas", P("chaparral"))
c.at("Pero la idea no murió", P("bt46"))
chapters.append(c)

c = ch("ch06", 2.5)
c.at(0, rank(1, "Brabham BT46B", "m_bt46b", 1, "Fórmula 1 · 1978", "el coche aspiradora"))
c.at("Volvemos al principio", P("anderstorp"))
c.at("El piloto era Niki Lauda", photo("h_lauda", 1, "in", cap="Niki Lauda|Brabham BT46B"))
c.at("Lauda ganó la carrera", say("Una carrera. Una victoria. Retirado.", "RETIRADO", 120))
c.at("Lo más curioso es que", P("bt46"))
c.at("Piénsalo", P("bt46"))
c.at("Así que ya lo ves", P("fast"))
c.at("Y ahora te pregunto a ti", P("old"))
c.at("Y si te ha gustado el vídeo", cta("Suscríbete", "historias de coches clásicos"))
chapters.append(c)

CTX = ["fast", "r4", "bmw", "corvair", "superbird", "chaparral", "bt46"]
print(A.finish(chapters, "ES08_PROHIBIDOS.mp4", CTX, subtitles="ES08.ass"))
