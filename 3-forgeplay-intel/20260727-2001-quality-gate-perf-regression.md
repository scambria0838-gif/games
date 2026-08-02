# Quality gate — Perf / regression assert extensions

## Context

ForgePlay **Quality-gate checklist for generated feel** is PARTIAL. Existing `20260727-1917-quality-gate-fields.md` covers schema/arcade bounds. Codex profiling report adds regression-gate pattern.

## Source

- `you-are-the-lead-research-engineer\work\2026-07-27_profiling-telemetry-regression-gates.md`
- Level/AI perf budgets spirit (world-ai-performance reports)

## Additive fields (proposal)

```ts
qualityGate?: {
  // ...existing...
  maxSimStepMs?: number;          // default 4 @60Hz smoke host
  maxActiveAgents?: number;       // default 12 — peds/guards/sweepors
  maxRooms?: number;              // copper interior
  requireHudSnapshot?: boolean;   // shared HUD contract
  requireFailReasons?: string[];  // e.g. ["cartStolen","fired","electrocute","caught"]
}
```

Still deterministic — no GPU frame-time flakiness in CI; use sim-step budget + counts.

## Status impact

Supports moving quality-gate feel row toward stronger PARTIAL / future HAVE-candidate when coding agent wires asserts.
