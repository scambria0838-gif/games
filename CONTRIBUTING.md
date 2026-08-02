# Contributing to SuperNinja

## Adding a new skill

1. **Pick a name** in snake_case. Avoid collisions with built-ins.
2. **Add a mock implementation** in `sn_mock_unreal.py`:

   ```python
   def skill_my_new_thing(args):
       # validate args
       # mutate SCENE inside SCENE.lock
       _push_undo("my_new_thing", lambda: ...)   # if it changes state
       return _ok({"detail": "..."})

   SKILLS["my_new_thing"] = skill_my_new_thing
   ```

3. **Allowlist it** in `superninja_cloud_command_server.py` →
   `SKILL_COMMANDS`. If destructive, also add to `DESTRUCTIVE_COMMANDS`.

4. **Allowlist it on the companion** in `sn_companion_phase2.py` →
   `ALLOWED_COMMANDS`.

5. **Implement the real version** in `sn_skill_executor.py` or a sibling
   skill module that the in-Unreal client imports.

6. **Document it** in `SKILLS_CATALOG.md`.

7. **Test it** — add a case to `test_e2e_extended.py`:

   ```python
   cid = submit("my_new_thing", {"arg":"value"})
   test("my_new_thing succeeds", lambda: is_success(wait_result(cid)))
   ```

8. Restart the stack: `./start_all.sh && ./run_all_tests.sh`.

## Adding a new HTTP endpoint

- All POSTs go through `_check_api_key()` and `_read_body()`.
- All responses go through `_json_response()` (CORS + security headers).
- Update `API_REFERENCE.md`.

## Coding style

- Python 3.11+. Type hints on new code.
- Specific exceptions only (no bare `except:`).
- Acquire `queue_lock` (RLock) before touching shared state.
- Small functions; one responsibility each.
- Run `python3 -c "import <file>"` after every edit to catch syntax errors.

## Releasing

Bump `VERSION` in `superninja_cloud_command_server.py`, append to
`CHANGELOG.md`, restart, run `./run_all_tests.sh`.
