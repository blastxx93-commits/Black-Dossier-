#!/usr/bin/env python3
"""CZ06 Dragunov — not built for snipers, built for something worse. Footage first, AI fills gaps, 3 cards.
    python3 build_cz06.py <narration_dir> > episode.json   (run from the work folder; a/ = assets/cz06-dragunov)
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "engine"))
import aus_kit as A
from aus_kit import P, ch, hf, cta

AI = lambda *n: ["ai:" + x for x in n]  # noqa: E731
PHOTOS = {
    "svd": ["svd", "museum_svd", "pso1"] + AI("ai_bayonet_svd", "ai_scope_view", "ai_cartridges_long"),
    "squad": ["svd_soldier", "soviet_army"] + AI("ai_squad_btr", "ai_marksman_attack"),
    "plan": ["soviet_army", "sniper_ww2"] + AI("ai_soviet_planners", "ai_machinegun_nest"),
    "design": ["dragunov_person", "izhevsk", "mosin"] + AI("ai_izhevsk_factory", "ai_test_snow", "ai_target_shooter"),
    "afghan": ["svd_afghan"] + AI("ai_afghan_ridge", "ai_mujahideen_ridge"),
    "world": ["type79", "psl"],
    "cz": ["czech_svd"] + AI("ai_csla_range"),
    "ukraine": ["ukraine_svd"] + AI("ai_ukraine_trench"),
    "west": ["dmr"] + AI("ai_two_doctrines"),
}
CLIPS = json.load(open(os.path.join(HERE, "clips.json")))
GENERIC = CLIPS.pop("_generic", [])
FALLBACK = {k: ["svd", "squad", "plan"] for k in PHOTOS}
A.setup(sys.argv[1], os.path.join(HERE, "skip.json"), PHOTOS, CLIPS, GENERIC, FALLBACK, ["svd", "squad", "plan"])
A.CLIP_TARGET, A.ARCHIVE_OK, A.SPLIT_BY_SUBJECT = 0.45, True, True
A.MAX_HOLD, A.KEEP = 11.0, 7.0
chapters = []

c = ch("ch00_hook", 0.6)
c.at(0, P("svd")); c.at("Odstřelovač leží schovaný", P("plan")); c.at("Jenže sovětská puška Dragunov bodák má", P("svd"))
c.at("Na Západě se o ní dlouho", P("squad")); c.at("Byl postaven pro něco jiného", P("squad"))
c.at("Co přesně Sověti", P("plan")); c.at("A proč ji armády po celém světě", P("ukraine"))
c.at("A na konci se podíváme", P("cz")); c.at("Tohle je příběh pušky", P("svd")); chapters.append(c)

c = ch("ch01")
c.at(0, P("plan")); c.at("Počítalo se s tím", P("squad")); c.at("V takové válce nebyl čas", P("plan"))
c.at("Zároveň se ale vojenští plánovači", P("squad")); c.at("Sovětské družstvo tak mohlo", P("plan"))
c.at("Armáda proto chtěla", P("squad")); c.at("A úkol postavit ji dostal", P("design")); chapters.append(c)

c = ch("ch02")
c.at(0, P("design")); c.at("Dragunov se nejdřív proslavil", P("design")); c.at("Na konci padesátých let", P("design"))
c.at("Mezi soupeři byl", P("design")); c.at("Hlavní problém byl", P("svd")); c.at("Dragunovovi se podle mnoha", hf("g_spec"))
c.at("Ale pozor na to slovo", P("svd")); chapters.append(c)

c = ch("ch03")
c.at(0, P("svd")); c.at("Dragunov je samonabíjecí puška", P("svd")); c.at("Střílí silný puškový náboj", P("design"))
c.at("Mechanismus vychází", P("svd")); c.at("Nejvýraznějším prvkem je pažba", P("svd")); c.at("A pak tu je zaměřovač", P("svd"))
c.at("A nakonec bodák", P("svd")); c.at("Bodák na odstřelovací pušce", P("squad")); chapters.append(c)

c = ch("ch04")
c.at(0, P("squad")); c.at("Sovětská armáda ho nerozdávala", P("squad")); c.at("Tenhle muž nebyl", P("squad"))
c.at("Výcvik takového střelce", P("squad")); c.at("A teď si položte otázku", P("plan")); c.at("Ne na náhodné vojáky", P("plan"))
c.at("Dnes by se o takovém střelci", P("west")); c.at("A v tom je to něco horšího", hf("g_compare")); c.at("Jenže jak se tahle teorie", P("afghan"))
chapters.append(c)

c = ch("ch05")
c.at(0, cta("Odebírat", "příběhy zbraní, které změnily dějiny")); c.at("Velká válka v Evropě", P("afghan"))
c.at("Sovětská armáda tam", P("afghan")); c.at("Ironií je", P("afghan")); c.at("Dragunov se mezitím rozšířil", P("world"))
c.at("Na fotografiích z Blízkého východu", P("world")); c.at("A Dragunov se dostal i do Československa", P("cz")); chapters.append(c)

c = ch("ch06")
c.at(0, P("cz")); c.at("Proč? Vývoj přesné", P("cz")); c.at("Českoslovenští vojáci ji používali", P("cz"))
c.at("Po roce devatenáct set osmdesát devět", P("cz")); c.at("Zajímavé je, jak dlouho", hf("g_timeline"))
c.at("Rusko se ji mezitím", P("svd")); c.at("Proč? Co je na něm", P("svd")); chapters.append(c)

c = ch("ch07")
c.at(0, P("west")); c.at("Jenže Dragunov měl jiné přednosti", P("svd")); c.at("Dragunov tak není zbraní", P("squad"))
c.at("Západ dlouho vsázel", P("west")); c.at("Které pojetí bylo lepší", P("west")); c.at("Takže když se dnes podíváte", P("west"))
chapters.append(c)

c = ch("ch08", 2.5)
c.at(0, P("svd")); c.at("Ne pro osamělého odstřelovače", P("squad")); c.at("To je to něco horšího", P("plan"))
c.at("Sovětští plánovači pochopili", P("plan")); c.at("Dragunov tak není jen puška", P("svd"))
c.at("Teď je řada na vás", cta("Setkali jste se s Dragunovem?", "napište do komentářů"))
c.at("A pokud vás zajímají další příběhy", cta("Odebírat", "příště: zbraně pro Izrael")); chapters.append(c)

print(A.finish(chapters, "CZ06_dragunov.mp4", ctx=["svd", "plan", "design", "svd", "squad", "afghan", "cz", "west", "svd"], subtitles="CZ06.ass"))
