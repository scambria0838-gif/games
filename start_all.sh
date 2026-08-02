#!/bin/bash
# Sprint 75 task 46 — start the full local stack.
set -e
cd "$(dirname "$0")"
echo "🟢 starting cloud server (8791) + mock unreal worker (8765)…"
supervisorctl restart 8791_python 8765_python3
sleep 2
supervisorctl status 8791_python 8765_python3
echo
python3 test_smoke.py
