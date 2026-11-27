#!/usr/bin/env python3
"""ES21 Por qué estos autos nunca morían. Race template. Regra: imagem = narração."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "engine"))
import aus_kit as A
from aus_kit import P, photo, rank, stat, say, cta, title, ch

PHOTOS = {"taxi": ["m_w123taxi"], "w123": ["m_w123"], "mus": ["m_w123mus"], "2cv": ["m_2cv"], "2cvm": ["m_2cvmotor"],
          "600": ["m_600", "m_600b"], "404": ["m_404"], "falcon": ["m_falcon", "m_falconmotor"], "r4": ["m_r4"],
          "r4d": ["m_r4dash"], "vocho": ["m_vocho"], "vwm": ["m_vwmotor"]}
CLIPS = json.load(open(os.path.join(HERE, "clips.json")))
GENERIC = CLIPS.pop("_generic", [])
FALLBACK = {k: [] for k in PHOTOS}
FALLBACK.update({"taxi": ["w123"], "w123": ["taxi"], "mus": ["w123"], "2cvm": ["2cv"], "r4d": ["r4"], "vwm": ["vocho"]})
RES = ["m_w123taxi/11", "m_2cv/13", "m_600b/2", "m_404/1", "m_falcon/13", "m_w123/1", "m_r4/10", "m_vocho/1"]
A.setup(sys.argv[1], os.path.join(HERE, "skip.json"), PHOTOS, CLIPS, GENERIC, FALLBACK, [], reserved=RES)
A.THEME = "race"; A.CLIP_TARGET = 0.0; A.MAX_HOLD, A.KEEP = 12.0, 8.0
A.ARCHIVE_OK = True; A.STRICT_POOLS = True; A.SPLIT_BY_SUBJECT = True
chapters = []

c = ch("ch00_hook", 0.6)
c.at(0, photo("m_w123taxi", 11, "in", cap="Mercedes-Benz diésel|taxi"))
c.at("Siete millones. Es como", stat("+7.000.000 km", "taxi Mercedes de Gran Canaria", "según las fuentes", count=False))
c.at("Y no es el único", P("falcon"))
c.at("Hoy los autos tienen pantallas", P("vocho"))
c.at("Hoy vas a conocer", title("Nunca morían", "los secretos de los autos inmortales", "1948 – 2003", "r4"))
c.at("Y vas a descubrir, pieza por pieza", P("vwm"))
chapters.append(c)

c = ch("ch01")
c.at(0, P("vwm"))
c.at("Número siete. El Citroën Dos Caballos", rank(7, "Citroën 2CV", "m_2cv", 13, "1948 – 1990", "el paraguas con ruedas"))
c.at("En Francia lo llamaban", P("2cv"))
c.at("¿Cuál era su secreto? La sencillez", P("2cvm"))
c.at("Su suspensión era muy blanda", P("2cv"))
c.at("Y además, casi todo se podía desmontar", P("2cv"))
c.at("Y tenía otra ventaja", P("2cv"))
c.at("Número seis. El Fiat 600", rank(6, "Fiat 600", "m_600b", 2, "Argentina · España", "el «Fitito» y el Seiscientos"))
c.at("En España fue el Seiscientos", P("600"))
c.at("Su secreto era otro", P("600"))
c.at("El motor iba atrás", P("600"))
chapters.append(c)

c = ch("ch02")
c.at(0, say("¿Desde dónde nos estás viendo?", "VIENDO", 120))
c.at("Y si todavía no estás suscrito", cta("Suscríbete", "historias de autos clásicos", tv=True))
c.at("Número cinco. El Peugeot 404", P("404"))
c.at("Si hay un auto que se ganó fama", rank(5, "Peugeot 404", "m_404", 1, "Argentina · 1962 – 1980", "el indestructible"))
c.at("¿Cuál era su secreto? Una construcción", P("404"))
c.at("Además, el 404 fue uno", P("404"))
c.at("Número cuatro. El Ford Falcon", rank(4, "Ford Falcon", "m_falcon", 13, "Argentina · 1962 – 1991", "30 años sin cambiar"))
c.at("Este es un caso único", stat("494.209", "Ford Falcon fabricados en Argentina", "según las fuentes", count=True))
c.at("Treinta años casi sin cambiar", P("falcon"))
c.at("¿Y su secreto? Su motor de seis", P("falcon"))
c.at("Y hay otro dato clave", stat("98 %", "piezas argentinas al final de su producción", "según las fuentes", count=False))
c.at("Además, el Falcon tenía", P("falcon"))
chapters.append(c)

c = ch("ch03")
c.at(0, rank(3, "Mercedes-Benz diésel", "m_w123", 1, "años 70 · 80", "el taxi eterno"))
c.at("Volvamos al taxi de Gran Canaria", P("taxi"))
c.at("Y hay otro Mercedes igual de famoso", P("mus"))
c.at("¿Cuál era el secreto de este Mercedes?", P("w123"))
c.at("Por eso, durante décadas", P("taxi"))
c.at("Número dos. El Renault 4", rank(2, "Renault 4", "m_r4", 10, "1961 – 1992", "el amigo fiel"))
c.at("El «amigo fiel» de Colombia", stat("+8.130.000", "Renault 4 fabricados en el mundo", "según las fuentes", count=False))
c.at("¿Su secreto?", P("r4"))
c.at("Y tenía un detalle muy curioso", P("r4d"))
c.at("Además, era ligero", P("r4"))
chapters.append(c)

c = ch("ch04")
c.at(0, rank(1, "Volkswagen Sedán", "m_vocho", 1, "1938 – 2003", "el rey de todos"))
c.at("Y en el primer lugar", stat("+21.500.000", "escarabajos fabricados en el mundo", "según las fuentes", count=False))
c.at("¿Por qué duraba tanto?", P("vwm"))
c.at("Pero su mayor secreto era otro", P("vwm"))
c.at("Y fue el gran taxi", P("vocho"))
c.at("Y ahora que conoces los siete autos", P("vocho"))
c.at("El primer secreto: la sencillez", P("2cvm"))
c.at("El segundo secreto: motores", P("falcon"))
chapters.append(c)

c = ch("ch05", 2.5)
c.at(0, P("falcon"))
c.at("el Renault 4 en Colombia", P("r4"))
c.at("el Vocho en México", P("vocho"))
c.at("el Seiscientos en España", P("600"))
c.at("El cuarto secreto: los mecánicos", P("vwm"))
c.at("Y el quinto secreto", P("404"))
c.at("Pero ojo: no todo era perfecto", P("2cv"))
c.at("Entonces, ¿los autos de hoy son peores?", P("taxi"))
c.at("Por eso, todavía hoy", P("vocho"))
c.at("Y ahora te pregunto a ti", P("r4"))
c.at("Y si has llegado hasta aquí", cta("Gracias por llegar al final", "suscríbete y déjame tu opinión", tv=True, remote=True))
chapters.append(c)

CTX = ["taxi", "2cv", "404", "w123", "vocho", "falcon"]
print(A.finish(chapters, "ES21_NUNCA_MORIAN.mp4", CTX, subtitles="ES21.ass"))
