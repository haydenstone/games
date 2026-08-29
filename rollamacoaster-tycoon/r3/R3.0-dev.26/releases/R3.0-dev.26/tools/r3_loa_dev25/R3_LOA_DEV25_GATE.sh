#!/usr/bin/env bash
set -euo pipefail

R3_BASE="${1:-http://127.0.0.1:8766}"
KNOWN_QUERY="${R3_LOA_TEST_QUERY:-GREEN}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

pass(){ printf '\033[1;32mPASS\033[0m %s\n' "$*"; }
fail(){ printf '\033[1;31mFAIL\033[0m %s\n' "$*" >&2; exit 1; }
info(){ printf '\033[1;36mINFO\033[0m %s\n' "$*"; }

info "R3 base: $R3_BASE"

curl -fsS "$R3_BASE/api/dev/status" >/tmp/r3-dev-status.$$ || fail "R3 dev server status is not reachable"
pass "R3 dev server reachable"

STATUS_JSON="$(curl -fsS "$R3_BASE/api/alexandria/status")" || fail "R3 Alexandria status route failed"
echo "$STATUS_JSON" | python3 -m json.tool
python3 - "$STATUS_JSON" <<'PY' || exit 1
import json,sys
x=json.loads(sys.argv[1])
assert x.get('ok') is True, x
PY
pass "R3 -> LoA status bridge"

SEARCH_JSON="$({ python3 - "$KNOWN_QUERY" <<'PY'
import json,sys
print(json.dumps({'query':sys.argv[1], 'limit':5}))
PY
} | curl -fsS -X POST -H 'Content-Type: application/json' --data-binary @- "$R3_BASE/api/alexandria/search")" || fail "R3 Alexandria search failed"
echo "$SEARCH_JSON" | python3 -m json.tool
python3 - "$SEARCH_JSON" <<'PY' || exit 1
import json,sys
x=json.loads(sys.argv[1])
assert x.get('ok') is True, x
assert 'results' in x and isinstance(x['results'], list), x
PY
pass "R3 -> LoA search bridge"

HTML="$ROOT/rollamacoasterTycoon_R3_rebuilt.html"
[[ -f "$HTML" ]] || fail "Missing R3 artifact: $HTML"
grep -q 'R3_LOA_DEV25_BROWSER_BEGIN' "$HTML" || fail "Browser adapter marker missing"
pass "Browser adapter is present in artifact"

python3 "$(dirname "${BASH_SOURCE[0]}")/r3_guestprofile_const_scan.py" "$HTML" && pass "guestProfile static const scan" || {
  printf '\033[1;33mP0 WARNING\033[0m guestProfile scan found/reported a possible runtime blocker. LoA gate can pass, but dev.25 release should not be called green until the operations crash is resolved.\n'
}

cat <<TXT

DEV.25 BOUNDED LoA GATE COMPLETE

Manual browser checks still required:
  await R3Alexandria.status()
  await R3Alexandria.search(${KNOWN_QUERY@Q}, {limit:5})
  await R3Alexandria.queryForEntity('guest-test', ${KNOWN_QUERY@Q}, {force:true})

Then verify in DevTools > Application > IndexedDB:
  RCT_R3_AlexandriaLive / results

Offline resilience test:
  stop LoA, keep R3 open, verify gameplay continues and status() fails without boot/frame lock.
TXT
