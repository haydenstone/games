#!/bin/sh
set -u
IMAGE="rct-r5-dev5"; NAME="rct-r5"; PORT="${R5_PORT:-8765}"; CODEX="${CODEX_PATH_HOST:-$HOME/Documents/codex.json}"; ROOT=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd); DATA="$ROOT/data"
bold='\033[1m'; dim='\033[2m'; green='\033[32m'; yellow='\033[33m'; red='\033[31m'; cyan='\033[36m'; reset='\033[0m'
logo(){ printf "${cyan}${bold}🎢 R5 // Ava World Runtime${reset}\n${dim}   one world • one port • external Codex${reset}\n\n"; }
exists(){ docker inspect "$NAME" >/dev/null 2>&1; }; running(){ [ "$(docker inspect -f '{{.State.Running}}' "$NAME" 2>/dev/null || true)" = true ]; }
info(){ logo; printf "🐳 Image       ${bold}%s${reset}\n📦 Container   %s\n🌐 Gameplay    http://127.0.0.1:%s\n📖 Codex       %s\n💾 Data        %s\n" "$IMAGE" "$NAME" "$PORT" "$CODEX" "$DATA"; if running;then printf "🟢 State       ${green}RUNNING${reset}\n";docker inspect -f '⏱  Started     {{.State.StartedAt}}\n🔌 Ports       {{json .NetworkSettings.Ports}}' "$NAME";elif exists;then printf "🟡 State       ${yellow}STOPPED${reset}\n";else printf "⚪ State       not created\n";fi; }
need_codex(){ [ -f "$CODEX" ] || { printf "${red}📕 Codex missing:${reset} %s\nSet CODEX_PATH_HOST if it lives elsewhere.\n" "$CODEX"; exit 2; }; }
build(){ logo; printf "🔨 Building ${bold}%s${reset}...\n" "$IMAGE"; docker build -t "$IMAGE" "$ROOT"; }
start(){ need_codex; mkdir -p "$DATA"; if running;then printf "🟢 %s is already running on port %s.\n" "$NAME" "$PORT";exit 0;fi; docker rm -f "$NAME" >/dev/null 2>&1 || true; docker image inspect "$IMAGE" >/dev/null 2>&1 || build; logo; printf "🚀 Starting Ava...\n";docker run -d --name "$NAME" -p "$PORT:8765" -v "$DATA:/app/data" -v "$CODEX:/codex/codex.json:ro" "$IMAGE" >/dev/null; sleep 1; info; printf "\n📜 Recent log\n";docker logs --tail 8 "$NAME"; }
stop(){ logo;if exists;then printf "🛑 Stopping %s...\n" "$NAME";docker rm -f "$NAME" >/dev/null;printf "✅ Stopped and removed. Port %s is free.\n" "$PORT";else printf "⚪ Nothing to stop.\n";fi; }
testit(){ need_codex; docker image inspect "$IMAGE" >/dev/null 2>&1 || build; logo;printf "🧪 Running self-starting integration test...\n";docker run --rm -v "$CODEX:/codex/codex.json:ro" "$IMAGE" npm test; }
logs(){ docker logs -f --tail 50 "$NAME"; }
case "${1:-status}" in start)start;;stop)stop;;restart)stop;start;;status|info)info;;build)build;;test)testit;;logs)logs;;*)logo;printf "Usage: ./start.sh {status|start|stop|restart|build|test|logs|info}\n";exit 1;;esac
