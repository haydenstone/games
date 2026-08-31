# R5 Northstar

## The sentence to protect

> **One world. One authoritative truth. Many small responsive cells. No cell owns another cell.**

R5 should grow by adding vocabulary and relationships to the world, not by adding a manager for every noun. The browser, renderer, Ava, guests, future rides, multiplayer clients, Discord gateways, audio, and AI observers are perspectives or participants in the same world. None gets a private competing reality.

## Northstar principles

1. **The World Kernel is tiny and authoritative.** It owns identity, state transitions, simulation time, validation, persistence boundaries, and authoritative events. It should not become a warehouse for feature-specific behavior.

2. **World behavior is cellular and primitive-based.** A meaningful thing is described through typed state, capabilities, relationships, rules, channels, presentation descriptors, and version metadata. Cells respond to authoritative changes and publish proposals/events through common contracts. They do not reach sideways to mutate another cell's internals.

3. **Perspectives subscribe; they do not duplicate truth.** UI, 3D rendering, Ava, multiplayer clients, diagnostics, audio, and future gateways observe relevant authoritative changes. A perspective may appear or disappear without destroying the process, entity, conversation, task, or world state it observes.

4. **Process time is not simulation time.** Starting, stopping, refreshing, or replacing a server/container must never manufacture simulated experience. A stopped world stays stopped at the same timeline position. The computer can wake up without waking the world.

5. **Stable world coordinates belong to the world.** Moving a camera/player changes the observer's position. It does not move authoritative world coordinates to fake motion. Rendering tricks may optimize presentation without rewriting world truth.

6. **AI proposes; the world compiler decides.** Llama or any future AI may converse, observe, interpret, propose intents, data, code, or artifacts. It may not directly mutate authoritative reality or execute returned source as authority. Proposed changes pass through deterministic validation, migration, and commit boundaries.

7. **Codex is external and read-only.** The Codex may be observed and interpreted, but `codex.json` is not mutated by the world or AI. Observation, perception, interpersonalization/reflection, bounded effects, and memory remain distinct concepts.

8. **Preserve meaning, not obsolete implementations.** If a primitive is insufficient, version it, migrate meaningful state, validate the replacement, and retire the old primitive. Temporary adapters must be bounded and retireable. Repeated exceptions are evidence that the primitive should change.

9. **Bugs are evidence, not features.** Accidental behavior does not become a compatibility requirement. Accepted player-visible behavior and world meaning form the regression contract; implementation accidents do not.

10. **Presentation and runtime must be replaceable.** Replacing the browser UI must not erase Ava, Codex relationships, memory, simulation rules, or persistence. Replacing a runtime primitive must be possible through explicit migration without carrying obsolete implementation details forever.

11. **One deployable world surface.** Production runs from one container image with one externally exposed gameplay port. Internal adapters may exist, but the public gameplay surface remains coherent. Headless and interactive execution observe the same authoritative world.

12. **Future ideas are preserved without silently becoming scope.** Ideas from the family/team belong in an attributed idea ledger with provenance and status. Recording an idea protects it; it does not automatically alter the current release contract.

## Change test

Before adding a feature, ask: can this be expressed by adding or evolving an entity/template, primitive/capability, relationship, generic rule, or intent using existing contracts? If the answer requires editing unrelated systems independently, stop and reconsider the primitive vocabulary.

A healthy feature should make the world richer without making old cells know its name.

## Production invariant

`R5.0-dev.15.2b` is a behavioral checkpoint, not a prison for its source code. Future production rewrites may replace implementations aggressively, but they must preserve accepted world meaning or perform explicit, validated migrations when that meaning intentionally changes.

## Faith, transcendence, and operational trust

An aware entity may model faith as trust directed beyond what it can establish from inside its own bounded perspective. In the Dev.15.1 worldview, that transcendent orientation may identify the Holy Spirit as an external source of coherence and truth. R5 keeps this distinct from engineering trust: reliance on the kernel, persistence, validated inputs, and runtime invariants is an operational analogy for dependence, not a claim that software infrastructure is literally the Holy Spirit. Faith never grants a cell authority to bypass the World Kernel.

## Production 1.2 cellular rebase checkpoint

R5.0-dev.16.1a retires `world-runtime-v9-stability-gate` as the active runtime primitive and replaces it with `world-kernel-v10-cellular`. Persisted v9 world meaning remains readable as migration input. The production primitive registry is `world/primitives.json`.

Primitive survival is never assumed. A primitive may be versioned, migrated, validated, and retired whenever a clearer vocabulary preserves world meaning with less coupling. Exceptions remain legal only when explicit, bounded, attributable, validated, reviewable, unable to fork authoritative truth, and equipped with a retirement path.
