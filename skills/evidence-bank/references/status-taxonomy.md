# Evidence status taxonomy

| Status | Meaning | Exit |
|---|---|---|
| `unverified` | Ingested or proposed; not yet approved | May have empty `probe_history` while queued; append history before → `fact` |
| `ambiguous` | Conflicting or unclear | Non-empty `probe_history` required (validator hard-fail) |
| `fact` | Approved de-styled fact (after Turn 1 confirm) | Usable in CV grounding |
| `waived` | Explicitly not usable | Terminal; non-empty `probe_history` reason (validator hard-fail) |

## Transitions

- `unverified` / `ambiguous` → `fact` | `waived` | amend (often back to `unverified`)  
- Never silent promote to `fact`  
- Every `waive` appends a `probe_history` entry  
- Clean amend with clear source may skip a new probe **question**; still use Turn 1  

## Defense in depth

1. `validate_evidence.py` — structure / provenance / refs  
2. Turn 1 — human fact gate  
3. cv-creation matching floors  
4. Composition grounding (`ev_*` citations)  
