# CV System — Architecture inventory (v1.0)

> **Skill SoT:** `skills/` (not embedded here).  
> **Design SoT:** `docs/design/`.  
> Full historical embed archived at `docs/archive/CV-SYSTEM-ARCHITECTURE-v1.0-full-embed.md`.

**Updated:** 2026-11-18 (repo layout option A)

Install: copy `skills/evidence-bank` and `skills/cv-creation` into the Agent Skills client’s skills folder (examples: `.cursor/skills/`, `.agents/skills/`). Do not invent files beyond this inventory.

## A. Build target

### Folder tree

```
skills/
  cv-creation/SKILL.md
  cv-creation/assets/application-meta.template.yaml
  cv-creation/assets/ats-rules.template.yaml
  cv-creation/assets/career.config.template.yaml
  cv-creation/assets/checkpoint.template.yaml
  cv-creation/assets/composition.template.yaml
  cv-creation/assets/export-style.template.yaml
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
  evidence-bank/assets/probe-checklist.md
  evidence-bank/assets/fixtures/ok.yaml
  evidence-bank/assets/fixtures/bad-missing-source.yaml
  evidence-bank/references/continuity.md
  evidence-bank/references/destyling-rules.md
  evidence-bank/references/evidence-schema.md
  evidence-bank/references/probe-question-bank.md
  evidence-bank/references/probe-ui.md
  evidence-bank/references/status-taxonomy.md
  evidence-bank/scripts/validate_evidence.py
```

### Purpose per file (one sentence)

| Path | Purpose |
|---|---|
| `cv-creation/SKILL.md` | CV-creation skill entrypoint, stages, and shared T3/T6 contract. |
| `cv-creation/assets/application-meta.template.yaml` | Copy-ready template or checklist asset. |
| `cv-creation/assets/ats-rules.template.yaml` | Copy-ready template or checklist asset. |
| `cv-creation/assets/career.config.template.yaml` | Copy-ready template or checklist asset. |
| `cv-creation/assets/checkpoint.template.yaml` | Copy-ready template or checklist asset. |
| `cv-creation/assets/composition.template.yaml` | Scaffold for composition.yaml on app create. |
| `cv-creation/assets/export-style.template.yaml` | Copy-ready template or checklist asset. |
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
| `cv-creation/references/ats-check.md` | Stage [7] coverage and consistency rules. |
| `cv-creation/references/checkpoint-schema.md` | On-demand reference loaded by the skill. |
| `cv-creation/references/continuity.md` | LIVE/STATUS progress SoT + memory mirror (identical to evidence-bank). |
| `evidence-bank/references/continuity.md` | LIVE/STATUS progress SoT + memory mirror (identical to cv-creation). |
| `cv-creation/references/composition-rules.md` | On-demand reference loaded by the skill. |
| `cv-creation/references/differentiator-rules.md` | On-demand reference loaded by the skill. |
| `cv-creation/references/export-pipeline.md` | On-demand reference loaded by the skill. |
| `cv-creation/references/hitl-gate-catalogue.md` | On-demand reference loaded by the skill. |
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
| `evidence-bank/assets/probe-checklist.md` | Copy-ready template or checklist asset. |
| `evidence-bank/assets/fixtures/ok.yaml` | Bank CI fixture — valid evidence.yaml. |
| `evidence-bank/assets/fixtures/bad-missing-source.yaml` | Bank CI fixture — expected validate fail. |
| `evidence-bank/references/destyling-rules.md` | On-demand reference loaded by the skill. |
| `evidence-bank/references/evidence-schema.md` | On-demand reference loaded by the skill. |
| `evidence-bank/references/probe-question-bank.md` | On-demand reference loaded by the skill. |
| `evidence-bank/references/probe-ui.md` | On-demand reference loaded by the skill. |
| `evidence-bank/references/status-taxonomy.md` | On-demand reference loaded by the skill. |
| `evidence-bank/scripts/validate_evidence.py` | Validate evidence.yaml integrity (Q8 hard-fail vs warn). |

### Changes from baseline inventory

Added across design sessions:

- `evidence-bank/references/probe-ui.md`
- `cv-creation/references/ui-turn-types.md`
- `cv-creation/references/export-pipeline.md`
- `cv-creation/references/ats-baseline-rules.md`
- `cv-creation/references/ats-check.md`
- `cv-creation/references/taxonomy-mechanics.md`
- `cv-creation/references/invocation.md`
- `cv-creation/assets/export-style.template.yaml`
- `cv-creation/assets/ats-rules.template.yaml`
- `cv-creation/assets/composition.template.yaml`
- `cv-creation/assets/gitignore.template`
- `cv-creation/assets/inbox.README.md`
- `cv-creation/assets/fixtures/mini-app/`
- `cv-creation/scripts/export_resume.py`

Runtime-created under `career/` (not in this tree): `inbox/` (resumes, linkedin, from-links), `_skill_state/LIVE.yaml`, `_skill_state/STATUS.md`, `applications/<app>/composition.yaml`, `applications/<app>/ats-check.yaml`, `applications/<app>/export/`, `profile/export-style.yaml`, `profile/norms/ats/*.yaml`.

Stage outputs: [6] → composition.yaml + draft.md; [7] → ats-check.yaml + audit.md; [8] reads draft.md + identity + export-style only.


## C. Install & verify

```bash
# From this repo
SKILL_ROOT=skills

python -m py_compile $SKILL_ROOT/evidence-bank/scripts/*.py $SKILL_ROOT/cv-creation/scripts/*.py

python $SKILL_ROOT/evidence-bank/scripts/validate_evidence.py \
  $SKILL_ROOT/evidence-bank/assets/fixtures/ok.yaml
# expect OK

python $SKILL_ROOT/evidence-bank/scripts/validate_evidence.py \
  $SKILL_ROOT/evidence-bank/assets/fixtures/bad-missing-source.yaml
# expect exit 1

# Install into a career project (examples — use your client’s skills folder)
# cp -a skills/evidence-bank skills/cv-creation /path/to/Career/.agents/skills/
# cp -a skills/evidence-bank skills/cv-creation /path/to/Career/.agents/skills/
```

Turn 3 / Turn 6 body+decisions must stay identical across both `SKILL.md` files.

## D. Out of scope here

- Career **data** (`profile/`, `applications/`, `inbox/`) lives in the career project, not this repo.
- Do not regenerate full file-body embeds; edit files under `skills/` directly.
