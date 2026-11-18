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
