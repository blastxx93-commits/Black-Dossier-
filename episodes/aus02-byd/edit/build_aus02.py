#!/usr/bin/env python3
"""AUS02 BYD repairs: full edit, every shot anchored to the phrase it illustrates.
Run from the episode work folder (a/ = assets of aus02-byd, audio/, sfx/, trilha.wav):
    python3 build_aus02.py <narration_dir> > episode.json
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "engine"))
import aus_kit as A
from aus_kit import P, photo, stat, bars, say, cta, title, ch, questions

PHOTOS = {
    "crash": ["h_crash", "h_bumper", "ai:ai_smash_repairer", "ai:ai_car_waiting_weeks"],
    "repairer": ["ai:ai_smash_repairer", "ai:ai_workshop_backlog", "h_mechanic", "h_ev_workshop"],
    "waiting": ["ai:ai_car_waiting_weeks", "h_calendar"],
    "kangaroo": ["ai:ai_kangaroo_road_night", "h_kangaroo_road", "h_kangaroo"],
    "parts": ["ai:ai_parts_shelves", "h_warehouse", "h_forklift"],
    "ship": ["h_ship"],
    "phone": ["ai:ai_owner_phone", "h_phone", "h_email", "h_customer_service"],
    "ev": ["h_ev_charge", "h_battery"],
    "battery": ["ai:ai_battery_pack", "h_battery"],
    "tech": ["ai:ai_ev_technician", "h_ev_workshop", "h_mechanic"],
    "insurance": ["ai:ai_insurance_papers", "h_insurance", "h_documents"],
    "byd": ["g_byd_badge", "g_byd_store", "m_atto3", "m_dolphin", "m_seal", "m_sealion6", "m_sealion7", "m_atto1"],
    "dealer": ["ai:ai_three_questions", "h_dealer"],
    "melbourne": ["h_melbourne", "h_highway_night"],
    "rights": ["ai:ai_fair_trading", "h_documents", "h_email"],
    "delivery": ["ai:ai_delivery_van"],
    "road": ["h_highway_night", "h_kangaroo_road"],
    "tyre": ["h_spare_tyre"],
}
CLIPS = {
    "repairer": ["v_mechanic/3", "v_ev_repair/3"], "tech": ["v_laptop/1", "v_mechanic/3"],
    "waiting": ["v_waiting/1", "v_waiting/3"], "kangaroo": ["v_kangaroo/1", "v_kangaroo/2", "v_kangaroo/3"],
    "parts": ["v_warehouse/3", "v_cargo_ship/2"], "ship": ["v_cargo_ship/1", "v_cargo_ship/3", "v_warehouse/2"],
    "phone": ["v_phone/1", "v_phone/2", "v_phone/3"], "ev": ["v_ev_charge/1", "v_ev_charge/2", "v_ev_charge/3"],
    "insurance": ["v_laptop/3"], "melbourne": ["v_city/1", "v_city/2", "v_city/3", "v_night_drive/1"],
    "rights": ["v_laptop/2", "v_laptop/1"], "delivery": ["v_delivery/2", "v_delivery/3", "v_ev_repair/2"],
    "road": ["v_road/1", "v_road/2", "v_road/3", "v_night_drive/3"], "byd": ["v_ev_charge/2"],
}
GENERIC = ["v_road/1", "v_road/2", "v_road/3", "v_city/1", "v_city/2", "v_city/3", "v_night_drive/1", "v_night_drive/3",
           "v_cargo_ship/1", "v_delivery/2", "v_kangaroo/2", "v_ev_charge/3"]
FALLBACK = {"byd": ["dealer", "ev"], "crash": ["repairer"], "repairer": ["tech", "crash"], "waiting": ["phone"],
            "parts": ["ship", "delivery"], "phone": ["rights"], "ev": ["battery", "byd"], "insurance": ["rights"],
            "melbourne": ["road"], "road": ["melbourne"], "dealer": ["byd"], "tech": ["repairer"], "ship": ["parts"],
            "delivery": ["road"], "battery": ["ev"], "tyre": ["crash"], "kangaroo": ["road"], "rights": ["insurance", "phone"]}
A.setup(sys.argv[1], os.path.join(HERE, "skip.json"), PHOTOS, CLIPS, GENERIC, FALLBACK, ["road", "melbourne", "ev"],
        reserved=["m_atto3/1", "m_dolphin/1", "m_dolphin/3", "m_seal/1", "m_shark6/1", "m_shark6/5", "m_denza/1", "m_denza/2"])
BYD = "BYD Australia"
chapters = []

# ---------------------------------------------------------------- hook
c = ch("ch00_hook", 0.6)
c.at(0, P("byd"))
c.at("A few months later, you hit a kangaroo", P("kangaroo"))
c.at("Your insurance accepts the claim", P("insurance"))
c.at("The parts are ordered", P("parts"))
c.at("And then nothing", say("And then… nothing.", "NOTHING", 150))
c.at("Eleven weeks later", stat("11 WEEKS", "still sitting at the smash repairer", "owner's post, r/CarsAustralia, Jan 2025", red=True, count=False))
c.at("And the supplier tells you", stat("+8 WEEKS", "more to wait for the missing parts", "owner's post, r/CarsAustralia, Jan 2025", red=True, count=False))
c.at("That's not a made-up story", P("crash"))
c.at("It's what one BYD owner described publicly", P("phone", cap="Owner's forum post|Early 2025"))
c.at("Parts delays, calls that go unanswered", P("phone"))
c.at("long waits just to get a car looked at", P("waiting"))
c.at("Today, BYD is one of the biggest car brands", P("byd"))
questions(c, ["What went wrong?", "How much to repair?", "Has BYD fixed it?"],
          ["So what went wrong after the sale", "How expensive is a BYD to repair", "And has BYD actually fixed it"])
c.at("Because in October 2026, BYD made", title("BYD's Repair Problem", "And the $25 million fix", "Australia 2026", "parts"))
chapters.append(c)

# ---------------------------------------------------------------- the rise
c = ch("ch01")
c.at(0, photo("m_atto3", 1, "in", cap="Where it started|BYD Atto 3"))
c.at("Within a few years, it had a full range", photo("m_dolphin", 1, "left"))
c.at("the Seal, the Sealion 6 and Sealion 7", photo("m_seal", 1, "right"))
c.at("the Shark 6 ute", photo("m_shark6", 1, "in"))
c.at("and now even a budget EV, the Atto 1", stat("$19,990", "BYD Atto 1 · starting price", "CarsGuide"))
c.at("In the first half of 2026, BYD sold more than", stat("52,000+", "BYD sales · first half of 2026", "CarsGuide / VFACTS"))
c.at("In March, it broke into the top three", stat("TOP 3", "BYD's brand ranking · March 2026", "CarExpert / VFACTS", count=False))
c.at("By October, BYD said it had more than", stat("150,000+", "BYD customers in Australia", BYD))
c.at("That's incredible growth", P("melbourne"))
c.at("Selling cars is one thing", say("Selling cars is one thing. Fixing them is another.", "FIXING", 120))
c.at("Every one of those 150,000 cars will need servicing", P("tech"))
c.at("sooner or later crash repairs", P("crash"))
c.at("And the network to support them", P("repairer"))
chapters.append(c)

# ---------------------------------------------------------------- problem 1: parts
c = ch("ch02")
c.at(0, P("ship"))
c.at("When a part isn't stocked locally", P("ship"))
c.at("BYD's own executives have been open", P("byd"))
c.at("When Stephen Collins took over", say("Shake off the reputation for parts delays", "PARTS DELAYS", 110))
c.at("CarsGuide reported that months-long parts delays", P("phone", cap="CarsGuide|Common owner complaints"))
c.at("with some posts attracting thousands", P("phone"))
c.at("And there was another issue", P("tech"))
c.at("Mark Harland, the boss of BYD's premium brand Denza", photo("m_denza", 1, "in", cap="Denza|BYD's premium brand"))
c.at("Even if a workshop had the part", P("repairer"))
c.at("Not always", say("Not always.", "ALWAYS", 170))
chapters.append(c)

# ---------------------------------------------------------------- problem 2: the wait
c = ch("ch03")
c.at(0, say("This isn't only a BYD problem.", "ONLY", 130))
c.at("In July 2026, the Australian Automotive Dealer Association", P("rights", cap="AADA review|July 2026"))
c.at("especially electric vehicles", P("ev"))
c.at("Dealers told the review that workshop backlogs", stat("6–8 WEEKS", "just to diagnose a fault", "AADA / Buchan review", red=True, count=False))
c.at("Not fix it", say("Not fix it. Just diagnose it.", "DIAGNOSE", 130))
c.at("Combine that with slow parts", P("waiting"))
c.at("no loan car", P("road"))
c.at("The report also pointed at the wave of new brands", P("dealer"))
c.at("Australia has more than seventy car brands", stat("70+", "car brands sharing ~1.2 million sales a year", "CarExpert"))
c.at("Denza, Geely, IM Motors and GAC", photo("m_denza", 2, "left"))
c.at("Not all of them have the parts warehouses", P("parts"))
chapters.append(c)

# ---------------------------------------------------------------- problem 3: cost
c = ch("ch04")
c.at(0, P("insurance"))
c.at("Here's what we can actually back up", say("Here's what we can actually back up.", "BACK", 120))
c.at("EVs and plug-in hybrids are generally more expensive", P("crash"))
c.at("A senior figure in BYD's collision repair network", P("repairer", cap="Paint & Panel|BYD collision repair network"))
c.at("That pushes insurance premiums up", P("insurance"))
c.at("The battery is the big one", P("battery"))
c.at("It's not just the battery, either", photo("m_shark6", 5, "in"))
c.at("A rear bumper isn't just plastic anymore", P("crash"))
c.at("A low-speed car park bump", P("crash"))
c.at("Insurance comparison site Compare the Market", bars("Average yearly premium", [["Dolphin", 1425], ["Corolla Hyb.", 1587],
     ["Sealion 7", 1770], ["RAV4 Hyb.", 1773], ["Shark 6", 2071, "red"]], None, "Compare the Market via CarExpert", prefix="$"))
c.at("but still well below the two Teslas", stat("$3,000+", "average premium · Tesla Model 3 and Model Y", "Compare the Market via CarExpert", red=True))
c.at("So the honest answer is", P("byd"))
c.at("It depends heavily on the model", say("It depends on the model.", "MODEL", 150))
chapters.append(c)

# ---------------------------------------------------------------- mid CTA
c = ch("ch05")
c.at(0, cta("Own a BYD? Tell us.", "Your repair story helps other Aussies decide"))
questions(c, ["How was your service?", "Good or bad?"], ["what your service and repair experience has been", "Good or bad"])
c.at("And if you want honest", P("byd"))
chapters.append(c)

# ---------------------------------------------------------------- recall
c = ch("ch06")
c.at(0, stat("32,009", "Shark 6 utes recalled · spare wheel assembly", BYD, red=True, tag="recall"))
c.at("BYD advised affected owners to remove the spare wheel", P("tyre"))
c.at("Recalls happen to every brand", P("dealer"))
c.at("A recall is actually the system working", say("A recall is the system working.", "WORKING", 130))
c.at("But for a brand already fighting a reputation", P("repairer"))
chapters.append(c)

# ---------------------------------------------------------------- the fix
c = ch("ch07")
c.at(0, say("Has BYD fixed it?", "FIXED", 160))
c.at("On the 20th of October 2026", stat("580,000+", "BYD and Denza parts held in Australia", "BYD Australia · 20 Oct 2026"))
c.at("That's around 95 per cent", stat("95%", "of parts kept in local stock", BYD))
c.at("The value of those parts is more than", stat("$25M+", "of parts on hand at any time", BYD))
c.at("spread across more than", P("parts", cap="4 warehouses|24,000+ m² in four cities"))
c.at("The biggest is in Melbourne", P("melbourne"))
c.at("BYD says dealers close to a warehouse", stat("24 HRS", "in-stock parts to dealers near a warehouse", BYD, count=False))
c.at("remote or rural areas within about a week", P("delivery"))
c.at("Importantly, BYD says it now keeps Blade battery packs", P("battery"))
c.at("and batteries are one of the slowest parts", P("ship"))
c.at("Chief operating officer Stephen Collins", say("\"Our commitment to Australian customers doesn't end at the handover. It starts there.\"", "STARTS THERE", 86))
c.at("BYD also set up its own approved collision repair network", P("repairer"))
c.at("That's a smart shortcut", P("tech"))
chapters.append(c)

# ---------------------------------------------------------------- your rights
c = ch("ch08")
c.at(0, P("waiting"))
c.at("Under the Australian Consumer Law", say("Australian Consumer Law", "CONSUMER LAW", 140))
c.at("manufacturers and importers must make spare parts", P("parts"))
c.at("The problem, as the dealer association's review", say("\"Reasonable\" is vague.", "REASONABLE", 150))
c.at("Until that happens, the best thing you can do", P("rights"))
c.at("contact the manufacturer's head office directly", P("phone"))
c.at("go to your state's fair trading office", P("rights", cap="If it drags on|Contact Fair Trading"))
c.at("There's also the Motor Vehicle Service", P("tech", cap="Since 2022|Repair information sharing scheme"))
c.at("But the Insurance Council has raised concerns", P("repairer"))
chapters.append(c)

# ---------------------------------------------------------------- verdict
c = ch("ch09")
c.at(0, say("Is the problem real? Yes.", "YES", 140))
c.at("Owners waited far too long for parts", P("waiting"))
c.at("Are BYD cars more expensive to repair", P("crash"))
c.at("but insurance on models like the Dolphin", photo("m_dolphin", 3, "right"))
c.at("And has it been fixed", P("parts"))
c.at("of parts and four warehouses", say("$25M of parts. 4 warehouses.", "$25M", 120))
c.at("The real test is whether owners notice", P("byd"))
c.at("Because a warehouse full of parts only helps", P("phone"))
questions(c, ["Nearest approved repairer?", "Service booking wait?", "Loan car policy?"],
          ["Where is the nearest approved collision repairer", "How long are current service bookings", "what's the loan car policy"])
c.at("The answers will tell you more", P("dealer"))
chapters.append(c)

# ---------------------------------------------------------------- end
c = ch("ch10", 2.5)
c.at(0, P("road"))
c.at("If this helped you", cta("If this helped, hit like", "and subscribe for honest Aussie car data"))
questions(c, ["Would you buy a BYD in 2026?"], ["would you buy a BYD in 2026"])
c.at("the next video is ten car brands", title("10 Car Brands in Serious Trouble", "Up next", "next video", "dealer"))
chapters.append(c)

CTX = ["crash", "byd", "parts", "repairer", "insurance", "byd", "repairer", "parts", "rights", "byd", "road"]
print(A.finish(chapters, "AUS02_BYD_Repairs.mp4", CTX, subtitles="AUS02.ass"))
