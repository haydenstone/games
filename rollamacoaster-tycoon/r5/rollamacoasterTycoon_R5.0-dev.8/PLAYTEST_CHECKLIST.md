# R5.0-dev.8 playtest checklist

## Baseline contract
- [ ] UI renders immediately and remains readable.
- [ ] Ava still reflects on a Codex verse.
- [ ] Stop simulation: tick, Ava experience, happiness, wisdom, memory, and Guest 001 movement all freeze.
- [ ] Restart the server while stopped: simulation remains stopped.
- [ ] Resume: both Ava and Guest 001 continue from their saved positions.

## Ava dual timeline projection
- [ ] Two Ava markers travel around the clock simultaneously in opposite directions.
- [ ] They remain synchronized as projections of one Ava, not two independent entities.
- [ ] Stopping simulation freezes both projections.

## First guest
- [ ] Guest 001 appears on the path between Park entrance and Destination 01.
- [ ] Guest moves toward the destination only while simulation runs.
- [ ] Guest reaches the destination and reports arrived.
- [ ] No guest behavior affects Ava's Codex state or memory.

## Architecture smell test
- [ ] A guest exists as a generic actor, not through a GuestManager.
- [ ] Ava and Guest 001 share actor/time machinery without sharing inappropriate state.
- [ ] Presentation could be replaced without changing actor truth.
- [ ] Report any behavior that seems to require editing unrelated systems.
