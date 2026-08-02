#!/bin/bash
# Sprint 75 task 48 — one-screen health snapshot.
set -e
cd "$(dirname "$0")"
echo "================================================================"
echo " SuperNinja Status — $(date '+%Y-%m-%d %H:%M:%S')"
echo "================================================================"
echo
echo "Supervisor:"
supervisorctl status 8791_python 8765_python3 2>&1 | sed 's/^/  /'
echo
echo "Cloud /health:"
curl -s http://localhost:8791/health | python3 -m json.tool | sed 's/^/  /' || echo "  (unreachable)"
echo
echo "Cloud /metrics:"
curl -s http://localhost:8791/metrics | python3 -m json.tool | sed 's/^/  /' || true
echo
echo "Cloud /version:"
curl -s http://localhost:8791/version | python3 -m json.tool | sed 's/^/  /' || true
