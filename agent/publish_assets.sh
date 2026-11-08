#!/usr/bin/env bash
# Publish an agent's output folder into the assets branch, safely when several agents run at once.
# Usage: agent/publish_assets.sh <source_dir> <dest_subdir_in_assets> "<commit message>"
# Re-syncs to the latest assets branch before every attempt and retries, so parallel runs never lose work.
set -u
SRC="$1"; DEST="$2"; MSG="$3"
ROOT="$PWD"
SRC="$(cd "$SRC" 2>/dev/null && pwd)" || { echo "Nada para publicar"; exit 0; }
for attempt in 1 2 3 4 5 6; do
  WT="$ROOT/pubwt"
  rm -rf "$WT"; git -C main worktree prune
  git -C main fetch -q --depth=1 origin +refs/heads/assets:refs/remotes/origin/assets || { sleep 5; continue; }
  # sparse worktree: check out only the destination folder (the full assets branch is several GB)
  git -C main worktree add -q -f --detach --no-checkout "$WT" origin/assets || { sleep 5; continue; }
  # only the paths this agent writes (the episode folder can hold GBs of clips): one pattern per top-level entry
  PATS=$(cd "$SRC" && for e in * .[!.]*; do [ -e "$e" ] && printf '/%s/%s\n' "$DEST" "$e"; done; true)
  [ -z "$PATS" ] && PATS="/$DEST/"
  printf '%s\n' "$PATS" | git -C "$WT" sparse-checkout set --no-cone --stdin && git -C "$WT" checkout -q --detach origin/assets || { sleep 5; continue; }
  mkdir -p "$WT/$DEST"
  cp -r "$SRC"/. "$WT/$DEST/"
  cd "$WT"
  git config user.name "black-dossier-agent"
  git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
  git add -A "$DEST"
  if git diff --cached --quiet; then echo "Nada novo"; exit 0; fi
  git commit -q -m "$MSG"
  if git push -q origin HEAD:assets; then echo "Publicado (tentativa $attempt)"; exit 0; fi
  cd "$ROOT"
  echo "Push recusado (outro agente publicou junto); tentando de novo..."
  sleep $((attempt * 5))
done
echo "FALHA ao publicar depois de 6 tentativas"; exit 1
