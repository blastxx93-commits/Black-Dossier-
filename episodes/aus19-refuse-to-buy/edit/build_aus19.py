#!/usr/bin/env python3
"""AUS19 10 new cars Australians refuse to buy (2026): full edit, shots anchored to phrases.
    python3 build_aus19.py <narration_dir> > episode.json   (run from the work folder)
Opens on car photos with the impact number as caption (rule 01/11/2026). New 'electric' template (rule 14/11/2026).
No AI images (Replicate out of credit): real scene photos only, every file reviewed.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "engine"))
import aus_kit as A
from aus_kit import P, photo, stat, bars, say, cta, title, ch, questions, rank

PHOTOS = {
    "dealer": ["h_dealer", "h_lot", "h_keys"],
    "street": ["h_traffic", "h_outback"],
    "port": ["h_port"],
    "money": ["h_money"],
    "ev": ["h_ev"],
    "cars": ["m_camry", "m_hilux", "m_prado", "m_geelyex5", "m_everest", "m_rav4"],
}
CLIPS = json.load(open(os.path.join(HERE, "clips.json")))
GENERIC = CLIPS.pop("_generic", [])
FALLBACK = {"dealer": ["street", "cars"], "street": ["dealer", "cars"], "port": ["street"], "money": ["dealer"], "ev": ["street"], "cars": ["street"]}
RES = ["m_accord/3", "m_camry/3", "m_ev9/1", "m_ev9/2", "m_mache/1", "m_mache/3", "m_karoq/1", "m_karoq/3", "m_wrangler/1", "m_wrangler/3",
       "m_rexton/1", "m_octavia/1", "m_octavia/3", "m_cx70/1", "m_cx70/3", "m_sonata/1", "m_sonata/3", "m_fabia/1", "m_fabia/3", "m_mg3/1",
       "m_q4/1", "m_ix/1", "m_kangoo/1", "m_scross/1", "m_tonale/1", "m_fortuner/1", "m_defender/1", "m_lc300/3", "m_sealion7/1",
       "m_compass/1", "m_superb/3", "m_everest/3", "m_rav4/3", "m_ev9/3", "m_wrangler/2"]
A.setup(sys.argv[1], os.path.join(HERE, "skip.json"), PHOTOS, CLIPS, GENERIC, FALLBACK, ["dealer", "street", "cars"], reserved=RES)
A.CLIP_TARGET = 0.55
A.MAX_HOLD, A.KEEP = 15.0, 9.5
chapters = []
GA = "GoAuto / VFACTS"
SRC = "VFACTS via CarExpert"

c = ch("ch00_hook", 0.6)
c.at(0, photo("m_accord", 3, "in", cap="59|Honda Accords sold · Jan–Sept 2026"))
c.at("In the same nine months, Toyota sold", photo("m_camry", 3, "left", cap="Toyota Camry|9,471 sold"))
c.at("over one hundred and sixty Camrys", say("160 Camrys for every Accord", "160", 130))
c.at("A seven-seat Kia", photo("m_ev9", 1, "right", cap="Kia EV9|from $97,000"))
c.at("A Ford with a famous badge", photo("m_mache", 1, "in", cap="Mustang Mach-E|cut up to ~$9,500"))
c.at("A Skoda that the RAV4 outsells", photo("m_karoq", 1, "left", cap="Skoda Karoq|135 RAV4s for every one"))
c.at("And one brand that has", P("dealer"))
c.at("October 2026 was the biggest October", P("street"))
c.at("So in this video, I'm counting down", title("10 Cars Australians Refuse to Buy", "real sales · real prices", "Australia 2026", "cars"))
c.at("Stay to the end", P("dealer"))
chapters.append(c)

c = ch("ch01")
c.at(0, P("street"))
c.at("Australians bought 107,493", stat("107,493", "new vehicles · October 2026 · record October", SRC))
c.at("Electric car sales were up 237", stat("+237%", "EV sales · Oct 2026 vs Oct 2025", SRC))
c.at("BYD sold more than ten thousand", photo("m_sealion7", 1, "in", cap="BYD|10,025 sales in October"))
c.at("Now look at who's going backwards", bars("October 2026 · brands", [["Mitsubishi", -50.0], ["Volkswagen", -46.4], ["Audi", -44.8],
     ["Subaru", -41.5], ["Hyundai", -28.6], ["Mazda", -19.7]], None, SRC, suffix="%"))
c.at("So this isn't a weak market", P("dealer"))
c.at("A quick word on how I built this list", P("cars"))
c.at("Let's start the countdown", P("street"))
chapters.append(c)

c = ch("ch02")
c.at(0, rank(10, "KGM Rexton", "m_rexton", 1, "371 sold · -67%", "Jan–Sept 2026"))
c.at("On paper, that's great value", P("cars"))
c.at("In the first nine months of 2026, the Rexton found", bars("KGM Rexton · Jan–Sept", [["2025", 1125], ["2026", 371, "red"]], None, GA))
c.at("GoAuto put it brutally", say("\"…the dubious honour…\" – GoAuto", "DUBIOUS HONOUR", 110))
c.at("the Ford Everest sold more than sixteen thousand", photo("m_everest", 3, "in", cap="Ford Everest|44 for every Rexton"))
c.at("Part of the problem is the price climb", P("money"))
c.at("Chinese brands have flooded", P("dealer"))
chapters.append(c)

c = ch("ch03")
c.at(0, rank(9, "Skoda Octavia", "m_octavia", 1, "340 sold · -39%", "Jan–Sept 2026"))
c.at("The Octavia is a car that motoring journalists", photo("m_octavia", 3, "left"))
c.at("The Octavia sold 340 cars", bars("Skoda Octavia · Jan–Sept", [["2025", 557], ["2026", 340, "red"]], None, GA))
c.at("In the same segment, the Toyota Camry sold", photo("m_camry", 1, "in", cap="Toyota Camry|28 for every Octavia"))
c.at("The problem isn't that the Octavia", P("street"))
c.at("Buyers who want something new", P("dealer"))
chapters.append(c)

c = ch("ch04")
c.at(0, rank(8, "Jeep Wrangler", "m_wrangler", 1, "247 sold · -28%", "Jan–Sept 2026"))
c.at("Price is the big issue", A.price("Jeep Wrangler 4-door", "~$37,000", "$75,950", "2014", "2026 (+ ORC)", None, "CarSauce"))
c.at("GoAuto worked out that the Ford Everest", stat("65 : 1", "Ford Everest vs Jeep Wrangler · 2026", GA, count=False))
c.at("And look at the rest of the Jeep showroom", photo("m_compass", 1, "left", cap="Jeep Compass|1 sale in October"))
c.at("Right now, Jeep is offering", photo("m_wrangler", 3, "in", cap="Wrangler Rubicon|$4,000 deposit contribution"))
c.at("When a brand starts paying", P("dealer"))
chapters.append(c)

c = ch("ch05")
c.at(0, rank(7, "Skoda Karoq", "m_karoq", 3, "232 sold · -32%", "Jan–Sept 2026"))
c.at("from $40,990 drive-away", P("cars"))
c.at("The Karoq sold 752 cars in 2024", bars("Skoda Karoq sales", [["2024", 752], ["2025", 470], ["2026 (9 mo.)", 232, "red"]], None, "CarExpert"))
c.at("Toyota RAV4", photo("m_rav4", 3, "in", cap="Toyota RAV4|135 for every Karoq"))
c.at("The reviewer's verdict was revealing", say("\"…feels like a rental…\" – CarExpert", "RENTAL", 120))
c.at("That's exactly the kind of car", P("dealer"))
chapters.append(c)

c = ch("ch06")
c.at(0, rank(6, "Ford Mustang Mach-E", "m_mache", 3, "206 sold · -34%", "Jan–Sept 2026"))
c.at("It's an electric SUV, in a year", P("ev"))
c.at("The Mach-E sold 206 cars", bars("Mach-E · Jan–Sept", [["2025", 314], ["2026", 206, "red"]], None, GA))
c.at("Ford has already cut the price", A.price("Mach-E GT", "$98,490", "$89,000", "previous price", "drive-away offer", None, "EV Central"))
c.at("desperate to shift", say("Ford \"desperate to shift\" stock – EV Central", "DESPERATE", 110))
c.at("Compare that with America", P("street"))
c.at("In October alone, the Model Y sold", bars("Electric SUVs", [["Tesla Model Y · Oct", 3105], ["Mach-E · 9 months", 206, "red"]], None, SRC))
chapters.append(c)

c = ch("ch07")
c.at(0, rank(5, "Mazda CX-70", "m_cx70", 1, "182 sold · -35%", "Jan–Sept 2026"))
c.at("It sold 182 cars", bars("Large SUVs over $80k · Jan–Sept", [["LR Defender", 3098], ["Mazda CX-70", 182, "red"]], None, GA))
c.at("the Land Rover Defender sold", photo("m_defender", 1, "in", cap="Land Rover Defender|17 for every CX-70"))
c.at("In July 2026, Mazda slashed", stat("$8,051", "Mazda CX-70 price cut · July 2026", "Mazda", count=False))
c.at("Then in late October", photo("m_cx70", 3, "left", cap="CX-70|ending US production"))
c.at("But when a car is built mainly for America", P("dealer"))
chapters.append(c)

c = ch("ch08")
c.at(0, rank(4, "Hyundai Sonata N Line", "m_sonata", 1, "179 sold · -37%", "Jan–Sept 2026"))
c.at("Here's a car whose sales are collapsing", P("cars"))
c.at("The Toyota Camry outsold it", stat("53 : 1", "Camry vs Sonata · 2026", GA, count=False))
c.at("Hyundai raised the Sonata N Line's price", A.price("Hyundai Sonata N Line", "$56,500", "$57,000", "before 1 Oct", "from 1 Oct (+ ORC)", None, "Hyundai"))
c.at("global economic factors", say("\"…global economic factors, manufacturing, logistics and local policy.\" – Hyundai", "LOCAL POLICY", 88))
c.at("Hyundai was fined 4.2 million", stat("$4.2M", "Hyundai NVES penalty · 2025", "ACM report", red=True, count=False))
c.at("And the bigger picture for Hyundai", photo("m_sonata", 3, "in", cap="Hyundai|-28.6% in October"))
chapters.append(c)

c = ch("ch09")
c.at(0, rank(3, "Skoda Fabia", "m_fabia", 3, "140 sold · -43%", "Jan–Sept 2026"))
c.at("The Fabia is Skoda's smallest car", photo("m_fabia", 1, "left"))
c.at("In the light car segment, the MG3 sold", bars("Light cars · Jan–Sept", [["MG3", 6340], ["Skoda Fabia", 140, "red"]], None, GA))
c.at("A cheap Chinese-made hybrid", photo("m_mg3", 1, "in", cap="MG3|45 for every Fabia"))
c.at("In October, the Skoda Superb", photo("m_superb", 3, "right", cap="Skoda Superb|9 sales in October"))
c.at("To be fair to Skoda", P("dealer"))
chapters.append(c)

c = ch("ch10")
c.at(0, rank(2, "Kia EV9", "m_ev9", 2, "120 sold · -50%", "Jan–Sept 2026"))
c.at("And here's how many Australians bought one", bars("Kia EV9 · Jan–Sept", [["2025", 238], ["2026", 120, "red"]], None, GA))
c.at("Toyota LandCruiser 300", photo("m_lc300", 3, "in", cap="LandCruiser 300|81 for every EV9"))
c.at("So what went wrong", P("ev"))
c.at("A hundred-thousand-dollar electric family bus", photo("m_ev9", 3, "left", cap="Kia EV9 GT|$129,250"))
c.at("sold just four cars in October", P("dealer"))
chapters.append(c)

c = ch("ch11")
c.at(0, rank(1, "Honda Accord", "m_accord", 3, "59 sold · -24%", "Jan–Sept 2026"))
c.at("That's fewer than seven cars a month", stat("< 7", "Honda Accords sold per month in Australia", GA, count=False))
c.at("The Accord is now sold here", P("cars"))
c.at("That's over one hundred and sixty Camrys", bars("Mid-size cars · Jan–Sept", [["Toyota Camry", 9471], ["Honda Accord", 59, "red"]], None, GA))
c.at("Honda's business model in Australia", P("dealer"))
c.at("Its end-of-year plate clearance", stat("$1,000", "gift card on the Accord · plate clearance", "CarExpert", count=False))
c.at("GoAuto made an important point", say("\"…unrelated to product quality…\" – GoAuto", "PRODUCT QUALITY", 105))
chapters.append(c)

c = ch("ch12")
c.at(0, title("October's Shockers", "1, 2, 3, 4 sales", "bonus", "street"))
c.at("88 models recorded zero sales", stat("88", "models with ZERO sales · October 2026", SRC, red=True))
c.at("The Audi Q4 e-tron", photo("m_q4", 1, "in", cap="Audi Q4 e-tron|2 sales · -96%"))
c.at("The BMW iX electric SUV", photo("m_ix", 1, "left", cap="BMW iX|4 sales · -86%"))
c.at("The Suzuki S-Cross", photo("m_scross", 1, "right", cap="Suzuki S-Cross|2 sales"))
c.at("The Renault Kangoo van", photo("m_kangoo", 1, "in", cap="Renault Kangoo|2 sales · -97%"))
c.at("And the Alfa Romeo Tonale", photo("m_tonale", 1, "left", cap="Alfa Romeo Tonale|1 sale"))
c.at("The Toyota Fortuner sold just eight", photo("m_fortuner", 1, "in", cap="Toyota Fortuner|8 sales · axed"))
chapters.append(c)

c = ch("ch13", 2.5)
c.at(0, title("What This Means for You", "buyers & owners", "advice", "dealer"))
c.at("If you're buying, cars that aren't selling", P("money"))
c.at("But be careful", P("street"))
c.at("And if you already own one", P("cars"))
c.at("So that's the list", P("dealer"))
c.at("Which car on this list would you actually buy", cta("Which would YOU buy?", "if the price was right · comments"))
c.at("hit like and subscribe", cta("Like · Subscribe", "numbers-first car videos"))
c.at("in the next video", title("Biggest Discounts Right Now", "next video", "coming up", "street"))
chapters.append(c)

CTX = ["dealer", "street", "cars", "street", "cars", "dealer", "ev", "cars", "dealer", "cars", "ev", "dealer", "street", "dealer"]
print(A.finish(chapters, "AUS19_Refuse_To_Buy.mp4", CTX, subtitles="AUS19.ass", theme="electric"))
