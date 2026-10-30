#!/usr/bin/env python3
"""AUS09 What changes for EV owners in 2027: full edit, shots anchored to phrases.
    python3 build_aus09.py <narration_dir> > episode.json   (run from the work folder)
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "engine"))
import aus_kit as A
from aus_kit import P, photo, stat, bars, say, cta, title, ch, questions

PHOTOS = {
    "ev": ["ai:ai_ev_driveway", "h_ev_charge", "h_home_charger", "h_ev2", "h_charge2", "h_suburb"],
    "office": ["ai:ai_lease_meeting", "h_contract", "h_office2"],
    "premium": ["ai:ai_premium_ev_showroom", "m_bmw_ix", "m_eqe", "m_polestar", "m_taycan"],
    "road": ["ai:ai_kms_road", "h_road_sydney", "h_highway", "h_city", "h_highway2", "h_roadtrip"],
    "calendar": ["ai:ai_calendar_deadline", "h_calendar"],
    "charger": ["ai:ai_regional_charger", "ai:ai_ev_queue"],
    "family": ["ai:ai_family_ev"],
    "port": ["ai:ai_ev_port", "h_dealer"],
    "money": ["h_money", "h_calc", "h_aud"], "fuel": ["h_fuel"], "politics": ["h_parliament"], "eu": ["h_eu_flag"],
    "odo": ["h_odometer"],
    "cheap": ["m_atto1", "m_mg4", "m_kona_ev", "m_ev5", "m_sealion7"],
    "tesla": ["m_model_y", "m_model_3", "m_zeekr", "h_tesla", "h_byd"],
}
CLIPS = json.load(open(os.path.join(HERE, "clips.json")))
GENERIC = CLIPS.pop("_generic", [])
FALLBACK = {"ev": ["charger", "cheap"], "office": ["money"], "premium": ["tesla"], "road": ["odo", "ev"], "calendar": ["office"],
            "charger": ["ev"], "family": ["ev", "cheap"], "port": ["cheap"], "money": ["office"], "fuel": ["road"],
            "politics": ["money"], "eu": ["politics"], "odo": ["road"], "cheap": ["ev"], "tesla": ["ev"]}
RES = ["m_model_y/1", "m_model_y/3", "m_model_3/1", "m_sealion7/1", "m_atto1/1", "m_atto1/3", "m_mg4/1", "m_kona_ev/1",
       "m_polestar/1", "m_polestar/3", "m_bmw_ix/1", "m_bmw_ix/3", "m_eqe/3", "m_taycan/1", "m_ev5/1", "m_zeekr/3"]
A.setup(sys.argv[1], os.path.join(HERE, "skip.json"), PHOTOS, CLIPS, GENERIC, FALLBACK,
        ["ev", "road", "cheap", "money", "office", "tesla", "charger"], reserved=RES)
chapters = []

c = ch("ch00_hook", 0.6)
c.at(0, stat("$17,000+", "tax savings some EV lease owners could lose", "NRMA · 2026 budget", red=True, count=False))
c.at("a change that starts on the 1st of April 2027", P("calendar", cap="1 April 2027|FBT change starts"))
c.at("In July 2027, New South Wales plans", P("road", cap="NSW · July 2027|per-km charge for EVs"))
c.at("a new luxury car tax threshold", P("premium"))
c.at("And the emissions rules", P("port"))
c.at("Some of these changes will save you money", say("Some save. Some cost.", "SAVE", 140))
c.at("depending on when you buy", P("money"))
c.at("So in this video", title("EV Changes in 2027", "what every Aussie EV buyer must know", "Australia", "ev"))
questions(c, ["What's confirmed", "What's still being decided", "What it means for you"],
          ["what's confirmed", "what's still being decided", "what it means if you're thinking"])
c.at("the timing of your purchase has never mattered more", say("Timing has never mattered more.", "TIMING", 125))
chapters.append(c)

c = ch("ch01")
c.at(0, title("Change 1", "The Electric Car Discount (FBT)", "1 April 2027", "office"))
c.at("Since 2022, electric cars provided by an employer", P("office"))
c.at("currently $91,387", stat("$91,387", "EV FBT cap – fuel-efficient LCT threshold", "ATO", count=False))
c.at("here's how a novated lease works", P("office"))
c.at("Your employer pays the car's costs", P("money"))
c.at("For eligible EVs, that tax has been zero", say("FBT on eligible EVs: $0", "$0", 140))
c.at("For a lot of Australians, this has been the single biggest reason", P("ev"))
c.at("Australia's most effective demand-side lever", say("\"Australia's most effective demand-side lever for EV uptake.\" – NALSPA", "MOST EFFECTIVE", 90))
c.at("But it's been expensive for the government", P("politics"))
c.at("the revenue costs of the Electric Car Discount", say("\"…revenue costs… increasing significantly.\"", "SIGNIFICANTLY", 110))
c.at("And it's been popular", P("family"))
c.at("So in May 2026, the government confirmed", P("politics", cap="May 2026|wound back in 3 stages"))
chapters.append(c)

c = ch("ch02")
c.at(0, say("3 stages", "3", 150))
c.at("Stage one: until the 31st of March 2027", stat("to 31 Mar 2027", "full exemption – nothing changes", "Federal government", count=False))
c.at("Stage two: from the 1st of April 2027", stat("$75,000", "full exemption cap from 1 April 2027", "Federal government", red=True, count=False))
c.at("get a twenty-five per cent discount", stat("25%", "FBT discount for EVs over $75k", "Federal government", count=False))
c.at("Stage three: from the 1st of April 2029", stat("1 Apr 2029", "all eligible EVs: 25% discount only", "Federal government", red=True, count=False))
c.at("First, existing leases are protected", say("Existing leases are protected.", "PROTECTED", 130))
c.at("What does \"grandfathered\" mean", P("office"))
c.at("when that lease ends", P("calendar"))
c.at("plug-in hybrids already lost their exemption", stat("1 Apr 2025", "PHEVs lost the FBT exemption", "ATO", count=False))
c.at("The NRMA estimated", stat("$17,000+", "potential lost tax savings for some", "NRMA", red=True, count=False))
c.at("Your own number depends", P("money"))
c.at("The Electric Vehicle Council welcomed", P("ev"))
c.at("good news for everyday Australians", say("\"Good news for everyday Australians…\" – EVC", "GOOD NEWS", 105))
chapters.append(c)

c = ch("ch03")
c.at(0, say("What it means for you", "YOU", 140))
c.at("If you're looking at an EV under $75,000", P("cheap"))
c.at("seven electric cars available for under forty", stat("7", "EVs under $40,000 drive-away", "CarsGuide · Feb 2026"))
c.at("the BYD Atto 1 started from $23,990", photo("m_atto1", 1, "in", cap="BYD Atto 1|from $23,990 + ORC"))
c.at("But if you're looking at an EV between $75,000", P("premium"))
c.at("Sign an eligible novated lease before", P("office"))
c.at("Sign after, and you only get", P("calendar"))
c.at("I'd expect a rush", P("port"))
c.at("talk to your employer and your lease provider now", P("office"))
c.at("One warning: delivery times", P("port"))
c.at("ordering in late March might be too late", say("Late March may be too late.", "TOO LATE", 125))
chapters.append(c)

c = ch("ch04")
c.at(0, title("Change 2", "Luxury Car Tax", "1 July 2027", "premium"))
c.at("an extra tax of thirty-three per cent", stat("33%", "LCT on every dollar over the threshold", "ATO", count=False))
c.at("Prime Minister Anthony Albanese announced", P("eu", cap="24 March 2026|Australia–EU trade deal"))
c.at("remove the five per cent tariff", stat("5% → 0%", "tariff on European cars", "Australia–EU FTA", count=False))
c.at("a new luxury car tax category for zero-emissions", stat("$120,000", "new LCT threshold for zero-emissions vehicles", "CarExpert", count=False))
c.at("The trade deal still needs to be formally ratified", P("politics"))
c.at("an EV priced at $100,000", A.price("EV priced at $100,000 · LCT", "~$2,842", "$0", "today", "under $120k threshold", None, "illustration"))
c.at("But don't get too excited", P("premium"))
c.at("a narrow change that will only affect less than one per cent", say("\"…less than one per cent of vehicles sold.\" – AADA", "ONE PER CENT", 100))
c.at("think Polestar, BMW, Mercedes-Benz", photo("m_polestar", 1, "in"))
c.at("everyday BYD or MG", photo("m_mg4", 1, "left"))
chapters.append(c)

c = ch("ch05")
c.at(0, P("ev"))
c.at("Tell me in the comments", cta("Buy sooner – or later?", "Tell me in the comments"))
c.at("hit subscribe", cta("Subscribe", "what's changing in 2027"))
chapters.append(c)

c = ch("ch06")
c.at(0, title("Change 3", "Paying per kilometre", "NSW · July 2027", "road"))
c.at("Every time you fill up with petrol", P("fuel"))
c.at("EV drivers don't buy fuel", P("ev"))
c.at("the federal government temporarily halved it", bars("Fuel excise (cents/litre)", [["Normal", 52.6], ["1 Apr–1 Jul 2026", 26.3]], None, "NRMA"))
c.at("fell to seventy per cent", stat("70%", "of fuel excise reinvested in roads (2026 budget)", "NRMA", count=False))
c.at("Chasing Cars estimated that EVs cost", stat("$130–165M", "lost fuel excise from EVs a year", "Chasing Cars", count=False))
c.at("New South Wales plans to fix that", P("road"))
c.at("about 2.974 cents per kilometre", bars("NSW proposed charge (cents/km)", [["EV", 2.974], ["Plug-in hybrid", 2.379]], None, "Chasing Cars · July 2026"))
c.at("forecast to raise $440 million", stat("$440M", "forecast revenue · first 3 years", "AAP", count=False))
c.at("At 12,000 to 15,000 kilometres a year", bars("Per year · 12–15k km", [["EV road charge", 450], ["Petrol excise (7L/100km)", 550]], None, "Chasing Cars", prefix="up to $"))
c.at("plug-in hybrids would pay the charge too", P("fuel"))
c.at("But there's a legal problem", say("The High Court problem.", "HIGH COURT", 130))
c.at("in 2023 the High Court found", P("politics", cap="Victoria 2.8c/km|struck down · 2023"))
c.at("NSW Treasurer Daniel Mookhey", say("\"…it remains the intent of the NSW government to enact the law\" – NSW Treasurer", "INTENT", 85))
c.at("refer its powers to NSW", P("politics"))
chapters.append(c)

c = ch("ch07")
c.at(0, P("politics"))
c.at("accelerating work", say("\"Accelerating work\" – Treasurer, 2025", "ACCELERATING", 120))
c.at("it may not be the time for it right now", say("\"It may not be the time for it right now.\" – Transport Minister", "NOT THE TIME", 95))
c.at("one state charging EV drivers", P("road"))
c.at("everybody who uses roads should contribute", say("\"Everybody who uses roads should contribute.\" – NSW Govt", "CONTRIBUTE", 95))
c.at("only start once EVs make up thirty per cent", stat("30%", "EV fleet share before charging – EVC's view", "Electric Vehicle Council", count=False))
c.at("fails on all three fronts", say("\"Fails on all three fronts.\" – EVC", "FAILS", 120))
c.at("twenty-eight per cent of likely EV buyers", stat("28%", "of likely EV buyers would be dissuaded", "Sydney University via EVC", red=True))
c.at("New Zealand", bars("NZ EV share of sales (per EVC)", [["Before", 20.6], ["After charge", 3.8, "red"]], None, "Electric Vehicle Council", suffix="%"))
c.at("thinly veiled tax", say("\"Thinly veiled tax\" – Polestar Australia", "TAX", 120))
c.at("It's worth putting those numbers side by side", P("money"))
c.at("running an EV on home charging is still likely", P("ev"))
c.at("My take", say("Coming eventually. The fight is when and how much.", "WHEN", 100))
chapters.append(c)

c = ch("ch08")
c.at(0, title("Change 4", "Tougher emissions rules", "the good news", "port"))
c.at("drops from 117 grams", bars("Passenger car target (g/km)", [["2026", 117], ["2027", 92], ["2028", 68], ["2029", 58]], None, "NVES"))
c.at("Car makers that miss their targets", P("money"))
c.at("the fastest way to sell more EVs is to cut prices", say("Cut prices to sell more EVs.", "CUT PRICES", 125))
c.at("Hyundai cut up to $13,857", photo("m_kona_ev", 1, "in", cap="Hyundai Kona Electric|up to $13,857 off"))
c.at("sixty million dollars to Hyundai Capital", stat("$60M", "CEFC → cheaper Hyundai & Kia EV finance", "CarsGuide", count=False))
c.at("More than sixty new EV models", stat("60+", "new EV models expected in Australia", "Yahoo / industry", count=False))
c.at("The Australian Automobile Association reported", stat("31.61%", "BEV + PHEV share · June quarter 2026", "AAA"))
c.at("battery electric cars made up more than twenty-four", photo("m_model_y", 1, "left", cap="EVs: 24%+ of sales|September 2026"))
c.at("the federal opposition has promised to scrap", P("politics"))
c.at("forty million dollars to new regional and kerbside chargers", stat("$40M", "regional & kerbside chargers · 2026 budget", "NRMA", count=False))
c.at("especially outside the big cities", P("charger"))
chapters.append(c)

c = ch("ch09")
c.at(0, say("Buy before 2027 – or wait?", "WAIT", 130))
c.at("If you're buying an EV over $75,000 through a novated lease", say("EV over $75k on lease → before 31 March 2027", "31 MARCH", 95))
c.at("If you're buying a premium EV between", say("Premium EV $91k–$120k → maybe after 1 July 2027", "1 JULY", 95))
c.at("get any promise in writing", P("office"))
c.at("If you live in New South Wales", say("NSW → budget ~$360–$450/yr", "NSW", 120))
c.at("That's still less than the fuel excise", P("fuel"))
c.at("If you're buying a cheaper EV, under $75,000", P("cheap"))
c.at("Shop around, compare drive-away prices", P("port"))
c.at("And think about resale", P("premium"))
c.at("buy a car you're happy to keep", P("family"))
c.at("don't let a deadline push you into the wrong car", say("Don't let a deadline pick your car.", "DEADLINE", 115))
chapters.append(c)

c = ch("ch10", 2.5)
c.at(0, P("ev"))
c.at("On the 1st of April 2027, the full fringe benefits", stat("1 Apr 2027", "FBT: full exemption only ≤ $75k", None, count=False))
c.at("In July 2027, NSW plans", stat("Jul 2027", "NSW per-km EV charge (planned)", None, red=True, count=False))
c.at("a new $120,000 luxury car tax threshold", stat("$120k", "new ZEV LCT threshold (due Jul 2027)", None, count=False))
c.at("tougher emissions targets", P("port"))
questions(c, ["31 March 2027", "1 April 2027", "1 July 2027"], ["The 31st of March 2027", "The 1st of April 2027: the new rules", "The 1st of July 2027"])
c.at("All of them make timing more important", say("Timing matters more than ever.", "TIMING", 125))
c.at("If this helped, hit like", cta("Like · Subscribe · Share", "with someone going electric"))
questions(c, ["Sooner – or later?"], ["will these changes make you buy"])
c.at("in the next video", title("New Cars Coming in 2027", "10 that could shake up Australia", "next video", "port"))
chapters.append(c)

CTX = ["ev", "office", "money", "cheap", "premium", "ev", "road", "road", "cheap", "ev", "ev"]
print(A.finish(chapters, "AUS09_EV_Changes_2027.mp4", CTX, subtitles="AUS09.ass"))
