# R3.0-dev.25 acceptance sheet

## Scope of this release

Dev.25 is the **knowledge-spine + runtime-stabilization** cycle. The uploaded dev.24 review remains the master visual/interaction backlog, but this release intentionally prioritizes the new Alexandria/Ollama/entity/database request plus the repeated operations frame fault captured during the dev.24 run.

## Closed in dev.25

- [x] Fix repeated `guestProfile()` operations frame fault: `Assignment to constant variable`.
- [x] IndexedDB schema v5.
- [x] `alexandriaDocuments` store.
- [x] `alexandriaQueries` store.
- [x] `knowledgeEdges` store.
- [x] SEARCH / DISCOVERED / ARCHIVED persistence model.
- [x] Same-origin Python LoA bridge. No Elasticsearch credentials in HTML.
- [x] Real LoA keyword-search route proxy.
- [x] LoA document/debug proxy.
- [x] Deliberate full-document archive path with byte cap.
- [x] Systems → Alexandria Neural Link manager.
- [x] Entity-targeted discoveries for guest/staff/pet/wildlife/world/park research.
- [x] Guest FrontierOS Alexandria research app.
- [x] Guest first-person chat LoA retrieval grounding.
- [x] Guest Flock LoA retrieval grounding.
- [x] Ollama KnowledgeBroker RAG path with retained source IDs.
- [x] Database Explorer exposes LoA cache/query/edge stores.
- [x] Core dump reports Alexandria bridge state plus new DB counts.
- [x] LoA outage does not block game boot.

## Dev.24 review backlog retained for the next visual/interaction cycle

The following dev.24 comments were reviewed and are deliberately **not marked closed merely because dev.25 exists**:

- camera pivot/axis closer to lens,
- richer entrance hover and park-value graph/HUD symbol,
- broader multi-tile lighting,
- authoritative dark-gray grid everywhere,
- tree hotkey consistency,
- richer wildlife locomotion/action animation,
- richer guest group/item/sitting animations,
- underground ground transparency/blackout behavior,
- phone as a self-contained OS surface,
- full-screen phone apps/home/apps/volume controls,
- park map visual fidelity,
- phone-hosted map framing,
- live Wi-Fi/no-signal bars,
- shift-click rapid placement,
- ctrl-click demolish + $12 tree value,
- R rotate / B build routing,
- pet/wildlife facing and animation,
- collective guest health bars,
- handyman uniform rebuild and trash-bin duty,
- collapsed technical records on all UUID entities,
- worker phone texting/chat,
- worker 10-thought tracker and equip-in-hand animation,
- entertainer-hire runtime path regression test.

Dev.25 must not hide these behind a generic "review passed" claim. They remain explicit targets for the next pass after the knowledge spine is proven in live play.

## Dev.25 playtest

1. Boot with no `RCT_LOA_BASE`. Command Deck must appear and game must remain playable.
2. Open park and run long enough to spawn many guests. Confirm the old `Assignment to constant variable` frame fault never returns.
3. Systems → Alexandria Neural Link. Confirm status says not configured/offline and local Alexandria/Codex still search.
4. Start LoA and relaunch with `RCT_LOA_BASE=...`. Refresh Alexandria status and confirm LIVE.
5. Search a known LoA term. Confirm results appear in `alexandriaDocuments` at SEARCH level.
6. Right-click a guest, then open Alexandria and Discover a result. Confirm a `knowledgeEdges` row and guest brain knowledge record are created.
7. Repeat for a worker and a wildlife entity.
8. Use Guest FrontierOS → Alexandria and let that guest learn a result.
9. Use Retrieve + Ask with Ollama online. Confirm answer names source IDs and top used records become DISCOVERED.
10. Archive one small document. Confirm level ARCHIVED and complete payload metadata in `alexandriaDocuments`.
11. Open Database Explorer and inspect `alexandriaDocuments`, `alexandriaQueries`, `knowledgeEdges`.
12. Run Guest Flock with a research question and confirm it receives live/cached LoA context without gameplay blocking.
13. Capture Full Viewport, Core Dump, Export Review Packet.
