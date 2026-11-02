#!/usr/bin/env python3
"""ES01 Los 12 coches más peligrosos de los años 50: full edit, shots anchored to phrases.
    python3 build_es01.py <narration_dir> > episode.json   (run from the work folder)
Editing style from the Aussie channel (aus_kit). Real photos/clips first; AI only where nothing real exists.
Never footage of the Le Mans 1955 crash, the James Dean crash or victims.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "engine"))
import aus_kit as A
from aus_kit import P, photo, stat, say, cta, title, ch, questions, rank

PHOTOS = {
    "edsel": ["m_edsel", "m_edsel_2", "m_edsel_wheel"],
    "biscuter": ["m_biscuter", "m_biscuter_2"],
    "kr200": ["m_kr200", "m_kr200_2", "ai:ai_bubble_traffic"],
    "isetta": ["m_isetta", "m_isetta_2", "m_isetta_door"],
    "trabant": ["m_trabant_p50", "m_trabant_2", "h_ddr"],
    "seat600": ["m_seat600", "m_seat600_2", "m_seat600_door", "h_seat_factory", "ai:ai_spain_family_600"],
    "beetle": ["m_beetle", "m_beetle_2"],
    "porsche": ["m_porsche550", "m_porsche550_2"],
    "dauphine": ["m_dauphine", "m_dauphine_2", "h_fasa_valladolid"],
    "sl": ["m_300sl", "m_300sl_2", "m_300slr_2"],
    "slr": ["m_300slr", "h_jaguar_d", "h_healey", "h_lemans_track", "h_lemans_1955"],
    "belair": ["m_belair59", "m_belair57", "m_belair_2", "h_fins", "h_usa_1950s"],
    "volvo": ["m_volvo_pv544", "h_seatbelt", "ai:ai_bohlin_belt"],
    "dash": ["h_dashboard_1950s", "ai:ai_column_spear"],
    "usa": ["h_usa_1950s", "h_fins", "m_belair57"],
    "europe": ["h_germany_1950s", "h_spain_1950s", "m_isetta_2"],
    "crash": ["h_crash_dummy", "h_cornell", "ai:ai_cornell_lab"],
    "dean": ["h_james_dean", "h_cholame", "ai:ai_desert_crossroads"],
    # one-line AI scenes (nothing real shows these)
    "edsel_horn": ["ai:ai_edsel_horn"], "lift": ["ai:ai_lift_microcar"], "tank": ["ai:ai_tank_engine"],
    "dipstick": ["ai:ai_dipstick"], "suicide": ["ai:ai_suicide_door"], "swing": ["ai:ai_swing_axle"],
    "crosswind": ["ai:ai_crosswind"], "lemans_night": ["ai:ai_lemans_night"], "corvair": ["h_usa_1950s"],
}
CLIPS = json.load(open(os.path.join(HERE, "clips.json")))
GENERIC = CLIPS.pop("_generic", [])
FALLBACK = {"edsel": ["usa", "dash"], "biscuter": ["europe"], "kr200": ["europe", "isetta"], "isetta": ["europe", "kr200"],
            "trabant": ["europe"], "seat600": ["europe"], "beetle": ["europe"], "porsche": ["sl"], "dauphine": ["europe", "seat600"],
            "sl": ["porsche"], "slr": ["sl"], "belair": ["usa"], "volvo": ["belair"], "dash": ["usa"], "usa": ["belair"],
            "europe": ["seat600"], "crash": ["dash"], "dean": ["porsche"]}
# photos kept for the line that names them (photo()/rank())
RES = ["m_edsel/2", "m_edsel_wheel/3", "m_edsel_wheel/4", "m_biscuter/5", "m_biscuter/6", "m_biscuter/1", "m_kr200/3", "m_kr200_2/3",
       "m_isetta/1", "m_isetta_door/4", "m_isetta_door/1", "m_isetta/3", "m_trabant_p50/1", "m_trabant_2/1", "m_seat600/2",
       "m_seat600_door/2", "m_seat600/1", "m_beetle/5", "m_beetle_2/2", "m_porsche550/3", "m_porsche550_2/4", "m_dauphine/3",
       "m_dauphine_2/1", "m_300sl/4", "m_300sl_2/3", "m_300slr/1", "m_300slr/3", "h_lemans_1955/2", "m_belair59/1", "m_belair59/3",
       "m_volvo_pv544/2", "h_fasa_valladolid/1", "h_cholame/3", "h_james_dean/1", "h_hawthorn/2", "h_levegh/1", "m_edsel_2/3"]
A.setup(sys.argv[1], os.path.join(HERE, "skip.json"), PHOTOS, CLIPS, GENERIC, FALLBACK,
        ["usa", "europe", "belair", "seat600", "beetle"], reserved=RES)
A.CLIP_TARGET = 0.30          # few period clips exist: real photos fill the rest (owner rule 02/11: real first)
A.MAX_HOLD, A.KEEP = 9.0, 6.0
chapters = []

# ---------------------------------------------------------------- hook: opens on a car (rule), never the crash
c = ch("ch00_hook", 0.6)
c.at(0, photo("m_300slr", 1, "in", cap="Le Mans|11 de junio de 1955"))
c.at("Delante de él, tres coches", P("slr"))
c.at("Hay un roce", P("slr"))
c.at("Fue la peor tragedia", photo("h_lemans_1955", 2, "in", cap="In memoriam|11 de junio de 1955"))
c.at("Pero ese coche no es el número uno", say("No es el número uno.", "NÚMERO UNO", 150))
c.at("casi ningún coche llevaba cinturón", P("dash"))
c.at("Los salpicaderos eran de chapa", P("dash"))
c.at("podía clavarse en el pecho", P("dash"))
c.at("Hoy vas a conocer", title("Los 12 coches más peligrosos", "de los años 50", "1950 – 1959", "usa"))
questions(c, ["Sin marcha atrás", "El volante en la puerta", "Gasolina sobre el motor"],
          ["Uno se fabricó en España", "Otro llevaba el volante", "Otro escondía el depósito"])
c.at("Y el número uno no es un coche de carreras", P("belair"))
c.at("Al final te contaré", P("usa"))
chapters.append(c)

# ---------------------------------------------------------------- 12 Edsel · 11 Biscúter
c = ch("ch01")
c.at(0, P("usa"))
c.at("No había estrellas de seguridad", P("dash"))
c.at("Los fabricantes vendían potencia", P("usa"))
c.at("Así que cuando digo peligroso", P("belair"))
c.at("Número doce", rank(12, "Edsel", "m_edsel", 2, "1958", "Ford · cambio de botones Teletouch"))
c.at("El nombre era un homenaje", P("edsel"))
c.at("Ford llevaba años preparándolo", P("edsel"))
c.at("el cambio automático se manejaba con botones", photo("m_edsel_wheel", 3, "in", cap="Teletouch|botones en el centro del volante"))
c.at("Justo donde, en cualquier otro coche", photo("m_edsel_wheel", 4, "left"))
c.at("Piensa en un conductor de 1958", P("edsel_horn", photo_only=True))
c.at("Un peatón se cruza", P("edsel"))
c.at("Además, muchos propietarios se quejaban", P("edsel"))
c.at("El Edsel acabó siendo", photo("m_edsel_2", 3, "right", cap="Edsel|1958 – 1960"))
c.at("Número once", rank(11, "Biscúter", "m_biscuter", 1, "1953 · España", "Autonacional · Sant Adrià de Besòs"))
c.at("Barcelona, 1953", photo("m_biscuter", 5, "in", cap="Biscúter|años 50"))
c.at("Y Voisin no era cualquiera", P("biscuter"))
c.at("En Francia no lo quisieron", P("biscuter"))
c.at("Tenía un motor Hispano Villiers", P("biscuter"))
c.at("Exacto. Las primeras unidades no tenían marcha atrás", say("Sin marcha atrás.", "MARCHA ATRÁS", 150))
c.at("te bajabas, levantabas el coche", P("lift", photo_only=True))
c.at("Los frenos eran de tambor", P("biscuter"))
c.at("cualquier choque con un camión", P("biscuter"))
c.at("Aun así, se fabricaron más de diez mil", photo("m_biscuter", 6, "left", cap="Biscúter|más de 10.000 unidades"))
c.at("Hasta que en 1957 llegó otro coche", P("seat600"))
chapters.append(c)

# ---------------------------------------------------------------- 10 KR200 · 9 Isetta
c = ch("ch02")
c.at(0, P("europe"))
c.at("Número diez", rank(10, "Messerschmitt KR200", "m_kr200", 3, "1955", "De la fábrica de aviones a la carretera"))
c.at("Después de la guerra", P("kr200"))
c.at("de tres ruedas, con dos asientos en fila", photo("m_kr200_2", 3, "in", cap="Dos asientos en fila|como en un caza"))
c.at("Y el techo era una burbuja", P("kr200"))
c.at("En Alemania lo llamaban", say("«El ataúd de Blancanieves»", "BLANCANIEVES", 110))
c.at("Podía acercarse a los noventa", P("kr200"))
c.at("En el tráfico de los años cincuenta", P("kr200"))
c.at("Y tenía otra rareza", P("kr200"))
c.at("El motor de dos tiempos giraba al revés", P("kr200"))
c.at("Y la dirección no era un volante normal", P("kr200"))
c.at("Número nueve", rank(9, "BMW Isetta", "m_isetta", 1, "1955", "La única puerta, delante"))
c.at("Si el Messerschmitt parecía un avión", P("isetta"))
c.at("La única puerta estaba delante", photo("m_isetta_door", 1, "in", cap="Isetta|la puerta es todo el frontal"))
c.at("Y el volante y el cuadro de instrumentos", photo("m_isetta", 3, "left"))
c.at("Ahora piensa en un choque frontal", P("isetta"))
c.at("Y si se deformaba", P("isetta"))
c.at("Por eso el Isetta llevaba un techo de lona", P("isetta"))
c.at("Era la salida de emergencia", say("La salida de emergencia era el techo.", "TECHO", 120))
c.at("Aun así, el Isetta fue un éxito enorme", stat("161.728", "BMW Isetta fabricados", "BMW Group Classic", count=True))
c.at("Mucha gente que hoy conduce un BMW", photo("m_isetta_door", 4, "in"))
chapters.append(c)

# ---------------------------------------------------------------- 8 Trabant · 7 SEAT 600
c = ch("ch03")
c.at(0, rank(8, "Trabant P50", "m_trabant_p50", 1, "1957", "Alemania del Este"))
c.at("En la Alemania del Este", P("trabant"))
c.at("Su carrocería no era de acero", P("trabant"))
c.at("Pero lo más inquietante estaba escondido", photo("m_trabant_2", 1, "in"))
c.at("el depósito iba colocado más alto", P("tank", photo_only=True))
c.at("en un choque frontal, el depósito", say("Depósito encima del motor. Sin bomba de gasolina.", "DEPÓSITO", 100))
c.at("Hoy, las normas de seguridad prohíben", P("trabant"))
c.at("Y otro detalle", P("trabant"))
c.at("metías una varilla", P("dipstick", photo_only=True))
c.at("El Trabant se siguió fabricando", P("trabant"))
c.at("La gente lo encargaba", P("europe"))
c.at("Número siete", rank(7, "SEAT 600", "m_seat600", 2, "1957 · España", "El coche que motorizó a España"))
c.at("Veintisiete de junio de 1957", P("seat600"))
c.at("Con él, millones de españoles", P("seat600"))
c.at("las puertas suicidas", photo("m_seat600_door", 2, "in", cap="SEAT 600|puertas «suicidas»"))
c.at("Si una puerta se abría en marcha", P("suicide", photo_only=True))
c.at("Las puertas suicidas siguieron", P("seat600"))
c.at("Cuatro adultos, una maleta", P("seat600"))
c.at("El Seiscientos motorizó a España", photo("m_seat600", 1, "left"))
c.at("De la Zona Franca salieron", stat("≈800.000", "SEAT 600 fabricados hasta 1973", "SEAT / Motorpasión", count=False))
c.at("siempre hay alguien que se acerca", P("seat600"))
chapters.append(c)

# ---------------------------------------------------------------- 6 Escarabajo
c = ch("ch04")
c.at(0, rank(6, "Volkswagen Escarabajo", "m_beetle", 5, "años 50", "Uno de los más vendidos del mundo"))
c.at("En los años cincuenta, el Escarabajo", P("beetle"))
c.at("Dos cosas", say("Dos problemas.", "DOS", 160))
c.at("La primera: su suspensión trasera", P("beetle"))
c.at("Cuando el coche tomaba una curva rápida", P("beetle"))
c.at("Un sobreviraje repentino", P("swing", photo_only=True))
c.at("La segunda: dónde estaba el depósito", P("beetle"))
c.at("a pocos centímetros de las piernas", P("beetle"))
c.at("ni siquiera tenía indicador de gasolina", photo("m_beetle_2", 2, "in", cap="Escarabajo|sin indicador de gasolina"))
c.at("Cuando el motor empezaba a fallar", P("beetle"))
c.at("Esa suspensión trasera acabaría", P("usa"))
c.at("En 1965, el abogado Ralph Nader", say("«Inseguro a cualquier velocidad» – Ralph Nader, 1965", "INSEGURO", 95))
c.at("Su primer capítulo atacaba al Chevrolet Corvair", P("corvair"))
c.at("Pero diez años antes", P("beetle"))
c.at("Y no era el único coche", P("sl"))
c.at("Pero antes de llegar a ese coche", P("porsche"))
chapters.append(c)

# ---------------------------------------------------------------- 5 Porsche 550 · 4 Dauphine
c = ch("ch05")
c.at(0, rank(5, "Porsche 550 Spyder", "m_porsche550", 3, "1955", "Carrocería de aluminio, sin techo"))
c.at("El 550 Spyder era un coche de carreras", P("porsche"))
c.at("Muy ligero y muy rápido", P("porsche"))
c.at("En septiembre de 1955, el actor James Dean", photo("h_james_dean", 1, "in", cap="James Dean|1931 – 1955"))
c.at("Sus amigos lo llamaban Little Bastard", photo("m_porsche550_2", 4, "left"))
c.at("Ese mismo día, un par de horas antes", P("dean"))
c.at("El treinta de septiembre de 1955", P("porsche"))
c.at("En un cruce cerca de un pueblo llamado Cholame", photo("h_cholame", 3, "in", cap="Cholame, California"))
c.at("El Ford era mucho más pesado", P("dean"))
c.at("James Dean murió", say("James Dean murió. Tenía 24 años.", "24", 120))
c.at("La carrocería de aluminio del Spyder", P("porsche"))
c.at("Número cuatro", rank(4, "Renault Dauphine", "m_dauphine", 3, "1956", "Fabricado en Valladolid por FASA"))
c.at("En España se fabricó en Valladolid", photo("h_fasa_valladolid", 1, "in", cap="FASA|Valladolid"))
c.at("Pero tenía el motor detrás", P("dauphine"))
c.at("En carreteras con viento lateral", P("crosswind", photo_only=True))
c.at("En España se le acabó colgando", say("«El coche de las viudas»", "VIUDAS", 120))
c.at("Hay quien dice que el apodo fue injusto", P("dauphine"))
c.at("Aun así, el Dauphine fue uno de los coches", photo("m_dauphine_2", 1, "left"))
chapters.append(c)

# ---------------------------------------------------------------- 3 300 SL
c = ch("ch06")
c.at(0, rank(3, "Mercedes-Benz 300 SL", "m_300sl", 4, "1954", "Alas de Gaviota"))
c.at("Se presentó en Nueva York en 1954", P("sl"))
c.at("Fue el primer coche de producción con inyección", P("sl"))
c.at("podía rozar los doscientos sesenta", stat("≈260 km/h", "velocidad máxima según el desarrollo", "Mercedes-Benz", count=False))
c.at("Las puertas se abrían hacia arriba", P("sl"))
c.at("Salir deprisa no era fácil", photo("m_300sl_2", 3, "in"))
c.at("Y debajo de toda esa belleza", P("sl"))
c.at("En manos expertas era una maravilla", P("sl"))
c.at("Y, como casi todos sus contemporáneos", P("sl"))
c.at("Entre 1954 y 1957 se fabricaron", stat("≈1.400", "300 SL Gullwing fabricados", "1954 – 1957", count=False))
c.at("Hoy, los que sobreviven", P("sl"))
c.at("Mercedes acabó cambiando", P("sl"))
c.at("Y lo hizo de la peor manera posible", P("slr"))
chapters.append(c)

# ---------------------------------------------------------------- 2 300 SLR (no crash images)
c = ch("ch07")
c.at(0, rank(2, "Mercedes-Benz 300 SLR", "m_300slr", 3, "1955", "Le Mans, 11 de junio"))
c.at("Volvemos al principio", P("slr"))
c.at("Mike Hawthorn, con un Jaguar", P("slr"))
c.at("Detrás, Lance Macklin", P("slr"))
c.at("Y justo detrás llega Pierre Levegh", P("slr"))
c.at("El Mercedes golpea", P("slr"))
c.at("La carrocería del SLR", P("slr"))
c.at("Pierre Levegh murió en el acto", photo("h_levegh", 1, "in"))
c.at("Y murieron más de ochenta espectadores", stat("+80", "espectadores muertos · más de 120 heridos", "Le Mans, 1955", red=True, count=False))
c.at("Increíblemente, la carrera siguió", P("lemans_night", photo_only=True))
c.at("Al día siguiente", photo("h_hawthorn", 2, "in"))
c.at("Las consecuencias fueron enormes", P("slr"))
c.at("Y Suiza prohibió las carreras", say("Suiza prohibió las carreras en circuito.", "SUIZA", 110))
c.at("El 300 SLR no era un coche de calle", P("slr"))
c.at("Y aun así, no es el número uno", P("usa"))
chapters.append(c)

# ---------------------------------------------------------------- 1 Bel Air + Volvo belt + end CTA
c = ch("ch08", 2.5)
c.at(0, rank(1, "Chevrolet Bel Air", "m_belair59", 1, "1959", "El coche familiar soñado"))
c.at("Para muchos, el Bel Air es el símbolo", P("belair"))
c.at("Pero era como casi todos los coches americanos", P("belair"))
c.at("Con un salpicadero de metal", photo("m_belair59", 3, "in"))
c.at("Ya en esos años, investigadores", P("crash"))
c.at("el volante y la columna de dirección", P("dash"))
c.at("Hubo un fabricante que intentó escucharles", P("usa"))
c.at("Durante décadas se repitió", P("usa"))
c.at("Y ahora, la prueba que te prometí", say("La prueba.", "PRUEBA", 160))
c.at("En septiembre de 2009", P("crash"))
c.at("Cogió un Chevrolet Bel Air de 1959", P("belair"))
c.at("A sesenta y cuatro kilómetros por hora", stat("64 km/h", "choque frontal · 1959 contra 2009", "IIHS", count=False))
c.at("El Bel Air era el más pesado", P("crash"))
c.at("El del Bel Air se colapsó", say("El habitáculo del Bel Air se colapsó.", "COLAPSÓ", 110))
c.at("El coche que todo el mundo soñaba", P("belair"))
c.at("Pero la historia tiene un final inesperado", photo("m_volvo_pv544", 2, "in", cap="Volvo PV544|1959"))
c.at("Nils Bohlin presentó algo muy sencillo", P("volvo"))
c.at("Y después hizo algo que casi ninguna empresa", P("volvo"))
c.at("Según la propia Volvo", stat("+1.000.000", "vidas salvadas por el cinturón de tres puntos", "Volvo (estimación)", count=False))
c.at("Así que la próxima vez", P("volvo"))
c.at("Si te ha gustado el vídeo", cta("Suscríbete", "historias de coches clásicos"))
c.at("¿en cuál te habrías atrevido a viajar?", cta("¿En cuál te habrías atrevido a viajar?", "cuéntamelo en los comentarios"))
chapters.append(c)

CTX = ["usa", "usa", "europe", "europe", "beetle", "porsche", "sl", "slr", "belair"]
print(A.finish(chapters, "ES01_Peligrosos_50.mp4", CTX, subtitles="ES01.ass"))
