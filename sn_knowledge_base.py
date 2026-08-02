"""
SuperNinja Knowledge Base — Real Unreal Expertise

This isn't just a list of commands — it's the accumulated knowledge
of how to make scenes look GOOD in Unreal Engine. Real numbers,
real ratios, real artistic principles.

When the AI brain needs to decide "what intensity should this light be?"
or "where do I put the camera?" — it looks here.
"""

# ======================================================================
# LIGHTING DESIGN KNOWLEDGE
# ======================================================================

LIGHTING_PRESETS = {
    "golden_hour": {
        "description": "Warm sunset/sunrise light. Most cinematic time of day.",
        "sun": {
            "intensity": 3.5,
            "temperature": 3500,       # Very warm
            "rotation": [-8, 200, 0],  # Low angle, slightly behind
            "shadow_enabled": True,
            "light_color": [1.0, 0.8, 0.5],
        },
        "sky_light": {"intensity": 0.4, "light_color": [0.7, 0.75, 1.0]},
        "fog": {"fog_density": 0.012, "fog_color": [0.9, 0.7, 0.4], "start_distance": 2000},
        "atmosphere": True,
        "tips": [
            "Shadows are LONG at this angle — great for depth",
            "Warm sun + cool sky fill = natural color contrast",
            "Fog catches the warm light beautifully",
        ],
    },

    "midday_sun": {
        "description": "Harsh overhead sunlight. High contrast, short shadows.",
        "sun": {
            "intensity": 8.0,
            "temperature": 6500,        # Daylight white
            "rotation": [-75, 30, 0],   # Nearly overhead
            "shadow_enabled": True,
            "light_color": [1.0, 0.98, 0.95],
        },
        "sky_light": {"intensity": 0.8},
        "fog": {"fog_density": 0.003, "fog_color": [0.85, 0.88, 0.92]},
        "atmosphere": True,
        "tips": [
            "Very harsh shadows — consider softening with source_radius on the directional light",
            "High intensity needed because UE uses physical light units",
            "Sky light should be strong to fill shadow areas",
        ],
    },

    "overcast": {
        "description": "Soft, diffused lighting. No hard shadows. Moody and flat.",
        "sun": {
            "intensity": 1.5,
            "temperature": 7500,        # Cool daylight
            "rotation": [-45, 0, 0],
            "shadow_enabled": False,     # Overcast = no hard shadows
            "light_color": [0.85, 0.88, 0.92],
        },
        "sky_light": {"intensity": 1.2, "light_color": [0.9, 0.92, 0.95]},
        "fog": {"fog_density": 0.008, "fog_color": [0.75, 0.78, 0.8]},
        "atmosphere": True,
        "tips": [
            "No shadows means shapes can look flat — use fog and depth to compensate",
            "Sky light is the PRIMARY light source in overcast",
            "Great for revealing texture detail without shadow distraction",
        ],
    },

    "blue_hour": {
        "description": "Deep twilight. Blue-purple ambient. City lights starting.",
        "sun": {
            "intensity": 0.3,
            "temperature": 9000,        # Very cool
            "rotation": [-3, 220, 0],   # Just below horizon
            "shadow_enabled": True,
            "light_color": [0.5, 0.6, 1.0],
        },
        "sky_light": {"intensity": 0.2, "light_color": [0.3, 0.4, 0.8]},
        "fog": {"fog_density": 0.02, "fog_color": [0.3, 0.35, 0.55]},
        "atmosphere": True,
        "tips": [
            "Add warm point lights to contrast the cool ambient — they'll pop",
            "Very low sun intensity + strong atmosphere = dramatic sky gradients",
            "Fog should be tinted blue to match the ambient",
        ],
    },

    "film_noir": {
        "description": "High contrast black and white movie look. Dramatic shadows.",
        "sun": {
            "intensity": 6.0,
            "temperature": 4200,
            "rotation": [-15, 90, 0],   # Side-lit for dramatic shadows
            "shadow_enabled": True,
            "light_color": [0.95, 0.92, 0.88],
        },
        "sky_light": {"intensity": 0.05, "light_color": [0.5, 0.5, 0.55]},  # Very dim fill
        "fog": {"fog_density": 0.025, "fog_color": [0.25, 0.25, 0.3]},
        "atmosphere": True,
        "tips": [
            "Key ratio: fill light should be 1/10th of key for noir look",
            "Side-lighting creates the dramatic shadow patterns on faces",
            "Use venetian blind shadow patterns for classic noir look",
            "Point lights should have small attenuation_radius for pools of light",
        ],
    },

    "neon_city": {
        "description": "Cyberpunk nighttime. Neon colors, rain, reflections.",
        "sun": {
            "intensity": 0.0,           # No sun — it's night
            "temperature": 0,
            "rotation": [-90, 0, 0],
            "shadow_enabled": False,
        },
        "sky_light": {"intensity": 0.1, "light_color": [0.15, 0.1, 0.25]},
        "fog": {"fog_density": 0.035, "fog_color": [0.15, 0.1, 0.2], "start_distance": 500},
        "atmosphere": True,
        "point_lights": [
            {"location": [0, 0, 350], "intensity": 8000, "light_color": [1.0, 0.1, 0.5], "attenuation_radius": 600, "name": "SN_NeonPink"},
            {"location": [400, 200, 250], "intensity": 6000, "light_color": [0.1, 0.8, 1.0], "attenuation_radius": 500, "name": "SN_NeonBlue"},
            {"location": [-300, -100, 300], "intensity": 7000, "light_color": [0.2, 1.0, 0.3], "attenuation_radius": 450, "name": "SN_NeonGreen"},
            {"location": [200, -400, 200], "intensity": 5000, "light_color": [1.0, 0.5, 0.0], "attenuation_radius": 350, "name": "SN_NeonOrange"},
        ],
        "tips": [
            "Small attenuation_radius makes neon lights feel local and focused",
            "High intensity + small radius = bright pools in darkness",
            "Fog is CRITICAL — it catches the neon colors and spreads them",
            "Rain + neon reflections need a wet floor material",
        ],
    },

    "studio_3point": {
        "description": "Classic photography 3-point lighting. Professional and clean.",
        "key_light": {
            "type": "spot",
            "location": [-300, -200, 500],
            "rotation": [-45, 30, 0],
            "intensity": 8000,
            "inner_cone_angle": 20,
            "outer_cone_angle": 50,
            "light_color": [1.0, 0.95, 0.9],
            "name": "SN_Key",
        },
        "fill_light": {
            "type": "point",
            "location": [300, 200, 300],
            "intensity": 2000,
            "light_color": [0.9, 0.92, 1.0],
            "attenuation_radius": 2000,
            "name": "SN_Fill",
        },
        "rim_light": {
            "type": "spot",
            "location": [0, -400, 400],
            "rotation": [-60, 180, 0],
            "intensity": 6000,
            "inner_cone_angle": 15,
            "outer_cone_angle": 40,
            "light_color": [1.0, 1.0, 1.0],
            "name": "SN_Rim",
        },
        "sky_light": {"intensity": 0.2},
        "tips": [
            "Key:Fill ratio of 4:1 gives professional dimensionality",
            "Key is the brightest, fill is softer and from opposite side",
            "Rim light creates edge separation from background",
            "Move key light's yaw to change Rembrandt vs butterfly vs split lighting",
        ],
    },

    "horror": {
        "description": "Creepy, underlit scene. Heavy shadows, single light source.",
        "sun": {
            "intensity": 0.5,
            "temperature": 2500,        # Sickly warm
            "rotation": [-5, 0, 0],     # Nearly horizontal
            "shadow_enabled": True,
            "light_color": [0.9, 0.7, 0.5],
        },
        "sky_light": {"intensity": 0.03, "light_color": [0.2, 0.2, 0.25]},
        "fog": {"fog_density": 0.05, "fog_color": [0.2, 0.2, 0.18], "start_distance": 200},
        "point_lights": [
            {"location": [0, 0, 100], "intensity": 300, "light_color": [1.0, 0.85, 0.6], "attenuation_radius": 300, "name": "SN_CandleLight"},
        ],
        "tips": [
            "Single light source = maximum shadow drama",
            "Keep fill light near ZERO — you want deep blacks",
            "Fog creates uncertainty and limits visibility",
            "Flickering light (via Blueprint) adds life to the horror",
            "Warm candlelight against cool darkness = unsettling contrast",
        ],
    },

    "interior_office": {
        "description": "Fluorescent office lighting. Flat, institutional.",
        "point_lights": [
            {"location": [0, 0, 300], "intensity": 4000, "light_color": [0.98, 0.97, 0.95], "attenuation_radius": 1500, "name": "SN_CeilingLight1"},
            {"location": [500, 0, 300], "intensity": 4000, "light_color": [0.98, 0.97, 0.95], "attenuation_radius": 1500, "name": "SN_CeilingLight2"},
            {"location": [-500, 0, 300], "intensity": 4000, "light_color": [0.98, 0.97, 0.95], "attenuation_radius": 1500, "name": "SN_CeilingLight3"},
            {"location": [0, 500, 300], "intensity": 4000, "light_color": [0.98, 0.97, 0.95], "attenuation_radius": 1500, "name": "SN_CeilingLight4"},
        ],
        "sky_light": {"intensity": 0.15, "light_color": [0.85, 0.9, 1.0]},
        "tips": [
            "Evenly-spaced overhead lights create the flat institutional look",
            "Slightly cool color temperature mimics fluorescent bulbs",
            "Add a window with warm daylight for visual interest",
            "Low contrast = boring but realistic",
        ],
    },
}

# ======================================================================
# COMPOSITION KNOWLEDGE
# ======================================================================

COMPOSITION_RULES = {
    "rule_of_thirds": {
        "description": "Place subjects at 1/3 and 2/3 lines. Most natural-looking composition.",
        "viewport_offsets": {
            "subject_left_third": {"yaw_offset": 15},   # Nudge subject off-center
            "subject_right_third": {"yaw_offset": -15},
        },
        "camera_tip": "If the subject is at left third, look slightly left of center. The empty space gives breathing room.",
    },

    "depth_layers": {
        "description": "Every good scene has 3 depth layers: foreground, midground, background.",
        "foreground_distance": 200,    # Close to camera — blurred, frames the shot
        "midground_distance": 1000,   # Where the action is
        "background_distance": 5000,  # Distant — sets the mood
        "tip": "Place an object within 200cm of the camera to create instant depth. A pillar, foliage, or prop in the foreground makes everything look better.",
    },

    "camera_heights": {
        "eye_level": {"z_offset": 170, "description": "Human perspective. Default for most scenes."},
        "low_angle": {"z_offset": 50, "description": "Looking up. Makes subjects look powerful/dramatic."},
        "high_angle": {"z_offset": 500, "description": "Looking down. Overview, surveillance feel."},
        "dutch_angle": {"z_offset": 170, "roll": 15, "description": "Tilted. Tension, unease."},
        "bird_eye": {"z_offset": 2000, "description": "Straight down. God's eye view, maps, planning."},
    },

    "framing_techniques": {
        "natural_frame": "Use doorways, windows, arches to frame your subject",
        "leading_lines": "Roads, fences, corridors draw the eye to the subject",
        "negative_space": "Leave 60-70% of frame empty for clean compositions",
        "symmetry": "Center the subject for formal, powerful shots (Kubrick style)",
    },
}

# ======================================================================
# UNREAL-SPECIFIC KNOWLEDGE
# ======================================================================

UNREAL_TIPS = {
    "light_units": {
        "description": "UE5 uses physical light units. Here are real-world reference values.",
        "candle": 12,               # candela
        "40w_bulb": 400,            # candela
        "100w_bulb": 2800,          # candela
        "street_lamp": 15000,       # candela
        "car_headlight": 30000,     # candela
        "sun_overcast": 3.0,        # lux (directional)
        "sun_direct": 10.0,         # lux (directional)
        "note": "Point/Spot lights use Candela. Directional uses Lux. These are physically correct.",
    },

    "shadow_quality": {
        "source_radius": "Higher source_radius = softer shadows (sun default ~0.5, overcast ~5.0)",
        "shadow_bias": "Reduce bias for sharper contact shadows, increase to prevent shadow acne",
        "cascaded_shadows": "Directional lights use CSM — set Cascade Transition to smooth for outdoor scenes",
        "ray_traced": "If Lumen is enabled, shadows are handled automatically. No need to tweak cascade settings.",
    },

    "lumen_tips": {
        "enabled_by_default": True,
        "turn_off": "r.Lumen.ScreenProbeGather 0 (for performance testing)",
        "surface_cache": "Lumen caches surface lighting — move lights slowly or use Movable for dynamic changes",
        "hardware_reqs": "Lumen needs RTX 2060+ or equivalent for real-time. Software Lumen works on any GPU but slower.",
    },

    "nanite_tips": {
        "enabled_by_default": True,
        "fallback_mesh": "If Nanite can't render (translucent, masked), it falls back to normal rendering",
        "pixel_depth": "Nanite auto-LODs based on screen pixels — no need to manually set LODs",
    },

    "common_mistakes": {
        "light_too_dim": "If scene looks dark, check: is Sky Light enabled? What's the exposure? Try increasing EV100.",
        "sky_black": "No Sky Sphere or Sky Atmosphere = black sky. Add one.",
        "fog_too_thick": "fog_density above 0.1 is VERY thick. Start with 0.01-0.03.",
        "shadows_missing": "Check: shadow_enabled=True, Mobility=Movable or Stationary, and light intensity > 0",
        "actors_invisible": "Common causes: 1) Material not applied 2) Actor scaled to 0 3) Actor below floor 4) USD import material issue",
        "performance_bad": "Reduce: shadow map resolution, light count, post-processing quality. Nanite + Lumen help a lot.",
    },
}

# ======================================================================
# SCENE TEMPLATES — Pre-built complete scenes
# ======================================================================

SCENE_TEMPLATES = {
    "empty_outdoor": {
        "description": "Clean outdoor environment with sky, sun, and atmosphere. Ready for content.",
        "commands": [
            {"skill": "add_directional_light", "args": {"intensity": 4.0, "rotation": [-45, 45, 0], "temperature": 5500, "shadow_enabled": True, "name": "SN_Sun"}},
            {"skill": "add_sky_light", "args": {"intensity": 1.0, "name": "SN_SkyLight"}},
            {"skill": "add_sky_atmosphere", "args": {"name": "SN_Atmosphere"}},
            {"skill": "add_exponential_height_fog", "args": {"fog_density": 0.01, "fog_color": [0.75, 0.8, 0.85], "name": "SN_Fog"}},
            {"skill": "spawn_actor", "args": {"shape": "Plane", "scale": [50, 50, 1], "name": "SN_Ground"}},
            {"skill": "frame_viewport", "args": {"distance": 2000, "pitch": -25, "yaw": 45}},
        ],
    },

    "dark_alley": {
        "description": "Film noir style dark alley. Single light, fog, moody.",
        "commands": [
            {"skill": "add_directional_light", "args": {"intensity": 1.0, "rotation": [-10, 200, 0], "temperature": 3500, "shadow_enabled": True, "name": "SN_MoonLight"}},
            {"skill": "add_sky_light", "args": {"intensity": 0.05, "light_color": [0.3, 0.3, 0.4], "name": "SN_NightSky"}},
            {"skill": "add_exponential_height_fog", "args": {"fog_density": 0.04, "fog_color": [0.2, 0.2, 0.25], "name": "SN_AlleyFog"}},
            {"skill": "add_point_light", "args": {"location": [0, 0, 300], "intensity": 8000, "light_color": [1.0, 0.85, 0.5], "attenuation_radius": 500, "name": "SN_StreetLamp"}},
            {"skill": "spawn_actor", "args": {"shape": "Plane", "scale": [20, 50, 1], "name": "SN_AlleyFloor"}},
            {"skill": "spawn_actor", "args": {"shape": "Cube", "location": [800, 0, 400], "scale": [1, 50, 8], "name": "SN_WallLeft"}},
            {"skill": "spawn_actor", "args": {"shape": "Cube", "location": [-800, 0, 400], "scale": [1, 50, 8], "name": "SN_WallRight"}},
            {"skill": "frame_viewport", "args": {"location": [0, 0, 170], "distance": 1500, "pitch": -10, "yaw": 30}},
        ],
    },

    "showroom": {
        "description": "Clean product showcase. 3-point lighting, neutral background.",
        "commands": [
            {"skill": "add_sky_light", "args": {"intensity": 0.3, "name": "SN_Ambient"}},
            {"skill": "add_spot_light", "args": {"location": [-300, -200, 500], "rotation": [-45, 30, 0], "intensity": 8000, "inner_cone_angle": 20, "outer_cone_angle": 50, "name": "SN_KeyLight"}},
            {"skill": "add_point_light", "args": {"location": [300, 200, 300], "intensity": 2000, "light_color": [0.9, 0.92, 1.0], "attenuation_radius": 2000, "name": "SN_FillLight"}},
            {"skill": "add_spot_light", "args": {"location": [0, -400, 400], "rotation": [-60, 180, 0], "intensity": 6000, "inner_cone_angle": 15, "outer_cone_angle": 40, "name": "SN_RimLight"}},
            {"skill": "spawn_actor", "args": {"shape": "Plane", "scale": [30, 30, 1], "name": "SN_ShowroomFloor"}},
            {"skill": "frame_viewport", "args": {"distance": 800, "pitch": -15, "yaw": 30}},
        ],
    },

    "neon_street": {
        "description": "Cyberpunk neon-lit street. Colorful point lights, fog, atmosphere.",
        "commands": [
            {"skill": "add_sky_light", "args": {"intensity": 0.1, "light_color": [0.15, 0.1, 0.25], "name": "SN_NightAmbient"}},
            {"skill": "add_exponential_height_fog", "args": {"fog_density": 0.035, "fog_color": [0.15, 0.1, 0.2], "start_distance": 500, "name": "SN_NeonFog"}},
            {"skill": "add_sky_atmosphere", "args": {"name": "SN_NightAtmosphere"}},
            {"skill": "add_point_light", "args": {"location": [0, 0, 350], "intensity": 8000, "light_color": [1.0, 0.1, 0.5], "attenuation_radius": 600, "name": "SN_NeonPink"}},
            {"skill": "add_point_light", "args": {"location": [400, 200, 250], "intensity": 6000, "light_color": [0.1, 0.8, 1.0], "attenuation_radius": 500, "name": "SN_NeonBlue"}},
            {"skill": "add_point_light", "args": {"location": [-300, -100, 300], "intensity": 7000, "light_color": [0.2, 1.0, 0.3], "attenuation_radius": 450, "name": "SN_NeonGreen"}},
            {"skill": "spawn_actor", "args": {"shape": "Plane", "scale": [30, 50, 1], "name": "SN_StreetFloor"}},
            {"skill": "frame_viewport", "args": {"distance": 1200, "pitch": -20, "yaw": 45}},
        ],
    },
}

# ======================================================================
# QUICK REFERENCE — Common values
# ======================================================================

QUICK_VALUES = {
    "typical_room_size_cm": 600,           # 6m = 600cm
    "human_height_cm": 180,
    "door_height_cm": 210,
    "ceiling_height_cm": 280,
    "street_width_cm": 1200,
    "building_height_cm": 1500,            # ~5 stories
    "car_length_cm": 450,
    "light_switch_height_cm": 110,

    "point_light_indoor_default": 3000,    # Candela for a room
    "point_light_outdoor_default": 15000,  # Candela for street lamp
    "directional_sun_default": 3.0,        # Lux for outdoor
    "fog_outdoor_subtle": 0.005,
    "fog_outdoor_medium": 0.02,
    "fog_indoor_thin": 0.003,
    "fog_dramatic": 0.05,

    "exposure_default_ev100": 0.0,
    "exposure_indoor_ev100": 2.0,
    "exposure_night_ev100": 6.0,
    "exposure_bright_outdoor_ev100": -2.0,
}


def get_preset(name: str) -> dict:
    """Get a lighting preset by name."""
    return LIGHTING_PRESETS.get(name.lower())


def get_template(name: str) -> dict:
    """Get a scene template by name."""
    return SCENE_TEMPLATES.get(name.lower())


def list_presets() -> list:
    """List available lighting presets."""
    return list(LIGHTING_PRESETS.keys())


def list_templates() -> list:
    """List available scene templates."""
    return list(SCENE_TEMPLATES.keys())


if __name__ == "__main__":
    print("SuperNinja Knowledge Base")
    print(f"  Lighting presets: {len(LIGHTING_PRESETS)} — {', '.join(LIGHTING_PRESETS.keys())}")
    print(f"  Scene templates: {len(SCENE_TEMPLATES)} — {', '.join(SCENE_TEMPLATES.keys())}")
    print(f"  Composition rules: {len(COMPOSITION_RULES)}")
    print()
    
    for name, preset in LIGHTING_PRESETS.items():
        print(f"\n  {name.upper()}: {preset['description']}")
        if "sun" in preset:
            sun = preset["sun"]
            print(f"    Sun: intensity={sun.get('intensity', 'N/A')}, temp={sun.get('temperature', 'N/A')}K, angle={sun.get('rotation', 'N/A')}")