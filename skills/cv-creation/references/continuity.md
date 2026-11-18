# Continuity (shared — keep identical in evidence-bank and cv-creation)

Progress across chat windows and agents is **files in the career project**, not chat history and not long-term memory.

## Ranked SoT

| Rank | Layer | Role |
| :--- | :--- | :--- |
| 1 | Domain files | Authoritative data (`profile/evidence.yaml`, `applications/<app>/*`, …) |
| 2 | `_skill_state/LIVE.yaml` | Live pointer: where we are now |
| 3 | Checkpoints / queue files | History and detail (`_skill_state/...`) |
| 4 | External memory (MCP, memory skills, …) | **Optional cache only** |

If memory ≠ disk, **repair memory from disk**. Never the reverse.

## Standing obligations (not user commands)

After every meaningful step (Turn decision persisted, gate closed, stage advanced, export done, ingest item advanced):

1. Update **domain files**.
2. Overwrite **`_skill_state/LIVE.yaml`** (schema below).
3. Overwrite **`_skill_state/STATUS.md`** (short human mirror of LIVE).
4. For evidence-bank ingest: update queue `cursor` and per-item status when applicable.
5. Run validators when the skill already requires them (e.g. `validate_evidence.py` after evidence persist).
6. **If** this agent has long-term memory tools (MCP checkpoint, memory skill, …): **mirror** LIVE into memory in the **same turn** (write-through).  
   **If** it has no memory tools: skip silently — disk is enough.

Do **not** ask the user to run `sync-memory`, `validate`, or “update status file.” Those are obligations.

## Resume / status / continue algorithm

1. Read `_skill_state/LIVE.yaml` if present.  
2. **Verify** against domain files (e.g. which evidence ids are already `fact`/`waived`; which app stage files exist).  
3. If LIVE is missing or conflicts with domain → **recompute** LIVE from domain + queue/checkpoints; write LIVE + STATUS.  
4. Tell the user plain progress (`current of total`, awaiting id, next action).  
5. Proceed only from that recomputed state.

Never resume from memory or another chat’s transcript alone.

## LIVE.yaml schema (`cv-skills-live/v1`)

Path: `_skill_state/LIVE.yaml`  
Active application (cv-creation): also keep `_skill_state/<app-id>/LIVE.yaml` in sync while that app is in focus; project LIVE points at the active app.

```yaml
schema: cv-skills-live/v1
updated_at: "2026-11-18T22:00:00Z"
skill: evidence-bank          # or cv-creation
mode: bulk_ingest             # e.g. bulk_ingest | single_probe | application
app_id: null                  # applications/<id> when cv-creation
progress:
  current: 10
  total: 16
  label: "Turn 1: Experience validation"
awaiting:
  id: ev_010
  kind: turn1_confirm         # short machine hint
pointers:
  evidence: profile/evidence.yaml
  queue: _skill_state/ingest/queue.yaml
  # app_dir: applications/acme-de-2026-01-01
next_action: "Ask Turn 1 for ev_010 (confirm/amend/waive/ambiguous)"
```

## STATUS.md

Path: `_skill_state/STATUS.md` — few lines for humans/agents skimming:

```markdown
# CV skills — live status
- Updated: …
- Skill / mode: …
- Progress: 10 of 16 — Turn 1: Experience validation
- Awaiting: ev_010
- Next: …
- Pointers: …
```

## User intent (not obligations)

Users steer with plain language. Optional short aliases (see `invocation.md` in cv-creation; same meanings here):

| Intent | Examples |
| :--- | :--- |
| Resume | “continue”, “resume ingest”, `continue` |
| Where are we? | “status”, `status` |
| Inspect | “show matching”, `show …` |
| Open HITL | “probe r_4”, “gate”, `probe` / `gate` |
| Export / env | “export PDF”, `export`, `check-env` |
| Exception | “override ATS because …”, `override-ats` |

Housekeeping (LIVE, memory mirror, validate-after-persist, plain labels, `current of total`) is **never** a user command.
