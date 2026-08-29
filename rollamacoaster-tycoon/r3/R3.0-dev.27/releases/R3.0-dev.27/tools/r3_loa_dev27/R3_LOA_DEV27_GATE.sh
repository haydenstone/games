#!/usr/bin/env bash
set -euo pipefail
BASE="${1:-http://127.0.0.1:8765}"; ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
python3 "$ROOT/tools/r3_loa_dev27/r3_dev27_contract_scan.py" "$ROOT/rollamacoasterTycoon_R3_rebuilt.html"
curl -fsS "$BASE/api/dev/status" >/dev/null && echo "PASS R3 dev server reachable"
if curl -fsS "$BASE/api/alexandria/status" >/dev/null; then echo "PASS Alexandria reachable through R3"; else echo "INFO Alexandria offline; park remains local"; fi
echo "DEV.27 Alexandria gate complete"
