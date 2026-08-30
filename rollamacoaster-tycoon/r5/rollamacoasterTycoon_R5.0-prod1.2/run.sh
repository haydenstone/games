#!/bin/sh
set -eu
IMAGE=rct-r5-prod1-2
NAME=rct-r5
PORT=${R5_PORT:-8765}
CODEX=${CODEX_PATH_HOST:-$HOME/Documents/codex.json}
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
DATA="$ROOT/data"
OTP_FILE="$DATA/developer-otp"
OLLAMA=${OLLAMA_BASE_URL:-http://host.docker.internal:11434}
REMOTE_URL=${R5_REMOTE_STATE_URL:-}
REMOTE_TOKEN=${R5_REMOTE_STATE_TOKEN:-}
need_codex(){ [ -f "$CODEX" ] || { echo "Codex not found: $CODEX"; echo "Set CODEX_PATH_HOST=/path/to/codex.json"; exit 2; }; }
build(){ docker build -t "$IMAGE" "$ROOT"; }
stop(){ docker rm -f "$NAME" >/dev/null 2>&1 || true; }
start(){
  need_codex; mkdir -p "$DATA"; stop
  docker image inspect "$IMAGE" >/dev/null 2>&1 || build
  docker run -d --name "$NAME" --add-host=host.docker.internal:host-gateway \
    -p "$PORT:8765" -v "$DATA:/app/data" -v "$CODEX:/codex/codex.json:ro" \
    -e OLLAMA_BASE_URL="$OLLAMA" -e R5_PROVISION_FILE=/app/data/developer-otp \
    -e R5_REMOTE_STATE_URL="$REMOTE_URL" -e R5_REMOTE_STATE_TOKEN="$REMOTE_TOKEN" \
    "$IMAGE" >/dev/null
  echo "R5.0-prod1.2 started: http://127.0.0.1:$PORT"
  i=0
  while [ "$i" -lt 100 ]; do
    if docker exec "$NAME" sh -c 'test -s /app/data/developer-otp' >/dev/null 2>&1; then
      echo "Developer Mode one-use key: $(docker exec "$NAME" sh -c 'cat /app/data/developer-otp' | tr -d '\r\n')"
      return
    fi
    if docker logs "$NAME" 2>&1 | grep -q 'developer OTP already enabled'; then
      echo "Developer Mode is already enabled for this persisted world."
      return
    fi
    sleep 0.1; i=$((i+1))
  done
  echo "Developer OTP was not provisioned before timeout. Inspect: ./run.sh logs"
}
case "${1:-start}" in
  start) start ;;
  stop) stop; echo "R5 stopped" ;;
  restart) stop; start ;;
  build) build ;;
  status) docker ps --filter "name=^/$NAME$" ;;
  logs) docker logs "$NAME" ;;
  provision) docker exec "$NAME" sh -c 'test -s /app/data/developer-otp && printf "Developer Mode one-use key: " && cat /app/data/developer-otp' || { echo "No active OTP. Developer Mode may already be enabled."; exit 1; } ;;
  test) need_codex; docker run --rm --add-host=host.docker.internal:host-gateway -v "$CODEX:/codex/codex.json:ro" -v "$ROOT:/work" -w /work -e CODEX_PATH=/codex/codex.json node:22-alpine node tests/smoke.mjs ;;
  *) echo "usage: $0 start|stop|restart|build|status|logs|provision|test"; exit 1 ;;
esac
