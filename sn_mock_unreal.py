#!/usr/bin/env python3
"""
sn_mock_unreal.py - Headless Unreal Engine simulator for testing SuperNinja
================================================================================

This simulates a real UE5 instance for end-to-end testing of the SuperNinja
pipeline. It plays the role of:
  - sn_local_bridge_phase2.py (HTTP relay on port 8765)
  - sn_unreal_nonblocking_phase2.py (Unreal Python client)

Plus it implements ~30 of our skills as pure-Python fakes that maintain a
"virtual scene" (dict of actors, lights, materials).

Run:
    python3 sn_mock_unreal.py

Then submit commands to http://localhost:8791/enqueue and they will flow:
    Cloud Server -> Companion -> THIS Mock Bridge -> THIS Mock Unreal -> Result
"""

import json
import time
import threading
import http.server
import socketserver
import urllib.request
import urllib.parse
import urllib.error
from collections import deque
from datetime import datetime
import base64
import io
import sys
import math
import random

# ============================================================================
# CONFIG
# ============================================================================

BRIDGE_PORT = 8765
CLOUD_URL = "http://localhost:8791"   # local cloud server
POLL_INTERVAL = 1.0
VERBOSE = True

# ============================================================================
# VIRTUAL SCENE - in-memory state that mimics a UE5 level
# ============================================================================

class VirtualScene:
    """A pure-Python representation of a UE5 level."""

    def __init__(self):
        self.actors = {}           # name -> actor dict
        self.materials = {}        # name -> material dict
        self.lights = {}           # name -> light dict
        self.next_id = 1
        self.lock = threading.RLock()  # reentrant - allows nested acquires

    def _new_name(self, base):
        with self.lock:
            i = 1
            while f"{base}_{i}" in self.actors:
                i += 1
            return f"{base}_{i}"

    def spawn(self, shape="Cube", mesh_path=None, location=None, rotation=None, scale=None, name=None):
        with self.lock:
            actor_name = name or self._new_name(shape)
            actor = {
                "name": actor_name,
                "id": self.next_id,
                "class": "StaticMeshActor",
                "shape": shape,
                "mesh_path": mesh_path or f"/Engine/BasicShapes/{shape}",
                "location": location or [0, 0, 0],
                "rotation": rotation or [0, 0, 0],
                "scale": scale or [1, 1, 1],
                "tags": [],
                "spawned_at": time.time(),
            }
            self.actors[actor_name] = actor
            self.next_id += 1
            return actor

    def delete(self, name):
        with self.lock:
            return self.actors.pop(name, None)

    def move(self, name, location):
        with self.lock:
            if name in self.actors:
                self.actors[name]["location"] = location
                return self.actors[name]
            return None

    def rotate(self, name, rotation):
        with self.lock:
            if name in self.actors:
                self.actors[name]["rotation"] = rotation
                return self.actors[name]
            return None

    def scale(self, name, scale):
        with self.lock:
            if name in self.actors:
                self.actors[name]["scale"] = scale
                return self.actors[name]
            return None

    def list_actors(self):
        with self.lock:
            return list(self.actors.values())

    def add_light(self, light_type, location=None, intensity=5000.0, color=None, name=None):
        with self.lock:
            light_name = name or self._new_name(light_type)
            light = {
                "name": light_name,
                "type": light_type,
                "location": location or [0, 0, 200],
                "intensity": intensity,
                "color": color or [1, 1, 1],
            }
            self.lights[light_name] = light
            self.actors[light_name] = light  # also visible as actor
            return light

    def render_screenshot(self):
        """Render an ASCII top-down screenshot of the scene."""
        with self.lock:
            grid_w, grid_h = 60, 20
            grid = [["." for _ in range(grid_w)] for _ in range(grid_h)]
            scale = 100.0  # 100 cm per cell
            cx, cy = grid_w // 2, grid_h // 2

            for actor in self.actors.values():
                loc = actor.get("location", [0, 0, 0])
                gx = cx + int(loc[0] / scale)
                gy = cy - int(loc[1] / scale)
                if 0 <= gx < grid_w and 0 <= gy < grid_h:
                    char = "#"
                    if "Light" in actor.get("type", "") or "Light" in actor.get("class", ""):
                        char = "*"
                    elif actor.get("shape") == "Sphere":
                        char = "O"
                    elif actor.get("shape") == "Cube":
                        char = "#"
                    elif actor.get("shape") == "Cylinder":
                        char = "I"
                    else:
                        char = "@"
                    grid[gy][gx] = char

            border = "+" + "-" * grid_w + "+"
            lines = [border]
            for row in grid:
                lines.append("|" + "".join(row) + "|")
            lines.append(border)
            lines.append(f"  Actors: {len(self.actors)}  Lights: {len(self.lights)}")
            return "\n".join(lines)


SCENE = VirtualScene()

# Undo stack of (op_name, undo_callable) — most recent last.
UNDO_STACK = deque(maxlen=200)


def _push_undo(name, fn):
    UNDO_STACK.append((name, fn))


# ============================================================================
# SKILL EXECUTOR - mock implementations for ~30 skills
# ============================================================================

def _ok(extra=None):
    r = {"status": "success", "timestamp": time.time()}
    if extra:
        r.update(extra)
    return r

def _err(msg):
    return {"status": "error", "error": msg, "timestamp": time.time()}

def skill_spawn_actor(args):
    shape = args.get("shape", "Cube")
    mesh_path = args.get("mesh_path") or args.get("mesh")
    location = args.get("location") or args.get("loc") or [0, 0, 0]
    rotation = args.get("rotation") or [0, 0, 0]
    scale = args.get("scale") or [1, 1, 1]
    name = args.get("name")
    actor = SCENE.spawn(shape=shape, mesh_path=mesh_path, location=location,
                       rotation=rotation, scale=scale, name=name)
    _push_undo("spawn_actor", lambda n=actor["name"]: SCENE.delete(n))
    return _ok({"actor": actor})

def skill_delete_actor(args):
    name = args.get("name") or args.get("actor_name")
    if not name:
        return _err("name required")
    deleted = SCENE.delete(name)
    if deleted:
        _push_undo("delete_actor",
                   lambda d=dict(deleted): SCENE.actors.__setitem__(d["name"], d))
        return _ok({"deleted": deleted})
    return _err(f"actor not found: {name}")

def skill_move_actor(args):
    name = args.get("name") or args.get("actor_name")
    location = args.get("location") or args.get("loc")
    if not name or location is None:
        return _err("name and location required")
    actor = SCENE.move(name, location)
    return _ok({"actor": actor}) if actor else _err(f"actor not found: {name}")

def skill_rotate_actor(args):
    name = args.get("name")
    rotation = args.get("rotation")
    if not name or rotation is None:
        return _err("name and rotation required")
    a = SCENE.rotate(name, rotation)
    return _ok({"actor": a}) if a else _err(f"actor not found: {name}")

def skill_scale_actor(args):
    name = args.get("name")
    scale = args.get("scale")
    if not name or scale is None:
        return _err("name and scale required")
    a = SCENE.scale(name, scale)
    return _ok({"actor": a}) if a else _err(f"actor not found: {name}")

def skill_list_actors(args):
    actors = SCENE.list_actors()
    return _ok({"actors": actors, "count": len(actors)})

def skill_find_actors(args):
    pattern = (args.get("pattern") or args.get("name") or "").lower()
    actors = [a for a in SCENE.list_actors() if pattern in a["name"].lower()]
    return _ok({"matches": actors, "count": len(actors)})

def skill_add_point_light(args):
    loc = args.get("location") or [0, 0, 300]
    intensity = args.get("intensity", 5000)
    color = args.get("color") or [1, 1, 1]
    light = SCENE.add_light("PointLight", location=loc, intensity=intensity, color=color)
    return _ok({"light": light})

def skill_add_directional_light(args):
    intensity = args.get("intensity", 10)
    color = args.get("color") or [1, 0.95, 0.8]
    light = SCENE.add_light("DirectionalLight", location=[0, 0, 1000],
                           intensity=intensity, color=color)
    return _ok({"light": light})

def skill_add_spot_light(args):
    loc = args.get("location") or [0, 0, 500]
    intensity = args.get("intensity", 8000)
    light = SCENE.add_light("SpotLight", location=loc, intensity=intensity)
    return _ok({"light": light})

def skill_light_scene(args):
    preset = args.get("preset", "cinematic")
    presets = {
        "cinematic": [("DirectionalLight", 5, [1, 0.9, 0.7]),
                     ("PointLight", 3000, [0.3, 0.5, 1])],
        "moody":     [("DirectionalLight", 1, [0.5, 0.4, 0.6]),
                     ("SpotLight", 5000, [1, 0.2, 0.2])],
        "outdoor":   [("DirectionalLight", 12, [1, 1, 0.95])],
        "studio":    [("PointLight", 8000, [1, 1, 1])] * 3,
        "neon":      [("PointLight", 6000, [1, 0, 1]),
                     ("PointLight", 6000, [0, 1, 1])],
        "golden_hour": [("DirectionalLight", 6, [1, 0.7, 0.4])],
    }
    if preset not in presets:
        return _err(f"unknown preset: {preset}")
    added = []
    for kind, intensity, color in presets[preset]:
        light = SCENE.add_light(kind, intensity=intensity, color=color)
        added.append(light)
    return _ok({"preset": preset, "lights_added": added})

def skill_take_screenshot(args):
    img_text = SCENE.render_screenshot()
    encoded = base64.b64encode(img_text.encode()).decode()
    return _ok({
        "screenshot_format": "ascii",
        "screenshot_b64": encoded,
        "preview": img_text,
    })

def skill_scatter_props(args):
    count = args.get("count", 10)
    radius = args.get("radius", 1000)
    shapes = args.get("shapes") or ["Cube", "Sphere", "Cylinder"]
    spawned = []
    for _ in range(count):
        x = random.uniform(-radius, radius)
        y = random.uniform(-radius, radius)
        shape = random.choice(shapes)
        scale = random.uniform(0.5, 2.0)
        actor = SCENE.spawn(shape=shape, location=[x, y, 0],
                           scale=[scale, scale, scale])
        spawned.append(actor["name"])
    return _ok({"spawned_count": len(spawned), "names": spawned})

def skill_add_foliage(args):
    count = args.get("count", 50)
    radius = args.get("radius", 2000)
    spawned = []
    for _ in range(count):
        x = random.uniform(-radius, radius)
        y = random.uniform(-radius, radius)
        scale = random.uniform(0.7, 1.4)
        rotation = [0, 0, random.uniform(0, 360)]
        actor = SCENE.spawn(shape="Foliage", location=[x, y, 0],
                           scale=[scale, scale, scale], rotation=rotation)
        spawned.append(actor["name"])
    return _ok({"foliage_count": len(spawned)})

def skill_cleanup_duplicates(args):
    dry_run = args.get("dry_run", True)
    seen = {}
    dupes = []
    for actor in SCENE.list_actors():
        key = (actor.get("shape"), tuple(actor.get("location", [0, 0, 0])))
        if key in seen:
            dupes.append(actor["name"])
        else:
            seen[key] = actor["name"]
    if not dry_run:
        for name in dupes:
            SCENE.delete(name)
    return _ok({"dry_run": dry_run, "duplicates_found": len(dupes), "names": dupes})

def skill_run_python_snippet(args):
    code = args.get("code", "")
    if not code:
        return _err("code required")
    # Execute safely with scene access
    local_ns = {"SCENE": SCENE, "result": None}
    captured = io.StringIO()
    old_stdout = sys.stdout
    try:
        sys.stdout = captured
        exec(code, {"__builtins__": __builtins__}, local_ns)
        return _ok({"stdout": captured.getvalue(), "result": str(local_ns.get("result"))})
    except Exception as e:
        return _err(f"{type(e).__name__}: {e}")
    finally:
        sys.stdout = old_stdout

def skill_get_actor_properties(args):
    name = args.get("name")
    if not name or name not in SCENE.actors:
        return _err(f"actor not found: {name}")
    return _ok({"actor": SCENE.actors[name]})

def skill_set_actor_property(args):
    name = args.get("name")
    prop = args.get("property")
    value = args.get("value")
    if not name or not prop:
        return _err("name and property required")
    if name not in SCENE.actors:
        return _err(f"actor not found: {name}")
    SCENE.actors[name][prop] = value
    return _ok({"actor": SCENE.actors[name]})

def skill_echo(args):
    return _ok({"echo": args})

def skill_chat(args):
    msg = args.get("message", "")
    return _ok({"reply": f"[mock-unreal] heard: {msg}"})

def skill_ask_user(args):
    return _ok({"question": args.get("question", ""), "note": "mock auto-acknowledged"})


SKILLS = {
    "spawn_actor": skill_spawn_actor,
    "delete_actor": skill_delete_actor,
    "move_actor": skill_move_actor,
    "rotate_actor": skill_rotate_actor,
    "scale_actor": skill_scale_actor,
    "list_actors": skill_list_actors,
    "find_actors": skill_find_actors,
    "add_point_light": skill_add_point_light,
    "add_directional_light": skill_add_directional_light,
    "add_spot_light": skill_add_spot_light,
    "light_scene": skill_light_scene,
    "take_screenshot": skill_take_screenshot,
    "screenshot": skill_take_screenshot,
    "scatter_props": skill_scatter_props,
    "add_foliage": skill_add_foliage,
    "cleanup_duplicates": skill_cleanup_duplicates,
    "delete_duplicates": skill_cleanup_duplicates,
    "run_python_snippet": skill_run_python_snippet,
    "get_actor_properties": skill_get_actor_properties,
    "set_actor_property": skill_set_actor_property,
    "echo": skill_echo,
    "chat": skill_chat,
    "ask_user": skill_ask_user,
}


# ============================================================================
# Sprint 75 Group G — new skills
# ============================================================================

import os as _os


def skill_save_to_file(args):
    """Persist the virtual scene to a JSON file."""
    path = args.get("path") or "scene.json"
    with SCENE.lock:
        data = {
            "version": 1,
            "saved_at": time.time(),
            "actors": list(SCENE.actors.values()),
            "lights": list(SCENE.lights.values()),
            "next_id": SCENE.next_id,
        }
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, default=str)
    except OSError as e:
        return _err(f"write failed: {e}")
    return _ok({"path": _os.path.abspath(path),
                "actors": len(data["actors"]),
                "lights": len(data["lights"])})


def skill_load_from_file(args):
    path = args.get("path") or "scene.json"
    if not _os.path.exists(path):
        return _err(f"file not found: {path}")
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        return _err(f"read failed: {e}")
    with SCENE.lock:
        SCENE.actors.clear()
        SCENE.lights.clear()
        for a in data.get("actors", []):
            if isinstance(a, dict) and a.get("name"):
                SCENE.actors[a["name"]] = a
        for l in data.get("lights", []):
            if isinstance(l, dict) and l.get("name"):
                SCENE.lights[l["name"]] = l
                SCENE.actors[l["name"]] = l
        SCENE.next_id = max(int(data.get("next_id", 1)),
                            len(SCENE.actors) + 1)
    return _ok({"loaded": True, "actors": len(SCENE.actors),
                "lights": len(SCENE.lights)})


def skill_clear_scene(args):
    if not args.get("confirm"):
        return _err("clear_scene requires confirm=true")
    with SCENE.lock:
        snapshot = (dict(SCENE.actors), dict(SCENE.lights), SCENE.next_id)
        SCENE.actors.clear()
        SCENE.lights.clear()
        SCENE.next_id = 1

    def _undo():
        with SCENE.lock:
            SCENE.actors.update(snapshot[0])
            SCENE.lights.update(snapshot[1])
            SCENE.next_id = snapshot[2]
    _push_undo("clear_scene", _undo)
    return _ok({"cleared": True})


def skill_undo_last_command(args):
    if not UNDO_STACK:
        return _ok({"undone": False, "reason": "stack empty"})
    name, fn = UNDO_STACK.pop()
    try:
        fn()
    except Exception as e:
        return _err(f"undo of {name} failed: {e}")
    return _ok({"undone": True, "operation": name,
                "stack_remaining": len(UNDO_STACK)})


def skill_export_scene_json(args):
    with SCENE.lock:
        return _ok({
            "scene": {
                "version": 1,
                "actors": list(SCENE.actors.values()),
                "lights": list(SCENE.lights.values()),
            },
            "actor_count": len(SCENE.actors),
            "light_count": len(SCENE.lights),
        })


def skill_import_scene_json(args):
    scene = args.get("scene") or {}
    actors = scene.get("actors", [])
    lights = scene.get("lights", [])
    if not isinstance(actors, list) or not isinstance(lights, list):
        return _err("scene.actors/lights must be lists")
    imported = 0
    with SCENE.lock:
        for a in actors:
            if isinstance(a, dict) and a.get("name"):
                SCENE.actors[a["name"]] = a
                imported += 1
        for l in lights:
            if isinstance(l, dict) and l.get("name"):
                SCENE.lights[l["name"]] = l
                SCENE.actors[l["name"]] = l
                imported += 1
    return _ok({"imported": imported})


def skill_export_screenshot_png(args):
    """Write a tiny real PNG of the ASCII scene grid (no external deps)."""
    path = args.get("path") or f"/workspace/screenshots/screenshot_{int(time.time())}.png"
    try:
        _os.makedirs(_os.path.dirname(path) or ".", exist_ok=True)
    except OSError:
        pass
    # Rasterize the ASCII grid to a 1-bit PNG via stdlib only.
    grid_lines = SCENE.render_screenshot().split("\n")
    h = len(grid_lines)
    w = max(len(l) for l in grid_lines)
    # Each cell -> 4x4 px block.
    cell = 4
    img_w, img_h = w * cell, h * cell
    # Build raw RGB bytes
    pixels = bytearray()
    for row in range(img_h):
        line_idx = row // cell
        line = grid_lines[line_idx] if line_idx < h else ""
        line = line.ljust(w)
        # PNG scanlines start with filter byte 0
        pixels.append(0)
        for col in range(img_w):
            ch = line[col // cell] if (col // cell) < len(line) else " "
            if ch in ("#", "@", "I", "O"):
                pixels += b"\x20\x80\xff"      # actor: blue-ish
            elif ch == "*":
                pixels += b"\xff\xe0\x40"      # light: yellow
            elif ch in ("+", "-", "|"):
                pixels += b"\x40\x40\x40"      # border: dark
            else:
                pixels += b"\x10\x18\x28"      # background: navy
    # Now encode minimal PNG
    import struct, zlib
    def chunk(tag, data):
        return (struct.pack(">I", len(data)) + tag + data
                + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF))
    sig = b"\x89PNG\r\n\x1a\n"
    ihdr = struct.pack(">IIBBBBB", img_w, img_h, 8, 2, 0, 0, 0)  # 8-bit RGB
    idat = zlib.compress(bytes(pixels), 6)
    png = sig + chunk(b"IHDR", ihdr) + chunk(b"IDAT", idat) + chunk(b"IEND", b"")
    try:
        with open(path, "wb") as f:
            f.write(png)
    except OSError as e:
        return _err(f"write failed: {e}")
    return _ok({"path": path, "width": img_w, "height": img_h,
                "size_bytes": len(png)})


SKILLS.update({
    "save_to_file": skill_save_to_file,
    "load_from_file": skill_load_from_file,
    "clear_scene": skill_clear_scene,
    "undo_last_command": skill_undo_last_command,
    "export_scene_json": skill_export_scene_json,
    "import_scene_json": skill_import_scene_json,
    "export_screenshot_png": skill_export_screenshot_png,
})


def execute_skill(skill_name, args):
    fn = SKILLS.get(skill_name)
    if fn is None:
        return _ok({
            "skill": skill_name,
            "note": "skill not implemented in mock - would normally run on Unreal",
            "args_received": args,
        })
    try:
        return fn(args or {})
    except Exception as e:
        return _err(f"{type(e).__name__}: {e}")


# ============================================================================
# WORKER - polls cloud server for commands and executes them
# ============================================================================

def log(msg):
    if VERBOSE:
        ts = datetime.now().strftime("%H:%M:%S")
        print(f"[{ts}] {msg}", flush=True)


def http_get(url, timeout=5):
    try:
        with urllib.request.urlopen(url, timeout=timeout) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        return {"_http_error": e.code}
    except Exception as e:
        return {"_error": str(e)}


def http_post(url, data, timeout=5):
    body = json.dumps(data).encode()
    req = urllib.request.Request(url, data=body, method="POST",
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        return {"_http_error": e.code, "body": e.read().decode()}
    except Exception as e:
        return {"_error": str(e)}


WORKER_RUNNING = True
COMMANDS_PROCESSED = 0
LAST_COMMAND = None


def worker_loop():
    global COMMANDS_PROCESSED, LAST_COMMAND
    log(f"Worker started, polling {CLOUD_URL}/poll every {POLL_INTERVAL}s")
    consecutive_errors = 0
    iteration = 0

    while WORKER_RUNNING:
        iteration += 1
        try:
            poll_result = http_get(f"{CLOUD_URL}/poll", timeout=5)

            if "_error" in poll_result or "_http_error" in poll_result:
                consecutive_errors += 1
                backoff = min(POLL_INTERVAL * (2 ** min(consecutive_errors - 1, 4)), 30.0)
                log(f"Poll error: {poll_result} (retry in {backoff:.0f}s)")
                time.sleep(backoff)
                continue

            consecutive_errors = 0

            cmd = poll_result.get("command")
            if not cmd:
                time.sleep(POLL_INTERVAL)
                continue

            cmd_id = cmd.get("id") or cmd.get("command_id") or "unknown"
            skill_name = cmd.get("command") or cmd.get("skill") or cmd.get("name")
            args = cmd.get("args") or {}

            log(f"--> [{cmd_id[:20]}] skill={skill_name} args={json.dumps(args)[:80]}")
            LAST_COMMAND = {"id": cmd_id, "skill": skill_name, "args": args}

            t0 = time.time()
            try:
                result = execute_skill(skill_name, args)
            except Exception as e:
                import traceback
                log(f"!! execute_skill threw: {type(e).__name__}: {e}")
                log(traceback.format_exc())
                result = _err(f"executor exception: {type(e).__name__}: {e}")
            elapsed_ms = int((time.time() - t0) * 1000)

            log(f"<-- [{cmd_id[:20]}] status={result.get('status')} ({elapsed_ms}ms)")

            # Post result back to cloud server
            payload = {
                "id": cmd_id,
                "command_id": cmd_id,
                "command": skill_name,
                "result": result,
                "elapsed_ms": elapsed_ms,
            }
            try:
                post_resp = http_post(f"{CLOUD_URL}/result", payload, timeout=5)
                if "_error" in post_resp or "_http_error" in post_resp:
                    log(f"!! Failed to post result: {post_resp}")
                else:
                    COMMANDS_PROCESSED += 1
            except Exception as e:
                log(f"!! post exception: {type(e).__name__}: {e}")

            time.sleep(0.05)

        except Exception as e:
            import traceback
            log(f"!! Worker outer exception: {type(e).__name__}: {e}")
            log(traceback.format_exc())
            time.sleep(POLL_INTERVAL)

    log("Worker loop exited")


# ============================================================================
# OPTIONAL: local bridge HTTP server (so companion-style polling also works)
# ============================================================================

class BridgeHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, *args, **kwargs):
        pass  # silence default logging

    def _json(self, code, data):
        body = json.dumps(data).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/health":
            self._json(200, {
                "status": "healthy",
                "service": "sn_mock_unreal",
                "actors": len(SCENE.actors),
                "lights": len(SCENE.lights),
                "commands_processed": COMMANDS_PROCESSED,
                "last_command": LAST_COMMAND,
            })
        elif self.path == "/scene":
            self._json(200, {
                "actors": SCENE.list_actors(),
                "lights": list(SCENE.lights.values()),
            })
        elif self.path == "/screenshot":
            self._json(200, {"preview": SCENE.render_screenshot()})
        else:
            self._json(404, {"error": "not found"})

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode() if length else "{}"
        try:
            data = json.loads(body)
        except Exception:
            return self._json(400, {"error": "bad json"})

        if self.path == "/execute":
            skill = data.get("skill") or data.get("command")
            args = data.get("args", {})
            result = execute_skill(skill, args)
            self._json(200, result)
        else:
            self._json(404, {"error": "not found"})


def run_bridge():
    server = http.server.ThreadingHTTPServer(("127.0.0.1", BRIDGE_PORT), BridgeHandler)
    log(f"Mock bridge listening on http://127.0.0.1:{BRIDGE_PORT}")
    server.serve_forever()


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print(" SuperNinja MOCK UNREAL - Headless test harness")
    print("=" * 70)
    print(f" Cloud server : {CLOUD_URL}")
    print(f" Bridge port  : {BRIDGE_PORT}")
    print(f" Skills       : {len(SKILLS)} mock skills implemented")
    print(f" Polling      : every {POLL_INTERVAL}s")
    print("=" * 70)
    print()

    # Start bridge in a thread
    bridge_thread = threading.Thread(target=run_bridge, daemon=True)
    bridge_thread.start()

    # Start worker in a thread
    worker_thread = threading.Thread(target=worker_loop, daemon=True)
    worker_thread.start()

    try:
        while True:
            time.sleep(60)
            log(f"Heartbeat - actors={len(SCENE.actors)} processed={COMMANDS_PROCESSED}")
    except KeyboardInterrupt:
        WORKER_RUNNING = False
        log("Shutting down...")
