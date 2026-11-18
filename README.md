# application-skills

Workshop repo for the **CV System** Cursor skills: design decisions + installable skill trees.

Career **data** (identity, evidence YAML, applications) lives in the career project (e.g. `Projects/Career`), not here.

## Read order

1. `AGENTS.md` — agent load order  
2. `COMMUNICATION_CONTRACT.md` — plain labels, progress, recommend+reason  
3. `docs/design/CV-SYSTEM-HANDOFF.md` — settled system design (do not reopen Clusters 1–3 / Q1–Q7)  
4. `docs/design/EVIDENCE-BANK-DECISIONS.md` — evidence-bank locks  
5. `skills/` — skill SoT  
6. `docs/architecture/CV-SYSTEM-ARCHITECTURE.md` — inventory + install/verify (no file-body embeds)

## Layout

```
docs/design/          Active design SoT
docs/architecture/    Thin inventory
docs/archive/         Superseded specs, fat embed, session prompts
skills/               evidence-bank + cv-creation
memory/               Optional MCP continuity (OKF)
```

## Install

```bash
cp -a skills/evidence-bank skills/cv-creation /path/to/your/career-project-folder/.cursor/skills/
```

## Smoke (bank)

```bash
python skills/evidence-bank/scripts/validate_evidence.py \
  skills/evidence-bank/assets/fixtures/ok.yaml
```
