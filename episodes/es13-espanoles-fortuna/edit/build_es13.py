#!/usr/bin/env python3
"""ES13 Los coches españoles que hoy valen una fortuna. Countdown; rendered with the Race template (engine/hf_race.py).
    python3 build_es13.py <narration_dir> > episode.json   (run from the work folder)
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "engine"))
import aus_kit as A
from aus_kit import P, photo, rank, stat, say, cta, title, ch

PHOTOS = {
    "pegaso": ["m_pegaso"], "s600": ["m_seat600"], "bisc": ["m_biscuter"], "boca": ["m_bocanegra"], "s1430": ["m_seat1430"],
    "s124": ["m_124sport"], "r5": ["m_r5copa"], "auction": ["h_auction"], "conc": ["h_concentracion"], "desg": ["h_desguace"],
    "mix": ["h_auction", "h_concentracion", "h_desguace"],
}
CLIPS = json.load(open(os.path.join(HERE, "clips.json")))
GENERIC = CLIPS.pop("_generic", [])
FALLBACK = {k: [] for k in PHOTOS}
FALLBACK.update({"mix": ["auction", "s600"], "conc": ["s600", "auction"], "desg": ["s600", "bisc"], "auction": ["mix"]})
RES = ["m_pegaso/3", "m_pegaso/7", "m_seat600/12", "m_biscuter/13", "m_bocanegra/12", "m_seat1430/4", "m_124sport/2",
       "m_r5copa/1"]
A.setup(sys.argv[1], os.path.join(HERE, "skip.json"), PHOTOS, CLIPS, GENERIC, FALLBACK, [], reserved=RES)
A.THEME = "race"
A.CLIP_TARGET = 0.0
A.MAX_HOLD, A.KEEP = 10.0, 7.0
A.ARCHIVE_OK = True
A.STRICT_POOLS = True
A.SPLIT_BY_SUBJECT = True
chapters = []

c = ch("ch00_hook", 0.6)
c.at(0, photo("m_pegaso", 3, "in", cap="Pegaso Z-102|Barcelona, 1953"))
c.at("Con ese dinero se podían comprar", P("s600"))
c.at("Hoy, ese mismo coche", stat("≈1.000.000 $", "Pegaso Z-102 · Pebble Beach, 2014", "según la fuente", count=False))
c.at("Y no es el único", P("auction"))
c.at("Coches que acabaron olvidados", P("desg"))
c.at("Coches que tu abuelo vendió", P("boca"))
c.at("Hoy vas a conocer", title("Hoy valen una fortuna", "coches españoles", "1951 – 1985", "mix"))
c.at("Y quédate hasta el final", P("pegaso"))
c.at("Una advertencia antes de empezar", P("auction"))
chapters.append(c)

c = ch("ch01")
c.at(0, rank(7, "SEAT 600", "m_seat600", 12, "Barcelona · 1957", "el coche que motorizó España"))
c.at("El Seiscientos salió a la venta", stat("65.000 pts", "precio de salida del SEAT 600 (sin impuestos)", "según la fuente", count=False))
c.at("Aun así, se vendieron", P("s600"))
c.at("Hoy la historia es otra", P("s600"))
c.at("En una subasta por su sesenta aniversario", stat("+8.000 €", "estimación · SEAT 600 N de 1962", "Catawiki", count=False))
c.at("No es una fortuna de millonario", P("s600"))
c.at("Número seis", rank(6, "Biscúter", "m_biscuter", 13, "Barcelona · años 50", "la «zapatilla»"))
c.at("Precisamente por eso hoy son tan buscados", P("bisc"))
c.at("Según la casa de subastas Setdart", stat("10.000 – 12.000 €", "estimación · Biscúter 1957 sin restaurar", "Setdart", count=False))
c.at("Y en 2026 se anunciaba", P("bisc"))
c.at("Piénsalo", P("bisc"))
chapters.append(c)

c = ch("ch02")
c.at(0, rank(5, "SEAT 1200 Sport", "m_bocanegra", 12, "1975 – 1979", "el «Bocanegra»"))
c.at("Se fabricaron unas diecinueve mil", P("boca"))
c.at("Según la plataforma Classic Trader", stat("≈300", "Bocanegra supervivientes conocidos", "Classic Trader", count=False))
c.at("Y eso se nota en el precio", P("boca"))
c.at("Número cuatro", rank(4, "SEAT 1430", "m_seat1430", 4, "1972", "el de Julio Iglesias"))
c.at("El SEAT 1430 fue la berlina", P("s1430"))
c.at("Pero en 2017 salió a subasta", stat("25.000 – 32.500 €", "estimación · 1430 de Julio Iglesias", "Catawiki", count=False))
c.at("¿Se llegó a pagar esa cifra?", P("s1430"))
c.at("Las pujas iniciales", P("s1430"))
c.at("en el mundo de los clásicos", say("Una buena historia también vale dinero.", "HISTORIA", 120))
chapters.append(c)

c = ch("ch03")
c.at(0, P("conc"))
c.at("Número tres", rank(3, "SEAT 124 Sport", "m_124sport", 2, "Barcelona · 1970", "el coupé de los sueños"))
c.at("Era caro y era el sueño", P("s124"))
c.at("Hoy, un 124 Sport en buen estado", P("s124"))
c.at("En los anuncios de 2026", stat("27.500 €", "SEAT 124 Sport Coupé 1800 · anuncio 2026", "TheParking", count=False))
c.at("Número dos", rank(2, "Renault 5 Copa Turbo", "m_r5copa", 1, "FASA · Valladolid", "los turbo de Valladolid"))
c.at("Durante años fueron coches baratos", P("r5"))
c.at("sus precios se mueven", stat("8.000 – 30.000 €", "Copa Turbo / Supercinco GT Turbo", "Motor1", count=False))
c.at("Y ahora sí", P("pegaso"))
chapters.append(c)

c = ch("ch04")
c.at(0, rank(1, "Pegaso Z-102", "m_pegaso", 7, "ENASA · 1951", "el coche español más caro"))
c.at("El resultado fue el Pegaso Z-102", P("pegaso"))
c.at("Pero era carísimo", stat("500.000 pts", "precio del Z-102 · un SEAT 600: ≈70.000", "según las fuentes", count=False))
c.at("Solo se fabricaron", P("pegaso"))
c.at("Hoy, el Pegaso Z-102", P("pegaso"))
c.at("En 2014, un Z-102", stat("≈1.000.000 $", "Z-102 Saoutchik · Pebble Beach 2014", "según la fuente", count=False))
c.at("Otra unidad fue subastada", P("pegaso"))
c.at("Un coche que en España", P("pegaso"))
chapters.append(c)

c = ch("ch05", 2.5)
c.at(0, P("conc"))
c.at("Así que, si en tu familia", P("desg"))
c.at("Y ahora te pregunto a ti", P("mix"))
c.at("Y si te ha gustado esta historia", cta("Suscríbete", "historias de coches clásicos"))
chapters.append(c)

CTX = ["mix", "s600", "s1430", "s124", "pegaso", "mix"]
print(A.finish(chapters, "ES13_FORTUNA_ES.mp4", CTX, subtitles="ES13.ass"))
