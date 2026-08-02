# Shared — Audio Bus Hooks

## Exact MECHANICS_MASTER_LIST row

> Hustle: Shared systems (all hustles)  
> Mechanic: `Audio bus (SFX / bed / stinger)`  
> Current row: `| Audio bus (SFX / bed / stinger) | NEED | hooks only until assets |`

## Status proposal

`HAVE-candidate` — this note defines the shared routing and event hooks needed before final audio assets exist. It is not true `HAVE` until the Web Audio graph and event bindings ship.

## Sources

- MDN, Web Audio API modular routing: https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API
- MDN, `AudioNode` routing graph: https://developer.mozilla.org/en-US/docs/Web/API/AudioNode
- MDN, `GainNode`: https://developer.mozilla.org/en-US/docs/Web/API/GainNode
- MDN, `AudioContext.suspend()`: https://developer.mozilla.org/en-US/docs/Web/API/AudioContext/suspend
- Local skill: `C:\Users\steve\Desktop\GAME SKILLS\2026-07-27_audio-realtime-mixer-spatial-streaming.md`
- Asset candidate: `C:\Users\steve\Desktop\AI-INBOX\2-assets\20260727-1919-shared-lot-alley-sfx.md`

## Apply note

1. Route every voice through stable `sfx`, `bed`, `stinger`, and `ui` gain buses, then a `master` bus.
2. Simulation emits semantic audio events with tick, event ID, position, intensity, and variant seed; it never owns Web Audio nodes.
3. Presentation deduplicates event IDs under rollback and schedules the selected asset with a short gain ramp.
4. Limit repeated impact/pickup voices per category and deterministically choose replacement/drop priority.
5. Duck `bed` under `stinger` and major fail/win events; never change simulation timing to match audio.
6. Use listener-relative panning for world SFX while UI and stingers remain non-spatial.
7. On pause or hidden tab, ramp buses down or suspend the context; resume only after a user gesture when the browser requires it.
8. Allow placeholder oscillator/noise or silence for missing assets so hooks are testable before Agent B completes sourcing.

## Proposed knobs only

- `masterGain`: `0–1`
- `sfxGain`: `0–1`
- `bedGain`: `0–1`
- `stingerGain`: `0–1`
- `uiGain`: `0–1`
- `stingerDuckGain`: `0.1–1`
- `duckAttackMs`: `5–250`
- `duckReleaseMs`: `50–2000`
- `maxImpactVoices`: `2–32`
- `maxPickupVoices`: `1–16`
- `voiceStealFadeMs`: `0–100`
- `spatialRefDistance`: `0.5–20`
- `spatialMaxDistance`: `10–250`

## Dependencies

- Agent B: lot/alley bed validation; win/fail stingers; UI confirm/cancel; shared impact, pickup, alarm, and tool-hit SFX.
- Agent C: `shared.audio.buses`, `shared.audio.voiceLimits`, and event-to-cue mapping fields.
- Coding agent: Web Audio bus graph, autoplay unlock, pause/visibility handling, rollback deduplication, and voice pool.
- QA: missing assets, rapid impacts, simultaneous pickups, win/fail ducking, pause/resume, hidden tab, and AudioContext interruption.
