#!/usr/bin/env python3
"""CZ04 Bren — how a Czechoslovak machine gun became a British legend: full edit, shots anchored to phrases.
    python3 build_cz04.py <narration_dir> > episode.json   (run from the work folder; a/ = assets/cz04-bren)
Footage first, AI (Replicate) only fills gaps, always last in each pool; 3 HyperFrames cards.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "engine"))
import aus_kit as A
from aus_kit import P, ch, hf, cta

AI = lambda *names: ["ai:" + n for n in names]  # noqa: E731
PHOTOS = {
    "bren": ["bren", "bren_l4", "museum_mg"] + AI("ai_top_magazine", "ai_barrel_change", "ai_museum_bren"),
    "war": ["bren_ww2", "normandy", "bren_desert", "bren_burma", "bren_carrier"] + AI("ai_desert_gunner", "ai_jungle_gunner", "ai_normandy_hedge"),
    "zb": ["zb26", "holek", "museum_mg", "x_bren_zb26", "x_weapons_museum", "x_sa23", "x_vz27"] + AI("ai_holek_workshop"),
    "brno": ["zbrojovka_brno", "brno_old", "czech_bunker", "x_brno_zbrojovka", "x_brno_city", "x_czsl_army"] + AI("ai_brno_factory_1920s"),
    "uk": ["enfield", "lewis_gun", "bren_girl", "x_hi_power"] + AI("ai_trials_england", "ai_contract_1935", "ai_enfield_line", "ai_canada_women"),
    "dunkirk": ["dunkirk", "dunkirk_1945", "czech_exile"] + AI("ai_dunkirk_beach", "ai_exile_camp", "ai_dunkirk_siege", "ai_resistance_drop"),
    "occupation": ["protectorate", "czech_bunker", "x_cold_war_army", "x_conscripts"] + AI("ai_protectorate_factory", "ai_sabotage"),
    "late": ["bren_l4", "falklands", "cz_bren"] + AI("ai_falklands", "ai_reenactors"),
}
CLIPS = json.load(open(os.path.join(HERE, "clips.json")))
GENERIC = CLIPS.pop("_generic", [])
FALLBACK = {k: ["war", "bren", "zb"] for k in PHOTOS}
A.setup(sys.argv[1], os.path.join(HERE, "skip.json"), PHOTOS, CLIPS, GENERIC, FALLBACK, ["war", "bren", "zb"])
A.CLIP_TARGET = 0.45
A.MAX_HOLD, A.KEEP = 12.0, 8.0
A.ARCHIVE_OK = True
A.SPLIT_BY_SUBJECT = True
chapters = []

c = ch("ch00_hook", 0.6)
c.at(0, P("dunkirk"))
c.at("A na písku za sebou", P("dunkirk"))
c.at("O pár let později", P("war"))
c.at("Stane se jedním ze symbolů", P("war"))
c.at("Jenže tahle britská legenda", P("brno"))
c.at("Jak se stalo", P("zb"))
c.at("A jak je možné", P("occupation"))
c.at("Je to příběh", P("bren"))
c.at("Tohle je příběh kulometu", P("bren"))
chapters.append(c)

c = ch("ch01")
c.at(0, P("brno"))
c.at("V Brně proto vzniká", P("brno"))
c.at("Narodil se koncem", P("zb"))
c.at("Holek byl samouk", P("zb"))
c.at("První světová válka ukázala", P("uk"))
c.at("Holek chtěl postavit", P("zb"))
c.at("Výsledkem byl lehký kulomet", P("zb"))
chapters.append(c)

c = ch("ch02")
c.at(0, P("zb"))
c.at("Zásobník se nasazoval shora", P("zb"))
c.at("Největší předností ale byla hlaveň", P("bren"))
c.at("A pak tu byla kvalita výroby", P("brno"))
c.at("Zbrojovka začala kulomet nabízet", P("zb"))
c.at("V Číně se kulomety", P("zb"))
c.at("Doma mezitím", P("occupation"))
c.at("Na začátku třicátých let", P("uk"))
chapters.append(c)

c = ch("ch03")
c.at(0, P("uk"))
c.at("Mezi nimi dánský Madsen", P("uk"))
c.at("Českoslovenští konstruktéři do Anglie", P("zb"))
c.at("Jenže tu byl jeden problém", P("bren"))
c.at("Zbrojovka proto musela", P("bren"))
c.at("V roce devatenáct set třicet pět", P("uk"))
c.at("A tady vzniklo jméno", hf("g_name"))
c.at("V roce devatenáct set třicet sedm", hf("g_spec"))
chapters.append(c)

c = ch("ch04")
c.at(0, P("war"))
c.at("Britští vojáci si ho rychle", P("war"))
c.at("V britské pěchotní četě", P("war"))
c.at("Jméno Bren se dokonce", P("war"))
c.at("Pak přišel rok", P("dunkirk"))
c.at("Výroba se proto musela", P("uk"))
c.at("V kanadské továrně", P("uk"))
c.at("Bren se tak během pár let", P("war"))
chapters.append(c)

c = ch("ch05")
c.at(0, cta("Odebírat", "příběhy zbraní, které změnily dějiny"))
c.at("Patnáctého března", P("occupation"))
c.at("Pro nacistické Německo", P("occupation"))
c.at("Vznikla tak jedna z nejpodivnějších", P("brno"))
c.at("Mnoho českých dělníků", P("occupation"))
c.at("A pak tu byla ještě jedna skupina", P("dunkirk"))
chapters.append(c)

c = ch("ch06")
c.at(0, P("dunkirk"))
c.at("Pro mnoho z nich", P("bren"))
c.at("V letech devatenáct set čtyřicet čtyři", P("dunkirk"))
c.at("Bren mezitím bojoval", P("war"))
c.at("Breny dostávaly i exilové", P("war"))
c.at("Dokonce i Němci", P("war"))
c.at("Do konce války", P("bren"))
c.at("Jenže válka skončila", P("late"))
chapters.append(c)

c = ch("ch07")
c.at(0, P("late"))
c.at("Britové ale svůj Bren", P("late"))
c.at("A Bren dál bojoval", hf("g_timeline"))
c.at("Teprve v devadesátých letech", P("late"))
c.at("Dnes jsou Breny", P("bren"))
c.at("A co jeho domov", P("late"))
c.at("Jméno, které vzniklo z Brna", P("brno"))
chapters.append(c)

c = ch("ch08", 2.5)
c.at(0, P("zb"))
c.at("Britové si nevybrali Bren", P("war"))
c.at("Je v tom zvláštní ironie", P("occupation"))
c.at("A čeští vojáci v exilu", P("dunkirk"))
c.at("Dnes najdete Bren", P("bren"))
c.at("Teď je řada na vás", cta("Věděli jste to?", "napište do komentářů"))
c.at("A pokud vás zajímají další příběhy", cta("Odebírat", "příště: proč vz. 58 odchází"))
chapters.append(c)

print(A.finish(chapters, "CZ04_bren.mp4", ctx=["bren", "zb", "zb", "uk", "war", "occupation", "dunkirk", "late", "bren"],
               subtitles="CZ04.ass"))
