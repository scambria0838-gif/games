# SuperNinja Runbook

## Daily ops

| Action | Command |
|---|---|
| Start everything | `./start_all.sh` |
| Stop everything | `./stop_all.sh` |
| One-screen status | `./status.sh` |
| Smoke test | `python3 test_smoke.py` |
| Full test battery | `./run_all_tests.sh` |
| Live dashboard | open `status.html` in a browser |

## Restart only the cloud server
```bash
supervisorctl restart 8791_python
```

## Restart only the mock Unreal worker
```bash
supervisorctl restart 8765_python3
```

## Rotate a config knob

Set in `/etc/supervisor/conf.d/8791_python.conf` or in the shell when
launching manually:

```bash
PORT=8791                  # listen port
SN_API_KEY=secret          # require X-API-Key on every POST
SN_RATE_LIMIT=0            # disable per-IP rate limit
SN_LOG_LEVEL=DEBUG         # increase verbosity
SN_LOG_DIR=/var/log/superninja
```

Then `supervisorctl restart 8791_python`.

## Viewing logs

```bash
python3 sn_logs.py            # live tail of every file
python3 sn_logs.py grep ERROR # all errors
python3 sn_logs.py last 200   # last 200 lines per file
```

Or directly: `/workspace/logs/sn_cloud.log`,
`/var/log/supervisor/8791_python-*.log`.

## Sending an ad-hoc command

```bash
python3 sn_cli.py spawn_actor name=Hero shape=Cube
python3 sn_cli.py status
python3 sn_cli.py exec "make it brighter and place a police station"
python3 sn_cli.py repl   # interactive REPL
```

## Backing up a scene

```bash
python3 sn_cli.py export_scene_json | tee scene_$(date +%F).json
```

Or via the worker side:
```bash
python3 sn_cli.py save_to_file path=/workspace/scenes/$(date +%F).json
```

## Rebuilding the queue after a worker crash

The reaper auto-times out commands that were pulled but not ack'd within
60s (`commands_timed_out` metric). To force a re-enqueue of recent items,
call `/replay` with `last_n`.
