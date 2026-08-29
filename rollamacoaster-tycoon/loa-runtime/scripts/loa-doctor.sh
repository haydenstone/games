#!/usr/bin/env bash
set -u

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo '==================================================='
echo ' RCT // LIBRARY OF ALEXANDRIA PRE-FLIGHT DOCTOR'
echo '==================================================='

echo
echo '--- Memory ---'
free -h

echo
echo '--- Disk ---'
df -h "$ROOT"

echo
echo '--- Java ---'
java -version 2>&1 | head -3

echo
echo '--- Docker ---'
docker --version
docker compose version

echo
echo '--- vm.max_map_count ---'
sysctl vm.max_map_count

echo
echo '--- Runtime binaries ---'
for f in \
  bin/loa-conductor.jar \
  bin/loa-vault.jar \
  bin/loa-web.jar
do
  if [[ -r "$f" ]]; then
    printf 'OK   %-24s -> %s\n' "$f" "$(readlink -f "$f")"
  else
    printf 'FAIL %s\n' "$f"
  fi
done

echo
echo '--- Config files ---'
for f in \
  compose.yaml \
  config/conductor/application.properties \
  config/vault/application.properties \
  config/web/application.properties
do
  if [[ -r "$f" ]]; then
    echo "OK   $f"
  else
    echo "FAIL $f"
  fi
done

echo
echo '--- Compose validation ---'
docker compose config >/dev/null \
  && echo 'OK   compose.yaml' \
  || echo 'FAIL compose.yaml'

echo
echo '--- Planned ports ---'
for port in 27017 9200 8092 8093 8090; do
  if ss -ltn 2>/dev/null | grep -q ":${port}[[:space:]]"; then
    echo "BUSY :$port"
  else
    echo "FREE :$port"
  fi
done

echo
echo '--- Existing external services ---'
curl -fsS --max-time 2 http://127.0.0.1:11434/api/version \
  >/dev/null 2>&1 \
  && echo 'LIVE Ollama :11434' \
  || echo 'OFF  Ollama :11434'

echo
echo '--- Docker containers ---'
docker compose ps -a

echo
echo 'Pre-flight complete.'
