# Proposal: Deterministic quality-gate fields for coding agents

**Status:** proposal only  
**Explicit:** no production code — proposal only

## Context

ForgePlay meta: Quality-gate checklist for generated feel is PARTIAL. Coding agents (and `meter-driveby-quality-gate` skill) need **boolean / numeric assertions** they can check without human taste. Fields declare the contract a generated GameSpec claims to meet; CI/smoke fails if claims are true but runtime violates them.

## Proposed GameSpec fields

```ts
qualityGate?: {
  /** Schema / structure */
  requireSeed?: boolean;              // default true — seed non-empty
  requireFixedStepHz?: number;        // default 60, allowed 30|60 only
  maxCourseLength?: number;           // default 240, range 120–300 — vs tuning course.length * mults
  minCorridorHalf?: number;           // default 6.5, range 5–10

  /** Arcade-safe bounds (must hold after merge with tuning + overrides) */
  vmaxMax?: number;                   // default 12, range 8–14
  healthMaxRange?: [number, number];  // default [60, 140]
  softDensityRange?: [number, number];// default [0.4, 2.2] — mirrors CourseOverridesSchema
  frictionScaleRange?: [number, number]; // default [0.5, 1.5]

  /** Deterministic smoke claims */
  checksumReplay?: boolean;           // default true for MD-B — same seed+input → same checksum
  noNaNState?: boolean;               // default true
  dockReachable?: boolean;            // default true — course length / corridor admit a win path
  guardOnlyAfterActFrac?: number;     // default 0.55, range 0.4–0.75 — if forceGuard

  /** Presentation / a11y claims */
  reduceMotionHonored?: boolean;      // if systems.a11y.reduceMotion, shake ≤ threshold
  audioBusesDeclared?: boolean;       // if systems.audio present, buses booleans consistent

  /** ForgePlay generation hygiene */
  themeTagsMax?: number;              // default 8
  titleMaxLen?: number;               // default 48
  blurbMaxLen?: number;               // default 160
}
```

**Check style (for Agent D / coding agents — not implemented here):**

1. Parse GameSpec with Zod ranges.  
2. Merge overrides into effective tuning.  
3. Assert each `qualityGate` flag that is `true` / present.  
4. Fail smoke with field name + measured value (deterministic).

**Suggested generator default:** always emit

```json
"qualityGate": {
  "requireSeed": true,
  "requireFixedStepHz": 60,
  "checksumReplay": true,
  "noNaNState": true,
  "dockReachable": true
}
```

for Meter Drive-By templates.

## MECHANICS_MASTER_LIST rows unlocked

| Row | Status |
|-----|--------|
| Quality-gate checklist for generated feel | ForgePlay meta PARTIAL → field contract |
| Fixed-step sim / deterministic tick | Shared PARTIAL — `requireFixedStepHz` |
| Fixed 60 Hz sim + replay checksum | MD-B HAVE — `checksumReplay` asserts keep |
| Course density / spacing / traps | MD-B HAVE — range checks vs softDensity / trapChance |
| Prompt → GameSpec template pick | ForgePlay PARTIAL — title/blurb/tag hygiene |

## ASSET rows Agent B should prioritize

Quality gates are code/sim contracts — **no new art required**. Optional:

| Asset | Why |
|-------|-----|
| Credits / licence template (NEED) | Gate later: generated builds must ship licence rollup |
| Hustle thumbnails ×5 (NEED) | Gate: picker assets exist when recipe.hustle ≠ meterDriveBy |

## Compatibility vs existing knobs

| Existing | Interaction |
|----------|-------------|
| `softDensity` / `meterSpacingMult` | Gate ranges must **match** Zod CourseOverridesSchema (0.4–2.2 / 0.7–1.4); do not invent wider bands |
| `forceGuard` | Pair with `guardOnlyAfterActFrac` so guard does not spawn at t=0 unless Act frac met |
| `trapChance` | Optional assert `trapChance ∈ [0,1]` already in schema; no new field needed |
| `duskBias` / `rainBias` / `frictionScale` | `frictionScaleRange` mirrors WorldEnvironmentSchema; dusk/rain stay presentation unless reduceMotion gate |
| `melee` | Gate may assert melee ∈ {flamingo, sign}; nail_bat asset HAVE but not in GameSpec enum yet — do not widen enum here |

Quality gate never overrides sim values — it only **asserts** post-merge legality.

## Explicit

**no production code — proposal only**
