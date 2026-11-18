# State machine

## Level 1 — item

not_started → in_progress → awaiting_hitl → approve → approved. Revise returns to in_progress (+ revision_count). Explicit reopen → awaiting_hitl.

## Level 2 — stage

extract items → loop item lifecycle → gate → else re-extract → stage done. Exit: no pending, gate passed, no open flags.

## Level 3 — global

Full run [1]→[8]; resume from checkpoint; single-item probe with no stage transition.
