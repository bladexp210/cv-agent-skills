# CV System — Specification & Architecture (v0.1)

**Status:** Design complete for data model, workflow, state, filesystem, and skill interfaces. Pending: UI/UX, composition stage, export, onboarding details, and the items in §17.

**Purpose:** A two-skill system that produces custom CVs that are undeniably the user's — factually grounded in a personal evidence bank, styled by a personal voice profile, and bounded by context-appropriate CV norms. AI is used for selection, ordering, emphasis, and phrasing; never for invention. The user is in control at every gate.

**Scope of this document:** Carries settled design decisions; enumerates the architecture that exists; identifies pending work for the next design session.

---

## 1. Design principles (settled — do not reopen)

If you disagree with any of these, flag it once with evidence, then proceed.

1. **Two skills, not one.** CV creation and evidence-bank are separate skills with separate lifecycles. The evidence bank is reusable across applications; the CV skill is per-application.
2. **Facts and voice are separated.** The evidence bank holds de-styled facts only. Voice lives in a separate reusable profile applied at composition. No style tokens enter the bank.
3. **AI proposes, the user approves.** Every gate is explicit; no silent inference is promoted to a fact.
4. **Differentiators are hypotheses, not claims.** An inference about the employer's values may reorder or re-emphasize existing evidence. It never injects a new factual claim about the user.
5. **State is loops, not a linear chain.** `approved` is an exit transition, not a successor state. Backward edges exist and are explicit.
6. **One canonical file per artifact.** Markdown views are generated into `views/` and are read-only.
7. **Checkpoints are durable, structured, and layered.** Beyond checklists: decisions, rejections, pending capture, and the state itself.
8. **User judgment is the tie-breaker.** Conflicts (norms, scoring, matching) surface to the user. Rules are optional and scoped when saved.
9. **Skill code and career data are separated.** Code lives in `.cursor/skills/`; data lives in the project tree. Neither depends on the other's internals.
10. **No fabrication.** A skill or a fact in the CV without a supporting evidence row is a bug, not a judgment call.

---

## 2. System overview

```
┌──────────────────────┐       ┌──────────────────────┐
│  Evidence-Bank Skill │◄─────►│   CV Creation Skill  │
│  (reusable lifecycle)│ probe │   (per-application)  │
└──────────────────────┘       └──────────────────────┘
        │                                │
        ▼                                ▼
  profile/evidence.yaml         applications/<app>/
  profile/evidence_skills       requirements.yaml
                                keywords.yaml
                                scores.yaml
                                matching.yaml
                                draft.md
                                views/*.md
```

- **Evidence-Bank Skill** — builds and maintains the reusable fact base from the master resume, via a probe loop with the user. Exposes a single-item probe interface for the CV skill's matching stage.
- **CV Creation Skill** — runs one application end-to-end: JD intake → requirements → skills/keywords → scoring → matching → composition → ATS check → export.

---

## 3. Data model

All persistent structured data lives in YAML. Markdown carries only human-facing narrative. No artifact is duplicated as both.

### 3.1 Taxonomy (global, in `profile/`)

```yaml
# profile/skills.yaml (or derived — see §17 open question)
skills:
  - id: sk_python
    canonical_name: Python
    type: language            # language | tool | framework | domain | practice | modifier
    parent_id: null
    aliases: [python3, py]
    ats_forms: [Python, python]
  - id: sk_aws_lambda
    canonical_name: AWS Lambda
    type: tool
    parent_id: sk_aws
    aliases: [lambda, lambda function]
    ats_forms: [Lambda, AWS Lambda]
```

**Type matters.** `modifier` is a non-skill (e.g., "production", "fast-paced"). Modifiers are extracted from JDs to filter noise, not scored. Parent/child expresses taxonomy (AWS → Lambda, S3), not containment in requirements.

### 3.2 Evidence bank (in `profile/evidence.yaml`)

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
    fact: "Rebuilt nightly billing ETL with Python and Airflow on AWS; cut runtime 40% vs. previous job"
    actor: self
    action: rebuilt
    object: nightly billing ETL
    scale: "~2M rows/night"
    metric: "runtime -40%"
    tool: [Python, Airflow, AWS, S3]
    date: 2023
    outcome: "production until migration"
    status: fact              # fact | ambiguous | unverified | waived
    source: "master_resume_v7.pdf, p.2, bullet 3"
    probe_history: []         # each resolution/waiver recorded
    revision_count: 0

evidence_skills:
  - evidence_id: ev_001
    skill_id: sk_python
    strength: strong          # weak | moderate | strong
    recency: current          # current | <3y | stale
  - evidence_id: ev_001
    skill_id: sk_airflow
    strength: strong
    recency: current
  - evidence_id: ev_001
    skill_id: sk_aws
    strength: moderate
    recency: current
```

Rules:
- Every `evidence` row has a `source` span (file + location) — no provenance, no row.
- `status: ambiguous | unverified` requires at least one entry in `probe_history` before approval.
- `waived` is a valid terminal status; `probe_history` records the reason.
- `strength` and `recency` are per (evidence, skill) link, not per evidence row.

### 3.3 Per-application data (in `applications/<app>/`)

```yaml
# requirements.yaml
requirements:
  - id: r_1
    text: "5+ years building production data pipelines in Python"
    emphasis: must_have        # must_have | strong | required | nice_to_have
    requirement_weight: 1.5    # 1.5 | 1.25 | 1.0 | 0.75
requirement_skills:
  - requirement_id: r_1
    skill_id: sk_python
    importance_in_req: 5       # 1..5
  - requirement_id: r_1
    skill_id: sk_data_pipelines
    importance_in_req: 4
```

```yaml
# keywords.yaml
jd_keywords:
  - id: kw_1
    raw_text: "k8s"
    normalized: "Kubernetes"
    occurrences: 1
    placement: body            # title | summary | body | boilerplate
keyword_skills:
  - keyword_id: kw_1
    skill_id: sk_kubernetes
```

```yaml
# scores.yaml (materialized view over requirements + keywords)
job_skill_scores:
  - skill_id: sk_python
    importance_sum: 10.5
    priority_raw: 10.5
    priority_norm: 100
    frequency: 2
    ats_weight: 4              # 1..5, derived from keywords
```

```yaml
# matching.yaml
matching:
  - skill_id: sk_python
    priority_norm: 100
    best_evidence_id: ev_001
    strength: strong
    action: core               # core | use | covered_indirectly | mention | gap | ask_user
    differentiator_ids: []
differentiators:
  - id: d_001
    text: "Hands-on cost optimization experience"
    source: industry           # jd | industry | company | user
    confidence: 3
    source_url: "https://..."
    confirmed_by_user: false
    rejected: false
```

```yaml
# meta.yaml
application:
  id: acme-dataeng-2026-11-20
  company: Acme
  role: Data Engineer
  jd_source: "https://..."
  created: 2026-11-20T10:00Z
  stage: matching              # current stage
  stage_items: { total: 14, done: 11, awaiting_hitl: 2, pending: 1 }
  open_flags: [f_003, f_007]
  revision_counts: { r_3: 2, r_7: 1 }
```

### 3.4 Profile-level reusable artifacts

```yaml
# profile/identity.yaml
name: ...
contact: { email, phone, location, links: [] }

# profile/norms/_overrides.yaml
- dimension: photo_policy
  value: no_photo
  scope: { country: FR, industry: data-engineering, seniority: senior }
  reason: "Convention in FR senior DE CVs; recruiter confirmed"
  created: 2026-11-20

# profile/voice.md — template + filled content (see §12)
```

---

## 4. Filesystem layout

### 4.1 Project tree

```
career/                              ← project root (open as Cursor workspace)
  career.config.yaml                 ← required; path + defaults
  .cursor/skills/
    evidence-bank/                   ← SKILL.md, references/, assets/, scripts/
    cv-creation/
  profile/                           ← reusable, user-owned
    identity.yaml
    voice.md
    evidence.yaml
    evidence_skills.yaml             ← may be merged into evidence.yaml
    skills.yaml                      ← skill taxonomy (or external)
    norms/
      <industry>-<country>-<lang>.md
      _overrides.yaml
    templates/                       ← CV layouts
  applications/
    <company>-<role>-<yyyy-mm-dd>/
      meta.yaml
      jd.md
      requirements.yaml
      keywords.yaml
      scores.yaml
      matching.yaml
      draft.md
      audit.md                       ← append-only decision log
      notes.md                       ← free text
      views/                         ← GENERATED, read-only
        requirements.md
        keywords.md
        scoring.md
        matching.md
        _manifest.yaml               ← sha256 of each view's source
  _skill_state/
    <application-id>/
      <timestamp>-<slug>.yaml        ← checkpoints
      index.yaml                     ← checkpoint index with pins
  assets/                            ← user-editable, skill-readable
    checklists/
    question-banks/
    reference-cv-examples/
```

### 4.2 Configuration

```yaml
# career.config.yaml
career_root: "."
defaults:
  country: FR
  language: en
  seniority: senior
  industry: data-engineering
checkpointing:
  turn_floor: 10                     ← safety-net turn count
  flag_threshold: 5
  retention_k: 20
norms:
  staleness_months: 12
paths:
  skills_dir: ".cursor/skills"
  profile_dir: "profile"
  applications_dir: "applications"
  state_dir: "_skill_state"
```

**Rule:** Neither skill hardcodes paths. Both read `career.config.yaml` at run start. If absent, the skill runs onboarding.

---

## 5. Pipeline (CV creation skill)

Stages run in order. Each has a HITL gate. Backward edges are explicit and flag-triggered only.

```
[0] Bootstrap        → ensure tree, config, minimum profile files
[1] JD intake        → jd.md, meta.yaml
[2] Requirements     → requirements.yaml
[3] Skills & keywords → keywords.yaml, taxonomy links
[4] Scoring          → scores.yaml
[5] Matching         → matching.yaml, differentiators (with evidence-bank probes)
[6] Composition      → draft.md
[7] ATS & consistency → audit.md additions, may loop back to [6] or [5]
[8] Export           → final file(s)
```

**HITL gates:** after [2], [4], [5], [6], [7]. Stage [8] is terminal unless export fails.

**Backward edges (only flag-triggered):**

| From | To | Trigger |
|---|---|---|
| [4] Scoring | [2] Requirements | Noise detected (e.g., `modifier` scored as skill) |
| [5] Matching | evidence bank (probe) | Gap or single-item ambiguity |
| [6] Composition | [5] Matching | Bullet can't be grounded in evidence |
| [7] ATS check | [6] Composition | Coverage below threshold |
| [7] ATS check | [5] Matching | Required skill absent from evidence entirely |

---

## 6. Scoring

Two distinct aggregations, computed once per application:

- **`importance_in_req`** — per (requirement, skill) — how central the skill is to *that* requirement (1–5).
- **`requirement_weight`** — per requirement — from emphasis markers: must_have=1.5, strong=1.25, required=1.0, nice_to_have=0.75.

```
contribution(skill, req) = importance_in_req × requirement_weight
priority_raw(skill)      = Σ over requirements (frequency is implicit in the sum)
priority_norm            = 100 × priority_raw / max_raw
```

**`ats_weight` (1–5)** is a *separate, JD-wide* ATS signal derived from `jd_keywords`:
- occurrences × 1
- +1 if placed in title or summary
- +1 if the skill's canonical name or an alias appears as a keyword (exact match)
- capped at 5

It is a **tiebreaker** in ranking and a **component** of the ATS coverage check. It is not a multiplier on priority.

**Where stored:** `scores.yaml` (materialized). Recomputable from `requirements.yaml` + `keywords.yaml` at any time; never migrated, always rebuilt.

**Noise handling:** `modifier` type skills are extracted but excluded from scoring. Detected as a flag for the gate.

---

## 7. Matching

The join between required skills and evidence:

```
required    = { skills with priority_norm > 0 in scores.yaml }
evidenced   = { skills reachable from evidence_skills }

required ∩ evidenced  → core / use / covered_indirectly / mention   (ranked by priority × strength)
required − evidenced  → gaps                                         (probe the evidence bank; never invent)
evidenced − required  → spare material / differentiators             (use sparingly; these make it yours)
```

Each required skill gets an `action`:

| Action | Meaning |
|---|---|
| `core` | High priority, strong evidence — placed in a prominent section |
| `use` | High priority, moderate evidence — placed but not over-emphasized |
| `covered_indirectly` | Priority is met by a broader evidence row (e.g., "Cloud warehouse" via Snowflake) |
| `mention` | Low priority but evidenced — skills line only |
| `gap` | Required, not evidenced — surfaced at gate |
| `ask_user` | Weak or stale evidence — probe before deciding |

**Differentiators** are stored alongside matching (see §10) and only influence **ordering/emphasis**, never invent content.

---

## 8. State machine (three levels)

### Level 1 — item lifecycle

```
not_started → in_progress → awaiting_hitl ──approve──→ approved (exit)
                                  │  ↑
                           revise │  │ resubmit
                                  ▼  │
                                in_progress
```

- No `revised` state. `in_progress` + `revision_count` field.
- `approved` is terminal for the item; only an explicit `reopen` moves it back.

### Level 2 — stage loop

```
run_stage(stage):
  items = extract()
  while pending_item = next_pending(items):
      run item lifecycle
      # user may add/remove items here → items changes → loop continues
  if not gate(stage):
      goto re-extract
  stage.status = done
```

**Exit:** no pending items AND gate passed AND no open flags.

### Level 3 — global

Three entry points:

- **Full run:** stage [1] → [8] with all gates.
- **Resume:** read latest checkpoint for the application, reconcile `pending_capture`, continue.
- **Single-item probe (from evidence-bank skill):** load item → probe → return → no stage transitions.

**Backward edges** as listed in §5. Each is created by a named flag with a reason and an owner (user or agent).

---

## 9. Checkpointing & retention

### 9.1 Triggers

- **Always** on state transition (item approved, gate passed, stage done, revision).
- **Always** before lossy operations (web search, large LLM call).
- **Every `checkpointing.turn_floor` turns** as a floor (safety net).
- **On open-flag count ≥ `checkpointing.flag_threshold`.**
- **On explicit command** (`checkpoint`).

### 9.2 Checkpoint content

```yaml
# _skill_state/<app-id>/<timestamp>-<slug>.yaml
state:
  stage: matching
  items: { total: 14, done: 11, awaiting_hitl: 2, pending: 1 }
  revision_counts: { r_3: 2, r_7: 1 }
  open_flags: [...]
decisions:
  - id: d_014
    what: "Airflow vs Dagster tie broken by ats_weight"
    why: "JD emphasis: Airflow named first, 2 mentions"
    at: 2026-11-18T14:22Z
rejected:
  - what: "Differentiator: cost-optimization experience (inferred)"
    why: "No evidence; user confirmed not applicable"
recent_context:
  - turn: 42
    summary: "User prefers bullet-led phrasing for metrics; not yet in voice.md"
    pending_capture: true
```

`pending_capture` items are resolved at next session start: promoted into the appropriate persistent file (voice, norms, evidence) or dismissed.

### 9.3 Retention & pinning

- Retention applies **per application**, not globally.
- Unpinned checkpoints older than the most recent `retention_k` are deleted.
- **Pinned checkpoints are never deleted.** A checkpoint is pinned when it is the *state immediately before a decision that was later reversed or revised*.

Example:
- 2026-11-20: checkpoint `after-matching.yaml`.
- 2026-11-21: during composition you realize matching missed `stakeholder communication`. Composition → matching backward edge fires.
- The `after-matching.yaml` checkpoint is **pinned** (before-of-revision).
- A new checkpoint `revised-matching.yaml` is written after re-match.
- `index.yaml` records: `pinned: true, revised_by: revised-matching.yaml`.

Pinned checkpoints answer "why is the draft the way it is?" — they are the audit trail.

### 9.4 Index

```yaml
# _skill_state/<app-id>/index.yaml
checkpoints:
  - file: 2026-11-20T14-00-after-matching.yaml
    pinned: true
    reason: "Before revision: stakeholder comm. reclassified from 'use' to 'core'"
    revised_by: 2026-11-21T09-00-revised-matching.yaml
```

---

## 10. Differentiators

A differentiator is a **hypothesis** about what the employer values, sourced from:

| Source | Confidence range | Use |
|---|---|---|
| JD text (explicit or strongly implied) | 4–5 | Ordering / emphasis |
| Industry context | 3–4 | Ordering / emphasis |
| Company context (web search) | 2–3 | Ordering / emphasis; source URL recorded |
| User input | 5 | Becomes a fact once evidence bank stores it |

```yaml
- id: d_001
  text: "Cost optimization"
  source: industry
  confidence: 3
  source_url: "https://..."
  confirmed_by_user: false
  rejected: false
```

**Hard boundary:** an unconfirmed differentiator influences selection/ordering only. To influence content, it must pass through the evidence-bank skill, be probed, and be stored as an evidence row with `source: user`. From that point it is a fact, not an inference.

**Rejected differentiators** are recorded (`rejected: true`) so re-runs don't re-derive them.

---

## 11. Norms and overrides

Norms are parameterized, reusable, and user-owned:

```yaml
# profile/norms/<industry>-<country>-<lang>.md  (frontmatter)
context: { industry, country, language, seniority_band, sector, ats_regime }
source:
  - { url: ..., retrieved: 2026-11-18 }
  - { user_edit: 2026-11-20 }
last_verified: 2026-11-18
confidence: 4
```

### 11.1 Precedence

`overrides > more-specific context > less-specific context > global default`

Conflicts are surfaced, never auto-resolved. The prompt presents:

```
Conflict: photo policy
  FR / data-engineering / senior  → no photo    (user_edit, 2026-11-15)
  EU / data-engineering / senior  → optional    (web, confidence 3)

Decide for this application:  [ no photo ] [ optional ] [ other ]
Save as:
  ( ) Once — this application only          (default)
  ( ) Rule — future <FR + data-engineering + senior>
  ( ) Rule — future <FR + any industry>
  ( ) Rule — global override for photo policy
```

### 11.2 Staleness

`last_verified` older than `norms.staleness_months` triggers a re-verification offer at next use. Overrides are subject to the same staleness check.

---

## 12. Voice profile

**Location:** `profile/voice.md`. **Created by:** elicitation session, not per application. **Applied by:** composition stage only.

**Voice captures:**
- Sentence length and rhythm preferences
- Verb preferences (action-led vs. outcome-led)
- First-person stance (implied vs. explicit)
- Technical density and jargon tolerance
- Bullet structure preferences (fragment vs. full sentence, metric-first vs. context-first)
- Formatting habits (dashes, parentheses, capitalization)

**Voice does not capture:** tone outside CV norms (flowery, narrative, humor), subjective claims, invented vocabulary.

**Storage:** frontmatter + prose + examples. `last_verified` and `confidence` fields same as norms.

**Consumption:** composition stage reads `voice.md`, applies it to drafting. Voice never enters the evidence bank.

---

## 13. View generation

Human-facing views in `views/` are **generated**, not hand-edited.

- Each view carries a banner: `<!-- GENERATED from ../<source>.yaml at <timestamp> — edit the YAML and regenerate -->`
- `views/_manifest.yaml` records sha256 of each source file.
- Any load path recomputes the hash; on mismatch, warn and regenerate before proceeding.
- Regeneration runs on every checkpoint.

The user edits YAML (structured) or `notes.md`/`audit.md` (free text). Views are never edited.

---

## 14. Config & invocation

- **Config:** `career.config.yaml` (§4.2). Absent → onboarding runs.
- **Invocation grammar:** stage names and item-scoped commands are the natural verbs. Exact syntax is pending (see §17).
- **Session lifecycle:** `new` (start an application), `resume` (read checkpoint), `list`, `abandon`, `probe <item>` (single-item evidence-bank probe).

---

## 15. HITL gate catalogue

Every gate produces a summary containing: stage, done/total, open flags, revision counts, and any conflicts requiring decision.

| Gate | After stage | Summary includes | Possible decisions |
|---|---|---|---|
| G1 | [2] Requirements | Extracted requirements, weights | Approve, revise, add/remove |
| G2 | [4] Scoring | Ranked skills, noise flags, tiebreakers | Approve, adjust, re-extract |
| G3 | [5] Matching | Actions per skill, gaps, differentiators, open probes | Approve, resolve gaps, accept differentiators |
| G4 | [6] Composition | Draft, section plan, evidence citation per bullet | Approve, revise, buffer-resolve gaps |
| G5 | [7] ATS & consistency | Coverage table, warnings, backward-edge proposals | Approve, accept edge, export |

Drafting-stage flags are **buffered** and resolved at G4 as a batch.

---

## 16. Bootstrap (first run)

Trigger: `career.config.yaml` missing or profile tree incomplete.

Steps:
1. Create directory tree per §4.1.
2. Write `career.config.yaml` with defaults; ask user to confirm.
3. Create `profile/identity.yaml` from prompts (minimal fields).
4. `profile/evidence.yaml` — empty allowed; offer to run the evidence-bank skill.
5. `profile/voice.md` — copy template, no elicitation at bootstrap.
6. `profile/norms/` — empty allowed; created lazily on first application.
7. Print a short “what's empty and when you'll be prompted for it” report.

**Non-blocking.** Missing voice → prompted at composition. Missing norms → prompted at scoring. Do not block the first application on profile completion.

---

## 17. Pending items (work for the next session)

### 17.1 UI/UX (priority 1)
- **Visual tracker design**
  - Global stage view: current stage, per-stage done/total, open flags, revision counts.
  - Per-stage item view: item list with status, revision counts, current gate state.
  - Where does the tracker live — a generated markdown file, a terminal-rendered block, a chat-injected summary, or all three?
  - Update cadence: per state transition, per turn, or on demand.
- **Rendering primitives per turn type**
  - Validation of an experience item
  - Validation of a keyword
  - Gap probe (single-item evidence-bank probe)
  - Differentiator confirmation
  - Norms conflict tie-breaker
  - Gate summary
  - Draft review
  - ATS coverage report
- **HMI principles catalogue** — attention, consistency, signal/noise, progressive disclosure in chat.
- **Onboarding wizard flow** — first-run prompts, ordering, skip rules.
- **Error rendering** — parse failures, missing files, corrupt views, hash mismatches.
- **Accessibility** — terminal and screen-reader fallback (may be out of scope; decide).

### 17.2 Composition stage (priority 1)
- Section plan generation (which sections, order, length).
- Bullet ordering from matching + differentiators + voice.
- Evidence-grounding contract (each bullet references an `ev_*` id).
- Voice application rules (how voice modifies phrasing without inventing facts).
- Handling of unconfirmed differentiators (ordering/emphasis only).
- Buffering behavior for composition → matching backward edge.

### 17.3 Export (priority 1)
- Output format(s): PDF, DOCX, markdown-first, both.
- Pipeline: draft.md → templating → final file.
- Format fidelity constraints (fonts, ATS-safe layouts).
- Where in the application folder export artifacts live.

### 17.4 ATS & consistency check (priority 2)
- Coverage formula: what counts as covered (canonical name in draft? alias? skills line?).
- Threshold values (per-application vs. per-skill).
- Consistency checks (dates, tense, voice markers, style tokens).
- Backward-edge proposals and user override behavior.

### 17.5 Voice elicitation (priority 2)
- Method for eliciting voice (prompt bank, existing CVs as input, editing an example).
- Structural schema for `voice.md`.
- How voice is validated (spot-check that bullets match profile without breaking norms).

### 17.6 Skill taxonomy (priority 2)
- Whether taxonomy is bundled with the skill or lives in `profile/skills.yaml` (open question: shared across users vs. per-user).
- Alias resolution algorithm.
- Conflict handling (two skills with overlapping aliases).
- Update mechanism (versioned taxonomy vs. free-form).

### 17.7 Keyword extraction details (priority 2)
- What counts as a "keyword" vs. an atomic skill in extraction.
- How phrases covering multiple skills (`cloud`, `data pipelines`) are decomposed.
- Weighting inputs for `ats_weight` (occurrences, placement, emphasis).

### 17.8 Evidence strength & recency rubric (priority 2)
- Thresholds for `strong | moderate | weak` per (evidence, skill).
- Thresholds for `current | <3y | stale`.
- Handling of unquantified evidence in the strength calculation.

### 17.9 CLI / invocation grammar (priority 2)
- Command set: `new`, `resume`, `list`, `abandon`, `checkpoint`, `probe <item>`.
- Argument schemas.
- How the CV skill detects its current stage from `meta.yaml`.

### 17.10 View regeneration script (priority 2)
- Implementation shape (Python vs. shell).
- Hash manifest format.
- Failure behavior on missing source.
- Where it runs (checkpoint hook vs. standalone command).

### 17.11 Checkpoint trigger thresholds (priority 3)
- Confirm `turn_floor: 10`, `flag_threshold: 5`, `retention_k: 20`.
- Interaction between flag-count checkpoint and gate-summary checkpoint (avoid double writes).

### 17.12 Privacy & security (priority 3)
- Where personal data lives (all under `career/`; none in `.cursor/skills/`).
- At-rest handling expectations (user's OS-level responsibility vs. skill-level).
- Web search: what leaves the machine, when, and how to disable.

### 17.13 Version control (priority 3)
- Whether `career/` is a git repo by default.
- What is committed vs. gitignored (views? checkpoints? applications?).
- Skill versioning and migration policy when schema changes.

### 17.14 Multi-language (priority 3)
- Handling of applications in non-default language.
- Whether voice and norms are per-language.

### 17.15 Testing (priority 3)
- Golden-set approach: a small corpus of JDs + a small evidence bank as fixtures.
- Acceptance tests per stage.
- Regression tests for the drift detector, checkpoint retention, and backward edges.

### 17.16 Open questions to resolve
- **Skill packaging:** two independent skills, or one composite skill with two entry points?
- **Norms:** part of a skill, or agent behavior driven by `profile/norms/`?
- **Voice:** separate skill, or composition stage within CV creation skill?
- **Taxonomy location:** bundled with skill (shared across users) vs. `profile/skills.yaml` (per user)?
- **Tracker surface:** markdown file, terminal output, chat-injected summary, or all three?
- **Export target:** PDF, DOCX, markdown, or a configurable pipeline?
- **ATS check:** local ruleset, or web-search-informed per ATS regime?

---

## 18. Working method for the next session

1. **Read this document and the attached CV skill / evidence-bank seed.** Summarize the current state and the pending list in your own words. Stop for confirmation.
2. **Resolve open questions in §17.16 first.** Each is a fork that changes downstream work; resolving them after designing UX would waste the work.
3. **Design UI/UX (§17.1) next.** The tracker surface decision drives how every other UI element is expressed.
4. **Design composition (§17.2) and export (§17.3)** in that order. Composition depends on matching output format; export depends on composition output.
5. **Fill the remaining §17 items** in order of dependency, not numbering.
6. **Produce a v0.2 of this document** with §17 replaced by designs, and a change log at the top.

Every decision in §1–§16 is settled. Disagreements get flagged once, with evidence, and then proceeded past unless the user changes their mind.

---

## 19. Change log

- **v0.1** — first consolidation. Settles data model, workflow, state machine, filesystem, checkpointing, norms, voice, differentiators. Enumerates pending items in §17. Open questions in §17.16.