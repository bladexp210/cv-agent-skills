# Composition rules

## SoT

`composition.yaml` owns section plan, bullets (including text), skills_line, grounding, buffered_flags. `draft.md` is always re-rendered from composition + identity header. They revise together.

## Section inclusion

| Section | Rule |
|---|---|
| Header | Always from identity |
| Summary | ≥3 core/use **or** ≥2 confirmed differentiators; 2–3 bullets |
| Skills | Any core/use/mention; group by parent_id; order core→use→mention; ATS forms; **not** covered_indirectly |
| Experience | Always; default reverse-chronological; norms may relevance-first |
| Education | Per norms |
| Projects/Certs | Only if evidenced + norms-appropriate; never empty |

## Bullet ordering

Experience: (1) max priority_norm of linked skills desc (2) confirmed differentiator boost confidence×0.5 (3) date desc (4) user_pinned sticky. Summary: summed priority_norm then differentiator hits. **Voice never orders.**

## Grounding (G4 machine checks)

1. Summary/Experience bullets: `ev_ids.length ≥ 1`
2. Each ev exists
3. status fact or waived with reason
4. `skill_ids[]` ⊆ skills on cited ev via evidence_skills; **core** bullets need ≥1 strong link; **use** ≥ moderate
5. Education/certs from identity exempt; else same
6. Skills-line item iff skill in core|use|mention
7. `grounding.uncovered` empty to pass

Ungroundable → omit from draft, add buffered_flag.

## Buffer resolve-flag

drop | rephrase | route-to-bank (only this fires [6]→[5]) | waive

## Unconfirmed differentiators

Reorder/emphasis only. G4 must confirm/reject/route-to-bank/defer each used id. T4 envelope embedded in T7.
