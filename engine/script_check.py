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

# Portuguese (canal Antártica): used automatically when the text has Portuguese accents/words
STOP_PT = set("""a o as os um uma uns umas de do da dos das em no na nos nas por pelo pela pelos pelas para pra com sem
sob sobre entre até ate e ou mas que se não nao sim é ser era foi são sao está esta estão estao estava eram foram tem têm
ter tinha há ha isso isto aquilo esse essa esses essas este esta estes estas aquele aquela aqueles aquelas ele ela eles
elas você voce vocês nós nos seu sua seus suas dele dela deles delas meu minha qual quais quem quando onde como porque
porquê muito muita muitos muitas mais menos já ja ainda também tambem só so então entao assim lhe lhes me te mesmo mesma
cada todo toda todos todas outro outra outros outras dois duas três tres mil vez vezes pode podem num numa ao aos à às
""".split())
CRUTCH_PT = {"realmente", "simplesmente", "basicamente", "literalmente", "praticamente", "incrível", "inacreditável", "de repente"}


def main(path):
    global STOP, CRUTCH
    text = open(path).read()
    pt = len(re.findall(r"[ãõçáéíóúâêô]", text.lower())) > len(text) / 400
    if pt:
        STOP, CRUTCH = STOP | STOP_PT, CRUTCH_PT
    names = set(re.findall(r"\b([A-ZÁÉÍÓÚÂÊÔÃÕ][a-zà-ÿ]+)\b", text))
    words = [w.lower() for w in re.findall(r"[A-Za-zÀ-ÿ']+", text)]
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
    for w in (("e", "mas", "então") if pt else ("and", "but", "so")):
        share = first[w] / max(1, len(sents))
        if share > 0.08:
            problems += 1
            print(f"\nMuitas frases começando com \"{w.capitalize()}\": {first[w]} ({share:.0%})")

    low = " ".join(words)
    cr = [(w, low.count(w) if " " in w else words.count(w)) for w in CRUTCH]
    cr = [(w, n) for w, n in cr if n > 2]
    if cr:
        problems += len(cr)
        print("\nMuletas:", ", ".join(f"{w} ({n}x)" for w, n in cr))

    print("\nOK, sem problemas." if not problems else f"\n{problems} ponto(s) para revisar.")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
