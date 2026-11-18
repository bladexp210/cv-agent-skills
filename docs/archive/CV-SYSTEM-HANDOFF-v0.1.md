# CV System — Design & Build Handoff (v0.1)

## 0. How to use this file

1. Start a new DeepSeek chat.
2. Upload **this file only**. Nothing else is needed.
3. Type `read`.
4. Follow the working method in **§20**.
5. The session's **only deliverable** is the Architecture File specified in **§21**.
6. Download it, open a **fresh Cursor project**, add the file, tell Cursor to build.
7. Cursor produces one folder tree. Copy-paste it into `career/.cursor/skills/`.
8. The skills bootstrap the rest of `career/` on first run.

**The operational sections of this file are §20, §21, §22.** Sections §1–§19 are the settled design; read them as background, do not rewrite them, and use them as the reference when producing the deliverable.

**If you are the receiving session:** confirm you have read the whole file, restate §20 in one sentence, and stop for the user to say “go.”

**If you are the user:** the short version is — the next session resolves open questions, designs the pending items, then writes out every file Cursor needs. It is expected to be long. Do not shortcut §21.

---

## Part B — Settled design (§1–§19)

### 1. Design principles (settled — do not reopen)

If you disagree with any of these, flag it once with evidence, then proceed.

1. **Two skills, not one.** CV creation and evidence-bank are separate skills with separate lifecycles.
2. **Facts and voice are separated.** Bank holds de-styled facts only. Voice is a separate reusable profile applied at composition.
3. **AI proposes, the user approves.** Every gate is explicit; no silent inference is promoted to a fact.
4. **Differentiators are hypotheses, not claims.** They reorder or re-emphasize existing evidence. Never inject new claims.
5. **State is loops, not a linear chain.** `approved` is an exit transition. Backward edges are explicit and flag-triggered.
6. **One canonical file per artifact.** Markdown views are generated into `views/` and are read-only.
7. **Checkpoints are durable, structured, layered.** Decisions, rejections, pending capture, state.
8. **User judgment is the tie-breaker.** Conflicts surface. Rules are optional and scoped when saved.
9. **Skill code and career data are separated.** Code in `.cursor/skills/`; data in the project tree.
10. **No fabrication.** A fact in the CV without a supporting evidence row is a bug.

### 2. System overview

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

- **Evidence-Bank Skill** — builds and maintains the reusable fact base from the master resume via a probe loop. Exposes a single-item probe interface for the CV skill's matching stage.
- **CV Creation Skill** — one application end-to-end: JD intake → requirements → skills/keywords → scoring → matching → composition → ATS check → export.

### 3. Data model

Persistent structured data lives in YAML. Markdown carries only human-facing narrative. No artifact is duplicated as both.

#### 3.1 Taxonomy

```yaml
# profile/skills.yaml
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

`modifier` is a non-skill (e.g., "production", "fast-paced"). Modifiers are extracted from JDs to filter noise, not scored. Parent/child expresses taxonomy, not containment in requirements.

#### 3.2 Evidence bank

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
    probe_history: []
    revision_count: 0

evidence_skills:
  - evidence_id: ev_001
    skill_id: sk_python
    strength: strong          # weak | moderate | strong
    recency: current          # current | <3y | stale
```

Rules:
- Every `evidence` row has a `source` span — no provenance, no row.
- `status: ambiguous | unverified` requires a `probe_history` entry before approval.
- `waived` is a valid terminal status; `probe_history` records the reason.
- `strength` and `recency` are per (evidence, skill) link, not per evidence row.

#### 3.3 Per-application data

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
# scores.yaml (materialized view)
job_skill_scores:
  - skill_id: sk_python
    importance_sum: 10.5
    priority_raw: 10.5
    priority_norm: 100
    frequency: 2
    ats_weight: 4              # 1..5
```

```yaml
# matching.yaml
matching:
  - skill_id: sk_python
    priority_norm: 100
    best_evidence_id: ev_001
    strength: strong
    action: core               # core | use | covered_indirectly | mention | gap | ask_user
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
  stage: matching
  stage_items: { total: 14, done: 11, awaiting_hitl: 2, pending: 1 }
  open_flags: [f_003, f_007]
  revision_counts: { r_3: 2, r_7: 1 }
```

#### 3.4 Profile-level reusable artifacts

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
```

### 4. Filesystem layout

#### 4.1 Project tree

```
career/                              ← project root (open as Cursor workspace)
  career.config.yaml                 ← required; path + defaults
  .cursor/skills/
    evidence-bank/                   ← SKILL.md, references/, assets/, scripts/
    cv-creation/
  profile/
    identity.yaml
    voice.md
    evidence.yaml
    skills.yaml                      ← taxonomy
    norms/
      <industry>-<country>-<lang>.md
      _overrides.yaml
    templates/
  applications/
    <company>-<role>-<yyyy-mm-dd>/
      meta.yaml
      jd.md
      requirements.yaml
      keywords.yaml
      scores.yaml
      matching.yaml
      draft.md
      audit.md
      notes.md
      views/                         ← GENERATED, read-only
        requirements.md
        keywords.md
        scoring.md
        matching.md
        _manifest.yaml
  _skill_state/
    <application-id>/
      <timestamp>-<slug>.yaml
      index.yaml
  assets/
    checklists/
    question-banks/
    reference-cv-examples/
```

#### 4.2 Config

```yaml
# career.config.yaml
career_root: "."
defaults:
  country: FR
  language: en
  seniority: senior
  industry: data-engineering
checkpointing:
  turn_floor: 10
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

**Rule:** Neither skill hardcodes paths. Both read `career.config.yaml` at run start. If absent, run onboarding.

### 5. Pipeline (CV creation skill)

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

**Backward edges (flag-triggered only):**

| From | To | Trigger |
|---|---|---|
| [4] Scoring | [2] Requirements | Noise detected (modifier scored as skill) |
| [5] Matching | evidence bank (probe) | Gap or single-item ambiguity |
| [6] Composition | [5] Matching | Bullet can't be grounded in evidence |
| [7] ATS check | [6] Composition | Coverage below threshold |
| [7] ATS check | [5] Matching | Required skill absent from evidence entirely |

### 6. Scoring

- **`importance_in_req`** — per (requirement, skill), 1–5.
- **`requirement_weight`** — must_have=1.5, strong=1.25, required=1.0, nice_to_have=0.75.

```
contribution(skill, req) = importance_in_req × requirement_weight
priority_raw(skill)      = Σ over requirements
priority_norm            = 100 × priority_raw / max_raw
```

**`ats_weight` (1–5)** — JD-wide ATS signal from `jd_keywords`: occurrences + placement boost (title/summary) + exact alias match, capped at 5. **Tiebreaker only, not a multiplier.**

**Where stored:** `scores.yaml` (materialized; always rebuilt, never migrated).

**Noise:** `modifier`-type skills extracted but excluded from scoring; flagged for the gate.

### 7. Matching

```
required    = { skills with priority_norm > 0 }
evidenced   = { skills reachable from evidence_skills }

required ∩ evidenced  → core / use / covered_indirectly / mention
required − evidenced  → gaps                 (probe; never invent)
evidenced − required  → differentiators      (use sparingly)
```

| Action | Meaning |
|---|---|
| `core` | High priority, strong evidence |
| `use` | High priority, moderate evidence |
| `covered_indirectly` | Met via broader evidence row |
| `mention` | Low priority, evidenced — skills line only |
| `gap` | Required, not evidenced |
| `ask_user` | Weak or stale evidence — probe before deciding |

### 8. State machine (three levels)

#### Level 1 — item lifecycle

```
not_started → in_progress → awaiting_hitl ──approve──→ approved (exit)
                                  │  ↑
                           revise │  │ resubmit
                                  ▼  │
                                in_progress
```

No `revised` state. `in_progress` + `revision_count`. Only explicit `reopen` returns to `awaiting_hitl`.

#### Level 2 — stage loop

```
run_stage(stage):
  items = extract()
  while pending_item = next_pending(items):
      run item lifecycle
  if not gate(stage):
      goto re-extract
  stage.status = done
```

Exit: no pending items AND gate passed AND no open flags.

#### Level 3 — global

- **Full run:** [1] → [8] with all gates.
- **Resume:** read latest checkpoint, reconcile `pending_capture`, continue.
- **Single-item probe:** load item → probe → return. No stage transitions.

### 9. Checkpointing & retention

#### Triggers

- **Always** on state transition.
- **Always** before lossy operations (web search, large LLM call).
- **Every `checkpointing.turn_floor` turns** as a floor.
- **On open-flag count ≥ `checkpointing.flag_threshold`.**
- **On explicit command.**

#### Content

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

`pending_capture` items are resolved at next session start: promoted to the persistent file (voice, norms, evidence) or dismissed.

#### Retention & pinning

- Retention is **per application**.
- Unpinned checkpoints older than the most recent `retention_k` are deleted.
- **Pinned checkpoints are never deleted.** Pinned when it is the state immediately before a decision that was later revised or reversed.

Example: `after-matching.yaml` (2026-11-20) is pinned on 2026-11-21 when composition reveals matching missed a skill. A new `revised-matching.yaml` is written. `index.yaml` records both, with `pinned: true` on the first and `revised_by` pointing to the second.

### 10. Differentiators

| Source | Confidence | Use |
|---|---|---|
| JD text | 4–5 | Ordering / emphasis |
| Industry | 3–4 | Ordering / emphasis |
| Company (web) | 2–3 | Ordering / emphasis; URL recorded |
| User input | 5 | Becomes a fact once bank stores it |

**Hard boundary:** an unconfirmed differentiator influences selection/ordering only. To influence content, it passes through the evidence-bank skill, is probed, and is stored as an evidence row with `source: user`.

**Rejected differentiators** are recorded so re-runs don't re-derive them.

### 11. Norms and overrides

Norms files are parameterized, reusable, user-owned. Frontmatter includes `context`, `source[]`, `last_verified`, `confidence`.

**Precedence:** `overrides > more-specific > less-specific > global default`. Conflicts surface to the user; never auto-resolved.

**Tie-breaker prompt** presents the conflict, current values, and three save options: once, scoped rule, wider rule (ordered narrow→wide).

**Staleness:** `last_verified` older than `norms.staleness_months` triggers re-verification offer. Applies to overrides too.

### 12. Voice profile

**Location:** `profile/voice.md`. Created by elicitation, not per application. Applied by composition stage only.

**Captures:** sentence length, verb preferences, first-person stance, technical density, bullet structure, formatting habits.

**Does not capture:** tone outside CV norms, subjective claims, invented vocabulary.

**Never enters the evidence bank.**

### 13. View generation

Human-facing views in `views/` are **generated**, not hand-edited. Each carries a `<!-- GENERATED from ... -->` banner. `views/_manifest.yaml` stores sha256 of sources. Mismatch → warn and regenerate. Runs on every checkpoint.

### 14. Config & invocation

Config: `career.config.yaml`. Absent → onboarding.

Invocation grammar and command set are **pending** (see §17.9).

### 15. HITL gate catalogue

| Gate | After stage | Summary includes | Decisions |
|---|---|---|---|
| G1 | [2] Requirements | Extracted requirements, weights | Approve, revise, add/remove |
| G2 | [4] Scoring | Ranked skills, noise flags, tiebreakers | Approve, adjust, re-extract |
| G3 | [5] Matching | Actions, gaps, differentiators, probes | Approve, resolve gaps, accept |
| G4 | [6] Composition | Draft, section plan, evidence citation | Approve, revise, buffer-resolve |
| G5 | [7] ATS & consistency | Coverage table, warnings, backward-edge proposals | Approve, accept edge, export |

Drafting-stage flags are **buffered** and resolved at G4 as a batch.

### 16. Bootstrap (first run)

Trigger: `career.config.yaml` missing or profile tree incomplete.

1. Create directory tree.
2. Write `career.config.yaml`; ask user to confirm.
3. Create `profile/identity.yaml` via prompts.
4. `profile/evidence.yaml` — empty allowed; offer evidence-bank skill.
5. `profile/voice.md` — copy template, no elicitation.
6. `profile/norms/` — empty allowed; created lazily.
7. Print "what's empty and when you'll be prompted" report.

**Non-blocking.** Missing voice → prompted at composition. Missing norms → prompted at scoring.

### 17. Pending items (the session's work)

#### 17.1 UI/UX (priority 1)
- Visual tracker design: global view (stage, done/total, flags, revisions) and per-stage item view.
- Tracker surface decision: generated markdown, terminal block, chat-injected summary, or all three.
- Update cadence: per transition, per turn, on demand.
- Rendering primitives per turn type (experience validation, keyword validation, gap probe, differentiator confirmation, norms tie-breaker, gate summary, draft review, ATS report).
- HMI principles catalogue: attention, consistency, signal/noise, progressive disclosure.
- Onboarding wizard flow.
- Error rendering (parse failures, missing files, hash mismatches).
- Accessibility fallback (may be out of scope — decide).

#### 17.2 Composition stage (priority 1)
- Section plan generation.
- Bullet ordering from matching + differentiators + voice.
- Evidence-grounding contract (bullet → `ev_*` id).
- Voice application rules.
- Handling of unconfirmed differentiators (ordering/emphasis only).
- Buffering behavior for composition → matching backward edge.

#### 17.3 Export (priority 1)
- Output format(s): PDF, DOCX, markdown-first, both.
- Pipeline: draft.md → templating → final file.
- Format fidelity constraints (fonts, ATS-safe layouts).
- Where export artifacts live.

#### 17.4 ATS & consistency check (priority 2)
- Coverage formula.
- Threshold values.
- Consistency checks.
- Backward-edge proposals and user override.

#### 17.5 Voice elicitation (priority 2)
- Method (prompt bank, existing CVs, editing an example).
- Structural schema for `voice.md`.
- Validation (spot-check).

#### 17.6 Skill taxonomy (priority 2)
- Bundled with skill vs. `profile/skills.yaml` (per user).
- Alias resolution.
- Conflict handling.
- Update mechanism.

#### 17.7 Keyword extraction details (priority 2)
- "Keyword" vs. atomic skill in extraction.
- Decomposition of phrases covering multiple skills.
- Weighting inputs for `ats_weight`.

#### 17.8 Evidence strength & recency rubric (priority 2)
- Thresholds for `strong | moderate | weak`.
- Thresholds for `current | <3y | stale`.
- Handling of unquantified evidence.

#### 17.9 CLI / invocation grammar (priority 2)
- Commands: `new`, `resume`, `list`, `abandon`, `checkpoint`, `probe <item>`.
- Argument schemas.
- How the CV skill detects its current stage from `meta.yaml`.

#### 17.10 View regeneration script (priority 2)
- Implementation shape (Python vs. shell).
- Hash manifest format.
- Failure behavior on missing source.
- Where it runs.

#### 17.11 Checkpoint trigger thresholds (priority 3)
- Confirm defaults.
- Avoid double writes.

#### 17.12 Privacy & security (priority 3)
- Personal data all under `career/`; none in skills.
- At-rest expectations.
- Web search scope; opt-in vs. config.

#### 17.13 Version control (priority 3)
- Whether `career/` is a git repo by default.
- What is committed vs. gitignored.
- Skill versioning and migration policy.

#### 17.14 Multi-language (priority 3)
- Handling non-default language.
- Whether voice and norms are per-language.

#### 17.15 Testing (priority 3)
- Golden-set approach: fixtures.
- Acceptance tests per stage.
- Regression tests for drift detector, retention, backward edges.

#### 17.16 Open questions (resolve FIRST)
- **Skill packaging:** two independent skills, or one composite with two entry points?
- **Norms:** part of a skill, or agent behavior driven by `profile/norms/`?
- **Voice:** separate skill, or composition stage within CV creation skill?
- **Taxonomy location:** bundled with skill vs. `profile/skills.yaml`?
- **Tracker surface:** markdown, terminal, chat, or all three?
- **Export target:** PDF, DOCX, markdown, or configurable?
- **ATS check:** local ruleset, or web-informed per regime?

### 18. Working method (original — superseded by §20)

### 19. Change log

- **v0.1** — first consolidation. Data model, workflow, state machine, filesystem, checkpointing, norms, voice, differentiators. Pending items in §17. Open questions in §17.16.

---

## Part C — Session operations (§20–§22)

### 20. Working method for this session

Follow strictly. Stop at every 🔴.

**20.1 Onboarding (after user types `read`).**
- Confirm you have read all of §0–§22.
- Restate §20 in one sentence.
- Ask the user to say `go`.
- 🔴 **Stop.**

**20.2 Resolve §17.16 open questions.**
- Present each question with 2–3 viable options, one recommendation, and one-line tradeoffs.
- Ask the user to decide each; record the decisions.
- Do not proceed until all seven are resolved.
- 🔴 **Stop and show the decision record.**

**20.3 Design pending items in dependency order.**
- §17.1 UI/UX first (tracker surface decision drives everything).
- Then §17.2 Composition, §17.3 Export, §17.4 ATS, §17.5 Voice elicitation, §17.6 Taxonomy, §17.7 Keywords, §17.8 Rubrics, §17.9 CLI, §17.10 View regen, §17.11–§17.15 remaining.
- Present each design compactly. Do not write file contents yet.
- 🔴 **Stop after each cluster of related items** (UI/UX; composition+export; remaining).

**20.4 Produce the Architecture File (§21).**
- Only after §20.2 and §20.3 are complete.
- Long output. Do not truncate. Do not leave TODOs.
- 🔴 **Stop when finished.**

**20.5 Self-check against §22.**
- Walk through each acceptance criterion.
- Fix any that fail before declaring done.
- 🔴 **Stop. Deliver.**

**Behavioral rules:**
- Do not reopen §1–§19. If you must flag one, do it once with evidence and proceed.
- Do not compress the deliverable. If it is long, say so and continue.
- Do not propose alternate architecture at §20.4. The design is settled by then.
- Do not ask the user to “fill in later” items in the architecture file. If a gap exists, resolve it now.

### 21. Deliverable — the Architecture File

**21.1 Target of the build.**

Cursor will produce **one folder tree** to paste into `career/.cursor/skills/`. It must contain both skills, complete, and every asset the bootstrap needs. It must NOT produce the `career/` data tree — that is created by the skills on first run.

**21.2 The Architecture File itself.**

Produce **one markdown file**, self-contained, structured as follows:

```
# CV System — Architecture File (v1.0)
## A. Build target
   - The exact folder tree Cursor must produce
   - One-sentence purpose per file
## B. File contents
   - For every file: full path as heading, then a fenced code block with the complete content
   - Order: SKILL.md files first, then references/, then assets/, then scripts/
   - No placeholders, no "see §X", no TODOs
## C. Build order
   - Numbered steps for Cursor
## D. Verification checklist
   - Commands or checks Cursor can run against its own output
## E. Post-build handoff
   - What the user does next (copy into career/, run first invocation)
```

**21.3 File inventory Cursor must produce.**

```
.cursor/skills/
  evidence-bank/
    SKILL.md
    references/
      destyling-rules.md
      probe-question-bank.md
      status-taxonomy.md
      evidence-schema.md
    assets/
      evidence-record-template.yaml
      probe-checklist.md
      de-styling-checklist.md
    scripts/
      validate_evidence.py
  cv-creation/
    SKILL.md
    references/
      scoring-rubric.md
      matching-rules.md
      composition-rules.md
      voice-guide.md
      norms-guide.md
      hitl-gate-catalogue.md
      state-machine.md
      checkpoint-schema.md
      differentiator-rules.md
      ui-turn-types.md
    assets/
      career.config.template.yaml
      identity.template.yaml
      voice.template.md
      norms.template.md
      jd.template.md
      checkpoint.template.yaml
      application-meta.template.yaml
      tracker.template.md
      onboarding-checklist.md
    scripts/
      bootstrap_career.py
      regenerate_views.py
      verify_views.py
      validate_application.py
```

Adjust this inventory if a design decision in §20.3 implies a change (e.g., if voice becomes a separate skill, split accordingly). Document any change in §A of the architecture file.

**21.4 Content rules for every file.**

- **SKILL.md** — full frontmatter (`name`, `description` per Agent Skills spec); body with steps, edge cases, and explicit “when to load X” conditions for every reference and asset. Under 500 lines.
- **references/** — detailed documentation, loaded on demand. Include worked examples where the rule is non-obvious.
- **assets/** — complete templates ready to copy. Bootstrapping depends on these.
- **scripts/** — complete, runnable. Include docstring, imports, argument parsing, main block. No pseudo-code.
- **Cross-file consistency** — if SKILL.md mentions a path, that path exists in the tree. If a reference names an asset, the asset exists.

**21.5 What NOT to include.**

- Design rationale (§1–§19 already covers it; Cursor does not need it).
- Open decisions (must all be resolved at §20.2).
- Optional features not specified.
- Anything Cursor would have to invent.

### 22. Acceptance criteria

The session is done when the Architecture File satisfies all of:

1. **Completeness.** Every file in §21.3 has full content in §B of the architecture file. No TODOs, no “fill in later,” no `# ...` abbreviations.
2. **Self-containment.** No references to §1–§19. If a Cursor agent read only the architecture file, it can build the system.
3. **Path integrity.** Every path mentioned in any file exists in the inventory, or is explicitly created at runtime by bootstrap.
4. **Bootstrap works.** `assets/career.config.template.yaml` and the other templates are complete enough that `bootstrap_career.py` produces a working `career/` tree on first run, with only user-input prompts for identity fields.
5. **Both skills invocable.** Each `SKILL.md` description is triggerable (imperative, “Use when…”, covers both full-run and single-item-probe cases as appropriate).
6. **Cross-skill interface documented.** The single-item probe interface the evidence-bank skill exposes to the CV skill is specified in both `SKILL.md` files identically.
7. **Verification.** §D of the architecture file contains at least: (a) a syntax check for each Python script, (b) a tree diff Cursor can run to confirm all files were created, (c) a smoke test that invokes the bootstrap against an empty directory and inspects the result.
8. **No silent drift.** Every file the user might want to change later is a template in `assets/` or a reference in `references/`, not hardcoded in `SKILL.md`.

When all eight pass, declare the deliverable complete and hand off.

---

## 23. Change log addendum

- **v0.1b** — added §0 (usage), §20 (working method), §21 (deliverable spec), §22 (acceptance criteria). Spec §1–§19 carried forward unchanged. This version is the session handoff; it is not the deliverable.