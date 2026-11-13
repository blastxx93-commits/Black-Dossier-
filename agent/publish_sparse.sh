#!/usr/bin/env bash
# Publica uma pasta no branch assets SEM baixar o branch inteiro (clone raso + esparso só da pasta de destino).
# Uso: agent/publish_sparse.sh <pasta_origem> <subpasta_no_assets> "<mensagem>"   (precisa de GITHUB_TOKEN e GITHUB_REPOSITORY)
set -u
SRC="$(cd "$1" 2>/dev/null && pwd)" || { echo "Nada para publicar"; exit 0; }
DEST="$2"; MSG="$3"
URL="https://x-access-token:${GITHUB_TOKEN}@github.com/${GITHUB_REPOSITORY}.git"
for attempt in 1 2 3 4 5 6; do
  WT="$(mktemp -d)"
  if git clone -q --depth=1 --filter=blob:none --sparse --branch assets "$URL" "$WT"; then
    cd "$WT"
    git sparse-checkout set "$DEST" > /dev/null
    mkdir -p "$DEST"; cp -r "$SRC"/. "$DEST/"
    git config user.name "black-dossier-agent"
    git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
    git add -A "$DEST"
    if git diff --cached --quiet; then echo "Nada novo"; exit 0; fi
    git commit -q -m "$MSG"
    if git push -q origin HEAD:assets; then echo "Publicado (tentativa $attempt)"; exit 0; fi
    cd /
  fi
  echo "Tentando de novo..."; sleep $((attempt * 5))
done
echo "FALHA ao publicar depois de 6 tentativas"; exit 1
