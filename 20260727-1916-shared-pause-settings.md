# Shared — Pause / Settings

## Exact MECHANICS_MASTER_LIST row

> Hustle: Shared systems (all hustles)  
> Mechanic: `Pause / settings`  
> Current row: `| Pause / settings | NEED | |`

## Status proposal

`HAVE-candidate` — this note supplies a portable fixed-step pause contract, browser lifecycle behavior, and bounded GameSpec knobs. It is not true `HAVE` until implemented and tested.

## Sources

- MDN, Page Visibility API: https://developer.mozilla.org/en-US/docs/Web/API/Page_Visibility_API
- MDN, `AudioContext.suspend()`: https://developer.mozilla.org/en-US/docs/Web/API/AudioContext/suspend
- W3C WAI, WCAG 2.2 SC 2.2.1 Timing Adjustable: https://www.w3.org/WAI/WCAG22/Understanding/timing-adjustable.html
- Local skill: `C:\Users\steve\Desktop\GAME SKILLS\2026-07-27_audio-realtime-mixer-spatial-streaming.md`

## Apply note

1. Add a shared `runState` outside hustle simulation state: `running`, `paused`, `won`, or `failed`.
2. While paused, stop consuming fixed simulation ticks; continue rendering the last interpolated pose and pause-menu UI.
3. Clear the real-time accumulator on resume so hidden-tab time never produces a catch-up burst.
4. Keep deterministic tick count, RNG, score timer, AI, hazards, and input-edge consumption frozen.
5. Treat `visibilitychange` or focus loss as an auto-pause request in solo play, never an implicit auto-resume.
6. Snapshot pressed controls on pause and require fresh edges after resume to prevent stuck movement or attacks.
7. Duck or suspend game audio while paused, then restore buses with a short gain ramp after user resume.
8. Put pause policy and settings defaults in shared GameSpec; individual hustles may only override declared fields.

## Proposed knobs only

- `pauseEnabled`: `false | true`
- `autoPauseOnHidden`: `false | true`
- `autoPauseOnFocusLoss`: `false | true`
- `resumeInputGuardMs`: `0–500`
- `pauseAudioGain`: `0–0.25`
- `pauseAudioRampMs`: `0–500`
- `allowTimerWhilePaused`: `false | true`
- `allowCameraWhilePaused`: `false | true`

## Dependencies

- Agent B: pause-open, pause-close, confirm, and cancel UI SFX; optional neutral pause backdrop.
- Agent C: `shared.pause` GameSpec block containing every proposed knob.
- Coding agent: shared run-state gate, accumulator reset, input-edge flush, visibility listener, and audio suspend/duck adapter.
- QA: hidden-tab, focus-loss, held-key, gamepad disconnect, win/fail, and repeated pause/resume fixtures.
