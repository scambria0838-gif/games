# SuperNinja Skills Catalog

This is the canonical list of every command the cloud server will accept.
Categories mirror the in-Unreal skill modules.

> Each entry: `command` — purpose. `args:` typical fields.

## Core comms
- `ping` — round-trip check. `args: {}`
- `echo` — return whatever you sent. `args: {*}`
- `log` — write to UE5 output log. `args: {msg}`
- `safe_log` — log without crashing. `args: {msg}`
- `stop` — gracefully stop the worker. `args: {}`
- `screenshot` — capture viewport (legacy alias of `take_screenshot`).
- `take_screenshot` — capture viewport. `args: {filename?}`

## Lighting
- `add_directional_light` — sun-like light. `args: {intensity?, rotation?}`
- `add_point_light` — omnidirectional. `args: {location?, intensity?}`
- `add_spot_light` — cone light. `args: {location?, intensity?, cone_angle?}`
- `add_sky_light` — captures the sky. `args: {}`
- `adjust_light` — modify an existing light. `args: {name, intensity?, color?}`
- `light_scene` — high-level preset. `args: {preset: "cinematic"|"daylight"|"noir"|"night"}`

## Placement & transforms
- `spawn_actor` — create actor. `args: {shape, mesh_path?, location?, rotation?, scale?, name?}`
- `move_actor` — translate. `args: {name, location}`
- `rotate_actor` — rotate. `args: {name, rotation}`
- `scale_actor` — scale. `args: {name, scale}`
- `scatter_actors` — spread copies. `args: {mesh_path, count, radius}`
- `scatter_props` — alias of scatter_actors with prop-friendly defaults.
- `delete_actor` — remove one. `args: {name}`
- `delete_duplicates` — dedupe by exact mesh+location.
- `cleanup_duplicates` — alias.

## Analysis
- `list_actors` — every actor in the scene.
- `find_actors` — search by name. `args: {pattern}`
- `find_actors_advanced` — filter by class/tags. `args: {class?, tag?}`
- `get_actor_properties` — `args: {name}`
- `set_actor_property` — `args: {name, property, value}`
- `get_scene_info` — counts and bounds.

## Camera
- `frame_viewport` — fly camera to fit a target. `args: {target?}`

## Environment
- `add_exponential_height_fog` — `args: {density?, color?}`
- `add_sky_atmosphere` — `args: {}`
- `add_volumetric_clouds` — `args: {coverage?}`
- `add_post_process_volume` — `args: {settings}`
- `set_skybox` — `args: {hdri_path}`
- `add_height_fog` — alias.
- `add_water_body` — `args: {type, location?}`
- `setup_landscape` — `args: {size?, heightmap?}`

## Materials & rendering
- `apply_material` — `args: {actor_name, material_path}`
- `setup_post_process` — `args: {preset}`
- `setup_reflections` — `args: {method}`
- `setup_groom_system` — `args: {}`
- `setup_rvt` — runtime virtual textures. `args: {}`
- `analyze_rendering` — read-only diagnostics.

## Procedural
- `add_foliage` — `args: {mesh_path, count, density?}`
- `add_landscape` — alias.

## VFX & audio
- `add_niagara_effect` — `args: {effect_path, location?}`
- `add_audio_ambient` — `args: {sound_path, volume?}`

## AI / nav
- `setup_ai_character` — `args: {behavior_tree?, location?}`
- `add_navmesh` — `args: {bounds?}`

## Optimization
- `optimize_scene` — auto LODs, instancing.
- `get_fps_optimization_profile` — read-only suggestions.

## Cinematics & networking
- `setup_cinematic` — `args: {sequence_name}`
- `get_multiplayer_pattern` — knowledge query.

## Knowledge queries (read-only)
- `query_knowledge`
- `query_advanced_knowledge`
- `query_expert_knowledge`
- `query_master_knowledge`
- `query_master_landscape_preset`
- `explain_ue5_concept`
- `suggest_blueprint_pattern`
- `get_lighting_setup`
- `get_material_recipe`

## Conversational
- `say`, `ask_user`, `report_progress`, `explain_scene`,
  `suggest_improvements`, `chat`

## Master / virtual production
- `setup_virtual_production`, `setup_physics_constraints`,
  `add_chaos_vehicle`, `setup_source_control`

## Utility
- `save_level`, `undo`, `execute_console_command`,
  `import_asset`, `list_content`, `run_python_snippet`

## Sprint 75 — new capabilities
- `save_to_file` — persist scene. `args: {path}`
- `load_from_file` — restore scene. `args: {path}`
- `clear_scene` — wipe. `args: {confirm: true}` (refuses without confirm).
- `undo_last_command` — revert most recent op.
- `export_scene_json` — return scene as JSON.
- `import_scene_json` — recreate from JSON. `args: {scene}`
- `export_screenshot_png` — write a real PNG to disk. `args: {path?}`

> Anything not in this list will be refused with `403 command not allowed`.
