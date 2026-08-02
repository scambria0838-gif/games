# Proposal: Shared pause / a11y / audio bus GameSpec flags

**Status:** proposal only  
**Explicit:** no production code — proposal only

## Context

Shared NEED rows: Pause / settings, Accessibility, Audio bus. No GameSpec surface today — MD-B playable has no pause/a11y contract and only informal SFX hooks. Optional flags let ForgePlay declare intent; play shell implements later.

## Proposed GameSpec fields

Additive optional top-level (or nested `presentation`) block:

```ts
systems?: {
  pause?: {
    enabled?: boolean;           // default true when present; omit = implementation default
    allowRestartFromPause?: boolean; // default true
  };

  a11y?: {
    reduceMotion?: boolean;      // default false — damp cam shake / FOV punch
    colorblindHud?: boolean;     // default false — high-contrast score/timer
    holdToToggleBrake?: boolean; // default false — sticky brake for one-hand play
    // Remap is runtime UI; GameSpec only flags that remap UI must be offered:
    offerRemap?: boolean;        // default true when a11y block present
  };

  audio?: {
    // Bus presence flags + relative gains (0–1). Assets optional until HAVE.
    sfxBus?: boolean;            // default true
    bedBus?: boolean;            // default true
    stingerBus?: boolean;        // default true
    sfxGain?: number;            // default 1.0, range 0–1
    bedGain?: number;            // default 0.55, range 0–1
    stingerGain?: number;        // default 0.85, range 0–1
    muteBedWhenPaused?: boolean; // default true
  };
}
```

**Arcade-safe defaults:** if `systems` omitted entirely → no behavior change. If only `audio.bedBus: true` → shell may play silence until bed asset lands.

## MECHANICS_MASTER_LIST rows unlocked

| Row | Hustle | Status today |
|-----|--------|--------------|
| Pause / settings | Shared systems | NEED |
| Accessibility (remap, reduce motion) | Shared systems | NEED |
| Audio bus (SFX / bed / stinger) | Shared systems | NEED |
| Hit / impact feedback (cam shake, flash, SFX hook) | Shared | PARTIAL — `reduceMotion` gates shake |

## ASSET rows Agent B should prioritize

| Asset | Why |
|-------|-----|
| Lot / alley SFX bed (NEED) | `bedBus` content |
| Win / fail stingers (NEED) | `stingerBus` |
| UI font (display + HUD) (NEED) | Pause / settings / remap chrome |
| Hustle icons (×5 + ForgePlay) (NEED) | Settings / pause identity |
| Spill VFX + chime SFX (NEED) | Vending later; shared chime pattern for stingers |
| Alley SFX / Construction SFX / Buzz·spark SFX | Per-hustle beds once bus exists |

## Compatibility vs existing knobs

| Existing | Interaction |
|----------|-------------|
| `duskBias` / `rainBias` | Visual only; `reduceMotion` must **not** zero rain/dusk — only damp camera/shake presentation |
| `frictionScale` / course overrides / `melee` | Unaffected — systems block is shell/presentation |
| `forceGuard` / `trapChance` / `softDensity` | Unaffected |

Keep gains small (0–1). Do not put sim tick rate or health in this block.

## Explicit

**no production code — proposal only**
