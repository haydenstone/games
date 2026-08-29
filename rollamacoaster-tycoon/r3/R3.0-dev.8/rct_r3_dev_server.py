#!/usr/bin/env python3
"""RollamacoasterTycoon R3 playtest launcher + diagnostics collector.

Serves the exact standalone HTML artifact and captures the in-game development
Test Bench POSTs into timestamped session folders. Standard-library only.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import threading
import webbrowser
from datetime import datetime, timezone
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
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


class Handler(SimpleHTTPRequestHandler):
    server_version = "RCT-R3-Dev/1.0"

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
        path = urlparse(self.path).path
        if path == "/":
            self.send_response(HTTPStatus.FOUND)
            self.send_header("Location", f"/{ARTIFACT}")
            self.end_headers()
            return
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
        path = urlparse(self.path).path
        if path not in {"/api/dev/session", "/api/dev/comment", "/api/dev/core-dump", "/api/dev/review-packet"}:
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
