#!/usr/bin/env python3
"""CZ07 The weapons that saved Israel came from Prague. Footage first, AI fills gaps, 3 cards.
    python3 build_cz07.py <narration_dir> > episode.json   (run from the work folder; a/ = assets/cz07-izrael)
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "engine"))
import aus_kit as A
from aus_kit import P, ch, hf, cta

AI = lambda *n: ["ai:" + x for x in n]  # noqa: E731
PHOTOS = {
    "avia": ["avia199", "iaf_museum", "kbely"] + AI("ai_avia_flight", "ai_pilot_cockpit", "ai_dismantled_fighter", "ai_museum_avia"),
    "war": ["israel_1948", "haifa_1948"] + AI("ai_haganah_rifles", "ai_egypt_column"),
    "people": ["holocaust_ships", "ben_gurion"],
    "weapons": ["mauser_cz", "mg34"] + AI("ai_rifle_crates", "ai_ammo_crates"),
    "prague": ["praha_1948"] + AI("ai_negotiation"),
    "balak": ["zatec", "c54"] + AI("ai_zatec_night", "ai_plane_over_sea", "ai_onion_ship"),
    "spitfire": ["spitfire_cz"] + AI("ai_spitfire_longrange"),
    "training": AI("ai_training_cz"),
    "trial": ["slansky"] + AI("ai_courtroom_1952"),
    "later": ["havel_israel", "kbely", "iaf_museum"],
}
CLIPS = json.load(open(os.path.join(HERE, "clips.json")))
GENERIC = CLIPS.pop("_generic", [])
FALLBACK = {k: ["war", "weapons", "avia"] for k in PHOTOS}
A.setup(sys.argv[1], os.path.join(HERE, "skip.json"), PHOTOS, CLIPS, GENERIC, FALLBACK, ["war", "weapons", "avia"])
A.CLIP_TARGET, A.ARCHIVE_OK, A.SPLIT_BY_SUBJECT = 0.45, True, True
A.MAX_HOLD, A.KEEP = 11.0, 7.0
chapters = []

c = ch("ch00_hook", 0.6)
c.at(0, P("avia")); c.at("Ty samé letouny", P("avia")); c.at("Jenže na trupu nemají hákový kříž", P("avia"))
c.at("Letí zastavit egyptskou armádu", P("war")); c.at("Přišly z Československa", P("prague"))
c.at("Jak je možné", P("trial")); c.at("A jak se dostaly tisíce zbraní", P("balak")); c.at("Je to jeden z nejpřekvapivějších", P("weapons"))
c.at("Tohle je příběh zbraní", P("prague")); chapters.append(c)

c = ch("ch01")
c.at(0, P("war")); c.at("Židovská komunita v Palestině", P("war")); c.at("Do země přitom připlouvaly", P("people"))
c.at("A bylo jasné", P("war")); c.at("Získat zbraně přitom bylo", P("war")); c.at("Židovští vyslanci tak objížděli", P("prague"))
chapters.append(c)

c = ch("ch02")
c.at(0, P("prague")); c.at("Za prvé, mělo zbraně", P("weapons")); c.at("Za druhé, potřebovalo peníze", P("prague"))
c.at("A za třetí", P("prague")); c.at("V lednu devatenáct set čtyřicet osm", P("prague")); c.at("To je možná nejpřekvapivější", P("prague"))
c.at("Muž, který za židovskou stranu", P("prague")); c.at("Jenže koupit zbraně", P("balak")); chapters.append(c)

c = ch("ch03")
c.at(0, hf("g_list")); c.at("Základem byly pušky", P("weapons")); c.at("Dále kulomety", P("weapons"))
c.at("A pak přišlo to nejcennější", P("avia")); c.at("Izrael neměl žádné stíhačky", P("avia")); c.at("Výsledek byl podivný stroj", P("avia"))
c.at("Později přibyly i lepší letouny", P("spitfire")); c.at("Jejich přesun byl ještě odvážnější", P("spitfire"))
c.at("Ale jak dostat letadlo", P("balak")); chapters.append(c)

c = ch("ch04")
c.at(0, hf("g_map")); c.at("Na letišti v Žatci", P("balak")); c.at("Piloti byli směsice", P("balak"))
c.at("Obyvatelé Žatce", P("balak")); c.at("Stíhačky Avia se do dopravních", P("avia")); c.at("Další zbraně putovaly po moři", P("balak"))
c.at("Celá operace probíhala", P("balak")); c.at("Jenže zbraně tekly dál", P("war")); chapters.append(c)

c = ch("ch05")
c.at(0, cta("Odebírat", "příběhy zbraní, které změnily dějiny")); c.at("Čtrnáctého května", P("people"))
c.at("Egyptská armáda postupovala", P("war")); c.at("Dvacátého devátého května", P("avia")); c.at("Vojenský účinek útoku", P("avia"))
c.at("Do bojů mezitím šly", P("war")); c.at("David Ben Gurion později", P("people")); c.at("Jenže zatímco Izrael slavil", P("trial"))
chapters.append(c)

c = ch("ch06")
c.at(0, P("training")); c.at("Na československých letištích", P("avia")); c.at("Mezi cvičenci byli", P("training"))
c.at("Pak se ale situace začala měnit", P("prague")); c.at("Na začátku padesátých let", P("trial"))
c.at("Proces měl silně antisemitský", P("trial")); c.at("Jedenáct obžalovaných", P("trial")); chapters.append(c)

c = ch("ch07")
c.at(0, hf("g_timeline")); c.at("Samopaly, pušky, letadla", P("weapons")); c.at("Diplomatické vztahy se obnovily", P("later"))
c.at("Dnes patří Česká republika", P("later")); c.at("V izraelském leteckém muzeu", P("avia")); c.at("Jeden exemplář Avie", P("later"))
chapters.append(c)

c = ch("ch08", 2.5)
c.at(0, P("war")); c.at("Většina historiků se shoduje", P("weapons")); c.at("Ale motivy", P("prague"))
c.at("A přesto výsledek", P("trial")); c.at("Je to příběh plný ironie", P("avia"))
c.at("Teď je řada na vás", cta("Věděli jste to?", "napište do komentářů"))
c.at("A pokud vás zajímají další příběhy", cta("Odebírat", "nová videa každý týden")); chapters.append(c)

print(A.finish(chapters, "CZ07_izrael.mp4", ctx=["avia", "war", "prague", "weapons", "balak", "war", "trial", "later", "war"], subtitles="CZ07.ass"))
