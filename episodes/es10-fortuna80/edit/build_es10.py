#!/usr/bin/env python3
"""ES10 Coches de los 80 que hoy valen una fortuna. Countdown list; rendered with the Race template (engine/hf_race.py).
    python3 build_es10.py <narration_dir> > episode.json   (run from the work folder)
Real photos only.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "engine"))
import aus_kit as A
from aus_kit import P, photo, rank, stat, say, cta, title, ch, questions

PHOTOS = {
    "golf": ["m_golfgti"], "p205": ["m_205gti"], "copa": ["m_r5copa"], "s5": ["m_supercinco"], "fasa": ["h_fasa"],
    "r5t2": ["m_r5turbo2"], "sierra": ["m_sierracos"], "rs500": ["m_rs500"], "m3": ["m_m3e30"], "delta": ["m_integrale"],
    "evo": ["m_190evo"], "f40": ["m_f40"], "f40lm": ["m_f40lm"], "count": ["m_countach"], "quattro": ["m_quattro"],
    "dmc": ["m_delorean"], "auction": ["h_auction"], "maranello": ["h_maranello"],
    "eighties": ["m_golfgti", "m_205gti", "h_auction"],
}
CLIPS = json.load(open(os.path.join(HERE, "clips.json")))
GENERIC = CLIPS.pop("_generic", [])
FALLBACK = {k: ["eighties"] for k in PHOTOS}
FALLBACK.update({"eighties": ["f40"], "copa": ["s5", "r5t2"], "s5": ["copa", "r5t2"], "fasa": ["s5", "copa"],
                 "r5t2": ["copa", "s5"], "sierra": ["rs500", "auction"], "rs500": ["sierra", "auction"], "evo": ["auction", "delta"], "delta": ["auction"], "m3": ["auction"], "f40": ["f40lm", "maranello"],
                 "f40lm": ["f40"], "maranello": ["f40"], "auction": ["eighties"]})
RES = ["m_f40/1", "m_golfgti/7", "m_205gti/3", "m_supercinco/7", "m_r5copa/7", "m_r5turbo2/3", "m_sierracos/3", "m_m3e30/4",
       "m_integrale/1", "m_190evo/2", "m_rs500/3", "m_countach/1", "m_quattro/4", "m_delorean/2", "m_f40lm/3", "h_maranello/4"]
A.setup(sys.argv[1], os.path.join(HERE, "skip.json"), PHOTOS, CLIPS, GENERIC, FALLBACK, ["eighties", "f40"], reserved=RES)
A.THEME = "revista"
A.CLIP_TARGET = 0.0
A.MAX_HOLD, A.KEEP = 10.0, 7.0
A.ARCHIVE_OK = True
A.SPLIT_BY_SUBJECT = True
chapters = []

c = ch("ch00_hook", 0.6)
c.at(0, photo("m_f40", 1, "in", cap="Maranello|1987"))
c.at("Hoy, ese mismo coche", stat("+3.000.000 $", "Ferrari F40 en subasta", "RM Sotheby's", count=False))
c.at("No es el único", P("eighties"))
c.at("coches que se vendían en cualquier concesionario", P("s5"))
c.at("Hoy vas a conocer diez coches", title("Hoy valen una fortuna", "10 coches de los años 80", "1976 – 1990", "eighties"))
questions(c, ["Fabricado en Valladolid", "Una berlina de 590.000 $", "El coche más deseado"],
          ["Dos de ellos se vendían", "Uno se vendió en subasta", "Y el número uno"])
c.at("Y una advertencia antes de empezar", P("auction"))
chapters.append(c)

c = ch("ch01")
c.at(0, P("eighties"))
c.at("A eso se suma algo más", P("eighties"))
c.at("Número diez", rank(10, "Volkswagen Golf GTI", "m_golfgti", 7, "Alemania · 1976", "el primer GTI"))
c.at("Nadie esperaba gran cosa", P("golf"))
c.at("Durante los años ochenta", stat("≈19.000 €", "Golf GTI I en buen estado · anuncios en España", "coches.net", count=False))
c.at("Número nueve", rank(9, "Peugeot 205 GTI", "m_205gti", 3, "Francia · 1984", "el más divertido… y traicionero"))
c.at("Además, el 205 tenía la mejor publicidad", P("p205"))
c.at("Ligero, ágil", P("p205"))
c.at("Si en los noventa podías comprar", stat("20.000 – 30.000 €", "205 GTI 1.9 · anuncios en España", "coches.net", count=False))
chapters.append(c)

c = ch("ch02")
c.at(0, rank(8, "R5 Copa Turbo · GT Turbo", "m_supercinco", 7, "FASA · Valladolid", "los nuestros"))
c.at("Se fabricaba en Valladolid", P("fasa"))
c.at("Primero llegó el Renault 5 Copa Turbo", photo("m_r5copa", 7, "in", cap="Renault 5 Copa Turbo|España, 1982 – 1984"))
c.at("Después, en 1985, llegó el Supercinco", P("s5"))
c.at("El Supercinco GT Turbo pesaba muy poco", P("s5"))
c.at("Hoy encontrar uno bueno es complicado", stat("8.000 – 30.000 €", "Supercinco GT Turbo · subasta y anuncios", "Motor1", count=False))
c.at("Si en tu familia hubo", P("copa"))
c.at("Número siete", rank(7, "Renault 5 Turbo 2", "m_r5turbo2", 3, "Francia · 1983", "el R5 que fue al gimnasio"))
c.at("Para homologarlo", P("r5t2"))
c.at("Hoy, un Renault 5 Turbo 2", stat("+100.000 €", "Renault 5 Turbo 2 en buen estado", "Motor1", count=False))
chapters.append(c)

c = ch("ch03")
c.at(0, rank(6, "Ford Sierra RS Cosworth", "m_sierracos", 3, "Reino Unido · 1986", "la «cola de ballena»"))
c.at("El Sierra Cosworth fue el coche", P("sierra"))
c.at("Pero eso no es lo más sorprendente", P("rs500"))
c.at("Número cinco", rank(5, "BMW M3", "m_m3e30", 4, "Alemania · 1986", "nacido para las carreras"))
c.at("En los circuitos fue imbatible", P("m3"))
c.at("Durante años, los M3", stat("≈65.000 – 70.000 $", "BMW M3 E30 en buen estado", "Hagerty", count=False))
c.at("Antes de seguir, una pregunta rápida", say("¿Cuál crees que es el número uno?", "NÚMERO UNO", 110))
c.at("Y ahora llegamos a los cuatro primeros", P("eighties"))
chapters.append(c)

c = ch("ch04")
c.at(0, rank(4, "Lancia Delta Integrale", "m_integrale", 1, "Italia · 1987 – 1992", "seis títulos mundiales"))
c.at("Con el Delta, Lancia ganó seis", stat("6", "títulos mundiales de marcas seguidos", "FIA", count=True))
c.at("Hoy el Integrale es uno de los clásicos", stat("+130.000 $", "Integrale Evo 2 en subasta", "Hagerty", count=False))
c.at("Número tres", rank(3, "Mercedes 190 E Evo II", "m_190evo", 2, "Alemania · 1990", "la berlina con alerón de carreras"))
c.at("Se fabricaron solo quinientas", stat("500", "unidades de calle del Evolution II", "Mercedes-Benz", count=True))
c.at("Hoy ya nadie se ríe", P("evo"))
chapters.append(c)

c = ch("ch05")
c.at(0, rank(2, "Ford Sierra RS500", "m_rs500", 3, "Reino Unido · 1987", "500 unidades"))
c.at("El resultado fue el RS500", P("rs500"))
c.at("Y aquí viene la cifra que da vértigo", stat("590.500 $", "Ford Sierra RS500 · récord en subasta", "según la fuente", count=False))
c.at("Si alguien te hubiera dicho", P("sierra"))
chapters.append(c)

c = ch("ch06", 2.5)
c.at(0, photo("m_countach", 1, "in", cap="Lamborghini Countach"))
c.at("El Audi Quattro", photo("m_quattro", 4, "in", cap="Audi Quattro"))
c.at("Y el DeLorean", photo("m_delorean", 2, "in", cap="DeLorean DMC-12"))
c.at("Y ahora sí", rank(1, "Ferrari F40", "m_f40", 3, "Italia · 1987", "el último Ferrari de Enzo"))
c.at("Maranello, Italia, 1987", P("maranello"))
c.at("No tenía nada que sobrara", P("f40"))
c.at("El F40 fue, además", P("f40"))
c.at("Ferrari pensaba fabricar", P("f40"))
c.at("Hoy, un F40 normal", stat("≈3.900.000 $", "Ferrari F40 · Abu Dabi, 2025", "RM Sotheby's", count=False))
c.at("Y la versión de carreras", photo("m_f40lm", 3, "in", cap="Ferrari F40 LM|+11.000.000 $"))
c.at("Piénsalo", say("Lo que costaba una casa… hoy cuesta un edificio.", "EDIFICIO", 100))
c.at("Así que ya lo sabes", P("eighties"))
c.at("Y si te ha gustado el vídeo", cta("Suscríbete", "historias de coches clásicos"))
chapters.append(c)

CTX = ["eighties", "golf", "s5", "sierra", "delta", "rs500", "f40"]
print(A.finish(chapters, "ES10_FORTUNA80.mp4", CTX, subtitles="ES10.ass"))
