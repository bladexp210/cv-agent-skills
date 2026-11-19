# Communication contract

> Project overlay for Adaptive Clarity.  
> Optional host defaults: `~/.cursor/USER_PROFILE.md` (if present) + skill `adaptive-clarity`.  
> If no host profile exists, this contract and the skills are enough.

**Project:** application-skills (CV System)  
**Updated:** 2026-11-19

---

## Audience

| Who | What they need |
| :--- | :---- |
| Operator / designer | Plain labels; stage progress; Decision-mode options tables; recommend+reason |
| Future agents | `AGENTS.md` → design docs → `skills/`; do not invent from chat |
| Skill end-users (CV / evidence-bank in an Agent Skills client) | Same plain-label + progress rules on every HITL turn |

## Source of truth (read order)

1. `AGENTS.md`
2. `docs/design/EVIDENCE-BANK-DECISIONS.md` (bank work)
3. `docs/design/CV-SYSTEM-HANDOFF.md` settled slices (do not reopen Clusters 1–3 / Q1–Q7)
4. `skills/` (skill SoT)
5. `docs/architecture/CV-SYSTEM-ARCHITECTURE.md` (inventory only)
6. This contract
7. Optional host Adaptive Clarity profile (`~/.cursor/USER_PROFILE.md` if present)

## Glossary (critical terms — no synonym drift)

| Term | Meaning | Do not say (alone) |
| :--- | :---- | :---- |
| Turn N: \<Name\> | Human-facing HITL primitive | Bare `T0`…`T8` |
| Ingest scope | Turn 0 — bank bulk pass; operator approves queue composition before enqueue (G1; G2 if curated/revise) | “T0” without the name |
| Experience validation | Turn 1 — bank fact confirm/amend/waive/ambiguous | “T1” without the name |
| Gap probe | Turn 3 — shared bank ↔ cv-creation | “T3” alone |
| Gate summary | Turn 6 — stage rollup; bulk ingest includes Coverage (included vs deferred vs source) | “T6” alone |
| evidence-bank | Skill that owns de-styled facts | “the bank” without path on first use in a scene |

## Default modes

| Artifact / task | Mode |
| :--- | :---- |
| Chat with the operator | Chat / Decision (one question per turn while designing) |
| Session / handoff updates | Handoff |
| Skill user-facing HITL | Procedure-shaped envelope + plain labels |
| Architecture / ADR locks | Decision |

## Language

| Surface | Language |
| :--- | :---- |
| Agent / harness / ADRs / skill **logic** (schemas, validators, machine decision tokens) | English — Adaptive Clarity |
| HITL **display** (turn headers, option labels) | Follows `ui.locale` (`en` \| `fr` \| `ar`; missing ⇒ `en`). User may still reply with the English machine token or option number. |
| Install / use docs for everyday users | Locale hubs: `docs/user/<lang>/`, `prompts/<lang>/` when STATUS marks that locale `current` (`fr`, `ar` live). EN SoT remains root README / `docs/` / `prompts/` |
| Exported CV content | Per application `meta.language` |

## Project-only constraints

### Plain labels (locked 2026-11-18)

- Never show bare turn codes to the operator or skill users.
- Required form: **`Turn N: <plain name>`** (example: `Turn 1: Experience validation`).
- Optional builder cue: append `(T1)` only after the plain label.

### Interaction mode

- `ui.interaction_mode` (`standard` \| `strict`) sets HITL density; see `skills/cv-creation/references/interaction-mode.md`. Missing key ⇒ strict. Turn 1 always solo.

### Stage progress (locked 2026-11-18)

- When a stage, ingest queue, or design questionnaire has a known total, every active turn shows **`current of total`**.

### Recommend + reason (locked 2026-11-18)

- Options/proposals to the operator always include a **recommendation** and **short reasoning**.

### Repo layout (locked 2026-11-18, option A)

- Skill SoT: `skills/` only  
- Design: `docs/design/`  
- Archive: `docs/archive/` (not live SoT)  
- No parallel `career/.cursor/skills` or `architecture-v1.0/` trees in this repo  

### Evidence-bank

- Turn 0: Ingest scope is **bank-only** (not in cv-creation catalogue); required before every bulk enqueue.
- Turn 3 / Turn 6 contract body+decisions stay verbatim-identical with cv-creation unless jointly edited (Turn 6 includes Coverage).

### Continuity (locked 2026-11-18)

- Progress SoT is career project files + `_skill_state/LIVE.yaml` (see skill `references/continuity.md` in both skills — keep identical).
- Long-term memory (MCP, etc.) is optional write-through after LIVE; never outrank disk.
- Housekeeping (LIVE, memory mirror, validate-after-persist) is a skill obligation — not a user-facing command.

## Out of scope for this contract

- Persona/marketing copy outside the CV skills
- Reopening cv-creation composition / export / ATS locks
