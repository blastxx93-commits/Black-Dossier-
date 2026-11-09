#!/usr/bin/env python3
"""ES07 Los 12 coches secretos de la Guerra Fría. Countdown list, theme "revista" (cyan + magenta magazine, Anton).
    python3 build_es07.py <narration_dir> > episode.json   (run from the work folder)
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "engine"))
import aus_kit as A
from aus_kit import P, photo, rank, stat, say, cta, title, ch, questions


def ai(*names):
    """AI scenes that exist in the reviewed set only (re-generated ones may be missing)."""
    rev = json.load(open(os.path.join(HERE, "reviewed.json")))
    return ["ai:" + n for n in names if f"ai/{n}_1.jpg" in rev]


PHOTOS = {
    "trabant": ["m_trabant"] + ai("ai_trabant_queue"), "wallfall": ["h_wall_fall"],
    "zastava": ["m_zastava750"], "s600": ["m_seat600"],
    "tatra": ["m_tatra603"],
    "volga": ai("ai_black_volga_night") + ["m_gaz21", "h_volga_deer"],
    "chaika": ["m_chaika"], "wedding": ["h_soviet_wedding"],
    "s124": ["m_seat124"], "lada": ["m_lada2101"], "fiat124": ["m_fiat124"],
    "zil": ["m_zil114"] + ai("ai_zil_lane") + ["m_zil111"], "moscow": ["h_kgb"],
    "volvo": ["m_volvo264te"] + ai("ai_wandlitz"), "wandlitz": ["h_wandlitz"],
    "wall": ["h_berlin_wall", "h_checkpoint"], "checkpoint": ai("ai_checkpoint_night") + ["h_checkpoint"],
    "sprite": ["m_sprite"], "isetta": ai("ai_isetta_hidden") + ["m_isetta"], "mauer": ["h_mauermuseum"],
    "lincoln": ai("ai_camp_david") + ["m_lincoln73"], "nixon": ["h_nixon_brezhnev"], "riga": ["h_riga_museum"],
    "gaz23": ["m_gaz23"] + ai("ai_kgb_chase"), "kgb": ["h_kgb"], "gaz24": ["m_gaz24"],
    "berlin": ["h_berlin_wall", "h_checkpoint"],
    "east": ["m_trabant", "m_gaz21", "m_tatra603", "m_chaika", "m_lada2101"],
}
CLIPS = json.load(open(os.path.join(HERE, "clips.json")))
GENERIC = CLIPS.pop("_generic", [])
FALLBACK = {k: ["east"] for k in PHOTOS}
FALLBACK.update({"east": ["wall"], "trabant": ["wallfall", "wall"], "wallfall": ["trabant", "wall"], "zastava": ["s600"], "s600": ["zastava"],
                 "volga": ["gaz24", "east"], "wedding": ["chaika"], "s124": ["fiat124", "lada"], "lada": ["s124", "fiat124"],
                 "zil": ["moscow", "chaika"], "moscow": ["zil"], "volvo": ["wandlitz", "wall"], "wandlitz": ["volvo"],
                 "wall": ["checkpoint", "berlin"], "checkpoint": ["wall", "sprite"], "sprite": ["checkpoint", "wall"],
                 "isetta": ["mauer", "wall"], "mauer": ["isetta", "wall"], "lincoln": ["nixon", "riga"], "nixon": ["lincoln"],
                 "riga": ["lincoln"], "gaz23": ["volga", "kgb", "gaz24"], "kgb": ["gaz23", "volga"], "gaz24": ["gaz23", "volga"],
                 "berlin": ["wall"]})
RES = ["m_trabant/1", "m_zastava750/1", "m_seat600/1", "m_tatra603/3", "m_gaz21/6", "m_chaika/1", "m_seat124/3", "m_lada2101/1",
       "m_zil114/1", "m_volvo264te/1", "m_sprite/3", "m_isetta/1", "m_lincoln73/1", "m_gaz23/6", "h_checkpoint/6", "h_wall_fall/3",
       "h_nixon_brezhnev/1", "h_riga_museum/1", "h_mauermuseum/2", "h_volga_deer/1"]
A.setup(sys.argv[1], os.path.join(HERE, "skip.json"), PHOTOS, CLIPS, GENERIC, FALLBACK, ["east", "wall"], reserved=RES)
A.THEME = "revista"
A.CLIP_TARGET = 0.10
A.MAX_HOLD, A.KEEP = 13.0, 9.0
A.ARCHIVE_OK = True
A.SPLIT_BY_SUBJECT = True
chapters = []

c = ch("ch00_hook", 0.6)
c.at(0, photo("m_sprite", 3, "in", cap="Berlín|mayo de 1963"))
c.at("Al volante va un joven austriaco", P("checkpoint"))
c.at("Delante hay una barrera de hierro", photo("h_checkpoint", 6, "in", cap="Checkpoint Charlie"))
c.at("Durante más de cuarenta años", P("berlin"))
c.at("Fue la Guerra Fría", P("moscow"))
c.at("Coches para huir", P("east"))
c.at("Y en esa historia, aunque te sorprenda", P("s124"))
c.at("Hoy vas a conocer los doce coches secretos", title("Coches secretos", "de la Guerra Fría", "1957 – 1979", "east"))
questions(c, ["Un Seiscientos comunista", "Coches que cruzaron el Muro", "El Volga que el KGB destruía"],
          ["de la Guerra Fría", "Y el número uno", "el KGB lo destruía"])
chapters.append(c)

c = ch("ch01")
c.at(0, rank(12, "Trabant", "m_trabant", 1, "Alemania Oriental · 1957", "el coche de cartón"))
c.at("El Trabant tenía un motor de dos tiempos", P("trabant"))
c.at("Pero lo peor no era el coche", stat("10–15 años", "de espera para un Trabant nuevo", "según la fuente", count=False))
c.at("Se fabricaron más de tres millones", P("trabant"))
c.at("Y en noviembre de 1989", photo("h_wall_fall", 3, "in", cap="Berlín|noviembre de 1989"))
c.at("El coche de cartón se convirtió", P("wallfall"))
c.at("Número once", rank(11, "SEAT 600 · Zastava 750", "m_zastava750", 1, "España · Yugoslavia", "los gemelos del Telón de Acero"))
c.at("Si viste nuestro vídeo sobre el SEAT 600", photo("m_seat600", 1, "in", cap="SEAT 600|Barcelona"))
c.at("En Yugoslavia, la fábrica Zastava", P("zastava"))
c.at("Piénsalo", P("s600"))
c.at("La Guerra Fría separó a Europa", P("zastava"))
chapters.append(c)

c = ch("ch02")
c.at(0, rank(10, "Tatra 603", "m_tatra603", 3, "Checoslovaquia · 1956", "el coche que el pueblo no podía comprar"))
c.at("Checoslovaquia, 1956", P("tatra"))
c.at("Pero el Tatra 603 tenía otra particularidad", P("tatra"))
c.at("Se fabricaron unos veinte mil", P("tatra"))
c.at("Número nueve", rank(9, "GAZ-21 Volga", "m_gaz21", 6, "Unión Soviética · 1956", "la leyenda del Volga negro"))
c.at("Era el coche soñado", photo("h_volga_deer", 1, "in"))
c.at("Y de ahí nació una leyenda", P("volga"))
c.at("Nunca se demostró nada", P("volga"))
chapters.append(c)

c = ch("ch03")
c.at(0, rank(8, "GAZ-13 Chaika", "m_chaika", 1, "Unión Soviética · 1959", "la gaviota del Partido"))
c.at("Una limusina de inspiración americana", P("chaika"))
c.at("El Chaika no se vendía", P("chaika"))
c.at("casarse", P("wedding"))
c.at("Entre 1959 y 1981 se fabricaron", stat("≈3.100", "GAZ-13 Chaika · 1959–1981", "GAZ", count=False))
c.at("Número siete", rank(7, "SEAT 124 · Lada", "m_seat124", 3, "España · URSS", "el mismo coche a los dos lados"))
c.at("Moscú, 1966", P("fiat124"))
c.at("Fiat ayudó a levantar la fábrica", photo("m_lada2101", 1, "in", cap="VAZ-2101 «Zhiguli»|1970"))
c.at("Y aquí entra España", P("s124"))
c.at("Así que, en los años setenta", P("lada"))
c.at("Y el Lada siguió fabricándose", P("lada"))
chapters.append(c)

c = ch("ch04")
c.at(0, rank(6, "ZIL-114", "m_zil114", 1, "Moscú · 1967", "la limusina del Politburó"))
c.at("La fábrica ZIL de Moscú", P("zil"))
c.at("Solo podían viajar en él", P("zil"))
c.at("La gente lo llamaba", say("«El carril ZIL»", "ZIL", 140))
c.at("Aquellas caravanas también eran un blanco", P("moscow"))
c.at("Número cinco", rank(5, "Volvo 264 TE", "m_volvo264te", 1, "Alemania Oriental · 1976", "los Volvo de los comunistas"))
c.at("A partir de 1976", P("volvo"))
c.at("Los altos dirigentes vivían todos juntos", P("wandlitz"))
c.at("Volvogrado", say("«Volvogrado»", "VOLVOGRADO", 140))
c.at("El pueblo esperaba quince años", P("volvo"))
chapters.append(c)

c = ch("ch05")
c.at(0, P("wall"))
c.at("Familias, parejas y amigos quedaron separados", P("wall"))
c.at("Número cuatro", rank(4, "Austin-Healey Sprite", "m_sprite", 5, "Berlín · 1963", "por debajo de la barrera"))
c.at("Así que Meixner estudió el Checkpoint Charlie", P("checkpoint"))
c.at("Le quitó el parabrisas", stat("≈95 cm", "de altura sin parabrisas", "según la fuente", count=False))
c.at("En la madrugada del cinco de mayo de 1963", P("checkpoint"))
c.at("Al día siguiente", P("sprite"))
c.at("Número tres", rank(3, "BMW Isetta", "m_isetta", 1, "Berlín · años 60", "el coche que escondía personas"))
c.at("Jacobi tenía un BMW Isetta", P("isetta"))
c.at("Funcionó", stat("9", "personas escaparon en coches como este", "Museo del Muro de Berlín", count=True))
c.at("El coche original se puede ver hoy", photo("h_mauermuseum", 2, "in", cap="Museo del Muro|Checkpoint Charlie"))
chapters.append(c)

c = ch("ch06")
c.at(0, rank(2, "Lincoln Continental", "m_lincoln73", 1, "EE. UU. · 1973", "el regalo de Nixon a Brézhnev"))
c.at("El líder soviético Leonid Brézhnev", photo("h_nixon_brezhnev", 1, "in", cap="Nixon y Brézhnev|1973"))
c.at("Así que le tiene preparado un regalo", P("lincoln"))
c.at("Brézhnev no se lo pensó", P("lincoln"))
c.at("Y no fue el único regalo", P("nixon"))
c.at("Brézhnev fue el mayor coleccionista", P("lincoln"))
c.at("El Lincoln de Nixon se conserva hoy", photo("h_riga_museum", 1, "in", cap="Museo del Motor|Riga"))
chapters.append(c)

c = ch("ch07", 2.5)
c.at(0, rank(1, "GAZ-23 Volga", "m_gaz23", 6, "KGB · 1962", "el coche que el KGB destruía"))
c.at("Unión Soviética, 1962", P("kgb"))
c.at("La solución salió de la fábrica GAZ", P("gaz23"))
c.at("Lo llamaron GAZ-23", say("«Dogoniálka»: la que te alcanza.", "TE ALCANZA", 110))
c.at("Por fuera, nadie notaba nada", P("gaz23"))
c.at("Entre 1962 y 1970 se fabricaron unos seiscientos", stat("≈600", "GAZ-23 fabricados · 1962–1970", "según la fuente", count=False))
c.at("Así era la Guerra Fría sobre ruedas", P("east"))
c.at("Ahora te pregunto a ti", P("berlin"))
c.at("Y si te ha gustado el vídeo", cta("Suscríbete", "historias de coches clásicos"))
chapters.append(c)

CTX = ["wall", "trabant", "tatra", "chaika", "zil", "wall", "lincoln", "gaz23"]
print(A.finish(chapters, "ES07_GUERRA_FRIA.mp4", CTX, subtitles="ES07.ass"))
