# Proposal: Mechanics recipe block shape (Vending / Homeless / Day Labor / Copper)

**Status:** proposal only  
**Explicit:** no production code — proposal only

## Context

ForgePlay meta NEED: “Mechanics recipe block in GameSpec”. Only Meter Drive-By is playable; other hustles are enum/roadmap. A shared recipe envelope lets generators emit structured intent without implementing those sims yet. Coding agents ignore unknown hustle recipes until a runner exists.

## Proposed GameSpec fields

```ts
/** Discriminated recipe — optional; MD-B playables may omit and use feelOverrides + courseOverrides. */
recipe?: {
  hustle: "meterDriveBy" | "vending" | "homeless" | "dayLabor" | "copper";

  /** Shared timer / win-fail envelope (all hustles). */
  run?: {
    timeLimitSec?: number;     // default per hustle below; range 45–240
    winCondition?: "dock" | "escape" | "redeemQuota" | "shiftComplete" | "extract";
    failCondition?: "wreck" | "caught" | "timeout" | "injury" | "electrocute";
    retryAllowed?: boolean;    // default true
  };

  /** Hustle-specific knobs — only fields for `hustle` are read. */
  vending?: {
    pryHoldSec?: number;       // default 1.4, range 0.8–2.5
    noiseGain?: number;        // default 1.0, range 0.5–1.5 — stealth meter fill rate
    escapeWindowSec?: number;  // default 25, range 15–45
    carrySlots?: number;       // default 3, range 2–6
    spillMagnetRadius?: number;// default 2.0, range 1.2–3.5
  };

  homeless?: {
    diveHoldSec?: number;      // default 1.6, range 0.9–2.8
    staminaDrain?: number;     // default 0.35, range 0.15–0.55 (push fatigue /s normalized)
    staminaRecover?: number;   // default 0.22, range 0.1–0.4
    redeemQuota?: number;      // default 8, range 4–16 bottles/cans
    nightPressure?: number;    // default 0.4, range 0–1 — maps later to dusk/AI
  };

  dayLabor?: {
    shiftSec?: number;         // default 90, range 60–180
    carrySlowMult?: number;    // default 0.65, range 0.45–0.85 (walk speed when loaded)
    placeSnapRadius?: number;  // default 1.2, range 0.8–2.0
    hazardChance?: number;     // default 0.25, range 0–0.5
    fatigueDrain?: number;     // default 0.3, range 0.15–0.5
  };

  copper?: {
    snipHoldSec?: number;      // default 1.1, range 0.6–2.0
    sparkStunSec?: number;     // default 1.2, range 0.5–2.5
    coilSlowMult?: number;     // default 0.7, range 0.5–0.9
    detectRadius?: number;     // default 6, range 3–12
    flashlightConeDeg?: number;// default 40, range 25–60
  };
}
```

**MD-B note:** when `hustle === "meterDriveBy"`, prefer existing `courseOverrides` + `env` + proposed `feelOverrides`; do not duplicate density/friction here.

**Suggested hustle defaults for `run.timeLimitSec`:** vending 75 · homeless 120 · dayLabor 90 · copper 100 · meterDriveBy omit (course length driven).

## MECHANICS_MASTER_LIST rows unlocked

| Row | Hustle |
|-----|--------|
| Mechanics recipe block in GameSpec | ForgePlay meta NEED |
| Interact / hold-to-pry vending; Escape timer; Carry capacity | Vending NEED |
| Scavenge interact; Fatigue; Redeemables; Night cycle pressure | Homeless NEED |
| Place/stack; Job checklist / shift timer; Fatigue; Site hazard | Day Labor NEED |
| Snip/cut interact; Spark hazard; Carry coil weight; Detection | Copper NEED |
| Win / fail / retry loop | Shared PARTIAL — `run` generalizes |

Does **not** implement locomotion/hit modules (see sibling proposal); only recipe knobs.

## ASSET rows Agent B should prioritize

When a recipe targets a hustle, Agent B priority order:

| Hustle | Priority assets |
|--------|-----------------|
| Vending | Vending machine, Crowbar, Snack/can pickups, Security cam, Spill VFX + chime SFX, Store aisle kit |
| Homeless | Bottle/can redeemables, Blanket/clothes piles, Tent/cardboard, Cart tarp, Alley SFX, Dumpster dive contents |
| Day Labor | Hammer/shovel/tool belt, Lumber/pallet/drywall, Cone/sawhorse/tape, Truck/van, Construction SFX, Hard hat |
| Copper | Copper coil/pipe, Snips/pliers, Junction box, Flashlight + spark VFX, Buzz/spark SFX, Abandoned interior kit |

Shared: Hustle thumbnails ×5, Win/fail stingers.

## Compatibility vs existing knobs

| Existing | Interaction |
|----------|-------------|
| `softDensity` / `meterSpacingMult` / `forceGuard` / `trapChance` | MD-B only; ignore when `hustle !== "meterDriveBy"` |
| `duskBias` / `rainBias` / `frictionScale` | Reusable world env for any hustle; `homeless.nightPressure` may **bias** dusk later but must not replace `env.duskBias` |
| `melee` | MD-B loadout; vending/dayLabor tools use recipe + future interact module, not `melee` enum |

Recipe is additive optional; parsers should strip/ignore unknown hustle keys safely.

## Explicit

**no production code — proposal only**
