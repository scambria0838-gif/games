# Shared — Pause / settings

## Master-list row

> **Pause / settings** | Shared systems (all hustles) | was **NEED**

## Status proposal

**HAVE-candidate** — portable recipe for a local pause overlay + settings shell that freezes presentation clocks without rewriting the fixed-step sim. Coding agent marks true HAVE after wire-up in `apps/play` (+ ForgePlay shell).

## Source

- Game-flow / pause clock pattern: `C:\Users\steve\Desktop\GAME-SKILLS-UNIQUE\by-name\RESEARCH_INDEX__2b8b84b5.md` (game-flow state machines; platform pause ≠ game pause; explicit clock domains)
- Arcade precedent: most browser arcade (pause = Esc / P; settings = mute, reduce-motion, remap entry)
- Local HAVE grounding: MD-B has win/fail/retry but no pause gate in `apps/play/src/meter-driveby/gameplay.ts`

## Apply note (Three.js fixed-step / GameSpec)

1. Keep `FIXED_DT` sim **off** while paused: do not call `stepRun` / hustle step; accumulate no catch-up ticks.
2. Separate clocks: `simClock` (paused), `uiClock` (always runs for overlay fade), `audioClock` (duck/mute via bus).
3. Overlay is DOM/CSS on top of the WebGL canvas — no scene rebuild. Esc toggles; R still means retry only when **unpaused** and run ended.
4. Settings panel is a child of pause: mute toggles, reduce-motion, open remap (see accessibility + input-map notes). Persist to `localStorage` key `dump.play.settings.v1`.
5. Platform/tab blur: optional auto-pause (`document.visibilitychange`) — GameSpec/flag `autoPauseOnBlur: true` default for local play.
6. Do **not** use `timeScale = 0` on the renderer loop; keep `requestAnimationFrame` for overlay + optional idle bob, but skip sim steps.
7. ForgePlay: same pause shell wraps generated hustles; GameSpec needs no per-hustle pause fields beyond optional `allowPause: boolean` (default true).
8. Cross-link Agent A: pause should zero cam-shake accumulation so resume does not dump buffered shake.

## Proposed knobs

| Knob | Range | Notes |
|------|-------|-------|
| `allowPause` | bool | default true |
| `autoPauseOnBlur` | bool | default true (local) |
| `pauseFadeMs` | 80–250 | overlay in/out |
| `settingsPersistKey` | string | versioned LS key |
| `resumeInputGraceTicks` | 0–12 | ignore lean/brake edges after resume |

## Dependencies

- **Agent C:** optional GameSpec `meta.allowPause`, `meta.autoPauseOnBlur`
- **Agent B:** none required (UI chrome optional; win/fail stingers already NEED elsewhere)
- **Agent A:** feel skill — zero shake/FOV lerp on pause enter
