# SuperNinja Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `curl /health` returns "OFFLINE" | cloud server crashed | `supervisorctl restart 8791_python`; check `/var/log/supervisor/8791_python-stderr*.log` |
| `commands_timed_out` keeps rising | worker not ack'ing or crashed | Restart `8765_python3`; check that the worker can reach `localhost:8791` |
| `403 command not allowed` | command not in cloud allowlist | Add it to `SKILL_COMMANDS` in `superninja_cloud_command_server.py`, restart |
| `429 Too Many Requests` | per-IP rate limit | export `SN_RATE_LIMIT=0` (dev only) or raise `RATE_LIMIT_MAX_REQUESTS` |
| `503 queue full` | sustained backpressure | Worker is too slow or down. Check `pending_acks`, restart worker. |
| Companion stuck "discovering URL" | tunnel not registered | `curl -X POST .../set_tunnel_url -d '{"tunnel_url":"..."}'`, or set `SN_CLOUD_URL` |
| Screenshot upload fails with 400 | base64 padding wrong | Server uses strict validation (`validate=True`); ensure proper padding |
| `clear_scene` returns `requires confirm=true` | safety guard | Pass `args: {"confirm": true}` |
| Tests pass for echo but real skills hang | worker not connected to cloud | Check `mock_unreal` log; verify `CLOUD_URL` inside `sn_mock_unreal.py` |
| Dashboard shows OFFLINE in browser | CORS or wrong port | Open `status.html` while server runs on 8791; or edit `SERVER` constant in the file |
| `commands_rejected` grows | clients sending bad payloads | Check `/history` for the offending entries; tighten client validation |
| Memory growing slowly | result store retains TTL | Default TTL is 1h; tune `RESULT_TTL_SECONDS` |
| Logs filling disk | rotation disabled | `sn_logging.py` rotates at 10 MB by default; verify `SN_LOG_DIR` writable |
| Cannot run UE5 on this VM | no GPU / 3.5GB free disk / 3.8GB RAM | See `UNREAL_ON_VM_RESEARCH.md` — UE5 must run on the user's Windows PC |
