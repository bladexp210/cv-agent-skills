# First-run briefing (evidence-bank)

Show **once** before the first **Turn 1: Experience validation** when required (below). Then start Turn 1. Do **not** repeat on every Turn 1.

## Script (say to the user — ~8 short lines)

1. We are building a **facts bank** from files you put in `inbox/` (resume, LinkedIn text, notes). Facts only — no CV voice yet.
2. This turn is **one fact**: choose **confirm**, **amend**, **waive**, or **mark ambiguous**.
3. **Skill ratings** appear so we link which skills this fact supports (strength + how recent). You can change them.
4. **k of n** (example: `10 of 16`) means item *k* in a queue of *n* facts.
5. **Journey:** Facts bank (now) → later: match a job → draft CV → export.
6. Files: drop sources in `inbox/`; saved facts live in `profile/`; progress lives in `_skill_state/`.
7. After the queue you may see an optional **Turn 6: Gate summary**. Later, cv-creation uses this bank for a job.
8. Say **help** or **onboarding** anytime to see this briefing again.

## When to show

Once per career project when **any** of:

- `_skill_state/LIVE.yaml` is missing, **or**
- the evidence bank is empty, **or**
- the user asks for help / onboarding

Skip if the shown-flag is already set (unless the user asks again).

## Flag (do not repeat every Turn 1)

After showing, set **one** of:

- `_skill_state/LIVE.yaml` → `onboarding_briefing_shown: true`, **or**
- `_skill_state/onboarding_briefing_shown: true` (sidecar if LIVE is not written yet)

Prefer the LIVE field when you write LIVE. Keep or restore the flag when recomputing LIVE so a resume does not re-brief.
