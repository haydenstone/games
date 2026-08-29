# RollamacoasterTycoon!! Reverse-Engineering Master Plan

## Executive conclusion
The R233M lineage should be treated as a behavioral specification and archaeological reference, not as the code foundation. Revision 3 has the correct clean-core direction, but it intentionally omitted specialized late experiments. The rebuild should therefore preserve R3 kernel contracts while importing legacy behavior through bounded domain modules and a parity harness.

Automated static extraction recovered **11,923 feature/implementation/design atoms** from the legacy file. This number intentionally includes user-facing behaviors, UI contracts, data keys, event hooks, diagnostics, functions and implementation symbols. It is not a claim that the game has 11,923 independent menu-visible features.

### Recovery totals
- **Legacy build catalog:** 140 items
- **R3 build catalog:** 54 items
- **Legacy catalog keys without an exact R3 key match:** 106 (semantic alias review still required)
- **revision_meta_description:** 201
- **revision_requirement:** 609
- **build_catalog_item:** 140
- **build_meta_description:** 75
- **audit_contract:** 221
- **function:** 1,345
- **arrow_function:** 63
- **dom_id:** 900
- **css_class:** 213
- **runtime_userdata_key:** 298
- **dataset_contract:** 125
- **persistence_key:** 13
- **event_binding:** 363
- **ui_tooltip:** 72
- **ui_placeholder:** 43
- **ui_button_label:** 484
- **external_endpoint:** 28
- **implementation_symbol:** 6,724

## Non-negotiable rebuild principles
- **Feature registry before implementation.** Every legacy atom receives a stable registry ID, owner domain, parity status, evidence line and test status.
- **Plain state, runtime views.** No Three.js objects, DOM nodes, audio elements, controls, renderers, curves or transient camera state may enter saves.
- **One authority per concept.** One economy ledger, one entity registry, one ride readiness calculation, one queue owner, one input router, one window manager, one simulation clock.
- **No monkey-patch architecture.** Later features register with domain interfaces/events. They do not replace global functions after boot.
- **Queue and rider ownership are mutually exclusive.** Waiting avatar and rider proxy are different states with explicit boarding/unboarding transitions.
- **Navigation is data, visuals are projections.** Paths/queues/bridges generate a graph; rails, ribbons and guides are derived render layers.
- **Every write is schema-validated.** Saves, brains, conversations, Flock files, Alexandria records and migration payloads are versioned.
- **Performance optimizations cannot silently change semantics.** LOD/batching may change rendering cost, never entity existence, routing, queue state, inventories or economy.
- **Legacy audits become release tests.** The 221 recovered audit hooks are ported into deterministic assertions or scenario checks.
- **No deletion by cleanup.** A legacy item can be marked superseded or intentionally retired only by an explicit parity decision, never because the new architecture lacks a place for it.

## Target architecture
Each domain owns state transitions and exposes commands/events. The renderer subscribes to state and keeps runtime objects in maps keyed by stable IDs.

### KERNEL · Kernel / Boot / Time / Event Bus
**Depends on:** none

One boot state machine, simulation clock, event bus, deterministic RNG, lifecycle and error boundary.

### DATA · Canonical Data Contracts
**Depends on:** KERNEL

Plain serializable park state, stable IDs, schemas, migrations, runtime-reference firewall.

### UI · Desktop UI / Windowing / Input Router
**Depends on:** KERNEL, DATA

One command router, one draggable/z-order manager, keyboard priority, hover/inspect contracts, title/HUD/status/pulse.

### WORLD · World / Terrain / Spatial Index / Camera
**Depends on:** KERNEL, DATA, UI

Three.js runtime maps, raycasting, terrain, land, camera modes, entity picking and LOD boundaries.

### BUILD · Build Database / Placement / Demolition
**Depends on:** WORLD, DATA, UI

Authoritative catalog, ghosts, rotation, freeplace/grid modes, bulldoze/refunds, research visibility.

### PATH · Paths / Queues / Navigation Graph
**Depends on:** BUILD, WORLD

2m cells plus freeplace engineering, welded path topology, queue-only semantics, snake geometry, bridges/elevated paths.

### ECON · Economy / Inventory / R&D
**Depends on:** DATA, BUILD

Single ledger, wallets, prices, COGS, wages, park value, research tree and funding.

### GUEST · Guest Entity / Brain / Needs / Social
**Depends on:** PATH, ECON

Needs, routing, thoughts, wellbeing, inventory visuals, seating, identities, relationships and persistent brains.

### STAFF · Staff / Duties / Operations
**Depends on:** PATH, ECON

Handymen, security, entertainers/mechanics where present, duty toggles, placement, fire/follow/inspect and service jobs.

### RIDE · Attractions / Access / Queue / Boarding
**Depends on:** PATH, GUEST, ECON

Ride registry, access drop zones, readiness authority, FIFO queues, rider proxies, seat ownership, operation and managers.

### ENGINEERING · Custom Coaster / Route Ride / Path Engineering
**Depends on:** RIDE, BUILD, PATH

Custom coaster points/validation/skins/stations, tram/train/monorail/log routes, custom elevated path engineer.

### RETAIL · Shops / Services / Facilities
**Depends on:** GUEST, ECON, BUILD

Stocked products, consumption, ATM, restrooms, care/security/clinic/water/charging and service routing.

### ENV · Scenery / Water / Wildlife / Lighting / Audio
**Depends on:** WORLD, BUILD, GUEST

HD scenery constructors, trees/grass/water, animals, programmable lights, ambience, speakers and Main PA.

### ALEX · Alexandria / Geocache Knowledge DB
**Depends on:** DATA, GUEST, BUILD

10k deterministic index, relational topic records, caches, portable/tradable files/cards, guest learning.

### PHONE · FrontierOS / Wi-Fi / Messaging
**Depends on:** GUEST, ALEX, ENV

Guest and manager phones, SSIDs/APs, maps, messages, research/social apps, Park AI.

### FLOCK · Guest Flock / IDE / Ollama Brokers
**Depends on:** GUEST, ALEX, DATA, UI

Persistent conversations/projects/files, role agents, CHAT/BUILD, code/preview, context linking, Ollama/GPT broker.

### PERF · Performance / Diagnostics / Compatibility
**Depends on:** WORLD, GUEST, RIDE, ENV, FLOCK

Benchmarks, budgets, batching/LOD, audits, browser guards and feature-preserving performance policy.

### SAVE · Save / Migration / Legacy Import
**Depends on:** DATA, WORLD, GUEST, RIDE, FLOCK

IndexedDB snapshots, project saves, JSON interchange, R138 migration, legacy normalization, reconstruction-only load.

### PARITY · Parity Harness / Golden Playtests
**Depends on:** SAVE, PERF

Port 221 audit hooks, behavioral scenarios, screenshots, save round-trips and no-feature-loss release gates.

## Canonical state split
```text
ParkSnapshot (serializable)
  schema / metadata / simulation clock
  economy + ledger references
  entities[] / paths[] / rides[] / services[]
  guests[] / staff[]
  research / settings
  alexandria refs / phone network refs
  flock project refs

RuntimeWorld (never serialized)
  scene / renderer / cameras / controls
  meshesByEntityId / lights / audio nodes
  nav caches / raycast acceleration / LOD batches
  hover targets / placement ghosts / open windows
```

## Feature parity workflow
1. Ingest `rollamacoaster_feature_atoms.jsonl`. Normalize duplicates into human-scale capabilities while retaining every source atom as evidence.
2. Assign each capability to one target domain and mark `legacy_only`, `r3_present`, `porting`, `parity_pass`, or `intentional_retirement`.
3. For each legacy `*AuditR...` hook, implement an R3 test adapter before porting the feature. The test should fail first.
4. Port data model and commands before visuals. Then add visuals as projections of authoritative state.
5. Run save/load round-trip after every domain milestone. A loaded park must reconstruct a fresh runtime and return to active neutral camera state.
6. Run scenario packs: empty park, 300 guests, 2,000 guests, queues, transports, custom coaster, shops, geocaches, phones, media, Flock, and legacy save import.
7. Do not declare a phase complete until its registry rows have no unexplained `missing` status.

## Build roadmap
### Phase 0 · Freeze the fossil
Hash the legacy and R3 inputs; generate manifest/registry; capture catalog, revision notes, audits, UI labels, storage keys and endpoint contracts. No gameplay coding until this is reproducible.

### Phase 1 · Clean kernel
Finalize KERNEL + DATA + UI. Boot state machine, event bus, clock, deterministic IDs/RNG, error boundary, input priority, draggable/z-order window manager, plain-state schemas.

### Phase 2 · World substrate
WORLD + BUILD. Terrain, land, starter park, raycast inspect, placement ghosts, rotation, demolition, authoritative build catalog. Port every catalog item as data even if its constructor is temporarily stubbed.

### Phase 3 · Paths are the nervous system
PATH. 2m grid and freeplace modes, cardinal/welded topology, queue-only nodes, snake detection, bridges, custom elevated path engineer, graph rebuild and path audits.

### Phase 4 · Money cannot fork
ECON. Single transaction API for construction/refunds/admission/rides/retail/COGS/wages/maintenance/R&D. Port park value and finance audits before advanced guest logic.

### Phase 5 · Living guests and workers
GUEST + STAFF. Identities, needs, wallets, thoughts, wellbeing, inventory visuals, seating, duties, placement/firing/follow/inspect. Persist brains separately from world entities.

### Phase 6 · Ride authority
RIDE. Ride registry, open/close/readiness, standard entrance/exit drop zones, queue demand, FIFO slots, board/unboard state machine, Ferris upright cabins and seat proxies, manager/hover telemetry.

### Phase 7 · Commerce and facilities
RETAIL. Every food/shop/service product, stock, consumption, ATM, restrooms, Family Care, First Aid/Clinic, Security, water, charging, bins and operational routing.

### Phase 8 · Engineering attractions
ENGINEERING. Custom coaster builder/validation/commissioning/skins, transport route builders/stations, log flume route mode, custom bridges/paths, access overlays.

### Phase 9 · Park atmosphere
ENV. All scenery constructors, trees/flowers/grass, water animation, wildlife autonomy, lighting programs, Wave Beacon soft sine default, speakers/Main PA/Jamendo/Radio/Synthwave, ambience.

### Phase 10 · Alexandria
ALEX. 10,000-topic deterministic database, relational detail/search, geocache placement/routing/read/trade/file inventory, guest learning and peer-context integration.

### Phase 11 · FrontierOS
PHONE. Guest + manager phones, paper map, geocache client, messages, Wi-Fi multi-SSID/MU-MIMO/beamforming, apps and Park AI.

### Phase 12 · Flock IDE
FLOCK. Persistent chats/projects/files, Codex/Unsloth command strip, explorer/search/conversation drawers, editor tabs/dirty state, code/preview, role agents, Ollama discovery/chat, optional GPT broker.

### Phase 13 · Performance without amnesia
PERF. Port benchmark suite, adaptive budgets, batching/LOD and distance options. Verify each optimization against semantic audits so proxies never change simulation truth.

### Phase 14 · Save and migration hardening
SAVE. IndexedDB schemas, project saves, Save As/Open/Delete, export/import, R138 detection, FULL_SIMULATION_SNAPSHOT normalization, version migrations, no runtime refs.

### Phase 15 · Parity burn-down
PARITY. Convert all 221 audit hooks, replay revision feature scenarios, compare legacy/R3 behavior, close every unexplained registry gap. Only then call the structured build feature-complete.

## Highest-risk seams to eliminate
- Classic-script ↔ ES-module scope fractures. R233M itself ends with a root fix because later scripts could not access authoritative module scope.
- Camera/input ownership after load or modal close. Transient interaction state must never be serialized.
- Multiple queue/rider render owners. Boarding must atomically transfer ownership.
- Repeated function replacement across revisions. Replace with registered handlers and event subscriptions.
- Economy side effects scattered across shops/rides/inventory. All money movement must go through one ledger transaction API.
- DOM as state. Panels should render from stores; hiding/showing a node must not determine simulation truth.
- Performance code that alters entity semantics. Rendering LOD must be orthogonal to simulation LOD.
- Browser-origin persistence assumptions. IndexedDB migrations need explicit versioning and portable export paths.
- External media/network failures. Jamendo/Radio/Ollama/GPT integrations require capability detection, timeouts and local fallbacks.

## Design language to preserve
- **Park shell:** dark forest/charcoal glass UI, thin green-gray borders, compact monospace telemetry, gold/cyan/green status accents, dense draggable utility windows.
- **Build language:** icon + name + lore + price, category/subcategory organization, search, placement ghost, rotation, clear build-mode footer.
- **World feedback:** hover telemetry, entity inspectors, bottom contextual status dock, Park Pulse feed/announcements, world-space entrance/exit markers.
- **Flock language:** darker neutral IDE surface distinct from park glass, compact command strip, on-demand drawers, editor/preview split, explicit model/run/stage state.
- **Meta/lore:** item descriptions are gameplay-facing documentation, not decoration. Preserve catalog lore, technical codes, research descriptions and revision-intent notes in data files.

## Suggested structured repository
```text
rollamacoaster/
  app/
    kernel/          boot, clock, events, commands, errors
    data/            schemas, migrations, ids, repositories
    world/           terrain, spatial, render adapters, cameras
    build/           catalog, placement, demolition
    navigation/      paths, queues, graph, bridges
    economy/         ledger, pricing, inventory, research
    guests/          entities, brains, needs, routing, social
    staff/           roles, duties, operations
    rides/           registry, access, queues, boarding, vehicles
    engineering/     coaster/path/route builders
    retail/          shops, products, services
    environment/     scenery, wildlife, water, lighting, media
    alexandria/      knowledge DB, geocaches
    frontieros/      phones, wifi, messaging, apps
    flock/           projects, conversations, agents, brokers
    ui/              windows, panels, inspectors, pulse, HUD
    persistence/     IndexedDB, saves, import/export
    diagnostics/     audits, benchmarks, parity harness
  content/
    build-catalog.json
    research-tree.json
    lore.json
    feature-registry.jsonl
  tests/
    audits/
    scenarios/
    migrations/
    golden/
```

## Concrete first implementation slice
The first shippable slice should be intentionally narrow but architecturally complete: title → new/open park → orbit/interact → build path → build one shop/service/ride → spawn guest → guest routes and spends → queue/board ride → save → reload → same authoritative state reconstructed. Every later feature plugs into those contracts rather than modifying them.

## Generated companion files
- `rollamacoaster_reverse_engineering_manifest.json` — structured summaries, catalogs, design tokens, counts and domain roadmap.
- `rollamacoaster_feature_atoms.jsonl` — exhaustive static recovery ledger with source lines and inferred domains.
- `rollamacoaster_revision_meta.md` — chronological revision-intent descriptions recovered from the legacy file.