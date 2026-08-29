# RollamacoasterTycoon R3 POC Sprint 01

## Candidate

`rollamacoasterTycoon_R3_POC_SPRINT01_conversion_lab.html`

This sprint uses the uploaded R233M game as the gameplay body and adds an isolated Revision Conversion Lab.

## Required development cycle

**RELEASE → TEST → COMMENTS → CORE DUMP → REVIEW → PLAN → BUILD → RELEASE**

The cycle is implemented in the in-game developer overlay and persisted separately from park state.

## What was added

- early event-listener, fetch, error and rejection instrumentation
- a read-only module bridge to the existing authoritative `parkSnapshotR53()`
- `rct crawl` DOM/API/storage/environment mapping
- authoritative core dump
- snapshots and state diff
- comments tied to the active release cycle
- review and plan packets
- build-candidate checkpoints
- release records
- conversion-pack JSON export
- separate IndexedDB `rollamacoaster-revision-conversion-lab`

## Safety boundary

The lab does **not** treat the DOM or Three.js objects as authoritative game state. Core state comes through the existing R233M park snapshot function.

The original late revision scripts are byte-for-byte preserved. The authoritative module changes only at one explicit seam that exposes the read-only development bridge.

## Validation

- Inline executable scripts checked: **19**
- JavaScript syntax: **PASS**
- Late original scripts preserved: **PASS**
- Developer bridge insertion isolated: **PASS**
- Static DOM contains conversion lab: **PASS**
- Full automated WebGL runtime smoke: **not completed in container** because the legacy build dynamically imports Three.js from jsDelivr and the headless container could not complete that network boot. Interactive browser playtest is therefore the next release-test stage.

## How to use

1. Open the HTML normally.
2. Start or load the park as usual.
3. Click the small **R3** button at lower-right.
4. Run `rct crawl`.
5. Run `rct test`.
6. Enter observations in Comments.
7. Run `rct dump`.
8. Run `rct review`.
9. Run `rct plan`.
10. Run `rct build` before the next code mutation.
11. After testing the next candidate, run `rct release`.
12. Use `rct export` to download the complete conversion pack.

## First playtest targets

- New Game opens and camera becomes active.
- Existing save opens without camera/UI lock.
- Build panel opens.
- Paths can be placed.
- Guests spawn/walk.
- Scenery remains visible and animated.
- Ferris wheel/ride animation still functions.
- Guest Flock panel opens.
- `rct crawl` produces a system fingerprint.
- `rct test` sees the authoritative snapshot.
- `rct dump` exports the live park state without freezing the game.
