#!/usr/bin/env python3
"""ES22 Inventos que llegaron 30 años antes. Race template. Regra: imagem = narração."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "engine"))
import aus_kit as A
from aus_kit import P, photo, rank, stat, say, cta, title, ch

PHOTOS = {"ds": ["m_ds"], "dss": ["m_dssusp"], "dsf": ["m_dsfaros"], "ctype": ["m_ctype"], "disco": ["m_disco"],
          "mini": ["m_mini"], "minim": ["m_minimotor"], "sl": ["m_300sl"], "w111": ["m_w111"], "bar": ["m_barenyi"],
          "w116": ["m_w116"], "w126": ["m_w126"], "volvo": ["m_volvo"], "930": ["m_930"], "ro80": ["m_ro80"], "787": ["m_787b"]}
CLIPS = json.load(open(os.path.join(HERE, "clips.json")))
GENERIC = CLIPS.pop("_generic", [])
FALLBACK = {k: [] for k in PHOTOS}
FALLBACK.update({"disco": ["ctype"], "dss": ["ds"], "dsf": ["ds"], "minim": ["mini"], "bar": ["w111"], "ds": ["dss", "dsf"]})
RES = ["m_ds/13", "m_ctype/1", "m_mini/1", "m_300sl/10", "m_w111/9", "m_dssusp/8", "m_dsfaros/1", "m_w116/2", "m_w126/3"]
A.setup(sys.argv[1], os.path.join(HERE, "skip.json"), PHOTOS, CLIPS, GENERIC, FALLBACK, [], reserved=RES)
A.THEME = "race"; A.CLIP_TARGET = 0.0; A.MAX_HOLD, A.KEEP = 12.0, 8.0
A.ARCHIVE_OK = True; A.STRICT_POOLS = True; A.SPLIT_BY_SUBJECT = True
chapters = []

c = ch("ch00_hook", 0.6)
c.at(0, photo("m_ds", 13, "in", cap="Citroën DS|París, 1955"))
c.at("Cuando se apaga el motor", P("dss"))
c.at("Ese auto era el Citroën DS", P("ds"))
c.at("La historia del automóvil", P("sl"))
c.at("Muchos de esos inventos los tienes", P("w126"))
c.at("Hoy vas a conocer", title("Llegaron 30 años antes", "inventos adelantados a su tiempo", "1953 – 1981", "ds"))
c.at("Y vas a descubrir quién", P("w111"))
chapters.append(c)

c = ch("ch01")
c.at(0, rank(8, "Frenos de disco", "m_ctype", 1, "Jaguar C-Type · 1953", "Le Mans"))
c.at("Hoy casi todos los autos tienen frenos", P("disco"))
c.at("El problema de los frenos de tambor", P("ctype"))
c.at("Y entonces llegó Jaguar", P("ctype"))
c.at("Aquella victoria demostró", P("ctype"))
c.at("El SEAT Seiscientos, el Vocho", P("disco"))
c.at("Número siete. El motor transversal", rank(7, "Motor transversal", "m_mini", 1, "Mini · 1959", "Alec Issigonis"))
c.at("Para entender este invento", P("mini"))
c.at("En el Reino Unido nace el Mini", P("mini"))
c.at("Issigonis colocó el motor de lado", P("minim"))
c.at("Hoy, casi todos los autos pequeños", P("mini"))
c.at("Y en España, por cierto", P("mini"))
chapters.append(c)

c = ch("ch02")
c.at(0, say("¿Desde dónde nos estás viendo?", "VIENDO", 120))
c.at("Y si todavía no estás suscrito", cta("Suscríbete", "historias de autos clásicos", tv=True))
c.at("Número seis. La inyección directa", P("sl"))
c.at("Pero hubo un auto que la tenía", rank(6, "Inyección directa", "m_300sl", 10, "Mercedes 300 SL · 1954", "con Bosch"))
c.at("¿Por qué no se usó en todos", P("sl"))
c.at("Número cinco. La zona de deformación", P("w111"))
c.at("Este es, quizá, uno de los inventos", P("bar"))
c.at("Durante mucho tiempo se pensó", P("w111"))
c.at("Según la oficina alemana de patentes", photo("m_w111", 9, "in", cap="Mercedes-Benz W111|1959 · zonas de deformación"))
c.at("Hoy, todos los autos del mundo", P("w111"))
chapters.append(c)

c = ch("ch03")
c.at(0, rank(4, "Suspensión hidroneumática", "m_dssusp", 8, "Citroën DS · 1955", "flotaba sobre esferas"))
c.at("Volvamos al auto del principio", P("ds"))
c.at("El resultado era una comodidad", P("dss"))
c.at("Ese mismo sistema hidráulico", P("ds"))
c.at("El DS se fabricó durante", stat("≈1.500.000", "Citroën DS vendidos (1955 – 1975)", "según las fuentes", count=False))
c.at("En Francia lo apodaron", P("ds"))
c.at("Número tres. Los faros que giran", rank(3, "Faros direccionales", "m_dsfaros", 1, "Citroën DS · años 60", "giraban con el volante"))
c.at("Este es otro invento", P("dsf"))
c.at("Era una idea brillante", P("dsf"))
chapters.append(c)

c = ch("ch04")
c.at(0, P("w116"))
c.at("¿Qué pasa cuando frenas", P("w116"))
c.at("El sistema antibloqueo", P("w116"))
c.at("La idea ya se había probado", P("w116"))
c.at("Pero según la historia de la marca, el primer auto", rank(2, "Frenos ABS", "m_w116", 2, "Mercedes Clase S · 1978", "con Bosch"))
c.at("Al principio era un extra", P("w116"))
c.at("Número uno. El airbag", rank(1, "Airbag", "m_w126", 3, "Mercedes Clase S · 1981", "W126"))
c.at("Y en el primer lugar", P("w126"))
c.at("La idea del airbag existía", P("w126"))
c.at("Según la historia de Mercedes-Benz", P("w126"))
chapters.append(c)

c = ch("ch05", 2.5)
c.at(0, P("w126"))
c.at("El cinturón de seguridad de tres puntos", P("volvo"))
c.at("En mil novecientos cincuenta y nueve, el ingeniero sueco", P("volvo"))
c.at("El turbo", P("930"))
c.at("Y el motor rotativo", P("ro80"))
c.at("Y le salió bien", P("787"))
c.at("La primera: el precio", P("sl"))
c.at("La segunda: la tecnología", P("w116"))
c.at("Y la tercera: las leyes", P("volvo"))
c.at("Así que la próxima vez", P("w126"))
c.at("Y ahora te pregunto a ti", P("ds"))
c.at("Y si has llegado hasta aquí", cta("Gracias por llegar al final", "suscríbete y déjame tu opinión", tv=True, remote=True))
chapters.append(c)

CTX = ["ds", "ctype", "sl", "ds", "w116", "w126"]
print(A.finish(chapters, "ES22_INVENTOS.mp4", CTX, subtitles="ES22.ass"))
