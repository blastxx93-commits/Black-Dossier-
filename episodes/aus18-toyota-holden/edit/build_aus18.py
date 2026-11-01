#!/usr/bin/env python3
"""AUS18 Toyota: the next Holden?: full edit, shots anchored to phrases.
    python3 build_aus18.py <narration_dir> > episode.json   (run from the work folder)
Opens on car footage (rule 01/11/2026). Balanced: shows both sides; verdict 'not yet'.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "engine"))
import aus_kit as A
from aus_kit import P, photo, stat, bars, say, cta, title, ch, questions

PHOTOS = {
    "toyota": ["h_toyota_dealer", "ai:ai_family_suv", "m_kluger", "m_yaris_cross", "m_yaris"],
    "holden": ["h_holden_dealer", "m_holden_old"],
    "outback": ["ai:ai_ute_farm", "h_outback"],
    "dealer": ["h_dealer", "h_keys"],
    "ship": ["h_ship"],
    "street": ["h_traffic"],
    "money": ["h_calc"],
    "race": ["h_bathurst"],
}
CLIPS = json.load(open(os.path.join(HERE, "clips.json")))
GENERIC = CLIPS.pop("_generic", [])
FALLBACK = {"toyota": ["dealer", "street", "outback", "ship", "money"], "holden": ["race", "street"], "outback": ["toyota"], "dealer": ["street"], "ship": ["dealer"],
            "street": ["dealer"], "money": ["dealer"], "race": ["holden"]}
RES = ["m_rav4/1", "m_rav4_old/1", "m_rav4_old/3", "m_hilux/3", "m_prado/1", "m_prado/3", "m_lc300/3", "m_lc300/1", "m_lc70/1", "m_lc70/3",
       "m_kluger/1", "m_yaris/1", "m_yaris_cross/1", "m_corolla/3", "m_commodore/1", "m_commodore/3", "m_holden_monaro/1", "m_holden_old/1",
       "m_holden_old/3", "m_sealion7/1", "m_sealion7/3", "m_atto3/1", "m_shark6/1", "m_h7/1", "m_cx5/1", "m_outlander/1"]
A.setup(sys.argv[1], os.path.join(HERE, "skip.json"), PHOTOS, CLIPS, GENERIC, FALLBACK, ["toyota", "street", "dealer", "outback", "money"], reserved=RES)
A.CLIP_TARGET = 0.55
A.MAX_HOLD, A.KEEP = 16.0, 10.0
chapters = []
SRC = "VFACTS via CarExpert"

c = ch("ch00_hook", 0.6)
c.at(0, photo("m_rav4", 1, "in", cap="243|cars between Toyota and BYD · June 2026"))
c.at("separating the most powerful car brand", photo("m_sealion7", 1, "left", cap="BYD|18,881 sales in June"))
c.at("Toyota has been Australia's best-selling brand since 2003", photo("m_lc300", 3, "right", cap="Toyota|#1 in Australia since 2003"))
c.at("Holden. The brand that was once", photo("m_holden_old", 1, "in", cap="Holden|Australia's own"))
c.at("Holden was gone", photo("m_commodore", 3, "left", cap="Holden|retired 2020"))
c.at("Now Toyota's own numbers are falling", stat("-24.6%", "Toyota sales · Jan–May 2026", "CarExpert", red=True))
c.at("The Prado, the Kluger, the Yaris", photo("m_prado", 1, "in", cap="Toyota Prado|-64% in May"))
c.at("Toyota is the new Holden", say("\"Toyota is the new Holden – not in a good way.\" – CarsGuide", "NEW HOLDEN", 95))
c.at("So is it true", title("Is Toyota the Next Holden?", "the real numbers", "Australia 2026", "toyota"))
c.at("what actually killed Holden", P("holden"))
c.at("whether your Toyota is still the safe bet", P("toyota"))
chapters.append(c)

c = ch("ch01")
c.at(0, P("toyota"))
c.at("In 2024, Toyota sold 241,296", stat("241,296", "Toyota sales in Australia · 2024 record", "CarExpert"))
c.at("almost one in every five new vehicles", stat("1 in 5", "new vehicles sold in 2025 was a Toyota", "CarsGuide", count=False))
c.at("Toyota's rise is one of the great business stories", P("street"))
c.at("including the Camry at its factory in Altona", P("toyota"))
c.at("Think about the names", photo("m_hilux", 3, "in", cap="Toyota HiLux"))
c.at("The LandCruiser, a legend", photo("m_lc70", 1, "right", cap="LandCruiser 70"))
c.at("That reputation shows up in the resale numbers", bars("Value kept after 2 years", [["RAV4", 88], ["LandCruiser", 88], ["HiLux", 85]], None,
     "Pickles / Datium · 2025", suffix="%"))
c.at("Toyota didn't just lead the market", P("outback"))
chapters.append(c)

c = ch("ch02")
c.at(0, title("The 2026 Slide", "in Toyota's own numbers", "the data", "toyota"))
c.at("Its share of the new-car market fell from 20.7", bars("Toyota market share", [["2025 (to May)", 20.7], ["2026 (to May)", 16.0, "red"]], None, "CarExpert", suffix="%"))
c.at("And it was across the range", bars("Toyota models · Jan–May 2026", [["Prado", -45.0], ["RAV4", -47.1], ["Yaris", -44.4], ["Kluger", -39.9],
     ["Yaris Cross", -31.7], ["HiLux", -13.2]], None, "CarExpert", suffix="%"))
c.at("And LandCruiser 70 Series ute sales", photo("m_lc70", 3, "in", cap="LandCruiser 70 ute|-82%"))
c.at("Toyota's explanation for the Prado", say("\"…reflects lower supply on this very popular model.\" – Toyota", "LOWER SUPPLY", 95))
c.at("LandCruiser 300 and 70 Series wagon sales combined", photo("m_lc300", 1, "left", cap="LandCruiser wagons|+29.3% Jan–May"))
c.at("By September, things had improved", bars("Toyota · Jan–Sept", [["2025", 181860], ["2026", 152944, "red"]], None, SRC))
c.at("For any other brand, that would be a bad year", P("toyota"))
chapters.append(c)

c = ch("ch03")
c.at(0, P("street"))
c.at("In June 2026, Toyota sold 19,124", bars("June 2026", [["Toyota", 19124], ["BYD", 18881, "red"]], None, "VFACTS"))
c.at("A Chinese brand that only started", photo("m_sealion7", 3, "in", cap="BYD|13.5% share in June"))
c.at("The Australian automotive market has shifted", say("\"…shifted on its axis…\" – Tony Weber, FCAI", "AXIS", 115))
c.at("We asked our customers to back us in", P("dealer"))
c.at("BYD hasn't caught Toyota since", bars("September 2026", [["Toyota", 17682], ["BYD", 8191]], None, "VFACTS"))
c.at("Chinese-built cars now make up almost four in ten", stat("38.9%", "of new cars were built in China · Sept 2026", "Cars24 / VFACTS"))
c.at("But here's an important detail", bars("Japanese brands · Jan–Sept 2026", [["Toyota", -15.9], ["Mazda", -16.2], ["Subaru", -29.3], ["Mitsubishi", -30.2],
     ["Nissan", -33.3]], None, SRC, suffix="%"))
c.at("If Toyota is in trouble", photo("m_outlander", 1, "right", cap="Mitsubishi|-30.2%"))
chapters.append(c)

c = ch("ch04")
c.at(0, title("How Holden Fell", "the lesson", "history", "holden"))
c.at("The Commodore was the country's favourite car", photo("m_commodore", 1, "in", cap="Holden Commodore"))
c.at("Holden and Ford's rivalry defined Bathurst", P("race"))
questions(c, ["2003 · Toyota takes #1", "2013 · local manufacturing to end", "2017 · last Aussie Commodore", "2020 · Holden retired"],
          ["But in 2003, Toyota", "In 2013, Holden announced", "The last Australian-built Commodore", "Then, on the 17th of February 2020"])
c.at("regret[s] that we could not prioritize", say("\"…could not prioritize the investment required for Holden…\" – GM", "INVESTMENT", 92))
c.at("By the end of 2020, Holden was gone", photo("m_holden_monaro", 1, "left"))
c.at("The lesson most people take from Holden", P("holden"))
c.at("It's worth remembering that Holden's decline", P("street"))
chapters.append(c)

c = ch("ch05")
c.at(0, P("toyota"))
c.at("Tell me in the comments", cta("Do you own a Toyota?", "would you buy another? comments"))
c.at("hit subscribe", cta("Subscribe", "numbers-first car videos"))
chapters.append(c)

c = ch("ch06")
c.at(0, title("The Case For", "'the next Holden'", "prosecution", "street"))
c.at("there are no guarantees in this business", say("\"…there are no guarantees in this business…\" – Stephen Ottley, CarsGuide", "NO GUARANTEES", 88))
c.at("The number of Chinese models on sale", stat("72 → 120", "Chinese models on sale by 2027", "Cars24", count=False))
c.at("Price is a big part of it", A.price("Plug-in hybrid SUVs", "$58,840", "$49,990", "RAV4 PHEV + ORC", "Haval H7 drive-away", None, "Toyota / GWM"))
c.at("GWM's new Haval H7", photo("m_h7", 1, "in"))
c.at("Then there's regulation", bars("NVES target · utes & vans", [["2026", 180], ["2027", 150, "red"]], None, "Federal government", suffix=" g/km"))
c.at("cannot rule out", say("Toyota \"cannot rule out\" price increases", "CANNOT RULE OUT", 100))
c.at("And there's the question of whether loyalty is weakening", P("dealer"))
c.at("And the brand count keeps growing", stat("~70", "car brands in Australia", "Toyota Australia", count=False))
chapters.append(c)

c = ch("ch07")
c.at(0, title("The Case Against", "Toyota's side", "defence", "toyota"))
c.at("This has predominantly been a production", say("\"…predominantly a production and stock related issue.\" – John Pappas, Toyota", "PRODUCTION", 88))
c.at("Toyota secured two extra shipments", P("ship"))
c.at("There's another telling statistic", bars("New cars sold per dealer, per month", [["Toyota", 72], ["BYD", 48]], None, "BDO · early 2026"))
c.at("Second, the numbers are already turning", stat("4,624", "Toyota RAV4 · Sept 2026 (+81%) · #2 in Australia", "VFACTS"))
c.at("We don't plan to be declining", say("\"We don't plan to be declining. We plan to continue to grow.\" – Pappas", "GROW", 90))
c.at("Toyota is certainly in no danger", say("\"Toyota is certainly in no danger of collapsing like Holden did…\" – Ottley", "NO DANGER", 88))
c.at("And the differences with Holden are huge", P("toyota"))
c.at("Toyota's best sellers", photo("m_rav4_old", 1, "in", cap="Toyota RAV4 PHEV"))
chapters.append(c)

c = ch("ch08")
c.at(0, P("toyota"))
c.at("plug-in hybrids made up 39 per cent", stat("39%", "of RAV4 sales were plug-in hybrid · July 2026", "CarExpert"))
c.at("A cheaper RAV4 GXL plug-in hybrid", photo("m_rav4_old", 3, "left", cap="RAV4 GXL PHEV|early 2027"))
c.at("The new HiLux arrived", P("outback"))
c.at("offering deals", stat("$4,000", "HiLux SR5 deposit bonus · Toyota Finance", "CarsGuide", count=False))
c.at("Toyota has forecast around 230,000", stat("~230,000", "Toyota's 2026 sales forecast", "Toyota / CarExpert", count=False))
c.at("Toyota has also set a target", P("toyota"))
c.at("That's not the behaviour of a company in denial", P("dealer"))
chapters.append(c)

c = ch("ch09")
c.at(0, title("Toyota Owners & Buyers", "what to do", "advice", "dealer"))
c.at("If you already own a Toyota", P("toyota"))
c.at("If you're buying, this could actually be your moment", P("money"))
c.at("A brand that has lost market share needs your sale", say("They need your sale more than before.", "YOUR SALE", 115))
c.at("But keep an eye on resale", P("street"))
c.at("And if you've been waiting months", P("dealer"))
chapters.append(c)

c = ch("ch10", 2.5)
c.at(0, say("Is Toyota the next Holden?", "NEXT HOLDEN", 125))
c.at("On the evidence, no", say("Not yet.", "NOT YET", 160))
c.at("But the era of Toyota's easy dominance is over", P("toyota"))
questions(c, ["Share below 15% for a year", "A rival wins a full month", "Models cut, no replacement", "Resale values slip"],
          ["If Toyota's share falls below", "If BYD or another rival beats", "If Toyota starts cutting models", "Or if its famous resale values"])
c.at("Two or three together would be a crisis", P("street"))
c.at("If this helped", cta("Like · Subscribe · Share", "with a Toyota owner you know"))
c.at("will Toyota still be number one in 2030", cta("Toyota #1 in 2030?", "comments"))
c.at("in the next video", title("The Prado Just Got Undercut", "next video", "coming up", "outback"))
chapters.append(c)

CTX = ["toyota", "toyota", "toyota", "street", "holden", "toyota", "street", "toyota", "toyota", "dealer", "toyota"]
print(A.finish(chapters, "AUS18_Toyota_Holden.mp4", CTX, subtitles="AUS18.ass"))
