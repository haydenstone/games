# RollamacoasterTycoon!! Recovered Revision Meta Descriptions

Recovered 201 explicit hidden revision summaries from the R233M source.

## R96B · paths_construction
Source line 25276

rotation HUD visible only during active rotatable placement.

## R98B · core_misc
Source line 25278

high-detail to-scale food stalls with rooftop product sculptures.

## R99B · core_misc
Source line 25279

shorter individually themed HD food stalls.

## R100B · guest_sim
Source line 25280

remaining stalls themed, including balloons, information pavilion and arcade.

## R101B · guest_sim
Source line 25281

smaller restroom; continued HD theming for balloons, kiosks, candy, donuts, umbrellas and tacos.

## R102B · guest_sim
Source line 25282

guests understand and use ATMs to replenish spending money.

## R103B · rides_attractions
Source line 25283

backend ride geometry redraw, no generated images.

## R104B · rides_attractions
Source line 25284

every queue variant qualifies ride startup; queue corners render as cardinal 90-degree turns.

## R112B · rides_attractions
Source line 25285

exact R104 baseline; R103 redrawn ride models retained; animations expanded only inside frame.

## R114B · rides_attractions
Source line 25306

+10 HD/lore/logo/emoji/priced animated objects in paths, rides, shops, services and scenery.

## R126B · ui_ux
Source line 25307

stable R115D import architecture + builder exposure + unique HD models + universal ride class/access/economy + ride animations + $12 tree salvage. No selectedGuest global.

## R127B · persistence
Source line 25308

import/load reconstruction yields to browser between object/ride/guest batches to prevent Chrome UI freeze.

## R128B · guest_sim
Source line 25309

compact smiley happiness menu + diverse guest identities/interests + all-guests neural social mesh with independent/social behavior.

## R129B · economy_research
Source line 25310

completed economy/items for smoothie, pretzel, sushi, fries, souvenir, chicken and plush; selected advanced buildables are completely hidden until research unlocks them.

## R130B · ui_ux
Source line 25311

fixes R129 startup UI lock by removing pre-initialization dependency on researchStateR37 from initial builder render.

## R131B · ui_ux
Source line 25312

guests cannot form queues on ordinary paths; ride queue intent now requires a reachable queue entry and waiting positions remain queue-only.

## R132B · camera_input
Source line 25313

import camera lifecycle fix. Clears stale guest camera pivot and stranded pointer-disable state; explicitly transitions import to GAME + CAMERA READY.

## R133B · camera_input
Source line 25314

import readiness now ends in neutral ORBIT mode; saved park state never restores transient Build/editor camera interaction state.

## R134B · environment
Source line 25315

visual-only HD art pass for guests, placed trees, frontier trees, grass terrain and lighting. Gameplay/import/camera logic unchanged from R133B.

## R136B · ui_ux
Source line 25316

safe searchable Build Database built on R134. Keeps research visibility declarations and valid buildTopicR10 states intact.

## R137B · ui_ux
Source line 25317

Build Database can be opened repeatedly. Build button/F1 use canonical open path; closing exits build mode cleanly.

## R138B · persistence
Source line 25318

localStorage park project explorer replaces JSON import/export; Save/Save As/Open manage named internal save files. Build/F1 can open multiple independent Build Database windows.

## R139B · staff_ops
Source line 25319

guest puke/litter/bins + per-handyman duty checkboxes + garden watering + mowable growing grass stubble.

## R140B · performance_diagnostics
Source line 25320

guest models now face their actual travel direction; HD face geometry forward axis corrected by 180 degrees.

## R141B · guest_sim
Source line 25321

guests use benches/tables, sit and rest, animate eating/drinking purchased food, carry/release/click-pop balloons.

## R142B · guest_sim
Source line 25322

guests physically sit on bench/table geometry and visibly manage/eat/drink portable inventory while walking.

## R143B · guest_sim
Source line 25323

expands visible guest inventory to plush toys and souvenirs; guests can walk while carrying plush, maps, photos, keychains, guides and pet rocks.

## R145B · guest_sim
Source line 25324

safe wellbeing retry from R143. Positive/negative thoughts plus uncommon stress spirals using existing periodic service sweep; Family Care/Security can recover guests.

## R154B · persistence
Source line 25325

built directly from R145B. Root save/load fix: live Three.js runtime refs (guest limbs, ride rotors, meshes/curves) are never serialized or overwritten by legacy JSON.

## R159B · ui_ux
Source line 25326

built directly from R154B. Guest status/time/relationships + invitation-only whiteboard with duplicate merging/reinforcement counts + least-happy priority feed.

## R160B · guest_sim
Source line 25327

adds explicit whiteboard collaborator dismissal/revocation from guest page and idea cards; existing workflow history remains intact.

## R161B · ui_ux
Source line 25328

glass UI expert pass with contextual bottom information dock for camera modes, hovered/clicked entities, guests, placement, tooltips, and live status messages.

## R162B · ui_ux
Source line 25329

context glass dock moved upward 35px on desktop and mobile.

## R163E · economy_research
Source line 25330

main HUD park-value tracker derived from economy, placed asset appraisal, stock-at-cost and conservative operating goodwill.

## R165B · paths_construction
Source line 25331

new path/queue placement locked to 2m construction grid; grid visibility toggle; cardinal path snapping; auto queue bends/rails; queue capacity 3 guests per square with live occupancy tracking.

## R166B · ui_ux
Source line 25332

attached queue grid cells form continuous snaking/S-turn queues; rails open on shared edges, bends get contained inner guides, queue chain follows successive turns, and 3-person slot positions follow bend geometry.

## R167B · audio_media
Source line 25333

path speakers can open a YouTube selector popup, store a per-speaker YouTube video ID, and embed a minimized/openable youtube-nocookie player inside the speaker inspector.

## R168B · ui_ux
Source line 25334

queue cells visually weld into continuous snake corridors. Shared edges remain open, barriers only wrap outer perimeter, and orange center guides flow through straight and bent sections.

## R169B · audio_media
Source line 25335

Jamendo royalty-free/licensed track selector and minimized inline audio player replace YouTube speaker media.

## R170B · audio_media
Source line 25335

guests hear nearby path speakers, collect source/track/title/artist/tag/volume/distance/exposure metadata, form preference-based opinions, publish music thoughts, and retain music memories on guest records.

## R173B · audio_media
Source line 25336

starts from working R170 player. Jamendo playback now uses persistent hidden DOM audio elements per speaker, preserving the browser-compatible R170 playback path while surviving inspector close/refocus/re-render.

## R174B · audio_media
Source line 25337

Jamendo track title, artist, album, genre/mood/musicinfo tags, duration and license are fetched automatically from Jamendo track metadata using JSONP, including when opened from file://.

## R175B · audio_media
Source line 25338

path-speaker audio is spatially attenuated by camera distance. Main PA acts as a program bus reproduced by linked physical speakers, with link-all/unlink-all and PA play controls.

## R176B · paths_construction
Source line 25339

organized Family Zone expansion with 6 cinematic animated scenery objects and 4 gentle family rides, standardized through ITEMS, BUILD_META_R114, catalog grouping, placement, animation, and save-safe runtime references.

## R177B · environment
Source line 25340

Jumping Fountain now launches animated water packets from each of four valves to each of the other three valves using continuous ballistic arcs across the path.

## R178B · performance_diagnostics
Source line 25341

guest navigation is material-agnostic across every catalog path type; queues are restricted to active ride queue routing only, with legacy queue-wander recovery and diagnostics.

## R179B · environment
Source line 25342

verifies jumping-fountain ballistic water arcs and adds animated pond, waterfall, musical-fountain, duck-boat and rapids water surfaces with ripples, shimmer, flow and churn.

## R180B · environment
Source line 25343

repairs scenery placement previews and missing constructors for Rose Arch, Neon Tree, Firefly Grove, Mini Clock Tower and Laser Flowers; improves Frontier Statue/Park Gazebo/Topiary models; adds 6 HD tree species and 6 flower/garden items with lore, logos, prices and DB/economy placement.

## R181B · paths_construction
Source line 25344

hover any placed object or path and press R to rotate it 90 degrees. Placement ghosts retain R priority; selected-object rotation remains as fallback.

## R182B · paths_construction
Source line 25345

paths freeplace by default; Shift is burst-build drag mode; Ctrl+Shift is snapped burst mode using the 2m construction grid and cardinal stepping; Ctrl alone remains bulldoze.

## R183B · performance_diagnostics
Source line 25346

performance pass adds spatial hashing for paths/objects/speakers, staggered guest logic, throttled manager redraws, lower-frequency PA/music updates, guest LOD, and adaptive guest processing budget.

## R184B · paths_construction
Source line 25347

procedural soundscape adds category-aware placement SFX, sparse positional machinery squeaks, adaptive crowd ambience that grows with guest population, park open/close cues, and an ambience toggle.

## R185B · ui_ux
Source line 25348

repairs researchListR37 manual research with persistent active state, delegated Start buttons, explicit errors, manual activation/pause, expanded advanced attraction research, and separation from Finance auto-portfolio quota.

## R186B · economy_research
Source line 25349

Manual R&D now gates a prerequisite research tree. Activating Manual R&D unlocks tier-one projects; completing projects unlocks child programs beneath them, with explicit disabled states and prerequisite labels.

## R187B · alexandria_geocache
Source line 25350

geocaching mini-game adds buildable Alexandria Geocaches, exactly 10,000 deterministic indexed knowledge topics, coordinate hunting, guest route assignment, cache reading, portable information-card inventory, library search, cache atlas, and economy-linked network seeding.

## R188B · guest_sim
Source line 25351

Alexandria geocaching is explicitly free for guests. Hunting, reading, and information-card pickup never deduct from guest wallets; only the park pays the cache construction cost.

## R189B · flock_ai
Source line 25352

adds Guest Flock main-menu entry and persistent guest-agent DB modeled on shared neural workspace concepts: every guest auto-joins as Scout/Shepherd/Planner/Builder/Reviewer/Archivist, sharing tasks, facts, discoveries, turns and decisions; geocaches and whiteboard feed the workflow.

## R190B · ui_ux
Source line 25353

Guest Flock Studio adds custom tasks, CHAT/BUILD modes, thinking toggle, Ollama model selection, persistent project explorer, code editor, live web preview, popout, TAR/JSON export, and role-based file delivery.

## R191B · guest_sim
Source line 25354

Park Manager guest cap slider 0–2000 plus Unlimited; admission cap persists. Crowd optimization collapses mid/far HD guest bodies to single-mesh proxies, suppresses distant shadows/limb animation, and staggers leisure/inventory/mess systems.

## R192B · flock_ai
Source line 25355

Guest Flock Studio UI redesigned around the attached Ollama Studio composition with left rail, model header, agent state bar, chat-style composer, project drawer and right live/code preview. Adds explicit run ID, elapsed timer, mode, current stage, active guest agent, stage progression, file delivery count, stop/stopping/error/complete states and recent-run status.

## R193B · flock_ai
Source line 25356

preserves full recognizable human guest models at every distance, uses shadow/animation LOD rather than capsule replacement, adds guest dogs/cats, and connects all guests through a persistent shared neural-learning mesh that exchanges nearby observations, collective facts and lessons and feeds them into Guest Flock.

## R194B · ui_ux
Source line 25357

Project Explorer can open in a dedicated new window. Double-click any file or press Window. The external explorer includes file tree, code editor, save/create/delete sync back to the game project DB, and split live web preview with relative HTML/CSS/JS resolution.

## R196B · ui_ux
Source line 25357

rebased from R194B. Natural multi-project explorer adds create/switch/rename/delete projects, persistent folders including empty folders, file/folder selection, create, rename, move, duplicate and delete operations, while preserving R194 external window and live-preview behavior.

## R197B · flock_ai
Source line 25358

Flock coding workflow now enforces operator-intent deliverables, requires index.html for website/app requests, rejects config/settings-only website output, automatically requests a corrected Builder pass, injects the actual assigned live guest entity into every agent call, and shows every flock member with role icon, live park location and Chat button.

## R198B · ui_ux
Source line 25359

fixes Builder no-file-block failures by accepting file tags, filename-labeled Markdown fences and raw HTML, adds automatic transport retry, and renders agent code in fenced transcript blocks with inline Copy and Preview controls.

## R199B · flock_ai
Source line 25360

adds strict artifact-only synthesis after prose-only Builder retries, plus deletable recent runs and recent flock conversations with open/delete controls.

## R200B · guest_sim
Source line 25361

operational reachable bathrooms relieve bathroom/nausea/comfort, hungry/thirsty guests route to stocked open food stalls and consume matching products, completed roller coasters relieve boredom and raise excitement/mood, and Park Manager exposes a live entity coverage audit.

## R201B · economy_research
Source line 25362

restores high-contrast Flock/Explorer text and hardens Research & Development with document-level click capture, auto-activation of Manual R&D on project start, persistent progress, catalog unlock refresh, live R&D audit, and Next Available action.

## R202B · ui_ux
Source line 25363

queue paths remain simple flat 2m ground slabs unless their connected topology forms a genuine snake: at least 5 queue slabs, exactly 2 endpoints, no junctions, and at least 2 bends. Snake rails/guides appear only while that topology remains valid.

## R203B · rides_attractions
Source line 25396

adds point-by-point custom roller coaster engineering with required complete circuits and intelligent intensity assessment. All ride guests remain visible while riding; every ride gets rider anchor placement and compact attractions auto-scale upward when needed to visibly hold people.

## R204B · paths_construction
Source line 25397

repairs R203 runtime regressions. beforeR200 snapshots now have function scope, Custom Coaster Builder no longer assigns nonexistent buildModeR47, its controls use delegated DOM listeners despite late markup, and open/placement errors surface visibly instead of failing silently.

## R205B · ui_ux
Source line 25398

Custom Coaster Builder is camera-mode independent. Number keys 1–5 switch camera modes without leaving the builder, key 2 no longer routes into the normal Build Manager while coaster engineering is active, the panel exposes 1–5 camera buttons, and mode-2 coaster engineering retains WASD/arrows plus Shift-wheel camera movement.

## R206B · rides_attractions
Source line 25399

coaster trains are articulated into independently sampled linked cars that bend and pitch around the curve, riders are visibly seated on individual cars, Ride Manager has configurable ride-cycle duration, every ride calculates an intensity rating, and guests choose/co-satisfy rides based on personal intensity cravings and craving-match quality.

## R207B · rides_attractions
Source line 25430

adds route-built Tram, Park Railway, Monorail and Log Flume engineering tools. Routes are laid point-by-point with camera 1-5 support, must form complete circuits, and transport rides support multiple station nodes. Built vehicles use articulated cars that follow the route independently and riders remain visible in cars.

## R208B · rides_attractions
Source line 25431

fixes route builders missing from Build Database. Tram and Park Railway now have explicit Rides catalog entries, Monorail and Log Flume are labeled as route builders, route types remain visible even when research-locked, and cloned Build Database windows launch the correct route engineer.

## R209B · rides_attractions
Source line 25432

Camera mode 1 is now exclusively Orbit while custom coaster, tram, train, monorail or flume builders are active. Canvas clicks/drags in mode 1 pass through to camera rotation and never create track nodes. Construction point placement is restricted to camera modes 2-5.

## R210B · rides_attractions
Source line 25433

every routed transport station can now receive its own entrance and exit gate, each access point must attach to a normal guest path, guests choose reachable origin/destination stations, wait at the origin, board during station dwell, remain visibly seated in articulated cars, and disembark onto the destination exit path. Tram/train/monorail cars also run with much tighter coupling spacing.

## R211B · paths_construction
Source line 25434

multi-stop station entrances/exits now reuse the exact normal ride-access placement pipeline: same full-size gatehouse geometry, same silhouette preview, same R rotation and rotation HUD, same pointer-following ghost, same right-click cancel, with station-specific path-link validation and metadata.

## R212B · paths_construction
Source line 25435

station access placement is now flexible. Routed rides default to an 18m entrance/exit placement radius and 4.5m path attachment tolerance, both adjustable per ride in Ride Manager from 6-40m and 2-8m respectively. Existing silhouette, R rotation and full-size gate behavior is retained.

## R213B · rides_attractions
Source line 25436

riders are now actively animated while mounted on rides. Boarding interpolates guests into seats, seated limbs pose correctly, bodies sway/bounce with ride motion and intensity, coaster/transport riders follow their individual cars, and poses reset on exit.

## R214B · rides_attractions
Source line 25437

station entrances/exits are now explicitly linked to the selected transport stop, may be placed several grid blocks away, automatically snap onto the nearest normal guest path, default to a 32m stop radius and 12m path-search radius, and can be adjusted up to 48m/14m in Ride Manager.

## R215B · performance_diagnostics
Source line 25438

hotkey 6 toggles Tree X-Ray. All identified placed trees and procedural frontier trees become 18% transparent with depth write disabled, then restore their original materials on the next press. State persists and newly created frontier/placed trees inherit it.

## R216B · rides_attractions
Source line 25439

fixes multi-station access placement. Every station Entrance/Exit button now carries the routed ride ID, each stop stores independent stable gate IDs, placed gates draw at the clicked world location aligned to path height, visibility/scene parenting is verified before the ghost clears, and legacy stale gate references can recover by stop metadata.

## R217B · queue_boarding
Source line 25440

sequential routed stops now expose independent world drop zones for missing entrance/exit gates and retain stop-specific placement after each gate. Guests may leave paths only for explicit animated reasons: trash disposal, bird watching, picnic seating, or geocache inspection, then return to their anchor path.

## R218B · queue_boarding
Source line 25441

station entrance/exit drop zones are now truly clickable. Raycastable green/blue markers resolve their exact routed ride, stop index and access type; clicking a marker arms the canonical gate silhouette for that sequential stop, R rotates it, and the following ground click places the full-size gate.

## R223B · rides_attractions
Source line 25443

fixes ride-start requirements for routed rides. Tram/train/monorail now require at least two operational stations, each with entrance + exit + linked paths, and do not require a queue. Routed non-transport rides require one operational station. Normal attractions retain entrance + exit + queue rules. R218 route-builder core remains unchanged.

## R224B · paths_construction
Source line 25444

routed transport now selects stops based on the guest actual destination and continues the original journey after alighting. Adds Main Menu Park Map: zoomable/pannable bird-eye grid plotting paths, buildings, rides, stations, guests and all world entities, with live database search/filter and shared customerParkMapR224 dataset/API.

## R225B · guest_sim
Source line 25445

adds a full Geocaching Website under More with cache creation, micro/small/regular/large containers, searchable park cache DB, JSON/text/binary file attachments, Ollama Guest Flock staging, guest-interest cache search, logged finds, and a persistent log book.

## R226B · alexandria_geocache
Source line 25446

ducks synthesize a quack on click. Geocaches now maintain persistent item inventories; attached files are takeable cache items; guests can take and leave items during visits; the Geocaching Website includes a live object tracker; file items support editable operator lore.

## R227B · paths_construction
Source line 25447

geocache seed networks now randomize cache locations and micro/small/regular/large sizes across owned public-path regions. Manual construction and custom coaster/transport route control nodes are blocked beyond the purchased land boundary.

## R228B · rides_attractions
Source line 25488

active coaster/transport builders support plain mouse-wheel height adjustment, while Shift+wheel remains camera movement. Save snapshots now persist routed tram/train/monorail/flume structural route data and load them through a dedicated runtime constructor that rebuilds track, stations, curve, cars and ride metadata.

## R228G · ui_ux
Source line 25492

routed ride vehicles use a dedicated self-healing visual and animation pass. Missing/detached cars are rebuilt, cars are forced visible and initialized on the curve immediately, and started routed rides animate independently of generic ride-category animation filtering.

## R228H · rides_attractions
Source line 25493

transport service now initializes at Station 1, performs deterministic 3.2s boarding/alighting dwells, directly services passengers on arrival, uses wider station capture at speed, evaluates guest transport every few seconds instead of rare random chance, and Ride Manager exposes current rider inventory with locate/chat controls.

## R228I · persistence
Source line 25494

save/load now persists explicit world coordinates for every routed station stop and exact station entrance/exit gate coordinates. Station access gates have a dedicated restore constructor and are relinked to their exact ride/stop after import, with path-link recovery by proximity when path IDs change.

## R228J · rides_attractions
Source line 25495

all rides use physical queue lines. Routed tram/train/monorail stations now require a queue connected near each entrance; transport guests walk to the queue, occupy visible FIFO slots, advance in line, board only during station dwell when their turn reaches the front, and alight at their selected destination station exit.

## R228K · rides_attractions
Source line 25496

queue-demand fix. Guests now evaluate normal rides and transport on periodic clocks instead of tiny frame lotteries. Transport can generate an exploratory destination when a guest has no existing goal, candidate routing targets the real queue entry, and physical arrival tolerance advances guests into the queue even if currentPath metadata lags behind their position.

## R228L · guest_sim
Source line 25497

Park Pulse and the bottom mode/status glass now annunciate live world operations including park state, attendance, ride availability, queue load, transit riders/waiters, guest hunger/thirst/mood, cleanliness, cash, geocaching activity, busiest ride queues, boarding and station arrivals.

## R228M · paths_construction
Source line 25498

New Game now force-neutralizes every transient build tool before entering the park, including tree placement, ghosts, path painting, coaster/route builders and station access placement. Startup forest generation is explicitly boot-only and cannot be re-run by New Game.

## R228N · paths_construction
Source line 25499

adds Main Menu → Cheats → Tree Clear. The command cancels tree/build placement, removes resettable trees, and restores the canonical 58-tree startup forest seed while leaving paths, rides, buildings, and non-tree scenery untouched.

## R228O · queue_boarding
Source line 25500

rider/boarding ownership overhaul. Queue and transport states now exclusively own guest movement; transport boards throughout station dwell; normal rides dispatch waiting guests in capacity batches; open rides get deterministic queue demand; all riders follow the actual moving ride mechanism; and ride/station entrance-exit gatehouses use one compact canonical scale.

## R228Q · rides_attractions
Source line 25501

safe retry from R228O. R228P lifecycle transition machinery is not included. Fixes walking suppression by letting approaching/joining guests use normal movement, keeps transport dwell boarding from R228O, strengthens rider attachment, and uses compact static gates.

## R228R · performance_diagnostics
Source line 25502

fixes frozen guest walking animation. The crowd LOD system keeps full articulated people visible at LOD 1/2, but the walker previously animated limbs only at LOD 0. Walking limbs now animate at every visible LOD with 1x/1⁄2x/1⁄4x update frequency for performance, plus missing limb runtime references self-repair on demand.

## R228S · paths_construction
Source line 25503

standardizes normal and transport ride entrances/exits through one guest-proportional gate constructor sized once at placement/restore. Adds Custom Elevated Bridge to the build database and a dedicated Bridge Builder in Path Engineer with 0.5–16m height, wheel height control, freeplace/CTRL+SHIFT snap, SHIFT burst building, optional rails, supports and auto-ramp elevation constraints. R228R walking-animation LOD fix retained.

## R228T · rides_attractions
Source line 25504

transport passengers wait FIFO for the next vehicle dwell, reserve a stable physical seat index (two seats per car), and remain attached to that exact moving car-seat coordinate until their destination station. Adds a lightweight GPS Mind to every guest with an autonomous five-step park schedule spanning rides, transport, food, drinks, restrooms, geocaches, scenery, rest and exploration; scheduling feeds existing navigation systems rather than creating a second movement engine.

## R228U · guest_sim
Source line 25505

Park Pulse guest thoughts now draw from a broader contextual palette including needs, queues, transport, rides, GPS plans, pets, relationships, Alexandria readings, wildlife, ruins and exploration. Every two real-time minutes a random Alexandria topic is sent to the selected local Ollama model for a concise Park Pulse reading, with deterministic offline fallback. Guest entity chat/status now displays the full GPS Mind itinerary and Ollama guest chat receives that schedule as persona context.

## R228V · guest_sim
Source line 25506

guest hover now exposes a live Doing Now section, mood/needs/location, GPS current+next task, compact inventory contents, geocache hunt state, logged finds, latest carried Alexandria cache reading, recent Alexandria topic IDs/titles, wallet and current thought. Camera Mode 5 hover banner uses the same telemetry source.

## R228W · guest_sim
Source line 25507

replaces generic GPS schedules with a queued Ollama itinerary planner. Each prompt includes live guest health needs, interests, mood, wallet, thrill target, location, geocache history, park time and up to 70 reachable named park entities. Ollama returns strict JSON with five real destination IDs and human reasons. Local planning remains as an immediate/offline fallback; generic "explore park area" is avoided whenever named reachable destinations exist. Guest panel includes planner source/state and manual GPS replan.

## R228X · rides_attractions
Source line 25508

fixes queue admission root cause. Transport guests are now authorized users of queue paths, preventing the generic path guard from ejecting them when they reach a station. Queue-entry tolerance is widened and near-tile route failures recover instead of cancelling. Riding now uses an explicit temporary rider proxy: the walking avatar is hidden, a cloned articulated guest is drawn at the exact ride/car seat coordinate every frame, the hidden authoritative guest coordinate follows it, then the proxy is removed and the walking avatar is restored at exit.

## R228Y · ui_ux
Source line 25509

Escape menu is now a true keyboard toggle. Press Escape once to open the main escape menu and press Escape again to close it and return to the park. Text-entry controls retain their Escape guard.

## R229A · rides_attractions
Source line 25510

transport now uses explicit station event flags. Arrival opens BOARDING at one station epoch; queue guests physically near their assigned slot become QUEUE_LOCKED and stop oscillating. When the train is present, waiting guests receive BOARD_GRANTED, are removed from the queue, reserve a seat, hide their walking avatar and attach the rider proxy. Departure sets DEPARTED; every station sets ARRIVED; destination stations set ALIGHT_GRANTED and restore the walking avatar at the exit.

## R229B · rides_attractions
Source line 25511

queues are now true single-file formations with two guests per 2m queue slab and ~0.82m spacing. FIFO order is re-indexed every update so duplicate/stale slots cannot stack guests. Both normal and transport queues proximity-lock guests into reserved positions to prevent meet-point bouncing. While riding, the walking avatar always disappears; the temporary articulated rider proxy is only shown after a valid chair/seat coordinate is available, otherwise the rider remains hidden rather than floating beside the attraction.

## R229C · rides_attractions
Source line 25512

transport rider visuals are now tucked into the actual vehicle box. Tram/train/monorail cars include recessed seat cushions and backs; seat anchor Y is lowered below the car lip, transportation rider proxies use a compact seated scale, and legs tuck farther into the car. Normal thrill-ride rider scale is unchanged.

## R229D · rides_attractions
Source line 25513

fixes Log Flume and other single-station routed thrill rides being trapped at their load station. Station capture is now armed/disarmed: after loading, the vehicle must clear the station zone before that station can be detected again, preventing an endless dwell-recapture loop. Log Flume starts once at its platform, pauses briefly for loading, then runs the full circuit before returning.

## R229F · paths_construction
Source line 25514

adds a node-based Custom Elevated Path Engineer modeled after the coaster builder. Camera 1 orbits; cameras 2–5 place 3D control nodes; mouse wheel sets each next node height from 0–24m; Build Path interpolates a continuous walkable elevated route with optional rails/supports and optional grid snap. Path duplicate and graph logic are now height-aware, allowing true overpasses and underpasses without accidentally connecting elevated and ground paths.

## R229J · rides_attractions
Source line 25515

rebased directly from R229F with only three targeted changes: routed non-transport rides such as Log Flume board only during physical station dwell and unload only on a later station-arrival event; Custom Path Engineer can choose normal path textures directly through Building Manager; geocache spontaneous discovery/revisits are less frequent and logbook signatures are varied first-person guest notes.

## R229K · paths_construction
Source line 25516

UI bootstrap root-cause repair. R229J referenced customPathBuilderStateR229F inside renderBuildCatalogR10 before that const was initialized; the initial renderBuildCatalogR10 call therefore hit JavaScript temporal-dead-zone semantics and could abort module initialization, making the UI appear locked. Catalog highlighting now reads a safe global state bridge. Custom path preview GPU resources are also disposed when rebuilt to prevent accumulated preview memory churn.

## R229L · economy_research
Source line 25517

adds a subtle procedural cash-register cha-ching to the existing ambient SFX bus for monetary economy-ledger transactions. The ledger is hooked centrally so builds, sales, refunds, payroll, ATM movements, research spending and other money events are covered without duplicating handlers. Retail COGS entries are intentionally silent because the paired income entry already represents the same customer transaction. Ambience toggle controls the sound.

## R229M · rides_attractions
Source line 25518

right-click inspects guests and placed entities in camera modes when no build/cancel tool owns the click. Log Flume routed rider anchors are lowered to 0.17m with compact 0.40 rider proxies and deeper leg tuck so riders sit inside the raft hull. Ride Manager Dispatch Seconds is now the authoritative boarding/loading wait: normal rides wait before dispatching a batch and routed rides hold physically at stations for the configured dispatch duration before leaving.

## R229N · paths_construction
Source line 25519

fixes right-click inspection specifically in Orbit mode. The R229M listener ran in bubble phase after OrbitControls had already preventDefaulted contextmenu, so the inspector returned early. The inspector now runs in capture phase before OrbitControls, uses the existing contextual raycast for guests/objects, adds a path fallback, and still yields to active placement/cancel tools.

## R229O · rides_attractions
Source line 25520

transport queue demand fairness/root-cause fix. The route seeder previously looped over a specific tram/train/monorail but called the global transport chooser, so guests could be claimed by a different route and leave other transport lines empty. GPS transport tasks also ignored their selected transport entity. The chooser now accepts a preferred route; per-ride seeding and GPS honor it, spontaneous selection includes a load-balancing penalty, and seeding sorts guests by the nearest operational station.

## R229P · rides_attractions
Source line 25521

system-wide rider-fit audit. Static rides are measured and, only when undersized, enlarged once to a ride-type minimum footprint; routed rides/custom coasters keep their authored world scale. All boarded guests immediately enter the animated rider-proxy lifecycle and generic ride seats use wider spaced rows. Ride and station entrances/exits are now fixed-size 1.55m guest-scale geometry at transform scale 1.0; placement and save/load explicitly re-lock that scale so gates cannot grow after placement.

## R229Q · ui_ux
Source line 25522

fixes Custom Path Engineer discoverability in Build Manager. Root cause: the engineer existed as a Path Engineer button only, while Build Manager renders strictly from catalogR10; no custompath catalog record or click route existed. A first-class Custom Elevated Path Engineer entry now appears under Paths in both the main Build Manager and independent Build Database windows and opens the existing R229F engineer.

## R229R · performance_diagnostics
Source line 25523

adds persistent Lo-Def performance mode under More and hotkey 6. Low-def reduces WebGL pixel ratio, disables shadows, uses more aggressive guest LOD, halves full path enforcement, throttles pet/bird/decorative animations, reduces marquee/clock update frequency, cuts background guest logic budget and slows hidden-manager UI refresh. Simulation state, queues, rides, transport, saves and gameplay remain active.

## R229S · paths_construction
Source line 25524

removes the redundant legacy Bridge Builder UI and consolidates elevated path construction into Custom Path Engineer. Legacy bridgepath objects remain load-compatible. Custom Path Engineer now defaults to Asphalt Path, has a one-click Asphalt texture button, excludes legacy bridgepath from texture choices, and normal Asphalt remains independently selectable from Build Manager when the custom engineer is not active.

## R229T · paths_construction
Source line 25525

elevated path traversal + stronger transport demand. Guests now follow path Y while walking, snap to elevated path height on arrival/recovery, custom elevated path sampling is denser, and adjacent custom ramp pieces can connect across up to 1.15m vertical steps while true overpasses remain separated. Transport checks are more frequent, exploratory acceptance rises to 82%, route benefit discounts riding versus walking, per-route seeding can add two guests at once, and long wander decisions give transit first refusal.

## R229U · staff_ops
Source line 25526

handyman/staff visual overhaul. Newly hired handymen use a full adult-height articulated human model (~1.72m) with head, torso, arms, legs, boots, cap, work-vest accents and broom. Staff now face travel direction, walk with alternating limb animation, follow elevated path Y, and handymen animate sweeping/cleaning/mowing plus empty-bin/watering motions based on their current task.

## R229W · ui_ux
Source line 25527

handymen are now conversational staff entities with first-person operational opinions, persistent-in-session chat, and a dedicated duties window. Handymen can be opened from Staff Manager or right-clicked in the world. Guest, object and handyman entity windows receive an embedded live entity camera. The live camera uses one shared throttled secondary WebGL renderer that follows the currently opened entity rather than creating expensive renderers per panel.

## R229X · queue_boarding
Source line 25528

deep ride boarding root-cause fix + raised-path confinement. Normal rides previously chose the queue nearest the ride BODY rather than the queue touching their own entrance, so dense parks could make multiple rides claim the wrong queue and produce zero reachable riders. Queue ownership now resolves from each ride entrance first. Ride demand seeds only guests with a valid graph route to that queue entry. Walking avatars remain hidden while riding. Guests on paths above 0.32m cannot start/continue off-path excursions; path enforcement clamps X/Y/Z to the bridge corridor until they reach a ground-connected path or turn around.

## R229Y · camera_input
Source line 25529

Orbit-mode left-click is now camera navigation only. Root cause was a generic object pointerdown handler that excluded only Build mode, so mode 1 still opened object inspectors; the main non-build handler could also open Park/Land panels before guest mode checks. All left-click UI selection is suppressed in Orbit, including double-click recovery. Interact/Inspect modes retain left-click entity UI, and right-click inspection remains available in Orbit.

## R229Z · paths_construction
Source line 25530

replaces the old single Park Bench with Path Bench Pair furniture. Bench placement now requires a nearby walkable path, snaps to that path center/elevation, aligns to path direction, and creates two adult-scale benches on opposite walkway edges with four seats total. Paired benches are treated as integrated path furniture so guests can sit on them even on elevated paths without leaving the bridge deck.

## R230A · queue_boarding
Source line 25531

GPS ride invariant. Unless a guest is actively taking a rest/break, their GPS task queue is continuously repaired to contain a ride or transport entrance immediately followed by that ride’s proceeding exit. When operational transport exists, mandatory ride-pair generation chooses transport with a 50% probability; spontaneous transport acceptance is also 50%. Breaks temporarily exempt the invariant, and standing up immediately restores it. Path Bench Pair seat facings are corrected so opposite benches face each other across the walkway.

## R230B · guest_sim
Source line 25532

corrects Path Bench Pair orientation. The north/+Z bench now keeps its default front toward -Z/path center, the south/-Z bench rotates 180 degrees toward +Z/path center, and seated guest facings match those inward directions.

## R230C · guest_sim
Source line 25533

park closing evacuation root fix. Closing now cancels rides, transport, leisure, geocache and GPS intent; restores each guest walking avatar; routes every guest through the actual park entrance path using routeBetweenPathsR28; and removes the guest entity when it reaches the gate. The old code targeted the internal spawn coordinate (-12,14) and called nonexistent findPathRouteR28, so evacuation routes could silently fail. GPS ignores guests while they are leaving.

## R230D · rides_attractions
Source line 25534

Build-mode object pickup/move. Right-clicking a placed build object selects and lifts it instead of opening an inspector. The object follows the pointer; left-click places it, right-click or Escape cancels, and R rotates 90 degrees. Moving a ride carries separately placed linked ride/station access gates as one assembly. Path Bench Pair furniture re-snaps to a valid path and gate objects refresh their nearest path linkage. Protected park infrastructure cannot be moved.

## R230E · camera_input
Source line 25535

restores generic SHIFT rapid-build behavior. In Build mode, hold SHIFT + left mouse and drag while an ordinary catalog item is in hand to stamp repeated copies along the pointer path. Adaptive spacing and duplicate-cell guards prevent accidental piles. The selected material remains in hand after the stroke. Existing path burst painting, right-click object pickup/move, specialized coaster/route/custom-path builders and path-bench snapping remain separate and intact.

## R230F · persistence
Source line 25536

ordinary paths and queues are now centerline-drawn instead of square-tile placed. Left-click and drag draws a continuous ribbon from the navigation line guests actually follow; samples are inserted about every 0.5m so routing remains connected. Queue lines get narrower ribbons with side rails. The old square visual meshes are suppressed while navigation entities remain intact for pathfinding and save/load.

## R230G · ui_ux
Source line 25537

temporary nearest-queue diagnostic mode. Every eligible non-break guest without an active ride/transport trip is forced toward the closest reachable operational queue, including normal rides and transportation stations. A Ride Debug panel under More reports per-ride running state, queue linkage/capacity, reachable free guests, approaching/waiting/riding counts, transport station readiness, dispatch timers, assignment failures and recent force-routing events, with a copy-to-clipboard dump button.

## R230H · rides_attractions
Source line 25538

moves Ride Debug into a unified Settings window with General, Diagnostics and Docs tabs. Fixes rideEntrance/rideExit gatehouses being misclassified as attractions by isRideR27. Based on the supplied R230G dump, the transport failure boundary is narrowed to queue approach/entry handoff: Station 1 was operational and full (4/4 assigned) while all four guests remained approaching. Transport diagnostics now record distance-to-entry, route node count, route failures, approach duration, current path and target path; approach routes refresh every 2.5s without teleporting guests.

## R230I · flock_ai
Source line 25539

adds 26 free-roaming animated wildlife entities: deer, foxes, rabbits, raccoons, squirrels and ducks. Animals have simple articulated gait/body animations, autonomous roaming targets, species-specific temperaments and observations, right-click entity tracking, shared live entity camera, first-person Ollama chat with local fallback, and Park Map animal markers/search filtering.

## R230J · ui_ux
Source line 25540

cleans the main More menu by removing Lo-Def, Ambience, Entity DB and Map DB buttons. Those controls now live in Settings → General, with Settings remaining the single main-HUD gateway. Free-roaming wildlife heading is rotated 180 degrees so animals face the direction they travel instead of walking backward.

## R230K · queue_boarding
Source line 25541

fixes the transport queue approach root cause revealed by the supplied debug dump. The shared guest movement loop cleared targetPath after each route node, then chose a random wander target even when routeR28 still contained the remaining explicit route. Transport guests therefore advanced roughly one route node per periodic repair and could remain queueApproaching indefinitely. Explicit route nodes now outrank wandering, and reaching the queue-entry node immediately transitions to queueJoining.

## R230L · paths_construction
Source line 25542

ground-walking entities avoid water. Deer, foxes, rabbits, raccoons and squirrels reject water targets and turn away before entering; ducks/fowl may enter. Guest off-path excursions cannot target water, staff reject ground-level water path nodes, and guests reject ground-level water nodes while elevated bridges over water remain valid. Grid control moves from More into Settings → General. Park Value is now a live readout instead of a clickable button.

## R230M · queue_boarding
Source line 25543

orderly queue holding. Guests snap into unique FIFO queue slots once within 0.82m, then their world position is locked exactly to that slot every frame. Waiting animation only moves limbs, never X/Z, eliminating wall vibration and queue shuffling. Joining motion approaches the reserved slot center directly. Normal and transport queues share this behavior. Force Nearest Queue diagnostics default OFF.

## R230N · rides_attractions
Source line 25544

fixes transport alighting locality, persists workers, and adds wildlife population control. Transport riders now rematerialize only on the exit path belonging to the station where the vehicle is physically stopped, with a 0.9s exit hold that blocks stale onward routing/teleporting. Saves now include staff role/name/position/path/task/duties/chat/opinion/shift time and restore workers without charging hire costs. Settings General adds a 0–80 wildlife population slider and persists its target.

## R230O · performance_diagnostics
Source line 25545

Phase 1 GPU acceleration. WebGL requests high-performance GPU preference. Far trees switch from individual scene hierarchies to two THREE.InstancedMesh batches (trunks + crowns), reducing far-forest draw calls. Guest and wildlife articulated limb animation is distance-throttled at 1/3/8-frame cadence while simulation movement remains authoritative. Settings Diagnostics adds live renderer/GPU telemetry for FPS, draw calls, triangles, textures, geometries, WebGL capabilities and far-tree instance count. Exact VRAM bytes are not exposed by WebGL.

## R230P · ui_ux
Source line 25546

Settings is now directly available from the Escape/Pause menu. Pause → Settings opens the same General/Diagnostics/Docs workspace, temporarily hides the pause overlay, and closing Settings or pressing Escape returns to Pause. Settings opened from the main HUD still closes directly back to the park. R230O GPU acceleration remains intact.

## R230Q · environment
Source line 25547

GPU Phase 2. Far guests are rendered through one InstancedMesh crowd batch instead of full articulated child hierarchies. Far wildlife is rendered through one InstancedMesh per species. Original entity simulation/state remains authoritative, and right-click raycasts on GPU instances map back to the real guest/animal entity. Adaptive resolution adjusts renderer pixel ratio using measured FPS. R230P pause-menu Settings and R230O tree batching remain intact.

## R230R · queue_boarding
Source line 25548

fixes queue jitter and normal-ride starvation. Queue slots are no longer compacted/re-numbered every update. Once a normal or transport guest reaches waiting state, the assigned slot remains immutable and owns the guest transform until boarding, eliminating back/forth movement as other guests board. Every operational non-transport ride entrance now independently attracts reachable guests every 1.3 seconds toward a target queue occupancy of about 55% capacity, while individual ride selection favors queue-starved attractions instead of transport dominating demand.

## R230S · queue_boarding
Source line 25549

park-closing evacuation now understands disconnected path components connected only by transport rides. Guests first try a normal walking route to the park entrance. If none exists, the evacuation planner finds a reachable operational transport station on the guest side and a destination station whose exit path has a walking route to the park entrance. The guest queues, rides across, alights at that station exit, and then resumes walking evacuation. The evacuation updater does not overwrite an active emergency transport trip.

## R230T · ui_ux
Source line 25550

entity hover is information-only. Pointer movement over wildlife, workers, guests or objects may update the context glass, but it never opens entity UI panels. Animal/staff windows and other entity inspectors now require an explicit right-click inspection gesture.

## R230U · performance_diagnostics
Source line 25551

Performance Phase 3. Adds an adaptive CPU performance governor driven by measured FPS; caches ride/routed-ride/fountain/water/decor hot object sets; removes duplicate rider-proxy synchronization passes; adaptively throttles decorative water/fountain/catalog animation and noncritical guest maintenance; reduces crowd/wildlife GPU instance-buffer update frequency under pressure; renders entity live cameras only while visible; and permits a lower adaptive-resolution floor under heavy load. Core locomotion, queues, boarding, ride movement and economy remain full-authority.

## R230V · performance_diagnostics
Source line 25552

Draw-call collapse pass based on supplied 2 FPS / 2116 calls / 138,528 triangles / 2,178 geometries telemetry. Derived path ribbons, queue rails and queue guides are converted from individual BoxGeometry meshes into material-grouped InstancedMesh batches, and the original per-piece geometries are disposed. Queue rail/guide visuals now use topology signatures so they are not destroyed and rebuilt every 450ms when unchanged. Auto Shadow Governor disables shadow rendering below 44 FPS and only restores after sustained >55 FPS recovery. Navigation and queue simulation remain unchanged.

## R230W · performance_diagnostics
Source line 25553

profiling/test build following R230V draw-call collapse. Adds a repeatable 12-second performance benchmark under Settings → Diagnostics → GPU / Renderer. Samples FPS, render calls, triangle count and adaptive pixel ratio every 500ms, then reports average/min/p10/median/max FPS and renderer averages. A scene-cost profiler groups visible meshes, unique geometries and materials by rides, paths, queues, guests, wildlife, workers, trees, scenery, water and GPU batches to identify the next remaining bottleneck.

## R230X · performance_diagnostics
Source line 25554

benchmark-directed mesh collapse. R230W measured 2.02 FPS, 2,146 draw calls, 8,395 visible meshes, 8,384 unique geometries, and 6,612 unique materials. Dominant categories were otherScene (5,992 meshes) and trees (1,356 meshes). R230X converts decorative frontier trees/rocks into at most four shared InstancedMesh draw calls and hides their original multi-mesh hierarchies. Park-tree full-detail radius drops from 34m to 18m.

## R230Y · paths_construction
Source line 25555

static terrain/path optimization. Ground transform matrices no longer update during simulation. Path node transforms and children are frozen between edit operations; the nodes remain lightweight navigation/snap/bridge records. Base path deck meshes are hidden and replaced with material-grouped InstancedMesh batches. Path topology/corner/queue adjacency recalculates only when the player builds, rotates, moves, or constructs elevated/custom paths, not continuously.

## R230Z · performance_diagnostics
Source line 25556

CPU hot-path optimization based on the R230Y benchmark. Draw calls had already fallen from 2,146 to ~407 while FPS remained ~2.14, proving GPU submission was no longer the primary limiter. Path adjacency is now cached and rebuilt only after path edits; routeBetweenPaths uses cached neighbors and an index-based BFS queue; blocked paths are cached instead of scanning objects per edge; water footprints are cached instead of traversing the 5,900+ frontier scene on every point-in-water test. Static path batching is fixed for path nodes that are Mesh roots.

## R231A · performance_diagnostics
Source line 25557

CPU phase profiling build. Empty-map benchmark with camera motion averaged 44.45 FPS at 114 draw calls, while the populated park previously remained near 2 FPS after draw-call collapse. Adds a 10-second profiler for guest movement, transport, queues, workers, economy, needs/background logic, GPS, frontier, wildlife, ride animation, GPU instance updates, renderer.render, and entity live camera work. This identifies the actual JS hot subsystem in the populated save.

## R231B · ui_ux
Source line 25558

interaction-safe CPU hot-path pass. INTERACT/INSPECT left-click and right-click on guests/workers now follow the selected entity and open its entity panel. All worker roles can open the worker entity panel. Guest and worker panels continue attaching the embedded live entity camera. Hover remains non-opening. CPU changes include 750ms ride-access economy maintenance, staggered ambient guest decisions, cached transport availability, and cached carryable hierarchy lookup.

## R231C · environment
Source line 25559

Distance-based render reduction is now an optional Settings feature and defaults OFF. When OFF, full-detail park trees, guests and wildlife remain rendered regardless of distance; static navigation/path batching and other non-visual CPU optimizations remain active. Object Inspector now contains an embedded live camera feed targeting the selected object, and the main live-camera update gate includes the Object Inspector.

## R231D · staff_ops
Source line 25560

entity camera singleton cleanup. Object Inspector no longer creates a second dynamic camera mount inside its body; it uses only the canonical static entityCamMountObjectR229W mount. attachEntityLiveCameraR229W now enforces at most one .entityLiveCamR229W wrapper/canvas per entity page and clears stale duplicate mounts from older renders. Guest, worker, wildlife and object pages retain live camera feeds.

## R231E · flock_ai
Source line 25561

Guest Flock Studio gains an optional GPT Knowledge Broker, OFF by default. GPT uses the OpenAI Responses API to create workflow direction, knowledge briefs, per-role directives, acceptance checks and risk notes that are injected into the local Ollama Scout/Shepherd/Planner/Builder/Reviewer/Archivist prompts. Default OpenAI model is gpt-5.6-luna, with Terra and Sol selectable. Direct mode accepts an API key into module-scoped session memory only; the password input is immediately cleared and the key is never stored in localStorage, save data, project files, exports, transcripts or diagnostics. Local Relay mode is available for stronger server-side key isolation. Broker errors do not block the local Ollama workflow.

## R231G · camera_input
Source line 25562

wildlife receives the same rich pointer-hover treatment as guests. Hovering an animal now shows its species icon/name, coordinates, current activity, temperament, nearby guest count, habitat, distance from home range and current thought without opening a panel. Right-click inspection now has an explicit normal-wildlife raycast in addition to GPU-instance mapping, so Orbit mode reliably opens the wildlife entity window and live camera whether distance render reduction is on or off.

## R231I · camera_input
Source line 25563

guest entity windows replace the generic auto-spinning live camera with an interactive Guest Observer. The replacement reuses the shared secondary renderer for performance but adds Orbit, Follow, Face and first-person POV modes, drag orbiting, wheel zoom, a live mode/target readout and POV crosshair. Wildlife, worker and object cameras remain unchanged.

## R231J · flock_ai
Source line 25564

Guest Flock chat transcript is left anchored and left aligned across ordinary responses and fenced code while preserving selectable themed text and Copy/Preview controls.

## R231K · rides_attractions
Source line 25394

repairs Custom Coaster finalization. Commission cost/affordability is now shown inside the coaster panel instead of only in the globally hidden status line; BUILD RIDE uses a guarded off-scene geometry phase followed by an atomic scene/entity commit; successful rides force the attraction/performance caches to refresh, initialize their train immediately, and use the authoritative buildSpend economy transaction. registerEntityR36 also no longer returns before its refresh hooks.

## R231L · paths_construction
Source line 25565

restores CTRL+left-click demolition priority. A capture-phase bulldozer guard now runs before specialized construction/inspection handlers that can stopImmediatePropagation. Plain CTRL+click demolishes again even while Custom Path, Custom Coaster, route/station builders, grabber, or Inspect mode are active; CTRL+SHIFT on a normal path remains reserved for snapped path construction.

## R231M · rides_attractions
Source line 25395

custom coasters now use persistent selectable skins, physically dwell at their loading station for FIFO queue boarding, launch only after the dispatch timer seats riders, complete exactly one circuit, return and unload before the next train. Guest-demand seeding gives custom coasters a stronger visible queue target. Save/load now excludes live coaster car Object3D arrays, writes an explicit compact customCoaster record, and reconstructs track/station/train geometry through the same constructor used by BUILD RIDE.

## R231P · flock_ai
Source line 25566

reverted the R231O mobility experiment to the stable R231N camera/control baseline. Adds a complete persistent Ollama/GPT Flock conversation browser backed by IndexedDB with search, speaker/run filters, pagination, copy and JSON export. Existing retained turns/tasks migrate into the archive. Park Map is redrawn as a live colored paper map with parchment terrain, colored path/queue ink, coaster routes, water washes and cartographic markers. No camera/control-loop handlers are changed.

## R231Q · rides_attractions
Source line 25486

ride visibility authority fix. The bottom ride count, Attraction Manager, guest GPS, queue-demand scheduler and transport selection now share one operational/readiness predicate. Legacy running flags are repaired from authoritative commerce state, the old attraction renderer delegates to the canonical manager, and services no longer masquerade as rides in the manager. rideVisibilityAuditR231Q() exposes per-ride guest visibility reasons.

## R231R · paths_construction
Source line 25567

fixes three live-simulation regressions without changing the main camera control loop. Guest Observer now owns a dedicated throttled secondary renderer so object/wildlife/worker camera attachments cannot steal its canvas; it targets visible rider proxies when present and temporarily reveals LOD-hidden guest visuals only for the secondary render. GPS ordinary destinations complete on the exact movement frame they are reached, closing the 1Hz scheduler gap that could pull guests back and forth across the same path tile, and New Game clears stale GPS planner jobs. CTRL+click demolition now resolves the highest registered object/path root across every ray hit instead of stopping on entity-tagged child meshes. Normal object, rapid-build and path placement now charge ITEMS catalog cost through the authoritative economy ledger and show the existing red spend popup; routed rides use that same ledger too.

## R231S · rides_attractions
Source line 25570

queue authority hardening. Guests walk only to the outer queue entrance; once inside a normal or transport queue they are mapped by FIFO order to unique contiguous three-per-tile world slots and hard-frozen with no idle/walk animation, eliminating competing walker ownership, slot collisions and visible queue jitter. Queue geometry now guarantees distinct center spacing on straight segments and bends. Rich entity hover now reports live riders/capacity for rides and live waiting occupancy/capacity for queue lines, including connected ride/station ownership. Diagnostics: queueFreezeAuditR231S() and rideQueueHoverAuditR231S().

## R231T · rides_attractions
Source line 25571

Attraction Manager DB actions now use side-effect-free entity lookup and click-phase inspector mounting; entity registration refreshes only on first registration. Waiting queue guests are excluded from far-crowd LOD batching and forced fully visible to eliminate queue blinking.

## R231U · rides_attractions
Source line 25581

transport performance hotfix. Transport route planning is removed from the guest walker, capped to one or two guests per frame, route/station readiness work is short-lived cached, demand seeding only requests future planning, and routed-ride scans reuse the performance object cache. This directly targets transport_trips and the transport work formerly leaking into guest_movement_loop.

## R231V · paths_construction
Source line 25582

path realism pass. Construction grid is offset by half a 2m cell so its lines represent cell boundaries and line up with the edges around the starter pavement. Standard paths are 1.44m wide and queues 0.96m wide rather than filling a full 2m square. R230F root-mesh suppression is corrected so square path bases no longer remain visible beneath centerline ribbons. Default asphalt uses a shared procedural aggregate/crack texture, and queue snake rails stay constrained to the narrow lane instead of rebuilding a full-tile perimeter.

## R231W · frontieros_comms
Source line 20792

Jamendo lookup now explicitly includes both singles and album tracks with direct-fetch plus JSONP fallback, and resolved music metadata is written into nearby guest music memory/neural context. Main PA linked speakers mirror one synchronized program at every physical speaker location. Adds $320 pole-mounted Wi-Fi access points with green/blue/red status lights, persistent configurable park SSIDs, a colored in-world hotspot coverage overlay, guest phone Wi-Fi state, a guest-visible FrontierOS phone with Browser/Messages/Map/Music/Wi-Fi/Ollama Park AI apps, and $240 continuously panning security cameras. Park Wi-Fi definitions are included in park saves.

## R231X · guest_sim
Source line 25569

removes guest-owned/follower animal coupling. All visible animals are independent world entities with individual temperament/personality, bounded autonomous roaming and first-person Ollama animal identity. Geocache Object Inspector now exposes cache inventory plus a guest-linked interaction ledger with each visitor's current or persisted inventory snapshot and signed log entries; live visitors can be opened directly.

## R231Y · frontieros_comms
Source line 25568

every guest has a persistent Frontier Phone inventory device with Wi-Fi/cellular Internet bearer, direct OPEN OS launch, and the rotation HUD heals its deleted value node so it cannot remain stuck visible after move/placement tools.

## R231Z · environment
Source line 20793

lighting realism adds real performance-budgeted local PointLights to lamp posts and luminous scenery plus four programmable lighting/spectacle objects with color, brightness, frequency, waveform and night automation controls. Community dogs/cats are independently guaranteed within wildlife populations instead of guest-owned pets. Queue ownership now purges stale far-crowd GPU instances immediately when a guest joins a line, preventing duplicate transparent blinking. Every guest owns a persistent individual brain with personal memory/knowledge, autonomous phone research and social sharing, guest-to-guest messaging, and FrontierOS Research/People/My Mind apps backed by the existing Ollama connection.

## R232A · ui_ux
Source line 20794

adds a persistent 📱 OS button to the primary HUD registered to Park Manager. It opens a dedicated FrontierOS Manager Edition handset, separate from guest identities, with live Dashboard, Guests, Attractions, Park Map, Wi-Fi, Main PA, Guest Flock, Settings and Ollama-backed Park AI launchers. Park Manager panel also exposes the registered device.

## R232B · frontieros_comms
Source line 20795

FrontierOS now renders the actual live paper park map inside both guest and Park Manager phones. Adds a searchable geocaching phone client with live cache locations and manual guest GPS targeting. Fixes programmable light color fidelity by recoloring each fixture's own cloned luminous materials, and makes nights substantially darker by reducing hemisphere fill, sun intensity and exposure so local lamps matter.

## R232C · frontieros_comms
Source line 25583

fixes blank Park Manager FrontierOS by correcting the SSID registry reference and adds persistent drag positioning. Guest phone texts are surfaced as an all-conversation message database in FrontierOS and in each guest entity database; guest-to-guest traffic periodically appears in Park Pulse. Park Pulse now continuously rotates through live ride, queue, guest, network, audio, wildlife, geocache, lighting, economy, social, research and operations topics. Night ambient floor is raised slightly from R232B while real local lights receive stronger output, longer practical reach and gentler falloff.

## R232D · environment
Source line 25274

park clock now runs one full day every 20 real minutes at 1x, with a 21:00-03:00 six-game-hour night lasting about 5 real minutes; automatic lamps follow the same night window.

## R232E · ui_ux
Source line 20796

wildlife entity explorer now mirrors the complete rich hover telemetry, including live activity, species, temperament, nearby guests, home distance, habitat, movement rate, coordinates, home range and current thought. The status block refreshes while the animal roams without altering the main camera/control loop.

## R232F · environment
Source line 25585

fixes Jumping Fountain self-animation by routing the catalog/save key jumpfountain into the existing R177 ballistic fountain constructor; removes the earlier static branch that intercepted it. Also removes the duplicate legacy speaker constructor so the updated weatherproof pole speaker model is authoritative.

## R232G · audio_media
Source line 25273

speaker online media adds Jamendo + Radio Browser provider selection, Jamendo singles/audio URL playback repair, generic local/PA media routing, and geocaches gain varied physical container shapes plus surface-aware adjustable-height placement.

## R232H · audio_media
Source line 20797

music playback gate repair. Direct URL playback no longer forces CORS mode; explicit Play URL controls report media errors; Jamendo Use Track and Radio Browser station selection attempt immediate local playback under the user's click gesture.

## R232I · ui_ux
Source line 25698

all child panels/dialogs and both FrontierOS handsets share universal drag, close and z-order behavior. Backspace discovers the actual top child dynamically, and the physical mouse Browser-Back button closes that same child. Future dynamically created child windows inherit the behavior automatically.

## R232J · audio_media
Source line 25752

guest phone messaging now reads authoritative inbox/outbox records and bootstraps two-way park introductions so guests do not sit at 0 sent / 0 received for minutes. Social autonomy checks are budgeted across several guests per tick. Speaker testing now has an inspector monitor that overrides distance attenuation only while the selected speaker inspector is open, Radio Browser prefers HTTPS non-HLS browser-playable stations, and media status reports actual playing/paused/local-field state instead of the misleading generic continues-unfocused label.

## R232K · audio_media
Source line 25754

adds a dedicated Synthwave Radio provider with ten curated preset streams: Nightride FM, ChillSynth FM, Datawave FM, SpaceSynth FM, DarkSynth, HorrorSynth, Synthwave City FM, SynthZone, Record Synthwave, and Nightwave Plaza. Presets use the existing persistent local-speaker and Main PA audio pipeline and retain station metadata for nearby guest minds.

## R232L · audio_media
Source line 25755

Main PA now owns its own provider/program selection instead of receiving media pushed from a speaker. Linked speakers subscribe to that program and may be individually switched to a persistent Local Override. Festival Banners expose per-entity cloth color and Rectangle/Pennant/Swallowtail/Vertical shape controls.

## R232M · paths_construction
Source line 25757

park Wi-Fi access points are now 4×4 MU-MIMO entities that can broadcast multiple SSIDs at once, expose per-AP SSID checkboxes, support temporary directional beamforming pushes to selected guest phones, visualize the beam, and publish every push to Park Pulse. Normal build tiles and ride-access placements snap to one-eighth of the 2m construction cell (0.25m) while paths retain their dedicated navigation/strict-snap rules.

## R232N · ui_ux
Source line 25758

every speaker entity inspector now has a 📢 Open Main PA button that opens and fronts the authoritative PA console directly from the speaker UI without changing link/override state.

## R232P · flock_ai
Source line 20798

Guest Flock is reworked as a persistent IDE-style workbench with a dense collapsible project explorer, multiple editor tabs, dirty-state tracking, quick-open, full-project search, grouped conversation sessions, archived-run resume, file-to-agent context linking, conversation-to-file references, drag-to-move tree nodes, right-click file actions, and persistent linked-context priority in Ollama/GPT project prompts.

## R233A · ui_ux
Source line 26136

Guest Flock removes the permanent left activity rail and fixed workbench sidebar. Files/Search/Conversations are on-demand drawers; the project tree uses a compact VS Code/Nemo/Sublime-style editor presentation; Code and Preview are explicit workspace modes; grouped conversations have real per-session IndexedDB deletion; existing project/editor/context/agent behavior is preserved.

## R233B · rides_attractions
Source line 26353

waiting guests now use a queue-owned stationary idle/facing animation completely separate from ride rider proxies, preventing Ferris queues from inheriting wheel motion. Security guards and entertainers now use the same rich worker inspector model as handymen with role-specific duties, opinions, Ollama chat, live camera, persistent FrontierOS Worker phones, and a dedicated Forest Frontiers Worker WPA3 SSID broadcast by park APs. Normal attractions expose brighter, closer green Entrance and blue Exit pickup/drop handles immediately after placement, and those handles remain clickable even while a build tool is still selected.

## R233C · rides_attractions
Source line 26642

Ferris riding clears queue ownership at boarding and uses a once-per-frame cabin-seat renderer, eliminating rider/queue double ownership and ghost copies. All programmable park lights are heavily suppressed by daylight and rise naturally after dusk; Wave Beacon defaults to a much slower 0.08 Hz soft sine. Alexandria devotes a large recurring slice of its 10,000 entries to programming, web development, Linux/Bash, Docker, Ansible, Node, Python, LLMs, Ollama, RAG, databases, APIs, DevOps, networking and agents. A park-level Flock Topic of the Day panel drives real live guest-to-guest learning/messages and shared memory. Security guards are a distinct profession: ATM service, crime prevention, camera hotspot awareness, GPS suspect pursuit, vandalism response, most-wanted tracking, ejection and persistent incident reporting; they never perform handyman cleanup. Orbit left-click follow and right-click entity Inspect are restored.

## R233D · guest_sim
Source line 26934

user-facing ride readiness terminology now says guest-ready instead of the misleading guest-visible. All non-routed attractions missing access receive the same large green/blue pickup sockets plus standing gatehouse hologram shortcuts, even when a build catalog tool remains selected. GPS rest tasks reserve a real bench/table seat and remain active through the walk-to-seat, link, seated-rest and stand-up animation before completing. Adds small/medium live wildlife food/habitat objects including clover, berry shrubs, seed scatter, insect/pollinator patches, mushrooms, pondweed and community bowls; wildlife develops hunger, seeks compatible food, eats visible resources and natural sources regrow.

## R233E · alexandria_geocache
Source line 27075

Alexandria technical curriculum is promoted from keyword/tag enrichment into a searchable relational-style knowledge database. Every requested technical topic record exposes a parent topics row plus populated concepts, workflow, diagnostics, related_topics, and request_more child tables with named columns and detailed rows. Alexandria search indexes nested table content, topic detail renders the schema and rows, and each record explains how to request deeper information with local row search, real Guest Flock follow-up, or Topic-of-the-Day handoff.

## R233F · flock_ai
Source line 27211

flock learning now records the actual lesson instead of generic 'learned something' thoughts. The existing periodic flock peer loop routes into a real guest-backed Ollama conversation engine. Active live flock guests rotate through three-turn peer discussions grounded in Topic of the Day, their persistent personal brains, and Alexandria relational rows; every turn is stored as real guest-to-guest phone/social traffic, concrete TAKEAWAY lessons are written into memory/knowledge/neural lessons/shared flock facts, and the park-level Flock Topic panel shows the latest transcript and exact learned content with a manual learning-round trigger. Alexandria-grounded fallback is used only when local Ollama is unavailable.

## R233G · flock_ai
Source line 27356

adds a persistent park-level Collective Flock Prompt distinct from one-run Studio tasks and Topic of the Day, and injects it into role-based Ollama agents plus automatic real-guest peer learning. Alexandria relational technical additions are now explicitly married to geocaching: every placed cache owns a deterministic 12-entry Alexandria shelf with guaranteed relational technical records, old caches migrate, technical cards retain authoritative database references, and the Geocaching Website exposes each cache shelf directly. Park Pulse now renders inline hotlinks for mentioned guests, workers, wildlife, objects/caches, and Alexandria topic IDs; each link opens the entity's native UI or Alexandria record.

## R233M · staff_ops
Source line 28372

in-module root fix for Staff Manager worker/security inspector and urgent guest facility routing. Later classic scripts cannot access the core module scope; this patch lives inside the authoritative module.