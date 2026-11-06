#!/usr/bin/env python3
"""CZ03 Škorpion vz. 61 — who was it really made for: full edit, shots anchored to phrases.
    python3 build_cz03.py <narration_dir> > episode.json   (run from the work folder; a/ = assets/cz03-skorpion)
Footage first (real photos + clips), AI only fills gaps (always last in each pool), 3 HyperFrames cards.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "engine"))
import aus_kit as A
from aus_kit import P, ch, hf, cta

AI = lambda *names: ["ai:" + n for n in names]  # noqa: E731
PHOTOS = {
    "skorpion": ["skorpion", "skorpion_museum", "skorpion_holster", "weapons_museum"] + AI("ai_holster_belt", "ai_collector"),
    "rear": ["tank_crew", "radio_operator", "army_truck", "vz58_army"] + AI("ai_driver_cab", "ai_tank_hatch", "ai_signaller", "ai_staff_officer", "ai_ambush_column"),
    "design": ["strakonice", "pistol_32acp"] + AI("ai_rybar_desk", "ai_prototype", "ai_grip_mechanism", "ai_motorcycle_factory"),
    "factory": ["uh_brod", "strakonice"],
    "police": ["vb_police", "czech_police"] + AI("ai_police_70s"),
    "dark": ["italy_70s", "cold_war_border"] + AI("ai_coat_hidden", "ai_rome_70s", "ai_newspaper_stack", "ai_border_smuggle", "ai_warehouse_90s"),
    "balkan": ["yugoslav_war", "m84"] + AI("ai_balkan_ruins"),
    "pdw": ["p90", "mp7"],
    "modern": ["evo3", "czech_police"] + AI("ai_modern_smg", "ai_gamer"),
}
CLIPS = json.load(open(os.path.join(HERE, "clips.json")))
GENERIC = CLIPS.pop("_generic", [])
FALLBACK = {k: ["skorpion", "rear", "police"] for k in PHOTOS}
A.setup(sys.argv[1], os.path.join(HERE, "skip.json"), PHOTOS, CLIPS, GENERIC, FALLBACK, ["skorpion", "rear", "police"])
A.CLIP_TARGET = 0.45
A.MAX_HOLD, A.KEEP = 13.0, 8.5
A.ARCHIVE_OK = True
A.SPLIT_BY_SUBJECT = True
chapters = []

c = ch("ch00_hook", 0.6)
c.at(0, P("skorpion"))
c.at("A přesto dokáže vystřelit", P("skorpion"))
c.at("Jmenuje se Škorpion", P("skorpion"))
c.at("Používaly ho armády", P("police"))
c.at("A bohužel se dostal", P("dark"))
c.at("Jenže nic z toho nebylo v plánu", P("rear"))
c.at("Tak pro koho vlastně Škorpion vznikl", P("skorpion"))
c.at("Odpověď je překvapivě jednoduchá", P("design"))
c.at("Tohle je příběh samopalu", P("skorpion"))
chapters.append(c)

c = ch("ch01")
c.at(0, P("rear"))
c.at("Jenže armáda není jen pěchota", P("rear"))
c.at("Druhá světová válka ukázala", P("rear"))
c.at("Co jim dát", P("rear"))
c.at("Pistole je zase příliš slabá", hf("g_users"))
c.at("Armáda tedy potřebovala", P("rear"))
c.at("Dnes by se takové zbrani řeklo", P("pdw"))
c.at("Úkol dostal konstruktér", P("design"))
chapters.append(c)

c = ch("ch02")
c.at(0, P("design"))
c.at("Strakonická zbrojovka měla", P("factory"))
c.at("Jeho úkol byl v jednom ohledu", P("design"))
c.at("První rozhodnutí se týkalo náboje", P("design"))
c.at("Proč? Protože silný náboj", P("skorpion"))
c.at("Prototypy se zkoušely", P("design"))
c.at("Výsledek vážil prázdný", hf("g_spec"))
c.at("A jméno? Škorpion", P("skorpion"))
c.at("Jenže to nejzajímavější", P("design"))
chapters.append(c)

c = ch("ch03")
c.at(0, P("skorpion"))
c.at("Rybář tento problém vyřešil", P("design"))
c.at("Celé to trvá jen nepatrný", P("skorpion"))
c.at("Dalším chytrým prvkem", P("skorpion"))
c.at("Nábojnice vylétají nahoru", P("rear"))
c.at("Škorpion se nosil v koženém pouzdře", P("skorpion"))
c.at("Na papíře tak Škorpion vypadal", P("rear"))
c.at("Jenže na ty pár metrů", P("dark"))
chapters.append(c)

c = ch("ch04")
c.at(0, P("rear"))
c.at("Ale zbraň si rychle našla", P("police"))
c.at("Škorpion používala i tehdejší", P("police"))
c.at("A pak přišel export", P("factory"))
c.at("Zbrojovka zkoušela i silnější verze", P("skorpion"))
c.at("V Jugoslávii se Škorpion", P("balkan"))
c.at("Ale ještě předtím", P("dark"))
chapters.append(c)

c = ch("ch05")
c.at(0, cta("Odebírat", "příběhy zbraní, které změnily dějiny"))
c.at("Sedmdesátá léta byla v Evropě", P("dark"))
c.at("Škorpion jim vyhovoval", P("dark"))
c.at("Pro konstruktéry z Československa", P("design"))
c.at("Je to ale osud", P("skorpion"))
c.at("Na Škorpionu se také ukázalo", P("dark"))
c.at("Jenže zatímco jedni", P("police"))
chapters.append(c)

c = ch("ch06")
c.at(0, P("skorpion"))
c.at("Česká armáda i policie", P("police"))
c.at("Mnoho českých vojáků", P("rear"))
c.at("Ve světě mezitím pojem", hf("g_timeline"))
c.at("Později přišel i německý", P("pdw"))
c.at("Když se na ty požadavky", P("skorpion"))
c.at("V devadesátých letech se Škorpion", P("balkan"))
c.at("Pak přišlo nové tisíciletí", P("modern"))
chapters.append(c)

c = ch("ch07")
c.at(0, P("modern"))
c.at("Proč tedy stejné jméno", P("modern"))
c.at("Nový samopal se dostal", P("police"))
c.at("Původní Škorpion mezitím zažil", P("modern"))
c.at("A sběratelé", P("skorpion"))
c.at("Je ironií", P("skorpion"))
chapters.append(c)

c = ch("ch08", 2.5)
c.at(0, P("skorpion"))
c.at("Ne pro speciální jednotky", P("rear"))
c.at("Proto je tak malý", P("skorpion"))
c.at("Českoslovenští konstruktéři tak", P("pdw"))
c.at("To, co se stalo potom", P("dark"))
c.at("Škorpion je tak příběhem", P("skorpion"))
c.at("Teď je řada na vás", cta("Setkali jste se se Škorpionem?", "napište do komentářů"))
c.at("A pokud vás zajímají další příběhy", cta("Odebírat", "příště: kulomet Bren"))
chapters.append(c)

print(A.finish(chapters, "CZ03_skorpion.mp4", ctx=["skorpion", "rear", "design", "skorpion", "police", "dark", "skorpion", "modern", "skorpion"],
               subtitles="CZ03.ass"))
