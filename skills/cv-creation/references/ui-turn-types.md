# UI turn types (cv-creation)

## Hosts

`ui.chat_host`: `gui` (markdown-native) | `tui` (monospace). Glyphs: chat `auto` → emoji on gui, unicode on tui; `views` default emoji. `ascii` overrides both.

| Semantic | unicode | ascii | emoji |
|---|---|---|---|
| not_started | `·` | ` ` | ⬜ |
| in_progress | `◐` | `~` | 🟡 |
| awaiting_hitl | `◆` | `*` | 🔔 |
| approved | `✓` | `x` | ✅ |
| flag | `⚑` | `!` | ⚠️ |
| reopened | `↻` | `r` | 🔄 |
| gap / blocked | `✗` | `-` | 🛑 |
| pinned | `📌` | `P` | 📌 |

## Envelope

gui: bold header lines, numbered options, italic checkpoint. tui: aligned box with `[n]` options and rule before checkpoint. Error verb uses same envelope with ≥2 recoveries.

## Human labeling (locked 2026-11-18)

- Never show bare `T1`…`T8` to the user. Required: **`Turn N: <plain name>`** (e.g. `Turn 2: Keyword validation`). Optional builder cue `(T2)` only after the plain label.
- When the stage/queue total is known, show **`current of total`** in the header or question line (e.g. `3 of 14`).
- See repo `COMMUNICATION_CONTRACT.md` and handoff §19.5.3 HMI principles 5–6.

## Turn catalogue

| # | Human label | Type | Decisions |
|---|---|---|---|
| T2 | Turn 2: Keyword validation | Keyword validation | approve / remap / drop / add |
| T3 | Turn 3: Gap probe | Gap probe | has evidence / no evidence / waive (verbatim shared) |
| T4 | Turn 4: Differentiator confirmation | Differentiator | confirm / reject / route-to-bank |
| T5 | Turn 5: Norms tie-breaker | Norms tie-breaker | once / scoped rule / wider rule |
| T6 | Turn 6: Gate summary | Gate summary | approve / revise / resolve / accept (verbatim shared) |
| T7 | Turn 7: Draft review | Draft review | approve / revise / resolve-flag (drop\|rephrase\|route-to-bank\|waive) |
| T8 | Turn 8: ATS report | ATS report | approve / accept-edge / export / override |

## T2 gui example

```markdown
**▸ Turn 2: Keyword validation · kw_1 · 1 of 6**
**Raw:** k8s → **Normalized:** Kubernetes → **sk_kubernetes**
**Occurrences:** 1 · **Placement:** body
1. approve
2. remap
3. drop
4. add
*checkpoint 2026-11-21T08:00Z*
```

## T2 tui example

```
▸ Turn 2: Keyword validation · kw_1 · 1 of 6
  Raw: k8s → Normalized: Kubernetes → sk_kubernetes
  Occurrences: 1 · Placement: body
  [1] approve  [2] remap  [3] drop  [4] add
──────────────────────────────────────────── checkpoint 2026-11-21T08:00Z
```

## T4 gui / tui

gui: fields text, source, confidence, URL; decisions confirm/reject/route-to-bank. tui: same fields aligned with [1][2][3].

## T5 gui / tui

Show conflict, current values, three save options narrow→wide.

## T6 gui example

```markdown
**▸ Turn 6: Gate summary · G3 · matching**
**Stage:** matching · items 11/14 · awaiting 2
**Actions:** core 4 · use 3 · mention 2 · gap 2 · ask_user 1
*(core = high priority + strong evidence; use = high priority + moderate evidence; …)*
**Buffered flags:** 0
1. approve
2. revise
3. resolve
4. accept
*checkpoint 2026-11-21T09:15Z*
```

## T7 / T8

T7: draft excerpt, section plan, bullet→ev table, buffered flags batch, unconfirmed differentiator dispositions (T4 embedded). T8: coverage table, warnings, proposed edges, override reason field.

## Tracker cadence

Re-render on stage transition, gate open/close, flag-count change, revision-count change, or `status`. Floor: `checkpointing.turn_floor`. Double-render guard: once per event burst.
