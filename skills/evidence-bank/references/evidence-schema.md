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

On **amend**, re-propose links and show a skill delta (added / removed / strength or recency changed, or “Skills unchanged”) before persist — see `probe-ui.md`.
