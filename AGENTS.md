# Agents — application-skills

## Load order (every session that touches this repo)

1. `COMMUNICATION_CONTRACT.md`
2. `docs/design/CV-SYSTEM-HANDOFF.md` — only the slices your task needs; do not reopen locked clusters/Q1–Q7
3. `docs/design/EVIDENCE-BANK-DECISIONS.md` — when working on evidence-bank
4. `skills/<skill>/SKILL.md` + referenced files under that skill
5. `docs/architecture/CV-SYSTEM-ARCHITECTURE.md` — inventory / install only

## Install (Agent Skills clients)

Copy `skills/evidence-bank` and `skills/cv-creation` into the client’s skills folder (examples: `.cursor/skills/`, `.agents/skills/`). Do not invent files outside the architecture inventory.

## SoT rules

| Kind | Path |
|---|---|
| Skill code | `skills/` only |
| Design locks | `docs/design/` |
| Historical | `docs/archive/` (read-only unless resurrecting) |
| Career data | External career project — not this repo |

## Do not

- Edit `docs/archive/CV-SYSTEM-ARCHITECTURE-v1.0-full-embed.md` as live SoT  
- Duplicate skill trees under `career/` or `architecture-v1.0/`  
- Invent files outside the architecture inventory  

## Communication

Plain `Turn N: <name>` labels; show `current of total` on queues; options to the operator include recommendation + reasoning.
