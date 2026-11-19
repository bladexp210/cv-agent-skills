# ATS & consistency check

## Scope (say this to the user)

This stage measures **ATS readiness and coverage**: how well the draft covers requirements you extracted, under local deterministic rules (`profile/norms/ats/` + this file).

It is **not** a prediction that any employer’s ATS will rank, parse, or “pass” the CV at the same percentage. Do not present `coverage_pct` or G5 “pass” as an employer pass probability.

## Artifacts

`ats-check.yaml` (machine) + `audit.md` (narrative). Title/human copy: prefer **ATS readiness report** over bare “ATS score.”

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
