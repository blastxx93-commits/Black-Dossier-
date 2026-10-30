#!/usr/bin/env python3
"""AUS04 faulty new cars (2026 cases): full edit, every shot anchored to the phrase it illustrates.
Run from the episode work folder (a/ = assets of aus04-faulty, audio/, sfx/, trilha.wav):
    python3 build_aus04.py <narration_dir> > episode.json
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "engine"))
import aus_kit as A
from aus_kit import P, photo, stat, bars, say, cta, title, ch, questions

PHOTOS = {
    "dealer": ["ai:ai_dealer_empty_desk", "h_dealer", "h_showroom"],
    "argue": ["ai:ai_owner_angry_dealer", "h_phone"],
    "byd": ["m_atto3", "m_sealion8", "m_shark6"],
    "service": ["ai:ai_car_on_hoist", "h_mechanic", "h_engine"],
    "rust": ["ai:ai_rusty_panel", "h_rust"],
    "court": ["ai:ai_tribunal_room", "h_court", "h_judge"],
    "docs": ["ai:ai_documents_tribunal", "ai:ai_fault_diary", "h_documents", "h_contract"],
    "phone": ["h_phone", "h_email"],
    "breakdown": ["ai:ai_family_stranded", "h_broken", "h_tow"],
    "dash": ["h_dashboard", "h_screen"],
    "crash": ["h_crash_test", "h_seatbelt"],
    "money": ["h_money"], "calendar": ["h_calendar"], "news": ["ai:ai_owner_news", "h_news"],
    "keys": ["h_keys"], "used": ["ai:ai_resale_yard", "h_used"], "parliament": ["h_parliament"],
    "recall": ["ai:ai_recall_letter", "ai:ai_compliance_plate"],
    "ford": ["m_ranger", "m_everest", "m_f150"], "traffic": [],
}
CLIPS = json.load(open(os.path.join(HERE, "clips.json")))
GENERIC = CLIPS.pop("_generic", [])
FALLBACK = {"dealer": ["argue", "keys"], "argue": ["phone", "dealer"], "byd": ["dealer"], "service": ["breakdown", "dash"],
            "rust": ["used"], "court": ["docs"], "docs": ["phone", "court"], "phone": ["docs"], "breakdown": ["service"],
            "dash": ["service"], "crash": ["breakdown"], "money": ["used", "docs"], "calendar": ["docs"], "news": ["phone"],
            "keys": ["dealer"], "used": ["dealer"], "parliament": ["court"], "recall": ["docs", "service"], "ford": ["dealer"],
            "traffic": ["breakdown", "keys"]}
RES = ["m_atto3/1", "m_atto3/3", "m_sealion8/1", "m_sealion8/3", "m_shark6/1", "m_shark6/3", "m_ranger/1", "m_ranger/3",
       "m_everest/1", "m_everest/3", "m_f150/1", "m_f150/3", "m_fronx/1", "m_fronx/3", "m_deepal/1", "m_deepal/3",
       "m_mazda_cx5/1", "m_mazda_cx5/3"]
A.setup(sys.argv[1], os.path.join(HERE, "skip.json"), PHOTOS, CLIPS, GENERIC, FALLBACK,
        ["traffic", "dealer", "service", "docs", "keys", "breakdown", "phone", "money", "used", "dash"], reserved=RES)
chapters = []

# ---------------------------------------------------------------- hook
c = ch("ch00_hook", 0.6)
c.at(0, stat("1,265", "\"2026\" BYDs that were actually built in 2025", "ABC / SMH · July 2026", red=True))
c.at("drove away in what they were told", photo("m_atto3", 1, "in", cap="BYD Atto 3|sold as a 2026 model"))
c.at("only to find out it had actually been built", photo("m_sealion8", 1, "left", cap="Built in 2025|sold as 2026"))
c.at("A whole model year older", say("A whole year older than the paperwork said.", "YEAR OLDER", 120))
c.at("A whole year of depreciation", P("used"))
c.at("BYD called it an administrative error", say("\"An administrative error.\"", "ERROR", 150))
c.at("Its first offer was eleven hundred", stat("$1,100", "BYD's first offer to owners", "ABC · July 2026", red=True))
c.at("Owners said no", P("argue"))
c.at("They went to the media", P("news"))
c.at("the offer more than tripled", A.price("BYD compensation", "$1,100", "$3,500", "first offer", "after owners pushed back",
     "x3.2", "ABC / BYD · July 2026"))
c.at("plus a full refund or a swap", P("keys"))
c.at("a Victorian buyer took a dealer all the way", P("rust"))
c.at("and won a full refund", P("court"))
c.at("The car industry's own dealers have admitted", P("dealer"))
c.at("the government has agreed to hit businesses", P("parliament"))
c.at("Aussie drivers are fighting back", title("Fighting Back Against Faulty New Cars", "Australia · 2026", "real 2026 cases", "argue"))
questions(c, ["The real 2026 cases", "Why refunds are so hard", "Your exact next steps"],
          ["the real 2026 cases", "why it's still so hard", "the exact steps"])
c.at("Because most Aussies don't know their rights", say("Most Aussies don't know their rights.", "RIGHTS", 130))
chapters.append(c)

# ---------------------------------------------------------------- the law
c = ch("ch01")
c.at(0, P("traffic"))
c.at("Australia doesn't have a specific lemon law", say("No \"lemon law\" in Australia.", "LEMON LAW", 140))
c.at("What we have instead is the Australian Consumer Law", P("docs"))
questions(c, ["Acceptable quality", "Fit for purpose", "Matches the description", "Lasts a reasonable time"],
          ["acceptable quality", "fit for purpose", "match the description", "last a reasonable time"])
c.at("The guarantees don't stop when the warranty stops", say("Your rights don't end with the warranty.", "DON'T END", 120))
c.at("If a major part fails earlier", P("service"))
c.at("If your car has a minor fault", P("service"))
c.at("If it has a major failure", say("Major failure = refund or replacement.", "REFUND", 120))
c.at("these rights cannot be excluded", P("docs"))
c.at("Not by the small print", P("docs"))
c.at("So what counts as a major failure", P("dealer"))
c.at("Or if it's substantially unfit", P("breakdown"))
c.at("Or if it's unsafe", P("crash"))
c.at("In real life, that could be an engine", P("service"))
c.at("Electrical faults that leave you stranded", P("breakdown"))
c.at("Or a car that spends more time in the workshop", P("service"))
c.at("a series of minor faults can add up", say("Minor faults can add up to a major failure.", "MAJOR FAILURE", 115))
c.at("If your car keeps going back", P("service"))
c.at("It sounds simple", P("argue"))
chapters.append(c)

# ---------------------------------------------------------------- case 1 BYD
c = ch("ch02")
c.at(0, title("Case 1", "BYD and the wrong build year", "July 2026", "byd"))
c.at("In July 2026, the ABC and the Sydney Morning Herald", P("news"))
c.at("The affected models included", photo("m_shark6", 1, "in", cap="BYD Shark 6|one of the affected models"))
c.at("BYD said around 3,800 vehicles", bars("BYD build-date error", [["Listed wrongly", 3800, "red"], ["Sold or allocated", 1200]],
     None, "BYD via ABC · July 2026"))
c.at("BYD's explanation was that it had used the date", photo("m_atto3", 3, "right"))
c.at("called it an administrative error", say("\"No deceit.\"", "DECEIT", 150))
c.at("To be fair to BYD", photo("m_sealion8", 3, "left"))
c.at("the correct build date was in the vehicle", P("recall"))
c.at("But here's why owners were angry", P("argue"))
c.at("A car's build year affects its resale value", P("used"))
c.at("Erin Turner from the Consumer Policy", say("\"An extra year of depreciation.\"", "DEPRECIATION", 115))
c.at("The Insurance Council of Australia even advised", P("docs"))
c.at("BYD's first offer was $1,100", stat("$1,100", "first offer", "BYD · July 2026", red=True))
c.at("Within days, BYD added the option", P("keys"))
c.at("Then it raised the payment to $3,500", stat("$3,500", "final payment – backdated for everyone", "BYD · July 2026"))
c.at("Owners could also swap their car", photo("m_shark6", 3, "in"))
c.at("By late July, BYD said around seventy-two", stat("72%", "of owners took the $3,500 payment", "BYD · late July 2026"))
c.at("more than 350 had chosen a refund", stat("350+", "owners chose a refund or a replacement", "BYD · July 2026"))
c.at("That's what fighting back looks like", say("That's what fighting back looks like.", "FIGHTING BACK", 120))
c.at("They got a better deal for every owner", P("keys"))
chapters.append(c)

# ---------------------------------------------------------------- case 2 rust
c = ch("ch03")
c.at(0, title("Case 2", "The rusty car that went to the Supreme Court", "Victoria · 2026", "rust"))
c.at("a Victorian buyer discovered", P("rust"))
c.at("The tribunal found it was a clear breach", P("court"))
c.at("ordered a full refund", say("Full refund ordered.", "FULL REFUND", 140))
c.at("The dealer didn't accept that", P("dealer"))
c.at("And the Supreme Court of Victoria backed the buyer", P("court", cap="Supreme Court of Victoria|backed the buyer"))
c.at("Then, in January 2026, another buyer won", P("docs"))
c.at("The consumer guarantees don't only apply", P("used"))
c.at("If you buy a used car from a licensed dealer", P("used"))
c.at("The lesson from both cases is simple", say("\"No\" isn't the end of the road.", "NO", 130))
c.at("Tribunals and courts can", P("court"))
chapters.append(c)

# ---------------------------------------------------------------- recalls
c = ch("ch04")
c.at(0, P("recall"))
c.at("Because this year, there have been a lot", P("service"))
c.at("In September, BYD recalled 32,009", stat("32,009", "BYD Shark 6 utes recalled · spare wheel assembly", "Product Safety Australia · 2026", red=True))
c.at("Owners were told they could remove", P("service"))
c.at("In October, Ford recalled 1,085", photo("m_ranger", 1, "in", cap="Ford Ranger & Everest|1,085 recalled · October 2026"))
c.at("the 10.1-inch centre screen can go blank", photo("m_everest", 1, "right"))
c.at("which means the reversing camera image", P("dash"))
c.at("Ford also recalled the big F-150", photo("m_f150", 1, "left", cap="Ford F-150|fire-risk recall · October 2026"))
c.at("CarExpert notes that Ford issues more recalls", photo("m_f150", 3, "in"))
c.at("Suzuki's new Fronx small SUV", photo("m_fronx", 1, "in", cap="Suzuki Fronx|halted after ANCAP seatbelt failure"))
c.at("after a rear seatbelt failure", P("crash"))
c.at("And Deepal had a stop-sale order", photo("m_deepal", 1, "right", cap="Deepal|stop-sale order on the E07"))
c.at("A recall is the manufacturer admitting a fault", P("service"))
c.at("But a recall doesn't cancel your consumer rights", say("A recall doesn't cancel your rights.", "DOESN'T CANCEL", 120))
c.at("If the fix can't be done within a reasonable time", P("calendar"))
c.at("You can check whether your car is affected", P("phone"))
chapters.append(c)

# ---------------------------------------------------------------- mid CTA
c = ch("ch05")
c.at(0, P("argue"))
c.at("Tell me your story in the comments", cta("Tell me your story in the comments", "Did you win against the dealer?"))
c.at("hit subscribe and turn on notifications", cta("Subscribe & turn on notifications", "Honest videos for Aussie drivers"))
c.at("Now, let's talk about why this is still so hard", P("dealer"))
chapters.append(c)

# ---------------------------------------------------------------- why it's hard
c = ch("ch06")
c.at(0, P("calendar"))
c.at("In July 2026, the Australian Automotive Dealer Association", P("docs", cap="AADA review|July 2026"))
c.at("Its conclusion was blunt", say("\"No longer delivering fair or timely outcomes.\"", "NO LONGER", 100))
c.at("The review found that vague definitions", P("court"))
c.at("leaving drivers without their cars", P("breakdown"))
c.at("workshop backlogs could stretch six to eight weeks", stat("6–8 weeks", "just to DIAGNOSE a fault", "AADA review · July 2026", red=True, count=False))
c.at("Not fix it. Just find out", P("service"))
c.at("There's another twist", P("dealer"))
c.at("But the dealer didn't build the car", P("service"))
c.at("So it's calling on the federal government", P("parliament"))
c.at("And it's not just about cars", P("phone"))
c.at("making a complaint about a faulty car can involve", stat("60", "steps to complain about a faulty car", "CPRC / Consumer Action", red=True))
c.at("No wonder so many people give up", P("docs"))
chapters.append(c)

# ---------------------------------------------------------------- Mazda
c = ch("ch07")
c.at(0, P("court"))
c.at("Between 2013 and 2017, nine customers", photo("m_mazda_cx5", 1, "in", cap="Mazda|9 customers, 2013–2017"))
c.at("One car had its engine replaced three times", stat("3", "engine replacements on one car", "ACCC v Mazda", red=True))
c.at("Mazda refused, or offered only part", photo("m_mazda_cx5", 3, "left"))
c.at("took Mazda to the Federal Court", P("court"))
c.at("forty-nine false or misleading statements", stat("49", "false or misleading statements", "Federal Court"))
c.at("Mazda was ordered to pay $11.5 million", stat("$11.5M", "penalties ordered against Mazda · 2024", "Federal Court", red=True))
c.at("That case is the reason every car company", P("dealer"))
c.at("not our policy", say("\"Not our policy\" isn't the law.", "ISN'T THE LAW", 120))
chapters.append(c)

# ---------------------------------------------------------------- new rules
c = ch("ch08")
c.at(0, P("parliament"))
c.at("In November 2025, the state and federal", P("parliament", cap="Consumer affairs ministers|November 2025"))
c.at("The plan includes civil penalties", say("Civil penalties are coming.", "PENALTIES", 140))
c.at("Right now, a business that wrongly refuses", P("money"))
c.at("Penalties would change that maths", P("money"))
c.at("supplier indemnification", P("dealer"))
c.at("That matters to you, because a dealer", P("keys"))
c.at("Treasury is now drafting the new laws", P("docs"))
c.at("Refusing to fix a faulty car", say("Refusing to fix it will cost more.", "COST MORE", 125))
chapters.append(c)

# ---------------------------------------------------------------- steps
c = ch("ch09")
c.at(0, title("What to do", "if your new car is a lemon", "step by step", "docs"))
c.at("Step one: document everything", say("1 · Document everything", "1", 130))
c.at("Take photos and videos of the problem", P("dash"))
c.at("Keep every invoice and job card", P("docs"))
c.at("Step two: put it in writing", say("2 · Put it in writing", "2", 130))
c.at("A simple trick", P("phone"))
c.at("as discussed today", say("\"As discussed today…\"", "AS DISCUSSED", 130))
c.at("Keep a fault diary too", P("docs"))
c.at("If a tribunal ever has to decide", P("court"))
c.at("Step three: contact the dealer", say("3 · Dealer + head office", "3", 130))
c.at("It keeps everyone accountable", P("dealer"))
c.at("Step four: use the right words", say("4 · Use the right words", "4", 130))
c.at("Say you're making a claim", say("\"A claim under the consumer guarantees of the ACL\"", "CONSUMER GUARANTEES", 95))
c.at("If the fault is serious", P("argue"))
c.at("Step five: know what they can't do", say("5 · Know what they can't do", "5", 125))
c.at("You don't have to pay anything", P("money"))
c.at("And here's a myth worth busting", P("service"))
c.at("around forty per cent of new car owners", stat("40%", "think they must service at the dealer – you don't", "owner survey", red=True))
c.at("Using a qualified independent mechanic", P("service"))
c.at("Step six: if you get nowhere", say("6 · Fair trading, then tribunal", "6", 120))
c.at("take it to your state tribunal", P("court"))
questions(c, ["NCAT · NSW", "VCAT · Victoria", "QCAT · Queensland"], ["NCAT in New South Wales", "VCAT in Victoria", "QCAT in Queensland"])
c.at("Tribunal fees are usually modest", P("docs"))
c.at("You can also report the business", P("phone"))
c.at("don't be afraid to go public", P("news"))
chapters.append(c)

# ---------------------------------------------------------------- resale
c = ch("ch10")
c.at(0, P("used"))
c.at("even a paperwork problem can knock thousands", P("money"))
c.at("A car with a history of major faults", P("used"))
c.at("think about the end game", P("keys"))
c.at("And if you're offered compensation", P("money"))
c.at("You're allowed to ask for that same evidence", P("docs"))
c.at("And there's a lesson here for anyone buying", P("dealer"))
c.at("check the build date on the compliance plate", P("recall"))
c.at("Ask the dealer to confirm in writing", P("docs"))
c.at("And if you're buying second-hand", P("used"))
c.at("Five minutes of checking", say("5 minutes before vs months after.", "MONTHS", 120))
chapters.append(c)

# ---------------------------------------------------------------- end
c = ch("ch11", 2.5)
c.at(0, P("traffic"))
c.at("BYD owners more than tripled", stat("x3", "BYD owners' compensation after pushing back", "July 2026"))
c.at("A Victorian buyer won a full refund", P("court"))
c.at("And new penalties are on the way", P("parliament"))
c.at("The system is slow, but the law is on your side", say("The law is on your side.", "YOUR SIDE", 140))
c.at("If this video helped you, share it", cta("Share it with someone buying a car", "It could save them thousands"))
c.at("Hit like, subscribe", cta("Like · Subscribe", "and tell me your lemon story"))
c.at("And in the next video", title("Tesla Cancelled the Cybertruck", "for Australia – after 7 years of deposits", "next video", "keys"))
chapters.append(c)

CTX = ["argue", "docs", "byd", "rust", "service", "argue", "dealer", "court", "parliament", "docs", "used", "traffic"]
print(A.finish(chapters, "AUS04_Faulty_Cars_2026.mp4", CTX, subtitles="AUS04.ass"))
