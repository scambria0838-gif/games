# Meter Drive-By — lean / brake / smash combo juice

## Supports

- **MECHANICS_MASTER_LIST · I Meter Drive-By:** `Combo / streak smash bonuses` — Status NEED
- **MECHANICS_MASTER_LIST · I Meter Drive-By:** `Chase cam feel (shake, FOV, smoke, sparks)` — Status HAVE (extend, don’t rewrite)
- **MECHANICS_MASTER_LIST · I Meter Drive-By:** `Expose lean/brake/health/melee knobs in GameSpec` — Status NEED
- **MECHANICS_MASTER_LIST · I Meter Drive-By:** `Lean steer` / `Brake scrub` / `Ram meters` / `Melee swing` — Status HAVE
- **ASSET_MASTER_LIST · I Meter Drive-By:** `Tire smoke / sparks / rain VFX` — Status HAVE

## Source

- `C:\Users\steve\Desktop\skill\meter-driveby-feel\SKILL.md` (brake smoke, lean roll, meter pop hit-stop)
- Cue bus recipe: `1-skills\20260727-1914-shared-hit-feedback-cue-bus.md`
- Damage/effect stacking patterns: `EXTRA SKILS\...\operation-mythology-mechanics-20260727-015528.md` (stack refresh / aggregate — adapt as streak, not RPG buffs)
- Live: `graphics.ts` brakeGlow, lean roll, meter_pop hitStop/shake; `tuning.json` lean/brake knobs

## Apply path (Three.js / fixed-step sim)

1. **Sim owns streak:** on `meter_pop` within `comboWindowTicks`, increment `combo`; else reset. Jackpot may add bonus tier. Coins from sim only.
2. Presentation scales existing juice by combo tier: shake × (1+0.15×tier), sparks density, coin burst count, hitStop +0–2 frames (cap for a11y).
3. **Lean↔brake combo read:** if brake>threshold && |lean|>threshold while streak live → brief “drift” cue (extra tire smoke + lateral cam offset) — cosmetic, no extra score unless sim says so.
4. Melee during streak: `melee_swing` cue gets brighter swingVis / whoosh; landing a meter with melee can tag `comboStyle=melee` for HUD only.
5. HUD: streak numeral + short fire color ramp; never invent cash — display `coinsSC` + combo multiplier text from sim.
6. Fail / wreck / hard_hit: hard reset combo + red flash (existing) + sting cue.
7. GameSpec expose: `combo.windowSec`, `combo.multPerTier`, `combo.maxTier`, plus existing lean/brake FOV and smoke scales.
8. Quality: smoke-test that Reduce Motion still shows streak via HUD number alone.

## Cross-links

- **Agent B:** optional streak SFX / stinger; keep using HAVE spark/smoke textures.
- **Agent D:** implement combo as sim mechanic + events (`combo_up`, `combo_break`); near-miss tease OPTIONAL can feed same window.
- **Agent C:** move lean/brake/melee + new combo knobs from `tuning.json` into GameSpec recipe block.
