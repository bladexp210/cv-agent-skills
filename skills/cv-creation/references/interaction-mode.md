# Interaction mode (`ui.interaction_mode`)

Config key: `ui.interaction_mode` in `career.config.yaml`.

| Value | Meaning |
|---|---|
| `standard` | Lower HITL density on mid-pipeline cv-creation turns (default for **new** installs via template) |
| `strict` | Current dense HITL (one-item / full rollup cadence) |
| *(missing)* | Treat as **`strict`** — no surprise batching for existing careers |

Read the key at session start with `career.config.yaml`. Mode is agent-enforced UX only — G4/G5 machine validators are unchanged.

**Turn 1: Experience validation** is always **solo** in both modes (Q2 not reopened). evidence-bank may read the key for display only; it does not batch Turn 1.

## Behavior table

| Surface | Strict (current) | Standard |
|---|---|---|
| Turn 1 Experience validation | Solo | Solo (unchanged) |
| Turn 2 Keyword validation | One keyword per turn (current example) | One table of proposed map; single approve / remap-list / drop-list turn |
| Turn 3 Gap probe | One question | One question (unchanged — integrity) |
| Turn 4 Differentiator | Confirm each used | Only when differentiators are proposed/used; else skip |
| Turn 5 Norms tie-breaker | When tie | Only when a real tie exists; else skip |
| Turn 6 Gate summary (G1–G3) | Full rollup | Compact rollup + recommended **approve**; expand on request |
| Turn 7 Draft review (G4) | Full | Still required; recommend approve when `validate_application` G4 passes; flags still batch-resolved |
| Turn 8 ATS readiness (G5) | Full | Still required; recommend export/approve when coverage passes local thresholds |
| Tracker / journey chatter | Current cadence | Same triggers, shorter lines; no extra “status?” prompts |

## Integrity floor (both modes)

- G4/G5 machine checks stay (`validate_application` / ATS coverage rules).
- No fabrication.
- Do not skip Turn 3 when matching action is `gap` or `ask_user`.
