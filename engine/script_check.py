#!/usr/bin/env python3
"""Repetition check for narration scripts (channel rule: no heavy word repetition).

Usage: python3 engine/script_check.py episodes/<ep>/EP0X_roteiro.txt
Reports: overused content words, repeated 3-word phrases, consecutive sentences starting the same way,
and crutch words. Exit code 1 if something must be fixed before narration.
"""
import collections, re, sys

STOP = set("""a an the and or but of to in on at by for from with as is was were be been being it its this that these those
he she they them his her their him we you i me my our your who whom which what when where why how not no nor so than then
there here into out up down over under again once all any both each few more most other some such only own same too very
can will would could should may might must do does did done have has had having just also about after before between through
during against because while until if one two said""".split())
CRUTCH = {"really", "very", "just", "actually", "basically", "simply", "literally", "suddenly"}


def main(path):
    text = open(path).read()
    names = set(re.findall(r"\b([A-Z][a-z]+)\b", text))
    words = [w.lower() for w in re.findall(r"[A-Za-z']+", text)]
    total = len(words)
    sents = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text.replace("\n", " ")) if s.strip()]
    problems = 0

    cnt = collections.Counter(w for w in words if w not in STOP and len(w) > 3)
    limit = max(6, total // 250)
    over = [(w, n) for w, n in cnt.most_common(40) if n > limit and w.capitalize() not in names]
    print(f"Palavras: {total}  ·  limite por palavra comum: {limit}")
    if over:
        problems += len(over)
        print("\nPalavras repetidas demais (trocar por sinônimos):")
        for w, n in over:
            print(f"  {w}: {n}x")

    tri = collections.Counter(" ".join(words[i:i + 3]) for i in range(len(words) - 2))
    rep = [(t, n) for t, n in tri.most_common(30) if n >= 3 and not all(x in STOP for x in t.split())]
    if rep:
        problems += len(rep)
        print("\nExpressões repetidas (3+ vezes):")
        for t, n in rep:
            print(f"  \"{t}\": {n}x")

    starts = [" ".join(s.split()[:2]).lower() for s in sents]
    runs = [(sents[i][:60], starts[i]) for i in range(2, len(starts))
            if starts[i] == starts[i - 1] == starts[i - 2] and not starts[i].startswith("chapter")]
    if runs:
        problems += len(runs)
        print("\nTrês frases seguidas começando igual:")
        for s, st in runs:
            print(f"  \"{st}…\" → {s}")

    first = collections.Counter(s.split()[0].lower() for s in sents if s.split())
    for w in ("and", "but", "so"):
        share = first[w] / max(1, len(sents))
        if share > 0.08:
            problems += 1
            print(f"\nMuitas frases começando com \"{w.capitalize()}\": {first[w]} ({share:.0%})")

    cr = [(w, cnt[w] if w in cnt else words.count(w)) for w in CRUTCH if words.count(w) > 2]
    if cr:
        problems += len(cr)
        print("\nMuletas:", ", ".join(f"{w} ({n}x)" for w, n in cr))

    print("\nOK, sem problemas." if not problems else f"\n{problems} ponto(s) para revisar.")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
