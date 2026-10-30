#!/usr/bin/env python3
"""AUS10 10 new cars coming to Australia for 2027: full edit, shots anchored to phrases.
    python3 build_aus10.py <narration_dir> > episode.json   (run from the work folder)
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "engine"))
import aus_kit as A
from aus_kit import P, photo, stat, bars, say, cta, title, ch, questions, rank

PHOTOS = {
    "ute": ["h_tow", "h_ute_outback", "h_ute2", "m_hilux", "m_ranger", "m_shark6"],
    "suv": ["m_omoda7", "m_omoda4", "m_rav4", "m_outlander", "h_family", "h_suv2"],
    "ev": ["h_ev_charge", "m_model_y", "m_ix3", "h_ev3"],
    "show": ["h_motor_show", "h_dealer", "h_show2", "h_showroom", "h_carpark"],
    "road": ["h_road", "h_ute_outback", "h_road2", "h_drive"],
    "premium": ["m_zeekr", "m_polestar5", "m_ix3"],
    "4wd": ["m_prado", "m_patrol", "m_pajero"],
}
CLIPS = json.load(open(os.path.join(HERE, "clips.json")))
GENERIC = CLIPS.pop("_generic", [])
FALLBACK = {"ute": ["road"], "suv": ["show"], "ev": ["show"], "show": ["road"], "road": ["ute"], "premium": ["ev"], "4wd": ["ute"]}
RES = ['m_cx6e/1', 'm_cx6e/3', 'm_frontier_pro/1', 'm_frontier_pro/3', 'm_gac/1', 'm_gac/3', 'm_hilux/1', 'm_ix3/1', 'm_ix3/3', 'm_navara/1', 'm_omoda4/1', 'm_omoda7/1', 'm_omoda7/3', 'm_outlander/1', 'm_pajero/1', 'm_patrol/1', 'm_patrol/3', 'm_polestar5/1', 'm_prado/1', 'm_prado/3', 'm_ranger/1', 'm_ranger/3', 'm_rav4/1', 'm_shark6/1', 'm_super_one/1', 'm_super_one/3', 'm_symbioz/1', 'm_zeekr/1']
A.setup(sys.argv[1], os.path.join(HERE, "skip.json"), PHOTOS, CLIPS, GENERIC, FALLBACK, ["road", "show", "ev", "ute", "suv"], reserved=RES)
A.MAX_HOLD, A.KEEP = 13.0, 8.5  # cloud agents blocked (Actions minutes): fewer splits, no AI scenes
chapters = []
def ph(m, n, mv="in", cap=None):
    return photo(m, n, mv, cap=cap)

c = ch("ch00_hook", 0.6)
c.at(0, stat("300 kW", "Nissan Navara Pro PHEV · confirmed for 2027", "Nissan Australia", count=False))
c.at("Eight hundred newton-metres", stat("800 Nm", "torque · 3,500 kg towing target", "Nissan Australia", count=False))
c.at("That's not a Ranger Raptor", ph("m_frontier_pro", 1, "in", cap="Nissan Navara Pro PHEV|due in Australia 2027"))
c.at("A Chinese brand most Aussies have never heard of", ph("m_gac", 1, "left", cap="GAC|ute coming in 2027"))
c.at("Hyundai is finally building a ute", say("Hyundai is building a ute.", "UTE", 140))
c.at("Toyota is bringing a cheaper version", P("suv"))
c.at("coming back from the dead", say("A legend is coming back.", "LEGEND", 140))
c.at("2027 is shaping up", title("10 New Cars Coming in 2027", "that could shake up Australia", "countdown", "show"))
c.at("the emissions rules get tougher", P("road"))
c.at("So in this video, I'm counting down", P("show"))
questions(c, ["What they are", "When they're due", "What we know about price", "Who should be worried"],
          ["what they are", "when they're due", "what we know about the price", "who should be worried"])
c.at("number one could change", say("#1 could change the most important segment.", "#1", 110))
chapters.append(c)

c = ch("ch01")
c.at(0, say("Ground rules", "RULES", 150))
c.at("Some prices are confirmed, some are estimates", say("Confirmed vs estimate – I'll say which.", "ESTIMATE", 110))
c.at("Launch dates can slip", P("show"))
c.at("And why does 2027 matter so much", bars("NVES targets · 2026 → 2027 (g/km)", [["Cars 2026", 117], ["Cars 2027", 92, "red"], ["Utes 2026", 180], ["Utes 2027", 150, "red"]], None, "NVES"))
c.at("Every car maker needs more hybrids", P("ev"))
c.at("They're following the law", say("They're following the law.", "LAW", 140))
questions(c, ["#1 Ford Ranger", "#2 Toyota HiLux", "#3 Tesla Model Y"], ["the Ford Ranger, the Toyota HiLux", "the Toyota HiLux and", "and the Tesla Model Y"])
c.at("BYD is the second best-selling brand", stat("#2", "BYD – brand ranking 2026", "VFACTS", count=False))
c.at("more than twenty-four per cent", stat("24%+", "battery EV share · Sept 2026", "FCAI / EVC"))
c.at("Let's start the countdown", title("The Countdown", "10 → 1", "2027", "road"))
chapters.append(c)

c = ch("ch02")
c.at(0, rank(10, "Honda Super-One", "m_super_one", 1, "electric kei car · ~70 kW", "est. ~$35,000"))
c.at("It's an electric kei-style car", ph("m_super_one", 3, "left"))
c.at("an estimated price of around thirty-five thousand", stat("~$35,000", "estimated price – not confirmed", "CarsGuide", count=False))
c.at("the cheap end of the electric market has exploded", P("ev"))
c.at("seven electric cars available for under forty", stat("7", "EVs under $40k drive-away", "CarsGuide · Feb 2026"))
c.at("It also says something about where the industry", P("show"))
c.at("Number nine: the BMW iX3", rank(9, "BMW iX3", "m_ix3", 1, "new-generation electric SUV", "from $89,900 + ORC"))
c.at("CarsGuide reported the iX3 50 xDrive at $109,900", bars("BMW iX3 prices (+ORC)", [["iX3 40", 89900], ["iX3 50 xDrive", 109900]], None, "CarsGuide", prefix="$"))
c.at("it's just under the luxury car tax threshold", stat("$91,387", "fuel-efficient LCT threshold", "ATO", count=False))
c.at("a new $120,000 luxury car tax threshold", ph("m_ix3", 3, "right", cap="New ZEV LCT threshold|$120,000 from July 2027"))
c.at("It's a sign that the luxury brands", P("premium"))
chapters.append(c)

c = ch("ch03")
c.at(0, rank(8, "Mazda CX-6e", "m_cx6e", 1, "electric SUV · ~190 kW RWD", "est. ~$54,000"))
c.at("its estimated liability was around $25.4 million", stat("$25.4M", "Mazda NVES liability · Jul–Dec 2025", "NRMA", red=True))
c.at("The CX-6e is an electric SUV", ph("m_cx6e", 3, "left"))
c.at("an estimated price of around fifty-four", stat("~$54,000", "estimated – not confirmed", "CarsGuide", count=False))
c.at("For a brand that's built its reputation", P("show"))
c.at("Number seven: the BYD Atto 3 Evo", title("#7 BYD Atto 3 Evo", "RWD & AWD · up to 330 kW", "2027", "ev"))
c.at("the flagship producing 330 kilowatts", stat("330 kW", "Atto 3 Evo flagship", "CarsGuide", count=False))
c.at("And BYD keeps moving fast", P("ev"))
c.at("more than six million credits", stat("6.28M", "BYD NVES credits – most of any brand", "NRMA · Feb 2026"))
c.at("In September 2026, it sold 8,191", stat("8,191", "BYD sales · Sept 2026 (#2 brand)", "FCAI / EVC"))
c.at("the Toyota Corolla Cross, the Mazda CX-30", P("suv"))
chapters.append(c)

c = ch("ch04")
c.at(0, rank(6, "Omoda 4 & Omoda 7", "m_omoda7", 1, "new-energy SUVs", "first half 2027"))
c.at("The Omoda 4 is a compact SUV", ph("m_omoda4", 1, "in", cap="Omoda 4|compact SUV"))
c.at("The Omoda 7 is a mid-size SUV", ph("m_omoda7", 3, "left", cap="Omoda 7|mid-size SUV"))
c.at("Carsales has reported the Omoda 7 plug-in hybrid", bars("Omoda 7 PHEV (reported)", [["Power (kW)", 255], ["Torque (Nm)", 525], ["EV range (km)", 90]], None, "carsales"))
c.at("Omoda was created to challenge convention", say("\"Omoda was created to challenge convention.\"", "CHALLENGE", 110))
c.at("These brands are aiming straight at", P("suv"))
c.at("Number five: the Mitsubishi Pajero", rank(5, "Mitsubishi Pajero", "m_pajero", 1, "all-new 2.4L turbo-diesel · 150 kW", "from $68,490 + ORC"))
c.at("Mitsubishi stopped selling it here in 2021", P("4wd"))
c.at("Carsales reported prices from $68,490", bars("2027 Pajero prices (+ORC)", [["GLS 5-seat", 68490], ["GLS 7-seat", 69990], ["Exceed", 79990], ["GSR", 84990]], None, "carsales", prefix="$"))
c.at("It's due in showrooms from December 2026", stat("Dec 2026", "Pajero in showrooms", "Mitsubishi", count=False))
c.at("For four generations, the Pajero has defined Mitsubishi", say("\"For four generations, the Pajero has defined Mitsubishi.\"", "PAJERO", 95))
c.at("Mitsubishi calls it an all-new Pajero", P("road"))
c.at("Its main target is the Toyota Prado", ph("m_prado", 1, "in", cap="Toyota Prado|$73,200–$100,620"))
c.at("If Mitsubishi can undercut the Prado", ph("m_prado", 3, "right"))
chapters.append(c)

c = ch("ch05")
c.at(0, P("show"))
c.at("Which of these cars would you actually buy", cta("Which would you buy?", "And what did I miss? Comments"))
c.at("hit subscribe", cta("Subscribe", "everything new for 2027"))
chapters.append(c)

c = ch("ch06")
c.at(0, rank(4, "Cheaper Toyota RAV4 PHEV", "m_rav4", 1, "new GXL plug-in hybrid", "early 2027"))
c.at("plug-in hybrids made up thirty-nine per cent", stat("39%", "of RAV4 sales were PHEV · July 2026", "CarExpert"))
c.at("ahead of the BYD Shark 6 on 1,216 sales", bars("Best-selling PHEVs · July 2026", [["Toyota RAV4 PHEV", 2170], ["BYD Shark 6", 1216]], None, "CarExpert"))
c.at("Right now, the RAV4 PHEV starts at $58,840", A.price("Toyota RAV4 PHEV", "$58,840", "~$53,990", "XSE FWD now", "GXL 2027 (estimate)", None, "CarExpert"))
c.at("Toyota hasn't announced the price yet", say("Estimate – not official.", "ESTIMATE", 140))
c.at("a claimed electric range of 121 kilometres", stat("121 km", "claimed electric-only range", "Toyota", count=False))
c.at("enough to do the school run", P("suv"))
c.at("Because the RAV4 is one of the best-selling cars", P("ev"))
c.at("Mitsubishi Outlander plug-in hybrid", ph("m_outlander", 1, "left", cap="Outlander PHEV ES|$58,990 + ORC"))
chapters.append(c)

c = ch("ch07")
c.at(0, title("#3 Hyundai Ute", "hybrid or EREV", "late 2027 (expected)", "ute"))
c.at("There's no doubt we'll be late to the party", say("\"There's no doubt we'll be late to the party.\" – Hyundai", "LATE", 95))
c.at("the dual-cab ute's reveal is expected in 2027", P("road"))
c.at("a hybrid or an EREV", say("\"…a hybrid or an EREV…\"", "EREV", 135))
c.at("An EREV is an extended-range electric vehicle", P("ev"))
c.at("The benchmark in Australia historically", ph("m_ranger", 1, "in", cap="Ford Ranger|the benchmark"))
c.at("Number two: the GAC ute", rank(2, "GAC dual-cab ute", "m_gac", 3, "PHEV or range-extender · ladder frame", "2027"))
c.at("It's expected to look similar to the Pickup 01", P("road"))
c.at("we'll have a future advantage", say("\"…win the competition with Ranger, HiLux…\" – GAC", "WIN", 105))
c.at("balance commercial and passenger use", P("road"))
c.at("Chery has a diesel-hybrid ute", ph("m_shark6", 1, "left", cap="Already here|BYD, GWM, JAC, KGM, Deepal"))
chapters.append(c)

c = ch("ch08")
c.at(0, rank(1, "Nissan Navara Pro PHEV", "m_frontier_pro", 3, "300 kW · 800 Nm · 3,500 kg towing", "2027 · price TBC"))
c.at("The preliminary figures are huge", bars("Navara Pro PHEV (preliminary)", [["Power (kW)", 300], ["Torque (Nm)", 800]], None, "Nissan Australia"))
c.at("Nissan is targeting 3,500 kilograms", stat("3,500 kg", "braked towing target", "Nissan", count=False))
c.at("and a payload of up to 1,000 kilograms", bars("Payload (kg)", [["Navara Pro PHEV (target)", 1000], ["JAC T9 PHEV", 915], ["Ranger Hybrid Wildtrak", 901],
     ["Chery Stockman", 765], ["BYD Shark 6 Perf.", 725], ["GWM Cannon Alpha PHEV", 685]], None, "CarExpert"))
c.at("Nissan hasn't announced the price", say("Price, battery & EV range: TBC", "TBC", 130))
c.at("Utes are the most important segment", ph("m_hilux", 1, "in"))
c.at("The Ford Ranger and the Toyota HiLux", ph("m_ranger", 3, "right"))
c.at("A plug-in hybrid ute with more power than a Raptor", ph("m_navara", 1, "left"))
c.at("Australia wasn't simply where we tested", say("\"Australia… was one of the markets helping shape it.\" – Nissan", "SHAPE", 95))
chapters.append(c)

c = ch("ch09")
c.at(0, title("Honourable Mentions", "just missed the list", "2027", "4wd"))
c.at("The new Nissan Patrol is switching", ph("m_patrol", 1, "in", cap="Nissan Patrol|3.5L twin-turbo V6 · 317 kW"))
c.at("Australia will be the first right-hand-drive market", ph("m_patrol", 3, "left"))
c.at("The Zeekr 8X is a plug-in hybrid SUV", ph("m_zeekr", 1, "right", cap="Zeekr 8X|660 kW · est. ~$80,000"))
c.at("The Polestar 5", ph("m_polestar5", 1, "in", cap="Polestar 5|from $171,100"))
c.at("the Renault Symbioz", ph("m_symbioz", 1, "left", cap="Renault Symbioz|from $36,990"))
c.at("Isuzu has cancelled its plans for the electric D-Max", say("Cancelled: Isuzu D-Max EV", "CANCELLED", 130))
c.at("Customers don't want it", say("\"Customers don't want it.\" – Isuzu", "DON'T", 120))
c.at("If you're buying a ute", P("ute"))
c.at("If you're buying an SUV", P("suv"))
c.at("If you're buying an electric car", stat("1 Apr 2027", "EV FBT change · ≤ $75k keeps full exemption", None, count=False))
questions(c, ["Nearest service centre?", "Crash parts stocked here?", "Who backs the warranty?"],
          ["Where is the nearest service centre", "Are crash parts for this model", "how long is the warranty"])
c.at("look for real-world tests", P("road"))
c.at("waiting a few months can pay off", P("show"))
chapters.append(c)

c = ch("ch10", 2.5)
c.at(0, title("The Full List", "2027", "recap", "show"))
questions(c, ["10 Honda Super-One", "9 BMW iX3", "8 Mazda CX-6e", "7 BYD Atto 3 Evo", "6 Omoda 4 & 7"],
          ["Number ten, the Honda", "Number nine, the BMW", "Number eight, the Mazda", "Number seven, the BYD", "Number six, the Omoda"])
questions(c, ["5 Mitsubishi Pajero", "4 RAV4 PHEV GXL", "3 Hyundai ute", "2 GAC ute", "1 Navara Pro PHEV"],
          ["Number five, the Mitsubishi", "Number four, the cheaper", "Number three, the Hyundai", "Number two, the GAC", "number one, the Nissan"])
c.at("2027 is the year electrified utes go mainstream", P("ute"))
c.at("launch dates and prices can change", say("Prices & dates can change.", "CHANGE", 135))
c.at("If you enjoyed this", cta("Like · Subscribe · Share", "with someone planning their next car"))
questions(c, ["Which would you buy in 2027?"], ["which of these would you buy"])
chapters.append(c)

CTX = ["show", "road", "ev", "suv", "suv", "show", "suv", "ute", "ute", "road", "show"]
print(A.finish(chapters, "AUS10_New_Cars_2027.mp4", CTX, subtitles="AUS10.ass"))
