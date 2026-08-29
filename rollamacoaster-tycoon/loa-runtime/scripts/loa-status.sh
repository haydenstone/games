#!/usr/bin/env bash

echo '=== CONTAINERS ==='
docker compose ps -a

echo
echo '=== PORTS ==='
for port in 27017 9200 8092 8093 8090 61616; do
  if ss -ltn 2>/dev/null | grep -q ":${port}[[:space:]]"; then
    echo "LIVE :$port"
  else
    echo "OFF  :$port"
  fi
done

echo
echo '=== JAVA PROCESSES ==='
ps -ef | grep '[l]oa-.*\.jar' || true

echo
echo '=== MEMORY ==='
free -h
