# Copper Wire — flashlight cone + spark hazard feel (portable)

## Supports

- **MECHANICS_MASTER_LIST · V Copper Wire:** `Walk / crouch / flashlight cone` — Status NEED
- **MECHANICS_MASTER_LIST · V Copper Wire:** `Spark hazard on live wire (hit/stun)` — Status NEED
- **MECHANICS_MASTER_LIST · V Copper Wire:** `Detection (buzz, light sweep)` — Status NEED
- **MECHANICS_MASTER_LIST · V Copper Wire:** `Snip / cut interact on coils` / `Carry coil weight slow` — Status NEED
- **ASSET_MASTER_LIST · V Copper Wire:** `Flashlight + spark VFX` / `Buzz / spark SFX` / `Copper coil / pipe` / `Snips / pliers` — Status NEED
- **MECHANICS_MASTER_LIST · Shared:** `Hit / impact feedback`, `Audio bus` — PARTIAL / NEED

## Source

- Shared cue bus + a11y multichannel: `EXTRA SKILS\...\operation-mythology-mechanics-20260727-185614.md`
- Walk/crouch controller: `GAME SKILLS\2026-07-27_physics-character-controller-fp-tp.md`
- Perception/detection hysteresis: `GAME SKILLS\2026-07-28_gameplay-ai-decision-perception.md`
- Carry slow reuse: `1-skills\20260727-1917-homeless-cartpush-daylabor-carry-feel.md`
- Hold interact reuse: Vending pry feel note

## Apply path (Three.js / portable arcade)

1. Flashlight = **SpotLight** (or projected cone mesh) parented to look yaw; crouch lowers light origin; battery optional later.
2. Visibility feel only: dark exterior + light cone; detection uses sim cone/LOS, not GPU light intensity.
3. Buzz detection: audio bus volume ∝ proximity to patrol/light sweep; when “seen” band entered (hysteresis), HUD chip + cam micro-shake (a11y-scaled).
4. Live-wire spark hazard: on sim stun → strong cue (`spark_stun`): white-blue flash, shake, short presentClock freeze, spark VFX burst; HP/stun from sim.
5. Snip interact: hold progress on coil node; success = cut spark cosmetic + loot coil spawn; fail tug = soft reject cue.
6. Carry coil: reuse carrySlow + heavier bob; flashlight still usable but sway exaggerated slightly.
7. Photosafety: spark flashes must respect flashMax / Reduce Motion (edge arcs > fullscreen strobe).
8. Extraction drop: dock-like pad emissive ramp (MD-B dock feel cousin) when in stash volume.

## Cross-links

- **Agent B:** flashlight+spark VFX, buzz/spark SFX, coil/pipe, snips, junction box, abandoned interior kit.
- **Agent D:** crouch + flashlight cone query, snip interact, spark stun, detection sweep AI, carry coil.
- **Agent C:** `light.coneDeg`, `light.range`, `detect.enter/exit`, `spark.stunMs`, `snip.holdSec`, `carry.coilSlowMult`.
