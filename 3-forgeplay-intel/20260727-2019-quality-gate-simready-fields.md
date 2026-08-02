# Proposal: Quality-gate SimReady / PresentationReady asserts

**Status:** proposal only — no production code

## Context

Extends `20260727-1917-quality-gate-fields.md` with Mythology world-readiness vocabulary for ForgePlay generations (tiny courses, not Unreal World Partition).

## Source

- `C:\Users\steve\Documents\BACKUP\operation-mythology-world-ai-performance-20260727-013133.md` — Resident / SimReady / PresentationReady; transition commit gates
- Cross-link: existing `qualityGate` fields; `BACKUP-RESEARCH-SOURCE.md`

## Proposed additions

```ts
qualityGate?: {
  // ...existing fields...
  /** Course/hustle activation claims */
  requireSimReadyBeforeInput?: boolean; // colliders + spawns published before command intake
  requirePresentationReadyBeforeCam?: boolean; // meshes/HDR ready or explicit fallback sky
  failOnIncompleteExtractZone?: boolean; // copper/homeless drop points must exist when recipe needs them
  maxPortalNodes?: number; // default 32 — copper interior graph bound
}
```

## Apply note

1. Coding agent smoke: after course build, assert player spawn, win/fail volumes, and required interactables exist.
2. Do not implement cell streaming; treat “SimReady” as one-shot course publication barrier.
3. Presentation fallback (flat color fog) allowed if HDR missing — gate records fallback used.

## MECHANICS_MASTER_LIST

| Row | Status |
|-----|--------|
| Quality-gate checklist for generated feel | PARTIAL → PARTIAL-candidate (fields extended) |

## Explicit

**no production code — proposal only**
