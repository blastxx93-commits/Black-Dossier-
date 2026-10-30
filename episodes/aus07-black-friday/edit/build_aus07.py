#!/usr/bin/env python3
"""AUS07 Black Friday car deals (Nov 2026): full edit, every shot anchored to the phrase it illustrates.
Run from the episode work folder (a/ = assets of aus07-black-friday, audio/, sfx/, trilha.wav):
    python3 build_aus07.py <narration_dir> > episode.json
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "engine"))
import aus_kit as A
from aus_kit import P, photo, stat, bars, say, cta, title, ch, questions

PHOTOS = {
    "sale": ["ai:ai_bf_showroom", "h_bf_sale", "h_shopping"],
    "dealer": ["ai:ai_salesman_pitch", "h_dealer", "h_showroom", "h_salesman"],
    "finance": ["h_contract", "h_calc", "h_card"],
    "money": ["h_money", "h_calc"],
    "compare": ["ai:ai_couple_compare", "h_laptop"],
    "demo": ["ai:ai_demo_car", "h_odometer"],
    "yard": ["ai:ai_delivery_yard", "h_dealer"],
    "trade": ["ai:ai_trade_in"],
    "keys": ["ai:ai_new_car_keys", "h_keys"],
    "ev": ["ai:ai_ev_charger_home", "h_ev"],
    "fuel": ["h_fuel"], "calendar": ["h_calendar"], "traffic": ["h_road", "h_family"],
    "chinese": ["m_jolion", "m_h6", "m_tiggo8", "m_tiggo9", "m_tiggo4", "m_geely_ex5", "m_jaecoo", "m_leapmotor"],
    "evcars": ["m_mg4", "m_inster", "m_kona_ev", "m_leapmotor"],
}
CLIPS = json.load(open(os.path.join(HERE, "clips.json")))
GENERIC = CLIPS.pop("_generic", [])
FALLBACK = {"sale": ["dealer"], "dealer": ["yard", "keys"], "finance": ["money", "compare"], "money": ["finance"],
            "compare": ["finance"], "demo": ["yard"], "yard": ["dealer"], "trade": ["dealer"], "keys": ["dealer"],
            "ev": ["evcars"], "fuel": ["traffic"], "calendar": ["sale"], "traffic": ["yard"], "chinese": ["yard"],
            "evcars": ["ev"]}
RES = ["m_jolion/1", "m_jolion/4", "m_h6/1", "m_cannon/1", "m_tiggo8/1", "m_tiggo9/1", "m_tiggo9/3", "m_geely_ex5/1",
       "m_glc/1", "m_glc/3", "m_kodiaq/1", "m_superb/3", "m_jaecoo/2", "m_jaecoo/3", "m_vitara/3", "m_jimny/1", "m_dmax/1",
       "m_cx60/3", "m_kona_ev/1", "m_inster/1", "m_mg4/1", "m_leapmotor/2", "m_dmax/3", "m_superb/1"]
A.setup(sys.argv[1], os.path.join(HERE, "skip.json"), PHOTOS, CLIPS, GENERIC, FALLBACK,
        ["traffic", "dealer", "yard", "sale", "finance", "chinese", "money", "keys"], reserved=RES)
chapters = []

# ---------------------------------------------------------------- hook
c = ch("ch00_hook", 0.6)
c.at(0, stat("$4.5 BILLION", "spent by Australians on Black Friday", "Finder estimate", count=False))
c.at("this year, Black Friday lands on the 27th", P("calendar", cap="Black Friday 27 Nov|Cyber Monday 30 Nov"))
c.at("For years, Black Friday was about TVs", P("sale"))
c.at("Car brands have jumped in", P("dealer"))
c.at("Last November, Suzuki, Omoda Jaecoo", P("chinese"))
c.at("cashback, free servicing, cheap finance", P("money"))
c.at("But here's the problem", say("But here's the problem…", "PROBLEM", 140))
c.at("was really just a demo clearance", P("demo"))
c.at("deposits of up to thirty-five per cent", stat("35%", "deposit on some \"cheap\" finance deals", "Savvy · 2025", red=True))
c.at("So in this video", title("Black Friday Car Deals 2026", "real deals · real traps", "Australia", "sale"))
questions(c, ["What's on offer now", "Why 2026 could be bigger", "The traps", "Real deal vs fake"],
          ["what car deals are on the table", "why 2026 could be the biggest", "the traps that cost", "exactly how to tell"])
c.at("Because a car isn't a toaster", say("A car isn't a toaster.", "TOASTER", 140))
c.at("you could pay for it for the next five years", P("finance"))
chapters.append(c)

# ---------------------------------------------------------------- what happened
c = ch("ch01")
c.at(0, P("compare"))
c.at("most car brands haven't announced", say("2026 deals: not announced yet.", "NOT ANNOUNCED", 120))
c.at("So I'm not going to invent offers", P("dealer"))
c.at("Let's start with 2025", title("Black Friday 2025", "what brands offered", "last year", "sale"))
c.at("Suzuki ran a short Black Friday sale", photo("m_vitara", 3, "in", cap="Suzuki 2025|$1,000 cashback · 21–23 Nov"))
c.at("Omoda Jaecoo offered two thousand", photo("m_jaecoo", 2, "left", cap="Jaecoo J7|$2,000 cashback + 3 yrs servicing"))
c.at("with the J7 starting from $32,990", photo("m_jaecoo", 3, "right", cap="Jaecoo J7|from $32,990 drive-away"))
c.at("Geely offered gift cards", photo("m_geely_ex5", 1, "in", cap="Geely EX5|gift card + charging cable"))
c.at("Chery offered two thousand dollars off", P("chinese"))
c.at("Isuzu advertised drive-away discounts", photo("m_dmax", 1, "left", cap="Isuzu D-Max & MU-X|$5,000–$8,000 off"))
c.at("And the year before, in 2024", title("Black Friday 2024", "even bigger on slow sellers", "2 years ago", "yard"))
c.at("Skoda took ten thousand dollars off", photo("m_superb", 3, "in", cap="Skoda Superb|$10,000 off · last 135 cars"))
c.at("Mazda cut nearly ten thousand", photo("m_cx60", 3, "right", cap="Mazda CX-60|nearly $10,000 off"))
c.at("BYD took three thousand dollars off", P("ev", cap="BYD 2024|$3,000 off + wall charger"))
c.at("Suzuki offered ten per cent off", photo("m_jimny", 1, "left", cap="Suzuki 2024|10% off · stock only"))
c.at("Notice something", say("Notice something?", "NOTICE", 150))
c.at("Most of those deals came from Chinese brands", P("chinese"))
questions(c, ["Cashback", "Gift cards", "Free servicing", "Finance deals"],
          ["They were cashback", "gift cards, free", "free servicing or", "finance deals"])
chapters.append(c)

# ---------------------------------------------------------------- why bigger
c = ch("ch02")
c.at(0, title("Why 2026 Could Be Bigger", "4 reasons", "the market", "yard"))
c.at("Reason one: competition", say("1 · Competition", "1", 140))
c.at("around seventy car brands", stat("~70", "brands fighting for ~1.2M sales a year", "AADA review · 2026", count=False))
c.at("New Chinese brands keep arriving", P("chinese"))
c.at("In September 2026, BYD sold 8,191", stat("8,191", "BYD sales · Sept 2026 – #2 brand", "FCAI / EVC"))
c.at("GWM is pushing towards the top five", photo("m_jolion", 1, "in"))
c.at("everyone else has to sharpen their pencil", P("dealer"))
c.at("Reason two: the government's New Vehicle Efficiency", say("2 · Emissions penalties (NVES)", "2", 120))
c.at("In the first six months alone", bars("NVES liability · Jul–Dec 2025", [["Mazda", 25.4, "red"], ["Nissan", 10.7, "red"],
     ["Subaru", 7.0, "red"], ["Hyundai", 4.2, "red"]], None, "NRMA · Feb 2026", prefix="$", suffix="M"))
c.at("Meanwhile, BYD, Toyota and Tesla", P("ev"))
c.at("discounting is the fastest way to do it", P("yard"))
c.at("Hyundai, for example, cut up to $13,857", photo("m_kona_ev", 1, "in", cap="Hyundai Kona Electric|up to $13,857 off"))
c.at("Clean Energy Finance Corporation committed", stat("$60M", "CEFC to Hyundai Capital – cheaper EV loans", "CarsGuide · Feb 2026", count=False))
c.at("the cheap end of the EV market has exploded", photo("m_mg4", 1, "left"))
c.at("seven electric cars available for under forty", stat("7", "EVs under $40,000 drive-away", "CarsGuide · Feb 2026"))
c.at("the Leapmotor B10 and the Hyundai Inster", photo("m_inster", 1, "right"))
c.at("Reason three: fuel", say("3 · Fuel prices", "3", 140))
c.at("more buyers are looking at hybrids", P("fuel"))
c.at("fuel cards offered as a sweetener", P("fuel"))
c.at("In 2025, battery electric cars made up", bars("Battery EV share of new car sales", [["2025", 8.3], ["Sept 2026", 24.2]],
     None, "CarsGuide · FCAI / EVC", suffix="%"))
c.at("And reason four: the calendar", say("4 · The calendar", "4", 140))
c.at("every unsold 2026-built car becomes", P("yard", cap="1 January|2026-built cars look a year older"))
c.at("Dealers want those cars gone", P("dealer"))
chapters.append(c)

# ---------------------------------------------------------------- right now
c = ch("ch03")
c.at(0, title("On Offer Right Now", "October 2026 prices", "CarsGuide", "dealer"))
c.at("GWM was celebrating eighteen years", photo("m_jolion", 4, "in", cap="Haval Jolion Premium|$23,990 drive-away (-$3,000)"))
c.at("The Haval H6 hybrid Lux", photo("m_h6", 1, "left", cap="Haval H6 hybrid Lux|$37,990 (-$3,000)"))
c.at("the Cannon Alpha diesel Ultra", photo("m_cannon", 1, "right", cap="GWM Cannon Alpha Ultra|$54,990 (-$4,000)"))
c.at("Chery offered three thousand dollars cashback", photo("m_tiggo8", 1, "in", cap="Chery Tiggo 8 PHEV|$42,990 drive-away"))
c.at("the seven-seat Tiggo 9", photo("m_tiggo9", 1, "left", cap="Chery Tiggo 9 PHEV|$49,990 drive-away"))
c.at("fuel cards worth up to two thousand", P("fuel"))
c.at("Geely offered six per cent off", P("chinese", cap="Geely|6% off · novated lease only"))
c.at("At the premium end, Mercedes-Benz", A.price("Mercedes-Benz GLC 200", "~$89,000", "$79,990", "before on-roads", "drive-away",
     None, "CarsGuide · Oct 2026"))
c.at("as long as you order by the 30th", photo("m_glc", 1, "in"))
c.at("Skoda was offering the Kodiaq", photo("m_kodiaq", 1, "left", cap="Skoda Kodiaq mild hybrid|$49,990 drive-away"))
c.at("Now, these aren't Black Friday deals", say("These aren't Black Friday deals.", "AREN'T", 125))
c.at("they show you the starting point", P("compare"))
c.at("that's not a Black Friday deal", say("Same price = not a deal.", "NOT A DEAL", 130))
chapters.append(c)

# ---------------------------------------------------------------- mid CTA
c = ch("ch04")
c.at(0, P("dealer"))
c.at("tell me in the comments which car", cta("Which car are you after?", "Tell me in the comments"))
c.at("hit subscribe", cta("Subscribe", "Honest Aussie car news"))
chapters.append(c)

# ---------------------------------------------------------------- traps 1-2
c = ch("ch05")
c.at(0, title("The Traps", "don't get caught", "6 traps", "sale"))
c.at("trap number one is the oldest trick", say("Trap 1 · The fake \"was\" price", "TRAP 1", 115))
c.at("The ACCC watches Black Friday closely", P("sale"))
c.at("totalling $59,400", stat("$59,400", "ACCC fines · \"sitewide\" Black Friday ads (2024 sales)", "ACCC", red=True))
c.at("Those weren't car companies", P("sale"))
c.at("A dealer might compare the drive-away price", P("dealer"))
c.at("write down the drive-away price", P("compare"))
c.at("That's your real saving", say("Today's price → Black Friday price = real saving", "REAL SAVING", 95))
c.at("There's a big difference between a", say("Drive-away ≠ before on-road costs", "DRIVE-AWAY", 115))
questions(c, ["Stamp duty", "Registration", "CTP insurance", "Dealer charges"],
          ["stamp duty", "registration, compulsory", "compulsory third party", "dealer charges"])
c.at("Always compare drive-away with drive-away", P("compare"))
c.at("you can still negotiate", P("dealer"))
c.at("A Black Friday price is the dealer's opening offer", say("It's an opening offer.", "OPENING", 140))
c.at("Trap number two", say("Trap 2 · Demo dressed up as a sale", "TRAP 2", 110))
c.at("some manufacturers may just be selling demo", say("\"…demo, runout or plate clearance models.\" – Savvy", "DEMO", 95))
c.at("A demo can be a great buy", P("demo"))
c.at("Always ask how many kilometres", P("demo"))
chapters.append(c)

# ---------------------------------------------------------------- finance
c = ch("ch06")
c.at(0, say("Trap 3 · Finance", "TRAP 3", 140))
c.at("finance from 1.99 per cent", stat("1.99%", "the headline rate…", "advertised finance", count=False))
questions(c, ["36–48 month terms", "Up to 35% deposit", "Balloon payment"],
          ["short terms of thirty-six", "deposits of up to thirty-five", "a large balloon payment"])
c.at("On a fifty-thousand-dollar car", stat("$2,125", "a month on a $50,000 car (Savvy estimate)", "Savvy · 2025", red=True, count=False))
c.at("The devil is in the details", say("\"The devil is in the details.\"", "DETAILS", 130))
c.at("And there's another catch", P("finance"))
c.at("at or above ten per cent", stat("10%+", "the rate you may be offered instead", "Savvy", red=True, count=False))
c.at("let's do some simple maths", bars("$40,000 loan over 5 years – total repaid", [["7%", 47500], ["10%", 51000, "red"]],
     None, "calculated", prefix="$"))
c.at("That's around three and a half thousand dollars", stat("+$3,500", "extra – enough to wipe out the discount", None, red=True, count=False))
c.at("Get pre-approved for a car loan", P("compare"))
c.at("Always compare the comparison rate", say("Comparison rate, not headline rate.", "COMPARISON", 115))
c.at("work out the total amount", P("money"))
c.at("using buy now, pay later", P("finance"))
c.at("go easy on the other Black Friday sales", P("sale"))
chapters.append(c)

# ---------------------------------------------------------------- traps 4-6
c = ch("ch07")
c.at(0, say("Trap 4 · Sweeteners", "TRAP 4", 140))
c.at("Cashback, gift cards, fuel cards", P("money"))
c.at("Three years of free servicing on a Jaecoo J7", stat("~$900", "value of 3 yrs free servicing · Jaecoo J7", "CarExpert · 2025", count=False))
c.at("a fuel card or a gift card is not the same", P("fuel"))
c.at("BYD's Black Friday deal included a free wall charger", P("ev", cap="Free wall charger|installation not included"))
c.at("And some of these extras come with conditions", P("finance"))
c.at("always ask the dealer what the drive-away price would be", say("Price WITHOUT the extras?", "WITHOUT", 130))
c.at("Trap number five: the delivery deadline", say("Trap 5 · Delivery deadline", "TRAP 5", 120))
c.at("If the car you want isn't in stock", P("yard"))
c.at("Get the answer in writing", P("finance"))
c.at("And be careful with deposits", P("money"))
c.at("As we saw with the Cybertruck", say("A deposit is only as good as the paperwork.", "PAPERWORK", 105))
c.at("Trap number six", say("Trap 6 · Tied to a lender", "TRAP 6", 125))
c.at("three thousand dollars cashback on BYD models through Savvy", P("compare"))
c.at("a cheap car with an expensive loan isn't cheap", say("Cheap car + expensive loan ≠ cheap.", "≠ CHEAP", 115))
chapters.append(c)

# ---------------------------------------------------------------- EV FBT
c = ch("ch08")
c.at(0, P("ev"))
c.at("electric cars bought through a novated lease", P("evcars"))
c.at("currently $91,387", stat("$91,387", "EV FBT exemption cap (fuel-efficient LCT threshold)", "CarExpert · May 2026", count=False))
c.at("That's called the Electric Car Discount", P("ev"))
c.at("the government confirmed it's being wound back", P("calendar"))
c.at("The full exemption continues until", say("Full exemption until 31 March 2027", "31 MARCH 2027", 105))
c.at("only EVs costing $75,000 or less", stat("$75,000", "full exemption cap from 1 April 2027", "Federal government", red=True, count=False))
c.at("Existing leases are protected", P("evcars"))
c.at("plug-in hybrids already lost the exemption", P("chinese", cap="Plug-in hybrids|lost FBT exemption 1 Apr 2025"))
c.at("the timing matters more than any Black Friday sale", say("Timing beats any sale.", "TIMING", 140))
chapters.append(c)

# ---------------------------------------------------------------- checklist
c = ch("ch09")
c.at(0, title("The Checklist", "8 steps", "save this", "compare"))
c.at("Step one: decide on the car", say("1 · Pick the car first", "1", 130))
c.at("Black Friday is designed to make you buy on impulse", P("sale"))
c.at("Step two: record today's drive-away", say("2 · Today's price, in writing", "2", 125))
c.at("ask each one for the breakdown", P("dealer"))
c.at("Step three: get finance pre-approved", say("3 · Pre-approved finance", "3", 130))
c.at("Step four: when the deal drops", say("4 · Read the fine print", "4", 130))
c.at("Is it for new cars only", P("demo"))
c.at("Is it limited to stock on hand", P("yard"))
c.at("Step five: ask for the build date", say("5 · Ask the build date", "5", 130))
c.at("A car built in 2026 and sold in December", P("calendar"))
c.at("Step six: keep the trade-in separate", say("6 · Trade-in separate", "6", 130))
c.at("Get a written price for the new car first", P("trade"))
c.at("Step seven: check the boring stuff", say("7 · Servicing, warranty, recalls", "7", 115))
c.at("You can check recalls", P("compare"))
c.at("a sale price doesn't reduce your rights", say("Sale price ≠ fewer rights.", "RIGHTS", 135))
c.at("the discount doesn't change your right", P("keys"))
c.at("And step eight: be ready to walk away", say("8 · Be ready to walk away", "8", 125))
c.at("The end of December is often another big push", P("yard"))
chapters.append(c)

# ---------------------------------------------------------------- end
c = ch("ch10", 2.5)
c.at(0, P("dealer"))
c.at("The ones with emissions penalties to manage", P("yard"))
c.at("The Chinese brands fighting for market share", photo("m_tiggo9", 3, "left"))
c.at("any brand with a new model about to arrive", P("yard"))
c.at("are Black Friday car deals worth it", say("Worth it? They can be.", "CAN BE", 140))
c.at("That's a great setup for buyers", P("keys"))
c.at("But a Black Friday banner doesn't make a deal good", say("A banner doesn't make a deal.", "BANNER", 125))
c.at("The real saving is the difference", P("compare"))
c.at("If this video helped", cta("Like · Subscribe · Share", "with someone buying a car"))
questions(c, ["Which car do you want on sale?"], ["which car you're hoping"])
c.at("when the official 2026 deals land", title("See You Next Video", "real deals, checked", "Black Friday 2026", "sale"))
chapters.append(c)

CTX = ["sale", "dealer", "yard", "dealer", "dealer", "sale", "finance", "money", "ev", "compare", "dealer"]
print(A.finish(chapters, "AUS07_Black_Friday_Car_Deals.mp4", CTX, subtitles="AUS07.ass"))
