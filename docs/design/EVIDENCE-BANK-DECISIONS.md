# Evidence-Bank — Decision Record

**Status:** design closed (amended 2026-11-19 — Q12/Q13)  
**Closed:** 2026-11-18  
**Amended:** 2026-11-19 (ingest scope gate: Turn 0 + Turn 6 Coverage)  
**Parent (archived):** `docs/archive/EVIDENCE-BANK-DESIGN-HANDOFF.md`  
**Communication:** `COMMUNICATION_CONTRACT.md`  
**Skill SoT:** `skills/evidence-bank/`

This record is the design SoT for `evidence-bank`. Skill files live under `skills/evidence-bank/`.

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
| Options to the operator | Always include recommendation + short reasoning |

### Mid-session ingest-scope locks (2026-11-19 — do not reopen Q1–Q11)

| Q | Topic | Decision |
|---|---|---|
| Q12 | Ingest scope (Turn 0) | Before any **bulk** enqueue (first pass or later pass), run **Turn 0: Ingest scope**. Hard-fail for agents: do not write `queue.yaml` / start Turn 1 until Turn 0 is decided for that pass. **Body must include:** ingest surfaces used; proposed mode (`full` \| `curated`); roles/experiences **in** with candidate counts; roles/items **deferred** with one-line reasons; recommendation + short reasoning. **Decisions (exact labels):** `approve full` / `approve curated` / `revise` / `defer pass`. **Grain:** G1 always. If operator chooses `approve curated` or `revise`, show G2 candidate short-list (one line per proposed fact: role · fact stub · source id) and require **`approve queue`** / **`revise queue`** before enqueue. **Default recommendation:** `approve full` for remaining destyled candidates from the named surfaces (unless operator already scoped otherwise). Single-item / route-to-bank / Turn 3 probes: **no** Turn 0. |
| Q13 | Turn 6 coverage rollup | Extend the shared Turn 6 body (both skills, verbatim) with a **Coverage** block: (1) Bulk ingest / ingest revise — included roles+counts vs deferred/left-out vs source inventory (so `n/n` never means “whole warehouse done”); (2) Application stage gates — `Coverage: N/A (not bulk ingest)`. Decisions stay: `approve` / `revise` / `resolve` / `accept`. |

---

## 2. Already settled (inherited — not reopened)

Two skills; voice never in bank; taxonomy at `profile/skills.yaml`; YAML structure / MD narrative; §3.2 skeleton; provenance mandatory; status set; strength/recency on links; differentiator→bank boundary; gui/tui + glyphs; T1 owned by bank; no telemetry; per-URL OK; no fabrication; defense in depth = validate → Turn 1 → matching floors → composition grounding.

---

## 3. Item lifecycle (bank)

```
pending → destyled → awaiting_hitl → fact | waived | ambiguous
```

- Bulk mode: destyle → **Turn 0: Ingest scope** (Q12) → enqueue approved set → process one Turn 1 at a time; optional Turn 6 when queue empty (Coverage per Q13).
- Single-item mode: no bulk queue; same item states; **no** Turn 0.
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

**Repo skill root (2026-11-18 layout A):** `skills/evidence-bank/`  
**Install target:** copy into a career project’s Agent Skills folder (default `.agents/skills/evidence-bank/`; `.cursor/skills/` also fine if that is the client path).

---

## 5. Definition of done (session)

- [x] This decision record on disk
- [x] Skill tree built under `skills/evidence-bank/` (layout A: single SoT)
- [x] Turn 3 / Turn 6 body+decisions identical to cv-creation
- [x] `validate_evidence.py` matches Q8; smoke on fixtures documented
- [x] Design closed; thin architecture inventory at `docs/architecture/CV-SYSTEM-ARCHITECTURE.md`
