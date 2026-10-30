#!/usr/bin/env python3
"""AUS03 brands in trouble (2026 data): full edit, every shot anchored to the phrase it illustrates.
Run from the episode work folder (a/ = assets of aus03-brands, audio/, sfx/, trilha.wav):
    python3 build_aus03.py <narration_dir> > episode.json
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "engine"))
import aus_kit as A
from aus_kit import P, photo, stat, bars, say, cta, title, ch, questions, rank

PHOTOS = {
    "dealer": ["ai:ai_empty_dealer_day", "ai:ai_dealer_clearance", "h_dealer", "h_empty_showroom", "h_showroom"],
    "empty": ["ai:ai_empty_dealer_day", "ai:ai_luxury_empty", "h_empty_showroom"],
    "chinese": ["ai:ai_chinese_cars_lot", "ai:ai_showroom_ev_crowd", "m_geely", "m_zeekr", "m_omoda", "m_byd"],
    "port": ["ai:ai_chinese_cars_lot", "h_port", "h_parking"],
    "ev": ["h_ev"], "petrol": ["h_petrol"], "traffic": ["h_highway", "h_sydney", "h_melbourne"],
    "board": ["ai:ai_board_meeting", "h_chart"], "sale": ["ai:ai_dealer_clearance", "h_sale_sign"],
    "closed": ["h_closed"], "crash": ["ai:ai_crash_test", "h_crash_test", "h_seatbelt"],
    "service": ["ai:ai_service_centre", "ai:ai_parts_shelf", "h_mechanic"], "keys": ["h_keys", "h_contract", "h_handshake"],
    "money": ["h_money"], "family": ["ai:ai_family_driveway", "h_family_car"], "outback": ["ai:ai_offroad_heritage", "h_outback"],
    "used": ["h_used_cars", "h_parking"], "factory": ["h_factory"],
}
CLIPS = {
    "dealer": ["v_dealer/1", "v_parking/3"], "chinese": ["v_parking/3", "v_parking/1"], "port": ["v_parking/3", "v_port/2"],
    "ev": ["v_ev/1", "v_ev/2", "v_ev/3"], "traffic": ["v_highway/1", "v_highway/2", "v_highway/3", "v_city/1", "v_city/2", "v_city/3"],
    "board": ["v_chart/1", "v_chart/3"], "outback": ["v_offroad/1", "v_offroad/3", "v_dealer/3"], "service": ["v_mechanic/3"],
    "keys": ["v_signing/3"], "used": ["v_parking/1", "v_parking/2"], "family": ["v_road/1", "v_road/3"],
}
GENERIC = ["v_highway/1", "v_highway/2", "v_highway/3", "v_city/1", "v_city/2", "v_city/3", "v_road/1", "v_road/3",
           "v_port/1", "v_port/2", "v_parking/1", "v_parking/2", "v_dealer/3", "v_offroad/3"]
FALLBACK = {"empty": ["dealer"], "dealer": ["empty", "sale"], "chinese": ["port", "ev"], "port": ["chinese"], "board": ["dealer"],
            "sale": ["dealer"], "closed": ["empty"], "crash": ["service"], "service": ["keys"], "keys": ["service"],
            "money": ["sale"], "family": ["traffic"], "outback": ["traffic"], "used": ["dealer"], "factory": ["chinese"],
            "ev": ["chinese"], "petrol": ["traffic"], "traffic": ["family"]}
RES = ["m_deepal/1", "m_deepal/3", "m_kgm/1", "m_kgm/3", "m_alfa/1", "m_alfa/3", "m_suzuki_fronx/1", "m_suzuki_fronx/3",
       "m_jimny/1", "m_swift/1", "m_vw_troc/1", "m_vw_golf/1", "m_vw_troc/3", "m_forester/1", "m_outback/1", "m_forester/3",
       "m_xtrail/1", "m_qashqai/1", "m_patrol/1", "m_outlander/1", "m_asx/1", "m_triton/1", "m_jeep/1", "m_jeep/3",
       "m_grand_cherokee/1", "m_peugeot_5008/1", "m_peugeot_308/1", "m_peugeot_5008/3", "m_geely/1", "m_zeekr/1", "m_byd/1",
       "m_omoda/1", "m_xtrail/3", "m_outlander/3"]
A.setup(sys.argv[1], os.path.join(HERE, "skip.json"), PHOTOS, CLIPS, GENERIC, FALLBACK,
        ["traffic", "dealer", "chinese", "ev", "port", "family", "outback", "used", "keys", "service", "board", "petrol", "money", "sale"],
        reserved=RES)
VF = "FCAI VFACTS · Sept 2026"
chapters = []

# ---------------------------------------------------------------- hook
c = ch("ch00_hook", 0.6)
c.at(0, stat("16", "new Jeeps sold in Australia · September 2026", VF, red=True))
c.at("Not sixteen a day", say("Not a day. Not a week. A month.", "MONTH", 130))
c.at("across an entire country", photo("m_jeep", 1, "in"))
c.at("That same month, Jaguar sold zero", stat("0", "new Jaguars sold · September 2026", VF, red=True, count=False))
c.at("Peugeot sold eighty-nine", photo("m_peugeot_5008", 1, "left", cap="Peugeot|89 sales in September"))
c.at("Alfa Romeo sold twenty-one", photo("m_alfa", 1, "right", cap="Alfa Romeo|21 sales in September"))
c.at("Subaru was down more than forty-two", stat("-42.6%", "Subaru · September 2026", VF, red=True))
c.at("Mitsubishi, down forty-one", stat("-41.5%", "Mitsubishi · September 2026", VF, red=True))
c.at("Nissan's boss has openly called 2026", say("\"2026 is the low point.\"", "LOW POINT", 150))
c.at("Meanwhile, a Chinese brand most Aussies", stat("+870%", "Geely · September 2026 vs 2025", VF))
c.at("Australia's car market is going through", P("chinese"))
c.at("Today I'm counting down ten car brands", P("dealer"))
c.at("And if one of these is sitting in your driveway", P("family"))
questions(c, ["Your warranty?", "Your servicing?", "Your resale value?"], ["your warranty", "your servicing", "your resale value"])
c.at("if a brand pulls back or pulls out", title("10 Car Brands in Serious Trouble", "Australia · 2026", "real 2026 data", "empty"))
chapters.append(c)

# ---------------------------------------------------------------- context
c = ch("ch01")
c.at(0, P("board"))
c.at("Australians bought 108,778 new vehicles", stat("108,778", "new vehicles sold · September 2026", VF))
c.at("So the market isn't collapsing", P("traffic"))
c.at("What's changing is who they're buying from", say("What's changing is who they buy from.", "WHO", 120))
c.at("Look at the brands that grew", bars("Sept 2026 vs Sept 2025", [["Zeekr", 1608], ["Geely", 870], ["Omoda Jaecoo", 344],
     ["Leapmotor", 106], ["BYD", 61]], None, VF, prefix="+", suffix="%"))
c.at("now Australia's second best-selling brand", photo("m_byd", 1, "in", cap="BYD|#2 brand for 2026 so far"))
c.at("Now look at the other side", say("Now the other side.", "OTHER SIDE", 150))
c.at("Kia, down nineteen and a half", bars("Sept 2026 vs Sept 2025", [["Hyundai", 22.0, "red"], ["Kia", 19.5, "red"],
     ["Mazda", 18.9, "red"], ["Toyota", 3.5, "red"]], None, VF, prefix="-", suffix="%"))
c.at("Among the top ten brands, the only ones that grew", P("chinese"))
c.at("There's another big shift too", P("ev"))
c.at("electric vehicles made up 24.2 per cent", stat("24.2%", "EV share of new car sales · September 2026", "FCAI / EVC"))
c.at("Petrol sales fell thirty-six", stat("-36.2%", "petrol car sales · Sept 2026 vs 2025", "FCAI / EVC", red=True))
c.at("Diesel fell eighteen", P("petrol"))
c.at("If your range is mostly petrol and diesel", P("traffic"))
c.at("And the market is crowded", stat("~70", "brands fighting for ~1.2 million sales a year", "CarExpert", count=False))
c.at("So why is this happening now", say("Three forces, all at once.", "THREE", 140))
c.at("The first is price", P("chinese", cap="Force 1|Price"))
c.at("When a family can get a plug-in hybrid SUV", P("family"))
c.at("The second is fuel", P("petrol", cap="Force 2|Fuel and new rules"))
c.at("and the New Vehicle Efficiency Standard", P("board"))
c.at("The third is the sheer number of choices", P("dealer", cap="Force 3|Too many brands"))
c.at("A dealer body boss has already warned", P("empty"))
c.at("It's just being cut into thinner", P("port"))
c.at("So who's losing the most", say("Who's losing the most?", "LOSING", 150))
chapters.append(c)

# ---------------------------------------------------------------- 10 Deepal
c = ch("ch02")
c.at(0, rank(10, "Deepal", "m_deepal", 1, "-33.7% in Sept", "Changan's electric brand"))
c.at("But 2026 has been brutal", stat("594", "Deepal sales · Jan–May 2026", "CarExpert / VFACTS", red=True))
c.at("In September, it sold sixty-three", stat("63", "Deepal sales · September 2026", VF, red=True))
c.at("A big part of that was a stop-sale", photo("m_deepal", 3, "left", cap="Stop-sale|E07 'multitruck'"))
c.at("Losing a key model to a stop-sale", P("empty"))
c.at("The lesson here is simple", say("Chinese and electric isn't a guarantee.", "GUARANTEE", 120))
c.at("The newcomers are fighting each other", P("chinese"))
chapters.append(c)

# ---------------------------------------------------------------- 9 KGM
c = ch("ch03")
c.at(0, rank(9, "KGM (SsangYong)", "m_kgm", 1, "-37% in Sept", "New name, same fight"))
c.at("But in September 2026 it sold just 189", stat("189", "KGM sales · September 2026", VF, red=True))
c.at("KGM's strength has always been tough", photo("m_kgm", 3, "right"))
c.at("The problem is that this is exactly the space", P("chinese"))
c.at("and very sharp drive-away prices", P("sale"))
c.at("Changing a brand's name is hard enough", say("A new name in the most crowded market ever.", "CROWDED", 110))
chapters.append(c)

# ---------------------------------------------------------------- 8 Alfa
c = ch("ch04")
c.at(0, rank(8, "Alfa Romeo", "m_alfa", 3, "21 sales in Sept", "Beautiful cars, almost no buyers"))
c.at("In September 2026, Alfa Romeo sold twenty-one", stat("21", "Alfa Romeo sales · September 2026 (-59.6%)", VF, red=True))
c.at("Alfa sits inside Stellantis Australia", P("board"))
c.at("How long can a global company justify", P("empty"))
c.at("For now, Alfa Romeo is still here", P("service"))
c.at("its future in Australia will be decided in Europe", say("Decided in Europe, not in Aussie showrooms.", "EUROPE", 115))
chapters.append(c)

# ---------------------------------------------------------------- 7 Suzuki
c = ch("ch05")
c.at(0, rank(7, "Suzuki", "m_suzuki_fronx", 1, "-39.3% in Sept", "Small, cheap, fun – and under pressure"))
c.at("Suzuki built its name here on small", photo("m_swift", 1, "left"))
c.at("and of course the cult-favourite Jimny", photo("m_jimny", 1, "in"))
c.at("But by the end of May 2026", stat("-22%", "Suzuki sales · Jan–May 2026", "CarsGuide / VFACTS", red=True))
c.at("In September, they were down more than thirty-nine", stat("-39.3%", "Suzuki · September 2026", VF, red=True))
c.at("Part of it is safety ratings", P("crash"))
c.at("received a one-star ANCAP rating", stat("1 STAR", "Fronx ANCAP rating · rear seatbelt failure", "ANCAP / carsales", red=True, count=False))
c.at("Sales were halted while Suzuki's engineers", photo("m_suzuki_fronx", 3, "right", cap="Stop-sale|Investigation ongoing in March 2026"))
c.at("Suzuki's local boss even suggested", say("\"Up to one in five buyers\" scared off", "ONE IN FIVE", 110))
c.at("That's the brand's own estimate", P("crash"))
c.at("The other part is price", P("chinese"))
c.at("Even the Jimny was down twelve", stat("-12%", "Jimny sales · Jan–May 2026", "CarsGuide / VFACTS", red=True))
chapters.append(c)

# ---------------------------------------------------------------- 6 VW
c = ch("ch06")
c.at(0, rank(6, "Volkswagen", "m_vw_golf", 1, "-36.9% in Sept", "One of the world's biggest car makers"))
c.at("But in Australia, it's shrinking fast", stat("~29,000", "VW sales in 2025 (down 20%+)", "carsales", red=True, count=False))
c.at("By the end of May 2026 it was down another", stat("-17%", "Volkswagen · Jan–May 2026", "CarsGuide / VFACTS", red=True))
c.at("And in September, Volkswagen sold 1,599", stat("1,599", "VW sales · September 2026 (-36.9%)", VF, red=True))
c.at("Look inside those numbers", bars("Jan–May 2026 vs 2025", [["T-Roc", 55.9, "red"], ["T-Cross", 49, "red"], ["Amarok", 33, "red"]],
     None, "CarsGuide / VFACTS", prefix="-", suffix="%"))
c.at("At a launch event in May", photo("m_vw_troc", 1, "in"))
c.at("once you're selling fewer than ten thousand", say("Under 10,000 a year? You're niche.", "NICHE", 130))
c.at("And he made it clear Volkswagen doesn't want", P("board"))
c.at("The brand admits it has had gaps", photo("m_vw_troc", 3, "left"))
c.at("There's a new-generation T-Roc", P("ev"))
c.at("But the clock is ticking", say("The clock is ticking.", "TICKING", 160))
chapters.append(c)

# ---------------------------------------------------------------- mid CTA
c = ch("ch07")
c.at(0, cta("Real 2026 data. No rumours.", "A new Aussie car video every week"))
questions(c, ["Own one of these brands?", "Would you buy another?"], ["do you own one of the brands", "Would you buy another one"])
c.at("I read every comment", P("traffic"))
chapters.append(c)

# ---------------------------------------------------------------- 5 Subaru
c = ch("ch08")
c.at(0, rank(5, "Subaru", "m_forester", 1, "-42.6% in Sept", "Loyal owners, falling sales"))
c.at("Subaru has some of the most loyal owners", P("outback"))
c.at("Sales for the first five months were down", stat("-22.1%", "Subaru · Jan–May 2026", "CarExpert / VFACTS", red=True))
c.at("In September, Subaru sold 2,009", stat("2,009", "Subaru sales · September 2026 (-42.6%)", VF, red=True))
c.at("Subaru sold more than 46,000 cars in 2023", bars("Subaru yearly sales", [["2023", 46000], ["2024", 40604], ["2025", 39005, "red"]],
     None, "CarExpert"))
c.at("Now it has slipped behind Geely", photo("m_geely", 1, "right"))
c.at("Subaru's importer says this is partly planned", photo("m_outback", 1, "in"))
c.at("Managing director Blair Read", say("\"A rationalisation of the range.\"", "RATIONALISATION", 110))
c.at("the Forester and Outback were both replaced", photo("m_forester", 3, "left"))
c.at("Subaru says it will have nine models", stat("9", "Subaru models by end of 2026 · 5 hybrid or electric", "CarExpert"))
c.at("That's the plan", P("chinese"))
c.at("Subaru needs that new range to work", P("dealer"))
chapters.append(c)

# ---------------------------------------------------------------- 4 Nissan
c = ch("ch09")
c.at(0, rank(4, "Nissan", "m_xtrail", 1, "-33.7% to July", "From ~80,000 a year to fighting for survival"))
c.at("In 2012 it sold almost eighty thousand", stat("79,747", "Nissan sales in 2012 · 6th place", "CarExpert"))
c.at("To the end of July, Nissan had delivered", stat("15,445", "Nissan sales · Jan–Jul 2026 (-33.7%)", "CarExpert / VFACTS", red=True))
c.at("The Navara ute was down forty-nine", bars("Jan–Jul 2026 vs 2025", [["Qashqai", 73.5, "red"], ["Navara", 48.8, "red"], ["X-Trail", 15.1, "red"]],
     None, "CarExpert / VFACTS", prefix="-", suffix="%"))
c.at("In September, the brand was still down", stat("-30%", "Nissan · September 2026", VF, red=True))
c.at("Nissan has already cut the Juke", photo("m_qashqai", 1, "right"))
c.at("Globally, the company has been through", P("factory"))
c.at("And here's the remarkable part", say("Its own boss calls 2026 the bottom.", "BOTTOM", 125))
c.at("The plan includes hybrid X-Trails", photo("m_patrol", 1, "in", cap="Coming|New Patrol, hybrid X-Trail"))
c.at("When a brand's own boss calls this year", photo("m_xtrail", 3, "left"))
chapters.append(c)

# ---------------------------------------------------------------- 3 Mitsubishi
c = ch("ch10")
c.at(0, rank(3, "Mitsubishi", "m_outlander", 1, "-41.5% in Sept", "The value brand losing on value"))
c.at("In 2018 it sold almost 85,000", stat("84,944", "Mitsubishi sales in 2018 · its best year", "CarExpert"))
c.at("By the end of May 2026, Mitsubishi was down", stat("-26.4%", "Mitsubishi · Jan–May 2026", "CarsGuide / VFACTS", red=True))
c.at("And in September, it sold 2,769", stat("2,769", "Mitsubishi sales · September 2026 (-41.5%)", VF, red=True))
c.at("What went wrong", say("What went wrong?", "WRONG", 160))
c.at("The Pajero Sport and the Eclipse Cross", P("empty"))
c.at("The new ASX is now a rebadged Renault", photo("m_asx", 1, "right", cap="New ASX|695 sold Jan–May 2026"))
c.at("The Outlander, Mitsubishi's best seller", photo("m_outlander", 3, "in"))
c.at("the only Mitsubishi not going backwards", photo("m_triton", 1, "left"))
c.at("And here's the core problem", P("chinese"))
c.at("A new boss started in January", P("board"))
chapters.append(c)

# ---------------------------------------------------------------- 2 Jeep
c = ch("ch11")
c.at(0, rank(2, "Jeep", "m_jeep", 3, "16 sales in Sept", "A long, slow decline"))
c.at("Across the first eight months of the year", stat("378", "Jeep sales · Jan–Aug 2026", "CarsGuide", red=True))
c.at("Back in 2014, Jeep sold more than thirty thousand", bars("Jeep sales in Australia", [["2014", 30408], ["2024", 2377, "red"], ["Jan–Aug 2026", 378, "red"]],
     "-99%", "CarExpert / CarsGuide"))
c.at("The once-popular Grand Cherokee", photo("m_grand_cherokee", 1, "in", cap="Axed in 2025|Grand Cherokee"))
c.at("The dealer network has shrunk", stat("70+ → 44", "Jeep dealerships in Australia", "CarSauce", red=True, count=False))
c.at("But there's a twist", say("Then came the twist.", "TWIST", 160))
c.at("Stellantis, has partnered with Chinese giant Dongfeng", P("factory", cap="October 2026|Stellantis + Dongfeng"))
c.at("Reports say future Jeep and Peugeot models", P("chinese"))
c.at("So the brand famous for American off-roaders", P("outback"))
chapters.append(c)

# ---------------------------------------------------------------- 1 Peugeot
c = ch("ch12")
c.at(0, rank(1, "Peugeot", "m_peugeot_5008", 3, "Importer walked away", "The clearest warning sign"))
c.at("The numbers explain why", bars("Peugeot sales in Australia", [["2007", 8807], ["2025", 1350, "red"], ["Jan–May 2026", 373, "red"]],
     None, "The Beep / CarExpert"))
c.at("And in September 2026, it sold eighty-nine", stat("89", "Peugeot sales · September 2026", VF, red=True))
c.at("A facelifted 308 hatch was meant to arrive", photo("m_peugeot_308", 1, "right"))
c.at("Peugeot slashed prices across its passenger range", A.price("Peugeot 5008 GT Premium Hybrid", "$69,990", "$59,990",
     "drive-away before", "drive-away · July 2026", "-$10,000", "The Beep"))
c.at("Stellantis insists Peugeot is not leaving", P("board"))
c.at("But Inchcape already dropped Peugeot's sister brand", P("closed"))
c.at("Losing your importer is the clearest warning sign", say("Losing your importer is the clearest warning sign.", "WARNING", 110))
chapters.append(c)

# ---------------------------------------------------------------- bonus Jaguar
c = ch("ch13")
c.at(0, stat("0", "new Jaguars sold in Australia · September 2026", VF, red=True, count=False, tag="bonus"))
c.at("That's because Jaguar stopped selling new petrol cars", P("empty", cap="31 December 2025|Last new petrol Jaguars sold"))
c.at("Its new EVs are expected to cost", stat("~$300,000", "expected price of Jaguar's new EVs in Australia", "Man of Many", count=False))
c.at("Jaguar's local retailers are still servicing", P("service"))
c.at("But for now, a brand with nearly a century", P("empty"))
chapters.append(c)

# ---------------------------------------------------------------- what it means
c = ch("ch14")
c.at(0, P("family"))
c.at("First, the good news", say("You're not left on your own.", "NOT", 140))
c.at("Peugeot owners are being told the same", P("service"))
c.at("Second, the law is on your side", say("Australian Consumer Law", "CONSUMER LAW", 140))
c.at("must make spare parts and repair facilities", P("service"))
c.at("Third, the real risk is resale value", P("used"))
c.at("If you're buying one, use that to negotiate", P("sale"))
c.at("And if you're selling", P("keys"))
questions(c, ["Who backs the warranty?", "Nearest service centre?", "How fast are parts?"],
          ["How long is the warranty", "Where is the nearest service centre", "how quickly can they get common parts"])
c.at("And one more thing worth remembering", P("traffic"))
c.at("A Subaru Forester or a Volkswagen Golf", P("family"))
c.at("But when sales fall, dealers close", P("closed"))
c.at("will this brand still look after me", say("\"Will this brand still look after me in five years?\"", "FIVE YEARS", 105))
chapters.append(c)

# ---------------------------------------------------------------- end
c = ch("ch15", 2.5)
c.at(0, P("traffic"))
questions(c, ["Which brand leaves first?"], ["Which one do you think leaves first"])
c.at("If you got value from this", cta("If this helped, hit like", "and subscribe – we're tracking every month of 2026"))
c.at("the next video shows how Aussies", title("Aussies Are Fighting Back", "Faulty new cars – and winning", "next video", "keys"))
chapters.append(c)

CTX = ["dealer", "traffic", "chinese", "dealer", "empty", "crash", "dealer", "traffic", "outback", "factory", "chinese",
       "outback", "dealer", "empty", "service", "traffic"]
print(A.finish(chapters, "AUS03_Brands_In_Trouble_2026.mp4", CTX, subtitles="AUS03.ass"))
