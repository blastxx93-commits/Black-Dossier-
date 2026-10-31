#!/usr/bin/env python3
"""AUS16 A road tax for every driver?: full edit, shots anchored to phrases.
    python3 build_aus16.py <narration_dir> > episode.json   (run from the work folder)
Political-adjacent topic: graphics show both sides; cost figures are labelled as illustrations.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "engine"))
import aus_kit as A
from aus_kit import P, photo, stat, bars, say, cta, title, ch, questions

PHOTOS = {
    "fuel": ["ai:ai_servo_fill", "h_fuel_pump", "h_servo"],
    "ev": ["h_ev_charge", "m_kona_ev"],
    "road": ["ai:ai_ute_rural", "h_rural_road", "h_highway", "ai:ai_outer_suburb"],
    "city": ["h_sydney", "h_traffic"],
    "gov": ["h_parliament"],
    "money": ["ai:ai_family_bills", "h_calc"],
    "gps": ["h_gps", "h_odometer"],
    "works": ["h_roadworks"],
    "nz": ["h_nz_road"],
    "uk": ["h_uk_traffic"],
}
CLIPS = json.load(open(os.path.join(HERE, "clips.json")))
GENERIC = CLIPS.pop("_generic", [])
FALLBACK = {"fuel": ["road"], "ev": ["city"], "road": ["city"], "city": ["road"], "gov": ["city"], "money": ["fuel"], "gps": ["road"],
            "works": ["road"], "nz": ["road"], "uk": ["city"]}
RES = ["m_model_y/1", "m_model_y/3", "m_model3/1", "m_model3/2", "m_model3/3", "m_ranger/1", "m_ranger/3", "m_corolla/1", "m_landcruiser/3",
       "m_polestar/1", "m_polestar/3", "m_atto3/1", "m_rav4/1", "m_rav4/3"]
A.setup(sys.argv[1], os.path.join(HERE, "skip.json"), PHOTOS, CLIPS, GENERIC, FALLBACK, ["road", "city", "fuel", "money", "gps"], reserved=RES)
A.CLIP_TARGET = 0.55
A.MAX_HOLD, A.KEEP = 13.0, 8.5
chapters = []

c = ch("ch00_hook", 0.6)
c.at(0, stat("53.7c", "fuel excise on every litre of petrol & diesel", "ATO / CarExpert", count=False))
c.at("Fill up a big ute", photo("m_ranger", 1, "in", cap="80 litres|~$43 of excise"))
c.at("Now imagine paying that", say("…and a tax on every kilometre?", "EVERY KILOMETRE", 105))
c.at("Tesla – the world's best-known electric car company", photo("m_model_y", 1, "left", cap="Tesla|wants petrol & diesel drivers to pay too"))
c.at("The Australian Electric Vehicle Association has proposed", P("ev"))
c.at("Polestar's Australian boss says", photo("m_polestar", 1, "right", cap="Polestar|road-user charge 'inevitable'"))
c.at("And New South Wales already has a law", stat("1 July 2027", "NSW EV road-user charge due to start", "NSW Government", count=False))
c.at("So in this video, I'll explain exactly", title("A Tax for Every Driver?", "who wants it · what it costs", "road-user charge", "road"))
questions(c, ["Corolla", "LandCruiser", "Tesla"], ["whether you drive a Corolla", "a LandCruiser", "or a Tesla"])
c.at("the way Australians pay for roads is about to change", P("city"))
chapters.append(c)

c = ch("ch01")
c.at(0, P("fuel"))
c.at("It went back up to around 53.7 cents", bars("Fuel excise per litre", [["Before the 2026 cut", 52.6], ["From 3 Aug 2026", 53.7]], None, "New Technology / ATO", suffix="c"))
c.at("During the 2026 fuel crisis", P("fuel"))
c.at("It's also worth knowing that fuel excise isn't a dedicated road fund", P("gov"))
c.at("Fuel excise raises roughly fifteen billion", stat("~$15 billion", "raised by fuel excise each year", "New Technology", count=False))
c.at("the average petrol or diesel driver pays about $1,400", stat("~$1,400", "excise paid per petrol/diesel driver a year", "ABC", count=False))
c.at("Electric cars don't use fuel", P("ev"))
c.at("electric cars made up 24.2 per cent", bars("New-car sales by fuel · Sept 2026", [["Electric", 24.2], ["Petrol", 23.9], ["Diesel", 23.1]], None, "VFACTS / CarExpert", suffix="%"))
c.at("The Tesla Model Y beat the Ford Ranger", photo("m_model_y", 3, "in", cap="Tesla Model Y|#1 in May, June & August 2026"))
c.at("As more people switch, the excise money shrinks", P("money"))
c.at("Fuel excise was designed for a different vehicle fleet", say("\"Fuel excise was designed for a different vehicle fleet…\" – Transport Australia", "DIFFERENT", 88))
c.at("So governments are looking for a replacement", P("gov"))
c.at("Australia wouldn't be the first to do this", P("nz"))
c.at("76 New Zealand dollars per thousand kilometres", bars("New Zealand road-user charges (NZ$ per 1,000 km)", [["Electric car", 76], ["Plug-in hybrid", 53]], None, "NZTA / Driven"))
c.at("would pay about $912 in an EV", P("nz"))
c.at("And in the United Kingdom", P("uk", cap="UK from April 2028|3p per mile EVs · 1.5p PHEVs"))
c.at("Drivers will estimate their mileage", P("gps"))
c.at("if you don't pay at the pump", say("Don't pay at the pump? Pay by the kilometre.", "KILOMETRE", 100))
chapters.append(c)

c = ch("ch02")
c.at(0, P("city"))
c.at("For the 2026-27 financial year, the rate is 3.095", bars("NSW road-user charge 2026-27", [["Battery EV / hydrogen", 3.095], ["Plug-in hybrid", 2.476]], None,
     "NSW Government", suffix="c/km"))
c.at("It's due to start on the 1st of July 2027", say("From 1 July 2027 – or at 30% EV sales", "30%", 105))
c.at("In the June 2026 quarter", bars("Share of national sales · June qtr 2026", [["Battery EVs", 21.0], ["EVs + plug-in hybrids", 31.6]], None, "New Technology", suffix="%"))
c.at("Drive 15,000 kilometres a year", stat("~$464", "a year · NSW EV at 15,000 km", "illustration", count=False))
c.at("But there's a big legal problem", say("High Court, Oct 2023: Victoria's EV charge = excise (4–3)", "HIGH COURT", 88))
c.at("The Victorian scheme was struck down", P("gov"))
c.at("As of September 2026, no EV road-user charge", stat("$0", "EV road-user charges being collected · Sept 2026", "New Technology", count=False))
c.at("Western Australia had also announced", P("road"))
chapters.append(c)

c = ch("ch03")
c.at(0, P("gov"))
c.at("an idea whose time has come", say("\"…an idea whose time has come.\" – Treasurer Jim Chalmers", "TIME HAS COME", 95))
c.at("double-tax", say("Focus on EVs – not \"double-tax\" petrol & diesel cars.", "DOUBLE-TAX", 100))
c.at("Then things slowed down", P("gov"))
c.at("It's got to be done right", say("\"It's got to be done right… and that includes timing.\" – Chris Bowen", "DONE RIGHT", 95))
c.at("CarExpert reported that a 2028 start had been planned", P("money"))
questions(c, ["Government: don't discourage EVs", "Greens: oppose an EV-only charge", "AAA: legislate it in the 2027 Budget"],
          ["Transport Minister Catherine King", "The Greens oppose", "And the Australian Automobile Association"])
c.at("So the federal position, for now", say("Coming eventually · mainly EVs · no date", "NO DATE", 110))
c.at("And remember, the government is also changing EV incentives", stat("$75,000", "Electric Car Discount cap from April 2027", "Federal government", count=False))
chapters.append(c)

c = ch("ch04")
c.at(0, title("Tesla's Twist", "charge everyone – keep excise", "the submission", "ev"))
c.at("Tesla Australia argued that a road-user charge", photo("m_model3", 1, "in", cap="Tesla Australia|submission to a federal inquiry"))
c.at("apply it universally to all vehicles", say("\"…apply it universally to all vehicles on the road, phased-in.\" – Tesla", "ALL VEHICLES", 85))
c.at("Here's the controversial part", say("Keep fuel excise too.", "TOO", 150))
c.at("That means drivers of newly registered petrol", P("fuel"))
c.at("acts as a financial penalty for decarbonising", say("\"…a financial penalty for decarbonising personal transport.\" – Tesla", "PENALTY", 88))
c.at("consumers remain largely inelastic", P("city"))
c.at("Of course, Tesla sells only electric cars", photo("m_model3", 2, "left", cap="Worth knowing|Tesla sells only EVs"))
chapters.append(c)

c = ch("ch05")
c.at(0, P("road"))
c.at("Tell me in the comments", cta("Everyone, EVs only – or nobody?", "tell me in the comments"))
c.at("hit subscribe", cta("Subscribe", "straight-talking car videos"))
chapters.append(c)

c = ch("ch06")
c.at(0, P("ev"))
c.at("the Australian Electric Vehicle Association", say("AEVA: road-user charge for EVs – plus excise for fuel cars", "PLUS EXCISE", 95))
c.at("Its version is based on weight and distance", stat("3c", "per tonne-kilometre · phased in over 10 years", "AEVA", count=False))
c.at("a 2.2-tonne diesel ute or electric SUV", stat("$858", "a year · 2.2-tonne ute or SUV · 13,000 km", "AEVA", count=False))
c.at("it's only fair that they pay the same", say("\"…it's only fair that they pay the same road user charge.\" – Dr Chris Jones, AEVA", "FAIR", 85))
c.at("We're not after a free ride", P("ev"))
c.at("Polestar agrees with the principle", photo("m_polestar", 3, "in", cap="Polestar Australia|weight-based charge for all"))
c.at("We don't have a congestion tax", say("\"We don't have a congestion tax in Australia.\" – Scott Maynard, Polestar", "CONGESTION", 92))
c.at("And it's not just electric car companies", P("city"))
questions(c, ["Car dealers (AADA): all vehicle types", "Motoring clubs (AAA): distance-based charge"],
          ["The Australian Automotive Dealer Association", "The Australian Automobile Association has called"])
chapters.append(c)

c = ch("ch07")
c.at(0, title("The 'Fairer Roads' Plan", "a charge set by income", "McKell Institute", "money"))
c.at("It proposed introducing a road-user charge once electric cars reach thirty", stat("30%", "of the whole fleet electric → charge starts", "McKell Institute", count=False))
c.at("Rates would be set by income", bars("Income-based rates (c/km)", [["Lowest band", 3.74], ["Highest band", 12.86]], None, "McKell Institute", suffix="c"))
c.at("Once electric vehicles passed seventy-five", say("75% EVs → all vehicles pay, excise goes", "75%", 115))
c.at("an extra carbon surcharge", P("fuel"))
c.at("families in the outer suburbs drive the furthest", P("road"))
c.at("71 per cent of electric and hybrid drivers support", stat("71%", "of EV & hybrid drivers support a road-user charge", "Transport Australia"))
c.at("The debate isn't really about whether EVs should pay", say("The real fight: should everyone else pay more too?", "EVERYONE ELSE", 92))
chapters.append(c)

c = ch("ch08")
c.at(0, say("Illustrations – not confirmed prices", "ILLUSTRATIONS", 110))
c.at("Say you drive an electric car 15,000 kilometres", stat("~$464", "a year · EV · 15,000 km · NSW rate", "illustration", count=False))
c.at("Secondary reporting of a Parliamentary Budget Office", stat("~$795", "a year · 15,000 km at ~5.3c/km", "illustration (PBO via secondary reporting)", count=False))
c.at("Under the electric vehicle association's weight-based plan", P("road"))
c.at("A ute using around nine litres", bars("Diesel ute · 13,000 km · illustration", [["Fuel excise (~1,170 L)", 628], ["AEVA charge", 858], ["Total", 1486, "red"]], None,
     "illustration", prefix="$"))
c.at("And under Tesla's proposal", P("fuel"))
c.at("That's why this matters to every driver", say("A few hundred dollars – or well over a thousand.", "THOUSAND", 100))
chapters.append(c)

c = ch("ch09")
c.at(0, title("Who's Right?", "both sides", "the debate", "gov"))
c.at("Supporters say a road-user charge is simply fairer", say("FOR: everyone uses the roads", "FOR", 125))
c.at("Heavier vehicles cause more wear", P("works"))
c.at("Critics say a charge on top of fuel excise is a double tax", say("AGAINST: a double tax", "AGAINST", 125))
c.at("Regional and outer-suburban drivers", P("road"))
c.at("Some worry about privacy", P("gps"))
c.at("EV advocates warn", P("ev"))
c.at("There's also the question of how the money is collected", P("gps"))
c.at("GPS tracking can be more precise", P("gps"))
c.at("Both sides agree on one thing", say("Fuel excise alone won't pay for the roads forever.", "FOREVER", 100))
chapters.append(c)

c = ch("ch10", 2.5)
c.at(0, title("What to Do Now", "4 steps", "drivers", "road"))
c.at("First, don't panic", say("1 · Don't panic – nothing is being collected yet", "1", 100))
c.at("Second, if you're buying an electric car", say("2 · NSW EV buyers: budget ~$400–500 a year", "2", 100))
c.at("It still usually works out cheaper than fuel", P("ev"))
c.at("Third, keep good records", say("3 · Keep odometer records", "3", 120))
c.at("And fourth, have your say", say("4 · Have your say", "4", 130))
questions(c, ["NSW charge · 1 July 2027", "Motoring clubs: 2027 Budget", "Next federal election"],
          ["NSW's charge is due", "The motoring clubs want", "And the next federal election"])
c.at("So, could every Aussie driver end up paying", P("city"))
c.at("But the old system is running out of road", P("road"))
c.at("If this helped", cta("Like · Subscribe · Share", "with someone who drives a lot"))
c.at("should everyone pay, only EVs, or nobody", cta("Everyone, EVs only – or nobody?", "comments"))
chapters.append(c)

CTX = ["road", "fuel", "city", "gov", "fuel", "road", "fuel", "money", "fuel", "gov", "road"]
print(A.finish(chapters, "AUS16_Road_Tax.mp4", CTX, subtitles="AUS16.ass"))
