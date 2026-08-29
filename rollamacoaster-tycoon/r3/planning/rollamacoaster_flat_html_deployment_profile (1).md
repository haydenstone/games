# RollamacoasterTycoon!! Flat-HTML Deployment Profile

## Decision

The project SHALL ship a generated single-file browser artifact:

`rollamacoaster.html`

This does **not** change the source architecture. Development remains modular and testable. The flat HTML is a build/export target.

There are two supported runtime profiles.

---

# Profile A — Full Agentic Mode

```text
rollamacoaster.html
        │
        │ HTTP / WebSocket
        ▼
localhost RCT backend
        │
        ├── RAG database
        ├── vector/entity indexes
        ├── project memory
        ├── Flock orchestrator
        ├── Game API authority
        ├── audit/parity services
        ├── Ollama adapter
        ├── GPT broker adapter
        └── Gemini broker adapter
```

This is the primary mode.

The visible application remains one HTML file, but a local backend process provides the persistent agentic control plane.

Ollama is already an external localhost process in the recovered prototypes, so requiring a companion local RCT backend does not violate the project's local-first character.

### Benefits

- persistent Flock even if the game tab reloads
- real SQLite/vector storage
- secure GPT/Gemini key handling
- project filesystem tools
- validated Game API
- server-side RAG ingestion
- long-lived indexing
- transactional state changes
- durable audits and provenance
- WebSocket game/event stream
- provider switching without exposing secrets to browser code

---

# Profile B — Flat Standalone / Field Mode

`rollamacoaster.html` can also operate without the RCT backend.

In this mode the page owns a browser-local subset:

- Three.js game/simulation
- IndexedDB park saves
- IndexedDB guest brains
- IndexedDB conversations
- browser-local entity graph
- browser-local project memory
- compact lexical/entity retrieval
- embedded feature registry
- embedded lore/catalog
- direct Ollama connection when browser policy allows it
- JSON import/export
- save/open
- core Flock chat/inspect functionality
- all normal gameplay

Unavailable or reduced when the backend is absent:

- secure GPT/Gemini broker credentials
- persistent server-side vector database
- autonomous Flock continuation after the page closes
- privileged project filesystem mutation
- server-side source indexing
- background jobs
- durable server event ledger
- cross-client synchronization

The UI must visibly indicate:

`AGENT BACKEND: CONNECTED`

or

`STANDALONE MODE`

No gameplay save should become invalid merely because the backend is unavailable.

---

# Build philosophy

## Source tree

Development source stays modular:

```text
apps/
backend/
packages/
services/
data/
assets/
tests/
```

## Release compiler

A packaging step produces:

```text
dist/
  rollamacoaster.html
```

The packer:

1. bundles client JavaScript
2. bundles CSS
3. embeds Three.js/runtime dependencies
4. embeds small textures/icons as data URLs or generated geometry
5. compresses large JSON/lore/feature registries
6. writes bootstrap code
7. includes backend-discovery logic
8. includes standalone fallback services
9. generates a content/version manifest
10. validates that no external client asset is accidentally required

The result remains inspectable HTML, not an opaque Electron application.

---

# Boot sequence

```text
OPEN rollamacoaster.html
        │
        ▼
client boot state machine
        │
        ├── probe http://127.0.0.1:<rct-port>/api/health
        │
        ├── if connected:
        │      FULL AGENTIC MODE
        │      connect event stream
        │      request project/game snapshot
        │      attach Flock
        │
        └── if unavailable:
               STANDALONE MODE
               open IndexedDB
               construct local simulation
               optionally probe Ollama directly
```

Backend loss during play must degrade gracefully. It must not freeze camera/input or corrupt state.

---

# One client contract, two transports

The browser client does not maintain two completely different game implementations.

Use an abstraction:

```ts
interface RctControlPlane {
  query<T>(name: string, args?: unknown): Promise<T>;
  command<T>(name: string, args?: unknown): Promise<T>;
  subscribe(handler: (event: DomainEvent) => void): Unsubscribe;
}
```

Implementations:

- `RemoteControlPlane` → localhost backend
- `BrowserControlPlane` → local standalone services

The UI, renderer and game panels call this interface.

That prevents full-agentic mode and standalone mode from drifting apart.

---

# Flat HTML and RAG

A full vector/RAG stack should remain server-first, but the flat file contains a lightweight fallback index.

Embedded browser retrieval can include:

- feature registry lookup
- revision lookup
- symbol/name lookup
- entity graph expansion
- weighted lexical matching
- current guest/ride/stall context
- project memories stored in IndexedDB
- live park events

When connected, the same `rag.search` call is routed to the server hybrid index.

When disconnected, it falls back to browser retrieval.

Therefore Flock does not need separate prompting logic.

---

# Flat HTML and Ollama

The supplied Flock prototype already directly probes:

`http://127.0.0.1:11434/api/tags`

and sends chat requests to:

`http://127.0.0.1:11434/api/chat`

The final HTML preserves that as the **direct local fallback**.

Primary full-agentic routing is:

```text
HTML -> RCT backend -> Ollama
```

Fallback is:

```text
HTML -> Ollama
```

This keeps the flat artifact useful even when only Ollama is running.

Browser origin/CORS behavior varies by launch method and environment, so the release should also support serving the exact same single HTML file from the local backend:

`http://127.0.0.1:<rct-port>/`

No multi-file web deployment is required.

---

# Flat HTML and GPT / Gemini

GPT/Gemini broker calls should normally be:

```text
HTML -> backend broker API -> provider
```

Do not bake provider API keys into the HTML.

A purely browser-direct external-provider mode may exist as an explicit developer experiment, but it is not the secure default and should never persist the credential in the project or game save.

---

# Asset packaging

To remain genuinely flat:

### Inline/generated
- CSS
- application JS
- UI icons
- catalog metadata
- feature registry
- procedural geometry
- small SVGs
- shader strings

### Embedded/compressed
- lore databases
- default scenario data
- small textures
- migration maps

### Optional runtime cache
Large future media/model assets may be fetched/imported once and stored in Cache Storage or IndexedDB while the launcher itself remains one HTML file.

For the current procedural Three.js visual style, a fully self-contained HTML remains practical.

---

# Scenery / ride implications

The flat target must not force visual simplification.

Scenery, stalls and guest models remain protected assets.

Rebuilt stock rides can still contain:

- larger human-scale geometry
- explicit seats
- restraints
- boarding platforms
- animation anchors
- support structures
- multiple material regions
- richer procedural shapes

All of that can be generated from code inside the flat HTML bundle.

The custom coaster/path engineering systems are especially compatible with this strategy because their geometry is procedural.

---

# Persistence hierarchy

Full mode:

```text
backend authoritative durable DB
        +
browser cache/renderer state
```

Standalone:

```text
IndexedDB authoritative browser DB
```

Switching from standalone to backend mode should offer an explicit synchronization/import operation, never silently overwrite either side.

---

# Release acceptance tests

A release is not "flat" until:

- `dist/rollamacoaster.html` is the only required client file
- no client JS/CSS file is required next to it
- core game boots without network internet
- full gameplay works with backend disconnected
- saves work in standalone IndexedDB mode
- backend connection can be established after boot
- Flock can switch from browser fallback to backend service
- direct local Ollama fallback works in supported launch mode
- full backend Ollama mode works
- optional GPT broker works through backend
- optional Gemini broker works through backend
- no provider key appears in HTML, save, export or RAG corpus
- reconnecting the backend does not reset the park
- losing backend connection does not lock camera/input
- one HTML release can be served directly by the backend without modification

---

# Final product concept

The target is intentionally unusual:

**one HTML file on the surface, a serious local agentic operating system underneath.**

A user can carry `rollamacoaster.html` around as the visible game artifact.

If the RCT backend + Ollama are present, it wakes up into the complete agentic/RAG simulation platform.

If they are absent, it still opens as a playable, persistent standalone park rather than becoming a dead launcher.
