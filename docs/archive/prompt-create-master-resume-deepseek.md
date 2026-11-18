# Session: Design the Evidence-Bank Skill (Agent Skills format)

## Context
You are helping me design a second skill that pairs with an existing **CV creation skill**, which I have attached. The destination for both skills is Cursor, which follows the Agent Skills open standard (SKILL.md + references/ + assets/ + scripts/, progressive disclosure, description-driven triggering). This chat is a **design session** — you produce file contents, I copy them into the project.

The objective is to transform my master resume into a structured, de-styled, ambiguity-free **evidence bank** that the CV creation skill will consume for matching and composition.

## Required inputs
1. **Attached: CV creation skill files.** Read them first. Its interface determines what the evidence-bank skill must expose. Summarize the contract you found before proposing anything.
2. **Attached: master resume (if provided).** Treat it as raw material, not canonical. If not attached, ask me for a small slice to use in the dry pass.

## Design decisions already settled — do not reopen
If you disagree, flag it once with evidence, then proceed.

- The evidence bank is a **separate skill with its own lifecycle**, not a sub-step of the CV skill.
- **De-styling and ambiguity detection are one pass.** Stripping style exposes holes. Every surviving fact gets a status: `fact`, `ambiguous`, `unverified`, or `waived`.
- **Probing is a loop.** Ambiguous/unverified items trigger targeted questions until each is resolved or explicitly waived. “Don’t remember, drop it” is a valid terminal state.
- **The CV skill must be able to call this skill for a single item** (gap resolution during matching), not only as a full run. Design the interface for both.
- **Never synthesize or infer an unstated fact.** Extract, probe, record. Do not fill gaps.
- **The bank is facts-only.** Voice and style are the CV skill’s concern (a separate voice profile applied at composition), not the bank’s.
- **State is modeled as loops, not a linear chain.** `approved` is an exit transition, not a state you pass through. Do not include a `revised` state; use `in_progress` + `revision_count`.

## Scope of the evidence-bank skill
In scope:
- Read a master resume (and optionally a prior bank for incremental updates).
- Extract atomic evidence records with fields: actor, action, object, scale, metric, tool, date, outcome.
- Strip style: adjectives, self-praise verbs, unquantified claims (“significantly improved”), any sentence that cannot survive “how do you know?”
- Classify each fact with a status and, where needed, a probe question.
- Run the probe loop with the user (HITL), recording resolutions and waivers.
- Emit a normalized bank: `experiences`, `evidence`, `evidence_skills` (n:n), with strength and recency on each skill link.
- Expose a single-item probe interface for the CV skill’s matching stage.

Out of scope: JD analysis, scoring, matching, composition, voice. Those belong to the CV skill.

## Agent Skills constraints (output format)
- Skill directory: `.agents/skills/evidence-bank/`
- `SKILL.md` frontmatter: `name: evidence-bank` (match directory; lowercase, hyphens only); `description:` 1–1024 chars, imperative, must cover both full-bank creation and single-item probing, pushy about triggering.
- `SKILL.md` body: step-by-step instructions, input/output examples, edge cases. Target **under 500 lines / ~5,000 tokens**.
- Progressive disclosure: `references/` for detailed docs loaded on demand; `assets/` for templates and checklists; `scripts/` only for deterministic reusable checks. State in `SKILL.md` exactly when to load each.
- File references relative and one level deep from `SKILL.md`. No nested chains.
- Do not explain what a resume or JSON is. Add only what the agent would get wrong without the skill.

## State machine to design into the skill
Three levels, all loops.

**Level 1 — item lifecycle** (one evidence fact):
```
not_started → in_progress → awaiting_hitl ──approve──→ approved (exit)
                                  │  ↑
                           revise │  │ resubmit
                                  ▼  │
                                in_progress
```
Record `revision_count`. No `revised` state.

**Level 2 — stage loop:**
```
run_stage:
  items = extract()
  while pending_item = next_pending(items):
      run item lifecycle
      # user may add/remove items here → items changes → loop continues
  if not gate(stage):
      goto re-extract
  stage.status = done
```
Exit: no pending items AND gate passed AND no open flags.

**Level 3 — global** for this skill:
- Full run: extract → probe loop → gate → emit.
- Incremental: load existing bank → probe only new/changed items → gate → merge.
- Single-item probe (called by CV skill): load item → probe → return resolution → no full emit.

HITL gates: after extraction (before probing), after probing (before emit). Gate summary shows open flags and revision counts.

## Deliverables
Produce file contents, one code block per file, with the path as a heading above it. In order:

1. `.agents/skills/evidence-bank/SKILL.md`
2. `references/destyling-rules.md` — rules + before/after examples.
3. `references/probe-question-bank.md` — default probes per ambiguity type + rules for generating new ones.
4. `references/status-taxonomy.md` — `fact`/`ambiguous`/`unverified`/`waived`, transitions, what counts as evidence.
5. `references/evidence-schema.md` — `experiences` / `evidence` / `evidence_skills` model, field definitions, n:n link contract.
6. `assets/evidence-record-template.json` — blank record.
7. `assets/probe-checklist.md` and `assets/de-styling-checklist.md` — human-facing.
8. `scripts/validate_evidence.py` — validates required fields, allowed statuses, referential integrity of `evidence_skills.skill_id`.

In `SKILL.md`, state exactly when each reference and asset is loaded. Do not make the agent read everything on every run.

## Success criteria
- A master resume converts to a bank with no unaddressed `ambiguous` or `unverified` items (waived counts as addressed).
- Every skill traces to ≥1 evidence row; every evidence row has a source span in the master resume.
- The CV skill can request a single-item probe without a full re-extraction.
- No style tokens survive into the bank (spot-check: no “passionate”, “dynamic”, “spearheaded”, “significantly”).
- `SKILL.md` under 500 lines; its `description` fires on “build my evidence bank” and “do I have anything for Lambda?”, and does **not** fire on “tailor my CV to this JD” (that is the CV skill’s job).

## Working method
1. Read the attached CV skill. Summarize the interface contract in 5 bullets. **Stop and confirm with me before producing any file.**
2. Produce `SKILL.md` only, including file-load conditions. **Stop for review.**
3. Produce references and assets. **Stop for review.**
4. Produce the validation script last, against the schema as settled.
5. Run one dry pass on a small slice of the master resume. Show the item lifecycle in action, including one revise loop and one waiver.