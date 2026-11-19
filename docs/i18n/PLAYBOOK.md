# User-locale playbook (CV Agent Skills)

## Purpose

Ship install/use documentation and HITL *display* strings in user languages.
English remains source of truth for skills logic, schemas, validators, and machine decision tokens.

## Audiences

| Audience | Reads | Language |
| :--- | :--- | :--- |
| Installer / everyday user | docs/user/\<lang\>/, prompts/\<lang\>/ | fr, ar, … |
| Operator using skills in chat | HITL envelopes from locales/\<lang\>.yaml | ui.locale |
| Developer / agent maintainer | README, docs/design, docs/architecture, AGENTS | English |

## Principles

These bind **user docs** and **HITL display strings** (not developer ADRs).

1. **Audience first** — Write for someone installing and using skills, not for contributors reading design locks.
2. **Approachability** — One job per page; start with what to do next; hide developer paths behind one clear “for maintainers” link.
3. **Clarity** — Lead with what / where / next; short sentences; active voice; “you” + imperatives in procedures.
4. **Decode once** — Jargon (`Agent Skills`, `evidence-bank`, `Turn`) defined on first use per page; then reuse the locked glossary term (no synonym drift).
5. **Plain labels** — Never bare `T0`/`T1` alone; always `Turn N: <localized plain name>`.
6. **Progress visible** — When a total exists, show `current of total` (localized numeral phrasing OK; meaning identical).
7. **Recommend + reason** — Path choices include a recommendation and short why.
8. **Adult-Grice** — No lecturing, no fluff, no false reassurance; refusals/gaps in one plain sentence + closest next step.
9. **Fidelity over paraphrase** — Locales must preserve facts, safety warnings, and decision meaning; do not “simplify away” privacy or validate steps.
10. **Script / path literals** — Keep commands, filenames, and repo paths in the original form; translate surrounding prose only.
11. **RTL honesty (AR)** — Arabic pages note right-to-left reading; do not break fenced code; tables stay usable.
12. **English SoT** — If EN and locale disagree, EN wins until the locale is updated; never “fix” EN from a locale without an explicit maintainer decision.

## Corpus (Scope B)

### Docs + prompts (per language)

- README equivalent: `docs/user/<lang>/README.md`
- `docs/user/<lang>/quick-start.md`
- `docs/user/<lang>/web-chat.md`
- `docs/user/<lang>/privacy-security.md` (short user slice from `SECURITY.md`; link full EN `SECURITY.md`)
- `prompts/<lang>/install-full.md`
- `prompts/<lang>/install-lite.md`
- `prompts/<lang>/update.md`

### Out of corpus (stay English)

- `docs/design/*`, `docs/architecture/*`, `docs/portability*.md`, `AGENTS.md`,
  `COMMUNICATION_CONTRACT.md` (amend only the Language table),
  skill `SKILL.md` logic bodies, scripts, tests, Makefile.

### HITL display packs

- `skills/evidence-bank/references/locales/<lang>.yaml`
- `skills/cv-creation/references/locales/<lang>.yaml`
  (shared turn keys MUST be byte-identical across both skills)

## Glossary

Maintain `docs/i18n/glossary.yaml`:

- `id`, `en`, `fr`, `ar`, `notes`
- Critical ids: `agent_skills`, `evidence_bank`, `cv_creation`, turn_N_names,
  decision tokens (en machine form never changes).

## How to add or refresh a language

1. Copy `docs/user/_template/` and `prompts/_template/` → `<lang>/`
2. Translate using glossary; keep fences/paths/commands literal.
3. Author `locales/<lang>.yaml` (both skills); run shared-key identity check.
4. Add language switcher links on EN README and `docs/user/<lang>/README.md`.
5. Run fail-tests (below). Fix until green.
6. Update `docs/i18n/STATUS.md` (locale, EN commit pin, date, owner).

## ui.locale

`career.config.yaml` → `ui.locale: en|fr|ar` (missing ⇒ `en`).
Agents load matching locale pack for HITL headers/options.
User replies may use localized label OR English machine token OR option number.

## Sync rule

When an EN corpus file changes, bump `docs/i18n/STATUS.md` `en_pin` and mark
each locale stale until re-checked. Do not release a locale as “current”
while stale.

## Fail tests

See [`fail-tests.md`](fail-tests.md). Automated S1–S4 live under `tests/test_i18n_locale_packs.py`.
