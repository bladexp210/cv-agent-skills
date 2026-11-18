# Evidence-Bank — Decision Record

**Status:** design closed  
**Closed:** 2026-11-18  
**Parent:** `EVIDENCE-BANK-DESIGN-HANDOFF.md`  
**Communication:** `COMMUNICATION_CONTRACT.md`

This record is the SoT for building/replacing `evidence-bank`. Provisional tree is not approved by silence — each path below is **rewrite** unless noted.

---

## 1. Design locks (Q1–Q11)

| Q | Topic | Decision |
|---|---|---|
| Q1 | Ingest surfaces | **B** — master resume (PDF/MD) + LinkedIn paste (text dump, no live scrape) + manual entry + cv-creation route-to-bank |
| Q2 | Destyling + HITL | **C** — `destyling-rules.md` → `de-styling-checklist.md` → propose → mandatory **solo** Turn 1: Experience validation before every `fact` (no batch confirm) |
| Q3 | Experience model | **A** — one `exp_*` per role; same org → many rows; `YYYY-MM`; overlap allowed; `end: present` for current |
| Q4 | `probe_history` | **A** — entry shape `{ts, kind, question?, answer?, decision}`; probe required before `fact` from `unverified`/`ambiguous`; every `waive` logs an entry; clean amend with clear source may skip a new probe question |
| Q5 | Skill-link UX | **A** — agent proposes `sk_*` + strength + recency; user confirms/edits on the **same** Turn 1 |
| Q6 | Lifecycle | **A** — two modes: bulk ingest queue (one Turn 1 at a time; optional Turn 6: Gate summary when queue drains) vs single-item probe (Turn 3 / route-to-bank / `probe`); shared item states |
| Q7 | Profile layout | **A** — single `profile/evidence.yaml` (`experiences` + `evidence` + `evidence_skills`) |
| Q8 | Validation | **A** — hard-fail integrity (ids, source, refs, enums; `ambiguous`/`waived` need `probe_history`); `unverified` may have empty history while queued; warn on empty bank / org with no evidence rows |
| Q9 | Turn 3 / Turn 6 | **C** — freeze verbatim **body + decisions**; human headers are display-only (`Turn 3: Gap probe`, `Turn 6: Gate summary`) |
| Q10 | Inventory | **A** — keep listed skill paths; rewrite bodies; delete `PROVISIONAL.md` when built |
| Q11 | Bank CI | **A** — `py_compile` + validate on `assets/fixtures/ok.yaml` and `assets/fixtures/bad-missing-source.yaml` (expect fail) |

### Mid-session communication locks (apply to bank + cv-creation UI)

| Item | Decision |
|---|---|
| Plain labels | Never bare `T1`…`T8` to humans — `Turn N: <plain name>`; optional `(TN)` after |
| Stage progress | Show `current of total` when total known |
| Options to Mohamed | Always include recommendation + short reasoning |

---

## 2. Already settled (inherited — not reopened)

Two skills; voice never in bank; taxonomy at `profile/skills.yaml`; YAML structure / MD narrative; §3.2 skeleton; provenance mandatory; status set; strength/recency on links; differentiator→bank boundary; gui/tui + glyphs; T1 owned by bank; no telemetry; per-URL OK; no fabrication; defense in depth = validate → Turn 1 → matching floors → composition grounding.

---

## 3. Item lifecycle (bank)

```
pending → destyled → awaiting_hitl → fact | waived | ambiguous
```

- Bulk mode: extractions enter a queue; process one Turn 1 at a time; optional Turn 6 when queue empty.
- Single-item mode: no bulk queue; same item states.
- Persist after each approved decision; run `validate_evidence.py` before write.

---

## 4. Inventory disposition

| Path | Disposition |
|---|---|
| `SKILL.md` | **Rewrite** to locks |
| `references/evidence-schema.md` | **Rewrite** (Q3/Q4/Q7 + probe_history shape) |
| `references/destyling-rules.md` | **Rewrite** (adopt structure; tighten to Q2) |
| `references/status-taxonomy.md` | **Rewrite** (align Q4) |
| `references/probe-question-bank.md` | **Rewrite** (keep idea; plain labels in instructions) |
| `references/probe-ui.md` | **Rewrite** (plain labels + progress; envelopes) |
| `assets/evidence-record-template.yaml` | **Adopt shape** (empty lists) |
| `assets/de-styling-checklist.md` | **Rewrite** (Q2 gate) |
| `assets/probe-checklist.md` | **Rewrite** |
| `assets/fixtures/ok.yaml` | **Add** (Q11) |
| `assets/fixtures/bad-missing-source.yaml` | **Add** (Q11) |
| `scripts/validate_evidence.py` | **Rewrite** (Q8 hard-fail vs warn) |
| `PROVISIONAL.md` | **Delete** after build |

Build roots (identical content):

- `career/.cursor/skills/evidence-bank/` (install target)
- `architecture-v1.0/.cursor/skills/evidence-bank/` (Architecture File tree mirror)

---

## 5. Definition of done (session)

- [x] This decision record on disk
- [x] Skill tree built/replaced at both roots
- [x] Turn 3 / Turn 6 body+decisions identical to cv-creation
- [x] `validate_evidence.py` matches Q8; smoke on fixtures documented
- [x] Handoff status → design closed / built
- [x] Architecture File evidence-bank sections updated; provisional banner cleared for bank
