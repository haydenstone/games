#!/bin/sh
set -eu
IMAGE=rct-r5-dev8; NAME=rct-r5; PORT=${R5_PORT:-8765}; CODEX=${CODEX_PATH_HOST:-$HOME/Documents/codex.json}; ROOT=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd); DATA=$ROOT/data
logo(){ printf '\n🎢 R5 dev.8  🧭 runtime v4 actors  📖 external Codex  🚶 first guest\n'; }
need(){ [ -f "$CODEX" ] || { printf '📕 Missing %s\n' "$CODEX"; exit 2; }; }
build(){ logo; docker build -t "$IMAGE" "$ROOT"; }
start(){ need; mkdir -p "$DATA"; docker rm -f "$NAME" >/dev/null 2>&1 || true; docker image inspect "$IMAGE" >/dev/null 2>&1 || build; docker run -d --name "$NAME" -p "$PORT:8765" -v "$DATA:/app/data" -v "$CODEX:/codex/codex.json:ro" "$IMAGE" >/dev/null; printf '🟢 Running  http://127.0.0.1:%s\n📖 Codex   %s\n💾 Data    %s\n' "$PORT" "$CODEX" "$DATA"; }
stop(){ docker rm -f "$NAME" >/dev/null 2>&1 || true; printf '🛑 R5 stopped; port %s released.\n' "$PORT"; }
testit(){ need; docker image inspect "$IMAGE" >/dev/null 2>&1 || build; docker run --rm -v "$CODEX:/codex/codex.json:ro" "$IMAGE" npm test; }
status(){ logo; if [ "$(docker inspect -f '{{.State.Running}}' "$NAME" 2>/dev/null || true)" = true ];then printf '🟢 RUNNING http://127.0.0.1:%s\n' "$PORT";docker logs --tail 3 "$NAME";else printf '⚪ STOPPED\n';fi; }
case "${1:-start}" in start)start;;stop)stop;;restart)stop;start;;test)testit;;status)status;;build)build;;*)printf 'Usage: ./start.sh {start|stop|restart|test|status|build}\n';exit 1;;esac
