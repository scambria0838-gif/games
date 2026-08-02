# Shared — Accessibility / Remap / Reduce Motion

## Exact MECHANICS_MASTER_LIST row

> Hustle: Shared systems (all hustles)  
> Mechanic: `Accessibility (remap, reduce motion)`  
> Current row: `| Accessibility (remap, reduce motion) | NEED | |`

## Status proposal

`HAVE-candidate` — the note defines action-level remapping, reduced-motion behavior, timing assists, and GameSpec knobs. It remains a candidate until UI, persistence, and gameplay paths are implemented.

## Sources

- W3C, Gamepad specification and standard mapping: https://www.w3.org/TR/gamepad/
- MDN, `prefers-reduced-motion`: https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/%40media/prefers-reduced-motion
- W3C WAI, WCAG 2.2 SC 2.2.2 Pause, Stop, Hide: https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide.html
- Accessible Games Initiative, Tags and Criteria (2025): https://accessiblegames.com/wp-content/uploads/2025/03/Accessible-Games-Initiative-Tags-and-Criteria-March-2025.pdf
- Local skill: `C:\Users\steve\Desktop\GAME SKILLS\2026-07-27_platform-abstraction-capability-profiles.md`

## Apply note

1. Map physical keyboard/gamepad inputs to semantic actions such as `move`, `sprint`, `interact`, `hit`, `pause`, and `drop`.
2. Store bindings by action and context, with conflict detection, reset defaults, and keyboard-only completion for every menu.
3. Poll gamepads per render frame but latch normalized action state for each fixed simulation tick.
4. Apply dead zone, response curve, and hold/toggle policy before the hustle mechanic reads the action.
5. Seed reduced motion from `prefers-reduced-motion`, while preserving an explicit in-game override.
6. Reduced motion scales camera shake, FOV kick, bob, flashing, particles, and rapid UI transitions without changing hit timing.
7. Offer hold/toggle or hold-duration assists for sprint, crouch, pry, dive, snip, and carry interactions.
8. Persist settings outside replay/checksum state; replay records normalized actions, not device-specific button codes.

## Proposed knobs only

- `remapEnabled`: `false | true`
- `gamepadDeadZone`: `0.05–0.35`
- `gamepadResponseExp`: `1–3`
- `holdAssistMode`: `hold | toggle | autoComplete`
- `interactHoldScale`: `0.25–1`
- `reducedMotionDefault`: `system | off | on`
- `cameraShakeScale`: `0–1`
- `cameraBobScale`: `0–1`
- `fovKickScale`: `0–1`
- `flashIntensityScale`: `0–1`
- `particleDensityScale`: `0–1`
- `uiMotionScale`: `0–1`

## Dependencies

- Agent B: keyboard and standard-gamepad glyph sheet; non-flashing impact alternative; high-contrast focus/prompt states.
- Agent C: `shared.input.actions`, `shared.input.bindings`, and `shared.accessibility` GameSpec blocks.
- Coding agent: action mapper, rebind UI, persistence, conflict checks, gamepad hot-plug, and presentation-scale routing.
- QA: keyboard-only navigation, full remap, duplicate binding, dead-zone drift, device disconnect, OS reduced-motion, and replay parity.
