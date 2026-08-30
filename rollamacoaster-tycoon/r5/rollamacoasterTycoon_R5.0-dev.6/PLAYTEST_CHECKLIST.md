# R5.0-dev.6 playtest

This is the first primitive-retirement proof. Runtime v1 was not patched; its implementation was replaced by world-runtime-v2 while preserving the intended world concepts.

- [ ] `./start.sh start` gets to runtime with no manual Docker commands.
- [ ] Page is visibly rendered, not black/blank.
- [ ] All four controls are readable and consistently sized.
- [ ] Ava is visibly moving around the timeline ring while simulation runs.
- [ ] Stop simulation freezes tick and Ava's timeline position; start resumes from that position.
- [ ] Remove Codex access: Ava stops perceiving the verse and happiness trends down.
- [ ] Restore Codex access: the same iteration verse is perceived again and happiness trends up.
- [ ] New iteration chooses a new random verse while preserving Ava's bounded memory.
- [ ] Refresh browser: authoritative state remains coherent.
- [ ] Save, restart server, and confirm the v2 save is reloaded.
- [ ] Try rapid start/stop and Codex toggles. No contradictory UI/world state.
- [ ] Resize the browser. Timeline stays centered and controls remain readable.
- [ ] Architecture sanity: presentation could be deleted/replaced without changing simulation, Ava, Codex, memory, or rules.

Do not add mission-failure behavior during this proof. A future black mission-failure presentation must be intentionally specified, not preserved from an accidental blank-screen bug.
