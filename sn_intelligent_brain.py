"""
SuperNinja Intelligent Brain — LLM-powered decision engine for Unreal Editor.

This replaces the rule-based _analyze_scene_state with a knowledge-aware
reasoning system that can:
  1. Understand UE5 architecture (class hierarchy, framework patterns)
  2. Make informed lighting/material/composition decisions
  3. Generate contextual Blueprint/C++ guidance
  4. Learn from the UE5 training corpus to make better choices

Architecture:
  - Knowledge Layer: sn_ue5_knowledge.py + sn_knowledge_base.py
  - Reasoning Layer: This file (prompt engineering + structured reasoning)
  - Action Layer: sn_skills_registry.py + sn_skill_executor.py
  - Communication Layer: sn_ai_brain.py → cloud server → Unreal
"""

import json
import time
from typing import Optional

# Import knowledge bases
from sn_ue5_knowledge import (
    get_knowledge, get_all_categories, search_knowledge,
    UE5_CLASS_HIERARCHY, GAMEPLAY_FRAMEWORK, UE5_NAMING_CONVENTIONS,
    UE5_EDITOR_INTERFACE, BLUEPRINT_SYSTEM, CPP_BLUEPRINT_INTEROP,
    UE5_DIRECTORY_STRUCTURE, UE5_KEY_CONCEPTS, UE5_PYTHON_PATTERNS,
)
from sn_knowledge_base import (
    LIGHTING_PRESETS, COMPOSITION_RULES, SCENE_TEMPLATES,
    UNREAL_TIPS, QUICK_VALUES,
)
from sn_ue5_knowledge_advanced import (
    LIGHTING_SYSTEM, LUMEN_SYSTEM, SHADOW_SYSTEM, EXPOSURE_SYSTEM,
    LIGHTMASS_SYSTEM, MATERIALS_SYSTEM, RENDERING_SYSTEM,
    LEVEL_DESIGN_SYSTEM, ANIMATION_SYSTEM, PHYSICS_SYSTEM,
    NIAGARA_SYSTEM, PERFORMANCE_GUIDELINES, SCENE_WORKFLOW,
    search_advanced_knowledge, get_lighting_recommendation,
    get_material_recipe, get_advanced_category,
    GAMEPLAY_ABILITY_SYSTEM,
)
from sn_ue5_knowledge_expert import (
    NIAGARA_ADVANCED, AUDIO_SYSTEM, UI_SYSTEM, AI_SYSTEM,
    NETWORKING_SYSTEM, OPTIMIZATION_SYSTEM, PACKAGING_SYSTEM,
    CINEMATICS_SYSTEM, PLUGINS_SYSTEM,
    search_expert_knowledge, get_expert_category,
    get_optimization_profile, get_networking_pattern,
)
from sn_ue5_knowledge_master import (
    EDITOR_SCRIPTING, VIRTUAL_PRODUCTION, QUIXEL_LANDSCAPE, VOLUMETRICS,
    RENDERING_MASTER, GROOM_VT, PERFORMANCE_TOOLS, CONTENT_CREATION,
    PHYSICS_ADVANCED, SOURCE_CONTROL, API_PIPELINE, PRODUCTION,
    search_master_knowledge, get_master_category,
    get_landscape_preset, get_reflection_recommendation,
)


class IntelligentBrain:
    """
    Knowledge-aware reasoning engine for Unreal Editor.
    
    This brain doesn't just check rules — it UNDERSTANDS Unreal Engine.
    It knows why a DirectionalLight needs shadows, why too many point lights
    kill performance, and when to use a Blueprint Interface vs an Event Dispatcher.
    """

    def __init__(self):
        self.scene_memory = {}  # Persists across cycles
        self.decision_log = []  # Track reasoning for transparency
        
    def analyze_scene(self, scene_data: dict, goal: str = None) -> dict:
        """
        Deep analysis of scene state using UE5 knowledge.
        Returns: issues, actions, reasoning, and suggestions.
        """
        self.decision_log = []
        
        issues = []
        actions = []
        suggestions = []
        reasoning = []
        
        total = scene_data.get("total_actors", 0)
        lights = scene_data.get("lights", 0)
        meshes = scene_data.get("meshes", 0)
        type_breakdown = scene_data.get("type_breakdown", {})
        actor_list = scene_data.get("actors", [])
        
        # =====================================================================
        # LIGHTING ANALYSIS — Using real lighting design knowledge
        # =====================================================================
        lighting_analysis = self._analyze_lighting(scene_data, goal)
        issues.extend(lighting_analysis["issues"])
        actions.extend(lighting_analysis["actions"])
        reasoning.extend(lighting_analysis["reasoning"])
        suggestions.extend(lighting_analysis["suggestions"])
        
        # =====================================================================
        # COMPOSITION ANALYSIS — Using composition rules
        # =====================================================================
        composition_analysis = self._analyze_composition(scene_data, goal)
        issues.extend(composition_analysis["issues"])
        actions.extend(composition_analysis["actions"])
        reasoning.extend(composition_analysis["reasoning"])
        suggestions.extend(composition_analysis["suggestions"])
        
        # =====================================================================
        # PERFORMANCE ANALYSIS — Using UE5 best practices
        # =====================================================================
        perf_analysis = self._analyze_performance(scene_data, goal)
        issues.extend(perf_analysis["issues"])
        actions.extend(perf_analysis["actions"])
        reasoning.extend(perf_analysis["reasoning"])
        suggestions.extend(perf_analysis["suggestions"])
        
        # =====================================================================
        # SCENE HYGIENE — Duplicates, naming, organization
        # =====================================================================
        hygiene_analysis = self._analyze_hygiene(scene_data, goal)
        issues.extend(hygiene_analysis["issues"])
        actions.extend(hygiene_analysis["actions"])
        reasoning.extend(hygiene_analysis["reasoning"])
        suggestions.extend(hygiene_analysis["suggestions"])
        
        # =====================================================================
        # GOAL-DIRECTED PLANNING — If user specified a goal
        # =====================================================================
        if goal:
            goal_analysis = self._analyze_for_goal(scene_data, goal)
            issues.extend(goal_analysis["issues"])
            actions.extend(goal_analysis["actions"])
            reasoning.extend(goal_analysis["reasoning"])
            suggestions.extend(goal_analysis["suggestions"])

        # =====================================================================
        # ADVANCED ANALYSIS — Using Docs 21-60 knowledge (Lumen, Materials, etc.)
        # =====================================================================
        advanced = self.get_advanced_scene_analysis(scene_data, goal)
        issues.extend(advanced["issues"])
        actions.extend(advanced["actions"])
        reasoning.extend(advanced["reasoning"])
        suggestions.extend(advanced["suggestions"])

        # =====================================================================
        # EXPERT ANALYSIS — Using Docs 61-100 knowledge (Niagara, Audio, AI, etc.)
        # =====================================================================
        expert = self.get_expert_scene_analysis(scene_data, goal)
        issues.extend(expert["issues"])
        actions.extend(expert["actions"])
        reasoning.extend(expert["reasoning"])
        suggestions.extend(expert["suggestions"])

        # =====================================================================
        # MASTER ANALYSIS — Using Docs 101-151 knowledge (VP, Rendering, etc.)
        # =====================================================================
        master = self.get_master_scene_analysis(scene_data)
        for category, analysis in master.get("analyses", {}).items():
            issues.extend([f"[master:{category}] {i}" for i in analysis.get("issues", [])])
            suggestions.extend([f"[master:{category}] {s}" for s in analysis.get("suggestions", [])])
        # Add master reasoning
        if master.get("total_issues", 0) > 0:
            reasoning.append(f"Master analysis found {master['total_issues']} issues across {len(master.get('analyses', {}))} categories")
        if master.get("total_suggestions", 0) > 0:
            reasoning.append(f"Master analysis provides {master['total_suggestions']} suggestions for advanced features")

        # Build summary
        summary = f"Scene has {total} actors ({lights} lights, {meshes} meshes)"
        if issues:
            summary += f" — {len(issues)} issue(s) found"
        
        # Always save after changes
        if actions:
            actions.append({"skill": "save_level", "args": {}})
        
        # Update scene memory
        self.scene_memory["last_analysis"] = {
            "timestamp": time.time(),
            "total_actors": total,
            "lights": lights,
            "meshes": meshes,
            "issues_count": len(issues),
            "actions_count": len(actions),
            "goal": goal,
        }
        
        return {
            "summary": summary,
            "issues": issues,
            "actions": actions,
            "reasoning": reasoning,
            "suggestions": suggestions,
            "scene_memory": self.scene_memory,
        }

    # =========================================================================
    # LIGHTING ANALYSIS
    # =========================================================================
    
    def _analyze_lighting(self, scene_data: dict, goal: str = None) -> dict:
        """Analyze lighting using real lighting design knowledge from the corpus."""
        issues = []
        actions = []
        reasoning = []
        suggestions = []
        
        lights = scene_data.get("lights", 0)
        type_breakdown = scene_data.get("type_breakdown", {})
        actor_list = scene_data.get("actors", [])
        
        # Count light types
        dir_lights = type_breakdown.get("DirectionalLight", 0)
        point_lights = type_breakdown.get("PointLight", 0)
        spot_lights = type_breakdown.get("SpotLight", 0)
        sky_lights = type_breakdown.get("SkyLight", 0)
        
        # === No lights at all ===
        if lights == 0:
            issues.append("No lights in scene — scene will be completely black/unlit")
            # Choose lighting preset based on goal
            preset = self._choose_lighting_preset(goal)
            reasoning.append(
                f"No lights detected. Applying '{preset}' preset based on "
                f"goal '{goal or 'general improvement'}'. "
                f"From knowledge base: {LIGHTING_PRESETS.get(preset, {}).get('tips', ['Standard 3-point setup recommended'])[0]}"
            )
            actions.append({"skill": "light_scene", "args": {"style": self._preset_to_style(preset)}})
            
        # === Only one directional light (common beginner setup) ===
        elif dir_lights == 1 and point_lights == 0 and sky_lights == 0:
            issues.append("Only a single directional light — scene will have harsh shadows and no fill")
            reasoning.append(
                "Single directional light creates harsh contrast. "
                "Knowledge: A sky light provides ambient fill that softens shadows. "
                "Without fill, the shadow side goes completely black — this is the #1 beginner mistake."
            )
            actions.append({"skill": "add_sky_light", "args": {"intensity": 0.4}})
            suggestions.append("Add a SkyLight for ambient fill — it softens the hard shadow boundary from the directional light")
            
        # === Multiple directional lights (usually wrong) ===
        elif dir_lights > 1:
            issues.append(f"{dir_lights} directional lights — typically only one sun is needed")
            reasoning.append(
                "Multiple DirectionalLights create competing shadow directions, "
                "which looks unnatural. UE5's Sun should be a single light source. "
                "If you need fill, use SkyLight or PointLights instead."
            )
            suggestions.append("Keep only one DirectionalLight (the sun). Use SkyLight for ambient fill and PointLights for accents.")
            
        # === Too many point lights (performance concern) ===
        if point_lights > 15:
            issues.append(f"{point_lights} point lights may cause performance issues")
            reasoning.append(
                f"Each dynamic point light costs GPU time. With {point_lights} point lights, "
                "Lumen may struggle. Consider: using Light Functions for stationary lights, "
                "baking static lights with Lightmass, or reducing source radius."
            )
            suggestions.append("If lights don't need to move, set Mobility to Static and bake lighting. This is much cheaper at runtime.")
            
        # === No sky light when there are directional/point lights ===
        if lights > 0 and sky_lights == 0 and dir_lights > 0:
            reasoning.append(
                "Scene has a sun but no sky light. SkyLight provides indirect/ambient "
                "illumination that fills in shadows naturally. Without it, shadow areas "
                "are pitch black, which looks unrealistic."
            )
            actions.append({"skill": "add_sky_light", "args": {"intensity": 0.35}})
            
        # === Lighting for specific goals ===
        if goal:
            goal_lower = goal.lower()
            if any(w in goal_lower for w in ["noir", "dark", "shadow", "mystery"]):
                reasoning.append(
                    "Film noir style detected in goal. Knowledge: Film noir uses "
                    "high-contrast lighting with hard shadows, low-key fill, and "
                    "venetian blind shadow patterns. Temperature around 3200K, "
                    "intensity 8.0 for key, minimal fill."
                )
                if dir_lights > 0:
                    actions.append({"skill": "adjust_light", "args": {"filter": "DirectionalLight", "intensity": 8.0, "temperature": 3200, "shadow_enabled": True}})
            elif any(w in goal_lower for w in ["neon", "cyberpunk", "futuristic", "city"]):
                reasoning.append(
                    "Neon/cyberpunk style detected. Knowledge: Neon city uses "
                    "multiple colored point lights (cyan, magenta, warm white), "
                    "fog for light scattering, and no directional light (it's night)."
                )
            elif any(w in goal_lower for w in ["golden", "sunset", "warm", "evening"]):
                reasoning.append(
                    "Golden hour style detected. Knowledge: Sun at low angle (-8 degrees), "
                    "temperature 3500K, intensity 3.5, long dramatic shadows, "
                    "warm fog color (0.9, 0.7, 0.4). This is one of the most "
                    "cinematic lighting setups."
                )
        
        return {"issues": issues, "actions": actions, "reasoning": reasoning, "suggestions": suggestions}

    # =========================================================================
    # COMPOSITION ANALYSIS
    # =========================================================================
    
    def _analyze_composition(self, scene_data: dict, goal: str = None) -> dict:
        """Analyze scene composition using composition rules from the corpus."""
        issues = []
        actions = []
        reasoning = []
        suggestions = []
        
        actor_list = scene_data.get("actors", [])
        meshes = scene_data.get("meshes", 0)
        
        if not actor_list:
            return {"issues": issues, "actions": actions, "reasoning": reasoning, "suggestions": suggestions}
        
        # Analyze actor positions for composition
        locations = []
        for actor in actor_list:
            loc = actor.get("location", [0, 0, 0])
            if isinstance(loc, list) and len(loc) == 3:
                locations.append(loc)
        
        if not locations:
            return {"issues": issues, "actions": actions, "reasoning": reasoning, "suggestions": suggestions}
        
        # Check if everything is at origin
        all_at_origin = all(abs(loc[0]) < 100 and abs(loc[1]) < 100 for loc in locations)
        if all_at_origin and len(locations) > 1:
            issues.append("All actors clustered at origin — no spatial composition")
            reasoning.append(
                "All actors are at (0,0,0) ±100 units. This creates visual clutter "
                "with no sense of space. Composition rule: Use the rule of thirds — "
                "place key subjects at intersection points of a 3x3 grid. "
                "Create depth with foreground, midground, and background layers."
            )
            suggestions.append("Spread actors out to create depth. Place key subjects at rule-of-thirds positions.")
            
        # Check vertical distribution
        all_on_ground = all(abs(loc[2]) < 50 for loc in locations)
        if all_on_ground and len(locations) > 2:
            reasoning.append(
                "All actors are at ground level (Z ≈ 0). For interesting composition, "
                "vary the vertical positions. Knowledge: Camera height affects perception — "
                "eye level (170cm) feels neutral, low angle (50cm) feels powerful, "
                "high angle (300cm) feels observational."
            )
            suggestions.append("Vary actor heights for visual interest. Consider a low camera angle for dramatic effect.")
        
        # Frame viewport if there are actors
        if meshes > 0:
            # Calculate rough center of scene
            if locations:
                avg_x = sum(l[0] for l in locations) / len(locations)
                avg_y = sum(l[1] for l in locations) / len(locations)
                avg_z = sum(l[2] for l in locations) / len(locations)
                actions.append({
                    "skill": "frame_viewport",
                    "args": {
                        "target": [avg_x, avg_y, avg_z],
                        "distance": max(500, meshes * 200),
                        "pitch": -25,
                        "yaw": 45,
                    }
                })
        
        return {"issues": issues, "actions": actions, "reasoning": reasoning, "suggestions": suggestions}

    # =========================================================================
    # PERFORMANCE ANALYSIS
    # =========================================================================
    
    def _analyze_performance(self, scene_data: dict, goal: str = None) -> dict:
        """Analyze scene for performance issues using UE5 best practices."""
        issues = []
        actions = []
        reasoning = []
        suggestions = []
        
        type_breakdown = scene_data.get("type_breakdown", {})
        total = scene_data.get("total_actors", 0)
        
        # Too many actors
        if total > 500:
            issues.append(f"Scene has {total} actors — may cause editor slowdown")
            reasoning.append(
                f"Large actor count ({total}). UE5 handles thousands of actors, "
                "but the editor UI (Outliner, Details panel) slows down. "
                "Consider: Use World Partition for large worlds, merge static meshes, "
                "or use Hierarchical Level of Detail (HLOD)."
            )
            suggestions.append("For large scenes, use World Partition and HLOD to maintain performance.")
        
        # Too many dynamic lights
        dynamic_lights = 0
        for actor in scene_data.get("actors", []):
            class_name = actor.get("class", "")
            if "Light" in class_name:
                dynamic_lights += 1
        
        if dynamic_lights > 20:
            issues.append(f"{dynamic_lights} dynamic lights may exceed Lumen budget")
            reasoning.append(
                f"Lumen can typically handle 10-20 dynamic lights efficiently. "
                f"With {dynamic_lights}, some lights may not contribute to global illumination. "
                "Set non-essential lights to Static mobility and bake with Lightmass."
            )
            suggestions.append("Set stationary/moveable lights to Static where possible and bake lighting.")
        
        # Exponential Height Fog tip
        if "ExponentialHeightFog" not in type_breakdown and dynamic_lights > 5:
            reasoning.append(
                "Multiple lights without fog. Adding fog creates light shafts "
                "(god rays) and atmospheric scattering, making lights visible in the air. "
                "This dramatically improves the perceived quality of lighting."
            )
            suggestions.append("Add Exponential Height Fog to make lights look volumetric and atmospheric.")
        
        return {"issues": issues, "actions": actions, "reasoning": reasoning, "suggestions": suggestions}

    # =========================================================================
    # SCENE HYGIENE
    # =========================================================================
    
    def _analyze_hygiene(self, scene_data: dict, goal: str = None) -> dict:
        """Analyze scene for duplicates, naming issues, organization."""
        issues = []
        actions = []
        reasoning = []
        suggestions = []
        
        type_breakdown = scene_data.get("type_breakdown", {})
        actor_list = scene_data.get("actors", [])
        
        # Check for duplicate patterns (PHX_, SM_, etc.)
        duplicate_prefixes = {}
        for actor in actor_list:
            name = actor.get("name", "")
            for prefix in ["PHX_", "SM_", "Default"]:
                if name.startswith(prefix):
                    duplicate_prefixes[prefix] = duplicate_prefixes.get(prefix, 0) + 1
        
        for prefix, count in duplicate_prefixes.items():
            if count > 5:
                issues.append(f"{count} actors with prefix '{prefix}' — likely duplicates")
                reasoning.append(
                    f"Found {count} actors starting with '{prefix}'. These are typically "
                    "auto-generated duplicates from USD import or copy operations. "
                    "Knowledge: One File Per Actor (OFPA) in UE5 means each actor is "
                    "separate, but duplicate actors waste memory and make the Outliner "
                    "hard to navigate."
                )
                actions.append({
                    "skill": "delete_duplicates",
                    "args": {"prefix": prefix, "dry_run": True}
                })
                suggestions.append(f"Run delete_duplicates with prefix='{prefix}' to clean up (dry_run first).")
        
        # Check for default-named actors
        default_named = sum(1 for a in actor_list if a.get("name", "").startswith("StaticMeshActor"))
        if default_named > 10:
            reasoning.append(
                f"{default_named} actors have default names. "
                "Naming convention (from Epic Coding Standard): Use PascalCase, "
                "descriptive names. E.g., 'SM_Wall_Concrete_01' not 'StaticMeshActor_42'."
            )
            suggestions.append("Rename actors following UE5 conventions: SM_ for static meshes, LP_ for light props, etc.")
        
        return {"issues": issues, "actions": actions, "reasoning": reasoning, "suggestions": suggestions}

    # =========================================================================
    # GOAL-DIRECTED PLANNING
    # =========================================================================
    
    def _analyze_for_goal(self, scene_data: dict, goal: str) -> dict:
        """Generate actions specific to the user's stated goal."""
        issues = []
        actions = []
        reasoning = []
        suggestions = []
        
        goal_lower = goal.lower()
        
        # Match goal to scene templates
        for template_name, template in SCENE_TEMPLATES.items():
            if template_name.lower() in goal_lower or any(
                kw in goal_lower for kw in template.get("keywords", [])
            ):
                reasoning.append(
                    f"Goal matches scene template '{template_name}'. "
                    f"This template requires: {', '.join(template.get('required_elements', []))}. "
                    f"Tips: {'; '.join(template.get('tips', []))}"
                )
                break
        
        # Specific goal patterns
        if any(w in goal_lower for w in ["clean", "cleanup", "remove", "fix duplicate"]):
            reasoning.append(
                "Cleanup goal detected. Will focus on removing duplicates, "
                "organizing actors, and fixing naming conventions."
            )
            actions.append({"skill": "delete_duplicates", "args": {"prefix": "", "dry_run": True}})
            
        elif any(w in goal_lower for w in ["light", "bright", "dark", "mood", "atmosphere"]):
            preset = self._choose_lighting_preset(goal)
            reasoning.append(
                f"Lighting goal detected. Applying '{preset}' preset. "
                f"Knowledge: {LIGHTING_PRESETS.get(preset, {}).get('tips', ['See lighting presets'])[0]}"
            )
            actions.append({"skill": "light_scene", "args": {"style": self._preset_to_style(preset)}})
            
        elif any(w in goal_lower for w in ["empty", "start", "new", "beginning"]):
            reasoning.append(
                "Starting from scratch. Will set up a basic scene with "
                "proper lighting, sky, and a starting object."
            )
            actions.append({"skill": "spawn_actor", "args": {"shape": "Cube", "name": "SN_StartCube", "location": [0, 0, 50]}})
            actions.append({"skill": "light_scene", "args": {"style": "studio"}})
            
        return {"issues": issues, "actions": actions, "reasoning": reasoning, "suggestions": suggestions}

    # =========================================================================
    # KNOWLEDGE QUERIES
    # =========================================================================
    
    def query_ue5_knowledge(self, query: str) -> dict:
        """
        Search the UE5 knowledge base for information.
        Used when the user asks a question about UE5.
        """
        results = search_knowledge(query)
        
        # Also search the lighting/material knowledge bases
        lighting_results = {}
        for preset_name, preset_data in LIGHTING_PRESETS.items():
            if query.lower() in preset_name.lower() or query.lower() in str(preset_data).lower():
                lighting_results[preset_name] = preset_data
        
        composition_results = {}
        for rule_name, rule_data in COMPOSITION_RULES.items():
            if query.lower() in rule_name.lower() or query.lower() in str(rule_data).lower():
                composition_results[rule_name] = rule_data
        
        return {
            "ue5_docs": results,
            "lighting_presets": lighting_results,
            "composition_rules": composition_results,
            "query": query,
        }
    
    def explain_ue5_concept(self, concept: str) -> str:
        """
        Explain a UE5 concept in plain language using the knowledge base.
        """
        # Check key concepts first
        if concept.lower() in UE5_KEY_CONCEPTS:
            return UE5_KEY_CONCEPTS[concept.lower()]
        
        # Search all knowledge
        results = search_knowledge(concept)
        if results:
            # Build explanation from search results
            explanations = []
            for category, matches in results.items():
                for match in matches[:2]:
                    value = match.get("value", "")
                    if isinstance(value, str) and len(value) > 20:
                        explanations.append(f"[{category}] {value}")
                    elif isinstance(value, dict):
                        for k, v in list(value.items())[:3]:
                            if isinstance(v, str) and len(v) > 10:
                                explanations.append(f"[{category}] {k}: {v}")
            if explanations:
                return "\n".join(explanations[:5])
        
        return f"No specific knowledge found for '{concept}'. Try: pawn, actor, component, blueprint, material, lumen, nanite, lighting, or construction_script."
    
    def suggest_blueprint_pattern(self, use_case: str) -> dict:
        """
        Suggest the right Blueprint communication pattern for a use case.
        """
        use_case_lower = use_case.lower()
        bp_comm = BLUEPRINT_SYSTEM["communication_methods"]
        
        recommendations = []
        
        # One-to-one
        if any(w in use_case_lower for w in ["switch", "door", "single", "one other", "specific"]):
            recommendations.append({
                "method": "Direct Blueprint Communication",
                "pattern": bp_comm["direct_communication"],
                "why": "One-to-one relationship between two specific Actors",
            })
        
        # One-to-many
        if any(w in use_case_lower for w in ["broadcast", "notify", "multiple", "all", "everyone", "when dies", "trigger many"]):
            recommendations.append({
                "method": "Event Dispatchers",
                "pattern": bp_comm["event_dispatchers"],
                "why": "One-to-many: one event triggers multiple independent responses",
            })
        
        # Many-to-many / polymorphism
        if any(w in use_case_lower for w in ["different type", "same function", "interface", "polymorph", "interact", "use button"]):
            recommendations.append({
                "method": "Blueprint Interfaces",
                "pattern": bp_comm["blueprint_interfaces"],
                "why": "Common functionality across different Blueprint types",
            })
        
        # If no specific match, give all options
        if not recommendations:
            recommendations = [
                {"method": "Direct Communication", "pattern": bp_comm["direct_communication"], "when": "One-to-one between placed Actors"},
                {"method": "Event Dispatchers", "pattern": bp_comm["event_dispatchers"], "when": "One-to-many broadcasting"},
                {"method": "Blueprint Interfaces", "pattern": bp_comm["blueprint_interfaces"], "when": "Common functionality across types"},
                {"method": "Blueprint Casting", "pattern": bp_comm["blueprint_casting"], "when": "Access specialized versions"},
            ]
        
        return {"use_case": use_case, "recommendations": recommendations}

    # =========================================================================
    # HELPERS
    # =========================================================================
    
    def _choose_lighting_preset(self, goal: str = None) -> str:
        """Choose the best lighting preset based on the goal."""
        if not goal:
            return "studio_3point"
        
        goal_lower = goal.lower()
        
        preset_keywords = {
            "golden_hour": ["golden", "sunset", "warm", "evening", "dawn", "sunrise"],
            "midday_sun": ["midday", "noon", "bright", "daylight", "outdoor", "sunny"],
            "overcast": ["overcast", "cloudy", "diffused", "soft", "grey"],
            "blue_hour": ["twilight", "dusk", "blue hour", "moonlit", "night"],
            "film_noir": ["noir", "detective", "shadow", "mystery", "dramatic contrast"],
            "neon_city": ["neon", "cyberpunk", "futuristic", "city night", "neon street"],
            "studio_3point": ["studio", "product", "showroom", "clean", "professional"],
            "horror": ["horror", "scary", "creepy", "eerie", "dark", "unsettling"],
            "interior_office": ["office", "interior", "fluorescent", "corporate", "room"],
        }
        
        for preset, keywords in preset_keywords.items():
            if any(kw in goal_lower for kw in keywords):
                return preset
        
        return "studio_3point"
    
    def _preset_to_style(self, preset: str) -> str:
        """Map a knowledge base preset name to a light_scene style argument."""
        mapping = {
            "golden_hour": "cinematic",
            "midday_sun": "outdoor",
            "overcast": "outdoor",
            "blue_hour": "moody",
            "film_noir": "moody",
            "neon_city": "moody",
            "studio_3point": "studio",
            "horror": "moody",
            "interior_office": "interior",
        }
        return mapping.get(preset, "cinematic")
    
    def get_decision_log(self) -> list:
        """Return the reasoning log from the last analysis."""
        return self.decision_log
    
    def get_narration_for_action(self, skill: str, args: dict) -> str:
        """Generate a conversational narration for an action, using knowledge."""
        narrations = {
            "add_directional_light": lambda a: f"Adding sunlight at {a.get('intensity', 3.0)} intensity — this creates our primary light source with directional shadows",
            "add_point_light": lambda a: f"Placing a point light at {a.get('location', 'default position')} — this adds local illumination and fill",
            "add_spot_light": lambda a: f"Aiming a spotlight — great for focused, dramatic lighting with cone falloff",
            "add_sky_light": lambda a: f"Adding sky light for ambient fill — this prevents shadows from going completely black",
            "add_exponential_height_fog": lambda a: f"Adding atmospheric fog — this makes lights visible in the air (volumetric scattering) and adds depth",
            "add_sky_atmosphere": lambda a: f"Adding sky atmosphere — realistic sky rendering with rayleigh scattering",
            "adjust_light": lambda a: f"Tuning light properties — {', '.join(f'{k}={v}' for k, v in a.items() if k not in ['filter', 'name'])}",
            "spawn_actor": lambda a: f"Spawning a {a.get('shape', 'shape')} called '{a.get('name', 'unnamed')}' — placing geometry in the scene",
            "move_actor": lambda a: f"Moving '{a.get('name', 'actor')}' to {a.get('location', 'new position')}",
            "rotate_actor": lambda a: f"Rotating '{a.get('name', 'actor')}' — adjusting its orientation",
            "scale_actor": lambda a: f"Scaling '{a.get('name', 'actor')}' — changing its size",
            "delete_actor": lambda a: f"Deleting '{a.get('name', 'actor')}' — removing it from the scene",
            "delete_duplicates": lambda a: f"Scanning for duplicates (prefix: '{a.get('prefix', '*')}') — {'DRY RUN — just checking' if a.get('dry_run') else 'LIVE — will delete!'}",
            "scatter_actors": lambda a: f"Scattering copies of '{a.get('source_name', 'actor')}' — distributing objects across the scene",
            "light_scene": lambda a: f"Applying '{a.get('style', 'cinematic')}' lighting preset — setting up the complete lighting rig",
            "frame_viewport": lambda a: f"Framing the camera — adjusting viewpoint to see the scene from the best angle",
            "apply_material": lambda a: f"Applying material to '{a.get('actor_name', 'actor')}' — changing its surface appearance",
            "save_level": lambda a: "Saving the level — preserving our changes",
            "cleanup_duplicates": lambda a: f"Cleaning up duplicate actors — this will remove the redundant copies",
            "scatter_props": lambda a: f"Scattering props — distributing environment details for visual richness",
        }
        
        if skill in narrations:
            try:
                return narrations[skill](args)
            except Exception:
                return f"Executing {skill}..."
        return f"Running {skill} with {args}"


# =========================================================================
# ADVANCED ANALYSIS METHODS (using Documents 21-60 knowledge)
# =========================================================================

    def analyze_lighting_advanced(self, scene_data: dict, goal: str = None) -> dict:
        """Deep lighting analysis using Lumen, shadow, exposure, and lightmass knowledge."""
        issues = []
        actions = []
        reasoning = []
        suggestions = []

        type_breakdown = scene_data.get("type_breakdown", {})
        lights = scene_data.get("lights", 0)
        dir_lights = type_breakdown.get("DirectionalLight", 0)
        point_lights = type_breakdown.get("PointLight", 0)
        spot_lights = type_breakdown.get("SpotLight", 0)
        sky_lights = type_breakdown.get("SkyLight", 0)

        # === Lumen compatibility check ===
        if lights > 0:
            # Check if scene would benefit from Lumen
            movable_lights = point_lights + spot_lights
            if movable_lights > 8:
                reasoning.append(
                    f"Scene has {movable_lights} dynamic lights. Lumen handles dynamic GI efficiently, "
                    f"but performance degrades beyond ~20 dynamic lights. From advanced knowledge: "
                    f"Use Stationary mobility where possible for partial precomputation. "
                    f"Software Lumen is faster than Hardware Lumen on most GPUs."
                )
                suggestions.append(
                    "Consider switching some PointLights to Stationary mobility — "
                    "Lumen will precompute their contribution to static geometry while "
                    "still allowing color/intensity changes at runtime."
                )

            # === Shadow quality analysis ===
            if dir_lights > 0 and sky_lights == 0:
                reasoning.append(
                    "Directional light present without SkyLight. From shadow knowledge: "
                    "Virtual Shadow Maps (VSMs) provide consistent high-resolution shadows "
                    "in UE5, but without ambient fill from a SkyLight, shadow areas will be "
                    "completely black. VSMs work best with some indirect light to make shadows visible."
                )

            # === Exposure analysis ===
            if lights > 3 and lights < 10:
                suggestions.append(
                    "With multiple lights, consider locking auto-exposure by setting min/max EV "
                    "to the same value in a Post Process Volume. This prevents the scene from "
                    "brightening/darkening unexpectedly when lights change. EV100 values: "
                    "outdoor=12-15, indoor=6-10, night=2-5."
                )

            # === Lightmass vs Lumen recommendation ===
            if dir_lights > 0 and point_lights == 0:
                reasoning.append(
                    "Scene uses only a DirectionalLight. For static scenes, Lightmass can bake "
                    "beautiful GI with area shadows and diffuse interreflection. For dynamic scenes, "
                    "Lumen provides real-time GI. Consider the project's needs: if lighting doesn't "
                    "change at runtime, Lightmass gives higher quality; if it does, Lumen is the way to go."
                )

        # === Get lighting recommendation for goal ===
        if goal:
            goal_lower = goal.lower()
            scene_type = None
            mood = None

            if any(w in goal_lower for w in ["outdoor", "exterior", "outside", "landscape"]):
                scene_type = "outdoor_day"
                if any(w in goal_lower for w in ["sunset", "golden", "evening", "warm"]):
                    scene_type = "outdoor_golden_hour"
                if any(w in goal_lower for w in ["night", "dark", "moon"]):
                    scene_type = "night_exterior"
            elif any(w in goal_lower for w in ["interior", "indoor", "room", "office", "inside"]):
                scene_type = "interior_office"
            elif any(w in goal_lower for w in ["noir", "detective", "dramatic"]):
                scene_type = "night_exterior"
                mood = "dramatic"

            if any(w in goal_lower for w in ["moody", "atmospheric", "somber"]):
                mood = "moody"
            elif any(w in goal_lower for w in ["horror", "scary", "creepy"]):
                mood = "horror"
            elif any(w in goal_lower for w in ["cinematic", "film", "movie"]):
                mood = "cinematic"

            if scene_type:
                rec = get_lighting_recommendation(scene_type, mood)
                reasoning.append(
                    f"Lighting recommendation for '{goal}': {len(rec['lights'])} lights recommended. "
                    f"{'Fog enabled for depth. ' if rec.get('fog') else ''}"
                    f"{'Lumen recommended for dynamic GI. ' if rec.get('lumen') else ''}"
                    f"Mood modifier: {rec.get('mood_modifier', {})}"
                )
                for light_spec in rec.get("lights", []):
                    actions.append({"skill": f"add_{light_spec['type'].lower()}", "args": {
                        k: v for k, v in light_spec.items() if k != "type"
                    }})

        return {
            "issues": issues,
            "actions": actions,
            "reasoning": reasoning,
            "suggestions": suggestions,
        }

    def analyze_material_needs(self, scene_data: dict, goal: str = None) -> dict:
        """Analyze material needs based on scene content and goal."""
        issues = []
        actions = []
        reasoning = []
        suggestions = []

        actors = scene_data.get("actors", [])

        # Find actors that might need materials
        mesh_actors = [a for a in actors if "Mesh" in a.get("class", a.get("type", ""))]

        if len(mesh_actors) > 0:
            # Suggest material improvements based on common patterns
            reasoning.append(
                f"Scene has {len(mesh_actors)} mesh actors. From material knowledge: "
                f"Use Material Instances for variations of the same material (e.g., different colors). "
                f"This avoids full shader compilation for each variation. "
                f"Key PBR properties: Base Color (0-1 range, no pure black/white), "
                f"Roughness (0=mirror, 1=diffuse), Metallic (0 or 1, rarely in-between)."
            )

            # Suggest material recipes based on naming conventions
            for actor in mesh_actors[:5]:
                name = actor.get("name", "").lower()
                surface_type = None
                if any(w in name for w in ["concrete", "wall", "floor", "ground"]):
                    surface_type = "concrete"
                elif any(w in name for w in ["metal", "steel", "iron", "chrome"]):
                    surface_type = "metal_brushed"
                elif any(w in name for w in ["wood", "plank", "table"]):
                    surface_type = "wood"
                elif any(w in name for w in ["glass", "window", "mirror"]):
                    surface_type = "glass"
                elif any(w in name for w in ["leaf", "tree", "plant", "grass"]):
                    surface_type = "foliage"

                if surface_type:
                    recipe = get_material_recipe(surface_type)
                    shading_info = f", Shading Model={recipe.get('shading')}" if recipe.get('shading') else ""
                    suggestions.append(
                        f"Actor '{actor.get('name')}' looks like {surface_type}. "
                        f"Suggested PBR values: Roughness={recipe.get('roughness')}, "
                        f"Metallic={recipe.get('metallic')}{shading_info}"
                    )

        # Post-process suggestions
        if goal:
            goal_lower = goal.lower()
            if any(w in goal_lower for w in ["cinematic", "film", "movie", "dramatic"]):
                suggestions.append(
                    "For cinematic look: Add Post Process Volume with color grading. "
                    "From rendering knowledge: Use ACES tonemapper slope=0.6, "
                    "increase contrast in shadows, add subtle bloom (0.3-0.5), "
                    "and use depth of field for focus. Consider letterboxing (2.39:1 aspect)."
                )
            elif any(w in goal_lower for w in ["neon", "cyberpunk", "futuristic"]):
                suggestions.append(
                    "For neon look: High emissive values on materials (2.0+) trigger bloom. "
                    "From rendering knowledge: Use Custom Depth + Post Process material "
                    "for neon glow outlines. Increase bloom intensity to 0.8+. "
                    "Color grade: Boost saturation in highlights, cool shadows (8000K+)."
                )

        return {
            "issues": issues,
            "actions": actions,
            "reasoning": reasoning,
            "suggestions": suggestions,
        }

    def analyze_rendering_needs(self, scene_data: dict, goal: str = None) -> dict:
        """Analyze rendering pipeline needs based on scene complexity."""
        issues = []
        actions = []
        reasoning = []
        suggestions = []

        actor_count = scene_data.get("total_actors", scene_data.get("actor_count", 0))
        mesh_count = scene_data.get("meshes", 0)

        # === Nanite recommendations ===
        if mesh_count > 20:
            reasoning.append(
                f"Scene has {mesh_count} meshes. Nanite virtualized geometry can dramatically "
                f"reduce draw calls and memory. From Nanite knowledge: Enable Nanite on static "
                f"meshes to eliminate manual LODs. Nanite renders pixel-accurate detail and "
                f"integrates with Lumen and VSMs. Cannot be used on Skeletal Meshes."
            )
            suggestions.append(
                "Enable Nanite on your static meshes — it eliminates manual LOD work, "
                "reduces memory, and provides pixel-accurate geometry. Just check 'Nanite' "
                "in the Static Mesh editor. Works automatically with Lumen GI."
            )

        # === TSR recommendation ===
        if actor_count > 50:
            suggestions.append(
                "For complex scenes with 50+ actors, Temporal Super Resolution (TSR) can "
                "maintain visual quality while rendering at lower resolution for better performance. "
                "Enable in Project Settings > Rendering > Upscaling Method."
            )

        # === Post-process for atmosphere ===
        if goal:
            goal_lower = goal.lower()
            if any(w in goal_lower for w in ["fog", "atmosphere", "mist", "haze", "moody"]):
                suggestions.append(
                    "For atmospheric effects: Add Exponential Height Fog + Volumetric Fog. "
                    "From rendering knowledge: Enable 'Volumetric Fog' on the fog actor, "
                    "increase 'Fog Inscattering Color' to warm tones for god rays effect. "
                    "Pair with a Directional Light that has 'Volumetric Scattering Intensity' > 0."
                )

        return {
            "issues": issues,
            "actions": actions,
            "reasoning": reasoning,
            "suggestions": suggestions,
        }

    def analyze_level_design(self, scene_data: dict, goal: str = None) -> dict:
        """Analyze level design patterns and suggest improvements."""
        issues = []
        actions = []
        reasoning = []
        suggestions = []

        actor_count = scene_data.get("total_actors", scene_data.get("actor_count", 0))
        actors = scene_data.get("actors", [])

        # === Large scene recommendations ===
        if actor_count > 100:
            reasoning.append(
                f"Scene has {actor_count} actors. For large worlds, World Partition divides "
                f"the world into cells that stream in/out based on camera position. "
                f"From level design knowledge: This replaces traditional Level Streaming, "
                f"stores everything in one map file, and supports team collaboration."
            )
            suggestions.append(
                "For scenes with 100+ actors spread over a large area, consider converting "
                "to World Partition for automatic streaming. Use Tools > Convert Level."
            )

        # === Foliage/scatter suggestions ===
        duplicate_names = set()
        seen = set()
        for a in actors:
            name = a.get("name", "")
            base = name.rsplit("_", 1)[0] if "_" in name else name
            if base in seen:
                duplicate_names.add(base)
            seen.add(base)

        if len(duplicate_names) > 3:
            reasoning.append(
                f"Found {len(duplicate_names)} sets of similarly-named actors. "
                f"From level design knowledge: PCG (Procedural Content Generation) can scatter "
                f"props more efficiently than manual placement. Use PCG for trees, rocks, "
                f"debris — it handles density, random scale, and collision avoidance automatically."
            )
            suggestions.append(
                "Consider using PCG for scattering repeated elements like trees, rocks, and props. "
                "It handles density control, minimum spacing, and random scale variation automatically."
            )

        return {
            "issues": issues,
            "actions": actions,
            "reasoning": reasoning,
            "suggestions": suggestions,
        }

    def get_advanced_scene_analysis(self, scene_data: dict, goal: str = None) -> dict:
        """Run all advanced analyses and merge results."""
        all_issues = []
        all_actions = []
        all_reasoning = []
        all_suggestions = []

        analyses = {
            "lighting_advanced": self.analyze_lighting_advanced(scene_data, goal),
            "materials": self.analyze_material_needs(scene_data, goal),
            "rendering": self.analyze_rendering_needs(scene_data, goal),
            "level_design": self.analyze_level_design(scene_data, goal),
        }

        for name, result in analyses.items():
            all_issues.extend(result.get("issues", []))
            all_actions.extend(result.get("actions", []))
            all_reasoning.extend(result.get("reasoning", []))
            all_suggestions.extend(result.get("suggestions", []))

        return {
            "analyses": analyses,
            "issues": all_issues,
            "actions": all_actions,
            "reasoning": all_reasoning,
            "suggestions": all_suggestions,
        }

    def query_advanced_knowledge(self, query: str) -> dict:
        """Search the advanced knowledge base (Docs 21-60)."""
        results = search_advanced_knowledge(query)
        return {
            "query": query,
            "results": results,
            "total_found": len(results),
        }

    def get_lighting_setup(self, scene_type: str, mood: str = None) -> dict:
        """Get a complete lighting setup recommendation for a scene type and mood."""
        rec = get_lighting_recommendation(scene_type, mood)
        return {
            "scene_type": scene_type,
            "mood": mood,
            "recommendation": rec,
            "workflow": SCENE_WORKFLOW.get("lighting_workflow", {}),
        }

    def get_surface_recipe(self, surface_type: str) -> dict:
        """Get PBR material recipe for a surface type."""
        recipe = get_material_recipe(surface_type)
        return {
            "surface_type": surface_type,
            "recipe": recipe,
            "shading_info": MATERIALS_SYSTEM.get("shading_models", {}).get("available", {}),
        }


# =========================================================================
    # EXPERT ANALYSIS METHODS — Docs 61-100 (Niagara, Audio, UI, AI, Net, Opt)
    # =========================================================================

    def analyze_niagara_needs(self, scene_data: dict, goal: str = None) -> dict:
        """Analyze Niagara VFX needs based on scene content and goal."""
        issues = []
        actions = []
        reasoning = []
        suggestions = []

        actor_list = scene_data.get("actors", [])
        type_breakdown = scene_data.get("type_breakdown", {})
        total = scene_data.get("total_actors", 0)

        # Detect Niagara-related actors
        niagara_actors = [a for a in actor_list if "niagara" in a.get("type", "").lower()
                         or "emitter" in a.get("type", "").lower()
                         or "particle" in a.get("name", "").lower()]
        has_fire = any("fire" in a.get("name", "").lower() or "flame" in a.get("name", "").lower()
                       for a in actor_list)
        has_smoke = any("smoke" in a.get("name", "").lower() or "steam" in a.get("name", "").lower()
                        for a in actor_list)
        has_water = any("water" in a.get("name", "").lower() or "rain" in a.get("name", "").lower()
                        or "river" in a.get("name", "").lower() for a in actor_list)

        # Check for particle systems that could benefit from Niagara
        cascade_actors = [a for a in actor_list if "cascade" in a.get("type", "").lower()
                         or "particlessystem" in a.get("type", "").lower()]
        if cascade_actors:
            issues.append(f"Found {len(cascade_actors)} Cascade particle system(s) — consider migrating to Niagara for better performance and flexibility")
            reasoning.append("Niagara provides GPU simulation, modular stack architecture, and better data interfaces than Cascade")
            actions.append({"skill": "query_expert_knowledge", "args": {"query": "niagara migration cascade"}})
            suggestions.append("Niagara supports all Cascade features plus GPU particles, mesh emission, audio data interfaces, and custom modules")

        # VFX recommendations based on scene content
        if has_fire and not niagara_actors:
            issues.append("Fire elements detected but no Niagara systems — recommend Niagara Fluids fire simulation")
            reasoning.append("Niagara Fluids provides physically-accurate 2D/3D gas simulations for fire with dissipation, buoyancy, and turbulence")
            actions.append({"skill": "add_niagara_effect", "args": {"effect_type": "fire"}})
            suggestions.append("Use Niagara Fluids Grid3D for volumetric fire, or Grid2D for simpler fire with less GPU cost")

        if has_smoke and not niagara_actors:
            issues.append("Smoke/steam elements detected — recommend Niagara Fluids smoke simulation")
            reasoning.append("Niagara Fluids smoke uses the same gas simulation framework as fire but with different parameters for density and dissipation")
            actions.append({"skill": "add_niagara_effect", "args": {"effect_type": "smoke"}})
            suggestions.append("For low-GPU-cost smoke, use Grid2D gas simulation with high dissipation rate")

        if has_water and not niagara_actors:
            issues.append("Water elements detected — consider Niagara for rain, splashes, or waterfall effects")
            reasoning.append("Niagara Fluids provides liquid simulation (FLIP/PIC solver) for realistic water, plus simple particle rain")
            actions.append({"skill": "add_niagara_effect", "args": {"effect_type": "water"}})
            suggestions.append("For rain: use simple GPU particles with collision. For waterfalls/splashes: use Niagara Fluids Liquid3D")

        # Check for scene complexity affecting VFX budget
        if total > 500 and niagara_actors:
            perf_info = get_optimization_profile(60)
            reasoning.append(f"Large scene ({total} actors) with Niagara systems — check VFX budget")
            suggestions.append(f"Consider fixed FPS budgeting: allocate ~4ms for VFX at 60fps target")

        return {"issues": issues, "actions": actions, "reasoning": reasoning, "suggestions": suggestions}

    def analyze_audio_needs(self, scene_data: dict, goal: str = None) -> dict:
        """Analyze audio needs based on scene content and goal."""
        issues = []
        actions = []
        reasoning = []
        suggestions = []

        actor_list = scene_data.get("actors", [])
        type_breakdown = scene_data.get("type_breakdown", {})

        # Detect audio-related actors
        audio_actors = [a for a in actor_list if "audio" in a.get("type", "").lower()
                       or "sound" in a.get("type", "").lower()]
        ambient_actors = [a for a in actor_list if "ambient" in a.get("name", "").lower()
                         or "atmosphere" in a.get("name", "").lower()]

        # Check for scenes that need audio
        has_outdoor = any("landscape" in a.get("type", "").lower() or "foliage" in a.get("name", "").lower()
                         for a in actor_list)
        has_enclosed = any("room" in a.get("name", "").lower() or "interior" in a.get("name", "").lower()
                          for a in actor_list)

        if not audio_actors and has_outdoor:
            issues.append("Outdoor scene has no audio — recommend adding ambient MetaSounds (wind, birds, environment)")
            reasoning.append("MetaSounds provide procedurally-generated, data-driven audio that can react to game state without additional memory")
            actions.append({"skill": "add_audio_ambient", "args": {"environment": "outdoor"}})
            suggestions.append("Use MetaSound Source with random triggers for wind gusts and bird calls. Add Sound Attenuation for distance falloff.")

        if not audio_actors and has_enclosed:
            issues.append("Enclosed scene has no audio — recommend adding room tone and spatial audio")
            reasoning.append("Enclosed spaces benefit from spatial audio with reverb and Sound Attenuation settings")
            actions.append({"skill": "add_audio_ambient", "args": {"environment": "indoor"}})
            suggestions.append("Use Sound Attenuation with 3D stereo panning and reverb send for room tone")

        # Check for spatial audio setup
        spatial_audio = AUDIO_SYSTEM.get("spatial_audio", {})
        if audio_actors and has_outdoor:
            reasoning.append("Outdoor scenes benefit from Spatial Sound with distance attenuation and air absorption")
            suggestions.append("Enable Spatialization on audio sources. Use Attenuation Shapes (Box, Capsule, Sphere) for outdoor ambient sounds")

        # MetaSounds recommendation
        sound_cues = [a for a in audio_actors if "soundcue" in a.get("type", "").lower()]
        if sound_cues:
            issues.append(f"Found {len(sound_cues)} Sound Cue(s) — consider migrating to MetaSounds for procedural audio control")
            reasoning.append("MetaSounds replace Sound Cues with a node-based, data-driven system that eliminates random node order dependencies")
            actions.append({"skill": "query_expert_knowledge", "args": {"query": "metasound migration sound cue"}})

        return {"issues": issues, "actions": actions, "reasoning": reasoning, "suggestions": suggestions}

    def analyze_ui_needs(self, scene_data: dict, goal: str = None) -> dict:
        """Analyze UI/widget needs based on scene content and goal."""
        issues = []
        actions = []
        reasoning = []
        suggestions = []

        actor_list = scene_data.get("actors", [])

        # Detect UI-related actors
        widget_actors = [a for a in actor_list if "widget" in a.get("type", "").lower()
                        or "widgetcomponent" in a.get("type", "").lower()]
        hud_actors = [a for a in actor_list if "hud" in a.get("type", "").lower()
                     or "hud" in a.get("name", "").lower()]

        # Goal-based UI recommendations
        if goal and any(kw in goal.lower() for kw in ["menu", "ui", "interface", "hud", "widget"]):
            ui_rec = UI_SYSTEM.get("umg", {})
            reasoning.append(f"UI-focused goal detected — recommend UMG Widget Blueprint approach")
            suggestions.append("Use Widget Blueprint (UMG) for all in-game UI. Use Common UI for platform-agnostic input. Use Slate only for Editor tools.")

            if "menu" in goal.lower():
                suggestions.append("Use Common UI's CommonButton and CommonBorder for consistent menu styling across platforms")
            if "hud" in goal.lower():
                suggestions.append("Add Widget Component to 3D actors for world-space HUD elements. Use screen-space Widget for player HUD")

        # Check for widget components in 3D space
        if widget_actors:
            reasoning.append(f"Found {len(widget_actors)} Widget Component(s) — verify tick and render settings for performance")
            suggestions.append("Set Widget Component Tick Mode to 'When Drawn' for performance. Use Visible flag to control rendering")

        return {"issues": issues, "actions": actions, "reasoning": reasoning, "suggestions": suggestions}

    def analyze_ai_needs(self, scene_data: dict, goal: str = None) -> dict:
        """Analyze AI system needs based on scene content and goal."""
        issues = []
        actions = []
        reasoning = []
        suggestions = []

        actor_list = scene_data.get("actors", [])
        type_breakdown = scene_data.get("type_breakdown", {})

        # Detect AI-related actors
        character_actors = [a for a in actor_list if "character" in a.get("type", "").lower()
                           or "pawn" in a.get("type", "").lower()]
        ai_actors = [a for a in actor_list if "aicontroller" in a.get("type", "").lower()
                    or "behaviortree" in a.get("name", "").lower()]
        nav_volumes = [a for a in actor_list if "navmesh" in a.get("type", "").lower()
                      or "navmeshbounds" in a.get("type", "").lower()
                      or "navigation" in a.get("name", "").lower()]

        # AI recommendations for characters without controllers
        pawns_without_ai = [c for c in character_actors
                           if "player" not in c.get("name", "").lower()
                           and not any(ai.get("name", "").lower() in c.get("name", "").lower() for ai in ai_actors)]

        if pawns_without_ai and goal and "gameplay" in goal.lower():
            issues.append(f"Found {len(pawns_without_ai)} non-player character(s) without AI controllers — recommend adding Behavior Trees")
            reasoning.append("UE5 AI uses AIController + Behavior Tree + Blackboard for decision-making. EQS for spatial queries.")
            actions.append({"skill": "setup_ai_character", "args": {"character_type": "basic"}})
            suggestions.append("Pattern: AIController → Runs Behavior Tree → Blackboard stores state → EQS finds positions → Navigation Mesh moves pawn")

        # NavMesh check for AI movement
        if character_actors and not nav_volumes:
            issues.append("Characters detected but no NavMeshBoundsVolume — AI won't be able to navigate")
            reasoning.append("Navigation Mesh is required for AI movement. Place NavMeshBoundsVolume covering the playable area.")
            actions.append({"skill": "add_navmesh", "args": {}})
            suggestions.append("Add NavMeshBoundsVolume covering walkable areas. Press P in editor to visualize NavMesh. Use NavModifier volumes for custom areas.")

        # Behavior tree depth guidance
        if ai_actors:
            bt_info = AI_SYSTEM.get("behavior_trees", {})
            reasoning.append("Behavior Trees should be kept simple — use 3-5 depth max, leverage Decorators and Services")
            suggestions.append("Use Decorators for conditional checks (Has Ammo? Is Enemy Visible?). Use Services for periodic updates (Update Target every 0.5s). Use State Tree for simpler AI.")

        return {"issues": issues, "actions": actions, "reasoning": reasoning, "suggestions": suggestions}

    def analyze_networking_needs(self, scene_data: dict, goal: str = None) -> dict:
        """Analyze multiplayer/networking needs based on scene content and goal."""
        issues = []
        actions = []
        reasoning = []
        suggestions = []

        actor_list = scene_data.get("actors", [])

        # Detect networking-related actors
        player_starts = [a for a in actor_list if "playerstart" in a.get("type", "").lower()]
        network_actors = [a for a in actor_list if "network" in a.get("name", "").lower()
                         or "replicated" in a.get("name", "").lower()]

        # Check for multiplayer goal
        if goal and any(kw in goal.lower() for kw in ["multiplayer", "network", "online", "co-op", "dedicated"]):
            net_info = NETWORKING_SYSTEM.get("replication", {})
            reasoning.append("Multiplayer goal detected — ensure proper replication setup")
            issues.append("Multiplayer scene — verify replication settings on all gameplay-critical actors")
            actions.append({"skill": "query_expert_knowledge", "args": {"query": "networking multiplayer replication setup"}})
            suggestions.append("Pattern: Set bReplicates=True on server-authoritative actors. Use RPCs for client→server calls. Use OnRep_ for client-side property sync.")

        if player_starts and len(player_starts) > 1:
            reasoning.append(f"Found {len(player_starts)} PlayerStarts — verify multiplayer spawn setup")
            suggestions.append("For multiplayer: use PlayerStart for each team. Implement ChoosePlayerStart() in GameMode for spawn logic. Consider online subsystem for session management.")

        return {"issues": issues, "actions": actions, "reasoning": reasoning, "suggestions": suggestions}

    def analyze_optimization_needs(self, scene_data: dict, goal: str = None) -> dict:
        """Deep optimization analysis using expert knowledge from Docs 86-90."""
        issues = []
        actions = []
        reasoning = []
        suggestions = []

        total = scene_data.get("total_actors", 0)
        lights = scene_data.get("lights", 0)
        meshes = scene_data.get("meshes", 0)
        actor_list = scene_data.get("actors", [])
        type_breakdown = scene_data.get("type_breakdown", {})

        # Dynamic lights check (Lumen performance)
        dynamic_lights = [a for a in actor_list if "light" in a.get("type", "").lower()
                         and a.get("mobility", "").lower() == "movable"]
        if len(dynamic_lights) > 5:
            perf_60 = get_optimization_profile(60)
            reasoning.append(f"{len(dynamic_lights)} dynamic lights detected — Lumen shadow tracing cost increases significantly")
            issues.append(f"High dynamic light count ({len(dynamic_lights)}) — Lumen shadow tracing will be expensive")
            suggestions.append(f"At 60fps target, Lumen budget is ~4ms. Use Stationary lights where possible. Limit dynamic shadows to key lights only.")

        # Large scene optimization
        if total > 1000:
            perf_30 = get_optimization_profile(30)
            reasoning.append(f"Very large scene ({total} actors) — consider level streaming and HLOD")
            issues.append("Scene exceeds 1000 actors — performance-critical scenario")
            actions.append({"skill": "optimize_scene", "args": {"target_fps": 60}})
            suggestions.append("Use World Partition for large worlds. Enable HLOD for distant meshes. Use Nanite for static meshes. Use Virtual Texturing for large textures.")

        # Nanite check for static meshes
        static_meshes = [a for a in actor_list if "staticmesh" in a.get("type", "").lower()]
        if len(static_meshes) > 50:
            nanite_info = OPTIMIZATION_SYSTEM.get("nanite_technical", {})
            reasoning.append(f"{len(static_meshes)} static meshes — verify Nanite is enabled on source meshes")
            suggestions.append("Nanite auto-enables on imported meshes with 'Use Nanite' checked. Check with 'Nanite Visualization' in viewport. Use Fallback Mesh for non-Nanite platforms.")

        # Scalability recommendations
        if total > 500:
            scalability = OPTIMIZATION_SYSTEM.get("scalability", {})
            reasoning.append("Use scalability groups to test across hardware tiers")
            suggestions.append("Test at scalability levels: Low/Medium/High/Epic/Cinematic. Key groups: sg.ShadowQuality, sg.LumenQuality, sg.EffectsQuality, sg.TextureQuality")

        return {"issues": issues, "actions": actions, "reasoning": reasoning, "suggestions": suggestions}

    def analyze_cinematics_needs(self, scene_data: dict, goal: str = None) -> dict:
        """Analyze cinematics/Sequencer needs based on scene content and goal."""
        issues = []
        actions = []
        reasoning = []
        suggestions = []

        actor_list = scene_data.get("actors", [])

        # Detect cinematic-related actors
        camera_actors = [a for a in actor_list if "camera" in a.get("type", "").lower()]
        sequencer_actors = [a for a in actor_list if "sequence" in a.get("type", "").lower()
                           or "levelsequence" in a.get("name", "").lower()]

        # Goal-based cinematic recommendations
        if goal and any(kw in goal.lower() for kw in ["cinematic", "cutscene", "sequence", "animation", "movie"]):
            cine_info = CINEMATICS_SYSTEM.get("sequencer", {})
            reasoning.append("Cinematic goal detected — recommend Sequencer-based workflow")
            issues.append("Cinematic scene — set up Level Sequence with camera tracks")
            actions.append({"skill": "setup_cinematic", "args": {"sequence_type": "level_sequence"}})
            suggestions.append("Pattern: Create Level Sequence → Add Camera Track → Keyframe transforms → Add Animation Tracks for characters → Use Movie Render Queue for final output")

        # Camera setup recommendations
        if camera_actors:
            reasoning.append(f"Found {len(camera_actors)} camera(s) — consider CineCameraActor for cinematic shots")
            suggestions.append("CineCameraActor provides film-industry controls: focal length, sensor size, aperture (f-stop), focus distance. Use with Camera Animation Sequence for shake.")

        # Sequencer best practices
        if sequencer_actors:
            mrq = CINEMATICS_SYSTEM.get("movie_render_queue", {})
            reasoning.append("For final-quality renders, use Movie Render Queue instead of Play-in-Editor capture")
            suggestions.append("MRQ settings: Use .exr for compositing, .png for web. Enable Anti-Aliasing (Temporal). Use Custom Render Passes for separate layers.")

        return {"issues": issues, "actions": actions, "reasoning": reasoning, "suggestions": suggestions}

    def get_expert_scene_analysis(self, scene_data: dict, goal: str = None) -> dict:
        """Run all expert analyses (Docs 61-100) and merge results."""
        all_issues = []
        all_actions = []
        all_reasoning = []
        all_suggestions = []

        analyses = {
            "niagara": self.analyze_niagara_needs(scene_data, goal),
            "audio": self.analyze_audio_needs(scene_data, goal),
            "ui": self.analyze_ui_needs(scene_data, goal),
            "ai": self.analyze_ai_needs(scene_data, goal),
            "networking": self.analyze_networking_needs(scene_data, goal),
            "optimization": self.analyze_optimization_needs(scene_data, goal),
            "cinematics": self.analyze_cinematics_needs(scene_data, goal),
        }

        for name, result in analyses.items():
            all_issues.extend(result.get("issues", []))
            all_actions.extend(result.get("actions", []))
            all_reasoning.extend(result.get("reasoning", []))
            all_suggestions.extend(result.get("suggestions", []))

        return {
            "analyses": analyses,
            "issues": all_issues,
            "actions": all_actions,
            "reasoning": all_reasoning,
            "suggestions": all_suggestions,
        }

    def query_expert_knowledge(self, query: str) -> dict:
        """Search the expert knowledge base (Docs 61-100)."""
        results = search_expert_knowledge(query)
        return {
            "query": query,
            "results": results,
            "total_found": len(results),
        }

    def get_fps_optimization_profile(self, target_fps: int) -> dict:
        """Get optimization settings for a target FPS."""
        profile = get_optimization_profile(target_fps)
        return {
            "target_fps": target_fps,
            "profile": profile,
            "optimization_system": OPTIMIZATION_SYSTEM.get("lumen_performance", {}),
        }

    def get_multiplayer_pattern(self, pattern_name: str) -> dict:
        """Get common networking/multiplayer implementation patterns."""
        pattern = get_networking_pattern(pattern_name)
        return {
            "pattern_name": pattern_name,
            "pattern": pattern,
            "networking_overview": NETWORKING_SYSTEM.get("replication", {}),
        }

    # =============================================================================
    # MASTER KNOWLEDGE ANALYSIS (Docs 101-151)
    # =============================================================================

    def analyze_editor_scripting_needs(self, scene_data: dict) -> dict:
        """Analyze scene for editor scripting and automation opportunities."""
        from sn_ue5_knowledge_master import EDITOR_SCRIPTING
        
        issues = []
        suggestions = []
        
        # Check for repetitive tasks that could be automated
        total_actors = scene_data.get("total_actors", 0)
        if total_actors > 50:
            suggestions.append("Consider Editor Utility Widgets for batch operations")
            suggestions.append("Use Python scripting for bulk actor modifications")
        
        # Check for naming patterns that suggest manual work
        actors = scene_data.get("actors", [])
        duplicate_names = len([a for a in actors if "Duplicate" in a.get("name", "")])
        if duplicate_names > 5:
            issues.append(f"Found {duplicate_names} actors with 'Duplicate' in name - use Python for cloning")
            suggestions.append("Create Python script for intelligent actor duplication with renaming")
        
        return {
            "category": "editor_scripting",
            "issues": issues,
            "suggestions": suggestions,
            "knowledge": EDITOR_SCRIPTING,
        }

    def analyze_virtual_production_needs(self, scene_data: dict) -> dict:
        """Analyze scene for virtual production requirements."""
        from sn_ue5_knowledge_master import VIRTUAL_PRODUCTION
        
        issues = []
        suggestions = []
        
        # Check for camera and lighting setup
        actors = scene_data.get("actors", [])
        has_cine_camera = any("CineCamera" in a.get("class", "") for a in actors)
        has_lighting = scene_data.get("lights", 0) > 0
        
        if not has_cine_camera:
            suggestions.append("Add CineCameraActor for virtual production camera tracking")
        
        if not has_lighting:
            suggestions.append("Set up proper lighting for ICVFX compositing")
        
        # Check for green screen elements
        has_green_screen = any("Green" in a.get("name", "") or "Screen" in a.get("name", "") for a in actors)
        if has_green_screen:
            suggestions.append("Configure ICVFX settings for green screen compositing")
            suggestions.append("Set up Light Card actors for virtual lighting")
        
        return {
            "category": "virtual_production",
            "issues": issues,
            "suggestions": suggestions,
            "knowledge": VIRTUAL_PRODUCTION,
        }

    def analyze_quixel_landscape_needs(self, scene_data: dict) -> dict:
        """Analyze scene for Quixel and landscape optimization."""
        from sn_ue5_knowledge_master import QUIXEL_LANDSCAPE
        
        issues = []
        suggestions = []
        
        # Check for landscape actors
        actors = scene_data.get("actors", [])
        has_landscape = any("Landscape" in a.get("class", "") for a in actors)
        
        if has_landscape:
            suggestions.append("Use Quixel Bridge for high-quality landscape materials")
            suggestions.append("Implement landscape LODs for large terrains")
            suggestions.append("Consider Runtime Virtual Texturing for landscape detail")
        else:
            suggestions.append("Add Landscape actor for outdoor environments")
        
        # Check for water
        has_water = any("Water" in a.get("class", "") or "Water" in a.get("name", "") for a in actors)
        if not has_water:
            suggestions.append("Add Water body for realistic water simulation")
        
        return {
            "category": "quixel_landscape",
            "issues": issues,
            "suggestions": suggestions,
            "knowledge": QUIXEL_LANDSCAPE,
        }

    def analyze_volumetrics_needs(self, scene_data: dict) -> dict:
        """Analyze scene for volumetric effects (clouds, fog, atmosphere)."""
        from sn_ue5_knowledge_master import VOLUMETRICS
        
        issues = []
        suggestions = []
        
        # Check for atmospheric actors
        actors = scene_data.get("actors", [])
        has_sky_atmosphere = any("SkyAtmosphere" in a.get("class", "") for a in actors)
        has_height_fog = any("HeightFog" in a.get("class", "") for a in actors)
        has_volumetric_cloud = any("VolumetricCloud" in a.get("class", "") for a in actors)
        
        if not has_sky_atmosphere:
            suggestions.append("Add SkyAtmosphere actor for realistic atmospheric scattering")
        
        if not has_height_fog:
            suggestions.append("Add ExponentialHeightFog for depth and atmosphere")
        
        if not has_volumetric_cloud:
            suggestions.append("Add VolumetricCloud actor for dynamic cloud simulation")
        
        # Check lighting for volumetrics
        lights = scene_data.get("lights", 0)
        if lights > 0:
            suggestions.append("Configure lights for volumetric scattering")
        
        return {
            "category": "volumetrics",
            "issues": issues,
            "suggestions": suggestions,
            "knowledge": VOLUMETRICS,
        }

    def analyze_rendering_master_needs(self, scene_data: dict) -> dict:
        """Analyze scene for advanced rendering techniques."""
        from sn_ue5_knowledge_master import RENDERING_MASTER
        
        issues = []
        suggestions = []
        
        # Check for reflection setup
        actors = scene_data.get("actors", [])
        has_planar_reflection = any("PlanarReflection" in a.get("class", "") for a in actors)
        has_sky = any("Sky" in a.get("class", "") or "SkySphere" in a.get("name", "") for a in actors)
        
        if not has_sky:
            suggestions.append("Add Sky actor for proper reflections and lighting")
        
        # Check for post-processing
        has_post_process = any("PostProcess" in a.get("class", "") for a in actors)
        if not has_post_process:
            suggestions.append("Add PostProcessVolume for SSR, SSAO, and other effects")
        
        # Check for decals
        has_decals = any("Decal" in a.get("class", "") for a in actors)
        if not has_decals:
            suggestions.append("Use Decal actors for surface detail and weathering")
        
        # Check for distance fields
        total_meshes = scene_data.get("meshes", 0)
        if total_meshes > 20:
            suggestions.append("Enable Mesh Distance Fields for soft shadows and AO")
        
        return {
            "category": "rendering_master",
            "issues": issues,
            "suggestions": suggestions,
            "knowledge": RENDERING_MASTER,
        }

    def analyze_groom_vt_needs(self, scene_data: dict) -> dict:
        """Analyze scene for groom (hair) and virtual texturing needs."""
        from sn_ue5_knowledge_master import GROOM_VT
        
        issues = []
        suggestions = []
        
        # Check for groom/hair
        actors = scene_data.get("actors", [])
        has_groom = any("Groom" in a.get("class", "") or "Hair" in a.get("name", "") for a in actors)
        
        if not has_groom:
            suggestions.append("Use Groom system for realistic hair and fur rendering")
        
        # Check for large textures that could benefit from VT
        total_meshes = scene_data.get("meshes", 0)
        if total_meshes > 30:
            suggestions.append("Consider Runtime Virtual Texturing for large texture sets")
            suggestions.append("Use Virtual Texturing for landscape and terrain materials")
        
        return {
            "category": "groom_vt",
            "issues": issues,
            "suggestions": suggestions,
            "knowledge": GROOM_VT,
        }

    def analyze_performance_tools_needs(self, scene_data: dict) -> dict:
        """Analyze scene for performance optimization tools."""
        from sn_ue5_knowledge_master import PERFORMANCE_TOOLS
        
        issues = []
        suggestions = []
        
        total_actors = scene_data.get("total_actors", 0)
        total_meshes = scene_data.get("meshes", 0)
        
        # HLOD recommendations
        if total_meshes > 50:
            issues.append(f"High mesh count ({total_meshes}) - consider HLOD")
            suggestions.append("Set up Hierarchical Level of Detail (HLOD) for distant objects")
        
        # Replication Graph for multiplayer
        if total_actors > 100:
            suggestions.append("Use Replication Graph for efficient network replication")
        
        # Profiling
        suggestions.append("Use Session Frontend and Stat commands for profiling")
        suggestions.append("Enable Network Profiler for multiplayer optimization")
        
        return {
            "category": "performance_tools",
            "issues": issues,
            "suggestions": suggestions,
            "knowledge": PERFORMANCE_TOOLS,
        }

    def analyze_content_creation_needs(self, scene_data: dict) -> dict:
        """Analyze scene for content creation tools and workflows."""
        from sn_ue5_knowledge_master import CONTENT_CREATION
        
        issues = []
        suggestions = []
        
        # Shader development
        suggestions.append("Use Material Editor for shader creation")
        suggestions.append("Consider custom shaders for special effects")
        
        # Texture optimization
        total_meshes = scene_data.get("meshes", 0)
        if total_meshes > 20:
            suggestions.append("Optimize texture sizes and formats")
            suggestions.append("Use texture streaming for memory management")
        
        # Console commands
        suggestions.append("Use console commands for quick testing and debugging")
        
        return {
            "category": "content_creation",
            "issues": issues,
            "suggestions": suggestions,
            "knowledge": CONTENT_CREATION,
        }

    def analyze_physics_advanced_needs(self, scene_data: dict) -> dict:
        """Analyze scene for advanced physics simulation."""
        from sn_ue5_knowledge_master import PHYSICS_ADVANCED
        
        issues = []
        suggestions = []
        
        # Check for physics actors
        actors = scene_data.get("actors", [])
        has_physics = any("Physics" in a.get("name", "") for a in actors)
        
        if not has_physics:
            suggestions.append("Add Physics Constraint actors for realistic joint physics")
        
        # Vehicle physics
        has_vehicle = any("Vehicle" in a.get("class", "") or "Car" in a.get("name", "") for a in actors)
        if has_vehicle:
            suggestions.append("Use Chaos Vehicle system for realistic vehicle physics")
        else:
            suggestions.append("Consider Chaos Vehicles for vehicle simulation")
        
        return {
            "category": "physics_advanced",
            "issues": issues,
            "suggestions": suggestions,
            "knowledge": PHYSICS_ADVANCED,
        }

    def analyze_source_control_needs(self, scene_data: dict) -> dict:
        """Analyze project for source control and pipeline needs."""
        from sn_ue5_knowledge_master import SOURCE_CONTROL
        
        issues = []
        suggestions = []
        
        # Source control recommendations
        suggestions.append("Set up Perforce or Git for version control")
        suggestions.append("Use proper branching strategy for team collaboration")
        
        # Console development
        suggestions.append("Configure console SDKs for target platforms")
        suggestions.append("Test on console hardware early in development")
        
        return {
            "category": "source_control",
            "issues": issues,
            "suggestions": suggestions,
            "knowledge": SOURCE_CONTROL,
        }

    def analyze_api_pipeline_needs(self, scene_data: dict) -> dict:
        """Analyze project for API and pipeline needs."""
        from sn_ue5_knowledge_master import API_PIPELINE
        
        issues = []
        suggestions = []
        
        # C++ API
        suggestions.append("Use C++ API for performance-critical systems")
        suggestions.append("Expose C++ functions to Blueprints for flexibility")
        
        # Asset pipeline
        suggestions.append("Automate asset import/export with Python scripts")
        suggestions.append("Use Datasmith for CAD data import")
        
        return {
            "category": "api_pipeline",
            "issues": issues,
            "suggestions": suggestions,
            "knowledge": API_PIPELINE,
        }

    def analyze_production_needs(self, scene_data: dict) -> dict:
        """Analyze project for production and optimization needs."""
        from sn_ue5_knowledge_master import PRODUCTION
        
        issues = []
        suggestions = []
        
        # Profiling
        suggestions.append("Use Unreal Insights for performance profiling")
        suggestions.append("Profile early and often during development")
        
        # Localization
        suggestions.append("Set up localization system for multi-language support")
        
        # Crash reporting
        suggestions.append("Enable crash reporting for production builds")
        
        # Editor extensibility
        suggestions.append("Create custom editor tools for team workflows")
        
        return {
            "category": "production",
            "issues": issues,
            "suggestions": suggestions,
            "knowledge": PRODUCTION,
        }

    def get_master_scene_analysis(self, scene_data: dict) -> dict:
        """Run all master knowledge analyses on the scene."""
        analyses = {
            "editor_scripting": self.analyze_editor_scripting_needs(scene_data),
            "virtual_production": self.analyze_virtual_production_needs(scene_data),
            "quixel_landscape": self.analyze_quixel_landscape_needs(scene_data),
            "volumetrics": self.analyze_volumetrics_needs(scene_data),
            "rendering_master": self.analyze_rendering_master_needs(scene_data),
            "groom_vt": self.analyze_groom_vt_needs(scene_data),
            "performance_tools": self.analyze_performance_tools_needs(scene_data),
            "content_creation": self.analyze_content_creation_needs(scene_data),
            "physics_advanced": self.analyze_physics_advanced_needs(scene_data),
            "source_control": self.analyze_source_control_needs(scene_data),
            "api_pipeline": self.analyze_api_pipeline_needs(scene_data),
            "production": self.analyze_production_needs(scene_data),
        }
        
        # Aggregate all issues and suggestions
        all_issues = []
        all_suggestions = []
        for category, analysis in analyses.items():
            all_issues.extend([f"[{category}] {issue}" for issue in analysis.get("issues", [])])
            all_suggestions.extend([f"[{category}] {sugg}" for sugg in analysis.get("suggestions", [])])
        
        return {
            "analyses": analyses,
            "total_issues": len(all_issues),
            "total_suggestions": len(all_suggestions),
            "all_issues": all_issues,
            "all_suggestions": all_suggestions,
        }

    def query_master_knowledge(self, query: str) -> dict:
        """Search the master knowledge base (Docs 101-151)."""
        results = search_master_knowledge(query)
        return {
            "query": query,
            "results": results,
            "total_found": len(results),
        }

    def get_landscape_preset_recommendation(self, preset_name: str) -> dict:
        """Get landscape configuration presets."""
        preset = get_landscape_preset(preset_name)
        return {
            "preset_name": preset_name,
            "preset": preset,
        }

    def get_reflection_setup_recommendation(self, scenario: str) -> dict:
        """Get reflection method recommendations for a scenario."""
        rec = get_reflection_recommendation(scenario)
        return {
            "scenario": scenario,
            "recommendation": rec,
        }


# =============================================================================
# CONVENIENCE: Drop-in replacement for the old _analyze_scene_state
# =============================================================================

def analyze_scene_intelligent(scene_data: dict, goal: str = None) -> dict:
    """
    Drop-in replacement for SuperNinjaBrain._analyze_scene_state().
    Returns the same format: {summary, issues, actions} plus new fields.
    """
    brain = IntelligentBrain()
    return brain.analyze_scene(scene_data, goal)


if __name__ == "__main__":
    print("=== SuperNinja Intelligent Brain ===\n")
    
    # Test with a sample scene
    test_scene = {
        "total_actors": 58,
        "lights": 1,
        "meshes": 42,
        "type_breakdown": {
            "DirectionalLight": 1,
            "StaticMeshActor": 42,
            "PHX_Duplicate": 15,
        },
        "actors": [
            {"name": "DirectionalLight_0", "class": "DirectionalLight", "location": [0, 0, 500]},
            {"name": "PHX_Cube_01", "class": "StaticMeshActor", "location": [0, 0, 0]},
            {"name": "PHX_Cube_02", "class": "StaticMeshActor", "location": [0, 0, 0]},
        ] + [{"name": f"PHX_Mesh_{i}", "class": "StaticMeshActor", "location": [0, 0, 0]} for i in range(3, 16)]
        + [{"name": f"SM_Wall_{i}", "class": "StaticMeshActor", "location": [i*200, 0, 0]} for i in range(15)]
    }
    
    print("--- Test 1: General Analysis ---")
    brain = IntelligentBrain()
    result = brain.analyze_scene(test_scene)
    print(f"Summary: {result['summary']}")
    print(f"Issues: {len(result['issues'])}")
    for issue in result['issues']:
        print(f"  ⚠️  {issue}")
    print(f"Actions: {len(result['actions'])}")
    for action in result['actions']:
        print(f"  → {action['skill']}: {action['args']}")
    print(f"Reasoning: {len(result['reasoning'])}")
    for r in result['reasoning']:
        print(f"  💡 {r[:120]}...")
    
    print("\n--- Test 2: Film Noir Goal ---")
    result2 = brain.analyze_scene(test_scene, goal="Make it look like a film noir alley")
    print(f"Reasoning for noir goal:")
    for r in result2['reasoning']:
        if 'noir' in r.lower() or 'noir' in r.lower():
            print(f"  🎬 {r[:150]}...")
    
    print("\n--- Test 3: Knowledge Query ---")
    q = brain.query_ue5_knowledge("pawn")
    print(f"Knowledge about 'pawn': found in {len(q['ue5_docs'])} categories")
    
    print("\n--- Test 4: Blueprint Pattern Suggestion ---")
    bp = brain.suggest_blueprint_pattern("I want a boss to notify all enemies when it dies")
    for rec in bp['recommendations']:
        print(f"  → {rec['method']}: {rec['why']}")
    
    print("\n--- Test 5: Concept Explanation ---")
    print(f"Actor: {brain.explain_ue5_concept('actor')}")
    print(f"Construction script: {brain.explain_ue5_concept('construction_script')}")