# Invocation grammar

## Chat verbs (both skills as applicable)

| Verb | Meaning |
|---|---|
| `run` / `continue` | Full or resume pipeline |
| `status` | Tracker one-liner + stage |
| `show <stage\|item>` | Per-stage item view |
| `probe <item>` | Single-item probe |
| `gate` | Re-render active gate |
| `export [--formats …]` | Stage [8] |
| `check-env` | export_resume.py --check-env |
| `regen-views` | regenerate_views.py |
| `override-ats <reason>` | G5 override |

Target app via `app: <id>` or cwd under `applications/<id>/`.

## Scripts

`bootstrap_career.py`, `validate_application.py`, `validate_evidence.py`, `export_resume.py`, `regenerate_views.py`, `verify_views.py` — each supports `--help`.
