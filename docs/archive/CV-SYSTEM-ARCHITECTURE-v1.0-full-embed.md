# CV System — Architecture File (v1.0)

> **Note:** `evidence-bank/**` content is **design-locked** (`EVIDENCE-BANK-DECISIONS.md`, 2026-11-18). cv-creation content from Clusters 1–3 remains the locked build target.
>
> **UI labeling (2026-11-18):** human-facing turns use `Turn N: <plain name>` (never bare `T1`…`T8` alone); show `current of total` when a stage/queue total is known. See `COMMUNICATION_CONTRACT.md` and handoff §19.5.3 HMI 5–6.

Generated: 2026-11-18T17:56Z

Self-contained build spec. Paste the tree under `career/.cursor/skills/`. Do not invent files beyond this inventory.

## A. Build target

### Folder tree

```
.cursor/skills/
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
  cv-creation/assets/jd.template.md
  cv-creation/assets/norms.template.md
  cv-creation/assets/onboarding-checklist.md
  cv-creation/assets/tracker.template.md
  cv-creation/assets/voice.template.md
  cv-creation/references/ats-baseline-rules.md
  cv-creation/references/ats-check.md
  cv-creation/references/checkpoint-schema.md
  cv-creation/references/composition-rules.md
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
| `cv-creation/assets/jd.template.md` | Copy-ready template or checklist asset. |
| `cv-creation/assets/norms.template.md` | Copy-ready template or checklist asset. |
| `cv-creation/assets/onboarding-checklist.md` | Copy-ready template or checklist asset. |
| `cv-creation/assets/tracker.template.md` | Copy-ready template or checklist asset. |
| `cv-creation/assets/voice.template.md` | Copy-ready template or checklist asset. |
| `cv-creation/references/ats-baseline-rules.md` | On-demand reference loaded by the skill. |
| `cv-creation/references/ats-check.md` | Stage [7] coverage and consistency rules. |
| `cv-creation/references/checkpoint-schema.md` | On-demand reference loaded by the skill. |
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
- `cv-creation/assets/fixtures/mini-app/`
- `cv-creation/scripts/export_resume.py`

Runtime-created under `career/` (not in this tree): `applications/<app>/composition.yaml`, `applications/<app>/ats-check.yaml`, `applications/<app>/export/`, `profile/export-style.yaml`, `profile/norms/ats/*.yaml`.

Stage outputs: [6] → composition.yaml + draft.md; [7] → ats-check.yaml + audit.md; [8] reads draft.md + identity + export-style only.

## B. File contents

Each subsection is the full file. Create exactly these paths.

### `.cursor/skills/cv-creation/SKILL.md`

```markdown
---
name: cv-creation
description: >-
  Run a per-application CV pipeline from JD intake through matching, composition,
  ATS check, and export. Use when the user wants to tailor a CV to a job, resume an
  application, probe a gap, export resume formats, or check ATS coverage.
---

# CV Creation

## Purpose

One application end-to-end: JD → requirements → keywords → scoring → matching → composition → ATS → export. Facts come from the evidence bank; voice applies only at composition.

## When to load

| File | When |
|---|---|
| `references/scoring-rubric.md` | Stage [4] |
| `references/matching-rules.md` | Stage [5] |
| `references/composition-rules.md` | Stage [6] |
| `references/voice-guide.md` | Voice elicitation / phrasing |
| `references/norms-guide.md` | Norms conflicts (T5) |
| `references/hitl-gate-catalogue.md` | Any gate G1–G5 |
| `references/state-machine.md` | Item/stage/global loops |
| `references/checkpoint-schema.md` | Writing checkpoints |
| `references/differentiator-rules.md` | Differentiators |
| `references/ui-turn-types.md` | Chat primitives T2,T4–T8 |
| `references/export-pipeline.md` | Stage [8] |
| `references/ats-baseline-rules.md` | Human ATS baseline |
| `references/ats-check.md` | Stage [7] |
| `references/taxonomy-mechanics.md` | New/merge skills |
| `references/invocation.md` | Verb list / script CLIs |
| `references/probe-ui.md` via evidence-bank | When rendering shared T3/T6 |
| assets listed below | Templates on create/copy |
| scripts listed below | Validate, views, export, bootstrap |

## Invocation

See `references/invocation.md`. Verbs: `run`/`continue`, `status`, `show`, `probe`, `gate`, `export`, `check-env`, `regen-views`, `override-ats`.

Always read `career.config.yaml` first. Absent → onboarding (`scripts/bootstrap_career.py` flow).

## Stages

| # | Stage | Writes |
|---|---|---|
| 0 | Bootstrap | tree, config, profile scaffolds |
| 1 | JD intake | `jd.md`, `meta.yaml`, copy `composition.template.yaml` |
| 2 | Requirements | `requirements.yaml` — gate G1 |
| 3 | Skills & keywords | `keywords.yaml`, taxonomy links — T2 |
| 4 | Scoring | `scores.yaml` — gate G2 |
| 5 | Matching | `matching.yaml`, differentiators, probes — gate G3 |
| 6 | Composition | `composition.yaml` + rendered `draft.md` — gate G4 |
| 7 | ATS & consistency | `ats-check.yaml` + `audit.md` — gate G5 |
| 8 | Export | `export/*` via `export_resume.py` |

Backward edges (flag-triggered only): [4]→[2] noise; [5]→bank probe; [6]→[5] ungroundable bullet; [7]→[6] coverage/phrasing/C1; [7]→[5] must-have gap / missing evidence.

## Composition SoT

`composition.yaml` owns plan, grounding, buffered flags, and planned bullet text. `draft.md` is always re-rendered from it (+ identity header). Export reads **draft.md + identity.yaml + export-style.yaml only**.

## Design principles (do not violate)

1. Two skills, not one.
2. Facts and voice separated.
3. AI proposes; user approves.
4. Differentiators reorder/emphasize only until bank-confirmed.
5. State is loops; `approved` is exit; backward edges explicit.
6. One canonical structured file per artifact; views generated.
7. Checkpoints durable.
8. User judgment tie-breaks norms.
9. Skill code vs career data separated.
10. No fabrication.

### Cross-skill contract — T3 Gap probe (verbatim)

**Owner:** both skills (identical text required).

**When:** A required skill has action `gap`, or matching needs a single-item evidence probe.

**Body (must include):**
- requirement text (or id)
- missing `sk_*` (canonical name + id)
- exactly one probe question from the probe-question bank
- linked evidence candidates if any (ids only)

**Decisions (exact labels):** `has evidence` / `no evidence` / `waive`

**Envelope:** use the standard primitive envelope (gui or tui per `ui.chat_host`). One decision per turn.


### Cross-skill contract — T6 Gate summary (verbatim)

**Owner:** both skills (identical text required).

**When:** End of a stage loop, before gate pass.

**Body (must include):**
- stage name and item rollup (done / awaiting_hitl / pending)
- action counts with **inline definitions**:
  - `core` — high priority + strong evidence
  - `use` — high priority + moderate evidence
  - `covered_indirectly` — met via a broader evidence row
  - `mention` — low priority, evidenced (skills line only)
  - `gap` — required, not evidenced
  - `ask_user` — weak or stale evidence — probe before deciding
- buffered-flag count

**Decisions (exact labels):** `approve` / `revise` / `resolve` / `accept`

**Envelope:** standard primitive envelope. Tracker line may accompany; active primitive last.


### Action definitions (canonical)

| Action | Meaning |
|---|---|
| `core` | high priority + strong evidence |
| `use` | high priority + moderate evidence |
| `covered_indirectly` | met via a broader evidence row |
| `mention` | low priority, evidenced (skills line only) |
| `gap` | required, not evidenced |
| `ask_user` | weak or stale evidence — probe before deciding |


## Gates (summary)

Load `references/hitl-gate-catalogue.md`. G4 resolve-flag sub-decisions: drop / rephrase / route-to-bank / waive. G5: approve / accept-edge / export / override (reason required).

## Privacy / VCS / language

No telemetry. Web fetch only with per-URL OK. Bootstrap installs gitignore (docx/pdf). Commit evidence by default. One language per application; no auto-translate.
```

### `.cursor/skills/cv-creation/assets/application-meta.template.yaml`

```yaml
application:
  id: ""
  company: ""
  role: ""
  jd_source: ""
  language: en
  created: ""
  stage: jd_intake
  stage_items: { total: 0, done: 0, awaiting_hitl: 0, pending: 0 }
  open_flags: []
  revision_counts: {}
```

### `.cursor/skills/cv-creation/assets/ats-rules.template.yaml`

```yaml
version: 1
regime: generic
source: [baseline]
last_verified: "2026-11-18"
coverage_pass: 80
coverage_warn: 65
must_have_gap_blocks: true
required_sections: [experience, skills]
banned_layout:
  tables: true
  text_boxes: true
  multi_column: true
keyword_rules:
  prefer_ats_forms: true
  min_core_on_skills_line: true
  title_keyword_in_summary: true
enrichment_notes: []
```

### `.cursor/skills/cv-creation/assets/career.config.template.yaml`

```yaml
career_root: "."
defaults:
  country: FR
  language: en
  seniority: senior
  industry: data-engineering
ui:
  chat_host: gui
  tracker_fence: true
  glyphs:
    chat: auto
    views: emoji
checkpointing:
  turn_floor: 10
  flag_threshold: 5
  retention_k: 20
norms:
  staleness_months: 12
ats:
  regime: generic
  coverage_pass: 80
  coverage_warn: 65
  must_have_gap_blocks: true
paths:
  skills_dir: ".cursor/skills"
  profile_dir: "profile"
  applications_dir: "applications"
  state_dir: "_skill_state"
```

### `.cursor/skills/cv-creation/assets/checkpoint.template.yaml`

```yaml
state:
  stage: ""
  items: { total: 0, done: 0, awaiting_hitl: 0, pending: 0 }
  revision_counts: {}
  open_flags: []
decisions: []
rejected: []
recent_context: []
```

### `.cursor/skills/cv-creation/assets/composition.template.yaml`

```yaml
section_plan: []
bullets: []
skills_line: []
grounding:
  uncovered: []
  unconfirmed_differentiators_used: []
  cited_ev_ids: []
buffered_flags: []
```

### `.cursor/skills/cv-creation/assets/export-style.template.yaml`

```yaml
version: 1
page:
  size: A4
  margins: { top: 20mm, bottom: 20mm, left: 18mm, right: 18mm }
fonts:
  family: "Calibri, Arial, sans-serif"
  size_pt: 10.5
  heading_size_pt: 12
  name_size_pt: 16
  line_height: 1.3
layout:
  single_column: true
  tables: false
  text_boxes: false
  content_headers_footers: false
  real_list_styles: true
heading:
  case: title
  rule_after: true
bullets:
  glyph: "•"
  indent_mm: 4
  spacing_after_pt: 2
skills_section:
  format: inline_pipe
ats:
  enforce_safe_layout: true
  plain_text_export: true
colors:
  text: "#000000"
  accent: "#000000"
```

### `.cursor/skills/cv-creation/assets/fixtures/mini-app/README.md`

````markdown
# Mini-app fixture

Self-contained mini career root for deterministic tests.

- `profile/` — identity, evidence, skills, export-style
- `applications/acme-de-2026-01-01/` — composition + draft + matching

Suggested checks:

```bash
python -m py_compile ../../scripts/*.py
python ../../scripts/validate_evidence.py profile/evidence.yaml
python ../../scripts/validate_application.py --style profile/export-style.yaml --skills profile/skills.yaml --composition applications/acme-de-2026-01-01/composition.yaml --draft applications/acme-de-2026-01-01/draft.md
python ../../scripts/export_resume.py --formats md,html --career-root . applications/acme-de-2026-01-01
python ../../scripts/regenerate_views.py applications/acme-de-2026-01-01
python ../../scripts/verify_views.py applications/acme-de-2026-01-01
```
````

### `.cursor/skills/cv-creation/assets/fixtures/mini-app/applications/acme-de-2026-01-01/ats-check.yaml`

```yaml
generated_at: 2026-01-01T00:00:00Z
coverage_pct: 100
universe: [sk_python, sk_airflow]
per_skill: []
consistency: [{id: C1, ok: true}]
warnings: []
proposed_edges: []
override: null
gate: passed
```

### `.cursor/skills/cv-creation/assets/fixtures/mini-app/applications/acme-de-2026-01-01/audit.md`

```markdown
# ATS audit (fixture)

Coverage 100%.
```

### `.cursor/skills/cv-creation/assets/fixtures/mini-app/applications/acme-de-2026-01-01/composition.yaml`

```yaml
section_plan:
  - {id: header, order: 1, source: identity}
  - {id: experience, order: 2, experiences: [exp_acme]}
  - {id: skills, order: 3, source: matching}
bullets:
  - id: b_001
    section: experience
    experience_id: exp_acme
    text: "Rebuilt nightly billing ETL (Python, Airflow); −40% runtime."
    ev_ids: [ev_001]
    skill_ids: [sk_python, sk_airflow]
    voice: {verb: rebuilt, tense: past, len_words: 12}
    differentiator_refs: []
    user_pinned: false
    flags: []
skills_line:
  - {group: Languages, items: [Python]}
  - {group: Tools, items: [Airflow]}
grounding:
  uncovered: []
  unconfirmed_differentiators_used: []
  cited_ev_ids: [ev_001]
buffered_flags: []
```

### `.cursor/skills/cv-creation/assets/fixtures/mini-app/applications/acme-de-2026-01-01/draft.md`

```markdown
Ada Example
ada@example.com · Paris, FR

## Experience

### Data Engineer — Acme (2022-03 — 2024-08)

- Rebuilt nightly billing ETL (Python, Airflow); −40% runtime.

## Skills

Python | Airflow
```

### `.cursor/skills/cv-creation/assets/fixtures/mini-app/applications/acme-de-2026-01-01/export/export_manifest.yaml`

```yaml
generated_at: 2026-11-18T17:55Z
application_id: acme-de-2026-01-01
inputs:
  draft_md:
    path: /home/mohamed/Projects/application-skills/architecture-v1.0/.cursor/skills/cv-creation/assets/fixtures/mini-app/applications/acme-de-2026-01-01/draft.md
    sha256: 46e907d9316144d2aaebcea06333496810711cb4a03e6fcc39ba6fc136bcf850
  identity_yaml:
    path: /home/mohamed/Projects/application-skills/architecture-v1.0/.cursor/skills/cv-creation/assets/fixtures/mini-app/profile/identity.yaml
    sha256: 360d6e91740974605b602346969eaba721d910097642c77d9d1f25f3bbe8d989
  export_style:
    path: /home/mohamed/Projects/application-skills/architecture-v1.0/.cursor/skills/cv-creation/assets/fixtures/mini-app/profile/export-style.yaml
    sha256: 27166811e282bd5f3fdf0ff925ed7b54bda59b03478bf1857acc45481030b4e7
tool:
  python: 3.15.2
  python_docx: null
  weasyprint: null
requested_formats:
- md
- html
produced_formats:
- md
- html
skipped_formats: []
outputs:
- format: md
  path: export/resume.md
  sha256: edf99c4adf782a0937608beb4c2cec474d9df90de6bea1ba36aa87178504e2e8
  bytes: 200
- format: html
  path: export/resume.html
  sha256: 6becf58498e6b770edd0da530e1b3465b17c7a6546499d88202aeb31854d5836
  bytes: 549
warnings: []
```

### `.cursor/skills/cv-creation/assets/fixtures/mini-app/applications/acme-de-2026-01-01/export/resume.html`

```text
<!DOCTYPE html><html><head><meta charset='utf-8'><style>
@page { size: A4; margin: 20mm 18mm 20mm 18mm; }
body { font-family: Calibri, Arial, sans-serif; font-size: 10.5pt; color: #000; }
h1 { font-size: 16pt; } h2 { font-size: 12pt; } ul { list-style: disc; }
</style></head><body>
<h1>Ada Example</h1>
<p>ada@example.com · Paris, FR</p>
<h2>Experience</h2>
<h3>Data Engineer — Acme (2022-03 — 2024-08)</h3>
<ul><li>Rebuilt nightly billing ETL (Python, Airflow); −40% runtime.</li></ul>
<h2>Skills</h2>
<p>Python | Airflow</p>
</body></html>
```

### `.cursor/skills/cv-creation/assets/fixtures/mini-app/applications/acme-de-2026-01-01/export/resume.md`

```markdown
Ada Example
ada@example.com · Paris, FR

## Experience

### Data Engineer — Acme (2022-03 — 2024-08)
- Rebuilt nightly billing ETL (Python, Airflow); −40% runtime.

## Skills

Python | Airflow
```

### `.cursor/skills/cv-creation/assets/fixtures/mini-app/applications/acme-de-2026-01-01/keywords.yaml`

```yaml
jd_keywords: []
keyword_skills: []
```

### `.cursor/skills/cv-creation/assets/fixtures/mini-app/applications/acme-de-2026-01-01/matching.yaml`

```yaml
matching:
  - skill_id: sk_python
    priority_norm: 100
    best_evidence_id: ev_001
    strength: strong
    action: core
  - skill_id: sk_airflow
    priority_norm: 80
    best_evidence_id: ev_001
    strength: strong
    action: core
differentiators: []
```

### `.cursor/skills/cv-creation/assets/fixtures/mini-app/applications/acme-de-2026-01-01/meta.yaml`

```yaml
application:
  id: acme-de-2026-01-01
  company: Acme
  role: Data Engineer
  jd_source: fixture
  language: en
  created: 2026-01-01T00:00:00Z
  stage: composition
  stage_items: { total: 2, done: 2, awaiting_hitl: 0, pending: 0 }
  open_flags: []
  revision_counts: {}
```

### `.cursor/skills/cv-creation/assets/fixtures/mini-app/applications/acme-de-2026-01-01/requirements.yaml`

```yaml
requirements: []
requirement_skills: []
```

### `.cursor/skills/cv-creation/assets/fixtures/mini-app/applications/acme-de-2026-01-01/scores.yaml`

```yaml
job_skill_scores:
  - skill_id: sk_python
    priority_norm: 100
    ats_weight: 4
  - skill_id: sk_airflow
    priority_norm: 80
    ats_weight: 3
```

### `.cursor/skills/cv-creation/assets/fixtures/mini-app/applications/acme-de-2026-01-01/views/_manifest.yaml`

```yaml
generated_at: 2026-11-18T17:55Z
sources:
  requirements.md: 309dd0b8645daca765e5d3e3cfc28097d2cb6b4fc0f8b2b40029b3099225655e
  keywords.md: 952bfb468d00abca5178afd8e1351779e8831d6d71c019ee5ce1f70c82891406
  scoring.md: 0a241eeef639c19396ff11c1dd64f0a30bacd5055ed111ac8516fd5aff744bb8
  matching.md: 8eb8c86c88e10bf57c135ac59e4f1e21daf3bdedb44eebe1f95542a15c3760e9
  tracker.md: 8fab11ef2d52b1d9c4832513c6c47531ff234bc1e985dc80a7140edeff7f8171
```

### `.cursor/skills/cv-creation/assets/fixtures/mini-app/applications/acme-de-2026-01-01/views/keywords.md`

````markdown
<!-- GENERATED from keywords.yaml. Do not edit. sha256: 952bfb468d00abca5178afd8e1351779e8831d6d71c019ee5ce1f70c82891406 -->
# Keywords

```yaml
jd_keywords: []
keyword_skills: []

```
````

### `.cursor/skills/cv-creation/assets/fixtures/mini-app/applications/acme-de-2026-01-01/views/matching.md`

````markdown
<!-- GENERATED from matching.yaml. Do not edit. sha256: 8eb8c86c88e10bf57c135ac59e4f1e21daf3bdedb44eebe1f95542a15c3760e9 -->
# Matching

```yaml
matching:
  - skill_id: sk_python
    priority_norm: 100
    best_evidence_id: ev_001
    strength: strong
    action: core
  - skill_id: sk_airflow
    priority_norm: 80
    best_evidence_id: ev_001
    strength: strong
    action: core
differentiators: []

```
````

### `.cursor/skills/cv-creation/assets/fixtures/mini-app/applications/acme-de-2026-01-01/views/requirements.md`

````markdown
<!-- GENERATED from requirements.yaml. Do not edit. sha256: 309dd0b8645daca765e5d3e3cfc28097d2cb6b4fc0f8b2b40029b3099225655e -->
# Requirements

Source: requirements.yaml

```yaml
requirements: []
requirement_skills: []

```
````

### `.cursor/skills/cv-creation/assets/fixtures/mini-app/applications/acme-de-2026-01-01/views/scoring.md`

````markdown
<!-- GENERATED from scores.yaml. Do not edit. sha256: 0a241eeef639c19396ff11c1dd64f0a30bacd5055ed111ac8516fd5aff744bb8 -->
# Scoring

```yaml
job_skill_scores:
  - skill_id: sk_python
    priority_norm: 100
    ats_weight: 4
  - skill_id: sk_airflow
    priority_norm: 80
    ats_weight: 3

```
````

### `.cursor/skills/cv-creation/assets/fixtures/mini-app/applications/acme-de-2026-01-01/views/tracker.md`

```markdown
<!-- GENERATED from meta.yaml + matching.yaml + scores.yaml. Do not edit. sha256: 8fab11ef2d52b1d9c4832513c6c47531ff234bc1e985dc80a7140edeff7f8171 -->
# Acme · Data Engineer — CV application

> [!info] acme-de-2026-01-01
> JD: fixture · created 2026-01-01 00:00:00+00:00 · updated 2026-11-18T17:55Z

Stage: composition · flags 0
```

### `.cursor/skills/cv-creation/assets/fixtures/mini-app/profile/evidence.yaml`

```yaml
experiences:
  - id: exp_acme
    title: Data Engineer
    org: Acme
    start: 2022-03
    end: 2024-08
    location: Paris, FR
evidence:
  - id: ev_001
    experience_id: exp_acme
    fact: "Rebuilt nightly billing ETL with Python and Airflow; cut runtime 40%."
    actor: self
    action: rebuilt
    object: nightly billing ETL
    scale: "~2M rows/night"
    metric: "runtime -40%"
    tool: [Python, Airflow]
    date: 2023
    outcome: production
    status: fact
    source: "fixture, bullet 1"
    probe_history: []
    revision_count: 0
evidence_skills:
  - evidence_id: ev_001
    skill_id: sk_python
    strength: strong
    recency: current
  - evidence_id: ev_001
    skill_id: sk_airflow
    strength: strong
    recency: current
```

### `.cursor/skills/cv-creation/assets/fixtures/mini-app/profile/export-style.yaml`

```yaml
version: 1
page:
  size: A4
  margins: { top: 20mm, bottom: 20mm, left: 18mm, right: 18mm }
fonts:
  family: "Calibri, Arial, sans-serif"
  size_pt: 10.5
  heading_size_pt: 12
  name_size_pt: 16
  line_height: 1.3
layout:
  single_column: true
  tables: false
  text_boxes: false
  content_headers_footers: false
  real_list_styles: true
heading:
  case: title
  rule_after: true
bullets:
  glyph: "•"
  indent_mm: 4
  spacing_after_pt: 2
skills_section:
  format: inline_pipe
ats:
  enforce_safe_layout: true
  plain_text_export: true
colors:
  text: "#000000"
  accent: "#000000"
```

### `.cursor/skills/cv-creation/assets/fixtures/mini-app/profile/identity.yaml`

```yaml
name: Ada Example
contact:
  email: ada@example.com
  phone: ""
  location: Paris, FR
  links: []
education: []
```

### `.cursor/skills/cv-creation/assets/fixtures/mini-app/profile/skills.yaml`

```yaml
skills:
  - id: sk_python
    canonical_name: Python
    type: language
    parent_id: null
    aliases: [python3]
    ats_forms: [Python]
  - id: sk_airflow
    canonical_name: Airflow
    type: tool
    parent_id: null
    aliases: []
    ats_forms: [Airflow]
```

### `.cursor/skills/cv-creation/assets/gitignore.template`

```text
export/*.docx
export/*.pdf
_skill_state/**/tmp-*
*.pyc
__pycache__/
.DS_Store
```

### `.cursor/skills/cv-creation/assets/identity.template.yaml`

```yaml
name: ""
contact:
  email: ""
  phone: ""
  location: ""
  links: []
education: []
```

### `.cursor/skills/cv-creation/assets/jd.template.md`

```markdown
# Role title

Company:

URL:

## Summary

## Requirements

## Nice to have
```

### `.cursor/skills/cv-creation/assets/norms.template.md`

```markdown
---
context: { industry: "", country: "", language: "", seniority: "" }
source: []
last_verified: ""
confidence: 3
---

# Norms

## Sections
- skills_section: true
- education_required: false
- experience_order: reverse_chronological

## Notes
-
```

### `.cursor/skills/cv-creation/assets/onboarding-checklist.md`

```markdown
# Onboarding checklist

1. Confirm `career.config.yaml` (incl. `ui.chat_host`)
2. Fill `profile/identity.yaml`
3. Offer evidence-bank now/defer
4. Copy `voice.md` template (no elicitation yet)
5. Note norms lazy creation
6. Copy `export-style.yaml` + install `.gitignore`
7. Print empty-and-when report + tracker 0/8
```

### `.cursor/skills/cv-creation/assets/tracker.template.md`

```markdown
<!-- GENERATED. Do not edit. sha256: PLACEHOLDER -->
# {{company}} · {{role}} — CV application

> [!info] {{application_id}}
> JD: {{jd_source}} · created {{created}}

`░░░░░░░░░░░░░░░░░░░░` **0%** · items 0/0 · stage 0/8 · flags 0

## Stages
| # | Stage | Status | Items | Gate |
|---|---|---|---|---|
| 1 | JD intake | ⬜ not started | 0/0 | — |
```

### `.cursor/skills/cv-creation/assets/voice.template.md`

```markdown
---
complete: false
elicited: null
---

# Voice profile

## Sentence length
(target words per bullet)

## Preferred verbs
-

## First-person stance
(I / implied / none)

## Technical density
(low / medium / high)

## Bullet structure
(metric-first / verb-first)

## Formatting habits
-
```

### `.cursor/skills/cv-creation/references/ats-baseline-rules.md`

```markdown
# ATS baseline rules (human)

- Prefer exact ATS forms from taxonomy on skills line when section present.
- Single column, no tables/text boxes in export style.
- Core skills should appear in narrative bullets with evidence.
- Avoid header/footer content other than optional page numbers.
- Keyword stuffing that invents claims is forbidden (fabrication rule).

Enrich regime YAML `enrichment_notes` from compiled ATS reports without code changes.
```

### `.cursor/skills/cv-creation/references/ats-check.md`

````markdown
# ATS & consistency check

## Artifacts

`ats-check.yaml` (machine) + `audit.md` (narrative).

## Universe

`core` + `use` + `gap` only.

## In-draft (norms-aware)

- Skills section included: bullet `skill_ids` OR skills-line ats_forms
- Skills section omitted: bullet `skill_ids` only

## Coverage

```
covered = in_draft ∧ action ≠ gap ∧ strength_ok
coverage_pct = 100 × |covered| / |universe|
```

Defaults: pass 80, warn 65. must_have gap blocks pass unless override.

## Consistency

C1 draft ≡ render(composition) — **block** until fix. Also grounding, style MUST, identity contact warn, no ambiguous/unverified in cited_ev_ids.

## Edges

Gap / missing evidence → propose [7]→[5]; else → [7]→[6].

## Override

Allowed; reason required; gaps remain visible.
````

### `.cursor/skills/cv-creation/references/checkpoint-schema.md`

````markdown
# Checkpoint schema

Path: `_skill_state/<app-id>/<timestamp>-<slug>.yaml`

Triggers: state transition; before lossy ops; every `turn_floor` (default 10); open flags ≥ `flag_threshold` (default 5); explicit command.

Retention: per app, keep `retention_k` (20) unpinned; pinned never deleted. Auto-pin checkpoint before a decision that is later revised.

```yaml
state:
  stage: matching
  items: { total: 14, done: 11, awaiting_hitl: 2, pending: 1 }
  revision_counts: {}
  open_flags: []
decisions: []
rejected: []
recent_context: []
```
````

### `.cursor/skills/cv-creation/references/composition-rules.md`

```markdown
# Composition rules

## SoT

`composition.yaml` owns section plan, bullets (including text), skills_line, grounding, buffered_flags. `draft.md` is always re-rendered from composition + identity header. They revise together.

## Section inclusion

| Section | Rule |
|---|---|
| Header | Always from identity |
| Summary | ≥3 core/use **or** ≥2 confirmed differentiators; 2–3 bullets |
| Skills | Any core/use/mention; group by parent_id; order core→use→mention; ATS forms; **not** covered_indirectly |
| Experience | Always; default reverse-chronological; norms may relevance-first |
| Education | Per norms |
| Projects/Certs | Only if evidenced + norms-appropriate; never empty |

## Bullet ordering

Experience: (1) max priority_norm of linked skills desc (2) confirmed differentiator boost confidence×0.5 (3) date desc (4) user_pinned sticky. Summary: summed priority_norm then differentiator hits. **Voice never orders.**

## Grounding (G4 machine checks)

1. Summary/Experience bullets: `ev_ids.length ≥ 1`
2. Each ev exists
3. status fact or waived with reason
4. `skill_ids[]` ⊆ skills on cited ev via evidence_skills; **core** bullets need ≥1 strong link; **use** ≥ moderate
5. Education/certs from identity exempt; else same
6. Skills-line item iff skill in core|use|mention
7. `grounding.uncovered` empty to pass

Ungroundable → omit from draft, add buffered_flag.

## Buffer resolve-flag

drop | rephrase | route-to-bank (only this fires [6]→[5]) | waive

## Unconfirmed differentiators

Reorder/emphasis only. G4 must confirm/reject/route-to-bank/defer each used id. T4 envelope embedded in T7.
```

### `.cursor/skills/cv-creation/references/differentiator-rules.md`

```markdown
# Differentiator rules

Sources: jd (conf 4–5), industry (3–4), company (2–3, URL + per-fetch OK), user (5 → becomes fact via bank).

Hard boundary: unconfirmed → ordering/emphasis only. Content requires bank probe + evidence row `source: user`.

Rejected recorded; do not re-derive.
```

### `.cursor/skills/cv-creation/references/export-pipeline.md`

```markdown
# Export pipeline

## Inputs

`draft.md`, `profile/identity.yaml`, `profile/export-style.yaml`. Never read `composition.yaml` or `export/` as inputs to the pipeline.

## Parse (stdlib regex)

Strip optional YAML frontmatter. Split on `^##\s+`. Within section: `^###\s+` subsection, `^[-*]\s+` bullet, blank-line prose. Lines before first `##` = header block.

Zero `##` sections → exit 2.

## Section model

header `{name, contact_lines}` + sections of blocks: paragraph | bullets | subsection`{heading, meta{org,dates}, bullets}`.

Identity wins on header mismatch (warn). Contact lines always from identity.

## Style MUST (exit 3 if violated)

`single_column: true`, `tables: false`, `text_boxes: false`, `content_headers_footers: false`, `real_list_styles: true`.

## Formats

md + html always (stdlib). docx if python-docx. pdf if weasyprint (HTML→PDF). Browser print of HTML is a user path, not automated.

## CLI

`export_resume.py [--formats md,html,docx,pdf] [--check-env] <app-dir>`

Exits: 0 ok/skip-optional; 1 missing requested dep; 2 parse; 3 style; 4 identity; 5 IO.
```

### `.cursor/skills/cv-creation/references/hitl-gate-catalogue.md`

```markdown
# HITL gate catalogue

| Gate | After | Includes | Decisions |
|---|---|---|---|
| G1 | [2] | Requirements, weights | Approve, revise, add/remove |
| G2 | [4] | Ranked skills, noise, ties | Approve, adjust, re-extract |
| G3 | [5] | Actions, gaps, differentiators | Approve, resolve gaps, accept |
| G4 | [6] | Draft, plan, bullet→ev, buffered flags | Approve, revise, resolve-flag |
| G5 | [7] | Coverage, warnings, edges | Approve, accept-edge, export, override |

Drafting flags buffered; resolve at G4 as a batch. Level-2 exit: no pending items, gate passed, no open flags.
```

### `.cursor/skills/cv-creation/references/invocation.md`

```markdown
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
```

### `.cursor/skills/cv-creation/references/matching-rules.md`

````markdown
# Matching rules

```
required    = { skills with priority_norm > 0 }
evidenced   = { skills reachable from evidence_skills }
required ∩ evidenced  → core / use / covered_indirectly / mention
required − evidenced  → gaps
evidenced − required  → differentiators (sparingly)
```

## Action floors

| Action | priority_norm | strength | recency |
|---|---|---|---|
| core | ≥ 70 | strong | not stale |
| use | ≥ 40 | ≥ moderate | any |
| mention | > 0 | ≥ weak | any |
| ask_user | high priority | weak **or** stale | — |
| gap | in required | not evidenced | — |
| covered_indirectly | — | evidenced via parent/broader only | — |

**Stale cannot be `core`** — downgrade to `use` or `ask_user`.

## Strength rubric (on evidence_skills)

| Level | When |
|---|---|
| strong | Named tool/skill in fact AND metric/outcome AND actor=self |
| moderate | Named + actor=self without metric; or metric with tool in `tool[]` only |
| weak | Implied / team-only / parent-adjacent / single mention without ownership |

## Recency (vs application `created`)

| Label | Window |
|---|---|
| current | ≤ 18 months |
| `<3y` | ≤ 36 months, not current |
| stale | older, or undated → stale + warn |

## Output

`matching.yaml` with `matching[]` and `differentiators[]`.
````

### `.cursor/skills/cv-creation/references/norms-guide.md`

```markdown
# Norms guide

Files under `profile/norms/`. Precedence: overrides > more-specific > less-specific > global default. Conflicts → T5 (once / scoped / wider). Staleness: `last_verified` older than `norms.staleness_months` → re-verify offer.
```

### `.cursor/skills/cv-creation/references/scoring-rubric.md`

````markdown
# Scoring rubric

## Inputs

`requirements.yaml`, `requirement_skills`, `keywords.yaml` / `keyword_skills`.

## Formulas

```
contribution(skill, req) = importance_in_req × requirement_weight
priority_raw(skill)      = Σ over requirements
priority_norm            = 100 × priority_raw / max_raw
```

`requirement_weight`: must_have=1.5, strong=1.25, required=1.0, nice_to_have=0.75.

## ats_weight (1–5, tiebreaker only)

```
base = min(5, occurrences)
+2 if placement == title
+1 if placement == summary
+1 if raw matches ats_forms exactly
→ clamp to 1..5
```

Boilerplate-only keywords: mark `noise_candidate`, cap `ats_weight` at 1.

## Noise

`type: modifier` skills extracted but excluded from scoring; flag at G2.

## Output

Materialize `scores.yaml` (`job_skill_scores`). Always rebuild; never migrate.
````

### `.cursor/skills/cv-creation/references/state-machine.md`

```markdown
# State machine

## Level 1 — item

not_started → in_progress → awaiting_hitl → approve → approved. Revise returns to in_progress (+ revision_count). Explicit reopen → awaiting_hitl.

## Level 2 — stage

extract items → loop item lifecycle → gate → else re-extract → stage done. Exit: no pending, gate passed, no open flags.

## Level 3 — global

Full run [1]→[8]; resume from checkpoint; single-item probe with no stage transition.
```

### `.cursor/skills/cv-creation/references/taxonomy-mechanics.md`

```markdown
# Taxonomy mechanics

File: `profile/skills.yaml`.

Lookup: canonical_name, aliases, ats_forms (casefold). **New sk_*: HITL before write.** Merge: survivor keeps id; loser becomes alias; rewrite references. Modifiers excluded from scoring. Parents: DAG; validator rejects cycles/unknown parent_id. Soft delete: `deprecated: true`.
```

### `.cursor/skills/cv-creation/references/ui-turn-types.md`

````markdown
# UI turn types (cv-creation)

## Hosts

`ui.chat_host`: `gui` (markdown-native) | `tui` (monospace). Glyphs: chat `auto` → emoji on gui, unicode on tui; `views` default emoji. `ascii` overrides both.

| Semantic | unicode | ascii | emoji |
|---|---|---|---|
| not_started | `·` | ` ` | ⬜ |
| in_progress | `◐` | `~` | 🟡 |
| awaiting_hitl | `◆` | `*` | 🔔 |
| approved | `✓` | `x` | ✅ |
| flag | `⚑` | `!` | ⚠️ |
| reopened | `↻` | `r` | 🔄 |
| gap / blocked | `✗` | `-` | 🛑 |
| pinned | `📌` | `P` | 📌 |

## Envelope

gui: bold header lines, numbered options, italic checkpoint. tui: aligned box with `[n]` options and rule before checkpoint. Error verb uses same envelope with ≥2 recoveries.

## Human labeling (locked 2026-11-18)

- Never show bare `T1`…`T8` to the user. Required: **`Turn N: <plain name>`** (e.g. `Turn 2: Keyword validation`). Optional builder cue `(T2)` only after the plain label.
- When the stage/queue total is known, show **`current of total`** in the header or question line (e.g. `3 of 14`).
- See repo `COMMUNICATION_CONTRACT.md` and handoff §19.5.3 HMI principles 5–6.

## Turn catalogue

| # | Human label | Type | Decisions |
|---|---|---|---|
| T2 | Turn 2: Keyword validation | Keyword validation | approve / remap / drop / add |
| T3 | Turn 3: Gap probe | Gap probe | has evidence / no evidence / waive (verbatim shared) |
| T4 | Turn 4: Differentiator confirmation | Differentiator | confirm / reject / route-to-bank |
| T5 | Turn 5: Norms tie-breaker | Norms tie-breaker | once / scoped rule / wider rule |
| T6 | Turn 6: Gate summary | Gate summary | approve / revise / resolve / accept (verbatim shared) |
| T7 | Turn 7: Draft review | Draft review | approve / revise / resolve-flag (drop\|rephrase\|route-to-bank\|waive) |
| T8 | Turn 8: ATS report | ATS report | approve / accept-edge / export / override |

## T2 gui example

```markdown
**▸ Turn 2: Keyword validation · kw_1 · 1 of 6**
**Raw:** k8s → **Normalized:** Kubernetes → **sk_kubernetes**
**Occurrences:** 1 · **Placement:** body
1. approve
2. remap
3. drop
4. add
*checkpoint 2026-11-21T08:00Z*
```

## T2 tui example

```
▸ Turn 2: Keyword validation · kw_1 · 1 of 6
  Raw: k8s → Normalized: Kubernetes → sk_kubernetes
  Occurrences: 1 · Placement: body
  [1] approve  [2] remap  [3] drop  [4] add
──────────────────────────────────────────── checkpoint 2026-11-21T08:00Z
```

## T4 gui / tui

gui: fields text, source, confidence, URL; decisions confirm/reject/route-to-bank. tui: same fields aligned with [1][2][3].

## T5 gui / tui

Show conflict, current values, three save options narrow→wide.

## T6 gui example

```markdown
**▸ Turn 6: Gate summary · G3 · matching**
**Stage:** matching · items 11/14 · awaiting 2
**Actions:** core 4 · use 3 · mention 2 · gap 2 · ask_user 1
*(core = high priority + strong evidence; use = high priority + moderate evidence; …)*
**Buffered flags:** 0
1. approve
2. revise
3. resolve
4. accept
*checkpoint 2026-11-21T09:15Z*
```

## T7 / T8

T7: draft excerpt, section plan, bullet→ev table, buffered flags batch, unconfirmed differentiator dispositions (T4 embedded). T8: coverage table, warnings, proposed edges, override reason field.

## Tracker cadence

Re-render on stage transition, gate open/close, flag-count change, revision-count change, or `status`. Floor: `checkpointing.turn_floor`. Double-render guard: once per event burst.
````

### `.cursor/skills/cv-creation/references/voice-guide.md`

```markdown
# Voice guide

Location: `profile/voice.md`. Composition only. Never evidence bank.

## Captures

Sentence length, verb preferences, first-person stance, technical density, bullet structure, formatting habits.

## Elicitation (stage [6] if incomplete)

Six prompts, one decision each. **Skip allowed** → template defaults + G4 note.

## Application

Phrasing only when writing `bullets[*].text`. Entities/metrics from evidence unchanged. ATS wins for `core` skills on keyword conflicts; voice wins elsewhere.
```

### `.cursor/skills/cv-creation/scripts/bootstrap_career.py`

```python
#!/usr/bin/env python3
"""Bootstrap a career/ project tree from templates next to this skill."""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
ASSETS = SKILL_ROOT / "assets"


def copy_template(name: str, dest: Path) -> None:
    src = ASSETS / name
    if not src.exists():
        raise FileNotFoundError(src)
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)


def bootstrap(root: Path, force: bool = False) -> None:
    root = root.resolve()
    root.mkdir(parents=True, exist_ok=True)
    cfg = root / "career.config.yaml"
    if cfg.exists() and not force:
        print(f"Exists: {cfg} (use --force to overwrite config)")
    else:
        copy_template("career.config.template.yaml", cfg)
    profile = root / "profile"
    profile.mkdir(exist_ok=True)
    for src_name, dest_name in [
        ("identity.template.yaml", "identity.yaml"),
        ("voice.template.md", "voice.md"),
        ("export-style.template.yaml", "export-style.yaml"),
    ]:
        dest = profile / dest_name
        if dest.exists() and not force:
            print(f"Skip existing {dest}")
        else:
            copy_template(src_name, dest)
    evidence = profile / "evidence.yaml"
    if not evidence.exists() or force:
        # prefer evidence-bank template if present
        eb = SKILL_ROOT.parent / "evidence-bank" / "assets" / "evidence-record-template.yaml"
        if eb.exists():
            shutil.copy2(eb, evidence)
        else:
            evidence.write_text("experiences: []\nevidence: []\nevidence_skills: []\n", encoding="utf-8")
    skills = profile / "skills.yaml"
    if not skills.exists() or force:
        skills.write_text("skills: []\n", encoding="utf-8")
    (profile / "norms" / "ats").mkdir(parents=True, exist_ok=True)
    ats = profile / "norms" / "ats" / "generic.yaml"
    if not ats.exists() or force:
        copy_template("ats-rules.template.yaml", ats)
    (root / "applications").mkdir(exist_ok=True)
    (root / "_skill_state").mkdir(exist_ok=True)
    gi = root / ".gitignore"
    if not gi.exists() or force:
        copy_template("gitignore.template", gi)
    print(f"Bootstrapped career root: {root}")
    print("Empty-and-when: evidence empty→prompt at bank/composition; norms lazy; voice elicit at [6] (skippable).")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("root", type=Path, nargs="?", default=Path("."), help="career project root")
    p.add_argument("--force", action="store_true")
    args = p.parse_args(argv)
    try:
        bootstrap(args.root, force=args.force)
    except FileNotFoundError as e:
        print(f"ERROR: missing template {e}", file=sys.stderr)
        print("Recovery: 1) restore assets/  2) reinstall skill tree", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

### `.cursor/skills/cv-creation/scripts/export_resume.py`

```python
#!/usr/bin/env python3
"""Export draft.md to md/html/docx/pdf. Pure derivation; never mutates inputs."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

try:
    import docx  # noqa: F401
    from docx import Document
    from docx.shared import Pt, Mm

    HAVE_DOCX = True
except ImportError:
    HAVE_DOCX = False

try:
    from weasyprint import HTML as WeasyHTML

    HAVE_WEASYPRINT = True
except ImportError:
    HAVE_WEASYPRINT = False

FRONTMATTER_RE = re.compile(r"^---\n.*?\n---\n", re.S)
H2_RE = re.compile(r"^##\s+(.+)$")
H3_RE = re.compile(r"^###\s+(.+)$")
BULLET_RE = re.compile(r"^[-*]\s+(.+)$")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def load_yaml(path: Path) -> dict:
    if yaml is None:
        raise SystemExit("PyYAML required: pip install pyyaml")
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def parse_draft(text: str) -> dict:
    text = FRONTMATTER_RE.sub("", text)
    lines = text.splitlines()
    header_lines: list[str] = []
    sections: list[dict] = []
    i = 0
    while i < len(lines) and not H2_RE.match(lines[i]):
        if lines[i].strip():
            header_lines.append(lines[i].strip())
        i += 1
    current = None
    buf_para: list[str] = []
    buf_bullets: list[str] = []
    sub = None

    def flush_blocks(sec):
        nonlocal buf_para, buf_bullets, sub
        if sub is not None:
            if buf_bullets:
                sub["bullets"].extend(buf_bullets)
                buf_bullets = []
            sec["blocks"].append(sub)
            sub = None
        if buf_bullets:
            sec["blocks"].append({"type": "bullets", "items": buf_bullets})
            buf_bullets = []
        if buf_para:
            sec["blocks"].append({"type": "paragraph", "text": "\n".join(buf_para)})
            buf_para = []

    while i < len(lines):
        line = lines[i]
        m2 = H2_RE.match(line)
        m3 = H3_RE.match(line)
        mb = BULLET_RE.match(line)
        if m2:
            if current:
                flush_blocks(current)
                sections.append(current)
            current = {"heading": m2.group(1).strip(), "blocks": []}
            sub = None
        elif m3 and current is not None:
            flush_blocks(current)
            sub = {"type": "subsection", "heading": m3.group(1).strip(), "meta": {"org": "", "dates": ""}, "bullets": []}
        elif mb and current is not None:
            if buf_para:
                current["blocks"].append({"type": "paragraph", "text": "\n".join(buf_para)})
                buf_para = []
            if sub is not None:
                sub["bullets"].append(mb.group(1).strip())
            else:
                buf_bullets.append(mb.group(1).strip())
        elif current is not None:
            if line.strip() == "":
                if buf_bullets and sub is None:
                    current["blocks"].append({"type": "bullets", "items": buf_bullets})
                    buf_bullets = []
                elif buf_para:
                    current["blocks"].append({"type": "paragraph", "text": "\n".join(buf_para)})
                    buf_para = []
            else:
                if buf_bullets and sub is None:
                    current["blocks"].append({"type": "bullets", "items": buf_bullets})
                    buf_bullets = []
                buf_para.append(line.strip())
        i += 1
    if current:
        flush_blocks(current)
        sections.append(current)
    name = header_lines[0] if header_lines else ""
    return {"header": {"name": name, "contact_lines": header_lines[1:]}, "sections": sections}


def check_style_must(style: dict) -> list[str]:
    layout = style.get("layout") or {}
    must = {
        "single_column": True,
        "tables": False,
        "text_boxes": False,
        "content_headers_footers": False,
        "real_list_styles": True,
    }
    return [f"layout.{k} must be {v}" for k, v in must.items() if layout.get(k) != v]


def render_md(model: dict, identity: dict) -> str:
    name = identity.get("name") or model["header"]["name"]
    contact = identity.get("contact") or {}
    lines = [name]
    bits = [contact.get("email"), contact.get("phone"), contact.get("location")]
    lines.append(" · ".join(x for x in bits if x))
    for link in contact.get("links") or []:
        lines.append(str(link))
    lines.append("")
    for sec in model["sections"]:
        lines.append(f"## {sec['heading']}")
        lines.append("")
        for block in sec["blocks"]:
            if block["type"] == "paragraph":
                lines.append(block["text"])
                lines.append("")
            elif block["type"] == "bullets":
                for it in block["items"]:
                    lines.append(f"- {it}")
                lines.append("")
            elif block["type"] == "subsection":
                lines.append(f"### {block['heading']}")
                meta = block.get("meta") or {}
                if meta.get("org") or meta.get("dates"):
                    lines.append(f"{meta.get('org','')} — {meta.get('dates','')}".strip(" —"))
                for it in block.get("bullets") or []:
                    lines.append(f"- {it}")
                lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_html(model: dict, identity: dict, style: dict) -> str:
    md_like = render_md(model, identity)
    # minimal semantic HTML from model
    name = identity.get("name") or model["header"]["name"]
    margins = (style.get("page") or {}).get("margins") or {}
    margin_css = " ".join(margins.get(k, "20mm") for k in ("top", "right", "bottom", "left"))
    parts = [
        "<!DOCTYPE html><html><head><meta charset='utf-8'><style>",
        f"@page {{ size: {(style.get('page') or {}).get('size', 'A4')}; margin: {margin_css}; }}",
        "body { font-family: Calibri, Arial, sans-serif; font-size: 10.5pt; color: #000; }",
        "h1 { font-size: 16pt; } h2 { font-size: 12pt; } ul { list-style: disc; }",
        "</style></head><body>",
        f"<h1>{_esc(name)}</h1>",
    ]
    contact = identity.get("contact") or {}
    parts.append("<p>" + _esc(" · ".join(x for x in [contact.get("email"), contact.get("phone"), contact.get("location")] if x)) + "</p>")
    for sec in model["sections"]:
        parts.append(f"<h2>{_esc(sec['heading'])}</h2>")
        for block in sec["blocks"]:
            if block["type"] == "paragraph":
                parts.append(f"<p>{_esc(block['text'])}</p>")
            elif block["type"] == "bullets":
                parts.append("<ul>" + "".join(f"<li>{_esc(i)}</li>" for i in block["items"]) + "</ul>")
            elif block["type"] == "subsection":
                parts.append(f"<h3>{_esc(block['heading'])}</h3>")
                parts.append("<ul>" + "".join(f"<li>{_esc(i)}</li>" for i in block.get("bullets") or []) + "</ul>")
    parts.append("</body></html>")
    return "\n".join(parts)


def _esc(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def render_docx(model: dict, identity: dict, style: dict, path: Path) -> None:
    doc = Document()
    name = identity.get("name") or model["header"]["name"]
    doc.add_heading(name, level=0)
    contact = identity.get("contact") or {}
    doc.add_paragraph(" · ".join(x for x in [contact.get("email"), contact.get("phone"), contact.get("location")] if x))
    for sec in model["sections"]:
        doc.add_heading(sec["heading"], level=1)
        for block in sec["blocks"]:
            if block["type"] == "paragraph":
                doc.add_paragraph(block["text"])
            elif block["type"] == "bullets":
                for it in block["items"]:
                    doc.add_paragraph(it, style="List Bullet")
            elif block["type"] == "subsection":
                doc.add_heading(block["heading"], level=2)
                for it in block.get("bullets") or []:
                    doc.add_paragraph(it, style="List Bullet")
    doc.save(path)


def check_env(requested: list[str]) -> int:
    rows = [
        ("md", True, "stdlib", ""),
        ("html", True, "stdlib", ""),
        ("docx", HAVE_DOCX, _ver("docx"), "pip install python-docx"),
        ("pdf", HAVE_WEASYPRINT, _ver("weasyprint"), "pip install weasyprint"),
    ]
    print(f"{'format':<8} {'available':<10} {'version':<12} install_hint")
    missing = []
    for fmt, ok, ver, hint in rows:
        print(f"{fmt:<8} {str(ok):<10} {ver or '-':<12} {hint if not ok else ''}")
        if fmt in requested and not ok:
            missing.append(fmt)
    return 1 if missing else 0


def _ver(pkg: str) -> str:
    try:
        mod = __import__(pkg)
        return getattr(mod, "__version__", "?")
    except Exception:
        return ""


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("app_dir", type=Path, nargs="?", help="applications/<app>/ directory")
    p.add_argument("--formats", default="md,html,docx,pdf")
    p.add_argument("--check-env", action="store_true")
    p.add_argument("--career-root", type=Path, default=None, help="career root for identity/style")
    args = p.parse_args(argv)
    requested = [x.strip() for x in args.formats.split(",") if x.strip()]
    formats_explicit = any(a.startswith("--formats") for a in (argv or sys.argv[1:]))
    if args.check_env:
        return check_env(requested)

    if not args.app_dir:
        print("ERROR: app_dir required unless --check-env", file=sys.stderr)
        print("Recovery: 1) pass applications/<id>  2) --check-env", file=sys.stderr)
        return 2

    app_dir = args.app_dir.resolve()
    career = args.career_root or app_dir.parent.parent
    draft = app_dir / "draft.md"
    identity_path = career / "profile" / "identity.yaml"
    style_path = career / "profile" / "export-style.yaml"
    export_dir = app_dir / "export"

    if not identity_path.is_file():
        print(f"ERROR: identity missing: {identity_path}", file=sys.stderr)
        print("Recovery: 1) run bootstrap  2) create identity.yaml", file=sys.stderr)
        return 4

    warnings: list[str] = []
    if style_path.is_file():
        style = load_yaml(style_path)
    else:
        warnings.append("style missing; using safe defaults")
        style = {
            "page": {"size": "A4", "margins": {"top": "20mm", "bottom": "20mm", "left": "18mm", "right": "18mm"}},
            "layout": {
                "single_column": True,
                "tables": False,
                "text_boxes": False,
                "content_headers_footers": False,
                "real_list_styles": True,
            },
        }

    must_errs = check_style_must(style)
    if must_errs:
        for e in must_errs:
            print(f"ERROR: {e}", file=sys.stderr)
        print("Recovery: 1) fix style MUST flags  2) reset template", file=sys.stderr)
        return 3

    if not draft.is_file():
        print(f"ERROR: draft missing: {draft}", file=sys.stderr)
        print("Recovery: 1) run composition  2) pass correct app_dir", file=sys.stderr)
        return 2

    model = parse_draft(draft.read_text(encoding="utf-8"))
    if not model["sections"]:
        print("ERROR: draft.md has no ## sections", file=sys.stderr)
        print("Recovery: 1) re-render draft from composition  2) fix headings", file=sys.stderr)
        return 2

    identity = load_yaml(identity_path)
    try:
        export_dir.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        print(f"ERROR: cannot write export dir {export_dir}: {e}", file=sys.stderr)
        print("Recovery: 1) fix permissions  2) choose writable path", file=sys.stderr)
        return 5

    produced, skipped, outputs = [], [], []
    for fmt in requested:
        if fmt == "md":
            out = export_dir / "resume.md"
            out.write_text(render_md(model, identity), encoding="utf-8")
            produced.append(fmt)
            outputs.append({"format": fmt, "path": str(out.relative_to(app_dir)), "sha256": sha256_file(out), "bytes": out.stat().st_size})
        elif fmt == "html":
            out = export_dir / "resume.html"
            out.write_text(render_html(model, identity, style), encoding="utf-8")
            produced.append(fmt)
            outputs.append({"format": fmt, "path": str(out.relative_to(app_dir)), "sha256": sha256_file(out), "bytes": out.stat().st_size})
        elif fmt == "docx":
            if not HAVE_DOCX:
                if not formats_explicit:
                    skipped.append(fmt)
                    print("warn: python-docx missing; skipping docx", file=sys.stderr)
                else:
                    print("ERROR: docx requested but python-docx missing. pip install python-docx", file=sys.stderr)
                    return 1
            else:
                out = export_dir / "resume.docx"
                render_docx(model, identity, style, out)
                produced.append(fmt)
                outputs.append({"format": fmt, "path": str(out.relative_to(app_dir)), "sha256": sha256_file(out)})
        elif fmt == "pdf":
            if not HAVE_WEASYPRINT:
                if not formats_explicit:
                    skipped.append(fmt)
                    print("warn: weasyprint missing; skipping pdf", file=sys.stderr)
                else:
                    print("ERROR: pdf requested but weasyprint missing. pip install weasyprint", file=sys.stderr)
                    return 1
            else:
                html = render_html(model, identity, style)
                out = export_dir / "resume.pdf"
                WeasyHTML(string=html).write_pdf(out)
                produced.append(fmt)
                outputs.append({"format": fmt, "path": str(out.relative_to(app_dir)), "sha256": sha256_file(out)})
        else:
            print(f"ERROR: unknown format {fmt}", file=sys.stderr)
            return 1

    manifest = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ"),
        "application_id": app_dir.name,
        "inputs": {
            "draft_md": {"path": str(draft), "sha256": sha256_file(draft)},
            "identity_yaml": {"path": str(identity_path), "sha256": sha256_file(identity_path)},
            "export_style": {"path": str(style_path) if style_path.is_file() else None, "sha256": sha256_file(style_path) if style_path.is_file() else None},
        },
        "tool": {
            "python": ".".join(map(str, sys.version_info[:3])),
            "python_docx": _ver("docx") if HAVE_DOCX else None,
            "weasyprint": _ver("weasyprint") if HAVE_WEASYPRINT else None,
        },
        "requested_formats": requested,
        "produced_formats": produced,
        "skipped_formats": skipped,
        "outputs": outputs,
        "warnings": warnings,
    }
    man_path = export_dir / "export_manifest.yaml"
    if yaml:
        man_path.write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")
    else:
        man_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"Wrote {len(produced)} format(s) to {export_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

### `.cursor/skills/cv-creation/scripts/regenerate_views.py`

````python
#!/usr/bin/env python3
"""Regenerate applications/<app>/views/* from YAML sources. Never blocks on mismatch."""
from __future__ import annotations

import argparse
import hashlib
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def load_yaml(path: Path) -> dict:
    if not path.is_file():
        return {}
    if yaml is None:
        raise SystemExit("PyYAML required")
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def write_view(path: Path, sources: list[Path], body: str) -> str:
    joined = b"".join(s.read_bytes() if s.is_file() else b"" for s in sources)
    digest = sha256_bytes(joined)
    banner = f"<!-- GENERATED from {' + '.join(s.name for s in sources)}. Do not edit. sha256: {digest} -->\n"
    path.write_text(banner + body, encoding="utf-8")
    return digest


def regen(app_dir: Path) -> int:
    views = app_dir / "views"
    views.mkdir(exist_ok=True)
    meta = load_yaml(app_dir / "meta.yaml")
    req = app_dir / "requirements.yaml"
    kw = app_dir / "keywords.yaml"
    scores = app_dir / "scores.yaml"
    matching = app_dir / "matching.yaml"
    manifest_sources = {}

    app = meta.get("application") or {}
    title = f"{app.get('company', 'App')} · {app.get('role', '')} — CV application"

    body = f"# Requirements\n\nSource: requirements.yaml\n\n```yaml\n{(req.read_text(encoding='utf-8') if req.is_file() else 'requirements: []')}\n```\n"
    manifest_sources["requirements.md"] = write_view(views / "requirements.md", [req], body)

    body = f"# Keywords\n\n```yaml\n{(kw.read_text(encoding='utf-8') if kw.is_file() else 'jd_keywords: []')}\n```\n"
    manifest_sources["keywords.md"] = write_view(views / "keywords.md", [kw], body)

    body = f"# Scoring\n\n```yaml\n{(scores.read_text(encoding='utf-8') if scores.is_file() else 'job_skill_scores: []')}\n```\n"
    manifest_sources["scoring.md"] = write_view(views / "scoring.md", [scores], body)

    body = f"# Matching\n\n```yaml\n{(matching.read_text(encoding='utf-8') if matching.is_file() else 'matching: []')}\n```\n"
    manifest_sources["matching.md"] = write_view(views / "matching.md", [matching], body)

    tracker = f"""# {title}

> [!info] {app.get('id', app_dir.name)}
> JD: {app.get('jd_source', '')} · created {app.get('created', '')} · updated {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%MZ')}

Stage: {app.get('stage', '')} · flags {len(app.get('open_flags') or [])}
"""
    manifest_sources["tracker.md"] = write_view(
        views / "tracker.md",
        [app_dir / "meta.yaml", matching, scores],
        tracker,
    )

    man = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ"),
        "sources": {k: v for k, v in manifest_sources.items()},
    }
    if yaml:
        (views / "_manifest.yaml").write_text(yaml.safe_dump(man, sort_keys=False), encoding="utf-8")
    print(f"Regenerated views in {views}")
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("app_dir", type=Path)
    args = p.parse_args(argv)
    if not args.app_dir.is_dir():
        print(f"ERROR: not a directory: {args.app_dir}", file=sys.stderr)
        print("Recovery: 1) pass applications/<id>  2) create app first", file=sys.stderr)
        return 2
    return regen(args.app_dir)


if __name__ == "__main__":
    raise SystemExit(main())
````

### `.cursor/skills/cv-creation/scripts/validate_application.py`

```python
#!/usr/bin/env python3
"""Validate application artifacts, export-style MUST flags, and taxonomy DAG."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

MUST = {
    "single_column": True,
    "tables": False,
    "text_boxes": False,
    "content_headers_footers": False,
    "real_list_styles": True,
}


def load_yaml(path: Path):
    if yaml is None:
        raise SystemExit("PyYAML required: pip install pyyaml")
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def check_style(style: dict) -> list[str]:
    errors = []
    layout = style.get("layout") or {}
    for key, expected in MUST.items():
        if layout.get(key) != expected:
            errors.append(f"layout.{key} must be {expected}, got {layout.get(key)}")
    return errors


def check_taxonomy(skills_doc: dict) -> list[str]:
    errors = []
    skills = skills_doc.get("skills") or []
    ids = {s.get("id") for s in skills if s.get("id")}
    children: dict[str, list[str]] = {i: [] for i in ids}
    for s in skills:
        sid = s.get("id")
        parent = s.get("parent_id")
        if parent:
            if parent not in ids:
                errors.append(f"{sid}: unknown parent_id {parent}")
            else:
                children[parent].append(sid)
    # cycle detect
    visiting, visited = set(), set()

    def dfs(n: str) -> None:
        if n in visiting:
            errors.append(f"taxonomy cycle involving {n}")
            return
        if n in visited:
            return
        visiting.add(n)
        for c in children.get(n, []):
            dfs(c)
        visiting.remove(n)
        visited.add(n)

    for i in ids:
        dfs(i)
    return errors


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--style", type=Path, help="export-style.yaml")
    p.add_argument("--skills", type=Path, help="skills.yaml")
    p.add_argument("--composition", type=Path, help="composition.yaml")
    p.add_argument("--draft", type=Path, help="draft.md (existence check)")
    args = p.parse_args(argv)
    errors: list[str] = []
    if args.style:
        if not args.style.is_file():
            print(f"ERROR: style missing: {args.style}", file=sys.stderr)
            return 4
        errors.extend(check_style(load_yaml(args.style)))
        if any("layout." in e for e in errors):
            for e in errors:
                print(f"ERROR: {e}", file=sys.stderr)
            print("Recovery: 1) reset from export-style.template.yaml  2) fix MUST flags", file=sys.stderr)
            return 3
    if args.skills and args.skills.is_file():
        errors.extend(check_taxonomy(load_yaml(args.skills)))
    if args.composition and args.composition.is_file():
        comp = load_yaml(args.composition)
        if (comp.get("grounding") or {}).get("uncovered"):
            errors.append("grounding.uncovered must be empty at G4")
    if args.draft and not args.draft.is_file():
        errors.append(f"draft missing: {args.draft}")
    if errors:
        for e in errors:
            print(f"ERROR: {e}", file=sys.stderr)
        print("Recovery: 1) fix listed issues  2) re-run validator", file=sys.stderr)
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

### `.cursor/skills/cv-creation/scripts/verify_views.py`

```python
#!/usr/bin/env python3
"""Verify views banners/hashes. Exit 0 match, 1 stale, 2 missing banner."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

BANNER_RE = re.compile(r"^<!-- GENERATED from .* sha256: ([a-f0-9]+) -->")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("app_dir", type=Path)
    args = p.parse_args(argv)
    views = args.app_dir / "views"
    if not views.is_dir():
        print("ERROR: views/ missing", file=sys.stderr)
        print("Recovery: 1) regen-views  2) check app_dir", file=sys.stderr)
        return 2
    status = 0
    for path in sorted(views.glob("*.md")):
        first = path.read_text(encoding="utf-8").splitlines()[:1]
        if not first or not BANNER_RE.match(first[0]):
            print(f"MISSING BANNER: {path.name}", file=sys.stderr)
            status = 2
            continue
        print(f"OK banner: {path.name}")
    # Stale detection vs sources is done by comparing regen; here we only ensure banners exist.
    # Callers who need hash recompute should run regenerate_views and diff.
    return status


if __name__ == "__main__":
    raise SystemExit(main())
```

### `.cursor/skills/evidence-bank/SKILL.md`

````markdown
---
name: evidence-bank
description: >-
  Maintain a de-styled career evidence bank (facts, experiences, skill links).
  Use when the user wants to capture, probe, destyle, validate, or waive CV evidence;
  when cv-creation routes a gap probe or differentiator to the bank; or for a single-item probe.
---

# Evidence Bank

## Purpose

Store **de-styled facts** only. Voice never enters this skill. Provenance is mandatory. No fabrication.

Design SoT: repo `EVIDENCE-BANK-DECISIONS.md`. UI labeling: repo `COMMUNICATION_CONTRACT.md`.

## When to load

| File | When |
|---|---|
| `references/evidence-schema.md` | Creating or editing evidence rows |
| `references/destyling-rules.md` | Ingesting resume / LinkedIn / manual / route-to-bank claims |
| `references/probe-question-bank.md` | Running a gap or ambiguity probe |
| `references/status-taxonomy.md` | Setting `status` / waiver reasons |
| `references/probe-ui.md` | Rendering Turn 1 / Turn 3 / Turn 6 |
| `assets/evidence-record-template.yaml` | New file or empty-bank scaffold |
| `assets/de-styling-checklist.md` | Before proposing a row for Turn 1 |
| `assets/probe-checklist.md` | Before closing a probe |
| `scripts/validate_evidence.py` | Before persist; on user `validate` |

## Invocation

Chat verbs (shared grammar with cv-creation `references/invocation.md`): `run` / `continue`, `status`, `show`, `probe`, `gate`, `validate`.

Config: read `career.config.yaml` at start. Paths are never hardcoded.

## Ingest surfaces (allowed)

1. Master resume — PDF and/or Markdown  
2. LinkedIn — **paste** (text dump only; no live scrape)  
3. Manual entry  
4. cv-creation **route-to-bank** (gap / differentiator / buffered flag)

Company URL fetch is **not** an ingest surface; only with explicit per-URL OK when routed for differentiators.

## Pipeline

### Bulk ingest mode

1. Load `profile/evidence.yaml` + `profile/skills.yaml` (create empty evidence from template if missing).  
2. Extract candidates from the ingest surface → apply `destyling-rules.md` → pass `de-styling-checklist.md` → enqueue.  
3. Process queue **one item at a time** with **Turn 1: Experience validation** (mandatory solo HITL; no batch confirm).  
4. On each Turn 1, propose `sk_*` + strength + recency; user confirms or edits.  
5. Persist after each decision; run `validate_evidence.py`.  
6. When the queue drains, offer optional **Turn 6: Gate summary** (ingest rollup).  

### Single-item mode

Same item states; no bulk queue. Used for `probe`, Turn 3: Gap probe from cv-creation, and route-to-bank.

### Item states

```
pending → destyled → awaiting_hitl → fact | waived | ambiguous
```

## Evidence rules (summary)

- No row without a `source` span.  
- `unverified` may sit queued with empty `probe_history`; append history before → `fact`.  
- `ambiguous` / `waived` require `probe_history` (validator hard-fail).  
- `waived` is terminal; reason in `probe_history`.  
- `probe_history` entry: `{ts, kind, question?, answer?, decision}` (minimal).  
- Clean amend with clear source may skip a new probe question; still needs Turn 1.  
- `strength` and `recency` live on `evidence_skills` links, not the evidence row.  
- Experiences: one `exp_*` per **role**; overlap allowed; `end: present` for current.  
- Never invent facts. Never apply voice.  

## Human labeling

- Never show bare `T1`…`T8` to the user. Use **`Turn N: <plain name>`** (optional `(TN)` after).  
- When a queue/stage total is known, show **`current of total`** in the header or question line.  

## Turn types owned here

- **Turn 1: Experience validation** — confirm / amend / waive / mark ambiguous  
- **Turn 3: Gap probe** — shared verbatim body/decisions below  
- **Turn 6: Gate summary** — shared verbatim body/decisions below  

Load `references/probe-ui.md` for gui/tui envelopes and examples.

### Cross-skill contract — T3 Gap probe (verbatim)

**Owner:** both skills (identical text required).

**When:** A required skill has action `gap`, or matching needs a single-item evidence probe.

**Body (must include):**
- requirement text (or id)
- missing `sk_*` (canonical name + id)
- exactly one probe question from the probe-question bank
- linked evidence candidates if any (ids only)

**Decisions (exact labels):** `has evidence` / `no evidence` / `waive`

**Envelope:** use the standard primitive envelope (gui or tui per `ui.chat_host`). One decision per turn.


### Cross-skill contract — T6 Gate summary (verbatim)

**Owner:** both skills (identical text required).

**When:** End of a stage loop, before gate pass.

**Body (must include):**
- stage name and item rollup (done / awaiting_hitl / pending)
- action counts with **inline definitions**:
  - `core` — high priority + strong evidence
  - `use` — high priority + moderate evidence
  - `covered_indirectly` — met via a broader evidence row
  - `mention` — low priority, evidenced (skills line only)
  - `gap` — required, not evidenced
  - `ask_user` — weak or stale evidence — probe before deciding
- buffered-flag count

**Decisions (exact labels):** `approve` / `revise` / `resolve` / `accept`

**Envelope:** standard primitive envelope. Tracker line may accompany; active primitive last.


### Action definitions (canonical)

| Action | Meaning |
|---|---|
| `core` | high priority + strong evidence |
| `use` | high priority + moderate evidence |
| `covered_indirectly` | met via a broader evidence row |
| `mention` | low priority, evidenced (skills line only) |
| `gap` | required, not evidenced |
| `ask_user` | weak or stale evidence — probe before deciding |

## Validation

```bash
python scripts/validate_evidence.py path/to/profile/evidence.yaml
```

Hard-fail (exit 1): missing id/source; duplicate ids; bad `experience_id`; invalid status/strength/recency; `ambiguous`/`unverified` without `probe_history`; unknown `evidence_id` on links; `skill_id` missing when link present.

Warn (exit 0): empty bank; experience with no evidence rows.

Smoke fixtures:

```bash
python scripts/validate_evidence.py assets/fixtures/ok.yaml          # expect OK
python scripts/validate_evidence.py assets/fixtures/bad-missing-source.yaml  # expect fail
```

## Privacy

No telemetry. Do not fetch URLs unless the user explicitly approves each URL.

## Errors

Name path and attempt; offer ≥2 recoveries; quote parse line numbers. Abort the item loop without corrupting state.
````

### `.cursor/skills/evidence-bank/assets/de-styling-checklist.md`

```markdown
# De-styling checklist

Complete **before** proposing a row for Turn 1: Experience validation.

- [ ] No superlatives / fluff / slogan language
- [ ] Actor clear (`self` / `team`)
- [ ] Action verb plain
- [ ] Object / system named
- [ ] Tools only if present in source
- [ ] Metrics not inflated vs source
- [ ] Outcome only if evidenced
- [ ] Source span present (file + location, or paste date + index, or user+doc)
- [ ] No voice-profile content mixed in
```

### `.cursor/skills/evidence-bank/assets/evidence-record-template.yaml`

```yaml
experiences: []
evidence: []
evidence_skills: []
```

### `.cursor/skills/evidence-bank/assets/probe-checklist.md`

```markdown
# Probe checklist

Before closing a probe or promoting to `fact`:

- [ ] Exactly one question asked this turn
- [ ] Source span requested if claiming a new fact
- [ ] Destyle rules + de-styling checklist applied
- [ ] Skill ids proposed for links (with strength + recency)
- [ ] User completed Turn 1 (solo) — no batch confirm
- [ ] `probe_history` updated when required (unverified/ambiguous → fact; every waive)
- [ ] Status updated only after user decision
- [ ] `validate_evidence.py` clean on the target file
```

### `.cursor/skills/evidence-bank/assets/fixtures/ok.yaml`

```yaml
experiences:
  - id: exp_acme_de
    title: Data Engineer
    org: Acme Corp
    start: 2022-03
    end: 2024-08
    location: Paris, FR

evidence:
  - id: ev_001
    experience_id: exp_acme_de
    fact: "Rebuilt nightly billing ETL with Python and Airflow on AWS; cut runtime 40% vs previous job"
    actor: self
    action: rebuilt
    object: nightly billing ETL
    scale: "~2M rows/night"
    metric: "runtime -40%"
    tool: [Python, Airflow, AWS, S3]
    date: 2023
    outcome: "production until migration"
    status: fact
    source: "master_resume_v7.pdf, p.2, bullet 3"
    probe_history:
      - ts: "2026-11-18T10:00:00Z"
        kind: confirm
        question: null
        answer: null
        decision: confirm
    revision_count: 0

evidence_skills:
  - evidence_id: ev_001
    skill_id: sk_python
    strength: strong
    recency: current
```

### `.cursor/skills/evidence-bank/assets/fixtures/bad-missing-source.yaml`

```yaml
experiences:
  - id: exp_acme_de
    title: Data Engineer
    org: Acme Corp
    start: 2022-03
    end: present
    location: Paris, FR

evidence:
  - id: ev_bad_001
    experience_id: exp_acme_de
    fact: "Did cloud things"
    actor: self
    action: did
    object: cloud things
    status: unverified
    source: ""
    probe_history: []
    revision_count: 0

evidence_skills: []
```

### `.cursor/skills/evidence-bank/references/destyling-rules.md`

```markdown
# Destyling rules

Strip marketing voice **before** proposing a row. Then pass `assets/de-styling-checklist.md`. Then **Turn 1: Experience validation** (mandatory solo HITL). Never silent-promote to `fact`.

Voice profile content must never be stored here.

## Remove

- Superlatives ("world-class", "passionate", "ninja", "transformative")
- Soft-skill filler without observable action
- Company slogan / branding language
- Unattributed team wins claimed as personal without probe
- First-person style flourishes that are voice, not fact

## Keep

- Actor, action, object
- Tools named in the **source**
- Metrics and scale as written (do not inflate)
- Dates / duration when present
- Outcome if evidenced in the source

## Transform

| From | To |
|---|---|
| "Spearheaded transformative cloud journey" | Plain action + object; drop "transformative" |
| "Helped the team deliver X" | Set `actor: team` or probe who did what |
| "Expert in Y" | Do not store as fact; link skill only via concrete work evidence |
| LinkedIn buzz ("driven results across…") | Concrete system, role, metric, or mark ambiguous |

## Ingest notes

- Master resume PDF/MD: cite page/section/bullet in `source`.  
- LinkedIn paste: cite paste date + bullet index (or quoted span).  
- Manual / route-to-bank: cite `user` plus any ticket/doc span the user provides.  

## Gate order (locked)

1. Extract  
2. Apply these rules  
3. Checklist (`assets/de-styling-checklist.md`)  
4. Propose → Turn 1 (one row per turn)
```

### `.cursor/skills/evidence-bank/references/evidence-schema.md`

````markdown
# Evidence schema

## File

Single file: `profile/evidence.yaml` holds `experiences`, `evidence`, and `evidence_skills`.

Taxonomy lives in `profile/skills.yaml` (bank links `sk_*`; does not own that file’s location).

## Experience

One row per **role**. Same org → multiple `exp_*`. Overlapping dates allowed when true. Current role: `end: present`.

```yaml
experiences:
  - id: exp_acme_de
    title: Data Engineer
    org: Acme Corp
    start: 2022-03
    end: 2024-08          # or present
    location: Paris, FR
```

## Evidence row

```yaml
evidence:
  - id: ev_001
    experience_id: exp_acme_de
    fact: "Rebuilt nightly billing ETL with Python and Airflow on AWS; cut runtime 40% vs previous job"
    actor: self
    action: rebuilt
    object: nightly billing ETL
    scale: "~2M rows/night"
    metric: "runtime -40%"
    tool: [Python, Airflow, AWS, S3]
    date: 2023
    outcome: "production until migration"
    status: fact                # fact | ambiguous | unverified | waived
    source: "master_resume_v7.pdf, p.2, bullet 3"
    probe_history: []
    revision_count: 0
```

### Rules

- `source` required — no provenance, no row.  
- `unverified` may have empty `probe_history` while queued; **before** promoting to `fact`, append history (probe and/or Turn 1 confirm).  
- `ambiguous` and `waived` require non-empty `probe_history` (validator hard-fail).  
- New ingest rows typically start as `unverified` until Turn 1 promotes them.  

### `probe_history` entry (minimal)

```yaml
probe_history:
  - ts: "2026-11-18T09:00:00Z"
    kind: waive                 # probe | confirm | amend | waive | mark_ambiguous | …
    question: null              # optional
    answer: null                # optional
    decision: waive
```

Clean amend with clear source may omit a new probe `question`; still append a history entry with `kind: amend` / `decision` when useful for audit.

## evidence_skills

Strength and recency are per **link**, not per evidence row. Matching floors are owned by cv-creation; bank stores user-approved values.

```yaml
evidence_skills:
  - evidence_id: ev_001
    skill_id: sk_python
    strength: strong            # weak | moderate | strong
    recency: current            # current | <3y | stale
```

On Turn 1: Experience validation, the agent proposes `sk_*` + strength + recency; the user confirms or edits on the same turn.
````

### `.cursor/skills/evidence-bank/references/probe-question-bank.md`

```markdown
# Probe question bank

Pick **exactly one** question per Turn 3: Gap probe (or ambiguity probe). Do not stack questions in one turn.

## Gap probes

1. "Do you have a concrete example where you used {skill}? What was the system and your role?"
2. "Was {skill} hands-on for you, or only adjacent (reviewed/configured by others)?"
3. "Approx. when did you last use {skill}, and at what scale?"

## Ambiguity probes

1. "Was the metric {metric} measured by you, and over what baseline?"
2. "Which tools in {tool_list} did you personally use?"
3. "Should this claim be waived for this application?"

## Differentiator → bank

1. "Can you point to a source span (resume, ticket, doc) for: {claim}?"
2. "If confirmed, which experience id should own this fact?"

After `has evidence`, destyle → checklist → Turn 1: Experience validation before `status: fact`.
```

### `.cursor/skills/evidence-bank/references/probe-ui.md`

````markdown
# Probe UI (evidence-bank)

Glyphs and envelope match cv-creation `ui-turn-types.md`. `ui.chat_host`: `gui` | `tui`. Glyph modes: unicode | ascii | emoji (chat `auto` → emoji on gui, unicode on tui).

**Human labeling:** never bare `T1` / `T3` / `T6` — use `Turn N: <plain name>`; show `current of total` when the queue/stage total is known. See repo `COMMUNICATION_CONTRACT.md`.

Turn 3 / Turn 6 **body fields and decision labels** are verbatim with cv-creation (see `SKILL.md`).

## Envelope

### gui

```markdown
**▸ Turn N: <plain name> · item-id · k of n**
**Field:** value
*One question.*
1. Option A
2. Option B
3. Other: …
*checkpoint ⟨ts⟩*
```

### tui

```
▸ Turn N: <plain name> · item-id · k of n
  ⟨body ≤12 lines, aligned⟩
  [1] Option A  [2] Option B  [other: …]
──────────────────────────────────────────── checkpoint ⟨ts⟩
```

## Turn 1: Experience validation — worked example (gui)

```markdown
**▸ Turn 1: Experience validation · ev_001 · 1 of 3**
**Fact:** Rebuilt nightly billing ETL with Python and Airflow on AWS; cut runtime 40%.
**Source:** master_resume_v7.pdf, p.2, bullet 3
**Skills (proposed):** sk_python (strong, current), sk_airflow (strong, current)
*Confirm this fact and skill links?*
1. confirm
2. amend
3. waive
4. mark ambiguous
*checkpoint 2026-11-21T09:00Z*
```

## Turn 1: Experience validation — worked example (tui)

```
▸ Turn 1: Experience validation · ev_001 · 1 of 3
  Fact: Rebuilt nightly billing ETL with Python and Airflow on AWS; cut runtime 40%.
  Source: master_resume_v7.pdf, p.2, bullet 3
  Skills: sk_python (strong, current), sk_airflow (strong, current)
  [1] confirm  [2] amend  [3] waive  [4] mark ambiguous
──────────────────────────────────────────── checkpoint 2026-11-21T09:00Z
```

## Turn 3: Gap probe — worked example (gui)

```markdown
**▸ Turn 3: Gap probe · r_4 · matching**
**Requirement:** Deep Airflow experience for production DAGs
**Missing skill:** sk_airflow (Airflow)
**Probe:** Do you have a concrete example where you used Airflow? What was the system and your role?
1. has evidence
2. no evidence
3. waive
*checkpoint 2026-11-21T09:10Z*
```

## Turn 3: Gap probe — worked example (tui)

```
▸ Turn 3: Gap probe · r_4 · matching
  Requirement: Deep Airflow experience for production DAGs
  Missing: sk_airflow (Airflow)
  Probe: Do you have a concrete example where you used Airflow? What was the system and your role?
  [1] has evidence  [2] no evidence  [3] waive
──────────────────────────────────────────── checkpoint 2026-11-21T09:10Z
```
````

### `.cursor/skills/evidence-bank/references/status-taxonomy.md`

```markdown
# Evidence status taxonomy

| Status | Meaning | Exit |
|---|---|---|
| `unverified` | Ingested or proposed; not yet approved | May have empty `probe_history` while queued; append history before → `fact` |
| `ambiguous` | Conflicting or unclear | Non-empty `probe_history` required (validator hard-fail) |
| `fact` | Approved de-styled fact (after Turn 1 confirm) | Usable in CV grounding |
| `waived` | Explicitly not usable | Terminal; non-empty `probe_history` reason (validator hard-fail) |

## Transitions

- `unverified` / `ambiguous` → `fact` | `waived` | amend (often back to `unverified`)  
- Never silent promote to `fact`  
- Every `waive` appends a `probe_history` entry  
- Clean amend with clear source may skip a new probe **question**; still use Turn 1  

## Defense in depth

1. `validate_evidence.py` — structure / provenance / refs  
2. Turn 1 — human fact gate  
3. cv-creation matching floors  
4. Composition grounding (`ev_*` citations)
```

### `.cursor/skills/evidence-bank/scripts/validate_evidence.py`

```python
#!/usr/bin/env python3
"""Validate profile/evidence.yaml structure and referential integrity.

Hard-fail (exit 1): integrity issues (Q8).
Warn (exit 0 with WARN lines): empty bank; experience with no evidence rows.
Exit 2: file missing / unreadable.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

VALID_STATUS = frozenset({"fact", "ambiguous", "unverified", "waived"})
VALID_STRENGTH = frozenset({"weak", "moderate", "strong"})
VALID_RECENCY = frozenset({"current", "<3y", "stale"})


def load_yaml(path: Path):
    if yaml is None:
        raise SystemExit("PyYAML required: pip install pyyaml")
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def validate(data: dict) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    experiences = data.get("experiences") or []
    evidence = data.get("evidence") or []
    links = data.get("evidence_skills") or []

    if not experiences and not evidence and not links:
        warnings.append("empty bank (no experiences, evidence, or links)")

    exp_ids: set[str] = set()
    for exp in experiences:
        eid = exp.get("id")
        if not eid:
            errors.append("experience row missing id")
            continue
        if eid in exp_ids:
            errors.append(f"duplicate experience id {eid}")
        exp_ids.add(eid)

    ev_ids: set[str] = set()
    evidence_by_exp: dict[str, int] = {i: 0 for i in exp_ids}

    for row in evidence:
        eid = row.get("id")
        if not eid:
            errors.append("evidence row missing id")
            continue
        if eid in ev_ids:
            errors.append(f"duplicate evidence id {eid}")
        ev_ids.add(eid)

        source = row.get("source")
        if source is None or (isinstance(source, str) and not source.strip()):
            errors.append(f"{eid}: missing source")

        exp = row.get("experience_id")
        if not exp:
            errors.append(f"{eid}: missing experience_id")
        elif exp not in exp_ids:
            errors.append(f"{eid}: unknown experience_id {exp}")
        else:
            evidence_by_exp[exp] = evidence_by_exp.get(exp, 0) + 1

        status = row.get("status")
        hist = row.get("probe_history") or []
        if status is None:
            errors.append(f"{eid}: missing status")
        elif status not in VALID_STATUS:
            errors.append(f"{eid}: invalid status {status}")
        elif status == "ambiguous" and not hist:
            # Ambiguity means a probe already ran or must be recorded.
            errors.append(f"{eid}: ambiguous requires probe_history")
        elif status == "waived" and not hist:
            errors.append(f"{eid}: waived requires probe_history reason")
        # unverified may have empty probe_history while queued (Q4);
        # skill must append history before promoting to fact.

    for exp_id, count in evidence_by_exp.items():
        if count == 0:
            warnings.append(f"{exp_id}: experience has no evidence rows yet")

    for link in links:
        ev = link.get("evidence_id")
        if ev not in ev_ids:
            errors.append(f"evidence_skills: unknown evidence_id {ev}")
        sk = link.get("skill_id")
        if not sk:
            errors.append(f"evidence_skills: missing skill_id on evidence_id {ev}")
        strength = link.get("strength")
        if strength is not None and strength not in VALID_STRENGTH:
            errors.append(f"invalid strength {strength!r} on {ev}")
        recency = link.get("recency")
        if recency is not None and recency not in VALID_RECENCY:
            errors.append(f"invalid recency {recency!r} on {ev}")

    return errors, warnings


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("evidence_yaml", type=Path, help="path to evidence.yaml")
    args = p.parse_args(argv)

    if not args.evidence_yaml.is_file():
        print(f"ERROR: file not found: {args.evidence_yaml}", file=sys.stderr)
        print("Recovery: 1) create from template  2) pass correct path", file=sys.stderr)
        return 2

    try:
        errors, warnings = validate(load_yaml(args.evidence_yaml))
    except Exception as exc:  # noqa: BLE001 — surface parse errors to operator
        print(f"ERROR: failed to read YAML: {exc}", file=sys.stderr)
        print("Recovery: 1) fix YAML syntax  2) re-run validate", file=sys.stderr)
        return 2

    for w in warnings:
        print(f"WARN: {w}", file=sys.stderr)

    if errors:
        for e in errors:
            print(f"ERROR: {e}", file=sys.stderr)
        print("Recovery: 1) fix listed rows  2) re-run validate", file=sys.stderr)
        return 1

    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

