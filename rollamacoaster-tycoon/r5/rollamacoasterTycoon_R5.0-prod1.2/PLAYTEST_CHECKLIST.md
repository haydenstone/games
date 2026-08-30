# R5.0-prod1.2 production playtest

1. Run `./run.sh start`, then open `http://127.0.0.1:8765`.
2. Continue into the Welcome Lobby. Click the world if the camera-control notice is visible.
3. Verify mouse up looks up, mouse down looks down, left/right remain correct, WASD moves, Shift accelerates, and Space jumps.
4. Press Escape. Verify the pause menu opens. Resume. If browser camera control is absent, verify the notifier appears; click the world and confirm mouse look returns.
5. Walk to a recognizable position/direction. Refresh, then restart the server. Confirm player position/direction persist.
6. Create a named save. Verify it appears in Saved games, loads, and deletes using the in-panel confirmation. Confirm no browser prompt/confirm dialog appears.
7. Pause the simulation and verify Ava/timeline experiential state freezes across server restart. Resume and verify simulation continues.
8. Toggle the Codex relationship while running and inspect Ava/diagnostics. Codex remains read-only and effects remain simulation-time gated.
9. If Llama is available, send a short conversation from Command Center. If unavailable, confirm the deterministic world still operates.
10. Download diagnostics and confirm the release identifies `R5.0-prod1.2`, spec 9, and `world-runtime-v9-stability-gate`.
11. Run `./run.sh test`. The automated production gate must pass.

## Dev.15.1 RC focused gate
- Open Developer Mode > Command Center > Llama.
- Send two conversation prompts. Confirm both remain visible in running history.
- Ask for a Markdown response with a heading, link, list, inline code, and fenced code. Confirm it renders as rich content.
- Ask for an HTML or Markdown fenced artifact. Confirm Copy works and Preview opens inside the response without executing scripts.
- Download a response as JSON and confirm the file contains the structured relay envelope.
- Restart R5 and confirm relay history remains.
- Confirm simulation still runs when Llama is offline.

## Dev.15.2a focused gate

1. Send three Llama messages and confirm the newest response is at the top.
2. Confirm each response has compact copy and download icons at its upper-right, with no large Copy response / Download JSON buttons.
3. Press Enter to send. After success, confirm the composer is empty and the caret remains in it ready for the next message.
4. Confirm Shift+Enter still creates a new line.

## Dev.prod1.2 focused gate
- Enter or Send clears the composer immediately, before the Llama response returns, and focus remains in the composer.
- Response copy/download controls remain flush-right and uniform, using compact line icons.
- The in-world relay persona uses consciousness/operator framing rather than generic AI-assistant boilerplate; provider identity remains an implementation detail.
