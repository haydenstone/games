# RollamacoasterTycoon!! R3 Playtest Development Loop

The development loop is now:

**RELEASE → TEST → COMMENTS → CORE DUMP → REVIEW → PLAN → BUILD → RELEASE**

## 1. Release and launch

From the folder containing the R3 files:

```bash
./run_rct_r3_dev.sh
```

Equivalent manual commands:

```bash
python3 rct_r3_release.py
python3 rct_r3_dev_server.py
```

The release command rebuilds the standalone HTML, runs static JavaScript checks, fingerprints the artifact, writes a release manifest, and stages an immutable copy under `releases/<release-id>/`.

The development server opens the same standalone HTML at:

```text
http://127.0.0.1:8080/rollamacoasterTycoon_R3_rebuilt.html
```

## 2. Test in the actual game

Open **🧪 Test** in the top toolbar, or use the floating **🧪 DEV** button.

Play normally. When something is wrong, do not stop to reconstruct the state from memory. Leave the park in the failing state and enter a comment in the Test Bench.

Each comment automatically attaches:

- release ID and test-session ID
- active tool and selected buildable
- selected and hovered entity
- camera position and target
- visible UI windows
- park open/closed state
- time and simulation speed
- cash, guest count, staff count, and entity count
- number of browser/runtime errors observed so far

Use **PASS** and **FAIL** as checkpoints during the same test session.

## 3. Capture a core dump

When a defect is visible, click **🧠 Capture Core Dump** before changing the game state.

The browser core dump contains plain diagnostic data only. It includes:

- boot phase and boot log
- comments
- uncaught errors and rejected promises
- recent console log/warn/error events
- camera/tool/entity context
- performance and heap information when Chromium exposes it
- IndexedDB store counts
- recent economy ledger transactions
- complete plain simulation state

It deliberately does **not** serialize Three.js/WebGL runtime objects.

When running through `rct_r3_dev_server.py`, dumps are written automatically to:

```text
rct_r3_dev_sessions/<session-id>/
```

Useful files are:

```text
session.json
comments.jsonl
core-latest.json
review-latest.json
```

In standalone `file://` mode the Test Bench falls back to downloadable JSON files instead.

## 4. Screenshot the visible defect

Use **📷 Save View PNG** while the defect is still on screen. This captures the actual game canvas separately from the machine-readable core dump.

## 5. Export the review packet

At the end of a test run click **📦 Export Review Packet**.

The resulting JSON contains the exact release identity, all playtest comments, PASS/FAIL state, and the latest core dump. Upload that review packet with the next change request.

This is the preferred handoff into REVIEW.

## 6. Review and plan

The next development pass should use the review packet to produce:

1. observed behavior
2. intended behavior
3. reproducible sequence
4. root-cause hypothesis
5. affected authoritative subsystem
6. regression risks
7. smallest clean-core change
8. validation tests

The plan should fix the authoritative system rather than adding a later patch that intercepts another patch.

## 7. Build

Changes go into `build_rct_r3.py` or source data used by that builder. Do not hand-patch only the emitted HTML.

Rebuild with:

```bash
python3 build_rct_r3.py
```

## 8. Release again

Run:

```bash
python3 rct_r3_release.py
```

A release is not considered ready for the next playtest until the release manifest reports `"passed": true`.

Then launch the dev server and repeat the loop.


### Dev.6 path acceptance check
1. Turn the construction grid on.
2. Select Asphalt Path.
3. Place several adjacent tiles in horizontal and vertical runs.
4. Confirm each path occupies exactly one grid cell and adjoining tiles share cell edges.
5. Try placing a path beyond the perimeter fence; it must be rejected.
6. Inspect the full fence and entrance visually from Orbit mode.
7. Comment + core dump if any cell center, boundary, or fence section is wrong.


### Dev.8 acceptance
Right-click the entrance and fence separately; change sign text/font; orbit the sign; inspect the wilderness approach path; purchase a property parcel and confirm cash/ledger persistence.

### Dev.9 acceptance
1. Open the systems tray and confirm FrontierNet, Land Office, Park Pulse, Gateworks and Survey Grid carry distinct logos/lore.
2. Buy a neighboring parcel. Confirm cash feedback appears, the fence/grid reconnect around the newly owned envelope, and construction becomes legal inside the purchased land but remains blocked beyond it.
3. Attempt a purchase/build with insufficient cash and confirm the contextual tooltip reports the shortage.
4. Place/bulldoze a paid object and confirm transient red/green transaction text appears near the action.
5. Open Park Manager: verify live entrance camera, five visual gate families, five masonry finishes, sign text/font, and no redundant Interact Mode button.
6. Use the main-HUD simulation-rate slider.
7. Click the guest-cap HUD and enter an exact static guest cap.
8. Open FrontierNet as its own manager and Park Pulse as its own manager.
9. Stop moving briefly and confirm the self-aware tooltip can surface Park Pulse context.
10. Inspect title/welcome screen, tray and managers for the dark cinematic glass presentation.


## dev.10 acceptance pass

1. Start a park and press Escape. The Command Deck must render centered above every game surface.
2. Press × or Continue. The exact running park returns.
3. Press Escape → Save. Confirm a real IndexedDB save is created.
4. Press Escape → Load. Confirm saves appear with Load and Delete controls.
5. Delete a disposable save and confirm the current running park is unchanged.
6. Enter Load mode, press ×, and confirm it simply continues the current park.
7. Toggle Systems repeatedly at different browser sizes. It must remain attached below the Systems button and stay inside the viewport.
8. Capture a DEV screenshot and confirm the PNG contains the rendered park rather than a black frame.
9. Export the review packet.


## dev.11 acceptance pass

1. Enter Interact mode.
2. Left-click the physical park entrance, including its sign/towers/hit volume.
3. Confirm only Park Manager / Gateworks opens. Entity/Object Inspector must remain closed.
4. Close Park Manager and right-click the entrance. Confirm the same manager-only route.
5. Left-click a normal ride/shop/path entity and confirm its normal inspector still works.
6. Right-click the perimeter fence and confirm Property / Land Office opens.
7. Capture a core dump and verify `interaction.lastRoute.route` reports `park-manager`, `property-manager`, or `entity-inspector` as appropriate.

- Command Deck **New** action uses the same canonical initializer as the welcome screen and asks before replacing a running park.

## dev.13 acceptance pass
1. Confirm **Settings** appears immediately before **Systems** in the main toolbar.
2. Open Settings and verify Construction Grid + Render Quality live there and no longer appear in Park Manager.
3. Open Systems and then FrontierNet, Land Office, Park Pulse, Gateworks, and Alexandria as child surfaces. Close each child with Backspace and the mouse Back button and confirm the Systems parent remains underneath.
4. Open Park Manager and confirm the live entrance camera is the first content surface. Park Display, Park Pulse, and Alexandria must not appear as Park Operations modules.
5. Open Admission + Capacity. Drag admission from $0 through $200 and type values directly into the number field. Values above $200 must clamp to $200.
6. Change the guest cap through both slider and exact number fields in Park Manager and the HUD. No browser prompt dialog should appear.
7. Open the park at several admission prices. New candidate wallets should center on $120; guests unable to cover the fee should decline admission rather than enter with negative cash.
8. Save, reload, and verify an entrance fee greater than $200 can never survive normalization.
9. Export the review packet and inspect `economyRules.maxEntranceFee`, `economyRules.guestWalletMean`, errors, and frame faults.

## dev.16 focused playtest

1. Open the park and watch new guests appear at the far end of the wilderness path rather than at the gate.
2. Follow at least two guests from map edge to entrance and confirm admission is charged only at the gate.
3. Open Guest Atlas and compare several profiles, activities, needs and route plans.
4. Right-click a guest in the 3D world and verify their individual guest mind opens.
5. Confirm the GPS panel contains ten forecast points whenever the guest is not deliberately resting.
6. Leave the park open long enough to see local/Ollama thoughts diverge between guests.
7. In Entrance Identity, switch fonts and verify the sign preview visibly changes typeface.
8. In Gateworks, verify architecture icons and masonry swatches communicate their visual theme.
9. Capture Full Viewport, then export the review JSON. Confirm `visualCapture` is populated in the JSON and includes the PNG data URL.
10. Exercise Attractions, Staff, Economy, Lore and Command Deck Load/Delete routes to verify the semantic manager hardening.


## R3.0-dev.17
- Guest arrivals are stochastic and scheduled from live park rating/popularity and occupancy.
- Guest Mind opens with a live per-guest camera; GPS is collapsed by default.
- Guest credentials include phone, wallet, admission ticket after entry, and return-pass lifecycle.
- All chat composers use Enter to send and Shift+Enter for a newline through one delegated input router.

## R3.0-dev.18

Playtest target: guest credential projection + Economy Ledger hierarchy.

- Admission tickets are authoritative persistent guest credentials.
- Credential issuance is idempotent and repairs older admitted guest records on load.
- An already-open Guest Mind window refreshes ticket, wallet, inventory, and phase live after gate entry.
- Economy Ledger keeps transaction history collapsed by default behind a drill-down while preserving a single latest-transaction summary.
- Release validation rejects the former always-expanded transaction-list layout.
