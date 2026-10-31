#!/usr/bin/env python3
"""AUS15 The ute price war: full edit, shots anchored to phrases.
    python3 build_aus15.py <narration_dir> > episode.json   (run from the work folder)
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "engine"))
import aus_kit as A
from aus_kit import P, photo, stat, bars, say, cta, title, ch, questions, rank

PHOTOS = {
    "ute": ["ai:ai_ute_outback", "h_outback", "ai:ai_tradie_ute"],
    "fuel": ["ai:ai_diesel_fill", "h_diesel"],
    "dealer": ["ai:ai_ute_dealer", "h_dealer", "h_keys"],
    "money": ["h_calc"],
    "tow": ["h_ute_tow"],
}
CLIPS = json.load(open(os.path.join(HERE, "clips.json")))
GENERIC = CLIPS.pop("_generic", [])
FALLBACK = {"ute": ["tow"], "fuel": ["money"], "dealer": ["money"], "money": ["dealer"], "tow": ["ute"]}
RES = ["m_ranger/1", "m_ranger/3", "m_ranger/2", "m_ranger_phev/1", "m_ranger_phev/3", "m_ranger_tremor/1", "m_hilux/1", "m_hilux/3",
       "m_rav4/3", "m_tasman/1", "m_tasman/3", "m_shark6/1", "m_shark6/3", "m_triton/1", "m_triton/3", "m_cannon/1", "m_amarok/1",
       "m_amarok/3", "m_dmax/1", "m_dmax/3", "m_jac_t9/2", "m_jac_t9/3", "m_ram1500/1", "m_ram1500/3", "m_t60/1", "m_t60/3", "m_terron/1"]
A.setup(sys.argv[1], os.path.join(HERE, "skip.json"), PHOTOS, CLIPS, GENERIC, FALLBACK, ["ute", "dealer", "money", "fuel", "tow"], reserved=RES)
A.CLIP_TARGET = 0.55
A.MAX_HOLD, A.KEEP = 13.0, 8.5
chapters = []
SRC = "VFACTS Sept 2026 via CarExpert"

c = ch("ch00_hook", 0.6)
c.at(0, stat("$4,000", "off a Toyota HiLux · October 2026", "CarsGuide", count=False))
c.at("Toyota almost never needs to discount", photo("m_hilux", 1, "in", cap="Toyota HiLux|a 'rare' $4,000 bonus"))
c.at("Ford has cut its Ranger plug-in hybrid", photo("m_ranger_phev", 1, "left", cap="Ford Ranger Hybrid|$10,000+ less"))
c.at("Kia has slashed up to fifteen thousand", photo("m_tasman", 1, "right", cap="Kia Tasman|up to $15,000 off"))
c.at("BYD is offering four thousand dollars cashback", photo("m_shark6", 1, "in", cap="BYD Shark 6|$4,000 cashback"))
c.at("is in a full-blown price war", title("The Ute Price War", "who's cutting · by how much", "Australia", "ute"))
c.at("Sales of traditional utes and vans were down", stat("-13.2%", "utes & vans · September 2026", "Chasing Cars", red=True))
c.at("Some of the biggest names", P("ute"))
c.at("In this video, I'll show you who's cutting prices", P("dealer"))
c.at("the traps hidden inside some of these offers", say("…and the traps in the fine print.", "TRAPS", 120))
chapters.append(c)

c = ch("ch01")
c.at(0, P("ute"))
c.at("the Ford Ranger was Australia's best-selling vehicle", photo("m_ranger", 1, "in", cap="Ford Ranger|#1 · 5,062 (+4%)"))
c.at("But the Toyota HiLux fell to fourth", photo("m_hilux", 3, "left", cap="Toyota HiLux|#4 · 4,455 (-11.7%)"))
c.at("the Toyota RAV4 SUV, with 4,624 sales", bars("September 2026", [["Ford Ranger", 5062], ["Toyota RAV4", 4624], ["Toyota HiLux", 4455, "red"]], None, "VFACTS"))
c.at("For the year to date", bars("2026 to September", [["Ford Ranger", 37858], ["Toyota HiLux", 36616]], None, SRC))
c.at("And winning that crown matters", P("dealer"))
c.at("We've hit peak ute", say("\"We've hit peak ute and the only way is down.\" – CarsGuide", "PEAK UTE", 95))
c.at("It's a remarkable turnaround", P("ute"))
c.at("Sean Hanley, saw this coming", say("\"…the number of ute models… will expand rapidly.\" – Sean Hanley, ex-Toyota", "EXPAND", 90))
questions(c, ["Fuel prices", "Emissions rules", "More alternatives"], ["First, fuel", "Second, the government's emissions rules", "Third, the alternatives"])
c.at("diesel reached as high as $3.50", stat("$3.50/L", "diesel peak in parts of Australia · May 2026", "CarExpert", red=True, count=False))
c.at("you're up for about $280", P("fuel"))
c.at("diesel utes are some of the highest emitters", P("ute"))
c.at("Chinese-built vehicles made up more than thirty-five", stat("35%+", "of new-car sales were Chinese-built · Sept 2026", "Chasing Cars"))
c.at("Buyers who once defaulted to a dual-cab", P("dealer"))
chapters.append(c)

c = ch("ch02")
c.at(0, title("Toyota", "the $4,000 HiLux bonus", "deal #1", "dealer"))
c.at("Toyota is offering a $4,000", photo("m_hilux", 1, "in", cap="HiLux SR5 4x4|$4,000 deposit bonus"))
c.at("the SR5 range starts at $69,901", bars("HiLux SR5 · NSW drive-away", [["Double-Cab Pick-Up", 69901], ["Double-Cab Cab-Chassis V-Active", 73952]], None,
     "CarsGuide", prefix="$"))
c.at("But read the fine print", say("Fine print: Toyota Finance · $10,000+ borrowed", "FINE PRINT", 100))
questions(c, ["Toyota Finance only", "Min. $10,000 financed", "Apply 1 Sep – 31 Dec 2026", "Settle by 28 Feb 2027"],
          ["The bonus only applies", "with at least ten thousand", "between the 1st of September", "settled by the 28th of February"])
c.at("Why is Toyota doing this", say("\"…a very strong, record fourth quarter…\" – John Pappas, Toyota", "RECORD", 92))
c.at("Toyota has more utes coming", P("ute"))
c.at("And remember, this is a brand-new HiLux", photo("m_hilux", 3, "right", cap="New-generation HiLux|-11.7% in September"))
c.at("When the market leader starts offering finance bonuses", P("money"))
chapters.append(c)

c = ch("ch03")
c.at(0, title("Ford", "Ranger Hybrid cut by $10,000+", "deal #2", "ute"))
c.at("In April 2026, Ford slashed the price", photo("m_ranger_phev", 3, "in", cap="Ford Ranger Hybrid|from $62,000 drive-away"))
c.at("The XLT Hybrid dropped to $62,000", bars("Ranger Hybrid drive-away · April 2026", [["XLT", 62000], ["Sport", 66000], ["Wildtrak", 70000],
     ["Stormtrak", 73000]], None, "CarExpert", prefix="$"))
c.at("Ford handed out a $4,000 fuel card", stat("$4,000", "fuel card · MY26 Ranger & Everest Trend", "Ford / CarExpert", count=False))
c.at("short-term pain at the pump", say("\"…short-term pain at the pump.\" – Fadi Mawal, Ford Australia", "PAIN", 105))
c.at("Farmers registered as primary producers", P("ute"))
c.at("And buyers responded", photo("m_ranger", 3, "left"))
c.at("Australian buyers are doing the maths", say("\"Australian buyers are doing the maths.\" – Ford", "MATHS", 115))
c.at("Here's the interesting part", photo("m_ranger", 2, "right"))
chapters.append(c)

c = ch("ch04")
c.at(0, title("Kia Tasman", "up to $15,000 off", "deal #3", "ute"))
c.at("Kia forecast 20,000 sales", bars("Kia Tasman", [["First-year target", 20000], ["Sold, launch to Sept 2026", 7898, "red"]], None, "GoAuto / VFACTS"))
c.at("In September, it found 355 buyers", stat("355", "Tasmans sold · Sept 2026 (-56%)", SRC, red=True))
c.at("So Kia went hard on price", photo("m_tasman", 3, "in"))
c.at("The top X-Pro dropped to $64,990", A.price("Kia Tasman X-Pro", "$74,990", "$64,990", "before on-roads", "drive-away · May 2026", None, "CarsGuide"))
c.at("Kia's own executives have been remarkably honest", say("\"We've fallen short. We know the facts.\" – Damien Meredith, Kia", "FALLEN SHORT", 90))
c.at("once you're inside it", photo("m_tasman", 1, "left"))
c.at("We'd like to sell more cars", say("\"We'd like to sell more cars. It's as simple as that.\" – Dennis Piccoli, Kia", "SIMPLE", 90))
chapters.append(c)

c = ch("ch05")
c.at(0, P("ute"))
c.at("Tell me in the comments", cta("Would you buy a ute now?", "tell me in the comments"))
c.at("hit subscribe", cta("Subscribe", "data-first car videos"))
chapters.append(c)

c = ch("ch06")
c.at(0, title("The Scoreboard", "winners and losers", "September 2026", "ute"))
c.at("The losers first", bars("Losers · Sept 2026 vs Sept 2025", [["Kia Tasman", -56.0], ["JAC T9", -47.3], ["VW Amarok", -42.7], ["KGM Musso", -38.4],
     ["Nissan Navara", -34.9], ["GWM Cannon", -31.6], ["Mitsubishi Triton", -30.6]], None, SRC, suffix="%"))
c.at("The Mitsubishi Triton: 1,202", photo("m_triton", 1, "in", cap="Mitsubishi Triton|1,202 · -30.6%"))
c.at("The GWM Cannon: 852", photo("m_cannon", 1, "left", cap="GWM Cannon|852 · -31.6%"))
c.at("The Volkswagen Amarok: 244", photo("m_amarok", 1, "right", cap="Volkswagen Amarok|244 · -42.7%"))
c.at("And the JAC T9 Chinese ute", photo("m_jac_t9", 2, "in", cap="JAC T9|58 · -47.3%"))
c.at("Even the Isuzu D-Max", photo("m_dmax", 3, "left", cap="Isuzu D-Max|1,866 · -6.2%"))
c.at("Customers don't want it", say("\"Customers don't want it.\" – Isuzu, on the electric D-Max", "DON'T WANT", 100))
c.at("Now the winners", bars("Winners · Sept 2026 vs Sept 2025", [["LDV Terron 9", 195.1], ["LDV T60", 68.9], ["BYD Shark 6", 25.1]], None, SRC, prefix="+", suffix="%"))
c.at("The BYD Shark 6 plug-in hybrid: 1,492", photo("m_shark6", 3, "in", cap="BYD Shark 6|1,492 · +25%"))
c.at("I reckon we can do better", say("\"I reckon we can do better.\" – Stephen Collins, BYD", "BETTER", 110))
c.at("LDV's cheaper T60", photo("m_t60", 1, "right", cap="LDV T60|+69%"))
c.at("LDV's new Terron 9", photo("m_terron", 1, "in", cap="LDV Terron 9|+195%"))
c.at("And big American pick-up trucks", photo("m_ram1500", 1, "left", cap="US pick-ups|+12% this year"))
c.at("So the ute market isn't just shrinking", say("Not shrinking – splitting.", "SPLITTING", 140))
c.at("Buyers are going either cheaper", P("ute"))
chapters.append(c)

c = ch("ch07")
c.at(0, title("BYD", "$4,000 cashback", "deal #4", "dealer"))
c.at("CarsGuide listed the Shark 6 cab-chassis", bars("Shark 6 with cashback (+ ORC)", [["Cab-chassis Dynamic", 51990], ["Premium", 53900], ["Performance", 62900]], None,
     "CarsGuide", prefix="$"))
c.at("Cars have to be delivered", P("dealer"))
c.at("And at the top end of the market", bars("Top-spec utes · drive-away (Sydney)", [["Mitsubishi Triton Raider", 74990], ["Toyota HiLux Rugged X", 78117],
     ["Ford Ranger Tremor", 82404]], None, "CarExpert", prefix="$"))
c.at("That's several thousand dollars of difference", photo("m_triton", 3, "in"))
c.at("GWM has played the same game", stat("$57,490", "GWM Cannon Alpha PHEV drive-away · 2025 (-$7,100)", "CarExpert", count=False))
c.at("Every brand is chasing the same", P("money"))
questions(c, ["JAC Hunter PHEV", "Chery diesel-electric ute", "Smaller GWM Cannon PHEV", "Next Nissan Navara PHEV"],
          ["The JAC Hunter", "Chery has a diesel-electric", "GWM plans a plug-in", "And Nissan's next Navara"])
c.at("More choice means more competition", P("ute"))
chapters.append(c)

c = ch("ch08")
c.at(0, say("These discounts might not last.", "MIGHT NOT LAST", 110))
c.at("Under the New Vehicle Efficiency Standard", bars("NVES target · utes & vans", [["2026", 180], ["2027", 150, "red"]], None, "Federal government", suffix=" g/km"))
c.at("the HiLux SR5 with Toyota's mild-hybrid diesel", stat("191 g/km", "HiLux SR5 V-Active · 41 g over the 2027 target", "CarsGuide", red=True, count=False))
c.at("really challenging", say("\"…cannot rule out\" price increases. – Toyota", "CANNOT RULE OUT", 100))
c.at("And the first actual penalty bills", P("money"))
c.at("On the 29th of September 2026", say("Coalition: repeal the NVES if elected", "REPEAL", 120))
c.at("The point is simple", P("ute"))
chapters.append(c)

c = ch("ch09")
c.at(0, title("How to Win the Price War", "6 rules", "buyers", "dealer"))
c.at("First, compare drive-away prices", say("1 · Compare drive-away prices", "1", 125))
c.at("Ask every dealer for a written", P("dealer"))
c.at("Second, read the finance conditions", say("2 · Read the finance conditions", "2", 125))
c.at("compare the interest rate", P("money"))
c.at("Third, check the build date", say("3 · Build date & demonstrators", "3", 125))
c.at("Fourth, think about resale", say("4 · Think about resale", "4", 125))
c.at("Look at the total cost", P("money"))
c.at("Fifth, use the calendar", say("5 · Use the calendar", "5", 125))
questions(c, ["Black Friday · 27 Nov", "BYD cashback · to 21 Dec", "HiLux finance · to 31 Dec"],
          ["Black Friday falls", "BYD's cashback runs", "the HiLux finance window"])
c.at("And finally, buy the ute you actually need", say("6 · Buy the ute you need", "6", 125))
c.at("If you tow a heavy caravan", P("tow"))
c.at("So should you buy now, or wait", P("dealer"))
c.at("But if you can wait, keep an eye on 2027", P("ute"))
chapters.append(c)

c = ch("ch10", 2.5)
c.at(0, say("Are ute prices collapsing?", "COLLAPSING", 120))
c.at("Toyota is offering $4,000 on the HiLux", bars("The biggest ute cuts", [["Kia Tasman", 15000], ["Ford Ranger Hybrid", 10000], ["Toyota HiLux", 4000],
     ["BYD Shark 6", 4000]], None, "CarsGuide / CarExpert", prefix="up to $"))
c.at("The reason is simple", P("ute"))
c.at("Here's what to watch next", P("dealer"))
c.at("The race between the Ranger and the HiLux", P("dealer"))
c.at("Whatever you drive", P("ute"))
c.at("If this helped", cta("Like · Subscribe · Share", "with a mate shopping for a ute"))
c.at("Ranger, HiLux, Shark or something else", cta("Ranger, HiLux or Shark?", "comments"))
c.at("in the next video", title("A New Road Tax?", "for every driver", "next video", "fuel"))
chapters.append(c)

CTX = ["ute", "ute", "dealer", "ute", "ute", "ute", "ute", "dealer", "money", "dealer", "ute"]
print(A.finish(chapters, "AUS15_Ute_Price_War.mp4", CTX, subtitles="AUS15.ass"))
