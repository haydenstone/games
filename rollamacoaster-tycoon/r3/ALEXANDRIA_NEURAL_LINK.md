# R3.0-dev.25 — Alexandria Neural Link

Revision 3 treats the Library of Alexandria (LoA) as an external searchable knowledge ocean, not as data to mirror into the browser.

## Data flow

```text
Guest / Worker / Wildlife / World Entity / Park Research / Guest Flock
                               │
                               ▼
                        KnowledgeBroker
                   ┌───────────┼───────────┐
                   ▼           ▼           ▼
          AlexandriaSource   Codex    local Alexandria
                   │
          same-origin R3 bridge
             /api/alexandria/*
                   │
                   ▼
         LoA Web Application API
                   │
          Elasticsearch + Vault
```

The browser never receives Elasticsearch credentials or an arbitrary upstream URL. `rct_r3_dev_server.py` owns the configured LoA Web Application base and only exposes the narrow proxy surface below.

## Bridge configuration

Normal R3 still runs with no LoA installation:

```bash
bash run_rct_r3_dev.sh 8765
```

To connect a running Library of Alexandria Web Application:

```bash
RCT_LOA_BASE=http://127.0.0.1:8081 bash run_rct_r3_dev.sh 8765
```

Replace `8081` with the actual LoA Web Application port in your installation.

Optional controls:

```bash
RCT_LOA_TIMEOUT=6 \
RCT_LOA_ARCHIVE_MAX_BYTES=16777216 \
RCT_LOA_BASE=http://127.0.0.1:8081 \
bash run_rct_r3_dev.sh 8765
```

You can also invoke the server directly:

```bash
python3 rct_r3_dev_server.py \
  --port 8765 \
  --loa-base http://127.0.0.1:8081 \
  --loa-timeout 6 \
  --loa-archive-max 16777216
```

## R3 bridge endpoints

```text
GET  /api/alexandria/status
POST /api/alexandria/search
GET  /api/alexandria/document/:id
GET  /api/alexandria/document/:id/debug
POST /api/alexandria/cache/prefetch
```

The search proxy maps to LoA's Web Application route:

```text
/document/find-by/keyword/{query}/
```

with the same result-size, exact-match, language, document-length and document-type filters used by the LoA frontend.

## IndexedDB schema v5

Revision 3 keeps the older synthetic `alexandria` store as a local/offline knowledge source and adds three stores for the live archive link.

### alexandriaDocuments

One normalized record per LoA document actually encountered by this park/browser profile.

```js
{
  id: "alexandria:<sourceId>",
  sourceId: "<LoA document id>",
  title: "...",
  author: "...",
  description: ["..."],
  snippet: "...",
  type: "PDF",
  language: "en",
  pageCount: 123,
  vault: "...",
  source: "...",
  sourceLocations: ["..."],
  queryTags: ["steam engines"],
  level: "SEARCH | DISCOVERED | ARCHIVED",
  discoveredBy: "guest_042",
  discoveredAt: 0,
  fetchedAt: 0,
  lastAccessedAt: 0,
  archive: null
}
```

### alexandriaQueries

TTL cache mapping a normalized query/filter set to document IDs. Search metadata remains small and can be refreshed without modifying entity memory.

### knowledgeEdges

Persistent links from a park entity or park research root to a LoA document.

```js
{
  id: "ke:<entityId>:<sourceId>",
  entityId: "guest_042",
  entityUuid: "...",
  entityType: "guest",
  documentId: "alexandria:<sourceId>",
  sourceId: "<sourceId>",
  title: "...",
  level: "DISCOVERED",
  reason: "frontieros-research",
  query: "history of roller coasters",
  learnedAt: 0
}
```

## Three persistence levels

- **SEARCH** — metadata/snippet appeared in a search result. Cached but not treated as something an entity knows.
- **DISCOVERED** — a guest, worker, wildlife entity, world object, or the park research root deliberately learned/used the record. A `knowledgeEdges` row is written.
- **ARCHIVED** — the player deliberately fetches the complete document through the local bridge. Text documents are stored as text; binary documents are stored as base64, subject to the configurable archive-size limit.

## Ollama grounding

`KnowledgeBroker.ask(entityId, question)` retrieves:

1. live/cached LoA results,
2. the local 10,000-topic Alexandria fallback,
3. relevant Codex records,
4. target-entity state and already learned knowledge.

Only that retrieved context is handed to Ollama. The broker asks the model to state uncertainty and reference LoA source IDs rather than inventing unsupported material.

The top LoA records actually used in an answer are promoted to `DISCOVERED` for the target entity.

## Game surfaces

- **Systems → Alexandria Neural Link** shows bridge health, cache levels and knowledge-edge counts.
- Select/right-click an entity before opening Alexandria to make it the active neural target.
- Search results can be **Discover**, **Archive**, or **Inspect Metadata**.
- **Retrieve + Ask** performs RAG-style retrieval before Ollama inference.
- **Guest FrontierOS → Alexandria** lets an individual guest search and deliberately learn a result.
- Guest first-person Ollama chat is automatically supplied with a small live/cached LoA retrieval set.
- Guest Flock tasks retrieve LoA context before inference.
- **Database Explorer** exposes `alexandriaDocuments`, `alexandriaQueries`, and `knowledgeEdges` as ordinary inspectable R3 stores.

## Offline behavior

LoA is optional. If `RCT_LOA_BASE` is unset or the archive is unreachable:

- boot does not block,
- simulation continues,
- IndexedDB cache remains searchable when a query was previously cached,
- local Alexandria and Codex remain available,
- Ollama can still answer from those local sources.

This is deliberately a graceful knowledge degradation, not a game-entry dependency.
