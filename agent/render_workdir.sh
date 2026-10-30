#!/usr/bin/env bash
# Builds the render work folder on a runner: work/a -> assets/<ep>, work/audio -> narration, sound kit,
# episode.json and subtitles from episodes/<ep>/edit/. Run from $GITHUB_WORKSPACE (main/ and assets/ checked out).
set -eu
EP="$1"
mkdir -p work
ln -sfn "$PWD/assets/$EP" work/a
ln -sfn "$PWD/assets/$EP/narration_audio" work/audio
python3 main/engine/aus_audio.py work
cp "main/episodes/$EP/edit/episode.json" work/
cp main/episodes/"$EP"/edit/*.ass work/ 2>/dev/null || true
mkdir -p ~/.fonts && cp main/engine/fonts/*.otf ~/.fonts/ && fc-cache -f > /dev/null || true
echo "pasta de render pronta: $(ls work)"
