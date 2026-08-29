# Library of Alexandria + rollamacoasterTycoon R3

Short development guide for the local Alexandria knowledge stack used by
rollamacoasterTycoon Revision 3.

This is a development runtime only. It does not install systemd services.

## Location

```text
/home/hstone/Documents/games/rollamacoaster-tycoon/loa-runtime
```

Main manager:

```text
./ALEXANDRIA
```

## Start Alexandria

```bash
cd /home/hstone/Documents/games/rollamacoaster-tycoon/loa-runtime
./ALEXANDRIA start
```

Startup order:

```text
MongoDB
  ↓
Elasticsearch
  ↓
Conductor
  ↓
Queue / Artemis
  ↓
Vault
  ↓
Web / API
  ↓
Indexer
```

## Check status

```bash
./ALEXANDRIA status
```

Expected ports:

```text
27017  MongoDB
9200   Elasticsearch
8092   Conductor
61616  Queue / Artemis
8093   Vault
8090   Alexandria Web/API
11434  Ollama, managed separately
```

## View logs

All recent logs:

```bash
./ALEXANDRIA logs
```

Follow one service:

```bash
./ALEXANDRIA logs conductor
./ALEXANDRIA logs queue
./ALEXANDRIA logs vault
./ALEXANDRIA logs web
./ALEXANDRIA logs indexer
```

## Restart

```bash
./ALEXANDRIA restart
```

## Stop

```bash
./ALEXANDRIA stop
```

## Preflight / doctor

```bash
./ALEXANDRIA doctor
```

## Direct Alexandria tests

Elasticsearch:

```bash
curl -fsS 'http://127.0.0.1:9200/_cluster/health?pretty'
```

Indexed document count:

```bash
curl -fsS \
  'http://127.0.0.1:9200/vault_documents/_count?pretty'
```

Alexandria keyword search:

```bash
curl -sS \
  'http://127.0.0.1:8090/document/find-by/keyword/roller%20coaster/' \
  | python3 -m json.tool
```

An empty successful result is valid when the library contains no matching documents.

## Start R3 with Alexandria

Current development revision example:

```bash
cd /home/hstone/Documents/games/rollamacoaster-tycoon/r3/R3.0-dev.24

bash run_rct_r3_dev.sh 8766
```

The R3 launcher defaults Alexandria to:

```text
http://127.0.0.1:8090
```

R3 game:

```text
http://127.0.0.1:8766/rollamacoasterTycoon_R3_rebuilt.html
```

## Test the R3 → Alexandria bridge

Status:

```bash
curl -sS \
  http://127.0.0.1:8766/api/alexandria/status \
  | python3 -m json.tool
```

Search:

```bash
curl -sS \
  -X POST \
  -H 'Content-Type: application/json' \
  -d '{"query":"roller coaster","limit":5}' \
  http://127.0.0.1:8766/api/alexandria/search \
  | python3 -m json.tool
```

## Architecture

```text
rollamacoasterTycoon R3
        │
        ▼
R3 Python development bridge
        │
        ▼
Alexandria Web/API :8090
        │
        ├── Conductor :8092
        ├── MongoDB :27017
        ├── Elasticsearch :9200
        ├── Queue :61616
        ├── Vault :8093
        └── Indexer
                │
                ▼
          vault_documents
```

Vault document payloads persist under:

```text
loa-runtime/vault/archive/
```

MongoDB and Elasticsearch data persist under:

```text
loa-runtime/mongo/
loa-runtime/elasticsearch/
```

## Development rule

Do not manually insert normal game knowledge directly into Elasticsearch.

Preferred flow:

```text
document
  → Alexandria ingestion
  → Mongo metadata
  → Vault
  → Indexer
  → Elasticsearch
  → R3 KnowledgeBroker
  → entity / guest / staff brain
  → Ollama
```

## R3 development cycle

```text
RELEASE
  → TEST
  → COMMENTS
  → CORE DUMP
  → REVIEW
  → PLAN
  → BUILD
  → RELEASE
```
