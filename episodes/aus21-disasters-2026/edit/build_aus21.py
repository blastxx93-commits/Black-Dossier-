#!/usr/bin/env python3
"""AUS21 The 10 biggest car disasters of 2026 in Australia: full edit, shots anchored to phrases.
    python3 build_aus21.py <narration_dir> > episode.json   (run from the work folder)
Opens on car photos with the impact number as caption. Template 'ember'. Real photos only, every file reviewed.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "engine"))
import aus_kit as A
from aus_kit import P, photo, stat, bars, say, cta, title, ch, rank

PHOTOS = {
    "dealer": ["h_dealer", "h_lot", "h_keys"],
    "street": ["h_traffic", "h_outback"],
    "money": ["h_money"], "ev": ["h_ev"], "port": ["h_port"],
    "cars": ["m_camry", "m_hilux", "m_prado", "m_everest", "m_sealion7", "m_ranger", "m_gv70", "m_modely"],
    "ute": ["m_hilux", "m_ranger", "m_shark6"], "gloom": ["h_lot", "h_port"],
}
CLIPS = json.load(open(os.path.join(HERE, "clips.json")))
GENERIC = CLIPS.pop("_generic", [])
FALLBACK = {k: ["street", "dealer", "cars"] for k in PHOTOS}
FALLBACK.update({"street": ["dealer", "cars"], "dealer": ["street", "cars"], "cars": ["street", "dealer"]})
RES = ["m_tasman/1", "m_tasman/3", "m_cybertruck/1", "m_cybertruck/3", "m_palisade/1", "m_palisade/3", "m_wrangler/1", "m_wrangler/2",
       "m_wrangler/3", "m_grandcherokee/1", "m_gladiator/1", "m_avenger/1", "m_navara/3", "m_qashqai/1", "m_pathfinder/1", "m_p208/1",
       "m_p308/1", "m_partner/3", "m_p3008/1", "m_qashqai/3", "m_grecale/1", "m_grecale/3", "m_levante/1", "m_ghibli/4", "m_gv70/1", "m_accord/3",
       "m_accord/1", "m_camry/3", "m_mache2/1", "m_mache2/3", "m_modely/1", "m_cx70/1", "m_cx70/3", "m_defender/1", "m_ev9/2", "m_q4/1",
       "m_polestar4/1", "m_fortuner/1", "m_jaguar/1", "m_lotus/1", "m_mclaren/1", "m_ranger/1", "m_hilux/3", "m_shark6/1", "m_everest/3",
       "m_prado/1"]
A.setup(sys.argv[1], os.path.join(HERE, "skip.json"), PHOTOS, CLIPS, GENERIC, FALLBACK, ["dealer", "street", "cars"], reserved=RES)
A.CLIP_TARGET = 0.7
A.MAX_HOLD, A.KEEP = 15.0, 9.5
chapters = []
SRC = "VFACTS via CarExpert"
GA = "GoAuto / VFACTS"

c = ch("ch00_hook", 0.6)
c.at(0, photo("m_tasman", 1, "in", cap="20,000|Kia's first-year target"))
c.at("Fifteen months later", P("ute", cap="7,898|sold in 15 months"))
c.at("Clearly we are not satisfied yet", say("\"Clearly we are not satisfied yet.\" – Kia", "NOT SATISFIED", 120))
c.at("A Tesla that Australians waited", photo("m_cybertruck", 1, "left", cap="Tesla Cybertruck|cancelled after 7 years"))
c.at("A big family SUV pulled from sale", photo("m_palisade", 1, "right", cap="Hyundai Palisade|stop-sale"))
c.at("A famous French brand", photo("m_p3008", 1, "in", cap="Peugeot|dumped by its importer"))
c.at("An American icon", photo("m_wrangler", 1, "left", cap="Jeep|-66%"))
c.at("And a Japanese giant", photo("m_qashqai", 3, "in", cap="Nissan|\"the low point\""))
c.at("Here's what makes it even crazier", P("street"))
c.at("So in this video, I'm counting down", title("2026's 10 Biggest Car Disasters", "from bad to unbelievable", "Australia 2026", "dealer"))
c.at("And stay until number one", P("dealer"))
chapters.append(c)

c = ch("ch01")
c.at(0, P("street"))
c.at("Australians bought 107,493", stat("107,493", "new vehicles · October 2026 · record October", SRC))
c.at("Cars built in China were up 104", stat("+104%", "China-built cars · October 2026", SRC))
c.at("At the same time, cars from Japan", bars("October 2026 · by origin / brand", [["Japan", -13.1], ["Korea", -23.5], ["Germany", -24.0],
     ["Mitsubishi", -50.0], ["Volkswagen", -46.4]], None, SRC, suffix="%"))
c.at("In a market moving this fast", P("dealer"))
c.at("A quick word on how I chose this list", P("cars"))
chapters.append(c)

c = ch("ch02")
c.at(0, rank(10, "Mazda CX-70", "m_cx70", 1, "182 sold · -35%", "Jan–Sept 2026"))
c.at("It didn't work", bars("Large SUVs over $80k · Jan–Sept", [["LR Defender", 3098], ["Mazda CX-70", 182, "red"]], None, GA))
c.at("the Land Rover Defender sold more than three thousand", photo("m_defender", 1, "in", cap="Land Rover Defender|17 for every CX-70"))
c.at("And this is after a big price cut", stat("$8,051", "max CX-70 price cut · July 2026", "Mazda", count=False))
c.at("Then in late October", photo("m_cx70", 3, "left", cap="CX-70|US production ending"))
c.at("Mazda as a whole was down", P("dealer"))
chapters.append(c)

c = ch("ch03")
c.at(0, rank(9, "Ford Mustang Mach-E", "m_mache2", 1, "206 sold · -34%", "Jan–Sept 2026"))
c.at("Instead, the Mach-E sold 206", P("ev"))
c.at("Ford tried to fix it with price cuts", A.price("Mach-E GT", "$98,490", "$89,000", "previous price", "drive-away offer", None, "EV Central"))
c.at("desperate to shift", say("Ford \"desperate to shift\" stock – EV Central", "DESPERATE", 110))
c.at("In October alone, the Tesla Model Y", bars("Electric SUVs", [["Model Y · October", 3105], ["Mach-E · 9 months", 206, "red"]], None, SRC))
c.at("In the United States", photo("m_mache2", 3, "in", cap="USA|50,000+ sold in 2025"))
c.at("In Australia, against a wall", P("street"))
chapters.append(c)

c = ch("ch04")
c.at(0, rank(8, "Honda Accord", "m_accord", 3, "59 sold", "Jan–Sept 2026"))
c.at("At around $64,900 drive-away", photo("m_accord", 1, "left", cap="Accord e:HEV RS|$64,900 drive-away"))
c.at("In the same period, Toyota sold 9,471", bars("Mid-size cars · Jan–Sept", [["Toyota Camry", 9471], ["Honda Accord", 59, "red"]], None, GA))
c.at("Honda moved to a fixed-price", P("dealer"))
c.at("Now Honda is trying to clear", stat("$1,000", "gift card on the Accord · plate clearance", "CarExpert", count=False))
c.at("To be fair, GoAuto pointed out", say("\"…unrelated to product quality…\" – GoAuto", "PRODUCT QUALITY", 105))
chapters.append(c)

c = ch("ch05")
c.at(0, rank(7, "Maserati", "m_grecale", 1, "101 sold · -33%", "first half 2026"))
c.at("According to CarExpert's analysis", bars("Luxury SUVs · H1 2026", [["Genesis GV70", 570], ["Maserati Grecale", 98, "red"]], None, "CarExpert"))
c.at("the Genesis GV70 luxury SUV alone", photo("m_gv70", 1, "in", cap="Genesis GV70|570 sold"))
c.at("And the range is shrinking", photo("m_levante", 1, "left", cap="Maserati Levante|discontinued"))
c.at("In October, the Ghibli and the Levante", photo("m_ghibli", 4, "right", cap="Ghibli|0 sales in October"))
c.at("When a luxury brand stops selling", P("dealer"))
c.at("That's how a brand slowly disappears", photo("m_grecale", 3, "in"))
chapters.append(c)

c = ch("ch06")
c.at(0, rank(6, "Peugeot", "m_p308", 1, "dumped by importer", "July 2026"))
c.at("The sales numbers explain why", bars("Peugeot sales in Australia", [["2007 (peak)", 8807], ["2025", 1350], ["2026 (to May)", 373, "red"]], None, "CarExpert"))
c.at("the Peugeot 208 small car recorded just one", photo("m_p208", 1, "in", cap="Peugeot 208|1 delivery in H1 2026"))
c.at("And in October, the Peugeot 308", stat("3", "Peugeot 308 sales · October 2026", SRC, red=True))
c.at("Stellantis, Peugeot's parent company", say("\"We intend to maintain continuity of distribution in Australia.\" – Stellantis", "CONTINUITY", 92))
c.at("But this is the second French brand", photo("m_partner", 3, "left", cap="Peugeot Partner|best seller"))
c.at("If you own a Peugeot", P("dealer"))
chapters.append(c)

c = ch("ch07")
c.at(0, rank(5, "Nissan", "m_navara", 3, "-34% · Jan–July", "Navara -49%"))
c.at("From January to July, Nissan delivered", bars("Nissan · Jan–July 2026", [["Navara", -48.8], ["Qashqai", -73.5], ["X-Trail", -15.1]], None,
     "CarExpert", suffix="%"))
c.at("The Qashqai was down 73", photo("m_qashqai", 1, "in", cap="Nissan Qashqai|-73.5%"))
c.at("Then came the cuts", photo("m_pathfinder", 1, "left", cap="Pathfinder|axed"))
c.at("2026 is the low point", say("\"2026 is the low point…\" – Steve Milette, Nissan Oceania", "LOW POINT", 105))
c.at("To be fair to Nissan", P("cars"))
chapters.append(c)

c = ch("ch08")
c.at(0, rank(4, "Jeep", "m_wrangler", 2, "-66% · first half", "365 sold in 6 months"))
c.at("In September 2026, the whole of Jeep", stat("16", "Jeep sales in Australia · September 2026 · all models", SRC, red=True))
c.at("The Compass was down 84", bars("Jeep · H1 2026", [["Compass", -84.3], ["Grand Cherokee", -96.6], ["Gladiator", -56.3]], None, "CarExpert", suffix="%"))
c.at("The Grand Cherokee was down almost 97", photo("m_grandcherokee", 1, "in", cap="Grand Cherokee|-97%"))
c.at("The Gladiator ute", photo("m_gladiator", 1, "left", cap="Jeep Gladiator|-56%"))
c.at("And the little Avenger", photo("m_avenger", 1, "right", cap="Jeep Avenger|\"a flop\""))
c.at("The problem is price", A.price("Jeep Wrangler 4-door", "~$37,000", "$75,950", "2014", "2026 (+ ORC)", None, "CarSauce"))
c.at("Jeep is now offering four thousand", photo("m_wrangler", 3, "in", cap="Wrangler Rubicon|$4,000 deposit"))
chapters.append(c)

c = ch("ch09")
c.at(0, rank(3, "Tesla Cybertruck", "m_cybertruck", 3, "cancelled", "after almost 7 years"))
c.at("In November 2019, Tesla started taking", stat("$150", "Cybertruck deposits · from November 2019", "CarExpert", count=False))
c.at("The reservation portal closed in May 2022", P("gloom"))
c.at("After careful consideration", say("\"…plans to produce Cybertruck for Australia and New Zealand have been discontinued.\" – Tesla", "DISCONTINUED", 88))
c.at("The Cybertruck is built only in left-hand drive", P("street"))
c.at("Tesla is refunding deposits", photo("m_modely", 1, "in", cap="Model 3 / Model Y|free year of FSD"))
c.at("seven years of waiting", P("dealer"))
chapters.append(c)

c = ch("ch10")
c.at(0, rank(2, "Hyundai Palisade", "m_palisade", 3, "stop-sale & recall", "March–April 2026"))
c.at("On the 7th of March", P("gloom"))
c.at("may not adequately detect", say("\"…may not adequately detect contact with an occupant or object…\" – Hyundai", "DETECT", 88))
c.at("Hyundai halted sales and deliveries", stat("2,242", "Palisades recalled in Australia · 2 April 2026", "Cars24 / recall notice"))
c.at("The fix is free", P("dealer"))
c.at("This is a tragedy first", P("dealer", cap="Palisade owners|check your recall status"))
chapters.append(c)

c = ch("ch11")
c.at(0, rank(1, "Kia Tasman", "m_tasman", 3, "7,898 in 15 months", "target: 20,000 in year one"))
c.at("The Tasman arrived in July 2025", bars("Kia Tasman", [["First-year target", 20000], ["Sold in 15 months", 7898, "red"]], None, GA))
c.at("We're not making or looking for excuses", say("\"We're not making or looking for excuses.\" – Damien Meredith, Kia Australia", "EXCUSES", 92))
c.at("Clearly we are not satisfied yet", say("\"Clearly we are not satisfied yet.\" – Spencer Cho, Kia", "NOT SATISFIED", 105))
c.at("The discounts have been huge", A.price("Kia Tasman SX+ 4WD", "$62,390", "$54,990", "+ on-road costs", "drive-away · Nov 2026", None, "ACM"))
c.at("And in Korea, local media reported", P("ute"))
c.at("Why didn't it work", photo("m_ranger", 1, "in", cap="Ford Ranger|the benchmark"))
c.at("Whatever the reason", photo("m_shark6", 1, "left", cap="BYD Shark 6|PHEV rival"))
chapters.append(c)

c = ch("ch12")
c.at(0, title("Dishonourable Mentions", "just missed the top 10", "bonus", "street"))
c.at("The Kia EV9", photo("m_ev9", 2, "in", cap="Kia EV9|120 sold · -50%"))
c.at("The Audi Q4 e-tron", photo("m_q4", 1, "left", cap="Audi Q4 e-tron|2 sales in October"))
c.at("Polestar.", photo("m_polestar4", 1, "right", cap="Polestar|-10% YTD in an EV boom"))
c.at("The Toyota Fortuner", photo("m_fortuner", 1, "in", cap="Toyota Fortuner|8 sales · axed"))
c.at("Mitsubishi. Sales down 50", stat("-50%", "Mitsubishi · October 2026", SRC, red=True))
c.at("And three brands that recorded exactly zero", photo("m_jaguar", 1, "left", cap="Jaguar|0 sales in October"))
c.at("To be fair, Jaguar has stopped", photo("m_lotus", 1, "in", cap="Lotus|0 sales"))
c.at("But a month with zero sales", photo("m_mclaren", 1, "right", cap="McLaren|0 sales"))
chapters.append(c)

c = ch("ch13", 2.5)
c.at(0, title("What the Disasters Have in Common", "and what it means for you", "verdict", "dealer"))
c.at("Most of them made the same mistake", P("street"))
c.at("First, if you're buying, disasters mean deals", P("money"))
c.at("Second, think about resale", P("cars"))
c.at("Third, if you already own one", P("dealer"))
c.at("So that's the list", P("street"))
c.at("Which of these do you think is the biggest disaster", cta("Biggest disaster of 2026?", "tell me in the comments"))
c.at("hit like and subscribe", cta("Like · Subscribe", "numbers-first car videos"))
c.at("in the next video", title("10 Cars Australia Went CRAZY For", "next video", "coming up", "street"))
chapters.append(c)

CTX = ["dealer", "street", "cars", "ev", "dealer", "cars", "dealer", "cars", "street", "street", "dealer", "ute", "street", "dealer"]
print(A.finish(chapters, "AUS21_Disasters_2026.mp4", CTX, subtitles="AUS21.ass", theme="ember"))
