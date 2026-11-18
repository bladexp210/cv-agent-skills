# Matching rules

```
required    = { skills with priority_norm > 0 }
evidenced   = { skills reachable from evidence_skills }
required ∩ evidenced  → core / use / covered_indirectly / mention
required − evidenced  → gaps
evidenced − required  → differentiators (sparingly)
```

## Action floors

| Action | priority_norm | strength | recency |
|---|---|---|---|
| core | ≥ 70 | strong | not stale |
| use | ≥ 40 | ≥ moderate | any |
| mention | > 0 | ≥ weak | any |
| ask_user | high priority | weak **or** stale | — |
| gap | in required | not evidenced | — |
| covered_indirectly | — | evidenced via parent/broader only | — |

**Stale cannot be `core`** — downgrade to `use` or `ask_user`.

## Strength rubric (on evidence_skills)

| Level | When |
|---|---|
| strong | Named tool/skill in fact AND metric/outcome AND actor=self |
| moderate | Named + actor=self without metric; or metric with tool in `tool[]` only |
| weak | Implied / team-only / parent-adjacent / single mention without ownership |

## Recency (vs application `created`)

| Label | Window |
|---|---|
| current | ≤ 18 months |
| `<3y` | ≤ 36 months, not current |
| stale | older, or undated → stale + warn |

## Output

`matching.yaml` with `matching[]` and `differentiators[]`.
