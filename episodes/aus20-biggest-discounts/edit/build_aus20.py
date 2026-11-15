#!/usr/bin/env python3
"""AUS20 the 10 biggest new-car deals in Australia (Nov 2026): full edit, shots anchored to phrases.
    python3 build_aus20.py <narration_dir> > episode.json   (run from the work folder)
Opens on car photos with the impact number as caption (rule 01/11/2026). New 'electric' template (rule 14/11/2026).
No AI images: real scene photos only, every file reviewed.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "engine"))
import aus_kit as A
from aus_kit import P, photo, stat, bars, say, cta, title, ch, questions, rank

PHOTOS = {
    "dealer": ["h_dealer", "h_lot", "h_keys"],
    "street": ["h_traffic", "h_outback"],
    "money": ["h_money"],
    "ev": ["h_ev"],
    "ute": ["m_hilux", "m_cannon", "m_triton", "m_shark6", "m_ranger"],
    "cars": ["m_h6", "m_hrv", "m_crv", "m_outlander", "m_koleos", "m_arkana", "m_sealion5", "m_seal6", "m_vitara"],
    "fuel": ["h_outback"], "sale": ["h_dealer"],
}
CLIPS = json.load(open(os.path.join(HERE, "clips.json")))
GENERIC = CLIPS.pop("_generic", [])
FALLBACK = {"dealer": ["street", "cars"], "street": ["dealer", "cars"], "money": ["dealer"], "ev": ["street"], "cars": ["street"],
            "ute": ["street", "cars"], "fuel": ["street"], "sale": ["dealer"], "port": ["street"]}
RES = ["m_tasman/1", "m_tasman/3", "m_atto1/1", "m_atto1/3", "m_dolphin/1", "m_atto2/1", "m_evitara/3", "m_jimny/1", "m_jimny/3",
       "m_swift/1", "m_ranger/1", "m_ranger/3", "m_duster/1", "m_duster/3", "m_sealion5/1", "m_shark6/1", "m_seal6/1", "m_hilux/3", "m_hilux/1",
       "m_jolion/1", "m_h6/1", "m_cannon/1", "m_crv/1", "m_zrv/1", "m_tiggo4/3", "m_triton/1", "m_outlander/1", "m_q4/1", "m_q4/3",
       "m_arkana/1", "m_koleos/1", "m_accord/3"]
A.setup(sys.argv[1], os.path.join(HERE, "skip.json"), PHOTOS, CLIPS, GENERIC, FALLBACK, ["dealer", "street", "cars"], reserved=RES)
A.CLIP_TARGET = 0.6
A.MAX_HOLD, A.KEEP = 15.0, 9.5
chapters = []
SRC = "VFACTS via CarExpert"

c = ch("ch00_hook", 0.6)
c.at(0, photo("m_tasman", 1, "in", cap="$10,000+|off a brand-new ute"))
c.at("Not a used car", P("ute"))
c.at("And the reason is brutal", P("ute", cap="Kia Tasman|target: 20,000 in year one"))
c.at("Fifteen months after launch", P("street", cap="7,898|sold in 15 months"))
c.at("Right now, you can buy a brand-new car", photo("m_atto1", 1, "in", cap="BYD Atto 1|$19,990 drive-away"))
c.at("Toyota – a brand that almost never discounts", photo("m_hilux", 3, "left", cap="Toyota HiLux|$4,000 bonus"))
c.at("Ford is offering five thousand", photo("m_ranger", 1, "right", cap="Ford Ranger|$5,000"))
c.at("And Black Friday deals", P("sale"))
c.at("So in this video, I'm counting down", title("10 Biggest New-Car Deals", "Australia · November 2026", "deals", "dealer"))
c.at("Stay to the end", P("dealer"))
chapters.append(c)

c = ch("ch01")
c.at(0, P("street"))
c.at("Australians bought 107,493", stat("107,493", "new vehicles · October 2026 · record October", SRC))
c.at("Electric car sales were up 237", stat("+237%", "EV sales · Oct 2026 vs Oct 2025", SRC))
c.at("That means a lot of brands are sitting on stock", P("dealer"))
c.at("Mitsubishi sales were down 50", bars("October 2026 · brands", [["Renault", -58.2], ["Mitsubishi", -50.0], ["Hyundai", -28.6], ["Ford", -3.4]],
     None, SRC, suffix="%"))
c.at("And there's a second pressure", P("sale"))
c.at("So brands are throwing everything", P("money"))
c.at("A quick note before we start", say("Get the final price in writing.", "IN WRITING", 125))
c.at("Let's go", P("street"))
chapters.append(c)

c = ch("ch02")
c.at(0, rank(10, "The Fuel Card War", "m_tiggo4", 3, "up to $3,000", "Chery · Mitsubishi"))
c.at("Some brands don't want to cut the price", P("fuel"))
c.at("Chery is offering a two-thousand-dollar fuel card", bars("Chery · fuel cards", [["Tiggo 7", 2000], ["Tiggo 4", 1500], ["E5 cashback", 2000]], None,
     "CarSorted", prefix="$"))
c.at("Mitsubishi is doing the same thing", photo("m_triton", 1, "in", cap="Mitsubishi Triton|$3,000 fuel card"))
c.at("Outlander LS Black Edition", photo("m_outlander", 1, "left", cap="Outlander LS Black Edition|$47,990 drive-away"))
c.at("Now, here's the catch with fuel cards", say("A fuel card is NOT a discount.", "NOT", 125))
c.at("If a dealer offers you a fuel card", P("dealer"))
c.at("Mitsubishi's sales halved in October", stat("-50%", "Mitsubishi sales · October 2026", SRC, red=True))
chapters.append(c)

c = ch("ch03")
c.at(0, rank(9, "Honda Plate Clearance", "m_crv", 1, "up to $3,000 gift card", "until 31 Jan 2027"))
c.at("The biggest gift card is three thousand dollars", photo("m_zrv", 1, "in", cap="ZR-V e:HEV X|$3,000 gift card"))
c.at("And the Civic, the HR-V", bars("Honda gift cards", [["CR-V / ZR-V e:HEV X", 3000], ["Other CR-V / ZR-V hybrids", 1500],
     ["Civic · HR-V · Prelude · Accord", 1000]], None, "CarExpert", prefix="$"))
c.at("Honda is throwing in the first five", stat("$1,395", "5 free services · 5 years / 50,000 km", "CarExpert", count=False))
c.at("So on the best-value models", P("cars"))
c.at("Honda's annual service price has just gone up", A.price("Honda service", "$199", "$279", "last month", "now · per service", None, "CarExpert"))
c.at("And if you're thinking about the Accord", photo("m_accord", 3, "left", cap="Honda Accord|59 sold in 9 months"))
chapters.append(c)

c = ch("ch04")
c.at(0, rank(8, "GWM Haval", "m_jolion", 1, "$3,000 deposit", "until 30 Nov"))
c.at("GWM is a Chinese brand", stat("-0.3%", "GWM sales · October 2026", SRC, red=True, count=False))
c.at("the Haval Jolion Premium Hybrid is", bars("GWM drive-away deals", [["Jolion Hybrid", 32990], ["H6 Lux", 35990], ["Cannon", 39990],
     ["H6 Ultra Hybrid", 43990]], None, "GWM / CarSorted", prefix="$"))
c.at("The bigger Haval H6 Ultra Hybrid", photo("m_h6", 1, "in", cap="Haval H6 Hybrid|+ $3,000 deposit"))
c.at("And the Cannon ute", photo("m_cannon", 1, "left", cap="GWM Cannon|from $39,990"))
c.at("Back in October, CarExpert reported", P("dealer"))
c.at("The catch?", P("money"))
chapters.append(c)

c = ch("ch05")
c.at(0, rank(7, "Toyota HiLux", "m_hilux", 1, "$4,000 finance bonus", "SR5 4x4 diesel"))
c.at("In October, the HiLux was the best-selling", stat("5,954", "HiLux sales · October 2026 · #1", SRC))
c.at("But the ute market is getting crowded", P("ute"))
c.at("With the bonus, CarExpert says", bars("HiLux SR5 with bonus (+ ORC)", [["Manual dual-cab", 59990], ["Auto cab-chassis", 60490],
     ["Auto dual-cab", 61990]], None, "CarExpert", prefix="$"))
c.at("Now, here's the catch", say("Minimum $10,000 through Toyota Finance.", "TOYOTA FINANCE", 105))
c.at("So if you were going to pay cash", P("money"))
chapters.append(c)

c = ch("ch06")
c.at(0, rank(6, "BYD Cashback", "m_sealion5", 1, "$4,000 off", "orders by 21 Dec"))
c.at("BYD is the second biggest brand", stat("+153%", "BYD sales · October 2026", SRC))
c.at("BYD is offering four thousand dollars cashback", P("cars"))
c.at("With the cashback", bars("BYD with $4,000 cashback (+ ORC)", [["Sealion 5", 29990], ["Sealion 7", 50990], ["Shark 6", 53900]], None,
     "CarExpert", prefix="$"))
c.at("And the Shark 6 Premium", photo("m_shark6", 1, "in", cap="BYD Shark 6|$53,900"))
c.at("There's also 0.99 per cent finance", photo("m_seal6", 1, "left", cap="BYD Seal 6|0.99% finance"))
c.at("The catch?", P("dealer"))
chapters.append(c)

c = ch("ch07")
c.at(0, rank(5, "Renault Duster", "m_duster", 1, "up to $5,000 off", "1 Nov – 31 Dec"))
c.at("the entry-level Evolution", A.price("Renault Duster Evolution 4x2", "$31,990", "$29,990", "before on-roads", "drive-away", None, "Cars24"))
c.at("The four-wheel-drive versions", photo("m_duster", 3, "in", cap="Duster 4x4|~$34,700–36,250 NSW"))
c.at("In October, the whole Renault brand sold", stat("164", "Renault sales · October 2026 · -58%", SRC, red=True))
c.at("The Arkana sold four", photo("m_arkana", 1, "left", cap="Renault Arkana|4 sales in October"))
c.at("The catch?", photo("m_koleos", 1, "in", cap="Renault Koleos|21 sales in October"))
c.at("Also think about the brand's future", P("dealer"))
chapters.append(c)

c = ch("ch08")
c.at(0, rank(4, "Ford Ranger", "m_ranger", 3, "$5,000 fuel card or discount", "XLT · Wildtrak · Tremor"))
c.at("But it's in a fight", P("ute"))
c.at("So according to CarExpert, Ford is offering", bars("Ford Ranger offers", [["MY26.5", 5000], ["MY27", 4000]], None, "CarExpert", prefix="$"))
c.at("Here's the smart move", say("Take the discount, not the fuel card.", "DISCOUNT", 115))
c.at("As I said earlier", P("money"))
c.at("The catch?", P("street"))
chapters.append(c)

c = ch("ch09")
c.at(0, rank(3, "Suzuki Black Friday", "m_evitara", 3, "up to $5,774 off", "black cars only")
     )
c.at("The biggest saving", A.price("Suzuki e Vitara Ultra", "$57,736", "$51,962", "before saving", "drive-away", None, "CarExpert"))
c.at("The e Vitara Motion", stat("$4,874", "e Vitara Motion saving · now $42,862 drive-away", "CarExpert", count=False))
c.at("And here's the one that'll get attention", photo("m_jimny", 1, "left", cap="Jimny 3-door|$35,762 · save $3,474"))
c.at("The five-door Jimny XL", photo("m_jimny", 3, "in", cap="Jimny XL|$37,562 · save $3,674"))
c.at("The Swift Hybrid starts at", photo("m_swift", 1, "right", cap="Swift Hybrid|$23,022"))
c.at("The catches are important", say("Private buyers · by 30 Nov · not QLD or northern NSW", "30 NOV", 92))
chapters.append(c)

c = ch("ch10")
c.at(0, rank(2, "BYD Atto 1", "m_atto1", 3, "$19,990 drive-away", "orders by 15 Dec"))
c.at("The BYD Atto 1 Essential is now", stat("$19,990", "BYD Atto 1 · drive-away · cheapest new car (Zecar)", "Zecar", count=False))
c.at("The offer runs for orders", photo("m_dolphin", 1, "in", cap="BYD Dolphin|$28,888 drive-away"))
c.at("Atto 2 plug-in hybrid", photo("m_atto2", 1, "left", cap="BYD Atto 2 DM-i|$25,990 drive-away"))
c.at("Think about what that means", P("street"))
c.at("The catch?", P("ev"))
chapters.append(c)

c = ch("ch11")
c.at(0, rank(1, "Kia Tasman", "m_tasman", 3, "$10,000+ saving", "SX+ 4WD · November"))
c.at("So now Kia is cutting hard", A.price("Kia Tasman SX+ 4WD", "$62,390", "$54,990", "+ on-road costs", "drive-away", None, "ACM / Canberra Times"))
c.at("Tasman SX four-wheel drive is now", stat("$49,990", "Tasman SX 4WD · drive-away (was $54,490 + ORC)", "ACM", count=False))
c.at("ABN holders can also get", P("dealer"))
c.at("The catch?", say("2025 cars only · order & deliver in November", "NOVEMBER", 100))
c.at("A ute with a small fan base", P("street"))
chapters.append(c)

c = ch("ch12")
c.at(0, title("Bonus: Audi's $18,000 Cut", "the updated Q4 e-tron", "bonus", "street"))
c.at("According to Cars24", photo("m_q4", 1, "in", cap="Audi Q4 e-tron|from $71,650 + ORC"))
c.at("Because the current Q4 e-tron sold just two", photo("m_q4", 3, "left", cap="Q4 e-tron|2 sales in October · -96%"))
chapters.append(c)

c = ch("ch13", 2.5)
c.at(0, title("How to Get the Best Deal", "before Christmas", "advice", "dealer"))
questions(c, ["Read the fine print", "Drive-away price in writing", "Discount beats fuel card", "Compare finance rates"],
          ["First, read the fine print", "Second, always ask", "Third, prefer a real discount", "Fourth, if a deal depends"])
c.at("Fifth, ask about demonstrators", P("dealer"))
c.at("Sixth, timing", P("sale"))
c.at("And finally, think about resale", P("street"))
c.at("So that's the list", P("ute"))
c.at("which of these deals would you actually take", cta("Which deal would YOU take?", "comments"))
c.at("hit like and subscribe", cta("Like · Subscribe · Share", "with anyone buying before Christmas"))
chapters.append(c)

CTX = ["dealer", "street", "cars", "cars", "cars", "ute", "cars", "cars", "ute", "cars", "ev", "ute", "street", "dealer"]
print(A.finish(chapters, "AUS20_Biggest_Discounts.mp4", CTX, subtitles="AUS20.ass", theme="electric"))
