# ForgePlay Intel — Contracts, Seeds, Course Beats, and Gates

**Date:** 2026-07-27  
**Agent:** C (ForgePlay Intel)  
**Scope:** Prompt → GameSpec → deterministic Three.js mini-game. Small apply rules only; no AAA architecture.

## Corpus check and gap

`C:\Users\steve\Desktop\AI-INBOX` did not exist at the start of this run, so it contained no prior intel entries. The recursive `GAME-SKILLS-UNIQUE` inventory already covered the high-level ForgePlay flow, same-seed repeatability, camera damping as an allowed mechanic, environment/render separation, PMREM rebake guidance, a visual-feedback table, and a basic six-point smoke gate.

The missing value is implementation-sized policy: how to make LLM GameSpec output safe and evolvable, keep generated courses valid without heavyweight PCG, stop random-call coupling, apply camera/environment rules inside a small Three.js loop, and turn the quality checklist into reproducible automated evidence.

## Intel 1 — Make GameSpec a closed intent contract, then run semantic validation

**Priority: P0**

### Sourced facts

- OpenAI Structured Outputs with `strict: true` constrains supported model output to a supplied JSON Schema; plain JSON mode only guarantees valid JSON, not schema conformance. Structured Outputs can still return a refusal or be cut short, and schema conformity does not make the values semantically correct [1][2].
- JSON Schema supports required properties, enums, numeric/array limits, composition, and closed objects through `additionalProperties` or `unevaluatedProperties`. The `default` keyword is annotation rather than automatic mutation, and `format` may also be annotation depending on the validator [3][4].

### ForgePlay change idea

Use one versioned, closed `GameSpec` as the only LLM product. It describes bounded intent; it never contains JavaScript, shader source, arbitrary asset URLs, or executable expressions.

Minimum contract:

```text
schemaVersion
seed
mode: enum
course: { length, width, density, difficulty, beatMix }
environment: { timeOfDay, weather, visibility }
feel: { cameraLag, speedFeel, impact }
loadout: bounded enums
```

Apply three gates in order:

1. **Structural decode:** strict provider schema when available, followed by the same local JSON Schema validator regardless of provider.
2. **Semantic normalize:** clamp numeric values, reject non-finite values, verify cross-field rules, fill defaults in code, and canonicalize enum aliases.
3. **Generation admission:** estimate course/object/effect budgets before `createRun`; return a typed error or known-good template if the spec exceeds them.

Store `rawPrompt`, `rawModelOutput` only in diagnostics; runtime receives `NormalizedGameSpec { schemaVersion, specHash, seed, values }`. Migrations are pure `vN → vN+1` functions. Do not ask the LLM to repair its own malformed output in an unbounded loop: allow at most one retry with validator errors, then use a deterministic fallback.

### Why this is new

The existing ForgePlay skill names the GameSpec flow but does not define closed-schema behavior, refusal/truncation handling, local revalidation, semantic cross-field checks, migrations, or bounded fallback.

## Intel 2 — Generate a short course from gameplay beats, then validate/repair once

**Priority: P0**

### Sourced facts

- PCG research distinguishes constructive generation from search-based generation. Designer-authored constraints and graph/grammar structures can control generated sequences of player actions and their associated content [5][6].
- Two-step constructive methods separate macro layout from furnishing, which reduces the number of interacting decisions [7].

### ForgePlay change idea

Do not generate free-form world geometry and do not bring in WFC, evolutionary search, or an LLM level designer. Compile `GameSpec.course` into a small list of semantic beats, then realize them with existing pieces.

Recommended course plan:

```text
START → TEACH → PRESSURE → RECOVERY → FINALE → DOCK
```

Each beat owns a bounded longitudinal span and a tiny budget tuple:

```text
{ hazards, rewards, meters, guards, props, lanePressure }
```

Pipeline:

1. Derive a beat sequence from difficulty and length.
2. Reserve the playable aisle and start/dock clearance first.
3. Place gameplay objects per beat using its named RNG stream.
4. Furnish decoration afterward, only outside the aisle and reserved interaction envelopes.
5. Validate hard invariants.
6. Run one deterministic repair pass; if still invalid, fall back to the nearest template course.

Hard invariants should be cheap geometry checks, not agent AI:

- continuous aisle from start to dock;
- minimum clearance around rider, meters, guards, and dock;
- no prop overlap with reserved gameplay envelopes;
- finite coordinates and declared object-count caps;
- reward/hazard density within difficulty bands;
- at least one recovery span before the finale.

Record a compact `CoursePlan` before instantiating Three.js objects. Its hash is the course identity and test oracle. This is the small ForgePlay interpretation of Mythology’s separation between gameplay truth and presentation.

### Why this is new

The corpus exposes course density and tuning caps, but not a beat grammar, macro-before-furnish ordering, reserved envelopes, bounded validation/repair, or a deterministic template fallback.

## Intel 3 — Fixed-step simulation plus named random streams; rendering only interpolates

**Priority: P0**

### Sourced facts

- The fixed-step accumulator pattern advances simulation only in constant `dt` increments and carries the remainder for rendering; this prevents behavior from changing with render-frame duration. It also requires headroom or a catch-up cap to avoid a “spiral of death” [8].
- Three.js exposes deterministic `MathUtils.seededRandom`, but one shared random sequence remains vulnerable to call-order coupling [9].

### ForgePlay change idea

Use a small runtime seam:

```text
normalizeSpec → buildCoursePlan → createSim → fixedUpdate → SimSnapshot
                                                     ↓
                                            syncView(interp)
```

Apply rules:

- Pick one authoritative tick, initially `1/60 s` unless current tuning is authored for another fixed rate.
- Clamp incoming frame delta (for tab switches) and cap catch-up to 4–5 ticks. If debt remains, discard excess presentation time and emit a counter; never run an unbounded update loop.
- Keep previous/current simulation snapshots. Render `alpha = accumulator / fixedDt`; interpolate positions/orientations only. Discrete events belong to ticks, not interpolation.
- Derive named PRNG streams from `(masterSeed, subsystemTag)`: `course`, `hazards`, `rewards`, `cosmetics`, `audio`. Adding a cosmetic random call must not move a hazard.
- Never use `Math.random()` in generation or authoritative simulation. Rendering may use nondeterministic noise only when it cannot feed back into gameplay or screenshot gates.
- Add a stable state hash over a quantized gameplay snapshot every N ticks. The hash excludes Three.js object IDs, particles, camera, real time, and GPU state.

This is enough for same-seed replay and bug reproduction without networking, rollback, ECS, or cross-machine floating-point promises.

### Why this is new

The existing quality gate says “same seed → same run,” but it does not specify accumulator limits, simulation/render snapshots, random-stream isolation, forbidden entropy, or what the deterministic hash includes.

## Intel 4 — Keep semantic environment and camera targets out of the Three.js scene graph

**Priority: P1**

### Sourced facts

- Three.js recommends `renderer.setAnimationLoop()` for the application loop. `MathUtils.damp(x, y, lambda, dt)` provides delta-time-aware, frame-rate-independent smoothing [9][10].
- `EffectComposer` owns an ordered post-processing chain and final screen output; its render targets and passes have explicit resize/disposal responsibilities [11].

### ForgePlay change idea

Keep three small records:

```text
SimSnapshot       // cart, hazards, rewards, score, authoritative environment tags
PresentationState // interpolated transforms, camera rig, one-shot visual tokens
RenderResources   // scene objects, materials, composer, PMREM, textures
```

Apply Mythology ideas as local rules:

- **Environment ≠ render:** simulation publishes tags/scalars such as `weather=rain`, `visibility=0.7`, `surfaceGrip=0.8`. A presentation mapper chooses sky, fog, wetness, exposure, bloom, rain particles, and PMREM. Gameplay never reads fog density, luminance, bloom, or scene background.
- **Camera damping:** compute an unsmoothed target from the interpolated cart, then use `MathUtils.damp` per position component and a delta-aware quaternion interpolation policy. Do not use constant-per-frame lerp factors.
- **Discontinuities:** respawn, course regeneration, teleport, and camera-mode switch set a `presentationReset` flag that snaps camera/history instead of slowly crossing the map.
- **One composer:** configure a single bounded post chain. Juice events toggle parameters/spawn pooled effects; they do not add/remove passes during play.
- **Lifecycle:** a new generated run disposes old geometries, materials, textures, and composer targets before publishing the replacement scene.

No custom render graph, ECS extraction, or GPU-driven pipeline is needed.

### Why this is new

The current skills say to damp the camera and keep an environment bake sky separate, but they do not define the three-record boundary, reset behavior, fixed target/interpolated source order, one-composer rule, or generated-run disposal boundary.

## Intel 5 — Turn “juice” and quality into deterministic, budgeted evidence

**Priority: P1 now; P2 for prompt-diversity evaluation**

### Sourced facts

- Playwright can control `Date`, timers, `requestAnimationFrame`, `performance`, and event timestamps, and can compare screenshots with `toHaveScreenshot()` [12][13].
- fast-check uses seeded generators so failing property-based cases can be repeated [14].
- Three.js renderer information exposes per-frame draw calls/triangles and resource/memory counters suitable for coarse regression limits [10][15].

### ForgePlay change idea

Convert simulation events into stable presentation tokens:

```text
{ runId, tick, sequence, kind, intensity, worldPos }
```

The renderer deduplicates token IDs and applies an importance budget. A meter pop may claim camera kick + sparks + hit flash; a low-priority scrape may receive only sparks when the frame budget is full. This preserves readable juice without letting every generated object emit every effect.

Add a three-layer gate:

1. **Spec properties:** arbitrary prompts/specs normalize to finite bounded values; serialization round-trips; unsupported fields fail closed.
2. **Course/sim properties:** 100–500 seeded plans satisfy invariants; same normalized spec+seed yields identical plan and state hashes; changing only `cosmetics` does not change gameplay hashes.
3. **Browser evidence:** fixed clock and seed, scripted inputs, screenshot checkpoints at named ticks, no console errors, plus coarse `renderer.info` ceilings for draw calls, triangles, textures, and geometries.

Keep visual baselines per browser/OS environment and use a small pixel tolerance. Capture the normalized spec, seed, course-plan hash, sim hash, screenshot, and counters as one failure artifact.

**P2:** Maintain a tiny 12–20 prompt corpus by intent category. Test that paraphrases normalize to equivalent core mechanics while deliberately different prompts change at least one meaningful GameSpec field. This is more useful than asserting that two arbitrary prompts merely produce different seeds.

### Why this is new

The existing checklist is manual and boolean. It does not freeze browser time, test random GameSpecs/course invariants, distinguish gameplay versus cosmetic determinism, cap juice concurrency, retain failure artifacts, or set render-resource ceilings.

## Priority stack

### P0 — land before adding more generator vocabulary

1. Closed versioned GameSpec + local structural/semantic validation + deterministic fallback.
2. Beat-based `CoursePlan` with hard invariants, one repair pass, and template fallback.
3. Fixed-step accumulator, named RNG streams, and gameplay state hashes.

### P1 — next polish/reliability pass

1. `SimSnapshot → PresentationState → RenderResources` boundary.
2. `MathUtils.damp` camera with explicit reset events.
3. Deterministic juice tokens, Playwright clock/screenshots, property tests, and renderer budgets.

### P2 — after P0/P1 produce stable artifacts

1. Small prompt-equivalence/diversity eval corpus.
2. Per-device quality tiers derived from measured renderer counters.
3. Automated minimization of failing specs/seeds beyond fast-check’s ordinary shrinking.

## Apply next

- Add `normalizeGameSpec(raw)` returning a closed versioned spec, validation issues, `specHash`, and deterministic fallback; make `createRun` accept only that type.
- Introduce `buildCoursePlan(spec, rngStreams)` with reserved aisle/envelopes, beat budgets, invariant validation, one repair pass, and `planHash`.
- Put simulation on a capped fixed-step loop and add one Playwright test proving identical tick hashes for the same spec+seed while camera/juice render from interpolated snapshots.

## Sources

1. OpenAI, **Introducing Structured Outputs in the API** — https://openai.com/index/introducing-structured-outputs-in-the-api/
2. OpenAI API Reference, **JSON Schema response format / strict adherence** — https://platform.openai.com/docs/api-reference
3. JSON Schema, **Type-specific keywords** — https://json-schema.org/understanding-json-schema/reference/type
4. JSON Schema, **Object and unevaluated/additional properties** — https://json-schema.org/understanding-json-schema/reference/object
5. Linden, Lopes, Bidarra, **Designing Procedurally Generated Levels** (AIIDE) — https://doi.org/10.1609/aiide.v9i3.12592
6. Togelius et al., **Procedural Content Generation in Games, search-based approach** — https://www.pcgbook.com/chapter02.pdf
7. van der Linden et al., **Two-step Constructive Approaches for Dungeon Generation** — https://arxiv.org/abs/1906.04660
8. Glenn Fiedler, **Fix Your Timestep!** — https://gafferongames.com/post/fix_your_timestep/
9. Three.js, **MathUtils (`damp`, `seededRandom`)** — https://threejs.org/docs/pages/MathUtils.html
10. Three.js, **WebGLRenderer (`setAnimationLoop`, renderer information)** — https://threejs.org/docs/pages/WebGLRenderer.html
11. Three.js, **EffectComposer** — https://threejs.org/docs/pages/EffectComposer.html
12. Playwright, **Clock** — https://playwright.dev/docs/clock
13. Playwright, **Visual comparisons** — https://playwright.dev/docs/test-snapshots
14. fast-check, **What is Property-Based Testing?** — https://fast-check.dev/docs/introduction/what-is-property-based-testing/
15. Three.js, **Renderer Info metrics** — https://threejs.org/docs/pages/Info.html
