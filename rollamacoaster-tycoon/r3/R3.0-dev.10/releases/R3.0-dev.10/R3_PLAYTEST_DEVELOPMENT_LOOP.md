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
