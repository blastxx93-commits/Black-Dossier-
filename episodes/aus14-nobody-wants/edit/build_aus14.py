#!/usr/bin/env python3
"""AUS14 12 new cars nobody wants in Australia: full edit, shots anchored to phrases.
    python3 build_aus14.py <narration_dir> > episode.json   (run from the work folder)
All monthly figures: VFACTS September 2026 via CarExpert's sales atlas.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "engine"))
import aus_kit as A
from aus_kit import P, photo, stat, bars, say, cta, title, ch, questions, rank

PHOTOS = {
    "dealer": ["ai:ai_empty_yard", "h_dealer_lot", "ai:ai_salesman_waiting", "h_showroom"],
    "money": ["h_calc", "h_discount"],
    "keys": ["h_keys", "h_salesman"],
    "traffic": ["h_traffic"],
    "buyer": ["ai:ai_buyer_compare", "h_used"],
}
CLIPS = json.load(open(os.path.join(HERE, "clips.json")))
GENERIC = CLIPS.pop("_generic", [])
FALLBACK = {"dealer": ["buyer"], "money": ["keys"], "keys": ["dealer"], "traffic": ["dealer"], "buyer": ["dealer"]}
RES = ["m_ioniq9/3", "m_id4/1", "m_id4/3", "m_tcross/1", "m_omoda9/1", "m_omoda9/3", "m_koleos/1", "m_koleos/3", "m_cx70/1", "m_cx70/3",
       "m_gv80/1", "m_gv70/1", "m_gv70/3", "m_bmw_ix/1", "m_bmw_ix/3", "m_polestar3/1", "m_polestar3/3", "m_wrangler/1", "m_wrangler/3",
       "m_gladiator/1", "m_gladiator/3", "m_tonale/1", "m_stelvio/1", "m_fiat500/1", "m_fiat500/2", "m_peugeot308/1", "m_peugeot308/3",
       "m_lc70/1", "m_lc70/3", "m_fortuner/1", "m_ora/1", "m_troc/1", "m_cclass/1", "m_xc90/1", "m_cx90/1", "m_sonata/3", "m_superb/3",
       "m_civic/1", "m_ranger/1", "m_rav4/3", "m_sealion7/1", "m_tiggo4/3", "m_jolion/1", "m_ex5/1", "m_ix3/1", "m_cx60/1", "m_model_y/1",
       "m_hilux/3"]
A.setup(sys.argv[1], os.path.join(HERE, "skip.json"), PHOTOS, CLIPS, GENERIC, FALLBACK,
        ["dealer", "traffic", "buyer", "money", "keys"], reserved=RES)
A.CLIP_TARGET = 0.55
A.MAX_HOLD, A.KEEP = 13.0, 8.5
chapters = []
SRC = "VFACTS Sept 2026 via CarExpert"

c = ch("ch00_hook", 0.6)
c.at(0, stat("1", "Hyundai Ioniq 9 sold in Australia · September 2026", SRC, red=True, count=False))
c.at("A big, seven-seat electric family SUV", say("A 7-seat electric SUV. One buyer. One month.", "ONE", 105))
c.at("seventy-nine different makes and models recorded zero sales", stat("79", "models with ZERO sales in September", SRC, red=True))
c.at("Plenty more limped along", P("dealer"))
c.at("they're slashing prices", P("money"))
c.at("So in this video, I'm counting down twelve", title("12 New Cars Nobody Wants", "real sales · real price cuts", "Australia 2026", "dealer"))
c.at("I'll also show you a few cars that look like disasters", say("Some 'disasters' aren't what they seem.", "AREN'T", 110))
c.at("how to use all of this to get a better deal", P("keys"))
chapters.append(c)

c = ch("ch01")
c.at(0, P("traffic"))
c.at("Australians bought 108,778 new vehicles", stat("108,778", "new vehicles sold · September 2026 (+1.8%)", "VFACTS"))
c.at("It's a market where buyers are moving", P("buyer"))
c.at("Electric cars outsold petrol cars", bars("September 2026 sales", [["Electric", 26287], ["Petrol", 26018], ["Diesel", 25173]], None, "VFACTS / CarExpert"))
c.at("Geely's sales jumped 870 per cent", stat("+870%", "Geely sales · Sept 2026 vs Sept 2025", "VFACTS"))
c.at("The Ford Ranger was the country's best seller", photo("m_ranger", 1, "in", cap="Ford Ranger|#1 · 5,062 sales"))
c.at("the BYD Sealion 7 with 2,687", bars("Chinese models in the top 10 · Sept 2026", [["BYD Sealion 7", 2687], ["Chery Tiggo 4", 2059],
     ["GWM Haval Jolion", 2018], ["Geely EX5", 2008]], None, "VFACTS"))
c.at("Geely EX5 with 2,008", photo("m_ex5", 1, "left", cap="Geely EX5|+620%"))
c.at("Now look at who's going backwards", bars("Brands going backwards · Sept 2026", [["Subaru", -42.6, "red"], ["Mitsubishi", -41.5, "red"],
     ["Volkswagen", -36.9, "red"], ["Nissan", -30.0, "red"], ["Hyundai", -22.0, "red"]], None, "VFACTS", suffix="%"))
c.at("When money moves this quickly", P("dealer"))
c.at("often paid for with borrowed money", P("money"))
c.at("A couple of ground rules", say("Only cars still on sale. Axed models: later.", "STILL ON SALE", 100))
chapters.append(c)

c = ch("ch02")
c.at(0, rank(12, "Volkswagen ID.4", "m_id4", 1, "47 sales · -73%", "Sept 2026"))
c.at("Its little brother, the T-Cross", photo("m_tcross", 1, "right", cap="Volkswagen T-Cross|29 sales · -81%"))
c.at("And Volkswagen knows it has a problem", say("\"Whenever you start selling less than 10,000 vehicles a year… you're niche.\" – VW Australia", "NICHE", 85))
c.at("Volkswagen sold roughly 29,000", stat("~29,000", "VW sales in Australia · 2025 (down 20%+)", "carsales"))
c.at("Volkswagen's product boss", photo("m_id4", 3, "in"))
c.at("By then, cheaper electric SUVs from China", P("buyer"))
c.at("Volkswagen has been cutting prices", P("money"))
c.at("Number eleven: the Omoda 9", rank(11, "Omoda 9", "m_omoda9", 1, "35 sales · -61.5%", "$61,990 + ORC"))
c.at("This is the one that proves", photo("m_omoda9", 3, "left", cap="Omoda 9|nearly 400 kW PHEV"))
c.at("would I rather have a Toyota", P("dealer"))
c.at("Being Chinese is no longer enough", say("Being Chinese isn't enough. The price has to make sense.", "PRICE", 95))
chapters.append(c)

c = ch("ch03")
c.at(0, rank(10, "Renault Koleos", "m_koleos", 1, "18 sales · -70.5%", "from $36,990 drive-away"))
c.at("Toyota sold more than 4,600 RAV4s", bars("Mid-size SUVs · Sept 2026", [["Toyota RAV4", 4624], ["Renault Koleos", 18, "red"]], None, SRC))
c.at("And it's not because it's expensive", photo("m_koleos", 3, "in", cap="Renault Koleos|from $36,990 drive-away"))
c.at("That's the first big lesson", say("Lesson 1: a low price can't save a car that feels old.", "FEELS OLD", 95))
c.at("Buyers in 2026 are walking into showrooms", P("buyer"))
c.at("Number nine: the Mazda CX-70", rank(9, "Mazda CX-70", "m_cx70", 1, "16 sales · 182 this year", "price cut up to $8,051"))
c.at("To put that in perspective", bars("Mazda large SUVs · 2026 to Sept", [["CX-60", 3566], ["CX-80", 1931], ["CX-90", 470], ["CX-70", 182, "red"]], None, "CarsGuide"))
c.at("In July 2026, Mazda slashed CX-70 prices", stat("-$8,051", "biggest Mazda CX-70 price cut · July 2026", "CarExpert", red=True, count=False))
c.at("Mazda confirmed the CX-70 is ending production", photo("m_cx70", 3, "left", cap="Mazda CX-70|production ending for the US"))
c.at("still has a small but loyal fanbase", say("\"…a small but loyal fanbase.\" – Mazda Australia", "LOYAL", 110))
chapters.append(c)

c = ch("ch04")
c.at(0, rank(8, "Genesis", "m_gv80", 1, "66 sales · whole brand", "-54.5%"))
c.at("The GV80 wagon moved two", photo("m_gv70", 1, "in", cap="Genesis GV70|46 sales"))
c.at("The discounts tell the story", bars("Genesis EOFY offers · July 2026", [["GV70", 7000], ["GV80", 10000]], None, "CarExpert", prefix="up to $"))
c.at("Luxury buyers are notoriously loyal", P("dealer"))
c.at("Number seven: the BMW iX", rank(7, "BMW iX", "m_bmw_ix", 1, "7 sales · -88%", "Sept 2026"))
c.at("Its new iX3 arrived this year", photo("m_ix3", 1, "right", cap="BMW iX3|new, sharper price"))
c.at("in April BMW cut up to $8,900", stat("-$8,900", "BMW iX1 / iX2 price cuts · April 2026", "CarExpert", red=True, count=False))
c.at("That's the second big lesson", say("Lesson 2: the worst enemy can be the next model in the same showroom.", "SAME SHOWROOM", 85))
chapters.append(c)

c = ch("ch05")
c.at(0, P("dealer"))
c.at("Tell me in the comments", cta("Looked at one of these?", "tell me in the comments"))
c.at("hit subscribe", cta("Subscribe", "numbers-first car videos"))
chapters.append(c)

c = ch("ch06")
c.at(0, rank(6, "Polestar 3", "m_polestar3", 3, "6 sales · -88.5%", "from $116,700 + ORC"))
c.at("Even Polestar's global boss admits", say("\"…maybe also a bit too expensive.\" – Polestar CEO Michael Lohscheller", "TOO EXPENSIVE", 85))
c.at("He also admitted the company is still", photo("m_polestar3", 1, "in"))
c.at("Number five: the Jeep Wrangler and Gladiator", rank(5, "Jeep Wrangler & Gladiator", "m_wrangler", 1, "9 + 5 sales", "Sept 2026"))
c.at("The whole Jeep brand sold sixteen", photo("m_gladiator", 1, "left", cap="Jeep Gladiator|5 sales · -80%"))
c.at("Price is a big part of it", A.price("Jeep Wrangler 4-door", "~$37,000", "$75,950", "2014", "2025 (+ ORC)", None, "CarSauce"))
c.at("At that price, buyers are comparing it", photo("m_wrangler", 3, "right"))
c.at("Jeep says it's committed to Australia", P("dealer"))
chapters.append(c)

c = ch("ch07")
c.at(0, rank(4, "Alfa Romeo Tonale & Stelvio", "m_tonale", 1, "2 + 2 sales", "Sept 2026"))
c.at("The bigger Stelvio also registered two", photo("m_stelvio", 1, "in", cap="Alfa Romeo Stelvio|2 sales"))
c.at("The updated Tonale starts at $64,990", stat("$64,990", "Alfa Romeo Tonale · before on-road costs", "Cars24", count=False))
c.at("Think about that for a moment", bars("Small SUVs · Sept 2026", [["Chery Tiggo 4", 2059], ["Alfa Romeo Tonale", 2, "red"]], None, SRC))
c.at("Brand heritage counts for a lot less", photo("m_tiggo4", 3, "left", cap="Chery Tiggo 4|2,059 sales"))
c.at("Number three: the Fiat 500", rank(3, "Fiat 500 / Abarth", "m_fiat500", 1, "2 sales · -94.7%", "Sept 2026"))
c.at("Fiat already tried the price-cut route", A.price("Fiat 500e La Prima", "$52,500", "$38,990", "before on-roads", "drive-away · 2025", None, "CarsGuide"))
c.at("stimulate sales and clear out existing stock", say("\"…clear out existing stock.\" – Fiat", "CLEAR OUT", 120))
c.at("you know things are tough", photo("m_fiat500", 2, "in"))
chapters.append(c)

c = ch("ch08")
c.at(0, rank(2, "Peugeot 308", "m_peugeot308", 1, "2 sales · 17 all year", "Sept 2026"))
c.at("Seventeen cars in nine months", stat("17", "Peugeot 308s sold in 2026 · Jan–Sept", SRC, red=True))
c.at("And the 308's problem goes beyond the car", say("July 2026: importer Inchcape to end Peugeot partnership", "INCHCAPE", 100))
c.at("nervous buyers don't sign contracts", photo("m_peugeot308", 3, "right"))
c.at("And number one: the Hyundai Ioniq 9", rank(1, "Hyundai Ioniq 9", "m_ioniq9", 3, "1 sale in September", "65 this year · 40 in 2025"))
c.at("Sixty-five for the whole of 2026", bars("Hyundai Ioniq 9 sales in Australia", [["2025", 40], ["2026 to Sept", 65], ["Sept 2026", 1, "red"]], None, SRC))
c.at("Price is part of it", stat("~$128,000", "Ioniq 9 Calligraphy · drive-away Sydney", "CarExpert", count=False))
c.at("Competition is part of it too", P("buyer"))
c.at("We do a terrible job with our EVs", say("\"We do a terrible job with our EVs.\" – Hyundai Australia CEO Don Romano", "TERRIBLE", 88))
c.at("More than a year later", P("dealer"))
chapters.append(c)

c = ch("ch09")
c.at(0, title("Quick-Fire", "just missed the list", "honourable mentions", "traffic"))
c.at("The Mercedes-Benz C-Class", photo("m_cclass", 1, "in", cap="Mercedes-Benz C-Class|39 sales · -58%"))
c.at("The Volvo XC90 seven-seater", photo("m_xc90", 1, "left", cap="Volvo XC90|33 sales · -62%"))
c.at("The Mazda CX-90", photo("m_cx90", 1, "right", cap="Mazda CX-90|36 sales · -33%"))
c.at("The Hyundai Sonata", photo("m_sonata", 3, "in", cap="Hyundai Sonata|16 sales"))
c.at("The Skoda Superb", photo("m_superb", 3, "left", cap="Skoda Superb|10 sales · -55%"))
c.at("And the Honda Civic", photo("m_civic", 1, "right", cap="Honda Civic|55 sales · -38%"))
c.at("Notice something?", P("traffic"))
c.at("Now, before you assume", title("Not What It Seems", "big drops with a reason", "read the data", "dealer"))
c.at("The Toyota LandCruiser 70 Series", photo("m_lc70", 1, "in", cap="LandCruiser 70|-96% · orders paused, not unloved"))
c.at("Buyers want them", photo("m_lc70", 3, "left"))
c.at("The Toyota Fortuner", photo("m_fortuner", 1, "right", cap="Toyota Fortuner|-94% · axed, no replacement"))
c.at("The GWM Ora electric hatch", photo("m_ora", 1, "in", cap="GWM Ora|-99% · replaced by Ora 5"))
c.at("And the Volkswagen T-Roc", photo("m_troc", 1, "left", cap="Volkswagen T-Roc|-84% · new generation due 2027"))
c.at("The lesson?", say("Unloved – or just being replaced? Find out.", "FIND OUT", 115))
chapters.append(c)

c = ch("ch10", 2.5)
c.at(0, title("What It Means for You", "deals – and traps", "buyers", "money"))
c.at("We've seen Mazda cut up to $8,051", bars("Price cuts we've seen", [["Genesis GV80", 10000], ["BMW iX1", 8900], ["Mazda CX-70", 8051]], None,
     "CarExpert", prefix="up to $"))
c.at("ask for a drive-away price in writing", P("keys"))
c.at("Old stock is often where the dealer", P("dealer"))
c.at("It's also worth asking about demonstrators", say("Ask about demonstrators.", "DEMONSTRATORS", 130))
c.at("And always compare", P("buyer"))
c.at("But be careful", say("Hard to sell new = hard to sell used.", "USED", 120))
c.at("Check the warranty, the service plan", P("money"))
c.at("And if you already own one of these cars", P("keys"))
questions(c, ["#12 VW ID.4", "#1 Hyundai Ioniq 9", "1 sale in a month"], ["from the Volkswagen ID.4", "all the way to the Hyundai", "with one single sale"])
c.at("If this helped", cta("Like · Subscribe · Share", "with someone buying a new car"))
c.at("which of these surprised you the most", cta("Which one surprised you?", "comments"))
c.at("in the next video", title("The Ute Price War", "Toyota & Ford are cutting", "next video", "traffic"))
chapters.append(c)

CTX = ["dealer", "traffic", "dealer", "buyer", "dealer", "dealer", "dealer", "money", "dealer", "traffic", "money"]
print(A.finish(chapters, "AUS14_Nobody_Wants.mp4", CTX, subtitles="AUS14.ass"))
