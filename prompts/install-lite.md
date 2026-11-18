# Install (lite) — copy and paste

Use this when you want the **Agent Skills** folders installed, but you do **not** want the agent to install Python packages unless you say yes.

**How to use:** Copy everything inside the box below. Paste it into a new chat in your **career** project. You do not need the skills repo open in the workspace.

**Default source:** public GitHub repo  
`https://github.com/bladexp210/cv-agent-skills`

---

```text
You are installing CV Agent Skills in LITE mode.

Source of skill files (important)
- DEFAULT: get skills from the public GitHub repo https://github.com/bladexp210/cv-agent-skills
  (clone, sparse checkout, or download — your choice; prefer a fresh clone into a temp dir if needed).
- Do NOT use a random local folder such as application-skills, or any sibling project, unless I explicitly give you that path.
- If both a local checkout and GitHub are available, still prefer GitHub unless I say otherwise.
- Temporary fetch only: if you clone/download into a temp dir to obtain the pack, you MUST delete that temp dir after skills are copied (required cleanup). Do not delete a path I explicitly named as my permanent local checkout.

Goals
1. Install the skills only: evidence-bank and cv-creation.
2. Do not install Python packages or other dependencies unless I agree first.
3. Tell me what works strongly and what is weak. I decide next steps.

How to install skills
- Use your own product docs for where Agent Skills live on this client.
- Do not hardcode one vendor path.
- Obtain the pack from GitHub (default) or from an explicit local path I gave you.
- Copy or link both skill trees from the pack’s skills/ folder into the correct skills location for this client.
- If you used a temporary clone/download dir, delete it now (required). Confirm path removed, or state “no temp dir — used explicit permanent path.” Never delete my career project, skill install target, or a permanent path I gave you.
- Confirm both skills load (or say clearly if one did not).
- Report the source you used (GitHub URL + ref/commit if known, or the explicit local path).

Dependencies policy (lite)
- Do not run pip, apt, brew, or similar to add packages unless I explicitly agree.
- Prefer bundled skill scripts when they already run on this machine.
- If a script fails for a missing dependency, stop. Report the gap. Ask me before installing anything.

Inventory (check and report)
Check these partial cases and say pass / fail / unknown for each:
- Python available?
- PyYAML available? (needed for YAML validation scripts)
- Native PDF export available in this agent/client?
- Native DOCX export available in this agent/client?

Report format
Give me a short table or list:
- Source used
- Strong: what already works without new installs
- Weak: what is missing or unreliable
- Recommendation: what you suggest I do next (and why)
Then wait for my decision.

Adaptation
- Where scripts cannot run, adapt with agent tools you already have: rules, skills, hooks, native export, or manual steps.
- Say clearly that output quality tracks this agent’s capability when we skip scripted validation or export.
- Do not invent career facts. Career data stays in this project; use fixtures from the skills pack only for smoke checks.

Smoke (optional, no new installs)
- If validate_evidence.py already runs with the fixture under the installed evidence-bank assets/fixtures/, run that smoke and report the result.
- If it does not run, say so. Do not install PyYAML unless I agree.

Bootstrap the career project (you do this — do not ask me to DIY)
- After skills are in place, run bootstrap yourself (no new pip installs):
  `python <skill-root>/cv-creation/scripts/bootstrap_career.py .`
- If Python/script fails, create the layout yourself: `profile/`, `applications/`, `_skill_state/`, `inbox/resumes/`, `inbox/linkedin/`, `inbox/from-links/`, and copy `inbox/README.md` from the skill assets when available.
- If the tree already exists, still ensure `inbox/` and subfolders exist.
- After bootstrap, set `paths.skills_dir` in `career.config.yaml` to the skill root you actually used (relative path, e.g. `.agents/skills` or `.cursor/skills`). Do not leave a mismatched default.
- Tell me briefly what you created. Do not stop at “you should create folders.”

When you finish
1. Confirm both skills are installed (or what failed) and the source used.
2. Confirm temp fetch cleaned up (yes + path / n/a permanent path).
3. Confirm career bootstrap / inbox paths.
4. Show the strong vs weak inventory.
5. Tell me where to drop CV / LinkedIn / URL saves (`inbox/resumes/`, `inbox/linkedin/`, `inbox/from-links/`).
6. Ask me whether to install any missing deps, stay lite, ingest from inbox, or adapt another way — offer to do the next step yourself when I agree.
```
