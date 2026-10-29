#!/usr/bin/env python3
"""AUS01 utes: full edit. Every shot is anchored to the phrase it illustrates.
Run from the episode work folder (a/ = assets of aus01-utes, audio/, sfx/, trilha.wav):
    python3 build_aus01.py <narration_dir> > episode.json
Photos come from pools (one folder per search); each photo is used once (channel rule: no repeats).
"""
import glob, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "engine"))
from cues import Chapter
import edit_kit as K

SCRIPT = sys.argv[1]
K.SFX.update({"hit": ("sfx/hit.wav", -16), "whoosh": ("sfx/whoosh.wav", -20), "pop": ("sfx/pop.wav", -22)})
fx = K.fx
SKIP = set(json.load(open(os.path.join(HERE, "skip.json")))) if os.path.exists(os.path.join(HERE, "skip.json")) else set()
CREDITS = {}
if os.path.exists("a/credits.csv"):
    import csv
    for r in csv.DictReader(open("a/credits.csv")):
        f = r.get("file") or r.get("arquivo") or ""
        CREDITS[os.path.basename(f)] = r


def pool(cat):
    files = sorted(glob.glob(f"a/{cat}/*.jpg") + glob.glob(f"a/{cat}/*.png") + glob.glob(f"a/{cat}/*.jpeg"))
    return [f[2:] for f in files if f"{cat}/{os.path.basename(f)}" not in SKIP]


POOLS = {}
USED = set()
MOVES = ["in", "left", "out", "right", "in", "up", "out", "down"]
_mv = [0]
# related pools to fall back on when one runs dry (still never repeating a photo)
FALLBACK = {
    "g_car_dealership": ["g_car_yard", "g_motor_show", "g_byd_store"],
    "g_car_yard": ["g_car_dealership", "g_car_terminal", "au_car_carrier_port"],
    "g_motor_show": ["g_car_dealership", "g_byd_store"],
    "g_car_terminal": ["g_port_melbourne", "g_car_unloading", "au_car_carrier_port", "g_car_yard"],
    "g_port_melbourne": ["g_car_terminal", "au_car_carrier_port", "g_car_unloading"],
    "g_ute_outback": ["g_red_dirt_road", "g_outback_road", "g_bush_track", "g_hilux_au", "g_ranger_au"],
    "g_outback_road": ["g_red_dirt_road", "g_road_train", "g_ute_outback"],
    "g_red_dirt_road": ["g_outback_road", "g_ute_outback", "g_bush_track"],
    "g_bush_track": ["g_beach_4wd", "g_ute_outback", "g_red_dirt_road"],
    "g_beach_4wd": ["g_bush_track", "g_ute_outback"],
    "g_tradie": ["g_farm_ute", "g_dmax_au", "g_hilux_au"],
    "g_farm_ute": ["g_country_town", "g_tradie", "g_ute_outback"],
    "g_sydney_traffic": ["g_melbourne_traffic", "g_country_town"],
    "g_melbourne_traffic": ["g_sydney_traffic", "g_country_town"],
    "g_fuel_station": ["g_road_train", "g_outback_road"],
    "g_ev_charging": ["g_byd_store", "g_motor_show"],
    "g_caravan_tow": ["g_outback_road", "g_beach_4wd"],
    "g_holden_ute": ["g_falcon_ute"],
    "g_falcon_ute": ["g_holden_ute"],
    "g_country_town": ["g_farm_ute", "g_outback_road"],
    "g_byd_store": ["g_motor_show", "g_ev_charging"],
    "g_hilux_au": ["m_hilux", "g_ute_outback"],
    "g_ranger_au": ["m_ranger", "g_ute_outback"],
    "g_dmax_au": ["m_dmax", "g_ute_outback"],
    "g_triton_au": ["m_triton", "g_ute_outback"],
}


def P(cat, move=None, cap=None, **kw):
    """Next unused photo from a pool (or a related pool)."""
    for c in [cat] + FALLBACK.get(cat, []) + ["g_ute_outback", "g_outback_road", "g_car_yard", "g_motor_show"]:
        if c not in POOLS:
            POOLS[c] = pool(c)
        while POOLS[c]:
            f = POOLS[c].pop(0)
            if f in USED:
                continue
            USED.add(f)
            if move is None:
                move = MOVES[_mv[0] % len(MOVES)]; _mv[0] += 1
            return K.img(f, move, cap=cap, **kw)
    sys.exit(f"Sem fotos novas para '{cat}' (e alternativas) — buscar mais imagens")


def M(cat, n, **kw):
    """A specific photo of a model pool (by its number on the contact sheet)."""
    f = [x for x in glob.glob(f"a/{cat}/{n}_*") if os.path.splitext(x)[1].lower() in (".jpg", ".jpeg", ".png")][0][2:]
    USED.add(f)
    if f in POOLS.get(cat, []):
        POOLS[cat].remove(f)
    return f


def credit(path):
    r = CREDITS.get(os.path.basename(path), {})
    a = (r.get("author") or r.get("autor") or "").strip()
    lic = (r.get("license") or r.get("licenca") or r.get("licença") or "").strip()
    return f"Photo: {a[:40]} · {lic}" if a else ""


def rank(num, name, cat, n, tag=None, sub=None):
    f = M(cat, n)
    s = {"type": "rank", "num": num, "name": name, "photo": "a/" + f, "credit": credit(f), "trans": "wipe",
         "sfx": [fx("whoosh"), fx("hit", 0.15, -6)]}
    if tag: s["tag"] = tag
    if sub: s["sub"] = sub
    return s


def photo(cat, n, move="in", cap=None):
    return K.img(M(cat, n), move, cap=cap)


def stat(value, label, source=None, red=False, tag=None, count=True):
    s = {"type": "stat", "value": value, "label": label, "count": count, "sfx": [fx("pop", 0.05)]}
    if source: s["source"] = source
    if red: s["color"] = "red"
    if tag: s["tag"] = tag
    return s


def bars(title, items, delta=None, source=None):
    s = {"type": "bars", "title": title, "items": items, "sfx": [fx("whoosh", 0, -4)]}
    if delta: s["delta"] = delta
    if source: s["source"] = source
    return s


def price(model, old, new, old_note=None, new_note=None, save=None, source=None):
    s = {"type": "price", "model": model, "old": old, "new": new, "sfx": [fx("pop", 0.6), fx("pop", 1.0)]}
    for k, v in (("old_note", old_note), ("new_note", new_note), ("save", save), ("source", source)):
        if v: s[k] = v
    return s


def say(text, hl="", size=140):
    return {"type": "statement", "text": text, "highlight": hl, "size": size, "sfx": [fx("hit", 0, -4)]}


def cta(text, sub):
    return {"type": "cta", "text": text, "sub": sub, "sfx": [fx("whoosh"), fx("pop", 1.2)]}


def ch(name, tail=0.8):
    return Chapter(name, f"{SCRIPT}/{name}.txt", f"a/words/{name}.words.json", f"audio/{name}.flac", tail=tail)


def questions(c, items, phrases):
    """Question cards, each one popping in exactly on its phrase."""
    ts = [c.find(p) for p in phrases]
    if None in ts:
        sys.exit(f"{c.name}: frase das perguntas não encontrada: {phrases}")
    t0 = max(0.0, ts[0] - 0.12)
    c.cues.append((t0, {"type": "questions", "items": items, "starts": [int((t - 0.12 - t0) * 24) for t in ts],
                        "sfx": [fx("pop", t - 0.12 - t0) for t in ts]}))


VF = "FCAI VFACTS"
chapters = []

# ---------------------------------------------------------------- HOOK
c = ch("ch00_hook", 0.6)
c.at(0, P("g_ute_outback", "in"))
c.at("Tradies, farmers, families", P("g_tradie"))
c.at("weekend campers", P("g_beach_4wd"))
c.at("everyone wanted a dual-cab", P("g_hilux_au"))
c.at("But right now, something has quietly broken", say("Something has quietly broken.", "BROKEN"))
c.at("sales of 4x4 utes fell", stat("-15.2%", "4x4 ute sales · July 2026 vs July 2025", VF, red=True))
c.at("Australia's best-selling ute lost its crown", P("g_ranger_au", cap="July 2026|The Ranger lost the top spot"))
c.at("One brand-new ute sold barely", stat("212", "new Navara sales · July 2026", VF, red=True))
c.at("And one dealer boss says", P("g_car_terminal"))
c.at("see cars sitting everywhere", P("g_port_melbourne"))
questions(c, ["Who's struggling?", "Who's cutting prices?", "Buy now – or trap?"],
          ["So which utes are feeling the squeeze", "Who's cutting prices", "is this the best time"])
c.at("Stick around, because number one", {"type": "title", "title": "10 Utes Feeling the Pressure",
     "subtitle": "Australia's 2026 ute slump", "tag": "#1 will surprise you", "bg": P("g_red_dirt_road")["src"],
     "trans": "zoom", "sfx": [fx("whoosh"), fx("hit", 0.6, -4)]})
chapters.append(c)

# ---------------------------------------------------------------- CH 1 context
c = ch("ch01")
c.at(0, P("g_car_dealership"))
c.at("the 4x4 pick-up segment dropped", bars("4x4 ute sales", [["Jul 2025", 17351], ["Jul 2026", 14705, "red"]], "-15.2%", VF))
c.at("And it's not a one-month blip", P("g_car_yard"))
c.at("Across the first eight months of 2026", stat("-13.6%", "4x4 ute sales · Jan–Aug 2026", "FCAI VFACTS via CarsGuide", red=True))
c.at("Now here's the strange part", P("g_sydney_traffic"))
c.at("June 2026 was the biggest single month", stat("RECORD", "June 2026: biggest month ever for new car sales", VF, count=False, tag="all-time high"))
c.at("So Aussies are still buying cars", P("g_melbourne_traffic"))
c.at("They're just buying fewer utes", say("Just fewer utes.", "UTES"))
c.at("Diesel sales overall were down", stat("-13.1%", "diesel vehicle sales · 2026 so far", "FCAI VFACTS via The Driven", red=True))
c.at("as buyers moved into hybrids", P("g_ev_charging"))
c.at("At the same time, choice has exploded", P("g_motor_show"))
c.at("There are now around twenty-five different utes", stat("25", "different utes on sale in Australia", "CarsGuide"))
c.at("Back in January 2025", P("g_motor_show"))
c.at("Australia had hit", say("\"Peak ute\"?", "PEAK UTE", 170))
c.at("Eighteen months later", P("g_car_yard"))
c.at("And when supply goes up while demand goes down", P("g_car_terminal"))
c.at("the dealer's yard", P("g_car_dealership"))
c.at("there was excess inventory everywhere", say("\"Excess inventory everywhere.\"", "EXCESS INVENTORY"))
c.at("with cars piled up at the ports", P("g_port_melbourne", cap="Car terminals|Stock waiting at the ports"))
c.at("Add the New Vehicle Efficiency Standard", P("g_parliament", cap="NVES|New Vehicle Efficiency Standard"))
c.at("and diesel utes have become harder", P("g_fuel_station"))
c.at("Why does this matter so much", P("g_country_town"))
c.at("It replaced the big family sedan", P("g_holden_ute"))
c.at("It tows the boat, the caravan", P("g_caravan_tow"))
c.at("It does the school run on Monday", P("g_sydney_traffic"))
c.at("and the beach on Saturday", P("g_beach_4wd"))
c.at("When a vehicle that important starts to slow down", P("g_outback_road"))
c.at("about interest rates", say("Interest rates. Cost of living.", "RATES LIVING", 120))
c.at("So let's count down the ten utes", say("10 utes feeling it the most", "10", 150))
chapters.append(c)

# ---------------------------------------------------------------- #10 LDV T60
c = ch("ch02")
c.at(0, rank(10, "LDV T60 Max Pro", "m_ldv_t60", 2, "$2,000 off", "Australia's cheapest dual-cab with a tub (late 2025)"))
c.at("In late 2025, LDV dropped", price("LDV T60 Max Pro 4x4 auto", "$38,990", "$36,990", "previous ABN drive-away price",
                                     "drive-away for ABN holders · offer to 31 Dec 2025", "-$2,000", "Cars24 / Drive"))
c.at("and at the time it made the T60", photo("m_ldv_t60", 3, "right"))
c.at("The T60 also picked up safety gear", photo("m_ldv_t60", 4, "in", cap="2026 update|Autonomous emergency braking added"))
c.at("But here's the catch", P("g_car_yard"))
c.at("Chinese rivals are now fighting", P("g_motor_show"))
c.at("If you just need a basic work ute", P("g_tradie"))
chapters.append(c)

# ---------------------------------------------------------------- #9 Kia Tasman
c = ch("ch03")
c.at(0, rank(9, "Kia Tasman", "m_kia_tasman", 1, "Slow start", "Kia's first ute, built with Australia in mind"))
c.at("This was a big deal when it launched", photo("m_kia_tasman", 2, "left"))
c.at("backed by one of the strongest brands", photo("m_kia_tasman", 3, "in"))
c.at("In May 2026, the Tasman 4x4 managed", stat("382", "Tasman 4x4 sales · May 2026", VF, red=True))
c.at("For comparison, the Toyota HiLux", bars("4x4 sales · July 2026", [["HiLux", 4119], ["Tasman", 355, "red"]], None, VF))
c.at("That's more than eleven HiLuxes", say("11 HiLuxes for every Tasman", "11", 130))
c.at("To be fair, it's early days", photo("m_kia_tasman", 4, "out"))
c.at("it was Australia's third best-selling brand", stat("#3", "Kia's brand ranking · July 2026", VF, count=False))
c.at("But in a slumping segment", P("g_car_dealership"))
c.at("For buyers, that could make", P("g_bush_track"))
chapters.append(c)

# ---------------------------------------------------------------- #8 Amarok
c = ch("ch04")
c.at(0, rank(8, "Volkswagen Amarok", "m_vw_amarok", 3, "271 sales in May", "Ranger underneath, German badge"))
c.at("Underneath, the current Amarok is a Ford Ranger", photo("m_vw_amarok", 1, "left", cap="Built with the Ranger|South Africa"))
c.at("Same bones, German badge", say("Same bones. German badge. Higher price.", "HIGHER PRICE", 120))
c.at("In May 2026, the Amarok sold just", stat("271", "Amarok sales · May 2026", VF, red=True))
c.at("Volkswagen's answer was to go upmarket", photo("m_vw_amarok", 2, "in", cap="New flagship|Amarok W600"))
c.at("a name Aussie car fans will know", P("g_holden_ute"))
c.at("But the W600 is priced about", stat("+$1,300", "W600 price vs Ford Ranger Raptor", "CarsGuide"))
c.at("which is the most famous performance ute", photo("m_ranger_raptor", 2, "right"))
c.at("It's a bold bet", photo("m_vw_amarok", 4, "out"))
c.at("But it's hard to win buyers", photo("m_ranger_raptor", 3, "in"))
c.at("If you like the Ranger but want something", P("g_car_dealership"))
chapters.append(c)

# ---------------------------------------------------------------- #7 Triton
c = ch("ch05")
c.at(0, rank(7, "Mitsubishi Triton", "m_triton", 3, "Twin trouble", "Bounced back in early 2026"))
c.at("After a quiet 2025", stat("1,747", "Triton 4x4 sales · February 2026", VF))
c.at("But here's why it's on this list", photo("m_triton", 2, "in"))
c.at("Mitsubishi's biggest new rival", say("Its biggest rival? Itself.", "ITSELF", 140))
c.at("The brand-new Nissan Navara is essentially", photo("m_triton", 4, "left", cap="Same ute|Two badges"))
c.at("So in showrooms across Australia", P("g_car_dealership"))
c.at("By July, Triton 4x4 sales had slipped", bars("Triton 4x4 sales", [["Feb 2026", 1747], ["Jul 2026", 1081, "red"]], "-38%", VF))
c.at("When two brands split", P("g_car_yard"))
c.at("And when that happens", P("g_triton_au"))
chapters.append(c)

# ---------------------------------------------------------------- #6 D-Max
c = ch("ch06")
c.at(0, rank(6, "Isuzu D-Max", "m_dmax", 3, "Diesel loyalist", "Third best-selling 4x4 ute in July 2026"))
c.at("In February it held onto third spot", photo("m_dmax", 2, "right"))
c.at("in July it was still the third", stat("1,292", "D-Max 4x4 sales · July 2026", VF))
c.at("So why is it here", P("g_dmax_au"))
c.at("The BYD Shark 6 has been trading blows", photo("m_byd_shark", 3, "in"))
c.at("GAC has confirmed its ute", say("Electrified utes are coming.", "ELECTRIFIED", 130))
c.at("and Chery's diesel-electric Stockman", P("g_motor_show", cap="Late 2026|Chery Stockman PHEV ute"))
c.at("The D-Max is a diesel ute", P("g_fuel_station"))
c.at("It's not falling yet", photo("m_dmax", 4, "out"))
c.at("For the farmers and tradies", P("g_farm_ute"))
chapters.append(c)

# ---------------------------------------------------------------- mid-video CTA
c = ch("ch07")
c.at(0, cta("Real sales data. No rumours.", "A new Aussie car video every week"))
questions(c, ["What ute do you drive?", "Would you buy it again?"], ["what ute do you drive right now", "would you buy the same one"])
c.at("I read every comment", P("g_ute_outback"))
chapters.append(c)

# ---------------------------------------------------------------- #5 Cannon Alpha
c = ch("ch08")
c.at(0, rank(5, "GWM Cannon Alpha", "m_cannon_alpha", 1, "$4,000 off", "One of the Chinese success stories"))
c.at("But look at the price tags", price("GWM Cannon Alpha Ultra diesel", "$58,990", "$54,990", "drive-away before the deal",
                                      "drive-away · offer to 31 Oct 2026", "-$4,000", "CarsGuide"))
c.at("A $4,000 cut on a large dual-cab", P("g_car_dealership"))
c.at("It shows that even the brands winning", P("g_motor_show"))
c.at("because every buyer they win", P("g_car_yard"))
chapters.append(c)

# ---------------------------------------------------------------- #4 Navara
c = ch("ch09")
c.at(0, rank(4, "Nissan Navara", "m_navara", 3, "212 sales in July", "An Aussie favourite under pressure"))
c.at("Nissan as a brand had a rough 2025", stat("-21.6%", "Nissan sales · 2025", "CarExpert / VFACTS", red=True))
c.at("and the old Navara fell", stat("-28%", "Navara sales · 2025", "CarExpert / VFACTS", red=True))
c.at("The new-generation Navara", photo("m_navara", 4, "left"))
c.at("But in May 2026 it managed", bars("New Navara sales", [["May 2026", 217], ["Jul 2026", 212, "red"]], None, VF))
c.at("So Nissan reached for the price lever", price("Nissan Navara (base)", "$53,348", "$49,990", "before on-road costs",
                                               "drive-away · offer ended 31 Aug 2026", "-$3,358", "CarsGuide"))
c.at("The top Pro-4X dropped", price("Nissan Navara Pro-4X", "$68,418", "$63,990", "plus on-road costs",
                                    "drive-away · offer ended 31 Aug 2026", None, "CarsGuide"))
c.at("Existing Nissan owners were offered", stat("+$2,000", "loyalty bonus for existing Nissan owners", "CarsGuide"))
c.at("Those deals have now ended", P("g_car_dealership"))
c.at("A brand-new model being discounted", say("A warning sign.", "WARNING", 170))
chapters.append(c)

# ---------------------------------------------------------------- #3 BYD Shark 6
c = ch("ch10")
c.at(0, rank(3, "BYD Shark 6", "m_byd_shark", 1, "Plug-in hybrid", "The ute that shook up the segment"))
c.at("A plug-in hybrid, more than 300 kilowatts", stat("300+ KW", "plug-in hybrid power", None, count=False))
c.at("It became Australia's best-selling plug-in hybrid", P("g_byd_store"))
c.at("But 2026 has been bumpier", stat("-53.2%", "Shark sales · March 2026", "CarExpert / VFACTS", red=True))
c.at("BYD ran a drive-away deal", stat("$57,900", "Shark 6 Premium drive-away · Feb–Mar 2026", "BYD offer"))
c.at("And then came a recall", stat("32,009", "Shark 6 utes recalled · spare wheel assembly", "BYD Australia", red=True, tag="recall"))
c.at("BYD told owners they could remove", photo("m_byd_shark", 2, "in"))
c.at("To be clear, the Shark is still a big seller", P("g_byd_store"))
c.at("But it shows that even the disruptor", P("g_car_yard"))
chapters.append(c)

# ---------------------------------------------------------------- #2 HiLux
c = ch("ch11")
c.at(0, rank(2, "Toyota HiLux", "m_hilux", 3, "-19.1% in May", "For years it was untouchable"))
c.at("In early 2026, Toyota as a whole", stat("-25%", "Toyota sales · early 2026", "CarExpert / VFACTS", red=True))
c.at("The HiLux was down 19.1 per cent", stat("-19.1%", "HiLux · May 2026 vs May 2025", "CarExpert / VFACTS", red=True))
c.at("Through the first part of the year", stat("2,600", "fewer HiLuxes sold in 2026 so far", "The Driven / VFACTS", red=True))
c.at("There's also a product question", P("g_hilux_au"))
c.at("Toyota also launched a HiLux electric ute", stat("14", "HiLux electric utes delivered in May 2026", "The Driven"))
c.at("Now, here's the twist", bars("4x4 ute sales · July 2026", [["HiLux", 4119], ["Ranger", 3827]], None, VF))
c.at("So the HiLux isn't dying", photo("m_hilux", 4, "in"))
c.at("But Toyota fighting stock shortages", P("g_outback_road"))
chapters.append(c)

# ---------------------------------------------------------------- #1 Ranger
c = ch("ch12")
c.at(0, rank(1, "Ford Ranger", "m_ranger", 1, "Even the king", "Australia's best-selling vehicle"))
c.at("Australia's best-selling vehicle", P("g_ranger_au"))
c.at("Because even the king is discounting", say("Even the king is discounting.", "KING", 140))
c.at("Ford has been offering $3,000 off", stat("-$3,000", "selected Ranger 4x4 variants", "Ford Australia / CarExpert", tag="+ free servicing"))
c.at("That's ahead of the updated MY26.5", photo("m_ranger", 2, "right"))
c.at("Ford sold about 1,600 fewer Rangers", stat("1,600", "fewer Rangers sold in 2026 so far", "The Driven / VFACTS", red=True))
c.at("And in July, it lost the monthly top spot", photo("m_ranger_raptor", 1, "in"))
c.at("Think about what that means", photo("m_ranger", 4, "left"))
c.at("then every ute below it", P("g_car_terminal"))
c.at("That's the real story of 2026", say("The real story of 2026.", "2026", 140))
chapters.append(c)

# ---------------------------------------------------------------- what it means
c = ch("ch13")
c.at(0, P("g_car_dealership"))
c.at("First, this is a buyer's market", say("It's a buyer's market.", "BUYERS", 150))
c.at("Don't pay sticker price", P("g_car_yard"))
c.at("Second, check the run-out stock", say("Check the run-out stock.", "RUNOUT", 140))
c.at("the outgoing stock is often", P("g_car_terminal"))
c.at("Third, think about resale", P("g_car_yard"))
c.at("If you're buying a ute that's struggling", P("g_country_town"))
c.at("And finally, deals change every month", P("g_motor_show"))
c.at("always confirm the current drive-away price", say("Confirm the drive-away price.", "DRIVEAWAY", 130))
c.at("A few more tips before you hit the yards", P("g_car_dealership"))
c.at("If you have an ABN", stat("ABN", "ask about business pricing", None, count=False))
c.at("Look at the build date", say("Check the build date.", "BUILD DATE", 150))
c.at("And if you're thinking about a plug-in hybrid", P("g_ev_charging"))
c.at("If you charge at home", P("g_melbourne_traffic"))
c.at("If you tow heavy loads", P("g_caravan_tow"))
c.at("Most importantly, don't let a big discount", P("g_red_dirt_road"))
c.at("The cheapest ute is the one", say("The right ute beats the cheapest ute.", "RIGHT", 120))
chapters.append(c)

# ---------------------------------------------------------------- end CTA
c = ch("ch14", 2.5)
c.at(0, P("g_bush_track"))
c.at("If you learned something", cta("If this helped, hit like", "and subscribe for real Aussie car data"))
questions(c, ["Which ute will be #1 in 5 years?"], ["drop a comment telling me"])
c.at("Next up, we're looking at", {"type": "title", "title": "10 Car Brands in Serious Trouble", "subtitle": "Up next",
     "tag": "next video", "bg": P("g_motor_show")["src"], "trans": "zoom", "sfx": [fx("whoosh")]})
chapters.append(c)

ep = K.build_episode(chapters, "AUS01_Utes_2026.mp4", music="trilha.wav", music_gain=-24, final_fade=0)
ep["size"] = [1920, 1080]
# title cards use a photo as background: count it as used in the no-repeat check
seen = {}
for ci, chap in enumerate(ep["chapters"]):
    for s in chap["shots"]:
        for k in ("src", "photo", "bg"):
            if s.get(k):
                if s[k] in seen:
                    sys.exit(f"IMAGEM REPETIDA: {s[k]} (cap. {seen[s[k]]} e {ci})")
                seen[s[k]] = ci
sys.stderr.write(f"{sum(len(c['shots']) for c in ep['chapters'])} planos, {len(seen)} imagens diferentes\n")
print(json.dumps(ep, indent=1))
