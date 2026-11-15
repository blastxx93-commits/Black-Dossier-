#!/usr/bin/env python3
"""AUS22 The 10 cars Australians went crazy for in 2026: full edit, shots anchored to phrases.
    python3 build_aus22.py <narration_dir> > episode.json   (run from the work folder)
Opens on car photos with the impact number as caption. Template 'mint'. Real photos only, every file reviewed.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "engine"))
import aus_kit as A
from aus_kit import P, photo, stat, bars, say, cta, title, ch, rank

PHOTOS = {
    "dealer": ["h_dealer", "h_lot", "h_keys", "m_byd"],
    "street": ["h_traffic", "h_outback"],
    "money": ["h_money"], "ev": ["h_ev"], "port": ["h_port"],
    "cars": ["m_sealion6", "m_starray", "m_sportage", "m_kona2", "m_dmax", "m_gac", "m_everest"],
    "ute": ["m_dmax", "m_ranger"], "gloom": ["h_port"],
}
CLIPS = json.load(open(os.path.join(HERE, "clips.json")))
GENERIC = CLIPS.pop("_generic", [])
FALLBACK = {k: ["street", "dealer", "cars"] for k in PHOTOS}
FALLBACK.update({"street": ["dealer", "cars"], "dealer": ["street", "cars"], "cars": ["street", "dealer"]})
RES = ["m_ex5/1", "m_ex5/2", "m_ex5/3", "m_ex5/4", "m_modely/1", "m_modely/3", "m_tiggo4/1", "m_tiggo4/3", "m_hilux/1", "m_hilux/3",
       "m_atto2/1", "m_atto2/3", "m_atto1/1", "m_jolion/1", "m_jolion/2", "m_prado/1", "m_everest/3", "m_j5/2", "m_j5/3", "m_j5/4",
       "m_zeekr7x/1", "m_zeekr7x/2", "m_zeekr7x/3", "m_zeekr7x/4", "m_sealion7/1", "m_sealion7/3", "m_ranger/1", "m_ranger/3", "m_rav4/3",
       "m_shark6/1", "m_tiggo7/1", "m_kona/1", "m_kona/3", "m_gac/1", "m_byd/1"]
A.setup(sys.argv[1], os.path.join(HERE, "skip.json"), PHOTOS, CLIPS, GENERIC, FALLBACK, ["dealer", "street", "cars"], reserved=RES)
A.CLIP_TARGET = 0.6
A.MAX_HOLD, A.KEEP = 15.0, 9.5
chapters = []
SRC = "VFACTS via CarExpert"
YTD = "VFACTS / EVC · Jan–Sept 2026"

c = ch("ch00_hook", 0.6)
c.at(0, photo("m_ex5", 1, "in", cap="+620%|one SUV · September 2026"))
c.at("A car most Australians had never heard of", photo("m_ex5", 3, "left", cap="Geely EX5|national top 10"))
c.at("One electric SUV more than doubled", photo("m_modely", 1, "right", cap="Tesla Model Y|+108%"))
c.at("One brand you've probably never driven", photo("m_zeekr7x", 1, "in", cap="Zeekr|+1,560%"))
c.at("A small Chinese SUV is outselling", photo("m_tiggo4", 3, "left", cap="Chery Tiggo 4|beating the Kona"))
c.at("And Toyota's most famous ute", photo("m_hilux", 3, "right", cap="Toyota HiLux|#1 in October"))
c.at("2026 has been the most dramatic year", P("street"))
c.at("So in this video, I'm counting down", title("10 Cars Australia Went CRAZY For", "2026's biggest hits", "Australia 2026", "dealer"))
c.at("And stay to the end", P("dealer"))
chapters.append(c)

c = ch("ch01")
c.at(0, P("street"))
c.at("Australians bought 107,493", stat("107,493", "new vehicles · October 2026 · record October", SRC))
c.at("Electric car sales in October were up 237", stat("+237%", "EV sales · Oct 2026 vs Oct 2025", SRC))
c.at("BYD sold more than ten thousand", photo("m_byd", 1, "in", cap="BYD|#2 brand in Australia"))
c.at("In the first nine months of the year, Geely", bars("Brand growth · Jan–Sept 2026", [["Zeekr", 1560.3], ["Geely", 639.2], ["Omoda Jaecoo", 620.9]],
     None, "ACM / VFACTS", suffix="%"))
c.at("Meanwhile, plenty of familiar names", P("dealer"))
c.at("So what makes a winner in 2026", P("cars"))
c.at("A quick note on the numbers", P("street"))
chapters.append(c)

c = ch("ch02")
c.at(0, rank(10, "BYD Atto 2", "m_atto2", 1, "#8 in October", "brand-new nameplate"))
c.at("In the first half of 2026, the Atto 2 sold", stat("5,401", "BYD Atto 2 · first half 2026", "CarExpert"))
c.at("And in October, it was the eighth", stat("1,943", "Atto 2 · October 2026 · #8 in Australia", SRC))
c.at("Part of the reason is price", photo("m_atto2", 3, "in", cap="Atto 2 DM-i|$25,990 drive-away"))
c.at("If buyers don't want the Atto 2", photo("m_atto1", 1, "left", cap="BYD Atto 1|$19,990 drive-away"))
c.at("And that's exactly why BYD", P("dealer"))
chapters.append(c)

c = ch("ch03")
c.at(0, rank(9, "GWM Haval Jolion", "m_jolion", 1, "17,051 sold · +20%", "Jan–Sept 2026"))
c.at("That puts it above some very big names", P("cars"))
c.at("The reason is value", photo("m_jolion", 2, "in", cap="Jolion Hybrid|$32,990 drive-away"))
c.at("And the Jolion shows something important", P("street"))
c.at("GWM as a brand has had a tougher", P("dealer"))
chapters.append(c)

c = ch("ch04")
c.at(0, rank(8, "Toyota Prado", "m_prado", 1, "+64% in October", "the comeback"))
c.at("In the first five months of the year", stat("-45%", "Prado sales · Jan–May 2026", "CarExpert", red=True))
c.at("Then the supply came back", stat("2,397", "Prado · October 2026 · +64%", SRC))
c.at("By the end of October, the Prado had moved ahead", bars("Year to October 2026", [["Toyota Prado", 18062], ["Ford Everest", 17944]], None, SRC))
c.at("That matters, because the Everest", photo("m_everest", 3, "in", cap="Ford Everest|overtaken"))
c.at("The new Prado is bigger", P("ute"))
chapters.append(c)

c = ch("ch05")
c.at(0, rank(7, "Chery Tiggo 4", "m_tiggo4", 1, "19,865 sold · +43%", "Jan–Sept 2026"))
c.at("In the first nine months of the year, the Tiggo 4", bars("Jan–Sept 2026", [["Chery Tiggo 4", 19865], ["Hyundai Kona", 18533]], None, YTD))
c.at("ahead of the Hyundai Kona", photo("m_kona", 1, "in", cap="Hyundai Kona|beaten"))
c.at("The reason is price", stat("$23,990", "Tiggo 4 Urban · drive-away + $1,500 fuel card", "CarSorted", count=False))
c.at("And Chery as a brand is flying", photo("m_tiggo7", 1, "left", cap="Chery|+77% in first half"))
c.at("In October, the Tiggo 4 was again", P("dealer"))
chapters.append(c)

c = ch("ch06")
c.at(0, rank(6, "Jaecoo J5", "m_j5", 2, "11,000+ sold", "Jan–Sept 2026"))
c.at("According to ACM's motoring team", stat("+621%", "Omoda Jaecoo · Jan–Sept 2026", "ACM / VFACTS"))
c.at("Why? Price and style", bars("Jaecoo J5 drive-away", [["J5 petrol", 25990], ["J5 EV", 36990]], None, "Jaecoo / CarSauce", prefix="$"))
c.at("It has a boxy, upmarket look", photo("m_j5", 3, "in"))
c.at("The J5 EV had more than four thousand orders", photo("m_j5", 4, "left", cap="J5 EV|4,000+ orders"))
c.at("The J5 shows how fast", P("dealer"))
chapters.append(c)

c = ch("ch07")
c.at(0, rank(5, "Zeekr 7X", "m_zeekr7x", 2, "Zeekr +1,560%", "Jan–Sept 2026"))
c.at("In the first nine months of the year, Zeekr's sales", stat("12,120", "Zeekr sales · Jan–Sept 2026 · +1,560%", "ACM / VFACTS"))
c.at("The Driven reported in May", photo("m_zeekr7x", 3, "in", cap="Zeekr 7X|best-selling premium SUV"))
c.at("Think about how remarkable that is", P("cars"))
c.at("The 7X wins on technology and value", photo("m_zeekr7x", 4, "left"))
c.at("If you want to know where the luxury car market", P("ev"))
chapters.append(c)

c = ch("ch08")
c.at(0, rank(4, "Toyota HiLux", "m_hilux", 1, "#1 in October · +34%", "5,954 sales"))
c.at("It beat the Ford Ranger", bars("October 2026", [["Toyota HiLux", 5954], ["Ford Ranger", 4841]], None, SRC))
c.at("That's a big deal, because it had been", photo("m_ranger", 1, "in", cap="Ford Ranger|led most of 2026"))
c.at("And Toyota is fighting harder than usual", stat("$4,000", "HiLux SR5 finance deposit bonus", "CarExpert", count=False))
c.at("Now, the HiLux isn't growing", P("ute"))
chapters.append(c)

c = ch("ch09")
c.at(0, rank(3, "Geely EX5", "m_ex5", 2, "+620% in September", "#10 in October"))
c.at("Geely as a brand sold 23,632", stat("23,632", "Geely sales · Jan–Sept 2026 · +639%", "ACM / VFACTS"))
c.at("The EX5 is a mid-size electric SUV", photo("m_ex5", 4, "in", cap="Geely EX5|$41,990 + ORC"))
c.at("Geely isn't a small company", P("ev"))
chapters.append(c)

c = ch("ch10")
c.at(0, rank(2, "BYD Sealion 7", "m_sealion7", 1, "19,964 sold · +135%", "#5 in Australia"))
c.at("In the first nine months of 2026, it sold 19,964", bars("Jan–Sept 2026", [["BYD Sealion 7", 19964], ["Isuzu D-Max", 18237], ["Ford Everest", 16203]],
     None, YTD))
c.at("The Sealion 7 gives buyers", photo("m_sealion7", 3, "in", cap="Sealion 7 Premium|$50,990 with cashback"))
c.at("BYD finished second in the national brand rankings", stat("10,025", "BYD sales · October 2026 · +153%", SRC))
c.at("The Sealion 7 is the car", P("dealer"))
chapters.append(c)

c = ch("ch11")
c.at(0, rank(1, "Tesla Model Y", "m_modely", 3, "35,930 · +108%", "#3 in Australia · Jan–Sept"))
c.at("Think about that", bars("Jan–Sept 2026", [["Ford Ranger", 37858], ["Toyota HiLux", 36616], ["Tesla Model Y", 35930], ["Toyota RAV4", 31209]],
     None, YTD))
c.at("And in May and June", say("#1 new vehicle in Australia · May & June 2026", "#1", 110))
c.at("In October, the Model Y sold 3,105", stat("+322%", "Model Y · October 2026", SRC))
c.at("It hasn't been perfect", P("ev"))
c.at("When an EV sits on the national podium", P("street"))
chapters.append(c)

c = ch("ch12")
c.at(0, title("Honourable Mentions", "just missed the top 10", "bonus", "street"))
c.at("The Ford Ranger", photo("m_ranger", 3, "in", cap="Ford Ranger|#1 year to September"))
c.at("The new-generation Toyota RAV4", photo("m_rav4", 3, "left", cap="Toyota RAV4|+81% in September"))
c.at("The BYD Shark 6", photo("m_shark6", 1, "right", cap="BYD Shark 6|+72% in October"))
c.at("The Chery Tiggo 7", P("cars"))
c.at("The Hyundai Kona", photo("m_kona", 3, "in", cap="Hyundai Kona|+9% · 18,533"))
c.at("And GAC", photo("m_gac", 1, "left", cap="GAC|3,175 sold already"))
chapters.append(c)

c = ch("ch13", 2.5)
c.at(0, title("What the Winners Have in Common", "and what it means for you", "verdict", "dealer"))
c.at("First, value", P("money"))
c.at("Second, choice of power", P("ev"))
c.at("Third, the old champions", P("ute"))
c.at("And what does this mean for you", P("dealer"))
c.at("So that's the list", P("street"))
c.at("which of these would you actually buy", cta("Which would YOU buy?", "and 2027's surprise hit? comments"))
c.at("hit like and subscribe", cta("Like · Subscribe", "numbers-first car videos"))
chapters.append(c)

CTX = ["dealer", "street", "cars", "cars", "ute", "cars", "dealer", "ev", "ute", "ev", "dealer", "ev", "street", "dealer"]
print(A.finish(chapters, "AUS22_Hits_2026.mp4", CTX, subtitles="AUS22.ass", theme="mint"))
