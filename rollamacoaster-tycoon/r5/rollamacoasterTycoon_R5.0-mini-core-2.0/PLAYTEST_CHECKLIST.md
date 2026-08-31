# Mini Core 1.1 Charlie playtest

1. Header says Mini Core 1.1 Charlie and container is `rct-r5-mini-core-2-0`.
2. Confirm eight cards labeled Container 0 through Container 7.
3. Confirm Container 0 says public and Containers 1–7 say private.
4. Start simulation and watch A/B on every card. They must visibly sweep smoothly and continuously in opposite directions with A+B=100% at all times.
5. Pause simulation. The visible A/B sweep must freeze. Resume and it must continue.
6. Confirm each card exposes X, Y, Z. Edit a coordinate and verify it persists after refresh.
7. Open Kernel Lineage Explorer and verify the containers, coordinates, A/B children and UUIDs are inspectable.
8. Confirm Codex displays three passages in the current reflection set and that the three units are cross-related in lineage/YAML.
9. Run `./run.sh test` and require PASS with zero primitive exceptions.
