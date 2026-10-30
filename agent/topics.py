#!/usr/bin/env python3
"""Topic agent (pauta) for the Aussie car channel.

Reads recent Australian car news (Google News search feeds + the main motoring sites' feeds), keeps only
stories from the last N days, groups them by subject (brand / model / theme), ranks the subjects by how many
different outlets are covering them and how recent the stories are, and writes a report with video ideas.

No API keys. Output (in <out>/pauta/):
    pauta_<date>.md     ranked subjects, each with its headlines + links (the facts to check before writing)
    pauta_<date>.json   same data for Claude to read
Usage: python3 agent/topics.py [--out assets_out] [--days 14]
"""
import argparse, datetime as dt, email.utils, html, json, os, re, time, urllib.parse
from collections import defaultdict
import xml.etree.ElementTree as ET
import requests

UA = "AusCarTopicAgent/1.0 (YouTube research; github.com/blastxx93-commits/Black-Dossier-)"
GNEWS = "https://news.google.com/rss/search?q={q}&hl=en-AU&gl=AU&ceid=AU:en"
QUERIES = [
    "Australia car sales VFACTS", "car brand Australia leaving", "car recall Australia", "ACCC car", "car prices Australia",
    "ute Australia sales", "electric car Australia", "Chinese car brand Australia", "dealership Australia", "car insurance Australia",
    "New Vehicle Efficiency Standard", "fuel prices Australia cars", "car discounts Australia", "ANCAP rating", "car warranty Australia",
    "Toyota Australia", "Ford Ranger Australia", "BYD Australia", "Tesla Australia", "Mitsubishi Australia", "Nissan Australia",
    "Hyundai Kia Australia", "Mazda Australia", "Subaru Australia", "Volkswagen Australia", "GWM Australia", "Chery Australia",
    "Geely Australia", "MG Australia", "car repair delays Australia", "used car prices Australia", "car finance Australia",
]
SITE_FEEDS = ["https://www.carexpert.com.au/feed", "https://www.drive.com.au/feed/", "https://www.carsguide.com.au/rss",
              "https://thebeep.com.au/feed", "https://www.whichcar.com.au/feed"]
BRANDS = ["Toyota", "Ford", "BYD", "Tesla", "Mazda", "Kia", "Hyundai", "Mitsubishi", "Nissan", "Subaru", "Suzuki", "Volkswagen",
          "Isuzu", "GWM", "Haval", "MG", "Chery", "Geely", "Zeekr", "Omoda", "Jaecoo", "LDV", "KGM", "SsangYong", "Jeep",
          "Peugeot", "Citroen", "Fiat", "Alfa Romeo", "Renault", "Skoda", "Cupra", "Polestar", "Leapmotor", "Xpeng", "Deepal",
          "Denza", "GAC", "Honda", "Lexus", "BMW", "Mercedes", "Audi", "Volvo", "Jaguar", "Land Rover", "Holden"]
THEMES = {
    "sales slump": r"sales (fall|drop|slump|plunge|down)|slump|worst|decline", "leaving / exit": r"leav|exit|axed|quit|pull(s|ed)? out|distributor",
    "recall / safety": r"recall|ancap|stop-sale|stop sale|safety", "price cuts / deals": r"discount|price cut|slash|cheaper|deal|drive-away",
    "EV shift": r"\bev\b|electric|plug-in|phev|hybrid", "consumer rights": r"accc|consumer law|refund|lemon|fined|court",
    "utes": r"\bute|hilux|ranger|navara|triton|d-max|shark", "repairs / parts": r"repair|parts|service|warranty",
    "policy / tax": r"nves|efficiency standard|tax|tariff|government|rebate", "Chinese brands": r"chinese|china",
}
S = requests.Session(); S.headers["User-Agent"] = UA


def fetch(url):
    for k in range(3):
        try:
            r = S.get(url, timeout=25)
            if r.status_code == 429:
                time.sleep(10 * (k + 1)); continue
            r.raise_for_status()
            return r.content
        except Exception:
            time.sleep(3)
    return None


def parse(xml_bytes, origin):
    out = []
    try:
        root = ET.fromstring(xml_bytes)
    except ET.ParseError:
        return out
    for it in root.iter("item"):
        title = html.unescape((it.findtext("title") or "").strip())
        link = (it.findtext("link") or "").strip()
        src = (it.find("source").text if it.find("source") is not None else "") or origin
        try:
            when = email.utils.parsedate_to_datetime(it.findtext("pubDate") or "")
        except Exception:
            when = None
        if " - " in title and origin == "google":   # Google News appends " - Outlet"
            title, src = title.rsplit(" - ", 1)[0], title.rsplit(" - ", 1)[1]
        out.append({"title": title, "link": link, "source": src.strip(), "when": when})
    return out


def subjects_of(title):
    t = title.lower(); subs = []
    for b in BRANDS:
        if re.search(r"\b" + re.escape(b.lower()) + r"\b", t):
            subs.append(b)
    for name, rx in THEMES.items():
        if re.search(rx, t):
            subs.append("#" + name)
    return subs


IDEAS = {
    "sales slump": "Why {b} sales are falling in {y} – the real numbers", "leaving / exit": "Is {b} leaving Australia? What owners need to know",
    "recall / safety": "{b} recall explained: who's affected and what to do", "price cuts / deals": "{b} is slashing prices – are the deals worth it?",
    "EV shift": "{b} and the EV shift: winning or losing in {y}?", "consumer rights": "{b} vs the ACCC: what happened and your rights",
    "utes": "The {b} ute battle in {y}", "repairs / parts": "{b} owners waiting for repairs – what's going on?",
    "policy / tax": "How the new rules hit {b} buyers", "Chinese brands": "How {b} is fighting the Chinese brands",
}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--out", default="assets_out"); ap.add_argument("--days", type=int, default=14)
    a = ap.parse_args()
    now = dt.datetime.now(dt.timezone.utc); since = now - dt.timedelta(days=a.days)
    items = []
    for q in QUERIES:
        b = fetch(GNEWS.format(q=urllib.parse.quote(q + f" when:{a.days}d")))
        if b: items += parse(b, "google")
        time.sleep(1)
    for f in SITE_FEEDS:
        b = fetch(f)
        if b: items += parse(b, f.split("/")[2].replace("www.", ""))
    seen, fresh = set(), []
    for it in items:
        key = re.sub(r"\W+", "", it["title"].lower())[:90]
        if not it["title"] or key in seen or (it["when"] and it["when"] < since):
            continue
        seen.add(key); fresh.append(it)
    groups = defaultdict(list)
    for it in fresh:
        for s in subjects_of(it["title"]):
            groups[s].append(it)
    def score(lst):
        outlets = len({x["source"] for x in lst})
        rec = sum(max(0.0, 1 - (now - x["when"]).days / a.days) if x["when"] else 0.3 for x in lst)
        return round(outlets * 2 + rec, 1)
    ranked = sorted(groups.items(), key=lambda kv: -score(kv[1]))
    brands = [(k, v) for k, v in ranked if not k.startswith("#")][:15]
    themes = [(k, v) for k, v in ranked if k.startswith("#")]
    day = now.strftime("%Y-%m-%d"); y = now.year
    lines = [f"# Pauta – canal Austrália ({day})", "", f"{len(fresh)} notícias dos últimos {a.days} dias, de {len(QUERIES)} buscas e {len(SITE_FEEDS)} sites.",
             "Ranking: quantos veículos diferentes cobrem o assunto (peso 2) + quão recentes são as notícias.", "",
             "## Marcas em alta no noticiário", ""]
    out = {"date": day, "days": a.days, "brands": [], "themes": []}
    for b, lst in brands:
        th = defaultdict(int)
        for x in lst:
            for s in subjects_of(x["title"]):
                if s.startswith("#"): th[s[1:]] += 1
        top = sorted(th, key=lambda k: -th[k])[:2]
        ideas = [IDEAS[t].format(b=b, y=y) for t in top if t in IDEAS]
        lines += [f"### {b} — pontuação {score(lst)} ({len(lst)} notícias, {len({x['source'] for x in lst})} veículos)"]
        if ideas: lines += ["Ideias: " + " · ".join(ideas)]
        for x in sorted(lst, key=lambda x: x["when"] or since, reverse=True)[:6]:
            d = x["when"].strftime("%d/%m") if x["when"] else "?"
            lines.append(f"- {d} · {x['source']}: [{x['title']}]({x['link']})")
        lines.append("")
        out["brands"].append({"subject": b, "score": score(lst), "ideas": ideas,
                              "news": [{"title": x["title"], "source": x["source"], "link": x["link"],
                                        "date": x["when"].isoformat() if x["when"] else None} for x in lst[:12]]})
    lines += ["## Temas do momento", ""]
    for t, lst in themes:
        lines.append(f"- **{t[1:]}** — {len(lst)} notícias, pontuação {score(lst)}")
        out["themes"].append({"theme": t[1:], "score": score(lst), "count": len(lst)})
    lines += ["", "Antes de virar roteiro: abrir as notícias, conferir números na fonte original e usar só fatos de " + str(y) + "."]
    d = os.path.join(a.out, "pauta"); os.makedirs(d, exist_ok=True)
    rep = "\n".join(lines) + "\n"
    open(os.path.join(d, f"pauta_{day}.md"), "w").write(rep)
    open(os.path.join(d, "pauta_ultima.md"), "w").write(rep)
    json.dump(out, open(os.path.join(d, f"pauta_{day}.json"), "w"), indent=1)
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        open(os.environ["GITHUB_STEP_SUMMARY"], "a").write(rep)
    print(rep[:3000])


if __name__ == "__main__":
    main()
