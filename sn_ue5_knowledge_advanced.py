"""
SuperNinja UE5 Advanced Knowledge Base
=======================================
Structured knowledge extracted from UE5 Training Corpus Documents 21-60.
Covers: GAS, Lighting, Materials, Rendering, Level Design, Animation, Physics, VFX

This module provides the deep domain knowledge that powers SuperNinja's
intelligent reasoning about UE5 scenes, lighting, materials, and more.
"""

# ============================================================================
# GAMEPLAY ABILITY SYSTEM (Docs 21-22)
# ============================================================================

GAMEPLAY_ABILITY_SYSTEM = {
    "overview": {
        "description": "Framework for building attributes, abilities, and interactions that an Actor can own and trigger",
        "use_cases": ["RPGs", "Action-Adventure", "MOBAs", "Any gameplay-driven project"],
        "key_classes": ["UGameplayAbility", "UAbilityTask", "FGameplayAttribute", "UAbilitySystemComponent"],
    },
    "gameplay_abilities": {
        "description": "C++ or Blueprint children of UGameplayAbility class",
        "defines": "What the Ability does in code or Blueprint scripting",
        "behaviors": ["replication", "instancing"],
        "states": ["Activated", "In-Progress", "Completed"],
        "tasks": "Asynchronous building blocks derived from UAbilityTask, call delegates (C++) or output execution pins (Blueprints)",
    },
    "gameplay_attributes": {
        "description": "Float values stored in FGameplayAttribute structure",
        "examples": ["health", "strength", "jump_height", "attack_speed", "mana"],
        "storage": "Owned by Ability System Component on the Actor",
    },
    "gameplay_effects": {
        "description": "Alter Gameplay Attributes instantaneously or over time (buffs/debuffs)",
        "examples": [
            "Subtract magic points when casting a spell",
            "Grant movement speed boost during Sprint Ability",
            "Gradually restore health over time (healing medicine)",
        ],
    },
    "ability_system_component": {
        "description": "Required component on any Actor that interacts with GAS",
        "responsibilities": ["Activate Abilities", "Store Attributes", "Update Effects", "Handle Actor interactions"],
    },
    "setup": {
        "plugin": "Enable Gameplay Ability System Plugin in Edit > Plugins",
        "build_cs": 'Add "GameplayAbilities", "GameplayTags", "GameplayTasks" to PublicDependencyModuleNames in .Build.cs',
        "modules_needed": ["GameplayAbilities", "GameplayTags", "GameplayTasks"],
    },
    "lyra_starter_game": {
        "description": "Learning resource and sample game project for UE5 frameworks",
        "features": [
            "Cross-platform compatibility and scalability",
            "Online multiplayer with Epic Online Services",
            "Three game modes: Elimination, Control, Exploder",
            "Customized Gameplay Ability System",
            "Niagara FX, UMG widgets, UI Icons",
            "Optimized locomotion animation assets and sounds",
            "Weapon system compatible with any Pawn",
            "New UE5 Mannequins (Manny, Quinn) sharing MetaHuman skeleton",
        ],
        "architecture": "Modular core system with Gameplay Feature Plugins",
        "experiences": "Defined using LyraExperienceDefinition class",
    },
}

# ============================================================================
# LIGHTING (Docs 23-30)
# ============================================================================

LIGHTING_SYSTEM = {
    "overview": {
        "description": "Tools and lighting actors for determining how a virtual world is lit",
        "importance": "Lighting is one of the most critical aspects of building any virtual world",
        "light_types": {
            "DirectionalLight": "Simulates sunlight - infinite distance, parallel rays, affects entire scene",
            "PointLight": "Emit light in all directions from a single point - like a light bulb",
            "SpotLight": "Emit light in a cone shape from a single point",
            "RectLight": "Emit light from a rectangular surface - like a TV screen or window",
            "SkyLight": "Captures distant parts of scene to use as ambient lighting",
        },
    },
    "mobility": {
        "Static": {
            "description": "Cannot be moved at runtime, baked into lightmaps by Lightmass",
            "best_for": "Environment lighting that never changes",
            "performance": "Best - precomputed, no runtime cost",
            "shadows": "Baked into lightmaps, highest quality soft shadows",
        },
        "Stationary": {
            "description": "Can change color/intensity at runtime, but NOT position",
            "best_for": "Lights that need runtime adjustments but stay in place",
            "performance": "Good - partial precomputation, Lumen handles dynamic parts",
            "shadows": "Static geometry shadows baked, dynamic objects use Lumen/VSM shadows",
            "limit": "4-5 overlapping stationary lights recommended max (shadow map channels)",
        },
        "Movable": {
            "description": "Can be moved and changed at runtime, fully dynamic",
            "best_for": "Movable objects, dynamic gameplay elements",
            "performance": "Highest cost - all lighting computed at runtime",
            "shadows": "Real-time shadows via Virtual Shadow Maps or Lumen",
        },
    },
    "intensity_units": {
        "DirectionalLight": "Lux (default ~10 for sunlight)",
        "PointLight": "Candela (luminous intensity)",
        "SpotLight": "Candela (luminous intensity)",
        "RectLight": "Candela (luminous intensity)",
        "note": "Use physical units for realistic results. Enable 'Use Physical Light Units' in project settings.",
    },
    "color_temperature": {
        "description": "Measured in Kelvin, overrides light color when enabled",
        "common_values": {
            "candle": 1700,
            "tungsten_bulb": 2800,
            "halogen": 3200,
            "midday_sun": 5500,
            "daylight_D65": 6500,
            "overcast_sky": 7500,
            "blue_sky": 10000,
        },
        "tip": "Warmer temps (2700-3500K) feel cozy/indoor, cooler temps (5500-7500K) feel outdoor/daylight",
    },
    "lighting_best_practices": {
        "directional_light": [
            "Always pair a Directional Light with a Sky Light for ambient fill",
            "Use temperature for realistic sunlight (5500-6500K for midday)",
            "Set shadow bias carefully to avoid shadow acne vs light leaking",
            "Use Atmospheric Fog or Sky Atmosphere with Directional Light",
        ],
        "point_lights": [
            "Use inverse square falloff for physically accurate attenuation",
            "Set Source Radius for soft shadows (larger = softer)",
            "Avoid too many overlapping point lights (performance cost)",
            "Use Light Functions for flickering/pattern effects",
        ],
        "general": [
            "Start with 3-point lighting: Key + Fill + Rim",
            "Use Lumen for dynamic GI instead of many point lights",
            "Keep total dynamic lights under 20 for good performance",
            "Light important areas first, then add fill/accent lights",
            "Use IES profiles for realistic light distribution patterns",
        ],
    },
}

LUMEN_SYSTEM = {
    "overview": {
        "description": "UE5's fully dynamic global illumination and reflections system",
        "designed_for": "Next-generation consoles and high-end PCs",
        "no_baking": "Does not require lightmap baking - everything is dynamic",
        "quality_levels": ["High", "Medium", "Low", "Epic"],
    },
    "how_it_works": {
        "surface_cache": "Captures surface lighting from multiple directions around each surface point",
        "tracing": "Rays traced from camera to find surface cache lighting at hit points",
        "final_gather": "Traces additional rays for higher quality indirect lighting",
        "reflections": "Uses ray tracing against surface cache for screen-space and world-space reflections",
    },
    "technical_details": {
        "ray_tracing_methods": ["Screen Traces (first)", "Depth Intersection Test", "Surface Cache Tracing"],
        "surface_cache": {
            "description": "Represents lighting on surfaces from multiple directions",
            "card_placement": "Automatically placed on surfaces that can be seen from the camera",
            "update_rate": "Updated incrementally as the camera moves",
            "resolution": "Controlled by 'Lumen Scene Detail' quality setting",
        },
        "screen_traces": {
            "description": "First ray tracing method used, traces against depth buffer",
            "advantage": "Fast and handles thin objects well",
            "limitation": "Cannot see off-screen geometry",
            "fallback": "Falls back to surface cache when screen traces miss",
        },
    },
    "hardware_ray_tracing": {
        "description": "Optional enhancement using RT cores on modern GPUs",
        "when_to_use": "When you need higher quality reflections or translucency GI",
        "requirements": ["RTX 2000+ or Radeon RX 6000+", "DX12", "Support Hardware Ray Tracing enabled"],
        "commands": {
            "enable": "r.Lumen.HardwareRayTracing 1",
            "translucency": "r.Lumen.TranslucencyVolumeTracing 0 (switch to HW RT)",
        },
    },
    "performance_tips": {
        "lumen_quality": "Lower 'Lumen Scene Detail' for better performance",
        "view_distance": "Reduce 'Lumen Max Trace Distance' for distant scenes",
        "software_vs_hardware": "Software tracing is faster on most hardware; HW RT for highest quality",
        "surface_cache_updates": "Reduce update frequency with 'Lumen Scene Update Frequency'",
        "key_console_vars": [
            "r.Lumen.ScreenProbeGather - Controls screen probe quality",
            "r.Lumen.ScreenSpaceBentNormal - Improves ambient occlusion",
            "r.Lumen.DiffuseIndirect.Allow - Toggle Lumen GI",
            "r.Lumen.Reflections.Allow - Toggle Lumen reflections",
        ],
    },
}

SHADOW_SYSTEM = {
    "overview": {
        "description": "Shadows make objects feel grounded, give depth and space sense",
        "methods": {
            "Virtual Shadow Maps": "Default in UE5, consistent high-resolution shadowing",
            "Shadow Maps (Legacy)": "Traditional shadow mapping from UE4",
            "Contact Shadows": "Screen-space detail shadows for small features",
            "Ray Traced Shadows": "Hardware ray traced, highest quality",
        },
    },
    "virtual_shadow_maps": {
        "description": "New shadow mapping method delivering consistent, high-resolution shadowing",
        "advantages": [
            "Consistent shadow resolution regardless of scene complexity",
            "Works with Nanite geometry seamlessly",
            "Single shadow method for all light types",
            "Per-pixel accuracy without manual shadow bias tuning",
        ],
        "requirements": ["Nanite enabled for static meshes (recommended)", "Meshes need valid UVs and lightmap UVs for non-Nanite"],
        "performance": "More VRAM intensive than traditional shadow maps, but scales well",
        "console_vars": {
            "enable": "r.Shadow.Virtual.Enable 1",
            "page_pool": "r.Shadow.Virtual.MaxPageAllocatorResolution (control VRAM usage)",
            "cache": "r.Shadow.Virtual.CacheMode (0=off, 1=cached)",
        },
    },
    "shadow_techniques": {
        "cascaded_shadow_maps": "Used by Directional Lights for large outdoor scenes",
        "local_lights": "Point/Spot lights use VSMs for per-object shadows",
        "self_shadowing": "Nanite + VSMs = accurate self-shadowing on detailed geometry",
        "culling": "Shadow casting culled for very small/distant objects for performance",
    },
}

EXPOSURE_SYSTEM = {
    "overview": {
        "description": "Auto exposure (eye adaptation) adjusts scene brightness based on luminance",
        "purpose": "Simulates human eye adapting to bright/dark environments",
        "post_process": "Controlled via Post Process Volume exposure settings",
    },
    "settings": {
        "min_ev": "Minimum exposure value (EV) - darkest auto exposure can go",
        "max_ev": "Maximum exposure value (EV) - brightest auto exposure can go",
        "speed_up": "How quickly exposure adapts to bright scenes",
        "speed_down": "How quickly exposure adapts to dark scenes",
        "low_percent": "Auto exposure targets this percentile of luminance histogram",
        "high_percent": "Auto exposure targets this percentile of luminance histogram",
    },
    "tips": {
        "disable_auto": "Set min/max EV to same value for manual exposure control",
        "filmic": "Use filmic tonemapper with manual EV for cinematic control",
        "ev100": "EV values are in EV100 (ISO 100) standard",
        "metering": "Use Post Process Volume with 'Unbound' checked to affect entire level",
    },
}

LIGHTMASS_SYSTEM = {
    "overview": {
        "description": "Creates lightmaps with complex light interactions like area shadowing and diffuse interreflection",
        "when_to_use": "Static lighting workflows where lights don't change at runtime",
        "requires": "Static lights and static geometry with proper lightmap UVs",
    },
    "workflow": {
        "step1": "Set lights to Static or Stationary mobility",
        "step2": "Ensure meshes have proper lightmap UVs (Auto-generate in mesh import)",
        "step3": "Build lighting from Build menu or Lightning Quality dropdown",
        "step4": "Lightmass bakes lighting into lightmap textures",
    },
    "settings": {
        "indirect_lighting_quality": "Higher = better GI quality but longer build times",
        "indirect_lighting_smoothness": "Controls how smooth indirect lighting appears",
        "compress_lightmaps": "Reduces lightmap size at slight quality cost",
        "lightmap_density": "Control per-mesh via Overwrite Lightmap Res setting",
    },
    "tips": {
        "lumen_vs_lightmass": "Use Lumen for dynamic scenes, Lightmass for static precomputed quality",
        "lightmap_uv": "Always generate lightmap UVs when importing meshes",
        "build_times": "Large scenes with high quality can take 30+ minutes to build",
    },
}

# ============================================================================
# MATERIALS (Docs 31-36)
# ============================================================================

MATERIALS_SYSTEM = {
    "overview": {
        "description": "Materials define surface properties of objects in the scene",
        "tell_engine": "How light interacts with surfaces, what color, roughness, metalness, emissive properties",
        "main_inputs": ["Base Color", "Metallic", "Specular", "Roughness", "Emissive Color", "Normal", "Ambient Occlusion"],
    },
    "main_properties": {
        "base_color": {
            "description": "The overall color of the material without any lighting influence",
            "type": "Vector (RGB 0-1 range)",
            "tip": "Use physically plausible values (no pure 0 or 1 for real surfaces)",
        },
        "metallic": {
            "description": "How metal-like the surface is (0 = dielectric, 1 = metal)",
            "type": "Scalar (0-1)",
            "tip": "Should generally be 0 or 1, not intermediate values (except for rust/dirt transitions)",
        },
        "roughness": {
            "description": "How rough or smooth the surface appears (0 = mirror, 1 = completely rough/diffuse)",
            "type": "Scalar (0-1)",
            "tip": "Most real surfaces are 0.3-0.8 roughness, avoid pure 0 or 1",
        },
        "specular": {
            "description": "Amount of specular reflection for dielectric surfaces",
            "type": "Scalar (0-1, default 0.5)",
            "tip": "Most dielectrics are 0.3-0.6, only change if you know the IOR",
        },
        "emissive_color": {
            "description": "Light emitted from the surface (self-illumination)",
            "type": "Vector (RGB, can exceed 1.0 for HDR bloom)",
            "tip": "Use Intensity parameter for bloom control, high values trigger bloom effect",
        },
        "normal": {
            "description": "Normal map input for surface detail without extra geometry",
            "type": "Texture (tangent-space normal map)",
            "tip": "Use flat normal (0,0,1) if no normal map needed",
        },
    },
    "material_editor": {
        "description": "Node-based graph interface for creating shaders",
        "viewport": "Live preview of material applied to mesh",
        "nodes": "Connect pins to build shader logic (Material Output node is final result)",
        "types": ["Material", "Material Function", "Material Layer"],
        "compilation": "Materials compile to shader bytecode for the rendering hardware",
    },
    "material_instances": {
        "description": "Lightweight variations of a parent Material that can override parameters",
        "advantage": "Change parameters without recompiling the parent material shader",
        "use_cases": ["Color variations of same material", "Switching textures", "Adjusting parameters per-object"],
        "parent_child": "Instance inherits all properties from parent, can only override exposed parameters",
        "vs_material": "Material = full shader compilation, Instance = cheap parameter overrides",
    },
    "layered_materials": {
        "description": "Two main ways to layer materials and create complex blends",
        "material_layers": {
            "description": "System that lets you create reusable layers and blend them",
            "advantage": "More modular, layers are reusable assets",
            "use_case": "Complex multi-layer surfaces (e.g., paint over metal with rust)",
        },
        "material_functions": {
            "description": "Traditional approach using Material Function nodes for layering",
            "advantage": "More control over blend logic",
            "use_case": "Custom blending between surface types",
        },
    },
    "subsurface_scattering": {
        "description": "Lighting phenomenon where light scatters as it passes through translucent material",
        "examples": ["Skin", "Wax", "Marble", "Candle wax", "Leaves"],
        "shading_models": ["Subsurface", "Subsurface Profile (recommended for skin)", "Clear Coat Bottom"],
        "profile": "Subsurface Profile asset provides realistic scattering parameters for skin",
        "tip": "Use Subsurface Profile for character skin, Subsurface for other translucent materials",
    },
    "shading_models": {
        "description": "Determine how Material inputs are combined to make final color",
        "available": {
            "Unlit": "No lighting applied, just emissive color",
            "Default Lit": "Standard PBR shading (most common)",
            "Subsurface": "For translucent materials with light scattering",
            "Clear Coat": "Dual-layer material (clear coat over base) for car paint, lacquer",
            "Two Sided Foliage": "For leaves and foliage with subsurface scattering",
            "Hair": "Anisotropic shading for hair strands",
            "Cloth": "Shading for fabric and cloth surfaces",
            "Eye": "Complex shading for realistic eye rendering",
            "Thin Translucent": "For glass and thin transparent objects",
        },
    },
}

# ============================================================================
# RENDERING (Docs 37-42)
# ============================================================================

RENDERING_SYSTEM = {
    "post_process": {
        "description": "Non-destructive effects that change the look and feel of a level",
        "analogy": "Like applying filters to a photo in Photoshop",
        "volume_types": {
            "PostProcessVolume": "Define post process settings in a region of space",
            "unbound": "Check 'Unbound' to affect entire level regardless of volume bounds",
            "priority": "Higher priority volumes override lower ones",
            "blendable": "Multiple volumes can blend together based on priority and blend weight",
        },
        "available_effects": [
            "Bloom", "Depth of Field", "Exposure", "Color Grading",
            "Lens Flare", "Chromatic Aberration", "Vignette",
            "Screen Space Reflections", "Ambient Occlusion",
            "Motion Blur", "Tone Mapper",
        ],
    },
    "color_grading": {
        "description": "Covers Tone Mapping (HDR to LDR) and Color Correction adjustments",
        "sections": {
            "global": "Affects entire image uniformly",
            "shadows": "Affects only dark areas",
            "midtones": "Affects mid-range brightness",
            "highlights": "Affects only bright areas",
        },
        "parameters": {
            "saturation": "Color intensity (0 = grayscale, 1 = normal, >1 = oversaturated)",
            "contrast": "Difference between dark and light areas",
            "gamma": "Mid-tone brightness adjustment (power curve)",
            "gain": "Multiplier for highlights",
            "offset": "Additive shift for all colors",
        },
        "filmic_tonemapper": {
            "description": "Maps HDR scene values to LDR display range",
            "slope": "Controls contrast in the toe of the curve",
            "toe": "Controls the dark end of the curve",
            "shoulder": "Controls the bright end of the curve",
            "black_clip": "Clips negative values in the darkest areas",
            "white_clip": "Clips values above 1.0 in highlights",
        },
        "tip": "Use ACES for cinematic look, Rec709 for standard, use OCIO for professional color pipelines",
    },
    "nanite": {
        "description": "Virtualized geometry system using internal mesh format and rendering technology",
        "key_features": [
            "Render virtually unlimited polygon counts",
            "Automatic mesh LOD system (no manual LODs needed)",
            "Pixel-accurate detail level - only renders what's visible",
            "Seamless integration with Lumen and VSMs",
            "Dramatically reduced mesh memory and draw call overhead",
        ],
        "requirements": {
            "mesh_format": "Must enable Nanite on Static Mesh asset",
            "no_skeleton": "Cannot use on Skeletal Meshes (as of 5.4)",
            "materials": "Supports most material types, some restrictions with masked/translucent",
            "tessellation": "Replaces hardware tessellation - use Displacement in material instead",
        },
        "performance": {
            "cluster_culling": "Nanite clusters geometry into small groups, culls at cluster level",
            "visibility_buffer": "Renders to visibility buffer instead of GBuffer for efficiency",
            "streaming": "Automatically streams in detail based on camera distance",
        },
        "console_vars": {
            "enable": "r.Nanite 1",
            "visualize": "r.Nanite.ShowStats 1, r.Nanite.Visualize 1",
            "max_pixels": "r.Nanite.MaxPixelsPerEdge (control detail level)",
        },
    },
    "temporal_super_resolution": {
        "description": "Epic's advanced temporal upscaling technology (TSR)",
        "purpose": "Render at lower resolution, reconstruct at higher resolution using temporal history",
        "quality": "Near-native quality at much lower rendering cost",
        "settings": {
            "quality": "Controls TSR reconstruction quality vs performance",
            "sharpen": "Amount of sharpening applied to reconstructed image",
        },
        "alternatives": ["DLSS (NVIDIA)", "FSR (AMD)", "XeSS (Intel)"],
    },
    "virtual_texturing": {
        "description": "Enable large textures with lower and more consistent memory usage",
        "how_it_works": "Streams texture tiles on demand based on camera view instead of loading entire texture",
        "use_cases": ["Large landscape textures", "Megatextures", "Satellite imagery", "Detailed architectural textures"],
        "setup": "Convert texture to Virtual Texture in content browser, set material to sample VT",
        "performance": "Reduces texture memory significantly for large surfaces",
    },
    "forward_vs_deferred": {
        "forward": {
            "description": "Faster baseline, simpler per-light cost",
            "advantages": ["Lower latency", "Better for VR", "MSAA support", "Simpler shader"],
            "disadvantages": ["Limited lights", "No GBuffer", "Harder post-processing"],
        },
        "deferred": {
            "description": "Default renderer in UE5, renders to GBuffer first then lights",
            "advantages": ["Unlimited lights", "GBuffer for post-processing", "More consistent performance with many lights"],
            "disadvantages": ["Higher VRAM usage", "No MSAA", "Higher latency"],
        },
        "recommendation": "Use Deferred (default) unless targeting VR or mobile where Forward is better",
    },
}

# ============================================================================
# LEVEL DESIGN (Docs 43-48)
# ============================================================================

LEVEL_DESIGN_SYSTEM = {
    "quick_start": {
        "description": "Core level design workflow in UE5",
        "skills": [
            "Navigate viewports (WASD + mouse, fly/orbit modes)",
            "Place and transform actors in the level",
            "Use the Content Browser to find and drag assets",
            "Apply materials to meshes",
            "Use BSP/Geometry brushes for blocking out spaces",
            "Build lighting and test the level",
        ],
        "workflow": ["Block out with simple shapes", "Refine with proper assets", "Light the scene", "Add details and polish"],
    },
    "pcg": {
        "description": "Procedural Content Generation Framework for creating procedural content and tools",
        "how_it_works": "Node graph system that generates and places content procedurally",
        "components": {
            "pcg_graph": "Asset that defines the procedural generation rules",
            "pcg_volume": "Volume actor that triggers PCG generation in its bounds",
            "pcg_component": "Attached to actor, links to PCG graph for generation",
        },
        "use_cases": [
            "Scatter trees, rocks, and props across landscapes",
            "Generate buildings and city layouts",
            "Create point clouds for asset placement",
            "Build reusable procedural tools",
        ],
        "nodes": ["Surface Sampler", "Density Filter", "Static Mesh Spawner", "Transform Points", "Spline"],
    },
    "foliage": {
        "description": "Paint or fill landscapes with foliage and props",
        "tool_modes": {
            "Paint": "Brush-based painting of individual instances",
            "Fill": "Automatically fill a region with foliage",
            "Erase": "Remove painted instances",
            "Reapply": "Reapply with new settings without erasing",
        },
        "settings": {
            "density": "Instances per square meter",
            "radius": "Minimum distance between instances",
            "min_scale/max_scale": "Random scale range for variety",
        },
    },
    "modeling_mode": {
        "description": "In-editor geometry editing tools (BSP replacement)",
        "tools": ["PolyEdit", "MeshSelect", "TriSelect", "Boolean operations", "Deformers"],
        "use_cases": ["Block out levels", "Create custom collision", "Quick prototyping"],
    },
    "world_partition": {
        "description": "UE5's system for handling large worlds by dividing them into cells",
        "replaces": "Replaces traditional Level Streaming and sublevels for large worlds",
        "how_it_works": {
            "cells": "World is divided into grid cells that load/unload based on camera position",
            "loading_range": "Distance from camera at which cells load",
            "data_layers": "Cells can be organized into Data Layers for toggling content",
            "one_file": "Entire world stored in a single map file (no sublevels needed)",
        },
        "benefits": [
            "Handles worlds of any size",
            "Automatic streaming based on camera position",
            "No manual level streaming setup required",
            "Collaboration-friendly (multiple artists can work on same map)",
        ],
        "conversion": "Convert existing levels to World Partition from Tools > Convert Level",
    },
    "data_layers": {
        "description": "Organize content into layers that can be toggled on/off",
        "use_cases": [
            "Toggle between day/night versions of same level",
            "Show/hide debugging geometry",
            "Seasonal variations (summer/winter foliage)",
            "Different gameplay configurations",
        ],
        "runtime": "Can be toggled at runtime via Blueprints or C++",
        "workflow": "Create Data Layer assets, assign actors to layers, toggle visibility",
    },
}

# ============================================================================
# ANIMATION (Docs 49-54)
# ============================================================================

ANIMATION_SYSTEM = {
    "skeletal_mesh_overview": {
        "description": "Animation system for characters and objects with skeletal rigs",
        "components": {
            "skeletal_mesh": "Mesh with bone hierarchy for deformation",
            "skeleton": "Bone hierarchy asset shared by multiple meshes",
            "animation_sequence": "Single animation clip (walk, run, jump, etc.)",
            "blend_space": "2D blend between animations based on parameters",
            "anim_montage": "Animation that can be triggered from code and supports sections",
        },
    },
    "animation_blueprints": {
        "description": "Specialized Blueprint that controls which animations play and when",
        "graph_types": {
            "event_graph": "Calculate variables and conditions that drive animation",
            "anim_graph": "Blend and select animations based on state",
            "state_machine": "Define animation states and transitions (idle, walk, run, jump)",
        },
        "common_patterns": {
            "locomotion": "Blend space driven by speed/direction → state machine (idle, walk, run)",
            "aiming": "Layered blend per bone to add upper-body aiming on top of locomotion",
            "combat": "Montage playback with notifiers for hit/sound events",
        },
    },
    "control_rig": {
        "description": "Procedural rigging system for creating custom rig logic",
        "in_editor": "Full rig editing directly in UE5, no external DCC needed",
        "use_cases": [
            "Procedural secondary animation (bouncing, overlapping)",
            "IK solving for foot placement, hand positioning",
            "Constraint-based rigging for mechanical objects",
            "Post-process animation adjustments",
        ],
        "language": "Control Rig is written in its own VM language (RigVM)",
    },
    "ik_rig": {
        "description": "System for defining IK goals and solvers on a skeletal mesh",
        "goals": "Named IK targets (e.g., hand_l, foot_r, head) that can be driven from Blueprints",
        "solvers": {
            "limb_ik": "Standard analytical IK for arms/legs",
            "full_body_ik": "Full body IK solving with center of mass balancing",
            "pbd": "Position Based Dynamics for chain/rope IK",
        },
    },
    "motion_warping": {
        "description": "System for adjusting root motion to match target locations",
        "use_cases": [
            "Make character step exactly to a mark point",
            "Vault over obstacles of different heights",
            "Reach for objects at different positions",
        ],
        "how_it_works": "Defines 'warp targets' in animation that get adjusted to match world positions",
    },
    "full_body_ik": {
        "description": "IK solver that maintains full-body constraints while reaching for goals",
        "features": ["Center of mass balancing", "Multiple effector goals", "Natural-looking poses"],
        "use_cases": ["Character interaction with environment", "Foot placement on uneven terrain", "Reaching/grabbing"],
    },
}

# ============================================================================
# PHYSICS (Docs 55-59)
# ============================================================================

PHYSICS_SYSTEM = {
    "collision": {
        "description": "Collision detection system in Unreal Engine",
        "collision_types": {
            "NoCollision": "No collision at all",
            "QueryOnly": "Only used for traces/overlaps, no physical simulation",
            "PhysicsOnly": "Only used for physics simulation, no traces",
            "QueryAndPhysics": "Used for both traces and physics (most common)",
        },
        "responses": {
            "Ignore": "No collision interaction at all",
            "Overlap": "Generate overlap events but no blocking",
            "Block": "Full blocking collision",
        },
        "channels": "Custom collision channels can be created in Project Settings > Collision",
        "presets": "Collision presets provide common setups (Default, TriggerPawn, PhysicsActor, etc.)",
    },
    "physics_bodies": {
        "description": "Physics simulation bodies attached to skeletal meshes or actors",
        "setup": "Add Physics Asset to Skeletal Mesh, bodies auto-generated from bone geometry",
        "simulation": "Set 'Simulate Physics' on body instance to enable physics simulation",
        "constraints": "Limits on body movement/rotation (hinges, prismatic, ball-socket)",
    },
    "chaos_physics": {
        "description": "UE5's unified physics and destruction system (replaces PhysX)",
        "features": [
            "Physics simulation for rigid bodies",
            "Destruction system with fracture tools",
            "Cloth simulation",
            "Fluid simulation",
            "Hair simulation",
        ],
        "determinism": "Chaos supports deterministic physics for networked games",
        "substeps": "Control physics substep count for stability (more = more accurate but slower)",
    },
    "chaos_destruction": {
        "description": "Destructible mesh system using Chaos physics",
        "workflow": [
            "Select mesh and use Fracture tool to create pieces",
            "Define fracture levels (cluster hierarchy) for progressive destruction",
            "Set damage threshold and impact damage settings",
            "Trigger destruction via Blueprint or gameplay events",
        ],
        "fracture_types": {
            "uniform": "Evenly sized pieces",
            "clustered": "Hierarchical clusters that break progressively",
            "plane": "Slice along a plane",
            "voronoi": "Voronoi-based fracture for natural-looking pieces",
        },
        "tip": "Use cluster hierarchy for realistic progressive destruction - outer pieces break first, then inner",
    },
    "cloth_simulation": {
        "description": "Real-time cloth physics using Chaos",
        "setup": "Apply clothing asset to skeletal mesh, paint weight maps for stiffness",
        "properties": {
            "stiffness": "How rigid the cloth is (high = stiff, low = flowing)",
            "damping": "How quickly cloth stops moving after force applied",
            "wind": "External wind force affecting cloth",
            "collision": "Cloth can collide with character body and other meshes",
        },
    },
}

# ============================================================================
# VFX (Doc 60)
# ============================================================================

NIAGARA_SYSTEM = {
    "overview": {
        "description": "UE5's next-generation VFX system replacing Cascade",
        "paradigm": "Stack-based module system with full programmability",
        "key_concepts": {
            "emitter": "Single particle effect (e.g., smoke, sparks)",
            "system": "Collection of emitters that form a complete effect",
            "module": "Reusable function that modifies particle behavior",
            "stage": "Rendering stage (e.g., GPU simulation, CPU simulation, render)",
        },
    },
    "workflow": {
        "step1": "Create Niagara System asset",
        "step2": "Add emitters or select template (simple spray, fire, etc.)",
        "step3": "Configure particle parameters (spawn rate, lifetime, size, color)",
        "step4": "Add modules for behavior (velocity, gravity, collision, color over life)",
        "step5": "Set renderer (Sprite, Mesh, Ribbon, Light) for visual output",
        "step6": "Place in level or attach to actor",
    },
    "emitter_types": {
        "cpu": "More flexible, supports collision and events, fewer particles",
        "gpu": "Massively parallel, supports millions of particles, limited logic",
    },
    "renderers": {
        "sprite_renderer": "Render particles as camera-facing sprites (most common)",
        "mesh_renderer": "Render particles as 3D meshes (debris, leaves)",
        "ribbon_renderer": "Connect particles with ribbon (trails, smoke trails)",
        "light_renderer": "Emit light from particles (fire, sparks)",
        "component_renderer": "Spawn full actor components from particles",
    },
    "common_effects": {
        "fire": "Sprite renderer + color over life (yellow→orange→red→black) + velocity + turbulence",
        "smoke": "Sprite renderer + color over life (gray→transparent) + curl noise + fade",
        "sparks": "Sprite renderer + small size + velocity + gravity + light renderer",
        "rain": "Sprite renderer + streak + gravity + collision + splash event",
        "explosion": "Burst spawn + velocity + gravity + color fade + light + sound",
    },
}

# ============================================================================
# CROSS-CUTTING KNOWLEDGE
# ============================================================================

PERFORMANCE_GUIDELINES = {
    "lighting_performance": {
        "lumen_tips": [
            "Use Software Lumen on most hardware (faster than Hardware Lumen)",
            "Reduce Lumen Scene Detail for distant scenes",
            "Limit dynamic light count to under 20 for good performance",
            "Use Stationary lights where possible (partial precomputation)",
            "Avoid Movable lights unless needed for gameplay",
        ],
        "nanite_tips": [
            "Enable Nanite on all eligible static meshes",
            "Use Nanite visualization to identify expensive meshes",
            "Fallback meshes needed for translucent/masked materials",
            "Nanite eliminates manual LOD creation",
        ],
        "general": [
            "Profile with 'stat unit' and 'stat GPU' commands",
            "Use 'ProfileGPU' for detailed frame breakdown",
            "Monitor draw calls with 'stat scenrendering'",
            "Check VRAM usage with 'stat memory'",
        ],
    },
    "target_fps": {
        "cinematic_30fps": "High quality, Lumen Epic, Nanite enabled, all effects",
        "smooth_60fps": "Balanced, Lumen Medium-High, moderate dynamic lights",
        "vr_90fps": "Forward renderer, minimal post-processing, baked lighting preferred",
    },
}

SCENE_WORKFLOW = {
    "lighting_workflow": {
        "order": [
            "1. Start with Directional Light (sun) + Sky Atmosphere",
            "2. Add Sky Light for ambient fill",
            "3. Place key lights for important areas (3-point setup)",
            "4. Add fill lights to soften shadows",
            "5. Add accent/rim lights for separation",
            "6. Add volumetric effects (fog, god rays) for atmosphere",
            "7. Post-process for final look (color grading, bloom, DoF)",
        ],
        "common_mistakes": [
            "No sky light with directional light = unrealistic ambient",
            "Too many dynamic lights = poor performance",
            "Overlapping stationary lights beyond 4-5 = shadow artifacts",
            "Pure white base color = broken bloom and exposure",
            "Missing Exponential Height Fog for outdoor depth",
        ],
    },
    "material_workflow": {
        "order": [
            "1. Create master Material with all needed parameters",
            "2. Expose parameters as Material Instance overrides",
            "3. Create Material Instances for each variation",
            "4. Use Material Layers for complex multi-surface materials",
            "5. Test with different lighting conditions",
        ],
    },
}

# ============================================================================
# SEARCH AND QUERY FUNCTIONS
# ============================================================================

_ALL_CATEGORIES = {
    "gameplay_ability_system": GAMEPLAY_ABILITY_SYSTEM,
    "lighting": LIGHTING_SYSTEM,
    "lumen": LUMEN_SYSTEM,
    "shadows": SHADOW_SYSTEM,
    "exposure": EXPOSURE_SYSTEM,
    "lightmass": LIGHTMASS_SYSTEM,
    "materials": MATERIALS_SYSTEM,
    "rendering": RENDERING_SYSTEM,
    "level_design": LEVEL_DESIGN_SYSTEM,
    "animation": ANIMATION_SYSTEM,
    "physics": PHYSICS_SYSTEM,
    "niagara": NIAGARA_SYSTEM,
    "performance": PERFORMANCE_GUIDELINES,
    "scene_workflow": SCENE_WORKFLOW,
}

def get_advanced_category(name: str) -> dict:
    """Get a specific knowledge category by name."""
    return _ALL_CATEGORIES.get(name, {})

def get_all_advanced_categories() -> list:
    """Get list of all advanced knowledge category names."""
    return list(_ALL_CATEGORIES.keys())

def search_advanced_knowledge(query: str, max_results: int = 10) -> list:
    """Search all advanced knowledge categories for matching content.
    
    Returns list of dicts with: category, key, snippet, relevance
    """
    query_lower = query.lower()
    results = []
    
    for cat_name, cat_data in _ALL_CATEGORIES.items():
        _search_recursive(cat_data, cat_name, query_lower, results, "")
    
    # Sort by relevance (more matches = higher)
    results.sort(key=lambda x: x.get("relevance", 0), reverse=True)
    return results[:max_results]

def _search_recursive(data, cat_name, query, results, path):
    """Recursively search nested dicts for query matches."""
    if isinstance(data, dict):
        for key, value in data.items():
            current_path = f"{path}.{key}" if path else key
            # Check if key matches
            if query in key.lower():
                results.append({
                    "category": cat_name,
                    "key": current_path,
                    "snippet": str(value)[:200] if isinstance(value, (str, int, float)) else str(value)[:200],
                    "relevance": 2.0,  # Key match is more relevant
                })
            # Check if string value matches
            elif isinstance(value, str) and query in value.lower():
                results.append({
                    "category": cat_name,
                    "key": current_path,
                    "snippet": value[:200],
                    "relevance": 1.0,
                })
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, str) and query in item.lower():
                        results.append({
                            "category": cat_name,
                            "key": current_path,
                            "snippet": item[:200],
                            "relevance": 1.0,
                        })
                        break  # Only add once per list
            # Recurse into nested dicts
            elif isinstance(value, dict):
                _search_recursive(value, cat_name, query, results, current_path)

def get_lighting_recommendation(scene_type: str, mood: str = None) -> dict:
    """Get lighting recommendations based on scene type and mood."""
    recommendations = {
        "outdoor_day": {
            "lights": [
                {"type": "DirectionalLight", "intensity": 10.0, "temperature": 6500, "shadows": True},
                {"type": "SkyLight", "intensity": 1.0},
            ],
            "post_process": {"exposure_ev": 12.0, "temperature": 6500},
            "fog": True,
            "lumen": True,
        },
        "outdoor_golden_hour": {
            "lights": [
                {"type": "DirectionalLight", "intensity": 3.5, "temperature": 3500, "shadows": True, "angle": -10},
                {"type": "SkyLight", "intensity": 0.6, "temperature": 5500},
            ],
            "post_process": {"exposure_ev": 10.0, "bloom": 0.5, "temperature": 4500},
            "fog": True,
            "lumen": True,
        },
        "interior_office": {
            "lights": [
                {"type": "RectLight", "intensity": 2.0, "temperature": 4000, "width": 200, "height": 60},
                {"type": "PointLight", "intensity": 1.5, "temperature": 4000},
            ],
            "post_process": {"exposure_ev": 8.0, "temperature": 4000},
            "fog": False,
            "lumen": True,
        },
        "night_exterior": {
            "lights": [
                {"type": "DirectionalLight", "intensity": 0.1, "temperature": 10000, "shadows": True},
                {"type": "SkyLight", "intensity": 0.2, "temperature": 9000},
                {"type": "PointLight", "intensity": 500, "temperature": 2800, "color": [1.0, 0.8, 0.5]},
            ],
            "post_process": {"exposure_ev": 4.0, "bloom": 0.8, "temperature": 7500},
            "fog": True,
            "lumen": True,
        },
    }
    
    if mood:
        mood_modifiers = {
            "moody": {"bloom": 0.3, "contrast": 1.2, "saturation": 0.8},
            "dramatic": {"bloom": 0.5, "contrast": 1.5, "saturation": 0.9},
            "cheerful": {"bloom": 0.2, "contrast": 0.9, "saturation": 1.2},
            "horror": {"bloom": 0.1, "contrast": 1.8, "saturation": 0.5, "vignette": 0.8},
            "cinematic": {"bloom": 0.4, "contrast": 1.1, "saturation": 0.95, "letterbox": True},
        }
        rec = recommendations.get(scene_type, recommendations["outdoor_day"]).copy()
        rec["mood_modifier"] = mood_modifiers.get(mood, {})
        return rec
    
    return recommendations.get(scene_type, recommendations["outdoor_day"])

def get_material_recipe(surface_type: str) -> dict:
    """Get material property recipe for common surface types."""
    recipes = {
        "concrete": {"base_color": [0.5, 0.5, 0.48], "roughness": 0.85, "metallic": 0.0, "normal": "strong"},
        "metal_brushed": {"base_color": [0.6, 0.58, 0.55], "roughness": 0.3, "metallic": 1.0, "normal": "subtle"},
        "wood": {"base_color": [0.35, 0.22, 0.1], "roughness": 0.7, "metallic": 0.0, "normal": "medium"},
        "glass": {"base_color": [0.9, 0.95, 1.0], "roughness": 0.05, "metallic": 0.0, "specular": 1.0, "shading": "Thin Translucent"},
        "plastic": {"base_color": "varies", "roughness": 0.4, "metallic": 0.0, "specular": 0.5},
        "skin": {"base_color": [0.7, 0.5, 0.4], "roughness": 0.5, "metallic": 0.0, "shading": "Subsurface Profile"},
        "fabric": {"base_color": "varies", "roughness": 0.9, "metallic": 0.0, "shading": "Cloth"},
        "car_paint": {"base_color": "varies", "roughness": 0.2, "metallic": 0.0, "shading": "Clear Coat"},
        "marble": {"base_color": [0.9, 0.88, 0.85], "roughness": 0.3, "metallic": 0.0, "shading": "Subsurface"},
        "foliage": {"base_color": [0.1, 0.3, 0.05], "roughness": 0.7, "metallic": 0.0, "shading": "Two Sided Foliage"},
    }
    return recipes.get(surface_type, {"base_color": [0.5, 0.5, 0.5], "roughness": 0.5, "metallic": 0.0})

# Export summary
ADVANCED_KNOWLEDGE_SUMMARY = {
    "total_categories": len(_ALL_CATEGORIES),
    "categories": list(_ALL_CATEGORIES.keys()),
    "total_documents_covered": "21-60",
    "topics": [
        "Gameplay Ability System & Lyra",
        "Lighting, Lumen, Shadows, Exposure, Lightmass, VSMs",
        "Materials, Instances, Layers, SSS, Shading Models",
        "Post Process, Color Grading, Nanite, TSR, VT, Rendering",
        "Level Design, PCG, Foliage, Modeling, World Partition, Data Layers",
        "Animation, Control Rig, IK, Motion Warping",
        "Physics, Collision, Chaos, Destruction, Cloth",
        "Niagara VFX System",
    ],
}