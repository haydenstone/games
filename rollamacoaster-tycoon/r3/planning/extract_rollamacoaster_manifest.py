from pathlib import Path
import re, json, html, hashlib, bisect, csv
from collections import Counter, defaultdict

OLD=Path('/mnt/data/rollamacoasterTycoon_R233M_playtest_guard_needs_root_fix(2).html')
R3=Path('/mnt/data/index(20260828-190842).html')
NOTES=Path('/mnt/data/rollamacoasterTycoon_R3_REBUILD_NOTES(1).md')
BUILDER=Path('/mnt/data/build_rct_r3(1).py')
OUT=Path('/mnt/data')
old=OLD.read_text(errors='replace')
r3=R3.read_text(errors='replace')
notes_text=NOTES.read_text(errors='replace')

# line mapping
line_starts=[0]
for m in re.finditer('\n',old): line_starts.append(m.end())
def line_no(pos): return bisect.bisect_right(line_starts,pos)

def clean_text(x):
    x=re.sub(r'<[^>]+>',' ',x)
    x=html.unescape(x)
    return re.sub(r'\s+',' ',x).strip()

def rev_from_name(s):
    ms=list(re.finditer(r'R(\d{1,3})([A-Z]{0,2})',s or ''))
    return ('R'+ms[-1].group(1)+ms[-1].group(2)) if ms else None

CATEGORY_RULES=[
('persistence',['save','load','import','export','indexeddb','localstorage','snapshot','migration','project']),
('flock_ai',['flock','ollama','openai','gpt','agent','broker','conversation','chat','prompt','neural','peer']),
('alexandria_geocache',['alexandria','geocache','cache','knowledge','curriculum','library']),
('frontieros_comms',['frontieros','phone','wifi','wi-fi','ssid','message','internet','browser','cellular']),
('audio_media',['speaker','audio','music','jamendo','radio','youtube','pa ','synthwave','media','track']),
('rides_attractions',['ride','coaster','ferris','wheel','carousel','tower','tram','train','monorail','rapids','attraction','rider','station']),
('queue_boarding',['queue','boarding','seat','fifo','entrance','exit','drop zone']),
('paths_construction',['path','grid','build','placement','bulldoz','rotation','bridge','terrain','construction']),
('guest_sim',['guest','need','hunger','thirst','bathroom','nausea','mood','thought','wallet','inventory','balloon','bench','rest']),
('staff_ops',['staff','handyman','security','worker','entertainer','mechanic','duty','mow','trash']),
('economy_research',['economy','cash','revenue','ledger','price','stock','research','r&d','funding','cost','wage','park value']),
('environment',['wildlife','animal','tree','grass','water','pond','fountain','lighting','lamp','scenery','weather','night']),
('ui_ux',['ui','panel','window','hover','hud','tooltip','drawer','sidebar','explorer','editor','preview','button','menu','glass','title']),
('performance_diagnostics',['performance','fps','benchmark','diagnostic','lod','draw call','geometry','material','throttle','budget','audit']),
('camera_input',['camera','orbit','interact','pointer','mouse','keyboard','ctrl','shift','backspace','raycast']),
]
def classify(text):
    t=(text or '').lower()
    scores=[]
    for cat,ks in CATEGORY_RULES:
        score=sum(1 for k in ks if k in t)
        if score: scores.append((score,cat))
    return max(scores)[1] if scores else 'core_misc'

atoms=[]
def add(kind,name,pos=None,description=None,revision=None,extra=None):
    revision=revision or rev_from_name(name) or rev_from_name(description or '')
    line=line_no(pos) if pos is not None else None
    txt=' '.join(x for x in [name,description] if x)
    atoms.append({
        'atom_id':f'A{len(atoms)+1:06d}','kind':kind,'name':name,'line':line,
        'revision':revision,'domain':classify(txt),'description':description or '',
        'extra':extra or {}
    })

# 1. Revision summary/meta descriptions
revision_summaries=[]
for m in re.finditer(r'<div[^>]*style=["\'][^"\']*display\s*:\s*none[^"\']*["\'][^>]*>(.*?)</div>',old,re.I|re.S):
    t=clean_text(m.group(1))
    mm=re.match(r'(R\d+[A-Z]{0,2})\s*:\s*(.*)',t)
    if not mm: continue
    rec={'revision':mm.group(1),'line':line_no(m.start()),'description':mm.group(2),'domain':classify(mm.group(2))}
    revision_summaries.append(rec)
    add('revision_meta_description',rec['revision'],m.start(),rec['description'],rec['revision'])
    # split into requirement clauses as semantic feature atoms
    desc=rec['description']
    # conservative split on semicolons/sentences plus list-style commas after verbs
    clauses=[c.strip(' .') for c in re.split(r'(?<=[.!?])\s+|;\s+',desc) if len(c.strip())>12]
    for i,c in enumerate(clauses,1):
        add('revision_requirement',f"{rec['revision']}#{i}",m.start(),c,rec['revision'])

# 2. Functions
for m in re.finditer(r'\bfunction\s+([A-Za-z_$][\w$]*)\s*\(',old):
    add('function',m.group(1),m.start())
# arrow-assigned named functions (dedupe by exact kind/name/line later unnecessary)
for m in re.finditer(r'\b(?:const|let|var)\s+([A-Za-z_$][\w$]*)\s*=\s*(?:async\s*)?\([^)]*\)\s*=>',old):
    add('arrow_function',m.group(1),m.start())

# 3. Declared symbols
for m in re.finditer(r'\b(?:const|let|var)\s+([A-Za-z_$][\w$]*)\b',old):
    add('implementation_symbol',m.group(1),m.start())

# 4. DOM ids
for m in re.finditer(r'\bid=["\']([^"\']+)["\']',old):
    add('dom_id',m.group(1),m.start())

# 5. classes, unique names with first occurrence
seen=set()
for m in re.finditer(r'\bclass=["\']([^"\']+)["\']',old):
    for c in m.group(1).split():
        if c not in seen:
            seen.add(c); add('css_class',c,m.start())

# 6. state keys
for pat,kind in [(r'userData\.([A-Za-z_$][\w$]*)','runtime_userdata_key'),(r'dataset\.([A-Za-z_$][\w$]*)','dataset_contract')]:
    seen=set()
    for m in re.finditer(pat,old):
        n=m.group(1)
        if n not in seen:
            seen.add(n); add(kind,n,m.start())
# persistence keys
seen=set()
for m in re.finditer(r'localStorage\.(?:getItem|setItem|removeItem)\(["\']([^"\']+)',old):
    n=m.group(1)
    if n not in seen: seen.add(n); add('persistence_key',n,m.start())

# 7. event bindings, preserve occurrences because each is a behavioral hook
for m in re.finditer(r'addEventListener\(["\']([^"\']+)',old):
    add('event_binding',m.group(1),m.start(),extra={'event':m.group(1)})

# 8. UI text contracts
for attr,kind in [('title','ui_tooltip'),('placeholder','ui_placeholder'),('aria-label','ui_accessibility_label')]:
    for m in re.finditer(r'\b'+re.escape(attr)+r'=["\']([^"\']+)["\']',old,re.I):
        txt=clean_text(m.group(1))
        if txt: add(kind,txt,m.start(),txt)
# static button labels
for m in re.finditer(r'<button\b[^>]*>(.*?)</button>',old,re.I|re.S):
    txt=clean_text(m.group(1))
    if txt and len(txt)<=160: add('ui_button_label',txt,m.start(),txt)

# 9. external service endpoints
seen=set()
for m in re.finditer(r'https?://[^\s"\'<>`]+',old):
    u=m.group(0)
    if u not in seen: seen.add(u); add('external_endpoint',u,m.start(),u)

# 10. audit contracts (separate semantic layer)
seen=set()
for m in re.finditer(r'\b([A-Za-z_$][\w$]*AuditR\w*)\s*=\s*',old):
    n=m.group(1)
    if n not in seen: seen.add(n); add('audit_contract',n,m.start(),f'Legacy executable parity/diagnostic hook {n}')

# Catalog extraction
catalog=[]
start=old.find('const catalogR10=')
end=old.find('let buildTopicR10',start)
if start>=0 and end>start:
    seg=old[start:end]
    for m in re.finditer(r'\[\s*"([^"]+)"\s*,\s*"([^"]*)"\s*,\s*"([^"]+)"\s*,\s*"([^"]*)"\s*\]',seg):
        key,icon,name,lore=m.groups(); pos=start+m.start()
        # category from nearest preceding top-level group label in segment
        before=seg[:m.start()]
        cats=list(re.finditer(r'\b(paths|food|facilities|scenery|rides)\s*:\s*\{label:',before))
        category=cats[-1].group(1) if cats else 'unknown'
        catalog.append({'key':key,'icon':icon,'name':name,'description':lore,'category':category,'line':line_no(pos)})
        add('build_catalog_item',key,pos,f'{name}: {lore}',extra={'name':name,'icon':icon,'category':category})

# ITEMS prices/types
items={}
start_i=old.find('const ITEMS={')
end_i=old.find('let objects=',start_i)
if start_i>=0 and end_i>start_i:
    seg=old[start_i:end_i]
    for m in re.finditer(r'([A-Za-z0-9_]+)\s*:\s*\[\s*"([^"]+)"\s*,\s*([0-9.]+)\s*,\s*"([^"]+)"\s*\]',seg):
        key,name,price,typ=m.groups(); items[key]={'name':name,'price':float(price),'type':typ,'line':line_no(start_i+m.start())}
for c in catalog:
    if c['key'] in items: c.update({'price':items[c['key']]['price'],'entity_type':items[c['key']]['type']})

# BUILD_META_R114 descriptions
build_meta=[]
start_m=old.find('const BUILD_META_R114={')
end_m=old.find('};',start_m)
if start_m>=0 and end_m>start_m:
    seg=old[start_m:end_m+2]
    for m in re.finditer(r'([A-Za-z0-9_]+)\s*:\s*\[\s*"([^"]*)"\s*,\s*"([^"]*)"\s*,\s*"([^"]*)"\s*\]',seg):
        key,icon,code,desc=m.groups(); pos=start_m+m.start()
        build_meta.append({'key':key,'icon':icon,'code':code,'description':desc,'line':line_no(pos)})
        add('build_meta_description',key,pos,desc,extra={'icon':icon,'code':code})

# R3 clean-core catalog extraction for parity surface comparison
r3_catalog=[]
r3_start=r3.find('const CATALOG=')
r3_end=r3.find('const ITEM_BY_KIND',r3_start)
if r3_start>=0 and r3_end>r3_start:
    rseg=r3[r3_start:r3_end]
    for m in re.finditer(r'\["([^"]+)","([^"]+)",([0-9.]+),"([^"]*)","([^"]*)"\]',rseg):
        key,name,price,icon,lore=m.groups()
        r3_catalog.append({'key':key,'name':name,'price':float(price),'icon':icon,'description':lore})
legacy_catalog_keys={x['key'] for x in catalog}
r3_catalog_keys={x['key'] for x in r3_catalog}
catalog_surface_comparison={
    'legacy_catalog_items':len(legacy_catalog_keys),
    'r3_catalog_items':len(r3_catalog_keys),
    'exact_key_overlap':len(legacy_catalog_keys & r3_catalog_keys),
    'legacy_keys_not_exactly_present_in_r3':sorted(legacy_catalog_keys-r3_catalog_keys),
    'r3_keys_not_exactly_present_in_legacy':sorted(r3_catalog_keys-legacy_catalog_keys),
    'warning':'Exact-key comparison only; some R3 concepts are renamed or consolidated and require semantic parity review.'
}

# CSS colors/design tokens (legacy evidence)
color_counts=Counter(re.findall(r'#[0-9a-fA-F]{3,8}\b',old))
legacy_palette=[{'color':c,'uses':n} for c,n in color_counts.most_common(40)]
# R3 CSS vars
r3_vars={k:v for k,v in re.findall(r'--([\w-]+)\s*:\s*([^;}{]+)',r3[:20000])}

# R3 counts and parity rough surface comparison
patterns={
 'functions':r'\bfunction\s+([A-Za-z_$][\w$]*)\s*\(',
 'dom_ids':r'\bid=["\']([^"\']+)["\']',
 'runtime_userdata_keys':r'userData\.([A-Za-z_$][\w$]*)',
 'events':r'addEventListener\(["\']([^"\']+)',
}
comparison={}
for label,pat in patterns.items():
    a=set(re.findall(pat,old)); b=set(re.findall(pat,r3))
    comparison[label]={'legacy_unique':len(a),'r3_unique':len(b),'overlap':len(a&b),'legacy_not_named_in_r3':len(a-b),'r3_only':len(b-a)}

# dedupe only exact atom tuple to reduce trivial repeated UI labels while keeping event occurrences
out=[]; seen=set()
for a in atoms:
    key=(a['kind'],a['name'],a['line'])
    if key in seen: continue
    seen.add(key); out.append(a)
atoms=out
for i,a in enumerate(atoms,1): a['atom_id']=f'A{i:06d}'

# summaries
kind_counts=Counter(a['kind'] for a in atoms)
domain_counts=Counter(a['domain'] for a in atoms)
rev_counts=Counter(a['revision'] for a in atoms if a['revision'])

# roadmap architecture domains
roadmap_domains=[
 {'id':'KERNEL','name':'Kernel / Boot / Time / Event Bus','depends_on':[],'purpose':'One boot state machine, simulation clock, event bus, deterministic RNG, lifecycle and error boundary.'},
 {'id':'DATA','name':'Canonical Data Contracts','depends_on':['KERNEL'],'purpose':'Plain serializable park state, stable IDs, schemas, migrations, runtime-reference firewall.'},
 {'id':'UI','name':'Desktop UI / Windowing / Input Router','depends_on':['KERNEL','DATA'],'purpose':'One command router, one draggable/z-order manager, keyboard priority, hover/inspect contracts, title/HUD/status/pulse.'},
 {'id':'WORLD','name':'World / Terrain / Spatial Index / Camera','depends_on':['KERNEL','DATA','UI'],'purpose':'Three.js runtime maps, raycasting, terrain, land, camera modes, entity picking and LOD boundaries.'},
 {'id':'BUILD','name':'Build Database / Placement / Demolition','depends_on':['WORLD','DATA','UI'],'purpose':'Authoritative catalog, ghosts, rotation, freeplace/grid modes, bulldoze/refunds, research visibility.'},
 {'id':'PATH','name':'Paths / Queues / Navigation Graph','depends_on':['BUILD','WORLD'],'purpose':'2m cells plus freeplace engineering, welded path topology, queue-only semantics, snake geometry, bridges/elevated paths.'},
 {'id':'ECON','name':'Economy / Inventory / R&D','depends_on':['DATA','BUILD'],'purpose':'Single ledger, wallets, prices, COGS, wages, park value, research tree and funding.'},
 {'id':'GUEST','name':'Guest Entity / Brain / Needs / Social','depends_on':['PATH','ECON'],'purpose':'Needs, routing, thoughts, wellbeing, inventory visuals, seating, identities, relationships and persistent brains.'},
 {'id':'STAFF','name':'Staff / Duties / Operations','depends_on':['PATH','ECON'],'purpose':'Handymen, security, entertainers/mechanics where present, duty toggles, placement, fire/follow/inspect and service jobs.'},
 {'id':'RIDE','name':'Attractions / Access / Queue / Boarding','depends_on':['PATH','GUEST','ECON'],'purpose':'Ride registry, access drop zones, readiness authority, FIFO queues, rider proxies, seat ownership, operation and managers.'},
 {'id':'ENGINEERING','name':'Custom Coaster / Route Ride / Path Engineering','depends_on':['RIDE','BUILD','PATH'],'purpose':'Custom coaster points/validation/skins/stations, tram/train/monorail/log routes, custom elevated path engineer.'},
 {'id':'RETAIL','name':'Shops / Services / Facilities','depends_on':['GUEST','ECON','BUILD'],'purpose':'Stocked products, consumption, ATM, restrooms, care/security/clinic/water/charging and service routing.'},
 {'id':'ENV','name':'Scenery / Water / Wildlife / Lighting / Audio','depends_on':['WORLD','BUILD','GUEST'],'purpose':'HD scenery constructors, trees/grass/water, animals, programmable lights, ambience, speakers and Main PA.'},
 {'id':'ALEX','name':'Alexandria / Geocache Knowledge DB','depends_on':['DATA','GUEST','BUILD'],'purpose':'10k deterministic index, relational topic records, caches, portable/tradable files/cards, guest learning.'},
 {'id':'PHONE','name':'FrontierOS / Wi-Fi / Messaging','depends_on':['GUEST','ALEX','ENV'],'purpose':'Guest and manager phones, SSIDs/APs, maps, messages, research/social apps, Park AI.'},
 {'id':'FLOCK','name':'Guest Flock / IDE / Ollama Brokers','depends_on':['GUEST','ALEX','DATA','UI'],'purpose':'Persistent conversations/projects/files, role agents, CHAT/BUILD, code/preview, context linking, Ollama/GPT broker.'},
 {'id':'PERF','name':'Performance / Diagnostics / Compatibility','depends_on':['WORLD','GUEST','RIDE','ENV','FLOCK'],'purpose':'Benchmarks, budgets, batching/LOD, audits, browser guards and feature-preserving performance policy.'},
 {'id':'SAVE','name':'Save / Migration / Legacy Import','depends_on':['DATA','WORLD','GUEST','RIDE','FLOCK'],'purpose':'IndexedDB snapshots, project saves, JSON interchange, R138 migration, legacy normalization, reconstruction-only load.'},
 {'id':'PARITY','name':'Parity Harness / Golden Playtests','depends_on':['SAVE','PERF'],'purpose':'Port 221 audit hooks, behavioral scenarios, screenshots, save round-trips and no-feature-loss release gates.'},
]

manifest={
 'project':'RollamacoasterTycoon!! clean-core reverse engineering manifest',
 'generated_from':{
    'legacy':{'name':OLD.name,'sha256':hashlib.sha256(OLD.read_bytes()).hexdigest(),'lines':old.count('\n')+1,'bytes':OLD.stat().st_size},
    'r3':{'name':R3.name,'sha256':hashlib.sha256(R3.read_bytes()).hexdigest(),'lines':r3.count('\n')+1,'bytes':R3.stat().st_size},
    'r3_notes':{'name':NOTES.name,'sha256':hashlib.sha256(NOTES.read_bytes()).hexdigest()},
    'builder':{'name':BUILDER.name,'sha256':hashlib.sha256(BUILDER.read_bytes()).hexdigest()},
 },
 'interpretation':'Atoms are recoverable implementation/behavior/design contracts, not a claim that every row is an independent player-facing feature.',
 'counts':{
    'feature_implementation_atoms':len(atoms),
    'revision_meta_descriptions':len(revision_summaries),
    'build_catalog_items':len(catalog),
    'build_meta_descriptions':len(build_meta),
    'legacy_audit_contracts':kind_counts.get('audit_contract',0),
    'legacy_functions':kind_counts.get('function',0),
    'legacy_dom_ids':kind_counts.get('dom_id',0),
    'legacy_runtime_userdata_keys':kind_counts.get('runtime_userdata_key',0),
 },
 'atom_counts_by_kind':dict(kind_counts),
 'atom_counts_by_domain':dict(domain_counts),
 'legacy_r3_surface_comparison':comparison,
 'revision_summaries':revision_summaries,
 'catalog':catalog,
 'r3_catalog':r3_catalog,
 'catalog_surface_comparison':catalog_surface_comparison,
 'build_meta':build_meta,
 'legacy_palette':legacy_palette,
 'r3_css_variables':r3_vars,
 'roadmap_domains':roadmap_domains,
}

# JSON + JSONL
(OUT/'rollamacoaster_reverse_engineering_manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False))
with (OUT/'rollamacoaster_feature_atoms.jsonl').open('w') as f:
    for a in atoms: f.write(json.dumps(a,ensure_ascii=False)+'\n')

# Human-readable report
kc=kind_counts; dc=domain_counts
report=[]
report.append('# RollamacoasterTycoon!! Reverse-Engineering Master Plan')
report.append('')
report.append('## Executive conclusion')
report.append('The R233M lineage should be treated as a behavioral specification and archaeological reference, not as the code foundation. Revision 3 has the correct clean-core direction, but it intentionally omitted specialized late experiments. The rebuild should therefore preserve R3 kernel contracts while importing legacy behavior through bounded domain modules and a parity harness.')
report.append('')
report.append(f'Automated static extraction recovered **{len(atoms):,} feature/implementation/design atoms** from the legacy file. This number intentionally includes user-facing behaviors, UI contracts, data keys, event hooks, diagnostics, functions and implementation symbols. It is not a claim that the game has {len(atoms):,} independent menu-visible features.')
report.append('')
report.append('### Recovery totals')
report.append(f'- **Legacy build catalog:** {len(catalog):,} items')
report.append(f'- **R3 build catalog:** {len(r3_catalog):,} items')
report.append(f'- **Legacy catalog keys without an exact R3 key match:** {len(legacy_catalog_keys-r3_catalog_keys):,} (semantic alias review still required)')
for k in ['revision_meta_description','revision_requirement','build_catalog_item','build_meta_description','audit_contract','function','arrow_function','dom_id','css_class','runtime_userdata_key','dataset_contract','persistence_key','event_binding','ui_tooltip','ui_placeholder','ui_button_label','external_endpoint','implementation_symbol']:
    if kc.get(k): report.append(f'- **{k}:** {kc[k]:,}')
report.append('')
report.append('## Non-negotiable rebuild principles')
principles=[
'**Feature registry before implementation.** Every legacy atom receives a stable registry ID, owner domain, parity status, evidence line and test status.',
'**Plain state, runtime views.** No Three.js objects, DOM nodes, audio elements, controls, renderers, curves or transient camera state may enter saves.',
'**One authority per concept.** One economy ledger, one entity registry, one ride readiness calculation, one queue owner, one input router, one window manager, one simulation clock.',
'**No monkey-patch architecture.** Later features register with domain interfaces/events. They do not replace global functions after boot.',
'**Queue and rider ownership are mutually exclusive.** Waiting avatar and rider proxy are different states with explicit boarding/unboarding transitions.',
'**Navigation is data, visuals are projections.** Paths/queues/bridges generate a graph; rails, ribbons and guides are derived render layers.',
'**Every write is schema-validated.** Saves, brains, conversations, Flock files, Alexandria records and migration payloads are versioned.',
'**Performance optimizations cannot silently change semantics.** LOD/batching may change rendering cost, never entity existence, routing, queue state, inventories or economy.',
'**Legacy audits become release tests.** The 221 recovered audit hooks are ported into deterministic assertions or scenario checks.',
'**No deletion by cleanup.** A legacy item can be marked superseded or intentionally retired only by an explicit parity decision, never because the new architecture lacks a place for it.'
]
report.extend('- '+p for p in principles)
report.append('')
report.append('## Target architecture')
report.append('Each domain owns state transitions and exposes commands/events. The renderer subscribes to state and keeps runtime objects in maps keyed by stable IDs.')
report.append('')
for d in roadmap_domains:
    deps=', '.join(d['depends_on']) or 'none'
    report.append(f"### {d['id']} · {d['name']}\n**Depends on:** {deps}\n\n{d['purpose']}\n")
report.append('## Canonical state split')
report.append('```text\nParkSnapshot (serializable)\n  schema / metadata / simulation clock\n  economy + ledger references\n  entities[] / paths[] / rides[] / services[]\n  guests[] / staff[]\n  research / settings\n  alexandria refs / phone network refs\n  flock project refs\n\nRuntimeWorld (never serialized)\n  scene / renderer / cameras / controls\n  meshesByEntityId / lights / audio nodes\n  nav caches / raycast acceleration / LOD batches\n  hover targets / placement ghosts / open windows\n```')
report.append('')
report.append('## Feature parity workflow')
report.append('1. Ingest `rollamacoaster_feature_atoms.jsonl`. Normalize duplicates into human-scale capabilities while retaining every source atom as evidence.')
report.append('2. Assign each capability to one target domain and mark `legacy_only`, `r3_present`, `porting`, `parity_pass`, or `intentional_retirement`.')
report.append('3. For each legacy `*AuditR...` hook, implement an R3 test adapter before porting the feature. The test should fail first.')
report.append('4. Port data model and commands before visuals. Then add visuals as projections of authoritative state.')
report.append('5. Run save/load round-trip after every domain milestone. A loaded park must reconstruct a fresh runtime and return to active neutral camera state.')
report.append('6. Run scenario packs: empty park, 300 guests, 2,000 guests, queues, transports, custom coaster, shops, geocaches, phones, media, Flock, and legacy save import.')
report.append('7. Do not declare a phase complete until its registry rows have no unexplained `missing` status.')
report.append('')
report.append('## Build roadmap')
phases=[
('0 · Freeze the fossil','Hash the legacy and R3 inputs; generate manifest/registry; capture catalog, revision notes, audits, UI labels, storage keys and endpoint contracts. No gameplay coding until this is reproducible.'),
('1 · Clean kernel','Finalize KERNEL + DATA + UI. Boot state machine, event bus, clock, deterministic IDs/RNG, error boundary, input priority, draggable/z-order window manager, plain-state schemas.'),
('2 · World substrate','WORLD + BUILD. Terrain, land, starter park, raycast inspect, placement ghosts, rotation, demolition, authoritative build catalog. Port every catalog item as data even if its constructor is temporarily stubbed.'),
('3 · Paths are the nervous system','PATH. 2m grid and freeplace modes, cardinal/welded topology, queue-only nodes, snake detection, bridges, custom elevated path engineer, graph rebuild and path audits.'),
('4 · Money cannot fork','ECON. Single transaction API for construction/refunds/admission/rides/retail/COGS/wages/maintenance/R&D. Port park value and finance audits before advanced guest logic.'),
('5 · Living guests and workers','GUEST + STAFF. Identities, needs, wallets, thoughts, wellbeing, inventory visuals, seating, duties, placement/firing/follow/inspect. Persist brains separately from world entities.'),
('6 · Ride authority','RIDE. Ride registry, open/close/readiness, standard entrance/exit drop zones, queue demand, FIFO slots, board/unboard state machine, Ferris upright cabins and seat proxies, manager/hover telemetry.'),
('7 · Commerce and facilities','RETAIL. Every food/shop/service product, stock, consumption, ATM, restrooms, Family Care, First Aid/Clinic, Security, water, charging, bins and operational routing.'),
('8 · Engineering attractions','ENGINEERING. Custom coaster builder/validation/commissioning/skins, transport route builders/stations, log flume route mode, custom bridges/paths, access overlays.'),
('9 · Park atmosphere','ENV. All scenery constructors, trees/flowers/grass, water animation, wildlife autonomy, lighting programs, Wave Beacon soft sine default, speakers/Main PA/Jamendo/Radio/Synthwave, ambience.'),
('10 · Alexandria','ALEX. 10,000-topic deterministic database, relational detail/search, geocache placement/routing/read/trade/file inventory, guest learning and peer-context integration.'),
('11 · FrontierOS','PHONE. Guest + manager phones, paper map, geocache client, messages, Wi-Fi multi-SSID/MU-MIMO/beamforming, apps and Park AI.'),
('12 · Flock IDE','FLOCK. Persistent chats/projects/files, Codex/Unsloth command strip, explorer/search/conversation drawers, editor tabs/dirty state, code/preview, role agents, Ollama discovery/chat, optional GPT broker.'),
('13 · Performance without amnesia','PERF. Port benchmark suite, adaptive budgets, batching/LOD and distance options. Verify each optimization against semantic audits so proxies never change simulation truth.'),
('14 · Save and migration hardening','SAVE. IndexedDB schemas, project saves, Save As/Open/Delete, export/import, R138 detection, FULL_SIMULATION_SNAPSHOT normalization, version migrations, no runtime refs.'),
('15 · Parity burn-down','PARITY. Convert all 221 audit hooks, replay revision feature scenarios, compare legacy/R3 behavior, close every unexplained registry gap. Only then call the structured build feature-complete.'),
]
for name,desc in phases: report.append(f'### Phase {name}\n{desc}\n')
report.append('## Highest-risk seams to eliminate')
for x in [
'Classic-script ↔ ES-module scope fractures. R233M itself ends with a root fix because later scripts could not access authoritative module scope.',
'Camera/input ownership after load or modal close. Transient interaction state must never be serialized.',
'Multiple queue/rider render owners. Boarding must atomically transfer ownership.',
'Repeated function replacement across revisions. Replace with registered handlers and event subscriptions.',
'Economy side effects scattered across shops/rides/inventory. All money movement must go through one ledger transaction API.',
'DOM as state. Panels should render from stores; hiding/showing a node must not determine simulation truth.',
'Performance code that alters entity semantics. Rendering LOD must be orthogonal to simulation LOD.',
'Browser-origin persistence assumptions. IndexedDB migrations need explicit versioning and portable export paths.',
'External media/network failures. Jamendo/Radio/Ollama/GPT integrations require capability detection, timeouts and local fallbacks.'
]: report.append('- '+x)
report.append('')
report.append('## Design language to preserve')
report.append('- **Park shell:** dark forest/charcoal glass UI, thin green-gray borders, compact monospace telemetry, gold/cyan/green status accents, dense draggable utility windows.')
report.append('- **Build language:** icon + name + lore + price, category/subcategory organization, search, placement ghost, rotation, clear build-mode footer.')
report.append('- **World feedback:** hover telemetry, entity inspectors, bottom contextual status dock, Park Pulse feed/announcements, world-space entrance/exit markers.')
report.append('- **Flock language:** darker neutral IDE surface distinct from park glass, compact command strip, on-demand drawers, editor/preview split, explicit model/run/stage state.')
report.append('- **Meta/lore:** item descriptions are gameplay-facing documentation, not decoration. Preserve catalog lore, technical codes, research descriptions and revision-intent notes in data files.')
report.append('')
report.append('## Suggested structured repository')
report.append('```text\nrollamacoaster/\n  app/\n    kernel/          boot, clock, events, commands, errors\n    data/            schemas, migrations, ids, repositories\n    world/           terrain, spatial, render adapters, cameras\n    build/           catalog, placement, demolition\n    navigation/      paths, queues, graph, bridges\n    economy/         ledger, pricing, inventory, research\n    guests/          entities, brains, needs, routing, social\n    staff/           roles, duties, operations\n    rides/           registry, access, queues, boarding, vehicles\n    engineering/     coaster/path/route builders\n    retail/          shops, products, services\n    environment/     scenery, wildlife, water, lighting, media\n    alexandria/      knowledge DB, geocaches\n    frontieros/      phones, wifi, messaging, apps\n    flock/           projects, conversations, agents, brokers\n    ui/              windows, panels, inspectors, pulse, HUD\n    persistence/     IndexedDB, saves, import/export\n    diagnostics/     audits, benchmarks, parity harness\n  content/\n    build-catalog.json\n    research-tree.json\n    lore.json\n    feature-registry.jsonl\n  tests/\n    audits/\n    scenarios/\n    migrations/\n    golden/\n```')
report.append('')
report.append('## Concrete first implementation slice')
report.append('The first shippable slice should be intentionally narrow but architecturally complete: title → new/open park → orbit/interact → build path → build one shop/service/ride → spawn guest → guest routes and spends → queue/board ride → save → reload → same authoritative state reconstructed. Every later feature plugs into those contracts rather than modifying them.')
report.append('')
report.append('## Generated companion files')
report.append('- `rollamacoaster_reverse_engineering_manifest.json` — structured summaries, catalogs, design tokens, counts and domain roadmap.')
report.append('- `rollamacoaster_feature_atoms.jsonl` — exhaustive static recovery ledger with source lines and inferred domains.')
report.append('- `rollamacoaster_revision_meta.md` — chronological revision-intent descriptions recovered from the legacy file.')

(OUT/'rollamacoaster_reverse_engineering_master_plan.md').write_text('\n'.join(report))

# revision meta chronology
def revkey(r):
    m=re.match(r'R(\d+)([A-Z]*)',r); return (int(m.group(1)),m.group(2)) if m else (9999,r)
revmd=['# RollamacoasterTycoon!! Recovered Revision Meta Descriptions','',f'Recovered {len(revision_summaries)} explicit hidden revision summaries from the R233M source.']
for rec in sorted(revision_summaries,key=lambda x:revkey(x['revision'])):
    revmd += ['',f"## {rec['revision']} · {rec['domain']}",f"Source line {rec['line']}",'',rec['description']]
(OUT/'rollamacoaster_revision_meta.md').write_text('\n'.join(revmd))

print(json.dumps({
 'atoms':len(atoms),
 'kind_counts':dict(kind_counts),
 'domain_counts':dict(domain_counts),
 'revision_summaries':len(revision_summaries),
 'catalog':len(catalog),
 'build_meta':len(build_meta),
 'comparison':comparison,
 'outputs':[str(OUT/'rollamacoaster_reverse_engineering_master_plan.md'),str(OUT/'rollamacoaster_reverse_engineering_manifest.json'),str(OUT/'rollamacoaster_feature_atoms.jsonl'),str(OUT/'rollamacoaster_revision_meta.md')]
},indent=2))
