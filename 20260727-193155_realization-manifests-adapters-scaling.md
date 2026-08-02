# ForgePlay Intel — Realization Receipts, Run Manifests, Adapters, and Scaling

**Date:** 2026-07-27  
**Agent:** C (ForgePlay Intel)  
**Status:** Proposal only; no production code  
**Scope:** Small prompt → GameSpec → deterministic Three.js mini-game rules. No AAA ECS, render graph, networking, or general engine rewrite.

## Inventory and identified gap

This run recursively checked:

- `C:\Users\steve\Desktop\AI-INBOX`, including all five existing Agent C proposals and the shared skills/mechanics notes;
- `C:\Users\steve\Desktop\AGENT 3\3-forgeplay-intel`, including the prior contracts/seeds/course-gates report;
- `C:\Users\steve\Desktop\GAME-SKILLS-UNIQUE`.

Already covered and therefore excluded: Meter Drive-By feel overrides; pause/accessibility/audio flags; hustle recipe fields; locomotion/interact/hit switches; declared quality-gate fields; strict structural GameSpec validation; beat-based course construction; capped fixed-step simulation; named random streams; camera damping; simulation/environment versus rendering; deterministic cue budgets; Playwright/property gates.

The uncovered layer is what happens after a valid GameSpec exists: prove what the current build can actually realize, make a run reproducible across generator revisions, measure course difficulty as several axes rather than one adjective, keep each hustle behind a tiny runtime seam, and prevent generated runs from leaking resources or changing gameplay when presentation quality adapts.

## Intel 1 — Return a realization receipt; never silently ignore valid GameSpec intent

**Priority: P0**

### Sourced facts

- Semantic Versioning requires a declared public API and distinguishes incompatible, backward-compatible feature, and backward-compatible fix changes through major/minor/patch increments [1].
- JSON Schema can prove structural shape, but application-specific relationships and implementation availability still require semantic checks. A schema-valid request can ask for a recipe/module that the current build has not implemented.

### ForgePlay change idea

Add a deterministic compile phase between normalized GameSpec and run creation:

```text
NormalizedGameSpec
  → realizeSpec(spec, BuildCapabilities)
  → RealizationReceipt
  → createRun(receipt.realizedSpec)
```

Suggested receipt:

```ts
type RealizationReceipt = {
  requestedSpecHash: string;
  capabilitySetVersion: string;
  runnerId: "meterDriveBy" | "vending" | "homeless" | "dayLabor" | "copper";
  status: "realized" | "degraded" | "rejected";
  realizedSpec: NormalizedGameSpec | null;
  decisions: Array<{
    path: string;                      // e.g. recipe.vending.noiseGain
    outcome: "applied" | "clamped" | "substituted" | "omitted" | "unsupported";
    requested?: unknown;
    realized?: unknown;
    reasonCode: string;
  }>;
  requiredAssets: string[];            // catalog IDs, not URLs
  receiptHash: string;
};
```

Rules:

1. Every requested non-default field gets one decision or is covered by an explicit “applied subtree” decision.
2. Unsupported **core mechanics** reject the run. Optional presentation may degrade through a documented fallback.
3. A valid `recipe.hustle="vending"` must not open Meter Drive-By while quietly ignoring the recipe.
4. The UI shows a compact “Built / substituted / unavailable” summary before Play.
5. Coding agents add a capability only when its runner and smoke fixture exist; proposal-only fields remain unsupported.

Keep the support table finite:

```text
runner → schema range → supported modules → required assets → fallback policy
```

This is capability negotiation, not a plugin system. It prevents ForgePlay from appearing to honor an LLM request that the current mini-game cannot express.

### Why this is new

Existing Agent C notes intentionally say unimplemented hustle recipes may be ignored. A realization receipt changes that unsafe ambiguity into an inspectable apply/substitute/reject decision without changing the GameSpec schema itself.

## Intel 2 — Reproduce and share a run with a canonical RunManifest, not raw prompt state

**Priority: P0**

### Sourced facts

- RFC 8785 defines a canonical JSON representation with deterministic primitive serialization and recursively sorted object properties, making JSON reliably hashable [2].
- Web Crypto exposes SHA-256 digests in browsers and workers. A digest is an identity/integrity aid; without a secret or signing key it is not proof that content is trusted [3].
- Semantic Versioning communicates API compatibility, but a build/content hash is still needed to identify exact generator code and catalogs [1].

### ForgePlay change idea

Publish one immutable manifest after realization and course compilation:

```ts
type RunManifest = {
  manifestVersion: 1;
  normalizedSpec: NormalizedGameSpec;
  specHash: string;
  seed: string;
  generator: { apiVersion: string; buildId: string };
  capabilitySetVersion: string;
  realizationReceiptHash: string;
  coursePlanHash: string;
  assetCatalogRevision: string;
  runnerId: string;
};
```

Compute hashes from canonical JSON bytes, not ordinary object insertion order. Exclude diagnostics, timestamps, raw prompt, UI selection, localStorage keys, screenshots, and hardware quality tier from deterministic identity.

Transport policy:

- Preferred share URL: `?run=<short server/content-store id>` resolving to a manifest.
- Offline fallback: a bounded, versioned encoded manifest payload only if it is below an explicit application byte cap.
- Never place the raw prompt, model transcript, arbitrary asset URLs, or unbounded JSON in the query string.
- Anything loaded from URL/localStorage is untrusted input: parse, migrate, validate, realize again, then confirm the recomputed hashes.
- If the exact generator/content revision is unavailable, label the result “re-realized on build X” and issue a new manifest instead of claiming exact replay.

Use two user-facing actions:

- **Replay exact:** allowed only when required build/catalog compatibility is available and hashes match.
- **Remix:** migrates/re-realizes the normalized spec on the current build, intentionally producing new hashes.

### Why this is new

The current ForgePlay flow mentions `localStorage` and `?spec=` but does not define size/trust boundaries, exact-versus-remix semantics, generator/catalog identity, canonical hashing, or requested-versus-realized linkage.

## Intel 3 — Replace one “difficulty” number with a small measured course vector

**Priority: P0 for metrics; P1 for prompt mapping**

### Sourced facts

- PCG evaluation literature recommends analyzing a generator across measurable content dimensions rather than judging only a few samples. Expressivity analysis treats each quantitative property as a dimension of generated-content space [4].
- Quality-diversity research separates feasibility/quality from characteristic dimensions; different content can be playable while occupying meaningfully different regions of a metric space [5].
- This does not require ForgePlay to adopt evolutionary search or MAP-Elites. Those sources support measuring multiple content characteristics, not importing their heavy generation algorithms.

### ForgePlay change idea

Compile prompt adjectives to a bounded target vector, then measure the realized course:

```ts
type DifficultyVector = {
  pace: number;          // target speed / reaction cadence
  congestion: number;    // aisle occupancy and clearance pressure
  hazardPressure: number;// expected hazard exposure per distance
  precision: number;     // narrow timing/aim windows
  recovery: number;      // inverse pressure: safe span + reward support
}; // each canonicalized to 0..1
```

Do not let the LLM directly set dozens of low-level spawn values. Map stable prompt tags to this vector, then let the deterministic course compiler choose bounded beat budgets.

Add measured metrics to `CoursePlan`:

```text
minClearance
hazardsPer100m
medianHazardGap
longestPressureRun
recoverySpanCount
rewardToHazardRatio
estimatedReactionWindow
```

Validation rules:

1. Hard playability constraints still pass before any difficulty judgment.
2. Realized metrics must land inside a tolerance band around the target vector.
3. Generator tests compare ordered presets: `easy`, `normal`, `hard` should be monotonic on declared pressure axes across a fixed seed set, with recovery allowed to move inversely.
4. Diversity tests ensure different seeds do not merely reshuffle decorations while producing identical gameplay metrics.
5. If a target cannot be realized within caps, the receipt records the nearest realized vector; it does not secretly exceed density or clearance budgets.

Keep tuning empirical. The vector predicts content pressure, not human-perceived difficulty with scientific certainty. Later playtest data may recalibrate mappings without changing the course generator shape.

### Why this is new

The previous report defines gameplay beats and invariant checks. This item adds a measurable target-versus-realized difficulty contract, monotonic preset tests, and protection against “different seed, same oatmeal” output.

## Intel 4 — Use one tiny HustleAdapter and semantic spawn records

**Priority: P1**

### Sourced facts

- Three.js `InstancedMesh` reduces draw calls for many objects sharing geometry/material while retaining per-instance transforms [6].
- Removing an object from a Three.js scene does not release its geometries, materials, textures, render targets, controls, or passes; the application owns disposal because Three.js cannot infer lifetimes [7].

### ForgePlay change idea

Define a small shell contract, not a general engine:

```ts
interface HustleAdapter {
  readonly id: RunnerId;
  realize(spec: NormalizedGameSpec, caps: BuildCapabilities): RealizationReceipt;
  buildCourse(receipt: RealizationReceipt): CoursePlan;
  createSim(plan: CoursePlan): SimHandle;
  step(sim: SimHandle, input: InputFrame): SimEvents;
  snapshot(sim: SimHandle): SimSnapshot;
  createView(plan: CoursePlan, assets: AssetCatalog): ViewHandle;
  syncView(view: ViewHandle, snapshot: SimSnapshot, alpha: number, events: SimEvents): void;
  disposeView(view: ViewHandle): void;
}
```

The shared play shell owns input sampling, fixed-step accumulation, pause, results/retry, audio buses, accessibility policy, HUD slots, share manifest, and lifecycle. Each adapter owns only its hustle-specific sim/course mapping and Three.js view.

Course output uses semantic spawn records:

```ts
{
  stableId,
  archetypeId,       // approved catalog key
  transform,
  gameplayRole: "solid" | "soft" | "trigger" | "pickup" | "none",
  presentationRole: "hero" | "dressing" | "effectAnchor",
  tags
}
```

Apply rules:

- Gameplay collision/query data is compiled from `gameplayRole`; it never depends on whether a mesh finished loading or is currently visible.
- Dressing with `gameplayRole="none"` may be instanced, culled, reduced, or omitted by the presentation tier.
- Soft versus hard collision is a semantic course decision. A replacement mesh cannot change it.
- Stable spawn IDs derive from course-plan identity and ordinal, not Three.js UUIDs.
- Asset load failure swaps a catalog fallback mesh while preserving gameplay bounds/role.

This is the small ForgePlay form of Mythology’s gameplay/render separation.

### Why this is new

Existing module proposals describe locomotion/interact/hit fields but not the runner lifecycle, shell ownership, semantic spawn ABI, stable IDs, collision/render independence, or asset-failure behavior.

## Intel 5 — Adapt presentation quality with hysteresis; never mutate the active course or sim

**Priority: P1; P2 for telemetry-calibrated defaults**

### Sourced facts

- Three.js exposes renderer draw/resource information, `setPixelRatio`, instancing, and explicit disposal APIs [6][7][8].
- The Page Visibility API emits `visibilitychange` when a document becomes hidden or visible, enabling pages to avoid unnecessary work [9].
- Browser frame work that exceeds the available frame budget causes skipped/inconsistent frames; timing APIs exist to observe slow work, but support differs, so an in-loop rolling frame-time measure remains a practical baseline [10].

### ForgePlay change idea

Use three named presentation tiers selected independently of GameSpec and simulation:

```text
LOW:  pixelRatio cap 1.0, low dressing cap, reduced particles, bloom off/cheap
MED:  pixelRatio cap 1.5, normal dressing, bounded particles, standard bloom
HIGH: pixelRatio cap device-limited 2.0, full approved dressing/effects
```

The tier may change only presentation knobs:

- pixel ratio / render target size;
- dressing visibility or instance count;
- particle and trail pool capacity;
- shadow and post-effect quality;
- environment-map resolution/update cadence.

It must not change colliders, hazards, pickups, timers, score, RNG streams, course-plan hash, or simulation rate.

Controller rules:

1. Measure a rolling window after warm-up; ignore loading and tab-hidden frames.
2. Downgrade only after sustained slow frames (for example 2–3 seconds) and upgrade only after a much longer healthy window (for example 8–12 seconds).
3. Enforce a cooldown between changes and change one tier at a time.
4. Resize renderer and composer together; avoid rebuilding the scene.
5. On `document.hidden`, auto-pause local simulation under the shared policy and stop expensive presentation work. On resume, reset frame accumulator and camera temporal state.
6. On run replacement, call the adapter’s disposal path, then compare renderer resource counters after a short settling period. Repeating Generate → Play → Retry must not show unbounded growth.

**P2:** collect opt-in aggregate frame-tier outcomes to choose better defaults by broad device class. Do not generate bespoke gameplay or persist hardware-dependent values into GameSpec/RunManifest identity.

### Why this is new

The corpus says pixel ratio is an allowed scalability knob and mentions pause-on-visibility. It does not define presentation-only tier boundaries, downgrade/upgrade hysteresis, resize coupling, hidden-frame exclusion, or a repeat-run leak gate.

## Priority stack

### P0

1. `RealizationReceipt` with applied/substituted/rejected decisions.
2. Canonical `RunManifest` separating exact replay from remix.
3. Target and measured `DifficultyVector` plus monotonic seed-set tests.

### P1

1. Minimal `HustleAdapter` and semantic spawn records.
2. Presentation-only quality tiers with hysteresis and view disposal.
3. Prompt-tag mapping to the difficulty vector after metrics exist.

### P2

1. Telemetry-calibrated tier defaults.
2. Long-lived manifest storage or signed public sharing, only if product requirements justify a service.
3. More advanced course search/quality-diversity only if constructive generation demonstrably cannot meet coverage goals.

## Apply next

- Add `realizeSpec()` returning a complete `RealizationReceipt`; reject unsupported core hustle/module requests instead of silently ignoring them.
- Add a canonical `RunManifest` containing spec, seed, build/catalog IDs, receipt hash, plan hash, and exact-replay versus remix handling.
- Extend `CoursePlan` with a five-axis target/measured difficulty record and semantic spawn roles; gate three ordered presets across a fixed seed corpus.

## Sources

1. Semantic Versioning 2.0.0 — https://semver.org/
2. IETF RFC 8785, **JSON Canonicalization Scheme** — https://datatracker.ietf.org/doc/html/rfc8785
3. MDN / Web Crypto, **SubtleCrypto.digest()** — https://developer.mozilla.org/en-US/docs/Web/API/SubtleCrypto/digest
4. Shaker, Togelius, Nelson, **Procedural Content Generation in Games, Chapter 12: Evaluating Content Generators** — https://www.pcgbook.com/chapter12.pdf
5. Liapis et al., **Procedural Content Generation through Quality Diversity** — https://antoniosliapis.com/papers/procedural_content_generation_via_quality_diversity.pdf
6. Three.js, **InstancedMesh** — https://threejs.org/docs/pages/InstancedMesh.html
7. Three.js, **How to dispose of objects** — https://threejs.org/manual/en/how-to-dispose-of-objects.html
8. Three.js, **WebGLRenderer / Info** — https://threejs.org/docs/pages/WebGLRenderer.html
9. MDN, **Page Visibility API** — https://developer.mozilla.org/en-US/docs/Web/API/Page_Visibility_API
10. W3C, **Frame Timing** — https://www.w3.org/TR/frame-timing/
