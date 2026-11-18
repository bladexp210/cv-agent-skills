---
name: evidence-bank
description: >-
  Maintain a de-styled career evidence bank (facts, experiences, skill links).
  Use when the user wants to capture, probe, destyle, validate, or waive CV evidence;
  when cv-creation routes a gap probe or differentiator to the bank; or for a single-item probe.
---

# Evidence Bank

## Purpose

Store **de-styled facts** only. Voice never enters this skill. Provenance is mandatory. No fabrication.

Design SoT: repo `EVIDENCE-BANK-DECISIONS.md`. UI labeling: repo `COMMUNICATION_CONTRACT.md`.

## When to load

| File | When |
|---|---|
| `references/evidence-schema.md` | Creating or editing evidence rows |
| `references/destyling-rules.md` | Ingesting resume / LinkedIn / manual / route-to-bank claims |
| `references/probe-question-bank.md` | Running a gap or ambiguity probe |
| `references/status-taxonomy.md` | Setting `status` / waiver reasons |
| `references/probe-ui.md` | Rendering Turn 1 / Turn 3 / Turn 6 |
| `assets/evidence-record-template.yaml` | New file or empty-bank scaffold |
| `assets/de-styling-checklist.md` | Before proposing a row for Turn 1 |
| `assets/probe-checklist.md` | Before closing a probe |
| `scripts/validate_evidence.py` | Before persist; on user `validate` |

## Invocation

Chat verbs (shared grammar with cv-creation `references/invocation.md`): `run` / `continue`, `status`, `show`, `probe`, `gate`, `validate`.

Config: read `career.config.yaml` at start. Paths are never hardcoded.

## Ingest surfaces (allowed)

1. Master resume — PDF and/or Markdown  
2. LinkedIn — **paste** (text dump only; no live scrape)  
3. Manual entry  
4. cv-creation **route-to-bank** (gap / differentiator / buffered flag)

Company URL fetch is **not** an ingest surface; only with explicit per-URL OK when routed for differentiators.

## Pipeline

### Bulk ingest mode

1. Load `profile/evidence.yaml` + `profile/skills.yaml` (create empty evidence from template if missing).  
2. Extract candidates from the ingest surface → apply `destyling-rules.md` → pass `de-styling-checklist.md` → enqueue.  
3. Process queue **one item at a time** with **Turn 1: Experience validation** (mandatory solo HITL; no batch confirm).  
4. On each Turn 1, propose `sk_*` + strength + recency; user confirms or edits.  
5. Persist after each decision; run `validate_evidence.py`.  
6. When the queue drains, offer optional **Turn 6: Gate summary** (ingest rollup).  

### Single-item mode

Same item states; no bulk queue. Used for `probe`, Turn 3: Gap probe from cv-creation, and route-to-bank.

### Item states

```
pending → destyled → awaiting_hitl → fact | waived | ambiguous
```

## Evidence rules (summary)

- No row without a `source` span.  
- `unverified` may sit queued with empty `probe_history`; append history before → `fact`.  
- `ambiguous` / `waived` require `probe_history` (validator hard-fail).  
- `waived` is terminal; reason in `probe_history`.  
- `probe_history` entry: `{ts, kind, question?, answer?, decision}` (minimal).  
- Clean amend with clear source may skip a new probe question; still needs Turn 1.  
- `strength` and `recency` live on `evidence_skills` links, not the evidence row.  
- Experiences: one `exp_*` per **role**; overlap allowed; `end: present` for current.  
- Never invent facts. Never apply voice.  

## Human labeling

- Never show bare `T1`…`T8` to the user. Use **`Turn N: <plain name>`** (optional `(TN)` after).  
- When a queue/stage total is known, show **`current of total`** in the header or question line.  

## Turn types owned here

- **Turn 1: Experience validation** — confirm / amend / waive / mark ambiguous  
- **Turn 3: Gap probe** — shared verbatim body/decisions below  
- **Turn 6: Gate summary** — shared verbatim body/decisions below  

Load `references/probe-ui.md` for gui/tui envelopes and examples.

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

## Validation

```bash
python scripts/validate_evidence.py path/to/profile/evidence.yaml
```

Hard-fail (exit 1): missing id/source; duplicate ids; bad `experience_id`; invalid status/strength/recency; `ambiguous`/`unverified` without `probe_history`; unknown `evidence_id` on links; `skill_id` missing when link present.

Warn (exit 0): empty bank; experience with no evidence rows.

Smoke fixtures:

```bash
python scripts/validate_evidence.py assets/fixtures/ok.yaml          # expect OK
python scripts/validate_evidence.py assets/fixtures/bad-missing-source.yaml  # expect fail
```

## Privacy

No telemetry. Do not fetch URLs unless the user explicitly approves each URL.

## Errors

Name path and attempt; offer ≥2 recoveries; quote parse line numbers. Abort the item loop without corrupting state.
