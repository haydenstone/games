#!/usr/bin/env python3
"""Idempotently add same-origin Alexandria proxy routes to rct_r3_dev_server.py.

Routes added:
  GET  /api/alexandria/status
  GET  /api/alexandria/document/<id>
  POST /api/alexandria/search  {"query":"...", "limit":5}

The game browser never needs to call LoA :8090 directly.
"""
from __future__ import annotations

from pathlib import Path
import re
import sys

if len(sys.argv) != 2:
    raise SystemExit("usage: r3_loa_patch_server.py /path/to/rct_r3_dev_server.py")

p = Path(sys.argv[1])
s = p.read_text()

if "R3_LOA_DEV25_SERVER_BEGIN" in s:
    print("R3 LoA server patch already present.")
    raise SystemExit(0)

# Add imports safely after the import block. We intentionally use unique aliases.
imports = '''\n# R3_LOA_DEV25_SERVER_BEGIN\nimport json as _r3_loa_json\nimport os as _r3_loa_os\nimport urllib.error as _r3_loa_urlerror\nimport urllib.parse as _r3_loa_urlparse\nimport urllib.request as _r3_loa_urlrequest\n\n_R3_LOA_BASE = _r3_loa_os.environ.get("RCT_LOA_BASE", "http://127.0.0.1:8090").rstrip("/")\n_R3_LOA_TIMEOUT = float(_r3_loa_os.environ.get("RCT_LOA_TIMEOUT", "4.0"))\n# R3_LOA_DEV25_SERVER_IMPORTS_END\n'''

# Put imports immediately before Handler so normal stdlib imports have already occurred.
class_match = re.search(r'(?m)^class\s+Handler\s*\(\s*SimpleHTTPRequestHandler\s*\)\s*:', s)
if not class_match:
    raise SystemExit("Could not locate class Handler(SimpleHTTPRequestHandler); refusing unsafe patch.")
s = s[:class_match.start()] + imports + "\n" + s[class_match.start():]

# Add Handler helper methods directly after class declaration.
class_match = re.search(r'(?m)^class\s+Handler\s*\(\s*SimpleHTTPRequestHandler\s*\)\s*:\s*\n', s)
assert class_match
methods = r'''    # R3_LOA_DEV25_HANDLER_METHODS_BEGIN
    def _r3_loa_send_json(self, status, payload):
        body = _r3_loa_json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _r3_loa_http_json(self, url):
        req = _r3_loa_urlrequest.Request(url, headers={"Accept": "application/json"})
        with _r3_loa_urlrequest.urlopen(req, timeout=_R3_LOA_TIMEOUT) as res:
            raw = res.read()
            return res.status, _r3_loa_json.loads(raw.decode("utf-8"))

    def _r3_loa_status(self):
        # Use a zero-result keyword query as a real application health probe.
        probe = _r3_loa_urlparse.quote("__r3_health_probe__", safe="")
        url = f"{_R3_LOA_BASE}/document/find-by/keyword/{probe}/"
        try:
            status, data = self._r3_loa_http_json(url)
            self._r3_loa_send_json(200, {
                "ok": True,
                "source": "library-of-alexandria",
                "base": _R3_LOA_BASE,
                "upstreamStatus": status,
                "totalHitCount": data.get("totalHitCount", 0),
            })
        except Exception as exc:
            self._r3_loa_send_json(503, {
                "ok": False,
                "source": "library-of-alexandria",
                "base": _R3_LOA_BASE,
                "error": str(exc),
            })

    def _r3_loa_document(self, document_id):
        safe_id = _r3_loa_urlparse.quote(document_id, safe="")
        url = f"{_R3_LOA_BASE}/document/{safe_id}"
        try:
            req = _r3_loa_urlrequest.Request(url)
            with _r3_loa_urlrequest.urlopen(req, timeout=_R3_LOA_TIMEOUT) as res:
                body = res.read()
                self.send_response(res.status)
                self.send_header("Content-Type", res.headers.get("Content-Type", "application/octet-stream"))
                self.send_header("Content-Length", str(len(body)))
                self.send_header("Cache-Control", "no-store")
                self.end_headers()
                self.wfile.write(body)
        except _r3_loa_urlerror.HTTPError as exc:
            body = exc.read()
            self.send_response(exc.code)
            self.send_header("Content-Type", exc.headers.get("Content-Type", "application/json"))
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        except Exception as exc:
            self._r3_loa_send_json(503, {"ok": False, "error": str(exc)})

    def _r3_loa_search(self):
        try:
            length = int(self.headers.get("Content-Length", "0") or 0)
            payload = _r3_loa_json.loads(self.rfile.read(length) or b"{}")
            query = str(payload.get("query", "")).strip()
            limit = max(1, min(int(payload.get("limit", 6) or 6), 25))
            if not query:
                return self._r3_loa_send_json(400, {"ok": False, "error": "query is required"})

            encoded = _r3_loa_urlparse.quote(query, safe="")
            url = f"{_R3_LOA_BASE}/document/find-by/keyword/{encoded}/"
            upstream_status, raw = self._r3_loa_http_json(url)
            hits = raw.get("searchHits") or []
            limited = hits[:limit]

            def pick(obj, *keys):
                if not isinstance(obj, dict):
                    return None
                for key in keys:
                    val = obj.get(key)
                    if val not in (None, ""):
                        return val
                return None

            normalized = []
            for hit in limited:
                source = hit.get("source") if isinstance(hit, dict) and isinstance(hit.get("source"), dict) else hit
                normalized.append({
                    "id": pick(source, "id", "documentId", "document_id", "_id"),
                    "title": pick(source, "title", "name", "filename"),
                    "snippet": pick(source, "snippet", "description", "content", "text"),
                    "type": pick(source, "type", "documentType", "mimeType"),
                    "raw": hit,
                })

            self._r3_loa_send_json(200, {
                "ok": True,
                "source": "library-of-alexandria",
                "query": query,
                "limit": limit,
                "upstreamStatus": upstream_status,
                "totalHitCount": raw.get("totalHitCount", len(hits)),
                "searchHits": limited,
                "results": normalized,
            })
        except Exception as exc:
            self._r3_loa_send_json(502, {
                "ok": False,
                "source": "library-of-alexandria",
                "error": str(exc),
            })
    # R3_LOA_DEV25_HANDLER_METHODS_END

'''
s = s[:class_match.end()] + methods + s[class_match.end():]

# Route GET before existing body logic. We do not depend on its local path variable.
get_match = re.search(r'(?m)^(\s{4})def\s+do_GET\s*\(self\)\s*:\s*\n', s)
if not get_match:
    raise SystemExit("Could not locate Handler.do_GET; refusing unsafe patch.")
get_inject = '''        # R3_LOA_DEV25_GET_ROUTES\n        _r3_path = self.path.split("?", 1)[0]\n        if _r3_path == "/api/alexandria/status":\n            return self._r3_loa_status()\n        if _r3_path.startswith("/api/alexandria/document/"):\n            return self._r3_loa_document(_r3_path.rsplit("/", 1)[-1])\n'''
s = s[:get_match.end()] + get_inject + s[get_match.end():]

# Route POST before any existing whitelist, which previously rejected unknown routes.
post_match = re.search(r'(?m)^(\s{4})def\s+do_POST\s*\(self\)\s*:\s*\n', s)
if not post_match:
    raise SystemExit("Could not locate Handler.do_POST; refusing unsafe patch.")
post_inject = '''        # R3_LOA_DEV25_POST_ROUTES\n        _r3_path = self.path.split("?", 1)[0]\n        if _r3_path == "/api/alexandria/search":\n            return self._r3_loa_search()\n'''
s = s[:post_match.end()] + post_inject + s[post_match.end():]

s += "\n# R3_LOA_DEV25_SERVER_END\n"
p.write_text(s)
print(f"Patched {p}")
