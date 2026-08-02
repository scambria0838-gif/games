# SuperNinja UE5 — Makefile (Sprint 75 task 30, 52)
.PHONY: help start stop status smoke test test-extended test-security test-concurrent bench dashboard

PY := python3

help:
	@echo "Targets:"
	@echo "  start            - start cloud + mock unreal worker"
	@echo "  stop             - stop both services"
	@echo "  status           - show health/metrics"
	@echo "  smoke            - quick alive check"
	@echo "  test             - run all test suites"
	@echo "  test-extended    - extended end-to-end tests"
	@echo "  test-security    - hostile-input tests"
	@echo "  test-concurrent  - throughput / threading test"
	@echo "  bench            - benchmark throughput"
	@echo "  dashboard        - print URL for the live dashboard"

start:
	./start_all.sh

stop:
	./stop_all.sh

status:
	./status.sh

smoke:
	$(PY) test_smoke.py

test:
	$(PY) test_smoke.py
	$(PY) test_e2e_headless.py
	$(PY) test_e2e_extended.py
	$(PY) test_security.py

test-extended:
	$(PY) test_e2e_extended.py

test-security:
	$(PY) test_security.py

test-concurrent:
	$(PY) test_concurrent_clients.py

bench:
	$(PY) bench.py --workers 8 --total 400

dashboard:
	@echo "open ./status.html in a browser (refreshes every 3s)"
