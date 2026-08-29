#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

PORT="${1:-${PORT:-8080}}"

echo "R3 project: $ROOT"
echo "Dev port:   $PORT"

python3 build_rct_r3_PORTABLE.py --codex codex.json
python3 rct_r3_release_PORTABLE.py

python3 rct_r3_dev_server.py --port "$PORT"
