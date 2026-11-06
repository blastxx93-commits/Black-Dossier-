#!/usr/bin/env python3
"""CZ02 CZ 75 — why manufacturers all over the world copied it: full edit, shots anchored to phrases.
    python3 build_cz02.py <narration_dir> > episode.json   (run from the work folder; a/ = assets/cz02-cz75)
Footage first (real photos + clips), AI only fills gaps (always last in each pool), 3 HyperFrames cards.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "engine"))
import aus_kit as A
from aus_kit import P, ch, hf, cta

AI = lambda *names: ["ai:" + n for n in names]  # noqa: E731
PHOTOS = {
    "cz75": ["cz75", "cz75_field", "cz75_compact"] + AI("ai_frame_rails", "ai_low_bore", "ai_magazine15"),
    "design": ["cz75_field"] + AI("ai_brothers_office", "ai_drafting_pistol", "ai_prototype_bench", "ai_test_range_70s"),
    "factory": ["cz_factory", "uh_brod"] + AI("ai_assembly_70s", "ai_factory_90s"),
    "east": ["vz52_pistol", "makarov", "vz82", "vz27"],
    "west": ["hi_power", "ammo_9mm"] + AI("ai_revolver_vs"),
    "cold": ["prague_70s"] + AI("ai_customs_border", "ai_hard_currency", "ai_export_crates"),
    "usa": ["gun_show", "jeff_cooper"] + AI("ai_us_gun_store", "ai_gun_magazine_70s"),
    "clones": ["tanfoglio", "jericho", "sphinx", "canik", "nz75"] + AI("ai_italy_workshop", "ai_swiss_precision", "ai_world_map_pins", "ai_patent_office"),
    "sport": ["ipsc", "cz_shadow"] + AI("ai_shooter_competition", "ai_medals", "ai_collector_case"),
    "modern": ["cz_p07", "cz75_compact", "police_cz", "czech_army_pistol", "colt"] + AI("ai_police_holster", "ai_hartford"),
    "1989": ["velvet"] + AI("ai_velvet_keys"),
}
CLIPS = json.load(open(os.path.join(HERE, "clips.json")))
GENERIC = CLIPS.pop("_generic", [])
FALLBACK = {k: ["cz75", "sport", "clones"] for k in PHOTOS}
A.setup(sys.argv[1], os.path.join(HERE, "skip.json"), PHOTOS, CLIPS, GENERIC, FALLBACK, ["cz75", "sport", "clones"])
A.CLIP_TARGET = 0.45
A.MAX_HOLD, A.KEEP = 11.0, 7.0
A.ARCHIVE_OK = True
A.SPLIT_BY_SUBJECT = True
chapters = []

c = ch("ch00_hook", 0.6)
c.at(0, P("cold"))
c.at("A právě tady, v zbrojovce", P("factory"))
c.at("Američtí instruktoři", P("usa"))
c.at("Sportovní střelci", P("sport"))
c.at("A výrobci od Itálie", P("clones"))
c.at("Jenže je tu háček", P("east"))
c.at("Pistole z Uherského Brodu byla od začátku", P("cz75"))
c.at("Tak pro koho vlastně vznikla", P("cz75"))
c.at("A proč se proti všem těm kopiím", P("clones"))
c.at("Tohle je příběh pistole", P("cz75"))
chapters.append(c)

c = ch("ch01")
c.at(0, P("east"))
c.at("V ostatních zemích bloku", P("east"))
c.at("Na Západě se ale střílelo jinak", P("west"))
c.at("Přitom Československo mělo", P("east"))
c.at("A Československo prodávat chtělo", P("cold"))
c.at("Zbrojovky to dělaly už před válkou", P("factory"))
c.at("Na konci šedesátých let", P("design"))
chapters.append(c)

c = ch("ch02")
c.at(0, P("design"))
c.at("Teď ale dostali úkol", P("design"))
c.at("Za vzor si vzali", P("west"))
c.at("Nová pistole měla mít zásobník", P("cz75"))
c.at("Vývoj trval několik let", P("design"))
c.at("V roce devatenáct set sedmdesát pět byla pistole hotová", hf("g_spec"))
c.at("Na první pohled to byla elegantní", P("cz75"))
chapters.append(c)

c = ch("ch03")
c.at(0, P("cz75"))
c.at("CZ sedmdesát pět to má obráceně", P("cz75"))
c.at("Proč na tom záleží", P("cz75"))
c.at("K tomu přidejte ergonomii", P("sport"))
c.at("Pak je tu zásobník", hf("g_compare"))
c.at("A nakonec spoušť", P("cz75"))
c.at("Celá pistole byla z oceli", P("cz75"))
c.at("Jenže kvalitní konstrukce nestačí", P("cold"))
chapters.append(c)

c = ch("ch04")
c.at(0, P("cold"))
c.at("Ve Spojených státech", P("usa"))
c.at("Dnes jsou mezi sběrateli", P("sport"))
c.at("A přesto, nebo možná právě proto", P("usa"))
c.at("Ještě zajímavější je, co se dělo doma", P("east"))
c.at("Pro komunistické hospodářství", P("cold"))
c.at("A vydělával", P("clones"))
chapters.append(c)

c = ch("ch05")
c.at(0, cta("Odebírat", "příběhy zbraní, které změnily dějiny"))
c.at("Tady je ta nejpodivnější kapitola", P("clones"))
c.at("Jak je to možné", P("cold"))
c.at("A přesně to se stalo", P("clones"))
c.at("Ve Spojených státech se tyto italské", P("usa"))
c.at("Na italský základ navázal Izrael", P("clones"))
c.at("Ve Švýcarsku vznikla", P("clones"))
c.at("Odhaduje se, že po světě", hf("g_clones"))
c.at("Česká zbrojovka se dívala", P("factory"))
chapters.append(c)

c = ch("ch06")
c.at(0, P("clones"))
c.at("Prvním důvodem", P("cz75"))
c.at("Druhým důvodem", P("usa"))
c.at("Třetím důvodem", P("factory"))
c.at("A čtvrtým důvodem byl sport", P("sport"))
c.at("Na velkých mezinárodních soutěžích", P("sport"))
c.at("A pak tu byli sběratelé", P("sport"))
c.at("Zajímavé je, že kopie", P("clones"))
c.at("Jenže aby se k originálu", P("1989"))
chapters.append(c)

c = ch("ch07")
c.at(0, P("1989"))
c.at("Česká zbrojovka v Uherském Brodě se během", P("factory"))
c.at("Pistole se konečně začala", P("sport"))
c.at("A doma", P("modern"))
c.at("Jedna z policejních verzí", P("modern"))
c.at("Česká zbrojovka mezitím rostla", P("modern"))
c.at("Zbrojovka z malého moravského města", P("factory"))
chapters.append(c)

c = ch("ch08", 2.5)
c.at(0, P("cz75"))
c.at("Protože byla dobrá", P("cz75"))
c.at("Protože ji Západ chtěl", P("usa"))
c.at("A protože ji nikdo neochránil", P("clones"))
c.at("Je v tom zvláštní ironie", P("cold"))
c.at("Dnes, po padesáti letech", P("modern"))
c.at("Teď je řada na vás", cta("Stříleli jste z CZ 75?", "napište do komentářů"))
c.at("A pokud vás zajímají další příběhy", cta("Odebírat", "příště: Škorpion vz. 61"))
chapters.append(c)

print(A.finish(chapters, "CZ02_cz75.mp4", ctx=["cz75", "east", "design", "cz75", "cold", "clones", "sport", "modern", "cz75"],
               subtitles="CZ02.ass"))
