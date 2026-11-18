---
schema_version: '0.3'
key: ui-plain-labels-and-progress
namespace: contracts
type: contract
version: 1
updated_at: '2026-11-18T18:29:23Z'
updated_by: agent:cursor
status: active
verified: false
stale_after: '2027-02-16'
tags:
- communication
- ui
- evidence-bank
- cv-creation
sources:
- COMMUNICATION_CONTRACT.md
- CV-SYSTEM-HANDOFF-v0.2.md
- USER_PROFILE.md
title: Plain turn labels and stage progress
description: 'Human-facing HITL must use Turn N: name and show current of total.'
---

Locked 2026-11-18 for Mohamed and CV-system skill users.

1. Plain labels: never bare T1..T8 (or bare gate codes) alone. Required form: `Turn N: <plain name>` e.g. `Turn 1: Experience validation`. Optional builder cue `(T1)` only after the plain label.
2. Stage progress: when a stage/queue/design list has a known total, every active turn shows `current of total` (e.g. `Q7 of 11`, `3 of 14`) in header or question line.

Pinned in: USER_PROFILE.md §3; application-skills/COMMUNICATION_CONTRACT.md; CV-SYSTEM-HANDOFF-v0.2.md §19.5.3 HMI 5–6; Architecture note + ui-turn-types.md + probe-ui.md examples.

Does not change T3/T6 verbatim body/decision contract text.
