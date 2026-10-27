#!/usr/bin/env python3
"""EP01 Apalachin: full edit. Every shot is anchored to the phrase it illustrates.

Run from the folder that holds a/ (images + words), audio/, sfx/, trilha.wav:
    python3 build_ep01.py <script_dir> > episode.json
"""
import json, os, subprocess, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "engine"))
from cues import Chapter

SCRIPT = sys.argv[1]

# --- sound levels (lower than the test: effects sit under the voice) ---
SFX = {"type": ("sfx/typewriter.wav", -24), "hit": ("sfx/hit.wav", -20),
       "whoosh": ("sfx/whoosh.wav", -27), "stamp": ("sfx/stamp.wav", -19)}


def fx(name, at=0.0, extra=0):
    f, g = SFX[name]
    return {"file": f, "gain": g + extra, "at": at}


def img(path, move="in", cap=None, focus=None, **kw):
    s = {"type": "image", "src": "a/" + path, "move": move}
    if cap: s["caption"] = cap
    if focus: s["focus"] = focus
    s.update(kw)
    return s


def ai(name, move="in", **kw):
    return img("ai/" + name, move, **kw)


def typer(text, size=60, sound=True):
    s = {"type": "typewriter", "text": text, "size": size}
    if sound: s["sfx"] = [fx("type", 0.1)]
    return s


def say(text, size=150, hit=True):
    s = {"type": "statement", "text": text, "size": size}
    if hit: s["sfx"] = [fx("hit")]
    return s


def doc(text, stamp=None):
    s = {"type": "document", "text": text}
    if stamp: s["stamp"] = stamp
    return s


def card(num, title):
    return {"type": "chapter", "num": num, "title": title, "sfx": [fx("whoosh")]}


def black():
    return {"type": "black"}


def counter(to, label, prefix="", suffix=""):
    return {"type": "counter", "to": to, "label": label, "prefix": prefix, "suffix": suffix}


def timeline(items):
    return {"type": "timeline", "items": items}


PHOTOS = {"Vito Genovese": ("ch03_vito_genovese/1_commons.jpg", [0.5, 0.15]),
          "Carlo Gambino": ("ch05_carlo_gambino/1_commons.jpg", [0.5, 0.3]),
          "Joseph Profaci": ("ch05_joseph_profaci/1_loc.jpg", [0.5, 0.3]),
          "Carmine Galante": ("ch02_carmine_galante/1_commons.jpg", [0.5, 0.25]),
          "Frank Costello": ("ch01_frank_costello/2_commons.jpg", [0.5, 0.3]),
          "Joseph Valachi": ("ch08_valachi_1963/1_commons.jpg", [0.5, 0.3])}


def dossier(name, label="SUBJECT", stamp=None, **fields):
    s = {"type": "dossier", "name": name, "label": label,
         "fields": {k.replace("_", " "): v for k, v in fields.items()}, "sfx": [fx("whoosh")]}
    if name in PHOTOS:
        s["photo"] = "a/" + PHOTOS[name][0]
        s["focus"] = PHOTOS[name][1]
    if stamp:
        s["stamp"] = stamp
        s["sfx"].append(fx("stamp", 1.2))
    return s


# reusable images
HOOVER_DESK = img("ch01_hoover_portrait/3_commons.jpg", "in", focus=[0.5, 0.25])
HOOVER_PORT = img("ch01_hoover_portrait/1_commons.jpg", "down", focus=[0.5, 0.12])
HOOVER_EVENT = img("ch01_hoover_portrait/2_commons.jpg", "in", focus=[0.4, 0.3])
JUSTICE = img("ch07_fbi_building/3_commons.jpg", "up", focus=[0.5, 0.4])
JUSTICE_DOOR = img("ch07_fbi_building/1_commons.jpg", "in", focus=[0.5, 0.4])
GMAN = img("ch01_g_men_1930s/1_commons.jpg", "out", focus=[0.5, 0.35])
FARM_SILOS = img("ch02_southern_tier_farm/2_loc.jpg", "in")
FARM_SILOS2 = img("ch02_southern_tier_farm/3_loc.jpg", "left")
MEET1, MEET2 = ai("ch00_apalachin_meeting_1.jpg", "in"), ai("ch00_apalachin_meeting_2.jpg", "right")
ROAD1, ROAD2 = ai("ch00_country_road_1.jpg", "in"), ai("ch00_country_road_2.jpg", "in")
TROOP1, TROOP2 = ai("ch00_state_trooper_1.jpg", "in"), ai("ch00_state_trooper_2.jpg", "left")
RUN1, RUN2 = ai("ch00_pasture_woods_1.jpg", "in"), ai("ch00_pasture_woods_2.jpg", "right")
BLOCK1, BLOCK2 = ai("ch05_police_roadblock_1.jpg", "in"), ai("ch05_police_roadblock_2.jpg", "in")
BARR1, BARR2 = ai("ch06_police_barracks_1.jpg", "in"), ai("ch06_police_barracks_2.jpg", "left")
CAR_TEAL = img("ch00_cars_1957/4_commons.jpg", "left")
CAR_FINS = img("ch00_cars_1957/2_loc.jpg", "in")
CAR_ROW = img("ch00_cars_1957/3_openverse.jpg", "right")
MOTEL = img("ch04_motel_1950s/1_commons.jpg", "in")
BUTCHER = img("ch04_butcher_shop/1_commons.jpg", "in")
PRESS = img("ch07_newspaper_press/2_commons.jpg", "in")
TV = img("ch01_tv_1950s/1_commons.jpg", "in")
COURT = img("ch07_courthouse/1_commons.jpg", "in", focus=[0.5, 0.4])
COURT2 = img("ch07_courthouse/3_commons.jpg", "up", focus=[0.5, 0.4])
COURT3 = img("ch07_courthouse/4_commons.jpg", "in", focus=[0.5, 0.4])
BOTTLING = img("ch02_bottling_plant/2_openverse.jpg", "in")
CPW = img("ch03_central_park_west/1_commons.jpg", "left")
GENOVESE_IMG = img("ch03_vito_genovese/1_commons.jpg", "in", focus=[0.5, 0.15])
COSTELLO_IMG = img("ch01_frank_costello/2_commons.jpg", "in", focus=[0.5, 0.3])
KEFAUVER = img("ch01_kefauver_hearing/2_commons.jpg", "in", cap="Kefauver Committee, 1951")
VALACHI = img("ch08_valachi_1963/1_commons.jpg", "in", focus=[0.5, 0.3], cap="Joseph Valachi, U.S. Senate, 1963")
VALACHI2 = img("ch08_valachi_1963/2_commons.jpg", "in", focus=[0.5, 0.3])

BARBARA = dict(name="Joseph Barbara", label="THE HOST", Born="1905, Sicily", Business="Canada Dry distributor")
CROSWELL = dict(name="Edgar Croswell", label="SERGEANT", Agency="N.Y. State Police")


def ch(name, title_tail=0.8):
    return Chapter(name, f"{SCRIPT}/{name}.txt", f"a/words/{name}.words.json", f"audio/{name}.wav", tail=title_tail)


chapters = []

# ---------------------------------------------------------------- HOOK
c = ch("ch00_hook", 1.6)
c.at(0, dict(typer("NOVEMBER 14, 1957\nAPALACHIN, NEW YORK"), fade_in=0.6))
c.at("A cold, gray Thursday", dict(FARM_SILOS, caption="Southern Tier, New York"))
c.at("Up a muddy country road", ROAD1)
c.at("behind a stone house", MEET2)
c.at("Cadillacs", dict(CAR_TEAL, xfade=0.2))
c.at("Lincolns", dict(CAR_FINS, xfade=0.2))
c.at("Imperials", dict(CAR_ROW, xfade=0.2))
c.at("Their license plates read", typer("NEW YORK · NEW JERSEY · OHIO\nILLINOIS · TEXAS\nCALIFORNIA · FLORIDA", 58))
c.at("Inside, around a barbecue pit", MEET1)
c.at("stand some of the most", dossier("Vito Genovese", "GUEST", City="New York"))
c.at("in the United States", dossier("Joseph Profaci", "GUEST", City="Brooklyn"))
c.at("And then, someone looks", ROAD2)
c.at("sees a car that should not", dict(TROOP2, sfx=[fx("hit", 0.6)]))
c.at("Within minutes, men in silk", RUN1)
c.at("Crashing through the brush", RUN2)
c.at("Bosses who commanded small armies", dict(RUN1, move="left"))
c.at("And waiting for them at the bottom", BLOCK2)
c.at("one stubborn state trooper", TROOP1)
c.at("a man the FBI had ignored", dossier(**CROSWELL))
c.at("The meeting never even really began", MEET2)
c.at("the most powerful lawman in America", dict(HOOVER_DESK, caption="J. Edgar Hoover, FBI Director"))
c.at("brushed aside for decades", HOOVER_PORT)
c.at("The Mafia was real", say("The Mafia was real."))
c.at("And it was national", say("And it was national.", hit=False))
c.at("And the strangest part", COURT)
c.at("Almost nobody went to prison", say("Almost nobody went to prison.", 120, hit=False))
c.at("This is Black Dossier", black())
c.at("is Apalachin", {"type": "title", "title": "Apalachin", "subtitle": "The day the Mafia was exposed",
                      "file": "FILE No. 001", "stamp": "CLASSIFIED", "fade_out": 0.8,
                      "sfx": [fx("whoosh"), fx("stamp", 0.9)]})
chapters.append(c)

# ---------------------------------------------------------------- CH 1
c = ch("ch01")
c.at(0, card(1, "The man who said it didn't exist"))
c.at("To understand why one afternoon", dict(MEET1, move="out"))
c.at("the man who ran American", dict(HOOVER_DESK, caption="J. Edgar Hoover"))
c.at("By 1957, J. Edgar Hoover", dict(JUSTICE, caption="Department of Justice, Washington"))
c.at("He had built its legend", img("ch01_g_men_1930s/3_commons.jpg", "left"))
c.at("chasing bank robbers", img("ch01_dillinger/3_commons.jpg", "in", focus=[0.5, 0.35], caption="John Dillinger"))
c.at("Dillinger", typer("DILLINGER\nBABY FACE NELSON\nPRETTY BOY FLOYD", 64))
c.at("His agents were heroes", GMAN)
c.at("But on one subject", HOOVER_PORT)
c.at("When people spoke of a national", MEET2)
c.at("Hoover pushed back", HOOVER_EVENT)
c.at("they were local problems", TROOP2)
c.at("The FBI had bigger enemies", typer("COMMUNISTS\nSPIES\nSUBVERSIVES", 72))
c.at("Not everyone agreed", black())
c.at("At the Federal Bureau of Narcotics", doc("FEDERAL BUREAU OF NARCOTICS\n\nMEMORANDUM\n\nSubject: Network of Sicilian and Italian-American criminals moving heroin, money and favors across state lines.", "CONFIDENTIAL"))
c.at("And in 1950 and 1951", typer("1950 – 1951\nU.S. SENATE", 70))
c.at("led by Estes Kefauver", KEFAUVER)
c.at("took the question to television", TV)
c.at("Frank Costello, refused", dossier("Frank Costello", "WITNESS", City="New York"))
c.at("So the cameras showed only his hands", img("ch01_kefauver_hearing/2_commons.jpg", "in", focus=[0.5, 0.95]))
c.at("The Kefauver Committee concluded", say("A nationwide crime syndicate did exist.", 110))
c.at("And still, the FBI kept", JUSTICE_DOOR)
c.at("Historians have argued", typer("WHY?", 110, sound=False))
c.at("Some point to Hoover's obsession", dict(HOOVER_DESK, move="out"))
c.at("Others point to his worry", HOOVER_EVENT)
c.at("Whatever the reason", JUSTICE)
c.at("would soon gather on a hill", MEET1)
c.at("But one state trooper", TROOP1)
chapters.append(c)

# ---------------------------------------------------------------- CH 2
c = ch("ch02")
c.at(0, card(2, "The bottler on McFall Road"))
c.at("Apalachin sits in New York's", dict(FARM_SILOS, caption="Southern Tier, New York"))
c.at("Locals pronounce it", typer("AP-UH-LAY-KIN", 90))
c.at("In the 1950s it was rolling", FARM_SILOS2)
c.at("And on one of those roads", ROAD2)
c.at("lived a man named Joseph Barbara", dossier(**BARBARA))
c.at("Barbara was born in 1905", img("ch02_castellammare/1_commons.jpg", "in", cap="Castellammare del Golfo, Sicily"))
c.at("That town matters", img("ch02_castellammare/4_commons.jpg", "right"))
c.at("It produced an entire generation", img("ch02_castellammare/3_openverse.jpg", "in"))
c.at("The men who would later lead", typer("BROOKLYN · BUFFALO", 80, sound=False))
c.at("Barbara came to America young", img("ch02_prohibition/1_commons.jpg", "in"))
c.at("Over the years he was arrested", doc("SUBJECT: BARBARA, JOSEPH\nBORN: 1905, CASTELLAMMARE DEL GOLFO\n\nARRESTS: MORE THAN ONE\nNAMED IN: SERIOUS INVESTIGATIONS\nCONVICTIONS: NOTHING STUCK", "FILE"))
c.at("By the 1950s, Joseph Barbara looked", BOTTLING)
c.at("He owned a large estate", MEET2)
c.at("And he had a lot of guests", MEET1)
c.at("far from New York City", CPW)
c.at("For years, it had been used", dict(MEET2, move="in"))
c.at("Somebody noticed", say("Somebody noticed.", hit=False))
c.at("His name was Edgar Croswell", dossier(**CROSWELL))
c.at("Croswell was not a celebrity", TROOP1)
c.at("Barbara's official record", TROOP2)
c.at("he simply had a feeling", typer("\"...the big mobster in the area.\"", 58))
c.at("So he watched", ROAD1)
c.at("In 1956, Croswell pulled over", BLOCK1)
c.at("Carmine Galante", dossier("Carmine Galante", "SUBJECT", Family="Bonanno", City="Brooklyn"))
c.at("Why would a Brooklyn gangster", typer("Why would a Brooklyn gangster be leaving\na soft drink distributor's house?", 50))
c.at("Croswell kept asking", ROAD2)
c.at("But the following year", MEET1)
chapters.append(c)

# ---------------------------------------------------------------- CH 3
c = ch("ch03")
c.at(0, card(3, "1957. The year the underworld shook"))
c.at("To understand why so many bosses", MEET1)
c.at("what happened in New York", ai("ch03_park_sheraton_2.jpg", "left"))
c.at("For years, the city's underworld", CPW)
c.at("One of the most powerful was Frank", dossier("Frank Costello", "BOSS", City="New York"))
c.at("Costello was called the Prime", KEFAUVER)
c.at("On the night of May 2nd", typer("MAY 2, 1957\nCENTRAL PARK WEST"))
c.at("walked into the lobby", CPW)
c.at("A man stepped out of the shadows", black())
c.at("He survived", say("He survived.", hit=False))
c.at("In his pocket, police found", doc("Found in Costello's pocket:\n\nA slip of paper.\nHandwritten figures.\n\nLater traced to the earnings of a new Las Vegas casino.", "EVIDENCE"))
c.at("the Tropicana", ai("ch03_tropicana_vegas_1.jpg", "in", focus=[0.5, 0.6]))
c.at("Costello refused to name", COSTELLO_IMG)
c.at("The man most widely believed", dossier("Vito Genovese", "SUBJECT", Family="Luciano family", City="New York"))
c.at("Ambitious, patient, and ruthless", GENOVESE_IMG)
c.at("Lucky Luciano's family", img("ch03_lucky_luciano/1_commons.jpg", "in", cap="Charles 'Lucky' Luciano"))
c.at("Then, on October 25th", typer("OCTOBER 25, 1957"))
c.at("Albert Anastasia, boss of", dossier("Albert Anastasia", "BOSS", City="New York"))
c.at("was killed in the barbershop", ai("ch03_park_sheraton_1.jpg", "in"))
c.at("The case was never solved", say("Never solved.", hit=False))
c.at("In just six months", timeline([["MAY 1957", "Costello shot"], ["OCT 1957", "Anastasia killed"], ["NOV 1957", "Apalachin"]]))
c.at("There were questions", MEET2)
c.at("Who would control Anastasia's", dossier("Carlo Gambino", "SUBJECT", City="New York"))
c.at("in Havana, Cuba", img("ch03_havana_1950s/1_commons.jpg", "left"))
c.at("To the narcotics trade", typer("HAVANA · NARCOTICS · TRUCKING", 60, sound=False))
c.at("To the trucking business", ai("ch03_garment_district_1.jpg", "in"))
c.at("According to most accounts", GENOVESE_IMG)
c.at("A gathering where bosses", MEET1)
c.at("The meeting needed a host", MEET2)
c.at("Joseph Barbara offered his home", dossier(**BARBARA))
c.at("The arrangements were reportedly", dossier("Russell Bufalino", "ORGANIZER", Region="Pennsylvania"))
c.at("The date was set", typer("THURSDAY\nNOVEMBER 14, 1957"))
c.at("Bosses from New York", CAR_TEAL)
c.at("But the man they should", TROOP1)
c.at("He was standing in a motel lobby", MOTEL)
chapters.append(c)

# ---------------------------------------------------------------- CH 4
c = ch("ch04")
c.at(0, card(4, "Room reservations"))
c.at("On November 13th", typer("NOVEMBER 13, 1957\nVESTAL, NEW YORK"))
c.at("Sergeant Croswell was at the Parkway", MOTEL)
c.at("he noticed a familiar young man", img("ch04_motel_1950s/2_loc.jpg", "left"))
c.at("It was Joseph Barbara Junior", dossier("Joseph Barbara Jr.", "THE SON"))
c.at("The younger Barbara was reserving", doc("PARKWAY MOTEL, VESTAL, N.Y.\nNovember 13, 1957\n\nRooms reserved: several\nFor: out-of-town guests", "NOTED"))
c.at("For most police officers", TROOP2)
c.at("But Croswell knew who Joseph", dossier(**BARBARA))
c.at("And he knew who had visited", dossier("Carmine Galante", "VISITOR, 1956", Family="Bonanno"))
c.at("Then came another detail", BUTCHER)
c.at("Roughly two hundred pounds", counter(200, "pounds of steaks and chops", prefix="~"))
c.at("Rooms for out-of-town guests", MOTEL)
c.at("A feast big enough", BUTCHER)
c.at("At the home of a man", MEET2)
c.at("Croswell didn't have a crime", say("No crime. No warrant.", 130, hit=False))
c.at("What he had was a hunch", TROOP1)
c.at("So the next morning", ROAD1)
chapters.append(c)

# ---------------------------------------------------------------- CH 5
c = ch("ch05")
c.at(0, card(5, "The roadblock"))
c.at("On November 14th, Croswell", TROOP1)
c.at("Trooper Vincent Vasisko", typer("SGT. EDGAR CROSWELL\nTPR. VINCENT VASISKO\nTWO U.S. TREASURY AGENTS", 52))
c.at("They drove up McFall Road", ROAD1)
c.at("What they saw stopped them cold", dict(MEET1, sfx=[fx("hit", 0, -2)]))
c.at("Parked around Barbara's property", CAR_TEAL)
c.at("License plates from all over", CAR_FINS)
c.at("In a town where most people", MEET2)
c.at("The officers began writing", doc("PLATES OBSERVED, McFALL ROAD\n\nNEW YORK\nNEW JERSEY\nOHIO\nILLINOIS\nTEXAS\nCALIFORNIA\nFLORIDA", None))
c.at("At around twenty to one", typer("12:40 PM", 110))
c.at("someone inside the house noticed", MEET2)
c.at("Word spread through the property", MEET1)
c.at("He called for backup", TROOP2)
c.at("set up a roadblock", BLOCK1)
c.at("Then, at about twenty past one", typer("1:20 PM", 110))
c.at("Some of the guests jumped", BLOCK2)
c.at("Emanuele Zicari and Dominick Alaimo", typer("EMANUELE ZICARI\nDOMINICK ALAIMO", 64))
c.at("Others chose a different escape", black())
c.at("They ran", say("They ran.", 170))
c.at("Picture it", RUN1)
c.at("Expensive shoes sinking", RUN2)
c.at("Some headed for the woods", dict(RUN1, move="left"))
c.at("Some of them made it", BLOCK1)
c.at("One by one, the troopers", TROOP2)
c.at("Every one of them was taken", BARR1)
c.at("By the end of the day", counter(58, "men identified"))
c.at("Estimates suggest", typer("ATTENDED: ~100\nIDENTIFIED: 58\nESCAPED: DOZENS", 64, sound=False))
c.at("Among the names later linked", dossier("Sam Giancana", "ESCAPED?", City="Chicago"))
c.at("But the men who were caught", BARR2)
c.at("Vito Genovese, the man at the", dossier("Vito Genovese", "DETAINED", stamp="DETAINED", City="New York"))
c.at("Carlo Gambino, soon to become", dossier("Carlo Gambino", "DETAINED", stamp="DETAINED", City="New York"))
c.at("Joseph Profaci and Joseph Magliocco", dossier("Joseph Profaci", "DETAINED", stamp="DETAINED", City="Brooklyn"))
c.at("Santo Trafficante", dossier("Santo Trafficante", "DETAINED", City="Tampa / Havana"))
c.at("Joseph Civello", dossier("Joseph Civello", "DETAINED", City="Dallas"))
c.at("Russell Bufalino, the organizer", dossier("Russell Bufalino", "ORGANIZER", Region="Pennsylvania"))
c.at("And their host", dossier(**BARBARA))
c.at("In a single afternoon", TROOP1)
c.at("He had put names", BARR2)
c.at("Now came the hard part", BARR1)
chapters.append(c)

# ---------------------------------------------------------------- CH 6
c = ch("ch06")
c.at(0, card(6, "Visiting a sick friend"))
c.at("At the barracks", BARR1)
c.at("Why are you in Apalachin", typer("WHY ARE YOU IN APALACHIN?", 70))
c.at("And one by one, these men", BARR2)
c.at("They had come to visit", doc("STATEMENT\n\n\"Came to visit Joe Barbara.\nHeard he was sick.\"", "RECORDED"))
c.at("It was true that Barbara", dossier("Joseph Barbara", "THE HOST", Health="Heart attack, 1956"))
c.at("But the idea that dozens", MEET2)
c.at("Some described themselves", typer("OLIVE OIL IMPORTER\nDRESS MANUFACTURER\nRESTAURANT OWNER\nTAXI COMPANY OPERATOR", 54))
c.at("Together, according to later reports", counter(275, "arrests", suffix="+"))
c.at("over one hundred convictions", counter(100, "convictions", suffix="+"))
c.at("And yet, the officers faced", BARR1)
c.at("Attending a barbecue was not", say("Not a crime.", hit=False))
c.at("Running from a party", RUN2)
c.at("Croswell had their names", dossier(**CROSWELL))
c.at("What he didn't have", say("No charge.", hit=False))
c.at("So, after they were identified", dict(CAR_TEAL, move="out"))
c.at("It looked like a defeat", black())
c.at("It wasn't", say("It wasn't."))
chapters.append(c)

# ---------------------------------------------------------------- CH 7
c = ch("ch07")
c.at(0, card(7, "The fallout"))
c.at("The next morning", PRESS)
c.at("Reporters raced to Apalachin", MEET1)
c.at("Photographers stood outside", MEET2)
c.at("And Americans who had dismissed", TV)
c.at("If all these men", CAR_ROW)
c.at("what exactly were they part of", typer("...what exactly were they part of?", 56, sound=False))
c.at("The pressure landed squarely", JUSTICE)
c.at("The Federal Bureau of Narcotics had", doc("FEDERAL BUREAU OF NARCOTICS\n\nFILES ON:\nGenovese · Gambino · Profaci\nTrafficante · Bufalino · ...", "ON FILE"))
c.at("The FBI, by many accounts", HOOVER_PORT)
c.at("It was an embarrassment", HOOVER_DESK)
c.at("Within two weeks", typer("NOVEMBER 27, 1957", 80))
c.at("the Bureau sent out a directive", doc("FEDERAL BUREAU OF INVESTIGATION\nNovember 27, 1957\n\nTO: ALL FIELD OFFICES\nRE: TOP HOODLUM PROGRAM\n\nIdentify the leading racketeers in your territory. Gather intelligence on them, systematically.", "DIRECTIVE"))
c.at("Historians still debate", JUSTICE_DOOR)
c.at("But after Apalachin, the effort", JUSTICE)
c.at("In the years that followed", GMAN)
c.at("Washington reacted too", JUSTICE)
c.at("a young lawyer named Robert", img("ch07_rfk_mcclellan/1_commons.jpg", "in", cap="Robert F. Kennedy, Senate counsel"))
c.at("He would carry that conviction", img("ch07_rfk_mcclellan/2_loc.jpg", "out"))
c.at("As for the men themselves", BARR2)
c.at("In May 1959", dict(COURT, caption="Foley Square, New York"))
c.at("The charge was not attending", doc("UNITED STATES v. BUFALINO et al.\n\nCHARGE: Conspiracy to obstruct justice\n(lying about the purpose of the meeting)", None))
c.at("That December, twenty men", counter(20, "men convicted"))
c.at("They received prison sentences", typer("3 TO 5 YEARS\n13 FINED $10,000 EACH", 60))
c.at("Prosecutors called it", COURT2)
c.at("It didn't last", say("It didn't last."))
c.at("On November 28th, 1960", timeline([["MAY 1959", "Indicted"], ["DEC 1959", "20 convicted", True], ["NOV 1960", "All reversed"]]))
c.at("The reasoning was simple", COURT3)
c.at("And if you cannot prove", dict(COURT, move="out"))
c.at("Even some commentators", PRESS)
c.at("So, in the end", say("No one went to prison for Apalachin.", 110))
c.at("But that was never really", black())
chapters.append(c)

# ---------------------------------------------------------------- CH 8
c = ch("ch08", 2.5)
c.at(0, card(8, "The trooper who woke a nation"))
c.at("The meeting at Apalachin was supposed", MEET1)
c.at("Instead, it brought daylight", ROAD2)
c.at("For the men involved", BARR1)
c.at("Joseph Barbara, the host", dossier(**BARBARA))
c.at("He faced tax trouble", BOTTLING)
c.at("In June 1959, he died", dossier("Joseph Barbara", "THE HOST", stamp="DECEASED", Died="June 1959"))
c.at("His estate on McFall Road", dict(ROAD1, move="out"))
c.at("Vito Genovese, the man many", dossier("Vito Genovese", "SUBJECT", City="New York"))
c.at("In 1959, he was convicted", counter(15, "years in prison"))
c.at("He would die behind bars", dict(GENOVESE_IMG, move="out"))
c.at("Some in the underworld", black())
c.at("That has never been proven", say("Never proven.", hit=False))
c.at("And Sergeant Edgar Croswell", dossier(**CROSWELL))
c.at("He became, for a time", PRESS)
c.at("A small-town investigator", TROOP1)
c.at("followed a few rooms in a motel", MOTEL)
c.at("and a meat order", BUTCHER)
c.at("and exposed something", HOOVER_DESK)
c.at("The men at Apalachin had spent", MEET2)
c.at("No written records", typer("NO WRITTEN RECORDS.\nNO PUBLIC FACES.\nA CODE OF SILENCE.", 60))
c.at("And it all came undone", RUN1)
c.at("After that day", TV)
c.at("And the people hunting it", JUSTICE)
c.at("But the biggest blow", black())
c.at("Six years later", VALACHI2)
c.at("with television cameras rolling", VALACHI)
c.at("Its ranks", typer("ITS RANKS.\nITS RITUALS.\nITS NAME.", 72))
c.at("His name was Joseph Valachi", dossier("Joseph Valachi", "NEXT FILE", Family="Genovese", Testimony="1963"))
c.at("If you want to see it", {"type": "title", "title": "Valachi", "subtitle": "Next on Black Dossier",
                               "file": "FILE No. 002", "stamp": "NEXT", "sfx": [fx("stamp", 0.9)]})
c.at("I'll see you in the next file", dict(black(), fade_in=0))
chapters.append(c)


def dur(p):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                          "-of", "csv=p=0", p]).strip())


out = {"output": "BlackDossier_EP01_Apalachin.mp4", "fps": 24,
       "music": [{"file": "trilha.wav", "start": 0, "gain": -21, "fade_in": 4, "fade_out": 5}],
       "chapters": []}
for c in chapters:
    out["chapters"].append(c.build(dur(c.audio)))
    sys.stderr.write(f"{c.name}: {len(c.cues)} planos, alinhamento {c.matched:.0%}"
                     + (f", NAO ACHEI: {c.misses}" if c.misses else "") + "\n")
# last shot of the episode fades to black
out["chapters"][-1]["shots"][-1]["fade_out"] = 1.5
print(json.dumps(out, indent=1, ensure_ascii=False))
