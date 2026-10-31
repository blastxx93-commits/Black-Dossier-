#!/usr/bin/env python3
"""AUS12 GWM Haval H7 PHEV vs Toyota RAV4 PHEV: full edit, every shot anchored to the phrase it illustrates.
    python3 build_aus12.py <narration_dir> > episode.json   (run from the work folder)
Note: m_h7 photos show the OUTGOING H7 and are only captioned as such. No real photo of the new H7 exists,
so the new car is shown through data graphics, clips and unlabelled AI scenes.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "engine"))
import aus_kit as A
from aus_kit import P, photo, stat, bars, say, cta, title, ch, questions

PHOTOS = {
    "suv": ["ai:ai_boxy_suv", "h_suv_family", "ai:ai_family_suv"],
    "charge": ["ai:ai_phev_home", "h_ev_charge"],
    "money": ["ai:ai_price_compare", "h_calc"],
    "dealer": ["h_dealer", "h_keys"],
    "tow": ["ai:ai_suv_caravan", "h_caravan"],
    "interior": ["h_interior"],
    "fuel": ["h_fuel"],
    "toyota": ["m_rav4b", "m_rav4_phev"],
    "rivals": ["m_sealion6", "m_tiggo8", "m_outlander", "m_jolion", "m_h6"],
}
CLIPS = json.load(open(os.path.join(HERE, "clips.json")))
GENERIC = CLIPS.pop("_generic", [])
FALLBACK = {"suv": ["dealer"], "charge": ["suv"], "money": ["dealer"], "dealer": ["suv"], "tow": ["suv"], "interior": ["dealer"],
            "fuel": ["charge"], "toyota": ["dealer"], "rivals": ["dealer"]}
RES = ["m_h7/1", "m_h7/3", "m_h7/4", "m_rav4/1", "m_rav4_phev/1", "m_rav4_phev/3", "m_rav4b/1", "m_rav4b/2", "m_h6/1", "m_jolion/1",
       "m_jolion/3", "m_outlander/1", "m_sealion6/1", "m_tiggo8/1"]
A.setup(sys.argv[1], os.path.join(HERE, "skip.json"), PHOTOS, CLIPS, GENERIC, FALLBACK,
        ["suv", "dealer", "money", "charge", "toyota"], reserved=RES)
A.CLIP_TARGET = 0.55   # channel request (31/10): more clips
A.MAX_HOLD, A.KEEP = 13.0, 8.5
chapters = []

c = ch("ch00_hook", 0.6)
c.at(0, stat("$49,990", "drive-away · 2027 GWM Haval H7 PHEV", "GWM / CarExpert", count=False))
c.at("For a 320-kilowatt plug-in hybrid SUV", stat("320 kW", "AWD · 137 km claimed EV range (WLTC)", "GWM", count=False))
c.at("which officially launches in Australia", say("Launch: 2 November 2026", "2 NOVEMBER", 120))
c.at("the Toyota RAV4", photo("m_rav4_phev", 1, "in", cap="Toyota RAV4 PHEV|best-selling PHEV · July 2026"))
c.at("The cheapest RAV4 plug-in hybrid you can buy", A.price("Plug-in hybrid SUVs", "$58,840", "$49,990", "RAV4 XSE FWD + ORC", "H7 Lux drive-away", None, "Toyota / GWM"))
c.at("But is it really that simple", say("Is it really that simple?", "SIMPLE", 140))
questions(c, ["Price", "Power & range", "Towing & warranty", "Resale"], ["price, power", "range, towing", "warranty and resale", "what the numbers on the brochure"])
c.at("the cheapest car on the day", P("money"))
c.at("with Toyota bringing a cheaper RAV4", title("GWM vs Toyota", "the plug-in hybrid fight", "2027", "suv"))
chapters.append(c)

c = ch("ch01")
c.at(0, P("dealer"))
c.at("Its Haval Jolion small SUV", photo("m_jolion", 1, "left", cap="GWM Haval Jolion|a 2026 best-seller"))
c.at("You can see that shift in the official sales numbers", bars("Sales change · Sept 2026 vs Sept 2025", [["Geely", 870], ["Omoda Jaecoo", 344],
     ["Leapmotor", 106], ["BYD", 61], ["Toyota", -3.5, "red"]], None, "VFACTS", suffix="%"))
c.at("Toyota is still the biggest brand", P("toyota"))
c.at("First, let's meet the challenger", say("The challenger", "CHALLENGER", 150))
c.at("It's actually the second H7", photo("m_h7", 1, "in", cap="Outgoing Haval H7|replaced after ~1 year"))
c.at("GWM had delivered only 636", bars("GWM deliveries to end of July 2026", [["Old Haval H7", 636, "red"], ["Haval H6", 8759]], None, "CarExpert"))
c.at("It's also bigger than you might expect", stat("4,680 mm", "long · 4,800 with spare · 1,950 wide · 2,738 wheelbase", "CarExpert", count=False))
c.at("That boxy shape", P("suv"))
c.at("It comes in two powertrains", say("Hybrid or plug-in hybrid · AWD standard", "AWD", 110))
c.at("The hybrid uses a 1.5-litre turbo", stat("182 kW", "H7 hybrid · 670 Nm · 7.0 L/100 km claimed", "GWM", count=False))
c.at("The plug-in hybrid uses the same", stat("33.7 kWh", "PHEV battery", "GWM", count=False))
c.at("Combined output is a huge 320 kilowatts", stat("320 kW", "0–100 km/h in 4.9 s claimed", "GWM", count=False))
c.at("an electric-only range of 137", bars("H7 PHEV claimed range (WLTC)", [["Electric only", 137], ["Combined", 844]], None, "GWM", suffix=" km"))
c.at("It reported around 1,500 expressions", stat("~1,500", "expressions of interest after its debut", "GWM Australia"))
c.at("We have high expectations", say("\"We have high expectations for the all-new Haval H7.\" – Steve Maciver, GWM", "HIGH", 92))
chapters.append(c)

c = ch("ch02")
c.at(0, P("money"))
c.at("The H7 Lux hybrid: $45,990", bars("Haval H7 drive-away launch prices", [["Lux hybrid", 45990], ["Lux PHEV", 49990],
     ["Vanta hybrid", 49990], ["Vanta PHEV", 53990]], None, "CarExpert / Cars24", prefix="$"))
c.at("rising to $50,990 after", say("+$1,000 on Lux grades after 30 November", "30 NOVEMBER", 110))
c.at("The Lux gets 19-inch wheels", P("interior"))
c.at("The Vanta adds a locking rear differential", P("interior"))
c.at("A seven-seat version is due in 2027", say("7-seat H7 due in 2027", "2027", 140))
c.at("And GWM has been sharpening prices", photo("m_jolion", 3, "right", cap="Haval Jolion Premium|$23,990 drive-away"))
c.at("the Haval H6 hybrid Lux at $37,990", photo("m_h6", 1, "in", cap="Haval H6 hybrid Lux|$37,990 drive-away"))
c.at("Now, one important detail", say("Drive-away ≠ before on-roads", "≠", 130))
c.at("On-road costs – things like stamp duty", P("money"))
c.at("compare drive-away with drive-away", say("Compare drive-away with drive-away.", "DRIVE-AWAY", 120))
chapters.append(c)

c = ch("ch03")
c.at(0, say("The champion", "CHAMPION", 150))
c.at("The Toyota RAV4 is one of the best-selling", photo("m_rav4", 1, "in", cap="Toyota RAV4"))
c.at("plug-in hybrids made up thirty-nine per cent", stat("39%", "of RAV4 sales were PHEV · July 2026 (~2,170)", "CarExpert"))
c.at("ahead of the BYD Shark 6", P("toyota"))
c.at("Here's the current RAV4 plug-in hybrid range", bars("RAV4 PHEV prices (+ on-road costs)", [["XSE FWD", 58840], ["XSE AWD", 63340],
     ["GR Sport AWD", 66340]], None, "Toyota / CarExpert", prefix="$"))
c.at("It uses a 2.5-litre petrol engine", photo("m_rav4_phev", 3, "left", cap="RAV4 PHEV|201 kW FWD · 121 km EV range"))
c.at("And the regular RAV4 hybrid", photo("m_rav4b", 1, "right", cap="RAV4 GX hybrid 2WD|from $45,990 + ORC"))
c.at("So the H7 Lux hybrid's launch price", say("Same number – but drive-away and AWD.", "AWD", 110))
chapters.append(c)

c = ch("ch04")
c.at(0, title("Side by Side", "plug-in vs plug-in", "head to head", "suv"))
c.at("The H7 Lux PHEV: $49,990", bars("Price", [["H7 Lux PHEV (drive-away)", 49990], ["RAV4 XSE FWD (+ ORC)", 58840, "red"]], None,
     "GWM / Toyota", prefix="$"))
c.at("320 kilowatts, all-wheel drive", bars("Power", [["H7 PHEV", 320], ["RAV4 PHEV FWD", 201]], None, "GWM / Toyota", suffix=" kW"))
c.at("137 kilometres of claimed electric range", bars("Claimed electric range", [["H7 PHEV (WLTC)", 137], ["RAV4 PHEV", 121]], None,
     "GWM / Toyota", suffix=" km"))
c.at("the GWM is around nine thousand dollars cheaper", stat("~$9,000", "cheaper before the RAV4's on-road costs", None, count=False))
c.at("The H7's electric range figure is on the Chinese", P("charge"))
c.at("On features, the H7 Lux also comes with a lot", P("interior"))
c.at("make a list of what you actually need", P("dealer"))
c.at("And for families who mostly do short trips", P("suv"))
c.at("If you charge at home every night", P("charge"))
c.at("Let's do a quick illustration", say("Example only – not official figures", "EXAMPLE", 115))
c.at("A petrol SUV using seven litres", bars("Example: 14,600 km a year", [["Petrol · 7 L/100km @ $2", 2044, "red"],
     ["Electric · 20 kWh/100km @ 30c", 876]], None, "Illustration", prefix="$"))
c.at("Your own numbers will depend", P("fuel"))
c.at("But there are things the brochure", say("What the brochure doesn't tell you…", "BROCHURE", 115))
chapters.append(c)

c = ch("ch05")
c.at(0, cta("GWM or Toyota?", "tell me in the comments"))
c.at("hit subscribe", cta("Subscribe", "honest, fact-checked comparisons"))
chapters.append(c)

c = ch("ch06")
c.at(0, title("Towing", "check before you buy", "#1", "tow"))
c.at("CarExpert lists the new H7's braked towing", stat("1,500 kg", "H7 braked towing · hybrid and PHEV", "CarExpert", count=False))
c.at("if you're planning to tow a large caravan", P("tow"))
c.at("Second, warranty", title("Warranty", "read the fine print", "#2", "dealer"))
c.at("GWM offers a seven-year", stat("7 yrs", "GWM warranty · unlimited km · battery 8 yrs", "GWM Australia", count=False))
c.at("a battery state of health of seventy per cent", say("Battery health ≥70% isn't a warranty defect – GWM", "70%", 100))
c.at("Toyota's base warranty is five years", bars("Toyota warranty (if serviced to schedule)", [["Base", 5], ["Engine & driveline", 7],
     ["Hybrid battery", 10]], None, "CarsGuide", suffix=" yrs"))
c.at("So on paper, the warranties are closer", P("dealer"))
chapters.append(c)

c = ch("ch07")
c.at(0, say("No FBT exemption for plug-in hybrids", "PLUG-IN", 110))
c.at("Plug-in hybrids lost that exemption", stat("1 Apr 2025", "PHEVs lost the novated lease FBT exemption", "ATO", count=False))
c.at("but if you're also considering a fully electric SUV", P("charge"))
c.at("Third, and this is the big one", title("Resale Value", "the big one", "#3", "toyota"))
c.at("A 2025 analysis by Pickles and Datium", stat("88%", "value kept by a 2-year-old Toyota RAV4", "Pickles / Datium · 2025"))
c.at("We don't yet have long-term resale data", say("New H7: no resale data yet", "NO", 120))
c.at("The old H7 was replaced after just over a year", photo("m_h7", 3, "left", cap="Outgoing Haval H7|replaced after ~1 year"))
c.at("One Cars24 reader put it bluntly", say("\"…will lose value as soon as we hit 2027.\" – Cars24 reader", "LOSE VALUE", 92))
c.at("If you buy any car in November", P("dealer"))
c.at("Insurance is worth checking too", bars("Average premium rise in a year", [["EVs", 10], ["Some PHEVs (e.g. Sealion 6)", 18, "red"]], None,
     "Compare the Market · Apr 2026", prefix="+", suffix="%"))
c.at("get real quotes for both cars", P("money"))
c.at("A car that's nine thousand dollars cheaper", say("$9,000 cheaper – but $10,000 more lost?", "LOST", 105))
chapters.append(c)

c = ch("ch08")
c.at(0, P("dealer"))
c.at("Toyota has one of the largest dealer networks", P("toyota"))
c.at("As we saw in our video on BYD", say("Parts and repairers matter.", "REPAIRERS", 120))
c.at("check where your nearest service centre", P("dealer"))
c.at("And here's the twist", say("Toyota isn't standing still.", "STANDING STILL", 120))
c.at("In the first three months of 2027", A.price("Toyota RAV4 PHEV", "$58,840", "~$53,990", "XSE FWD now", "GXL 2027 (estimate)", None, "CarExpert"))
c.at("It's expected to use the same 201-kilowatt", say("RAV4 GXL PHEV · early 2027 · price TBC", "GXL", 110))
c.at("Mitsubishi Outlander plug-in hybrid", photo("m_outlander", 1, "left", cap="Mitsubishi Outlander PHEV|from $58,990 + ORC"))
c.at("Why is Toyota moving so fast", bars("NVES passenger car target", [["2026", 117], ["2027", 92, "red"]], None,
     "Federal government", suffix=" g/km"))
c.at("Toyota is already earning credits", photo("m_rav4b", 2, "in", cap="Toyota hybrids|earning NVES credits"))
c.at("So in 2027, the gap between", P("money"))
c.at("The seven-seat H7, due in 2027", stat("4,912 mm", "7-seat H7 length · 2,850 mm wheelbase", "GWM", count=False))
c.at("And GWM won't be the only one", photo("m_sealion6", 1, "right", cap="BYD Sealion 6|PHEV rival"))
c.at("from BYD, Chery, Geely", photo("m_tiggo8", 1, "in", cap="Chery Tiggo 8|PHEV rival"))
c.at("BYD was Australia's second best-selling brand", say("BYD: #2 brand · September 2026", "#2", 130))
chapters.append(c)

c = ch("ch09")
c.at(0, title("Which Should You Buy?", "how I'd decide", "verdict", "suv"))
c.at("Buy the GWM Haval H7 plug-in hybrid", say("H7: price · power · EV range", "H7", 125))
c.at("If you do lots of short trips", P("charge"))
c.at("Buy the Toyota RAV4 plug-in hybrid", say("RAV4: resale · reputation · network", "RAV4", 125))
c.at("especially in regional Australia", P("toyota"))
c.at("And think about how you'll actually use the battery", P("charge"))
c.at("a regular hybrid", P("fuel"))
c.at("diesel hit as high as $3.50", stat("$3.50/L", "diesel peak in parts of Australia · May 2026", "CarExpert", red=True, count=False))
c.at("On the test drive", P("interior"))
c.at("And how much boot space is left", P("suv"))
questions(c, ["Test drive both", "Drive-away vs drive-away", "Check towing", "Real running costs"],
          ["Test drive both", "Compare drive-away prices", "Check towing capacity", "And look at the real running costs"])
chapters.append(c)

c = ch("ch10", 2.5)
c.at(0, say("H7 Lux: +$1,000 after 30 November", "30 NOVEMBER", 115))
c.at("And Black Friday is on the 27th", P("dealer"))
c.at("write down today's drive-away price", P("money"))
c.at("So, did GWM just undercut", say("Did GWM just undercut the RAV4?", "UNDERCUT", 115))
c.at("A $49,990 drive-away plug-in hybrid", stat("$49,990", "drive-away · 320 kW · 137 km claimed", "GWM", count=False))
c.at("But Toyota still has the advantage", P("toyota"))
c.at("The real winner is you", say("The real winner: you.", "YOU", 150))
c.at("If this helped", cta("Like · Subscribe · Share", "with someone shopping for an SUV"))
c.at("Tell me in the comments: GWM or Toyota", cta("GWM or Toyota?", "comments"))
c.at("in the next video", title("Brands That May Not Survive 2027", "and what it means for owners", "next video", "dealer"))
chapters.append(c)

CTX = ["suv", "dealer", "money", "toyota", "suv", "dealer", "tow", "money", "dealer", "suv", "dealer"]
print(A.finish(chapters, "AUS12_GWM_vs_RAV4.mp4", CTX, subtitles="AUS12.ass"))
