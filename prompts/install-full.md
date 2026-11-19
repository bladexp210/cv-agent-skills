# Full install prompt (Agent Skills + Python deps)

**Who this is for (situation):** You have an Agent Skills client **and** you are willing to install Python, Python libraries, and related developer tools on your machine.

**End result:** Skills installed + **repeatable** validate/export via local scripts (validate, export, views).

**How to use:** Copy everything inside the box below. Paste it into a new chat in your **career** project (or wherever skills should be installed). You do not need the skills repo open in the workspace.

**Default source:** public GitHub repo  
`https://github.com/bladexp210/cv-agent-skills`

**Recommendation:** prefer **Full** when you have a skills client and can install the Python stack; use Lite instead if you refuse or cannot install those deps.

---

## Copy-paste block

```
You are installing the CV Agent Skills (Agent Skills open standard) into this project.

## Source of skill files (important)
- DEFAULT: get skills from the public GitHub repo https://github.com/bladexp210/cv-agent-skills
  (clone, sparse checkout, or download — your choice; prefer a fresh clone into a temp dir if needed).
- Do NOT use a random local folder such as application-skills, or any sibling project, unless I explicitly give you that path.
- If both a local checkout and GitHub are available, still prefer GitHub unless I say otherwise.
- Temporary fetch only: if you clone/download into a temp dir to obtain the pack, you MUST delete that temp dir after skills are copied (required cleanup). Do not delete a path I explicitly named as my permanent local checkout.

## Goal
Install evidence-bank and cv-creation so I can maintain a de-styled evidence bank and run a per-application CV pipeline with bundled scripts.

## Rules
1. Use YOUR client's skill-install path and docs. Do not hardcode Cursor-only paths. Common Agent Skills locations include `.cursor/skills/` and `.agents/skills/`; DeepSeek Harness (`dsh`) profiles may use a project skills dir — discover via profile/docs (e.g. `dsh --profile <name> --dump-config`), not a guessed path. If unsure, check your product docs for where Agent Skills folders go, then tell me the path you will use before copying.
2. At start and in the final handoff, report **client name** (e.g. Cursor, DeepSeek Harness / `dsh`, other) and the **skills path** you used. After install, walk the copyable smoke checklist in the skills pack’s `docs/portability.md` (or summarize each checkbox if that file is not in the workspace).
3. Career / personal data stays in THIS project (or another path I name). Do not invent facts. Prefer fixtures from the skills pack for smoke tests.
4. Prefer bundled scripts under each skill's `scripts/` folder over reinventing validation, views, bootstrap, or export.
5. When a step needs Python packages, install them. Do not skip deps on this full path. Ask me before any heavy or surprising install (system packages, WeasyPrint system libs, global pip). Guide me through permission / approval prompts in plain language.

## Steps (do in order)

### 1) Obtain the skills pack
- Fetch from https://github.com/bladexp210/cv-agent-skills (default).
- Confirm the pack contains `skills/evidence-bank/` and `skills/cv-creation/`.
- Report the source you used (GitHub URL + ref/commit if known, or the explicit local path I gave you).

### 2) Locate install target
- Name the client (Cursor, DeepSeek Harness / `dsh`, or other).
- Find where this client loads Agent Skills from (for this project). Do not assume `.cursor/skills/` only.
- Confirm with me: skill root path you will write to.

### 3) Install both skills
- Copy (or link) from the pack:
  - `skills/evidence-bank/` → `<skill-root>/evidence-bank/`
  - `skills/cv-creation/` → `<skill-root>/cv-creation/`
- Keep folder names and `SKILL.md` files intact.

### 3b) Cleanup temporary fetch (required when you used a temp dir)
- If you cloned or unpacked the pack into a temporary directory, delete that directory now.
- Confirm cleanup in one line (path removed), or state “no temp dir — used explicit permanent path.”
- Never delete my career project, skill install target, or a permanent checkout path I gave you.

### 4) Confirm skills load
- Reload or restart skills if your client requires it.
- Confirm both skills appear / load (list skills or open each `SKILL.md`).
- Report: evidence-bank = OK / FAIL; cv-creation = OK / FAIL.

### 5) Python deps (full path — install when needed)
- Base (YAML scripts): install from pack `requirements.txt` (PyYAML), or `pip install pyyaml` if that file is missing.
- Export (DOCX / PDF): when the user runs export or `check-env` needs them, install from `requirements-export.txt` (python-docx, weasyprint), or the same packages via pip.
- If WeasyPrint needs OS libraries, explain what to install and wait for my OK.
- Prefer a project/venv install when possible; say what you ran.

### 6) Smoke check (prefer scripts)
- Run evidence-bank validate on the fixture from the installed skill or the pack, for example:
  `python <skill-root>/evidence-bank/scripts/validate_evidence.py <skill-root>/evidence-bank/assets/fixtures/ok.yaml`
  (adjust paths as needed).
- If that fails for missing PyYAML, install deps (step 5), then retry.
- Do not rewrite the validator unless the script is broken.

### 7) Bootstrap the career project (you do this — do not ask me to DIY)
- Run the installed skill script yourself (do not tell me to run mkdir/bootstrap by hand):
  `python <skill-root>/cv-creation/scripts/bootstrap_career.py .`
  (use this project root; adjust if I named another career root).
- If the tree already exists, still run bootstrap so missing pieces (especially `inbox/`) are created; it skips existing files safely.
- If the script cannot run, create the same layout yourself: `profile/`, `applications/`, `_skill_state/`, and `inbox/resumes/`, `inbox/linkedin/`, `inbox/from-links/` plus `inbox/README.md` from the skill asset `inbox.README.md`.
- After bootstrap, set `paths.skills_dir` in `career.config.yaml` to the skill root you actually used (relative to the career project, e.g. `.agents/skills` or `.cursor/skills`). Do not leave a mismatched default.
- After it finishes, tell me briefly what was created or already present. Do not stop at “you should create folders.”

### 8) Hand off
Tell me in short bullets:
- Client name + skills path used
- Source used (GitHub vs explicit local path)
- Temp fetch cleaned up? (yes + path removed / n/a permanent path)
- Both skills load? (yes/no)
- Python packages installed (names)
- Smoke validate result (and portability checklist status if you ran it — see pack `docs/portability.md`)
- Career bootstrap / inbox paths ready
- Where to drop files: `inbox/resumes/`, `inbox/linkedin/`, `inbox/from-links/`
- Offer next step YOU can do: e.g. “Drop your CV/LinkedIn into inbox, or say ingest if files are already there” — then wait for my reply (do not invent career facts).
```

---

## Notes for humans

| Topic | Detail |
| :--- | :--- |
| Source | Default = GitHub `bladexp210/cv-agent-skills`. Pass a local path only when you mean to. |
| vs Lite | Lite installs skills only and asks before deps. Full installs deps when a step needs them. |
| Portability | Agent must report client name + skills path. Checklist: [`docs/portability.md`](../docs/portability.md). |
| Scripts | `evidence-bank/scripts/validate_evidence.py`; `cv-creation/scripts/` (bootstrap, validate, views, export). |
| Data | Put real career YAML in your private project, not in the public skills repo. |
