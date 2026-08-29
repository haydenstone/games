#!/usr/bin/env bash
set -euo pipefail
R3_BASE="${1:-http://127.0.0.1:8765}"
KNOWN_QUERY="${R3_LOA_TEST_QUERY:-GREEN}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
DEV25="$ROOT/tools/r3_loa_dev25/R3_LOA_DEV25_GATE.sh"
HTML="$ROOT/rollamacoasterTycoon_R3_rebuilt.html"

pass(){ printf '\033[1;32mPASS\033[0m %s\n' "$*"; }
fail(){ printf '\033[1;31mFAIL\033[0m %s\n' "$*" >&2; exit 1; }
info(){ printf '\033[1;36mINFO\033[0m %s\n' "$*"; }

[[ -x "$DEV25" ]] || fail "Missing dev.25 LoA transport gate"
info "Running proven dev.25 LoA transport/cache gate first"
R3_LOA_TEST_QUERY="$KNOWN_QUERY" bash "$DEV25" "$R3_BASE"

python3 "$(dirname "${BASH_SOURCE[0]}")/r3_dev26_contract_scan.py" "$HTML" || fail "dev.26 native guest knowledge contract"
pass "Dev.26 native guest knowledge bridge is present"

cat <<TXT

DEV.26 LoA guest knowledge gate complete

Manual browser acceptance:

1. Make sure at least one guest is in the park, then in DevTools Console:

   const guestId = R3GuestAlexandria.firstGuest()
   guestId

2. Adopt a real Alexandria result into that guest:

   const learned = await R3GuestAlexandria.researchGuest(guestId, ${KNOWN_QUERY@Q}, {force:true, limit:5})
   learned

   Pass: learned.ok === true, learned.hits >= 1, and learned.added >= 1 on the first run.

3. Inspect native guest state + brain:

   const beforeSave = await R3GuestAlexandria.inspect(guestId)
   beforeSave.guest.alexandriaKnowledge
   beforeSave.guest.alexandriaBias
   beforeSave.brain.research
   beforeSave.brain.knowledge

   Pass: the LoA source appears in both guest state and guestBrains research/knowledge.

4. Open that guest in the game UI.

   Pass: the "Alexandria knowledge" card appears, uses normal-case labels,
   shows learned/search counts, and lists retained source information.

5. Save the park from the normal game UI. Reload that save without clearing IndexedDB.
   Re-open the same guest and run:

   await R3GuestAlexandria.inspect(guestId)

   Pass: Alexandria knowledge, research history, counts, and bias survive load.

6. With Ollama online, chat with that guest about the learned topic.

   Pass: the answer remains first-person and can use retained Alexandria knowledge.
   The chat path may perform a bounded entity search automatically.

7. Offline isolation:

   Stop Alexandria while R3 stays open. Research should report unavailable/offline,
   but camera, simulation, guests, UI, save/load, and local guest brain must continue.
   Restart Alexandria and research again without reloading R3.

If all seven pass, dev.26 proves:
LoA -> entity lookup -> native guest brain -> conversation context -> bounded decisions -> save/load persistence.
TXT
