# ATS & consistency check

## Artifacts

`ats-check.yaml` (machine) + `audit.md` (narrative).

## Universe

`core` + `use` + `gap` only.

## In-draft (norms-aware)

- Skills section included: bullet `skill_ids` OR skills-line ats_forms
- Skills section omitted: bullet `skill_ids` only

## Coverage

```
covered = in_draft ∧ action ≠ gap ∧ strength_ok
coverage_pct = 100 × |covered| / |universe|
```

Defaults: pass 80, warn 65. must_have gap blocks pass unless override.

## Consistency

C1 draft ≡ render(composition) — **block** until fix. Also grounding, style MUST, identity contact warn, no ambiguous/unverified in cited_ev_ids.

## Edges

Gap / missing evidence → propose [7]→[5]; else → [7]→[6].

## Override

Allowed; reason required; gaps remain visible.
