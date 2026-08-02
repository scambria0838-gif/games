# GameSpec — Hustle fail / win reason fields

## Context

New Agent D fail notes need stable reason enums for adapters + HUD.

## Proposed

```ts
recipe?: {
  // per hustle blocks may include:
  failReasons?: Array<
    | "wreck" | "timeout" | "caught" | "cartStolen" | "busted"
    | "injury" | "fired" | "electrocute" | "quit"
  >;
  winReasons?: Array<"dock" | "extractQuota" | "checklistPay" | "cashTarget" | "redeemQuota">;
}
```

Coding agent maps reasons → retry UI strings. Do not fork MD-B wreck-only.

## Cross-links

- Mechanics fail notes 2002 / 2007 / 2012 + shared win/fail 1951
