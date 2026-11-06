#!/usr/bin/env python3
"""CZ01 Sa vz. 58 — why Czechoslovakia refused the Kalashnikov: full edit, shots anchored to phrases.
    python3 build_cz01.py <narration_dir> > episode.json   (run from the work folder; a/ = assets/cz01-vz58)
Look: reference channel (parchment & blueprint). Graphics are HyperFrames cards (a/hf/*.mp4, engine/hf_graphics.py);
footage = real photos (Commons/Openverse/LoC) + archive newsreels + AI scenes, never repeated, never black.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "engine"))
import aus_kit as A
from aus_kit import P, ch, hf, cta

AI = lambda *names: ["ai:" + n for n in names]  # noqa: E731
PHOTOS = {
    "vz58": ["vz58", "vz58_more", "vz58v", "museum_lesany", "weapons_museum"] + AI("ai_disassembled_vz58", "ai_museum_display"),
    "soldier": ["vz58_soldier", "czech_soldiers_vz58", "slovak_army", "czsl_army", "conscripts"] + AI("ai_soldier_march", "ai_conscripts_range", "ai_cleaning_rifle"),
    "army": ["czsl_army", "prague_parade", "conscripts", "cold_war_army"] + AI("ai_parade_1958", "ai_soldier_march", "ai_apc_crew"),
    "ak": ["ak47", "kalashnikov_museum", "soviet_army_parade"] + AI("ai_assembly_line_ak"),
    "pair": AI("ai_rifles_two_table", "ai_twins_silhouette", "ai_parts_mismatch", "ai_scale_weight"),
    "vz52": ["vz52", "ammo_762"] + AI("ai_vz52_render", "ai_rechamber_workshop", "ai_cartridges_compare"),
    "sa23": ["sa23", "uzi", "israel_1948_czech"],
    "bren": ["bren_zb26", "brno_zbrojovka"] + AI("ai_brno_factory_1930s", "ai_export_crates"),
    "brno": ["brno_city"] + AI("ai_konstrukta_office", "ai_engineer_drawing", "ai_designer_prototype", "ai_broom_corner"),
    "factory": ["cz_ub_factory", "uh_brod", "uh_brod_town"] + AI("ai_uh_brod_line", "ai_crates_rifles", "ai_pride_factory_gate"),
    "moscow": ["warsaw_pact", "soviet_army_parade", "cold_war_army"] + AI("ai_warsaw_1955", "ai_soviet_generals_map", "ai_supply_depot", "ai_archive_files"),
    "mech": ["vz58_more", "weapons_museum"] + AI("ai_rotating_bolt", "ai_locking_block", "ai_gas_piston", "ai_striker", "ai_empty_bolt_open", "ai_mud_test",
               "ai_magazine_closeup", "ai_stock_material", "ai_stripper_clip", "ai_bayonet", "ai_magazine_swap_fail") + ["walther_p38"],
    "variants": ["vz58v"] + AI("ai_paratrooper_folding", "ai_apc_crew"),
    "1968": ["prague_1968", "invasion_1968_more", "dubcek"] + AI("ai_tanks_night_border", "ai_prague_tanks_dawn", "ai_crowd_tank_flag", "ai_barracks_gate_closed",
                                 "ai_radio_1968", "ai_rifle_on_bunk", "ai_candles_memorial", "ai_soldier_window", "ai_barracks_rack"),
    "world": ["africa_rifle_70s"] + AI("ai_africa_patrol", "ai_jungle_patrol", "ai_news_photo", "ai_trade_ship"),
    "conscript": ["conscripts"] + AI("ai_conscripts_range", "ai_disassembly_timer", "ai_warehouse_racks", "ai_cleaning_rifle"),
    "split": ["velvet_1989", "velvet_more", "nato_1999"] + AI("ai_flag_split_1993"),
    "nato": ["cz805", "bren2", "czech_nato", "nato_1999"] + AI("ai_modern_rifle_render", "ai_modern_soldier"),
    "ukraine": ["ukraine_war", "ukraine_more"] + AI("ai_trucks_aid", "ai_trench_ukraine"),
    "civil": AI("ai_sport_shooter", "ai_collector_wall"),
    "end": AI("ai_sunset_soldier", "ai_museum_display", "ai_twins_silhouette"),
}
CLIPS = json.load(open(os.path.join(HERE, "clips.json")))
GENERIC = CLIPS.pop("_generic", [])
FALLBACK = {k: ["vz58", "soldier", "army"] for k in PHOTOS}
FALLBACK.update({"1968": ["army", "soldier"], "moscow": ["army"], "world": ["soldier", "vz58"], "ukraine": ["nato", "soldier"],
                 "mech": ["vz58", "pair"], "pair": ["vz58", "mech"], "brno": ["factory", "bren"], "factory": ["brno", "vz58"]})
A.setup(sys.argv[1], os.path.join(HERE, "skip.json"), PHOTOS, CLIPS, GENERIC, FALLBACK, ["vz58", "soldier", "army"])
A.CLIP_TARGET = 0.45   # owner 06/11: footage first (photos + clips); only 4 essential cards
A.MAX_HOLD, A.KEEP = 9.0, 6.0
A.ARCHIVE_OK = True
A.SPLIT_BY_SUBJECT = True
chapters = []

# ---------------------------------------------------------------- hook: August 1968, nobody fires
c = ch("ch00_hook", 0.6)
c.at(0, P("1968"))
c.at("Přes hranice Československa se valí tanky", P("1968"))
c.at("Statisíce vojáků", P("1968"))
c.at("Ve skladech a kasárnách", P("1968"))
c.at("A nikdo nevystřelí", P("1968"))
c.at("Ta zbraň, kterou ti vojáci drželi", P("vz58"))
c.at("Polsko, Maďarsko", P("ak"))
c.at("Jen Praha řekla ne", P("army"))
c.at("Místo toho postavili inženýři z Brna", P("brno"))
c.at("Na první pohled vypadá jako kalašnikov", P("pair"))
c.at("Jenže stačí ho rozebrat", P("mech"))
c.at("Tak proč si malá země", hf("g_map_cs"))
c.at("Co přesně se skrývá pod krytem", P("mech"))
c.at("A proč tenhle samopal", P("ukraine"))
c.at("Na konci se dostaneme", P("pair"))
c.at("Tohle je příběh samopalu", P("vz58"))
chapters.append(c)

# ---------------------------------------------------------------- 1955: Moscow wants one rifle
c = ch("ch01")
c.at(0, P("moscow"))
c.at("A Moskva chtěla jednu věc", P("moscow"))
c.at("Logistika vyhrává války", P("moscow"))
c.at("Jenže Československo nebylo", P("bren"))
c.at("Lehký kulomet z Brna si dokonce koupila", P("bren"))
c.at("Krátce po válce vznikla v Československu řada samopalů", P("sa23"))
c.at("Pokud vám to něco připomíná", P("sa23"))
c.at("Hned po válce se proto", P("vz52"))
c.at("A tady přichází první střet", P("moscow"))
c.at("Praha nakonec ustoupila", P("vz52"))
c.at("Jenže u náboje ústupky skončily", P("army"))
chapters.append(c)

# ---------------------------------------------------------------- Brno, project "Koště"
c = ch("ch02")
c.at(0, P("ak"))
c.at("Československo se rozhodlo jinak", P("brno"))
c.at("Zadání znělo jednoduše", P("brno"))
c.at("Podle dobových pramenů dostal projekt", P("brno"))
c.at("Proč ale Praha prostě nevzala kalašnikov", P("ak"))
c.at("Za prvé, hrdost", P("factory"))
c.at("Za druhé, peníze", P("world"))
c.at("A za třetí", P("brno"))
c.at("Měli pravdu", P("vz58"))
chapters.append(c)

# ---------------------------------------------------------------- inside the action
c = ch("ch03")
c.at(0, P("vz58"))
c.at("Položme vedle sebe", P("pair"))
c.at("Začněme tím, co rozhoduje", P("mech"))
c.at("Čermák šel úplně jinou cestou", P("mech"))
c.at("Podobný princip se objevil", P("mech"))
c.at("Druhý rozdíl", P("mech"))
c.at("Třetí rozdíl", P("mech"))
c.at("A čtvrtý", P("mech"))
c.at("Výsledek? Zbraň vážila", hf("g_compare"))
c.at("Jenže lehčí zbraň má i svou cenu", P("soldier"))
chapters.append(c)

# ---------------------------------------------------------------- 1958: in service
c = ch("ch04")
c.at(0, P("army"))
c.at("Výroba se rozjela v Uherském Brodě", P("factory"))
c.at("Až do roku devatenáct set osmdesát čtyři", hf("g_spec"))
c.at("Armáda dostala několik verzí", P("variants"))
c.at("Pažby se zpočátku vyráběly", P("mech"))
c.at("Konstruktéři mysleli i na drobnosti", P("mech"))
c.at("Jak se se zbraní sloužilo", P("soldier"))
c.at("Zásobníky z lehké slitiny", P("mech"))
c.at("A pak tu byla otázka spolehlivosti", P("mech"))
c.at("Jenže skutečná zkouška", P("1968"))
chapters.append(c)

# ---------------------------------------------------------------- mid CTA + August 1968
c = ch("ch05")
c.at(0, cta("Odebírat", "příběhy zbraní, které změnily dějiny"))
c.at("A teď zpátky do srpna", P("1968"))
c.at("překročila hranice Československa", P("1968"))
c.at("Stejní spojenci", P("1968"))
c.at("Československá armáda v té době", P("1968"))
c.at("Politické vedení chtělo", P("1968"))
c.at("Je to zvláštní paradox", P("1968"))
c.at("Na ulicích se přitom umíralo", P("1968"))
c.at("Pro samopal vzor padesát osm to ale nebyl konec", P("world"))
chapters.append(c)

# ---------------------------------------------------------------- export, conscripts, 1993
c = ch("ch06")
c.at(0, P("world"))
c.at("A tak se samopaly vzor padesát osm dostaly", P("world"))
c.at("Pro obchodníky se zbraněmi", P("world"))
c.at("Doma mezitím sloužila dál", P("conscript"))
c.at("Kdo sloužil, ten si pamatuje", P("conscript"))
c.at("Výroba skončila v roce", P("conscript"))
c.at("O pět let později padl komunistický režim", P("split"))
c.at("Česká i slovenská armáda", P("soldier"))
c.at("Česká republika vstoupila do NATO", P("nato"))
chapters.append(c)

# ---------------------------------------------------------------- BREN, Ukraine, civilians
c = ch("ch07")
c.at(0, P("nato"))
c.at("Nová puška střílí náboj NATO", P("nato"))
c.at("O několik let později přišla", P("nato"))
c.at("Mnozí čekali", P("vz58"))
c.at("V únoru dva tisíce dvacet dva", P("ukraine"))
c.at("Na fotografiích z ukrajinské fronty", P("ukraine"))
c.at("Historie se tak", hf("g_timeline_life"))
c.at("Civilní poloautomatické verze", P("civil"))
c.at("Proč vlastně ta zbraň nikdy nezmizela", P("vz58"))
c.at("Je to vůbec kopie kalašnikova", P("pair"))
chapters.append(c)

# ---------------------------------------------------------------- verdict + end CTA
c = ch("ch08", 2.5)
c.at(0, P("pair"))
c.at("Vezměte samopal vzor padesát osm", P("mech"))
c.at("Navenek dvojčata", P("pair"))
c.at("A to nebyla náhoda", P("army"))
c.at("Byla lepší než kalašnikov", P("pair"))
c.at("Vraťme se ještě ke třem otázkám", P("vz58"))
c.at("Jisté je jedno", P("end"))
c.at("Teď je řada na vás", cta("Vz. 58, nebo kalašnikov?", "napište do komentářů"))
c.at("A pokud chcete vidět další příběhy", cta("Odebírat", "příště: CZ 75"))
chapters.append(c)

print(A.finish(chapters, "CZ01_vz58.mp4", ctx=["1968", "moscow", "brno", "mech", "army", "1968", "world", "nato", "pair"],
               subtitles="CZ01.ass"))
