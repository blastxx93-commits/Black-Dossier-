#!/usr/bin/env python3
"""CZ05 Vz. 58 — why the Czech army started replacing it: full edit, shots anchored to phrases.
    python3 build_cz05.py <narration_dir> > episode.json   (run from the work folder; a/ = assets/cz05-vz58-nahrada)
Hook opens in action (illustrative Afghanistan scene). Footage first, AI only fills gaps; 3 HyperFrames cards.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "engine"))
import aus_kit as A
from aus_kit import P, ch, hf, cta

AI = lambda *names: ["ai:" + n for n in names]  # noqa: E731
PHOTOS = {
    "afghan": ["acr_afghanistan", "acr_iraq"] + AI("ai_logar_road", "ai_ally_hand", "ai_base_afghan", "ai_heavy_rifle"),
    "mag": ["ammo_556", "ammo_762"] + AI("ai_mag_mismatch"),
    "vz58": ["vz58", "vz58_mod", "museum_vz58", "x_vz58_more", "x_vz58_soldier", "x_conscripts", "x_czsl_army"] + AI("ai_old_rifles_rack", "ai_worn_rifle"),
    "nato": ["nato_1999", "acr_kosovo", "acr_training"] + AI("ai_soldier_gear"),
    "army": ["acr_training", "acr_kosovo", "x_czech_soldiers_vz58", "x_slovak_army", "x_czech_nato"] + AI("ai_soldier_gear", "ai_handover"),
    "bren": ["cz805", "bren2", "optics", "x_cz805", "x_bren2"] + AI("ai_new_rifles_crates"),
    "factory": ["uh_brod", "colt"] + AI("ai_factory_modern", "ai_design_cad", "ai_meeting_ministry", "ai_feedback"),
    "abroad": ["hungary", "grot"],
    "ukraine": ["ukraine", "x_ukraine_war", "x_ukraine_more"] + AI("ai_trucks_ukraine", "ai_trench_vz58", "ai_reserve_storage"),
    "end": AI("ai_sunset_two_rifles", "ai_handover"),
}
CLIPS = json.load(open(os.path.join(HERE, "clips.json")))
GENERIC = CLIPS.pop("_generic", [])
FALLBACK = {k: ["army", "vz58", "bren"] for k in PHOTOS}
A.setup(sys.argv[1], os.path.join(HERE, "skip.json"), PHOTOS, CLIPS, GENERIC, FALLBACK, ["army", "vz58", "bren"])
A.CLIP_TARGET = 0.45
A.MAX_HOLD, A.KEEP = 11.0, 7.0
A.ARCHIVE_OK = True
A.SPLIT_BY_SUBJECT = True
chapters = []

# hook: fast cuts, straight into the action
c = ch("ch00_hook", 0.6)
c.at(0, P("afghan"))
c.at("Hlídka spojeneckých vojáků", P("afghan"))
c.at("Američan vedle českého vojáka", P("afghan"))
c.at("Potřebuje munici", P("mag"))
c.at("Český voják mu podá", P("mag"))
c.at("Jiný náboj", P("mag"))
c.at("Přesně ta zbraň", P("vz58"))
c.at("Tahle scéna je jen ilustrace", P("afghan"))
c.at("Samopal vzor padesát osm byl kdysi chloubou", P("vz58"))
c.at("Varšavská smlouva se rozpadla", P("nato"))
c.at("A najednou se z legendy stal problém", P("vz58"))
c.at("Proč musela česká armáda", P("army"))
c.at("A proč se náhrada", P("bren"))
c.at("Na konci se podíváme", P("ukraine"))
c.at("Tohle je příběh o tom", P("vz58"))
chapters.append(c)

c = ch("ch01")
c.at(0, P("nato"))
c.at("Jenže vstup do NATO", P("nato"))
c.at("A tady byl problém", P("vz58"))
c.at("Armády NATO používaly jiný náboj", P("mag"))
c.at("Na papíře to nemusel být", P("army"))
c.at("Čeští vojáci sloužili v Bosně", P("afghan"))
c.at("Osmapadesátka, která vznikla", P("vz58"))
chapters.append(c)

c = ch("ch02")
c.at(0, hf("g_problems"))
c.at("Prvním problémem byla munice", P("mag"))
c.at("Druhým problémem bylo příslušenství", P("bren"))
c.at("Osmapadesátka žádné kolejnice", P("vz58"))
c.at("Třetím problémem bylo stáří", P("vz58"))
c.at("A čtvrtým problémem byla ergonomie", P("army"))
c.at("Žádný z těch problémů", P("army"))
chapters.append(c)

c = ch("ch03")
c.at(0, P("factory"))
c.at("Některé elitní jednotky", P("army"))
c.at("Řada lidí v armádě", P("factory"))
c.at("Kolem výběru nové zbraně", P("factory"))
c.at("Česká zbrojovka proto začala", P("factory"))
c.at("Zajímavostí bylo", P("bren"))
c.at("Kolem roku dva tisíce devět", P("bren"))
c.at("Jméno odkazovalo", P("bren"))
c.at("Jenže začátky nové pušky", P("afghan"))
chapters.append(c)

c = ch("ch04")
c.at(0, P("bren"))
c.at("Podle dobových zpráv", P("afghan"))
c.at("Objevily se i výtky", P("bren"))
c.at("Je potřeba říct", P("army"))
c.at("Čeští vojáci si mezitím", P("army"))
c.at("Česká zbrojovka zareagovala", P("factory"))
c.at("A zatímco se v Uherském Brodě", P("vz58"))
chapters.append(c)

c = ch("ch05")
c.at(0, cta("Odebírat", "příběhy zbraní, které změnily dějiny"))
c.at("V roce dva tisíce šestnáct", P("bren"))
c.at("Pro českou armádu to byl", P("army"))
c.at("A tady přichází zajímavý obrat", P("abroad"))
c.at("Česká zbrojovka se tak", P("factory"))
c.at("Ale co se stalo s osmapadesátkami", P("vz58"))
c.at("Odpověď přišla v únoru", P("ukraine"))
chapters.append(c)

c = ch("ch06")
c.at(0, P("ukraine"))
c.at("Ukrajina potřebovala zbraně", P("ukraine"))
c.at("Najednou se ukázalo", P("mag"))
c.at("Na fotografiích z ukrajinské fronty", P("ukraine"))
c.at("Ukrajinští vojáci podle", P("ukraine"))
c.at("Je v tom zvláštní historická symetrie", hf("g_timeline"))
c.at("Doma mezitím osmapadesátky", P("vz58"))
chapters.append(c)

c = ch("ch07")
c.at(0, P("vz58"))
c.at("Jenže to by byl omyl", P("vz58"))
c.at("Byla navržena pro armádu", P("vz58"))
c.at("Česká armáda ale dnes žije", hf("g_compare"))
c.at("Česká republika přitom nebyla jediná", P("abroad"))
c.at("Je to podobné", P("end"))
c.at("A je tu ještě jedna věc", P("factory"))
chapters.append(c)

c = ch("ch08", 2.5)
c.at(0, P("vz58"))
c.at("Protože střílel jiný náboj", P("mag"))
c.at("Náhrada ale nebyla jednoduchá", P("bren"))
c.at("Je to příběh o tom", P("end"))
c.at("Možná za padesát let", P("bren"))
c.at("Teď je řada na vás", cta("Vz. 58, nebo BREN?", "napište do komentářů"))
c.at("A pokud chcete vidět další příběhy", cta("Odebírat", "příště: Dragunov SVD"))
chapters.append(c)

print(A.finish(chapters, "CZ05_vz58_nahrada.mp4", ctx=["vz58", "nato", "vz58", "factory", "bren", "bren", "ukraine", "vz58", "vz58"],
               subtitles="CZ05.ass"))
