# Shared hit / impact feedback cue bus

## Supports

- **MECHANICS_MASTER_LIST · Shared systems:** `Hit / impact feedback (cam shake, flash, SFX hook)` — Status PARTIAL — “MD-B smash feel; need shared pattern”
- **MECHANICS_MASTER_LIST · Shared systems:** `Audio bus (SFX / bed / stinger)` — Status NEED (hooks only)
- **ASSET_MASTER_LIST · ForgePlay meta:** `Win / fail stingers` — Status NEED (consume same cue channels)
- **ASSET_MASTER_LIST · I Meter Drive-By:** `Tire smoke / sparks / rain VFX` — Status HAVE (presentation adapters already)

## Source

- `C:\Users\steve\Desktop\EXTRA SKILS\Operation Mythology Mechanics\operation-mythology-mechanics-20260727-185614.md` (cue-intent bus, adapters, coalesce, a11y routing)
- `C:\Users\steve\Desktop\EXTRA SKILS\Operation Mythology Mechanics\operation-mythology-mechanics-20260727-015528.md` (cues as presentation-only projections)
- Live: MD-B `SimEvent` → `graphics.ts` hitStop / shake / sparks / flash (meter_pop, hard_hit, guard_hit, wreck)

## Apply path (Three.js / shared feel)

1. Treat sim events as **semantic truth** (`meter_pop`, `hard_hit`, `guard_hit`, …). Presentation never awards coins or HP.
2. Map each event → a compact **CueIntent**: `{ type, intensity, pos, importance, coalesceKey, channels[] }`.
3. Adapters (independent): camera (shake/kick/hitStop frames), VFX (sparks/coins/smoke), HUD flash, SFX voice request, optional haptic. Any adapter may no-op.
4. **Coalesce** spam: bump/spark within N ms → max intensity, not N shakes. Jackpot / wreck = high importance, never drop.
5. Hit-stop = presentation clock pause (skip render integration N frames) **without** stopping fixed-step sim checksum — or clamp hitStop ≤ 2–3 frames if pause feels soft.
6. Accessibility router: Reduce Motion zeros shake/hitStop/FOV kick; keep color flash **or** HUD icon + SFX so hit still reads.
7. Photosafety: cap fullscreen flash opacity/duration; prefer edge vignette over full white strobes (XAG 118 spirit).
8. Extract MD-B event→feel table into a shared recipe JSON later; other hustles emit same cue types (`interact_complete`, `carry_drop`, `spark_stun`).

## Cross-links

- **Agent B:** NEED lot/alley SFX bed + win/fail stingers; spill VFX for Vending; buzz/spark SFX for Copper — wire as cue channel assets, not gameplay.
- **Agent D:** keep Soft vs hard collision emitting distinct cue intensities; shared interact/hit module should emit CueIntents.
- **Agent C:** `feel.shakeMax`, `feel.hitStopFrames`, `feel.coalesceMs`, `feel.flashMax`, `feel.reduceMotionDefault`.
