# Evidence-Bank Skill — Design Handoff

**Status:** design closed / built  
**Updated:** 2026-11-18  
**Parent system:** CV System (application-skills)  
**Decision record:** `EVIDENCE-BANK-DECISIONS.md`  
**Communication:** `COMMUNICATION_CONTRACT.md`  
**Rule:** Evidence-bank content under `career/.cursor/skills/evidence-bank/` (mirrored at `architecture-v1.0/.cursor/skills/evidence-bank/`) is **design-locked**. Do not treat older provisional drafts as SoT.

---

## 0. How to use this file

Historical bootstrap for the design session. New work starts from `EVIDENCE-BANK-DECISIONS.md` + the built skill tree.

---

## 1. Goal (achieved)

Design and build the `evidence-bank` Cursor skill so it is explicitly specified, then replace provisional files and update the Architecture File inventory for evidence-bank only.

---

## 2. Read list (disk SoT)

| # | Path | Why |
|---|---|---|
| 1 | `EVIDENCE-BANK-DECISIONS.md` | Locked decisions |
| 2 | `career/.cursor/skills/evidence-bank/` | Built skill |
| 3 | `CV-SYSTEM-HANDOFF-v0.2.md` settled slices | Inherited constraints |
| 4 | `COMMUNICATION_CONTRACT.md` | Plain labels + progress |

---

## 3. Already settled + session locks

See `EVIDENCE-BANK-DECISIONS.md` §§1–2.

---

## 6. Build target (done)

```
career/.cursor/skills/evidence-bank/
architecture-v1.0/.cursor/skills/evidence-bank/   # mirror
```

---

## 7. Definition of done

- [x] Decision record on disk (`EVIDENCE-BANK-DECISIONS.md`)
- [x] Every evidence-bank inventory path has intentional content
- [x] T3/T6 still identical across both skills
- [x] `validate_evidence.py` matches locked schema; smoke fixtures documented
- [x] This handoff status updated; Architecture File evidence-bank no longer labeled provisional

---

## 8. Pointers

- Install / SoT skill: `/home/mohamed/Projects/application-skills/career/.cursor/skills/evidence-bank/`
- Architecture mirror: `/home/mohamed/Projects/application-skills/architecture-v1.0/.cursor/skills/evidence-bank/`
