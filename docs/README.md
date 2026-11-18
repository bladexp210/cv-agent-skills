# Docs map

For forkers and agents who need how this repo thinks — not end-user install (see root README and `prompts/`).

| Path | Role |
| :--- | :--- |
| [`design/`](design/) | Locked design decisions. Read slices you need; do not reopen settled clusters / Q1–Q7. |
| [`architecture/`](architecture/) | Live inventory + install/verify. Skill bodies live under `skills/`, not embedded here. |
| [`archive/`](archive/) | Historical snapshots. Read-only unless resurrecting. |
| [`../COMMUNICATION_CONTRACT.md`](../COMMUNICATION_CONTRACT.md) | Project language: turn labels, glossary, HITL rules. |
| [`../AGENTS.md`](../AGENTS.md) | Load order and source-of-truth rules for every session. |

**Install target (Agent Skills clients):** copy `skills/evidence-bank` and `skills/cv-creation` into the client’s skills folder (examples: `.cursor/skills/`, `.agents/skills/`). Career data stays outside this repo.
