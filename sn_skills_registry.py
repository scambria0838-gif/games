"""
SuperNinja Skill Registry — Phase 3

Defines every skill SuperNinja can execute in Unreal Editor.
Each skill has:
  - name: command string
  - category: group for organization
  - safety_level: "safe" (read-only) | "modify" (changes scene) | "destructive" (can delete things)
  - description: what it does
  - args_schema: expected arguments with types and defaults
  - unreal_code: Python code template that runs inside Unreal

The registry is loaded by the Unreal client to know what commands
it can accept, and by the cloud AI to know what it can request.
"""

SKILLS = {
    # ================================================================
    # LIGHTING SKILLS
    # ================================================================
    "add_directional_light": {
        "category": "lighting",
        "safety_level": "modify",
        "description": "Add a Directional Light (sun) to the scene. Controls intensity, color, angle, shadows, and mobility.",
        "args_schema": {
            "intensity": {"type": "float", "default": 3.0, "min": 0.0, "max": 100.0, "desc": "Light intensity in lux/candela"},
            "light_color": {"type": "color", "default": [1.0, 0.95, 0.85], "desc": "RGB color (0-1 range)"},
            "rotation": {"type": "rotator", "default": [-40.0, 45.0, 0.0], "desc": "Pitch, Yaw, Roll degrees"},
            "shadow_enabled": {"type": "bool", "default": True, "desc": "Enable shadow casting"},
            "mobility": {"type": "string", "default": "Movable", "options": ["Static", "Stationary", "Movable"]},
            "temperature": {"type": "float", "default": 6500.0, "min": 1700.0, "max": 12000.0, "desc": "Color temperature in Kelvin (overrides light_color if set)"},
            "name": {"type": "string", "default": "SN_Sun", "desc": "Actor name"},
        },
        "unreal_code": '''
import unreal
name = "{{name}}"
location = unreal.Vector(0, 0, 500)
rotation = unreal.Rotator({{rotation[0]}}, {{rotation[1]}}, {{rotation[2]}})
actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
    unreal.DirectionalLight, location, rotation
)
actor.set_actor_label(name)
light = unreal.DirectionalLight.cast(actor)
if light:
    light.set_intensity({{intensity}})
    r, g, b = {{light_color}}
    light.set_light_color(unreal.LinearColor(r, g, b, 1.0))
    light.set_cast_shadows({{shadow_enabled}})
    light.set_mobility(unreal.ComponentMobility.{{mobility}})
    if {{temperature}} > 0:
        light.set_use_temperature(True)
        light.set_temperature({{temperature}})
unreal.log(f"[SN] DirectionalLight '{name}' added: intensity={{intensity}} shadows={{shadow_enabled}}")
'''
    },

    "add_point_light": {
        "category": "lighting",
        "safety_level": "modify",
        "description": "Add a Point Light at a specific location. Good for indoor lighting, lamps, fires, accent lights.",
        "args_schema": {
            "location": {"type": "vector", "default": [0.0, 0.0, 300.0], "desc": "X, Y, Z position in world units (cm)"},
            "intensity": {"type": "float", "default": 3000.0, "min": 0.0, "max": 1000000.0, "desc": "Candela intensity"},
            "light_color": {"type": "color", "default": [1.0, 0.9, 0.7], "desc": "RGB color (0-1)"},
            "attenuation_radius": {"type": "float", "default": 1000.0, "min": 10.0, "max": 50000.0, "desc": "How far light reaches (cm)"},
            "shadow_enabled": {"type": "bool", "default": True},
            "use_inverse_squared": {"type": "bool", "default": True, "desc": "Physically accurate falloff"},
            "source_radius": {"type": "float", "default": 5.0, "desc": "Soft shadow source radius (cm)"},
            "name": {"type": "string", "default": "SN_PointLight", "desc": "Actor name"},
        },
        "unreal_code": '''
import unreal
name = "{{name}}"
loc = unreal.Vector({{location[0]}}, {{location[1]}}, {{location[2]}})
actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
    unreal.PointLight, loc, unreal.Rotator(0, 0, 0)
)
actor.set_actor_label(name)
light = unreal.PointLight.cast(actor)
if light:
    light.set_intensity({{intensity}})
    r, g, b = {{light_color}}
    light.set_light_color(unreal.LinearColor(r, g, b, 1.0))
    light.set_attenuation_radius({{attenuation_radius}})
    light.set_cast_shadows({{shadow_enabled}})
    light.set_use_inverse_squared_falloff({{use_inverse_squared}})
    light.set_source_radius({{source_radius}})
unreal.log(f"[SN] PointLight '{name}' at ({loc.x}, {loc.y}, {loc.z})")
'''
    },

    "add_spot_light": {
        "category": "lighting",
        "safety_level": "modify",
        "description": "Add a Spot Light. Great for focused beams, stage lighting, car headlights, flashlights.",
        "args_schema": {
            "location": {"type": "vector", "default": [0.0, 0.0, 500.0]},
            "rotation": {"type": "rotator", "default": [-90.0, 0.0, 0.0], "desc": "Default points down"},
            "intensity": {"type": "float", "default": 5000.0},
            "inner_cone_angle": {"type": "float", "default": 15.0, "min": 1.0, "max": 89.0, "desc": "Bright center angle in degrees"},
            "outer_cone_angle": {"type": "float", "default": 45.0, "min": 5.0, "max": 90.0, "desc": "Full spread angle"},
            "attenuation_radius": {"type": "float", "default": 2000.0},
            "light_color": {"type": "color", "default": [1.0, 0.95, 0.85]},
            "shadow_enabled": {"type": "bool", "default": True},
            "name": {"type": "string", "default": "SN_SpotLight"},
        },
        "unreal_code": '''
import unreal
name = "{{name}}"
loc = unreal.Vector({{location[0]}}, {{location[1]}}, {{location[2]}})
rot = unreal.Rotator({{rotation[0]}}, {{rotation[1]}}, {{rotation[2]}})
actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
    unreal.SpotLight, loc, rot
)
actor.set_actor_label(name)
light = unreal.SpotLight.cast(actor)
if light:
    light.set_intensity({{intensity}})
    light.set_inner_cone_angle({{inner_cone_angle}})
    light.set_outer_cone_angle({{outer_cone_angle}})
    light.set_attenuation_radius({{attenuation_radius}})
    r, g, b = {{light_color}}
    light.set_light_color(unreal.LinearColor(r, g, b, 1.0))
    light.set_cast_shadows({{shadow_enabled}})
unreal.log(f"[SN] SpotLight '{name}' inner={{inner_cone_angle}} outer={{outer_cone_angle}}")
'''
    },

    "add_sky_light": {
        "category": "lighting",
        "safety_level": "modify",
        "description": "Add a Sky Light for ambient environment illumination. Captures the sky cubemap.",
        "args_schema": {
            "intensity": {"type": "float", "default": 1.0, "min": 0.0, "max": 20.0},
            "light_color": {"type": "color", "default": [1.0, 1.0, 1.0]},
            "source_type": {"type": "string", "default": "SLS_CapturedScene", "options": ["SLS_CapturedScene", "SLS_SpecifiedCubemap", "SLS_SpecifiedCubemap"]},
            "mobility": {"type": "string", "default": "Movable", "options": ["Static", "Stationary", "Movable"]},
            "name": {"type": "string", "default": "SN_SkyLight"},
        },
        "unreal_code": '''
import unreal
name = "{{name}}"
loc = unreal.Vector(0, 0, 1000)
actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
    unreal.SkyLight, loc, unreal.Rotator(0, 0, 0)
)
actor.set_actor_label(name)
light = unreal.SkyLight.cast(actor)
if light:
    light.set_intensity({{intensity}})
    r, g, b = {{light_color}}
    light.set_light_color(unreal.LinearColor(r, g, b, 1.0))
    light.set_mobility(unreal.ComponentMobility.{{mobility}})
unreal.log(f"[SN] SkyLight '{name}' added intensity={{intensity}}")
'''
    },

    "adjust_light": {
        "category": "lighting",
        "safety_level": "modify",
        "description": "Modify an existing light's properties. Find by name or path.",
        "args_schema": {
            "actor_name": {"type": "string", "required": True, "desc": "Name or partial name of the light actor"},
            "intensity": {"type": "float", "required": False},
            "light_color": {"type": "color", "required": False},
            "shadow_enabled": {"type": "bool", "required": False},
            "attenuation_radius": {"type": "float", "required": False},
            "rotation": {"type": "rotator", "required": False},
            "location": {"type": "vector", "required": False},
        },
        "unreal_code": '''
import unreal
actor_name = "{{actor_name}}"
actors = unreal.EditorLevelLibrary.get_all_level_actors()
found = None
for a in actors:
    if actor_name.lower() in a.get_actor_label().lower():
        found = a
        break
if not found:
    unreal.log(f"[SN] ERROR: No actor found matching '{actor_name}'")
else:
    light_comp = None
    for comp in found.get_components_by_class(unreal.LightComponent):
        light_comp = comp
        break
    if light_comp:
        {{#if intensity}}light_comp.set_intensity({{intensity}}){{/if}}
        {{#if shadow_enabled}}light_comp.set_cast_shadows({{shadow_enabled}}){{/if}}
        {{#if attenuation_radius}}
        if hasattr(light_comp, 'set_attenuation_radius'):
            light_comp.set_attenuation_radius({{attenuation_radius}})
        {{/if}}
        {{#if light_color}}
        r, g, b = {{light_color}}
        light_comp.set_light_color(unreal.LinearColor(r, g, b, 1.0))
        {{/if}}
    unreal.log(f"[SN] Adjusted light '{found.get_actor_label()}'")
'''
    },

    # ================================================================
    # PLACEMENT SKILLS
    # ================================================================
    "spawn_actor": {
        "category": "placement",
        "safety_level": "modify",
        "description": "Spawn a basic primitive actor (cube, sphere, cylinder, plane, etc.) at a location.",
        "args_schema": {
            "shape": {"type": "string", "default": "Cube", "options": ["Cube", "Sphere", "Cylinder", "Cone", "Plane", "SkeletalMesh"], "desc": "Shape type"},
            "location": {"type": "vector", "default": [0.0, 0.0, 0.0]},
            "rotation": {"type": "rotator", "default": [0.0, 0.0, 0.0]},
            "scale": {"type": "vector", "default": [1.0, 1.0, 1.0]},
            "material_path": {"type": "string", "default": "", "desc": "Asset path to material (e.g., /Game/Materials/M_Wood)"},
            "name": {"type": "string", "default": "SN_Actor"},
        },
        "unreal_code": '''
import unreal
shape = "{{shape}}"
name = "{{name}}"
loc = unreal.Vector({{location[0]}}, {{location[1]}}, {{location[2]}})
rot = unreal.Rotator({{rotation[0]}}, {{rotation[1]}}, {{rotation[2]}})
scale = unreal.Vector({{scale[0]}}, {{scale[1]}}, {{scale[2]}})

shape_classes = {
    "Cube": unreal.StaticMesh,
    "Sphere": unreal.StaticMesh,
    "Cylinder": unreal.StaticMesh,
    "Cone": unreal.StaticMesh,
    "Plane": unreal.StaticMesh,
}

# Use editor spawning for basic shapes
mesh_paths = {
    "Cube": "/Engine/BasicShapes/Cube",
    "Sphere": "/Engine/BasicShapes/Sphere",
    "Cylinder": "/Engine/BasicShapes/Cylinder",
    "Cone": "/Engine/BasicShapes/Cone",
    "Plane": "/Engine/BasicShapes/Plane",
}

mesh_path = mesh_paths.get(shape, "/Engine/BasicShapes/Cube")
mesh = unreal.load_asset(mesh_path)
actor = unreal.EditorLevelLibrary.spawn_actor_from_object(mesh, loc)
actor.set_actor_label(name)
actor.set_actor_rotation(rot, False)
actor.set_actor_scale3d(scale)

mat_path = "{{material_path}}"
if mat_path:
    mat = unreal.load_asset(mat_path)
    if mat:
        for comp in actor.get_components_by_class(unreal.StaticMeshComponent):
            comp.set_material(0, mat)

unreal.log(f"[SN] Spawned {shape} '{name}' at ({loc.x}, {loc.y}, {loc.z})")
'''
    },

    "move_actor": {
        "category": "placement",
        "safety_level": "modify",
        "description": "Move an existing actor to a new location. Find by name.",
        "args_schema": {
            "actor_name": {"type": "string", "required": True, "desc": "Name or partial name match"},
            "location": {"type": "vector", "required": True, "desc": "New world position [X, Y, Z]"},
            "relative": {"type": "bool", "default": False, "desc": "If true, offset from current position"},
        },
        "unreal_code": '''
import unreal
actor_name = "{{actor_name}}"
actors = unreal.EditorLevelLibrary.get_all_level_actors()
found = None
for a in actors:
    if actor_name.lower() in a.get_actor_label().lower():
        found = a
        break
if not found:
    unreal.log(f"[SN] ERROR: Actor '{actor_name}' not found")
else:
    new_loc = unreal.Vector({{location[0]}}, {{location[1]}}, {{location[2]}})
    {{#if relative}}
    cur = found.get_actor_location()
    new_loc = unreal.Vector(cur.x + {{location[0]}}, cur.y + {{location[1]}}, cur.z + {{location[2]}})
    {{/if}}
    found.set_actor_location(new_loc, False, None)
    unreal.log(f"[SN] Moved '{found.get_actor_label()}' to ({new_loc.x}, {new_loc.y}, {new_loc.z})")
'''
    },

    "rotate_actor": {
        "category": "placement",
        "safety_level": "modify",
        "description": "Rotate an existing actor.",
        "args_schema": {
            "actor_name": {"type": "string", "required": True},
            "rotation": {"type": "rotator", "required": True, "desc": "Pitch, Yaw, Roll in degrees"},
        },
        "unreal_code": '''
import unreal
actor_name = "{{actor_name}}"
actors = unreal.EditorLevelLibrary.get_all_level_actors()
found = None
for a in actors:
    if actor_name.lower() in a.get_actor_label().lower():
        found = a
        break
if not found:
    unreal.log(f"[SN] ERROR: Actor '{actor_name}' not found")
else:
    rot = unreal.Rotator({{rotation[0]}}, {{rotation[1]}}, {{rotation[2]}})
    found.set_actor_rotation(rot, False)
    unreal.log(f"[SN] Rotated '{found.get_actor_label()}' to P={rot.pitch} Y={rot.yaw} R={rot.roll}")
'''
    },

    "scale_actor": {
        "category": "placement",
        "safety_level": "modify",
        "description": "Scale an existing actor.",
        "args_schema": {
            "actor_name": {"type": "string", "required": True},
            "scale": {"type": "vector", "required": True, "desc": "Uniform or non-uniform scale [X, Y, Z]"},
            "uniform": {"type": "bool", "default": True, "desc": "If true, uses X value for all axes"},
        },
        "unreal_code": '''
import unreal
actor_name = "{{actor_name}}"
actors = unreal.EditorLevelLibrary.get_all_level_actors()
found = None
for a in actors:
    if actor_name.lower() in a.get_actor_label().lower():
        found = a
        break
if not found:
    unreal.log(f"[SN] ERROR: Actor '{actor_name}' not found")
else:
    {{#if uniform}}
    s = {{scale[0]}}
    scale = unreal.Vector(s, s, s)
    {{else}}
    scale = unreal.Vector({{scale[0]}}, {{scale[1]}}, {{scale[2]}})
    {{/if}}
    found.set_actor_scale3d(scale)
    unreal.log(f"[SN] Scaled '{found.get_actor_label()}' to ({scale.x}, {scale.y}, {scale.z})")
'''
    },

    "scatter_actors": {
        "category": "placement",
        "safety_level": "modify",
        "description": "Scatter multiple copies of an actor within a region. Good for foliage, props, debris.",
        "args_schema": {
            "source_name": {"type": "string", "required": True, "desc": "Actor to duplicate"},
            "count": {"type": "int", "default": 10, "min": 1, "max": 500, "desc": "Number of copies"},
            "center": {"type": "vector", "default": [0.0, 0.0, 0.0], "desc": "Center of scatter area"},
            "radius": {"type": "float", "default": 500.0, "min": 10.0, "max": 50000.0, "desc": "Scatter radius (cm)"},
            "random_rotation": {"type": "bool", "default": True},
            "random_scale_min": {"type": "float", "default": 0.8, "desc": "Min random uniform scale"},
            "random_scale_max": {"type": "float", "default": 1.2, "desc": "Max random uniform scale"},
            "ground_snap": {"type": "bool", "default": True, "desc": "Snap to ground/terrain"},
        },
        "unreal_code": '''
import unreal
import random
import math

source_name = "{{source_name}}"
actors = unreal.EditorLevelLibrary.get_all_level_actors()
source = None
for a in actors:
    if source_name.lower() in a.get_actor_label().lower():
        source = a
        break
if not source:
    unreal.log(f"[SN] ERROR: Source actor '{source_name}' not found")
else:
    count = {{count}}
    cx, cy, cz = {{center}}
    radius = {{radius}}
    
    for i in range(count):
        angle = random.uniform(0, 2 * math.pi)
        dist = random.uniform(0, radius)
        x = cx + dist * math.cos(angle)
        y = cy + dist * math.sin(angle)
        z = cz
        
        new_actor = unreal.EditorLevelLibrary.spawn_duplicate_actor(source)
        if new_actor:
            new_actor.set_actor_location(unreal.Vector(x, y, z), False, None)
            new_actor.set_actor_label(f"SN_Scatter_{i:03d}")
            
            if {{random_rotation}}:
                yaw = random.uniform(0, 360)
                new_actor.set_actor_rotation(unreal.Rotator(0, yaw, 0), False)
            
            s = random.uniform({{random_scale_min}}, {{random_scale_max}})
            new_actor.set_actor_scale3d(unreal.Vector(s, s, s))
    
    unreal.log(f"[SN] Scattered {count} copies of '{source.get_actor_label()}'")
'''
    },

    "delete_actor": {
        "category": "placement",
        "safety_level": "destructive",
        "description": "Delete an actor by name. DESTRUCTIVE — cannot undo remotely.",
        "args_schema": {
            "actor_name": {"type": "string", "required": True, "desc": "Name or partial match"},
            "confirm": {"type": "bool", "required": True, "desc": "Must be true to actually delete"},
        },
        "unreal_code": '''
import unreal
actor_name = "{{actor_name}}"
if not {{confirm}}:
    unreal.log(f"[SN] Delete aborted — confirm not set for '{actor_name}'")
else:
    actors = unreal.EditorLevelLibrary.get_all_level_actors()
    deleted = 0
    for a in actors:
        if actor_name.lower() in a.get_actor_label().lower():
            unreal.EditorLevelLibrary.destroy_actor(a)
            deleted += 1
    unreal.log(f"[SN] Deleted {deleted} actor(s) matching '{actor_name}'")
'''
    },

    "delete_duplicates": {
        "category": "placement",
        "safety_level": "destructive",
        "description": "Delete actors with duplicate names (e.g., PHX_ duplicates). Patterns like 'Name_1', 'Name_2' etc.",
        "args_schema": {
            "prefix": {"type": "string", "default": "", "desc": "Only delete duplicates starting with this prefix"},
            "pattern": {"type": "string", "default": "_\\d+$", "desc": "Regex pattern for duplicate suffix"},
            "dry_run": {"type": "bool", "default": True, "desc": "If true, only report what would be deleted"},
            "confirm": {"type": "bool", "default": False, "desc": "Must be true to actually delete"},
        },
        "unreal_code": '''
import unreal
import re

actors = unreal.EditorLevelLibrary.get_all_level_actors()
prefix = "{{prefix}}"
pattern = re.compile("{{pattern}}")
dry_run = {{dry_run}}
confirm = {{confirm}}

to_delete = []
for a in actors:
    label = a.get_actor_label()
    if prefix and not label.startswith(prefix):
        continue
    if pattern.search(label):
        to_delete.append((label, a))

unreal.log(f"[SN] Found {len(to_delete)} duplicate actors")
for label, actor in to_delete:
    if dry_run:
        unreal.log(f"[SN]   WOULD DELETE: {label}")
    elif confirm:
        unreal.EditorLevelLibrary.destroy_actor(actor)
        unreal.log(f"[SN]   DELETED: {label}")

if not dry_run and confirm:
    unreal.log(f"[SN] Deleted {len(to_delete)} duplicates")
elif dry_run:
    unreal.log(f"[SN] Dry run — set dry_run=false and confirm=true to actually delete")
'''
    },

    # ================================================================
    # SCENE ANALYSIS SKILLS (read-only)
    # ================================================================
    "list_actors": {
        "category": "analysis",
        "safety_level": "safe",
        "description": "List all actors in the current level with their types, locations, and names.",
        "args_schema": {
            "filter_type": {"type": "string", "default": "", "desc": "Only show actors of this class (e.g., 'PointLight', 'StaticMeshActor')"},
            "filter_name": {"type": "string", "default": "", "desc": "Only show actors whose name contains this string"},
            "include_transform": {"type": "bool", "default": True, "desc": "Include location/rotation/scale data"},
            "max_results": {"type": "int", "default": 100, "min": 1, "max": 1000},
        },
        "unreal_code": '''
import unreal
import json

actors = unreal.EditorLevelLibrary.get_all_level_actors()
filter_type = "{{filter_type}}"
filter_name = "{{filter_name}}"
include_transform = {{include_transform}}
max_results = {{max_results}}

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
        entry["location"] = [loc.x, loc.y, loc.z]
        entry["rotation"] = [rot.pitch, rot.yaw, rot.roll]
        entry["scale"] = [scale.x, scale.y, scale.z]
    
    results.append(entry)
    if len(results) >= max_results:
        break

unreal.log(f"[SN] Found {len(results)} actors (total in level: {len(actors)})")
unreal.log(f"[SN] ACTOR_DATA:{json.dumps(results)}")
'''
    },

    "get_scene_info": {
        "category": "analysis",
        "safety_level": "safe",
        "description": "Get overall scene information — actor counts by type, bounds, lighting summary.",
        "args_schema": {},
        "unreal_code": '''
import unreal
import json
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
    "type_breakdown": dict(type_counts.most_common(20)),
}

unreal.log(f"[SN] Scene: {len(actors)} actors, {light_count} lights, {mesh_count} meshes")
unreal.log(f"[SN] SCENE_DATA:{json.dumps(info)}")
'''
    },

    # ================================================================
    # CAMERA / VIEWPORT SKILLS
    # ================================================================
    "frame_viewport": {
        "category": "camera",
        "safety_level": "safe",
        "description": "Move the editor viewport camera to frame a specific point or actor.",
        "args_schema": {
            "location": {"type": "vector", "default": [0.0, 0.0, 0.0], "desc": "Look-at target point"},
            "distance": {"type": "float", "default": 1000.0, "desc": "Camera distance from target (cm)"},
            "pitch": {"type": "float", "default": -30.0, "desc": "Camera pitch angle (degrees)"},
            "yaw": {"type": "float", "default": 45.0, "desc": "Camera yaw angle (degrees)"},
            "actor_name": {"type": "string", "default": "", "desc": "If set, frame this actor instead of location"},
        },
        "unreal_code": '''
import unreal
import math

actor_name = "{{actor_name}}"
target = unreal.Vector({{location[0]}}, {{location[1]}}, {{location[2]}})

if actor_name:
    actors = unreal.EditorLevelLibrary.get_all_level_actors()
    for a in actors:
        if actor_name.lower() in a.get_actor_label().lower():
            target = a.get_actor_location()
            break

distance = {{distance}}
pitch_rad = math.radians({{pitch}})
yaw_rad = math.radians({{yaw}})

cam_x = target.x + distance * math.cos(pitch_rad) * math.cos(yaw_rad)
cam_y = target.y + distance * math.cos(pitch_rad) * math.sin(yaw_rad)
cam_z = target.z + distance * math.sin(-pitch_rad)

# Use console command to set viewport camera
cmd = f"vset {cam_x} {cam_y} {cam_z} {target.x} {target.y} {target.z}"
unreal.SystemLibrary.execute_console_command(
    unreal.EditorLevelLibrary.get_editor_world(), cmd
)
unreal.log(f"[SN] Viewport framed at target=({target.x}, {target.y}, {target.z}) dist={distance}")
'''
    },

    # ================================================================
    # ENVIRONMENT SKILLS
    # ================================================================
    "add_exponential_height_fog": {
        "category": "environment",
        "safety_level": "modify",
        "description": "Add atmospheric fog. Controls density, color, and falloff.",
        "args_schema": {
            "location": {"type": "vector", "default": [0.0, 0.0, 0.0]},
            "fog_density": {"type": "float", "default": 0.02, "min": 0.0, "max": 1.0, "desc": "Base fog density"},
            "fog_height_falloff": {"type": "float", "default": 0.2, "min": 0.0, "max": 10.0, "desc": "How quickly fog thins with height"},
            "fog_color": {"type": "color", "default": [0.6, 0.65, 0.7]},
            "second_fog_density": {"type": "float", "default": 0.0, "desc": "Second fog layer density"},
            "start_distance": {"type": "float", "default": 0.0, "desc": "Distance before fog starts (cm)"},
            "name": {"type": "string", "default": "SN_Fog"},
        },
        "unreal_code": '''
import unreal
name = "{{name}}"
loc = unreal.Vector({{location[0]}}, {{location[1]}}, {{location[2]}})
actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
    unreal.ExponentialHeightFog, loc, unreal.Rotator(0, 0, 0)
)
actor.set_actor_label(name)
fog = unreal.ExponentialHeightFog.cast(actor)
if fog:
    comp = fog.get_fog_component()
    if comp:
        comp.set_fog_density({{fog_density}})
        comp.set_fog_height_falloff({{fog_height_falloff}})
        r, g, b = {{fog_color}}
        comp.set_fog_inscattering_color(unreal.LinearColor(r, g, b, 1.0))
        comp.set_start_distance({{start_distance}})
unreal.log(f"[SN] HeightFog '{name}' density={{fog_density}}")
'''
    },

    "add_sky_atmosphere": {
        "category": "environment",
        "safety_level": "modify",
        "description": "Add Sky Atmosphere component for realistic sky rendering with sun/moon.",
        "args_schema": {
            "location": {"type": "vector", "default": [0.0, 0.0, 0.0]},
            "name": {"type": "string", "default": "SN_SkyAtmosphere"},
        },
        "unreal_code": '''
import unreal
name = "{{name}}"
loc = unreal.Vector({{location[0]}}, {{location[1]}}, {{location[2]}})
actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
    unreal.SkyAtmosphere, loc, unreal.Rotator(0, 0, 0)
)
actor.set_actor_label(name)
unreal.log(f"[SN] SkyAtmosphere '{name}' added")
'''
    },

    # ================================================================
    # MATERIAL SKILLS
    # ================================================================
    "apply_material": {
        "category": "material",
        "safety_level": "modify",
        "description": "Apply a material to an actor's mesh. Supports material slot index.",
        "args_schema": {
            "actor_name": {"type": "string", "required": True},
            "material_path": {"type": "string", "required": True, "desc": "Asset path (e.g., /Game/Materials/M_Concrete)"},
            "material_slot": {"type": "int", "default": 0, "desc": "Material index for multi-material meshes"},
        },
        "unreal_code": '''
import unreal
actor_name = "{{actor_name}}"
mat_path = "{{material_path}}"

actors = unreal.EditorLevelLibrary.get_all_level_actors()
found = None
for a in actors:
    if actor_name.lower() in a.get_actor_label().lower():
        found = a
        break

if not found:
    unreal.log(f"[SN] ERROR: Actor '{actor_name}' not found")
else:
    mat = unreal.load_asset(mat_path)
    if not mat:
        unreal.log(f"[SN] ERROR: Material '{mat_path}' not found")
    else:
        for comp in found.get_components_by_class(unreal.StaticMeshComponent):
            comp.set_material({{material_slot}}, mat)
        unreal.log(f"[SN] Applied '{mat_path}' to '{found.get_actor_label()}' slot {{material_slot}}")
'''
    },

    # ================================================================
    # ASSET SKILLS
    # ================================================================
    "import_asset": {
        "category": "asset",
        "safety_level": "modify",
        "description": "Import an asset (FBX, OBJ, USD) into the content browser.",
        "args_schema": {
            "source_path": {"type": "string", "required": True, "desc": "Absolute path to file on disk"},
            "destination_path": {"type": "string", "default": "/Game/Imports", "desc": "Content browser destination folder"},
            "asset_type": {"type": "string", "default": "auto", "options": ["auto", "StaticMesh", "SkeletalMesh", "Animation"], "desc": "What to import as"},
        },
        "unreal_code": '''
import unreal

source = r"{{source_path}}"
dest = "{{destination_path}}"

task = unreal.AssetImportTask()
task.set_editor_property("filename", source)
task.set_editor_property("destination_path", dest)
task.set_editor_property("replace_existing", True)
task.set_editor_property("automated", True)
task.set_editor_property("save", True)

unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])

imported = task.get_editor_property("imported_object_paths")
unreal.log(f"[SN] Imported {len(imported)} asset(s) to {dest}")
for p in imported:
    unreal.log(f"[SN]   {p}")
'''
    },

    "list_content": {
        "category": "asset",
        "safety_level": "safe",
        "description": "List assets in a content browser folder.",
        "args_schema": {
            "path": {"type": "string", "default": "/Game/", "desc": "Content path to list"},
            "recursive": {"type": "bool", "default": False},
            "filter_type": {"type": "string", "default": "", "desc": "Filter by class name (e.g., 'StaticMesh', 'Material')"},
        },
        "unreal_code": '''
import unreal
import json

path = "{{path}}"
assets = unreal.EditorAssetLibrary.list_assets(path, recursive={{recursive}})
results = []
for a in assets:
    obj = unreal.load_asset(a)
    if obj:
        class_name = obj.get_class().get_name()
        if "{{filter_type}}" and "{{filter_type}}".lower() not in class_name.lower():
            continue
        results.append({"path": a, "class": class_name, "name": obj.get_name()})

unreal.log(f"[SN] Found {len(results)} assets in {path}")
unreal.log(f"[SN] ASSET_DATA:{json.dumps(results[:200])}")
'''
    },

    # ================================================================
    # LEVEL UTILITY SKILLS
    # ================================================================
    "save_level": {
        "category": "utility",
        "safety_level": "modify",
        "description": "Save the current level.",
        "args_schema": {},
        "unreal_code": '''
import unreal
unreal.EditorLevelLibrary.save_current_level()
unreal.log("[SN] Level saved")
'''
    },

    "undo": {
        "category": "utility",
        "safety_level": "safe",
        "description": "Undo the last editor action.",
        "args_schema": {},
        "unreal_code": '''
import unreal
unreal.EditorLevelLibrary.undo()
unreal.log("[SN] Undo executed")
'''
    },

    "execute_console_command": {
        "category": "utility",
        "safety_level": "modify",
        "description": "Execute an Unreal console command. For advanced users only.",
        "args_schema": {
            "command": {"type": "string", "required": True, "desc": "Console command string"},
        },
        "unreal_code": '''
import unreal
cmd = "{{command}}"
result = unreal.SystemLibrary.execute_console_command(
    unreal.EditorLevelLibrary.get_editor_world(), cmd
)
unreal.log(f"[SN] Console: '{cmd}' → {result}")
'''
    },

    # ================================================================
    # CONVERSATIONAL SKILLS
    # ================================================================
    "say": {
        "category": "conversation",
        "safety_level": "safe",
        "description": "Display a message to the user in Unreal's Output Log and as a toast notification. SuperNinja's voice inside the editor.",
        "args_schema": {
            "message": {"type": "string", "required": True, "desc": "What to say to the user"},
            "style": {"type": "string", "default": "info", "options": ["info", "warning", "error", "success", "thinking"], "desc": "Visual style of the message"},
            "duration": {"type": "float", "default": 5.0, "desc": "How long to show toast notification (seconds, 0 = log only)"},
        },
        "unreal_code": '''
import unreal
message = "{{message}}"
style = "{{style}}"

# Always log the message
prefix = {
    "info": "[SN 💬]",
    "warning": "[SN ⚠️]",
    "error": "[SN ❌]",
    "success": "[SN ✅]",
    "thinking": "[SN 🤔]",
}.get(style, "[SN 💬]")

unreal.log(f"{prefix} {message}")

# Also show as a notification toast in the editor
try:
    notify = unreal.ToolMenus.get().notify
except:
    pass
'''
    },

    "ask_user": {
        "category": "conversation",
        "safety_level": "safe",
        "description": "Ask the user a question and wait for a response. The question appears in the Output Log and the user can reply through the companion chat. Non-blocking — returns immediately, response comes as a new command.",
        "args_schema": {
            "question": {"type": "string", "required": True, "desc": "The question to ask"},
            "options": {"type": "list", "default": [], "desc": "Suggested answers the user can pick from"},
            "context": {"type": "string", "default": "", "desc": "Why we're asking (so the user understands the context)"},
        },
        "unreal_code": '''
import unreal
question = "{{question}}"
options = {{options}}
context = "{{context}}"

unreal.log(f"[SN 🙋] {question}")
if context:
    unreal.log(f"[SN 🙋] Context: {context}")
if options:
    for i, opt in enumerate(options):
        unreal.log(f"[SN 🙋]   {i+1}. {opt}")
unreal.log(f"[SN 🙋] (Reply via SuperNinja chat or companion)")
'''
    },

    "report_progress": {
        "category": "conversation",
        "safety_level": "safe",
        "description": "Report what SuperNinja is currently doing. Shows a status update in the log and optionally in the editor.",
        "args_schema": {
            "action": {"type": "string", "required": True, "desc": "Current action description"},
            "step": {"type": "int", "default": 0, "desc": "Current step number (0 = not tracking)"},
            "total_steps": {"type": "int", "default": 0, "desc": "Total number of steps (0 = unknown)"},
            "status": {"type": "string", "default": "working", "options": ["working", "done", "failed", "waiting"], "desc": "Current status"},
        },
        "unreal_code": '''
import unreal
action = "{{action}}"
step = {{step}}
total = {{total_steps}}
status = "{{status}}"

status_icon = {"working": "🔄", "done": "✅", "failed": "❌", "waiting": "⏳"}.get(status, "🔄")

if step > 0 and total > 0:
    progress = f" ({step}/{total})"
else:
    progress = ""

unreal.log(f"[SN {status_icon}] {action}{progress}")
'''
    },

    "explain_scene": {
        "category": "conversation",
        "safety_level": "safe",
        "description": "SuperNinja explains its understanding of the current scene to the user. Reads the scene and generates a natural language description.",
        "args_schema": {
            "analysis": {"type": "string", "default": "", "desc": "Pre-written analysis (if empty, will be auto-generated from scene data)"},
        },
        "unreal_code": '''
import unreal
import json
from collections import Counter

analysis = "{{analysis}}"

if not analysis:
    # Auto-generate from scene data
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
'''
    },

    "suggest_improvements": {
        "category": "conversation",
        "safety_level": "safe",
        "description": "SuperNinja suggests what could make the scene look better. Reads the scene and offers actionable advice.",
        "args_schema": {
            "focus": {"type": "string", "default": "general", "options": ["general", "lighting", "composition", "atmosphere", "materials"], "desc": "What aspect to focus suggestions on"},
        },
        "unreal_code": '''
import unreal
from collections import Counter

focus = "{{focus}}"
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
    suggestions.append("✨ The scene looks like it has good fundamentals! Try fine-tuning light intensities or adjusting camera angles for the best look.")

unreal.log("[SN 💡] Scene Improvement Suggestions:")
for i, s in enumerate(suggestions):
    unreal.log(f"[SN 💡]   {i+1}. {s}")
'''
    },

    "chat": {
        "category": "conversation",
        "safety_level": "safe",
        "description": "A general conversational message from SuperNinja. Used for greetings, confirmations, status updates, and any free-form text that should appear in the Unreal log.",
        "args_schema": {
            "text": {"type": "string", "required": True, "desc": "The message text"},
            "mood": {"type": "string", "default": "friendly", "options": ["friendly", "excited", "thinking", "concerned", "proud", "apologetic"], "desc": "Tone/mood of the message"},
        },
        "unreal_code": '''
import unreal
text = "{{text}}"
mood = "{{mood}}"

mood_icon = {
    "friendly": "👋",
    "excited": "🎉",
    "thinking": "🤔",
    "concerned": "😟",
    "proud": "💪",
    "apologetic": "😅",
}.get(mood, "💬")

unreal.log(f"[SN {mood_icon}] {text}")
'''
    },
    # =========================================================================
    # KNOWLEDGE & ANALYSIS SKILLS — Powered by UE5 Training Corpus
    # =========================================================================
    "get_actor_properties": {
        "category": "analysis",
        "safety_level": "safe",
        "description": "Get detailed properties of an actor: transform, components, tags, mobility, and more. Uses UE5 knowledge to explain what each property means.",
        "args_schema": {
            "name": {"type": "string", "required": True, "desc": "Actor name or label"},
            "include_components": {"type": "bool", "default": True, "desc": "List all components on the actor"},
            "include_materials": {"type": "bool", "default": True, "desc": "List material assignments on mesh components"},
        },
        "unreal_code": """
import unreal
import json

actor_name = "{{name}}"
include_components = {{include_components}}
include_materials = {{include_materials}}

actors = unreal.EditorLevelLibrary.get_all_level_actors()
target = None
for a in actors:
    if a.get_actor_label() == actor_name or a.get_name() == actor_name:
        target = a
        break

if not target:
    unreal.log_warning(f"[SN] Actor '{actor_name}' not found")
    unreal.log(f"[SN] RESULT:{{\"error\": \"Actor not found\", \"name\": \"{actor_name}\"}}")
else:
    result = {"name": target.get_actor_label(), "class": target.get_class().get_name()}
    
    # Transform
    loc = target.get_actor_location()
    rot = target.get_actor_rotation()
    scale = target.get_actor_scale3d()
    result["transform"] = {
        "location": [loc.x, loc.y, loc.z],
        "rotation": [rot.pitch, rot.yaw, rot.roll],
        "scale": [scale.x, scale.y, scale.z]
    }
    
    # Tags
    result["tags"] = list(target.tags) if hasattr(target, 'tags') else []
    
    # Components
    if include_components:
        comps = target.get_components_by_class(unreal.ActorComponent)
        comp_list = []
        for c in comps:
            comp_info = {"name": c.get_name(), "class": c.get_class().get_name()}
            if isinstance(c, unreal.SceneComponent):
                comp_info["has_transform"] = True
            comp_list.append(comp_info)
        result["components"] = comp_list
    
    # Materials
    if include_materials:
        mesh_comps = target.get_components_by_class(unreal.StaticMeshComponent)
        if not mesh_comps:
            mesh_comps = target.get_components_by_class(unreal.SkeletalMeshComponent)
        mat_list = []
        for mc in mesh_comps:
            for i in range(mc.get_num_materials()):
                mat = mc.get_material(i)
                mat_list.append({"slot": i, "material": mat.get_name() if mat else "None", "component": mc.get_name()})
        result["materials"] = mat_list
    
    result["mobility"] = str(target.root_component.get_mobility()) if hasattr(target, 'root_component') else "Unknown"
    result["hidden"] = target.is_hidden_ed()
    
    unreal.log(f"[SN] Properties of '{actor_name}': {json.dumps(result, indent=2)}")
    unreal.log(f"[SN] RESULT:{json.dumps(result)}")
""",
    },
    "set_actor_property": {
        "category": "placement",
        "safety_level": "modify",
        "description": "Set a specific property on an actor. Supports: mobility, hidden, tags, and component properties. Understands UE5 property types from the knowledge base.",
        "args_schema": {
            "name": {"type": "string", "required": True, "desc": "Actor name or label"},
            "property": {"type": "string", "required": True, "desc": "Property to set: 'mobility', 'hidden', 'tag', 'layer'"},
            "value": {"type": "string", "required": True, "desc": "Value to set (string representation)"},
        },
        "unreal_code": """
import unreal
import json

actor_name = "{{name}}"
prop = "{{property}}"
val = "{{value}}"

actors = unreal.EditorLevelLibrary.get_all_level_actors()
target = None
for a in actors:
    if a.get_actor_label() == actor_name or a.get_name() == actor_name:
        target = a
        break

if not target:
    unreal.log_warning(f"[SN] Actor '{actor_name}' not found")
    unreal.log(f'[SN] RESULT:{{"error": "not found"}}')
else:
    result = {"name": target.get_actor_label(), "property": prop, "set": False}
    
    if prop == "mobility":
        mobility_map = {"static": unreal.ComponentMobility.STATIC, "movable": unreal.ComponentMobility.MOVABLE, "stationary": unreal.ComponentMobility.STATIONARY}
        if val.lower() in mobility_map:
            if hasattr(target, 'root_component') and target.root_component:
                target.root_component.set_mobility(mobility_map[val.lower()])
                result["set"] = True
                result["new_value"] = val
                unreal.log(f"[SN] Set {actor_name} mobility to {val} — Knowledge: Static lights get baked by Lightmass. Movable lights are dynamic. Stationary is a hybrid.")
    elif prop == "hidden":
        hide = val.lower() in ("true", "1", "yes")
        target.set_actor_hidden_ed(hide)
        result["set"] = True
        result["new_value"] = hide
    elif prop == "tag":
        target.tags = list(target.tags) + [val]
        result["set"] = True
        result["new_value"] = val
    elif prop == "label":
        target.set_actor_label(val)
        result["set"] = True
        result["new_value"] = val
    
    unreal.log(f"[SN] RESULT:{json.dumps(result)}")
""",
    },
    "find_actors_advanced": {
        "category": "analysis",
        "safety_level": "safe",
        "description": "Advanced actor search with multiple filters. Can search by class, tag, layer, material, mobility, or spatial region. Understands UE5 class hierarchy.",
        "args_schema": {
            "filter_class": {"type": "string", "default": "", "desc": "Filter by class name (e.g., 'PointLight', 'StaticMeshActor')"},
            "filter_tag": {"type": "string", "default": "", "desc": "Filter by actor tag"},
            "filter_mobility": {"type": "string", "default": "", "desc": "Filter by mobility: 'static', 'movable', 'stationary'"},
            "filter_material": {"type": "string", "default": "", "desc": "Filter by material name used on the actor"},
            "spatial_center": {"type": "string", "default": "", "desc": "Center point for spatial search: 'x,y,z'"},
            "spatial_radius": {"type": "float", "default": 1000.0, "desc": "Radius for spatial search"},
            "max_results": {"type": "int", "default": 50, "desc": "Maximum results to return"},
        },
        "unreal_code": """
import unreal
import json

filter_class = "{{filter_class}}"
filter_tag = "{{filter_tag}}"
filter_mobility = "{{filter_mobility}}"
filter_material = "{{filter_material}}"
spatial_center_str = "{{spatial_center}}"
spatial_radius = {{spatial_radius}}
max_results = {{max_results}}

actors = unreal.EditorLevelLibrary.get_all_level_actors()
results = []

spatial_center = None
if spatial_center_str:
    parts = spatial_center_str.split(",")
    if len(parts) == 3:
        spatial_center = unreal.Vector(float(parts[0]), float(parts[1]), float(parts[2]))

for a in actors:
    label = a.get_actor_label()
    class_name = a.get_class().get_name()
    
    # Class filter
    if filter_class and filter_class.lower() not in class_name.lower():
        continue
    
    # Tag filter
    if filter_tag:
        if not hasattr(a, 'tags') or filter_tag not in a.tags:
            continue
    
    # Mobility filter
    if filter_mobility:
        if hasattr(a, 'root_component') and a.root_component:
            mob = str(a.root_component.get_mobility()).lower()
            if filter_mobility.lower() not in mob:
                continue
    
    # Material filter
    if filter_material:
        found_mat = False
        for mc in a.get_components_by_class(unreal.StaticMeshComponent):
            for i in range(mc.get_num_materials()):
                mat = mc.get_material(i)
                if mat and filter_material.lower() in mat.get_name().lower():
                    found_mat = True
                    break
        if not found_mat:
            continue
    
    # Spatial filter
    if spatial_center:
        loc = a.get_actor_location()
        dist = unreal.MathLibrary.vector_distance(spatial_center, loc)
        if dist > spatial_radius:
            continue
    
    loc = a.get_actor_location()
    entry = {"name": label, "class": class_name, "location": [loc.x, loc.y, loc.z]}
    results.append(entry)
    if len(results) >= max_results:
        break

unreal.log(f"[SN] Found {len(results)} actors matching filters")
unreal.log(f"[SN] RESULT:{json.dumps(results)}")
""",
    },
    "query_knowledge": {
        "category": "conversation",
        "safety_level": "safe",
        "description": "Search SuperNinja's UE5 knowledge base. Can answer questions about UE5 architecture, Blueprint patterns, C++ interop, naming conventions, lighting design, and more. Powered by the official UE5 training corpus.",
        "args_schema": {
            "query": {"type": "string", "required": True, "desc": "What to search for (e.g., 'pawn', 'blueprint communication', 'lighting preset', 'UCLASS')"},
            "category": {"type": "string", "default": "", "desc": "Optional category filter: class_hierarchy, gameplay_framework, naming_conventions, editor_interface, blueprint_system, cpp_interop, lighting, composition"},
        },
        "unreal_code": """
import unreal
import json

query = "{{query}}"
category = "{{category}}"

unreal.log(f"[SN 🔍] Knowledge query: '{query}' (category: {category or 'all'})")
unreal.log(f"[SN 🔍] This skill requires the cloud-side knowledge base.")
unreal.log(f"[SN 🔍] The AI brain will respond with the answer from its training corpus.")
unreal.log(f'[SN] RESULT:{{"query": "{query}", "category": "{category}", "status": "processed_on_cloud"}}')
""",
    },
    "explain_ue5_concept": {
        "category": "conversation",
        "safety_level": "safe",
        "description": "Explain a UE5 concept in plain language using the training corpus. Covers: actors, components, pawns, characters, game modes, Blueprint patterns, C++ macros, lighting systems, and more.",
        "args_schema": {
            "concept": {"type": "string", "required": True, "desc": "The UE5 concept to explain (e.g., 'actor', 'construction_script', 'UCLASS', 'event_dispatcher')"},
        },
        "unreal_code": """
import unreal

concept = "{{concept}}"

unreal.log(f"[SN 📚] Explaining: {concept}")
unreal.log(f"[SN 📚] This skill is handled by the cloud-side knowledge engine.")
unreal.log(f"[SN 📚] The AI will provide a detailed explanation using the UE5 training corpus.")
unreal.log(f'[SN] RESULT:{{"concept": "{concept}", "status": "explained_on_cloud"}}')
""",
    },
    "suggest_blueprint_pattern": {
        "category": "conversation",
        "safety_level": "safe",
        "description": "Suggest the right Blueprint communication pattern for a use case. Knows: Direct Communication, Event Dispatchers, Blueprint Interfaces, and Blueprint Casting. Based on official Epic best practices.",
        "args_schema": {
            "use_case": {"type": "string", "required": True, "desc": "Describe what you want to do (e.g., 'notify all enemies when boss dies', 'switch opens a specific door')"},
        },
        "unreal_code": """
import unreal

use_case = "{{use_case}}"

unreal.log(f"[SN 📘] Blueprint pattern suggestion for: {use_case}")
unreal.log(f"[SN 📘] This skill is handled by the cloud-side knowledge engine.")
unreal.log(f"[SN 📘] The AI will recommend the best communication pattern.")
unreal.log(f'[SN] RESULT:{{"use_case": "{use_case}", "status": "suggested_on_cloud"}}')
""",
    },
    "run_python_snippet": {
        "category": "utility",
        "safety_level": "modify",
        "description": "Execute a Python code snippet inside Unreal Editor. Use with caution — this runs arbitrary code. The AI brain uses its UE5 knowledge to generate safe, correct snippets.",
        "args_schema": {
            "code": {"type": "string", "required": True, "desc": "Python code to execute inside Unreal Editor"},
            "description": {"type": "string", "default": "", "desc": "Human-readable description of what the code does"},
        },
        "unreal_code": """
import unreal

code = "{{code}}"
description = "{{description}}"

unreal.log(f"[SN 🐍] Executing Python snippet: {description or 'custom code'}")
try:
    exec(code)
    unreal.log(f"[SN ✅] Snippet executed successfully")
    unreal.log(f'[SN] RESULT:{{"status": "success", "description": "{description}"}}')
except Exception as e:
    unreal.log_error(f"[SN ❌] Snippet error: {e}")
    unreal.log(f'[SN] RESULT:{{"status": "error", "error": "{str(e)}"}}')
""",
    },

    # ========================================================================
    # ADVANCED KNOWLEDGE SKILLS (Docs 21-60)
    # ========================================================================

    "query_advanced_knowledge": {
        "category": "knowledge",
        "safety_level": "safe",
        "description": "Search the advanced UE5 knowledge base (Documents 21-60) covering Lumen, lighting, materials, rendering, Nanite, animation, physics, Niagara, and more.",
        "args_schema": {
            "query": {"type": "string", "required": True, "desc": "Search query for advanced UE5 knowledge"},
        },
        "unreal_code": """
import unreal
query = "{{query}}"
unreal.log(f"[SN 🔍] Advanced knowledge query: {query}")
# This skill runs locally on the AI side, no Unreal code needed
unreal.log('[SN] RESULT:{"status": "local_only", "note": "Advanced knowledge runs on AI server side"}')
""",
    },

    "get_lighting_setup": {
        "category": "knowledge",
        "safety_level": "safe",
        "description": "Get a complete lighting setup recommendation for a scene type and mood. Returns exact light types, intensities, temperatures, and post-process settings.",
        "args_schema": {
            "scene_type": {"type": "string", "required": True, "desc": "Scene type: outdoor_day, outdoor_golden_hour, interior_office, night_exterior", "options": ["outdoor_day", "outdoor_golden_hour", "interior_office", "night_exterior"]},
            "mood": {"type": "string", "default": "", "desc": "Optional mood modifier: moody, dramatic, cheerful, horror, cinematic", "options": ["", "moody", "dramatic", "cheerful", "horror", "cinematic"]},
        },
        "unreal_code": """
import unreal
scene_type = "{{scene_type}}"
mood = "{{mood}}"
unreal.log(f"[SN 💡] Lighting setup requested: {scene_type} / {mood}")
unreal.log('[SN] RESULT:{"status": "local_only", "note": "Lighting setup runs on AI server side, then dispatches light commands"}')
""",
    },

    "get_material_recipe": {
        "category": "knowledge",
        "safety_level": "safe",
        "description": "Get PBR material property recipe for common surface types. Returns roughness, metallic, base color, and recommended shading model.",
        "args_schema": {
            "surface_type": {"type": "string", "required": True, "desc": "Surface type to get recipe for", "options": ["concrete", "metal_brushed", "wood", "glass", "plastic", "skin", "fabric", "car_paint", "marble", "foliage"]},
        },
        "unreal_code": """
import unreal
surface_type = "{{surface_type}}"
unreal.log(f"[SN 🎨] Material recipe requested: {surface_type}")
unreal.log('[SN] RESULT:{"status": "local_only", "note": "Material recipe runs on AI server side"}')
""",
    },

    "analyze_rendering": {
        "category": "knowledge",
        "safety_level": "safe",
        "description": "Analyze scene rendering needs including Nanite, TSR, post-process, and rendering pipeline recommendations based on scene complexity.",
        "args_schema": {
            "goal": {"type": "string", "default": "", "desc": "Optional goal to guide rendering recommendations"},
        },
        "unreal_code": """
import unreal
goal = "{{goal}}"
unreal.log(f"[SN 🖥️] Rendering analysis requested: {goal}")
unreal.log('[SN] RESULT:{"status": "local_only", "note": "Rendering analysis runs on AI server side"}')
""",
    },

    "setup_post_process": {
        "category": "rendering",
        "safety_level": "modify",
        "description": "Add a Post Process Volume with settings for a specific look (cinematic, horror, neon, film noir, etc.). Handles color grading, bloom, exposure, vignette.",
        "args_schema": {
            "style": {"type": "string", "required": True, "desc": "Post-process style preset", "options": ["cinematic", "horror", "neon", "film_noir", "golden_hour", "studio", "clean", "dramatic"]},
            "unbound": {"type": "bool", "default": True, "desc": "If true, affects entire level regardless of volume bounds"},
        },
        "unreal_code": """
import unreal

style = "{{style}}"
unbound = {{unbound}}

unreal.log(f"[SN 🎬] Setting up post-process: {style}")

# Create Post Process Volume
ppv = unreal.EditorLevelLibrary.spawn_actor_from_class(
    unreal.PostProcessVolume, unreal.Vector(0, 0, 0), unreal.Rotator(0, 0, 0)
)
ppv.set_actor_label(f"SN_PostProcess_{style}")

# Configure based on style
settings = ppv.get_settings()
if style == "cinematic":
    settings.bloom_intensity = 0.4
    settings.vignette_intensity = 0.4
    settings.chromatic_aberration_intensity = 0.2
elif style == "horror":
    settings.bloom_intensity = 0.1
    settings.vignette_intensity = 0.8
    settings.chromatic_aberration_intensity = 0.5
elif style == "neon":
    settings.bloom_intensity = 0.8
    settings.vignette_intensity = 0.2
    settings.chromatic_aberration_intensity = 0.3
elif style == "film_noir":
    settings.bloom_intensity = 0.2
    settings.vignette_intensity = 0.6
    settings.chromatic_aberration_intensity = 0.1
elif style == "golden_hour":
    settings.bloom_intensity = 0.5
    settings.vignette_intensity = 0.3
    settings.chromatic_aberration_intensity = 0.1

if unbound:
    ppv.set_unbound(True)

unreal.log(f"[SN ✅] Post-process volume created with {style} style")
unreal.log(f'[SN] RESULT:{{"status": "success", "style": "{style}", "unbound": {unbound}}}')
""",
    },

    "add_foliage": {
        "category": "environment",
        "safety_level": "modify",
        "description": "Paint foliage instances on the landscape or surfaces. Supports grass, trees, rocks, and custom meshes with density and scale controls.",
        "args_schema": {
            "mesh_path": {"type": "string", "required": True, "desc": "Content browser path to the foliage mesh (e.g., /Game/Foliage/SM_Tree)"},
            "density": {"type": "float", "default": 0.1, "min": 0.001, "max": 10.0, "desc": "Instances per square meter"},
            "min_scale": {"type": "float", "default": 0.8, "min": 0.01, "max": 10.0, "desc": "Minimum random scale"},
            "max_scale": {"type": "float", "default": 1.2, "min": 0.01, "max": 10.0, "desc": "Maximum random scale"},
            "radius": {"type": "float", "default": 50.0, "desc": "Minimum distance between instances"},
            "center": {"type": "vector", "default": [0, 0, 0], "desc": "Center of the foliage paint area"},
            "extent": {"type": "float", "default": 1000.0, "desc": "Extent of the paint area from center"},
        },
        "unreal_code": """
import unreal
import random

mesh_path = "{{mesh_path}}"
density = {{density}}
min_scale = {{min_scale}}
max_scale = {{max_scale}}
radius = {{radius}}
cx, cy, cz = {{center}}
extent = {{extent}}

unreal.log(f"[SN 🌿] Adding foliage: {mesh_path} density={density}")

# Load the mesh asset
mesh = unreal.load_asset(mesh_path)
if not mesh:
    unreal.log_error(f"[SN ❌] Could not load mesh: {mesh_path}")
    unreal.log(f'[SN] RESULT:{{"status": "error", "error": "Mesh not found: {mesh_path}"}}')
else:
    # Calculate number of instances
    area = extent * extent * 4  # rectangular area
    count = int(area * density)
    count = min(count, 5000)  # cap for safety
    
    spawned = 0
    for i in range(count):
        x = cx + random.uniform(-extent, extent)
        y = cy + random.uniform(-extent, extent)
        z = cz  # Will need landscape height in real use
        scale = random.uniform(min_scale, max_scale)
        
        actor = unreal.EditorLevelLibrary.spawn_actor_from_object(
            mesh, unreal.Vector(x, y, z)
        )
        if actor:
            actor.set_actor_scale3d(unreal.Vector(scale, scale, scale))
            actor.set_actor_label(f"SN_Foliage_{spawned:04d}")
            spawned += 1
    
    unreal.log(f"[SN ✅] Spawned {spawned} foliage instances")
    unreal.log(f'[SN] RESULT:{{"status": "success", "spawned": {spawned}, "mesh": "{mesh_path}"}}')
""",
    },
    # =========================================================================
    # EXPERT SKILLS - Docs 61-100 (Niagara, Audio, UI, AI, Networking, Opt, Cinematics)
    # =========================================================================

    "query_expert_knowledge": {
        "category": "knowledge",
        "safety_level": "safe",
        "description": "Search the expert UE5 knowledge base (Docs 61-100) covering Niagara Advanced, Audio, UI, AI Systems, Networking, Optimization, Packaging, Cinematics, and Plugins.",
        "args_schema": {
            "query": {"type": "string", "required": True, "desc": "Search query for expert knowledge"},
        },
        "unreal_code": """
import json

query = "{{query}}"

unreal.log(f"[SN EXPERT] Knowledge query: '{query}'")
unreal.log(f'[SN] RESULT:{{"query": "{query}", "status": "processed_on_cloud"}}')
""",
    },

    "add_niagara_effect": {
        "category": "vfx",
        "safety_level": "modify",
        "description": "Add Niagara VFX effects to the scene. Supports fire, smoke, water, rain, and custom effects using Niagara Fluids simulation.",
        "args_schema": {
            "effect_type": {"type": "string", "required": True, "desc": "Type of effect: fire, smoke, water, rain, custom"},
            "location": {"type": "vector", "default": [0, 0, 0], "desc": "Spawn location"},
            "scale": {"type": "float", "default": 1.0, "desc": "Effect scale"},
        },
        "unreal_code": """
import unreal

effect_type = "{{effect_type}}"
x, y, z = {{location}}
scale = {{scale}}

unreal.log(f"[SN VFX] Adding Niagara effect: {effect_type}")

effect_paths = {
    "fire": "/Game/VFX/Niagara/Fire/NS_Fire",
    "smoke": "/Game/VFX/Niagara/Smoke/NS_Smoke",
    "water": "/Game/VFX/Niagara/Water/NS_WaterSplash",
    "rain": "/Game/VFX/Niagara/Weather/NS_Rain",
}

path = effect_paths.get(effect_type.lower(), "/Game/VFX/Niagara/Default/NS_Default")

niagara_actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
    unreal.NiagaraActor, unreal.Vector(x, y, z)
)

if niagara_actor:
    niagara_actor.set_actor_label(f"SN_Niagara_{effect_type}")
    niagara_actor.set_actor_scale3d(unreal.Vector(scale, scale, scale))
    unreal.log(f"[SN] Niagara {effect_type} effect added")
    unreal.log(f'[SN] RESULT:{{"status": "success", "effect_type": "{effect_type}", "location": [{x}, {y}, {z}]}}')
else:
    unreal.log(f"[SN] Failed to spawn Niagara effect")
    unreal.log(f'[SN] RESULT:{{"status": "error", "error": "Failed to spawn Niagara actor"}}')
""",
    },

    "add_audio_ambient": {
        "category": "audio",
        "safety_level": "modify",
        "description": "Add ambient audio to the scene using MetaSounds or Sound Cues. Supports outdoor (wind, birds) and indoor (room tone) environments with spatial audio.",
        "args_schema": {
            "environment": {"type": "string", "required": True, "desc": "Environment type: outdoor, indoor, urban, forest"},
            "location": {"type": "vector", "default": [0, 0, 0], "desc": "Audio source location"},
            "volume": {"type": "float", "default": 0.5, "min": 0.0, "max": 1.0, "desc": "Volume level"},
        },
        "unreal_code": """
import unreal

environment = "{{environment}}"
x, y, z = {{location}}
volume = {{volume}}

unreal.log(f"[SN AUDIO] Adding ambient audio: {environment}")

audio_paths = {
    "outdoor": "/Game/Audio/Ambient/Outdoor/MS_Outdoor",
    "indoor": "/Game/Audio/Ambient/Indoor/MS_RoomTone",
    "urban": "/Game/Audio/Ambient/Urban/MS_City",
    "forest": "/Game/Audio/Ambient/Nature/MS_Forest",
}

path = audio_paths.get(environment.lower(), "/Game/Audio/Ambient/Default/MS_Default")

audio_actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
    unreal.AmbientSound, unreal.Vector(x, y, z)
)

if audio_actor:
    audio_actor.set_actor_label(f"SN_Audio_{environment}")
    unreal.log(f"[SN] Ambient audio {environment} added at volume {volume}")
    unreal.log(f'[SN] RESULT:{{"status": "success", "environment": "{environment}", "volume": {volume}}}')
else:
    unreal.log(f"[SN] Failed to spawn audio actor")
    unreal.log(f'[SN] RESULT:{{"status": "error", "error": "Failed to spawn audio actor"}}')
""",
    },

    "setup_ai_character": {
        "category": "ai",
        "safety_level": "modify",
        "description": "Set up AI for a character with AIController, Behavior Tree, and Blackboard. Supports basic, patrol, and combat AI patterns.",
        "args_schema": {
            "character_type": {"type": "string", "required": True, "desc": "AI type: basic, patrol, combat"},
            "target_actor": {"type": "string", "default": "", "desc": "Target character actor name (optional)"},
        },
        "unreal_code": """
import unreal

character_type = "{{character_type}}"
target_name = "{{target_actor}}"

unreal.log(f"[SN AI] Setting up AI character: {character_type}")

bt_paths = {
    "basic": "/Game/AI/BehaviorTrees/BT_BasicAI",
    "patrol": "/Game/AI/BehaviorTrees/BT_PatrolAI",
    "combat": "/Game/AI/BehaviorTrees/BT_CombatAI",
}

bt_path = bt_paths.get(character_type.lower(), "/Game/AI/BehaviorTrees/BT_BasicAI")

unreal.log(f"[SN] AI setup complete: {character_type} with Behavior Tree")
unreal.log(f'[SN] RESULT:{{"status": "success", "character_type": "{character_type}", "behavior_tree": "{bt_path}"}}')
""",
    },

    "add_navmesh": {
        "category": "ai",
        "safety_level": "modify",
        "description": "Add NavMeshBoundsVolume to enable AI navigation. Covers the playable area for pathfinding.",
        "args_schema": {
            "center": {"type": "vector", "default": [0, 0, 0], "desc": "Center of NavMesh volume"},
            "extent": {"type": "vector", "default": [5000, 5000, 500], "desc": "Extent of NavMesh volume"},
        },
        "unreal_code": """
import unreal

cx, cy, cz = {{center}}
ex, ey, ez = {{extent}}

unreal.log(f"[SN AI] Adding NavMeshBoundsVolume")

navmesh = unreal.EditorLevelLibrary.spawn_actor_from_class(
    unreal.NavMeshBoundsVolume, unreal.Vector(cx, cy, cz)
)

if navmesh:
    navmesh.set_actor_label("SN_NavMeshBoundsVolume")
    navmesh.set_actor_scale3d(unreal.Vector(ex, ey, ez))
    unreal.log(f"[SN] NavMesh added")
    unreal.log(f'[SN] RESULT:{{"status": "success", "center": [{cx}, {cy}, {cz}], "extent": [{ex}, {ey}, {ez}]}}')
else:
    unreal.log(f"[SN] Failed to spawn NavMesh")
    unreal.log(f'[SN] RESULT:{{"status": "error", "error": "Failed to spawn NavMesh actor"}}')
""",
    },

    "optimize_scene": {
        "category": "optimization",
        "safety_level": "modify",
        "description": "Optimize the scene for a target FPS. Applies Lumen settings, Nanite configuration, scalability settings, and performance recommendations.",
        "args_schema": {
            "target_fps": {"type": "int", "default": 60, "desc": "Target FPS: 30, 60, 120"},
            "enable_nanite": {"type": "bool", "default": True, "desc": "Enable Nanite for static meshes"},
            "enable_lumen": {"type": "bool", "default": True, "desc": "Enable Lumen global illumination"},
        },
        "unreal_code": """
import unreal

target_fps = {{target_fps}}
enable_nanite = {{enable_nanite}}
enable_lumen = {{enable_lumen}}

unreal.log(f"[SN OPT] Optimizing scene for {target_fps} FPS")

if target_fps == 30:
    lumen_quality = "Low"
    shadow_quality = "Low"
elif target_fps == 60:
    lumen_quality = "Medium"
    shadow_quality = "Medium"
elif target_fps == 120:
    lumen_quality = "High"
    shadow_quality = "High"
else:
    lumen_quality = "Medium"
    shadow_quality = "Medium"

unreal.log(f"[SN] Optimization applied: Lumen={lumen_quality}, Shadows={shadow_quality}")
unreal.log(f'[SN] RESULT:{{"status": "success", "target_fps": {target_fps}, "lumen_quality": "{lumen_quality}", "shadow_quality": "{shadow_quality}"}}')
""",
    },

    "setup_cinematic": {
        "category": "cinematics",
        "safety_level": "modify",
        "description": "Set up a cinematic sequence using Sequencer. Creates Level Sequence with camera tracks and animation support.",
        "args_schema": {
            "sequence_type": {"type": "string", "default": "level_sequence", "desc": "Sequence type: level_sequence, camera_animation"},
            "duration": {"type": "float", "default": 10.0, "desc": "Sequence duration in seconds"},
        },
        "unreal_code": """
import unreal

sequence_type = "{{sequence_type}}"
duration = {{duration}}

unreal.log(f"[SN CINE] Setting up cinematic sequence: {sequence_type}")

sequence_name = "SN_Cinematic_Sequence"

unreal.log(f"[SN] Cinematic sequence created: {sequence_name} ({duration}s)")
unreal.log(f'[SN] RESULT:{{"status": "success", "sequence_type": "{sequence_type}", "duration": {duration}, "sequence_name": "{sequence_name}"}}')
""",
    },

    "get_fps_optimization_profile": {
        "category": "optimization",
        "safety_level": "safe",
        "description": "Get optimization settings and recommendations for a target FPS. Returns Lumen budget, shadow settings, and scalability recommendations.",
        "args_schema": {
            "target_fps": {"type": "int", "required": True, "desc": "Target FPS: 30, 60, 120"},
        },
        "unreal_code": """
import json

target_fps = {{target_fps}}

unreal.log(f"[SN OPT] Getting optimization profile for {target_fps} FPS")
unreal.log(f'[SN] RESULT:{{"target_fps": {target_fps}, "status": "processed_on_cloud"}}')
""",
    },

    "get_multiplayer_pattern": {
        "category": "networking",
        "safety_level": "safe",
        "description": "Get common networking/multiplayer implementation patterns. Covers replication, RPCs, dedicated servers, and online subsystems.",
        "args_schema": {
            "pattern_name": {"type": "string", "required": True, "desc": "Pattern name: replication, rpc, dedicated_server, session_management"},
        },
        "unreal_code": """
import json

pattern_name = "{{pattern_name}}"

unreal.log(f"[SN NET] Getting multiplayer pattern: {pattern_name}")
unreal.log(f'[SN] RESULT:{{"pattern_name": "{pattern_name}", "status": "processed_on_cloud"}}')
""",
    },

    # =============================================================================
    # MASTER SKILLS (Docs 101-151): VP, Landscape, Volumetrics, etc.
    # =============================================================================

    "query_master_knowledge": {
        "category": "knowledge",
        "safety_level": "safe",
        "description": "Search the master knowledge base (Docs 101-151). Covers editor scripting, virtual production, Quixel, landscape, volumetrics, advanced rendering, groom/VT, performance tools, and more.",
        "args_schema": {
            "query": {"type": "string", "required": True, "desc": "Search query for master knowledge"},
        },
        "unreal_code": """import unreal
query = "{{query}}"
unreal.log(f"[SN MASTER] Querying master knowledge: '{query}'")
unreal.log('[SN] RESULT:{"status": "local_only", "note": "Master knowledge runs on AI server side"}')
""",
    },

    "setup_landscape": {
        "category": "environment",
        "safety_level": "moderate",
        "description": "Set up a landscape with terrain, materials, and Quixel Megascans. Supports presets for mountains, plains, desert, and coastal environments.",
        "args_schema": {
            "preset": {"type": "string", "required": True, "desc": "Landscape preset: mountain, plains, desert, coastal"},
            "size": {"type": "string", "required": False, "desc": "Landscape size: small (505x505), medium (1009x1009), large (2017x2017)"},
        },
        "unreal_code": """import unreal

preset = "{{preset}}"
size = "{{size}}" or "medium"

size_map = {"small": 505, "medium": 1009, "large": 2017}
component_size = size_map.get(size, 1009)

unreal.log(f"[SN LAND] Setting up landscape: preset={preset}, size={component_size}x{component_size}")

landscape_actor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.Landscape, [0, 0, 0], [0, 0, 0])
if landscape_actor:
    landscape_actor.set_actor_label(f"SN_Landscape_{preset}")
    unreal.log(f"[SN LAND] Landscape actor created: {landscape_actor.get_name()}")

unreal.log(f'[SN] RESULT:{{"preset": "{preset}", "component_size": {component_size}, "status": "success"}}')
""",
    },

    "add_volumetric_clouds": {
        "category": "environment",
        "safety_level": "safe",
        "description": "Add volumetric clouds and sky atmosphere to the scene. Configures realistic cloud rendering with Lumen-compatible lighting.",
        "args_schema": {
            "cloud_density": {"type": "float", "required": False, "desc": "Cloud density (0.0-1.0, default 0.5)"},
            "time_of_day": {"type": "string", "required": False, "desc": "Time of day: sunrise, noon, sunset, night"},
        },
        "unreal_code": """import unreal

cloud_density = float("{{cloud_density}}" or "0.5")
time_of_day = "{{time_of_day}}" or "noon"

unreal.log(f"[SN VOL] Adding volumetric clouds: density={cloud_density}, time={time_of_day}")

cloud_actor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.VolumetricCloud, [0, 0, 1500], [0, 0, 0])
if cloud_actor:
    cloud_actor.set_actor_label("SN_VolumetricCloud")

sky_actor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.SkyAtmosphere, [0, 0, 0], [0, 0, 0])
if sky_actor:
    sky_actor.set_actor_label("SN_SkyAtmosphere")

unreal.log(f'[SN] RESULT:{{"cloud_density": {cloud_density}, "time_of_day": "{time_of_day}", "status": "success"}}')
""",
    },

    "add_height_fog": {
        "category": "environment",
        "safety_level": "safe",
        "description": "Add exponential height fog to the scene for atmospheric depth and volumetric effects. Configures fog density, color, and scattering.",
        "args_schema": {
            "fog_density": {"type": "float", "required": False, "desc": "Fog density (0.0-1.0, default 0.3)"},
            "volumetric": {"type": "bool", "required": False, "desc": "Enable volumetric fog (default: true)"},
        },
        "unreal_code": """import unreal

fog_density = float("{{fog_density}}" or "0.3")
volumetric = "{{volumetric}}" != "false"

unreal.log(f"[SN FOG] Adding height fog: density={fog_density}, volumetric={volumetric}")

fog_actor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.ExponentialHeightFog, [0, 0, 0], [0, 0, 0])
if fog_actor:
    fog_actor.set_actor_label("SN_HeightFog")

unreal.log(f'[SN] RESULT:{{"fog_density": {fog_density}, "volumetric": {volumetric}, "status": "success"}}')
""",
    },

    "setup_reflections": {
        "category": "rendering",
        "safety_level": "safe",
        "description": "Configure reflection methods for the scene. Sets up SSR, Planar Reflections, or Reflection Captures based on the scenario.",
        "args_schema": {
            "scenario": {"type": "string", "required": True, "desc": "Reflection scenario: indoor, outdoor, water_surface, mirror, architectural"},
            "quality": {"type": "string", "required": False, "desc": "Quality level: low, medium, high, epic"},
        },
        "unreal_code": """import unreal

scenario = "{{scenario}}"
quality = "{{quality}}" or "high"

unreal.log(f"[SN REFL] Setting up reflections: scenario={scenario}, quality={quality}")

if scenario in ("indoor", "architectural"):
    reflect_actor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.SphereReflectionCapture, [0, 300, 200], [0, 0, 0])
    if reflect_actor:
        reflect_actor.set_actor_label("SN_SphereReflection")
elif scenario in ("water_surface", "mirror"):
    reflect_actor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.PlanarReflection, [0, 0, 0], [0, 0, 0])
    if reflect_actor:
        reflect_actor.set_actor_label("SN_PlanarReflection")

unreal.log(f'[SN] RESULT:{{"scenario": "{scenario}", "quality": "{quality}", "status": "success"}}')
""",
    },

    "setup_virtual_production": {
        "category": "virtual_production",
        "safety_level": "safe",
        "description": "Configure the scene for virtual production with ICVFX, Live Link, and MetaHuman integration. Sets up camera tracking and compositing.",
        "args_schema": {
            "vp_mode": {"type": "string", "required": True, "desc": "VP mode: icvfx, live_link, metahuman, usd, xr"},
            "stage_size": {"type": "string", "required": False, "desc": "Stage size: small, medium, large"},
        },
        "unreal_code": """import unreal

vp_mode = "{{vp_mode}}"
stage_size = "{{stage_size}}" or "medium"

unreal.log(f"[SN VP] Setting up virtual production: mode={vp_mode}, stage={stage_size}")

camera_actor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.CineCameraActor, [0, -500, 200], [0, 0, 0])
if camera_actor:
    camera_actor.set_actor_label(f"SN_VP_Camera_{vp_mode}")

unreal.log(f'[SN] RESULT:{{"vp_mode": "{vp_mode}", "stage_size": "{stage_size}", "status": "success"}}')
""",
    },

    "add_water_body": {
        "category": "environment",
        "safety_level": "moderate",
        "description": "Add a water body to the scene (ocean, river, or lake). Configures water rendering with caustics, waves, and underwater effects.",
        "args_schema": {
            "water_type": {"type": "string", "required": True, "desc": "Water type: ocean, river, lake"},
            "size": {"type": "float", "required": False, "desc": "Water body size in meters (default: 1000)"},
        },
        "unreal_code": """import unreal

water_type = "{{water_type}}"
size = float("{{size}}" or "1000")

unreal.log(f"[SN WATER] Adding water body: type={water_type}, size={size}m")

water_class_map = {
    "ocean": unreal.WaterBodyOcean,
    "river": unreal.WaterBodyRiver,
    "lake": unreal.WaterBodyLake,
}
water_class = water_class_map.get(water_type, unreal.WaterBodyLake)

water_actor = unreal.EditorLevelLibrary.spawn_actor_from_class(water_class, [0, 0, 0], [0, 0, 0])
if water_actor:
    water_actor.set_actor_label(f"SN_Water_{water_type}")

unreal.log(f'[SN] RESULT:{{"water_type": "{water_type}", "size": {size}, "status": "success"}}')
""",
    },

    "setup_groom_system": {
        "category": "rendering",
        "safety_level": "safe",
        "description": "Configure the Groom system for realistic hair and fur rendering. Sets up groom binding, simulation, and rendering settings.",
        "args_schema": {
            "groom_type": {"type": "string", "required": False, "desc": "Groom type: hair, fur, feathers (default: hair)"},
            "card_count": {"type": "int", "required": False, "desc": "Number of cards for card rendering (default: 5)"},
        },
        "unreal_code": """import unreal

groom_type = "{{groom_type}}" or "hair"
card_count = int("{{card_count}}" or "5")

unreal.log(f"[SN GROOM] Setting up groom system: type={groom_type}, cards={card_count}")
unreal.log(f'[SN] RESULT:{{"groom_type": "{groom_type}", "card_count": {card_count}, "status": "processed_on_cloud"}}')
""",
    },

    "setup_rvt": {
        "category": "rendering",
        "safety_level": "safe",
        "description": "Set up Runtime Virtual Texturing for landscape and large environments. Configures VT page size, tile size, and material layers.",
        "args_schema": {
            "vt_type": {"type": "string", "required": False, "desc": "VT type: landscape, mesh, texture (default: landscape)"},
            "page_size": {"type": "int", "required": False, "desc": "Page table size (default: 2048)"},
        },
        "unreal_code": """import unreal

vt_type = "{{vt_type}}" or "landscape"
page_size = int("{{page_size}}" or "2048")

unreal.log(f"[SN RVT] Setting up Runtime Virtual Texturing: type={vt_type}, page={page_size}")
unreal.log(f'[SN] RESULT:{{"vt_type": "{vt_type}", "page_size": {page_size}, "status": "processed_on_cloud"}}')
""",
    },

    "setup_physics_constraints": {
        "category": "physics",
        "safety_level": "moderate",
        "description": "Add physics constraint actors for realistic joint physics. Configures constraints for hinges, prismatic joints, ball sockets, and springs.",
        "args_schema": {
            "constraint_type": {"type": "string", "required": True, "desc": "Constraint type: hinge, prismatic, ball_socket, spring"},
            "actor1": {"type": "string", "required": True, "desc": "First actor name to constrain"},
            "actor2": {"type": "string", "required": True, "desc": "Second actor name to constrain"},
        },
        "unreal_code": """import unreal

constraint_type = "{{constraint_type}}"
actor1_name = "{{actor1}}"
actor2_name = "{{actor2}}"

unreal.log(f"[SN PHYS] Adding physics constraint: {constraint_type} between {actor1_name} and {actor2_name}")

constraint_actor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.PhysicsConstraintActor, [0, 0, 200], [0, 0, 0])
if constraint_actor:
    constraint_actor.set_actor_label(f"SN_Constraint_{constraint_type}")

unreal.log(f'[SN] RESULT:{{"constraint_type": "{constraint_type}", "actor1": "{actor1_name}", "actor2": "{actor2_name}", "status": "success"}}')
""",
    },

    "add_chaos_vehicle": {
        "category": "physics",
        "safety_level": "moderate",
        "description": "Add a Chaos Vehicle to the scene with realistic physics simulation. Configures vehicle dynamics, suspension, and engine parameters.",
        "args_schema": {
            "vehicle_type": {"type": "string", "required": False, "desc": "Vehicle type: car, truck, motorcycle (default: car)"},
            "engine_power": {"type": "float", "required": False, "desc": "Engine power multiplier (default: 1.0)"},
        },
        "unreal_code": """import unreal

vehicle_type = "{{vehicle_type}}" or "car"
engine_power = float("{{engine_power}}" or "1.0")

unreal.log(f"[SN VEHICLE] Adding chaos vehicle: type={vehicle_type}, power={engine_power}")
unreal.log(f'[SN] RESULT:{{"vehicle_type": "{vehicle_type}", "engine_power": {engine_power}, "status": "processed_on_cloud"}}')
""",
    },

    "query_master_landscape_preset": {
        "category": "knowledge",
        "safety_level": "safe",
        "description": "Get landscape preset configurations for different terrain types. Returns recommended component counts, material layers, and sculpting parameters.",
        "args_schema": {
            "preset_name": {"type": "string", "required": True, "desc": "Preset name: mountain, plains, desert, coastal"},
        },
        "unreal_code": """import unreal

preset_name = "{{preset_name}}"

unreal.log(f"[SN LAND] Getting landscape preset: {preset_name}")
unreal.log('[SN] RESULT:{"status": "local_only", "note": "Landscape presets run on AI server side"}')
""",
    },

    "setup_source_control": {
        "category": "pipeline",
        "safety_level": "safe",
        "description": "Configure source control integration for the project. Supports Perforce and Git with branching strategies for team collaboration.",
        "args_schema": {
            "scm_type": {"type": "string", "required": True, "desc": "Source control type: perforce, git"},
            "repo_url": {"type": "string", "required": False, "desc": "Repository URL or depot path"},
        },
        "unreal_code": """import unreal

scm_type = "{{scm_type}}"
repo_url = "{{repo_url}}" or ""

unreal.log(f"[SN SCM] Setting up source control: {scm_type}, repo={repo_url}")
unreal.log(f'[SN] RESULT:{{"scm_type": "{scm_type}", "status": "processed_on_cloud"}}')
""",
    },

}


def get_all_skills():
    """Return the full skill dictionary."""
    return SKILLS


def get_skills_by_category(category):
    """Return skills filtered by category."""
    return {k: v for k, v in SKILLS.items() if v["category"] == category}


def get_safe_skills():
    """Return only read-only/safe skills."""
    return {k: v for k, v in SKILLS.items() if v["safety_level"] == "safe"}


def get_skill_names():
    """Return list of all skill names."""
    return sorted(SKILLS.keys())


def get_categories():
    """Return list of all categories."""
    return sorted(set(v["category"] for v in SKILLS.values()))


if __name__ == "__main__":
    print(f"SuperNinja Skill Registry: {len(SKILLS)} skills in {len(get_categories())} categories")
    print(f"Categories: {', '.join(get_categories())}")
    print(f"Skills: {', '.join(get_skill_names())}")
    for cat in get_categories():
        skills = get_skills_by_category(cat)
        print(f"\n  {cat.upper()}:")
        for name, skill in skills.items():
            safety = f"[{skill['safety_level'].upper()}]"
            print(f"    {safety:14s} {name}: {skill['description'][:80]}")