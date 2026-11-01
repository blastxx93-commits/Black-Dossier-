#!/usr/bin/env python3
"""AUS17 Chinese cars just took over Australia: full edit, shots anchored to phrases.
    python3 build_aus17.py <narration_dir> > episode.json   (run from the work folder)
Channel rule 01/11/2026: the video opens on car footage (numbers as captions), no graphics in the first seconds.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "engine"))
import aus_kit as A
from aus_kit import P, photo, stat, bars, say, cta, title, ch, questions

PHOTOS = {
    "ship": ["h_ship", "h_port", "ai:ai_car_yard_rows"],
    "china": ["h_shanghai", "h_factory"],
    "japan": ["h_tokyo"],
    "dealer": ["ai:ai_ev_showroom", "h_dealer", "h_keys"],
    "ev": ["h_ev"],
    "street": ["ai:ai_driveway_mix", "h_traffic"],
    "money": ["h_calc"],
    "cn_cars": ["m_atto3", "m_ex5", "m_jaecoo", "m_omoda", "m_zeekr", "m_atto1", "m_sealion7"],
    "jp_cars": ["m_cx5", "m_outlander", "m_xtrail", "m_forester", "m_corolla", "m_hilux"],
}
CLIPS = json.load(open(os.path.join(HERE, "clips.json")))
GENERIC = CLIPS.pop("_generic", [])
FALLBACK = {"ship": ["china", "street", "cn_cars"], "china": ["ship"], "japan": ["street"], "dealer": ["street"], "ev": ["dealer"], "street": ["dealer"],
            "money": ["dealer"], "cn_cars": ["dealer"], "jp_cars": ["street"]}
RES = ["m_sealion7/1", "m_sealion7/3", "m_tiggo4/3", "m_jolion/1", "m_jolion/4", "m_ex5/1", "m_ex5/2", "m_zeekr/1", "m_zeekr/3", "m_model_y/1",
       "m_model_y/3", "m_denza/1", "m_denza/2", "m_shark6/1", "m_terron/1", "m_atto1/1", "m_cx5/1", "m_outlander/1", "m_forester/3",
       "m_xtrail/1", "m_ranger/1", "m_hilux/3", "m_jaecoo/2", "m_omoda/1", "m_atto3/1"]
A.setup(sys.argv[1], os.path.join(HERE, "skip.json"), PHOTOS, CLIPS, GENERIC, FALLBACK, ["street", "dealer", "ship", "cn_cars", "jp_cars"], reserved=RES)
A.CLIP_TARGET = 0.55
A.MAX_HOLD, A.KEEP = 15.0, 9.5
chapters = []
SRC = "VFACTS via CarExpert"

c = ch("ch00_hook", 0.6)
c.at(0, P("ship", cap="42,045|China-built cars sold in ONE month · Sept 2026"))
c.at("More than every car shipped from Japan", photo("m_sealion7", 1, "in", cap="BYD Sealion 7|#5 in Australia · Sept 2026"))
c.at("Japan had been Australia's biggest source", photo("m_cx5", 1, "left", cap="Japan|#1 source of cars since 1998"))
c.at("Toyota, Mazda, Mitsubishi", P("jp_cars"))
c.at("And in 2026, China blew past all of them", photo("m_ex5", 1, "right", cap="Geely EX5|+620% · #8 in Australia"))
c.at("Almost four in every ten new vehicles", stat("38.9%", "of new-car sales were built in China · Sept 2026", "Cars24 / VFACTS"))
c.at("Four of the ten best-selling models", photo("m_tiggo4", 3, "in", cap="Chery Tiggo 4|#6 in Australia"))
c.at("One Chinese brand grew more than eight hundred", stat("+870%", "Geely sales · Sept 2026 vs Sept 2025", "VFACTS"))
c.at("Another went from a few hundred sales", photo("m_zeekr", 1, "left", cap="Zeekr|730 → 12,120 sales"))
c.at("This isn't a slow change", title("China Just Took Over", "Australia's car market in 12 months", "2026", "ship"))
c.at("Who's winning, who's getting crushed", P("dealer"))
c.at("the risks, the brands that might not last", P("street"))
chapters.append(c)

c = ch("ch01")
c.at(0, P("ship"))
c.at("In May 2025, Chinese-made cars made up 19.5", bars("China-built share of new-car sales (May)", [["2024", 15.0], ["2025", 19.5], ["2026", 34.8, "red"]], None,
     "CarExpert", suffix="%"))
c.at("Then came February 2026", bars("Source of new cars · February 2026", [["China", 22300, "red"], ["Japan", 21600], ["Thailand", 19400]], None, "FCAI via Caixin"))
c.at("For the first time since 1998", P("japan"))
c.at("By May, CarExpert reported", P("china"))
c.at("The increase in Chinese-made vehicle sales", say("\"…largely at the expense of Japan.\" – CarExpert", "JAPAN", 110))
c.at("In June, something even bigger happened", bars("June 2026", [["China", 55331, "red"], ["Japan + Thailand", 50395]], None, "Cars24 / VFACTS"))
c.at("Part of that was a single ship", P("ship"))
c.at("But in September, it happened again", bars("September 2026", [["China", 42045, "red"], ["Japan + Thailand", 40933]], None, "Cars24 / VFACTS"))
c.at("From fifteen per cent to nearly forty", say("15% → 38.9% in about two years", "38.9%", 120))
c.at("And there's a twist of history here", P("japan"))
c.at("By the time Ford, Holden and Toyota closed", P("street"))
c.at("Now the same story is playing out again", P("china"))
chapters.append(c)

c = ch("ch02")
c.at(0, P("cn_cars"))
c.at("BYD is the headline", bars("Biggest brands · Jan–Sept 2026", [["Toyota", 152944], ["BYD", 76614, "red"]], None, SRC))
c.at("And in June, it came within 243 cars", bars("June 2026", [["Toyota", 19124], ["BYD", 18881, "red"]], None, "VFACTS"))
c.at("Then there's Chery", P("cn_cars"))
c.at("Geely is the most extraordinary story", bars("Growth · Jan–Sept 2026", [["Geely", 639], ["BYD", 102], ["Chery", 58.2]], None, SRC, prefix="+", suffix="%"))
c.at("Its EX5 electric SUV sold 2,008", photo("m_ex5", 2, "in", cap="Geely EX5|2,008 sales in September"))
c.at("Geely's premium brand, Zeekr", photo("m_zeekr", 3, "right", cap="Zeekr|730 → 12,120"))
c.at("Omoda Jaecoo was up almost twelve hundred", photo("m_jaecoo", 2, "left", cap="Jaecoo|+1,177% first half"))
c.at("and its Haval Jolion was seventh", photo("m_jolion", 4, "in", cap="GWM Haval Jolion|#7 in September"))
c.at("Even MG, owned by China's SAIC", P("dealer"))
c.at("And the Chinese brands are moving upmarket", photo("m_denza", 1, "in", cap="Denza B5|aimed at the Toyota Prado"))
c.at("had been cut to under seventy-five thousand", photo("m_denza", 2, "right", cap="Denza B5|under $75,000 drive-away"))
c.at("The Australian automotive market has shifted", say("\"The Australian automotive market has shifted on its axis…\" – Tony Weber, FCAI", "SHIFTED", 88))
c.at("We asked our customers to back us in", say("\"We asked our customers to back us in…\" – Stephen Collins, BYD", "BACK US", 92))
chapters.append(c)

c = ch("ch03")
c.at(0, P("street"))
c.at("The Ford Ranger was number one", photo("m_ranger", 1, "in", cap="Ford Ranger|#1 · 5,062"))
c.at("But right behind them", bars("Chinese models in the top 10 · Sept 2026", [["BYD Sealion 7", 2687], ["Chery Tiggo 4", 2059], ["GWM Haval Jolion", 2018],
     ["Geely EX5", 2008]], None, "VFACTS"))
c.at("The Tesla Model Y sold in Australia is built in China", photo("m_model_y", 1, "left", cap="Tesla Model Y|built in China · #1 in May, June & August"))
c.at("So when you count where cars are actually made", P("china"))
c.at("There's also a flood of new models coming", stat("72 → 120", "Chinese models on sale in Australia by 2027", "Cars24", count=False))
c.at("Chery's upmarket brand, Exlantix", P("dealer"))
c.at("If you think the takeover is finished", say("It's barely started.", "BARELY", 150))
c.at("And the next battleground is the most Australian one", photo("m_shark6", 1, "in", cap="BYD Shark 6|13,500+ sold in 2026"))
c.at("LDV's new Terron 9 was up 195", photo("m_terron", 1, "right", cap="LDV Terron 9|+195% · Sept 2026"))
c.at("The Ranger and the HiLux have owned this segment", P("cn_cars"))
chapters.append(c)

c = ch("ch04")
c.at(0, P("jp_cars"))
c.at("Total new-vehicle sales for the first nine months", stat("914,312", "new vehicles · Jan–Sept 2026 – flat on 2025", SRC))
c.at("That means this is a zero-sum game", say("A zero-sum game.", "ZERO-SUM", 140))
c.at("Here's who's losing", bars("Japanese brands · Jan–Sept 2026", [["Nissan", -33.3], ["Mitsubishi", -30.2], ["Subaru", -29.3], ["Mazda", -16.2],
     ["Toyota", -15.9]], None, SRC, suffix="%"))
c.at("According to analysis by John Cadogan", bars("Built in… · Jan–Aug 2026 vs 2025", [["China", 71], ["Japan", -22]], None, "Auto Expert", suffix="%"))
c.at("It's not just the Japanese, either", photo("m_outlander", 1, "in", cap="Mitsubishi|-30.2% this year"))
c.at("Volkswagen was down almost 37", P("street"))
c.at("To put the scale of this into perspective", bars("Change in sales · Jan–Sept 2026", [["BYD", 38686], ["Geely", 20434], ["Chery", 13988],
     ["Mazda", -11380], ["Toyota", -28916]], None, "calculated from VFACTS"))
c.at("The money hasn't left the market", P("dealer"))
chapters.append(c)

c = ch("ch05")
c.at(0, P("cn_cars"))
c.at("Tell me in the comments", cta("Would you buy a Chinese car?", "tell me in the comments"))
c.at("hit subscribe", cta("Subscribe", "numbers-first car videos"))
chapters.append(c)

c = ch("ch06")
c.at(0, title("Why Australians Are Switching", "4 reasons", "the why", "dealer"))
c.at("The first is price", say("1 · Price", "1", 150))
c.at("BYD's little Atto 1 electric hatch", photo("m_atto1", 1, "in", cap="BYD Atto 1|from $23,990 + ORC"))
c.at("taking the Sealion 5 plug-in hybrid SUV down to $29,990", stat("$29,990", "BYD Sealion 5 PHEV with cashback (+ ORC)", "CarsGuide", count=False))
c.at("The second is technology", say("2 · Technology", "2", 150))
c.at("In September, electric vehicles outsold petrol cars", P("ev"))
c.at("The third is timing", say("3 · Timing", "3", 150))
c.at("diesel hit as high as $3.50", stat("$3.50/L", "diesel peak in parts of Australia · May 2026", "CarExpert", red=True, count=False))
c.at("Chinese brands had exactly the right cars", P("cn_cars"))
c.at("And the fourth is trust", say("4 · Trust", "4", 150))
c.at("Omoda Jaecoo has said publicly", photo("m_omoda", 1, "left", cap="Omoda Jaecoo|'stigma mostly gone'"))
c.at("Long warranties have helped too", stat("7 yrs", "GWM warranty · unlimited km", "GWM Australia", count=False))
c.at("That's how a market flips", P("street"))
chapters.append(c)

c = ch("ch07")
c.at(0, title("The Catch", "the risks nobody talks about", "be careful", "china"))
c.at("It's not sustainable", say("\"It's not sustainable. It's as simple as that.\" – Sam Venn, BDO", "NOT SUSTAINABLE", 92))
c.at("well over 150 car makers operate in China", stat("150+", "car makers in China – set to shrink", "BDO", count=False))
c.at("The dealer numbers show why", bars("New cars sold per dealer, per month · early 2026", [["Toyota", 72], ["BYD", 48], ["Geely", 7, "red"], ["JAC", 3, "red"],
     ["Deepal", 2, "red"]], None, "BDO"))
c.at("Even the boss of one Chinese brand", P("dealer"))
c.at("Then there's resale value", bars("Value kept after 2 years", [["Toyota RAV4", 88], ["BYD Atto 3", 54, "red"]], None, "Pickles / Datium · 2025", suffix="%"))
c.at("parts and approved repairers", P("ship"))
c.at("It means you need to choose the brand", say("Choose the brand – not just the deal.", "BRAND", 120))
c.at("There's also a bigger-picture question", P("china"))
c.at("Australia would not follow the United States", say("Australia won't ban Chinese cars from military sites – Oct 2026", "WON'T BAN", 95))
chapters.append(c)

c = ch("ch08")
c.at(0, P("jp_cars"))
c.at("Toyota insists it's not in decline", say("\"We don't plan to be declining. We plan to continue to grow.\" – John Pappas, Toyota", "GROW", 88))
c.at("And the RAV4 is bouncing back", stat("4,624", "Toyota RAV4 · Sept 2026 (+81%)", "VFACTS"))
c.at("it's offering a rare four-thousand-dollar bonus", photo("m_hilux", 3, "in", cap="Toyota HiLux|$4,000 bonus"))
c.at("Others are cutting prices hard", bars("Price cuts from the old guard", [["Kia Tasman", 15000], ["Ford Ranger Hybrid", 10000], ["Mazda CX-70", 8051]], None,
     "CarsGuide / CarExpert", prefix="up to $"))
c.at("there are now nearly seventy car brands", stat("~70", "car brands in Australia", "Toyota Australia", count=False))
chapters.append(c)

c = ch("ch09")
c.at(0, title("What It Means for You", "buyers & owners", "advice", "money"))
c.at("If you're buying, it's good news", P("money"))
c.at("they need your sale more than they did", say("\"They need your sale more than they did…\" – John Cadogan", "YOUR SALE", 95))
c.at("If you're considering a Chinese car", P("dealer"))
questions(c, ["How long in Australia?", "Dealers near you?", "Parts – how fast?", "Value in 3–5 years?"],
          ["How long has it been in Australia", "How many dealers and service centres", "How fast can it get parts", "And what will the car be worth"])
c.at("It's also worth checking whether the brand has a track record", P("money"))
c.at("And if you own a Japanese or Korean car", photo("m_xtrail", 1, "in"))
chapters.append(c)

c = ch("ch10", 2.5)
c.at(0, say("Did Chinese cars just take over Australia?", "TAKE OVER", 115))
c.at("By country of manufacture, yes", P("ship"))
c.at("BYD is now second only to Toyota", P("cn_cars"))
c.at("The Australian Automotive Dealer Association has forecast", stat("58%", "of cars on Australian roads could be Chinese-made by 2035", "AADA forecast", count=False))
c.at("But this takeover will also have casualties", P("street"))
c.at("If this helped", cta("Like · Subscribe · Share", "with someone shopping for a car"))
c.at("Chinese, Japanese, or something else", cta("Chinese or Japanese?", "comments"))
c.at("is Toyota the next Holden", title("Is Toyota the Next Holden?", "next video", "coming up", "jp_cars"))
chapters.append(c)

CTX = ["ship", "ship", "cn_cars", "street", "jp_cars", "cn_cars", "dealer", "china", "jp_cars", "money", "ship"]
print(A.finish(chapters, "AUS17_China_Takeover.mp4", CTX, subtitles="AUS17.ass"))
