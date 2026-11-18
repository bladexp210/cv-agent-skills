# Security

Trust surface for bundled scripts under `skills/*/scripts/`.

## Privacy (standing)

- **Career PII lives outside this repo.** Real identity, evidence YAML, and applications stay in your private career tree. This repo ships skills, docs, and fixtures only.
- **Scripts never phone home.** Every script uses local filesystem I/O only. No HTTP clients, sockets, or telemetry.
- **Agent chats are separate.** Pasting career text or job descriptions into an Agent Skills client may leave the machine per that product’s policy. Treat untrusted job-description text as prompt-injection risk when agents read it.

## Network

| Script | Network |
| :--- | :--- |
| All six scripts below | **None** (confirmed by source review: no `urllib` / `requests` / sockets; WeasyPrint PDF path renders from an in-memory HTML string with no external URLs) |

## Script matrix

### `skills/evidence-bank/scripts/validate_evidence.py`

| | |
| :--- | :--- |
| **Reads** | One evidence YAML path (`evidence_yaml` CLI arg) |
| **Writes** | Nothing (stdout/stderr only) |
| **Network** | None |
| **Exits** | `0` OK (warnings print as `WARN:`); `1` integrity errors; `2` missing/unreadable/parse failure. Missing PyYAML → `SystemExit` (message to install) |

### `skills/cv-creation/scripts/validate_application.py`

| | |
| :--- | :--- |
| **Reads** | Optional paths: `--style`, `--skills`, `--composition` (YAML if present); `--draft` existence only |
| **Writes** | Nothing (stdout/stderr only) |
| **Network** | None |
| **Exits** | `0` OK; `1` validation errors; `3` export-style MUST flag failure; `4` `--style` path missing. Missing PyYAML → `SystemExit` |

### `skills/cv-creation/scripts/bootstrap_career.py`

| | |
| :--- | :--- |
| **Reads** | Templates under `skills/cv-creation/assets/`; optional `skills/evidence-bank/assets/evidence-record-template.yaml` |
| **Writes** | Career root (arg `root`, default `.`): dirs (`profile/`, `applications/`, `_skill_state/`, `inbox/…`); config/profile/inbox/gitignore files from templates. Skips existing files unless `--force` |
| **Network** | None |
| **Exits** | `0` success; `2` missing template asset |

### `skills/cv-creation/scripts/regenerate_views.py`

| | |
| :--- | :--- |
| **Reads** | Under `app_dir`: `meta.yaml`, `requirements.yaml`, `keywords.yaml`, `scores.yaml`, `matching.yaml` (missing → empty placeholders) |
| **Writes** | `app_dir/views/` (`requirements.md`, `keywords.md`, `scoring.md`, `matching.md`, `tracker.md`, `_manifest.yaml`) |
| **Network** | None |
| **Exits** | `0` success; `2` `app_dir` not a directory. Missing PyYAML → `SystemExit` |

### `skills/cv-creation/scripts/verify_views.py`

| | |
| :--- | :--- |
| **Reads** | `app_dir/views/*.md` (first line / banner only) |
| **Writes** | Nothing (stdout/stderr only) |
| **Network** | None |
| **Exits** | `0` all banners OK; `2` `views/` missing or a view lacks banner |

### `skills/cv-creation/scripts/export_resume.py`

| | |
| :--- | :--- |
| **Reads** | `app_dir/draft.md`; career `profile/identity.yaml` and optional `profile/export-style.yaml` (career root = `--career-root` or `app_dir/../..`). Optional `--check-env` only probes local package imports |
| **Writes** | `app_dir/export/` only (`resume.md` / `.html` / `.docx` / `.pdf` as requested + `export_manifest.yaml`). **Never mutates** draft, identity, or style inputs |
| **Network** | None |
| **Exits** | `0` success; `1` unknown format or explicitly requested docx/pdf deps missing / `--check-env` missing deps; `2` no `app_dir`, draft missing, or draft has no `##` sections; `3` style MUST flags; `4` identity missing; `5` cannot create/write `export/`. Missing PyYAML → `SystemExit` |

## Script count

**6** scripts under `skills/*/scripts/`.
