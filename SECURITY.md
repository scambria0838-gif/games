# SuperNinja Security Notes

## Threat model
1. **Malicious client** sending arbitrary payloads to the cloud server.
2. **Network attacker** between client and cloud (mitigated by HTTPS via
   Cloudflare quick tunnel).
3. **Malicious command** trying to escape the worker sandbox (mitigated
   by allowlist + read-only knowledge skills).
4. **Resource-exhaustion attacker** (DoS): oversize bodies, infinite
   batch lists, request flood.

## Mitigations implemented in Sprint 75

| Threat | Mitigation | File / mechanism |
|---|---|---|
| Arbitrary command execution | Allowlist (`ALL_ALLOWED`) at cloud + companion | `superninja_cloud_command_server.py`, `sn_companion_phase2.py` |
| Oversize body DoS | 10 MB cap + content-length validation | `_read_body()` |
| Malformed JSON | strict `json.loads` + `isinstance(dict)` check | `_read_body()` |
| Batch flooding | 200-command max | `_handle_batch_execute()` |
| Per-IP flooding | rolling-window rate limit | `_check_rate_limit()` |
| Authn (optional) | `SN_API_KEY` → `X-API-Key` header | `_check_api_key()` |
| Stuck commands | reaper thread | `_reaper_loop()` |
| Atomic prune races | RLock + atomic dict ops | `queue_lock` |
| Image-file attacks | strict base64 + size cap | `_handle_upload_screenshot()` |
| Silent destructive ops | `clear_scene` requires `confirm=true`; audit log of every enqueue/result/timeout | `command_history`, `_audit_event()` |
| Log disk fill | rotating file handler (10 MB × 5) | `sn_logging.py` |
| Unspecific exceptions | replaced bare `except:` with typed catches | bridge, cloud, companion |

## Hardening recommendations for production

- Set `SN_API_KEY` and serve only over HTTPS.
- Tighten CORS to known origins by editing `_json_response()`.
- Lower `RATE_LIMIT_MAX_REQUESTS` from 1000 to a value matched to real use.
- Run cloud server as non-root (`User=nobody` in supervisor config).
- Mount `/workspace/scenes` and `/workspace/screenshots` read-write but
  with `noexec`.
- Forward `command_history.jsonl` to a SIEM.
