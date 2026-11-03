#!/usr/bin/env python3
"""ES03 Los 10 microcoches más locos de los años 50 y 60: full edit, shots anchored to phrases.
    python3 build_es03.py <narration_dir> > episode.json   (run from the work folder)
Editing style from the Aussie channel (aus_kit). Real photos first; AI only where nothing real exists.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "engine"))
import aus_kit as A
from aus_kit import P, photo, stat, say, cta, title, ch, questions, rank

ERA = ["h_microcar_museum", "h_bubble_rally", "h_microcar_show", "h_microcar_museum_2", "m_goggo", "m_fulda", "m_bond",
       "m_vespa400", "m_scootacar", "m_frisky", "m_lloyd", "m_velam", "m_nsu_prinz", "m_isetta", "m_kr200", "h_europe_50s"]
PHOTOS = {
    "era": ERA,
    "museum": ["h_microcar_museum", "h_microcar_museum_2", "h_bubble_rally", "h_microcar_show"],
    "subaru": ["m_subaru360", "m_subaru360_2"],
    "heinkel": ["m_heinkel", "m_heinkel_2"],
    "tiger": ["m_tiger", "m_tiger_2", "m_kr200", "ai:ai_tiger_race"],
    "ptv": ["m_ptv", "m_ptv_2", "h_manresa", "ai:ai_spain_microcar"],
    "pegasin": ["m_pegasin", "m_biscuter", "m_pegaso", "m_kapi"],
    "inter": ["m_inter", "m_inter_2"],
    "janus": ["m_janus", "m_janus_2"],
    "mopetta": ["m_mopetta"],
    "trident": ["m_trident", "m_trident_2", "ai:ai_bubble_hot"],
    "p50": ["m_p50", "m_p50_2", "h_isle_of_man"],
    "small": ["m_mini", "m_fiat500", "m_seat600"],
    "suez": ["ai:ai_suez_queue"], "handle": ["ai:ai_p50_handle"], "corridor": ["ai:ai_inter_corridor"],
    "bbc": ["h_bbc"],
}
CLIPS = json.load(open(os.path.join(HERE, "clips.json")))
GENERIC = CLIPS.pop("_generic", [])
FALLBACK = {k: ["museum", "era"] for k in PHOTOS}  # a car out of photos falls back to general microcar scenes, not another model
FALLBACK.update({"pegasin": ["ptv", "era"], "ptv": ["museum", "era"], "trident": ["p50", "era"], "p50": ["trident", "era"],
                 "small": ["era"], "tiger": ["era"], "era": ["small"]})
RES = ["m_subaru360/1", "m_heinkel/2", "m_tiger/1", "m_ptv/2", "m_pegasin/1", "m_inter/2", "m_janus/3", "m_mopetta/1",
       "m_trident/1", "m_p50/8", "m_p50/3", "m_janus/2", "m_pegaso/3", "m_biscuter/1", "m_trident/8", "m_mopetta/2", "m_inter/8",
       "m_heinkel/3", "m_subaru360/4", "m_mini/1", "m_seat600/3"]
A.setup(sys.argv[1], os.path.join(HERE, "skip.json"), PHOTOS, CLIPS, GENERIC, FALLBACK, ["era", "small"], reserved=RES)
A.CLIP_TARGET = 0.10
A.MAX_HOLD, A.KEEP = 12.0, 8.0     # longer holds on the right car beat cutting to a different microcar
A.ARCHIVE_OK = True
A.SPLIT_BY_SUBJECT = True
chapters = []

# ---------------------------------------------------------------- hook: opens on the P50
c = ch("ch00_hook", 0.6)
c.at(0, photo("m_p50", 3, "in", cap="Isla de Man|años 60"))
c.at("lo agarra por un asa", P("handle", photo_only=True))
c.at("Ese coche no tiene marcha atrás", P("p50"))
c.at("Es el coche de producción más pequeño", say("El coche más pequeño de la historia", "MÁS PEQUEÑO", 120))
c.at("Pero en los años cincuenta y sesenta, Europa", P("era"))
c.at("Coches con una sola puerta delante", P("heinkel"))
c.at("Coches con puertas delante y detrás", photo("m_janus", 2, "in"))
c.at("Coches con forma de huevo", photo("m_mopetta", 2, "left"))
c.at("Y dos de ellos se fabricaron en España", P("pegasin"))
c.at("Hoy vas a conocer", title("Los 10 microcoches más locos", "de los años 50 y 60", "1950 – 1969", "era"))
questions(c, ["Una fábrica de aviones de guerra", "Ruedas que se plegaban", "Dos caras, como un dios romano"],
          ["Uno lo fabricaba", "Otro podía doblar", "Y otro tenía dos caras"])
c.at("Y el número uno es ese coche", P("p50"))
chapters.append(c)

# ---------------------------------------------------------------- context · 10 Subaru 360 · 9 Heinkel
c = ch("ch01")
c.at(0, P("era"))
c.at("Después de la Segunda Guerra Mundial", P("era"))
c.at("Así nacieron los microcoches", P("era"))
c.at("Y en 1956, la crisis del canal de Suez", P("suez", photo_only=True))
c.at("En Alemania incluso tenían un nombre", say("Kabinenroller: scooters con cabina", "KABINENROLLER", 100))
c.at("Durante unos años, los ingenieros", P("era"))
c.at("Número diez", rank(10, "Subaru 360", "m_subaru360", 1, "1958 · Japón", "La «mariquita»"))
c.at("Lo empezamos en Japón", P("subaru"))
c.at("En Japón existía una categoría especial", P("subaru"))
c.at("Pero lo loco vino después", P("subaru"))
c.at("El precio era su gran argumento", stat("$1.300", "precio del Subaru 360 en EE. UU.", "CNN", count=False))
c.at("En abril de 1969", stat("37,5 s", "de 0 a 80 km/h · Consumer Reports, 1969", "Consumer Reports", red=True, count=False))
c.at("no aceptable", say("«No aceptable»", "NO ACEPTABLE", 140))
c.at("Lo curioso es que aquel fracaso", photo("m_subaru360", 4, "in"))
c.at("Número nueve", rank(9, "Heinkel Kabine", "m_heinkel", 2, "1956 · Alemania", "De los aviones a la burbuja"))
c.at("Si el nombre Heinkel te suena", P("heinkel"))
c.at("Durante la Segunda Guerra Mundial, la fábrica", P("heinkel"))
c.at("Era una burbuja con una sola puerta delante", photo("m_heinkel", 3, "in", cap="Heinkel Kabine|una sola puerta, delante"))
c.at("En 1958 se cedió la licencia", P("heinkel"))
c.at("En Gran Bretaña, el Heinkel se ganó", P("heinkel"))
c.at("Un coche alemán, diseñado", P("heinkel"))
chapters.append(c)

# ---------------------------------------------------------------- 8 Tiger · 7 PTV 250
c = ch("ch02")
c.at(0, rank(8, "FMR Tiger Tg500", "m_tiger", 1, "1958 · Alemania", "Cuatro ruedas · ≈126 km/h"))
c.at("Si viste nuestro vídeo", P("tiger"))
c.at("Lo fabricaba la empresa FMR", P("tiger"))
c.at("El motor era un dos tiempos", P("tiger"))
c.at("Resultado: unos ciento veintiséis", stat("126 km/h", "velocidad máxima del Tiger", "FMR", count=False))
c.at("Imagina ir a ciento veinte por hora", P("tiger"))
c.at("Número siete", rank(7, "PTV 250", "m_ptv", 2, "1956 · Manresa", "Perramon · Tachó · Vila"))
c.at("Manresa, 1956", P("ptv"))
c.at("El cuatro de mayo de 1956", P("ptv"))
c.at("El PTV 250 era un descapotable", P("ptv"))
c.at("Hubo incluso una pequeña serie", P("ptv"))
c.at("Pero en 1957 llegó el SEAT 600", photo("m_seat600", 3, "in", cap="SEAT 600|1957"))
c.at("Y aquí está lo curioso", P("ptv"))
chapters.append(c)

# ---------------------------------------------------------------- 6 Pegasín · 5 Inter
c = ch("ch03")
c.at(0, rank(6, "Biscúter Pegasín", "m_pegasin", 1, "1957 · Barcelona", "Un Pegaso en miniatura"))
c.at("En nuestro vídeo de los coches peligrosos", photo("m_biscuter", 1, "in", cap="Biscúter|la «Zapatilla»"))
c.at("En la España de los años cincuenta, el coche de los sueños", photo("m_pegaso", 3, "in", cap="Pegaso Z-102"))
c.at("La gente lo llamó Pegasín", P("pegasin"))
c.at("El Biscúter normal ya había vendido", P("pegasin"))
c.at("El problema es que, debajo", stat("75 km/h", "velocidad máxima del Pegasín", "Autonacional", count=False))
c.at("Era como ponerle el traje", P("pegasin"))
c.at("Número cinco", rank(5, "Inter 175 Berline", "m_inter", 2, "1953 · Francia", "Un avión sin alas"))
c.at("Francia, 1953", P("inter"))
c.at("SNCAN eran las siglas", P("inter"))
c.at("Su motor era un pequeño dos tiempos", P("inter"))
c.at("El Inter tenía tres ruedas", P("inter"))
c.at("Pero lo verdaderamente loco", P("corridor", photo_only=True))
c.at("En los modelos posteriores", photo("m_inter", 8, "in"))
chapters.append(c)

# ---------------------------------------------------------------- 4 Janus
c = ch("ch04")
c.at(0, rank(4, "Zündapp Janus", "m_janus", 3, "1957 · Alemania", "El coche de las dos caras"))
c.at("Zündapp era una marca alemana", P("janus"))
c.at("Y, otra vez, detrás había una empresa", P("janus"))
c.at("El Janus tenía una puerta delante", P("janus"))
c.at("El motor era un monocilíndrico", P("janus"))
c.at("Imagina el viaje", P("janus"))
c.at("Hoy, mucha gente lo conoce", P("janus"))
c.at("Era ingenioso, era raro", stat("≈6.900", "Zündapp Janus fabricados (1957–1958)", "Zündapp", count=False))
chapters.append(c)

# ---------------------------------------------------------------- 3 Mopetta · 2 Trident
c = ch("ch05")
c.at(0, rank(3, "Brütsch Mopetta", "m_mopetta", 1, "1956 · Alemania", "Un huevo con ruedas"))
c.at("Egon Brütsch era un diseñador", P("mopetta"))
c.at("Era un huevo", say("Un huevo con ruedas.", "HUEVO", 140))
c.at("Una carrocería de fibra de vidrio", P("mopetta"))
c.at("No había sitio para nadie más", say("Un solo asiento.", "UN SOLO ASIENTO", 140))
c.at("Georg von Opel", P("mopetta"))
c.at("Catorce coches en todo el mundo", stat("14", "Mopettas fabricados en total", "Brütsch", count=False))
c.at("Número dos", rank(2, "Peel Trident", "m_trident", 1, "1965 · Isla de Man", "El platillo volante terrestre"))
c.at("Y ahora viajamos a la Isla de Man", P("p50"))
c.at("El hombre detrás de Peel", P("trident"))
c.at("El Trident tenía tres ruedas", photo("m_trident", 8, "in"))
c.at("Para entrar, se levantaba toda la burbuja", P("trident"))
c.at("Su velocidad máxima", P("trident"))
c.at("Según algunas fuentes, costaba", P("trident"))
c.at("Se fabricaron muy pocos", P("trident"))
chapters.append(c)

# ---------------------------------------------------------------- 1 P50 + end
c = ch("ch06", 2.5)
c.at(0, rank(1, "Peel P50", "m_p50", 8, "1962 · Isla de Man", "El coche más pequeño de la historia"))
c.at("Isla de Man, 1962", P("p50"))
c.at("El P50 tenía tres ruedas", P("p50"))
c.at("Pesaba unos cincuenta y nueve kilos", stat("59 kg", "peso del Peel P50", "Peel", count=False))
c.at("Su motor era un dos tiempos", P("p50"))
c.at("Tenía tres marchas hacia delante", say("Sin marcha atrás.", "MARCHA ATRÁS", 150))
c.at("te bajabas, cogías el asa", P("p50"))
c.at("Se vendieron muy pocos", P("p50"))
c.at("Hasta que, en 2007", P("bbc"))
c.at("Y en 2010, el Libro Guinness", say("Guinness 2010: el coche de producción más pequeño", "GUINNESS", 100))
c.at("Hoy, un Peel P50 original", P("p50"))
c.at("Tanto gustó que", P("p50"))
c.at("Los microcoches desaparecieron", P("small"))
c.at("De hecho, el Mini nació", photo("m_mini", 1, "in", cap="Mini|1959"))
c.at("Hoy, muchos de estos coches sobreviven", P("era"))
c.at("Si te ha gustado el vídeo", cta("Suscríbete", "historias de coches clásicos"))
c.at("¿en cuál te atreverías a dar una vuelta?", cta("¿En cuál te atreverías a dar una vuelta?", "cuéntamelo en los comentarios"))
chapters.append(c)

CTX = ["p50", "era", "ptv", "pegasin", "janus", "trident", "p50"]
print(A.finish(chapters, "ES03_Microcoches.mp4", CTX, subtitles="ES03.ass"))
