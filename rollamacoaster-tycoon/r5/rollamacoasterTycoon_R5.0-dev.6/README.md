# Rollamacoaster Tycoon R5.0-dev.6

Primitive-retirement proof. `world/spec.json` is the declarative source for the tiny world. `world-runtime-v2` replaces the dev.5 runtime implementation rather than patching it. Browser presentation is separate static presentation code consuming the world API.

Codex is external and expected at `$HOME/Documents/codex.json` by `start.sh`.

Minimum runtime: `./start.sh start`
Test: `./start.sh test`
Stop: `./start.sh stop`
