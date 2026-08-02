# Vending Heist — walk + hold-to-pry feel (portable)

## Supports

- **MECHANICS_MASTER_LIST · II Vending Heist:** `On-foot walk / strafe / sprint` — Status NEED
- **MECHANICS_MASTER_LIST · II Vending Heist:** `Interact / hold-to-pry vending` — Status NEED
- **MECHANICS_MASTER_LIST · II Vending Heist:** `Crowbar swing / hit machine` — Status NEED
- **MECHANICS_MASTER_LIST · II Vending Heist:** `Spill / loot burst + pickup magnet` — Status NEED
- **ASSET_MASTER_LIST · II Vending Heist:** `Vending machine` / `Crowbar` / `Spill VFX + chime SFX` — Status NEED
- **MECHANICS_MASTER_LIST · ForgePlay meta:** `Shared locomotion module switch (cart vs walk)` / `Shared interact / hit module` — Status NEED

## Source

- `C:\Users\steve\Desktop\EXTRA SKILS\Operation Mythology Mechanics\operation-mythology-mechanics-20260727-015215.md` (InteractionOffer, duration/hold, Started/Interrupted/Completed)
- `C:\Users\steve\Desktop\GAME SKILLS\2026-07-27_physics-character-controller-fp-tp.md` (fixed-tick kinematic walk; camera presentation-only)
- A11y hold/toggle: `operation-mythology-mechanics-20260727-022147.md`
- Shared cue bus: `1-skills\20260727-1914-shared-hit-feedback-cue-bus.md`

## Apply path (Three.js / portable arcade)

1. Walk module: fixed-step `Move` intent → accel/decel on XZ; camera soft-follow (shared damping recipe), not physics owner.
2. Focus best `InteractionOffer` (pry) by distance + facing cone; show progress radial only when offer focused.
3. Hold-to-pry: accumulate `progress` while Interact held and in range; interrupt on move beyond leash / damage / alarm.
4. A11y: Toggle-to-pry (press once to start, press/cancel to abort) + longer `holdDuration` assist knob.
5. Crowbar swing = shared melee cue pattern (MD-B `melee_swing` cousin): arc mesh + whoosh; on machine hit emit `hard_hit`-class cue + pry progress bonus **from sim**.
6. On complete: spill cue (coins/cans burst like meter coins), chime SFX hook, magnet pickups — presentation follows sim loot spawns.
7. Noise meter feel: continuous low rumble volume ∝ noise; threshold flash uses cue bus (not new authority).
8. Reuse MD-B soft vs hard collision language for aisle vs wall; escape timer = HUD + presentClock urgency pulse.

## Cross-links

- **Agent B:** vending machine, crowbar, snack/can pickups, spill VFX, chime SFX, security cam prop.
- **Agent D:** author walk + hold interact + noise/escape mechanics; emit InteractionStarted/Completed events.
- **Agent C:** `walk.speed`, `walk.sprintMult`, `pry.holdSec`, `pry.toggleAssist`, `pry.leash`, `noise.alarmThreshold`, shared `locomotion: walk`.
