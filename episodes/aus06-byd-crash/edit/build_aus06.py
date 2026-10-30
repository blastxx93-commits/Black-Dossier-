#!/usr/bin/env python3
"""AUS06 BYD after the crash (2026): full edit, every shot anchored to the phrase it illustrates.
Run from the episode work folder (a/ = assets of aus06-byd-crash, audio/, sfx/, trilha.wav):
    python3 build_aus06.py <narration_dir> > episode.json
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "engine"))
import aus_kit as A
from aus_kit import P, photo, stat, bars, say, cta, title, ch, questions

PHOTOS = {
    "crash": ["ai:ai_rear_end", "h_bumper", "h_car_crash", "h_damaged"],
    "tow": ["ai:ai_flatbed_ev", "h_tow_truck", "h_tow2"],
    "quarantine": ["ai:ai_quarantine", "h_wrecking_yard"],
    "hv": ["ai:ai_hv_technician", "h_mechanic_ev", "h_mechanic2"],
    "battery": ["ai:ai_battery_lifted", "ai:ai_battery_cells", "h_battery_pack", "m_blade"],
    "sensors": ["ai:ai_bumper_sensors", "ai:ai_adas_calibration", "h_parking_sensor"],
    "repairer": ["ai:ai_cars_waiting", "h_panel_beater", "h_workshop", "h_spray", "h_repair3"],
    "assess": ["ai:ai_assessor", "h_insurance_form", "h_insurance2", "h_insurance3"],
    "dash": ["ai:ai_dashboard_warning"],
    "parts": ["ai:ai_parts_shelves", "h_warehouse"], "plane": ["h_cargo_plane"],
    "bills": ["ai:ai_renewal_letter", "h_calculator_bills", "h_worried", "h_bills2"], "compare": ["ai:ai_compare_quotes"],
    "phone": ["h_phone_call"], "byd": ["m_dolphin", "m_seal", "m_sealion6", "m_sealion7", "m_atto1", "m_byd2", "m_byd3", "m_byd4"],
    "dealer": ["m_byd_dealer", "m_byd_logo_building", "m_byd4"], "traffic": ["h_traffic_light", "h_road_au", "h_carpark", "h_road3"], "writeoff": ["h_wrecking_yard"],
    "ev": ["h_ev2"],
}
CLIPS = json.load(open(os.path.join(HERE, "clips.json")))
GENERIC = CLIPS.pop("_generic", [])
FALLBACK = {"crash": ["tow"], "tow": ["crash"], "quarantine": ["writeoff", "tow"], "hv": ["repairer", "battery"],
            "battery": ["hv"], "sensors": ["repairer"], "repairer": ["hv", "assess"], "assess": ["repairer", "bills"],
            "dash": ["sensors"], "parts": ["plane", "dealer"], "plane": ["parts"], "bills": ["compare", "assess"],
            "compare": ["bills"], "phone": ["assess"], "byd": ["dealer"], "dealer": ["byd"], "traffic": ["ev", "byd"],
            "writeoff": ["quarantine"], "ev": ["traffic", "byd"]}
RES = ["m_dolphin/1", "m_dolphin/3", "m_seal/1", "m_seal/3", "m_sealion6/1", "m_sealion6/3", "m_sealion7/1", "m_sealion7/3",
       "m_atto1/1", "m_atto1/3", "m_corolla/1", "m_cx30/1", "m_tesla_m3/1", "m_blade/1", "m_byd_dealer/1", "m_byd_dealer/3"]
A.setup(sys.argv[1], os.path.join(HERE, "skip.json"), PHOTOS, CLIPS, GENERIC, FALLBACK,
        ["traffic", "ev", "repairer", "crash", "byd", "bills", "assess", "parts"], reserved=RES)
A.MAX_HOLD, A.KEEP = 10.5, 7.0  # fewer splits after removing off-topic extras
chapters = []

# ---------------------------------------------------------------- hook
c = ch("ch00_hook", 0.6)
c.at(0, P("traffic"))
c.at("The car behind you doesn't stop in time", P("crash"))
c.at("The bumper's pushed in", P("sensors"))
c.at("a sensor light is flashing on the dash", P("dash"))
c.at("no worries, the insurance will sort it out", say("\"No worries, insurance will sort it out.\"", "NO WORRIES", 110))
c.at("But this is where a very different story begins", P("repairer"))
c.at("It's everything that happens after it", say("The real problem starts AFTER the crash.", "AFTER", 115))
questions(c, ["The tow", "The repairer", "The battery check", "The wait", "The renewal letter"],
          ["The tow truck", "The repairer that", "The battery check", "The wait for parts", "the insurance renewal letter"])
c.at("BYD is now one of the biggest car brands", photo("m_dolphin", 1, "in", cap="BYD|#2 brand in Australia · 2026"))
c.at("we're going to follow a BYD", P("byd"))
c.at("Just what actually happens", title("BYD's Biggest Problem Starts AFTER the Crash", "Australia · 2026", "real 2026 data", "crash"))
c.at("I'll give you a simple checklist", P("assess"))
chapters.append(c)

# ---------------------------------------------------------------- why it matters
c = ch("ch01")
c.at(0, P("ev"))
c.at("In September 2026, BYD sold 8,191", stat("8,191", "BYD sales in Australia · September 2026 (+61%)", "FCAI / EVC via Cars24"))
c.at("the second best-selling brand in the country", bars("Top brands · September 2026", [["Toyota", 17682], ["BYD", 8191]],
     None, "FCAI / EVC"))
c.at("Ford, Mazda, Kia, Hyundai", P("dealer"))
c.at("Its range now covers almost every type of buyer", photo("m_atto1", 1, "in", cap="BYD Atto 1|city car"))
c.at("the Atto 3 and Sealion 7 SUVs", photo("m_sealion7", 1, "left"))
c.at("the Seal sedan", photo("m_seal", 3, "right"))
c.at("the Sealion 6 plug-in hybrid", photo("m_sealion6", 1, "in"))
c.at("electric and plug-in cars have gone mainstream", P("ev"))
c.at("battery electric cars made up more than twenty-four", stat("24%+", "battery EV share of new car sales · September 2026", "FCAI / EVC"))
c.at("more pure electric cars were sold than petrol-only", say("More EVs than petrol-only cars – 2 months running.", "EVs", 100))
c.at("NRMA Insurance says requests", stat("+80%", "EV insurance quote requests · Jan–Sep 2026", "NRMA Insurance"))
c.at("More of these cars on the road means more", P("crash"))
c.at("That's not a criticism of BYD", say("Not a criticism. Just maths.", "MATHS", 140))
c.at("discover how an EV crash repair actually works", P("repairer"))
chapters.append(c)

# ---------------------------------------------------------------- tow + who can fix it
c = ch("ch02")
c.at(0, title("Step 1", "The tow", "after the crash", "tow"))
c.at("An EV has a large high-voltage battery", P("battery"))
c.at("Most tow operators will want to move it on a flatbed", P("tow"))
c.at("If the battery might have been hit", P("quarantine"))
c.at("Many assessing centres now keep damaged EVs", P("quarantine", cap="Damaged EVs|kept apart in quarantine"))
c.at("Then comes the next question", say("Who's allowed to fix it?", "WHO", 140))
c.at("Repairing an electric car properly needs trained technicians", P("hv"))
c.at("procedures to safely isolate the high-voltage system", P("hv"))
c.at("Back in 2024, the Motor Trades Association", stat("~10%", "of repairers EV-certified (2024)", "MTAA · Matt Hobbs", red=True, count=False))
c.at("technicians have to be trained to safely de-power", stat("400 V", "systems to de-power before any work", "MTAA · 2024", count=False))
c.at("only around forty-one per cent", stat("41%", "of EV technician jobs filled", "MTAA / Deloitte", red=True))
c.at("That number has been growing", P("repairer"))
c.at("BYD has its own approved collision repair network", P("dealer"))
c.at("the nearest approved shop could be a long way away", P("tow"))
c.at("So before a single panel is touched", say("Further. Longer. Before a single panel is touched.", "LONGER", 100))
chapters.append(c)

# ---------------------------------------------------------------- the damage
c = ch("ch03")
c.at(0, title("Step 2", "The damage you can't see", "at the repairer", "repairer"))
c.at("modern cars hide a lot behind the bumper", P("sensors"))
c.at("It can carry parking sensors", P("sensors"))
c.at("those sensors often need to be replaced", P("sensors", cap="Sensors & cameras|replace + recalibrate"))
c.at("A bump that would have cost a few hundred", A.price("Low-speed rear bump", "a few hundred $", "several thousand $",
     "older car", "car with sensors", None, "industry estimates"))
c.at("Then there's the battery", P("battery"))
c.at("On some models, that means removing the battery", P("battery"))
c.at("the battery can make up around thirty to fifty", stat("30–50%", "of an EV's value is the battery", "Taylor Fry · April 2026", red=True, count=False))
c.at("Replace the battery, and you may be looking", P("bills"))
c.at("That's why some EVs with relatively modest damage", P("writeoff"))
c.at("Not because the car is destroyed", P("crash"))
c.at("Industry insiders have described cases", P("battery"))
c.at("the salvage value of a written-off electric car", stat("8–10%", "salvage value of a written-off EV (2024)", "AAMC", red=True, count=False))
c.at("Every one of those write-offs is a cost", P("bills"))
c.at("not every insurer sees it the same way", P("assess"))
c.at("Allianz, for example, has said", say("Cosmetic EV repairs: about as fast as petrol – Allianz", "ALLIANZ", 90))
c.at("The problem is concentrated in the serious crashes", P("hv"))
chapters.append(c)

# ---------------------------------------------------------------- Blade battery
c = ch("ch04")
c.at(0, photo("m_blade", 1, "in", cap="BYD Blade battery|lithium iron phosphate"))
c.at("BYD uses what it calls the Blade battery", P("battery"))
c.at("allow damaged sections to be repaired", P("hv"))
c.at("Lithium iron phosphate cells are also generally", P("battery"))
c.at("That's genuinely good news for owners", photo("m_seal", 1, "left"))
c.at("But it only helps if the repairer is trained", P("repairer"))
c.at("And that brings us to the part almost every BYD owner", say("The part every owner talks about…", "EVERY OWNER", 115))
chapters.append(c)

# ---------------------------------------------------------------- the wait
c = ch("ch05")
c.at(0, title("Step 3", "The wait", "parts & workshops", "repairer"))
c.at("In the early years of BYD in Australia", P("repairer"))
c.at("Some owners publicly described waiting months", P("phone"))
c.at("BYD's own executives have acknowledged", P("dealer"))
c.at("And in 2026, BYD has spent serious money", P("parts"))
c.at("it now holds more than 580,000 parts", stat("580,000+", "parts held in Australia", "BYD · October 2026"))
c.at("covering around ninety-five per cent", stat("95%", "of parts in local stock · $25M+ · 4 warehouses", "BYD · October 2026"))
c.at("It says it now stocks Blade battery packs locally", P("battery"))
c.at("parts not in stock can be sent by air freight", P("plane"))
c.at("back in 2024, MG told CarAdvice", bars("Local parts fill rate", [["BYD (2026)", 95], ["MG (2024)", 91]], None,
     "BYD · CarAdvice", suffix="%"))
c.at("Polestar said overseas parts could take", stat("4–6 weeks", "Polestar overseas parts (2024)", "CarAdvice", count=False))
c.at("The real test is whether owners waiting", P("repairer"))
c.at("the average wait for a service booking", bars("BYD service booking wait", [["Now", 7], ["Target", 5]], None,
     "BYD via NRMA Open Road · Sept 2026", suffix=" days"))
c.at("But the wider industry still has a capacity problem", P("repairer"))
c.at("backlogs of six to eight weeks just to diagnose", stat("6–8 weeks", "just to DIAGNOSE a problem", "AADA review · July 2026", red=True, count=False))
c.at("the bottleneck can move to the workshop itself", P("hv"))
c.at("too many cars arriving at once", P("repairer"))
chapters.append(c)

# ---------------------------------------------------------------- mid CTA
c = ch("ch06")
c.at(0, P("crash"))
c.at("Have you had a crash repair", cta("Had a crash repair?", "How long did it take? Tell me in the comments"))
c.at("hit subscribe", cta("Subscribe", "Honest, fact-checked Aussie car news"))
chapters.append(c)

# ---------------------------------------------------------------- who pays
c = ch("ch07")
c.at(0, title("Step 4", "Who pays", "repair costs", "bills"))
c.at("the average cost of motor vehicle repairs has risen", stat("+26%", "average repair cost since 2022", "Insurance Council of Australia", red=True))
c.at("repair costs now account for roughly sixty", stat("~60%", "of motor claim payouts are repairs", "Insurance Council of Australia", count=False))
c.at("Sensors, cameras, more expensive paint", P("sensors"))
c.at("Electric cars add another layer", P("hv"))
c.at("EV repairs currently sit in a cost category", say("\"…more like high-end luxury cars.\"", "LUXURY", 115))
c.at("insurers have to charge more to cover the risk", P("assess"))
c.at("There's also a hire car issue", P("traffic"))
c.at("that hire bill keeps running", P("bills"))
c.at("the premiums everyone pays at renewal", P("bills"))
chapters.append(c)

# ---------------------------------------------------------------- renewal
c = ch("ch08")
c.at(0, P("bills"))
c.at("Compare the Market published an analysis", P("compare"))
c.at("the average premium for battery electric vehicles had risen", stat("+10.2%", "average BEV premium · now ~$2,300/yr", "Compare the Market · April 2026", red=True))
c.at("And for some BYD models, the jump was bigger", bars("BYD premium change · 2026", [["Sealion 6", 18, "red"], ["Dolphin", 9, "red"],
     ["Shark 6", 5, "red"], ["Sealion 7", 0.5]], None, "Compare the Market · April 2026", prefix="+", suffix="%"))
c.at("from around $1,482 to around $1,821", A.price("BYD Sealion 6 · average premium", "$1,482", "$1,821", "2025", "2026", "+18%",
     "Compare the Market"))
c.at("The Dolphin went up about nine per cent", photo("m_dolphin", 3, "in", cap="BYD Dolphin|$1,437 → $1,578"))
c.at("The Shark 6 rose about five per cent", stat("$2,172", "BYD Shark 6 average premium (+5%)", "Compare the Market · April 2026"))
c.at("And the Sealion 7 was almost flat", photo("m_sealion7", 3, "right"))
c.at("CHOICE reported in January 2026", bars("Average premium · CHOICE Jan 2026", [["EV", 2545, "red"], ["Petrol", 1702]], None,
     "CHOICE", prefix="$"))
c.at("the spread of quotes for an Atto 3", bars("Gap between cheapest & dearest quote", [["BYD Atto 3", 900, "red"],
     ["Mazda CX-30", 500]], None, "Taylor Fry · April 2026", prefix="$"))
c.at("These are averages from specific comparisons", P("compare"))
c.at("Your age, postcode, driving history", P("assess"))
c.at("BYD isn't the most expensive brand to insure", photo("m_tesla_m3", 1, "left", cap="Teslas|cost more to insure"))
c.at("the trend is clear", say("EV insurance is rising faster.", "FASTER", 130))
c.at("shopping around has never mattered more", P("compare"))
chapters.append(c)

# ---------------------------------------------------------------- your rights
c = ch("ch09")
c.at(0, P("phone"))
c.at("First, know that your insurer has rules to follow", say("General Insurance Code of Practice", "CODE", 120))
questions(c, ["Updates every 20 business days", "Replies within 10 business days", "Decision within 4 months"],
          ["a progress update at least every twenty", "respond to routine requests within ten", "make a decision on your claim within four months"])
c.at("If you feel your claim is stuck", P("phone"))
c.at("Second, if you're not happy with the answer", P("assess"))
c.at("Insurers generally have thirty days", stat("30 days", "for the insurer to answer a complaint", "AFCA", count=False))
c.at("Australian Financial Complaints Authority", say("AFCA – free & independent", "AFCA", 140))
c.at("Before you go, gather everything", P("assess"))
c.at("A clear timeline makes a complaint much stronger", P("bills"))
c.at("Third, if the delay is about parts", P("parts"))
c.at("Manufacturers and importers have to make spare parts", say("Parts must be reasonably available.", "REASONABLY", 120))
c.at("you also have consumer guarantee rights", P("dealer"))
c.at("Your state's fair trading office can help", P("phone"))
chapters.append(c)

# ---------------------------------------------------------------- checklist
c = ch("ch10")
c.at(0, title("The Checklist", "save this one", "before · renewal · after", "assess"))
c.at("Before a crash happens", say("Before a crash", "BEFORE", 150))
questions(c, ["Hire car cover?", "Capped in $ or days?", "Who chooses the repairer?"],
          ["Does it cover a hire car", "Is the hire car capped", "Can you choose your own repairer"])
c.at("find out where your nearest BYD-approved", P("dealer"))
c.at("When you renew", say("At renewal", "RENEWAL", 150))
c.at("Get quotes from at least three insurers", P("compare"))
c.at("a twenty-minute search can pay for itself", P("bills"))
c.at("Ask how they handle EV battery damage", P("battery"))
c.at("After a crash", say("After a crash", "AFTER", 150))
c.at("take photos of everything", P("crash"))
c.at("including the dashboard warnings", P("dash"))
c.at("Tell the tow operator", P("tow"))
c.at("Keep a diary of every call and email", P("phone"))
c.at("ask whether a battery health check has been done", P("battery"))
c.at("is your car insured for an agreed value or a market value", say("Agreed value or market value?", "VALUE", 120))
c.at("With an agreed value", P("assess"))
c.at("With market value, the insurer pays", P("bills"))
c.at("If an EV is written off because of battery damage", P("writeoff"))
c.at("So read the policy wording", P("compare"))
c.at("It's also worth knowing who chooses the repairer", say("Who chooses the repairer?", "WHO", 130))
c.at("If you want an EV-certified or BYD-approved repairer", P("hv"))
c.at("ask the dealer three questions before you sign", P("dealer"))
questions(c, ["Nearest approved repairer?", "Service wait right now?", "Crash parts stocked here?"],
          ["Where is the nearest approved collision repairer", "How long are service bookings", "are crash parts for this model"])
c.at("The answers will tell you a lot", P("byd"))
chapters.append(c)

# ---------------------------------------------------------------- end
c = ch("ch11", 2.5)
c.at(0, P("byd"))
c.at("The real challenge starts after the crash", say("The real challenge starts after the crash.", "AFTER", 110))
c.at("a repair industry that's still catching up", P("repairer"))
c.at("insurers adjusting their prices", P("bills"))
c.at("The good news is that BYD is clearly spending money", P("parts"))
c.at("The question for 2027", P("traffic"))
c.at("If this video helped you", cta("Like · Subscribe", "sources in the description"))
questions(c, ["Has your insurance gone up this year?"], ["has your insurance gone up this year"])
c.at("watch our video on how Tesla cancelled", title("Tesla Cancelled the Cybertruck", "for Australia – after 7 years of deposits", "watch next", "ev"))
chapters.append(c)

CTX = ["crash", "ev", "tow", "repairer", "battery", "parts", "crash", "bills", "bills", "assess", "assess", "byd"]
print(A.finish(chapters, "AUS06_BYD_After_The_Crash.mp4", CTX, subtitles="AUS06.ass"))
