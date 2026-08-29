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
