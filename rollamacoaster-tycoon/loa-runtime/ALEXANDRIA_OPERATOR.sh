#!/usr/bin/env bash
set -euo pipefail

# Library of Alexandria operator helper for rollamacoasterTycoon R3.
# Put this file in:
#   /home/hstone/Documents/games/rollamacoaster-tycoon/loa-runtime/
#
# It does NOT install a system service. It is only a small operator wrapper.

ROOT="$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")" && pwd)"
cd "$ROOT"

MANAGER="${LOA_MANAGER:-$ROOT/ALEXANDRIA}"
DOWNLOADER_JAR="${LOA_DOWNLOADER_JAR:-$ROOT/bin/loa-downloader.jar}"
DOWNLOADER_CONFIG="${LOA_DOWNLOADER_CONFIG:-$ROOT/config/downloader/application.properties}"

LOA_WEB="${LOA_WEB:-http://127.0.0.1:8090}"
ELASTIC="${LOA_ELASTIC:-http://127.0.0.1:9200}"
R3_BASE="${R3_BASE:-http://127.0.0.1:8766}"

INBOX="$ROOT/import/inbox"
FORENSICS="$ROOT/import/forensics"
DOWNLOADER_WORK="$ROOT/downloader-work"
STAGING="$ROOT/staging"

say() {
  printf '\n\033[1;36m==> %s\033[0m\n' "$*"
}

warn() {
  printf '\033[1;33mWARN:\033[0m %s\n' "$*" >&2
}

die() {
  printf '\033[1;31mERROR:\033[0m %s\n' "$*" >&2
  exit 1
}

require_file() {
  [[ -e "$1" ]] || die "Missing: $1"
}

json_pretty() {
  python3 -m json.tool
}

status() {
  require_file "$MANAGER"
  "$MANAGER" status
}

start() {
  require_file "$MANAGER"
  "$MANAGER" start
}

stop() {
  require_file "$MANAGER"
  "$MANAGER" stop
}

restart() {
  require_file "$MANAGER"
  "$MANAGER" restart
}

logs() {
  require_file "$MANAGER"
  "$MANAGER" logs "${1:-}"
}

search_loa() {
  local q="${1:-}"
  [[ -n "$q" ]] || die "Usage: $0 search \"search terms\""

  local encoded
  encoded="$(
    python3 - "$q" <<'PY'
import sys, urllib.parse
print(urllib.parse.quote(sys.argv[1], safe=""))
PY
  )"

  curl -fsS \
    "$LOA_WEB/document/find-by/keyword/$encoded/" \
    | json_pretty
}

search_r3() {
  local q="${1:-}"
  local limit="${2:-5}"
  [[ -n "$q" ]] || die "Usage: $0 r3-search \"search terms\" [limit]"

  python3 - "$q" "$limit" <<'PY' | \
    curl -fsS \
      -X POST \
      -H 'Content-Type: application/json' \
      --data-binary @- \
      "$R3_BASE/api/alexandria/search" \
    | python3 -m json.tool
import json, sys
print(json.dumps({
    "query": sys.argv[1],
    "limit": int(sys.argv[2]),
}))
PY
}

count_docs() {
  curl -fsS "$ELASTIC/vault_documents/_count" \
    | python3 -c 'import json,sys; print(json.load(sys.stdin)["count"])'
}

import_file() {
  local src="${1:-}"
  [[ -n "$src" ]] || die "Usage: $0 import /path/to/document"
  [[ -f "$src" ]] || die "Not a file: $src"

  require_file "$DOWNLOADER_JAR"
  require_file "$DOWNLOADER_CONFIG"

  mkdir -p "$INBOX" "$FORENSICS" "$DOWNLOADER_WORK" "$STAGING"

  local name
  name="$(basename "$src")"

  if [[ -e "$INBOX/$name" ]]; then
    die "Inbox already contains $name. Use a new filename so LoA receives a new source-location identity."
  fi

  cp -v "$src" "$INBOX/$name"

  say "Importing $name"
  java \
    -Xms128m \
    -Xmx1024m \
    -jar "$DOWNLOADER_JAR" \
    --spring.config.additional-location="file:$DOWNLOADER_CONFIG"

  say "Current indexed document count"
  count_docs
}

smoke() {
  say "Operator smoke test"

  echo "--- manager ---"
  status

  echo
  echo "--- Elasticsearch HTTP ---"
  curl -fsS "$ELASTIC/_cluster/health?pretty" | json_pretty

  echo
  echo "--- indexed documents ---"
  printf 'count='
  count_docs

  echo
  echo "--- LoA Web search endpoint ---"
  curl -fsS \
    "$LOA_WEB/document/find-by/keyword/GREEN/" \
    | json_pretty

  echo
  echo "--- R3 Alexandria bridge status ---"
  if curl -fsS "$R3_BASE/api/alexandria/status" >/tmp/rct-loa-r3-status.$$ 2>/dev/null; then
    cat /tmp/rct-loa-r3-status.$$ | json_pretty
    rm -f /tmp/rct-loa-r3-status.$$
  else
    warn "R3 bridge is not reachable at $R3_BASE. LoA itself may still be healthy."
    rm -f /tmp/rct-loa-r3-status.$$ 2>/dev/null || true
  fi

  echo
  echo "--- workspace separation ---"
  local dl_stage server_stage
  dl_stage="$(grep '^loa.downloader.staging-directory=' "$DOWNLOADER_CONFIG" 2>/dev/null | cut -d= -f2- || true)"
  server_stage="$(grep '^loa.staging.location=' "$ROOT/config/staging/application.properties" 2>/dev/null | cut -d= -f2- || true)"

  echo "downloader-work: ${dl_stage:-<unset>}"
  echo "staging-store:   ${server_stage:-<unset>}"

  if [[ -n "$dl_stage" && -n "$server_stage" && "$dl_stage" == "$server_stage" ]]; then
    die "Downloader work directory and Staging server directory MUST be different."
  fi

  say "Smoke test complete"
}

staging_probe() {
  local test_id="11111111-2222-4333-8444-555555555555"
  local payload="/tmp/loa-stage-direct-test.txt"

  printf 'ALEXANDRIA STAGING DIRECT TEST\n' > "$payload"

  say "Direct Staging POST"
  curl -fsS \
    -F "file=@$payload;type=application/octet-stream" \
    "http://127.0.0.1:8099/document/$test_id" \
    -o /dev/null

  [[ -f "$STAGING/$test_id" ]] \
    || die "Staging POST returned but expected file was not created."

  say "Direct Staging GET"
  local body
  body="$(curl -fsS "http://127.0.0.1:8099/document/$test_id")"
  [[ "$body" == "ALEXANDRIA STAGING DIRECT TEST" ]] \
    || die "Unexpected Staging GET body."

  [[ -f "$STAGING/$test_id" ]] \
    || die "GET consumed the staged file. Transactional non-destructive GET is not active."

  say "Direct Staging DELETE"
  curl -fsS \
    -X DELETE \
    "http://127.0.0.1:8099/document/$test_id" \
    -o /dev/null

  [[ ! -e "$STAGING/$test_id" ]] \
    || die "Staging DELETE did not remove the test payload."

  echo "PASS: POST → GET(non-destructive) → DELETE"
}

help_text() {
  cat <<'EOF'
ALEXANDRIA OPERATOR

Usage:
  ./ALEXANDRIA_OPERATOR.sh start
  ./ALEXANDRIA_OPERATOR.sh stop
  ./ALEXANDRIA_OPERATOR.sh restart
  ./ALEXANDRIA_OPERATOR.sh status
  ./ALEXANDRIA_OPERATOR.sh logs [service]
  ./ALEXANDRIA_OPERATOR.sh count
  ./ALEXANDRIA_OPERATOR.sh search "terms"
  ./ALEXANDRIA_OPERATOR.sh r3-search "terms" [limit]
  ./ALEXANDRIA_OPERATOR.sh import /path/to/document
  ./ALEXANDRIA_OPERATOR.sh staging-probe
  ./ALEXANDRIA_OPERATOR.sh smoke

Environment overrides:
  LOA_WEB=http://127.0.0.1:8090
  LOA_ELASTIC=http://127.0.0.1:9200
  R3_BASE=http://127.0.0.1:8766
EOF
}

case "${1:-help}" in
  start)         start ;;
  stop)          stop ;;
  restart)       restart ;;
  status)        status ;;
  logs)          logs "${2:-}" ;;
  count)         count_docs ;;
  search)        search_loa "${2:-}" ;;
  r3-search)     search_r3 "${2:-}" "${3:-5}" ;;
  import)        import_file "${2:-}" ;;
  staging-probe) staging_probe ;;
  smoke)         smoke ;;
  help|-h|--help) help_text ;;
  *) die "Unknown command: $1. Run: $0 help" ;;
esac
