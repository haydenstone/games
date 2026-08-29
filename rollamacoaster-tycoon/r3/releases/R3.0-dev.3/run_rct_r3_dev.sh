#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

if ! command -v python3 >/dev/null 2>&1; then
  echo "ERROR: python3 is required." >&2
  exit 1
fi

CODEX=""
for candidate in codex.json 'codex(1).json' codex*.json; do
  if [[ -f "$candidate" ]]; then CODEX="$candidate"; break; fi
done
if [[ -z "$CODEX" ]]; then
  echo "ERROR: No codex*.json found in $ROOT" >&2
  exit 1
fi

# Use the uniquely named portable scripts so stale canonical files cannot interfere.
echo "R3 project: $ROOT"
echo "Codex:      $CODEX"
python3 rct_r3_release_PORTABLE.py --codex "$CODEX"
exec python3 rct_r3_dev_server.py
