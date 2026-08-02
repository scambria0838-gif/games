# Graphics apply — Env snapshot → Three.js sky/post (portable)

## Supports

- Night/dusk pressure presentation; MD-B HDRI/dusk already HAVE; ForgePlay env knobs

## Source

- Gameplay env snapshot contract: `...\023037_time-weather-environment-gameplay-contract.md` (renderer adapter boundary)
- Graphics folder is mostly AAA (temporal upscaling, photometric IES, render graph) — **defer**; take adapter idea only
- Existing skills: `three-sky-env`, `polyhaven-sky-import` (project)

## Apply path (Three.js)

1. Sim publishes `{ dayFrac, wetness, visibilityClass }`. Three.js reads only.
2. Map dayFrac → HDRI intensity / envMap intensity / graded overlay; wetness → roughness boost + optional rain already in MD-B.
3. Post: bloom/vignette scales with night band; Reduce Motion disables pulse.
4. Do **not** invent new CC0 HDRI URLs here — use assets already in play or Agent B finds.

## Cross-links

- Mechanics night cycle; intel presentation-env adapter
- Asset master: Night/urban HDRI HAVE
