# Portability smoke — DeepSeek Harness (`dsh`) web mode

| Field | Value |
| :--- | :--- |
| Date (UTC) | 2026-11-19 |
| Client / mode | **DeepSeek Harness (`dsh`) — web mode** |
| `dsh` version | `0.2.1-rc.2` (Node `v26.12.1`) |
| Profile | `web` (`DSH_PROFILE=web`, `DSH_PROFILE_DIR=/home/mohamed/.dsh/profiles/web`) |
| Session | `session-6e617bbb-073c-4697-82b4-bf1d846c5889`, `DSH_WEB_URL=http://127.0.0.1:3080` |
| Source ref | tag **`v0.8.0`** (`git describe --tags` → `v0.8.0`; HEAD `3cf88ce`) |
| Temp career path used | `/tmp/as-dsh-web-smoke-259142` → **confirmed deleted** |
| Skills path used | `/tmp/as-dsh-web-smoke-259142/career-project/.agents/skills/{evidence-bank,cv-creation}` |
| Overall verdict | **PASS** (items 2–7); item 1 **partial** by design (local-checkout copy, not a GitHub fetch) |

## What this smoke actually was

A **Lite-shaped, script-level** smoke driven from the `web`-profile session's shell: install the two
skills by copying them into a disposable career project's `.agents/skills`, then exercise the skills'
own bootstrap and validator/export entry points with the system Python. It additionally exercised the
harness's **own** skill-discovery code (`FileSystemSkillProvider` from `@deepseek-ai/dsh-skill-filesystem`
`0.2.1-rc.2`) against the temp project root, so item 2 is product-verified rather than assumed.

It was **not** a Full-install HITL chat run, and the GUI agent's model did not itself invoke the skills
(see *Not exercised*).

## Skills install path — how it was determined

Not hardcoded. The resolved roots come from `@deepseek-ai/dsh-skill-filesystem` `lib/index.js`
(`async roots(cwd)`) and are confirmed by live output in this session:

| Rank | Source | Path (as resolved here) |
| ---: | :--- | :--- |
| 100 | `project-dsh` | `<project>/.dsh/skills` |
| 200 | `project-agents` | `<project>/.agents/skills` ← **install target used** |
| 400 | `user-dsh` | `/home/mohamed/.dsh/skills` (absent) |
| 500 | `user-agents` | `/home/mohamed/.agents/skills` (absent) |

`projectRoot` is the nearest ancestor containing `.git`, else the cwd. The temp career project was
therefore `git init`-ed so the walk stops there — **not** at the skills repo — and dsh resolves
`projectRoot=/tmp/as-dsh-web-smoke-259142/career-project`.

Web mode mounts `skill-filesystem` **per agent via presets**, not on the host plane:
`@deepseek-ai/dsh-web-app/cordis.patch.yml` disables the base host rows `skill-filesystem` and
`tool-skill`, and `dsh-web-app/presets/cordis.patch.yml` re-adds them per agent with
`customSkillDirs: [<dsh-agent-preset>/skills]`. That preset-level config sets **no**
`includeDefaultRoots: false`, so the default project/user roots above stay on — which is why the
`.agents/skills` target is legitimate in web mode and not only in headless.

## Checklist

| # | Item | Result | Evidence |
| :-: | :--- | :--- | :--- |
| 1 | Lite-shaped install into temp career skills path | **partial** | Copied `skills/evidence-bank` (15 files) and `skills/cv-creation` (69 files) from **this checkout** → `<temp>/.agents/skills/`, `__pycache__` stripped; no `pip install`. Source was the local tree, not a GitHub fetch → partial by the checklist's own definition. |
| 2 | Both skills visible/loadable | **pass** | Ran the harness's `FileSystemSkillProvider.list({cwd: <temp career>})`: `catalogued=2`, `warnings=[]` — `cv-creation` and `evidence-bank`, both `source=project-agents`, `rank=200`, `modelInvocable=true`. |
| 3 | `bootstrap_career` creates career tree inside temp dir only | **pass** | `python3 <installed>/cv-creation/scripts/bootstrap_career.py .` → "Bootstrapped career root: /tmp/as-dsh-web-smoke-259142/career-project", exit 0. Tree created: `profile/{evidence,export-style,identity,skills}.yaml`, `profile/{norms,voice.md}`, `applications/`, `inbox/{resumes,linkedin,from-links}`, `_skill_state/`, `career.config.yaml`, `.gitignore`. No career data created in the repo. |
| 4 | `validate_evidence` on `assets/fixtures/ok.yaml` | **pass** | `python3 <installed>/evidence-bank/scripts/validate_evidence.py <installed>/assets/fixtures/ok.yaml` → `OK`, exit 0. Negative control `bad-missing-source.yaml` → `ERROR: ev_bad_001: missing source`, exit 1 (validator discriminates). |
| 5 | Mini-app `validate_application` with **full G4 argv** | **pass** | All seven flags passed (`--style --skills --composition --draft --evidence --matching --identity`) against the mini-app copied to `/tmp` → `OK`, exit 0. Negative control `grounding-bad/cited-not-listed/composition.yaml` → `ERROR: b_cite_gap`, exit 1 (G4 enforcement live). |
| 6 | `export_resume --formats md,html` | **pass** | `python3 <installed>/cv-creation/scripts/export_resume.py --formats md,html --career-root <mini> <mini>/applications/acme-de-2026-01-01` → "Wrote 2 format(s) …", exit 0; `resume.md` (200 B) and `resume.html` (549 B) + `export_manifest.yaml` freshly rewritten. Ran on a `/tmp` copy — repo fixtures untouched. |
| 7 | `ui.interaction_mode` from bootstrapped `career.config.yaml` | **pass** | `career.config.yaml:8` → `interaction_mode: standard   # standard \| strict — missing key ⇒ treat as strict` (also `chat_host: gui`). Key present ⇒ **standard**, not strict. |

## Web-mode notes

- **No `--patch` needed in web mode.** Unlike headless (whose
  `/home/mohamed/.dsh/profiles/headless/cordis.patch.yml` is `[]`, which is what produced the earlier
  `MISSING_CREDENTIAL` / `NO_ADAPTER: openrouter` blockers), the `web` profile's
  `cordis.patch.yml` already wires `llm-pi-ai` plus `agent-default-model`
  (`provider: openrouter`, `model: ~deepseek/deepseek-flash-latest`). So neither blocker was
  reproduced in web mode — this run required no patch file and no API quirk workaround.
- **`dsh --profile web --dump-config` could not be used** to introspect the config: it fails with
  `EROFS: read-only file system, open '/home/mohamed/.dsh/profiles/web/cordis.yml'` because
  `~/.dsh` is read-only in this sandbox. That is an **environment limitation, not a product bug** —
  the profile YAML and plugin sources were read directly instead. Anything that makes dsh rewrite
  profile files would hit the same wall here.
- Web mode also has **no CLI subcommand that prints the skill catalog** (`dsh --profile web --help`
  offers only `--host/--port/--public-url/...`), which is why item 2 was verified by driving the
  discovery provider directly rather than by a listing command.
- Skills attach to the **cwd-sensitive** workspace root, so in the GUI the pack is only visible for
  sessions opened in a workspace whose `projectRoot` contains `.agents/skills`. The web default
  first-use workspace is `~/Documents/deepseek-harness-default-workspace` (from
  `dsh-api-workspace-controller`'s `xdg-user-dir DOCUMENTS` resolution), **not** this repo — an
  operator installing at user scope should use `~/.agents/skills` or `~/.dsh/skills` instead.

## Not exercised (do not read as covered)

- **Live GUI skill invocation** — the GUI agent's model was not asked to select and run
  `evidence-bank`/`cv-creation` in this smoke.
- **Full-install HITL** multi-turn interview flow.
- **API-key/LLM path** — no model call was needed; everything above is deterministic script +
  provider behavior.
- **`compare` of a real career project** — only the shipped mini-app fixture was used, on a `/tmp`
  copy.

## Cleanup confirmation

`/tmp/as-dsh-web-smoke-259142` (1016 K, containing the temp career project, the installed skills, and
the mini-app copy) plus the three helper `.mjs` probes were deleted. Verified afterwards: each path
reports `gone:`, and `ls -d /tmp/as-dsh*` → `none`. The skills repo was never a deletion target; after
the smoke, `git status --porcelain` in the repo was clean and no `profile/`, `applications/`,
`_skill_state/`, `career/`, `.agents/` or `.dsh/` had been created at the repo root.

## Verdict

**PASS** — checklist items 2–7 all passed on real runs with negative controls proving the validators
and grounding checks are not rubber stamps; item 1 stays **partial** because the skills came from this
local checkout rather than a GitHub fetch. Temp career and all scratch artifacts are confirmed deleted.
