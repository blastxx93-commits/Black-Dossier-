#!/usr/bin/env python3
"""Keyword agent: what people actually type into YouTube search (autocomplete), for titles, description and tags.

Reads episodes/<ep>/keywords_seeds.txt (one seed per line). For each seed it collects YouTube autocomplete
suggestions for the seed alone and for seed + a..z. A suggestion that shows up for many seeds/prefixes is a
term with real search demand. Writes <out>/<ep>/keywords.md and keywords.csv.

Usage: python3 agent/keywords.py ep03-bonanno [--out assets_out]
"""
import argparse, collections, csv, json, os, string, time
import requests

URL = "https://suggestqueries.google.com/complete/search"
S = requests.Session()
S.headers["User-Agent"] = "Mozilla/5.0 (BlackDossierKeywords/1.0)"


HL, GL = "en", "us"   # episodes with lang.txt = es search Spanish suggestions from Spain


def suggest(q):
    for k in range(3):
        try:
            r = S.get(URL, params={"client": "firefox", "ds": "yt", "hl": HL, "gl": GL, "q": q}, timeout=15)
            if r.status_code == 200:
                return json.loads(r.text)[1]
        except Exception:
            pass
        time.sleep(1 + k)
    return []


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("episode")
    ap.add_argument("--out", default="assets_out")
    a = ap.parse_args()
    global HL, GL
    lf = os.path.join("episodes", a.episode, "lang.txt")
    if os.path.exists(lf) and open(lf).read().strip() == "es":
        HL, GL = "es", "es"
    seeds = [l.strip() for l in open(os.path.join("episodes", a.episode, "keywords_seeds.txt")) if l.strip()]
    score, origin = collections.Counter(), collections.defaultdict(set)
    for seed in seeds:
        for i, q in enumerate([seed] + [f"{seed} {c}" for c in string.ascii_lowercase]):
            for rank, sug in enumerate(suggest(q)):
                sug = sug.strip().lower()
                score[sug] += (10 - rank) * (3 if i == 0 else 1)   # higher in the list and on the bare seed = more demand
                origin[sug].add(seed)
            time.sleep(0.25)
        print(f"{seed}: ok", flush=True)
    rows = [(k, v, len(origin[k])) for k, v in score.most_common(150)]
    d = os.path.join(a.out, a.episode)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "keywords.csv"), "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["termo", "pontuacao", "sementes"]); w.writerows(rows)
    md = [f"# Palavras-chave — {a.episode}", "", f"Sugestões reais da busca do YouTube ({GL.upper()}, {HL}). Pontuação maior = mais demanda.", "",
          "| # | termo | pontuação | aparece em |", "|---|---|---|---|"]
    md += [f"| {i+1} | {t} | {s} | {n} semente(s) |" for i, (t, s, n) in enumerate(rows[:80])]
    open(os.path.join(d, "keywords.md"), "w").write("\n".join(md) + "\n")
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        open(os.environ["GITHUB_STEP_SUMMARY"], "a").write("\n".join(md[:40]) + "\n")
    print("\n".join(md[:30]))


if __name__ == "__main__":
    main()
