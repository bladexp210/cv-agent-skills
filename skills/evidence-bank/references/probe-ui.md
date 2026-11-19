# Probe UI (evidence-bank)

Glyphs and envelope match cv-creation `ui-turn-types.md`. `ui.chat_host`: `gui` | `tui`. Glyph modes: unicode | ascii | emoji (chat `auto` → emoji on gui, unicode on tui).

**Human labeling:** never bare `T0` / `T1` / `T3` / `T6` — use `Turn N: <plain name>`; show `current of total` when the queue/stage total is known. See `COMMUNICATION_CONTRACT.md`.

**Progress strip (when total known):** directly under the Turn header (gui and tui), show a monospace-friendly bar + counts, e.g. `Ingest  [##########------] 10/16`. Use `#`/`-` or unicode blocks (`█`/`░`); one cell per item or a fixed-width scale that still reads as current/total. Omit the strip only when total is unknown (Turn 0 G1 may omit until the queue size is approved).

**Journey (bank ingest):** one short line under the strip (or under the header when no strip):  
`Journey: Facts bank (now) → later: match a job → draft CV → export`

Turn 3 / Turn 6 **body fields and decision labels** are verbatim with cv-creation (see `SKILL.md`). **Turn 0: Ingest scope** is bank-only (not in cv-creation catalogue).

## Envelope

### gui

```markdown
**▸ Turn N: <plain name> · item-id · k of n**
`Ingest  [##########------] 10/16`
`Journey: Facts bank (now) → later: match a job → draft CV → export`
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
  Ingest  [##########------] 10/16
  Journey: Facts bank (now) → later: match a job → draft CV → export
  ⟨body ≤12 lines, aligned⟩
  [1] Option A  [2] Option B  [other: …]
──────────────────────────────────────────── checkpoint ⟨ts⟩
```

## Turn 0: Ingest scope — G1 (gui)

Hard-fail: do not write `queue.yaml` or start Turn 1 until this pass’s Turn 0 is decided. Never silent-curate.

```markdown
**▸ Turn 0: Ingest scope · pass-2**
`Journey: Facts bank (now) → later: match a job → draft CV → export`
**Surfaces:** master_resume_v7.pdf; LinkedIn paste 2026-11-18
**Proposed mode:** full
**In (roles · candidate counts):**
- exp_acme_de · 9
- exp_beta_ba · 7
**Deferred (reason):**
- exp_gamma_intern · early career; out of target roles for this pass
**Recommendation:** approve full — remaining destyled candidates from named surfaces.
*Approve this ingest scope?*
1. approve full
2. approve curated
3. revise
4. defer pass
*checkpoint 2026-11-19T10:00Z*
```

## Turn 0: Ingest scope — G1 (tui)

```
▸ Turn 0: Ingest scope · pass-2
  Journey: Facts bank (now) → later: match a job → draft CV → export
  Surfaces: master_resume_v7.pdf; LinkedIn paste 2026-11-18
  Proposed mode: full
  In: exp_acme_de · 9; exp_beta_ba · 7
  Deferred: exp_gamma_intern — early career; out of target roles for this pass
  Rec: approve full — remaining destyled candidates from named surfaces.
  [1] approve full  [2] approve curated  [3] revise  [4] defer pass
──────────────────────────────────────────── checkpoint 2026-11-19T10:00Z
```

## Turn 0: Ingest scope — G2 candidate short-list (gui)

Show G2 only after the operator chooses **`approve curated`** or **`revise`**. Require **`approve queue`** / **`revise queue`** before enqueue.

```markdown
**▸ Turn 0: Ingest scope · pass-2 · G2 short-list**
`Journey: Facts bank (now) → later: match a job → draft CV → export`
**Proposed queue (role · fact stub · source id):**
1. exp_acme_de · Rebuilt nightly billing ETL… · src_resume_p2_b3
2. exp_acme_de · Owned Airflow DAG SLAs… · src_resume_p2_b4
3. exp_beta_ba · Ran stakeholder workshops… · src_li_exp2_b1
*(…one line per proposed fact…)*
**Recommendation:** approve queue — curated set matches operator revise notes.
*Approve this queue for enqueue?*
1. approve queue
2. revise queue
*checkpoint 2026-11-19T10:05Z*
```

## Turn 1: Experience validation — worked example (gui)

```markdown
**▸ Turn 1: Experience validation · ev_001 · 1 of 3**
`Ingest  [#--] 1/3`
`Journey: Facts bank (now) → later: match a job → draft CV → export`
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
  Ingest  [#--] 1/3
  Journey: Facts bank (now) → later: match a job → draft CV → export
  Fact: Rebuilt nightly billing ETL with Python and Airflow on AWS; cut runtime 40%.
  Source: master_resume_v7.pdf, p.2, bullet 3
  Skills: sk_python (strong, current), sk_airflow (strong, current)
  [1] confirm  [2] amend  [3] waive  [4] mark ambiguous
──────────────────────────────────────────── checkpoint 2026-11-21T09:00Z
```

## Turn 1 after amend — skill delta (required)

When the user chooses **amend** (or edits the fact text), before persisting as `fact`:

1. Show the **revised fact** (destyled).
2. Re-propose `evidence_skills` for that item.
3. Compare to the **previous proposal** (or last persisted links if already saved) and show a **skill delta**:
   - **Added** — new `sk_*` (with strength, recency)
   - **Removed** — dropped `sk_*`
   - **Changed** — same `sk_*` but strength and/or recency changed (show old → new)
   - If nothing changed: say **Skills unchanged** explicitly
4. Ask them to confirm the revised fact **and** the skill set (same 1–4 options, or a short “confirm revised”).

Do not silent-update skills on amend. Do not skip the delta when only ratings change.

After any Turn 1 decision is persisted: validate, update queue cursor/item status, write `_skill_state/LIVE.yaml` + `STATUS.md`, and mirror memory if tools exist — see `continuity.md`.

### Amend follow-up example (gui)

```markdown
**▸ Turn 1: Experience validation · ev_006 · 6 of 16 (after amend)**
**Revised fact:** Improved adoption of updated documentation and requirements standards; worked with software engineers and implementation colleagues so the updates stuck and post-kickoff rework dropped.
**Source:** … + user amend …
**Skills (proposed):** sk_requirements_governance (strong, current), sk_change_adoption (moderate, current)

**Skill changes vs previous proposal:**
- Added: sk_change_adoption (moderate, current)
- Removed: sk_stakeholder_mgmt
- Changed: sk_requirements_governance strong → moderate
(or: Skills unchanged)

*Confirm revised fact and skill links?*
1. confirm
2. amend
3. waive
4. mark ambiguous
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

## Turn 6: Gate summary — bulk ingest Coverage (gui)

Shared body+decisions with cv-creation; bank ingest must show Coverage so `n/n` never means “whole warehouse done.”

```markdown
**▸ Turn 6: Gate summary · ingest · pass-2**
`Ingest  [################] 16/16`
`Journey: Facts bank (now) → later: match a job → draft CV → export`
**Stage:** bulk ingest · items 16/16 · awaiting 0
**Actions:** N/A (ingest — not matching)
**Buffered flags:** 0
**Coverage:**
- Included: exp_acme_de · 9; exp_beta_ba · 7 (16 facts confirmed)
- Deferred / left out: exp_gamma_intern · early career (not offered this pass)
- Source inventory: master_resume_v7.pdf + LinkedIn paste — 3 roles / ~24 destyled candidates; this pass covered 2 roles / 16 facts
1. approve
2. revise
3. resolve
4. accept
*checkpoint 2026-11-19T11:00Z*
```

## Turn 6: Gate summary — application stage (Coverage N/A)

When Turn 6 is an application stage gate (cv-creation), use:  
`**Coverage:** N/A (not bulk ingest)`
