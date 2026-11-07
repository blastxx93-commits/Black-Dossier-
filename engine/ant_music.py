#!/usr/bin/env python3
"""Real (licensed) music for the Abaixo de Zero channel, one track per mood.

Reads episodes/<ep>/edit/trilha.json:
    {"moods": {"tensao": ["Gathering Darkness", "The Descent"], "misterio": [...], ...}}
For each mood, a track sent by the owner wins: episodes/<ep>/edit/musica/<mood>.mp3 (or the track named in
"aliases" for a mood without its own file). Otherwise it downloads the first track that exists from Kevin MacLeod's library (incompetech.com,
Creative Commons BY 4.0: credit goes in the video description) into <work>/musica/<mood>.mp3 and writes
<work>/musica/creditos.txt. If no track of a mood can be downloaded, a synthesized bed of a similar
style (engine/aus_music.py) is written instead, so a render never fails for lack of music.

Usage: python3 engine/ant_music.py episodes/<ep>/edit/trilha.json <work_dir>
"""
import json, os, subprocess, sys, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = "https://incompetech.com/music/royalty-free/mp3-royaltyfree/"
SYNTH = {"tensao": "tension", "misterio": "dark", "epico": "pulse", "drama": "dark", "frio": "doc",
         "maravilha": "doc", "descoberta": "doc", "reflexivo": "doc"}


def fetch(title, out):
    url = BASE + urllib.parse.quote(title) + ".mp3"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (AbaixoDeZero render)"})
        data = urllib.request.urlopen(req, timeout=60).read()
    except Exception as e:
        print(f"  {title}: {str(e)[:80]}", flush=True)
        return False
    if len(data) < 200_000 or not (data[:3] == b"ID3" or data[:1] == b"\xff"):
        print(f"  {title}: resposta não é mp3", flush=True)
        return False
    open(out, "wb").write(data)
    return True


def main(spec_path, work):
    spec = json.load(open(spec_path))
    d = os.path.join(work, "musica")
    os.makedirs(d, exist_ok=True)
    credits = []
    for mood, titles in spec["moods"].items():
        out = os.path.join(d, f"{mood}.mp3")
        src = mood
        own = os.path.join(os.path.dirname(os.path.abspath(spec_path)), "musica", f"{mood}.mp3")
        if not os.path.exists(own) and spec.get("aliases", {}).get(mood):
            src = spec["aliases"][mood]
            own = os.path.join(os.path.dirname(os.path.abspath(spec_path)), "musica", f"{src}.mp3")
        if os.path.exists(own):   # track sent by the owner: 4 copies joined with 4 s crossfades = a long bed, no jump at the loop
            subprocess.run(["ffmpeg", "-v", "error", "-y"] + ["-i", own] * 4 + ["-filter_complex",
                            "[0][1]acrossfade=d=4:c1=tri:c2=tri[a];[a][2]acrossfade=d=4:c1=tri:c2=tri[b];"
                            "[b][3]acrossfade=d=4:c1=tri:c2=tri[o]", "-map", "[o]", "-ar", "48000", "-b:a", "192k", out], check=True)
            print(f"{mood}: faixa do dono ({src}.mp3)", flush=True)
            continue
        got = next((t for t in titles if fetch(t, out)), None)
        if got:
            credits.append(f'"{got}" Kevin MacLeod (incompetech.com) — Licensed under Creative Commons: By Attribution 4.0 '
                           f"http://creativecommons.org/licenses/by/4.0/")
            print(f"{mood}: {got}", flush=True)
        else:
            wav = os.path.join(d, f"{mood}.wav")
            subprocess.run([sys.executable, os.path.join(HERE, "aus_music.py"), wav, SYNTH.get(mood, "doc"), "7"], check=True)
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", wav, "-b:a", "192k", out], check=True)
            os.remove(wav)
            print(f"{mood}: SEM FAIXA REAL — trilha sintetizada no lugar", flush=True)
    open(os.path.join(d, "creditos.txt"), "w").write("\n".join(dict.fromkeys(credits)) + "\n")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
