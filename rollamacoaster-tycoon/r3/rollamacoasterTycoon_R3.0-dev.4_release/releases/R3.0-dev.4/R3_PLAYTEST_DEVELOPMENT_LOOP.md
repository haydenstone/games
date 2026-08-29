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
