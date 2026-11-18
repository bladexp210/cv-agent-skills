# Full install prompt (Agent Skills + Python deps)

**Who this is for:** You use an Agent Skills client and want reliable scripts (validate, export, views).

**How to use:** Copy everything inside the box below. Paste it into a new chat with your agent. Point the agent at this repo (clone or local path) if it cannot see the files yet.

---

## Copy-paste block

```
You are installing the CV Agent Skills from this repository (Agent Skills open standard).

## Goal
Install evidence-bank and cv-creation so I can maintain a de-styled evidence bank and run a per-application CV pipeline with bundled scripts.

## Rules
1. Use YOUR client's skill-install path and docs. Do not hardcode Cursor-only paths. If unsure, check your product docs for where Agent Skills folders go, then tell me the path you will use before copying.
2. Career / personal data stays outside this repo. Do not invent facts. Prefer fixtures for smoke tests.
3. Prefer bundled scripts under each skill's `scripts/` folder over reinventing validation, views, bootstrap, or export.
4. When a step needs Python packages, install them. Do not skip deps on this full path. Ask me before any heavy or surprising install (system packages, WeasyPrint system libs, global pip). Guide me through permission / approval prompts in plain language.

## Steps (do in order)

### 1) Locate install target
- Find where this client loads Agent Skills from.
- Confirm with me: skill root path you will write to.

### 2) Install both skills
- Copy (or link) from this repo:
  - `skills/evidence-bank/` → `<skill-root>/evidence-bank/`
  - `skills/cv-creation/` → `<skill-root>/cv-creation/`
- Keep folder names and `SKILL.md` files intact.

### 3) Confirm skills load
- Reload or restart skills if your client requires it.
- Confirm both skills appear / load (list skills or open each `SKILL.md`).
- Report: evidence-bank = OK / FAIL; cv-creation = OK / FAIL.

### 4) Python deps (full path — install when needed)
- Base (YAML scripts): install from repo `requirements.txt` (PyYAML), or `pip install pyyaml` if that file is missing.
- Export (DOCX / PDF): when the user runs export or `check-env` needs them, install from `requirements-export.txt` (python-docx, weasyprint), or the same packages via pip.
- If WeasyPrint needs OS libraries, explain what to install and wait for my OK.
- Prefer a project/venv install when possible; say what you ran.

### 5) Smoke check (prefer scripts)
- Run evidence-bank validate on the fixture, for example:
  `python skills/evidence-bank/scripts/validate_evidence.py skills/evidence-bank/assets/fixtures/ok.yaml`
  (adjust path if cwd differs).
- If that fails for missing PyYAML, install deps (step 4), then retry.
- Do not rewrite the validator unless the script is broken.

### 6) Hand off
Tell me in short bullets:
- Skill install path used
- Both skills load? (yes/no)
- Python packages installed (names)
- Smoke validate result
- Next suggested command (e.g. bootstrap career tree, or start evidence-bank / cv-creation with my data elsewhere)

Stop after the handoff unless I ask to continue.
```

---

## Notes for humans

| Topic | Detail |
| :--- | :--- |
| vs Lite | Lite installs skills only and asks before deps. Full installs deps when a step needs them. |
| Scripts | `evidence-bank/scripts/validate_evidence.py`; `cv-creation/scripts/` (bootstrap, validate, views, export). |
| Data | Put real career YAML in your private project, not in this public repo. |
