#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python3 rct_r3_release.py
exec python3 rct_r3_dev_server.py
