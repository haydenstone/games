#!/usr/bin/env python3
"""RollamacoasterTycoon R3 playtest launcher + diagnostics collector.

Serves the exact standalone HTML artifact and captures the in-game development
Test Bench POSTs into timestamped session folders. Standard-library only.
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import re
import threading
import webbrowser
from datetime import datetime, timezone
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import os
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
ARTIFACT = "rollamacoasterTycoon_R3_rebuilt.html"
SESSIONS = ROOT / "rct_r3_dev_sessions"
MAX_BODY = 80 * 1024 * 1024


def utcstamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def safe_name(value: str) -> str:
    value = re.sub(r"[^A-Za-z0-9._-]+", "_", value or "unknown")
    return value[:160] or "unknown"


def atomic_json(path: Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    tmp.replace(path)



# R3_LOA_DEV25_SERVER_BEGIN
import json as _r3_loa_json
import os as _r3_loa_os
import urllib.error as _r3_loa_urlerror
import urllib.parse as _r3_loa_urlparse
import urllib.request as _r3_loa_urlrequest

_R3_LOA_BASE = _r3_loa_os.environ.get("RCT_LOA_BASE", "http://127.0.0.1:8090").rstrip("/")
_R3_LOA_TIMEOUT = float(_r3_loa_os.environ.get("RCT_LOA_TIMEOUT", "4.0"))
# R3_LOA_DEV25_SERVER_IMPORTS_END

class Handler(SimpleHTTPRequestHandler):

    # R3_LOA_DEV25_HANDLER_METHODS_BEGIN
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

    # ------------------------------------------------------------------
    # Alexandria Knowledge Bridge
    # ------------------------------------------------------------------

    def _loa_base(self):
        return os.environ.get("RCT_LOA_BASE", "").strip().rstrip("/")

    def _loa_send_json(self, status, payload):
        raw = json.dumps(
            payload,
            ensure_ascii=False,
            separators=(",", ":")
        ).encode("utf-8")

        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(raw)

    def _loa_status(self):
        base = self._loa_base()

        if not base:
            return self._loa_send_json(200, {
                "configured": False,
                "live": False,
                "base": None,
                "reason": "RCT_LOA_BASE is not configured"
            })

        try:
            req = urllib.request.Request(
                base + "/",
                headers={"User-Agent": "rollamacoasterTycoon-R3/AlexandriaBridge"}
            )

            with urllib.request.urlopen(req, timeout=3) as response:
                code = response.getcode()

            return self._loa_send_json(200, {
                "configured": True,
                "live": 200 <= code < 500,
                "base": base,
                "httpStatus": code
            })

        except urllib.error.HTTPError as exc:
            return self._loa_send_json(200, {
                "configured": True,
                "live": exc.code < 500,
                "base": base,
                "httpStatus": exc.code
            })

        except Exception as exc:
            return self._loa_send_json(200, {
                "configured": True,
                "live": False,
                "base": base,
                "error": str(exc)
            })

    def _loa_search(self):
        base = self._loa_base()

        if not base:
            return self._loa_send_json(503, {
                "ok": False,
                "error": "Alexandria is not configured",
                "configured": False
            })

        try:
            length = int(self.headers.get("Content-Length", "0") or "0")
            body = self.rfile.read(length) if length else b"{}"
            request_data = json.loads(body.decode("utf-8") or "{}")
        except Exception as exc:
            return self._loa_send_json(400, {
                "ok": False,
                "error": "Invalid JSON request body",
                "detail": str(exc)
            })

        query = str(request_data.get("query", "")).strip()

        if not query:
            return self._loa_send_json(400, {
                "ok": False,
                "error": "query is required"
            })

        try:
            requested_limit = int(request_data.get("limit", 10))
        except Exception:
            requested_limit = 10

        requested_limit = max(1, min(100, requested_limit))

        # LoA currently enforces resultSize >= 10, even if R3 asks for fewer.
        loa_result_size = max(10, requested_limit)

        encoded = urllib.parse.quote(query, safe="")

        url = (
            f"{base}/document/find-by/keyword/{encoded}/"
            f"?pageNumber=0&resultSize={loa_result_size}"
        )

        try:
            req = urllib.request.Request(
                url,
                headers={
                    "Accept": "application/json",
                    "User-Agent": "rollamacoasterTycoon-R3/AlexandriaBridge"
                }
            )

            with urllib.request.urlopen(req, timeout=15) as response:
                raw = response.read()
                result = json.loads(raw.decode("utf-8"))

            hits = result.get("searchHits") or []
            hits = hits[:requested_limit]

            return self._loa_send_json(200, {
                "ok": True,
                "source": "alexandria",
                "base": base,
                "query": query,
                "limit": requested_limit,

                # Preserve native LoA terminology.
                "totalHitCount": result.get("totalHitCount", len(hits)),
                "searchHits": hits,

                # R3-friendly alias for future KnowledgeBroker consumers.
                "results": hits
            })

        except urllib.error.HTTPError as exc:
            try:
                detail = exc.read().decode("utf-8", errors="replace")
            except Exception:
                detail = ""

            return self._loa_send_json(502, {
                "ok": False,
                "source": "alexandria",
                "query": query,
                "error": "Alexandria HTTP error",
                "httpStatus": exc.code,
                "detail": detail
            })

        except urllib.error.URLError as exc:
            return self._loa_send_json(503, {
                "ok": False,
                "source": "alexandria",
                "query": query,
                "error": "Alexandria is unreachable",
                "detail": str(exc.reason)
            })

        except Exception as exc:
            return self._loa_send_json(502, {
                "ok": False,
                "source": "alexandria",
                "query": query,
                "error": "Alexandria bridge failure",
                "detail": str(exc)
            })

    server_version = "RCT-R3-Dev/1.1"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def log_message(self, fmt, *args):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {self.address_string()} {fmt % args}")

    def _json(self, status: int, payload) -> None:
        raw = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def _read_json(self):
        try:
            size = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            size = 0
        if size <= 0 or size > MAX_BODY:
            raise ValueError(f"invalid Content-Length {size}")
        raw = self.rfile.read(size)
        return json.loads(raw.decode("utf-8"))

    def do_GET(self):
        # R3_LOA_DEV25_GET_ROUTES
        _r3_path = self.path.split("?", 1)[0]
        if _r3_path == "/api/alexandria/status":
            return self._r3_loa_status()
        if _r3_path.startswith("/api/alexandria/document/"):
            return self._r3_loa_document(_r3_path.rsplit("/", 1)[-1])
        path = urlparse(self.path).path
        if path == "/":
            self.send_response(HTTPStatus.FOUND)
            self.send_header("Location", f"/{ARTIFACT}")
            self.end_headers()
            return
        if path == "/api/alexandria/status":
            return self._loa_status()

        if path == "/api/dev/status":
            self._json(200, {
                "ok": True,
                "collector": "rct_r3_dev_server.py",
                "root": str(ROOT),
                "artifact": ARTIFACT,
                "sessions": str(SESSIONS),
                "time": datetime.now(timezone.utc).isoformat(),
            })
            return
        return super().do_GET()

    def do_POST(self):
        # R3_LOA_DEV25_POST_ROUTES
        _r3_path = self.path.split("?", 1)[0]
        if _r3_path == "/api/alexandria/search":
            return self._r3_loa_search()
        path = urlparse(self.path).path
        if path == "/api/alexandria/search":
            return self._loa_search()

        if path not in {"/api/dev/session", "/api/dev/comment", "/api/dev/core-dump", "/api/dev/review-packet", "/api/dev/viewport-capture"}:
            self._json(404, {"ok": False, "error": "unknown endpoint"})
            return
        try:
            data = self._read_json()
            session_id = safe_name(str(data.get("sessionId") or "unknown-session"))
            folder = SESSIONS / session_id
            folder.mkdir(parents=True, exist_ok=True)

            if path == "/api/dev/session":
                atomic_json(folder / "session.json", data)
                dest = folder / "session.json"
            elif path == "/api/dev/comment":
                dest = folder / "comments.jsonl"
                with dest.open("a", encoding="utf-8") as fh:
                    fh.write(json.dumps(data, ensure_ascii=False) + "\n")
            elif path == "/api/dev/core-dump":
                dest = folder / f"core-{utcstamp()}.json"
                atomic_json(dest, data)
                atomic_json(folder / "core-latest.json", data)
            elif path == "/api/dev/viewport-capture":
                capture = data.get("capture") or {}
                data_url = str(capture.get("dataUrl") or "")
                prefix = "data:image/png;base64,"
                if not data_url.startswith(prefix):
                    raise ValueError("viewport capture is missing PNG data")
                raw = base64.b64decode(data_url[len(prefix):], validate=True)
                stamp = utcstamp()
                dest = folder / f"viewport-{stamp}.png"
                dest.write_bytes(raw)
                (folder / "viewport-latest.png").write_bytes(raw)
                meta = {k:v for k,v in capture.items() if k != "dataUrl"}
                meta.update({"release": data.get("release"), "sessionId": session_id, "saved": str(dest.relative_to(ROOT))})
                atomic_json(folder / f"viewport-{stamp}.json", meta)
                atomic_json(folder / "viewport-latest.json", meta)
            else:
                dest = folder / f"review-{utcstamp()}.json"
                atomic_json(dest, data)
                atomic_json(folder / "review-latest.json", data)

            self._json(200, {"ok": True, "saved": str(dest.relative_to(ROOT)), "sessionId": session_id})
            print(f"  ↳ saved {dest.relative_to(ROOT)}")
        except Exception as exc:
            self._json(400, {"ok": False, "error": str(exc)})


def main() -> int:
    ap = argparse.ArgumentParser(description="Launch RollamacoasterTycoon R3 and collect playtest diagnostics")
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8080)
    ap.add_argument("--no-open", action="store_true", help="do not open a browser automatically")
    args = ap.parse_args()

    artifact = ROOT / ARTIFACT
    if not artifact.exists():
        raise SystemExit(f"Missing {artifact}. Run: python3 build_rct_r3.py")
    SESSIONS.mkdir(exist_ok=True)

    server = ThreadingHTTPServer((args.host, args.port), Handler)
    url = f"http://{args.host}:{args.port}/{ARTIFACT}"
    print("\nROLLAMACOASTERTYCOON!! R3 DEVELOPMENT LOOP")
    print("=" * 52)
    print(f"Game:      {url}")
    print(f"Artifact:  {artifact}")
    print(f"Collector: {SESSIONS}")
    print("Loop:      RELEASE → TEST → COMMENTS → CORE DUMP → REVIEW → PLAN → BUILD → RELEASE")
    print("Stop:      Ctrl+C\n")

    if not args.no_open:
        threading.Timer(0.45, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nDevelopment server stopped.")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

# R3_LOA_DEV25_SERVER_END
