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
- After install, you may delete any temporary clone.

Goals
1. Install the skills only: evidence-bank and cv-creation.
2. Do not install Python packages or other dependencies unless I agree first.
3. Tell me what works strongly and what is weak. I decide next steps.

How to install skills
- Use your own product docs for where Agent Skills live on this client.
- Do not hardcode one vendor path.
- Obtain the pack from GitHub (default) or from an explicit local path I gave you.
- Copy or link both skill trees from the pack’s skills/ folder into the correct skills location for this client.
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

When you finish
1. Confirm both skills are installed (or what failed) and the source used.
2. Show the strong vs weak inventory.
3. Ask me whether to install any missing deps, stay lite, or adapt another way.
```
