#!/bin/bash
# Sprint 75 task 55 — first-run setup.
set -e
cd "$(dirname "$0")"
echo "🔧 SuperNinja setup"
echo "  - python: $(python3 --version 2>&1)"
mkdir -p /workspace/logs /workspace/screenshots /workspace/scenes
chmod +x start_all.sh stop_all.sh status.sh sn_cli.py sn_logs.py 2>/dev/null || true
# Best-effort: install requests for sn_companion
if ! python3 -c "import requests" 2>/dev/null; then
  echo "  - installing 'requests' (optional, only needed by companion)…"
  pip install --quiet requests || true
fi
echo "✅ setup complete. Run: ./start_all.sh"
