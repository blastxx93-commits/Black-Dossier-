#!/usr/bin/env python3
"""AUS05 Tesla cancels the Cybertruck for Australia (Oct 2026): full edit, every shot anchored to its phrase.
Run from the episode work folder (a/ = assets of aus05-cybertruck, audio/, sfx/, trilha.wav):
    python3 build_aus05.py <narration_dir> > episode.json
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "engine"))
import aus_kit as A
from aus_kit import P, photo, stat, bars, say, cta, title, ch, questions

PHOTOS = {
    "cyber": ["m_cybertruck", "m_cybertruck_reveal", "m_cybertruck_interior", "m_cybertruck2", "m_cybertruck3", "m_cybertruck4", "ai:ai_angular_ute_rhd"],
    "email": ["ai:ai_reservation_email", "h_email_laptop"],
    "deposit": ["ai:ai_deposit_receipt", "ai:ai_wait_years"],
    "wait": ["ai:ai_wait_years"],
    "roadshow": ["ai:ai_roadshow_crowd"],
    "rhd": ["ai:ai_rhd_steering", "ai:ai_adr_engineer", "ai:ai_pedestrian_dummy"],
    "tesla": ["m_model_y", "m_model_3", "m_tesla_supercharger", "h_tesla_car"],
    "factory": ["m_gigafactory_texas", "h_factory_line"],
    "pickup": ["m_f150", "m_ram1500", "m_silverado", "ai:ai_towing_caravan", "h_pickup_au", "h_pickup3"],
    "ute": ["ai:ai_tradie_ute", "h_ute_outback", "m_hilux", "m_ranger", "m_dmax"],
    "evute": ["ai:ai_ev_ute_charging", "m_mg_u9"],
    "ev": ["h_ev_charging", "m_tesla_supercharger", "h_supercharger", "h_ev_road", "h_ev4"],
    "fuel": ["h_fuel_station"], "port": ["ai:ai_port_cars", "h_car_carrier", "h_containers"], "used": ["ai:ai_used_price"],
    "steel": ["h_stainless"], "traffic": ["h_sydney_road", "h_highway_au", "h_road2", "h_city2"], "cancel": ["m_nissan_leaf", "m_volvo_s60", "m_jaguar"],
}
CLIPS = json.load(open(os.path.join(HERE, "clips.json")))
GENERIC = CLIPS.pop("_generic", [])
FALLBACK = {"cyber": ["pickup", "steel"], "email": ["deposit"], "deposit": ["email", "wait"], "wait": ["deposit"],
            "roadshow": ["cyber"], "rhd": ["cyber", "port"], "tesla": ["ev"], "factory": ["cyber"], "pickup": ["ute"],
            "ute": ["pickup"], "evute": ["ev", "ute"], "ev": ["tesla"], "fuel": ["traffic"], "port": ["traffic"],
            "used": ["pickup"], "steel": ["cyber"], "traffic": ["ev"], "cancel": ["port"]}
RES = ["m_cybertruck/1", "m_cybertruck/3", "m_cybertruck_reveal/1", "m_cybertruck_reveal/3", "m_model_y/1", "m_model_y/3",
       "m_model_3/1", "m_model_3/3", "m_f150/1", "m_ram1500/1", "m_silverado/3", "m_hilux/1", "m_hilux/3", "m_mg_u9/1",
       "m_mg_u9/3", "m_shark6/1", "m_shark6/3", "m_dmax/1", "m_volvo_s60/1", "m_jaguar/1", "m_gigafactory_texas/1", "m_cybertruck_interior/3"]
A.setup(sys.argv[1], os.path.join(HERE, "skip.json"), PHOTOS, CLIPS, GENERIC, FALLBACK,
        ["traffic", "ev", "ute", "pickup", "cyber", "tesla", "port", "email", "steel"], reserved=RES)
A.MAX_HOLD, A.KEEP = 10.5, 7.0  # fewer splits after removing off-topic extras
chapters = []

# ---------------------------------------------------------------- hook
c = ch("ch00_hook", 0.6)
c.at(0, stat("$150", "Cybertruck deposit paid by Aussies · November 2019", "Tesla", red=True))
c.at("the most talked-about vehicle on the planet", photo("m_cybertruck", 1, "in", cap="Tesla Cybertruck|revealed November 2019"))
c.at("They waited through a pandemic", P("wait"))
c.at("the reservation page quietly disappeared", P("email"))
c.at("parade a Cybertruck around Australian showrooms", P("roadshow"))
c.at("They heard Tesla's local boss", say("\"Personally confident.\"", "CONFIDENT", 150))
c.at("on Friday the 23rd of October 2026", P("email", cap="23 October 2026|the email arrived"))
c.at("After careful consideration", say("\"…plans to produce Cybertruck for Australia and New Zealand have been discontinued.\"",
     "DISCONTINUED", 78))
c.at("That's it. No Cybertruck", title("CANCELLED", "Tesla Cybertruck · Australia", "October 2026", "cyber"))
questions(c, ["What happened?", "Why did Tesla walk away?", "What about the refund?", "What can Aussies buy instead?"],
          ["what actually happened", "Why did Tesla walk away", "What does the refund look like", "which electric and American utes"])
c.at("Stay with me, because the real reason", P("ute"))
chapters.append(c)

# ---------------------------------------------------------------- 2019
c = ch("ch01")
c.at(0, P("wait"))
c.at("In November 2019, Elon Musk walked on stage", photo("m_cybertruck_reveal", 1, "in", cap="Los Angeles|November 2019"))
c.at("Stainless steel body", P("steel"))
c.at("Armoured glass", photo("m_cybertruck_reveal", 3, "left"))
c.at("a promised starting price", stat("US$39,900", "promised starting price · 2019", "Tesla", count=False))
c.at("more than 500 miles", stat("800 km", "promised range of the top version (500+ miles)", "Tesla · 2019", count=False))
c.at("The internet went wild", P("cyber"))
c.at("with a $150 refundable deposit", P("deposit"))
c.at("Tesla has said tens of thousands", P("cyber"))
c.at("For Aussies, the idea made sense", P("ute"))
c.at("We love towing", P("pickup"))
c.at("But there was a problem from day one", say("Left-hand drive only.", "LEFT-HAND", 140))
c.at("Australia drives on the left", P("rhd"))
c.at("It means re-engineering the dashboard", P("rhd"))
c.at("when the Cybertruck finally reached American customers", photo("m_cybertruck", 3, "right", cap="Deliveries began|late 2023"))
c.at("The dream and the reality", say("The dream and the reality drifted apart.", "DRIFTED", 115))
chapters.append(c)

# ---------------------------------------------------------------- hope
c = ch("ch02")
c.at(0, P("wait"))
c.at("In May 2022, Tesla closed the local reservation page", P("email", cap="May 2022|reservation page closed"))
c.at("Most people simply forgot", P("deposit"))
c.at("Then, in 2024, the hope came roaring back", P("roadshow"))
c.at("People queued to take photos", P("cyber"))
c.at("Musk told shareholders", say("\"Sometime next year.\"", "NEXT YEAR", 150))
c.at("In March 2025, Tesla's Australia and New Zealand", say("\"Personally confident\" – March 2025", "CONFIDENT", 115))
c.at("Within about a month, his tone had changed", say("\"Not confident it's coming.\" – April 2025", "NOT CONFIDENT", 100))
c.at("By May 2025, the local team had been briefed", P("rhd"))
c.at("bumper widths, external lighting", P("rhd"))
c.at("And then came the silence", P("wait"))
chapters.append(c)

# ---------------------------------------------------------------- why
c = ch("ch03")
c.at(0, title("Why Tesla Pulled the Plug", "the numbers", "4 reasons", "cyber"))
c.at("Musk once predicted", stat("250,000", "Cybertrucks a year – Musk's prediction", None, count=False))
c.at("around 38,965 were sold in 2024", bars("Cybertruck sales in the US", [["2024", 38965], ["2025", 20237, "red"],
     ["Jan–Sep 2026", 11586, "red"]], None, "estimates via CarExpert"))
c.at("Then there's the price", P("cyber"))
c.at("now sells for around eighty thousand", A.price("Tesla Cybertruck (US)", "US$39,900", "~US$80,000", "promised 2019",
     "dual motor · 2026", "x2", "Tesla / CarExpert"))
c.at("it would likely have cost around $130,000", stat("~A$130,000", "estimated Australian price before on-roads", "EV Central", red=True, count=False))
c.at("Then there's right-hand drive", P("rhd"))
c.at("It isn't sold in any right-hand-drive market", P("rhd"))
c.at("Building a right-hand-drive version just for us", P("factory"))
c.at("And finally, the size of the market", P("pickup"))
c.at("sells roughly ten thousand vehicles a year", stat("~10,000", "full-size US pickups sold in Australia a year", None, count=False))
c.at("Even if Tesla grabbed a big slice", P("pickup"))
c.at("Put all of that together", say("The decision was almost made for them.", "MADE", 120))
c.at("the Cybertruck's track record in America", stat("11", "US recalls since launch", "NHTSA", red=True))
c.at("In April 2024, it was recalled", P("cyber", cap="April 2024|accelerator pedal pad"))
c.at("In March 2025, more than 46,000 trucks", stat("46,000+", "recalled · trim panel could detach · March 2025", "NHTSA", red=True))
c.at("In October 2025, more than 63,000", stat("63,000+", "recalled · parking lights too bright · October 2025", "NHTSA", red=True))
c.at("And in April 2026, there was a recall", P("cyber", cap="April 2026|brake rotor stud holes"))
c.at("Recalls happen to every brand", P("factory"))
c.at("every extra problem made the Australian business case", say("A weaker business case for Australia.", "WEAKER", 115))
chapters.append(c)

# ---------------------------------------------------------------- refund
c = ch("ch04")
c.at(0, P("email"))
c.at("deposits refunded in full", stat("$150", "refunded in full", "Tesla · October 2026"))
c.at("the money should arrive within thirty days", stat("30 days", "expected refund time", "EV Central", count=False))
c.at("And Tesla has added a sweetener", photo("m_model_y", 1, "in", cap="Order a Model 3 or Model Y|1 year of FSD (Supervised)"))
c.at("At the current price of $149 a month", stat("$1,788", "value of 1 year of FSD (Supervised) at $149/month", "Tesla"))
c.at("Supervised", P("tesla"))
c.at("The driver must stay alert", say("The driver stays responsible.", "RESPONSIBLE", 130))
c.at("It's a driver assistance feature", P("traffic"))
c.at("If you paid a deposit back in 2019", P("email"))
c.at("A $150 refund isn't life-changing", P("deposit"))
chapters.append(c)

# ---------------------------------------------------------------- mid CTA
c = ch("ch05")
c.at(0, P("cyber"))
c.at("Tell me in the comments", cta("Were you in the queue?", "Tell me in the comments"))
c.at("hit subscribe and turn on notifications", cta("Subscribe & turn on notifications", "Honest Aussie car news, 2026"))
chapters.append(c)

# ---------------------------------------------------------------- Tesla is fine
c = ch("ch06")
c.at(0, say("Tesla isn't struggling. The Cybertruck didn't fit.", "DIDN'T FIT", 105))
c.at("In September 2026, Tesla sold 5,654", stat("5,654", "Teslas sold in Australia · September 2026 (+21%)", "EVC / VFACTS"))
c.at("Electric vehicles made up 24.2 per cent", stat("24.2%", "EV share of new car sales · September 2026", "FCAI / EVC"))
c.at("with a fuel crisis pushing diesel", P("fuel", cap="Diesel|towards $3 a litre"))
c.at("more Aussies than ever are thinking", P("ev"))
c.at("NRMA Insurance says requests", stat("+80%", "EV insurance quote requests · Jan–Sep 2026", "NRMA Insurance"))
c.at("the share of Australians actively considering", bars("Aussies considering a battery EV", [["2024", 20], ["2026", 31]],
     None, "NRMA survey", suffix="%"))
c.at("It just isn't demand for a $130,000", P("steel"))
c.at("In June, Tesla sold 8,670", stat("8,670", "Teslas sold · June 2026 – best month ever", "EVC"))
c.at("The Model Y alone sold 8,072", photo("m_model_y", 3, "in", cap="Model Y|20,396 sold in H1 2026 (+95%)"))
c.at("Tesla's first-half total was 23,588", stat("23,588", "Tesla sales · first half 2026 (+67%)", "EVC"))
c.at("A big part of that came from the new six-seat", P("tesla"))
c.at("The Model 3 has gone backwards", photo("m_model_3", 1, "left", cap="Model 3|-47% in June"))
c.at("And BYD's Sealion 7 has become a serious rival", P("ev"))
c.at("But overall, Tesla is having one of its best years", P("tesla"))
c.at("So Tesla's message is clear", photo("m_model_3", 3, "right"))
c.at("than into a niche, left-hand-drive truck", P("cyber"))
c.at("That's a business decision", P("deposit"))
c.at("if not the Cybertruck, then what", say("If not the Cybertruck, then what?", "THEN WHAT", 120))
chapters.append(c)

# ---------------------------------------------------------------- US pickups
c = ch("ch07")
c.at(0, P("pickup"))
c.at("Australia already has the Ram 1500", photo("m_ram1500", 1, "in"))
c.at("In March 2026, the F-150 sold 270", bars("Full-size pickups · March 2026", [["Ford F-150", 270], ["Ram 1500", 181],
     ["Chevrolet Silverado", 172]], None, "VFACTS"))
c.at("These are big, expensive trucks", photo("m_silverado", 3, "left"))
c.at("Ford recalled the F-150 in Australia over a fire risk", photo("m_f150", 1, "right", cap="Ford F-150|fire-risk recall · October 2026"))
c.at("And there's a reason these trucks cost so much here", P("pickup"))
c.at("The Ram 1500 and the Chevrolet Silverado are remanufactured", say("Rebuilt in Melbourne: Walkinshaw (Ram, Silverado) · RMA (F-150)", "MELBOURNE", 80))
c.at("the F-150 is converted by RMA Automotive", P("pickup"))
c.at("Each truck arrives in left-hand drive", P("rhd"))
c.at("It's skilled, expensive work", stat("$100,000+", "many converted US pickups in Australia", None, red=True, count=False))
c.at("That's exactly the work the Cybertruck would have needed", P("cyber"))
c.at("its unusual steer-by-wire system", photo("m_cybertruck_interior", 3, "in"))
c.at("Even the established American trucks", P("pickup"))
c.at("The Cybertruck would have been a niche within a niche", say("A niche within a niche.", "NICHE", 140))
c.at("And Tesla isn't the only company", P("port"))
c.at("Isuzu has cancelled its plans", photo("m_dmax", 1, "in", cap="Isuzu D-Max EV|cancelled for Australia"))
c.at("Nissan has indefinitely postponed", P("cancel", cap="Nissan|new Leaf postponed"))
c.at("Jaguar stopped selling new petrol cars", photo("m_jaguar", 1, "left", cap="Jaguar|0 new cars sold in September"))
c.at("And Volvo has axed the S60", photo("m_volvo_s60", 1, "right", cap="Volvo S60 & V60 CC|axed"))
c.at("with around seventy brands fighting", stat("~70", "brands fighting for ~1.2 million sales a year", "AADA review · 2026", count=False))
c.at("car makers are being ruthless", P("port"))
chapters.append(c)

# ---------------------------------------------------------------- electric utes
c = ch("ch08")
c.at(0, P("evute"))
c.at("Electric utes make up less than one per cent", stat("<1%", "of ute sales are electric · 2026", "CarExpert", red=True, count=False))
c.at("there were 157,531 ute deliveries", stat("157,531", "ute deliveries Jan–Sep 2026", "CarExpert"))
c.at("Toyota launched the HiLux BEV", photo("m_hilux", 1, "in", cap="Toyota HiLux BEV|~300 sold May–early July"))
c.at("with fewer than ten going to private buyers", say("Fewer than 10 private buyers.", "10", 135))
c.at("KGM's Musso EV has sold just over 300", P("ute", cap="KGM Musso EV|just over 300 sold"))
c.at("Customers don't want it", say("\"Customers don't want it.\" – Isuzu", "DON'T WANT", 115))
c.at("MG confirmed the U9 EV", photo("m_mg_u9", 1, "in", cap="MG U9 EV|from $78,990 before on-roads"))
c.at("It claims 430 kilometres of range", bars("MG U9 EV", [["Range (km)", 430], ["Power (kW)", 325], ["Payload (kg)", 685]],
     None, "MG Australia"))
c.at("3,500 kilograms of braked towing", stat("3,500 kg", "braked towing – MG U9 EV", "MG Australia"))
c.at("It can charge from twenty to eighty", photo("m_mg_u9", 3, "right"))
c.at("Deliveries start in the last quarter", P("evute"))
c.at("MG says customers here have been", say("\"Yearning\" for an electric ute.", "YEARNING", 125))
c.at("led by the BYD Shark 6", photo("m_shark6", 1, "in", cap="BYD Shark 6|#3 4x4 pick-up · H1 2026"))
c.at("GAC has confirmed its upcoming ute", photo("m_shark6", 3, "left"))
c.at("So the electric ute is coming", say("The electric ute is coming. Just not like this.", "COMING", 110))
chapters.append(c)

# ---------------------------------------------------------------- what it means
c = ch("ch09")
c.at(0, P("traffic"))
c.at("If you had a Cybertruck reservation", P("email"))
c.at("If you've moved or changed email address", P("deposit"))
c.at("If you're thinking about a big American pickup", P("pickup"))
c.at("check recalls, service locations and resale", P("used"))
c.at("If you want an electric ute", P("evute"))
c.at("Range drops when you tow heavy loads", P("pickup"))
c.at("If you mostly do short runs", P("ev"))
c.at("especially with fuel prices", P("fuel"))
c.at("A reservation is not a promise", say("A reservation is not a promise.", "NOT A PROMISE", 125))
questions(c, ["Fully refundable?", "How do I get it back?", "Any delivery date?"],
          ["ask whether the deposit is fully refundable", "how you'll get it back", "whether there's any date"])
c.at("Under the Australian Consumer Law", say("Australian Consumer Law", "CONSUMER LAW", 140))
c.at("any contract term that lets a business keep", P("deposit"))
c.at("Put your request in writing", P("email"))
c.at("Keep a copy of Tesla's email", P("email"))
c.at("Note the date", P("wait"))
c.at("A hundred and fifty dollars might not sound", P("deposit"))
chapters.append(c)

# ---------------------------------------------------------------- end
c = ch("ch10", 2.5)
c.at(0, P("cyber"))
c.at("Seven years, a $150 deposit", stat("7 years", "from reservation to cancellation", "Nov 2019 → Oct 2026", red=True, count=False))
c.at("Lesson one: a reveal is not a product", say("1 · A reveal is not a product", "1", 125))
c.at("especially if it's only built in left-hand drive", P("rhd"))
c.at("Lesson two: right-hand drive matters", say("2 · Right-hand drive matters", "2", 125))
c.at("we're not always first in line", P("port"))
c.at("Lesson three", say("3 · Buy what you can service here", "3", 115))
c.at("Hype doesn't fix a recall", P("used"))
c.at("The truth is, the Cybertruck was always going to struggle", P("cyber"))
c.at("And the electric ute race in Australia", P("evute"))
questions(c, ["Would you pay ~$130,000?"], ["Would you have bought a Cybertruck"])
c.at("If you enjoyed this, hit like and subscribe", cta("Like · Subscribe", "new Aussie car stories every week"))
c.at("And in the next video", title("BYD's Biggest Problem Starts AFTER the Crash", "repairs · waits · insurance", "next video", "ev"))
chapters.append(c)

CTX = ["cyber", "cyber", "wait", "cyber", "email", "cyber", "tesla", "pickup", "evute", "traffic", "cyber"]
print(A.finish(chapters, "AUS05_Cybertruck_Cancelled.mp4", CTX, subtitles="AUS05.ass"))
