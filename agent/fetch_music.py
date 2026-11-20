#!/usr/bin/env python3
"""Download royalty-free music (Kevin MacLeod / incompetech.com, CC BY 4.0) into <out>/music/.
Usage: python3 agent/fetch_music.py <out_dir> "Title 1" "Title 2" ...
Writes <title>.mp3 for each track that exists, and credits.txt with the attribution lines required by CC BY 4.0.
"""
import os, sys, urllib.parse, requests
out = os.path.join(sys.argv[1], "music"); os.makedirs(out, exist_ok=True)
ok, lines = [], []
for t in sys.argv[2:]:
    url = "https://incompetech.com/music/royalty-free/mp3-royaltyfree/" + urllib.parse.quote(t) + ".mp3"
    try:
        r = requests.get(url, timeout=120, headers={"User-Agent": "Mozilla/5.0 (music fetch for licensed use)"})
    except Exception as e:
        print("ERRO", t, e); continue
    if r.status_code == 200 and len(r.content) > 200000 and r.content[:3] in (b"ID3", b"\xff\xfb", b"\xff\xf3", b"\xff\xf2"):
        fn = t.replace("/", "-") + ".mp3"
        open(os.path.join(out, fn), "wb").write(r.content); ok.append(fn)
        lines.append(f'"{t}" Kevin MacLeod (incompetech.com) · Licensed under Creative Commons: By Attribution 4.0 License · http://creativecommons.org/licenses/by/4.0/')
        print("OK", t, len(r.content))
    else:
        print("FALHOU", t, r.status_code, len(r.content))
open(os.path.join(out, "credits.txt"), "w").write("\n".join(lines) + "\n")
print(f"{len(ok)} faixas")
