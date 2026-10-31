#!/usr/bin/env python3
"""AUS13 Car brands that may not survive 2027 in Australia: full edit, shots anchored to phrases.
    python3 build_aus13.py <narration_dir> > episode.json   (run from the work folder)
The script says clearly that no brand has announced an exit; graphics keep that framing.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "engine"))
import aus_kit as A
from aus_kit import P, photo, stat, bars, say, cta, title, ch, questions

PHOTOS = {
    "dealer": ["ai:ai_closing_dealer", "h_closed"],
    "parts": ["ai:ai_parts_wait", "h_parts"],
    "workshop": ["h_workshop2"],
    "used": ["ai:ai_used_yard", "h_used"],
    "docs": ["h_docs", "h_keys"],
    "chinese": ["m_byd", "m_leapmotor"],
    "jeep": ["m_wrangler", "m_compass", "m_gladiator", "m_avenger", "m_grand_cherokee"],
    "japan": ["m_outlander", "m_forester", "m_outback", "m_xtrail", "m_cx5", "m_triton"],
}
CLIPS = json.load(open(os.path.join(HERE, "clips.json")))
GENERIC = CLIPS.pop("_generic", [])
FALLBACK = {"dealer": ["used"], "parts": ["workshop"], "workshop": ["parts"], "used": ["dealer"], "docs": ["dealer"],
            "chinese": ["dealer"], "jeep": ["used"], "japan": ["dealer"]}
RES = ["m_wrangler/1", "m_wrangler/3", "m_compass/1", "m_gladiator/1", "m_avenger/1", "m_grand_cherokee/1", "m_grand_cherokee/3",
       "m_peugeot_3008/1", "m_peugeot_5008/1", "m_peugeot_5008/3", "m_partner/3", "m_citroen/1", "m_citroen/3", "m_holden/1",
       "m_holden/3", "m_jaguar_car/1", "m_jaguar_car/3", "m_jaguar_car/5", "m_alfa/1", "m_alfa/3", "m_outlander/1", "m_pajero/1",
       "m_forester/1", "m_outback/1", "m_xtrail/1", "m_patrol/1", "m_cx5/1", "m_cx6e/1", "m_leapmotor/1", "m_byd/1"]
A.setup(sys.argv[1], os.path.join(HERE, "skip.json"), PHOTOS, CLIPS, GENERIC, FALLBACK,
        ["dealer", "used", "japan", "chinese", "docs"], reserved=RES)
A.CLIP_TARGET = 0.55   # channel request (31/10): more clips
A.MAX_HOLD, A.KEEP = 11.0, 7.5
chapters = []

c = ch("ch00_hook", 0.6)
c.at(0, stat("30,408", "Jeeps sold in Australia in 2014", "VFACTS"))
c.at("In the first half of 2026, Jeep sold just 365", stat("365", "Jeeps sold · first half of 2026", "CarExpert", red=True))
c.at("In June, it sold twenty-eight", photo("m_wrangler", 1, "in", cap="Jeep|28 sales in June 2026"))
c.at("Peugeot's Australian distributor", photo("m_peugeot_3008", 1, "left", cap="Peugeot|importer Inchcape walking away"))
c.at("Jaguar sold zero new cars", photo("m_jaguar_car", 1, "right", cap="Jaguar|0 new cars sold · Sept 2026"))
c.at("Alfa Romeo is going backwards", photo("m_alfa", 1, "in", cap="Alfa Romeo|sales going backwards"))
c.at("Mitsubishi, Subaru and Nissan", bars("Sales · first half 2026 vs 2025", [["Mitsubishi", -25.7, "red"], ["Subaru", -25.6, "red"]], None,
     "CarExpert", suffix="%"))
c.at("Australia now has around seventy car brands", stat("~70", "brands fighting for ~1.2 million sales a year", None, count=False))
c.at("has already warned that more brands will leave", P("dealer"))
c.at("So in this video", title("Brands That May Not Survive 2027", "real 2026 sales data", "Australia", "dealer"))
c.at("because none of them has announced", say("None has announced it's leaving.", "NONE", 130))
questions(c, ["Warranty", "Servicing", "Parts", "Resale value"], ["your warranty", "servicing", "parts and resale", "resale value if your brand"])
c.at("there are things you should do now", P("docs"))
chapters.append(c)

c = ch("ch01")
c.at(0, say("Why are so many brands struggling at once?", "STRUGGLING", 110))
c.at("Reason one: the Chinese brands", photo("m_byd", 1, "in", cap="BYD|+124% · first half 2026"))
c.at("BYD sales rose 124 per cent", bars("Sales growth · first half 2026", [["BYD", 124], ["Chery", 77], ["Tesla", 67], ["GWM", 20]], None,
     "CarExpert", prefix="+", suffix="%"))
c.at("In September 2026, Geely was up 870", bars("Sept 2026 vs Sept 2025", [["Geely", 870], ["Omoda Jaecoo", 344]], None, "VFACTS", prefix="+", suffix="%"))
c.at("Every one of those sales", P("chinese"))
c.at("Reason two: the government's emissions rules", say("Reason 2 · emissions penalties", "PENALTIES", 120))
c.at("Mazda's estimated liability", bars("Estimated NVES liability · first 6 months ($m)", [["Mazda", 25.4, "red"], ["Nissan", 10.7, "red"],
     ["Subaru", 7.0, "red"], ["Hyundai", 4.2, "red"]], None, "Estimates via CarExpert", prefix="$", suffix="m"))
c.at("And the targets get much tougher", P("japan"))
c.at("Reason three: the sheer number", stat("~70", "brands · ~1.2 million sales", None, count=False))
c.at("Even Toyota", stat("-21.4%", "Toyota · first half 2026 (95,141 sales)", "CarExpert", red=True))
c.at("Suzuki was down almost twenty-one", bars("First half 2026 vs 2025", [["Suzuki", -21], ["Porsche", -30], ["Cupra", -32], ["Maserati", -33]],
     None, "CarExpert", suffix="%"))
c.at("When the market leader is down by a fifth", P("dealer"))
c.at("Back in late 2024", say("\"I think we will see a number leave…\" – James Voortman, AADA", "LEAVE", 92))
c.at("how many important brands are going to leave", P("used"))
questions(c, ["Infiniti", "Chrysler", "Citroen", "Opel"], ["Infiniti", "Chrysler", "Citroen and", "Opel"])
c.at("Before that, of course, there was Holden", photo("m_holden", 1, "in", cap="Holden|retired in 2020"))
c.at("Brands leaving Australia isn't a theory", P("dealer"))
c.at("None of the brands in this video has announced", say("No brand here has announced an exit.", "NO BRAND", 115))
c.at("It's a list of brands under real pressure", P("docs"))
chapters.append(c)

c = ch("ch02")
c.at(0, title("#1 Jeep", "the most trouble on paper", "under pressure", "jeep"))
c.at("In 2014, Jeep sold 30,408", bars("Jeep sales in Australia", [["2014", 30408], ["2024", 2456, "red"], ["2025", 1682, "red"]], None,
     "VFACTS / CarExpert"))
c.at("CarExpert reported just 365 sales", stat("365", "first half 2026 · -66% · 28 in June", "CarExpert", red=True))
c.at("In September 2026, it sold sixteen", stat("16", "Jeeps sold · September 2026", "VFACTS", red=True))
c.at("The dealer network has shrunk too", bars("Jeep retailers", [["Peak", 70], ["2026", 44, "red"]], None, "CarExpert"))
c.at("some Jeep dealers sought legal advice", P("docs"))
c.at("Jeep's current Australian line-up", photo("m_avenger", 1, "in", cap="Jeep Avenger|electric SUV"))
c.at("the Compass, the Wrangler and the Gladiator", photo("m_gladiator", 1, "left", cap="Jeep Gladiator|ute"))
c.at("The Grand Cherokee, which sold 16,582", photo("m_grand_cherokee", 1, "right", cap="Jeep Grand Cherokee|16,582 (2014) → 645 (2024)"))
c.at("Prices are part of the problem", A.price("Jeep Wrangler 4-door", "~$37,000", "$75,950", "2014", "2025 (+ ORC)", None, "CarSauce"))
c.at("And Jeep paused the Grand Cherokee", photo("m_grand_cherokee", 3, "in", cap="Grand Cherokee|paused March 2025"))
c.at("But Jeep insists it's staying", say("\"…we're committed to right-hand drive [and] Australia.\" – Matt Nyquist, Jeep", "COMMITTED", 88))
c.at("Jeep says a new Compass is due", photo("m_compass", 1, "left", cap="Jeep Compass|new model due"))
c.at("Nyquist did acknowledge that plans can change", P("jeep"))
chapters.append(c)

c = ch("ch03")
c.at(0, P("jeep"))
c.at("Today, many Australians under thirty", P("dealer"))
c.at("Number two: Peugeot", title("#2 Peugeot", "importer walking away", "under pressure", "dealer"))
c.at("Peugeot's best year in Australia", bars("Peugeot sales in Australia", [["2007", 8807], ["2025", 1350, "red"]], None, "VFACTS / CarExpert"))
c.at("CarExpert reported 427 sales", stat("427", "first half 2026 · -41% · 89 in September", "CarExpert", red=True))
c.at("And look at what Peugeot is actually selling", photo("m_partner", 3, "in", cap="Peugeot Partner|~43% of deliveries to May"))
c.at("Among Stellantis brands in Australia", bars("Stellantis brands · 2026 to May", [["Ram", 1257], ["Fiat", 745], ["Peugeot", 373, "red"]], None, "CarExpert"))
c.at("Then, in July 2026, came the big blow", say("July 2026: Inchcape to end Peugeot partnership", "INCHCAPE", 105))
c.at("Inchcape had already dropped", photo("m_citroen", 1, "left", cap="Citroen|dropped by Inchcape in 2024"))
c.at("Stellantis says Peugeot is staying", say("\"Peugeot has a strong future in Australia…\" – Stellantis", "STRONG FUTURE", 92))
c.at("But it hasn't said who will actually distribute", P("docs"))
c.at("In the meantime, Inchcape will keep selling", P("workshop"))
c.at("And Peugeot has slashed prices", A.price("Peugeot 5008 GT Premium Hybrid", "$69,990", "$59,990", "before", "drive-away · July 2026", "-$10,000", "The Beep"))
c.at("from $69,990 to $59,990", photo("m_peugeot_5008", 1, "in", cap="Peugeot 5008|$10,000 price cut"))
chapters.append(c)

c = ch("ch04")
c.at(0, title("#3 Jaguar", "zero new cars", "a deliberate gamble", "used"))
c.at("Jaguar stopped selling new petrol cars", photo("m_jaguar_car", 3, "in", cap="Jaguar|no new petrol cars from 31 Dec 2025"))
c.at("That's why it sold zero new cars", stat("0", "new Jaguars sold · September 2026", "VFACTS", red=True, count=False))
c.at("The new electric Jaguars are expected to cost", stat("~$300,000", "expected price of new electric Jaguars", "Man of Many", count=False))
c.at("Jaguar's local retailers are still servicing", P("workshop"))
c.at("If you own a Jaguar", photo("m_jaguar_car", 5, "left", cap="Existing Jaguars|still supported locally"))
c.at("that can make selling a used Jaguar harder", P("used"))
c.at("Number four: Alfa Romeo", title("#4 Alfa Romeo", "a tiny number", "under pressure", "used"))
c.at("Alfa Romeo sold just twenty-one", stat("21", "Alfa Romeos sold · September 2026", "VFACTS", red=True))
c.at("By May, its sales were down almost forty-seven", photo("m_alfa", 3, "in", cap="Alfa Romeo|-47% to May 2026"))
c.at("when a brand only has a couple of models", P("dealer"))
c.at("Like Jeep and Peugeot, it's part of Stellantis", say("Jeep · Peugeot · Alfa Romeo = Stellantis", "STELLANTIS", 105))
chapters.append(c)

c = ch("ch05")
c.at(0, P("japan"))
c.at("Do you own a car from one of these brands", cta("Own one of these brands?", "dealer closed? parts trouble? comments"))
c.at("hit subscribe", cta("Subscribe", "what's changing for Aussie drivers in 2027"))
chapters.append(c)

c = ch("ch06")
c.at(0, title("The Japanese Brands", "not leaving – but under pressure", "2027", "japan"))
c.at("They sell tens of thousands of cars", P("dealer"))
c.at("Mitsubishi: 24,802 sales", photo("m_outlander", 1, "in", cap="Mitsubishi|24,802 · -25.7% · first half 2026"))
c.at("In September 2026, it was down 41.5", stat("-41.5%", "Mitsubishi · September 2026", "VFACTS", red=True))
c.at("The good news for Mitsubishi is the all-new Pajero", photo("m_pajero", 1, "left", cap="Mitsubishi Pajero|from $68,490 + ORC · Dec 2026"))
c.at("Subaru: 14,817 sales", photo("m_forester", 1, "in", cap="Subaru|14,817 · -25.6% · first half 2026"))
c.at("In September, down 42.6", photo("m_outback", 1, "right", cap="Subaru|-42.6% · September 2026"))
c.at("Nissan: 13,854 sales", photo("m_xtrail", 1, "in", cap="Nissan|13,854 · first half 2026"))
c.at("2026 is the low point", say("\"2026 is the low point.\" – Steve Milette, Nissan", "LOW POINT", 105))
c.at("and the new V6 Patrol", photo("m_patrol", 1, "left", cap="Nissan Patrol|new V6"))
c.at("And Mazda: the biggest estimated", photo("m_cx5", 1, "in", cap="Mazda|~$25.4m estimated liability · 6 months"))
c.at("including the CX-6e electric SUV", photo("m_cx6e", 1, "right", cap="Mazda CX-6e|electric SUV"))
c.at("Why does this matter if you own", P("used"))
questions(c, ["Higher prices", "Models cut", "Big discounts → lower resale"],
          ["It might raise prices", "It might cut slow-selling models", "Or it might slash prices"])
chapters.append(c)

c = ch("ch07")
c.at(0, title("Stellantis", "the group behind 3 of them", "the bigger picture", "jeep"))
c.at("Stellantis owns Jeep, Peugeot, Alfa Romeo and Fiat", P("jeep"))
c.at("Leapmotor sales were up more than 112", photo("m_leapmotor", 1, "in", cap="Leapmotor|+112% (CarsGuide, June 2026)"))
c.at("does Jeep have a long-term future", say("\"Does Jeep have a long-term future in Australia?\" – Stephen Ottley, CarsGuide", "FUTURE", 85))
c.at("General Motors said it was committed to Holden", photo("m_holden", 3, "left", cap="Holden|'committed' – until 2020"))
c.at("Stellantis says it's investing heavily", bars("Stellantis global plan", [["New vehicles", 60], ["Updated models", 50]], None, "Stellantis"))
c.at("But the numbers make it easy to see", P("dealer"))
c.at("So who's filling the gap", P("chinese"))
c.at("CarExpert reported Leapmotor up more than 150", stat("+150%", "Leapmotor · first half 2026 (779 sales)", "CarExpert"))
c.at("Denza had passed 1,600 sales", stat("1,600+", "Denza sales since arriving", "CarsGuide"))
c.at("And more Chinese brands keep arriving", P("chinese"))
c.at("The market isn't shrinking", say("The market isn't shrinking – the top is changing.", "CHANGING", 105))
chapters.append(c)

c = ch("ch08")
c.at(0, title("If Your Brand Leaves", "what happens to you", "owners", "dealer"))
c.at("First, your rights", say("Australian Consumer Law: parts & repairs for a reasonable time", "REASONABLE", 92))
c.at("That doesn't disappear", P("docs"))
c.at("When General Motors announced the end of Holden", say("Holden: parts and servicing \"at least the next 10 years\"", "10 YEARS", 100))
c.at("When Citroen stopped selling new cars", photo("m_citroen", 3, "in", cap="Citroen|servicing + warranty continued after Nov 2024"))
c.at("What about finance and insurance", P("docs"))
c.at("But insurers price policies partly on repair costs", P("parts"))
c.at("And if your car is on a novated lease", P("docs"))
c.at("If the car's market value falls", say("Market value < residual?", "RESIDUAL", 130))
c.at("But here's the reality", P("dealer"))
c.at("Some parts can take longer to arrive", P("parts"))
c.at("And independent mechanics", P("workshop"))
c.at("And the biggest hit is usually resale value", say("Biggest hit: resale value.", "RESALE", 130))
c.at("used buyers get nervous", P("used"))
chapters.append(c)

c = ch("ch09")
c.at(0, title("Own One? Do This Now", "6 steps", "owners", "docs"))
c.at("Step one: don't panic-sell", say("1 · Don't panic-sell", "1", 135))
c.at("Step two: check your warranty", say("2 · Warranty & service plan", "2", 125))
c.at("Keep every service record", P("docs"))
c.at("Step three: find your nearest service centres", say("3 · Find more than one service centre", "3", 115))
c.at("whether a good independent mechanic", P("workshop"))
c.at("Step four: keep up with recalls", say("4 · Recalls · productsafety.gov.au", "4", 115))
c.at("Step five: think about common parts", say("5 · Common parts", "5", 135))
c.at("brake pads, filters and windscreens", P("parts"))
c.at("Step six: if you're planning to sell", say("6 · Watch the market", "6", 135))
c.at("with your service history ready", P("used"))
c.at("And if you're buying a new car from a struggling brand", P("dealer"))
questions(c, ["Who backs the warranty?", "Nearest service centre?", "How fast are parts?"],
          ["who stands behind the warranty", "where is the nearest service centre", "how fast can they get common parts"])
c.at("Then factor a lower resale value", P("used"))
chapters.append(c)

c = ch("ch10", 2.5)
c.at(0, title("5 Warning Signs", "for any brand in 2027", "watch list", "dealer"))
questions(c, ["Sales collapsing", "Dealers closing", "Importer change", "Range shrinking", "Endless discounts"],
          ["sales collapsing", "dealers closing", "a change of importer", "the model range shrinking", "huge, ongoing discounts"])
c.at("One warning sign on its own", say("3 or 4 together = pay attention", "PAY ATTENTION", 110))
c.at("So, which car brands might not survive", P("used"))
c.at("On the numbers, Jeep and Peugeot", photo("m_wrangler", 3, "in", cap="Jeep|-90%+ from its peak"))
c.at("Peugeot with its importer walking away", photo("m_peugeot_5008", 3, "left", cap="Peugeot|importer leaving"))
c.at("Jaguar has deliberately stopped", P("used"))
c.at("And while Mitsubishi, Subaru, Nissan and Mazda", P("japan"))
c.at("But remember: none of these brands has announced", say("No exit announced – several say they're committed.", "COMMITTED", 100))
c.at("history tells us that not all of them", P("dealer"))
c.at("If this helped", cta("Like · Subscribe · Share", "with someone who owns one of these cars"))
c.at("which brand do you think won't make it", cta("Which brand won't make it?", "comments"))
chapters.append(c)

CTX = ["dealer", "chinese", "jeep", "dealer", "used", "japan", "japan", "chinese", "docs", "docs", "dealer"]
print(A.finish(chapters, "AUS13_Brands_2027.mp4", CTX, subtitles="AUS13.ass"))
