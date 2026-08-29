#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

PORT="${1:-${PORT:-8080}}"

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

echo "R3 project: $ROOT"
echo "Codex:      $CODEX"
echo "Dev port:   $PORT"
echo "Cycle:      RELEASE → TEST → COMMENTS → CORE DUMP → REVIEW → PLAN → BUILD → RELEASE"

python3 rct_r3_release.py --codex "$CODEX"
exec python3 rct_r3_dev_server.py --port "$PORT"
