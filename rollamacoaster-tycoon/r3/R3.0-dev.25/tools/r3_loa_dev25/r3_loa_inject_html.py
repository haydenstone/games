#!/usr/bin/env python3
"""Inject a bounded, non-blocking Alexandria browser adapter into the R3 HTML artifact.

The adapter is intentionally additive:
- same-origin only
- never blocks game boot
- exposes window.R3Alexandria
- small independent IndexedDB live-result cache
- emits r3:alexandria:* events so native R3 systems can adopt results incrementally

It does not replace the existing R3 Alexandria/Codex/brain systems.
"""
from pathlib import Path
import sys

if len(sys.argv) != 2:
    raise SystemExit("usage: r3_loa_inject_html.py /path/to/rollamacoasterTycoon_R3_rebuilt.html")

p = Path(sys.argv[1])
s = p.read_text()
start = "<!-- R3_LOA_DEV25_BROWSER_BEGIN -->"
end = "<!-- R3_LOA_DEV25_BROWSER_END -->"

block = r'''<!-- R3_LOA_DEV25_BROWSER_BEGIN -->
<script>
(() => {
  'use strict';
  if (window.R3Alexandria && window.R3Alexandria.__dev25) return;

  const DB_NAME = 'RCT_R3_AlexandriaLive';
  const DB_VERSION = 1;
  const STORE = 'results';
  const active = new Map();
  const entityLastQueryAt = new Map();
  let inFlight = 0;
  const GLOBAL_MAX = 3;
  const ENTITY_COOLDOWN_MS = 30000;

  function emit(name, detail) {
    try { window.dispatchEvent(new CustomEvent(name, {detail})); } catch (_) {}
  }

  function openCache() {
    return new Promise((resolve, reject) => {
      const req = indexedDB.open(DB_NAME, DB_VERSION);
      req.onupgradeneeded = () => {
        const db = req.result;
        if (!db.objectStoreNames.contains(STORE)) {
          const st = db.createObjectStore(STORE, {keyPath: 'cacheKey'});
          st.createIndex('query', 'query', {unique:false});
          st.createIndex('entityId', 'entityId', {unique:false});
          st.createIndex('cachedAt', 'cachedAt', {unique:false});
        }
      };
      req.onsuccess = () => resolve(req.result);
      req.onerror = () => reject(req.error);
    });
  }

  async function cacheRows(query, entityId, data) {
    try {
      const db = await openCache();
      const tx = db.transaction(STORE, 'readwrite');
      const store = tx.objectStore(STORE);
      const now = Date.now();
      const rows = Array.isArray(data.results) ? data.results : [];
      rows.forEach((row, i) => {
        const id = row && (row.id || (row.raw && (row.raw.id || row.raw._id))) || `rank:${i}`;
        store.put({
          cacheKey: `${query}::${entityId || 'operator'}::${id}`,
          source: 'library-of-alexandria',
          sourceId: id,
          query,
          entityId: entityId || null,
          cachedAt: now,
          discoveredAt: now,
          title: row && row.title || null,
          snippet: row && row.snippet || null,
          type: row && row.type || null,
          raw: row && row.raw || row || null,
        });
      });
      await new Promise((resolve, reject) => {
        tx.oncomplete = resolve;
        tx.onerror = () => reject(tx.error);
        tx.onabort = () => reject(tx.error || new Error('cache transaction aborted'));
      });
      db.close();
    } catch (error) {
      emit('r3:alexandria:cache-error', {query, entityId, error:String(error)});
    }
  }

  async function status() {
    const r = await fetch('/api/alexandria/status', {cache:'no-store'});
    const data = await r.json().catch(() => ({}));
    if (!r.ok) throw Object.assign(new Error(data.error || `Alexandria status ${r.status}`), {status:r.status, data});
    return data;
  }

  async function search(query, options={}) {
    query = String(query || '').trim();
    if (!query) throw new Error('Alexandria query is required');
    const limit = Math.max(1, Math.min(Number(options.limit || 6), 25));
    const entityId = options.entityId ? String(options.entityId) : null;

    if (entityId && !options.force) {
      const last = entityLastQueryAt.get(entityId) || 0;
      if (Date.now() - last < ENTITY_COOLDOWN_MS) {
        const error = new Error('Alexandria entity cooldown active');
        error.code = 'ALEXANDRIA_COOLDOWN';
        throw error;
      }
    }

    const key = `${query}::${limit}`;
    if (active.has(key)) return active.get(key);
    if (inFlight >= GLOBAL_MAX) {
      const error = new Error('Alexandria global concurrency limit reached');
      error.code = 'ALEXANDRIA_BUSY';
      throw error;
    }

    const job = (async () => {
      inFlight++;
      if (entityId) entityLastQueryAt.set(entityId, Date.now());
      emit('r3:alexandria:query', {query, limit, entityId});
      try {
        const r = await fetch('/api/alexandria/search', {
          method: 'POST',
          headers: {'Content-Type':'application/json'},
          body: JSON.stringify({query, limit}),
        });
        const data = await r.json().catch(() => ({}));
        if (!r.ok) throw Object.assign(new Error(data.error || `Alexandria search ${r.status}`), {status:r.status, data});
        await cacheRows(query, entityId, data);
        emit('r3:alexandria:results', {query, limit, entityId, data});
        return data;
      } catch (error) {
        emit('r3:alexandria:error', {query, limit, entityId, error:String(error)});
        throw error;
      } finally {
        inFlight--;
      }
    })();

    active.set(key, job);
    try { return await job; }
    finally { active.delete(key); }
  }

  async function document(id) {
    const r = await fetch(`/api/alexandria/document/${encodeURIComponent(id)}`, {cache:'no-store'});
    if (!r.ok) throw new Error(`Alexandria document ${r.status}`);
    return r;
  }

  async function queryForEntity(entityOrId, query, options={}) {
    const entityId = typeof entityOrId === 'string' ? entityOrId : entityOrId && entityOrId.id;
    const data = await search(query, {...options, entityId});
    // Deliberately do not mutate unknown native entity structures here.
    // Native R3 can listen to r3:alexandria:results and persist into its own brain schema.
    return data;
  }

  window.R3Alexandria = Object.freeze({
    __dev25: true,
    status,
    search,
    document,
    queryForEntity,
    config: Object.freeze({GLOBAL_MAX, ENTITY_COOLDOWN_MS, cacheDb:DB_NAME, cacheStore:STORE}),
  });

  // Non-blocking capability discovery. Failure is informational only.
  setTimeout(() => {
    status()
      .then(data => emit('r3:alexandria:online', data))
      .catch(error => emit('r3:alexandria:offline', {error:String(error)}));
  }, 1500);
})();
</script>
<!-- R3_LOA_DEV25_BROWSER_END -->'''

if start in s and end in s:
    a = s.index(start)
    b = s.index(end, a) + len(end)
    s = s[:a] + block + s[b:]
    p.write_text(s)
    print(f"Refreshed existing Alexandria adapter in {p}")
    raise SystemExit(0)

needle = '</body>'
idx = s.lower().rfind(needle)
if idx < 0:
    raise SystemExit('Could not locate </body>; refusing unsafe HTML injection.')
s = s[:idx] + block + '\n' + s[idx:]
p.write_text(s)
print(f"Injected Alexandria adapter into {p}")
