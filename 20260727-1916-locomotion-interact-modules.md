# Proposal: Shared locomotion + interact / hit module switches

**Status:** proposal only  
**Explicit:** no production code — proposal only

## Context

ForgePlay meta NEED rows: shared locomotion module switch (cart vs walk) and shared interact / hit module. MD-B already has cart lean + melee; on-foot hustles need a portable switch so Agent D can share walk/strafe/sprint and hold-to-interact without per-hustle forks.

## Proposed GameSpec fields

```ts
modules?: {
  locomotion?: {
    mode: "cartRide" | "walk" | "walkPushCart"; // required if modules.locomotion present
    walkSpeed?: number;       // default 3.2, range 2.2–4.5 (m/s arcade)
    sprintMult?: number;      // default 1.35, range 1.15–1.6
    strafeMult?: number;      // default 0.85, range 0.7–1.0
    crouchMult?: number;      // default 0.55, range 0.4–0.7 — copper
    cartPushMult?: number;    // default 0.75, range 0.55–0.95 — homeless walkPushCart
    turnRateDeg?: number;     // default 220, range 140–300 — on-foot yaw
  };

  interact?: {
    /** Primary use: hold interact / pry / dive / snip / place. */
    holdSec?: number;         // default 1.2, range 0.5–2.5
    reach?: number;           // default 1.8, range 1.2–2.8
    autoPickup?: boolean;     // default true for spill/loot
    magnetRadius?: number;    // default 1.6, range 0–3.5; 0 = off
  };

  hit?: {
    /** Melee / tool swing shared pattern (MD-B melee or crowbar/hammer). */
    enabled?: boolean;        // default true for MD-B / vending / dayLabor
    arcRad?: number;          // default 1.2, range 0.5–2.0
    reach?: number;           // default 2.0, range 1.4–3.0
    cooldownTicks?: number;   // default 20, range 12–30 @ 60 Hz
    damage?: number;          // default 1 “unit”; range 0.5–2.0 — hustle maps to chips/noise
  };
}
```

**Mode presets (documentation for generator):**

| Hustle | locomotion.mode | interact | hit |
|--------|-----------------|----------|-----|
| Meter Drive-By | `cartRide` | omit / off | enabled (use GameSpec `melee` + feelOverrides) |
| Vending | `walk` | pry hold | crowbar swing |
| Homeless | `walkPushCart` | dive hold | soft bump only (`hit.enabled: false`) |
| Day Labor | `walk` | place snap | tool swing |
| Copper | `walk` + crouchMult | snip hold | optional stun from spark (hazard, not player hit) |

When `locomotion.mode === "cartRide"`, walk/sprint fields ignored; MD-B tuning `vmax` / lean remain authoritative until feelOverrides land.

## MECHANICS_MASTER_LIST rows unlocked

| Row | Status |
|-----|--------|
| Shared locomotion module switch (cart vs walk) | ForgePlay meta NEED |
| Shared interact / hit module | ForgePlay meta NEED |
| On-foot walk / strafe / sprint | Vending NEED |
| Cart push (walk-coupled or ride toggle) | Homeless NEED |
| Walk + carry heavy object | Day Labor NEED |
| Walk / crouch / flashlight cone | Copper NEED (crouchMult; cone stays in recipe) |
| Crowbar swing / hit machine; Tool swing / hit | Vending / Day Labor NEED |
| Soft vs hard collision; Hit / impact feedback | Shared PARTIAL — hit module standardizes hooks |

## ASSET rows Agent B should prioritize

| Asset | Module |
|-------|--------|
| Crowbar (NEED) | hit + interact (vending) |
| Hammer / shovel / tool belt (NEED) | hit (day labor) |
| Snips / pliers (NEED) | interact (copper) |
| Cart + tarp (PARTIAL) | walkPushCart |
| Snack / can pickups; Bottle / can redeemables | interact autoPickup / magnet |
| Spill VFX + chime SFX | interact feedback |
| Flashlight + spark VFX | copper crouch / hazard (with recipe) |

MD-B cart/melee meshes already HAVE — cartRide path needs no new art.

## Compatibility vs existing knobs

| Existing | Interaction |
|----------|-------------|
| `melee` | When `cartRide` + hit enabled, `melee` id still selects flamingo/sign meshes; `modules.hit` arc/reach/cooldown are **fallbacks** if `feelOverrides` melee fields absent |
| `feelOverrides` (proposed) | Prefer feelOverrides for MD-B; modules.hit for non-MD-B tools |
| `softDensity` / `meterSpacingMult` / traps / guard | Course only; locomotion does not change density |
| `frictionScale` / rain / dusk | Env stays global; walk speed not multiplied by frictionScale unless hustle recipe says so later |
| Recipe block (proposed) | Recipe holds hustle timers/stealth; modules hold portable locomotion/interact/hit — recipe may override `interact.holdSec` when both set (recipe wins for that hustle) |

## Explicit

**no production code — proposal only**
