# Alexandria Operator Guide

A small operator layer for the local **Library of Alexandria + rollamacoasterTycoon R3** development stack.

This is **not** a system service. It is just a shell helper that sits beside the existing `./ALEXANDRIA` runtime manager.

## Install

Place both files in:

```text
/home/hstone/Documents/games/rollamacoaster-tycoon/loa-runtime/
```

Then:

```bash
cd /home/hstone/Documents/games/rollamacoaster-tycoon/loa-runtime

chmod +x ALEXANDRIA_OPERATOR.sh
```

The operator expects the existing manager here:

```text
./ALEXANDRIA
```

## Daily commands

Start the complete LoA runtime:

```bash
./ALEXANDRIA_OPERATOR.sh start
```

Check it:

```bash
./ALEXANDRIA_OPERATOR.sh status
```

Run a broad smoke test:

```bash
./ALEXANDRIA_OPERATOR.sh smoke
```

Stop it:

```bash
./ALEXANDRIA_OPERATOR.sh stop
```

Restart it:

```bash
./ALEXANDRIA_OPERATOR.sh restart
```

## Logs

Recent logs for every managed service:

```bash
./ALEXANDRIA_OPERATOR.sh logs
```

Follow one service through the existing manager:

```bash
./ALEXANDRIA_OPERATOR.sh logs vault
./ALEXANDRIA_OPERATOR.sh logs staging
./ALEXANDRIA_OPERATOR.sh logs indexer
```

## Count indexed documents

```bash
./ALEXANDRIA_OPERATOR.sh count
```

This reads:

```text
http://127.0.0.1:9200/vault_documents/_count
```

## Search Alexandria directly

```bash
./ALEXANDRIA_OPERATOR.sh search "roller coaster"
```

This uses the LoA Web API on:

```text
http://127.0.0.1:8090
```

## Search through R3

With the R3 development server running on `8766`:

```bash
./ALEXANDRIA_OPERATOR.sh r3-search "roller coaster"
```

Optional result limit:

```bash
./ALEXANDRIA_OPERATOR.sh r3-search "Ferris wheel" 10
```

## Import a local document

```bash
./ALEXANDRIA_OPERATOR.sh import /path/to/document.txt
```

The operator copies the file into:

```text
loa-runtime/import/inbox/
```

and runs the Downloader once in the foreground.

Use a **new filename** for a retried document. LoA's source-location identity is tied to the location/path, so repeatedly rewriting the same failed test path can be treated as an already-known source.

## Direct Staging transaction test

```bash
./ALEXANDRIA_OPERATOR.sh staging-probe
```

Expected result:

```text
PASS: POST → GET(non-destructive) → DELETE
```

This confirms the repaired Staging contract:

```text
POST payload
   ↓
staged file exists
   ↓
GET payload
   ↓
staged file STILL exists
   ↓
DELETE payload
   ↓
staged file removed
```

## Critical directory rule

These two directories must remain separate:

```text
Downloader private work:
loa-runtime/downloader-work/

Staging server storage:
loa-runtime/staging/
```

Do **not** point both configurations at the same directory.

The Downloader creates temporary working files and cleans them up when its local processing scope closes. If that workspace is also the Staging server's durable handoff directory, Downloader cleanup can delete the payload before Vault retrieves it.

Check the configured values:

```bash
grep '^loa.downloader.staging-directory' \
  config/downloader/application.properties

grep '^loa.staging.location' \
  config/staging/application.properties
```

Expected pattern:

```text
loa.downloader.staging-directory=.../loa-runtime/downloader-work
loa.staging.location=.../loa-runtime/staging
```

## Working architecture

```text
local document
      │
      ▼
Downloader
      │
      ├── private work: downloader-work/
      │
      ▼
Staging :8099
      │
      ├── durable handoff: staging/
      │
      ▼
Queue / Artemis :61616
      │
      ▼
Vault :8093
      │
      ├── SQLite document storage
      │
      ▼
MongoDB :27017
      │
      ▼
Indexer
      │
      ▼
Elasticsearch :9200
      │
      ▼
LoA Web/API :8090
      │
      ▼
R3 Alexandria bridge :8766
      │
      ▼
KnowledgeBroker / entities / guest brains / Ollama
```

## Current runtime ports

```text
27017  MongoDB
9200   Elasticsearch
8092   Conductor
61616  Queue / Artemis
8099   Staging
8093   Vault
8090   LoA Web/API
11434  Ollama, managed separately
8766   R3 development server, when running
```

A single-node Elasticsearch cluster may report `yellow` because replica shards cannot be assigned to a second node. Primary shards can still be healthy and usable for this development runtime.

## Smoke-test philosophy

Before changing the game integration, establish that the knowledge stack itself is green:

```bash
./ALEXANDRIA_OPERATOR.sh smoke
./ALEXANDRIA_OPERATOR.sh staging-probe
./ALEXANDRIA_OPERATOR.sh search "GREEN"
```

Then test R3:

```bash
./ALEXANDRIA_OPERATOR.sh r3-search "GREEN"
```

The desired path is:

```text
LoA healthy
   ↓
search healthy
   ↓
R3 bridge healthy
   ↓
entity knowledge integration
```

That keeps infrastructure failures separate from game-code failures.
