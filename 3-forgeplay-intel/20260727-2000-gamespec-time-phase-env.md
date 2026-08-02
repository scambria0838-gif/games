# GameSpec — Time / phase / env fields

## Context

Homeless night pressure + shared HUD/env need deterministic time fields without a full weather sim.

## Proposed fields

```ts
time?: {
  ticksPerGameDay?: number;     // 1800–7200
  startDayFrac?: number;        // 0–1
  nightStartFrac?: number;
  nightEndFrac?: number;
}
envPresentation?: {
  followSimDayFrac?: boolean;   // default true
  wetnessFromRecipe?: number;   // 0–1 optional
}
```

Hustle recipes may reference `time` for nightNoiseMult etc. (see Agent D night note).

## Cross-links

- `4-mechanics/20260727-2000-homeless-night-cycle-pressure.md`
- `1-skills/20260727-2004-graphics-env-snapshot-three.md`
- Prior `feelOverrides` dusk bias for MD-B remains valid
