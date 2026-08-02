"""
SuperNinja natural-language → command translator (Sprint 75 tasks 36-40, 43-45).

Pure-Python, dependency-free pattern matcher that converts a single English
phrase into a list of command dicts in the form:
    {"command": "<skill>", "args": {...}, "confidence": 0.0-1.0}

This is intentionally simple and deterministic; the cloud server uses it
behind /translate. A higher-end LLM-backed translator can replace this later.
"""

from __future__ import annotations

import re
from typing import List, Dict, Any

# ---------------------------------------------------------------------------
# Pattern rules (regex -> handler that returns one or more command dicts).
# ---------------------------------------------------------------------------

PATTERNS = []  # list of (compiled regex, handler)


def _rule(pattern: str):
    def deco(fn):
        PATTERNS.append((re.compile(pattern, re.IGNORECASE), fn))
        return fn
    return deco


def _cmd(name: str, args: dict | None = None, confidence: float = 0.85):
    return {"command": name, "args": args or {}, "confidence": confidence}


# --- Lighting -----------------------------------------------------------------

@_rule(r"\b(make (?:it|scene) (?:brighter|brighter)|brighten|more light|too dark)\b")
def _brighter(m, text):
    return [_cmd("light_scene", {"preset": "cinematic", "intensity_boost": 1.5}, 0.9)]


@_rule(r"\b(make (?:it|scene) (?:darker)|dim(?:mer)?|less light|too bright)\b")
def _darker(m, text):
    return [_cmd("light_scene", {"preset": "noir", "intensity_boost": 0.6}, 0.9)]


@_rule(r"\b(sun(?:ny|set|rise)?|daylight|outdoor lighting)\b")
def _sun(m, text):
    return [_cmd("light_scene", {"preset": "daylight"}, 0.85)]


@_rule(r"\b(night ?time|nighttime|moonlit|midnight)\b")
def _night(m, text):
    return [_cmd("light_scene", {"preset": "night"}, 0.85)]


# --- Spawn / scatter ----------------------------------------------------------

_OBJECT_TO_MESH = {
    "police station": "/Game/Buildings/PoliceStation",
    "house": "/Game/Buildings/House",
    "tree": "/Game/Foliage/Tree",
    "rock": "/Game/Foliage/Rock",
    "car": "/Game/Vehicles/Car",
    "lamp": "/Game/Props/Lamp",
    "barrel": "/Game/Props/Barrel",
    "cube": "/Engine/BasicShapes/Cube",
    "sphere": "/Engine/BasicShapes/Sphere",
}


@_rule(r"\b(?:place|spawn|add|put)\s+(?:a |an |the )?([a-z ]+?)(?:\s+(?:at|on|in)\b|\s*$)")
def _place(m, text):
    obj = m.group(1).strip().lower()
    # normalize: drop trailing "here", "there"
    obj = re.sub(r"\b(here|there|please)\b", "", obj).strip()
    mesh = _OBJECT_TO_MESH.get(obj)
    if not mesh:
        # closest single-word match
        for key, val in _OBJECT_TO_MESH.items():
            if key in obj or obj in key:
                mesh = val
                break
    if not mesh:
        return []
    return [_cmd("spawn_actor", {"mesh_path": mesh, "name": obj.replace(" ", "_")}, 0.8)]


@_rule(r"\b(?:scatter|sprinkle|distribute)\s+(\d+)?\s*([a-z ]+?)\b")
def _scatter(m, text):
    count = int(m.group(1) or "20")
    obj = m.group(2).strip().lower()
    mesh = _OBJECT_TO_MESH.get(obj)
    if not mesh:
        for key, val in _OBJECT_TO_MESH.items():
            if key in obj or obj in key:
                mesh = val
                break
    if not mesh:
        return []
    return [_cmd("scatter_props", {"mesh_path": mesh, "count": min(count, 200),
                                   "radius": 2000.0}, 0.85)]


# --- Forest / city / batch shortcuts ------------------------------------------

@_rule(r"\b(?:build|make|create)\s+(?:me\s+)?(?:a\s+)?forest\b")
def _forest(m, text):
    return [_cmd("scatter_props",
                 {"mesh_path": "/Game/Foliage/Tree", "count": 50, "radius": 3000.0},
                 0.9),
            _cmd("scatter_props",
                 {"mesh_path": "/Game/Foliage/Rock", "count": 20, "radius": 3000.0},
                 0.85),
            _cmd("light_scene", {"preset": "daylight"}, 0.8)]


@_rule(r"\b(?:build|make|create)\s+(?:me\s+)?(?:a\s+)?(?:small\s+)?(?:city|town|village)\b")
def _city(m, text):
    return [_cmd("scatter_props",
                 {"mesh_path": "/Game/Buildings/House", "count": 30, "radius": 4000.0},
                 0.85),
            _cmd("spawn_actor",
                 {"mesh_path": "/Game/Buildings/PoliceStation", "name": "PoliceStation_HQ"},
                 0.8)]


# --- Scene management ---------------------------------------------------------

@_rule(r"\b(?:clear|wipe|empty|reset)\s+(?:the\s+)?scene\b")
def _clear(m, text):
    return [_cmd("clear_scene", {"confirm": True}, 0.9)]


@_rule(r"\b(?:undo|revert|take that back)\b")
def _undo(m, text):
    return [_cmd("undo_last_command", {}, 0.95)]


@_rule(r"\b(?:save\s+(?:the\s+)?scene|save\s+to\s+file)\b")
def _save(m, text):
    return [_cmd("save_to_file", {"path": "scene.json"}, 0.85)]


@_rule(r"\b(?:load\s+(?:the\s+)?scene|load\s+from\s+file)\b")
def _load(m, text):
    return [_cmd("load_from_file", {"path": "scene.json"}, 0.85)]


@_rule(r"\b(?:describe|summari[sz]e|what(?:'s| is)\s+in)\s+(?:the\s+)?scene\b")
def _describe(m, text):
    return [_cmd("explain_scene", {}, 0.9)]


@_rule(r"\b(?:take\s+a?\s*screenshot|capture(?:\s+the)?\s+viewport|snap\s+a\s+pic)\b")
def _shot(m, text):
    return [_cmd("take_screenshot", {}, 0.95)]


# --- Camera -------------------------------------------------------------------

@_rule(r"\b(?:frame|focus|look at)\s+(?:the\s+)?(.+?)\b")
def _frame(m, text):
    target = m.group(1).strip().lower()
    return [_cmd("frame_viewport", {"target": target}, 0.7)]


# --- Public API ---------------------------------------------------------------

def translate(text: str) -> List[Dict[str, Any]]:
    """Translate one phrase into 0..N command dicts."""
    if not isinstance(text, str):
        return []
    text = text.strip()
    if not text:
        return []
    out: List[Dict[str, Any]] = []
    seen = set()
    for rx, handler in PATTERNS:
        m = rx.search(text)
        if m:
            for cmd in handler(m, text):
                key = (cmd["command"], tuple(sorted(cmd.get("args", {}).items(),
                                                    key=lambda kv: kv[0])))
                if key not in seen:
                    seen.add(key)
                    out.append(cmd)
    return out


# Demo when run directly
if __name__ == "__main__":
    samples = [
        "make it brighter",
        "place a police station",
        "build me a forest",
        "describe the scene",
        "scatter 30 trees",
        "take a screenshot",
        "clear the scene",
        "undo",
        "build a small city",
    ]
    for s in samples:
        print(f"{s!r:35s} -> {translate(s)}")
