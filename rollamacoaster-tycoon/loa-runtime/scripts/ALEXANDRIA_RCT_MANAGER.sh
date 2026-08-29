#!/usr/bin/env bash

set -u

SCRIPT_PATH="$(readlink -f "${BASH_SOURCE[0]}")"
ROOT="$(cd "$(dirname "$SCRIPT_PATH")/.." && pwd)"
cd "$ROOT"

mkdir -p run logs

CONDUCTOR_PORT=8092
QUEUE_PORT=61616
VAULT_PORT=8093
STAGING_PORT=8099
WEB_PORT=8090
MONGO_PORT=27017
ES_PORT=9200

JAVA_BIN="${JAVA_BIN:-java}"

# Heap sizes can be overridden from the shell if needed.
CONDUCTOR_HEAP="${LOA_CONDUCTOR_HEAP:-512m}"
QUEUE_HEAP="${LOA_QUEUE_HEAP:-768m}"
VAULT_HEAP="${LOA_VAULT_HEAP:-768m}"
STAGING_HEAP="${LOA_STAGING_HEAP:-512m}"
WEB_HEAP="${LOA_WEB_HEAP:-768m}"
INDEXER_HEAP="${LOA_INDEXER_HEAP:-1536m}"

say() {
    printf '\n\033[1;36m==> %s\033[0m\n' "$*"
}

warn() {
    printf '\033[1;33mWARN:\033[0m %s\n' "$*" >&2
}

fail() {
    printf '\033[1;31mERROR:\033[0m %s\n' "$*" >&2
    exit 1
}

pid_file() {
    echo "$ROOT/run/$1.pid"
}

log_file() {
    echo "$ROOT/logs/$1.log"
}

is_running() {
    local name="$1"
    local pf
    pf="$(pid_file "$name")"

    [[ -f "$pf" ]] || return 1

    local pid
    pid="$(cat "$pf" 2>/dev/null || true)"

    [[ -n "$pid" ]] || return 1
    kill -0 "$pid" 2>/dev/null
}

port_live() {
    local port="$1"
    ss -ltn 2>/dev/null | grep -q ":${port}[[:space:]]"
}

wait_port() {
    local name="$1"
    local port="$2"
    local tries="${3:-30}"

    for ((i=1; i<=tries; i++)); do
        if port_live "$port"; then
            echo "LIVE $name :$port"
            return 0
        fi

        sleep 1
    done

    warn "$name did not open :$port"
    return 1
}

start_java() {
    local name="$1"
    local jar="$2"
    local config="$3"
    local heap="$4"

    if is_running "$name"; then
        echo "$name already running PID $(cat "$(pid_file "$name")")"
        return 0
    fi

    [[ -r "$jar" ]] || fail "Missing JAR: $jar"
    [[ -r "$config" ]] || fail "Missing config: $config"

    rm -f "$(pid_file "$name")"

    say "Starting $name"

    nohup "$JAVA_BIN" \
        -Xms128m \
        -Xmx"$heap" \
        -jar "$jar" \
        --spring.config.additional-location="file:$config" \
        > "$(log_file "$name")" 2>&1 &

    local pid=$!
    echo "$pid" > "$(pid_file "$name")"

    sleep 2

    if kill -0 "$pid" 2>/dev/null; then
        echo "$name PID $pid"
    else
        warn "$name exited during startup"
        tail -80 "$(log_file "$name")" || true
        return 1
    fi
}

stop_java() {
    local name="$1"
    local pf
    pf="$(pid_file "$name")"

    if ! is_running "$name"; then
        rm -f "$pf"
        echo "$name already stopped"
        return 0
    fi

    local pid
    pid="$(cat "$pf")"

    say "Stopping $name PID $pid"

    kill "$pid" 2>/dev/null || true

    for _ in {1..15}; do
        if ! kill -0 "$pid" 2>/dev/null; then
            rm -f "$pf"
            echo "$name stopped"
            return 0
        fi
        sleep 1
    done

    warn "$name did not exit gracefully; sending SIGKILL"
    kill -9 "$pid" 2>/dev/null || true
    rm -f "$pf"
}

start_infra() {
    say "Starting MongoDB + Elasticsearch"

    docker compose up -d mongo elasticsearch || fail "Docker infrastructure failed"

    wait_port "MongoDB" "$MONGO_PORT" 30 || return 1

    say "Waiting for Elasticsearch HTTP API"

    local es_ready=0

    for i in {1..90}; do
        if curl -fsS \
            http://127.0.0.1:9200/_cluster/health \
            >/dev/null 2>&1
        then
            es_ready=1
            echo "LIVE Elasticsearch HTTP API"
            break
        fi

        if ! docker compose ps --status running elasticsearch \
            | grep -q rct-loa-elasticsearch
        then
            warn "Elasticsearch container stopped during startup"
            docker compose logs --tail=120 elasticsearch
            return 1
        fi

        printf 'Waiting for Elasticsearch HTTP... %d/90\r' "$i"
        sleep 1
    done

    echo

    if [[ "$es_ready" -ne 1 ]]; then
        warn "Elasticsearch HTTP API did not become ready"
        docker compose logs --tail=120 elasticsearch
        return 1
    fi

    curl -fsS \
        'http://127.0.0.1:9200/_cluster/health?pretty' \
        || return 1
}

start_all() {
    start_infra || exit 1

    start_java \
        conductor \
        "$ROOT/bin/loa-conductor.jar" \
        "$ROOT/config/conductor/application.properties" \
        "$CONDUCTOR_HEAP" || exit 1

    wait_port "Conductor" "$CONDUCTOR_PORT" 30 || exit 1

    start_java \
        queue \
        "$ROOT/bin/loa-queue.jar" \
        "$ROOT/config/queue/application.properties" \
        "$QUEUE_HEAP" || exit 1

    wait_port "Queue" "$QUEUE_PORT" 30 || exit 1

    start_java \
        staging \
        "$ROOT/bin/loa-staging.jar" \
        "$ROOT/config/staging/application.properties" \
        "$STAGING_HEAP" || exit 1

    wait_port "Staging" "$STAGING_PORT" 30 || exit 1

    start_java \
        vault \
        "$ROOT/bin/loa-vault.jar" \
        "$ROOT/config/vault/application.properties" \
        "$VAULT_HEAP" || exit 1

    wait_port "Vault" "$VAULT_PORT" 30 || exit 1

    start_java \
        web \
        "$ROOT/bin/loa-web.jar" \
        "$ROOT/config/web/application.properties" \
        "$WEB_HEAP" || exit 1

    wait_port "Web/API" "$WEB_PORT" 30 || exit 1

    start_java \
        indexer \
        "$ROOT/bin/loa-indexer.jar" \
        "$ROOT/config/indexer/application.properties" \
        "$INDEXER_HEAP" || exit 1

    say "LoA stack started"

    status_all
}

stop_all() {
    # Reverse dependency order.
    stop_java indexer
    stop_java web
    stop_java vault
    stop_java staging
    stop_java queue
    stop_java conductor

    say "Stopping MongoDB + Elasticsearch"
    docker compose stop elasticsearch mongo

    say "LoA stack stopped"
}

service_status() {
    local name="$1"
    local port="${2:-}"

    if is_running "$name"; then
        printf 'LIVE %-12s PID %-8s' \
            "$name" \
            "$(cat "$(pid_file "$name")")"
    else
        printf 'OFF  %-12s %-12s' "$name" ""
    fi

    if [[ -n "$port" ]]; then
        if port_live "$port"; then
            printf ' :%s LISTENING' "$port"
        else
            printf ' :%s CLOSED' "$port"
        fi
    fi

    echo
}

status_all() {
    echo
    echo '==================================================='
    echo ' LIBRARY OF ALEXANDRIA // RCT DEVELOPMENT RUNTIME'
    echo '==================================================='

    echo
    echo '--- Docker ---'
    docker compose ps

    echo
    echo '--- Java services ---'
    service_status conductor "$CONDUCTOR_PORT"
    service_status queue "$QUEUE_PORT"
    service_status staging "$STAGING_PORT"
    service_status vault "$VAULT_PORT"
    service_status web "$WEB_PORT"
    service_status indexer

    echo
    echo '--- Infrastructure ports ---'

    for pair in \
        "MongoDB:$MONGO_PORT" \
        "Elasticsearch:$ES_PORT"
    do
        name="${pair%%:*}"
        port="${pair##*:}"

        if port_live "$port"; then
            echo "LIVE $name :$port"
        else
            echo "OFF  $name :$port"
        fi
    done

    echo
    echo '--- Elasticsearch ---'
    curl -fsS \
        http://127.0.0.1:9200/_cluster/health\?pretty \
        2>/dev/null || echo 'Unavailable'

    echo
    echo '--- Alexandria search index ---'
    curl -fsS \
        'http://127.0.0.1:9200/vault_documents/_count?pretty' \
        2>/dev/null || echo 'vault_documents unavailable'

    echo
    echo '--- Memory ---'
    free -h
}

show_logs() {
    local service="${1:-}"

    if [[ -n "$service" ]]; then
        local lf
        lf="$(log_file "$service")"

        [[ -f "$lf" ]] || fail "No log for '$service': $lf"

        tail -f "$lf"
        return
    fi

    for name in conductor queue staging vault web indexer; do
        echo
        echo "================ $name ================"
        tail -30 "$(log_file "$name")" 2>/dev/null || true
    done
}

doctor() {
    if [[ -x "$ROOT/scripts/loa-doctor.sh" ]]; then
        exec "$ROOT/scripts/loa-doctor.sh"
    fi

    status_all
}

case "${1:-status}" in
    start)
        start_all
        ;;

    stop)
        stop_all
        ;;

    restart)
        stop_all
        start_all
        ;;

    status)
        status_all
        ;;

    logs)
        show_logs "${2:-}"
        ;;

    doctor)
        doctor
        ;;

    *)
        cat <<USAGE
Usage:
  $0 start
  $0 stop
  $0 restart
  $0 status
  $0 logs
  $0 logs <conductor|queue|vault|web|indexer>
  $0 doctor

This is a development process manager only.
It does NOT install or create system services.
USAGE
        exit 1
        ;;
esac
