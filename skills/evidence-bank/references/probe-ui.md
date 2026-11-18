# Probe UI (evidence-bank)

Glyphs and envelope match cv-creation `ui-turn-types.md`. `ui.chat_host`: `gui` | `tui`. Glyph modes: unicode | ascii | emoji (chat `auto` → emoji on gui, unicode on tui).

**Human labeling:** never bare `T1` / `T3` / `T6` — use `Turn N: <plain name>`; show `current of total` when the queue/stage total is known. See `COMMUNICATION_CONTRACT.md`.

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
