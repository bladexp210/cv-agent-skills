# User-locale status

English install/use docs at repo root (`README.md`, `docs/quick-start.md`, `docs/web-chat.md`, `SECURITY.md`, `prompts/*.md`) remain SoT until a locale is marked `current`.

| Locale | Status | EN pin | Checked | Owner | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `en` | SoT (pin) | `b91cc6bb92073367e43c77253b6f64f62cad1813` | 2026-11-19 | foundation | Canonical EN corpus + `locales/en.yaml` |
| `fr` | current | `b91cc6bb92073367e43c77253b6f64f62cad1813` | 2026-11-19 | french | Full corpus + `fr.yaml` HITL packs; S1–S4 green |
| `ar` | current | `b91cc6bb92073367e43c77253b6f64f62cad1813` | 2026-11-19 | arabic | Full corpus + `ar.yaml` HITL packs; RTL notes; S1–S4 green |

## Sync rule

When any EN corpus file or `locales/en.yaml` changes:

1. Update `en` row `EN pin` to the commit (or content hash) that owns the change.
2. Set every non-EN locale to `stale` until re-checked.
3. Do not mark a locale `current` while stale.

## Glossary

`docs/i18n/glossary.yaml` — FR and AR columns filled for critical terms (foundation).
