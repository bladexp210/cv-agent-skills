# Communication contract

> Project overlay for Adaptive Clarity.  
> Global defaults: `/home/mohamed/.cursor/USER_PROFILE.md` + skill `adaptive-clarity`.

**Project:** application-skills (CV System)  
**Updated:** 2026-11-18

---

## Audience

| Who | What they need |
| :--- | :---- |
| Mohamed (operator / designer) | Plain labels; stage progress; Decision-mode options tables |
| Future agents | Handoff + Architecture File + this contract; do not invent from chat |
| Skill end-users (CV / evidence-bank in Cursor) | Same plain-label + progress rules on every HITL turn |

## Source of truth (read order)

1. `EVIDENCE-BANK-DESIGN-HANDOFF.md` / `EVIDENCE-BANK-DECISIONS.md` (when present) for bank design
2. `CV-SYSTEM-HANDOFF-v0.2.md` settled slices (do not reopen Clusters 1–3 / Q1–Q7)
3. `CV-SYSTEM-ARCHITECTURE-v1.0.md` (cv-creation locked; evidence-bank provisional until redesign closes)
4. This contract
5. Global `USER_PROFILE.md`

## Glossary (critical terms — no synonym drift)

| Term | Meaning | Do not say (alone) |
| :--- | :---- | :---- |
| Turn N: \<Name\> | Human-facing HITL primitive | Bare `T1`…`T8` |
| Experience validation | Turn 1 — bank fact confirm/amend/waive/ambiguous | “T1” without the name |
| Gap probe | Turn 3 — shared bank ↔ cv-creation | “T3” alone |
| Gate summary | Turn 6 — stage rollup | “T6” alone |
| evidence-bank | Skill that owns de-styled facts | “the bank” without path on first use in a scene |

## Default modes

| Artifact / task | Mode |
| :--- | :---- |
| Chat with Mohamed | Chat / Decision (one question per turn while designing) |
| Session / handoff updates | Handoff |
| Skill user-facing HITL | Procedure-shaped envelope + plain labels |
| Architecture / ADR locks | Decision |

## Language

| Surface | Language |
| :--- | :---- |
| Agent / harness / ADRs / skills | English — Adaptive Clarity |
| Exported CV content | Per application `meta.language` |

## Project-only constraints

### Plain labels (locked 2026-11-18)

- Never show bare turn codes to Mohamed or skill users.
- Required form: **`Turn N: <plain name>`** (example: `Turn 1: Experience validation`).
- Optional builder cue: append `(T1)` only after the plain label.
- Same rule for gates/stages when spoken to humans: prefer the plain name; id in parentheses if needed.

### Stage progress (locked 2026-11-18)

- When a stage, ingest queue, or design questionnaire has a known total, every active turn shows **`current of total`** (examples: `Q7 of 11`, `3 of 14`).
- Put it in the header or the question line — not only in a buried tracker.

### Recommend + reason (locked 2026-11-18)

- When presenting options or proposals to Mohamed, always include a **recommendation** and **short reasoning** (tradeoffs, NFR assumption, confidence).
- Bare option tables without a preferred path are not enough.

### Evidence-bank design session

- Design before build; one review question per turn unless waived.
- Do not treat provisional `architecture-v1.0/.cursor/skills/evidence-bank/` as approved SoT.
- Turn 3 / Turn 6 contract body+decisions stay verbatim-identical with cv-creation unless jointly edited.

## Out of scope for this contract

- Persona/marketing copy outside the CV skills
- Reopening cv-creation composition / export / ATS locks
