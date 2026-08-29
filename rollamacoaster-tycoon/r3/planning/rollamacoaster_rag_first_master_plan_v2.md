# RollamacoasterTycoon!! RAG-First Agentic Backend Master Plan v2

## Architectural override

This v2 document supersedes the ordering assumptions in the earlier reverse-engineering plan.

**Primary product order:**

1. **Database / indexed project knowledge**
2. **RAG retrieval and entity graph**
3. **Flock agent runtime**
4. **Provider / knowledge-broker adapters**
5. **Validated project and Game API tool layer**
6. **Authoritative simulation services**
7. **3D game client**

RollamacoasterTycoon!! is therefore **not a game with an Ollama feature bolted into it**. It is a local-first agentic/RAG platform whose richest client is the theme-park simulation.

The browser/game must be able to close, reload, reconnect, or be replaced without destroying the authoritative project knowledge, memories, entity graph, Flock runs, simulation state, or audit history.

---

## 1. Backend-first mental model

```text
                         ┌────────────────────────────┐
                         │ Operator / Game UI / IDE   │
                         └──────────────┬─────────────┘
                                        │
                           HTTP + WebSocket/EventStream
                                        │
┌───────────────────────────────────────▼──────────────────────────────────────┐
│                    RCT AGENTIC BACKEND / CONTROL PLANE                      │
│                                                                              │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐   │
│  │ Flock       │  │ RAG / Search │  │ Entity Graph │  │ Project Memory  │   │
│  │ Orchestrator│  │ + Embeddings │  │ + Relations  │  │ + Lessons       │   │
│  └──────┬──────┘  └──────┬───────┘  └──────┬───────┘  └────────┬────────┘   │
│         │                │                 │                   │             │
│         └────────────────┴─────────────────┴───────────────────┘             │
│                                  │                                           │
│                         Context / Retrieval Bus                              │
│                                  │                                           │
│  ┌───────────────────────────────▼───────────────────────────────────────┐   │
│  │ Provider Router / Knowledge Brokers                                  │   │
│  │ Ollama default · OpenAI/GPT optional · Gemini optional · future      │   │
│  └───────────────────────────────┬───────────────────────────────────────┘   │
│                                  │                                           │
│  ┌───────────────────────────────▼───────────────────────────────────────┐   │
│  │ Tool + Policy + Validation Gateway                                   │   │
│  │ project.* · rag.* · game.* · save.* · audit.* · broker.*            │   │
│  └───────────────────────────────┬───────────────────────────────────────┘   │
│                                  │                                           │
│  ┌───────────────────────────────▼───────────────────────────────────────┐   │
│  │ Authoritative Simulation Services                                    │   │
│  │ park · entities · guests · staff · paths · rides · retail · economy │   │
│  │ research · wildlife · lighting · audio · Alexandria · FrontierOS     │   │
│  └───────────────────────────────┬───────────────────────────────────────┘   │
│                                  │                                           │
│  ┌───────────────────────────────▼───────────────────────────────────────┐   │
│  │ Durable Stores                                                       │   │
│  │ SQL/SQLite + vector index + event ledger + project files + snapshots │   │
│  └───────────────────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────────────────┘
                                        │
                             state/events/render DTOs
                                        │
                         ┌──────────────▼──────────────┐
                         │ Three.js Game Client       │
                         │ view + input + animation   │
                         └─────────────────────────────┘
```

The **game client is a projection**. It never becomes the only owner of important state.

---

## 2. Flock is a backend subsystem, not a panel

The legacy Guest Flock UI is retained as an in-game/admin console, but the actual Flock runtime moves to backend services.

### Flock backend responsibilities

- Own run IDs, stages, agents, turns, abort/cancel state and run history.
- Discover and route models.
- Build RAG context.
- Read/write project files through validated tools.
- Query and operate the game exclusively through the Game API.
- Maintain project memory and lessons.
- Maintain entity graph and relationship memory.
- Maintain knowledge/discovery records.
- Run build/review/validation loops.
- Run parity audits.
- Coordinate migrations.
- Generate structured change plans.
- Submit mutations as commands, never mutate renderer objects.
- Observe resulting domain events and verify that requested effects actually happened.
- Keep provenance for every retrieved chunk, tool call, state change and generated artifact.

### Flock roles

The recovered Scout / Shepherd / Planner / Builder / Reviewer / Archivist/Writer concepts survive as **agent roles**, not hard-wired guest render objects.

A live park guest can still be assigned as the narrative persona/identity for a role, but backend orchestration is not dependent on whether that guest's mesh is currently rendered.

Suggested roles:

- **Scout**: retrieval, state inspection, dependency discovery.
- **Shepherd**: intent alignment, task shaping, regression awareness.
- **Planner**: structured plan, API/tool sequence, acceptance criteria.
- **Builder**: code/project changes and permitted game commands.
- **Reviewer**: parity, scale, save, economy, routing and regression checks.
- **Archivist**: durable memory, changelog, provenance and feature registry updates.
- **Simulation Analyst**: live game telemetry and anomaly triage.
- **Art/Ride QA**: guest-scale, seat, boarding, camera and animation fit checks.

---

## 3. RAG database is the first implementation milestone

The former prototype's large "read lots of project text into the prompt" approach becomes a real ingestion/indexing pipeline.

### Data classes to index

1. **Source code**
   - HTML/CSS/JS/TS/Python/config
   - function/symbol index
   - imports/dependencies
   - DOM IDs/classes
   - API contracts
   - revision markers

2. **Feature archaeology**
   - all recovered feature atoms
   - revision metadata
   - audit hooks
   - catalog entries
   - design descriptions
   - known bugs and fixes
   - parity status

3. **Game data**
   - catalog
   - ride definitions
   - seat/boarding definitions
   - guest/staff archetypes
   - inventories/products
   - research
   - scenery
   - lore

4. **Live simulation knowledge**
   - entities
   - current states
   - notable events
   - transactions
   - incidents
   - route failures
   - ride faults
   - performance samples

5. **Project memory**
   - decisions
   - lessons
   - accepted conventions
   - migrations
   - validation outcomes

6. **Conversations / Flock runs**
   - operator requests
   - selected retrieved context
   - agent responses
   - tool calls
   - acceptance checks
   - final result

7. **Alexandria / Codex knowledge**
   - isolated corpus namespace
   - metadata and provenance preserved
   - searchable through the same retrieval service without mixing it blindly into engineering context

### Retrieval model

Use hybrid retrieval:

- lexical/BM25-style term matching
- vector similarity
- entity graph expansion
- dependency-edge expansion
- recency
- project/revision filters
- domain filters
- exact symbol/path lookup
- live-game relevance

Every retrieval result must include provenance.

---

## 4. Durable storage layout

Recommended local-first layout:

```text
data/
  rct.sqlite
  vectors/
  snapshots/
  events/
  imports/
  broker-secrets/       # server protected, never exported
projects/
  rollamacoaster/
    src/
    data/
    tests/
    assets/
```

Suggested logical tables/collections:

- `projects`
- `documents`
- `chunks`
- `embeddings`
- `entities`
- `entity_links`
- `memories`
- `conversations`
- `messages`
- `flock_runs`
- `flock_turns`
- `tool_calls`
- `audit_results`
- `feature_registry`
- `feature_evidence`
- `catalog_items`
- `park_snapshots`
- `park_entities`
- `guest_brains`
- `ledger_entries`
- `simulation_events`
- `provider_profiles`

The simulation may keep hot state in memory for speed, but durable truth is reconstructed from validated snapshots/events rather than renderer state.

---

## 5. Provider architecture: Ollama first, brokers optional

### Default behavior

**Ollama is the default worker provider.**

The backend detects local Ollama models and can assign different local models to roles.

### Broker contract

All external providers implement one backend interface:

```ts
interface KnowledgeBroker {
  id: "ollama" | "openai" | "gemini" | string;
  health(): Promise<ProviderHealth>;
  listModels(): Promise<ModelInfo[]>;
  complete(req: BrokerRequest): Promise<BrokerResponse>;
  review?(req: ReviewRequest): Promise<ReviewResponse>;
  embed?(req: EmbeddingRequest): Promise<EmbeddingResponse>;
  abort(runId: string): Promise<void>;
}
```

Provider-specific HTTP formats stay behind adapters. Flock only sees normalized requests/responses.

### Required modes

- **Local only**
  - Ollama performs all worker roles.
- **GPT knowledge broker**
  - preserve the recovered R231E behavior.
- **Gemini knowledge broker**
  - same normalized role as GPT, implemented as a provider adapter.
- **External worker**
  - optional future mode where a stage may be assigned directly to GPT/Gemini.
- **Mixed routing**
  - per-role/per-stage provider policies.

### Preserve recovered GPT broker semantics

The structured rebuild must preserve these behaviors from the late revision:

- broker OFF by default
- once-per-run broker cadence
- per-stage refresh cadence
- recursive review cadence:
  `Ollama agent draft -> broker critique -> same Ollama role correction -> next role`
- local workflow continues when optional broker fails
- broker emits:
  - conversation direction
  - knowledge brief
  - per-role directives
  - acceptance checks
  - risks
- direct or local-relay connection modes
- no API secrets in project files, saves, exports, transcripts, diagnostics or RAG corpora

### Secret policy

Because the new Flock is backend-first, preferred configuration is:

```text
browser/game -> localhost backend -> provider
```

The browser should not need provider keys.

Secrets live in process memory, OS keychain, environment variables, or a protected server-side secret store. They are excluded from:

- saves
- project export
- telemetry
- RAG indexing
- logs
- crash reports
- Flock transcripts

---

## 6. Game API: the only mutation boundary

The Flock does **not** directly edit Three.js objects, browser globals, or arbitrary in-memory simulation structures.

The human UI and the agents call the same command/query API.

### Query examples

```text
GET /api/game/state/summary
GET /api/game/entities
GET /api/game/entities/{id}
GET /api/game/guests/{id}
GET /api/game/staff/{id}
GET /api/game/rides/{id}
GET /api/game/stalls/{id}
GET /api/game/economy
GET /api/game/paths/graph
GET /api/game/incidents
GET /api/game/audits
```

### Command examples

```text
POST /api/game/commands/build
POST /api/game/commands/demolish
POST /api/game/commands/ride/configure
POST /api/game/commands/ride/open
POST /api/game/commands/ride/close
POST /api/game/commands/stall/configure
POST /api/game/commands/staff/hire
POST /api/game/commands/staff/fire
POST /api/game/commands/staff/assign
POST /api/game/commands/guest/route
POST /api/game/commands/economy/set-price
POST /api/game/commands/research/start
POST /api/game/commands/save
POST /api/game/commands/load
```

Each command:

1. authenticates local capability
2. validates schema
3. checks preconditions
4. executes through the domain service
5. writes event/ledger records
6. returns changed entity IDs
7. emits events
8. can be audited/replayed where appropriate

### Agent-specific tool facade

Flock receives semantic tools, for example:

- `game.search_entities`
- `game.inspect_entity`
- `game.inspect_area`
- `game.build`
- `game.demolish`
- `game.configure_ride`
- `game.configure_stall`
- `game.hire_staff`
- `game.fire_staff`
- `game.route_guest`
- `game.query_economy`
- `game.run_audit`
- `game.save`
- `game.load`
- `rag.search`
- `rag.lookup_symbol`
- `rag.lookup_feature`
- `project.read_file`
- `project.search`
- `project.propose_write`
- `project.apply_write`
- `project.validate`

There is no `eval()` or "write arbitrary game memory" tool.

---

## 7. Event stream from game to Flock

The game publishes structured domain events to the backend event bus:

```text
guest.spawned
guest.need_critical
guest.purchase
guest.thought_changed
guest.routed
guest.stuck

ride.built
ride.opened
ride.closed
ride.queue_changed
ride.boarded
ride.unboarded
ride.breakdown
ride.scale_audit_failed

stall.opened
stall.closed
stall.stock_changed
stall.sale

staff.hired
staff.fired
staff.task_started
staff.task_completed

economy.transaction
research.completed
park.opened
park.closed
save.created
save.loaded
audit.failed
```

Flock may subscribe for diagnostics and learning, but normal frame-by-frame animation never becomes LLM traffic.

---

## 8. Agent autonomy boundaries

Three levels:

### Observe
Read-only queries, RAG, audits, recommendations.

### Operate
Normal player-equivalent actions via validated Game API commands.

### Develop
Project/source modifications through project tools, validation and explicit artifact/version records.

Provider selection does not alter these permissions.

A GPT or Gemini broker cannot bypass permissions that an Ollama worker would have.

---

## 9. Asset preservation policy

The parity project now distinguishes **behavior preservation** from **geometry preservation**.

### Class A: preserve geometry/design unless broken

These are strong reference assets:

- guest models and recognizable human proportions
- scenery
- landscaping language
- decorative water/lighting pieces
- stalls/shops
- service buildings
- custom coaster engineering
- custom elevated/path engineering
- custom/route ride work that already supports credible scale and interaction

For these, the new implementation should preserve silhouettes, proportions, material language, animations and recognizable design intent while moving behavior into clean systems.

### Class B: preserve feature, rebuild geometry

Many stock/non-custom rides fall here.

A ride's **feature identity** must survive:
- name/category
- economics
- research/unlock relationship
- queue behavior
- ride cycle
- capacity
- excitement/needs effects
- breakdown/operations
- lore
- UI controls

But its old geometry is not sacred if it:
- is underscaled relative to guests
- cannot contain seated riders
- has no plausible boarding path
- clips legs/heads/restraints
- positions riders outside cabins
- makes the attraction read as a toy next to human models
- cannot support entry/exit animation
- has visually implausible vehicle/cabin dimensions

### Class C: review and choose

Mixed-quality assets get side-by-side parity review.

---

## 10. Human-scale ride standard

Create one canonical `GuestRigReference`.

Suggested baseline for testing:
- standing guest reference: approximately 1.70–1.80 m
- animated skeleton envelope includes head, torso, arms and walking leg swing
- seated pose envelope is separately defined

Every ride must declare explicit anchors:

```ts
type RideSeat = {
  seatId: string;
  position: Vec3;
  rotation: Euler;
  pose: "sit" | "straddle" | "stand" | "vehicle";
  occupantEnvelope: Bounds;
  restraint?: RestraintSpec;
};

type RideAccess = {
  entrance: Transform;
  queueMerge: Transform;
  boarding: Transform[];
  exit: Transform;
  seats: RideSeat[];
};
```

### Mandatory visual QA

For every ride:

- adult guest standing beside ride screenshot
- adult guest seated in every unique seat type
- child/small guest fit if child-scale models exist
- queue-to-boarding transition
- boarding-to-seat transition
- full ride cycle with occupied seats
- unboarding transition
- camera close-up
- maximum vehicle articulation
- no head/leg clipping
- believable hand/rail/restraint relationship
- world-scale comparison with nearby stall, bench and path

### Scale gate

No stock ride is considered ported merely because its mesh exists.

**A ride reaches parity only when a guest can physically inhabit it convincingly.**

This is a release-test requirement.

---

## 11. Ride rebuild priorities

### Protect / port first
- custom roller coaster engineer
- custom elevated/path engineer
- route/transport engineering that already has meaningful vehicle scale
- Ferris wheel behavior with upright cabins and proper rider ownership
- best-performing custom attractions

### Rebuild early
Stock rides with tiny cabins/platforms or weak rider fit.

Rebuild around:
1. guest rig
2. boarding path
3. seat anchors
4. vehicle/cabin
5. ride mechanism
6. supports/platform
7. scenery/theme shell

Do **not** build a decorative ride mesh first and try to squeeze riders into it afterward.

---

## 12. Stalls and scenery doctrine

The strong stall/scenery work becomes part of the visual design bible.

Preserve:
- scale relationship to paths and guests
- distinctive silhouettes
- readable fronts/counters
- product identity
- signage
- small decorative details
- park-density feel
- foliage variety
- landscaping layers
- fountains/water
- lighting fixtures
- benches/tables/bins
- whimsical/futuristic special scenery

Their backend data contracts still become structured and authoritative.

A stall is:
- simulation entity
- inventory endpoint
- economy endpoint
- staffing/service endpoint when relevant
- 3D projection
- RAG-addressable entity
- Flock-operable API resource

---

## 13. RAG-aware game entities

Every important game entity receives a stable URI-like identity:

```text
rct://park/{parkId}
rct://guest/{guestId}
rct://staff/{staffId}
rct://ride/{rideId}
rct://stall/{stallId}
rct://path/{pathId}
rct://research/{researchId}
rct://feature/{featureRegistryId}
rct://file/{projectRelativePath}
```

This lets retrieval connect:
- source definition
- revision history
- current simulation instance
- audit history
- memories
- incidents
- associated UI
- economic transactions

Example question supported naturally:

> Why are guests avoiding Ferris Wheel 3 after I loaded this save?

RAG can retrieve the ride definition, current instance, queue graph, recent guest thoughts, scale/access audits, saved migration history and relevant legacy fixes before the agent answers or acts.

---

## 14. Revised repository structure

```text
rollamacoaster/
  apps/
    game-web/
    flock-studio/
    admin/
  backend/
    server/
    api/
    websocket/
    auth/
  packages/
    contracts/
    event-bus/
    game-tools/
    project-tools/
    validation/
  services/
    rag/
    embeddings/
    entity-graph/
    memory/
    flock/
    brokers/
      ollama/
      openai/
      gemini/
    simulation/
      park/
      world/
      build/
      path/
      economy/
      guest/
      staff/
      rides/
      engineering/
      retail/
      environment/
      alexandria/
      frontieron/
    persistence/
    parity/
  data/
    catalogs/
    lore/
    migrations/
    feature-registry/
  assets/
    guests/
    scenery/
    stalls/
    rides/
      preserved/
      rebuilt/
      custom/
  tests/
    contracts/
    simulation/
    parity/
    ride-scale/
    migration/
    broker/
```

---

## 15. Revised build roadmap

### Phase 0: fossil freeze and feature registry
- Preserve R233M, R3 and extraction artifacts.
- Assign registry IDs.
- Mark assets A preserve / B rebuild / C review.

### Phase 1: backend process and contracts
- Local backend server.
- versioned schemas.
- event bus.
- project identity.
- health API.
- WebSocket/event stream.

### Phase 2: database and RAG
- ingest source/project files
- ingest feature registry/revision meta
- chunk/index
- entity graph
- hybrid retrieval
- project memory
- provenance
- Codex/Alexandria namespace

### Phase 3: Flock runtime
- persistent runs and turns
- roles
- tool execution
- aborts
- validations
- retrieval context
- project memory loop
- artifact/version records

### Phase 4: provider router
- Ollama adapter and model discovery
- preserve GPT broker semantics
- OpenAI relay/direct compatibility where desired
- Gemini adapter
- per-stage routing
- run/stage/recursive review policies
- graceful fallback
- secret isolation

### Phase 5: Project API and developer tools
- project search/read
- propose/apply write
- deterministic validation
- diff/versioning
- parity registry updates

### Phase 6: authoritative Game API skeleton
- park state
- entities
- build catalog
- commands/queries
- event stream
- save snapshot contract

### Phase 7: world client
- Three.js projection
- camera
- input router
- inspect/follow
- placement ghost
- renderer runtime maps

### Phase 8: path/navigation/economy
- path graph
- queues
- routing
- ledger
- wallets
- retail transactions

### Phase 9: guests/staff
- preserve guest models
- needs
- thoughts
- inventories
- staff duties
- seating/resting
- animation ownership

### Phase 10: scenery/stalls preservation pass
- port the strongest scenery
- port stalls at preserved scale/detail
- rebuild simulation contracts underneath without flattening the art

### Phase 11: custom engineering systems
- custom coaster
- custom elevated path
- route rides/transports
- validation

### Phase 12: stock ride reconstruction
- evaluate every ride against GuestRigReference
- preserve good geometry
- rebuild underscaled rides
- explicit seats/access anchors
- rider animation
- ride-scale automated audits

### Phase 13: Alexandria / Frontier systems
- geocaches
- knowledge inventory
- advanced services
- FrontierOS/media/network systems selected by parity ledger

### Phase 14: performance
- LOD
- batching
- worker budgets
- profiler
- no semantic degradation

### Phase 15: save/migration
- R3 saves
- R233 lineage imports where practical
- R138 compatibility
- clean scene reconstruction

### Phase 16: parity burn-down
- port the 221 audits
- process every recovered feature atom
- no unexplained omissions

---

## 16. First vertical slice

The first meaningful executable slice is not "render a coaster."

It is:

1. backend starts
2. project is indexed
3. RAG can answer where a feature lives and why
4. Ollama model is discovered
5. Flock run starts
6. optional broker can enrich/review it
7. Flock calls `game.state.summary`
8. game simulation creates a park
9. browser connects
10. user builds a path and stall
11. same actions are available as Game API commands
12. guest spawns, routes, buys product
13. transaction appears in ledger
14. Flock can inspect the purchase through RAG/Game API
15. save snapshot is created
16. browser reloads
17. backend reconstructs authoritative state
18. renderer reconnects and rebuilds scene
19. parity audit passes

Only then do we scale the art/content surface.

---

## 17. Definition of done

The rebuild is complete only when:

- Flock can manage and reason over the project without depending on the game window.
- RAG can trace any major feature to source, revisions, live state and audit evidence.
- Ollama works completely offline/local.
- GPT broker compatibility is preserved.
- Gemini can be selected through the broker/provider abstraction.
- broker failure cannot take down local simulation or local Flock.
- API secrets never enter saves/RAG/exports.
- all game mutations pass through validated commands.
- scenery and stalls retain the strong visual identity of the legacy game.
- guest models remain recognizable and correctly animated.
- custom ride engineering is preserved.
- weak stock rides are rebuilt at believable human scale.
- every ride supports explicit rider seats/boarding/exit where applicable.
- the old feature registry reaches explicit preserve/rebuild/supersede decisions.
- save/load reconstructs fresh runtime state.
- no major feature depends on patching a global function from a later script.

---

# Original reverse-engineering plan retained below

The original plan is preserved as an archaeological/reference appendix. Where it conflicts with the RAG-first/backend-first ordering above, this v2 architectural override wins.



---

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