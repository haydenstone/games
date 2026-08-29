# RollamacoasterTycoon!! Revision 3

## Clean-core rebuild

This is a new single-file game architecture reconstructed from the intended behavior in the R233M lineage rather than another additive patch to the old HTML.

### Architecture

- One ES-module application entry point and one boot state machine.
- One input/router layer and one draggable-window manager.
- Plain-data authoritative park state. Three.js meshes, materials, rotors, controls, renderers, and other runtime references live only in runtime maps and are never saved.
- Stable entity/guest/staff IDs connect simulation systems.
- Event bus for economy, park pulse, entities, and system-level notifications.
- IndexedDB database `rollamacoaster-r3`, schema version 3.
- Stores: `saves`, `ledger`, `guestBrains`, `conversations`, `flockFiles`, `metadata`, `codex`, `alexandria`.
- localStorage is used only for tiny preferences/current IDs and R138 compatibility. A memory fallback is used when localStorage is denied.

### Gameplay rebuilt natively

- Fresh Three.js park world, orbit/interact modes, raycast hover/inspection, build placement, R rotation, Ctrl-click demolition.
- 2 m path/queue grid with queue-only tiles.
- Ride entrance and exit drop-zone markers.
- Queue waiting state and ride-seat state are separate.
- Ferris wheel cabins remain upright while the wheel rotates; riding guests attach to cabins rather than rotating the waiting line.
- Shops, services, rides, scenery, lighting, benches/tables, bins, Alexandria geocaches, staff, guest spawning and needs.
- Guest wallets, admissions, ride/shop revenue, construction costs, staff wages, maintenance, park value, and a single authoritative economy ledger.
- Guest needs and autonomous routing for hunger, thirst, bathroom, energy, nausea/stress recovery, low cash, rides, rest, and geocaches.
- Family Care, First Aid, Security Outpost, ATM, Wi-Fi AP, speakers, security cameras and staff room are real service catalog entities.
- Handyman, security and entertainer roles with role-specific duties.
- Wave Beacon defaults to a quiet sine modulation at 0.08 Hz.

### Brains, lore and Ollama

- Persistent guest brain records are stored separately from render/simulation objects.
- Ollama model discovery through `/api/tags` and chat through `/api/chat` at `http://127.0.0.1:11434` by default.
- Direct first-person guest chat uses current needs, wallet, interests, nearby park entities, memories and knowledge context.
- Guest Flock Studio has persistent conversations, a small project filesystem, CHAT/BUILD modes, code editor, preview, Topic of the Day and peer-learning rounds.
- Alexandria generates a deterministic 10,000-record technical knowledge index on disk.
- The supplied `codex(1).json` is malformed as one JSON document, so R3 bundles its exact original bytes gzip-compressed and salvages verse records line-by-line into independent IndexedDB rows. The bundle was verified byte-for-byte against the upload before release.

### Saves and migration

- New saves are plain Revision 3 snapshots in IndexedDB.
- Save, Save As, Open, Delete, JSON Export and JSON Import are included.
- Legacy `FULL_SIMULATION_SNAPSHOT` JSON can be imported and normalized.
- R138 browser save keys are detected and can be migrated when the browser exposes the same localStorage origin.
- A load always reconstructs the scene from plain records and returns the camera to a neutral active orbit state.

## Validation performed

- `node --check` on the complete generated module: PASS.
- TypeScript `checkJs`: no internal unresolved identifiers or semantic application errors. The only remaining diagnostics are missing type declarations for the two HTTPS Three.js CDN module imports.
- HTML structural check: PASS, 78 unique IDs and no duplicate IDs.
- IndexedDB store declaration check: PASS.
- Generator integrity checks for the former R3DB upgrade bug, runtime-follow leak, repeated entity-panel redraw, and O(n²) rebuild graph call: PASS.
- Embedded Codex gzip payload decompresses byte-for-byte to the uploaded file: PASS.
- Full Chromium navigation/playtest could not be executed in the artifact container because its browser is administrator-blocked from navigating to local/file test URLs. Do not interpret that environment limitation as a browser-playtest pass.

## Scope note

Revision 3 is a functional clean-core rebuild, not a line-for-line port of every experimental micro-feature that accumulated across more than 200 old revisions. The core systems that previously caused cross-patch failures are recomposed here first. Highly specialized late experiments such as every FrontierOS micro-app, every wildlife behavior, every custom coaster/path engineering mode, third-party media integrations, and every old inspector variant can now be added against the R3 contracts without mutating the boot, database, camera, save, queue or economy cores.

## Development playtest loop (R3.0-dev.2)
R3 now includes an in-game Development Test Bench and optional Python diagnostics collector. The canonical loop is RELEASE → TEST → COMMENTS → CORE DUMP → REVIEW → PLAN → BUILD → RELEASE. `rct_r3_release.py` rebuilds, validates, fingerprints, and stages a release. `rct_r3_dev_server.py` serves the exact standalone artifact and persists comments/core dumps/review packets to per-session folders. The emitted HTML remains independently runnable and falls back to browser downloads when the collector is absent.


## R3.0-dev.6 — construction lattice + park boundary
- Replaced the generic origin-centered Three.js GridHelper with a park-specific 2 m lattice.
- Grid lines now represent the actual edges of path cells; path centers snap to even world coordinates.
- Path decks are visually sized to the 2 m construction cell instead of floating across grid intersections.
- Path placement is rejected outside the fenced buildable park rectangle.
- Added immutable perimeter infrastructure: stone curb, dark iron rails and pickets, gold finials, masonry piers, and an integrated illuminated Forest Frontiers entrance.
- Added construction geometry and last-placement telemetry to development core dumps.


## R3.0-dev.7
- Replaced the camera-facing Forest Frontiers entrance Sprite with fixed PlaneGeometry labels mounted to both masonry sign faces.
- Expanded ordinary path decks from 1.82m to the authoritative 2.0m construction cell so adjacent pavement surfaces meet flush.
- Queue lanes remain intentionally narrow, but their longitudinal deck/rails now span the full 2m cell.
- Added release guards against regression to the floating entrance sprite or 1.82m path deck.


## R3.0-dev.8
- Added permanent wilderness approach path from the main gate to the outer map edge.
- Entrance sign text and font are persistent Park Manager fields.
- Entrance right-click opens Park Manager.
- Fence right-click opens Property / Land Office.
- Property parcel purchases charge the authoritative economy ledger and persist in save state.

## R3.0-dev.9 — living operations + owned-boundary architecture
- Purchased north/east/south/west deeds now derive the authoritative owned envelope. Grid, fence, gate position, wilderness approach, placement legality, save/load normalization and diagnostics all use that envelope.
- Existing dev.8 deed state is load-compatible; purchased parcels expand and reconnect the fence on rebuild rather than remaining paper-only ownership.
- Construction is rejected outside currently owned fenced property.
- Added insufficient-funds contextual feedback and transient red/green world-space transaction amounts for operator purchases, refunds, land and staff.
- Park Manager gains a throttled live entrance camera, five persistent Gateworks entrance families, five masonry finishes, fixed sign text/font controls, and branded lore. The redundant Interact Mode button is removed.
- Simulation speed moved to a main-HUD slider; guest-cap HUD opens an exact numeric editor.
- FrontierNet and Park Pulse are independent managers reached from a downward systems tray.
- Added a self-aware action tooltip that reflects hovered entities, current construction intent, affordability and idle Park Pulse context.
- Reworked title screen, topbar, tray and manager surfaces into darker cinematic glass with living motion.
- Expanded logos and contextual lore across Build, Park, Guests, Attractions, Staff, Economy, Land Office, FrontierNet, Park Pulse, Gateworks, Lore and Save surfaces.


## R3.0-dev.10 — Command Deck / UI Layering

Playtest-driven changes from the dev.9 review packet:

- Systems tray is now an anchored, viewport-clamped popover with a high authoritative z-index instead of a fixed strip that can appear behind, below, or off to the side of the toolbar.
- Escape always opens the cinematic Command Deck while the park is running.
- Command Deck actions: Continue, Save, Load, Cheats, Exit, Systems, and a dedicated × resume control.
- Load mode reads the real IndexedDB save store, displays each save, and supports both Load and Delete. Closing Load with × resumes the current park without loading.
- Backspace remains the window/tool close key so Escape has one unambiguous job.
- Simulation operations and keyboard camera movement pause while the Command Deck is open without mutating the saved simulation-rate setting.
- Dev screenshot capture now forces a render and uses a preserved WebGL drawing buffer, addressing the all-black PNG captured during the dev.9 test.
- Core-dump UI telemetry now includes command-deck mode/open state and screenshot capture metadata.


## R3.0-dev.12 — authoritative interaction router

Playtest-driven changes from the uploaded R233M feedback/core dump:

- Park entrance infrastructure is tagged `park-manager-only` instead of behaving like a generic inspectable object.
- Left-clicking the entrance in Interact mode now routes exclusively to Park Manager / Gateworks and consumes the event before generic entity inspection.
- Right-clicking the entrance routes through the same authoritative manager path.
- Perimeter fence right-click still routes to Property / Land Office; left-click provides a contextual hint rather than opening a generic object inspector.
- World interaction routing now records the target, route, source gesture, consumed flag, and timestamp in diagnostics.
- Release regression guards reject the former direct `Interact → rootEntity → openEntity()` fall-through form.
- The `parkIsOpen is not defined` failures in the uploaded dump are identified as an R233M collector/legacy-module-bridge problem, not a clean R3 runtime dependency. R3 continues to use `state.sim.open` rather than reintroducing the legacy global.

- Command Deck **New** action uses the same canonical initializer as the welcome screen and asks before replacing a running park.


## R3.0-dev.12 UI pass
- Removed the legacy startup `#title .cardTitle`; boot now opens the same Escape Command Deck used in-game.
- Park Manager is menu-first with branded operation tiles and deeper controls only after selecting a module.
- FrontierNet is no longer embedded in Park Manager; it remains a dedicated Systems surface.
- Static guest cap is controlled by a slider plus a clickable exact-number control in both HUD and Frontier Operations.
- Expanded park-management logos and lore while reducing form density.
