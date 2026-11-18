# CV System — Handoff (v0.4 — all clusters closed)

## 0. How to use this file

1. Start a new DeepSeek chat.
2. Upload **this file only**.
3. Type `read`.
4. Follow **§20** (working method). Clusters 1–3 are complete; next is the Architecture File (§21).
5. The session's **only deliverable** is the Architecture File specified in **§21**.
6. Download it, open a fresh Cursor project, add it, tell Cursor to build.
7. Cursor produces one folder tree. Paste it into `career/.cursor/skills/`.
8. The skills bootstrap `career/` on first run.

**Operational sections: §19.5, §19.6, §19.7, §20, §21, §22.** §1–§19 settled design. Decision records: §19.5 Cluster 1, §19.6 Cluster 2, §19.7 Cluster 3 — read all, do not re-open.

**If you are the receiving session:** confirm you have read the whole file, restate §20 in one sentence, and stop for the user to say "go."

**If you are the user:** the next session writes the Architecture File (§21), then self-checks (§22). It is expected to be long. Do not shortcut §21.

**If you have v0.3:** the substantive addition is §19.7 (ATS through testing); §20 rewritten to produce the Architecture File; §21 inventory updated. §1–§19.6 unchanged in intent.

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
                                export/*
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
    export-style.yaml                ← copied from assets/export-style.template.yaml
    norms/
      <industry>-<country>-<lang>.md
      _overrides.yaml
      ats/
        <regime>.yaml                ← from assets/ats-rules.template.yaml
    templates/
  applications/
    <company>-<role>-<yyyy-mm-dd>/
      meta.yaml
      jd.md
      requirements.yaml
      keywords.yaml
      scores.yaml
      matching.yaml
      composition.yaml               ← structured companion to draft.md (§19.6)
      draft.md                       ← rendered narrative; always re-rendered from composition.yaml
      ats-check.yaml                 ← machine ATS/consistency result (§19.7)
      audit.md                       ← human ATS report (§19.7)
      notes.md
      views/                         ← GENERATED, read-only
        requirements.md
        keywords.md
        scoring.md
        matching.md
        tracker.md
        _manifest.yaml
      export/                        ← GENERATED (stage 8)
        resume.md
        resume.html
        resume.docx                  (if python-docx available)
        resume.pdf                   (if weasyprint available)
        export_manifest.yaml
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
ui:
  chat_host: gui          # gui | tui   (gui = Cursor and other markdown-rendering agents)
  tracker_fence: true     # render the chat tracker line as a fenced block on gui
  glyphs:
    chat:  auto           # auto → emoji on gui, unicode on tui. Or: unicode | ascii | emoji
    views: emoji
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
[6] Composition      → composition.yaml (plan + grounding) + draft.md (render)
[7] ATS & consistency → ats-check.yaml + audit.md; may loop back to [6] or [5]
[8] Export           → final file(s) in export/  (reads draft.md + identity + export-style only)
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
| `core` | high priority + strong evidence |
| `use` | high priority + moderate evidence |
| `covered_indirectly` | met via a broader evidence row |
| `mention` | low priority, evidenced (skills line only) |
| `gap` | required, not evidenced |
| `ask_user` | weak or stale evidence — probe before deciding |

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

Invocation grammar and command set are **pending** (see §17.9). CLI design is deferred to Cluster 3.

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
7. Copy `profile/export-style.yaml` from `assets/export-style.template.yaml`.
8. Print "what's empty and when you'll be prompted" report.

**Non-blocking.** Missing voice → prompted at composition. Missing norms → prompted at scoring.

### 17. Pending items (remaining work)

#### 17.1 UI/UX — ✅ RESOLVED (§19.5)
#### 17.2 Composition stage (priority 1) — ✅ RESOLVED (§19.6)
#### 17.3 Export (priority 1) — ✅ RESOLVED (§19.5.2 mechanism + §19.6 details)
#### 17.4 ATS & consistency check (priority 2) — ✅ RESOLVED (§19.7)
#### 17.5 Voice elicitation (priority 2) — ✅ RESOLVED (§19.7)
#### 17.6 Skill taxonomy (priority 2) — ✅ RESOLVED (§19.7; location Q4 / §19.5.1)
#### 17.7 Keyword extraction details (priority 2) — ✅ RESOLVED (§19.7)
#### 17.8 Evidence strength & recency rubric (priority 2) — ✅ RESOLVED (§19.7)
#### 17.9 CLI / invocation grammar (priority 2) — ✅ RESOLVED (§19.7)
#### 17.10 View regeneration script (priority 2) — ✅ RESOLVED (§19.7)
#### 17.11 Checkpoint trigger thresholds (priority 3) — ✅ RESOLVED (§19.7)
#### 17.12 Privacy & security (priority 3) — ✅ RESOLVED (§19.7)
#### 17.13 Version control (priority 3) — ✅ RESOLVED (§19.7)
#### 17.14 Multi-language (priority 3) — ✅ RESOLVED (§19.7)
#### 17.15 Testing (priority 3) — ✅ RESOLVED (§19.7)
#### 17.16 Open questions — ✅ ALL RESOLVED (§19.5)

### 18. Working method (original — superseded by §20)

### 19. Change log

- **v0.1** — first consolidation.
- **v0.1b** — added §0, §20, §21, §22. Spec §1–§19 unchanged.
- **v0.2** — session decisions recorded (§19.5); §20 rewritten to resume at Cluster 2; §21 inventory updated. §1–§19 unchanged.
- **v0.3** — Cluster 2 closed (§19.6); §20 rewritten to resume at Cluster 3; composition.yaml added to tree + inventory.
- **v0.4** — Cluster 3 closed (§19.7); all §17 pending resolved; §20 rewritten to Architecture File; inventory + tree updated.

---

### 19.5 Session decision record (v0.2)

**Do not re-open any of this.** If an inconsistency is found, flag it once with evidence and proceed.

#### 19.5.1 Open questions — resolved

| # | Question | Decision |
|---|---|---|
| Q1 | Skill packaging | **Two independent skills**: `evidence-bank/`, `cv-creation/` |
| Q2 | Norms | **Data-driven** from `profile/norms/`; skill reads files |
| Q3 | Voice | **Composition stage inside `cv-creation/`**; no third skill |
| Q4 | Taxonomy location | **`profile/skills.yaml`**, per-user, editable |
| Q5 | Tracker surface | **Chat summary + generated `views/tracker.md`** (no terminal renderer) |
| Q6 | Export target | **6b** — markdown-first; PDF/DOCX derived; mechanism in §19.5.2 |
| Q7 | ATS check | **Local deterministic ruleset**; regime rules data at `profile/norms/ats/<regime>.yaml`; baseline shipped in `references/ats-baseline-rules.md`; enrichable from the user's compiled ATS report without code changes |

#### 19.5.2 Export mechanism (Q6 detail)

**Canonical stays `draft.md`.** Export is a pure derivation; nothing in the pipeline reads `export/`.

Pipeline at stage [8]:

```
draft.md + identity.yaml + profile/export-style.yaml
        │
        ▼  parse (stdlib regex → section model)
   export_resume.py ──► export/resume.md
                    ├─► export/resume.html    (single-file, inline print CSS, A4, single column)
                    ├─► export/resume.docx    (python-docx, guarded import)
                    └─► export/resume.pdf     (weasyprint, guarded import; skipped if unavailable)
                        export/export_manifest.yaml   (sha256 of draft + style + tool versions)
```

- **Stdlib only** → `md` + `html`. PDF via browser print (zero install, full fidelity).
- **`python-docx`** → adds `docx`. Guarded import; warn + skip if absent; non-zero exit only if a *requested* format failed.
- **`weasyprint`** → optional headless PDF. Same guard. Never required.
- `export_resume.py --check-env` reports available formats before committing.

**Why no binary template:** §22.1 forbids binary blobs in the Architecture File. DOCX is generated programmatically from a declarative style file (`assets/export-style.template.yaml` → `profile/export-style.yaml`). Satisfies §22.8 — every knob is a template, none hardcoded in `SKILL.md`.

**ATS-safe layout is enforced by the style file:** single column, no tables, no text boxes, no content-bearing headers/footers, standard fonts, real list styles. `validate_application.py` rejects a style file that sets a violating flag.

#### 19.5.3 UI/UX design (Q5 + chat-host correction)

**Surfaces:**

| Surface | Role | Lifetime |
|---|---|---|
| **Chat** | Live state: one-line tracker + exactly one active primitive per turn | Ephemeral, re-rendered |
| **`views/tracker.md`** | Durable full tracker | Generated, read-only, hash-guarded |
| **`meta.yaml`** | Truth both surfaces derive from | Canonical |

Chat never renders the full tracker. `views/` never renders a *pending decision*.

**Chat host (critical correction from v0.1b):** Cursor and other GUI agents render markdown — proportional fonts, no column alignment, emoji fine. TUI agents (Claude Code, raw CLI) need monospace. **Two renderings per turn, selected by `ui.chat_host` (default `gui`).** Same data.

**Glyph modes (per surface, one code path):**

```yaml
ui:
  chat_host: gui
  tracker_fence: true
  glyphs:
    chat:  auto      # auto → emoji on gui, unicode on tui
    views: emoji
```

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

**Guardrail:** emoji must be single-codepoint where possible; `⚠️` (VS16) is the one exception and never appears in an aligned tracker line (only in table cells and callouts). `ascii` is the accessibility fallback and overrides both hosts.

**Primitive envelope — identical structure, two renderings.**

`gui` (Cursor, markdown-native — no box-drawing, no `▸` bullets, real headings and lists):

```markdown
**▸ Stage · item-id · verb**
**Field:** value
*One question.*
1. Option A
2. Option B
3. Other: …
*checkpoint ⟨ts⟩*
```

`tui` (monospace, aligned):

```
▸ stage · item-id · verb
  ⟨body ≤12 lines, aligned⟩
  [1] Option A  [2] Option B  [other: …]
──────────────────────────────────────────── checkpoint ⟨ts⟩
```

**The eight turn types** (human label = `Turn N: <Type>`; machine id `TN` secondary. T3 and T6 body/decisions are specified **verbatim-identically** in both SKILL.md files — the cross-skill contract, §22.6):

| # | Human label | Type | Owner | Body | Decisions |
|---|---|---|---|---|---|
| T1 | Turn 1: Experience validation | Experience validation | evidence-bank | `fact`, source span, de-styled fields, linked skills | confirm / amend / waive / mark ambiguous |
| T2 | Turn 2: Keyword validation | Keyword validation | cv-creation | keyword → normalized → `sk_*`, occurrence, placement | approve / remap / drop / add |
| T3 | Turn 3: Gap probe | Gap probe | **both (verbatim)** | requirement, missing `sk_*`, one probe question from bank | has evidence / no evidence / waive |
| T4 | Turn 4: Differentiator confirmation | Differentiator confirmation | cv-creation | text, source, confidence, URL | confirm / reject / route-to-bank |
| T5 | Turn 5: Norms tie-breaker | Norms tie-breaker | cv-creation | conflict, current values, three save options narrow→wide | once / scoped rule / wider rule |
| T6 | Turn 6: Gate summary | Gate summary | **both (verbatim)** | stage rollup, action counts **with inline definitions**, buffered-flag count | approve / revise / resolve / accept |
| T7 | Turn 7: Draft review (G4) | Draft review (G4) | cv-creation | draft, section plan, bullet→`ev_*` table, **buffered flags batch** | approve / revise / resolve-flag |
| T8 | Turn 8: ATS report (G5) | ATS report (G5) | cv-creation | coverage table, warnings, backward-edge proposals | approve / accept-edge / export / override |

**Action definitions (canonical wording — both T6 and T7 pull from here; §22.8):**

| Action | Meaning |
|---|---|
| `core` | high priority + strong evidence |
| `use` | high priority + moderate evidence |
| `covered_indirectly` | met via a broader evidence row |
| `mention` | low priority, evidenced (skills line only) |
| `gap` | required, not evidenced |
| `ask_user` | weak or stale evidence — probe before deciding |

**Update cadence.** Tracker line re-renders **only** on: stage transition, gate open/close, flag-count change, revision-count change, or explicit `status`. Not every turn. Floor: once per `checkpointing.turn_floor` turns (piggybacks the checkpoint write). `views/tracker.md` regenerates on **every** checkpoint (§13). **Double-render guard:** one event firing two triggers renders once, in the stage-transition form (supersedes the gate form).

**HMI principles:**
1. **Attention** — one decision per turn; active primitive is last in the turn.
2. **Consistency** — one envelope; same glyphs, same decision bracket order, same footer.
3. **Signal/noise** — tracker collapses to one line when idle; detail opt-in.
4. **Progressive disclosure** — one-line tracker → per-stage items → full `views/tracker.md`.
5. **Plain labels** — never show bare `T1`…`T8` (or bare gate codes) to the human. Required form: `Turn N: <plain name>` (e.g. `Turn 1: Experience validation`). Optional builder cue: `(T1)` only after the plain label. (Locked 2026-11-18; also `COMMUNICATION_CONTRACT.md`.)
6. **Stage progress** — when a stage or queue has a known total, every active turn shows `current of total` in the header or question line (e.g. `3 of 14`). (Locked 2026-11-18.)

**Per-stage item view** (chat, on `status`/`show ⟨stage⟩`, or when ≥3 items `awaiting_hitl`):

```
▸ stage 5 matching — awaiting you (2 of 14)
  ◆ r_4   Airflow depth       gap → probe queued
  ◆ d_002 cost-optimization   confirm / reject
  ✓ r_1   Python pipelines    core (ev_001, strong)
```

**Onboarding flow** (six steps, non-blocking, ends with empty-and-when report): confirm config (incl. `ui.chat_host`) → `identity.yaml` → offer evidence-bank now/defer → copy `voice.md` template → note norms lazy creation → print empty-and-when report + tracker at 0/8.

**Error primitive** (same envelope, header verb `error`):

```markdown
**▸ Bootstrap · career.config.yaml · missing**
**Expected:** `career/career.config.yaml`. **Found:** none.
**Recovery:** 1. Run onboarding · 2. Point to existing · 3. Abort
```

Rules: always name path and attempt; ≥2 recovery options; parse failures quote line numbers; `views/` hash mismatch **warns and regenerates**, never blocks; errors abort the stage loop but **do not** transition state — resume is clean.

**Accessibility:** ASCII glyph mode in scope (both hosts). Screen-reader optimization out of scope (documented, not relitigated).

**Approved `views/tracker.md` shape** (emoji mode, Obsidian-ready):

```markdown
<!-- GENERATED from meta.yaml + matching.yaml + scores.yaml. Do not edit. sha256: … -->
# Acme · Data Engineer — CV application

> [!info] acme-dataeng-2026-11-20
> JD: https://… · created 2026-11-20 · updated 2026-11-21T09:22Z

> [!todo] Waiting on you
> 🔔 **r_4** Airflow depth — gap probe answered, weak evidence
> 🔔 **d_002** Multi-cloud migrations — differentiator, confirm or reject

`████████████████░░░░` **79%** · items 11/14 · stage 5/8 · flags 1 · revisions r_3×2

## Stages
| # | Stage | Status | Items | Gate |
|---|---|---|---|---|
| 1 | JD intake | ✅ done | 3/3 | — |
| 5 | Matching | 🟡 in progress | 11/14 | G3 🔔 |
| 6 | Composition | ⬜ not started | 0/6 | G4 |

## Stage 5 — Matching
| State | Item | Skill / text | Action | Evidence |
|---|---|---|---|---|
| ✅ | r_1 | Python pipelines | core | ev_001 · strong |
| 🔔 | r_4 | Airflow depth | gap → probe | — |
| 🛑 | r_11 | Streaming (Kafka) | gap | — |

## Flags
| Flag | From | Reason | State |
|---|---|---|---|
| ⚠️ f_003 | scoring | "fast-paced" extracted as modifier; excluded | open |

## Differentiators
| ID | Text | Source | Conf | State |
|---|---|---|---|---|
| d_001 | Hands-on cost optimization | industry | 3 | ✅ confirmed |
| d_002 | Multi-cloud migrations | jd | 4 | 🟡 unconfirmed |

## Recent checkpoints
| When | Slug | Note | |
|---|---|---|---|
| 09:22 | after-matching | G3 open | |
| 08:41 | pre-scoring | before lossy LLM call | 📌 pinned |
```

**`ui-turn-types.md` owns:** envelope (both hosts), glyph table, T2/T4–T8 worked examples (two per type — gui + tui), cadence, HMI catalogue, action definitions table, a11y decision, error primitive.

**`evidence-bank/references/probe-ui.md` owns:** envelope + glyph table (verbatim-identical block), T1 and T3 worked examples, probe-turn cadence.

#### 19.5.4 Artifacts implied by this session's decisions

Added to the §21.3 inventory (v0.2):

- `cv-creation/references/ui-turn-types.md`
- `evidence-bank/references/probe-ui.md`
- `cv-creation/references/export-pipeline.md`
- `cv-creation/references/ats-baseline-rules.md`
- `cv-creation/references/ats-check.md`
- `cv-creation/assets/export-style.template.yaml`
- `cv-creation/assets/ats-rules.template.yaml`
- `cv-creation/scripts/export_resume.py`

Runtime-created (not in skill tree): `profile/export-style.yaml`, `profile/norms/ats/*.yaml`, `applications/<app>/export/`.

Further inventory from Cluster 2: see §19.6.11.

#### 19.6 Cluster 2 decision record — Composition (§17.2) + Export details (§17.3)

**Do not re-open any of this.** If an inconsistency is found, flag it once with evidence and proceed.

##### 19.6.1 Source of truth (SoT option A)

`composition.yaml` owns the section plan, grounding, buffered flags, and **planned bullet text**. `draft.md` is always **re-rendered** from `composition.yaml` (plus `identity.yaml` for the header). They are revised together: any change to composition triggers a draft re-render before the next gate or export.

- Export (§19.5.2) still reads **`draft.md` + `identity.yaml` + `export-style.yaml` only** — never `composition.yaml`.
- Consistency check (Cluster 3 / §17.4) asserts `draft.md ≡ render(composition.yaml)`.
- This keeps §3's split (YAML = structure, MD = narrative surface) without frontmatter inside `draft.md`, and without two competing prose editors.

##### 19.6.2 Artifacts at stage [6]

| File | Role | Canonical? |
|---|---|---|
| `composition.yaml` | Section plan, bullets (incl. text), skills_line, grounding, buffered flags | Yes — structure + planned text |
| `draft.md` | Rendered narrative (header + sections + bullets + skills line) | Yes — narrative surface; derived from composition |

Copied on **application creation** (stage [1] / app init — not career bootstrap) from `cv-creation/assets/composition.template.yaml`.

##### 19.6.3 `composition.yaml` shape

```yaml
section_plan:
  - {id: header,     order: 1, source: identity}
  - {id: summary,    order: 2, bullets: [b_001]}
  - {id: skills,     order: 3, source: matching}   # core → use → mention; grouped by taxonomy parent
  - {id: experience, order: 4, experiences: [exp_acme_de, exp_prev]}
  - {id: education,  order: 5, source: identity}
bullets:
  - id: b_001
    section: summary
    text: "Senior data engineer, 6y, Python/Airflow on AWS; cut billing ETL runtime 40%."
    ev_ids: [ev_001, ev_003]
    skill_ids: [sk_python, sk_airflow, sk_data_pipelines]
    voice: {verb: cut, tense: past, len_words: 18}
    differentiator_refs: [d_001]    # ordering/emphasis only
    user_pinned: false
    flags: []
  - id: b_002
    section: experience
    experience_id: exp_acme_de
    text: "Rebuilt nightly billing ETL (Python, Airflow, S3); −40% runtime, ~2M rows/night."
    ev_ids: [ev_001]
    skill_ids: [sk_python, sk_airflow]
    voice: {verb: rebuilt, tense: past, len_words: 16}
    differentiator_refs: []
    user_pinned: false
    flags: []
skills_line:
  - {group: Languages, items: [Python, SQL]}
  - {group: Tools,     items: [Airflow, AWS Lambda, S3]}
  - {group: Practices, items: [Data pipelines, Cost optimization]}
grounding:
  uncovered: []                              # MUST be empty to pass G4
  unconfirmed_differentiators_used: [d_002]
  cited_ev_ids: [ev_001, ev_003]
buffered_flags: []                           # populated only when grounding fails
```

##### 19.6.4 Section plan generation

Inputs: `matching.yaml` action distribution, `scores.yaml`, `career.config.defaults.seniority`, active norms file.

| Section | Inclusion |
|---|---|
| Header | Always; from `identity.yaml` |
| Summary | If ≥3 `core`/`use` skills **or** ≥2 confirmed differentiators; 2–3 bullets, each ≥1 `ev_*` |
| Skills | If any `core`/`use`/`mention`. Grouped by `skills.yaml` `parent_id`. Order within groups: core → use → mention. ATS forms preferred. **`covered_indirectly` is not on the skills line** (coverage via experience bullets) |
| Experience | Always. Default reverse-chronological; norms may override to relevance-first |
| Education | Per norms; omit if industry does not require and not evidenced |
| Projects / Certifications | Only if evidenced and norms-appropriate; never emit empty sections |

Section order, labels, inclusion: active norms file; global defaults in `career.config.yaml`. Precedence §11. Plan is **proposed** and HITL-gated at G4 (reorder / drop / relabel).

##### 19.6.5 Bullet ordering

Within **Experience**: (1) max `priority_norm` of linked skills desc; (2) differentiator boost = confidence × 0.5 for bullets whose `differentiator_refs` hit a **confirmed** differentiator (reorder only, never add bullets); (3) date desc within the same experience; (4) `user_pinned: true` sticky at G4.

Within **Summary**: summed `priority_norm` of cited evidence skills, then differentiator hits.

**Voice affects phrasing only — never ordering.** (§17.2's "ordering … + voice" pending line is resolved as: matching + differentiators order; voice phrases.)

##### 19.6.6 Evidence-grounding contract

Structural (machine) checks at G4:

1. Every Summary/Experience bullet has `ev_ids.length ≥ 1`.
2. Every `ev_id` exists in `evidence.yaml`.
3. Each cited evidence has `status: fact`, or `waived` with a recorded reason.
4. Every bullet has explicit `skill_ids[]`; those ids ⊆ union of skills reachable from cited `ev_*` via `evidence_skills` (allowed strengths per matching action — Cluster 3 may tighten).
5. Education/Certification lines: exempt if sourced from `identity.yaml`; if from evidence, same `ev_*` rules.
6. Skills-line item grounded iff its skill is in `core | use | mention`.
7. `grounding.uncovered` MUST be empty to pass G4.

Semantic fidelity (does wording faithfully restate the fact?) is a **human check at G4**, shown as the bullet → `ev_*` table (§15 G4 / T7).

If a planned bullet cannot be grounded: **omit from the draft render**, raise a `buffered_flags` entry (§19.6.9). Do not write ungrounded prose into `draft.md`.

##### 19.6.7 Voice application

`profile/voice.md` supplies: target sentence length, verb preferences, first-person stance, technical density, bullet structure, formatting habits.

- Applied only when generating `bullets[*].text` from evidence fields.
- Never changes facts: numbers, tools, dates, scope, org names come from evidence (faithful paraphrase OK; entities and metrics must match).
- Conflict with ATS rules: **ATS wins for `core` skills**; voice wins elsewhere. Significant conflicts → G4 note.
- Missing `voice.md`: prompt elicitation at [6] entry (§16); non-blocking.

##### 19.6.8 Unconfirmed differentiators

May: reorder bullets; influence which summary bullets are selected; be listed in `grounding.unconfirmed_differentiators_used`.

May **not**: introduce new claims, add skills to the skills line, change metrics, add or extend experience (§10).

**Enforcement:** structural checks ensure bullets only cite existing `ev_*` (same as §19.6.6). Detecting "new claim introduced by a differentiator" is **not** fully structural — it is the human semantic check at G4. Do not claim machine enforcement beyond the cite-existing-`ev_*` rule.

**G4 disposition (required before gate pass):** every id in `unconfirmed_differentiators_used` must receive confirm / reject / route-to-bank / **explicit defer**. Defer records a warning and allows approve; confirm → evidence-bank as `source: user`; reject → mark rejected, re-order without it, re-render draft.

Differentiator UI at G4 **reuses the T4 envelope** embedded in T7 (not a new turn type).

##### 19.6.9 Buffering for [6] → [5]

```yaml
buffered_flags:
  - {id: bf_001, intended_section: experience, intended_skill: sk_kafka,
     reason: "no ev_* with Kafka reachable; nearest ev_004 is moderate/indirect"}
```

Composition continues; no mid-draft HITL (§15). At G4, all `buffered_flags` shown as one batch. Per flag (T7 **`resolve-flag` sub-decisions**):

| Sub-decision | Effect |
|---|---|
| drop | Bullet removed; flag cleared |
| rephrase | User supplies groundable claim; re-check in place; no stage transition |
| route-to-bank | Fires §5 edge `[6]→[5]`; probe; on return [6] re-enters for affected bullets only |
| waive | Flag cleared; reason recorded in `composition.yaml` |

Only **route-to-bank** triggers the backward edge. Level 2 exit still requires no open flags (§8).

##### 19.6.10 Export details (§17.3)

**Parse** (`export_resume.py`, stdlib regex): strip optional frontmatter (defensive); split on `^##\s+`; within section `^###\s+` subsections, `^[-*]\s+` bullets, blank-line prose paragraphs; lines before first `##` = header block.

Section model:

```python
{
  "header": {"name": str, "contact_lines": [str]},
  "sections": [
    {"heading": str,
     "blocks": [
        {"type": "paragraph", "text": str},
        {"type": "bullets",   "items": [str]},
        {"type": "subsection","heading": str,
         "meta": {"org": str, "dates": str}, "bullets": [str]},
     ]},
  ]
}
```

- Header cross-check: `identity.yaml` wins on mismatch; warning emitted. Contact lines always from `identity.yaml`.
- Zero `## ` sections → parse error, exit 2.
- All renderers (md, html, docx, pdf) consume the same model.

**`export-style.template.yaml`:** page/fonts/layout/heading/bullets/skills_section/ats/colors. MUST flags (validated by `validate_application.py`, exit 3): `single_column: true`, `tables: false`, `text_boxes: false`, `content_headers_footers: false`, `real_list_styles: true`.

**`export_manifest.yaml`:** `generated_at`, `application_id`, input paths+sha256, tool versions, requested/produced/skipped formats, output paths+sha256, warnings. Input hash mismatch → warning, not fatal.

**`--check-env`:** table `format | available | version | install hint`. Always: md, html. docx iff `python-docx`; pdf iff `weasyprint`. Exit 0 if every **requested** format available; else 1. Writes nothing.

**Guarded imports + exits:**

| Condition | Exit |
|---|---|
| Default run; optional dep missing | Produce available; record `skipped_formats`; warn; **0** |
| `--formats` requests missing dep | Error + install hint; **1** |
| No `## ` sections | **2** |
| Style MUST violation | **3** |
| `identity.yaml` missing | **4** |
| Export dir not writable | **5** |
| Style file missing | Fall back to template defaults; warn; **0** |

Browser print of `resume.html` remains a **user** zero-install PDF path (§19.5.2). `export_resume.py`'s `pdf` format is weasyprint only — not a browser automation path.

Format notes: md = deterministic re-emission; html = single-file inline print CSS, semantic headings/lists, no tables; docx = named styles, no text boxes/tables; pdf = weasyprint(HTML).

##### 19.6.11 Inventory delta (document in Architecture File §A)

| Added | Type | Why |
|---|---|---|
| `applications/⟨app⟩/composition.yaml` | runtime-created | Companion to `draft.md` (§19.6.1–19.6.9) |
| `cv-creation/assets/composition.template.yaml` | skill-tree asset | Scaffold copied on application creation |

Also amend in §A (docs only, not new files): §4.1 tree line; §5 stage [6] outputs. No removals. No purpose change to existing inventory items.

#### 19.7 Cluster 3 decision record — §17.4–§17.15

**Do not re-open any of this.** Reviewed one lock at a time. If an inconsistency is found, flag it once with evidence and proceed.

##### 19.7.1 ATS & consistency (§17.4)

**Artifacts:** `ats-check.yaml` (machine) + `audit.md` (narrative) — pair, like composition/draft.

**Coverage universe:** `core` + `use` + `gap` only (`mention` / `covered_indirectly` reported, not in denominator).

```
covered(skill) = in_draft ∧ (action ≠ gap) ∧ strength_ok
coverage_pct   = 100 × |covered| / |universe|
```

Empty universe → `coverage_pct = 100` + warning `no_scored_skills`.

**Thresholds** (config / regime-overridable): `coverage_pass: 80`, `coverage_warn: 65`. Any `must_have` gap **blocks** G5 pass unless **override** or fix via edge.

**In-draft (norms-aware):**
- Skills section included → present if bullet `skill_ids` **or** skills-line `ats_forms` match.
- Skills section omitted → bullet `skill_ids` only.

**Override:** allowed below pass / with must-have gaps; reason required in `ats-check.yaml`; gaps stay visible.

**C1:** `draft.md ≢ render(composition.yaml)` → **block** G5 until re-render or accept `[7]→[6]`.

**Edge chooser:** evidence missing / must-have gap → propose `[7]→[5]`; else (phrasing, skills line, coverage, C1) → `[7]→[6]`.

**Regime file** `profile/norms/ats/<regime>.yaml`: thresholds, `must_have_gap_blocks`, `required_sections`, banned layout mirrors, keyword_rules, `enrichment_notes` (data-only; Q7). Baseline from `ats-rules.template.yaml` + `ats-baseline-rules.md`.

T8: approve / accept-edge / export / override.

##### 19.7.2 Voice elicitation (§17.5)

At [6] if voice incomplete: offer elicitation (length, verbs, stance, density, bullet shape, formatting). **Skip allowed** — template defaults + G4 note. Non-blocking (§16). Never writes evidence bank.

##### 19.7.3 Taxonomy mechanics (§17.6)

Location: `profile/skills.yaml` (Q4). Lookup via canonical / aliases / ats_forms. **New `sk_*` from JD: HITL approve before write.** Merge → survivor id + loser as alias; modifiers excluded from scoring; parents form a DAG (validator rejects cycles). Soft-delete via `deprecated: true`.

##### 19.7.4 Keywords (§17.7)

Zones: title / summary / body / boilerplate. Normalize via taxonomy; miss → T2 add/remap/drop. Boilerplate-only hits: `noise_candidate`, `ats_weight` capped at **1**.

`ats_weight` (tiebreaker only, §6): `min(5, occurrences)` +2 title +1 summary +1 exact ats_form; clamp 1..5.

##### 19.7.5 Strength & recency (§17.8)

Floors: **core → strong**; **use → ≥ moderate**. **Stale cannot be core** (downgrade to `use` or `ask_user`).

Recency vs application `created`: current ≤18mo; `<3y` ≤36mo; else stale (undated → stale + warn).

Composition grounding tighten: `core` bullets need ≥1 cited `evidence_skills` link with `strong`; `use` ≥ `moderate`.

##### 19.7.6 Invocation (§17.9)

Chat verbs (`run`/`continue`, `status`, `show`, `probe`, `gate`, `export`, `check-env`, `regen-views`, `override-ats`) documented in **both** `SKILL.md` Invocation sections **and** `references/invocation.md`. Scripts keep `--help`.

##### 19.7.7 Views (§17.10)

Regenerate requirements / keywords / scoring / matching / tracker + `_manifest.yaml` on every checkpoint and on `regen-views`. **No** `views/composition.md`. Hash mismatch → warn + regen, never block. `verify_views.py`: 0 match, 1 stale, 2 banner missing.

##### 19.7.8 Checkpoint thresholds (§17.11)

Keep defaults: `turn_floor: 10`, `flag_threshold: 5`, `retention_k: 20`. Also always: state transition; before lossy ops; explicit checkpoint/pin. Auto-pin prior checkpoint when a decision is later revised (§9).

##### 19.7.9 Privacy (§17.12)

No telemetry. Company-web differentiator fetch: **explicit user OK per URL**; store URL on row. No secrets in YAML. Local scripts only.

##### 19.7.10 Version control (§17.13)

Bootstrap installs `gitignore.template`: ignore `export/*.docx`, `export/*.pdf`, temp state. **Commit `profile/evidence.yaml` by default**; document that sensitive users may gitignore it. Commit apps YAML/MD, views, audit, ats-check, composition, draft, export md/html/manifest.

##### 19.7.11 Multi-language (§17.14)

One language per application (`meta.language` ← config default, overridable at [1]). No auto-translate. Mixed-language JD → extract + flag. Norms/ATS regime selection uses lang key.

##### 19.7.12 Testing (§17.15)

Deterministic tooling CI only: `py_compile`, bootstrap smoke, `assets/fixtures/mini-app/` (render round-trip, export parse, style MUST, views verify, taxonomy cycle). **No LLM-in-CI.**

##### 19.7.13 Inventory delta (Architecture File §A)

| Added | Type |
|---|---|
| `applications/⟨app⟩/ats-check.yaml` | runtime |
| `cv-creation/references/taxonomy-mechanics.md` | reference |
| `cv-creation/references/invocation.md` | reference |
| `cv-creation/assets/gitignore.template` | asset |
| `cv-creation/assets/fixtures/mini-app/` | asset |

Also amend in §A: tree lines for `ats-check.yaml`; stage [7] outputs. No removals.

---

## Part C — Session operations (§20–§22)

### 20. Working method for the resumed session

Follow strictly. Stop at every 🔴.

**20.1 Onboarding (after user types `read`).**
- Confirm you have read all of §0–§23.
- Restate §20 in one sentence.
- State: "Clusters 1–3 are complete (§19.5–§19.7). Next: produce the Architecture File (§21), then self-check (§22)."
- Ask the user to say `go`.
- 🔴 **Stop.**

**20.2 Acknowledge the decision records.**
- Do **not** re-open Q1–Q7 or Clusters 1–3 (§19.5–§19.7).
- If you find an inconsistency, flag it once with evidence and proceed; do not litigate.
- 🔴 **Stop after one-paragraph acknowledgement.**

**20.3–20.4** Clusters 2–3 — ✅ COMPLETE. Skip.

**20.5 Produce the Architecture File (§21).**
- Long output. Do not truncate. Do not leave TODOs.
- Include §A notes for inventory deltas §19.5.4, §19.6.11, §19.7.13 + tree/stage-output amendments.
- 🔴 **Stop when finished.**

**20.6 Self-check against §22.**
- Walk through each acceptance criterion.
- Fix any that fail before declaring done.
- 🔴 **Stop. Deliver.**

**Behavioral rules:**
- Do not reopen §1–§19 or §19.5–§19.7. If you must flag one, do it once with evidence and proceed.
- Do not compress the deliverable. If it is long, say so and continue.
- Do not propose alternate architecture at §20.5.
- Do not ask the user to "fill in later" items. If a gap exists, resolve it now.

### 21. Deliverable — the Architecture File

**21.1 Target of the build.**

Cursor will produce **one folder tree** to paste into `career/.cursor/skills/`. It must contain both skills, complete, and every asset the bootstrap needs. It must NOT produce the `career/` data tree — that is created by the skills on first run.

**21.2 The Architecture File itself.**

Produce **one markdown file**, self-contained, structured as:

```
# CV System — Architecture File (v1.0)
## A. Build target
   - The exact folder tree Cursor must produce
   - One-sentence purpose per file
   - A "changes from §21.3 baseline" note listing v0.2 (§19.5.4), v0.3 (§19.6.11), and v0.4 (§19.7.13) additions
## B. File contents
   - For every file: full path as heading, then a fenced code block with the complete content
   - Order: SKILL.md files first, then references/, then assets/, then scripts/
   - No placeholders, no "see §X", no TODOs
## C. Build order
   - Numbered steps for Cursor
## D. Verification checklist
   - (a) syntax check for each Python script
   - (b) tree diff Cursor can run to confirm all files were created
   - (c) smoke test: bootstrap against empty dir, inspect result
## E. Post-build handoff
   - What the user does next
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
      probe-ui.md                              ← added v0.2
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
      ui-turn-types.md                         ← added v0.2
      export-pipeline.md                       ← added v0.2
      ats-baseline-rules.md                    ← added v0.2
      ats-check.md                             ← added v0.2
      taxonomy-mechanics.md                    ← added v0.4 (§19.7)
      invocation.md                            ← added v0.4 (§19.7)
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
      export-style.template.yaml               ← added v0.2
      ats-rules.template.yaml                  ← added v0.2
      composition.template.yaml                ← added v0.3 (§19.6)
      gitignore.template                       ← added v0.4 (§19.7)
      fixtures/mini-app/                       ← added v0.4 (§19.7)
    scripts/
      bootstrap_career.py
      regenerate_views.py
      verify_views.py
      validate_application.py
      export_resume.py                         ← added v0.2
```

Runtime-created (not in skill tree; document in Architecture §A): `applications/⟨app⟩/composition.yaml` (§19.6), `applications/⟨app⟩/ats-check.yaml` (§19.7).

Inventory locked through Cluster 3. Document all deltas in §A of the architecture file.

**21.4 Content rules for every file.**

- **SKILL.md** — full frontmatter (`name`, `description` per Agent Skills spec); body with steps, edge cases, explicit "when to load X" for every reference and asset. Under 500 lines.
- **references/** — detailed documentation, loaded on demand. Worked examples where the rule is non-obvious. `ui-turn-types.md` and `probe-ui.md` must show **both** gui and tui renderings per turn type.
- **assets/** — complete templates ready to copy.
- **scripts/** — complete, runnable. Docstring, imports, argument parsing, main block. No pseudo-code. `export_resume.py` must include `--check-env`.
- **Cross-file consistency** — every path mentioned in SKILL.md exists in the tree; every named asset exists.

**21.5 What NOT to include.**

- Design rationale.
- Open decisions (all resolved).
- Optional features not specified.
- Anything Cursor would have to invent.

### 22. Acceptance criteria

The session is done when the Architecture File satisfies all of:

1. **Completeness.** Every file in §21.3 has full content in §B. No TODOs, no "fill in later," no `# ...` abbreviations.
2. **Self-containment.** No references to §1–§19 or §19.5–§19.7. If a Cursor agent read only the architecture file, it can build the system.
3. **Path integrity.** Every path mentioned in any file exists in the inventory, or is explicitly created at runtime by bootstrap.
4. **Bootstrap works.** `assets/career.config.template.yaml` and the other templates are complete enough that `bootstrap_career.py` produces a working `career/` tree on first run, with only user-input prompts for identity fields.
5. **Both skills invocable.** Each `SKILL.md` description is triggerable (imperative, "Use when…", covers both full-run and single-item-probe cases).
6. **Cross-skill interface documented.** The T3 gap probe and T6 gate summary are specified **verbatim-identically** in both SKILL.md files, including the action definitions table.
7. **Verification.** §D contains: (a) syntax check for each Python script, (b) a tree diff, (c) a bootstrap smoke test against an empty directory.
8. **No silent drift.** Every file the user might change later is a template in `assets/` or a reference in `references/`, not hardcoded in `SKILL.md`. This includes `ui.glyphs`, `ui.chat_host`, `export-style.yaml`, and `ats-rules.yaml`.

When all eight pass, declare the deliverable complete and hand off.

---

## 23. Change log

- **v0.1** — first consolidation.
- **v0.1b** — added §0, §20, §21, §22.
- **v0.2** — Q1–Q7 resolved (§19.5.1). Export mechanism fixed (§19.5.2). UI/UX designed, including gui/tui split, glyph modes, action definitions (§19.5.3). Eight artifacts added to inventory (§19.5.4, §21.3). §20 rewritten to resume at Cluster 2. §1–§19 unchanged.
- **v0.3** — Cluster 2 closed (§19.6): SoT option A (`composition.yaml` owns plan+text; `draft.md` re-rendered); grounding/`skill_ids`; G4 dispositions; export parse/style/manifest/`--check-env`/exits. §17.2–§17.3 marked resolved. Tree + §21.3 inventory updated (`composition.template.yaml`). §20 rewritten to resume at Cluster 3.
- **v0.4** — Cluster 3 closed (§19.7): ATS coverage/universe/thresholds/in-draft/override/C1/edges; voice skip; taxonomy HITL; keyword boilerplate; strength/recency floors; invocation.md; no composition view; checkpoint 10/5/20; privacy per-URL fetch; commit evidence; one language/app; deterministic CI + fixture. §17.4–§17.15 resolved. §20 → Architecture File. Inventory updated.
- **v0.4.1** — HMI additive (2026-11-18): plain `Turn N: <name>` labels; stage `current of total`. Does not reopen Q1–Q7. Project `COMMUNICATION_CONTRACT.md`.
