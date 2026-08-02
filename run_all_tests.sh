#!/bin/bash
# Sprint 75 task 31 — orchestrate every test suite.
set -e
cd "$(dirname "$0")"
RC=0
echo "==============================="
echo " SuperNinja — Full Test Battery"
echo "==============================="
for t in test_smoke.py test_e2e_headless.py test_e2e_extended.py test_security.py; do
  echo
  echo "--- $t ---"
  python3 "$t" || RC=$?
done
echo
echo "==============================="
echo " Final exit code: $RC"
echo "==============================="
exit $RC
