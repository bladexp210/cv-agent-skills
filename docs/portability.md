# Multi-client portability

Prove that Full / Lite install and a minimal smoke path work on more than one [Agent Skills](https://agentskills.io/home) client. Web chat stays an emulation path (no skill folders).

**Axes (do not conflate):**

| Axis | Meaning |
| :--- | :--- |
| Full / Lite | Install deps aggressiveness (`prompts/install-full.md` vs `install-lite.md`) |
| Standard / Strict | HITL interaction density (`ui.interaction_mode` in career config; skill refs) |
| Web chat | No Agent Skills client — [`web-chat.md`](web-chat.md) |

---

## Client matrix

| Client | Skills path examples | Full / Lite | Notes |
| :--- | :--- | :--- | :--- |
| Cursor | `.cursor/skills/` | Yes | Primary smoke |
| DeepSeek Harness (`dsh`) | Per harness profile / Agent Skills docs (often `.agents/skills/` or a project skills dir); discover via `dsh --profile <name> --dump-config` / product docs. Profiles live under `~/.dsh` or `$DSH_HOME`. CLI examples: `dsh headless "task"`, `dsh tui`, `dsh web` | Yes | Second smoke via `dsh` |
| Other Agent Skills hosts | Per product docs | Prompt-supported | Record when tested |
| Web chat | N/A | Emulation only | [`web-chat.md`](web-chat.md) |

Do **not** hardcode Cursor-only paths in install prompts. Report the client name and the skills path you actually used.

---

## Smoke checklist (copyable)

Use after Full or Lite install from release tag **`v0.6.1+`** (or a named ref). Fill Results below when you run Wave 2 smoke — do not invent pass/fail.

```text
Portability smoke checklist
===========================
Client name: ____________________
Skills path used: _______________
Install path: Full / Lite
Source ref (tag/commit): ________
Date (UTC): ____________________

[ ] 1. Full or Lite install from release tag v0.6.1+ (or named ref)
[ ] 2. Both skills visible/loadable (evidence-bank + cv-creation)
[ ] 3. bootstrap_career (or equivalent) creates career tree
[ ] 4. validate_evidence on fixture or empty bank
[ ] 5. Mini-app validate_application with full G4 argv
[ ] 6. Export md/html
[ ] 7. Note interaction_mode read from career.config.yaml (or “key absent → treat as strict”)

Overall: PASS / FAIL
Notes:
```

Fixture / argv reminders (adjust `<skill-root>` and career root):

```bash
# Evidence fixture
python <skill-root>/evidence-bank/scripts/validate_evidence.py \
  <skill-root>/evidence-bank/assets/fixtures/ok.yaml

# Mini-app G4 validate (from skills pack or installed skill mini-app)
python <skill-root>/cv-creation/scripts/validate_application.py \
  --style <mini>/profile/export-style.yaml \
  --skills <mini>/profile/skills.yaml \
  --composition <mini>/applications/acme-de-2026-01-01/composition.yaml \
  --draft <mini>/applications/acme-de-2026-01-01/draft.md \
  --evidence <mini>/profile/evidence.yaml \
  --matching <mini>/applications/acme-de-2026-01-01/matching.yaml \
  --identity <mini>/profile/identity.yaml

# Export md/html
python <skill-root>/cv-creation/scripts/export_resume.py \
  --formats md,html \
  --career-root <mini> \
  <mini>/applications/acme-de-2026-01-01
```

Install / update prompts: [`prompts/install-full.md`](../prompts/install-full.md), [`prompts/install-lite.md`](../prompts/install-lite.md), [`prompts/update.md`](../prompts/update.md).

---

## Results

### Cursor

| Field | Value |
| :--- | :--- |
| Date (UTC) | 2026-11-19 |
| Pass / fail | **PASS** (script smoke) |
| Skills path | Repo SoT `skills/`; also verified temp install `/tmp/as-career-*/.cursor/skills` |
| Full / Lite | Lite-style (copy skills → bootstrap → validators; not Cursor chat Full HITL) |
| Source ref | `6f60c21` (tag `v0.6.1`) + uncommitted Wave 1 UX/portability tree |
| Checklist | 1 partial (script install, not chat Full) · 2 pass · 3 pass · 4 pass · 5 pass · 6 pass · 7 pass |
| Notes | `pytest -q`: **42 passed, 1 skipped**. `validate_evidence` OK; mini-app `validate_application` full G4 argv OK; `export_resume --formats md,html` OK. `career.config.template.yaml` has `ui.interaction_mode: standard`; `references/interaction-mode.md` present; bootstrapped temp career copied the key. |

### DeepSeek Harness (`dsh`)

| Field | Value |
| :--- | :--- |
| Date (UTC) | 2026-11-19 |
| Pass / fail | **PARTIAL** (Lite headless re-smoke; not Full HITL) |
| Skills path | `<project>/.agents/skills` (real trees) + `<project>/.dsh/skills` (symlinks); catalog listed both |
| Profile / mode | `dsh --profile headless --patch /tmp/as-dsh-openrouter-full.patch.yml` (**`--patch` was used** — OpenRouter `llm-pi-ai` + `agent-default-model`; `DEEPSEEK_API_KEY` unset) |
| Full / Lite | **Lite** headless task (install-lite-shaped): skills pre-staged into temp project; agent confirmed path, bootstrapped, ran validators. **Full install HITL not run.** |
| Source ref | `6f60c21` / tag `v0.6.1` (+ Wave 1 tree); temp project `/tmp/as-dsh-lite-resmoke-229957` |
| Checklist | 1 **partial** (skills pre-copied by operator, not GitHub Lite fetch) · 2 **pass** · 3 **pass** (`bootstrap_career`) · 4 **pass** (`validate_evidence` fixture) · 5 **pass** (mini-app G4 argv) · 6 **pass** (export md/html) · 7 **pass** (`interaction_mode: standard`) |
| Notes | `dsh` **0.2.1-rc.2**. OpenRouter patch smoke succeeded (no `MISSING_CREDENTIAL` / `NO_ADAPTER`). Headless reported client=`DeepSeek Harness / dsh`, ran bootstrap + validators inside the session; parent also re-verified validators independently. **Do not treat as Full PASS** — multi-turn HITL / install-from-GitHub not exercised. |

**dsh blockers**

| Blocker | Detail |
| :--- | :--- |
| Default headless LLM | Stock headless uses `deepseek-official` → `MISSING_CREDENTIAL: … DEEPSEEK_API_KEY` when that env is unset. **Workaround used in re-smoke:** `--patch` with OpenRouter (`OPENROUTER_API_KEY`). |
| OpenRouter on headless | Without `--patch` adding `llm-pi-ai` openrouter provider + `agent-default-model` → `NO_ADAPTER: openrouter`. **Re-smoke applied** `/tmp/as-dsh-openrouter-full.patch.yml` and LLM calls succeeded. |
| Full install HITL | Still not exercised (headless one-shot cannot complete multi-turn HITL). Lite checklist 2–7 passed via headless + scripts; item 1 remains partial. |

### Other (optional)

| Client | Date (UTC) | Pass / fail | Skills path | Notes |
| :--- | :--- | :--- | :--- | :--- |
| — | — | — | — | — |
