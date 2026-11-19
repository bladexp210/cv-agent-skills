# CV System — Architecture inventory (v1.0)

> **Skill SoT:** `skills/` (not embedded here).  
> **Design SoT:** `docs/design/`.  
> Full historical embed archived at `docs/archive/CV-SYSTEM-ARCHITECTURE-v1.0-full-embed.md`.

**Updated:** 2026-11-19 (quick-start / Makefile / adversarial brief; dsh web-mode smoke report)

Install: copy `skills/evidence-bank` and `skills/cv-creation` into the Agent Skills client’s skills folder (examples: `.cursor/skills/`, `.agents/skills/`; discover per client — see `docs/portability.md`). Do not invent files beyond this inventory.

## A. Build target

### Folder tree

Repo root (trust / CI / tests) plus skill SoT under `skills/`. Paths under `skills/` stay relative to that folder (same as before).

```
SECURITY.md
Makefile
requirements-dev.txt
.github/workflows/ci.yml
docs/portability.md
docs/portability-smoke-dsh-web.md
docs/quick-start.md
prompts/adversarial-scripts-pass.md
tests/test_validate_evidence.py
tests/test_validate_application.py
tests/test_validate_application_grounding.py
tests/test_export_resume_md_html.py
tests/test_export_pdf_security.py
tests/test_evidence_schema_json.py
skills/
  cv-creation/SKILL.md
  cv-creation/assets/application-meta.template.yaml
  cv-creation/assets/ats-rules.template.yaml
  cv-creation/assets/career.config.template.yaml
  cv-creation/assets/checkpoint.template.yaml
  cv-creation/assets/composition.template.yaml
  cv-creation/assets/export-style.template.yaml
  cv-creation/assets/fixtures/grounding-bad/cited-not-listed/composition.yaml
  cv-creation/assets/fixtures/grounding-bad/draft-mismatch/composition.yaml
  cv-creation/assets/fixtures/grounding-bad/draft-mismatch/draft.md
  cv-creation/assets/fixtures/grounding-bad/empty-ev-ids/composition.yaml
  cv-creation/assets/fixtures/grounding-bad/missing-ev/composition.yaml
  cv-creation/assets/fixtures/grounding-bad/non-fact-status/composition.yaml
  cv-creation/assets/fixtures/grounding-bad/non-fact-status/evidence.yaml
  cv-creation/assets/fixtures/grounding-bad/skill-not-on-evidence/composition.yaml
  cv-creation/assets/fixtures/grounding-bad/uncovered/composition.yaml
  cv-creation/assets/fixtures/mini-app/README.md
  cv-creation/assets/fixtures/mini-app/applications/acme-de-2026-01-01/ats-check.yaml
  cv-creation/assets/fixtures/mini-app/applications/acme-de-2026-01-01/audit.md
  cv-creation/assets/fixtures/mini-app/applications/acme-de-2026-01-01/composition.yaml
  cv-creation/assets/fixtures/mini-app/applications/acme-de-2026-01-01/draft.md
  cv-creation/assets/fixtures/mini-app/applications/acme-de-2026-01-01/export/export_manifest.yaml
  cv-creation/assets/fixtures/mini-app/applications/acme-de-2026-01-01/export/resume.html
  cv-creation/assets/fixtures/mini-app/applications/acme-de-2026-01-01/export/resume.md
  cv-creation/assets/fixtures/mini-app/applications/acme-de-2026-01-01/keywords.yaml
  cv-creation/assets/fixtures/mini-app/applications/acme-de-2026-01-01/matching.yaml
  cv-creation/assets/fixtures/mini-app/applications/acme-de-2026-01-01/meta.yaml
  cv-creation/assets/fixtures/mini-app/applications/acme-de-2026-01-01/requirements.yaml
  cv-creation/assets/fixtures/mini-app/applications/acme-de-2026-01-01/scores.yaml
  cv-creation/assets/fixtures/mini-app/applications/acme-de-2026-01-01/views/_manifest.yaml
  cv-creation/assets/fixtures/mini-app/applications/acme-de-2026-01-01/views/keywords.md
  cv-creation/assets/fixtures/mini-app/applications/acme-de-2026-01-01/views/matching.md
  cv-creation/assets/fixtures/mini-app/applications/acme-de-2026-01-01/views/requirements.md
  cv-creation/assets/fixtures/mini-app/applications/acme-de-2026-01-01/views/scoring.md
  cv-creation/assets/fixtures/mini-app/applications/acme-de-2026-01-01/views/tracker.md
  cv-creation/assets/fixtures/mini-app/profile/evidence.yaml
  cv-creation/assets/fixtures/mini-app/profile/export-style.yaml
  cv-creation/assets/fixtures/mini-app/profile/identity.yaml
  cv-creation/assets/fixtures/mini-app/profile/skills.yaml
  cv-creation/assets/gitignore.template
  cv-creation/assets/identity.template.yaml
  cv-creation/assets/inbox.README.md
  cv-creation/assets/jd.template.md
  cv-creation/assets/norms.template.md
  cv-creation/assets/onboarding-checklist.md
  cv-creation/assets/tracker.template.md
  cv-creation/assets/voice.template.md
  cv-creation/references/ats-baseline-rules.md
  cv-creation/references/ats-check.md
  cv-creation/references/checkpoint-schema.md
  cv-creation/references/composition-rules.md
  cv-creation/references/continuity.md
  cv-creation/references/differentiator-rules.md
  cv-creation/references/export-pipeline.md
  cv-creation/references/hitl-gate-catalogue.md
  cv-creation/references/interaction-mode.md
  cv-creation/references/invocation.md
  cv-creation/references/matching-rules.md
  cv-creation/references/norms-guide.md
  cv-creation/references/scoring-rubric.md
  cv-creation/references/state-machine.md
  cv-creation/references/taxonomy-mechanics.md
  cv-creation/references/ui-turn-types.md
  cv-creation/references/voice-guide.md
  cv-creation/scripts/bootstrap_career.py
  cv-creation/scripts/export_resume.py
  cv-creation/scripts/regenerate_views.py
  cv-creation/scripts/validate_application.py
  cv-creation/scripts/verify_views.py
  evidence-bank/SKILL.md
  evidence-bank/assets/de-styling-checklist.md
  evidence-bank/assets/evidence-record-template.yaml
  evidence-bank/assets/evidence.schema.json
  evidence-bank/assets/probe-checklist.md
  evidence-bank/assets/fixtures/ok.yaml
  evidence-bank/assets/fixtures/bad-missing-source.yaml
  evidence-bank/references/continuity.md
  evidence-bank/references/destyling-rules.md
  evidence-bank/references/evidence-schema.md
  evidence-bank/references/first-run-briefing.md
  evidence-bank/references/probe-question-bank.md
  evidence-bank/references/probe-ui.md
  evidence-bank/references/status-taxonomy.md
  evidence-bank/scripts/validate_evidence.py
```

### Purpose per file (one sentence)

| Path | Purpose |
|---|---|
| `SECURITY.md` | Script I/O / network / exit matrix and privacy boundary for this repo. |
| `Makefile` | Solo-operator targets: deps, pytest, architecture smoke (`make smoke` / `make check`). |
| `requirements-dev.txt` | Dev-only pytest and jsonschema pins for local tests and CI. |
| `.github/workflows/ci.yml` | GitHub Actions workflow: pytest plus architecture smoke. |
| `docs/portability.md` | Multi-client matrix, copyable smoke checklist, Results for Cursor and DeepSeek Harness (`dsh`, headless + web). |
| `docs/portability-smoke-dsh-web.md` | Point-in-time record of the `dsh` **web-mode** portability smoke at `v0.8.0`: resolved skills path, checklist 1–7 evidence, web-mode notes, cleanup confirmation. |
| `docs/quick-start.md` | Five-minute human overview: paths, smoke, known limitations. |
| `prompts/adversarial-scripts-pass.md` | Paste-ready scoped red-team brief for a different model (export / validate scripts). |
| `tests/test_validate_evidence.py` | Pytest for validate_evidence against bank fixtures. |
| `tests/test_validate_application.py` | Pytest for validate_application against mini-app. |
| `tests/test_validate_application_grounding.py` | Pytest for G4 grounding OK + negative fixtures. |
| `tests/test_export_resume_md_html.py` | Pytest for md/html export on a temp mini-app copy. |
| `tests/test_export_pdf_security.py` | Pytest for page/margin allowlist and deny-all PDF url_fetcher. |
| `tests/test_evidence_schema_json.py` | Pytest that fixtures match evidence.schema.json. |
| `cv-creation/SKILL.md` | CV-creation skill entrypoint, stages, and shared T3/T6 contract. |
| `cv-creation/assets/application-meta.template.yaml` | Copy-ready template or checklist asset. |
| `cv-creation/assets/ats-rules.template.yaml` | Copy-ready template or checklist asset. |
| `cv-creation/assets/career.config.template.yaml` | Copy-ready template or checklist asset. |
| `cv-creation/assets/checkpoint.template.yaml` | Copy-ready template or checklist asset. |
| `cv-creation/assets/composition.template.yaml` | Scaffold for composition.yaml on app create. |
| `cv-creation/assets/export-style.template.yaml` | Copy-ready template or checklist asset. |
| `cv-creation/assets/fixtures/grounding-bad/cited-not-listed/composition.yaml` | G4 negative: cited ev_id missing from grounding.cited_ev_ids. |
| `cv-creation/assets/fixtures/grounding-bad/draft-mismatch/composition.yaml` | G4 negative: composition paired with draft missing bullet text. |
| `cv-creation/assets/fixtures/grounding-bad/draft-mismatch/draft.md` | G4 negative draft for draft-mismatch. |
| `cv-creation/assets/fixtures/grounding-bad/empty-ev-ids/composition.yaml` | G4 negative: empty ev_ids on a bullet (CI smoke fail fixture). |
| `cv-creation/assets/fixtures/grounding-bad/missing-ev/composition.yaml` | G4 negative: cited ev_id absent from evidence.yaml. |
| `cv-creation/assets/fixtures/grounding-bad/non-fact-status/composition.yaml` | G4 negative: composition citing non-fact evidence. |
| `cv-creation/assets/fixtures/grounding-bad/non-fact-status/evidence.yaml` | G4 negative evidence with non-fact status. |
| `cv-creation/assets/fixtures/grounding-bad/skill-not-on-evidence/composition.yaml` | G4 negative: skill_id not linked via evidence_skills. |
| `cv-creation/assets/fixtures/grounding-bad/uncovered/composition.yaml` | G4 negative: grounding.uncovered non-empty. |
| `cv-creation/assets/fixtures/mini-app/README.md` | Deterministic CI fixture data. |
| `cv-creation/assets/fixtures/mini-app/applications/acme-de-2026-01-01/ats-check.yaml` | Deterministic CI fixture data. |
| `cv-creation/assets/fixtures/mini-app/applications/acme-de-2026-01-01/audit.md` | Deterministic CI fixture data. |
| `cv-creation/assets/fixtures/mini-app/applications/acme-de-2026-01-01/composition.yaml` | Deterministic CI fixture data. |
| `cv-creation/assets/fixtures/mini-app/applications/acme-de-2026-01-01/draft.md` | Deterministic CI fixture data. |
| `cv-creation/assets/fixtures/mini-app/applications/acme-de-2026-01-01/export/export_manifest.yaml` | Deterministic CI fixture data. |
| `cv-creation/assets/fixtures/mini-app/applications/acme-de-2026-01-01/export/resume.html` | Deterministic CI fixture data. |
| `cv-creation/assets/fixtures/mini-app/applications/acme-de-2026-01-01/export/resume.md` | Deterministic CI fixture data. |
| `cv-creation/assets/fixtures/mini-app/applications/acme-de-2026-01-01/keywords.yaml` | Deterministic CI fixture data. |
| `cv-creation/assets/fixtures/mini-app/applications/acme-de-2026-01-01/matching.yaml` | Deterministic CI fixture data. |
| `cv-creation/assets/fixtures/mini-app/applications/acme-de-2026-01-01/meta.yaml` | Deterministic CI fixture data. |
| `cv-creation/assets/fixtures/mini-app/applications/acme-de-2026-01-01/requirements.yaml` | Deterministic CI fixture data. |
| `cv-creation/assets/fixtures/mini-app/applications/acme-de-2026-01-01/scores.yaml` | Deterministic CI fixture data. |
| `cv-creation/assets/fixtures/mini-app/applications/acme-de-2026-01-01/views/_manifest.yaml` | Deterministic CI fixture data. |
| `cv-creation/assets/fixtures/mini-app/applications/acme-de-2026-01-01/views/keywords.md` | Deterministic CI fixture data. |
| `cv-creation/assets/fixtures/mini-app/applications/acme-de-2026-01-01/views/matching.md` | Deterministic CI fixture data. |
| `cv-creation/assets/fixtures/mini-app/applications/acme-de-2026-01-01/views/requirements.md` | Deterministic CI fixture data. |
| `cv-creation/assets/fixtures/mini-app/applications/acme-de-2026-01-01/views/scoring.md` | Deterministic CI fixture data. |
| `cv-creation/assets/fixtures/mini-app/applications/acme-de-2026-01-01/views/tracker.md` | Deterministic CI fixture data. |
| `cv-creation/assets/fixtures/mini-app/profile/evidence.yaml` | Deterministic CI fixture data. |
| `cv-creation/assets/fixtures/mini-app/profile/export-style.yaml` | Deterministic CI fixture data. |
| `cv-creation/assets/fixtures/mini-app/profile/identity.yaml` | Deterministic CI fixture data. |
| `cv-creation/assets/fixtures/mini-app/profile/skills.yaml` | Deterministic CI fixture data. |
| `cv-creation/assets/gitignore.template` | Career .gitignore defaults. |
| `cv-creation/assets/identity.template.yaml` | Copy-ready template or checklist asset. |
| `cv-creation/assets/inbox.README.md` | Drop-zone guide for resumes / LinkedIn / URL saves. |
| `cv-creation/assets/jd.template.md` | Copy-ready template or checklist asset. |
| `cv-creation/assets/norms.template.md` | Copy-ready template or checklist asset. |
| `cv-creation/assets/onboarding-checklist.md` | Copy-ready template or checklist asset. |
| `cv-creation/assets/tracker.template.md` | Copy-ready template or checklist asset. |
| `cv-creation/assets/voice.template.md` | Copy-ready template or checklist asset. |
| `cv-creation/references/ats-baseline-rules.md` | On-demand reference loaded by the skill. |
| `cv-creation/references/ats-check.md` | Stage [7] readiness/coverage rules (local; not employer pass probability). |
| `cv-creation/references/checkpoint-schema.md` | On-demand reference loaded by the skill. |
| `cv-creation/references/continuity.md` | LIVE/STATUS progress SoT + memory mirror (identical to evidence-bank). |
| `evidence-bank/references/continuity.md` | LIVE/STATUS progress SoT + memory mirror (identical to cv-creation). |
| `cv-creation/references/composition-rules.md` | On-demand reference loaded by the skill. |
| `cv-creation/references/differentiator-rules.md` | On-demand reference loaded by the skill. |
| `cv-creation/references/export-pipeline.md` | On-demand reference loaded by the skill. |
| `cv-creation/references/hitl-gate-catalogue.md` | On-demand reference loaded by the skill. |
| `cv-creation/references/interaction-mode.md` | Standard vs Strict HITL density (`ui.interaction_mode`). |
| `cv-creation/references/invocation.md` | Shared chat verbs and script CLIs. |
| `cv-creation/references/matching-rules.md` | On-demand reference loaded by the skill. |
| `cv-creation/references/norms-guide.md` | On-demand reference loaded by the skill. |
| `cv-creation/references/scoring-rubric.md` | On-demand reference loaded by the skill. |
| `cv-creation/references/state-machine.md` | On-demand reference loaded by the skill. |
| `cv-creation/references/taxonomy-mechanics.md` | skills.yaml add/merge/DAG rules. |
| `cv-creation/references/ui-turn-types.md` | On-demand reference loaded by the skill. |
| `cv-creation/references/voice-guide.md` | On-demand reference loaded by the skill. |
| `cv-creation/scripts/bootstrap_career.py` | Create career/ tree from templates. |
| `cv-creation/scripts/export_resume.py` | Parse draft.md and export md/html/docx/pdf. |
| `cv-creation/scripts/regenerate_views.py` | Regenerate views/* and _manifest.yaml. |
| `cv-creation/scripts/validate_application.py` | Validate style MUST flags, taxonomy, composition grounding. |
| `cv-creation/scripts/verify_views.py` | Verify GENERATED banners on views. |
| `evidence-bank/SKILL.md` | Evidence-bank skill entrypoint, ingest/lifecycle, shared T3/T6 contract. |
| `evidence-bank/assets/de-styling-checklist.md` | Copy-ready template or checklist asset. |
| `evidence-bank/assets/evidence-record-template.yaml` | Copy-ready template or checklist asset. |
| `evidence-bank/assets/evidence.schema.json` | Machine-readable JSON Schema pin for evidence.yaml (tests only). |
| `evidence-bank/assets/probe-checklist.md` | Copy-ready template or checklist asset. |
| `evidence-bank/assets/fixtures/ok.yaml` | Bank CI fixture — valid evidence.yaml. |
| `evidence-bank/assets/fixtures/bad-missing-source.yaml` | Bank CI fixture — expected validate fail. |
| `evidence-bank/references/destyling-rules.md` | On-demand reference loaded by the skill. |
| `evidence-bank/references/evidence-schema.md` | On-demand reference loaded by the skill. |
| `evidence-bank/references/first-run-briefing.md` | One-shot onboarding briefing before first Turn 1 (flagged so it does not repeat). |
| `evidence-bank/references/probe-question-bank.md` | On-demand reference loaded by the skill. |
| `evidence-bank/references/probe-ui.md` | On-demand reference loaded by the skill. |
| `evidence-bank/references/status-taxonomy.md` | On-demand reference loaded by the skill. |
| `evidence-bank/scripts/validate_evidence.py` | Validate evidence.yaml integrity (Q8 hard-fail vs warn). |

### Changes from baseline inventory

Added across design sessions:

- `evidence-bank/references/first-run-briefing.md`
- `evidence-bank/references/probe-ui.md`
- `cv-creation/references/ui-turn-types.md`
- `cv-creation/references/export-pipeline.md`
- `cv-creation/references/ats-baseline-rules.md`
- `cv-creation/references/ats-check.md`
- `cv-creation/references/taxonomy-mechanics.md`
- `cv-creation/references/invocation.md`
- `cv-creation/references/interaction-mode.md`
- `cv-creation/assets/export-style.template.yaml`
- `cv-creation/assets/ats-rules.template.yaml`
- `cv-creation/assets/composition.template.yaml`
- `cv-creation/assets/gitignore.template`
- `cv-creation/assets/inbox.README.md`
- `cv-creation/assets/fixtures/mini-app/`
- `cv-creation/assets/fixtures/grounding-bad/`
- `cv-creation/scripts/export_resume.py`

Option C trust pack (shipped):

- `SECURITY.md`
- `requirements-dev.txt`
- `.github/workflows/ci.yml`
- `tests/test_validate_evidence.py`
- `tests/test_validate_application.py`
- `tests/test_validate_application_grounding.py`
- `tests/test_export_resume_md_html.py`
- `tests/test_export_pdf_security.py`
- `tests/test_evidence_schema_json.py`
- `evidence-bank/assets/evidence.schema.json` (repo path: `skills/evidence-bank/assets/evidence.schema.json`)

Portability (docs + Wave 2 Results filled 2026-11-19 — Cursor script PASS, dsh headless PARTIAL):

- `docs/portability.md`
- `docs/portability-smoke-dsh-web.md` (dsh **web-mode** smoke at `v0.8.0`: checklist 1 partial / 2–7 pass, resolved `.agents/skills` root, web-mode notes, cleanup confirmed)

Operator convenience + adversarial brief (2026-11-19):

- `Makefile`
- `docs/quick-start.md`
- `prompts/adversarial-scripts-pass.md`

Runtime-created under `career/` (not in this tree): `inbox/` (resumes, linkedin, from-links), `_skill_state/LIVE.yaml`, `_skill_state/STATUS.md`, `applications/<app>/composition.yaml`, `applications/<app>/ats-check.yaml`, `applications/<app>/export/`, `profile/export-style.yaml`, `profile/norms/ats/*.yaml`.

Stage outputs: [6] → composition.yaml + draft.md; [7] → ats-check.yaml + audit.md; [8] reads draft.md + identity + export-style only.


## C. Install & verify

```bash
# From this repo
SKILL_ROOT=skills
MINI=$SKILL_ROOT/cv-creation/assets/fixtures/mini-app
APP=$MINI/applications/acme-de-2026-01-01
BAD=$SKILL_ROOT/cv-creation/assets/fixtures/grounding-bad

python -m py_compile $SKILL_ROOT/evidence-bank/scripts/*.py $SKILL_ROOT/cv-creation/scripts/*.py

python $SKILL_ROOT/evidence-bank/scripts/validate_evidence.py \
  $SKILL_ROOT/evidence-bank/assets/fixtures/ok.yaml
# expect OK

python $SKILL_ROOT/evidence-bank/scripts/validate_evidence.py \
  $SKILL_ROOT/evidence-bank/assets/fixtures/bad-missing-source.yaml
# expect exit 1

python $SKILL_ROOT/cv-creation/scripts/validate_application.py \
  --style $MINI/profile/export-style.yaml \
  --skills $MINI/profile/skills.yaml \
  --composition $APP/composition.yaml \
  --draft $APP/draft.md \
  --evidence $MINI/profile/evidence.yaml \
  --matching $APP/matching.yaml \
  --identity $MINI/profile/identity.yaml
# expect exit 0

python $SKILL_ROOT/cv-creation/scripts/validate_application.py \
  --style $MINI/profile/export-style.yaml \
  --skills $MINI/profile/skills.yaml \
  --composition $BAD/empty-ev-ids/composition.yaml \
  --draft $APP/draft.md \
  --evidence $MINI/profile/evidence.yaml \
  --matching $APP/matching.yaml \
  --identity $MINI/profile/identity.yaml
# expect exit 1

# Install into a career project (examples — use your client’s skills folder)
# cp -a skills/evidence-bank skills/cv-creation /path/to/Career/.agents/skills/
# cp -a skills/evidence-bank skills/cv-creation /path/to/Career/.agents/skills/
```

Turn 3 / Turn 6 body+decisions must stay identical across both `SKILL.md` files.

## D. Out of scope here

- Career **data** (`profile/`, `applications/`, `inbox/`) lives in the career project, not this repo.
- Do not regenerate full file-body embeds; edit files under `skills/` directly.
