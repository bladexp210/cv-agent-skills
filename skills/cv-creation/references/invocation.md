# Invocation grammar

Shared by **evidence-bank** and **cv-creation**. Continuity obligations: `references/continuity.md` (identical in both skills).

## Obligations (automatic — not user commands)

Agents must do these without the user asking:

| Obligation | When |
| :--- | :--- |
| Write domain SoT files | After every accepted decision / stage write |
| Update `_skill_state/LIVE.yaml` + `STATUS.md` | After every meaningful step |
| Mirror LIVE into long-term memory **if tools exist** | Same turn as LIVE write |
| Validate after evidence persist | evidence-bank (and when bank files change) |
| Plain Turn labels + `current of total` | Every HITL / queue turn |
| Recompute from disk on resume | `continue` / “resume” / new chat pickup |

Do **not** invent user commands for: sync-memory, update-live, validate-after-save.

## User intent (plain language + optional aliases)

| Intent | Plain examples | Alias (optional) |
| :--- | :--- | :--- |
| Start or resume pipeline | “continue”, “resume ingest”, “keep going” | `run` / `continue` |
| Where are we? | “where are we?”, “status” | `status` |
| Inspect without advancing | “show matching”, “show ev_010” | `show <stage\|item>` |
| Open a probe | “probe the Airflow gap” | `probe <item>` |
| Re-show active gate | “show the gate again” | `gate` |
| Export CV | “export PDF and DOCX” | `export [--formats …]` |
| Check export tools | “check export environment” | `check-env` |
| Rebuild views | “regenerate views” | `regen-views` |
| ATS exception | “override ATS because …” | `override-ats <reason>` |

Prefer plain phrases for ESL users. Aliases remain valid for power users and old chats.

Target app via `app: <id>` or cwd under `applications/<id>/`.

## Scripts

`bootstrap_career.py`, `validate_application.py`, `validate_evidence.py`, `export_resume.py`, `regenerate_views.py`, `verify_views.py` — each supports `--help`. Prefer scripts when they run; do not ask the user to run them by hand when you can run them.
