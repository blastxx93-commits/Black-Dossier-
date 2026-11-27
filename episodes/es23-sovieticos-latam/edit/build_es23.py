#!/usr/bin/env python3
"""ES23 Los autos soviéticos de Latinoamérica. Race template. Regra: imagem = narração."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "engine"))
import aus_kit as A
from aus_kit import P, V, photo, rank, stat, say, cta, title, ch

PHOTOS = {"ladacuba": ["m_ladacuba"], "lada": ["m_lada"], "laika": ["m_laika"], "fiat": ["m_fiat124"], "vaz": ["m_togliatti"],
          "mosk": ["m_moskvich"], "volga": ["m_volga"], "polski": ["m_polski"], "niva": ["m_niva"], "samara": ["m_samara"],
          "habana": ["m_habana"]}
CLIPS = json.load(open(os.path.join(HERE, "clips.json")))
GENERIC = CLIPS.pop("_generic", [])
FALLBACK = {k: [] for k in PHOTOS}
FALLBACK.update({"ladacuba": ["lada", "laika"], "lada": ["laika"], "laika": ["lada"], "fiat": ["lada"], "vaz": ["lada"], "samara": ["niva"], "niva": ["lada"]})
RES = ["m_fiat124/2", "m_lada/1", "m_togliatti/3", "m_volga/12", "m_polski/2", "m_niva/12", "m_samara/6"]
A.setup(sys.argv[1], os.path.join(HERE, "skip.json"), PHOTOS, CLIPS, GENERIC, FALLBACK, [], reserved=RES)
A.THEME = "race"; A.CLIP_TARGET = 0.0; A.MAX_HOLD, A.KEEP = 18.0, 12.0
A.ARCHIVE_OK = True; A.STRICT_POOLS = True; A.SPLIT_BY_SUBJECT = True
chapters = []

c = ch("ch00_hook", 0.6)
c.at(0, P("habana"))
c.at("Es cuadrado, sencillo", P("ladacuba", cap="Lada|La Habana"))
c.at("Es un Lada", P("ladacuba"))
c.at("Pero la historia de los autos soviéticos", P("lada"))
c.at("En algunos países fueron líderes", P("samara"))
c.at("Hoy vas a conocer", title("Autos soviéticos", "en Latinoamérica", "1970 – 1991", "lada"))
c.at("Qué eran, por qué llegaron", P("ladacuba"))
chapters.append(c)

c = ch("ch01")
c.at(0, P("lada"))
c.at("Pero el Lada… en realidad era italiano", photo("m_fiat124", 2, "in", cap="Fiat 124|Italia, 1966"))
c.at("A finales de los años sesenta", photo("m_togliatti", 3, "in", cap="AvtoVAZ|Togliatti"))
c.at("Para hacerlo, firmó un acuerdo", P("fiat"))
c.at("El auto elegido fue el Fiat 124", P("fiat"))
c.at("Lo reforzaron para soportar", P("lada"))
c.at("Según las fuentes rusas", photo("m_lada", 1, "in", cap="Lada / Zhiguli|1970"))
c.at("Y hay un detalle curioso", P("vaz"))
c.at("Fue un éxito enorme", stat("≈4.800.000", "Lada del primer modelo y variantes (1970 – 1988)", "según las fuentes", count=False))
c.at("Y no fue el único auto soviético", P("mosk"))
c.at("Y estaba el Volga", P("volga"))
c.at("En la Unión Soviética, el auto que tenías", P("lada"))
c.at("Y hay otra cosa que explica", P("vaz"))
c.at("Y a miles de kilómetros de Moscú", P("habana"))
chapters.append(c)

c = ch("ch02")
c.at(0, say("¿Desde dónde nos estás viendo?", "VIENDO", 120))
c.at("Y si todavía no estás suscrito", cta("Suscríbete", "historias de autos clásicos", tv=True))
c.at("Después de la revolución", P("habana"))
c.at("Según los especialistas, los primeros Lada", P("ladacuba"))
c.at("Pero en Cuba no se compraba", P("ladacuba"))
c.at("Esto creó una situación muy particular", P("habana"))
c.at("Tener un Lada en la Cuba", P("ladacuba"))
c.at("Los modelos más comunes", P("ladacuba"))
chapters.append(c)

c = ch("ch03")
c.at(0, P("mosk"))
c.at("El Moskvitch fue el otro gran auto", photo("m_moskvich", 12, "in", cap="Moskvitch|Moscú"))
c.at("Luego estaba el Volga", photo("m_volga", 12, "in", cap="Volga|GAZ"))
c.at("En los países socialistas era sinónimo", P("volga"))
c.at("Y había un auto que los cubanos recuerdan", photo("m_polski", 2, "in", cap="Polski Fiat 126|el «polaquito»"))
c.at("Tenía un motor de dos cilindros", P("polski"))
c.at("Y entonces llegó un auto que iba a cambiar", photo("m_niva", 12, "in", cap="Lada Niva|1977"))
c.at("Según las fuentes, el Niva se presentó", P("niva"))
c.at("Su motor era sencillo y robusto", P("niva"))
c.at("El Niva se convirtió en una leyenda", P("niva"))
chapters.append(c)

c = ch("ch04")
c.at(0, P("lada"))
c.at("En Ecuador, según algunas fuentes", P("samara"))
c.at("Para muchas familias, ganar un Lada", photo("m_samara", 6, "in", cap="Lada Samara|años 80"))
c.at("En Chile, la historia fue", P("samara"))
c.at("En Argentina, el Lada se vendió", P("laika"))
c.at("el Samara y, por supuesto, el Niva", P("niva"))
c.at("Y en Venezuela", P("samara"))
c.at("En muchos de estos países, el Lada tenía", P("fiat"))
c.at("¿Por qué tuvieron éxito?", P("laika"))
c.at("Pero también tenían sus problemas", P("lada"))
chapters.append(c)

c = ch("ch05", 2.5)
c.at(0, P("vaz"))
c.at("En Cuba, el golpe fue todavía más duro", P("ladacuba"))
c.at("Los mecánicos cubanos", P("ladacuba"))
c.at("Por eso hoy, Cuba es una especie", P("habana"))
c.at("Y aunque pasaron los años", P("niva"))
c.at("Así que la próxima vez", P("ladacuba"))
c.at("Y ahora te pregunto a ti", P("lada"))
c.at("Y si has llegado hasta aquí", cta("Gracias por llegar al final", "suscríbete y déjame tu opinión", tv=True, remote=True))
chapters.append(c)

CTX = ["ladacuba", "lada", "ladacuba", "niva", "laika", "ladacuba"]
print(A.finish(chapters, "ES23_SOVIETICOS.mp4", CTX, subtitles="ES23.ass"))
