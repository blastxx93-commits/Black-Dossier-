#!/usr/bin/env python3
"""AUS11 Used EV prices in 2027: full edit, every shot anchored to the phrase it illustrates.
    python3 build_aus11.py <narration_dir> > episode.json   (run from the work folder)
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "engine"))
import aus_kit as A
from aus_kit import P, photo, stat, bars, say, cta, title, ch, questions

PHOTOS = {
    "auction": ["ai:ai_auction_evs", "h_auction"],
    "lease": ["ai:ai_lease_return", "h_keys"],
    "battery": ["ai:ai_battery_test", "h_battery"],
    "regional": ["ai:ai_regional_ev", "h_country"],
    "used": ["ai:ai_price_board", "h_used_lot", "ai:ai_couple_used_ev"],
    "charge": ["ai:ai_home_charge_used", "h_ev_charge"],
    "money": ["h_calc"], "fuel": ["h_fuel"], "online": ["h_laptop"], "mechanic": ["h_mechanic"], "tyre": ["h_tyre"],
    "evs": ["m_model_y", "m_model_3", "m_atto3", "m_mg4", "m_kona_ev", "m_ora", "m_polestar2", "m_ioniq5", "m_ev6", "m_atto1"],
}
CLIPS = json.load(open(os.path.join(HERE, "clips.json")))
GENERIC = CLIPS.pop("_generic", [])
FALLBACK = {"auction": ["used"], "lease": ["used", "money"], "battery": ["charge"], "regional": ["used"], "used": ["auction", "evs"],
            "charge": ["battery", "evs"], "money": ["online"], "fuel": ["charge"], "online": ["money"], "mechanic": ["battery"],
            "tyre": ["mechanic"], "evs": ["used"]}
RES = ["m_model_y/1", "m_model_y/3", "m_model_3/1", "m_model_3/3", "m_atto3/1", "m_atto3/3", "m_mg4/1", "m_mg4/3", "m_kona_ev/1",
       "m_kona_ev/3", "m_ora/1", "m_ora/3", "m_atto1/1", "m_atto1/3", "m_polestar2/1", "m_polestar2/3"]
A.setup(sys.argv[1], os.path.join(HERE, "skip.json"), PHOTOS, CLIPS, GENERIC, FALLBACK,
        ["used", "charge", "evs", "money", "auction"], reserved=RES)
A.CLIP_TARGET = 0.55   # channel request (31/10): more clips
A.MAX_HOLD, A.KEEP = 13.0, 8.5
chapters = []

c = ch("ch00_hook", 0.6)
c.at(0, stat("-48%", "2022 Tesla Model Y RWD value lost", "Savvy / RedBook · March 2026", red=True))
c.at("a 2022 Tesla Model Y", photo("m_model_y", 1, "in", cap="Tesla Model Y|~48% below new price"))
c.at("A BYD Atto 3 was down about thirty-nine", photo("m_atto3", 1, "left", cap="BYD Atto 3|~39% below new price"))
c.at("That may only be the beginning", say("That may only be the beginning.", "BEGINNING", 130))
c.at("a wave of electric cars is set to hit", P("auction"))
c.at("Cars that were bought on novated leases", P("lease"))
c.at("ex-novated lease volumes", stat("+157%", "ex-novated lease EVs at Pickles · Sept qtr vs March qtr 2026", "Pickles", red=True))
c.at("The volumes coming through now", say("\"The volumes coming through now are really just the beginning.\" – Pickles", "BEGINNING", 92))
c.at("So what happens to used EV prices in 2027", title("Used EV Prices in 2027", "crash – or opportunity?", "Australia", "used"))
questions(c, ["The real 2026 numbers", "Why 2027 is a turning point", "Who loses value fastest", "What to check"],
          ["the real 2026 numbers", "why 2027 could be a turning point", "which EVs are losing value", "exactly what to check"])
c.at("getting the timing wrong", P("money"))
chapters.append(c)

c = ch("ch01")
c.at(0, P("lease"))
c.at("In July 2022, the federal government", say("July 2022 · EVs exempt from FBT on novated leases", "FBT", 100))
c.at("Suddenly, a lot of workers could afford", P("charge"))
c.at("Novated leases typically run", stat("3–5 yrs", "typical novated lease term", None, count=False))
c.at("When a lease ends", P("lease"))
c.at("all arriving at roughly the same time", P("auction"))
c.at("the Electric Car Discount had just reached its fourth anniversary", P("lease", cap="July 2026|4 years of the Electric Car Discount"))
c.at("Pickles reported ex-novated volumes", bars("Ex-novated EVs at Pickles (vs Q1 2026)", [["Q2 2026", 118], ["Q3 2026", 157, "red"]], None,
     "Pickles · Oct 2026", prefix="+", suffix="%"))
c.at("more than 100,000 battery electric cars were sold new", stat("100,000+", "new EVs sold in Australia in 2025 (8.3%)", "CarsGuide"))
c.at("By September 2026, EVs were making up", stat("24%+", "EV share of new sales · Sept 2026", "FCAI / EVC"))
c.at("Every one of those cars will eventually", P("evs"))
c.at("the Electric Car Discount itself is being wound back", stat("$75,000", "full FBT exemption cap from 1 April 2027", "Federal government", red=True, count=False))
c.at("how many decide to buy used instead", P("used"))
chapters.append(c)

c = ch("ch02")
c.at(0, say("2026: a strong year for used EVs", "STRONG", 115))
c.at("Why? Fuel", P("fuel"))
c.at("used EV sales in the first half of 2026 rose", bars("Used sales · H1 2026 vs H1 2025", [["Used EVs", 54], ["All used cars", -6.6, "red"]], None,
     "AADA / AutoGrab", suffix="%"))
c.at("And used EVs started selling faster", bars("Days to sell a used EV", [["January", 60], ["June", 40]], None, "NRMA / AutoGrab"))
c.at("Pickles had its biggest quarter on record", stat("440+", "used EVs sold by Pickles · Sept qtr 2026 (record)", "Pickles"))
c.at("Over the twelve months to September", stat("1,580+", "used EVs sold in 12 months – more than double", "Pickles"))
c.at("Which brands are people buying second-hand", bars("Used sales by brand · H1 2026", [["Tesla", 7402], ["MG", 2582], ["Kia", 1927],
     ["BYD", 1767], ["Volkswagen", 990], ["Polestar", 732]], None, "AADA / AutoGrab via NRMA"))
c.at("Interest exploded too", P("online"))
c.at("more than 20,000 visitors", stat("20,436", "EV page visitors at Pickles · Q2 2026 (vs 2,156)", "Pickles"))
c.at("EV searches jumped almost seventy-seven", stat("+76.7%", "EV searches in one week · March 2026", "carsales"))
c.at("And it's not just city buyers", P("regional"))
c.at("regional buyers took thirty-two per cent", stat("32%", "of Pickles' used EV buyers were regional · FY26", "Pickles"))
c.at("In Queensland, almost half", P("regional", cap="Queensland|almost half of used EVs went regional"))
chapters.append(c)

c = ch("ch03")
c.at(0, say("So what happened to prices?", "PRICES", 140))
c.at("Its Used EV Index rose from 104", bars("Used EV Index (Datium)", [["Feb 2026", 104], ["May 2026", 122], ["Sept 2026", 107]], None,
     "Pickles / Datium Insights"))
c.at("used EV prices jumped during the fuel spike", P("fuel"))
c.at("the average used EV sale price at Pickles", bars("Average used EV price at Pickles · 2026", [["January", 35500], ["April", 41500],
     ["May", 35500], ["June", 31500, "red"]], None, "NRMA", prefix="$"))
c.at("And the average odometer reading went up", stat("51,000 km", "average odometer · May–June (from ~29,000)", "NRMA / Pickles", count=False))
c.at("More older, higher-kilometre EVs", P("used"))
c.at("the long-term picture for EV depreciation", bars("Value kept after 2 years", [["Toyota RAV4", 88], ["LandCruiser", 88], ["HiLux", 85],
     ["Tesla Model Y", 58, "red"], ["Tesla Model 3", 54, "red"], ["BYD Atto 3", 54, "red"], ["MG4", 50, "red"]], None,
     "Pickles / Datium · 2025", suffix="%"))
c.at("There's another way to measure this", P("money"))
c.at("the average residual value for hybrids", bars("Residual value · May 2026 (1–5 yrs old)", [["Hybrid", 94.3], ["Plug-in hybrid", 83.9],
     ["EV", 74.7, "red"]], None, "AADA / AutoGrab", suffix="%"))
c.at("But fewer EVs needed a discount", bars("Share of used cars discounted · May 2026", [["Diesel", 51.7, "red"], ["Petrol", 50.5, "red"],
     ["EV", 44.0]], None, "AADA / AutoGrab", suffix="%"))
c.at("When thousands of ex-lease EVs arrive", say("Will demand keep up?", "DEMAND", 140))
chapters.append(c)

c = ch("ch04")
c.at(0, P("evs"))
c.at("Tell me in the comments", cta("What would you pay?", "3-year-old Model 3 or Atto 3 – comments"))
c.at("hit subscribe", cta("Subscribe", "what's changing in 2027"))
chapters.append(c)

c = ch("ch05")
c.at(0, title("Who Loses Value Fastest", "and why", "used EVs", "evs"))
c.at("The biggest reason is new car prices", P("money"))
c.at("the BYD Atto 1", photo("m_atto1", 1, "in", cap="BYD Atto 1|new from $23,990 + ORC"))
c.at("When new cars get cheaper", say("New gets cheaper → used gets cheaper.", "CHEAPER", 115))
c.at("Tesla's repeated price cuts", photo("m_model_3", 1, "left", cap="Tesla Model 3|price cuts reset used values"))
c.at("Early long-range EVs, like the Hyundai Kona Electric", photo("m_kona_ev", 1, "right"))
c.at("earlier models can look dated quickly", P("used"))
c.at("Savvy, using RedBook data", bars("Below new price · March 2026", [["2022 Tesla Model Y RWD", 48, "red"], ["BYD Atto 3", 39, "red"]], None,
     "Savvy / RedBook", prefix="-", suffix="%"))
c.at("creates real opportunities", say("\"…real opportunities for Australians looking at the used EV market.\"", "OPPORTUNITIES", 95))
c.at("Every dollar an owner loses", P("money"))
c.at("Hyundai cut up to $13,857", photo("m_kona_ev", 3, "in", cap="Hyundai Kona Electric|up to $13,857 off new"))
c.at("Every cut on a new car", P("evs"))
c.at("like the GWM Ora", photo("m_ora", 1, "left", cap="GWM Ora|fewer direct rivals"))
chapters.append(c)

c = ch("ch06")
c.at(0, title("The Good News", "battery health", "Pickles data", "battery"))
c.at("The biggest fear people have", P("battery"))
c.at("On average, the state of health was ninety-six", bars("Battery state of health (2,500+ EVs)", [["All EVs", 96], ["Over 5 years old", 93],
     ["Over 120,000 km", 89]], None, "Pickles · Oct 2026", suffix="%"))
c.at("That's a lot better than many people expect", say("Better than most people expect.", "BETTER", 130))
c.at("charging habits, climate", P("charge"))
c.at("The average used EV sold by Pickles", stat("3.1 yrs", "average age · ~44,000 km", "Pickles · Sept qtr 2026", count=False))
c.at("buyers are becoming more comfortable", P("used"))
c.at("statutory write-off EVs sold for sixteen", bars("Write-off EVs vs petrol/diesel", [["Statutory write-off", 16], ["Repairable write-off", 71]], None,
     "Pickles", prefix="+", suffix="%"))
c.at("Damaged EVs are in demand", P("mechanic"))
chapters.append(c)

c = ch("ch07")
c.at(0, title("2027", "crash or boom?", "my honest read", "auction"))
c.at("On one side, supply is going up", say("Supply ↑", "↑", 160))
c.at("More ex-novated EVs are coming back", P("auction"))
c.at("On the other side, demand is also going up", say("Demand ↑", "↑", 160))
c.at("dealers increasing their participation", say("\"…tells us they're becoming more confident.\" – Pickles", "CONFIDENT", 100))
c.at("we would expect the used EV market to continue to mature", say("\"…continue to mature.\" – AADA", "MATURE", 125))
questions(c, ["Fuel prices", "New EV prices", "FBT change · Apr 2027", "NSW road charge · Jul 2027"],
          ["Fuel prices – if", "New EV prices – if", "The fringe benefits tax change", "the planned NSW road user charge"])
c.at("And don't forget the condition of the cars", P("lease"))
c.at("full service histories", P("mechanic"))
c.at("rather than a single crash", say("Not one crash – a bigger, tougher market.", "BIGGER", 105))
chapters.append(c)

c = ch("ch08")
c.at(0, title("Selling Your EV?", "4 things to do", "owners", "used"))
c.at("First, know your numbers", say("1 · Know your numbers", "1", 130))
c.at("Check comparable listings", P("online"))
c.at("Second, think about timing", say("2 · Think about timing", "2", 130))
c.at("Holding may suit people", P("money"))
c.at("Also, think about where you sell", P("regional"))
c.at("Third, prove the battery", say("3 · Prove the battery", "3", 130))
c.at("Keep your service history", P("mechanic"))
c.at("And fourth, if your car is coming off a novated lease", say("4 · Residual vs market value", "4", 120))
c.at("If it's worth less, talk to your lease provider", P("lease"))
chapters.append(c)

c = ch("ch09")
c.at(0, title("Buying a Used EV?", "7-step checklist", "2027", "used"))
c.at("Step one: ask for a battery health report", say("1 · Battery health report", "1", 130))
c.at("Many dealers and auction houses", P("battery"))
c.at("Step two: check the battery warranty", say("2 · Battery warranty left", "2", 130))
c.at("Step three: check the charging equipment", say("3 · Charging gear", "3", 130))
c.at("where will you charge it at home", P("charge"))
c.at("Step four: compare with new", say("4 · Compare with new", "4", 130))
c.at("make sure the used one is genuinely cheaper", P("money"))
c.at("Step five: check the model's history", say("5 · Recalls & updates", "5", 130))
c.at("Step six: get a pre-purchase inspection", say("6 · Pre-purchase inspection", "6", 125))
c.at("Check the tyres too", P("tyre"))
c.at("Step seven: if you're in New South Wales", say("7 · NSW road charge from July 2027", "7", 115))
chapters.append(c)

c = ch("ch10", 2.5)
c.at(0, say("Will used EV prices crash in 2027?", "CRASH", 115))
c.at("The supply wave is real", P("auction"))
questions(c, ["+54% used EV sales", "+157% ex-lease volumes", "Index 104 → 122 → 107", "96% battery health"],
          ["Used EV sales up about fifty-four", "Pickles' ex-novated lease volumes up", "The Used EV Index up", "Average battery health"])
c.at("But demand has grown too", P("regional"))
c.at("don't rely on old assumptions", P("online"))
c.at("If you're buying, 2027 could be", say("Buyers: 2027 could be a great year.", "GREAT", 120))
c.at("If this helped", cta("Like · Subscribe · Share", "with someone eyeing a used EV"))
questions(c, ["Would you buy a used EV in 2027?"], ["would you buy a second-hand electric car"])
c.at("in the next video", title("GWM vs Toyota RAV4", "the plug-in hybrid fight", "next video", "charge"))
chapters.append(c)

CTX = ["used", "lease", "used", "money", "evs", "evs", "charge", "auction", "used", "used", "used"]
print(A.finish(chapters, "AUS11_Used_EV_Prices_2027.mp4", CTX, subtitles="AUS11.ass"))
