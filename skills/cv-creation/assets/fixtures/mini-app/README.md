# Mini-app fixture

Self-contained mini career root for deterministic tests.

- `profile/` — identity, evidence, skills, export-style
- `applications/acme-de-2026-01-01/` — composition + draft + matching

Suggested checks (run from this directory):

```bash
python -m py_compile ../../../scripts/*.py
python ../../../../evidence-bank/scripts/validate_evidence.py profile/evidence.yaml
python ../../../scripts/validate_application.py --style profile/export-style.yaml --skills profile/skills.yaml --composition applications/acme-de-2026-01-01/composition.yaml --draft applications/acme-de-2026-01-01/draft.md --evidence profile/evidence.yaml --matching applications/acme-de-2026-01-01/matching.yaml --identity profile/identity.yaml
python ../../../scripts/export_resume.py --formats md,html --career-root . applications/acme-de-2026-01-01
python ../../../scripts/regenerate_views.py applications/acme-de-2026-01-01
python ../../../scripts/verify_views.py applications/acme-de-2026-01-01
```
