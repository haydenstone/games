# Rollamacoaster Tycoon R5.0-dev.8

First Guest transition. R5.0-dev.7 is now the immutable behavioral baseline contract. Dev.8 adds a generic actor primitive without adding a GuestManager.

- Ava is an actor with Codex perception and persistent memory.
- Ava's clockwise and counterclockwise timeline markers are two presentation projections of one authoritative timeline value.
- Guest 001 is another actor with a goal and path progress.
- The guest walks from Park entrance to Destination 01 only on simulation ticks.
- Process restart preserves simulation running/stopped state.
- External Codex remains at `$HOME/Documents/codex.json` by default.
- One Docker container, one exposed gameplay port: 8765.

Normal upgrade: stop old release, `cd ..`, unzip, enter directory, `./start.sh start`.
