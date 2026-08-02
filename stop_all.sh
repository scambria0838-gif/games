#!/bin/bash
# Sprint 75 task 47 — graceful stop.
set -e
cd "$(dirname "$0")"
echo "🛑 stopping cloud server + mock unreal worker…"
supervisorctl stop 8791_python 8765_python3 || true
supervisorctl status 8791_python 8765_python3 || true
