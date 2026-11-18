---
name: cv-creation
description: >-
  Run a per-application CV pipeline from JD intake through matching, composition,
  ATS check, and export. Use when the user wants to tailor a CV to a job, resume an
  application, probe a gap, export resume formats, or check ATS coverage.
---

# CV Creation

## Purpose

One application end-to-end: JD → requirements → keywords → scoring → matching → composition → ATS → export. Facts come from the evidence bank; voice applies only at composition.

## When to load

| File | When |
|---|---|
| `references/scoring-rubric.md` | Stage [4] |
| `references/matching-rules.md` | Stage [5] |
| `references/composition-rules.md` | Stage [6] |
| `references/voice-guide.md` | Voice elicitation / phrasing |
| `references/norms-guide.md` | Norms conflicts (T5) |
| `references/hitl-gate-catalogue.md` | Any gate G1–G5 |
| `references/state-machine.md` | Item/stage/global loops |
| `references/checkpoint-schema.md` | Writing checkpoints |
| `references/continuity.md` | LIVE.yaml, resume, memory mirror (shared with evidence-bank — keep identical) |
| `references/differentiator-rules.md` | Differentiators |
| `references/ui-turn-types.md` | Chat primitives T2,T4–T8 |
| `references/export-pipeline.md` | Stage [8] |
| `references/ats-baseline-rules.md` | Human ATS baseline |
| `references/ats-check.md` | Stage [7] |
| `references/taxonomy-mechanics.md` | New/merge skills |
| `references/invocation.md` | Obligations vs user-intent aliases / script CLIs |
| `references/probe-ui.md` via evidence-bank | When rendering shared T3/T6 |
| assets listed below | Templates on create/copy |
| scripts listed below | Validate, views, export, bootstrap |

## Invocation

See `references/invocation.md` and `references/continuity.md`.

- **Obligations:** LIVE + STATUS after each meaningful step; memory mirror if tools exist; disk-first resume.  
- **User intent:** plain language (`continue`, `status`, `export`, …) with optional aliases — not housekeeping commands.

Always read `career.config.yaml` first. Absent → onboarding (`scripts/bootstrap_career.py` flow). On resume, recompute from disk per `continuity.md`.

## Stages

| # | Stage | Writes |
|---|---|---|
| 0 | Bootstrap | tree, config, profile scaffolds |
| 1 | JD intake | `jd.md`, `meta.yaml`, copy `composition.template.yaml` |
| 2 | Requirements | `requirements.yaml` — gate G1 |
| 3 | Skills & keywords | `keywords.yaml`, taxonomy links — T2 |
| 4 | Scoring | `scores.yaml` — gate G2 |
| 5 | Matching | `matching.yaml`, differentiators, probes — gate G3 |
| 6 | Composition | `composition.yaml` + rendered `draft.md` — gate G4 |
| 7 | ATS & consistency | `ats-check.yaml` + `audit.md` — gate G5 |
| 8 | Export | `export/*` via `export_resume.py` |

Backward edges (flag-triggered only): [4]→[2] noise; [5]→bank probe; [6]→[5] ungroundable bullet; [7]→[6] coverage/phrasing/C1; [7]→[5] must-have gap / missing evidence.

## Composition SoT

`composition.yaml` owns plan, grounding, buffered flags, and planned bullet text. `draft.md` is always re-rendered from it (+ identity header). Export reads **draft.md + identity.yaml + export-style.yaml only**.

## Design principles (do not violate)

1. Two skills, not one.
2. Facts and voice separated.
3. AI proposes; user approves.
4. Differentiators reorder/emphasize only until bank-confirmed.
5. State is loops; `approved` is exit; backward edges explicit.
6. One canonical structured file per artifact; views generated.
7. Checkpoints durable.
8. User judgment tie-breaks norms.
9. Skill code vs career data separated.
10. No fabrication.

### Cross-skill contract — T3 Gap probe (verbatim)

**Owner:** both skills (identical text required).

**When:** A required skill has action `gap`, or matching needs a single-item evidence probe.

**Body (must include):**
- requirement text (or id)
- missing `sk_*` (canonical name + id)
- exactly one probe question from the probe-question bank
- linked evidence candidates if any (ids only)

**Decisions (exact labels):** `has evidence` / `no evidence` / `waive`

**Envelope:** use the standard primitive envelope (gui or tui per `ui.chat_host`). One decision per turn.


### Cross-skill contract — T6 Gate summary (verbatim)

**Owner:** both skills (identical text required).

**When:** End of a stage loop, before gate pass.

**Body (must include):**
- stage name and item rollup (done / awaiting_hitl / pending)
- action counts with **inline definitions**:
  - `core` — high priority + strong evidence
  - `use` — high priority + moderate evidence
  - `covered_indirectly` — met via a broader evidence row
  - `mention` — low priority, evidenced (skills line only)
  - `gap` — required, not evidenced
  - `ask_user` — weak or stale evidence — probe before deciding
- buffered-flag count

**Decisions (exact labels):** `approve` / `revise` / `resolve` / `accept`

**Envelope:** standard primitive envelope. Tracker line may accompany; active primitive last.


### Action definitions (canonical)

| Action | Meaning |
|---|---|
| `core` | high priority + strong evidence |
| `use` | high priority + moderate evidence |
| `covered_indirectly` | met via a broader evidence row |
| `mention` | low priority, evidenced (skills line only) |
| `gap` | required, not evidenced |
| `ask_user` | weak or stale evidence — probe before deciding |


## Gates (summary)

Load `references/hitl-gate-catalogue.md`. G4 resolve-flag sub-decisions: drop / rephrase / route-to-bank / waive. G5: approve / accept-edge / export / override (reason required).

## Privacy / VCS / language

No telemetry. Web fetch only with per-URL OK. Bootstrap installs gitignore (docx/pdf). Commit evidence by default. One language per application; no auto-translate.
