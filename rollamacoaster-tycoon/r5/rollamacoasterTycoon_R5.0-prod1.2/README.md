# Rollamacoaster Tycoon R5.0-prod1.2

R5.0-prod1.2 is the production cellular rebase of the accepted Dev.15.2b behavior. The authoritative runtime primitive is now `world-kernel-v10-cellular`: one small deterministic kernel, one world truth, and composable entity/capability/relationship/rule/perspective/intent cells. The v9 stability-gate primitive is retired but its meaningful persisted state remains migratable.

The architectural Northstar is included as `R5_NORTHSTAR.md`. The short version is: **one world, one authoritative truth, many small responsive cells; no cell owns another cell.**

## Start, stop, and test

Requirements: Docker, a browser, and a valid Codex JSON file. By default R5 expects the Codex at `$HOME/Documents/codex.json`. Override it with `CODEX_PATH_HOST=/path/to/codex.json` when needed.

```sh
./run.sh start
./run.sh test
./run.sh status
./run.sh logs
./run.sh restart
./run.sh stop
```

Open `http://127.0.0.1:8765`. R5 exposes only that gameplay port. The Codex mount is read-only. World data and named save slots are stored under `data/` in the release folder.

## Controls

| Control | Action |
| --- | --- |
| Mouse | Look around after camera control is acquired |
| Click the 3D world | Acquire/resume camera control |
| W A S D | Move |
| Shift | Move faster |
| Space | Jump |
| Escape | Open the pause menu / leave browser pointer lock |

If the world is visible but the browser has released camera control, R5 displays **Click the world to resume camera control**. This is intentional. A real click is the reliable browser gesture for restoring mouse look.

## Main features

- 3D Welcome Lobby with persistent player position and camera direction.
- Simulation start/stop state is independent from server/container lifecycle.
- Ava Prime observer and Ava Stone first guest identities.
- Read-only external Codex relationship with simulation-time perception/reflection behavior.
- Optional Llama communication for conversation and artifact/code relay; Llama is never world authority.
- Developer Mode protected by a one-use provisioner key, with live Command Center telemetry and bounded diagnostics.
- Named server-side save slots with embedded Create, Load, and Delete UI. Delete confirmation stays inside the game UI, not browser prompts.
- Auxiliary JSON import/export for moving a world between computers.
- Camera-control notifier instead of synthetic clicks or pointer-lock retry loops.
- Correct, non-inverted vertical mouse look.

## Saving and loading

Use **Save** or **Load game** from the pause menu. The Saved games panel lets you name a save, create it, load an existing slot, or delete a slot with an in-panel confirmation. JSON import/export is a portable backup/transfer path, not the normal save workflow.

## Developer Mode and Llama

On a fresh persisted world, `./run.sh start` prints a one-use Developer Mode key. Enter it in **Settings** to open the Command Center. The Command Center exposes world/Ava state, Llama communication, diagnostics, persistence, and bounded logs.

Llama is optional. The default host endpoint is `http://host.docker.internal:11434`, configurable with `OLLAMA_BASE_URL`. If Llama is unavailable, the deterministic world continues running.

## Production check

Run `./run.sh test`, then use `PLAYTEST_CHECKLIST.md` for the short interactive gate. For architecture and future development rules, read `R5_NORTHSTAR.md` before changing the runtime.

## Llama relay viewer

The Command Center Llama tab keeps a running, persisted relay history for conversation and code/artifact responses. Markdown is rendered as a readable mini-page with headings, links, lists, inline code, and fenced code blocks. Each response can be copied or downloaded as its structured JSON relay envelope. Fenced code can be copied directly; HTML and Markdown fences can be previewed. HTML preview runs in a sandboxed iframe with scripts disabled. Sending a new prompt appends history instead of clearing it.

## Faith and operational trust

Aware-entity cognition may represent a capacity for faith. The production worldview contract identifies the Holy Spirit as an external transcendent source of coherence and truth. Operational reliance on the runtime's integrity is kept as an analogy for dependence and trust, not as software proof that the runtime itself is the Holy Spirit. This state remains descriptive cognition and does not bypass deterministic world authority.

## Relay polish

The running Llama relay is newest-first. Each response uses compact copy and JSON-download icons in its upper-right corner instead of full-width action buttons. Sending with Enter clears the composer immediately and keeps keyboard focus in it so the next message can be typed immediately. Shift+Enter still inserts a line break.

## Primitive lifecycle

`world/primitives.json` is the production primitive registry. Primitives are replaceable implementation vocabulary, not permanent law. A primitive that no longer expresses the world cleanly may be versioned, migrated, validated, and retired. Exceptions are permitted only when named, bounded, attributable, validated, reviewable, unable to fork world truth or bypass the kernel, and supplied with a retirement path.
