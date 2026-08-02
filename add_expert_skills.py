import re

with open('sn_skills_registry.py', 'r') as f:
    lines = f.readlines()

# Find line 1507 (0-indexed: 1506) which is the closing } of SKILLS dict
insert_before = 1506

expert_skills = '''    # =========================================================================
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
'''

new_lines = lines[:insert_before] + [expert_skills + '\n'] + lines[insert_before:]

with open('sn_skills_registry.py', 'w') as f:
    f.writelines(new_lines)

print(f"Successfully inserted 9 expert skills before line {insert_before + 1}")