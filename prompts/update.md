# Update installed CV Agent Skills

**Who this is for:** You already installed `evidence-bank` and `cv-creation` in a career project and want newer skill code from GitHub.

**How to use:** Copy everything inside the box below. Paste it into a new agent chat in your **career** project.

**Default source:** https://github.com/bladexp210/cv-agent-skills  
**Default ref:** latest GitHub **release tag** (e.g. `v0.2.0`). If no releases exist, use `main`. You may name a tag, branch, or commit instead.

---

## Copy-paste block

```
You are UPDATING already-installed CV Agent Skills in this project (Agent Skills open standard).

## Goal
Replace the installed evidence-bank and cv-creation skill folders with a newer pack from GitHub. Preserve all career data.

## Source (important)
- DEFAULT repo: https://github.com/bladexp210/cv-agent-skills
- DEFAULT ref: latest GitHub release tag. Resolve with `gh release list` / GitHub Releases API, or the Releases page. If there are no releases, use `main`.
- If I named a tag, branch, or commit, use that instead.
- Do NOT use a random local folder (e.g. application-skills) unless I explicitly give that path.
- If you clone/download into a temp dir, you MUST delete it after copy (required cleanup). Never delete my career project, skill install root, or a permanent path I named.

## Hard rules — do not touch
- Do NOT modify, delete, or overwrite: profile/, inbox/, applications/, evidence YAML, identity, voice, norms, or any real career data.
- Do NOT re-run bootstrap_career.py in a way that overwrites filled templates (identity, evidence, voice, etc.). Creating missing empty dirs only is OK if inbox/ is missing.
- Do NOT invent career facts or restart ingest unless I ask.
- Prefer bundled scripts after update for smoke checks.

## Steps (do in order)

### 1) Locate current install
- Report **client name** (Cursor, DeepSeek Harness / `dsh`, or other) and the **skills path** you will update. Do not hardcode Cursor-only paths; `dsh` profiles may use a project skills dir — discover via profile/docs if needed.
- Find where this project’s Agent Skills live (read career.config.yaml `paths.skills_dir` if present; also check `.agents/skills/`, `.cursor/skills/`, and other Agent Skills locations per this client).
- Confirm both folders exist: `<skill-root>/evidence-bank/`, `<skill-root>/cv-creation/`.
- If missing, stop and tell me to run Full or Lite install instead.
- Record current version hint if any (e.g. a VERSION file, or say “unknown / no pin”).

### 2) Resolve target ref
- Default: latest release tag on bladexp210/cv-agent-skills.
- Fallback: `main` if no releases.
- Or the ref I named.
- Report: target ref + commit SHA you will fetch.

### 3) Fetch pack
- Clone/sparse-checkout/download that ref into a temp dir (or use an explicit permanent path I gave).
- Confirm pack has `skills/evidence-bank/` and `skills/cv-creation/`.

### 4) Replace skills only
- Overwrite:
  - pack `skills/evidence-bank/` → `<skill-root>/evidence-bank/`
  - pack `skills/cv-creation/` → `<skill-root>/cv-creation/`
- Keep folder names and SKILL.md intact.
- Do not copy career data out of the pack into this project.

### 5) Cleanup temp fetch (required if temp dir)
- Delete the temp clone/download.
- Confirm path removed, or “n/a permanent path.”

### 6) Align config
- Ensure `career.config.yaml` `paths.skills_dir` matches the skill root you updated (relative path).
- Do not reset other config keys.

### 7) Deps (light touch)
- If `requirements.txt` / PyYAML is needed for smoke and missing, install in the project venv (ask before heavy/global installs).
- Do not force export deps (python-docx, weasyprint) unless I ask or I am about to export.

### 8) Smoke
- Run validate on the fixture:
  `python <skill-root>/evidence-bank/scripts/validate_evidence.py <skill-root>/evidence-bank/assets/fixtures/ok.yaml`
- Report pass/fail.
- Prefer the copyable checklist in pack `docs/portability.md` if you run a fuller smoke after update.

### 9) Hand off
Short bullets:
- Client name + skills path used
- Previous install root
- Ref updated to (tag/branch + commit)
- Temp cleanup (yes/n/a)
- Smoke result
- Career data untouched (confirm)
- Notable skill changes if obvious from commit/release notes (optional, brief)
- Next: continue my workflow (e.g. ingest) — skills are refreshed; reload client skills if needed

Stop unless I ask to continue.
```

---

## Notes for humans

| Topic | Detail |
| :--- | :--- |
| vs Full/Lite | Those are first-time install. Use **Update** when skills already exist. |
| Portability | Agent must report client name + skills path. Checklist: [`docs/portability.md`](../docs/portability.md). |
| Data safety | Update replaces skill code only. Your `inbox/` and `profile/` stay. |
| Pinning | Pass a tag (e.g. `v0.2.0`) in chat to avoid surprise `main` commits. |
| After update | Restart/reload skills in your client if the new instructions do not appear. |
