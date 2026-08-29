#!/usr/bin/env bash

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo '=== CONDUCTOR ==='
tail -40 "$ROOT/logs/conductor.log" 2>/dev/null || true

echo
echo '=== VAULT ==='
tail -40 "$ROOT/logs/vault.log" 2>/dev/null || true

echo
echo '=== WEB ==='
tail -40 "$ROOT/logs/web.log" 2>/dev/null || true
