# RollamacoasterTycoon R3.0-dev.24 — dev.23 Review Acceptance

Source review: R3.0-dev.23 playtest packet. Dev.23 captured 70,183 frames with no recorded JS or console errors, so dev.24 is a feature/presentation expansion over the stable clean-core baseline.

## Review checklist implemented

1. **Camera pitch locomotion** — W/S follows the full camera look vector, including Y pitch. Space remains explicit vertical lift; Shift accelerates.
2. **Complete DB Explorer** — browse all IndexedDB stores, search, inspect objects, follow live entity links, inspect templates/UUID diffs, export bundle, import bundle, and double-arm reset a store.
3. **Collective Guest Signal window contract** — now a normal draggable panel with title bar, X, Backspace close, and mouse-Back close.
4. **Frontier environment** — mixed tree forms/species palette, two rivers, rock formations, water-edge scenery, and an abandoned mill.
5. **Camera focus/follow** — entrance, guests, workers, pets/wildlife and global map provide focus/follow actions where relevant.
6. **Grounded actors** — person rigs are lowered so feet meet terrain/path elevation instead of hovering.
7. **Human guest presentation** — rounded capsule/sphere bodies, faces, hair variation, long hair/ponytail/bob, age scaling, and purse inventory/props for some feminine presentations.
8. **Message-all replies** — FrontierOS admin broadcast produces retained guest replies back into the admin phone inbox.
9. **FrontierOS visual redesign** — phone-shaped frame, wallpaper/screen, app grid, dock and app views instead of a form-heavy manager.
10. **Global park map** — live top-down Three.js camera, legend, guest/staff/wildlife/attraction counts and focus actions.
11. **Notes** — editable, saveable and copyable admin and personal guest notes.
12. **Guest map app** — opens the same global live park map.
13. **Network truth** — guest phones start OFFLINE with 0 signal and only connect when a built Wi-Fi AP is in range.
14. **Guest FrontierOS button** — compact button rather than a full-width slab.
15. **Communication history** — retained face-to-face social-interaction log in addition to phone messages, plus Browser app.
16. **Worker inspector depth** — live worker camera, thought/status, mood/energy, inventory, FrontierOS network/messages, personality, duties and role metrics.
17. **Worker operations UI** — user-facing task/status first; editable uniform/presentation and duties; coordinate/UUID data remains under collapsed technical detail; Focus Camera and Follow are explicit actions.
18. **Day/night duration** — 3.5 sim minutes/real second at 1×, keeping a full simulated day under seven real minutes.
19. **Lighting** — entrance lantern intensity/range increased; lamp-class lights now cover a broader multi-grid area and brighten at night.
20. **Staff models** — staff use the same rounded human actor rig rather than Lego-like blocks.
21. **Crew Manager scale** — aggregate metrics plus separate Handyman/Security/Entertainer/Construction sections rather than one unbounded list.
22. **Entertainer variety** — human-first performer rig with selectable roles/costumes, including Frontier Ranger, Victorian Photographer, Princess, Dragon Host, Space Ranger, Pirate, Tiger, Elephant and Robot character layers.
23. **Wildlife density** — Settings slider controls persistent wildlife population. Deer, rabbit, fox, raccoon and squirrel actors are hoverable/inspectable with thoughts, inventory/field record, live camera, focus/follow and interactive field chat. Companion pets retain leash/unleash.

## Entertainer photo economy

- Entertainers retain one staff UUID while costume layers change.
- Park Photographer/performer behaviors can take photos of eligible nearby guests.
- Buyer wallet is debited and park cash credited through the authoritative economy ledger.
- Ledger rows retain buyer/photographer references and transaction history stays collapsed by default.
- The purchased photo is a persistent guest inventory item containing a reduced JPEG captured from the live Three.js renderer at the sale moment.
- Clicking the photo opens an inspectable Park Photo window with the actual image and links back to buyer, photographer and Economy Ledger.

## Release gates

- deterministic generator rebuild: PASS
- Node JavaScript syntax: PASS
- TypeScript unresolved-identifier scan: PASS
- required feature/regression markers: PASS
- camera/grid regression guard, including ban on legacy `forward.y=0`: PASS
- separate-directory portability rebuild: PASS, identical HTML SHA-256

## Next playtest

1. Boot into the Command Deck over a staged world, then Continue.
2. Aim camera sharply down and hold W; verify camera descends along view direction. Aim up and verify W climbs. Verify Space remains pure lift.
3. Open Systems → Database Explorer. Browse entityTemplates/entityInstances, follow a UUID diff to a live entity, export a bundle. Test import/reset only on disposable data.
4. Drag Collective Guest Signal; close it via X, Backspace and mouse Back.
5. Inspect rivers, mill, rocks and forest from the global Map and main camera.
6. Set wildlife density 0%, 50%, 100%; verify population responds and wildlife can be hovered/right-clicked/focused/followed/chatted with.
7. Inspect adult/teen/child guests and hair/presentation/prop variations. Confirm feet remain planted on paths/terrain.
8. Build no Wi-Fi AP and inspect a guest phone: OFFLINE/0 signal. Build an AP near guests and verify PARKNET connectivity.
9. Test guest Notes Save/Copy, Browser offline/online, Texts, Contacts and global Map.
10. Broadcast a message to all guests and confirm responses return to FrontierOS Admin.
11. Let guests socialize; inspect Relationships and In-Person Interactions plus phone Contacts/knowledge exchange.
12. Hire each staff role. Inspect worker live camera, thought, inventory, phone, duties, uniform and metrics; test Focus/Follow.
13. Hire an entertainer. Change role and cycle costumes including Tiger/Elephant/Robot. Confirm same UUID survives costume changes.
14. Let an entertainer sell a photo. Confirm guest wallet decreases, park ledger receives revenue, photo appears in guest inventory, and clicking it opens the actual captured picture.
15. Observe a complete day/night cycle and entrance/path lighting.
16. Capture Full Viewport, add comments, capture Core Dump and export the next review packet.
