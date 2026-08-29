# RollamacoasterTycoon!! Revision Conversion Tracker

Generated: 2026-08-28T19:32:49

## Mission

Convert the R233M lineage into the RAG-first/backend-first structured architecture without silently losing behavior, design identity, agentic systems, persistence, or revision-era capabilities.

## Current position

**Gates G0 and G1 are complete. Gate G2 is next.**

### Archaeology baseline

- Feature/implementation atoms: **11,923**
- Revision meta descriptions: **201**
- Legacy audit contracts: **221**
- Legacy catalog entries: **140**
- Legacy functions: **1,345**
- DOM/UI IDs: **900**
- Runtime state keys: **298**

## Conversion gates

| Gate | Scope | Status | Exit condition |
|---|---|---|---|
| G0 | Fossil freeze + semantic parity | **COMPLETE** | Legacy/R3 sources frozen; 11,923 atoms extracted; 201 revision descriptions; 221 audits; catalog disposition ledger created. |
| G1 | Backend contracts + process skeleton | **COMPLETE** | Create local control-plane server, versioned schemas, health endpoint, event bus, provider registry. |
| G2 | RAG database + ingestion | **NEXT** | Ingest source, revisions, feature registry, project memory, entity graph and Alexandria/Codex namespaces. |
| G3 | Flock backend runtime | **PENDING** | Persistent runs/roles/turns/tool calls; Ollama default; cancellation; provenance; validation loop. |
| G4 | GPT/Gemini broker adapters | **PENDING** | Preserve GPT-broker semantics; add normalized Gemini adapter; graceful fallback; secret isolation. |
| G5 | Project API + validated developer tools | **PENDING** | Search/read/propose/apply/diff/validate with project-relative paths and deterministic gates. |
| G6 | Authoritative Game API | **PENDING** | Queries/commands/event stream; no renderer mutation channel; shared human/agent API. |
| G7 | World + camera + input projection | **PENDING** | Three.js client rebuilt over Game API/control-plane contract; camera/load regression guards. |
| G8 | Paths + queues + navigation + economy | **PENDING** | 2m path graph, 0.25m placement policy where applicable, queue topology, ledger/wallets. |
| G9 | Guests + staff + brains + inventory | **PENDING** | Preserve guest models; authoritative needs/thoughts/inventory; staff professions and inspectors. |
| G10 | Scenery + stalls preservation pass | **PENDING** | Port protected scenery/stalls without reducing design quality. |
| G11 | Custom engineering systems | **PENDING** | Custom coaster, elevated paths, route rides/transports; engineering validation. |
| G12 | Stock ride human-scale reconstruction | **PENDING** | Seat/access anchors, rider animations, boarding/unboarding, scale audits; rebuild weak geometry. |
| G13 | Alexandria + FrontierOS + media/comms | **PENDING** | Geocaches, relational knowledge, Wi-Fi, PA, phones, lighting, wildlife/media parity. |
| G14 | Performance + LOD + diagnostics | **PENDING** | Performance budgets without changing simulation truth; profiler and audit dashboard. |
| G15 | Save/import/migration | **PENDING** | R3 snapshots, legacy normalization, browser standalone sync, fresh runtime reconstruction. |
| G16 | Revision parity burn-down | **PENDING** | Process all 201 revision descriptions and 11,923 atoms; port/replace/supersede with evidence. |
| G17 | Flat HTML release compiler | **PENDING** | Generate single dist/rollamacoaster.html with full-agentic and standalone runtime profiles. |
| G18 | Final acceptance | **PENDING** | All protected features dispositioned, all critical audits green, no unexplained omissions. |

## Asset policy locked at G0

- **Scenery:** preserve design language, geometry, materials, scale, and authored animation/effect behavior unless technically broken. Animated scenery is not considered converted if its motion/effects are flattened.
- **Stalls/shops:** preserve design language, scale, counters, signage and product identity.
- **Guest models:** protected; renderer/LOD may change but recognizable models and animation ownership survive.
- **Custom ride/path engineering:** protected systems.
- **Stock rides:** feature identity is protected; geometry must pass human-scale, seat-fit and boarding animation gates.
- **Ferris wheel:** late-lineage queue/rider/cabin behavior is specifically protected.
- **Animated elements:** preserve motion ownership, cycle timing, transform ranges, particles, lighting modulation, water motion, kinetic art, wildlife/ambient movement, ride machinery animation, and any guest-visible synchronized effects. If implementation changes, the visible behavior must remain equivalent or better.

The detailed 140-item catalog disposition is in `rollamacoaster_asset_disposition_ledger.csv`.

## Conversion rule

Nothing is considered converted because code was copied. A feature is converted only when:

1. its new authoritative owner is identified,
2. its data schema is explicit,
3. its UI/render projection is separate from simulation truth,
4. its legacy evidence/revision is linked,
5. its save/migration behavior is defined,
6. its audit/acceptance test passes, and
7. its parity ledger status moves to PORTED, REBUILT, or SUPERSEDED_WITH_EQUIVALENCE.

## Immediate next work: G2

Build the first durable RAG/database layer behind the now-green G1 control plane:

- project/source document ingestion
- chunking and provenance
- feature-registry ingestion
- revision-meta ingestion
- entity/link tables
- project memories
- Flock run/tool-call persistence
- lexical retrieval first, vector adapter boundary second
- isolated Alexandria/Codex namespace
- retrieval API that returns evidence, not just text

G2 must be able to answer where a feature came from, which revisions changed it, which source evidence supports it, and which current structured subsystem owns it before we port gameplay implementations.