#!/usr/bin/env python3
"""AUS08 Toyota warns ute prices could rise in 2027 (NVES): full edit, shots anchored to phrases.
    python3 build_aus08.py <narration_dir> > episode.json   (run from the work folder)
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "engine"))
import aus_kit as A
from aus_kit import P, photo, stat, bars, say, cta, title, ch, questions

PHOTOS = {
    "ute": ["ai:ai_tradie_ute", "h_ute_outback", "h_tradie", "h_pickup2", "h_4x4", "h_construction"],
    "farm": ["ai:ai_farmer_ute", "h_farm", "h_farm2"],
    "tow": ["ai:ai_caravan_tow", "h_caravan", "h_camping"],
    "lab": ["ai:ai_emissions_lab", "h_exhaust"],
    "dealer": ["ai:ai_price_tag_rise", "h_dealer"],
    "diesel": ["h_diesel", "h_exhaust", "h_fuel2"],
    "mine": ["ai:ai_mine_utes", "h_mine"],
    "politics": ["ai:ai_canberra_debate", "h_parliament"],
    "family": ["ai:ai_family_4wd", "h_caravan", "h_beach4wd"],
    "ev": ["h_ev_charge", "h_ev2"], "money": ["h_money", "h_calc"], "road": ["h_road", "h_outback2", "h_truck_road"],
    "toyota": ["m_hilux", "m_lc70", "m_prado", "m_tundra"],
    "rivals": ["m_ranger", "m_dmax", "m_triton", "m_bt50", "m_everest", "m_mux"],
    "evute": ["m_shark6", "m_cannon", "m_ranger_phev", "m_hilux_bev", "m_musso"],
}
CLIPS = json.load(open(os.path.join(HERE, "clips.json")))
GENERIC = CLIPS.pop("_generic", [])
FALLBACK = {"ute": ["farm", "rivals"], "farm": ["ute"], "tow": ["family", "ute"], "lab": ["diesel"], "dealer": ["rivals"],
            "diesel": ["lab"], "mine": ["road"], "politics": ["money"], "family": ["tow"], "ev": ["evute"], "money": ["dealer"],
            "road": ["ute"], "toyota": ["ute"], "rivals": ["ute"], "evute": ["ev"]}
RES = ["m_hilux/1", "m_hilux/3", "m_hilux_bev/1", "m_hilux_bev/3", "m_lc70/1", "m_lc70/3", "m_tundra/1", "m_tundra/3", "m_prado/1",
       "m_ranger/1", "m_ranger/3", "m_ranger_phev/1", "m_everest/1", "m_dmax/1", "m_dmax/3", "m_mux/1", "m_triton/1", "m_bt50/1",
       "m_shark6/1", "m_cannon/1", "m_musso/3", "m_mustang/1", "m_mustang/3"]
A.setup(sys.argv[1], os.path.join(HERE, "skip.json"), PHOTOS, CLIPS, GENERIC, FALLBACK,
        ["ute", "road", "farm", "rivals", "dealer", "toyota", "diesel", "money"], reserved=RES)
chapters = []

c = ch("ch00_hook", 0.6)
c.at(0, say("\"We cannot rule out price increases.\"", "PRICE INCREASES", 105))
c.at("That's Toyota", photo("m_hilux", 1, "in", cap="Toyota Australia|October 2026"))
c.at("In October 2026, Toyota Australia's sales boss", P("toyota", cap="John Pappas|VP Sales, Toyota Australia"))
c.at("really challenging", say("\"Really challenging.\"", "CHALLENGING", 150))
c.at("every tradie, farmer and family", P("ute"))
c.at("farmer and family with a caravan", P("tow"))
c.at("Because this isn't just about Toyota", P("rivals"))
c.at("So in this video", title("Ute Prices in 2027", "what's really coming", "Australia", "ute"))
questions(c, ["What changes in 2027", "How much it could add", "Who's best & worst placed", "What it means for you"],
          ["exactly what changes in 2027", "how much it could add", "which brands are best", "what it all means"])
c.at("the numbers are bigger than most people realise", P("money"))
chapters.append(c)

c = ch("ch01")
c.at(0, P("lab"))
c.at("It's called the New Vehicle Efficiency Standard", say("NVES · New Vehicle Efficiency Standard", "NVES", 120))
c.at("It started on the 1st of January 2025", P("politics"))
c.at("Every car brand gets an average carbon dioxide target", P("lab"))
c.at("Sell cleaner cars, and you earn credits", P("ev"))
c.at("Sell dirtier ones", P("diesel"))
c.at("There are two separate targets", P("rivals"))
c.at("the targets get tougher every single year", say("Tougher every year.", "EVERY YEAR", 140))
c.at("For passenger cars, the target is 117", bars("Passenger car target (g CO2/km)", [["2026", 117], ["2027", 92], ["2028", 68], ["2029", 58]], None, "NVES via carsales"))
c.at("For utes and vans, the target is 180", bars("Ute & van target (g CO2/km)", [["2026", 180], ["2027", 150, "red"], ["2028", 122, "red"], ["2029", 110, "red"]], None, "NVES via carsales"))
c.at("That jump from 180 to 150", stat("-17%", "ute target cut in ONE year (180 → 150 g/km)", "NVES", red=True))
c.at("the vast majority of utes sold in Australia are diesel", P("diesel"))
c.at("The big challenge comes from 2027", say("\"The big challenge comes from 2027…\" – Toyota", "2027", 100))
c.at("The law requires a review of the NVES", P("politics"))
c.at("the next twelve months are when", P("politics"))
chapters.append(c)

c = ch("ch02")
c.at(0, P("money"))
c.at("about fifty dollars for every gram", stat("~$50", "per gram over target, per vehicle", "NVES", count=False))
c.at("The real formula is more complicated", P("lab"))
c.at("Let's take a real example", photo("m_hilux", 3, "in", cap="HiLux SR5 V-Active|191 g/km claimed"))
c.at("CarsGuide estimated the penalty for a HiLux", stat("~$550", "estimated penalty per HiLux · 2026", "CarsGuide", red=True, count=False))
c.at("here's a rough calculation of my own", bars("Illustrative penalty · 191 g/km ute", [["2026", 550], ["2027", 2050, "red"], ["2029", 4000, "red"]], None, "rough calculation – not official", prefix="~$"))
c.at("In January 2026, carsales ran its own theoretical numbers", photo("m_ranger", 1, "left", cap="Ranger & Everest|~$3,706/vehicle (theoretical)"))
c.at("well over a billion dollars by 2029", stat("$1B+", "Ford's theoretical NVES bill by 2029", "carsales · assumptions", red=True, count=False))
c.at("But it shows the scale of the problem", P("rivals"))
chapters.append(c)

c = ch("ch03")
c.at(0, say("So who pays?", "WHO PAYS", 150))
c.at("Think of it like a seesaw", P("lab"))
c.at("A brand that sells almost nothing but diesel utes", P("diesel"))
questions(c, ["Sell more hybrids & EVs", "Buy credits", "Pay – and pass it on"], ["sell more hybrids", "buy credits from", "pay the penalty"])
c.at("In February 2026, NRMA reported the first results", bars("NVES liability · Jul–Dec 2025", [["Mazda", 25.4, "red"], ["Nissan", 10.7, "red"], ["Subaru", 7.0, "red"], ["Hyundai", 4.2, "red"]], None, "NRMA · Feb 2026", prefix="$", suffix="M"))
c.at("On the credit side, BYD had more than six million", bars("NVES credits · Jul–Dec 2025", [["BYD", 6.28], ["Toyota", 2.89], ["Tesla", 2.21]], None, "NRMA · Feb 2026", suffix="M"))
c.at("Toyota is in an interesting position", P("toyota"))
c.at("But its utes and big four-wheel drives", photo("m_lc70", 1, "in"))
c.at("self-managed as much as possible", say("\"Self-managed as much as possible.\"", "SELF-MANAGED", 115))
c.at("more \"pragmatic\" ute target", P("politics"))
c.at("the NVES has already contributed to price increases", photo("m_mustang", 1, "left", cap="Ford Ranger & Mustang|NVES-linked price rises"))
c.at("Mazda, Isuzu and Ram have also warned", P("rivals"))
c.at("Isuzu is in a particularly tough spot", photo("m_dmax", 1, "in", cap="Isuzu D-Max & MU-X|diesel only"))
c.at("Customers don't want it", say("\"Customers don't want it.\" – Isuzu", "DON'T WANT", 115))
c.at("the first actual penalty bills", stat("Feb 2028", "first penalty bills (for 2025 vehicles)", "carsales", count=False))
c.at("nobody knows yet exactly how much", P("dealer"))
chapters.append(c)

c = ch("ch04")
c.at(0, P("mine"))
c.at("a draft change could bring vehicles", say("Draft: 3,500–3,855 kg GVM into NVES from July 2027", "JULY 2027", 90))
c.at("Because some popular heavy-duty vehicles", photo("m_lc70", 3, "in", cap="LandCruiser 70|GVM 3,510 kg"))
c.at("and the Toyota Tundra", photo("m_tundra", 1, "left", cap="Toyota Tundra|GVM 3,536 kg"))
c.at("And this fight over utes isn't new", P("ute"))
c.at("applying stringent efficiency standards", say("\"…will substantially drive up the price\" – HIA, 2024", "PRICE", 100))
c.at("about $190 per ute or van", stat("$190", "govt's 2024 compliance cost estimate per ute/van", "Consultation paper", count=False))
c.at("If you're a farmer", P("farm"))
chapters.append(c)

c = ch("ch05")
c.at(0, P("ute"))
c.at("Tell me in the comments", cta("Diesel forever – or hybrid?", "Tell me in the comments"))
c.at("hit subscribe", cta("Subscribe", "everything changing in 2027"))
chapters.append(c)

c = ch("ch06")
c.at(0, P("road"))
c.at("Australians bought 184,328 light commercial", stat("184,328", "light commercials sold · Jan–Sep 2026", "VFACTS via carsales"))
c.at("155,040 of them were diesel", stat("84%", "diesel (155,040)", "VFACTS via carsales", red=True))
c.at("Electric light commercials", stat("1,630", "electric light commercials · Jan–Sep 2026", "VFACTS via carsales", count=False))
c.at("The 4x4 ute market is also shrinking", stat("-13.6%", "4x4 ute market (140,410)", "VFACTS · Sept YTD", red=True))
c.at("The Ford Ranger 4x4 led", bars("4x4 ute sales · Jan–Sep 2026", [["Ford Ranger 4x4", 35744], ["Toyota HiLux 4x4", 32238]], None, "VFACTS via carsales"))
c.at("Nearly fifty-four per cent", stat("54%", "of HiLux & LandCruiser buyers live outside major cities", "Toyota", count=False))
c.at("diesel is still the practical choice", P("farm"))
c.at("The Australian Automobile Association reported", bars("BEV + PHEV share of new sales · 2026", [["March qtr", 19.07], ["June qtr", 31.61]], None, "AAA", suffix="%"))
c.at("electric vehicles outsold both petrol and diesel", P("ev"))
c.at("To be fair to Toyota", P("toyota"))
c.at("the right tool of trade", say("\"The right tool of trade for regional and rural Australia.\"", "TOOL OF TRADE", 90))
c.at("It's about how fast utes can realistically get there", P("road"))
chapters.append(c)

c = ch("ch07")
c.at(0, P("evute"))
c.at("CarExpert listed every electrified ute", bars("Electrified utes · from (NSW drive-away)", [["GWM Cannon Alpha PHEV", 57490], ["Ford Ranger PHEV", 59000],
     ["KGM Musso EV", 60000], ["BYD Shark 6", 62660], ["Toyota HiLux BEV", 82752]], None, "CarExpert · May 2026", prefix="$"))
c.at("diesel reached as high as $3.50", stat("$3.50/L", "diesel in parts of Australia · May 2026", "CarExpert", red=True, count=False))
c.at("Ford cut the price of the Ranger plug-in hybrid", photo("m_ranger_phev", 1, "in", cap="Ranger Wildtrak Hybrid|$70,000 drive-away"))
c.at("Australian buyers are doing the maths", say("\"Australian buyers are doing the maths.\" – Ford", "MATHS", 110))
c.at("a price war has started", P("evute"))
c.at("The new JAC Hunter", stat("<$50K", "JAC Hunter PHEV target drive-away", "CarsGuide · May 2026", count=False))
c.at("Toyota's own 48-volt mild hybrid", P("toyota", cap="HiLux 48V mild hybrid|from $57,990 + ORC"))
c.at("Chery has a diesel-electric ute", P("evute"))
c.at("By 2027, ute buyers will have more electrified choices", P("ev"))
c.at("Toyota itself sells an electric HiLux", photo("m_hilux_bev", 1, "in", cap="HiLux BEV|$74,990–$82,990 + ORC"))
c.at("the diesel HiLux 4x4 range runs", A.price("Toyota HiLux 4x4", "$74,990+", "$45,990+", "electric HiLux", "diesel HiLux 4x4", None, "carsales"))
c.at("That's the squeeze in a nutshell", say("Diesel: penalties up. Electric: still pricier.", "SQUEEZE", 100))
c.at("especially for heavy towing", P("tow"))
chapters.append(c)

c = ch("ch08")
c.at(0, P("politics"))
c.at("the federal Coalition pledged to repeal", say("Coalition: repeal the NVES", "REPEAL", 130))
c.at("family car and ute tax", say("\"Family car and ute tax\" – Dan Tehan", "UTE TAX", 115))
c.at("Supporters of the NVES see it very differently", P("ev"))
c.at("Farmers for Climate Action", P("farm"))
c.at("stable, predictable and workable", say("\"Stable, predictable and workable\" – FCAI", "STABLE", 110))
questions(c, ["Targets stay → prices may rise", "Review softens targets", "Repealed after election"],
          ["Prices could rise in 2027", "The targets could be softened", "the whole scheme could be repealed"])
chapters.append(c)

c = ch("ch09")
c.at(0, title("What It Means for You", "if you're buying a ute", "5 tips", "dealer"))
c.at("First, nobody has announced a 2027 price rise", say("1 · No price rise announced yet", "1", 120))
c.at("Second, if you were already planning", say("2 · 2026 runout deals are here now", "2", 115))
c.at("there's no reason to wait", P("dealer"))
c.at("Third, work out your real costs", say("3 · Work out real running costs", "3", 120))
c.at("a plug-in hybrid ute can save a lot on fuel", P("ev"))
c.at("if you tow heavy loads long distances", P("tow"))
c.at("plug-in hybrids lost their fringe benefits tax exemption", stat("1 Apr 2025", "PHEVs lost the FBT exemption", "ATO / Treasury", count=False))
c.at("the MG U9 electric ute", stat("3,500 kg", "braked towing – MG U9 EV (claimed)", "MG Australia", count=False))
c.at("Fourth, think about resale", say("4 · Think about resale", "4", 130))
c.at("And fifth, watch the NVES review", say("5 · Watch the review & politics", "5", 120))
c.at("If they stay, 2027 is when the squeeze really starts", P("money"))
chapters.append(c)

c = ch("ch10", 2.5)
c.at(0, P("ute"))
c.at("The targets for utes drop from 180 grams to 150", stat("180 → 150", "g/km ute target in 2027", "NVES", red=True, count=False))
c.at("independent estimates suggest", P("money"))
c.at("it's not only Toyota's problem", P("rivals"))
c.at("But it's not a done deal", say("Not a done deal.", "NOT", 150))
c.at("Car makers can trade credits", P("evute"))
c.at("If this helped you understand", cta("Like · Subscribe", "everything changing in 2027"))
questions(c, ["Pay more for diesel – or switch?"], ["would you pay more for a diesel ute"])
c.at("in the next video", title("EV Changes in 2027", "tax · road charges · prices", "next video", "ev"))
chapters.append(c)

CTX = ["ute", "lab", "money", "rivals", "farm", "ute", "road", "ev", "ute", "dealer", "ute"]
print(A.finish(chapters, "AUS08_Ute_Prices_2027.mp4", CTX, subtitles="AUS08.ass"))
