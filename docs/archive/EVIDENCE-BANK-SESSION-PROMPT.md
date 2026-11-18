# Bootstrap prompt — Evidence-Bank design session

Copy everything inside the code block below into a **new** Cursor chat. Attach the files listed in the prompt.

---

````markdown
# Evidence-Bank skill — design then build

You are starting a **dedicated** session for the `evidence-bank` Cursor skill only.

## First actions

1. Read, in order:
   - `/home/mohamed/Projects/application-skills/EVIDENCE-BANK-DESIGN-HANDOFF.md`
   - The read list inside that file §2 (handoff slices + provisional tree + cv-creation T3/T6 only)
2. Do **not** treat `/home/mohamed/Projects/application-skills/architecture-v1.0/.cursor/skills/evidence-bank/` as approved SoT. It is **PROVISIONAL** (inferred during Architecture File generation without a design cluster).
3. Restate in one short paragraph: goal, out-of-scope, and the “do not reopen” list.
4. Ask me to say `go` before the first design question.
5. Stop.

## Working method

- **Design before build.** One review question per turn (options table). Wait for my letter/answer.
- After all design locks: write `EVIDENCE-BANK-DECISIONS.md`, then build/replace the evidence-bank skill on disk, then patch only evidence-bank parts of `CV-SYSTEM-ARCHITECTURE-v1.0.md`.
- Keep **T3** and **T6** verbatim-identical with `cv-creation` unless we explicitly jointly edit both.
- Do not reopen cv-creation Clusters 1–3, Q1–Q7, composition/export/ATS locks.
- Adaptive Clarity: lead with the answer; no dumps. Quality before speed — if a source is thin, say so and ask; do not invent a full skill from gaps.
- Ownership: for multi-file builds, explain-back ≥3 state mutations before calling done.

## When I say `go`

Start Design Q1 from `EVIDENCE-BANK-DESIGN-HANDOFF.md` §5 (or propose a better first question if §5 order is wrong — one sentence why, then ask).

Type `read` acknowledgment pattern only if useful; otherwise follow steps 1–5 above.
````
