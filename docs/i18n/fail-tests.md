# User-locale fail tests

Gate for shipping or refreshing a user language (FR, AR, …).
A PR that claims a locale is `current` in [`STATUS.md`](STATUS.md) must pass these.

Automated: `tests/test_i18n_locale_packs.py` covers **S1–S4**.
**P\*** and **H\*** stay human checklist until a later automation pass.

---

## A. Principle / approachability tests (checklist + spot script)

| ID | Fail if |
| :--- | :--- |
| P1 | User README does not lead with what this is + next action in first screenful |
| P2 | Page uses bare `T0`–`T8` / `G4` without a plain localized label |
| P3 | Path-choice table lacks recommendation + short reason |
| P4 | Critical term uses a synonym not in `glossary.yaml` for that lang |
| P5 | Safety/privacy warning dropped or softened vs EN |
| P6 | Code fence / path / command was translated or “helpfully” altered |
| P7 | AR page has no RTL note and mirrors EN column order in a way that confuses reading |
| P8 | Page tells user to edit `docs/design` or invent folder layout |

---

## B. Structural / sync tests (automatable)

| ID | Fail if |
| :--- | :--- |
| S1 | Locale tree missing any corpus path listed in playbook |
| S2 | Broken relative links inside `docs/user/<lang>/` or `prompts/<lang>/` |
| S3 | `locales/fr.yaml` (or ar) differs between evidence-bank and cv-creation on shared keys |
| S4 | Locale YAML missing a required turn/decision key present in `locales/en.yaml` |
| S5 | `STATUS.md` marks locale `current` while `en_pin` ≠ current EN corpus hash/commit |
| S6 | Architecture inventory missing new paths |

S1–S4: run `pytest -q tests/test_i18n_locale_packs.py`.
S5–S6: checklist (and inventory review) until automated.

### S1 scope (foundation nuance)

- Always require a complete corpus under `docs/user/_template/` and `prompts/_template/`.
- For each language marked `current` in `STATUS.md`, require the full corpus under `docs/user/<lang>/` and `prompts/<lang>/`.
- Skeleton dirs (`.gitkeep` only) with status `stale` / `pending` do not fail S1.

---

## C. HITL behavior tests

| ID | Fail if |
| :--- | :--- |
| H1 | Skill docs claim machine tokens change by locale |
| H2 | Worked example in locale pack shows bare turn codes |
| H3 | Acceptance rule omits “English token still valid” |

---

## How to run

```bash
# from repo root
pytest -q tests/test_i18n_locale_packs.py
# or full suite
make test
```

Before marking a locale `current` in `STATUS.md`, also walk P1–P8 and H1–H3 on that language’s pages and HITL packs.
