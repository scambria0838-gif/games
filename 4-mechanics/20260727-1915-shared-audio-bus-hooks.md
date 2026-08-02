# Shared — Audio bus (SFX / bed / stinger) hooks

## Master-list row

> **Audio bus (SFX / bed / stinger)** | Shared systems (all hustles) | was **NEED**

## Status proposal

**HAVE-candidate** — **hooks only** until Agent B lands CC0 beds/stingers. Define event → bus routing so coding can emit intents from sim events without picking a full mixer engine.

## Source

- Audio mixer domains: `C:\Users\steve\Desktop\GAME-SKILLS-UNIQUE\by-name\2026-07-27_audio-realtime-mixer-spatial-streaming.md` (buses/submixes; game emits intent, not DSP)
- Asset gaps: `ASSET_MASTER_LIST.md` — Lot / alley SFX bed NEED; Win / fail stingers NEED; Vending spill chime NEED
- MD-B today: visual sparks/smoke/shake only — no Web Audio graph

## Apply note (Three.js fixed-step / GameSpec)

1. Sim stays silent-authoritative: `stepRun` already emits events (`spark`, `guard_hit`, `guard_down`, meter ram, dock). Presentation layer maps events → `AudioIntent { bus, cueId, gain, pos? }`.
2. Three buses only for v1: `sfx` (one-shots), `bed` (loop ambience), `stinger` (win/fail/alarm). Master gain + per-bus mute.
3. Use Web Audio `GainNode` chain off one `AudioContext`; resume on first user gesture (browser autoplay policy).
4. Spatial: optional stereo pan from cart/player x vs camera; skip full HRTF. Cap concurrent sfx voices (e.g. 8) with steal-quietest.
5. Pause: set `bed` gain → 0 (or duck 12 dB); freeze one-shot scheduling; do not stop context if resume must be instant.
6. Reduce-motion does **not** mute audio; separate `muteSfx` / `muteBed` settings.
7. GameSpec: `audio.bedId`, `audio.stingerWinId`, `audio.stingerFailId` string refs (resolve to `/public/audio/...` later). Missing assets = no-op hook (log once).
8. Cross-link Agent B: prioritize lot bed + win/fail stingers + meter clang / pry scrape / alarm sting.

## Proposed knobs

| Knob | Range | Notes |
|------|-------|-------|
| `masterGain` | 0–1 | |
| `sfxGain` | 0–1 | |
| `bedGain` | 0–1 | |
| `stingerGain` | 0–1 | |
| `maxSfxVoices` | 4–16 | default 8 |
| `bedDuckOnStingerDb` | −18–0 | momentary duck |
| `spatialPanStrength` | 0–1 | 0 = mono bus |

## Dependencies

- **Agent B:** Lot/alley bed; win/fail stingers; MD-B clang/spark; Vending pry scrape + alarm; spill chime
- **Agent C:** GameSpec `audio: { bedId?, stingerWinId?, stingerFailId?, bedGain? }`
- **Agent A:** feel events already exist — map intensity fields to gain
