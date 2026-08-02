# Proposal: Clock domains + per-hustle override knobs

**Status:** proposal only — no production code

## Context

ForgePlay meta **Per-hustle override knobs** is PARTIAL. Mythology flow clocks give a portable rule: every timer names its clock; hustle overrides may scale sim timers without touching UI clocks.

## Source

- `C:\Users\steve\Documents\BACKUP\operation-mythology-mechanics-20260727-013709.md` — simulation / monotonic / presentation / session clocks; pause as schedule policy
- Cross-link: `20260727-1915-hustle-recipe-block.md`; `20260727-1913-mdb-feel-knobs.md`

## Proposed GameSpec

```ts
clocks?: {
  fixedStepHz?: 30 | 60;
  pauseFreezes: Array<'sim' | 'nightPhase' | 'shiftTimer' | 'detect'>;
};
overrides?: {
  density?: number;
  frictionScale?: number;
  timerScale?: number;      // multiplies sim timers only
  staminaDrainMult?: number;
  detectGainMult?: number;
};
```

## Apply note

1. Generator may emit per-hustle overrides; merge order = template → recipe → overrides.
2. `timerScale` must not scale UI tween durations.
3. Quality gate ranges clamp overrides after merge.

## MECHANICS_MASTER_LIST

| Row | Status |
|-----|--------|
| Per-hustle override knobs | PARTIAL → PARTIAL-candidate |

## Explicit

**no production code — proposal only**
