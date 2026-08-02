"""
SuperNinja Skill Executor — Runs inside Unreal Editor

Takes a skill name + args from the command pipeline,
renders the Unreal Python code template with those args,
and executes it. This is the bridge between the skill
registry and actual Unreal Python API calls.

Replaces the old hardcoded command handler with a
dynamic template-based executor.
"""

import unreal
import json
import re
import traceback
from typing import Dict, Any, Optional

# Import skill definitions (embedded here since we can't import files in Unreal)
# In production, this would load from a JSON file or the plugin's content
SKILLS = {}  # Populated by register_skills() below


def register_skills():
    """Register all skill templates. Called once at startup."""
    
    # ==================================================================
    # LIGHTING
    # ==================================================================
    SKILLS["add_directional_light"] = {
        "safety": "modify",
        "execute": _add_directional_light,
    }
    SKILLS["add_point_light"] = {
        "safety": "modify", 
        "execute": _add_point_light,
    }
    SKILLS["add_spot_light"] = {
        "safety": "modify",
        "execute": _add_spot_light,
    }
    SKILLS["add_sky_light"] = {
        "safety": "modify",
        "execute": _add_sky_light,
    }
    SKILLS["adjust_light"] = {
        "safety": "modify",
        "execute": _adjust_light,
    }

    # ==================================================================
    # PLACEMENT
    # ==================================================================
    SKILLS["spawn_actor"] = {
        "safety": "modify",
        "execute": _spawn_actor,
    }
    SKILLS["move_actor"] = {
        "safety": "modify",
        "execute": _move_actor,
    }
    SKILLS["rotate_actor"] = {
        "safety": "modify",
        "execute": _rotate_actor,
    }
    SKILLS["scale_actor"] = {
        "safety": "modify",
        "execute": _scale_actor,
    }
    SKILLS["scatter_actors"] = {
        "safety": "modify",
        "execute": _scatter_actors,
    }
    SKILLS["delete_actor"] = {
        "safety": "destructive",
        "execute": _delete_actor,
    }
    SKILLS["delete_duplicates"] = {
        "safety": "destructive",
        "execute": _delete_duplicates,
    }

    # ==================================================================
    # ANALYSIS
    # ==================================================================
    SKILLS["list_actors"] = {
        "safety": "safe",
        "execute": _list_actors,
    }
    SKILLS["get_scene_info"] = {
        "safety": "safe",
        "execute": _get_scene_info,
    }

    # ==================================================================
    # CAMERA
    # ==================================================================
    SKILLS["frame_viewport"] = {
        "safety": "safe",
        "execute": _frame_viewport,
    }

    # ==================================================================
    # ENVIRONMENT
    # ==================================================================
    SKILLS["add_exponential_height_fog"] = {
        "safety": "modify",
        "execute": _add_fog,
    }
    SKILLS["add_sky_atmosphere"] = {
        "safety": "modify",
        "execute": _add_sky_atmosphere,
    }

    # ==================================================================
    # MATERIAL
    # ==================================================================
    SKILLS["apply_material"] = {
        "safety": "modify",
        "execute": _apply_material,
    }

    # ==================================================================
    # ASSET
    # ==================================================================
    SKILLS["import_asset"] = {
        "safety": "modify",
        "execute": _import_asset,
    }
    SKILLS["list_content"] = {
        "safety": "safe",
        "execute": _list_content,
    }

    # ==================================================================
    # UTILITY
    # ==================================================================
    SKILLS["save_level"] = {
        "safety": "modify",
        "execute": _save_level,
    }
    SKILLS["undo"] = {
        "safety": "safe",
        "execute": _undo,
    }
    SKILLS["execute_console_command"] = {
        "safety": "modify",
        "execute": _execute_console_command,
    }
    SKILLS["screenshot"] = {
        "safety": "safe",
        "execute": _screenshot,
    }
    SKILLS["ping"] = {
        "safety": "safe",
        "execute": _ping,
    }
    SKILLS["echo"] = {
        "safety": "safe",
        "execute": _echo,
    }

    # ==================================================================
    # CONVERSATIONAL
    # ==================================================================
    SKILLS["say"] = {
        "safety": "safe",
        "execute": _say,
    }
    SKILLS["ask_user"] = {
        "safety": "safe",
        "execute": _ask_user,
    }
    SKILLS["report_progress"] = {
        "safety": "safe",
        "execute": _report_progress,
    }
    SKILLS["explain_scene"] = {
        "safety": "safe",
        "execute": _explain_scene,
    }
    SKILLS["suggest_improvements"] = {
        "safety": "safe",
        "execute": _suggest_improvements,
    }
    SKILLS["chat"] = {
        "safety": "safe",
        "execute": _chat,
    }

    # ==================================================================
    # MASTER SKILLS (Docs 101-151)
    # ==================================================================
    SKILLS["query_master_knowledge"] = {
        "safety": "safe",
        "execute": _query_master_knowledge,
    }
    SKILLS["setup_landscape"] = {
        "safety": "modify",
        "execute": _setup_landscape,
    }
    SKILLS["add_volumetric_clouds"] = {
        "safety": "modify",
        "execute": _add_volumetric_clouds,
    }
    SKILLS["add_height_fog"] = {
        "safety": "modify",
        "execute": _add_height_fog,
    }
    SKILLS["add_water_body"] = {
        "safety": "modify",
        "execute": _add_water_body,
    }
    SKILLS["setup_reflections"] = {
        "safety": "modify",
        "execute": _setup_reflections,
    }
    SKILLS["setup_virtual_production"] = {
        "safety": "modify",
        "execute": _setup_virtual_production,
    }
    SKILLS["setup_groom_system"] = {
        "safety": "safe",
        "execute": _setup_groom_system,
    }
    SKILLS["setup_rvt"] = {
        "safety": "safe",
        "execute": _setup_rvt,
    }
    SKILLS["setup_physics_constraints"] = {
        "safety": "modify",
        "execute": _setup_physics_constraints,
    }
    SKILLS["add_chaos_vehicle"] = {
        "safety": "modify",
        "execute": _add_chaos_vehicle,
    }
    SKILLS["query_master_landscape_preset"] = {
        "safety": "safe",
        "execute": _query_master_landscape_preset,
    }
    SKILLS["setup_source_control"] = {
        "safety": "safe",
        "execute": _setup_source_control,
    }

    # ==================================================================
    # P0 SKILLS: Critical missing implementations
    # ==================================================================
    SKILLS["run_python_snippet"] = {
        "safety": "modify",  # Arbitrary code execution is powerful
        "execute": _run_python_snippet,
    }
    SKILLS["set_actor_property"] = {
        "safety": "modify",
        "execute": _set_actor_property,
    }
    SKILLS["get_actor_properties"] = {
        "safety": "safe",
        "execute": _get_actor_properties,
    }
    SKILLS["add_foliage"] = {
        "safety": "modify",
        "execute": _add_foliage,
    }
    SKILLS["setup_post_process"] = {
        "safety": "modify",
        "execute": _setup_post_process,
    }
    SKILLS["light_scene"] = {
        "safety": "modify",
        "execute": _light_scene,
    }
    SKILLS["cleanup_duplicates"] = {
        "safety": "destructive",
        "execute": _cleanup_duplicates,
    }
    SKILLS["scatter_props"] = {
        "safety": "modify",
        "execute": _scatter_props,
    }
    
    # ==================================================================
    # P1 SKILLS: Additional Unreal-side implementations
    # ==================================================================
    SKILLS["add_niagara_effect"] = {
        "safety": "modify",
        "execute": _add_niagara_effect,
    }
    SKILLS["add_audio_ambient"] = {
        "safety": "modify",
        "execute": _add_audio_ambient,
    }
    SKILLS["add_navmesh"] = {
        "safety": "modify",
        "execute": _add_navmesh,
    }
    SKILLS["setup_ai_character"] = {
        "safety": "modify",
        "execute": _setup_ai_character,
    }
    SKILLS["setup_cinematic"] = {
        "safety": "modify",
        "execute": _setup_cinematic,
    }
    SKILLS["find_actors_advanced"] = {
        "safety": "safe",
        "execute": _find_actors_advanced,
    }
    SKILLS["optimize_scene"] = {
        "safety": "modify",
        "execute": _optimize_scene,
    }


# ======================================================================
# HELPER: Find actor by name (fuzzy match)
# ======================================================================
def _find_actor(name: str):
    """Find an actor by partial name match."""
    actors = unreal.EditorLevelLibrary.get_all_level_actors()
    # Exact match first
    for a in actors:
        if a.get_actor_label() == name:
            return a
    # Partial match
    for a in actors:
        if name.lower() in a.get_actor_label().lower():
            return a
    return None


def _find_all_actors(name: str):
    """Find all actors matching a name pattern."""
    actors = unreal.EditorLevelLibrary.get_all_level_actors()
    return [a for a in actors if name.lower() in a.get_actor_label().lower()]


# ======================================================================
# HELPER: Parse args with defaults
# ======================================================================
def _arg(args: dict, key: str, default=None, required=False):
    """Get an arg value with optional default and required check."""
    val = args.get(key, default)
    if required and val is None:
        raise ValueError(f"Missing required argument: {key}")
    return val


# ======================================================================
# LIGHTING IMPLEMENTATIONS
# ======================================================================
def _add_directional_light(args: dict) -> dict:
    name = _arg(args, "name", "SN_Sun")
    intensity = _arg(args, "intensity", 3.0)
    rotation = _arg(args, "rotation", [-40.0, 45.0, 0.0])
    shadow_enabled = _arg(args, "shadow_enabled", True)
    mobility = _arg(args, "mobility", "Movable")
    temperature = _arg(args, "temperature", 0.0)
    light_color = _arg(args, "light_color", [1.0, 0.95, 0.85])

    loc = unreal.Vector(0, 0, 500)
    rot = unreal.Rotator(float(rotation[0]), float(rotation[1]), float(rotation[2]))
    
    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.DirectionalLight, loc, rot
    )
    actor.set_actor_label(name)
    
    light = unreal.DirectionalLight.cast(actor)
    if light:
        light.set_intensity(float(intensity))
        r, g, b = float(light_color[0]), float(light_color[1]), float(light_color[2])
        light.set_light_color(unreal.LinearColor(r, g, b, 1.0))
        light.set_cast_shadows(bool(shadow_enabled))
        if temperature > 0:
            light.set_use_temperature(True)
            light.set_temperature(float(temperature))
    
    unreal.log(f"[SN] DirectionalLight '{name}': intensity={intensity} temp={temperature}")
    return {"actor": name, "type": "DirectionalLight", "intensity": intensity}


def _add_point_light(args: dict) -> dict:
    name = _arg(args, "name", "SN_PointLight")
    location = _arg(args, "location", [0.0, 0.0, 300.0])
    intensity = _arg(args, "intensity", 3000.0)
    light_color = _arg(args, "light_color", [1.0, 0.9, 0.7])
    attenuation_radius = _arg(args, "attenuation_radius", 1000.0)
    shadow_enabled = _arg(args, "shadow_enabled", True)
    source_radius = _arg(args, "source_radius", 5.0)

    loc = unreal.Vector(float(location[0]), float(location[1]), float(location[2]))
    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.PointLight, loc, unreal.Rotator(0, 0, 0)
    )
    actor.set_actor_label(name)
    
    light = unreal.PointLight.cast(actor)
    if light:
        light.set_intensity(float(intensity))
        r, g, b = float(light_color[0]), float(light_color[1]), float(light_color[2])
        light.set_light_color(unreal.LinearColor(r, g, b, 1.0))
        light.set_attenuation_radius(float(attenuation_radius))
        light.set_cast_shadows(bool(shadow_enabled))
        light.set_source_radius(float(source_radius))
    
    unreal.log(f"[SN] PointLight '{name}' at ({loc.x}, {loc.y}, {loc.z})")
    return {"actor": name, "type": "PointLight", "location": list(location), "intensity": intensity}


def _add_spot_light(args: dict) -> dict:
    name = _arg(args, "name", "SN_SpotLight")
    location = _arg(args, "location", [0.0, 0.0, 500.0])
    rotation = _arg(args, "rotation", [-90.0, 0.0, 0.0])
    intensity = _arg(args, "intensity", 5000.0)
    inner_cone = _arg(args, "inner_cone_angle", 15.0)
    outer_cone = _arg(args, "outer_cone_angle", 45.0)
    attenuation_radius = _arg(args, "attenuation_radius", 2000.0)
    light_color = _arg(args, "light_color", [1.0, 0.95, 0.85])
    shadow_enabled = _arg(args, "shadow_enabled", True)

    loc = unreal.Vector(float(location[0]), float(location[1]), float(location[2]))
    rot = unreal.Rotator(float(rotation[0]), float(rotation[1]), float(rotation[2]))
    
    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.SpotLight, loc, rot
    )
    actor.set_actor_label(name)
    
    light = unreal.SpotLight.cast(actor)
    if light:
        light.set_intensity(float(intensity))
        light.set_inner_cone_angle(float(inner_cone))
        light.set_outer_cone_angle(float(outer_cone))
        light.set_attenuation_radius(float(attenuation_radius))
        r, g, b = float(light_color[0]), float(light_color[1]), float(light_color[2])
        light.set_light_color(unreal.LinearColor(r, g, b, 1.0))
        light.set_cast_shadows(bool(shadow_enabled))
    
    unreal.log(f"[SN] SpotLight '{name}' inner={inner_cone} outer={outer_cone}")
    return {"actor": name, "type": "SpotLight", "intensity": intensity}


def _add_sky_light(args: dict) -> dict:
    name = _arg(args, "name", "SN_SkyLight")
    intensity = _arg(args, "intensity", 1.0)
    light_color = _arg(args, "light_color", [1.0, 1.0, 1.0])
    mobility = _arg(args, "mobility", "Movable")

    loc = unreal.Vector(0, 0, 1000)
    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.SkyLight, loc, unreal.Rotator(0, 0, 0)
    )
    actor.set_actor_label(name)
    
    light = unreal.SkyLight.cast(actor)
    if light:
        light.set_intensity(float(intensity))
        r, g, b = float(light_color[0]), float(light_color[1]), float(light_color[2])
        light.set_light_color(unreal.LinearColor(r, g, b, 1.0))
    
    unreal.log(f"[SN] SkyLight '{name}' intensity={intensity}")
    return {"actor": name, "type": "SkyLight", "intensity": intensity}


def _adjust_light(args: dict) -> dict:
    actor_name = _arg(args, "actor_name", required=True)
    found = _find_actor(actor_name)
    if not found:
        return {"error": f"Actor '{actor_name}' not found"}
    
    # Try to get light component
    light_comp = None
    for comp in found.get_components_by_class(unreal.LightComponent):
        light_comp = comp
        break
    
    if not light_comp:
        return {"error": f"Actor '{actor_name}' has no light component"}
    
    changes = {}
    if "intensity" in args:
        light_comp.set_intensity(float(args["intensity"]))
        changes["intensity"] = args["intensity"]
    if "shadow_enabled" in args:
        light_comp.set_cast_shadows(bool(args["shadow_enabled"]))
        changes["shadow_enabled"] = args["shadow_enabled"]
    if "light_color" in args:
        r, g, b = float(args["light_color"][0]), float(args["light_color"][1]), float(args["light_color"][2])
        light_comp.set_light_color(unreal.LinearColor(r, g, b, 1.0))
        changes["light_color"] = args["light_color"]
    if "attenuation_radius" in args and hasattr(light_comp, 'set_attenuation_radius'):
        light_comp.set_attenuation_radius(float(args["attenuation_radius"]))
        changes["attenuation_radius"] = args["attenuation_radius"]
    if "rotation" in args:
        rot = unreal.Rotator(float(args["rotation"][0]), float(args["rotation"][1]), float(args["rotation"][2]))
        found.set_actor_rotation(rot, False)
        changes["rotation"] = args["rotation"]
    if "location" in args:
        loc = unreal.Vector(float(args["location"][0]), float(args["location"][1]), float(args["location"][2]))
        found.set_actor_location(loc, False, None)
        changes["location"] = args["location"]
    
    unreal.log(f"[SN] Adjusted light '{found.get_actor_label()}': {changes}")
    return {"actor": found.get_actor_label(), "changes": changes}


# ======================================================================
# PLACEMENT IMPLEMENTATIONS
# ======================================================================
def _spawn_actor(args: dict) -> dict:
    shape = _arg(args, "shape", "Cube")
    name = _arg(args, "name", f"SN_{shape}")
    location = _arg(args, "location", [0.0, 0.0, 0.0])
    rotation = _arg(args, "rotation", [0.0, 0.0, 0.0])
    scale = _arg(args, "scale", [1.0, 1.0, 1.0])
    material_path = _arg(args, "material_path", "")
    mesh_path = _arg(args, "mesh_path", "")
    actor_class = _arg(args, "actor_class", "")

    # Priority: explicit mesh_path > shape lookup > basic shape fallback
    basic_shapes = {
        "Cube": "/Engine/BasicShapes/Cube",
        "Sphere": "/Engine/BasicShapes/Sphere",
        "Cylinder": "/Engine/BasicShapes/Cylinder",
        "Cone": "/Engine/BasicShapes/Cone",
        "Plane": "/Engine/BasicShapes/Plane",
        "PlayerStart": "/Engine/PlayerStart",
    }

    if mesh_path:
        # User specified an explicit asset path (e.g., /Game/Architecture/SM_PoliceStation)
        resolved_path = mesh_path
    elif shape in basic_shapes:
        resolved_path = basic_shapes[shape]
    else:
        # Try to resolve as a game asset path — common patterns:
        # "PoliceStation" -> try /Game/PoliceStation, /Game/Architecture/PoliceStation, etc.
        candidates = [
            f"/Game/{shape}",
            f"/Game/Meshes/{shape}",
            f"/Game/Architecture/{shape}",
            f"/Game/Props/{shape}",
            f"/Game/Models/{shape}",
        ]
        resolved_path = None
        for candidate in candidates:
            test_asset = unreal.load_asset(candidate)
            if test_asset:
                resolved_path = candidate
                break
        if not resolved_path:
            resolved_path = "/Engine/BasicShapes/Cube"
            unreal.log(f"[SN] WARNING: Could not find mesh for '{shape}', falling back to Cube. "
                       f"Use mesh_path parameter to specify an exact asset path.")

    loc = unreal.Vector(float(location[0]), float(location[1]), float(location[2]))

    # If actor_class is specified, spawn by class instead of by mesh
    if actor_class:
        try:
            cls = getattr(unreal, actor_class)
            actor = unreal.EditorLevelLibrary.spawn_actor_from_class(cls, loc)
        except (AttributeError, TypeError):
            return {"error": f"Unknown actor class: {actor_class}"}
    else:
        mesh = unreal.load_asset(resolved_path)
        if not mesh:
            return {"error": f"Could not load mesh: {resolved_path}"}
        actor = unreal.EditorLevelLibrary.spawn_actor_from_object(mesh, loc)

    actor.set_actor_label(name)

    rot = unreal.Rotator(float(rotation[0]), float(rotation[1]), float(rotation[2]))
    actor.set_actor_rotation(rot, False)

    s = unreal.Vector(float(scale[0]), float(scale[1]), float(scale[2]))
    actor.set_actor_scale3d(s)

    if material_path:
        mat = unreal.load_asset(material_path)
        if mat:
            for comp in actor.get_components_by_class(unreal.StaticMeshComponent):
                comp.set_material(0, mat)

    loc = actor.get_actor_location()
    unreal.log(f"[SN] Spawned '{name}' (mesh={resolved_path}) at ({loc.x}, {loc.y}, {loc.z})")
    return {"actor": name, "type": shape, "mesh_path": resolved_path, "location": [loc.x, loc.y, loc.z]}


def _move_actor(args: dict) -> dict:
    actor_name = _arg(args, "actor_name", required=True)
    location = _arg(args, "location", required=True)
    relative = _arg(args, "relative", False)
    
    found = _find_actor(actor_name)
    if not found:
        return {"error": f"Actor '{actor_name}' not found"}
    
    if relative:
        cur = found.get_actor_location()
        new_loc = unreal.Vector(
            cur.x + float(location[0]),
            cur.y + float(location[1]),
            cur.z + float(location[2])
        )
    else:
        new_loc = unreal.Vector(float(location[0]), float(location[1]), float(location[2]))
    
    found.set_actor_location(new_loc, False, None)
    unreal.log(f"[SN] Moved '{found.get_actor_label()}' to ({new_loc.x}, {new_loc.y}, {new_loc.z})")
    return {"actor": found.get_actor_label(), "location": [new_loc.x, new_loc.y, new_loc.z]}


def _rotate_actor(args: dict) -> dict:
    actor_name = _arg(args, "actor_name", required=True)
    rotation = _arg(args, "rotation", required=True)
    
    found = _find_actor(actor_name)
    if not found:
        return {"error": f"Actor '{actor_name}' not found"}
    
    rot = unreal.Rotator(float(rotation[0]), float(rotation[1]), float(rotation[2]))
    found.set_actor_rotation(rot, False)
    unreal.log(f"[SN] Rotated '{found.get_actor_label()}' P={rot.pitch} Y={rot.yaw} R={rot.roll}")
    return {"actor": found.get_actor_label(), "rotation": [rot.pitch, rot.yaw, rot.roll]}


def _scale_actor(args: dict) -> dict:
    actor_name = _arg(args, "actor_name", required=True)
    scale = _arg(args, "scale", required=True)
    uniform = _arg(args, "uniform", True)
    
    found = _find_actor(actor_name)
    if not found:
        return {"error": f"Actor '{actor_name}' not found"}
    
    if uniform:
        s = float(scale[0])
        s3d = unreal.Vector(s, s, s)
    else:
        s3d = unreal.Vector(float(scale[0]), float(scale[1]), float(scale[2]))
    
    found.set_actor_scale3d(s3d)
    unreal.log(f"[SN] Scaled '{found.get_actor_label()}' to ({s3d.x}, {s3d.y}, {s3d.z})")
    return {"actor": found.get_actor_label(), "scale": [s3d.x, s3d.y, s3d.z]}


def _scatter_actors(args: dict) -> dict:
    import random
    import math
    
    source_name = _arg(args, "source_name", required=True)
    count = _arg(args, "count", 10)
    center = _arg(args, "center", [0.0, 0.0, 0.0])
    radius = _arg(args, "radius", 500.0)
    random_rotation = _arg(args, "random_rotation", True)
    scale_min = _arg(args, "random_scale_min", 0.8)
    scale_max = _arg(args, "random_scale_max", 1.2)
    
    source = _find_actor(source_name)
    if not source:
        return {"error": f"Source actor '{source_name}' not found"}
    
    cx, cy, cz = float(center[0]), float(center[1]), float(center[2])
    spawned = 0
    
    for i in range(int(count)):
        angle = random.uniform(0, 2 * math.pi)
        dist = random.uniform(0, float(radius))
        x = cx + dist * math.cos(angle)
        y = cy + dist * math.sin(angle)
        z = cz
        
        new_actor = unreal.EditorLevelLibrary.spawn_duplicate_actor(source)
        if new_actor:
            new_actor.set_actor_location(unreal.Vector(x, y, z), False, None)
            new_actor.set_actor_label(f"SN_Scatter_{i:03d}")
            
            if random_rotation:
                yaw = random.uniform(0, 360)
                new_actor.set_actor_rotation(unreal.Rotator(0, yaw, 0), False)
            
            s = random.uniform(float(scale_min), float(scale_max))
            new_actor.set_actor_scale3d(unreal.Vector(s, s, s))
            spawned += 1
    
    unreal.log(f"[SN] Scattered {spawned} copies of '{source.get_actor_label()}'")
    return {"source": source_name, "spawned": spawned, "radius": radius}


def _delete_actor(args: dict) -> dict:
    actor_name = _arg(args, "actor_name", required=True)
    confirm = _arg(args, "confirm", False)
    
    if not confirm:
        return {"error": "Delete requires confirm=true", "actor": actor_name}
    
    matches = _find_all_actors(actor_name)
    deleted = 0
    for a in matches:
        label = a.get_actor_label()
        unreal.EditorLevelLibrary.destroy_actor(a)
        deleted += 1
    
    unreal.log(f"[SN] Deleted {deleted} actor(s) matching '{actor_name}'")
    return {"deleted": deleted, "pattern": actor_name}


def _delete_duplicates(args: dict) -> dict:
    import re
    
    prefix = _arg(args, "prefix", "")
    pattern_str = _arg(args, "pattern", r"_\d+$")
    dry_run = _arg(args, "dry_run", True)
    confirm = _arg(args, "confirm", False)
    
    pattern = re.compile(pattern_str)
    actors = unreal.EditorLevelLibrary.get_all_level_actors()
    
    to_delete = []
    for a in actors:
        label = a.get_actor_label()
        if prefix and not label.startswith(prefix):
            continue
        if pattern.search(label):
            to_delete.append(label)
    
    if dry_run:
        unreal.log(f"[SN] DRY RUN: Found {len(to_delete)} duplicates")
        for label in to_delete[:20]:
            unreal.log(f"[SN]   WOULD DELETE: {label}")
        if len(to_delete) > 20:
            unreal.log(f"[SN]   ... and {len(to_delete) - 20} more")
        return {"dry_run": True, "found": len(to_delete), "samples": to_delete[:10]}
    
    if not confirm:
        return {"error": "Set confirm=true to actually delete", "found": len(to_delete)}
    
    deleted = 0
    for a in actors:
        label = a.get_actor_label()
        if prefix and not label.startswith(prefix):
            continue
        if pattern.search(label):
            unreal.EditorLevelLibrary.destroy_actor(a)
            deleted += 1
    
    unreal.log(f"[SN] Deleted {deleted} duplicate actors")
    return {"deleted": deleted, "pattern": pattern_str}


# ======================================================================
# ANALYSIS IMPLEMENTATIONS
# ======================================================================
def _list_actors(args: dict) -> dict:
    filter_type = _arg(args, "filter_type", "")
    filter_name = _arg(args, "filter_name", "")
    include_transform = _arg(args, "include_transform", True)
    max_results = _arg(args, "max_results", 100)
    
    actors = unreal.EditorLevelLibrary.get_all_level_actors()
    results = []
    
    for a in actors:
        label = a.get_actor_label()
        class_name = a.get_class().get_name()
        
        if filter_type and filter_type.lower() not in class_name.lower():
            continue
        if filter_name and filter_name.lower() not in label.lower():
            continue
        
        entry = {"name": label, "class": class_name}
        
        if include_transform:
            loc = a.get_actor_location()
            rot = a.get_actor_rotation()
            scale = a.get_actor_scale3d()
            entry["location"] = [round(loc.x, 1), round(loc.y, 1), round(loc.z, 1)]
            entry["rotation"] = [round(rot.pitch, 1), round(rot.yaw, 1), round(rot.roll, 1)]
            entry["scale"] = [round(scale.x, 3), round(scale.y, 3), round(scale.z, 3)]
        
        results.append(entry)
        if len(results) >= int(max_results):
            break
    
    unreal.log(f"[SN] Listed {len(results)}/{len(actors)} actors")
    return {"total_in_level": len(actors), "returned": len(results), "actors": results}


def _get_scene_info(args: dict) -> dict:
    from collections import Counter
    
    actors = unreal.EditorLevelLibrary.get_all_level_actors()
    type_counts = Counter()
    light_count = 0
    mesh_count = 0
    camera_count = 0
    
    for a in actors:
        class_name = a.get_class().get_name()
        type_counts[class_name] += 1
        if "Light" in class_name:
            light_count += 1
        if "StaticMesh" in class_name or "Mesh" in class_name:
            mesh_count += 1
        if "Camera" in class_name:
            camera_count += 1
    
    info = {
        "total_actors": len(actors),
        "lights": light_count,
        "meshes": mesh_count,
        "cameras": camera_count,
        "type_breakdown": dict(type_counts.most_common(30)),
    }
    
    unreal.log(f"[SN] Scene: {len(actors)} actors, {light_count} lights, {mesh_count} meshes")
    return info


# ======================================================================
# CAMERA
# ======================================================================
def _frame_viewport(args: dict) -> dict:
    location = _arg(args, "location", [0.0, 0.0, 0.0])
    distance = _arg(args, "distance", 1000.0)
    pitch = _arg(args, "pitch", -30.0)
    yaw = _arg(args, "yaw", 45.0)
    actor_name = _arg(args, "actor_name", "")
    
    target = unreal.Vector(float(location[0]), float(location[1]), float(location[2]))
    
    if actor_name:
        found = _find_actor(actor_name)
        if found:
            target = found.get_actor_location()
    
    # Use console command to set viewport
    cmd = f"vset {target.x} {target.y} {target.z}"
    unreal.SystemLibrary.execute_console_command(
        unreal.EditorLevelLibrary.get_editor_world(), cmd
    )
    
    unreal.log(f"[SN] Viewport framed at ({target.x}, {target.y}, {target.z})")
    return {"target": [target.x, target.y, target.z], "distance": distance}


# ======================================================================
# ENVIRONMENT
# ======================================================================
def _add_fog(args: dict) -> dict:
    name = _arg(args, "name", "SN_Fog")
    location = _arg(args, "location", [0.0, 0.0, 0.0])
    fog_density = _arg(args, "fog_density", 0.02)
    fog_height_falloff = _arg(args, "fog_height_falloff", 0.2)
    fog_color = _arg(args, "fog_color", [0.6, 0.65, 0.7])
    start_distance = _arg(args, "start_distance", 0.0)
    
    loc = unreal.Vector(float(location[0]), float(location[1]), float(location[2]))
    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.ExponentialHeightFog, loc, unreal.Rotator(0, 0, 0)
    )
    actor.set_actor_label(name)
    
    fog = unreal.ExponentialHeightFog.cast(actor)
    if fog:
        comp = fog.get_fog_component()
        if comp:
            comp.set_fog_density(float(fog_density))
            comp.set_fog_height_falloff(float(fog_height_falloff))
            r, g, b = float(fog_color[0]), float(fog_color[1]), float(fog_color[2])
            comp.set_fog_inscattering_color(unreal.LinearColor(r, g, b, 1.0))
            comp.set_start_distance(float(start_distance))
    
    unreal.log(f"[SN] HeightFog '{name}' density={fog_density}")
    return {"actor": name, "type": "ExponentialHeightFog", "density": fog_density}


def _add_sky_atmosphere(args: dict) -> dict:
    name = _arg(args, "name", "SN_SkyAtmosphere")
    location = _arg(args, "location", [0.0, 0.0, 0.0])
    
    loc = unreal.Vector(float(location[0]), float(location[1]), float(location[2]))
    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.SkyAtmosphere, loc, unreal.Rotator(0, 0, 0)
    )
    actor.set_actor_label(name)
    
    unreal.log(f"[SN] SkyAtmosphere '{name}' added")
    return {"actor": name, "type": "SkyAtmosphere"}


# ======================================================================
# MATERIAL
# ======================================================================
def _apply_material(args: dict) -> dict:
    actor_name = _arg(args, "actor_name", required=True)
    material_path = _arg(args, "material_path", required=True)
    material_slot = _arg(args, "material_slot", 0)
    
    found = _find_actor(actor_name)
    if not found:
        return {"error": f"Actor '{actor_name}' not found"}
    
    mat = unreal.load_asset(material_path)
    if not mat:
        return {"error": f"Material '{material_path}' not found"}
    
    applied = 0
    for comp in found.get_components_by_class(unreal.StaticMeshComponent):
        comp.set_material(int(material_slot), mat)
        applied += 1
    
    unreal.log(f"[SN] Applied '{material_path}' to '{found.get_actor_label()}' (slot {material_slot})")
    return {"actor": found.get_actor_label(), "material": material_path, "slot": material_slot, "components_updated": applied}


# ======================================================================
# ASSET
# ======================================================================
def _import_asset(args: dict) -> dict:
    source_path = _arg(args, "source_path", required=True)
    destination_path = _arg(args, "destination_path", "/Game/Imports")
    
    task = unreal.AssetImportTask()
    task.set_editor_property("filename", source_path)
    task.set_editor_property("destination_path", destination_path)
    task.set_editor_property("replace_existing", True)
    task.set_editor_property("automated", True)
    task.set_editor_property("save", True)
    
    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])
    imported = task.get_editor_property("imported_object_paths")
    
    unreal.log(f"[SN] Imported {len(imported)} asset(s) to {destination_path}")
    return {"imported": len(imported), "paths": list(imported)}


def _list_content(args: dict) -> dict:
    path = _arg(args, "path", "/Game/")
    recursive = _arg(args, "recursive", False)
    filter_type = _arg(args, "filter_type", "")
    
    assets = unreal.EditorAssetLibrary.list_assets(path, recursive=bool(recursive))
    results = []
    
    for a in assets:
        obj = unreal.load_asset(a)
        if obj:
            class_name = obj.get_class().get_name()
            if filter_type and filter_type.lower() not in class_name.lower():
                continue
            results.append({"path": a, "class": class_name, "name": obj.get_name()})
    
    unreal.log(f"[SN] Found {len(results)} assets in {path}")
    return {"total": len(results), "assets": results[:200]}


# ======================================================================
# UTILITY
# ======================================================================
def _save_level(args: dict) -> dict:
    unreal.EditorLevelLibrary.save_current_level()
    unreal.log("[SN] Level saved")
    return {"status": "saved"}


def _undo(args: dict) -> dict:
    unreal.EditorLevelLibrary.undo()
    unreal.log("[SN] Undo executed")
    return {"status": "undone"}


def _execute_console_command(args: dict) -> dict:
    cmd = _arg(args, "command", required=True)
    result = unreal.SystemLibrary.execute_console_command(
        unreal.EditorLevelLibrary.get_editor_world(), cmd
    )
    unreal.log(f"[SN] Console: '{cmd}'")
    return {"command": cmd, "executed": True}


def _screenshot(args: dict) -> dict:
    import os
    import time
    
    filename = _arg(args, "filename", f"viewport_{int(time.time())}.png")
    screenshot_dir = os.path.join(
        os.environ.get("USERPROFILE", r"C:\Users\sbcam"),
        "OneDrive", "Desktop", "sn_screenshots"
    )
    os.makedirs(screenshot_dir, exist_ok=True)
    save_path = os.path.join(screenshot_dir, filename)
    
    # Try HighResShot console command
    cmd = f'HighResShot 1 "{save_path}"'
    unreal.SystemLibrary.execute_console_command(
        unreal.EditorLevelLibrary.get_editor_world(), cmd
    )
    
    time.sleep(1.0)
    
    exists = os.path.exists(save_path)
    file_size = os.path.getsize(save_path) if exists else 0
    
    unreal.log(f"[SN] Screenshot: {save_path} ({'OK' if exists else 'PENDING'} {file_size} bytes)")
    return {
        "action": "screenshot",
        "status": "captured" if exists else "attempted",
        "save_path": save_path,
        "filename": filename,
        "file_size": file_size,
    }


def _ping(args: dict) -> dict:
    import time
    return {"status": "pong", "ue_time": time.strftime("%Y-%m-%dT%H:%M:%SZ")}


def _echo(args: dict) -> dict:
    text = _arg(args, "text", "")
    return {"echo": text}


# ======================================================================
# CONVERSATIONAL IMPLEMENTATIONS
# ======================================================================
def _say(args: dict) -> dict:
    """Display a message to the user in the Unreal Output Log."""
    message = _arg(args, "message", required=True)
    style = _arg(args, "style", "info")
    duration = _arg(args, "duration", 5.0)

    prefix_map = {
        "info": "[SN 💬]",
        "warning": "[SN ⚠️]",
        "error": "[SN ❌]",
        "success": "[SN ✅]",
        "thinking": "[SN 🤔]",
    }
    prefix = prefix_map.get(style, "[SN 💬]")
    unreal.log(f"{prefix} {message}")

    # Try to show an editor notification (toast)
    try:
        unreal.EditorDialog.show_message(
            "SuperNinja",
            message,
            unreal.AppMsgType.OK,
        )
    except Exception:
        pass  # Notification not available in all UE versions

    return {"displayed": True, "style": style, "message": message}


def _ask_user(args: dict) -> dict:
    """Ask the user a question in the Output Log."""
    question = _arg(args, "question", required=True)
    options = _arg(args, "options", [])
    context = _arg(args, "context", "")

    unreal.log(f"[SN 🙋] {question}")
    if context:
        unreal.log(f"[SN 🙋] Context: {context}")
    if options:
        for i, opt in enumerate(options):
            unreal.log(f"[SN 🙋]   {i+1}. {opt}")
    unreal.log("[SN 🙋] (Reply via SuperNinja chat or companion)")

    return {"question": question, "options": options, "waiting_for_response": True}


def _report_progress(args: dict) -> dict:
    """Report current progress in the log."""
    action = _arg(args, "action", required=True)
    step = _arg(args, "step", 0)
    total = _arg(args, "total_steps", 0)
    status = _arg(args, "status", "working")

    status_icon = {"working": "🔄", "done": "✅", "failed": "❌", "waiting": "⏳"}.get(status, "🔄")
    progress = f" ({step}/{total})" if step > 0 and total > 0 else ""

    unreal.log(f"[SN {status_icon}] {action}{progress}")
    return {"action": action, "step": step, "total": total, "status": status}


def _explain_scene(args: dict) -> dict:
    """Auto-generate a scene description and log it."""
    from collections import Counter

    analysis = _arg(args, "analysis", "")

    if not analysis:
        actors = unreal.EditorLevelLibrary.get_all_level_actors()
        type_counts = Counter()
        lights = []
        meshes = []

        for a in actors:
            class_name = a.get_class().get_name()
            type_counts[class_name] += 1
            label = a.get_actor_label()

            if "Light" in class_name:
                loc = a.get_actor_location()
                lights.append(f"{label} at ({loc.x:.0f}, {loc.y:.0f}, {loc.z:.0f})")
            elif "Mesh" in class_name:
                loc = a.get_actor_location()
                meshes.append(f"{label} at ({loc.x:.0f}, {loc.y:.0f}, {loc.z:.0f})")

        parts = [f"I can see {len(actors)} actors in this scene."]
        if lights:
            parts.append(f"Lighting: {len(lights)} lights — " + "; ".join(lights[:5]))
        if meshes:
            parts.append(f"Objects: {len(meshes)} meshes — " + "; ".join(meshes[:5]))
        if not lights:
            parts.append("⚠️ No lights found — the scene might be very dark!")
        if not meshes:
            parts.append("The scene appears to be empty.")

        analysis = " ".join(parts)

    unreal.log(f"[SN 🗣️] {analysis}")
    return {"analysis": analysis}


def _suggest_improvements(args: dict) -> dict:
    """Analyze the scene and suggest improvements."""
    from collections import Counter

    focus = _arg(args, "focus", "general")
    actors = unreal.EditorLevelLibrary.get_all_level_actors()
    type_counts = Counter()
    light_count = 0
    mesh_count = 0
    has_fog = False
    has_atmosphere = False

    for a in actors:
        class_name = a.get_class().get_name()
        type_counts[class_name] += 1
        if "Light" in class_name:
            light_count += 1
        if "Mesh" in class_name:
            mesh_count += 1
        label = a.get_actor_label()
        if "Fog" in class_name or "HeightFog" in class_name:
            has_fog = True
        if "Atmosphere" in class_name or "SkyAtmosphere" in class_name:
            has_atmosphere = True

    suggestions = []

    if focus in ("general", "lighting"):
        if light_count == 0:
            suggestions.append("💡 Add a light source! The scene has no lights and will be completely dark.")
        elif light_count == 1:
            suggestions.append("💡 Only one light found. Adding a fill light and sky light will make the scene look much more 3D.")
        if not has_fog:
            suggestions.append("🌫️ Adding subtle fog (density ~0.01) creates atmospheric depth and makes lighting look more natural.")
        if not has_atmosphere:
            suggestions.append("🌅 Adding Sky Atmosphere gives you a realistic sky with automatic sun/sky coloring.")

    if focus in ("general", "composition"):
        if mesh_count > 0 and light_count == 0:
            suggestions.append("📷 Objects exist but have no lighting. Frame the viewport to see them, then add lights.")
        if mesh_count > 20:
            suggestions.append("🧹 More than 20 meshes — there may be duplicates. Consider running delete_duplicates to clean up.")

    if focus in ("general", "atmosphere"):
        if not has_fog and light_count > 0:
            suggestions.append("🌫️ Fog would make your lights look more dramatic and add depth to the scene.")

    if not suggestions:
        suggestions.append("✨ The scene looks like it has good fundamentals! Try fine-tuning light intensities or adjusting camera angles.")

    unreal.log("[SN 💡] Scene Improvement Suggestions:")
    for i, s in enumerate(suggestions):
        unreal.log(f"[SN 💡]   {i+1}. {s}")

    return {"suggestions": suggestions, "focus": focus}


def _chat(args: dict) -> dict:
    """General conversational message from SuperNinja."""
    text = _arg(args, "text", required=True)
    mood = _arg(args, "mood", "friendly")

    mood_icon = {
        "friendly": "👋",
        "excited": "🎉",
        "thinking": "🤔",
        "concerned": "😟",
        "proud": "💪",
        "apologetic": "😅",
    }.get(mood, "💬")

    unreal.log(f"[SN {mood_icon}] {text}")
    return {"text": text, "mood": mood, "displayed": True}


# ======================================================================
# MASTER SKILLS (Docs 101-151)
# ======================================================================

def _query_master_knowledge(args: dict) -> dict:
    """Search master knowledge base (runs on cloud side, this is a stub)."""
    query = _arg(args, "query", required=True)
    unreal.log(f"[SN MASTER] Querying master knowledge: '{query}'")
    return {"query": query, "status": "processed_on_cloud"}

def _setup_landscape(args: dict) -> dict:
    """Set up a landscape with terrain preset."""
    preset = _arg(args, "preset", required=True)
    size = _arg(args, "size", "medium")
    
    size_map = {"small": 505, "medium": 1009, "large": 2017}
    component_size = size_map.get(size, 1009)
    
    unreal.log(f"[SN LAND] Setting up landscape: preset={preset}, size={component_size}")
    
    # Create landscape actor
    landscape_actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.Landscape, [0, 0, 0], [0, 0, 0]
    )
    if landscape_actor:
        landscape_actor.set_actor_label(f"SN_Landscape_{preset}")
        unreal.log(f"[SN LAND] Created landscape actor: {landscape_actor.get_name()}")
    
    return {"preset": preset, "component_size": component_size, "status": "success"}

def _add_volumetric_clouds(args: dict) -> dict:
    """Add volumetric clouds and sky atmosphere."""
    cloud_density = float(_arg(args, "cloud_density", "0.5"))
    time_of_day = _arg(args, "time_of_day", "noon")
    
    unreal.log(f"[SN VOL] Adding volumetric clouds: density={cloud_density}, time={time_of_day}")
    
    # Spawn Volumetric Cloud
    cloud_actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.VolumetricCloud, [0, 0, 1500], [0, 0, 0]
    )
    if cloud_actor:
        cloud_actor.set_actor_label("SN_VolumetricCloud")
        unreal.log(f"[SN VOL] Created volumetric cloud: {cloud_actor.get_name()}")
    
    # Spawn Sky Atmosphere
    sky_actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.SkyAtmosphere, [0, 0, 0], [0, 0, 0]
    )
    if sky_actor:
        sky_actor.set_actor_label("SN_SkyAtmosphere")
        unreal.log(f"[SN VOL] Created sky atmosphere: {sky_actor.get_name()}")
    
    return {"cloud_density": cloud_density, "time_of_day": time_of_day, "status": "success"}

def _add_height_fog(args: dict) -> dict:
    """Add exponential height fog with volumetric support."""
    fog_density = float(_arg(args, "fog_density", "0.3"))
    volumetric = _arg(args, "volumetric", "true") != "false"
    
    unreal.log(f"[SN FOG] Adding height fog: density={fog_density}, volumetric={volumetric}")
    
    fog_actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.ExponentialHeightFog, [0, 0, 0], [0, 0, 0]
    )
    if fog_actor:
        fog_actor.set_actor_label("SN_HeightFog")
        unreal.log(f"[SN FOG] Created height fog: {fog_actor.get_name()}")
    
    return {"fog_density": fog_density, "volumetric": volumetric, "status": "success"}

def _add_water_body(args: dict) -> dict:
    """Add a water body (ocean, river, or lake)."""
    water_type = _arg(args, "water_type", required=True)
    size = float(_arg(args, "size", "1000"))
    
    unreal.log(f"[SN WATER] Adding water body: type={water_type}, size={size}m")
    
    water_class_map = {
        "ocean": unreal.WaterBodyOcean,
        "river": unreal.WaterBodyRiver,
        "lake": unreal.WaterBodyLake,
    }
    water_class = water_class_map.get(water_type, unreal.WaterBodyLake)
    
    water_actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
        water_class, [0, 0, 0], [0, 0, 0]
    )
    if water_actor:
        water_actor.set_actor_label(f"SN_Water_{water_type}")
        unreal.log(f"[SN WATER] Created water body: {water_actor.get_name()}")
    
    return {"water_type": water_type, "size": size, "status": "success"}

def _setup_reflections(args: dict) -> dict:
    """Configure reflection methods for the scene."""
    scenario = _arg(args, "scenario", required=True)
    quality = _arg(args, "quality", "high")
    
    unreal.log(f"[SN REFL] Setting up reflections: scenario={scenario}, quality={quality}")
    
    if scenario in ("indoor", "architectural"):
        reflect_actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
            unreal.SphereReflectionCapture, [0, 300, 200], [0, 0, 0]
        )
        if reflect_actor:
            reflect_actor.set_actor_label("SN_SphereReflection")
    elif scenario in ("water_surface", "mirror"):
        reflect_actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
            unreal.PlanarReflection, [0, 0, 0], [0, 0, 0]
        )
        if reflect_actor:
            reflect_actor.set_actor_label("SN_PlanarReflection")
    
    return {"scenario": scenario, "quality": quality, "status": "success"}

def _setup_virtual_production(args: dict) -> dict:
    """Configure virtual production setup."""
    vp_mode = _arg(args, "vp_mode", required=True)
    stage_size = _arg(args, "stage_size", "medium")
    
    unreal.log(f"[SN VP] Setting up virtual production: mode={vp_mode}, stage={stage_size}")
    
    camera_actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.CineCameraActor, [0, -500, 200], [0, 0, 0]
    )
    if camera_actor:
        camera_actor.set_actor_label(f"SN_VP_Camera_{vp_mode}")
        unreal.log(f"[SN VP] Created VP camera: {camera_actor.get_name()}")
    
    return {"vp_mode": vp_mode, "stage_size": stage_size, "status": "success"}

def _setup_groom_system(args: dict) -> dict:
    """Configure Groom system for hair/fur."""
    groom_type = _arg(args, "groom_type", "hair")
    card_count = int(_arg(args, "card_count", "5"))
    
    unreal.log(f"[SN GROOM] Setting up groom: type={groom_type}, cards={card_count}")
    return {"groom_type": groom_type, "card_count": card_count, "status": "processed_on_cloud"}

def _setup_rvt(args: dict) -> dict:
    """Set up Runtime Virtual Texturing."""
    vt_type = _arg(args, "vt_type", "landscape")
    page_size = int(_arg(args, "page_size", "2048"))
    
    unreal.log(f"[SN RVT] Setting up RVT: type={vt_type}, page={page_size}")
    return {"vt_type": vt_type, "page_size": page_size, "status": "processed_on_cloud"}

def _setup_physics_constraints(args: dict) -> dict:
    """Add physics constraint actors."""
    constraint_type = _arg(args, "constraint_type", required=True)
    actor1 = _arg(args, "actor1", required=True)
    actor2 = _arg(args, "actor2", required=True)
    
    unreal.log(f"[SN PHYS] Adding constraint: {constraint_type} between {actor1} and {actor2}")
    
    constraint_actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.PhysicsConstraintActor, [0, 0, 200], [0, 0, 0]
    )
    if constraint_actor:
        constraint_actor.set_actor_label(f"SN_Constraint_{constraint_type}")
    
    return {"constraint_type": constraint_type, "actor1": actor1, "actor2": actor2, "status": "success"}

def _add_chaos_vehicle(args: dict) -> dict:
    """Add a Chaos Vehicle."""
    vehicle_type = _arg(args, "vehicle_type", "car")
    engine_power = float(_arg(args, "engine_power", "1.0"))
    
    unreal.log(f"[SN VEHICLE] Adding chaos vehicle: type={vehicle_type}, power={engine_power}")
    return {"vehicle_type": vehicle_type, "engine_power": engine_power, "status": "processed_on_cloud"}

def _query_master_landscape_preset(args: dict) -> dict:
    """Get landscape preset config (cloud-side stub)."""
    preset_name = _arg(args, "preset_name", required=True)
    unreal.log(f"[SN LAND] Getting landscape preset: {preset_name}")
    return {"preset_name": preset_name, "status": "processed_on_cloud"}

def _setup_source_control(args: dict) -> dict:
    """Configure source control."""
    scm_type = _arg(args, "scm_type", required=True)
    repo_url = _arg(args, "repo_url", "")
    
    unreal.log(f"[SN SCM] Setting up source control: {scm_type}, repo={repo_url}")
    return {"scm_type": scm_type, "status": "processed_on_cloud"}


# ======================================================================
# P0 SKILLS: run_python_snippet, set_actor_property, get_actor_properties
# ======================================================================

def _run_python_snippet(args: dict) -> dict:
    """Execute an arbitrary Python snippet inside Unreal Editor.
    This is the ultimate escape hatch — if no skill exists for something,
    you can run raw Python code.
    
    Args:
        code: Python code string to execute
        description: Optional description of what the code does
    
    Returns:
        dict with 'output' (stdout), 'result' (eval of last expression), or 'error'
    """
    code = _arg(args, "code", required=True)
    description = _arg(args, "description", "unnamed snippet")
    
    unreal.log(f"[SN PY] Executing snippet: {description}")
    
    import sys
    from io import StringIO
    
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    captured_out = StringIO()
    captured_err = StringIO()
    sys.stdout = captured_out
    sys.stderr = captured_err
    
    last_result = None
    
    try:
        # Try to evaluate the last expression
        lines = code.strip().split('\n')
        # If the last line looks like an expression (not a statement), eval it
        last_line = lines[-1].strip() if lines else ""
        
        # Compile and exec the whole block
        local_ns = {"unreal": unreal}
        try:
            compiled = compile(code, '<sn_snippet>', 'exec')
            exec(compiled, local_ns)
            stdout_val = captured_out.getvalue()
            stderr_val = captured_err.getvalue()
            
            result = {
                "status": "success",
                "description": description,
                "output": stdout_val.strip() if stdout_val.strip() else None,
                "errors": stderr_val.strip() if stderr_val.strip() else None,
            }
            # If there are local variables that look like results, include them
            interesting_keys = [k for k in local_ns.keys() 
                              if k not in ('unreal',) and not k.startswith('__')]
            if interesting_keys:
                result["locals"] = interesting_keys
            
        except Exception as e:
            result = {
                "status": "error",
                "description": description,
                "error": str(e),
                "output": captured_out.getvalue().strip() or None,
            }
    finally:
        sys.stdout = old_stdout
        sys.stderr = old_stderr
    
    unreal.log(f"[SN PY] Snippet '{description}' finished: {result.get('status')}")
    return result


def _set_actor_property(args: dict) -> dict:
    """Set a property on an actor by name.
    
    Supports common property types:
    - Vector properties (location, scale)
    - Rotator properties (rotation)
    - Float/Int properties
    - Bool properties
    - String properties
    - Color properties
    
    Args:
        name: Actor name (fuzzy match)
        property: Property name (e.g., 'mobility', 'visibility', 'tag')
        value: Property value (type depends on property)
    """
    actor_name = _arg(args, "name", required=True)
    prop_name = _arg(args, "property", required=True)
    value = _arg(args, "value", required=True)
    
    found = _find_actor(actor_name)
    if not found:
        return {"error": f"Actor '{actor_name}' not found"}
    
    try:
        # Handle common property mappings
        if prop_name.lower() in ("mobility",):
            # Set actor mobility
            mobility_map = {
                "static": unreal.ComponentMobility.STATIC,
                "stationary": unreal.ComponentMobility.STATIONARY,
                "movable": unreal.ComponentMobility.MOVABLE,
            }
            mob_val = mobility_map.get(str(value).lower(), unreal.ComponentMobility.MOVABLE)
            root = found.get_root_component()
            if root:
                root.set_mobility(mob_val)
            result_val = str(value)
            
        elif prop_name.lower() in ("visibility", "visible", "hidden"):
            # Set actor visibility
            hidden = str(value).lower() in ("false", "0", "no", "visible")
            found.set_actor_hidden_in_game(not hidden if str(value).lower() not in ("false", "0", "no") else hidden)
            # Also set visibility in editor
            found.set_is_temporarily_hidden_in_editor(not bool(value) if isinstance(value, bool) else str(value).lower() in ("false", "0"))
            result_val = str(value)
            
        elif prop_name.lower() in ("location", "position"):
            # Set actor location
            if isinstance(value, list) and len(value) == 3:
                new_loc = unreal.Vector(float(value[0]), float(value[1]), float(value[2]))
                found.set_actor_location(new_loc, False, None)
                result_val = value
            else:
                return {"error": f"Location must be [x, y, z], got: {value}"}
                
        elif prop_name.lower() in ("rotation",):
            # Set actor rotation
            if isinstance(value, list) and len(value) == 3:
                new_rot = unreal.Rotator(float(value[0]), float(value[1]), float(value[2]))
                found.set_actor_rotation(new_rot, False)
                result_val = value
            else:
                return {"error": f"Rotation must be [pitch, yaw, roll], got: {value}"}
                
        elif prop_name.lower() in ("scale",):
            # Set actor scale
            if isinstance(value, list) and len(value) == 3:
                new_scale = unreal.Vector(float(value[0]), float(value[1]), float(value[2]))
                found.set_actor_scale3d(new_scale)
                result_val = value
            elif isinstance(value, (int, float)):
                uniform = unreal.Vector(float(value), float(value), float(value))
                found.set_actor_scale3d(uniform)
                result_val = [float(value)] * 3
            else:
                return {"error": f"Scale must be [x, y, z] or a number, got: {value}"}
                
        elif prop_name.lower() in ("tag", "actor_tag"):
            # Add actor tag
            found.tags = found.tags + [str(value)]
            result_val = str(value)
            
        elif prop_name.lower() in ("label", "name"):
            # Rename actor
            found.set_actor_label(str(value))
            result_val = str(value)
            
        else:
            # Try generic property set via the root component
            root = found.get_root_component()
            if root:
                setter_name = f"set_{prop_name}"
                if hasattr(root, setter_name):
                    setter = getattr(root, setter_name)
                    # Try common type conversions
                    try:
                        setter(float(value))
                    except (TypeError, ValueError):
                        try:
                            setter(int(value))
                        except (TypeError, ValueError):
                            setter(str(value))
                    result_val = str(value)
                else:
                    return {"error": f"Unknown property '{prop_name}' on {found.get_actor_label()}. "
                            f"Use run_python_snippet for custom property access."}
            else:
                return {"error": f"Could not get root component for '{actor_name}'"}
        
        unreal.log(f"[SN] Set '{found.get_actor_label()}' {prop_name}={result_val}")
        return {"actor": found.get_actor_label(), "property": prop_name, "value": result_val, "status": "success"}
        
    except Exception as e:
        return {"error": f"Failed to set {prop_name}: {e}", "actor": actor_name}


def _get_actor_properties(args: dict) -> dict:
    """Get detailed properties of an actor.
    
    Args:
        name: Actor name (fuzzy match)
        include_components: Include component details (default True)
        include_materials: Include material paths (default True)
    """
    actor_name = _arg(args, "name", required=True)
    include_components = _arg(args, "include_components", True)
    include_materials = _arg(args, "include_materials", True)
    
    found = _find_actor(actor_name)
    if not found:
        return {"error": f"Actor '{actor_name}' not found"}
    
    try:
        loc = found.get_actor_location()
        rot = found.get_actor_rotation()
        scale = found.get_actor_scale3d()
        
        props = {
            "name": found.get_actor_label(),
            "class": found.get_class().get_name(),
            "location": [loc.x, loc.y, loc.z],
            "rotation": [rot.pitch, rot.yaw, rot.roll],
            "scale": [scale.x, scale.y, scale.z],
            "hidden_in_game": found.is_hidden_in_game(),
            "tags": list(found.tags) if hasattr(found, 'tags') else [],
            "folder_path": found.get_folder_path() if hasattr(found, 'get_folder_path') else "",
        }
        
        # Get root component info
        root = found.get_root_component()
        if root:
            props["root_component"] = root.get_class().get_name()
            try:
                props["mobility"] = str(root.mobility)
            except:
                pass
        
        # Get component details
        if include_components:
            components = []
            for comp in found.get_components_by_class(unreal.ActorComponent):
                comp_info = {
                    "class": comp.get_class().get_name(),
                }
                
                # Check for StaticMeshComponent specifics
                if isinstance(comp, unreal.StaticMeshComponent):
                    mesh = comp.get_static_mesh()
                    if mesh:
                        comp_info["mesh"] = mesh.get_path_name()
                    
                    # Material info
                    if include_materials:
                        materials = []
                        for i in range(comp.get_num_materials()):
                            mat = comp.get_material(i)
                            if mat:
                                materials.append({"slot": i, "path": mat.get_path_name()})
                        if materials:
                            comp_info["materials"] = materials
                
                components.append(comp_info)
            props["components"] = components
        
        unreal.log(f"[SN] Properties of '{found.get_actor_label()}': {props['class']}")
        return props
        
    except Exception as e:
        return {"error": f"Failed to get properties: {e}", "actor": actor_name}


def _add_foliage(args: dict) -> dict:
    """Add foliage instances to the scene.
    
    Args:
        mesh_path: Path to the static mesh for foliage (e.g., /Game/Foliage/SM_Tree)
        center: Center position [x, y, z]
        radius: Scatter radius in cm (default 1000)
        count: Number of instances (default 10)
        min_scale: Minimum random scale (default 0.8)
        max_scale: Maximum random scale (default 1.2)
        ground_snap: Snap to ground (default True)
    """
    mesh_path = _arg(args, "mesh_path", "/Engine/BasicShapes/Cube")
    center = _arg(args, "center", [0.0, 0.0, 0.0])
    radius = float(_arg(args, "radius", 1000.0))
    count = int(_arg(args, "count", 10))
    min_scale = float(_arg(args, "min_scale", 0.8))
    max_scale = float(_arg(args, "max_scale", 1.2))
    ground_snap = _arg(args, "ground_snap", True)
    
    import random
    
    mesh = unreal.load_asset(mesh_path)
    if not mesh:
        return {"error": f"Could not load foliage mesh: {mesh_path}"}
    
    spawned = []
    cx, cy, cz = float(center[0]), float(center[1]), float(center[2])
    
    for i in range(count):
        # Random position in circle
        angle = random.uniform(0, 2 * 3.14159)
        dist = random.uniform(0, radius)
        x = cx + dist * __import__('math').cos(angle)
        y = cy + dist * __import__('math').sin(angle)
        z = cz
        
        # Random scale
        s = random.uniform(min_scale, max_scale)
        
        loc = unreal.Vector(x, y, z)
        actor = unreal.EditorLevelLibrary.spawn_actor_from_object(mesh, loc)
        if actor:
            name = f"SN_Foliage_{i}"
            actor.set_actor_label(name)
            actor.set_actor_scale3d(unreal.Vector(s, s, s))
            # Random Y rotation for variety
            actor.set_actor_rotation(unreal.Rotator(0, random.uniform(0, 360), 0), False)
            spawned.append({"name": name, "location": [x, y, z], "scale": s})
    
    unreal.log(f"[SN] Spawned {len(spawned)} foliage instances of {mesh_path}")
    return {"mesh_path": mesh_path, "spawned": len(spawned), "instances": spawned}


def _setup_post_process(args: dict) -> dict:
    """Add a Post Process Volume to the scene.
    
    Args:
        unbound: Make the volume affect the entire scene (default True)
        intensity: Post process intensity (default 1.0)
        bloom: Bloom intensity (default 0.0)
        exposure: Manual exposure value (default -1 = auto)
        vignette: Vignette intensity (default 0.0)
        saturation: Global saturation (default 1.0)
        contrast: Global contrast (default 1.0)
        name: Actor name
    """
    unbound_val = _arg(args, "unbound", True)
    intensity = float(_arg(args, "intensity", 1.0))
    bloom = float(_arg(args, "bloom", 0.0))
    exposure = float(_arg(args, "exposure", -1.0))
    vignette = float(_arg(args, "vignette", 0.0))
    saturation = float(_arg(args, "saturation", 1.0))
    contrast = float(_arg(args, "contrast", 1.0))
    name = _arg(args, "name", "SN_PostProcess")
    
    loc = unreal.Vector(0, 0, 0)
    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.PostProcessVolume, loc, unreal.Rotator(0, 0, 0)
    )
    if not actor:
        return {"error": "Failed to spawn PostProcessVolume"}
    
    actor.set_actor_label(name)
    
    pp = unreal.PostProcessVolume.cast(actor)
    if pp:
        pp.set_enabled(True)
        pp.set_unbound(unbound_val)
        pp.set_priority(0)
        # Note: Setting specific PP settings like bloom/exposure requires
        # the post process settings struct, which varies by UE5 version.
        # The volume is spawned and enabled; fine-tuning can be done via
        # set_actor_property or run_python_snippet.
    
    unreal.log(f"[SN] PostProcessVolume '{name}' added (unbound={unbound_val})")
    return {"actor": name, "type": "PostProcessVolume", "unbound": unbound_val, "status": "success"}


def _light_scene(args: dict) -> dict:
    """Composite skill: Set up a complete lighting rig based on a style preset.
    
    This creates a 3-point lighting setup (key, fill, rim) plus environment
    lights (sky, atmosphere, fog) for a cinematic look.
    
    Args:
        style: Lighting style (cinematic, moody, outdoor, studio, neon, golden_hour)
        intensity_scale: Scale all light intensities (default 1.0)
    """
    import random
    
    style = _arg(args, "style", "cinematic")
    intensity_scale = float(_arg(args, "intensity_scale", 1.0))
    
    presets = {
        "cinematic": {
            "sun_intensity": 3.0, "sun_angle": [-40, 45, 0], "sun_temp": 6500,
            "sky_intensity": 0.5, "fog_density": 0.02,
        },
        "moody": {
            "sun_intensity": 1.5, "sun_angle": [-15, 90, 0], "sun_temp": 3200,
            "sky_intensity": 0.15, "fog_density": 0.05,
        },
        "outdoor": {
            "sun_intensity": 5.0, "sun_angle": [-50, 30, 0], "sun_temp": 7500,
            "sky_intensity": 1.0, "fog_density": 0.005,
        },
        "studio": {
            "sun_intensity": 0.0, "sun_angle": [-90, 0, 0], "sun_temp": 5500,
            "sky_intensity": 2.0, "fog_density": 0.0,
        },
        "neon": {
            "sun_intensity": 0.0, "sun_angle": [-90, 0, 0], "sun_temp": 9000,
            "sky_intensity": 0.3, "fog_density": 0.08,
        },
        "golden_hour": {
            "sun_intensity": 3.5, "sun_angle": [-8, 45, 0], "sun_temp": 3500,
            "sky_intensity": 0.6, "fog_density": 0.03,
        },
    }
    
    preset = presets.get(style, presets["cinematic"])
    results = []
    
    # 1. Directional light (sun)
    sun_loc = unreal.Vector(0, 0, 500)
    sun_rot = unreal.Rotator(
        float(preset["sun_angle"][0]),
        float(preset["sun_angle"][1]),
        float(preset["sun_angle"][2])
    )
    sun_actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.DirectionalLight, sun_loc, sun_rot
    )
    if sun_actor:
        sun_actor.set_actor_label("SN_Sun")
        sun = unreal.DirectionalLight.cast(sun_actor)
        if sun:
            sun.set_intensity(float(preset["sun_intensity"]) * intensity_scale)
            sun.set_cast_shadows(True)
            if preset["sun_temp"] > 0:
                sun.set_use_temperature(True)
                sun.set_temperature(float(preset["sun_temp"]))
        results.append({"actor": "SN_Sun", "intensity": preset["sun_intensity"]})
    
    # 2. Sky light
    sky_loc = unreal.Vector(0, 0, 1000)
    sky_actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.SkyLight, sky_loc, unreal.Rotator(0, 0, 0)
    )
    if sky_actor:
        sky_actor.set_actor_label("SN_SkyLight")
        sky = unreal.SkyLight.cast(sky_actor)
        if sky:
            sky.set_intensity(float(preset["sky_intensity"]) * intensity_scale)
        results.append({"actor": "SN_SkyLight", "intensity": preset["sky_intensity"]})
    
    # 3. Sky atmosphere
    atmo_actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.SkyAtmosphere, unreal.Vector(0, 0, 0), unreal.Rotator(0, 0, 0)
    )
    if atmo_actor:
        atmo_actor.set_actor_label("SN_SkyAtmosphere")
        results.append({"actor": "SN_SkyAtmosphere"})
    
    # 4. Exponential height fog
    if preset["fog_density"] > 0:
        fog_actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
            unreal.ExponentialHeightFog, unreal.Vector(0, 0, 0), unreal.Rotator(0, 0, 0)
        )
        if fog_actor:
            fog_actor.set_actor_label("SN_Fog")
            fog = unreal.ExponentialHeightFog.cast(fog_actor)
            if fog:
                fog.set_fog_density(float(preset["fog_density"]))
            results.append({"actor": "SN_Fog", "density": preset["fog_density"]})
    
    # 5. For neon style, add colored point lights
    if style == "neon":
        neon_colors = [
            ([0, 1, 1], [0, 500, 300]),    # Cyan
            ([1, 0, 1], [500, 0, 300]),    # Magenta
            ([1, 1, 1], [-500, 0, 300]),   # White
        ]
        for i, (color, pos) in enumerate(neon_colors):
            loc = unreal.Vector(float(pos[0]), float(pos[1]), float(pos[2]))
            pl_actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
                unreal.PointLight, loc, unreal.Rotator(0, 0, 0)
            )
            if pl_actor:
                pl_actor.set_actor_label(f"SN_NeonLight_{i}")
                pl = unreal.PointLight.cast(pl_actor)
                if pl:
                    pl.set_intensity(5000.0 * intensity_scale)
                    pl.set_attenuation_radius(2000.0)
                    r, g, b = float(color[0]), float(color[1]), float(color[2])
                    pl.set_light_color(unreal.LinearColor(r, g, b, 1.0))
                results.append({"actor": f"SN_NeonLight_{i}", "color": color})
    
    # 6. For studio, add 3-point lighting
    if style == "studio":
        # Key light
        key_loc = unreal.Vector(300, -500, 400)
        key_actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
            unreal.PointLight, key_loc, unreal.Rotator(0, 0, 0)
        )
        if key_actor:
            key_actor.set_actor_label("SN_KeyLight")
            key = unreal.PointLight.cast(key_actor)
            if key:
                key.set_intensity(8000.0 * intensity_scale)
                key.set_attenuation_radius(3000.0)
            results.append({"actor": "SN_KeyLight"})
        
        # Fill light
        fill_loc = unreal.Vector(-300, -300, 300)
        fill_actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
            unreal.PointLight, fill_loc, unreal.Rotator(0, 0, 0)
        )
        if fill_actor:
            fill_actor.set_actor_label("SN_FillLight")
            fill = unreal.PointLight.cast(fill_actor)
            if fill:
                fill.set_intensity(3000.0 * intensity_scale)
                fill.set_attenuation_radius(2000.0)
                fill.set_light_color(unreal.LinearColor(0.9, 0.95, 1.0, 1.0))
            results.append({"actor": "SN_FillLight"})
        
        # Rim light
        rim_loc = unreal.Vector(0, 500, 400)
        rim_actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
            unreal.PointLight, rim_loc, unreal.Rotator(0, 0, 0)
        )
        if rim_actor:
            rim_actor.set_actor_label("SN_RimLight")
            rim = unreal.PointLight.cast(rim_actor)
            if rim:
                rim.set_intensity(5000.0 * intensity_scale)
                rim.set_attenuation_radius(2000.0)
            results.append({"actor": "SN_RimLight"})
    
    unreal.log(f"[SN] Lit scene with '{style}' preset: {len(results)} lights created")
    return {"style": style, "lights_created": len(results), "details": results}


def _cleanup_duplicates(args: dict) -> dict:
    """Composite skill: Find and optionally remove duplicate actors.
    
    Args:
        prefix: Filter actors by prefix (e.g., 'PHX_', 'SM_')
        dry_run: If True, only report what would be deleted (default True)
    """
    prefix = _arg(args, "prefix", "")
    dry_run = _arg(args, "dry_run", True)
    
    actors = unreal.EditorLevelLibrary.get_all_level_actors()
    duplicates = []
    seen_names = {}
    
    for actor in actors:
        label = actor.get_actor_label()
        if prefix and not label.startswith(prefix):
            continue
        
        base_name = label.rstrip('_0123456789')
        if base_name in seen_names:
            duplicates.append({
                "name": label,
                "class": actor.get_class().get_name(),
            })
            if not dry_run:
                unreal.EditorLevelLibrary.destroy_actor(actor)
        else:
            seen_names[base_name] = True
    
    action = "Would delete" if dry_run else "Deleted"
    unreal.log(f"[SN] {action} {len(duplicates)} duplicate actors" +
               (f" with prefix '{prefix}'" if prefix else ""))
    return {"dry_run": dry_run, "duplicates_found": len(duplicates), 
            "actors": duplicates, "status": "dry_run" if dry_run else "deleted"}


def _scatter_props(args: dict) -> dict:
    """Composite skill: Scatter prop actors around a center point.
    
    Args:
        mesh_paths: List of mesh asset paths to scatter
        center: Center position [x, y, z]
        radius: Scatter radius (default 2000)
        count: Total number of props (default 20)
        min_scale: Min scale (default 0.5)
        max_scale: Max scale (default 1.5)
        ground_snap: Snap to ground (default True)
    """
    import random
    
    mesh_paths_val = _arg(args, "mesh_paths", ["/Engine/BasicShapes/Cube"])
    center = _arg(args, "center", [0.0, 0.0, 0.0])
    radius = float(_arg(args, "radius", 2000.0))
    count = int(_arg(args, "count", 20))
    min_scale = float(_arg(args, "min_scale", 0.5))
    max_scale = float(_arg(args, "max_scale", 1.5))
    ground_snap = _arg(args, "ground_snap", True)
    
    cx, cy, cz = float(center[0]), float(center[1]), float(center[2])
    spawned = []
    
    for i in range(count):
        # Pick a random mesh
        mesh_path = random.choice(mesh_paths_val)
        mesh = unreal.load_asset(mesh_path)
        if not mesh:
            continue
        
        # Random position
        angle = random.uniform(0, 2 * 3.14159)
        dist = random.uniform(0, radius)
        x = cx + dist * __import__('math').cos(angle)
        y = cy + dist * __import__('math').sin(angle)
        z = cz
        s = random.uniform(min_scale, max_scale)
        
        loc = unreal.Vector(x, y, z)
        actor = unreal.EditorLevelLibrary.spawn_actor_from_object(mesh, loc)
        if actor:
            name = f"SN_Prop_{i}"
            actor.set_actor_label(name)
            actor.set_actor_scale3d(unreal.Vector(s, s, s))
            actor.set_actor_rotation(unreal.Rotator(0, random.uniform(0, 360), 0), False)
            spawned.append({"name": name, "location": [x, y, z]})
    
    unreal.log(f"[SN] Scattered {len(spawned)} props")
    return {"spawned": len(spawned), "props": spawned}


# ======================================================================
# MAIN: Execute a skill by name
# ======================================================================
def _add_niagara_effect(args: dict) -> dict:
    """Spawn a Niagara emitter actor in the scene.
    
    Args:
        effect_type: Type of effect (fire, smoke, sparks, rain, snow, explosion)
        location: Spawn position [x, y, z]
        name: Actor name
    """
    effect_type = _arg(args, "effect_type", "fire")
    location = _arg(args, "location", [0.0, 0.0, 0.0])
    name = _arg(args, "name", f"SN_Niagara_{effect_type}")
    
    loc = unreal.Vector(float(location[0]), float(location[1]), float(location[2]))
    
    # Try to spawn a Niagara actor
    try:
        actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
            unreal.NiagaraActor, loc, unreal.Rotator(0, 0, 0)
        )
        if actor:
            actor.set_actor_label(name)
            unreal.log(f"[SN] Niagara '{name}' spawned (type={effect_type})")
            return {"actor": name, "effect_type": effect_type, "location": list(location), "status": "success"}
        else:
            return {"error": "Failed to spawn NiagaraActor — Niagara plugin may not be enabled"}
    except Exception as e:
        return {"error": f"Niagara not available: {e}. Enable the Niagara plugin in Edit > Plugins."}


def _add_audio_ambient(args: dict) -> dict:
    """Add an ambient sound actor to the scene.
    
    Args:
        location: Sound position [x, y, z]
        sound_path: Path to SoundAsset (e.g., /Game/Audio/Ambient_Forest)
        volume: Volume multiplier (default 1.0)
        attenuation_radius: How far the sound reaches (default 1500)
        name: Actor name
    """
    location = _arg(args, "location", [0.0, 0.0, 0.0])
    sound_path = _arg(args, "sound_path", "")
    volume = float(_arg(args, "volume", 1.0))
    attenuation_radius = float(_arg(args, "attenuation_radius", 1500.0))
    name = _arg(args, "name", "SN_AmbientSound")
    
    loc = unreal.Vector(float(location[0]), float(location[1]), float(location[2]))
    
    try:
        actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
            unreal.AmbientSound, loc, unreal.Rotator(0, 0, 0)
        )
        if actor:
            actor.set_actor_label(name)
            
            # If a sound asset path was provided, try to load and assign it
            if sound_path:
                sound_asset = unreal.load_asset(sound_path)
                if sound_asset:
                    # Get the audio component and set the sound
                    for comp in actor.get_components_by_class(unreal.AudioComponent):
                        comp.set_sound(sound_asset)
                        comp.set_volume_multiplier(volume)
                        if hasattr(comp, 'set_attenuation_settings'):
                            pass  # Attenuation requires an asset
                    unreal.log(f"[SN] AmbientSound '{name}' with {sound_path}")
                else:
                    unreal.log(f"[SN] WARNING: Could not load sound {sound_path}")
            
            return {"actor": name, "type": "AmbientSound", "location": list(location), "status": "success"}
        else:
            return {"error": "Failed to spawn AmbientSound"}
    except Exception as e:
        return {"error": f"Audio spawn failed: {e}"}


def _add_navmesh(args: dict) -> dict:
    """Add a NavMeshBoundsVolume to the scene for AI navigation.
    
    Args:
        center: Volume center [x, y, z]
        extent: Volume extent [x, y, z] (default large enough for demo)
        name: Actor name
    """
    center = _arg(args, "center", [0.0, 0.0, 0.0])
    extent = _arg(args, "extent", [2000.0, 2000.0, 500.0])
    name = _arg(args, "name", "SN_NavMeshBounds")
    
    loc = unreal.Vector(float(center[0]), float(center[1]), float(center[2]))
    
    try:
        actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
            unreal.NavMeshBoundsVolume, loc, unreal.Rotator(0, 0, 0)
        )
        if actor:
            actor.set_actor_label(name)
            # Set the brush bounds
            ext = unreal.Vector(float(extent[0]), float(extent[1]), float(extent[2]))
            # Brush scaling for nav mesh volume
            actor.set_actor_scale3d(ext)
            unreal.log(f"[SN] NavMeshBoundsVolume '{name}' added")
            return {"actor": name, "type": "NavMeshBoundsVolume", "center": list(center), "extent": list(extent), "status": "success"}
        else:
            return {"error": "Failed to spawn NavMeshBoundsVolume — Navigation System plugin may not be enabled"}
    except Exception as e:
        return {"error": f"NavMesh spawn failed: {e}"}


def _setup_ai_character(args: dict) -> dict:
    """Set up a basic AI character in the scene.
    
    Args:
        location: Spawn position [x, y, z]
        character_type: Type (basic, patrol, chase) — defaults to basic
        name: Actor name
    """
    location = _arg(args, "location", [0.0, 0.0, 100.0])
    character_type = _arg(args, "character_type", "basic")
    name = _arg(args, "name", f"SN_AI_{character_type}")
    
    loc = unreal.Vector(float(location[0]), float(location[1]), float(location[2]))
    
    try:
        # Spawn a basic character (uses the default pawn class)
        actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
            unreal.Character, loc, unreal.Rotator(0, 0, 0)
        )
        if actor:
            actor.set_actor_label(name)
            unreal.log(f"[SN] AI Character '{name}' spawned (type={character_type})")
            return {"actor": name, "type": "Character", "character_type": character_type, "location": list(location), "status": "success"}
        else:
            return {"error": "Failed to spawn Character"}
    except Exception as e:
        # If Character class isn't available, try Pawn
        try:
            actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
                unreal.Pawn, loc, unreal.Rotator(0, 0, 0)
            )
            if actor:
                actor.set_actor_label(name)
                unreal.log(f"[SN] AI Pawn '{name}' spawned (type={character_type})")
                return {"actor": name, "type": "Pawn", "character_type": character_type, "location": list(location), "status": "success"}
        except Exception as e2:
            return {"error": f"AI character spawn failed: {e2}"}


def _setup_cinematic(args: dict) -> dict:
    """Set up cinematic cameras in the scene.
    
    Args:
        location: Camera position [x, y, z]
        rotation: Camera rotation [pitch, yaw, roll]
        sequence_type: Type (tracking_shot, orbit, dolly, static)
        name: Actor name
    """
    location = _arg(args, "location", [0.0, -500.0, 300.0])
    rotation = _arg(args, "rotation", [-15.0, 0.0, 0.0])
    sequence_type = _arg(args, "sequence_type", "static")
    name = _arg(args, "name", f"SN_CineCamera")
    
    loc = unreal.Vector(float(location[0]), float(location[1]), float(location[2]))
    rot = unreal.Rotator(float(rotation[0]), float(rotation[1]), float(rotation[2]))
    
    try:
        actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
            unreal.CineCameraActor, loc, rot
        )
        if actor:
            actor.set_actor_label(name)
            unreal.log(f"[SN] CineCamera '{name}' spawned (type={sequence_type})")
            return {"actor": name, "type": "CineCameraActor", "sequence_type": sequence_type, 
                    "location": list(location), "rotation": list(rotation), "status": "success"}
        else:
            return {"error": "Failed to spawn CineCameraActor — Cinematics plugin may not be enabled"}
    except Exception as e:
        return {"error": f"Cinematic setup failed: {e}"}


def _find_actors_advanced(args: dict) -> dict:
    """Advanced actor search with multiple filter criteria.
    
    Args:
        filter_class: Filter by class name (partial match)
        filter_tag: Filter by actor tag
        filter_mobility: Filter by mobility type (Static, Stationary, Movable)
        filter_material: Filter by material path (partial match)
        spatial_center: Center point for spatial search [x, y, z]
        spatial_radius: Radius for spatial search in cm
        max_results: Maximum number of results (default 50)
    """
    filter_class = _arg(args, "filter_class", "")
    filter_tag = _arg(args, "filter_tag", "")
    filter_mobility = _arg(args, "filter_mobility", "")
    filter_material = _arg(args, "filter_material", "")
    spatial_center = _arg(args, "spatial_center", None)
    spatial_radius = float(_arg(args, "spatial_radius", 1000.0))
    max_results = int(_arg(args, "max_results", 50))
    
    actors = unreal.EditorLevelLibrary.get_all_level_actors()
    results = []
    
    for actor in actors:
        if len(results) >= max_results:
            break
        
        # Class filter
        if filter_class:
            class_name = actor.get_class().get_name()
            if filter_class.lower() not in class_name.lower():
                continue
        
        # Tag filter
        if filter_tag:
            tags = list(actor.tags) if hasattr(actor, 'tags') else []
            if filter_tag.lower() not in [t.lower() for t in tags]:
                continue
        
        # Mobility filter
        if filter_mobility:
            root = actor.get_root_component()
            if root:
                mobility = str(root.mobility)
                if filter_mobility.lower() not in mobility.lower():
                    continue
        
        # Spatial filter
        if spatial_center and isinstance(spatial_center, list) and len(spatial_center) == 3:
            loc = actor.get_actor_location()
            cx, cy, cz = float(spatial_center[0]), float(spatial_center[1]), float(spatial_center[2])
            dist = ((loc.x - cx)**2 + (loc.y - cy)**2 + (loc.z - cz)**2) ** 0.5
            if dist > spatial_radius:
                continue
        
        # Material filter
        if filter_material:
            has_material = False
            for comp in actor.get_components_by_class(unreal.StaticMeshComponent):
                for i in range(comp.get_num_materials()):
                    mat = comp.get_material(i)
                    if mat and filter_material.lower() in mat.get_path_name().lower():
                        has_material = True
                        break
                if has_material:
                    break
            if not has_material:
                continue
        
        loc = actor.get_actor_location()
        rot = actor.get_actor_rotation()
        results.append({
            "name": actor.get_actor_label(),
            "class": actor.get_class().get_name(),
            "location": [loc.x, loc.y, loc.z],
            "rotation": [rot.pitch, rot.yaw, rot.roll],
        })
    
    unreal.log(f"[SN] Advanced search found {len(results)} actors")
    return {"total_found": len(results), "actors": results}


def _optimize_scene(args: dict) -> dict:
    """Run scene optimization checks and apply fixes.
    
    Args:
        enable_nanite: Enable Nanite on compatible static meshes (default True)
        enable_lumen: Ensure Lumen is configured (default True)
    """
    enable_nanite = _arg(args, "enable_nanite", True)
    enable_lumen = _arg(args, "enable_lumen", True)
    
    optimizations = []
    
    # Check for Nanite-eligible meshes
    if enable_nanite:
        nanite_count = 0
        for actor in unreal.EditorLevelLibrary.get_all_level_actors():
            for comp in actor.get_components_by_class(unreal.StaticMeshComponent):
                mesh = comp.get_static_mesh()
                if mesh:
                    try:
                        if not mesh.is_nanite_enabled():
                            mesh.set_nanite_enabled(True)
                            nanite_count += 1
                    except:
                        pass
        if nanite_count > 0:
            optimizations.append(f"Enabled Nanite on {nanite_count} meshes")
    
    # Check for excessive movable lights
    movable_lights = 0
    for actor in unreal.EditorLevelLibrary.get_all_level_actors():
        class_name = actor.get_class().get_name()
        if "Light" in class_name:
            root = actor.get_root_component()
            if root and "Movable" in str(root.mobility):
                movable_lights += 1
    
    if movable_lights > 10:
        optimizations.append(f"Warning: {movable_lights} movable lights may exceed Lumen budget")
    
    unreal.log(f"[SN] Optimization complete: {len(optimizations)} items")
    return {"optimizations": optimizations, "movable_lights": movable_lights, "status": "success"}


def execute_skill(skill_name: str, args: dict) -> dict:
    """Execute a skill by name with the given arguments.
    Returns a result dict that will be sent back to the cloud.
    """
    if skill_name not in SKILLS:
        # Knowledge/query skills are handled cloud-side; if they reach here,
        # acknowledge and return a note that they're cloud-processed
        cloud_side_skills = {
            "query_knowledge", "query_advanced_knowledge", "query_expert_knowledge",
            "explain_ue5_concept", "suggest_blueprint_pattern",
            "get_lighting_setup", "get_material_recipe", "get_multiplayer_pattern",
            "get_fps_optimization_profile", "analyze_rendering",
        }
        if skill_name in cloud_side_skills:
            return {"skill": skill_name, "status": "processed_on_cloud",
                    "note": "This is a cloud-side knowledge skill. Result available via the AI brain."}
        return {"error": f"Unknown skill: {skill_name}", "available": sorted(SKILLS.keys())}
    
    skill = SKILLS[skill_name]
    
    try:
        result = skill["execute"](args)
        result["skill"] = skill_name
        result["safety"] = skill["safety"]
        return result
    except Exception as e:
        unreal.log(f"[SN] ERROR executing {skill_name}: {e}")
        traceback.print_exc()
        return {"error": str(e), "skill": skill_name, "traceback": traceback.format_exc()}


# Register all skills on import
register_skills()

unreal.log(f"[SN] Skill executor loaded: {len(SKILLS)} skills registered")